#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app

app = create_app()

with app.app_context():
    from app.models import Blogger
    from app.services import WeiboSpiderService
    
    # 查找所有博主，检查哪个同步失败
    print("=" * 80)
    print("检查所有博主信息")
    print("=" * 80)
    
    bloggers = Blogger.query.all()
    for b in bloggers:
        print(f"\nID: {b.id}, 昵称: {b.nickname}")
        print(f"   UID: {b.weibo_uid or 'None'}")
        print(f"   头像: {b.avatar_url or 'None'}")
        print(f"   是否启用: {b.is_active}")
    
    print("\n" + "=" * 80)
    print("尝试同步没有UID的博主...")
    print("=" * 80)
    
    spider_service = WeiboSpiderService()
    
    for b in bloggers:
        if not b.weibo_uid and b.is_active:
            print(f"\n尝试同步: {b.nickname} (ID: {b.id})")
            result = spider_service.sync_blogger_info(b.id)
            print(f"结果: {result}")
