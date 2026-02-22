#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查数据库中的官方结果和微博数据
"""

from app import create_app
from app.models import db, OfficialResult, WeiboPost
from datetime import date

app = create_app()

with app.app_context():
    # 检查官方结果
    print("=" * 80)
    print("官方结果数据:")
    print("=" * 80)
    
    for d in ['2025-02-17', '2025-02-18', '2025-02-19', '2025-02-20', '2025-02-21', '2025-02-22']:
        target_date = date.fromisoformat(d)
        results = OfficialResult.query.filter_by(guess_date=target_date).all()
        print(f"\n{d}: {len(results)}条记录")
    
    # 检查所有微博数据（不看is_guess_related）
    print("\n" + "=" * 80)
    print("所有微博数据（按日期）:")
    print("=" * 80)
    
    for d in ['2025-02-17', '2025-02-18', '2025-02-19', '2025-02-20', '2025-02-21', '2025-02-22']:
        target_date = date.fromisoformat(d)
        posts = WeiboPost.query.filter_by(guess_date=target_date).all()
        print(f"\n{d}: {len(posts)}条微博")
        if posts:
            for p in posts[:5]:
                print(f"  博主{p.blogger_id}: 相关={p.is_guess_related}, 预测={p.guess_prediction}, 轮次={p.guess_round}")
                print(f"    内容: {p.content[:50]}...")
    
    # 检查所有微博（不限日期）
    print("\n" + "=" * 80)
    print("数据库中所有微博统计:")
    print("=" * 80)
    total = WeiboPost.query.count()
    related = WeiboPost.query.filter_by(is_guess_related=True).count()
    print(f"总微博数: {total}")
    print(f"相关微博数: {related}")
    
    # 查看所有guess_date分布
    print("\n" + "=" * 80)
    print("微博日期分布:")
    print("=" * 80)
    from sqlalchemy import func
    dates = db.session.query(WeiboPost.guess_date, func.count(WeiboPost.id)).group_by(WeiboPost.guess_date).all()
    for d, count in dates:
        print(f"  {d}: {count}条")
