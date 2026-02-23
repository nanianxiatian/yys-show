"""
检查数据库中的式神
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models.shikigami import Shikigami

def check_shikigami():
    app = create_app()
    
    with app.app_context():
        # 统计各稀有度数量
        rarity_stats = {'N': 0, 'R': 0, 'SR': 0, 'SSR': 0, 'SP': 0, 'UR': 0}
        
        for rarity in rarity_stats.keys():
            count = Shikigami.query.filter_by(rarity=rarity).count()
            rarity_stats[rarity] = count
        
        total = Shikigami.query.count()
        
        print(f'数据库中共有 {total} 个式神')
        print(f'\n各稀有度统计:')
        for rarity, count in rarity_stats.items():
            print(f'  {rarity}: {count} 个')
        
        # 显示前20个式神
        print(f'\n前20个式神:')
        shikigamis = Shikigami.query.limit(20).all()
        for s in shikigamis:
            print(f'  {s.name} ({s.rarity})')

if __name__ == '__main__':
    check_shikigami()
