"""
获取Mico林木森2026-02-23的所有微博（不加过滤）
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

def get_all_weibo():
    """获取所有微博"""
    app = create_app()
    
    with app.app_context():
        print("=== 获取Mico林木森2026-02-23的所有微博（无过滤）===\n")
        
        # 获取Cookie
        cookie = SystemConfig.get_value('weibo_cookie', '')
        uid = "5760856251"
        target_mid = "11456415368239603"
        target_date = datetime(2026, 2, 23)
        
        print(f"博主UID: {uid}")
        print(f"目标日期: {target_date.date()}")
        print(f"目标微博MID: {target_mid}\n")
        
        crawler = WeiboCrawler(cookie=cookie)
        
        all_weibo = []
        found_target = False
        
        for page in range(1, 21):  # 获取20页
            print(f"获取第 {page} 页...")
            
            try:
                url = 'https://weibo.com/ajax/statuses/mymblog'
                params = {
                    'uid': uid,
                    'page': page,
                    'feature': 0
                }
                
                time.sleep(0.5)
                
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
                
                # 处理每条微博（不过滤）
                for status in statuses:
                    weibo_id = str(status.get('id'))
                    created_at = status.get('created_at')
                    publish_time = crawler._parse_time(created_at)
                    
                    weibo_info = {
                        'id': weibo_id,
                        'time': publish_time,
                        'text': status.get('text', '')[:80],
                        'is_retweet': bool(status.get('retweeted_status')),
                        'user_id': str(status.get('user', {}).get('id', ''))
                    }
                    all_weibo.append(weibo_info)
                    
                    # 检查是否是目标微博
                    if weibo_id == target_mid:
                        found_target = True
                        print(f"\n  ✓✓✓ 找到目标微博！✓✓✓")
                        print(f"    ID: {weibo_id}")
                        print(f"    时间: {publish_time}")
                        print(f"    内容: {status.get('text', '')[:100]}...")
                        print(f"    是否转发: {weibo_info['is_retweet']}")
                        print(f"    用户ID: {weibo_info['user_id']}")
                
                # 检查是否已经翻到目标日期之前
                page_times = [crawler._parse_time(s.get('created_at')) for s in statuses if s.get('created_at')]
                if page_times:
                    oldest = min(page_times)
                    if oldest.date() < target_date.date():
                        print(f"  已经翻到目标日期之前({oldest.date()})，停止")
                        break
                        
            except Exception as e:
                print(f"  错误: {str(e)}")
        
        # 显示2026-02-23的所有微博
        print(f"\n\n=== 2026-02-23的所有微博 ===\n")
        feb23_weibo = [w for w in all_weibo if w['time'] and w['time'].date() == target_date.date()]
        
        if feb23_weibo:
            print(f"找到 {len(feb23_weibo)} 条微博:\n")
            for i, w in enumerate(feb23_weibo, 1):
                print(f"[{i}] ID: {w['id']}")
                print(f"    时间: {w['time']}")
                print(f"    是否转发: {w['is_retweet']}")
                print(f"    用户ID: {w['user_id']}")
                print(f"    内容: {w['text']}...")
                print()
        else:
            print("没有找到2026-02-23的微博\n")
        
        # 显示所有获取到的微博ID（用于对比）
        print(f"\n=== 所有获取到的微博ID（共{len(all_weibo)}条）===\n")
        for w in all_weibo[:20]:  # 只显示前20条
            date_str = w['time'].strftime('%m-%d') if w['time'] else 'Unknown'
            print(f"  {w['id']} ({date_str}) {'[转发]' if w['is_retweet'] else ''}")
        
        if len(all_weibo) > 20:
            print(f"  ... 还有 {len(all_weibo) - 20} 条")
        
        print(f"\n\n总结:")
        print(f"  总共获取: {len(all_weibo)} 条微博")
        print(f"  2026-02-23: {len(feb23_weibo)} 条")
        print(f"  找到目标微博: {'是' if found_target else '否'}")

if __name__ == '__main__':
    get_all_weibo()
