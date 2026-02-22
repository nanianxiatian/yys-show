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
    if not blogger:
        # 尝试查找阴阳师方寒
        blogger = Blogger.query.filter(Blogger.nickname == '阴阳师方寒').first()
    
    if blogger:
        print(f"找到博主: {blogger.nickname}, ID: {blogger.id}")
        print(f"当前微博UID: {blogger.weibo_uid}")
        
        # 更新为正确的昵称和UID
        blogger.nickname = 'yys方寒'
        blogger.weibo_uid = '7596104274'
        db.session.commit()
        
        print(f"\n✅ 已更新博主信息:")
        print(f"   昵称: {blogger.nickname}")
        print(f"   UID: {blogger.weibo_uid}")
        
        # 尝试获取头像和描述
        print("\n尝试获取头像和描述...")
        from app.services import WeiboSpiderService
        spider_service = WeiboSpiderService()
        result = spider_service.sync_blogger_info(blogger.id)
        
        if result['success']:
            print(f"✅ 同步成功!")
            print(f"   头像: {result['data']['avatar'][:50] if result['data']['avatar'] else 'None'}...")
            print(f"   描述: {result['data']['description'][:50] if result['data']['description'] else 'None'}...")
        else:
            print(f"⚠️ 同步详细信息失败: {result['error']}")
            print("   但基本的UID已更新，可以正常爬取微博")
    else:
        print("未找到博主，创建新博主...")
        # 创建新博主
        new_blogger = Blogger(
            nickname='yys方寒',
            weibo_uid='7596104274',
            is_active=True
        )
        db.session.add(new_blogger)
        db.session.commit()
        print(f"✅ 已创建博主: {new_blogger.nickname}, ID: {new_blogger.id}")
