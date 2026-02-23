"""
检查yys方寒的微博
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db, Blogger, WeiboPost
from datetime import datetime, timedelta

def check():
    """检查"""
    app = create_app()
    
    with app.app_context():
        # 查找yys方寒
        blogger = Blogger.query.filter_by(nickname='yys方寒').first()
        if not blogger:
            print("✗ 未找到博主: yys方寒")
            return
        
        print(f"✓ 找到博主: {blogger.nickname} (ID: {blogger.id}, UID: {blogger.weibo_uid})")
        
        # 昨天14:00-16:00的时间范围
        yesterday = datetime.now() - timedelta(days=1)
        start_time = yesterday.replace(hour=14, minute=0, second=0, microsecond=0)
        end_time = yesterday.replace(hour=16, minute=0, second=0, microsecond=0)
        
        print(f"\n时间范围: {start_time} 到 {end_time}")
        
        # 查询该博主在这个时间段的微博
        posts = WeiboPost.query.filter(
            WeiboPost.blogger_id == blogger.id,
            WeiboPost.publish_time >= start_time,
            WeiboPost.publish_time <= end_time
        ).order_by(WeiboPost.publish_time.desc()).all()
        
        print(f"\n数据库中该时间段共有 {len(posts)} 条微博:\n")
        
        for post in posts:
            print(f"微博ID: {post.weibo_id}")
            print(f"  发布时间: {post.publish_time}")
            print(f"  预测: {post.guess_prediction} ({post.get_prediction_text()})")
            print(f"  内容: {post.content}")
            print()

if __name__ == '__main__':
    check()
