"""
调试Cookie加载
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import SystemConfig
from app.services import WeiboSpiderService
from spider.weibo_crawler import WeiboCrawler

def debug_cookie():
    """调试Cookie"""
    app = create_app()
    
    with app.app_context():
        print("=== 调试Cookie加载 ===\n")
        
        # 1. 直接从数据库读取
        cookie_from_db = SystemConfig.get_value('weibo_cookie', '')
        print(f"1. 从数据库读取Cookie:")
        print(f"   长度: {len(cookie_from_db) if cookie_from_db else 0}")
        print(f"   前50字符: {cookie_from_db[:50] if cookie_from_db else 'None'}...")
        print()
        
        # 2. 通过WeiboSpiderService获取
        spider_service = WeiboSpiderService()
        crawler = spider_service._get_crawler()
        print(f"2. WeiboSpiderService中的Cookie:")
        print(f"   crawler.cookie长度: {len(crawler.cookie) if crawler.cookie else 0}")
        print(f"   crawler.cookie前50字符: {crawler.cookie[:50] if crawler.cookie else 'None'}...")
        print()
        
        # 3. 直接创建WeiboCrawler
        direct_crawler = WeiboCrawler(cookie=cookie_from_db)
        print(f"3. 直接创建WeiboCrawler:")
        print(f"   crawler.cookie长度: {len(direct_crawler.cookie) if direct_crawler.cookie else 0}")
        print(f"   crawler.cookie前50字符: {direct_crawler.cookie[:50] if direct_crawler.cookie else 'None'}...")
        print()
        
        # 4. 检查session中的Cookie
        print(f"4. Session headers中的Cookie:")
        session_cookie = direct_crawler.session.headers.get('Cookie', '')
        print(f"   长度: {len(session_cookie) if session_cookie else 0}")
        print(f"   前50字符: {session_cookie[:50] if session_cookie else 'None'}...")

if __name__ == '__main__':
    debug_cookie()
