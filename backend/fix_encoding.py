"""
修复数据库中式神名称的编码问题
"""
import sys
import os
import codecs

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models.shikigami import Shikigami
from app.models import db

def fix_encoding():
    """修复编码问题"""
    app = create_app()
    
    with app.app_context():
        shikigamis = Shikigami.query.all()
        
        fixed_count = 0
        for s in shikigamis:
            try:
                # 尝试修复编码
                # 如果名称已经是正确的UTF-8，则跳过
                if 'å' not in s.name and 'ç' not in s.name:
                    continue
                
                # 尝试用latin1编码然后utf8解码
                try:
                    fixed_name = s.name.encode('latin1').decode('utf-8')
                    s.name = fixed_name
                    fixed_count += 1
                    print(f'修复: {fixed_name}')
                except:
                    pass
                    
            except Exception as e:
                print(f'修复 "{s.name}" 失败: {e}')
        
        if fixed_count > 0:
            db.session.commit()
            print(f'\n共修复 {fixed_count} 个式神名称')
        else:
            print('没有需要修复的编码问题')

def show_shikigami():
    """显示所有式神"""
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
        
        # 显示所有式神
        print(f'\n所有式神列表:')
        shikigamis = Shikigami.query.order_by(Shikigami.rarity, Shikigami.id).all()
        current_rarity = None
        for s in shikigamis:
            if s.rarity != current_rarity:
                current_rarity = s.rarity
                print(f'\n【{s.rarity}级式神】')
            print(f'  {s.name}')

if __name__ == '__main__':
    # 先显示当前状态
    print("="*60)
    print("当前数据库状态")
    print("="*60)
    show_shikigami()
