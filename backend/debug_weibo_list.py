"""
调试获取微博列表
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import SystemConfig
from spider.weibo_crawler import WeiboCrawler

def debug_weibo_list():
    """调试获取微博列表"""
    app = create_app()
    
    with app.app_context():
        # 获取Cookie
        cookie = SystemConfig.get_value('weibo_cookie', '')
        print(f"Cookie: {'有' if cookie else '无'} (长度: {len(cookie)})")
        
        # 创建爬虫
        crawler = WeiboCrawler(cookie=cookie)
        
        # 测试获取微博列表
        uid = '1240631574'
        print(f"\n测试获取微博列表 - UID: {uid}")
        
        try:
            weibo_list = crawler.get_user_weibo_list(uid, page=1, count=20)
            print(f"获取到 {len(weibo_list)} 条微博")
            
            for i, weibo in enumerate(weibo_list[:3]):
                print(f"\n[{i+1}] ID: {weibo['weibo_id']}")
                print(f"    时间: {weibo['publish_time']}")
                print(f"    内容: {weibo['content'][:60]}...")
                
        except Exception as e:
            print(f"获取失败: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    debug_weibo_list()
