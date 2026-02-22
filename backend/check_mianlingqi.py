#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app

app = create_app()

with app.app_context():
    from app.models import Blogger
    from app.services import WeiboSpiderService
    
    # 查找面灵气喵
    blogger = Blogger.query.filter(Blogger.nickname.like('%面灵气%')).first()
    if blogger:
        print(f"找到博主: {blogger.nickname}, ID: {blogger.id}")
        print(f"当前微博UID: {blogger.weibo_uid}")
        print(f"当前头像: {blogger.avatar_url}")
        
        print("\n开始同步博主信息...")
        print("-" * 80)
        
        spider_service = WeiboSpiderService()
        result = spider_service.sync_blogger_info(blogger.id)
        
        print("-" * 80)
        print(f"同步结果: {result}")
    else:
        print("未找到博主 '面灵气喵'")
        print("\n所有博主:")
        bloggers = Blogger.query.all()
        for b in bloggers:
            print(f"  - {b.nickname} (ID: {b.id})")
