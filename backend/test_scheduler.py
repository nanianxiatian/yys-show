#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app

app = create_app()

with app.app_context():
    from app.services import SchedulerService
    
    scheduler = SchedulerService()
    
    # 获取任务列表
    jobs = scheduler.get_jobs()
    print("=" * 80)
    print("定时任务列表")
    print("=" * 80)
    
    for job in jobs:
        print(f"\n任务ID: {job['id']}")
        print(f"任务名称: {job['name']}")
        print(f"下次执行时间: {job['next_run_time']}")
        print(f"触发规则: {job['trigger']}")
    
    print("\n" + "=" * 80)
    
    # 检查调度器状态
    print(f"\n调度器运行状态: {scheduler._scheduler.running}")
    
    # 获取原始任务对象
    for job in scheduler._scheduler.get_jobs():
        print(f"\n任务 {job.id}:")
        print(f"  next_run_time: {job.next_run_time}")
