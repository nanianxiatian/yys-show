#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app

app = create_app()

with app.app_context():
    from app.models import Blogger
    from app.services import WeiboSpiderService
    
    print("=" * 80)
    print("检查所有博主并尝试同步")
    print("=" * 80)
    
    bloggers = Blogger.query.all()
    spider_service = WeiboSpiderService()
    
    for b in bloggers:
        print(f"\n{'='*60}")
        print(f"博主: {b.nickname} (ID: {b.id})")
        print(f"当前UID: {b.weibo_uid or 'None'}")
        print(f"当前头像: {b.avatar_url or 'None'}")
        
        if b.is_active:
            print("尝试同步...")
            result = spider_service.sync_blogger_info(b.id)
            print(f"结果: {result}")
        else:
            print("博主已禁用，跳过同步")
