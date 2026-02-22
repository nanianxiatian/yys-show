#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app
from app.models import Blogger, db
from app.services import WeiboSpiderService

app = create_app('development')

with app.app_context():
    print("=" * 60)
    print("测试同步博主信息")
    print("=" * 60)

    # 查找博主
    blogger = Blogger.query.filter_by(nickname='春秋霸主徐清林').first()

    if not blogger:
        print("\n✗ 未找到博主 '春秋霸主徐清林'")
        print("请先添加博主")
        sys.exit(1)

    print(f"\n博主信息:")
    print(f"  ID: {blogger.id}")
    print(f"  昵称: {blogger.nickname}")
    print(f"  UID: {blogger.weibo_uid or '未设置'}")
    print(f"  头像: {blogger.avatar_url[:50] + '...' if blogger.avatar_url else '未设置'}")
    print(f"  描述: {blogger.description or '未设置'}")

    # 执行同步
    print(f"\n开始同步...")
    print("-" * 60)

    service = WeiboSpiderService()
    result = service.spider_single_blogger(blogger.id)

    print("\n" + "=" * 60)
    print("同步结果:")
    print("=" * 60)
    print(f"  成功: {result.get('success')}")
    print(f"  消息: {result.get('message') or result.get('error')}")

    if result.get('success'):
        # 重新查询博主信息
        db.session.refresh(blogger)
        print(f"\n更新后信息:")
        print(f"  UID: {blogger.weibo_uid or '未设置'}")
        print(f"  头像: {blogger.avatar_url[:50] + '...' if blogger.avatar_url else '未设置'}")
        print(f"  描述: {blogger.description or '未设置'}")

    print("\n" + "=" * 60)
