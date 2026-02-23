"""
检查博主信息
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import Blogger

def check():
    """检查"""
    app = create_app()
    
    with app.app_context():
        # 检查ID 9和26
        for blogger_id in [9, 26]:
            blogger = Blogger.query.get(blogger_id)
            if blogger:
                print(f"博主ID {blogger_id}: {blogger.nickname} (UID: {blogger.weibo_uid})")
            else:
                print(f"博主ID {blogger_id}: 不存在")

if __name__ == '__main__':
    check()
