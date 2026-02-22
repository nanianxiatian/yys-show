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
    print("检查所有博主并尝试同步最新添加的")
    print("=" * 80)
    
    # 获取所有博主，按ID倒序查看最新的
    bloggers = Blogger.query.order_by(Blogger.id.desc()).all()
    
    print("\n所有博主列表（按ID倒序）:")
    print("-" * 80)
    for b in bloggers:
        print(f"ID: {b.id}, 昵称: {b.nickname}, UID: {b.weibo_uid or 'None'}, 启用: {b.is_active}")
    
    # 尝试同步最新的一个博主
    if bloggers:
        latest = bloggers[0]
        print(f"\n{'='*80}")
        print(f"尝试同步最新博主: {latest.nickname} (ID: {latest.id})")
        print(f"当前UID: {latest.weibo_uid or 'None'}")
        print(f"当前头像: {latest.avatar_url or 'None'}")
        print("=" * 80)
        
        spider_service = WeiboSpiderService()
        result = spider_service.sync_blogger_info(latest.id)
        
        print(f"\n同步结果: {result}")
