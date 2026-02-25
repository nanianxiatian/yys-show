"""
检查API错误详情
"""
import sys
import os
import time
import requests
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from spider.weibo_crawler import WeiboCrawler

def check_api():
    """检查API"""
    app = create_app()
    
    with app.app_context():
        print("=== 检查API错误详情 ===\n")
        
        uid = "5760856251"
        crawler = WeiboCrawler()
        
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
            print(f"Cookie已设置，长度: {len(crawler.cookie)}\n")
        else:
            print("Cookie未设置！\n")
        
        print(f"请求URL: {url}")
        print(f"请求参数: {params}")
        print(f"请求头: {dict(list(request_headers.items())[:3])}...\n")
        
        response = session.get(url, headers=request_headers, params=params, timeout=30)
        session.close()
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容前500字符:\n{response.text[:500]}\n")
        
        try:
            data = response.json()
            print(f"解析后的数据:")
            print(json.dumps(data, indent=2, ensure_ascii=False)[:1000])
        except Exception as e:
            print(f"解析JSON失败: {str(e)}")

if __name__ == '__main__':
    check_api()
