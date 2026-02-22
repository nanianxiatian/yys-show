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
    print("测试新爬虫逻辑 - 保存所有微博")
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

    # 获取最新一条微博
    print(f"\n5. 获取最新微博 (UID: {blogger.weibo_uid})...")
    latest_weibo = crawler.get_latest_weibo(blogger.weibo_uid, keyword=None)

    if not latest_weibo:
        print("   - 未获取到微博")
        sys.exit(1)

    print(f"   - 获取成功!")
    print(f"   - 微博ID: {latest_weibo['weibo_id']}")
    print(f"   - 内容: {latest_weibo['content'][:80]}...")

    # 解析微博
    parsed = GuessParser.parse_weibo(latest_weibo)
    print(f"\n6. 解析结果:")
    print(f"   - 是否对弈竞猜: {parsed['is_guess_related']}")
    print(f"   - 预测结果: {parsed['guess_prediction']}")
    print(f"   - 轮次: {parsed['guess_round']}")

    # 保存到数据库
    print(f"\n7. 保存到数据库...")

    # 检查是否已存在
    existing = WeiboPost.query.filter_by(weibo_id=latest_weibo['weibo_id']).first()
    if existing:
        # 更新现有记录
        existing.content = latest_weibo['content']
        existing.guess_prediction = parsed['guess_prediction']
        existing.guess_round = parsed['guess_round']
        existing.guess_date = parsed['guess_date']
        existing.publish_time = latest_weibo['publish_time']
        existing.reposts_count = latest_weibo['reposts_count']
        existing.comments_count = latest_weibo['comments_count']
        existing.attitudes_count = latest_weibo['attitudes_count']
        existing.is_guess_related = parsed['is_guess_related']
        print(f"   - 更新现有记录")
    else:
        # 创建新记录
        post = WeiboPost(
            blogger_id=blogger.id,
            weibo_id=latest_weibo['weibo_id'],
            content=latest_weibo['content'],
            guess_prediction=parsed['guess_prediction'],
            guess_round=parsed['guess_round'],
            guess_date=parsed['guess_date'],
            publish_time=latest_weibo['publish_time'],
            reposts_count=latest_weibo['reposts_count'],
            comments_count=latest_weibo['comments_count'],
            attitudes_count=latest_weibo['attitudes_count'],
            is_guess_related=parsed['is_guess_related']
        )
        db.session.add(post)
        print(f"   - 创建新记录")

    db.session.commit()
    print(f"   - 保存成功!")

    # 查询数据库验证
    print(f"\n8. 验证数据库...")
    posts = WeiboPost.query.filter_by(blogger_id=blogger.id).order_by(WeiboPost.publish_time.desc()).all()
    print(f"   - 博主共有 {len(posts)} 条微博记录")

    for i, post in enumerate(posts[:3], 1):
        print(f"\n   记录 {i}:")
        print(f"   - ID: {post.weibo_id}")
        print(f"   - 内容: {post.content[:50]}...")
        print(f"   - 是否对弈竞猜: {post.is_guess_related}")
        print(f"   - 预测: {post.guess_prediction}")

    print("\n" + "=" * 60)
    print("测试完成!")
    print("=" * 60)
