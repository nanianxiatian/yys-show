#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app
from app.models import SystemConfig
import requests
import json

app = create_app('development')

with app.app_context():
    print("=" * 60)
    print("测试各种微博API")
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
    session = requests.Session()

    # API 1: 用户微博列表
    apis = [
        {
            'name': '用户微博列表 (profile/statuses)',
            'url': 'https://weibo.com/ajax/profile/statuses',
            'params': {'uid': uid, 'page': 1, 'feature': 0}
        },
        {
            'name': '用户微博列表 (statuses/mymblog)',
            'url': 'https://weibo.com/ajax/statuses/mymblog',
            'params': {'uid': uid, 'page': 1, 'feature': 0}
        },
        {
            'name': '用户微博时间线 (statuses/container_timeline)',
            'url': 'https://weibo.com/ajax/statuses/container_timeline',
            'params': {'containerid': f'107603{uid}', 'page': 1}
        },
        {
            'name': '用户微博时间线 (friends)',
            'url': 'https://weibo.com/ajax/statuses/friends',
            'params': {'page': 1, 'uid': uid}
        }
    ]

    for api in apis:
        print(f"\n{'-'*60}")
        print(f"测试: {api['name']}")
        print(f"URL: {api['url']}")
        print(f"参数: {api['params']}")

        try:
            response = session.get(api['url'], headers=headers, params=api['params'], timeout=30)
            print(f"状态码: {response.status_code}")

            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"响应ok: {data.get('ok')}")

                    if data.get('ok') == 1:
                        # 检查是否有微博数据
                        if 'data' in data:
                            data_obj = data['data']
                            if isinstance(data_obj, list):
                                print(f"找到列表数据，长度: {len(data_obj)}")
                                if data_obj and len(data_obj) > 0:
                                    print(f"第一条数据类型: {type(data_obj[0])}")
                                    if isinstance(data_obj[0], dict):
                                        print(f"第一条数据键: {list(data_obj[0].keys())[:5]}")
                            elif isinstance(data_obj, dict):
                                print(f"找到对象数据，键: {list(data_obj.keys())}")
                                if 'list' in data_obj:
                                    print(f"list字段长度: {len(data_obj['list'])}")
                                if 'statuses' in data_obj:
                                    print(f"statuses字段长度: {len(data_obj['statuses'])}")
                                if 'cards' in data_obj:
                                    print(f"cards字段长度: {len(data_obj['cards'])}")
                except Exception as e:
                    print(f"解析JSON失败: {e}")
            else:
                print(f"请求失败: {response.status_code}")
        except Exception as e:
            print(f"请求异常: {e}")

    print("\n" + "=" * 60)
