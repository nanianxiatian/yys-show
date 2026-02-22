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
    print("调试按时间段爬取问题")
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
    
    # 获取所有微博
    all_weibos = []
    for page in range(1, 4):
        weibo_list = crawler.get_user_weibo_list(blogger.weibo_uid, page=page, count=20)
        if not weibo_list:
            break
        all_weibos.extend(weibo_list)
    
    print(f"总共获取到 {len(all_weibos)} 条微博\n")
    
    # 测试不同的时间范围
    test_ranges = [
        ("2026-02-22 10:00:00", "2026-02-22 12:00:00", "今天10-12点"),
        ("2026-02-21 10:00:00", "2026-02-21 12:00:00", "昨天10-12点"),
        ("2026-02-21 00:00:00", "2026-02-21 23:59:59", "昨天全天"),
        ("2026-02-20 00:00:00", "2026-02-22 23:59:59", "最近3天"),
    ]
    
    for start_str, end_str, desc in test_ranges:
        print(f"\n{'='*80}")
        print(f"测试时间范围: {desc}")
        print(f"范围: {start_str} 到 {end_str}")
        print(f"{'='*80}")
        
        start_dt = datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S')
        end_dt = datetime.strptime(end_str, '%Y-%m-%d %H:%M:%S')
        
        # 手动过滤
        filtered = []
        for weibo in all_weibos:
            pub_time = weibo.get('publish_time')
            if pub_time and start_dt <= pub_time <= end_dt:
                filtered.append(weibo)
        
        print(f"匹配到 {len(filtered)} 条微博")
        for w in filtered[:3]:
            print(f"  - {w.get('publish_time')}: {w.get('content', '')[:50]}...")
