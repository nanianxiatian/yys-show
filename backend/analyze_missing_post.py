"""
分析缺失的微博
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import WeiboPost, Blogger
from datetime import datetime

def analyze():
    """分析"""
    app = create_app()
    
    with app.app_context():
        print("=== 分析缺失的微博 ===\n")
        
        # 用户提供的微博ID
        target_weibo_id = "QtaCga9AD"
        
        # 检查数据库中是否有这条微博
        # 先查找所有Mico林木森的微博
        mico = Blogger.query.filter_by(nickname='Mico林木森').first()
        if not mico:
            print("未找到博主")
            return
        
        print(f"博主: {mico.nickname} (ID: {mico.id})")
        print(f"UID: {mico.weibo_uid}\n")
        
        # 查找2026-02-23的所有微博
        posts = WeiboPost.query.filter(
            WeiboPost.blogger_id == mico.id,
            WeiboPost.guess_date == '2026-02-23'
        ).order_by(WeiboPost.guess_round).all()
        
        print("2026-02-23 的微博:\n")
        for post in posts:
            print(f"  轮次 {post.guess_round}: {post.weibo_id}")
            print(f"    创建时间: {post.created_at}")
            print(f"    内容: {post.content[:60]}...")
            print()
        
        # 检查微博ID的格式
        print("\n微博ID分析:")
        print(f"  目标微博ID: {target_weibo_id}")
        print(f"  数据库中的ID格式: {posts[0].weibo_id if posts else 'N/A'}")
        
        # 检查是否有第4轮
        round4 = WeiboPost.query.filter(
            WeiboPost.blogger_id == mico.id,
            WeiboPost.guess_date == '2026-02-23',
            WeiboPost.guess_round == 4
        ).first()
        
        if round4:
            print(f"\n✓ 第4轮微博存在: {round4.weibo_id}")
        else:
            print("\n✗ 第4轮微博不存在")
            print("  这意味着 14:00-16:00 的微博确实没有同步到")
        
        # 检查第5轮的时间
        round5 = WeiboPost.query.filter(
            WeiboPost.blogger_id == mico.id,
            WeiboPost.guess_date == '2026-02-23',
            WeiboPost.guess_round == 5
        ).first()
        
        if round5:
            print(f"\n第5轮微博信息:")
            print(f"  ID: {round5.weibo_id}")
            print(f"  内容: {round5.content[:100]}...")
            print(f"  创建时间: {round5.created_at}")
            
            # 检查内容是否包含16:00或18:00相关信息
            if '16:00' in round5.content or '18:00' in round5.content:
                print("  ✓ 内容包含时间信息")

if __name__ == '__main__':
    analyze()
