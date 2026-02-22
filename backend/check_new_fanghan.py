#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app

app = create_app()

with app.app_context():
    from app.models import Blogger
    from app.services import WeiboSpiderService
    
    # 查找所有包含"方寒"的博主
    print("=" * 80)
    print("查找所有包含'方寒'的博主")
    print("=" * 80)
    
    bloggers = Blogger.query.filter(Blogger.nickname.like('%方寒%')).all()
    for b in bloggers:
        print(f"\nID: {b.id}")
        print(f"昵称: {b.nickname}")
        print(f"微博UID: {b.weibo_uid}")
        print(f"头像: {b.avatar_url}")
        print(f"描述: {b.description}")
        print(f"是否启用: {b.is_active}")
        print("-" * 80)
    
    # 尝试同步最新的一个
    if bloggers:
        latest = bloggers[-1]
        print(f"\n尝试同步博主: {latest.nickname} (ID: {latest.id})")
        print("-" * 80)
        
        spider_service = WeiboSpiderService()
        result = spider_service.sync_blogger_info(latest.id)
        
        print("-" * 80)
        print(f"同步结果: {result}")
