#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app
from app.models import SystemConfig
from spider import WeiboCrawler

app = create_app()
with app.app_context():
    cookie = SystemConfig.get_value('weibo_cookie', '')
    print(f'Cookie length: {len(cookie)}')

    crawler = WeiboCrawler(cookie=cookie)

    # 测试获取微博列表
    uid = '2953590535'
    print(f'\nTesting fetch weibo for UID: {uid}')
    weibo_list = crawler.get_user_weibo_list(uid, page=1, count=5)
    print(f'Got {len(weibo_list)} weibo posts')

    for w in weibo_list[:2]:
        print(f'\nWeibo ID: {w["weibo_id"]}')
        print(f'Content: {w["content"][:80]}...')
