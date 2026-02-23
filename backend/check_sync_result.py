"""
检查同步结果
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db, Blogger, WeiboPost
from datetime import datetime, timedelta

def check_sync():
    """检查同步结果"""
    app = create_app()
    
    with app.app_context():
        # 查找博主
        blogger = Blogger.query.filter_by(nickname='春秋霸主徐清林').first()
        if not blogger:
            print("✗ 未找到博主")
            return
        
        print(f"博主: {blogger.nickname} (ID: {blogger.id})")
        
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
            print(f"  内容: {post.content[:100]}...")
            print()
        
        # 检查所有微博ID
        all_weibo_ids = ['5269506997880742', '5269504173280197', '5269485968690787']
        print("="*50)
        print("检查特定微博ID:")
        for weibo_id in all_weibo_ids:
            post = WeiboPost.query.filter_by(weibo_id=weibo_id).first()
            if post:
                print(f"  ✓ {weibo_id}: 存在 (预测: {post.guess_prediction})")
            else:
                print(f"  ✗ {weibo_id}: 不存在")

if __name__ == '__main__':
    check_sync()
