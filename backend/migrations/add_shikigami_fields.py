"""
添加式神字段迁移脚本
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import db
from sqlalchemy import text


def upgrade():
    """添加式神字段到official_results表"""
    app = create_app()
    with app.app_context():
        # 获取现有字段
        result = db.session.execute(text("SHOW COLUMNS FROM official_results"))
        existing_columns = [row[0] for row in result]
        
        # 添加左侧式神字段
        for i in range(1, 6):
            column_name = f"left_shikigami_{i}"
            if column_name not in existing_columns:
                sql = f"""
                ALTER TABLE official_results 
                ADD COLUMN {column_name} VARCHAR(100) 
                COMMENT '左侧式神{i}'
                """
                db.session.execute(text(sql))
                print(f"添加字段: {column_name}")
            else:
                print(f"字段已存在: {column_name}")
        
        # 添加右侧式神字段
        for i in range(1, 6):
            column_name = f"right_shikigami_{i}"
            if column_name not in existing_columns:
                sql = f"""
                ALTER TABLE official_results 
                ADD COLUMN {column_name} VARCHAR(100) 
                COMMENT '右侧式神{i}'
                """
                db.session.execute(text(sql))
                print(f"添加字段: {column_name}")
            else:
                print(f"字段已存在: {column_name}")
        
        db.session.commit()
        print("式神字段添加成功！")


def downgrade():
    """删除式神字段"""
    app = create_app()
    with app.app_context():
        # 删除左侧式神字段
        for i in range(1, 6):
            sql = f"""
            ALTER TABLE official_results 
            DROP COLUMN IF EXISTS left_shikigami_{i}
            """
            try:
                db.session.execute(text(sql))
            except:
                pass
        
        # 删除右侧式神字段
        for i in range(1, 6):
            sql = f"""
            ALTER TABLE official_results 
            DROP COLUMN IF EXISTS right_shikigami_{i}
            """
            try:
                db.session.execute(text(sql))
            except:
                pass
        
        db.session.commit()
        print("式神字段删除成功！")


if __name__ == '__main__':
    upgrade()
