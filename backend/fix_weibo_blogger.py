"""
修复微博的博主ID
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db, Blogger, WeiboPost

def fix():
    """修复"""
    app = create_app()
    
    with app.app_context():
        # 获取鸽海成路
        blogger = Blogger.query.filter_by(nickname='鸽海成路').first()
        if not blogger:
            print("✗ 未找到博主: 鸽海成路")
            return
        
        print(f"✓ 找到博主: {blogger.nickname} (ID: {blogger.id}, UID: {blogger.weibo_uid})")
        
        # 修复微博 5269484910941738
        weibo_id = '5269484910941738'
        post = WeiboPost.query.filter_by(weibo_id=weibo_id).first()
        
        if post:
            old_blogger_id = post.blogger_id
            print(f"\n微博 {weibo_id}:")
            print(f"  当前博主ID: {old_blogger_id}")
            print(f"  应该改为: {blogger.id}")
            
            # 更新博主ID
            post.blogger_id = blogger.id
            db.session.commit()
            
            print(f"  ✓ 已修复")
            
            # 验证
            post = WeiboPost.query.filter_by(weibo_id=weibo_id).first()
            print(f"  新博主ID: {post.blogger_id}")
        else:
            print(f"✗ 未找到微博: {weibo_id}")

if __name__ == '__main__':
    fix()
