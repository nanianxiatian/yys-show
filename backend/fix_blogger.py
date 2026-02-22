#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app
from app.models import Blogger, db
from spider import WeiboCrawler
from app.models import SystemConfig

app = create_app('development')

with app.app_context():
    print("=" * 60)
    print("修复博主信息")
    print("=" * 60)

    # 查找博主
    blogger = Blogger.query.filter_by(nickname='春秋霸主徐清林').first()

    if not blogger:
        print("\n✗ 未找到博主 '春秋霸主徐清林'")
        sys.exit(1)

    print(f"\n当前博主信息:")
    print(f"  ID: {blogger.id}")
    print(f"  昵称: {blogger.nickname}")
    print(f"  UID: {blogger.weibo_uid or '未设置'}")
    print(f"  头像: {blogger.avatar_url[:50] + '...' if blogger.avatar_url else '未设置'}")
    print(f"  描述: {blogger.description or '未设置'}")

    # 获取Cookie
    cookie = SystemConfig.get_value('weibo_cookie', '')
    print(f"\n获取正确的用户信息...")

    # 创建爬虫并获取用户信息
    crawler = WeiboCrawler(cookie=cookie)
    user_info = crawler.get_user_info('春秋霸主徐清林')

    if user_info:
        print(f"\n✓ 获取到正确信息:")
        print(f"  UID: {user_info['uid']}")
        print(f"  昵称: {user_info['nickname']}")
        print(f"  头像: {user_info['avatar'][:50] + '...' if user_info['avatar'] else '未设置'}")
        print(f"  描述: {user_info['description'] or '未设置'}")

        # 更新博主信息
        blogger.weibo_uid = user_info['uid']
        blogger.avatar_url = user_info.get('avatar')
        blogger.description = user_info.get('description')
        db.session.commit()

        print(f"\n✓ 博主信息已更新!")

        # 重新查询确认
        db.session.refresh(blogger)
        print(f"\n更新后信息:")
        print(f"  UID: {blogger.weibo_uid}")
        print(f"  头像: {blogger.avatar_url[:50] + '...' if blogger.avatar_url else '未设置'}")
        print(f"  描述: {blogger.description or '未设置'}")
    else:
        print(f"\n✗ 无法获取用户信息")

    print("\n" + "=" * 60)
