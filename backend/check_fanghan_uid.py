"""
检查yys方寒的UID和微博
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
        weibo_list = crawler.get_user_weibo_list(uid, page=1, count=20)
        
        print(f"\n获取到 {len(weibo_list)} 条微博\n")
        
        for weibo in weibo_list:
            weibo_id = weibo['weibo_id']
            content = weibo['content'][:60]
            
            # 检查微博的user字段
            user_info = weibo.get('user', {})
            user_id = user_info.get('id')
            user_name = user_info.get('screen_name')
            
            print(f"微博ID: {weibo_id}")
            print(f"  内容: {content}...")
            print(f"  发布者ID: {user_id}")
            print(f"  发布者: {user_name}")
            print(f"  是否原创: {user_id == int(uid) if user_id else 'Unknown'}")
            print()

if __name__ == '__main__':
    check()
