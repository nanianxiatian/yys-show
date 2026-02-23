"""
检查微博类型（原创vs点赞/转发）
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
        weibo_ids = ['5269484910941738']  # 这条应该是鸽海成路的，但被同步到了yys方寒
        
        for weibo_id in weibo_ids:
            print(f"\n检查微博ID: {weibo_id}")
            # 通过微博详情API获取详细信息
            url = f"https://weibo.com/ajax/statuses/show?id={weibo_id}"
            try:
                response = crawler.session.get(url, headers=crawler.headers)
                if response.status_code == 200:
                    data = response.json()
                    print(f"  博主昵称: {data.get('user', {}).get('screen_name')}")
                    print(f"  博主UID: {data.get('user', {}).get('id')}")
                    print(f"  微博类型: {data.get('type')}")  # 1=原创, 2=转发
                    print(f"  是否转发: {data.get('retweeted_status') is not None}")
                    print(f"  是否点赞: {data.get(' attitudes_count')}")
                    
                    # 打印完整数据结构
                    print(f"\n  完整数据键: {list(data.keys())}")
                    
                    # 检查是否有转发信息
                    if 'retweeted_status' in data:
                        print(f"  转发来源: {data['retweeted_status'].get('user', {}).get('screen_name')}")
                else:
                    print(f"  请求失败: {response.status_code}")
            except Exception as e:
                print(f"  错误: {e}")

if __name__ == '__main__':
    check()
