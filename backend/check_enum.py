"""
检查数据库枚举值
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db
from sqlalchemy import text

def check_enum():
    """检查枚举值"""
    app = create_app()
    
    with app.app_context():
        # 查询数据库中的枚举值
        sql = """
        SELECT COLUMN_TYPE 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = 'weibo_posts' 
        AND COLUMN_NAME = 'guess_prediction'
        """
        result = db.session.execute(text(sql))
        row = result.fetchone()
        
        if row:
            print(f"数据库枚举值: {row[0]}")
        else:
            print("未找到枚举信息")
        
        # 检查模型中的枚举值
        from app.models.weibo_post import WeiboPost
        print(f"\n模型中的枚举值: {WeiboPost.guess_prediction.type.enums}")

if __name__ == '__main__':
    check_enum()
