#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试浏览器实际发送的请求
"""
import requests

base_url = "http://127.0.0.1:5000/api/weibo"

# 测试不同的参数组合
test_cases = [
    {"guess_prediction": "left"},
    {"guess_prediction": "right"},
    {"guess_prediction": "unknown"},
    {"guess_prediction": "left", "round": 1},
]

for params in test_cases:
    print("=" * 80)
    print(f"测试参数: {params}")
    print("=" * 80)
    
    response = requests.get(base_url, params=params)
    data = response.json()
    
    posts = data.get('data', [])
    left_count = sum(1 for p in posts if p.get('guess_prediction') == 'left')
    right_count = sum(1 for p in posts if p.get('guess_prediction') == 'right')
    unknown_count = sum(1 for p in posts if p.get('guess_prediction') == 'unknown')
    
    print(f"返回条数: {len(posts)}")
    print(f"left: {left_count}, right: {right_count}, unknown: {unknown_count}")
    print()
