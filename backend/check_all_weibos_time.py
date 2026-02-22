#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app

app = create_app()

with app.app_context():
    from app.services.weibo_spider import WeiboSpiderService
    from app.models import Blogger
    from datetime import datetime
    
    print("=" * 80)
    print("查看清流不加班所有微博的发布时间")
    print("=" * 80)
    
    blogger = Blogger.query.filter(Blogger.nickname.like('%清流%')).first()
    if not blogger:
        print("未找到博主")
        sys.exit(1)
    
    print(f"博主: {blogger.nickname}")
    print(f"UID: {blogger.weibo_uid}")
    print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    spider_service = WeiboSpiderService()
    crawler = spider_service._get_crawler()
    
    # 获取多页微博
    all_weibos = []
    for page in range(1, 4):
        weibo_list = crawler.get_user_weibo_list(blogger.weibo_uid, page=page, count=20)
        if not weibo_list:
            break
        all_weibos.extend(weibo_list)
        print(f"第{page}页获取到 {len(weibo_list)} 条微博")
    
    print(f"\n总共获取到 {len(all_weibos)} 条微博\n")
    print("=" * 80)
    
    # 按时间排序显示
    sorted_weibos = sorted(all_weibos, key=lambda x: x.get('publish_time') or datetime.min, reverse=True)
    
    print("\n微博发布时间列表（从新到旧）:\n")
    for i, weibo in enumerate(sorted_weibos):
        pub_time = weibo.get('publish_time')
        time_str = pub_time.strftime('%Y-%m-%d %H:%M:%S') if pub_time else '未知'
        content_preview = weibo.get('content', '')[:40]
        print(f"{i+1:2d}. {time_str} | {content_preview}...")
    
    # 检查最新微博的时间
    if sorted_weibos:
        latest = sorted_weibos[0]
        latest_time = latest.get('publish_time')
        if latest_time:
            days_ago = (datetime.now() - latest_time).days
            print(f"\n{'='*80}")
            print(f"最新微博发布时间: {latest_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"距离今天已经: {days_ago} 天")
            print(f"{'='*80}")
