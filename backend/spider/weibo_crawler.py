import requests
import re
import json
from datetime import datetime
from urllib.parse import quote
from bs4 import BeautifulSoup


class WeiboCrawler:
    """微博爬虫"""
    
    # 微博API基础URL
    BASE_URL = 'https://weibo.com'
    API_URL = 'https://weibo.com/ajax'
    
    def __init__(self, cookie=None):
        """
        初始化爬虫
        
        Args:
            cookie: 微博登录Cookie字符串
        """
        self.cookie = cookie
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://weibo.com/'
        }
        
        if cookie:
            self.set_cookie(cookie)
    
    def set_cookie(self, cookie):
        """
        设置Cookie
        
        Args:
            cookie: Cookie字符串
        """
        self.cookie = cookie
        self.session.headers.update({'Cookie': cookie})
    
    def get_user_info(self, nickname):
        """
        根据昵称搜索用户信息
        使用微博搜索API查找用户

        Args:
            nickname: 用户昵称

        Returns:
            dict: 用户信息，包含 uid, nickname, avatar, description
        """
        try:
            print(f"[DEBUG] 搜索用户: {nickname}")
            print(f"[DEBUG] Cookie是否存在: {bool(self.cookie)}")

            # 方法1: 使用微博搜索API (需要Cookie)
            print(f"[DEBUG] 尝试方法1: 使用微博搜索API")
            search_url = 'https://weibo.com/ajax/search/finder'
            params = {
                'search': nickname,
                'type': 'user',
                'page': 1
            }

            response = self.session.get(search_url, headers=self.headers, params=params, timeout=30)
            print(f"[DEBUG] 搜索API响应状态码: {response.status_code}")

            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"[DEBUG] 搜索API响应: {data}")

                    if data.get('ok') == 1:
                        users = data.get('data', {}).get('users', [])
                        print(f"[DEBUG] 找到 {len(users)} 个用户")

                        for user in users:
                            screen_name = user.get('screen_name', '')
                            print(f"[DEBUG] 检查用户: {screen_name}")
                            if screen_name == nickname:
                                uid = str(user.get('id'))
                                print(f"[DEBUG] 找到匹配用户，UID: {uid}")

                                return {
                                    'uid': uid,
                                    'nickname': user.get('screen_name'),
                                    'avatar': user.get('avatar_large', ''),
                                    'description': user.get('description', ''),
                                    'profile_url': f"https://weibo.com/u/{uid}"
                                }
                except Exception as e:
                    print(f"[DEBUG] 解析搜索API响应失败: {e}")

            # 方法2: 使用新版微博搜索API
            print(f"[DEBUG] 尝试方法2: 使用新版搜索API")
            search_url2 = 'https://weibo.com/ajax/side/search'
            params2 = {
                'q': nickname,
                'type': 'user',
                'page': 1
            }

            response2 = self.session.get(search_url2, headers=self.headers, params=params2, timeout=30)
            print(f"[DEBUG] 新版搜索API响应状态码: {response2.status_code}")

            if response2.status_code == 200:
                try:
                    data2 = response2.json()
                    print(f"[DEBUG] 新版搜索API响应: {data2}")

                    if data2.get('ok') == 1:
                        # 尝试从 'users' 数组获取
                        users = data2.get('data', {}).get('users', [])
                        print(f"[DEBUG] 从 'users' 找到 {len(users)} 个用户")

                        for user in users:
                            screen_name = user.get('screen_name', '')
                            print(f"[DEBUG] 检查用户: {screen_name}")
                            if screen_name == nickname:
                                uid = str(user.get('id'))
                                print(f"[DEBUG] 找到匹配用户，UID: {uid}")

                                return {
                                    'uid': uid,
                                    'nickname': user.get('screen_name'),
                                    'avatar': user.get('profile_image_url', ''),
                                    'description': user.get('description', ''),
                                    'profile_url': f"https://weibo.com/u/{uid}"
                                }

                        # 尝试从 'user' 数组获取
                        user_list = data2.get('data', {}).get('user', [])
                        print(f"[DEBUG] 从 'user' 找到 {len(user_list)} 个用户")

                        for user_info in user_list:
                            screen_name = user_info.get('nick', '')
                            print(f"[DEBUG] 检查用户: {screen_name}")
                            if screen_name == nickname:
                                uid = str(user_info.get('uid'))
                                print(f"[DEBUG] 找到匹配用户，UID: {uid}")

                                # 获取详细信息
                                detail = self._get_user_detail(uid)
                                if detail:
                                    return detail
                                else:
                                    return {
                                        'uid': uid,
                                        'nickname': screen_name,
                                        'avatar': '',
                                        'description': '',
                                        'profile_url': f"https://weibo.com/u/{uid}"
                                    }
                except Exception as e:
                    print(f"[DEBUG] 解析新版搜索API响应失败: {e}")

            # 方法3: 尝试从用户主页获取（如果Cookie有效）
            print(f"[DEBUG] 尝试方法3: 从用户主页获取")
            profile_url = f'https://weibo.com/n/{nickname}'
            response3 = self.session.get(profile_url, headers=self.headers, allow_redirects=True, timeout=30)

            print(f"[DEBUG] 用户主页响应状态码: {response3.status_code}")
            print(f"[DEBUG] 最终URL: {response3.url}")

            if response3.status_code == 200:
                import re
                # 从URL中提取UID
                uid_match = re.search(r'/u/(\d+)', response3.url)
                if uid_match:
                    uid = uid_match.group(1)
                    print(f"[DEBUG] 从URL提取到UID: {uid}")

                    # 获取用户详细信息
                    user_info = self._get_user_detail(uid)
                    if user_info:
                        return user_info
                    else:
                        return {
                            'uid': uid,
                            'nickname': nickname,
                            'avatar': '',
                            'description': '',
                            'profile_url': f"https://weibo.com/u/{uid}"
                        }

                # 从页面HTML中提取
                html = response3.text
                uid_patterns = [
                    r'\$CONFIG\[\'oid\'\]=\'(\d+)\'',
                    r'\$CONFIG\[\'uid\'\]=\'(\d+)\'',
                    r'uid[:\s]*["\']?(\d+)["\']?',
                    r'userId[:\s]*["\']?(\d+)["\']?',
                ]

                for pattern in uid_patterns:
                    match = re.search(pattern, html)
                    if match:
                        uid = match.group(1)
                        print(f"[DEBUG] 从HTML提取到UID: {uid}")

                        # 获取用户详细信息
                        user_info = self._get_user_detail(uid)
                        if user_info:
                            return user_info
                        else:
                            return {
                                'uid': uid,
                                'nickname': nickname,
                                'avatar': '',
                                'description': '',
                                'profile_url': f"https://weibo.com/u/{uid}"
                            }

            print(f"[DEBUG] 未找到匹配的用户: {nickname}")
            return None

        except Exception as e:
            print(f"获取用户信息失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

    def _get_user_detail(self, uid):
        """
        获取用户详细信息

        Args:
            uid: 用户ID

        Returns:
            dict: 用户信息
        """
        try:
            # 使用用户资料API获取详细信息
            profile_url = f'{self.API_URL}/profile/info'
            params = {
                'uid': uid
            }

            response = self.session.get(profile_url, headers=self.headers, params=params, timeout=30)
            print(f"[DEBUG] 用户详情API响应状态码: {response.status_code}")

            if response.status_code == 200:
                data = response.json()

                if data.get('ok') == 1:
                    user_data = data.get('data', {})
                    user_info = user_data.get('user', {})

                    if user_info:
                        return {
                            'uid': str(user_info.get('id')),
                            'nickname': user_info.get('screen_name'),
                            'avatar': user_info.get('avatar_large', ''),
                            'description': user_info.get('description', ''),
                            'profile_url': f"https://weibo.com/u/{user_info.get('id')}"
                        }

            return None

        except Exception as e:
            print(f"获取用户详情失败: {str(e)}")
            return None
    
    def get_user_weibo_list(self, uid, page=1, count=20):
        """
        获取用户微博列表
        
        Args:
            uid: 用户ID
            page: 页码
            count: 每页数量
            
        Returns:
            list: 微博列表
        """
        try:
            # 使用微博API获取用户微博列表
            url = f'{self.API_URL}/statuses/mymblog'
            params = {
                'uid': uid,
                'page': page,
                'feature': 0  # 全部微博
            }
            
            print(f"[DEBUG] 获取微博列表 - UID: {uid}, URL: {url}")
            response = self.session.get(url, headers=self.headers, params=params, timeout=30)
            
            print(f"[DEBUG] 微博列表响应状态码: {response.status_code}")
            
            if response.status_code != 200:
                print(f"获取微博列表失败: HTTP {response.status_code}")
                return []
            
            data = response.json()
            
            if data.get('ok') != 1:
                print(f"获取微博列表失败: {data.get('msg', '未知错误')}")
                return []
            
            weibo_list = []
            
            # 从list中提取微博数据
            statuses = data.get('data', {}).get('list', [])
            print(f"[DEBUG] 获取到 {len(statuses)} 条微博")
            
            for status in statuses[:count]:
                weibo_info = self._parse_weibo_item(status)
                if weibo_info:
                    weibo_list.append(weibo_info)
            
            return weibo_list
            
        except Exception as e:
            print(f"获取微博列表失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_latest_weibo(self, uid, keyword=None):
        """
        获取用户最新一条微博
        
        Args:
            uid: 用户ID
            keyword: 关键词过滤(可选)
            
        Returns:
            dict: 最新微博信息
        """
        weibo_list = self.get_user_weibo_list(uid, page=1, count=5)
        
        if not weibo_list:
            return None
        
        # 如果有关键词，查找包含关键词的最新微博
        if keyword:
            for weibo in weibo_list:
                if keyword in weibo.get('content', ''):
                    return weibo
            return None
        
        return weibo_list[0]

    def get_weibo_by_time_range(self, uid, start_time, end_time, keyword=None):
        """
        获取用户指定时间范围内的微博
        
        Args:
            uid: 用户ID
            start_time: 开始时间，格式：YYYY-MM-DD HH:MM:SS
            end_time: 结束时间，格式：YYYY-MM-DD HH:MM:SS
            keyword: 关键词过滤(可选)
            
        Returns:
            list: 微博列表
        """
        from datetime import datetime
        
        # 解析时间范围
        try:
            start_dt = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
            end_dt = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print(f"[ERROR] 时间格式错误: {str(e)}")
            return []
        
        print(f"[DEBUG] 获取时间段微博 - UID: {uid}, 时间范围: {start_time} 到 {end_time}")
        
        # 获取多页微博数据
        all_weibo = []
        found_in_range = False  # 标记是否已在时间范围内找到微博
        
        for page in range(1, 11):  # 最多获取10页(200条)，确保能覆盖到较早时间的微博
            weibo_list = self.get_user_weibo_list(uid, page=page, count=20)
            if not weibo_list:
                break
            
            # 检查这一页是否有在时间范围内的微博
            page_has_in_range = False
            for weibo in weibo_list:
                publish_time = weibo.get('publish_time')
                if publish_time and isinstance(publish_time, datetime):
                    if start_dt <= publish_time <= end_dt:
                        page_has_in_range = True
                        found_in_range = True
                        break
            
            all_weibo.extend(weibo_list)
            
            # 智能停止逻辑：
            # 注意：API返回的数据可能有置顶微博，不按时间排序，需要基于所有数据的整体时间范围判断
            # 1. 如果当前页有在时间范围内的微博，继续获取下一页（可能还有更多）
            # 2. 如果已经找到过时间范围内的微博，且当前页所有微博都早于开始时间，停止
            # 3. 计算当前已获取的所有微博的最早时间，如果早于开始时间且没找到目标，继续获取
            
            # 获取当前页所有微博的时间
            page_times = [w.get('publish_time') for w in weibo_list if w.get('publish_time') and isinstance(w.get('publish_time'), datetime)]
            
            if page_times:
                page_oldest = min(page_times)  # 当前页最早的微博时间
                page_newest = max(page_times)  # 当前页最新的微博时间
                
                # 情况1：已经找到过目标微博，且当前页最早的也早于开始时间，可以停止了
                if found_in_range and page_oldest < start_dt:
                    print(f"[DEBUG] 已找到目标日期微博，且当前页最早时间({page_oldest})早于开始时间，停止翻页")
                    break
                
                # 情况2：当前页所有微博都早于开始时间，且没有置顶微博干扰（最新也早于开始时间）
                if page_newest < start_dt:
                    print(f"[DEBUG] 当前页所有微博时间({page_newest} ~ {page_oldest})都早于开始时间，停止翻页")
                    break
        
        # 过滤时间范围内的微博
        filtered_weibo = []
        for weibo in all_weibo:
            publish_time = weibo.get('publish_time')
            if not publish_time or not isinstance(publish_time, datetime):
                continue
            
            # 检查是否在时间范围内
            if start_dt <= publish_time <= end_dt:
                # 如果有关键词，检查是否包含
                if keyword:
                    if keyword in weibo.get('content', ''):
                        filtered_weibo.append(weibo)
                else:
                    filtered_weibo.append(weibo)
        
        # 按发布时间排序，最新的在前
        filtered_weibo.sort(key=lambda x: x.get('publish_time', datetime.min), reverse=True)
        
        print(f"[DEBUG] 找到 {len(filtered_weibo)} 条符合条件的微博")
        return filtered_weibo
    
    def _parse_weibo_item(self, status):
        """
        解析微博数据
        
        Args:
            status: 微博原始数据
            
        Returns:
            dict: 解析后的微博信息
        """
        try:
            # 获取微博ID
            weibo_id = str(status.get('id'))
            
            # 获取微博内容
            text = status.get('text', '')
            # 去除HTML标签
            content = self._clean_html(text)
            
            # 获取发布时间
            created_at = status.get('created_at')
            publish_time = self._parse_time(created_at)
            
            # 获取互动数据
            reposts = status.get('reposts_count', 0)
            comments = status.get('comments_count', 0)
            attitudes = status.get('attitudes_count', 0)
            
            # 获取图片 - 微博API使用pic_ids存储图片ID
            pic_urls = []
            pic_ids = status.get('pic_ids', [])
            if pic_ids:
                # 根据pic_id构建图片URL
                for pic_id in pic_ids:
                    # 微博图片URL格式: https://wx1.sinaimg.cn/large/{pic_id}.jpg
                    pic_url = f"https://wx1.sinaimg.cn/large/{pic_id}.jpg"
                    pic_urls.append(pic_url)
            
            # 备用：如果pics字段存在，也尝试从中获取
            pics = status.get('pics', [])
            if pics and not pic_urls:
                pic_urls = [pic.get('large', {}).get('url', pic.get('url', '')) for pic in pics if pic.get('large', {}).get('url') or pic.get('url')]
            
            return {
                'weibo_id': weibo_id,
                'content': content,
                'publish_time': publish_time,
                'reposts_count': reposts,
                'comments_count': comments,
                'attitudes_count': attitudes,
                'pic_urls': pic_urls,
                'raw_data': status
            }
            
        except Exception as e:
            print(f"解析微博数据失败: {str(e)}")
            return None
    
    def _clean_html(self, html_text):
        """
        清除HTML标签，但保留标签内的文本内容
        
        Args:
            html_text: HTML文本
            
        Returns:
            str: 纯文本
        """
        if not html_text:
            return ''
        
        # 使用BeautifulSoup解析HTML，保留标签内的文本
        soup = BeautifulSoup(html_text, 'html.parser')
        # 获取所有文本内容
        text = soup.get_text()
        
        # 转义HTML实体
        text = text.replace('&quot;', '"')
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&nbsp;', ' ')
        
        return text.strip()
    
    def _parse_time(self, time_str):
        """
        解析时间字符串
        
        Args:
            time_str: 时间字符串
            
        Returns:
            datetime: 时间对象
        """
        if not time_str:
            return None
        
        try:
            # 处理不同格式的时间字符串
            # 格式1: "Mon Dec 18 12:00:00 +0800 2023"
            # 格式2: "2023-12-18 12:00:00"
            
            if '+' in time_str:
                # 处理带时区的格式
                time_str = re.sub(r'\+\d{4}', '', time_str).strip()
                return datetime.strptime(time_str, '%a %b %d %H:%M:%S %Y')
            else:
                return datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
                
        except Exception as e:
            print(f"解析时间失败: {time_str}, 错误: {str(e)}")
            return None
    
    def search_weibo_by_keyword(self, keyword, page=1, count=20):
        """
        搜索包含关键词的微博
        
        Args:
            keyword: 关键词
            page: 页码
            count: 每页数量
            
        Returns:
            list: 微博列表
        """
        try:
            search_url = f'{self.API_URL}/search/all'
            params = {
                'word': keyword,
                'page': page,
                'count': count
            }
            
            response = self.session.get(search_url, headers=self.headers, params=params, timeout=30)
            
            if response.status_code != 200:
                print(f"搜索微博失败: HTTP {response.status_code}")
                return []
            
            data = response.json()
            weibo_list = []
            
            # 解析搜索结果
            cards = data.get('data', {}).get('cards', [])
            for card in cards:
                if card.get('card_type') == 9:  # 微博卡片
                    mblog = card.get('mblog', {})
                    weibo_info = self._parse_weibo_item(mblog)
                    if weibo_info:
                        weibo_list.append(weibo_info)
            
            return weibo_list
            
        except Exception as e:
            print(f"搜索微博失败: {str(e)}")
            return []
    
    def check_cookie_valid(self):
        """
        检查Cookie是否有效
        
        Returns:
            bool: 是否有效
        """
        try:
            url = f'{self.API_URL}/config'
            response = self.session.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('data', {}).get('login', False)
            
            return False
            
        except Exception as e:
            print(f"检查Cookie失败: {str(e)}")
            return False
