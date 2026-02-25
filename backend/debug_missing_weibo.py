"""
调试缺失的微博 - 检查API返回的数据
"""
import sys
import os
import time
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import Blogger
from spider.weibo_crawler import WeiboCrawler

def debug_missing_weibo():
    """调试缺失的微博"""
    app = create_app()
    
    with app.app_context():
        print("=== 调试缺失的微博 ===\n")
        
        # 目标微博信息
        target_mid = "11456415368239603"
        target_url_id = "QtaCga9AD"
        uid = "5760856251"  # Mico林木森
        
        print(f"目标微博 MID: {target_mid}")
        print(f"目标微博 URL ID: {target_url_id}")
        print(f"博主 UID: {uid}\n")
        
        # 获取博主信息
        mico = Blogger.query.filter_by(weibo_uid=uid).first()
        if mico:
            print(f"博主: {mico.nickname} (ID: {mico.id})\n")
        
        # 初始化爬虫
        crawler = WeiboCrawler()
        
        # 获取多页数据，查找目标微博
        print("开始获取微博数据...\n")
        
        found_target = False
        all_weibo_ids = []
        
        for page in range(1, 11):  # 获取10页
            print(f"获取第 {page} 页...")
            
            try:
                url = 'https://weibo.com/ajax/statuses/mymblog'
                params = {
                    'uid': uid,
                    'page': page,
                    'feature': 0
                }
                
                time.sleep(1.0)
                
                session = requests.Session()
                request_headers = crawler.headers.copy()
                if crawler.cookie:
                    request_headers['Cookie'] = crawler.cookie
                
                response = session.get(url, headers=request_headers, params=params, timeout=30)
                session.close()
                
                if response.status_code != 200:
                    print(f"  HTTP错误: {response.status_code}")
                    continue
                
                data = response.json()
                
                if data.get('ok') != 1:
                    print(f"  API错误: {data.get('msg', '未知错误')}")
                    continue
                
                statuses = data.get('data', {}).get('list', [])
                print(f"  获取到 {len(statuses)} 条微博")
                
                if not statuses:
                    print("  没有更多数据，停止")
                    break
                
                # 检查每条微博
                page_times = []
                for status in statuses:
                    weibo_id = str(status.get('id'))
                    all_weibo_ids.append(weibo_id)
                    
                    created_at = status.get('created_at')
                    publish_time = crawler._parse_time(created_at)
                    
                    if publish_time:
                        page_times.append(publish_time)
                    
                    # 检查是否是目标微博
                    if weibo_id == target_mid:
                        found_target = True
                        print(f"\n  ✓✓✓ 找到目标微博！✓✓✓")
                        print(f"    ID: {weibo_id}")
                        print(f"    时间: {publish_time}")
                        print(f"    内容: {status.get('text', '')[:100]}...")
                        
                        # 检查是否是转发
                        if status.get('retweeted_status'):
                            print(f"    类型: 转发微博")
                        else:
                            print(f"    类型: 原创微博")
                        
                        # 检查用户ID
                        user = status.get('user', {})
                        actual_uid = str(user.get('id', ''))
                        print(f"    用户ID: {actual_uid}")
                        
                        if actual_uid != uid:
                            print(f"    ⚠ 用户ID不匹配！期望: {uid}, 实际: {actual_uid}")
                        
                        print()
                
                # 显示该页的时间范围
                if page_times:
                    oldest = min(page_times)
                    newest = max(page_times)
                    print(f"  该页时间范围: {oldest} ~ {newest}")
                
                # 检查是否需要继续翻页
                # 如果最早的时间已经早于2026-02-23，可以停止
                target_date = crawler._parse_time('Sun Feb 23 00:00:00 +0800 2026')
                if page_times and min(page_times) < target_date:
                    print(f"  已经翻到目标日期之前，停止翻页")
                    break
                    
            except Exception as e:
                print(f"  错误: {str(e)}")
                import traceback
                traceback.print_exc()
        
        print(f"\n\n总结:")
        print(f"  共获取 {len(all_weibo_ids)} 条微博")
        print(f"  找到目标微博: {'是' if found_target else '否'}")
        
        if not found_target:
            print(f"\n  目标微博 MID {target_mid} 不在API返回的数据中")
            print(f"  可能原因:")
            print(f"    1. 该微博已被删除")
            print(f"    2. 该微博被设置为私密")
            print(f"    3. API权限限制，无法获取该微博")
            print(f"    4. 该微博ID对应的不是Mico林木森的微博")

if __name__ == '__main__':
    debug_missing_weibo()
