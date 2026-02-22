#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app

app = create_app()

with app.app_context():
    from app.models import Blogger, WeiboPost
    
    print("=" * 80)
    print("查找清流不加班博主")
    print("=" * 80)
    
    # 查找清流不加班
    blogger = Blogger.query.filter(Blogger.nickname.like('%清流%')).first()
    if blogger:
        print(f"找到博主: {blogger.nickname}")
        print(f"ID: {blogger.id}")
        print(f"UID: {blogger.weibo_uid}")
        print(f"是否启用: {blogger.is_active}")
        
        print("\n" + "=" * 80)
        print("查找该博主的所有微博")
        print("=" * 80)
        
        weibos = WeiboPost.query.filter_by(blogger_id=blogger.id).order_by(WeiboPost.publish_time.desc()).all()
        print(f"\n总共找到 {len(weibos)} 条微博")
        
        print("\n" + "-" * 80)
        print("按轮次分组:")
        print("-" * 80)
        
        from collections import defaultdict
        round_dict = defaultdict(list)
        
        for w in weibos:
            round_num = w.guess_round or '未分类'
            round_dict[round_num].append(w)
        
        for round_num in sorted(round_dict.keys(), key=lambda x: (x == '未分类', x)):
            ws = round_dict[round_num]
            print(f"\n第 {round_num} 轮: {len(ws)} 条")
            for w in ws[:3]:  # 只显示前3条
                print(f"  - ID: {w.id}, 时间: {w.publish_time}, 内容: {w.content[:50]}...")
            if len(ws) > 3:
                print(f"  ... 还有 {len(ws) - 3} 条")
    else:
        print("未找到清流不加班博主")
        print("\n所有博主:")
        bloggers = Blogger.query.all()
        for b in bloggers:
            print(f"  - {b.nickname} (ID: {b.id})")
