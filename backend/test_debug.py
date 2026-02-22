#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app
from flask import request

app = create_app()

# 添加一个测试路由来查看接收到的参数
@app.route('/api/test-params')
def test_params():
    from flask import jsonify
    return jsonify({
        'args': dict(request.args),
        'guess_prediction': request.args.get('guess_prediction')
    })

with app.test_client() as client:
    # 测试参数接收
    print("=" * 80)
    print("测试参数接收")
    print("=" * 80)
    
    response = client.get('/api/test-params?guess_prediction=left')
    import json
    data = json.loads(response.data)
    print(f"接收到的参数: {data}")
    
    # 测试微博列表筛选
    print("\n" + "=" * 80)
    print("测试微博列表筛选")
    print("=" * 80)
    
    response = client.get('/api/weibo?guess_prediction=left&per_page=100')
    data = json.loads(response.data)
    
    posts = data.get('data', [])
    left_count = sum(1 for p in posts if p.get('guess_prediction') == 'left')
    right_count = sum(1 for p in posts if p.get('guess_prediction') == 'right')
    unknown_count = sum(1 for p in posts if p.get('guess_prediction') == 'unknown')
    
    print(f"返回条数: {len(posts)}")
    print(f"left: {left_count}, right: {right_count}, unknown: {unknown_count}")
