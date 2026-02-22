#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app

app = create_app()

with app.app_context():
    from app.services.weibo_spider import WeiboSpiderService
    
    print("=" * 80)
    print("手动爬取清流不加班的微博")
    print("=" * 80)
    
    spider_service = WeiboSpiderService()
    
    # 获取博主信息
    from app.models import Blogger
    blogger = Blogger.query.filter(Blogger.nickname.like('%清流%')).first()
    
    if not blogger:
        print("未找到博主")
        sys.exit(1)
    
    print(f"博主: {blogger.nickname}")
    print(f"UID: {blogger.weibo_uid}")
    print()
    
    # 手动爬取微博
    print("开始爬取微博...")
    result = spider_service.spider_single_blogger(blogger.id, keyword='对弈竞猜')
    
    print(f"\n爬取结果: {result}")
