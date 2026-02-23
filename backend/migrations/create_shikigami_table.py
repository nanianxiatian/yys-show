"""
创建式神表迁移脚本
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import db
from sqlalchemy import text


def upgrade():
    """创建式神表"""
    app = create_app()
    with app.app_context():
        # 检查表是否存在
        result = db.session.execute(text("""
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_schema = DATABASE() 
            AND table_name = 'shikigamis'
        """))
        
        if result.scalar() > 0:
            print("式神表已存在，跳过创建")
            return
        
        # 创建式神表
        sql = """
        CREATE TABLE shikigamis (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE COMMENT '式神名称',
            english_name VARCHAR(100) COMMENT '式神英文简称',
            skill_1 VARCHAR(200) COMMENT '一技能',
            skill_2 VARCHAR(200) COMMENT '二技能',
            skill_3 VARCHAR(200) COMMENT '三技能',
            description TEXT COMMENT '备注',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='式神表'
        """
        
        db.session.execute(text(sql))
        db.session.commit()
        print("式神表创建成功！")


def downgrade():
    """删除式神表"""
    app = create_app()
    with app.app_context():
        try:
            db.session.execute(text("DROP TABLE IF EXISTS shikigamis"))
            db.session.commit()
            print("式神表删除成功！")
        except Exception as e:
            print(f"删除失败: {e}")


if __name__ == '__main__':
    upgrade()
