"""
验证数据库中的式神数据
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models.shikigami import Shikigami

def verify_data():
    """验证数据"""
    app = create_app()
    
    with app.app_context():
        # 统计
        total = Shikigami.query.count()
        print(f'数据库中共有 {total} 个式神\n')
        
        # 各稀有度统计
        for rarity in ['N', 'R', 'SR', 'SSR', 'SP', 'UR']:
            count = Shikigami.query.filter_by(rarity=rarity).count()
            print(f'{rarity}: {count} 个')
        
        # 显示几个示例
        print('\n示例式神（检查中文是否正确）:')
        samples = [
            Shikigami.query.filter_by(rarity='UR').first(),
            Shikigami.query.filter_by(name='妖刀姬·绯夜猎刃').first(),
            Shikigami.query.filter_by(name='大天狗').first(),
            Shikigami.query.filter_by(name='不知火').first(),
        ]
        
        for s in samples:
            if s:
                print(f'  ID:{s.id} {s.name} ({s.rarity})')
                # 检查名称长度（中文字符应该正确存储）
                print(f'    名称长度: {len(s.name)} 字符')
                print(f'    名称bytes: {s.name.encode("utf-8")}')

if __name__ == '__main__':
    verify_data()
