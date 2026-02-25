"""
检查Cookie状态
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import Config

def check_cookie():
    """检查Cookie"""
    app = create_app()
    
    with app.app_context():
        print("=== 检查Cookie状态 ===\n")
        
        cookie_config = Config.query.filter_by(config_key='weibo_cookie').first()
        
        if cookie_config and cookie_config.config_value:
            cookie = cookie_config.config_value
            print(f"Cookie长度: {len(cookie)} 字符")
            print(f"Cookie前100字符: {cookie[:100]}...")
            
            # 检查关键字段
            if 'SUB=' in cookie:
                print("✓ 包含 SUB 字段")
            else:
                print("✗ 缺少 SUB 字段")
                
            if 'SUBP=' in cookie:
                print("✓ 包含 SUBP 字段")
            else:
                print("✗ 缺少 SUBP 字段")
        else:
            print("✗ Cookie未设置")

if __name__ == '__main__':
    check_cookie()
