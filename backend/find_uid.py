#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
手动查找微博用户UID的工具
可以通过微博网页版或手机版查找
"""

# 春秋霸主徐清林的微博主页
# 访问 https://weibo.com/u/XXXX 或者 https://weibo.com/n/春秋霸主徐清林
# 从页面源码或网络请求中查找UID

# 常见方法：
# 1. 访问 https://m.weibo.cn/n/春秋霸主徐清林 (手机版)
# 2. 查看页面源码，搜索 "uid" 或 "userId"
# 3. 或者查看网络请求，找到用户信息接口

# 让我尝试通过手机版微博获取
import requests
import re

nickname = '春秋霸主徐清林'

# 方法1: 手机版微博
print("方法1: 尝试手机版微博...")
url = f'https://m.weibo.cn/n/{nickname}'
headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.0',
}

try:
    response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
    print(f"状态码: {response.status_code}")
    print(f"最终URL: {response.url}")

    # 从URL中提取UID
    uid_match = re.search(r'/u/(\d+)', response.url)
    if uid_match:
        uid = uid_match.group(1)
        print(f"✓ 找到UID: {uid}")
    else:
        print("✗ 未从URL中找到UID")

        # 从页面内容中查找
        uid_match = re.search(r'uid[=:]\s*["\']?(\d+)["\']?', response.text)
        if uid_match:
            uid = uid_match.group(1)
            print(f"✓ 从页面内容找到UID: {uid}")
        else:
            print("✗ 未从页面内容中找到UID")
            print(f"\n页面内容片段:\n{response.text[:1000]}")

except Exception as e:
    print(f"请求失败: {e}")

print("\n" + "="*60)
print("建议:")
print("1. 打开浏览器访问: https://weibo.com/n/春秋霸主徐清林")
print("2. 查看页面源码，搜索 'uid' 或 'oid'")
print("3. 或者使用浏览器开发者工具查看网络请求")
print("="*60)
