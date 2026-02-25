"""
使用正确的Cookie调试API
"""
import sys
import os
import time
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import SystemConfig
from spider.weibo_crawler import WeiboCrawler

def debug_api():
    """调试API"""
    app = create_app()
    
    with app.app_context():
        print("=== 使用Cookie调试API ===\n")
        
        # 从数据库获取Cookie
        cookie = SystemConfig.get_value('weibo_cookie', '')
        print(f"Cookie长度: {len(cookie)}")
        print(f"Cookie前100字符: {cookie[:100]}...\n")
        
        uid = "5760856251"
        
        # 创建爬虫
        crawler = WeiboCrawler(cookie=cookie)
        
        # 测试API
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
        
        print(f"请求头中的Cookie长度: {len(request_headers.get('Cookie', ''))}\n")
        
        response = session.get(url, headers=request_headers, params=params, timeout=30)
        session.close()
        
        print(f"响应状态码: {response.status_code}")
        
        try:
            data = response.json()
            print(f"响应ok字段: {data.get('ok')}")
            
            if data.get('ok') == 1:
                statuses = data.get('data', {}).get('list', [])
                print(f"\n✓ API请求成功！")
                print(f"获取到 {len(statuses)} 条微博")
                
                # 查找目标微博
                target_mid = "11456415368239603"
                found = False
                
                for status in statuses:
                    weibo_id = str(status.get('id'))
                    if weibo_id == target_mid:
                        found = True
                        print(f"\n✓✓✓ 找到目标微博！")
                        print(f"  ID: {weibo_id}")
                        print(f"  内容: {status.get('text', '')[:100]}...")
                        break
                
                if not found:
                    print(f"\n✗ 第1页未找到目标微博 {target_mid}")
                    
            else:
                print(f"\n✗ API返回错误: {data.get('msg', '未知错误')}")
                print(f"完整响应: {data}")
        except Exception as e:
            print(f"解析失败: {str(e)}")
            print(f"响应内容: {response.text[:500]}")

if __name__ == '__main__':
    debug_api()
