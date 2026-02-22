#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app
from app.models import db, WeiboPost, Blogger

app = create_app()

with app.app_context():
    # 查找徐清林的微博
    blogger = Blogger.query.filter_by(nickname='春秋霸主徐清林').first()
    if blogger:
        print(f"博主: {blogger.nickname}, ID: {blogger.id}")
        posts = WeiboPost.query.filter_by(blogger_id=blogger.id).order_by(WeiboPost.id.desc()).all()
        print(f"共有 {len(posts)} 条微博\n")
        
        for post in posts:
            print(f"微博ID: {post.weibo_id}")
            print(f"内容: {post.content[:80]}...")
            print(f"是否相关: {post.is_guess_related}")
            print(f"预测结果: {post.guess_prediction}")
            print(f"轮次: {post.guess_round}")
            print(f"日期: {post.guess_date}")
            print("---")
    else:
        print("未找到博主")
