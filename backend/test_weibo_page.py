#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

import requests

# 测试获取微博页面
nickname = '春秋霸主徐清林'
url = f'https://weibo.com/n/{nickname}'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

response = requests.get(url, headers=headers, allow_redirects=True, timeout=30)

print(f"URL: {url}")
print(f"状态码: {response.status_code}")
print(f"最终URL: {response.url}")
print(f"\n页面内容前2000字符:")
print(response.text[:2000])

# 尝试查找UID
import re
patterns = [
    r'uid[=:]\s*["\']?(\d+)["\']?',
    r'userId[=:]\s*["\']?(\d+)["\']?',
    r'oid[=:]\s*["\']?(\d+)["\']?',
    r'\$CONFIG\[\'oid\'\]\s*=\s*[\'"](\d+)[\'"]',
    r'\$CONFIG\[\'uid\'\]\s*=\s*[\'"](\d+)[\'"]',
]

print("\n\n查找UID:")
for pattern in patterns:
    matches = re.findall(pattern, response.text)
    if matches:
        print(f"  模式 {pattern}: {matches[:3]}")  # 只显示前3个匹配
