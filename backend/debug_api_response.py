"""
调试API响应
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from spider.weibo_crawler import WeiboCrawler
from datetime import datetime

def debug_api():
    """调试API"""
    app = create_app()
    
    with app.app_context():
        print("=== 调试微博API响应 ===\n")
        
        uid = "5760856251"
        crawler = WeiboCrawler()
        
        # 获取第一页数据
        print("获取第1页数据...\n")
        
        import requests
        import time
        
        url = 'https://weibo.com/ajax/statuses/mymblog'
        params = {
            'uid': uid,
            'page': 1,
            'feature': 0
        }
        
        time.sleep(1.0)
        
        session = requests.Session()
        request_headers = crawler.headers.copy()
        if crawler.cookie:
            request_headers['Cookie'] = crawler.cookie
        
        response = session.get(url, headers=request_headers, params=params, timeout=30)
        session.close()
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('ok') == 1:
                statuses = data.get('data', {}).get('list', [])
                print(f"获取到 {len(statuses)} 条微博\n")
                
                # 显示前5条的详细信息
                for i, status in enumerate(statuses[:5]):
                    weibo_id = status.get('id')
                    created_at = status.get('created_at')
                    text = status.get('text', '')[:50]
                    
                    # 解析时间
                    publish_time = crawler._parse_time(created_at)
                    
                    print(f"[{i+1}] 微博ID: {weibo_id}")
                    print(f"    原始时间: {created_at}")
                    print(f"    解析时间: {publish_time}")
                    print(f"    内容: {text}...")
                    print()
                
                # 检查是否有2026-02-23的微博
                target_date = datetime(2026, 2, 23)
                found_target = False
                
                print("查找2026-02-23的微博...")
                for status in statuses:
                    created_at = status.get('created_at')
                    publish_time = crawler._parse_time(created_at)
                    
                    if publish_time and publish_time.date() == target_date.date():
                        found_target = True
                        print(f"\n找到目标日期微博:")
                        print(f"  ID: {status.get('id')}")
                        print(f"  时间: {publish_time}")
                        print(f"  内容: {status.get('text', '')[:100]}...")
                
                if not found_target:
                    print("第1页没有找到2026-02-23的微博")
                    
                    # 尝试获取更多页
                    print("\n尝试获取更多页...")
                    for page in range(2, 6):
                        print(f"\n获取第{page}页...")
                        time.sleep(1.0)
                        
                        params['page'] = page
                        session = requests.Session()
                        response = session.get(url, headers=request_headers, params=params, timeout=30)
                        session.close()
                        
                        if response.status_code == 200:
                            data = response.json()
                            if data.get('ok') == 1:
                                statuses = data.get('data', {}).get('list', [])
                                print(f"  获取到 {len(statuses)} 条微博")
                                
                                for status in statuses:
                                    created_at = status.get('created_at')
                                    publish_time = crawler._parse_time(created_at)
                                    
                                    if publish_time and publish_time.date() == target_date.date():
                                        found_target = True
                                        print(f"\n  找到目标日期微博:")
                                        print(f"    ID: {status.get('id')}")
                                        print(f"    时间: {publish_time}")
                                        print(f"    内容: {status.get('text', '')[:100]}...")
                                        break
                                
                                if found_target:
                                    break
                        
                        # 检查是否需要继续翻页
                        if statuses:
                            times = [crawler._parse_time(s.get('created_at')) for s in statuses if s.get('created_at')]
                            if times:
                                oldest = min(times)
                                print(f"  该页最早时间: {oldest}")
                                if oldest < target_date:
                                    print(f"  已经翻到目标日期之前，停止")
                                    break
                
                if not found_target:
                    print("\n✗ 未找到2026-02-23的微博")
                    print("可能原因:")
                    print("1. API只能获取最近几天的数据")
                    print("2. 该日期的微博已被删除或隐藏")
                    print("3. Cookie过期或权限不足")
            else:
                print(f"API返回错误: {data.get('msg', '未知错误')}")
        else:
            print(f"请求失败: HTTP {response.status_code}")

if __name__ == '__main__':
    debug_api()
