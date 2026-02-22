#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app

app = create_app()

with app.app_context():
    from app.models import Blogger, WeiboPost
    
    print("=" * 80)
    print("查看清流不加班的所有微博")
    print("=" * 80)
    
    blogger = Blogger.query.filter(Blogger.nickname.like('%清流%')).first()
    if not blogger:
        print("未找到博主")
        sys.exit(1)
    
    print(f"博主: {blogger.nickname}")
    print(f"UID: {blogger.weibo_uid}")
    print()
    
    weibos = WeiboPost.query.filter_by(blogger_id=blogger.id).order_by(WeiboPost.publish_time.desc()).all()
    print(f"总共 {len(weibos)} 条微博:\n")
    
    for w in weibos:
        print(f"ID: {w.id}")
        print(f"微博ID: {w.weibo_id}")
        print(f"发布时间: {w.publish_time}")
        print(f"轮次: {w.guess_round or '未分类'}")
        print(f"是否相关: {w.is_guess_related}")
        print(f"内容: {w.content[:200]}...")
        print("-" * 80)
