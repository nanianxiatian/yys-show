"""
最终验证数据库中的式神数据
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models.shikigami import Shikigami

def final_verify():
    """最终验证"""
    app = create_app()
    
    with app.app_context():
        # 统计
        total = Shikigami.query.count()
        print(f'✓ 数据库中共有 {total} 个式神\n')
        
        # 各稀有度统计
        print('各稀有度统计:')
        for rarity in ['N', 'R', 'SR', 'SSR', 'SP', 'UR']:
            count = Shikigami.query.filter_by(rarity=rarity).count()
            print(f'  {rarity}: {count} 个')
        
        # 显示各稀有度的部分式神
        print('\n各稀有度式神示例:')
        for rarity in ['N', 'R', 'SR', 'SSR', 'SP', 'UR']:
            shikigamis = Shikigami.query.filter_by(rarity=rarity).limit(5).all()
            if shikigamis:
                print(f'\n【{rarity}级式神】({Shikigami.query.filter_by(rarity=rarity).count()}个)')
                for s in shikigamis:
                    print(f'  - {s.name}')

if __name__ == '__main__':
    final_verify()
