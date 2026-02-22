#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

# 测试博主列表API
url = "http://127.0.0.1:5000/api/bloggers"
params = {
    "is_active": "true",
    "per_page": 100
}

try:
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
    
    print("API响应状态:", response.status_code)
    print("API返回数据条数:", len(data.get('data', [])))
    print("分页信息:", data.get('pagination'))
    
    # 查找段段以及南墙
    print("\n查找包含'段段'的博主:")
    found = False
    for blogger in data.get('data', []):
        nickname = blogger.get('nickname', '')
        if '段段' in nickname:
            print(f"找到: ID={blogger.get('id')}, 昵称={nickname}")
            found = True
    
    if not found:
        print("未找到包含'段段'的博主")
        
    # 显示所有博主昵称
    print("\n所有博主昵称:")
    nicknames = [b.get('nickname') for b in data.get('data', [])]
    print(", ".join(nicknames))
        
except Exception as e:
    print(f"请求失败: {e}")
