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
    print("检查微博内容是否包含关键词'对弈竞猜'")
    print("=" * 80)
    
    blogger = Blogger.query.filter(Blogger.nickname.like('%清流%')).first()
    if not blogger:
        print("未找到博主")
        sys.exit(1)
    
    spider_service = WeiboSpiderService()
    crawler = spider_service._get_crawler()
    
    # 获取所有微博
    all_weibos = []
    for page in range(1, 4):
        weibo_list = crawler.get_user_weibo_list(blogger.weibo_uid, page=page, count=20)
        if not weibo_list:
            break
        all_weibos.extend(weibo_list)
    
    # 检查今天10-12点的微博
    start_dt = datetime.strptime("2026-02-22 10:00:00", '%Y-%m-%d %H:%M:%S')
    end_dt = datetime.strptime("2026-02-22 12:00:00", '%Y-%m-%d %H:%M:%S')
    
    print(f"\n今天10-12点的微博:\n")
    
    for weibo in all_weibos:
        pub_time = weibo.get('publish_time')
        if pub_time and start_dt <= pub_time <= end_dt:
            content = weibo.get('content', '')
            has_keyword = '对弈竞猜' in content
            print(f"发布时间: {pub_time}")
            print(f"包含'对弈竞猜': {has_keyword}")
            print(f"内容: {content}")
            print("-" * 80)
