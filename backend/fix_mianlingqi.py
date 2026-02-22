#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app

app = create_app()

with app.app_context():
    from app.models import Blogger, db
    
    # 查找面灵气喵
    blogger = Blogger.query.filter(Blogger.nickname == '面灵气喵').first()
    if blogger:
        print(f"找到博主: {blogger.nickname}, ID: {blogger.id}")
        print(f"当前微博UID: {blogger.weibo_uid}")
        print(f"主页URL: {blogger.weibo_url if hasattr(blogger, 'weibo_url') else 'N/A'}")
        
        # 如果你有该博主的微博主页URL或UID，请在这里设置
        # 例如：https://weibo.com/u/xxxxxx
        # UID通常是URL中的数字部分
        
        # 尝试从weibo_url中提取UID
        if hasattr(blogger, 'weibo_url') and blogger.weibo_url:
            import re
            match = re.search(r'/u/(\d+)', blogger.weibo_url)
            if match:
                uid = match.group(1)
                blogger.weibo_uid = uid
                db.session.commit()
                print(f"\n✅ 已从URL提取并更新UID: {uid}")
            else:
                print("\n⚠️ 无法从URL提取UID")
                print("请提供该博主的微博UID或主页URL")
        else:
            print("\n⚠️ 博主没有设置weibo_url")
            print("请提供该博主的微博UID")
    else:
        print("未找到博主 '面灵气喵'")
