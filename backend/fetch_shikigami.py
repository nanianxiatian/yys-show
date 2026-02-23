"""
从阴阳师官网获取SR式神列表
"""
import requests
from bs4 import BeautifulSoup
import re

def fetch_sr_shikigami():
    """获取SR式神列表"""
    url = "https://yys.163.com/shishen/index.html?type=sr"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        
        print(f"状态码: {response.status_code}")
        print(f"内容长度: {len(response.text)}")
        
        # 保存HTML用于调试
        with open('shishen_page.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("页面内容已保存到 shishen_page.html")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 尝试多种方式查找式神名称
        shikigami_names = []
        
        # 方法1: 查找class包含shishen的元素
        elements = soup.find_all(class_=re.compile('shishen', re.I))
        print(f"\n找到 {len(elements)} 个包含'shishen'的元素")
        
        # 方法2: 查找所有图片的alt属性
        images = soup.find_all('img')
        for img in images:
            alt = img.get('alt', '')
            if alt and len(alt) < 20 and '式神' not in alt:
                shikigami_names.append(alt)
        
        # 方法3: 查找特定class的div或a标签
        name_elements = soup.find_all(['div', 'a', 'span'], class_=re.compile('name|title', re.I))
        for elem in name_elements:
            text = elem.get_text().strip()
            if text and len(text) < 20 and text not in shikigami_names:
                shikigami_names.append(text)
        
        # 去重
        shikigami_names = list(set(shikigami_names))
        
        print(f"\n找到 {len(shikigami_names)} 个可能的式神名称:")
        for name in shikigami_names[:30]:
            print(f"  - {name}")
        
        return shikigami_names
        
    except Exception as e:
        print(f"获取失败: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == '__main__':
    names = fetch_sr_shikigami()
