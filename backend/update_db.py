#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
更新数据库表结构 - 添加图片URL和微博链接字段
"""
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app
from app.models import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    # 添加 pic_urls 字段
    try:
        db.session.execute(text("""
            ALTER TABLE weibo_posts 
            ADD COLUMN pic_urls TEXT COMMENT '微博图片URL列表(JSON数组)'
        """))
        print("✅ 添加 pic_urls 字段成功")
    except Exception as e:
        if 'Duplicate column' in str(e) or 'already exists' in str(e):
            print("⚠️ pic_urls 字段已存在")
        else:
            print(f"❌ 添加 pic_urls 字段失败: {e}")
    
    # 添加 weibo_url 字段
    try:
        db.session.execute(text("""
            ALTER TABLE weibo_posts 
            ADD COLUMN weibo_url VARCHAR(500) COMMENT '微博原链接'
        """))
        print("✅ 添加 weibo_url 字段成功")
    except Exception as e:
        if 'Duplicate column' in str(e) or 'already exists' in str(e):
            print("⚠️ weibo_url 字段已存在")
        else:
            print(f"❌ 添加 weibo_url 字段失败: {e}")
    
    db.session.commit()
    print("\n数据库更新完成！")
