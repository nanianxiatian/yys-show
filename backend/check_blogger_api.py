#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app

app = create_app()

with app.app_context():
    from app.models import Blogger
    
    print("=" * 80)
    print("检查所有博主信息")
    print("=" * 80)
    
    # 获取所有博主
    all_bloggers = Blogger.query.all()
    print(f"\n数据库中共有 {len(all_bloggers)} 个博主:\n")
    
    for b in all_bloggers:
        print(f"ID: {b.id}, 昵称: {b.nickname}, 启用: {b.is_active}, UID: {b.weibo_uid}")
    
    # 查找段段及南墙
    print("\n" + "=" * 80)
    print("查找包含'段段'的博主:")
    print("=" * 80)
    
    duan_bloggers = Blogger.query.filter(Blogger.nickname.like('%段段%')).all()
    if duan_bloggers:
        for b in duan_bloggers:
            print(f"找到: {b.nickname} (ID: {b.id}, is_active: {b.is_active})")
    else:
        print("未找到包含'段段'的博主")
    
    # 检查is_active筛选
    print("\n" + "=" * 80)
    print("启用的博主 (is_active=True):")
    print("=" * 80)
    
    active_bloggers = Blogger.query.filter_by(is_active=True).all()
    for b in active_bloggers:
        print(f"- {b.nickname} (ID: {b.id})")
