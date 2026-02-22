#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
添加 pic_urls 字段到 weibo_posts 表
"""
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app
from app.models import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    # 执行SQL添加字段
    sql = """
    ALTER TABLE weibo_posts 
    ADD COLUMN pic_urls TEXT COMMENT '微博图片URL列表(JSON数组)' 
    AFTER is_guess_related
    """
    
    try:
        db.session.execute(text(sql))
        db.session.commit()
        print("✅ 成功添加 pic_urls 字段到 weibo_posts 表")
    except Exception as e:
        db.session.rollback()
        if "Duplicate column name" in str(e) or "already exists" in str(e):
            print("⚠️ 字段已存在，无需添加")
        else:
            print(f"❌ 添加字段失败: {e}")
