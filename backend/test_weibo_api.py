"""
测试微博API
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests
import json

def test_weibo_api():
    """测试微博API"""
    
    # 博主UID
    uid = '1240631574'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Referer': 'https://weibo.com/',
    }
    
    url = 'https://weibo.com/ajax/statuses/mymblog'
    params = {
        'uid': uid,
        'page': 1,
        'feature': 0
    }
    
    print(f"请求URL: {url}")
    print(f"参数: {params}")
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        print(f"\n响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"响应ok字段: {data.get('ok')}")
            
            if data.get('ok') == 1:
                statuses = data.get('data', {}).get('list', [])
                print(f"\n获取到 {len(statuses)} 条微博")
                
                for i, status in enumerate(statuses[:5]):
                    weibo_id = status.get('id')
                    created_at = status.get('created_at')
                    text = status.get('text', '')[:100]
                    
                    print(f"\n[{i+1}] 微博ID: {weibo_id}")
                    print(f"    创建时间: {created_at}")
                    print(f"    内容: {text}...")
            else:
                print(f"API返回错误: {data.get('msg', '未知错误')}")
                print(f"完整响应: {json.dumps(data, ensure_ascii=False, indent=2)[:500]}")
        else:
            print(f"请求失败: HTTP {response.status_code}")
            print(f"响应内容: {response.text[:500]}")
            
    except Exception as e:
        print(f"请求异常: {e}")

if __name__ == '__main__':
    test_weibo_api()
