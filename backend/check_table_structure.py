#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app
from app.models import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    # 检查表结构
    sql = "SHOW COLUMNS FROM weibo_posts"
    result = db.session.execute(text(sql))
    print("weibo_posts 表结构:")
    print("-" * 80)
    for row in result:
        print(f"  {row[0]}: {row[1]}")
