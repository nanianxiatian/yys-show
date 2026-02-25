"""
不加过滤条件获取所有微博
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
        print("=== 不加过滤获取所有微博 ===\n")
        
        # 获取Cookie
        cookie = SystemConfig.get_value('weibo_cookie', '')
        uid = "5760856251"
        target_mid = "11456415368239603"
        target_url_id = "QtaCga9AD"
        
        print(f"目标微博 MID: {target_mid}")
        print(f"目标微博 URL ID: {target_url_id}")
        print(f"博主 UID: {uid}\n")
        
        crawler = WeiboCrawler(cookie=cookie)
        
        all_weibo = []
        found_target = False
        
        # 获取多页数据
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
                
                # 记录所有微博（不过滤）
                for status in statuses:
                    weibo_id = str(status.get('id'))
                    created_at = status.get('created_at')
