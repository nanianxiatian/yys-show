#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app

app = create_app()

with app.app_context():
    from app.models import Blogger, db
    
    # 查找yys方寒
    blogger = Blogger.query.filter(Blogger.nickname == 'yys方寒').first()
    if blogger:
        print(f"找到博主: {blogger.nickname}, ID: {blogger.id}")
        print(f"当前微博UID: {blogger.weibo_uid}")
        
        # 更新昵称为正确的微博昵称
        old_nickname = blogger.nickname
        blogger.nickname = '阴阳师方寒'
        db.session.commit()
        
        print(f"\n✅ 已更新昵称: {old_nickname} -> {blogger.nickname}")
        
        # 现在尝试同步博主信息
        print("\n开始同步博主信息...")
        from app.services import WeiboSpiderService
        spider_service = WeiboSpiderService()
        result = spider_service.sync_blogger_info(blogger.id)
        
        if result['success']:
            print(f"✅ 同步成功!")
            print(f"   UID: {result['data']['uid']}")
            print(f"   头像: {result['data']['avatar']}")
            print(f"   描述: {result['data']['description']}")
        else:
            print(f"❌ 同步失败: {result['error']}")
    else:
        print("未找到博主 'yys方寒'")
