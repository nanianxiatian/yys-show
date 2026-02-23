"""
检查夜神月竞猜统计数据
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db, Blogger, WeiboPost
from datetime import datetime, timedelta

def check_stats():
    """检查统计"""
    app = create_app()
    
    with app.app_context():
        # 查找夜神月
        blogger = Blogger.query.filter_by(nickname='夜神月Lwaite').first()
        if not blogger:
            print("✗ 未找到博主: 夜神月Lwaite")
            return
        
        print(f"✓ 找到博主: {blogger.nickname} (ID: {blogger.id})")
        print(f"  UID: {blogger.weibo_uid}")
        
        # 查询所有微博
        posts = WeiboPost.query.filter_by(blogger_id=blogger.id).order_by(WeiboPost.publish_time.desc()).all()
        
        print(f"\n数据库中共有 {len(posts)} 条微博:\n")
        
        for post in posts:
            print(f"微博ID: {post.weibo_id}")
            print(f"  发布时间: {post.publish_time}")
            print(f"  日期: {post.guess_date}")
            print(f"  轮次: {post.guess_round}")
            print(f"  预测: {post.guess_prediction} ({post.get_prediction_text()})")
            print(f"  是否竞猜相关: {post.is_guess_related}")
            print(f"  内容: {post.content[:80]}...")
            print()
        
        # 按日期统计
        print("="*60)
        print("\n按日期统计:")
        
        from sqlalchemy import func
        
        stats = db.session.query(
            WeiboPost.guess_date,
            func.count(WeiboPost.id).label('count'),
            WeiboPost.guess_prediction
        ).filter_by(blogger_id=blogger.id).group_by(WeiboPost.guess_date, WeiboPost.guess_prediction).all()
        
        for date, count, prediction in stats:
            print(f"  {date}: {prediction} - {count}条")

if __name__ == '__main__':
    check_stats()
