#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app

app = create_app()

with app.app_context():
    from app.models import SpiderLog, Blogger
    from sqlalchemy import desc
    
    # 查找yys方寒
    fanghan = Blogger.query.filter(Blogger.nickname.like('%方寒%')).first()
    if fanghan:
        print(f"找到博主: {fanghan.nickname}, ID: {fanghan.id}")
        print(f"微博ID: {fanghan.weibo_id}")
        print(f"主页URL: {fanghan.home_url}")
        
        # 查找该博主的所有爬虫记录
        print(f"\n{fanghan.nickname} 的所有爬虫记录:")
        blogger_logs = SpiderLog.query.filter_by(blogger_id=fanghan.id).order_by(desc(SpiderLog.created_at)).all()
        
        if not blogger_logs:
            print("  没有找到记录")
        else:
            for log in blogger_logs:
                print(f'\n  ID: {log.id}')
                print(f'  状态: {log.status}')
                print(f'  类型: {log.spider_type}')
                print(f'  开始时间: {log.start_time}')
                print(f'  结束时间: {log.end_time}')
                print(f'  抓取数量: {log.posts_count}')
                print(f'  错误信息: {log.error_message}')
                print(f'  创建时间: {log.created_at}')
        
        # 查找所有失败的记录
        print("\n" + "=" * 80)
        print("所有失败的爬虫记录（最近10条）:")
        print("=" * 80)
        failed_logs = SpiderLog.query.filter_by(status='failed').order_by(desc(SpiderLog.created_at)).limit(10).all()
        for log in failed_logs:
            blogger = Blogger.query.get(log.blogger_id) if log.blogger_id else None
            print(f'\n  ID: {log.id}, 博主: {blogger.nickname if blogger else "全部"}, 时间: {log.created_at}')
            print(f'  错误: {log.error_message[:200] if log.error_message else "无"}...')
    else:
        print("未找到博主")
