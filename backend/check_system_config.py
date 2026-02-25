"""
检查系统配置
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import SystemConfig

def check_config():
    """检查配置"""
    app = create_app()
    
    with app.app_context():
        print("=== 检查系统配置 ===\n")
        
        # 获取所有配置
        configs = SystemConfig.query.all()
        
        print(f"共有 {len(configs)} 条配置:\n")
        
        for config in configs:
            value = config.config_value
            if value and len(value) > 100:
                value = value[:100] + "..."
            print(f"  {config.config_key}: {value}")
        
        # 专门检查weibo_cookie
        cookie = SystemConfig.get_value('weibo_cookie', '')
        print(f"\n\nweibo_cookie:")
        if cookie:
            print(f"  长度: {len(cookie)}")
            print(f"  前100字符: {cookie[:100]}...")
        else:
            print("  未设置或为空")

if __name__ == '__main__':
    check_config()
