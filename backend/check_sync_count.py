"""
检查同步数量差异
"""
import sys
import os
from datetime import datetime, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import WeiboPost, Blogger, db
from sqlalchemy import func

def check_sync_count():
    """检查同步数量"""
    app = create_app()
    
    with app.app_context():
        print("=== 检查2026-02-20 22-24点同步数量 ===\n")
        
        # 查询所有博主
        bloggers = Blogger.query.filter_by(is_active=True).all()
        
        for blogger in bloggers:
            # 查询该博主在指定时间段的微博
            posts = WeiboPost.query.filter(
                WeiboPost.blogger_id == blogger.id,
                WeiboPost.guess_date == '2026-02-20',
                WeiboPost.guess_round.in_([5, 6])  # 22点和24点对应第5、6轮
            ).all()
            
            if posts:
                print(f"\n博主: {blogger.nickname}")
                print(f"  总微博数: {len(posts)}")
                for post in posts:
                    print(f"    - ID: {post.id}, 轮次: {post.guess_round}, 时间: {post.created_at}")
        
        # 统计总数
        total = WeiboPost.query.filter(
            WeiboPost.guess_date == '2026-02-20',
            WeiboPost.guess_round.in_([5, 6])
        ).count()
        
        print(f"\n\n总计: {total} 条微博")
        
        # 检查Mico林木森 2026-02-23 16-18点
        print("\n\n=== 检查Mico林木森 2026-02-23 16-18点 ===\n")
        
        mico = Blogger.query.filter_by(nickname='Mico林木森').first()
        if mico:
            print(f"找到博主: {mico.nickname} (ID: {mico.id})")
            
            # 查询该博主在指定日期的所有微博
            posts = WeiboPost.query.filter(
                WeiboPost.blogger_id == mico.id,
                WeiboPost.guess_date == '2026-02-23'
            ).all()
            
            print(f"\n2026-02-23 所有微博 ({len(posts)} 条):")
            for post in posts:
                print(f"  - ID: {post.id}, 轮次: {post.guess_round}, 时间: {post.created_at}")
                print(f"    内容: {post.content[:50]}...")
        else:
            print("未找到博主 Mico林木森")
            # 列出所有博主
            all_bloggers = Blogger.query.all()
            print(f"\n所有博主 ({len(all_bloggers)} 个):")
            for b in all_bloggers:
                print(f"  - {b.nickname} (ID: {b.id})")

if __name__ == '__main__':
    check_sync_count()
