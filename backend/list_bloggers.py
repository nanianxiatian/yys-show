#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app

app = create_app()

with app.app_context():
    from app.models import Blogger
    
    print("=" * 80)
    print("所有博主列表")
    print("=" * 80)
    
    bloggers = Blogger.query.all()
    for b in bloggers:
        print(f"\nID: {b.id}")
        print(f"昵称: {b.nickname}")
        print(f"微博UID: {b.weibo_uid}")
        print(f"头像: {b.avatar_url[:50] if b.avatar_url else 'None'}...")
        print(f"描述: {b.description[:50] if b.description else 'None'}...")
        print("-" * 80)
