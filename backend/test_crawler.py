#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试爬虫功能
"""
import sys
sys.path.insert(0, 'f:\\trace\\work-space\\yys-show\\backend')

from spider import WeiboCrawler
from app import create_app
from app.models import SystemConfig

# 创建应用上下文
app = create_app()
with app.app_context():
    # 获取Cookie
    cookie = SystemConfig.get_value('weibo_cookie', '')
    print(f"Cookie长度: {len(cookie)}")
    print(f"Cookie前100字符: {cookie[:100]}...")

    # 创建爬虫实例
    crawler = WeiboCrawler(cookie=cookie)

    # 测试搜索用户
    nickname = "春秋霸主徐清林"
    print(f"\n开始搜索用户: {nickname}")

    user_info = crawler.get_user_info(nickname)
    if user_info:
        print(f"找到用户: {user_info}")

        # 测试获取微博
        print(f"\n开始获取用户 {nickname} 的微博...")
        weibo_list = crawler.get_user_weibo_list(user_info['uid'], page=1, count=10)
        print(f"获取到 {len(weibo_list)} 条微博")

        for weibo in weibo_list[:3]:  # 只显示前3条
            print(f"\n微博ID: {weibo['weibo_id']}")
            print(f"发布时间: {weibo['publish_time']}")
            print(f"内容: {weibo['content'][:100]}...")
            print(f"是否含对弈竞猜: {weibo.get('is_guess_related', False)}")
    else:
        print("未找到用户")
