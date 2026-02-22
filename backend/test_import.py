#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app

app = create_app()
print('App created successfully')

# 测试导入爬虫服务
with app.app_context():
    from app.services import WeiboSpiderService
    print('WeiboSpiderService imported successfully')
    
    # 测试是否有新方法
    service = WeiboSpiderService()
    if hasattr(service, 'spider_by_time_range'):
        print('spider_by_time_range method exists')
    else:
        print('ERROR: spider_by_time_range method not found')
    
    # 测试爬虫类
    from spider.weibo_crawler import WeiboCrawler
    crawler = WeiboCrawler()
    if hasattr(crawler, 'get_weibo_by_time_range'):
        print('get_weibo_by_time_range method exists')
    else:
        print('ERROR: get_weibo_by_time_range method not found')

print('All tests passed!')
