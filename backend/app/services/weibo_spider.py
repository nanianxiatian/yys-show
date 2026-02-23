from datetime import datetime
from spider import WeiboCrawler, GuessParser
from app.models import db, Blogger, WeiboPost, SpiderLog, SystemConfig


class WeiboSpiderService:
    """微博爬虫服务"""
    
    def __init__(self):
        self.crawler = None
    
    def _get_crawler(self):
        """延迟初始化爬虫"""
        if self.crawler is None:
            try:
                cookie = SystemConfig.get_value('weibo_cookie', '')
            except:
                cookie = ''
            self.crawler = WeiboCrawler(cookie=cookie)
        return self.crawler
    
    def update_cookie(self, cookie):
        """
        更新Cookie
        
        Args:
            cookie: 新的Cookie字符串
            
        Returns:
            bool: 是否成功
        """
        try:
            self._get_crawler().set_cookie(cookie)
            if self._get_crawler().check_cookie_valid():
                SystemConfig.set_value('weibo_cookie', cookie)
                SystemConfig.set_value('cookie_expire_time',
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                return True
            return False
        except Exception as e:
            print(f"更新Cookie失败: {str(e)}")
            return False

    def check_cookie(self):
        """
        检查Cookie是否有效

        Returns:
            bool: 是否有效
        """
        return self._get_crawler().check_cookie_valid()
    
    def spider_all_bloggers(self, spider_type='auto', blogger_id=None):
        """
        爬取博主的微博
        
        Args:
            spider_type: 爬虫类型(auto/manual)
            blogger_id: 指定博主ID，如果为None则同步所有博主
            
        Returns:
            dict: 爬取结果
        """
        # 创建爬虫日志
        log = SpiderLog(
            spider_type=spider_type,
            status='running',
            start_time=datetime.now()
        )
        db.session.add(log)
        db.session.commit()
        
        try:
            # 获取要同步的博主列表
            if blogger_id:
                blogger = Blogger.query.get(blogger_id)
                if not blogger:
                    return {'success': False, 'error': '博主不存在'}
                bloggers = [blogger]
            else:
                bloggers = Blogger.query.filter_by(is_active=True).all()
            
            total_posts = 0
            errors = []
            
            for blogger in bloggers:
                try:
                    count = self._spider_blogger(blogger)
                    total_posts += count
                except Exception as e:
                    error_msg = f"爬取博主 {blogger.nickname} 失败: {str(e)}"
                    errors.append(error_msg)
                    print(error_msg)
            
            # 更新日志
            log.status = 'success' if not errors else 'failed'
            log.end_time = datetime.now()
            log.posts_count = total_posts
            log.error_message = '\n'.join(errors) if errors else None
            db.session.commit()
            
            return {
                'success': True,
                'total_posts': total_posts,
                'bloggers_count': len(bloggers),
                'errors': errors
            }
            
        except Exception as e:
            log.status = 'failed'
            log.end_time = datetime.now()
            log.error_message = str(e)
            db.session.commit()
            
            return {
                'success': False,
                'error': str(e)
            }
    
    def spider_single_blogger(self, blogger_id, keyword='对弈竞猜'):
        """
        手动同步单个博主
        
        Args:
            blogger_id: 博主ID
            keyword: 关键词
            
        Returns:
            dict: 爬取结果
        """
        blogger = Blogger.query.get(blogger_id)
        if not blogger:
            return {'success': False, 'error': '博主不存在'}
        
        # 创建爬虫日志
        log = SpiderLog(
            spider_type='manual',
            blogger_id=blogger_id,
            status='running',
            start_time=datetime.now()
        )
        db.session.add(log)
        db.session.commit()
        
        try:
            # 获取博主UID
            if not blogger.weibo_uid:
                print(f"[SPIDER] 手动同步 - 尝试获取博主UID: {blogger.nickname}")
                user_info = self._get_crawler().get_user_info(blogger.nickname)
                if user_info:
                    blogger.weibo_uid = user_info['uid']
                    blogger.avatar_url = user_info.get('avatar')
                    blogger.description = user_info.get('description')
                    db.session.commit()
                    print(f"[SPIDER] 手动同步 - 获取到UID: {user_info['uid']}")
                else:
                    error_msg = f"无法自动获取博主 {blogger.nickname} 的UID。请在博主管理页面手动编辑该博主，填写其微博UID。"
                    print(f"[SPIDER] {error_msg}")
                    log.status = 'failed'
                    log.end_time = datetime.now()
                    log.error_message = error_msg
                    db.session.commit()
                    return {
                        'success': False,
                        'error': error_msg
                    }

            # 手动同步前，删除该博主最新一轮的自动同步数据
            print(f"[SPIDER] 手动同步 - 清理博主 {blogger.nickname} 的最新自动同步数据")
            from sqlalchemy import func
            latest_post = WeiboPost.query.filter_by(blogger_id=blogger_id)\
                .order_by(WeiboPost.publish_time.desc()).first()

            if latest_post:
                # 找到同一轮次的所有微博（同一天同一轮）
                same_round_posts = WeiboPost.query.filter_by(
                    blogger_id=blogger_id,
                    guess_date=latest_post.guess_date,
                    guess_round=latest_post.guess_round
                ).all()

                for post in same_round_posts:
                    db.session.delete(post)
                    print(f"[SPIDER] 删除自动同步数据: {post.weibo_id}")

                db.session.commit()
                print(f"[SPIDER] 已清理 {len(same_round_posts)} 条自动同步数据")

            # 获取最近多条微博（手动同步不限关键词，获取最近10条）
            weibo_list = self._get_crawler().get_user_weibo_list(
                blogger.weibo_uid,
                page=1,
                count=10
            )

            if not weibo_list:
                log.status = 'success'
                log.end_time = datetime.now()
                log.posts_count = 0
                db.session.commit()

                return {
                    'success': True,
                    'message': '未找到微博',
                    'posts_count': 0
                }

            # 筛选出对弈竞猜相关的微博
            guess_weibos = []
            for weibo in weibo_list:
                parsed = GuessParser.parse_weibo(weibo)
                if parsed['is_guess_related']:
                    guess_weibos.append((weibo, parsed))

            if not guess_weibos:
                log.status = 'success'
                log.end_time = datetime.now()
                log.posts_count = 0
                db.session.commit()

                return {
                    'success': True,
                    'message': '未找到竞猜相关微博',
                    'posts_count': 0
                }

            # 取最新的竞猜微博
            latest_weibo, parsed = guess_weibos[0]

            import json
            
            # 获取图片URL列表
            pic_urls = latest_weibo.get('pic_urls', [])
            pic_urls_json = json.dumps(pic_urls) if pic_urls else None
            
            # 构建微博原链接
            weibo_url = f"https://weibo.com/{blogger.weibo_uid}/{latest_weibo['weibo_id']}"

            # 创建新记录（手动同步的）
            post = WeiboPost(
                blogger_id=blogger_id,
                weibo_id=latest_weibo['weibo_id'],
                content=latest_weibo['content'],
                guess_prediction=parsed['guess_prediction'],
                guess_round=parsed['guess_round'],
                guess_date=parsed['guess_date'],
                publish_time=latest_weibo['publish_time'],
                reposts_count=latest_weibo['reposts_count'],
                comments_count=latest_weibo['comments_count'],
                attitudes_count=latest_weibo['attitudes_count'],
                is_guess_related=parsed['is_guess_related'],
                pic_urls=pic_urls_json,
                weibo_url=weibo_url
            )
            db.session.add(post)
            print(f"[SPIDER] 手动同步 - 保存新微博: {latest_weibo['weibo_id']}")

            db.session.commit()
            
            # 更新日志
            log.status = 'success'
            log.end_time = datetime.now()
            log.posts_count = 1
            db.session.commit()
            
            return {
                'success': True,
                'message': '同步成功',
                'posts_count': 1,
                'data': {
                    'content': latest_weibo['content'][:100] + '...' if len(latest_weibo['content']) > 100 else latest_weibo['content'],
                    'prediction': parsed['guess_prediction'],
                    'round': parsed['guess_round']
                }
            }
            
        except Exception as e:
            log.status = 'failed'
            log.end_time = datetime.now()
            log.error_message = str(e)
            db.session.commit()
            
            return {
                'success': False,
                'error': str(e)
            }

    def sync_blogger_info(self, blogger_id):
        """
        只同步博主信息（头像、UID、描述等），不爬取微博
        
        Args:
            blogger_id: 博主ID
            
        Returns:
            dict: 同步结果
        """
        blogger = Blogger.query.get(blogger_id)
        if not blogger:
            return {'success': False, 'error': '博主不存在'}
        
        try:
            print(f"[SYNC] 同步博主信息: {blogger.nickname}")
            
            user_info = None
            
            # 方法1: 如果已有UID，优先使用UID直接获取用户信息
            if blogger.weibo_uid:
                print(f"[SYNC] 使用已有UID获取信息: {blogger.weibo_uid}")
                user_info = self._get_crawler()._get_user_detail(blogger.weibo_uid)
                if user_info:
                    print(f"[SYNC] 通过UID获取信息成功")
            
            # 方法2: 如果没有UID或UID获取失败，使用昵称搜索
            if not user_info:
                print(f"[SYNC] 使用昵称搜索: {blogger.nickname}")
                user_info = self._get_crawler().get_user_info(blogger.nickname)
            
            if not user_info:
                return {
                    'success': False,
                    'error': f'无法获取博主 {blogger.nickname} 的信息，请检查昵称是否正确或Cookie是否有效'
                }
            
            # 更新博主信息
            blogger.weibo_uid = user_info['uid']
            blogger.avatar_url = user_info.get('avatar')
            blogger.description = user_info.get('description')
            # 同时更新昵称为最新的
            if user_info.get('nickname'):
                blogger.nickname = user_info['nickname']
            db.session.commit()
            
            print(f"[SYNC] 同步成功 - UID: {user_info['uid']}, 昵称: {blogger.nickname}")
            
            return {
                'success': True,
                'message': '博主信息同步成功',
                'data': {
                    'uid': user_info['uid'],
                    'nickname': user_info['nickname'],
                    'avatar': user_info.get('avatar'),
                    'description': user_info.get('description')
                }
            }
            
        except Exception as e:
            print(f"[SYNC] 同步失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': str(e)
            }

    def spider_by_time_range(self, start_time, end_time, blogger_id=None, spider_type='manual'):
        """
        按时间段爬取微博
        
        Args:
            start_time: 开始时间，格式：YYYY-MM-DD HH:MM:SS
            end_time: 结束时间，格式：YYYY-MM-DD HH:MM:SS
            blogger_id: 博主ID，为None则爬取所有博主
            spider_type: 爬虫类型（manual/auto）
            
        Returns:
            dict: 爬取结果
        """
        from app.models import SpiderLog
        from datetime import datetime
        
        # 创建爬虫日志
        log = SpiderLog(
            spider_type=spider_type,
            blogger_id=blogger_id,
            status='running',
            start_time=datetime.now()
        )
        db.session.add(log)
        db.session.commit()
        
        try:
            # 获取要同步的博主列表
            if blogger_id:
                blogger = Blogger.query.get(blogger_id)
                if not blogger:
                    return {'success': False, 'error': '博主不存在'}
                bloggers = [blogger]
            else:
                bloggers = Blogger.query.filter_by(is_active=True).all()
            
            total_posts = 0
            errors = []
            
            for blogger in bloggers:
                try:
                    count = self._spider_blogger_by_time_range(blogger, start_time, end_time)
                    total_posts += count
                except Exception as e:
                    error_msg = f"爬取博主 {blogger.nickname} 失败: {str(e)}"
                    errors.append(error_msg)
                    print(error_msg)
            
            # 更新日志
            log.status = 'success' if not errors else 'failed'
            log.end_time = datetime.now()
            log.posts_count = total_posts
            log.error_message = '\n'.join(errors) if errors else None
            db.session.commit()
            
            return {
                'success': True,
                'total_posts': total_posts,
                'bloggers_count': len(bloggers),
                'errors': errors
            }
            
        except Exception as e:
            log.status = 'failed'
            log.end_time = datetime.now()
            log.error_message = str(e)
            db.session.commit()
            
            return {
                'success': False,
                'error': str(e)
            }

    def _spider_blogger_by_time_range(self, blogger, start_time, end_time):
        """
        爬取单个博主指定时间段的微博
        
        Args:
            blogger: 博主对象
            start_time: 开始时间
            end_time: 结束时间
            
        Returns:
            int: 新增的微博数量
        """
        print(f"[SPIDER] 爬取博主 {blogger.nickname} 时间段 {start_time} 到 {end_time}")
        
        # 获取博主UID
        if not blogger.weibo_uid:
            print(f"[SPIDER] 尝试获取博主UID: {blogger.nickname}")
            user_info = self._get_crawler().get_user_info(blogger.nickname)
            if user_info:
                blogger.weibo_uid = user_info['uid']
                blogger.avatar_url = user_info.get('avatar')
                blogger.description = user_info.get('description')
                db.session.commit()
                print(f"[SPIDER] 获取到UID: {user_info['uid']}")
            else:
                print(f"[SPIDER] 无法获取博主 {blogger.nickname} 的UID，跳过")
                return 0
        
        # 爬取该时间段的微博（不限关键词，获取所有微博，最多取3条）
        weibo_list = self._get_crawler().get_weibo_by_time_range(
            blogger.weibo_uid,
            start_time,
            end_time,
            keyword=None
        )
        
        if not weibo_list:
            print(f"[SPIDER] 博主 {blogger.nickname} 在指定时间段没有微博")
            return 0
        
        print(f"[SPIDER] 获取到 {len(weibo_list)} 条微博")
        
        # 保存所有微博（不再筛选竞猜相关）
        import json
        saved_count = 0
        
        for weibo in weibo_list:
            # 检查是否已存在
            existing = WeiboPost.query.filter_by(weibo_id=weibo['weibo_id']).first()
            if existing:
                print(f"[SPIDER] 微博已存在，跳过: {weibo['weibo_id']}")
                continue
            
            # 解析微博（用于获取预测、轮次等信息）
            parsed = GuessParser.parse_weibo(weibo)
            print(f"[SPIDER] 处理微博 {weibo['weibo_id']}: 预测={parsed['guess_prediction']}, 内容={weibo['content'][:30]}...")
            
            pic_urls = weibo.get('pic_urls', [])
            pic_urls_json = json.dumps(pic_urls) if pic_urls else None
            weibo_url = f"https://weibo.com/{blogger.weibo_uid}/{weibo['weibo_id']}"
            
            # 如果有多条微博，标记为multiple
            prediction = parsed['guess_prediction']
            if len(weibo_list) > 1:
                prediction = 'multiple'
                print(f"[SPIDER] 博主 {blogger.nickname} 有多条微博，标记为multiple")
            
            post = WeiboPost(
                blogger_id=blogger.id,
                weibo_id=weibo['weibo_id'],
                content=weibo['content'],
                guess_prediction=prediction,
                guess_round=parsed['guess_round'],
                guess_date=parsed['guess_date'],
                publish_time=weibo['publish_time'],
                reposts_count=weibo['reposts_count'],
                comments_count=weibo['comments_count'],
                attitudes_count=weibo['attitudes_count'],
                is_guess_related=parsed['is_guess_related'],
                pic_urls=pic_urls_json,
                weibo_url=weibo_url
            )
            db.session.add(post)
            db.session.commit()
            
            print(f"[SPIDER] 保存微博: {weibo['weibo_id']}, 预测={prediction}")
            saved_count += 1
        
        print(f"[SPIDER] 博主 {blogger.nickname} 共保存 {saved_count} 条微博")
        return saved_count
    
    def _spider_blogger(self, blogger):
        """
        爬取单个博主的微博

        Args:
            blogger: 博主对象

        Returns:
            int: 新增/更新的微博数量
        """
        print(f"[SPIDER] 开始爬取博主: {blogger.nickname}")

        # 获取博主UID
        if not blogger.weibo_uid:
            print(f"[SPIDER] 获取博主UID: {blogger.nickname}")
            user_info = self._get_crawler().get_user_info(blogger.nickname)
            if user_info:
                blogger.weibo_uid = user_info['uid']
                blogger.avatar_url = user_info.get('avatar')
                blogger.description = user_info.get('description')
                db.session.commit()
                print(f"[SPIDER] 获取到UID: {user_info['uid']}")
            else:
                print(f"[SPIDER] 警告: 无法自动获取博主 {blogger.nickname} 的UID")
                print(f"[SPIDER] 建议: 在博主管理页面手动编辑该博主，填写其微博UID")
                return 0

        print(f"[SPIDER] 博主UID: {blogger.weibo_uid}")

        # 获取最近多条微博（不限关键词，获取最近10条）
        print(f"[SPIDER] 获取博主最近微博...")
        weibo_list = self._get_crawler().get_user_weibo_list(blogger.weibo_uid, page=1, count=10)

        if not weibo_list:
            print(f"[SPIDER] 未获取到微博")
            return 0

        print(f"[SPIDER] 获取到 {len(weibo_list)} 条微博")

        # 筛选出对弈竞猜相关的微博
        guess_weibos = []
        for weibo in weibo_list:
            parsed = GuessParser.parse_weibo(weibo)
            if parsed['is_guess_related']:
                guess_weibos.append((weibo, parsed))
                print(f"[SPIDER] 竞猜微博: {weibo['weibo_id']} - {weibo['content'][:50]}...")

        if not guess_weibos:
            print(f"[SPIDER] 未找到竞猜相关微博")
            return 0

        # 取最新的竞猜微博
        latest_weibo, parsed = guess_weibos[0]
        print(f"[SPIDER] 最新竞猜微博: {latest_weibo['weibo_id']}")
        print(f"[SPIDER] 内容: {latest_weibo['content'][:80]}...")
        print(f"[SPIDER] 预测结果: {parsed['guess_prediction']}")
        print(f"[SPIDER] 竞猜轮次: {parsed['guess_round']}")
        print(f"[SPIDER] 竞猜日期: {parsed['guess_date']}")

        import json
        
        # 获取图片URL列表
        pic_urls = latest_weibo.get('pic_urls', [])
        print(f"[SPIDER] 图片URL列表: {pic_urls}")
        pic_urls_json = json.dumps(pic_urls) if pic_urls else None
        
        # 构建微博原链接
        weibo_url = f"https://weibo.com/{blogger.weibo_uid}/{latest_weibo['weibo_id']}"
        print(f"[SPIDER] 微博链接: {weibo_url}")
        
        # 检查是否已存在相同微博ID
        existing = WeiboPost.query.filter_by(weibo_id=latest_weibo['weibo_id']).first()
        
        # 如果该微博属于某一轮次，检查是否已有该轮次的记录
        if parsed['guess_round'] and parsed['guess_date']:
            same_round_posts = WeiboPost.query.filter_by(
                blogger_id=blogger.id,
                guess_date=parsed['guess_date'],
                guess_round=parsed['guess_round']
            ).all()
            
            # 删除同一轮次的旧记录（保留最新的）
            for old_post in same_round_posts:
                if old_post.weibo_id != latest_weibo['weibo_id']:
                    print(f"[SPIDER] 删除同一轮次的旧微博: {old_post.weibo_id} (第{parsed['guess_round']}轮)")
                    db.session.delete(old_post)
        
        if existing:
            # 更新现有记录
            existing.content = latest_weibo['content']
            existing.guess_prediction = parsed['guess_prediction']
            existing.guess_round = parsed['guess_round']
            existing.guess_date = parsed['guess_date']
            existing.publish_time = latest_weibo['publish_time']
            existing.reposts_count = latest_weibo['reposts_count']
            existing.comments_count = latest_weibo['comments_count']
            existing.attitudes_count = latest_weibo['attitudes_count']
            existing.is_guess_related = parsed['is_guess_related']
            existing.pic_urls = pic_urls_json
            existing.weibo_url = weibo_url
            print(f"[SPIDER] 更新现有微博记录")
        else:
            # 创建新记录
            post = WeiboPost(
                blogger_id=blogger.id,
                weibo_id=latest_weibo['weibo_id'],
                content=latest_weibo['content'],
                guess_prediction=parsed['guess_prediction'],
                guess_round=parsed['guess_round'],
                guess_date=parsed['guess_date'],
                publish_time=latest_weibo['publish_time'],
                reposts_count=latest_weibo['reposts_count'],
                comments_count=latest_weibo['comments_count'],
                attitudes_count=latest_weibo['attitudes_count'],
                is_guess_related=parsed['is_guess_related'],
                pic_urls=pic_urls_json,
                weibo_url=weibo_url
            )
            db.session.add(post)
            print(f"[SPIDER] 创建新微博记录")

        db.session.commit()
        return 1
