"""
在多页中查找目标微博
"""
import sys
import os
import time
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import SystemConfig
from spider.weibo_crawler import WeiboCrawler
from datetime import datetime

def find_in_pages():
    """在多页中查找"""
    app = create_app()
    
    with app.app_context():
        print("=== 在多页中查找目标微博 ===\n")
        
        # 获取Cookie
        cookie = SystemConfig.get_value('weibo_cookie', '')
        uid = "5760856251"
        target_mid = "11456415368239603"
        target_date = datetime(2026, 2, 23)
        
        print(f"目标微博 MID: {target_mid}")
        print(f"目标日期: {target_date.date()}\n")
        
        crawler = WeiboCrawler(cookie=cookie)
        
        found_target = False
        all_weibo_ids = []
        
        for page in range(1, 11):
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
                    print("  没有更多数据")
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
                        print()
                        break
                
                if found_target:
                    break
                
                # 显示该页的时间范围
                if page_times:
                    oldest = min(page_times)
                    newest = max(page_times)
                    print(f"  该页时间范围: {oldest} ~ {newest}")
                    
                    # 如果最早的时间已经早于2026-02-23，可以停止
                    if oldest.date() < target_date.date():
                        print(f"  已经翻到目标日期之前，停止翻页")
                        break
                        
            except Exception as e:
                print(f"  错误: {str(e)}")
        
        print(f"\n\n总结:")
        print(f"  共获取 {len(all_weibo_ids)} 条微博")
        print(f"  找到目标微博: {'是' if found_target else '否'}")
        
        if not found_target:
            print(f"\n  目标微博 MID {target_mid} 不在API返回的数据中")
            print(f"\n  获取到的微博ID前10个:")
            for i, wid in enumerate(all_weibo_ids[:10]):
                print(f"    {i+1}. {wid}")

if __name__ == '__main__':
    find_in_pages()
