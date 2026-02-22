#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app

app = create_app()

with app.app_context():
    from app.services.weibo_spider import WeiboSpiderService
    from app.models import Blogger
    from datetime import datetime, timedelta
    
    print("=" * 80)
    print("测试按时间段爬取清流不加班的微博")
    print("=" * 80)
    
    # 获取博主信息
    blogger = Blogger.query.filter(Blogger.nickname.like('%清流%')).first()
    if not blogger:
        print("未找到博主")
        sys.exit(1)
    
    print(f"博主: {blogger.nickname}")
    print(f"UID: {blogger.weibo_uid}")
    print()
    
    # 设置时间范围：今天 10:00 - 12:00
    today = datetime.now().strftime('%Y-%m-%d')
    start_time = f"{today} 10:00:00"
    end_time = f"{today} 12:00:00"
    
    print(f"时间范围: {start_time} 到 {end_time}")
    print()
    
    spider_service = WeiboSpiderService()
    
    # 测试直接调用爬虫获取微博列表
    print("=" * 80)
    print("步骤1: 直接获取用户微博列表")
    print("=" * 80)
    
    crawler = spider_service._get_crawler()
    weibo_list = crawler.get_user_weibo_list(blogger.weibo_uid, page=1, count=20)
    
    print(f"获取到 {len(weibo_list)} 条微博:\n")
    
    for i, weibo in enumerate(weibo_list[:5]):  # 只显示前5条
        print(f"[{i+1}] 微博ID: {weibo.get('weibo_id')}")
        print(f"    发布时间: {weibo.get('publish_time')}")
        print(f"    内容: {weibo.get('content', '')[:100]}...")
        print()
    
    # 测试按时间段获取
    print("=" * 80)
    print("步骤2: 按时间段获取微博")
    print("=" * 80)
    
    time_range_weibos = crawler.get_weibo_by_time_range(
        blogger.weibo_uid,
        start_time,
        end_time,
        keyword=None
    )
    
    print(f"时间段内获取到 {len(time_range_weibos)} 条微博:\n")
    
    for weibo in time_range_weibos:
        print(f"微博ID: {weibo.get('weibo_id')}")
        print(f"发布时间: {weibo.get('publish_time')}")
        print(f"内容: {weibo.get('content', '')[:100]}...")
        print()
