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
    print("测试获取用户信息")
    print("=" * 60)

    # 获取Cookie
    cookie = SystemConfig.get_value('weibo_cookie', '')
    print(f"\nCookie长度: {len(cookie)}")

    # 创建爬虫
    crawler = WeiboCrawler(cookie=cookie)

    # 测试获取用户信息
    nickname = '春秋霸主徐清林'
    print(f"\n搜索用户: {nickname}")
    print("-" * 60)

    user_info = crawler.get_user_info(nickname)

    if user_info:
        print("\n✓ 获取成功!")
        print(f"  UID: {user_info['uid']}")
        print(f"  昵称: {user_info['nickname']}")
        print(f"  描述: {user_info['description']}")
        print(f"  头像: {user_info['avatar'][:50]}...")
    else:
        print("\n✗ 获取失败")

    print("\n" + "=" * 60)
