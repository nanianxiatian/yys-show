"""
检查第4轮（14:00-16:00）的微博
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import WeiboPost, Blogger
from datetime import datetime

def check():
    """检查"""
    app = create_app()
    
    with app.app_context():
        print("=== 检查2026-02-23 14:00-16:00（第4轮）的微博 ===\n")
        
        # 查找Mico林木森
        mico = Blogger.query.filter_by(nickname='Mico林木森').first()
        if not mico:
            print("未找到博主")
            return
        
        print(f"博主: {mico.nickname} (ID: {mico.id})\n")
        
        # 查询2026-02-23的所有微博
        posts = WeiboPost.query.filter(
            WeiboPost.blogger_id == mico.id,
            WeiboPost.guess_date == '2026-02-23'
        ).order_by(WeiboPost.guess_round).all()
        
        print("数据库中2026-02-23的微博:\n")
        for post in posts:
            print(f"  轮次 {post.guess_round}: {post.weibo_id}")
            print(f"    时间: {post.created_at}")
            print(f"    内容: {post.content[:80]}...")
            print()
        
        # 特别检查第4轮
        round4 = WeiboPost.query.filter(
            WeiboPost.blogger_id == mico.id,
            WeiboPost.guess_date == '2026-02-23',
            WeiboPost.guess_round == 4
        ).first()
        
        if round4:
            print("✓ 第4轮（14:00-16:00）存在！")
            print(f"  ID: {round4.weibo_id}")
            print(f"  内容: {round4.content}")
        else:
            print("✗ 第4轮（14:00-16:00）缺失！")
            print("  这就是截图中的那条微博没有同步到的原因")

if __name__ == '__main__':
    check()
