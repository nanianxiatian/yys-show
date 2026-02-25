"""
检查原始微博数据
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from spider.weibo_crawler import WeiboCrawler

def check_weibo():
    """检查微博"""
    app = create_app()
    
    with app.app_context():
        print("=== 检查Mico林木森原始微博数据 ===\n")
        
        uid = "5760856251"
        
        crawler = WeiboCrawler()
        
        # 获取第一页微博
        print("获取第一页微博...\n")
        weibo_list = crawler.get_user_weibo_list(uid, page=1, count=20)
        
        if weibo_list:
            print(f"获取到 {len(weibo_list)} 条微博\n")
            
            for i, weibo in enumerate(weibo_list[:10]):  # 只显示前10条
                print(f"[{i+1}] 微博ID: {weibo.get('weibo_id')}")
                print(f"    发布时间: {weibo.get('publish_time')}")
                print(f"    是否转发: {weibo.get('is_retweet', False)}")
                print(f"    用户ID: {weibo.get('user_id')}")
                print(f"    内容: {weibo.get('content', '')[:80]}...")
                print()
        else:
            print("没有获取到微博")

if __name__ == '__main__':
    check_weibo()
