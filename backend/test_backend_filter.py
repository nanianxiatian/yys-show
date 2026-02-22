#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app

app = create_app()

with app.test_client() as client:
    # 测试筛选 left
    print("=" * 80)
    print("测试: 筛选 guess_prediction=left")
    print("=" * 80)
    
    response = client.get('/api/weibo?guess_prediction=left&per_page=100')
    print(f"状态码: {response.status_code}")
    
    import json
    data = json.loads(response.data)
    print(f"总条数: {data.get('pagination', {}).get('total', 0)}")
    
    # 检查返回的数据
    posts = data.get('data', [])
    left_count = sum(1 for p in posts if p.get('guess_prediction') == 'left')
    right_count = sum(1 for p in posts if p.get('guess_prediction') == 'right')
    unknown_count = sum(1 for p in posts if p.get('guess_prediction') == 'unknown')
    
    print(f"left: {left_count}, right: {right_count}, unknown: {unknown_count}")
    
    # 打印所有非 left 的数据
    print("\n所有 guess_prediction != 'left' 的数据:")
    for post in posts:
        if post.get('guess_prediction') != 'left':
            print(f"  ID: {post.get('id')}, prediction: {post.get('guess_prediction')}")
