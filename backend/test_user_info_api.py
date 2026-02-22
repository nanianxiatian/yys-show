#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app

app = create_app()

with app.app_context():
    from app.models import SystemConfig
    import requests
    
    print("=" * 80)
    print("测试不同API获取用户信息")
    print("=" * 80)
    
    # 获取cookie
    cookie = SystemConfig.get_value('weibo_cookie', '')
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://weibo.com/',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    session = requests.Session()
    session.headers.update(headers)
    if cookie:
        session.headers.update({'Cookie': cookie})
    
    uid = '7629946033'
    
    # API 1: 用户信息API
    print("\n" + "=" * 60)
    print("API 1: /ajax/profile/info")
    print("=" * 60)
    
    url1 = f'https://weibo.com/ajax/profile/info?uid={uid}'
    response1 = session.get(url1, headers=headers, timeout=30)
    print(f"状态码: {response1.status_code}")
    if response1.status_code == 200:
        data1 = response1.json()
        print(f"响应: {data1}")
