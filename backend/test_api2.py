#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app
from flask import request

app = create_app()

with app.test_client() as client:
    # 测试筛选 left
    print("=" * 80)
    print("测试: 筛选 guess_prediction=left")
    print("=" * 80)
    
    response = client.get('/api/weibo?guess_prediction=left')
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
    
    # 打印前5条的预测值
    print("\n前5条数据的预测值:")
    for post in posts[:5]:
        print(f"  ID: {post.get('id')}, guess_prediction: {post.get('guess_prediction')}")
