"""
从阴阳师官网API获取式神列表 - 尝试不同API路径
"""
import requests
import json

def fetch_shikigami_from_api():
    """从官网API获取式神数据"""
    
    # 尝试多种可能的API路径
    api_urls = [
        "https://yys.163.com/api/get_heroid_list",
        "https://yys.163.com/shishen/get_heroid_list",
        "https://yys.163.com/data/get_heroid_list",
        "https://yys.res.netease.com/api/get_heroid_list",
        "https://yys.res.netease.com/pc/zt/20161108171335/data/shishen.json",
        "https://yys.res.netease.com/pc/gw/20160929201016/data/shishen.json",
        "https://yys.163.com/js/shishen.json",
        "https://yys.163.com/data/shishen.json",
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://yys.163.com/shishen/index.html',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    session = requests.Session()
    
    # 先访问页面
    try:
        page_response = session.get("https://yys.163.com/shishen/index.html", headers=headers, timeout=30)
        print(f"页面状态码: {page_response.status_code}")
    except Exception as e:
        print(f"访问页面失败: {e}")
    
    # 尝试各个API
    for api_url in api_urls:
        try:
            print(f"\n尝试: {api_url}")
            response = session.get(api_url, headers=headers, timeout=30)
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type', '')
                print(f"Content-Type: {content_type}")
                
                # 尝试解析JSON
                try:
                    data = response.json()
                    print(f"✓ 成功获取JSON数据!")
                    print(f"数据类型: {type(data)}")
                    
                    if isinstance(data, dict):
                        print(f"数据键: {list(data.keys())[:10]}")
                    elif isinstance(data, list):
                        print(f"数组长度: {len(data)}")
                        if len(data) > 0:
                            print(f"第一条数据: {data[0]}")
                    
                    # 保存数据
                    with open('shikigami_api_data.json', 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    print("数据已保存到 shikigami_api_data.json")
                    
                    return data
                    
                except Exception as e:
                    print(f"不是JSON格式: {e}")
                    if len(response.text) < 1000:
                        print(f"内容: {response.text[:500]}")
                    else:
                        print(f"内容长度: {len(response.text)}")
                        
        except Exception as e:
            print(f"请求失败: {e}")
    
    print("\n所有API都尝试失败")
    return None

if __name__ == '__main__':
    data = fetch_shikigami_from_api()
