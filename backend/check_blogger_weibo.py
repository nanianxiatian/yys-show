#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查博主微博数据
"""

from app import create_app
from app.models import WeiboPost, Blogger

app = create_app()

with app.app_context():
    # 查找鸽海成路博主ID
    blogger = Blogger.query.filter_by(nickname='鸽海成路').first()
    
    if not blogger:
        print("未找到博主: 鸽海成路")
    else:
        print(f"博主信息:")
        print(f"  ID: {blogger.id}")
        print(f"  昵称: {blogger.nickname}")
        print(f"  UID: {blogger.weibo_uid}")
        print()
        
        # 查找该博主的所有微博
        posts = WeiboPost.query.filter_by(blogger_id=blogger.id)\
            .order_by(WeiboPost.publish_time.desc()).all()
        
        print(f"共有 {len(posts)} 条微博:\n")
        
        for post in posts:
            print(f"微博ID: {post.weibo_id}")
            print(f"发布时间: {post.publish_time}")
            print(f"竞猜日期: {post.guess_date}")
            print(f"竞猜轮次: {post.guess_round}")
            print(f"预测: {post.guess_prediction}")
            print(f"内容: {post.content[:50]}...")
            print("-" * 80)
