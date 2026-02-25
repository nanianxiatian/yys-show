"""
检查特定微博
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import WeiboPost, Blogger

def check():
    """检查"""
    app = create_app()
    
    with app.app_context():
        print("=== 检查Mico林木森微博 ===\n")
        
        # 查找Mico林木森
        blogger = Blogger.query.filter_by(nickname='Mico林木森').first()
        if not blogger:
            print("未找到博主")
            return
        
        print(f"博主: {blogger.nickname} (ID: {blogger.id})")
        print(f"UID: {blogger.weibo_uid}\n")
        
        # 查询2026-02-23的所有微博
        posts = WeiboPost.query.filter(
            WeiboPost.blogger_id == blogger.id,
            WeiboPost.guess_date == '2026-02-23'
        ).order_by(WeiboPost.guess_round).all()
        
        print(f"2026-02-23 共有 {len(posts)} 条微博:\n")
        
        for post in posts:
            print(f"  轮次: {post.guess_round}, 微博ID: {post.weibo_id}")
            print(f"  发布时间: {post.created_at}")
            print(f"  内容: {post.content[:100]}...")
            print()
        
        # 检查是否有第4轮（14:00-16:00）的微博
        round4 = WeiboPost.query.filter(
            WeiboPost.blogger_id == blogger.id,
            WeiboPost.guess_date == '2026-02-23',
            WeiboPost.guess_round == 4
        ).first()
        
        if round4:
            print("✓ 找到第4轮(14:00-16:00)微博")
        else:
            print("✗ 未找到第4轮(14:00-16:00)微博")
        
        # 检查是否有第5轮（16:00-18:00）的微博
        round5 = WeiboPost.query.filter(
            WeiboPost.blogger_id == blogger.id,
            WeiboPost.guess_date == '2026-02-23',
            WeiboPost.guess_round == 5
        ).first()
        
        if round5:
            print("✓ 找到第5轮(16:00-18:00)微博")
            print(f"  内容: {round5.content[:100]}...")
        else:
            print("✗ 未找到第5轮(16:00-18:00)微博")

if __name__ == '__main__':
    check()
