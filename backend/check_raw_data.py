"""
检查微博原始数据
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.services.weibo_spider import WeiboSpiderService

def check():
    """检查"""
    app = create_app()
    
    with app.app_context():
        spider_service = WeiboSpiderService()
        crawler = spider_service._get_crawler()
        
        # yys方寒的UID
        uid = '7596104274'
        
        print(f"获取博主UID {uid} 的微博列表...")
        
        # 获取微博列表
        url = f'{crawler.API_URL}/statuses/mymblog'
        params = {
            'uid': uid,
            'page': 1,
            'feature': 0
        }
        
        response = crawler.session.get(url, headers=crawler.headers, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('ok') == 1:
                statuses = data.get('data', {}).get('list', [])
                
                # 找到5269484910941738这条微博
                for status in statuses:
                    if str(status.get('id')) == '5269484910941738':
                        print(f"\n找到微博 5269484910941738:")
                        print(f"  内容: {status.get('text_raw', '')[:80]}...")
                        
                        # 检查user字段
                        user = status.get('user', {})
                        print(f"\n  User字段:")
                        print(f"    id: {user.get('id')}")
                        print(f"    screen_name: {user.get('screen_name')}")
                        
                        # 检查mblogtype字段（0=原创，1=转发，2=快转）
                        print(f"\n  mblogtype: {status.get('mblogtype')}")
                        
                        # 检查retweeted_status
                        if 'retweeted_status' in status:
                            print(f"\n  是转发微博")
                            print(f"    原博主: {status['retweeted_status'].get('user', {}).get('screen_name')}")
                        else:
                            print(f"\n  是原创微博")
                        
                        # 打印所有字段
                        print(f"\n  所有字段: {list(status.keys())}")
                        break

if __name__ == '__main__':
    check()
