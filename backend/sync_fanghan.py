#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app

app = create_app()

with app.app_context():
    from app.services import WeiboSpiderService
    from app.models import Blogger
    
    # 查找阴阳师方寒
    blogger = Blogger.query.filter(Blogger.nickname == '阴阳师方寒').first()
    if blogger:
        print(f"找到博主: {blogger.nickname}, ID: {blogger.id}")
        print(f"当前微博UID: {blogger.weibo_uid}")
        print(f"当前头像: {blogger.avatar_url}")
        
        print("\n开始同步博主信息...")
        print("-" * 80)
        
        spider_service = WeiboSpiderService()
        result = spider_service.sync_blogger_info(blogger.id)
        
        print("-" * 80)
        if result['success']:
            print(f"✅ 同步成功!")
            print(f"   UID: {result['data']['uid']}")
            print(f"   头像: {result['data']['avatar'][:50]}...")
            print(f"   描述: {result['data']['description'][:50]}...")
        else:
            print(f"❌ 同步失败: {result['error']}")
    else:
        print("未找到博主 '阴阳师方寒'")
