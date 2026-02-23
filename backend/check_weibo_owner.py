"""
检查微博的实际博主
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
        
        # 微博ID列表
        weibo_ids = ['5269502239442384', '5269484910941738']
        
        for weibo_id in weibo_ids:
            print(f"\n检查微博ID: {weibo_id}")
            # 通过微博详情API获取博主信息
            url = f"https://weibo.com/ajax/statuses/show?id={weibo_id}"
            try:
                response = crawler.session.get(url, headers=crawler.headers)
                if response.status_code == 200:
                    data = response.json()
                    user = data.get('user', {})
                    print(f"  博主昵称: {user.get('screen_name')}")
                    print(f"  博主UID: {user.get('id')}")
                    print(f"  发布时间: {data.get('created_at')}")
                else:
                    print(f"  请求失败: {response.status_code}")
            except Exception as e:
                print(f"  错误: {e}")

if __name__ == '__main__':
    check()
