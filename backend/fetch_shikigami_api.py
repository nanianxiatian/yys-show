"""
从阴阳师官网API获取式神列表
"""
import requests
import json

def fetch_shikigami_from_api():
    """从官网API获取式神数据"""
    
    # API接口
    url = "https://yys.163.com/shishen/index.html"
    api_url = "https://yys.163.com/api/get_heroid_list"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://yys.163.com/shishen/index.html'
    }
    
    try:
        # 先访问页面获取必要的cookie
        session = requests.Session()
        session.get(url, headers=headers, timeout=30)
        
        # 然后请求API
        response = session.get(api_url, headers=headers, timeout=30)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"获取到数据，类型: {type(data)}")
            
            # 保存原始数据
            with open('shikigami_api_data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("数据已保存到 shikigami_api_data.json")
            
            return data
        else:
            print(f"请求失败: {response.status_code}")
            print(response.text[:500])
            
    except Exception as e:
        print(f"获取失败: {e}")
        import traceback
        traceback.print_exc()
    
    return None

if __name__ == '__main__':
    data = fetch_shikigami_from_api()
    if data:
        print("\n数据预览:")
        print(json.dumps(data, ensure_ascii=False, indent=2)[:1000])
