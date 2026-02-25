"""
查找目标微博
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import WeiboPost, Blogger

def find_weibo():
    """查找"""
    app = create_app()
    
    with app.app_context():
        print("=== 查找目标微博 ===\n")
        
        # 目标微博的MID
        target_mid = "11456415368239603"
        target_url_id = "QtaCga9AD"
        
        # 在数据库中查找
        post = WeiboPost.query.filter_by(weibo_id=target_mid).first()
        
        if post:
            print(f"✓ 找到目标微博！")
            print(f"  博主ID: {post.blogger_id}")
            print(f"  日期: {post.guess_date}")
            print(f"  轮次: {post.guess_round}")
            print(f"  内容: {post.content[:100]}...")
        else:
            print(f"✗ 未找到目标微博 (MID: {target_mid})")
            print(f"  URL ID: {target_url_id}")
            print(f"\n可能原因:")
            print("  1. 该微博从未被同步到数据库")
            print("  2. 同步时被过滤掉了（转发、非目标博主等）")
            print("  3. 同步时API没有返回这条数据")
        
        # 查找Mico林木森的所有微博
        mico = Blogger.query.filter_by(nickname='Mico林木森').first()
        if mico:
            print(f"\n\nMico林木森的所有微博:\n")
            posts = WeiboPost.query.filter(
                WeiboPost.blogger_id == mico.id
            ).order_by(WeiboPost.guess_date, WeiboPost.guess_round).all()
            
            for post in posts:
                print(f"  {post.guess_date} 轮次{post.guess_round}: {post.weibo_id}")

if __name__ == '__main__':
    find_weibo()
