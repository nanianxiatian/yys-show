#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

base_url = "http://127.0.0.1:5000/api/weibo"

print("=" * 80)
print("测试: 筛选 guess_prediction=left")
print("=" * 80)
response = requests.get(base_url, params={"guess_prediction": "left", "per_page": 100})
data = response.json()

posts = data.get('data', [])
left_count = sum(1 for p in posts if p.get('guess_prediction') == 'left')
right_count = sum(1 for p in posts if p.get('guess_prediction') == 'right')
unknown_count = sum(1 for p in posts if p.get('guess_prediction') == 'unknown')

print(f"返回条数: {len(posts)}")
print(f"left: {left_count}, right: {right_count}, unknown: {unknown_count}")

if right_count > 0:
    print("\n返回了 right 的数据（不应该出现）:")
    for post in posts:
        if post.get('guess_prediction') == 'right':
            print(f"  ID: {post.get('id')}, prediction: {post.get('guess_prediction')}")

print("\n" + "=" * 80)
print("测试: 筛选 guess_prediction=right")
print("=" * 80)
response = requests.get(base_url, params={"guess_prediction": "right", "per_page": 100})
data = response.json()

posts = data.get('data', [])
left_count = sum(1 for p in posts if p.get('guess_prediction') == 'left')
right_count = sum(1 for p in posts if p.get('guess_prediction') == 'right')
unknown_count = sum(1 for p in posts if p.get('guess_prediction') == 'unknown')

print(f"返回条数: {len(posts)}")
print(f"left: {left_count}, right: {right_count}, unknown: {unknown_count}")

if left_count > 0:
    print("\n返回了 left 的数据（不应该出现）:")
    for post in posts:
        if post.get('guess_prediction') == 'left':
            print(f"  ID: {post.get('id')}, prediction: {post.get('guess_prediction')}")
