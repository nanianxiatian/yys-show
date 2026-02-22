#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app
from app.models import db, WeiboPost

app = create_app()

with app.app_context():
    posts = WeiboPost.query.all()
    print(f"共有 {len(posts)} 条微博记录\n")
    for post in posts:
        print(f'ID: {post.id}, 微博ID: {post.weibo_id}')
        print(f'博主: {post.blogger.nickname if post.blogger else "未知"}')
        print(f'图片URL: {post.pic_urls}')
        print(f'微博链接: {post.weibo_url}')
        print('---')
