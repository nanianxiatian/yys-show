"""
检查微博发布时间
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import WeiboPost
from datetime import datetime, timedelta

def check_time():
    """检查时间"""
    app = create_app()
    
    with app.app_context():
        # 检查两条微博
        weibo_ids = ['5269502239442384', '5269484910941738']
        
        for weibo_id in weibo_ids:
            post = WeiboPost.query.filter_by(weibo_id=weibo_id).first()
            if post:
                print(f"\n微博ID: {weibo_id}")
                print(f"  发布时间: {post.publish_time}")
                print(f"  博主ID: {post.blogger_id}")
                print(f"  预测: {post.guess_prediction}")
                
                # 检查是否在昨天14:00-16:00
                yesterday = datetime.now() - timedelta(days=1)
                start_time = yesterday.replace(hour=14, minute=0, second=0, microsecond=0)
                end_time = yesterday.replace(hour=16, minute=0, second=0, microsecond=0)
                
                in_range = start_time <= post.publish_time <= end_time
                print(f"  是否在 {start_time} 到 {end_time} 范围内: {in_range}")

if __name__ == '__main__':
    check_time()
