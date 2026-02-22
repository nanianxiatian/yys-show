#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app

app = create_app()

with app.app_context():
    from app.models import SystemConfig
    from spider import WeiboCrawler
    
    print("=" * 80)
    print("测试用户详情API响应")
    print("=" * 80)
    
    # 获取cookie
    cookie = SystemConfig.get_value('weibo_cookie', '')
    crawler = WeiboCrawler(cookie=cookie)
    
    # 测试UID
    uid = '7629946033'
    
    import requests
    
    API_URL = 'https://weibo.com/ajax'
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
    
    profile_url = f'{API_URL}/profile/detail'
    params = {'uid': uid}
    
    print(f"\n请求URL: {profile_url}")
    print(f"参数: {params}")
    print(f"Cookie存在: {bool(cookie)}")
    
    response = session.get(profile_url, headers=headers, params=params, timeout=30)
    
    print(f"\n响应状态码: {response.status_code}")
    print(f"\n响应内容:")
    print(response.text[:2000])  # 打印前2000字符
