"""
使用Selenium从阴阳师官网获取式神列表
"""
import json
import time

def fetch_shikigami_with_selenium():
    """使用Selenium获取式神数据"""
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        # 配置Chrome选项
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 无头模式
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        
        # 启动浏览器
        print("启动Chrome浏览器...")
        driver = webdriver.Chrome(options=chrome_options)
        
        # 设置网络监听
        print("设置网络监听...")
        driver.execute_cdp_cmd('Network.enable', {})
        
        # 存储API响应
        api_responses = []
        
        def intercept_response(message):
            """拦截网络响应"""
            if 'Network.responseReceived' in message.get('method', ''):
                params = message.get('params', {})
                response = params.get('response', {})
                url = response.get('url', '')
                
                if 'heroid' in url or 'shishen' in url:
                    print(f"捕获到请求: {url}")
                    api_responses.append(url)
        
        # 访问页面
        url = "https://yys.163.com/shishen/index.html"
        print(f"访问页面: {url}")
        driver.get(url)
        
        # 等待页面加载
        time.sleep(5)
        
        # 尝试从页面中提取式神数据
        print("\n尝试从页面提取数据...")
        
        # 查找所有式神名称元素
        shikigami_names = []
        
        # 尝试多种选择器
        selectors = [
            '.shishen-name',
            '.shishen_item .name',
            '.shishen-item .name',
            '[class*="name"]',
            '.item .name',
            '.shishen_list .item',
        ]
        
        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                print(f"选择器 '{selector}' 找到 {len(elements)} 个元素")
                
                for elem in elements[:10]:
                    text = elem.text.strip()
                    if text and len(text) < 20:
                        print(f"  - {text}")
                        shikigami_names.append(text)
                        
            except Exception as e:
                print(f"选择器 '{selector}' 失败: {e}")
        
        # 保存页面源码
        page_source = driver.page_source
        with open('shishen_page_source.html', 'w', encoding='utf-8') as f:
            f.write(page_source)
        print("\n页面源码已保存到 shishen_page_source.html")
        
        # 关闭浏览器
        driver.quit()
        
        # 去重
        shikigami_names = list(set(shikigami_names))
        print(f"\n找到 {len(shikigami_names)} 个式神名称")
        
        return shikigami_names
        
    except ImportError:
        print("未安装selenium，请运行: pip install selenium")
        return None
    except Exception as e:
        print(f"获取失败: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == '__main__':
    names = fetch_shikigami_with_selenium()
    if names:
        print("\n式神列表:")
        for name in names[:30]:
            print(f"  - {name}")
