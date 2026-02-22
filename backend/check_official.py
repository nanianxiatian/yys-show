#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查官方结果数据
"""

from app import create_app
from app.models import OfficialResult
from datetime import date

app = create_app()

with app.app_context():
    # 检查2月22日的数据
    target_date = date(2025, 2, 22)
    results = OfficialResult.query.filter_by(guess_date=target_date).all()
    
    print(f"2025-02-22 官方结果: {len(results)}条")
    print("=" * 80)
    
    for r in results:
        print(f"\nID: {r.id}")
        print(f"日期: {r.guess_date}")
        print(f"轮次: {r.guess_round}")
        print(f"结果: {r.result}")
        print(f"左侧阵营: {r.left_team}")
        print(f"右侧阵营: {r.right_team}")
        print(f"to_dict(): {r.to_dict()}")
        print("-" * 80)
    
    # 检查所有日期的数据
    print("\n\n所有官方结果数据:")
    print("=" * 80)
    all_results = OfficialResult.query.order_by(OfficialResult.guess_date, OfficialResult.guess_round).all()
    for r in all_results:
        print(f"{r.guess_date} 第{r.guess_round}轮: {r.result}")
