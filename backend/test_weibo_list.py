#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app
from app.models import SystemConfig
from spider import WeiboCrawler

app = create_app('development')

with app.app_context():
    print("=" * 60)
    print("测试获取微博列表")
    print("=" * 60)

    # 获取Cookie
    cookie = SystemConfig.get_value('weibo_cookie', '')
    print(f"\nCookie长度: {len(cookie)}")

    # 创建爬虫
    crawler = WeiboCrawler(cookie=cookie)

    # 测试获取微博列表
    uid = '1240631574'  # 春秋霸主徐清林的UID
    print(f"\n获取博主微博列表 - UID: {uid}")
    print("-" * 60)

    weibo_list = crawler.get_user_weibo_list(uid, page=1, count=5)

    print(f"\n获取到 {len(weibo_list)} 条微博")

    if weibo_list:
        for i, weibo in enumerate(weibo_list[:3], 1):
            print(f"\n微博 {i}:")
            print(f"  ID: {weibo['weibo_id']}")
            print(f"  内容: {weibo['content'][:80]}...")
            print(f"  时间: {weibo['publish_time']}")
    else:
        print("\n✗ 未获取到微博")

    print("\n" + "=" * 60)
