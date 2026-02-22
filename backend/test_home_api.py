#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试首页API
"""
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

import requests

base_url = 'http://127.0.0.1:5000'

print("=" * 80)
print("测试首页API")
print("=" * 80)

# 测试系统统计API
print("\n1. 测试系统统计API (/api/system/stats)")
try:
    resp = requests.get(f'{base_url}/api/system/stats', timeout=10)
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print(f"   Success: {data.get('success')}")
        print(f"   Data: {data.get('data', {}).keys() if data.get('data') else 'None'}")
    else:
        print(f"   Error: {resp.text[:500]}")
except Exception as e:
    print(f"   Exception: {e}")

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)
