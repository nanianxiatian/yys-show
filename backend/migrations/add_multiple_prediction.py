"""
添加 multiple 选项到预测结果枚举
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import db
from sqlalchemy import text

def migrate():
    """执行迁移"""
    app = create_app()
    
    with app.app_context():
        try:
            # 修改 ENUM 类型，添加 'multiple' 选项
            sql = """
            ALTER TABLE weibo_posts 
            MODIFY COLUMN guess_prediction 
            ENUM('left', 'right', 'unknown', 'multiple') 
            DEFAULT 'unknown' 
            COMMENT '预测结果:左/右/未知/多条';
            """
            
            db.session.execute(text(sql))
            db.session.commit()
            
            print("✓ 成功添加 'multiple' 到预测结果枚举")
            
        except Exception as e:
            db.session.rollback()
            print(f"✗ 迁移失败: {e}")
            return False
        
        return True

if __name__ == '__main__':
    success = migrate()
    sys.exit(0 if success else 1)
