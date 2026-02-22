#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app

app = create_app()

with app.app_context():
    from app.models import Blogger, db
    
    # 查找ID为7的yys方寒（新添加的）
    blogger = Blogger.query.get(7)
    if blogger and '方寒' in blogger.nickname:
        print(f"找到博主: {blogger.nickname}, ID: {blogger.id}")
        print(f"当前微博UID: {blogger.weibo_uid}")
        
        # 直接设置UID
        blogger.weibo_uid = '7596104274'
        db.session.commit()
        
        print(f"\n✅ 已更新博主UID为: {blogger.weibo_uid}")
        print("现在可以正常爬取该博主的微博了！")
    else:
        print(f"未找到ID为7的博主或昵称不包含'方寒'")
        # 列出所有博主
        print("\n所有博主:")
        all_bloggers = Blogger.query.all()
        for b in all_bloggers:
            print(f"  ID: {b.id}, 昵称: {b.nickname}, UID: {b.weibo_uid}")
