"""
检查微博详情
"""
import sys
import os
import time
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import SystemConfig
from spider.weibo_crawler import WeiboCrawler

def check_detail():
    """检查详情"""
    app = create_app()
    
    with app.app_context():
        print("=== 检查微博详情 ===\n")
        
        # 获取Cookie
        cookie = SystemConfig.get_value('weibo_cookie', '')
        target_mid = "11456415368239603"
        
        print(f"目标微博 MID: {target_mid}\n")
        
        # 尝试直接访问微博详情API
        url = f'https://weibo.com/ajax/statuses/show'
        params = {
            'id': target_mid
        }
        
        time.sleep(1.0)
        
        crawler = WeiboCrawler(cookie=cookie)
        session = requests.Session()
        request_headers = crawler.headers.copy()
        request_headers['Cookie'] = crawler.cookie
        
        print(f"请求微博详情...")
        response = session.get(url, headers=request_headers, params=params, timeout=30)
        session.close()
        
        print(f"响应状态码: {response.status_code}")
        
        try:
            data = response.json()
            
            if data.get('ok') == 1:
                print(f"\n✓ 找到微博！")
                print(f"  微博ID: {data.get('id')}")
                print(f"  内容: {data.get('text', '')[:100]}...")
                
                # 获取用户信息
                user = data.get('user', {})
                print(f"\n  用户信息:")
                print(f"    用户ID: {user.get('id')}")
                print(f"    昵称: {user.get('screen_name')}")
                print(f"    头像: {user.get('profile_image_url', '')[:50]}...")
                
                # 检查是否是转发
                if data.get('retweeted_status'):
                    print(f"\n  类型: 转发微博")
                    retweet = data.get('retweeted_status')
                    print(f"  原微博ID: {retweet.get('id')}")
                    retweet_user = retweet.get('user', {})
                    print(f"  原博主: {retweet_user.get('screen_name')}")
                else:
                    print(f"\n  类型: 原创微博")
                
                # 检查时间
                created_at = data.get('created_at')
                publish_time = crawler._parse_time(created_at)
                print(f"\n  发布时间: {publish_time}")
                
            else:
                print(f"\n✗ 获取微博失败: {data.get('msg', '未知错误')}")
                print(f"  完整响应: {data}")
        except Exception as e:
            print(f"解析失败: {str(e)}")
            print(f"响应内容: {response.text[:500]}")

if __name__ == '__main__':
    check_detail()
