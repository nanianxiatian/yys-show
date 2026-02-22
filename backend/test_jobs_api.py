#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app

app = create_app()

with app.app_context():
    from app.services import SchedulerService
    
    scheduler = SchedulerService()
    
    # 启动调度器
    scheduler.start()
    
    # 获取任务列表
    jobs = scheduler.get_jobs()
    print("=" * 80)
    print(f"获取到 {len(jobs)} 个任务")
    print("=" * 80)
    
    for job in jobs:
        print(f"\n任务: {job}")
    
    # 关闭调度器
    scheduler.shutdown()
