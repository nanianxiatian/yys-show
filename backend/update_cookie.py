"""
更新数据库中的Cookie
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import SystemConfig

def update_cookie():
    """更新Cookie"""
    app = create_app()
    
    with app.app_context():
        # 从环境变量获取新Cookie
        env_cookie = os.getenv('WEIBO_COOKIE', '')
        
        if not env_cookie:
            print("✗ 环境变量中无Cookie")
            return
        
        # 更新到数据库
        SystemConfig.set_value('weibo_cookie', env_cookie)
        SystemConfig.set_value('cookie_expire_time', 
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        # 验证
        db_cookie = SystemConfig.get_value('weibo_cookie', '')
        if db_cookie == env_cookie:
            print("✓ Cookie已更新到数据库")
            print(f"  长度: {len(db_cookie)}")
        else:
            print("✗ 更新失败")

if __name__ == '__main__':
    from datetime import datetime
    update_cookie()
