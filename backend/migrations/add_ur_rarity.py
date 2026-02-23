"""
为式神表添加 UR 稀有度选项迁移脚本
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import db
from sqlalchemy import text


def upgrade():
    """修改稀有度字段，添加 UR 选项"""
    app = create_app()
    with app.app_context():
        # 检查字段是否存在
        result = db.session.execute(text("""
            SELECT COUNT(*) FROM information_schema.columns 
            WHERE table_schema = DATABASE() 
            AND table_name = 'shikigamis'
            AND column_name = 'rarity'
        """))
        
        if result.scalar() == 0:
            print("稀有度字段不存在，请先运行 add_shikigami_rarity.py")
            return
        
        # 修改 ENUM 字段，添加 UR 选项
        # MySQL 修改 ENUM 需要重建字段
        sql = """
        ALTER TABLE shikigamis 
        MODIFY COLUMN rarity ENUM('N', 'R', 'SR', 'SSR', 'SP', 'UR') DEFAULT 'SR' 
        COMMENT '稀有度'
        """
        
        db.session.execute(text(sql))
        db.session.commit()
        print("UR 稀有度添加成功！")


def downgrade():
    """移除 UR 稀有度选项"""
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
                print("稀有度字段不存在，跳过")
                return
            
            # 将 UR 改为 SR
            db.session.execute(text("UPDATE shikigamis SET rarity = 'SR' WHERE rarity = 'UR'"))
            
            # 修改 ENUM 字段，移除 UR 选项
            sql = """
            ALTER TABLE shikigamis 
            MODIFY COLUMN rarity ENUM('N', 'R', 'SR', 'SSR', 'SP') DEFAULT 'SR' 
            COMMENT '稀有度'
            """
            db.session.execute(text(sql))
            db.session.commit()
            print("UR 稀有度已移除！")
        except Exception as e:
            print(f"移除失败: {e}")


if __name__ == '__main__':
    upgrade()
