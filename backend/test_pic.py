#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from spider import WeiboCrawler
from app.models import SystemConfig

# 获取cookie
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')
from app import create_app
from app.models import db, SystemConfig

app = create_app()

with app.app_context():
    cookie = SystemConfig.get_value('weibo_cookie', '')
    print(f"Cookie长度: {len(cookie)}")
    
    crawler = WeiboCrawler(cookie=cookie)
    
    # 测试获取徐清林的微博
    uid = "1240631574"
    print(f"\n获取博主UID: {uid} 的微博")
    
    weibos = crawler.get_user_weibo_list(uid, count=1)
    
    if weibos:
        weibo = weibos[0]
        print(f"\n微博ID: {weibo['weibo_id']}")
        print(f"内容: {weibo['content'][:100]}...")
        print(f"图片URL: {weibo.get('pic_urls', [])}")
        print(f"图片数量: {len(weibo.get('pic_urls', []))}")
        
        # 打印原始数据的pics字段
        raw_data = weibo.get('raw_data', {})
        print(f"\n原始数据pics字段: {raw_data.get('pics', '不存在')}")
        print(f"原始数据pic_ids字段: {raw_data.get('pic_ids', '不存在')}")
    else:
        print("未获取到微博")
