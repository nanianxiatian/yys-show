#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app
from app.services import WeiboSpiderService
from app.models import Blogger, db

app = create_app()

with app.app_context():
    # 获取徐清林
    blogger = Blogger.query.filter_by(nickname='春秋霸主徐清林').first()
    if not blogger:
        print("未找到博主")
        exit(1)
    
    print(f"博主: {blogger.nickname}, UID: {blogger.weibo_uid}")
    
    # 创建爬虫服务
    spider = WeiboSpiderService()
    
    # 测试爬虫
    print("\n开始爬取...")
    result = spider.spider_single_blogger(blogger.id)
    print(f"\n爬取结果: {result}")
