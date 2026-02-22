#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app
from app.models import db, Blogger, WeiboPost, SystemConfig
from spider import WeiboCrawler, GuessParser

app = create_app('development')

with app.app_context():
    print("=" * 60)
    print("调试爬虫流程")
    print("=" * 60)

    # 获取Cookie
    cookie = SystemConfig.get_value('weibo_cookie', '')
    print(f"\n1. Cookie长度: {len(cookie)}")

    # 创建爬虫
    crawler = WeiboCrawler(cookie=cookie)
    print(f"2. 爬虫实例创建成功")

    # 获取博主
    blogger = Blogger.query.filter_by(nickname='春秋霸主徐清林').first()
    if not blogger:
        print("错误: 博主不存在")
        sys.exit(1)

    print(f"\n3. 博主信息:")
    print(f"   - 昵称: {blogger.nickname}")
    print(f"   - UID: {blogger.weibo_uid}")

    # 如果没有UID，先获取
    if not blogger.weibo_uid:
        print(f"\n4. 获取博主UID...")
        user_info = crawler.get_user_info(blogger.nickname)
        if user_info:
            blogger.weibo_uid = user_info['uid']
            db.session.commit()
            print(f"   - 获取成功: {user_info['uid']}")
        else:
            print("   - 获取失败")
            sys.exit(1)

    # 获取微博列表
    print(f"\n5. 获取微博列表 (UID: {blogger.weibo_uid})...")
    weibo_list = crawler.get_user_weibo_list(blogger.weibo_uid, page=1, count=10)
    print(f"   - 获取到 {len(weibo_list)} 条微博")

    # 显示每条微博的内容和是否包含对弈竞猜
    for i, weibo in enumerate(weibo_list[:5], 1):
        content = weibo.get('content', '')
        parsed = GuessParser.parse_weibo(weibo)

        print(f"\n   微博 {i}:")
        print(f"   - ID: {weibo['weibo_id']}")
        print(f"   - 内容: {content[:60]}...")
        print(f"   - 是否对弈竞猜: {parsed['is_guess_related']}")
        print(f"   - 预测结果: {parsed['guess_prediction']}")

    # 统计对弈竞猜相关微博
    guess_count = sum(1 for w in weibo_list if GuessParser.parse_weibo(w)['is_guess_related'])
    print(f"\n6. 统计结果:")
    print(f"   - 总微博数: {len(weibo_list)}")
    print(f"   - 对弈竞猜相关: {guess_count}")

    print("\n" + "=" * 60)
