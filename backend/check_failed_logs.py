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
    print("失败的爬虫记录")
    print("=" * 80)
    
    logs = SpiderLog.query.filter_by(status='failed').order_by(desc(SpiderLog.created_at)).limit(10).all()
    if not logs:
        print("\n没有失败的记录")
    else:
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
    
    print("\n" + "=" * 80)
    print("运行中的爬虫记录")
    print("=" * 80)
    
    running_logs = SpiderLog.query.filter_by(status='running').order_by(desc(SpiderLog.created_at)).limit(10).all()
    if not running_logs:
        print("\n没有运行中的记录")
    else:
        for log in running_logs:
            blogger = Blogger.query.get(log.blogger_id) if log.blogger_id else None
            print(f'\nID: {log.id}')
            print(f'博主: {blogger.nickname if blogger else "全部博主"} (ID: {log.blogger_id})')
            print(f'类型: {log.spider_type}')
            print(f'状态: {log.status}')
            print(f'开始时间: {log.start_time}')
            print(f'错误信息: {log.error_message}')
            print("-" * 80)
