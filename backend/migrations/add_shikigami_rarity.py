"""
为式神表添加稀有度字段迁移脚本
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import db
from sqlalchemy import text


def upgrade():
    """添加稀有度字段"""
    app = create_app()
    with app.app_context():
        # 检查字段是否已存在
        result = db.session.execute(text("""
            SELECT COUNT(*) FROM information_schema.columns 
            WHERE table_schema = DATABASE() 
            AND table_name = 'shikigamis'
            AND column_name = 'rarity'
        """))
        
        if result.scalar() > 0:
            print("稀有度字段已存在，跳过创建")
            return
        
        # 添加稀有度字段
        sql = """
        ALTER TABLE shikigamis 
        ADD COLUMN rarity ENUM('N', 'R', 'SR', 'SSR', 'SP') DEFAULT 'SR' 
        COMMENT '稀有度' AFTER english_name
        """
        
        db.session.execute(text(sql))
        db.session.commit()
        print("稀有度字段添加成功！")


def downgrade():
    """删除稀有度字段"""
    app = create_app()
    with app.app_context():
        try:
            # 检查字段是否存在
            result = db.session.execute(text("""
                SELECT COUNT(*) FROM information_schema.columns 
                WHERE table_schema = DATABASE() 
                AND table_name = 'shikigamis'
                AND column_name = 'rarity'
            """))
            
            if result.scalar() == 0:
                print("稀有度字段不存在，跳过删除")
                return
            
            db.session.execute(text("ALTER TABLE shikigamis DROP COLUMN rarity"))
            db.session.commit()
            print("稀有度字段删除成功！")
        except Exception as e:
            print(f"删除失败: {e}")


if __name__ == '__main__':
    upgrade()
