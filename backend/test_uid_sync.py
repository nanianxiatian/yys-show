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
    print("测试通过UID同步博主信息")
    print("=" * 80)
    
    # 测试ID 12 的新博主6033
    blogger = Blogger.query.get(12)
    if blogger:
        print(f"\n博主: {blogger.nickname}")
        print(f"当前UID: {blogger.weibo_uid}")
        print(f"当前头像: {blogger.avatar_url or 'None'}")
        print(f"当前描述: {blogger.description or 'None'}")
        
        print("\n开始同步...")
        print("-" * 80)
        
        spider_service = WeiboSpiderService()
        result = spider_service.sync_blogger_info(blogger.id)
        
        print("-" * 80)
        print(f"同步结果: {result}")
        
        # 重新查询查看最新状态
        blogger = Blogger.query.get(12)
        print(f"\n同步后状态:")
        print(f"  昵称: {blogger.nickname}")
        print(f"  UID: {blogger.weibo_uid}")
        print(f"  头像: {blogger.avatar_url or 'None'}")
        print(f"  描述: {blogger.description or 'None'}")
    else:
        print("未找到ID为12的博主")
