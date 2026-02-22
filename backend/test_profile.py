#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app
from app.models import SystemConfig
import requests

app = create_app('development')

with app.app_context():
    print("=" * 60)
    print("测试用户详情API")
    print("=" * 60)

    # 获取Cookie
    cookie = SystemConfig.get_value('weibo_cookie', '')
    print(f"\nCookie长度: {len(cookie)}")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Cookie': cookie,
        'Referer': 'https://weibo.com/',
        'Accept': 'application/json, text/plain, */*',
        'X-Requested-With': 'XMLHttpRequest'
    }

    uid = '1240631574'

    # 测试用户详情API
    url = 'https://weibo.com/ajax/profile/detail'
    params = {'uid': uid}

    print(f"\n请求URL: {url}")
    print(f"参数: {params}")

    session = requests.Session()
    response = session.get(url, headers=headers, params=params, timeout=30)

    print(f"\n响应状态码: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"\n响应ok: {data.get('ok')}")

        if data.get('ok') == 1:
            user_data = data.get('data', {})
            print(f"\n用户数据键: {list(user_data.keys())}")

            # 检查是否有statuses
            if 'statuses' in user_data:
                statuses = user_data['statuses']
                print(f"\nstatuses数量: {len(statuses)}")
                if statuses:
                    print(f"第一条微博ID: {statuses[0].get('id')}")
                    print(f"第一条微博内容: {statuses[0].get('text', '')[:100]}...")
            else:
                print("\n没有statuses字段")

            # 检查其他可能包含微博的字段
            for key in user_data.keys():
                if isinstance(user_data[key], list) and len(user_data[key]) > 0:
                    print(f"\n字段 '{key}' 是列表，长度: {len(user_data[key])}")
                    if isinstance(user_data[key][0], dict) and 'id' in user_data[key][0]:
                        print(f"  可能包含微博数据")

    print("\n" + "=" * 60)
