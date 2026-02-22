#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app

app = create_app()

with app.app_context():
    from app.models import SpiderLog, Blogger
    from sqlalchemy import desc
    
    print("=" * 80)
    print("最新的爬虫记录（最近5条）")
    print("=" * 80)
    
    logs = SpiderLog.query.order_by(desc(SpiderLog.created_at)).limit(5).all()
    for log in logs:
        blogger = Blogger.query.get(log.blogger_id) if log.blogger_id else None
        print(f'\nID: {log.id}')
        print(f'博主: {blogger.nickname if blogger else "全部博主"} (ID: {log.blogger_id})')
        print(f'类型: {log.spider_type}')
        print(f'状态: {log.status}')
        print(f'开始时间: {log.start_time}')
        print(f'结束时间: {log.end_time}')
        print(f'抓取数量: {log.posts_count}')
        print(f'错误信息: {log.error_message}')
        print("-" * 80)
    
    # 查找yys方寒的博主ID
    print("\n" + "=" * 80)
    print("查找博主 'yys方寒'")
    print("=" * 80)
    
    fanghan = Blogger.query.filter(Blogger.nickname.like('%方寒%')).first()
    if fanghan:
        print(f"找到博主: {fanghan.nickname}, ID: {fanghan.id}")
        
        # 查找该博主的最近记录
        print(f"\n{fanghan.nickname} 的最近爬虫记录:")
        blogger_logs = SpiderLog.query.filter_by(blogger_id=fanghan.id).order_by(desc(SpiderLog.created_at)).limit(5).all()
        for log in blogger_logs:
            print(f'  ID: {log.id}, 状态: {log.status}, 时间: {log.created_at}')
            if log.error_message:
                print(f'  错误: {log.error_message}')
    else:
        print("未找到博主 'yys方寒'")
        print("\n所有博主列表:")
        bloggers = Blogger.query.all()
        for b in bloggers:
            print(f"  - {b.nickname} (ID: {b.id})")
