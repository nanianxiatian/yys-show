#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
修复卡住的爬虫日志状态
"""
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app
from app.models import SpiderLog, db
from datetime import datetime, timedelta
from sqlalchemy import desc

app = create_app()

with app.app_context():
    print("=" * 80)
    print("修复卡住的爬虫日志")
    print("=" * 80)
    
    # 找出所有运行中的任务
    running_logs = SpiderLog.query.filter_by(status='running').all()
    
    print(f"\n发现 {len(running_logs)} 个运行中的任务")
    
    fixed_count = 0
    for log in running_logs:
        # 如果任务开始时间超过10分钟还没有结束，认为是卡住的任务
        if log.start_time:
            elapsed = datetime.now() - log.start_time
            if elapsed > timedelta(minutes=10):
                print(f"\n修复任务 ID: {log.id}")
                print(f"  类型: {log.spider_type}")
                print(f"  开始时间: {log.start_time}")
                print(f"  已运行: {elapsed}")
                
                # 将状态改为失败
                log.status = 'failed'
                log.end_time = datetime.now()
                log.error_message = '任务异常终止或超时'
                fixed_count += 1
                print(f"  ✅ 已修复为失败状态")
    
    if fixed_count > 0:
        db.session.commit()
        print(f"\n共修复 {fixed_count} 个任务")
    else:
        print("\n没有需要修复的任务")
    
    print("\n" + "=" * 80)
    
    # 显示修复后的统计
    running_count = SpiderLog.query.filter_by(status='running').count()
    success_count = SpiderLog.query.filter_by(status='success').count()
    failed_count = SpiderLog.query.filter_by(status='failed').count()
    
    print("修复后的统计:")
    print(f"  运行中: {running_count}")
    print(f"  成功: {success_count}")
    print(f"  失败: {failed_count}")
    
    print("\n" + "=" * 80)
