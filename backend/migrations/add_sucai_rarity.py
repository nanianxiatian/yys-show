"""
迁移脚本：添加素材稀有度
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
            # MySQL 修改 ENUM 类型
            sql = """
            ALTER TABLE shikigamis 
            MODIFY COLUMN rarity ENUM('N', 'R', 'SR', 'SSR', 'SP', 'UR', '素材') 
            DEFAULT 'SR' COMMENT '稀有度';
            """
            
            db.session.execute(text(sql))
            db.session.commit()
            
            print("✓ 迁移成功：已添加素材稀有度")
            
        except Exception as e:
            print(f"✗ 迁移失败: {e}")
            db.session.rollback()

if __name__ == '__main__':
    migrate()
