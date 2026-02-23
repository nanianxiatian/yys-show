"""
重新导入式神数据，正确处理编码
"""
import sys
import os
import json
import codecs

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models.shikigami import Shikigami
from app.models import db

# 稀有度映射: 1-N, 2-R, 3-SR, 4-SSR, 5-SP, 6-UR
RARITY_MAP = {
    1: 'N',
    2: 'R', 
    3: 'SR',
    4: 'SSR',
    5: 'SP',
    6: 'UR'
}

def reimport_shikigami():
    """重新导入式神数据"""
    
    # 读取之前保存的原始数据
    with open('shikigami_api_raw.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    shikigami_dict = data.get('data', {})
    print(f"从文件读取到 {len(shikigami_dict)} 个式神数据")
    
    app = create_app()
    
    with app.app_context():
        # 先清空表
        print("\n清空现有式神数据...")
        Shikigami.query.delete()
        db.session.commit()
        print("已清空")
        
        success_count = 0
        error_count = 0
        rarity_stats = {'N': 0, 'R': 0, 'SR': 0, 'SSR': 0, 'SP': 0, 'UR': 0}
        
        print(f"\n开始导入 {len(shikigami_dict)} 个式神...")
        
        for shikigami_id, info in shikigami_dict.items():
            try:
                # 获取unicode编码的名称
                name_unicode = info.get('name', '')
                
                # 正确解码unicode转义序列
                # 方法: 使用codecs.decode
                name = codecs.decode(name_unicode, 'unicode_escape')
                
                rarity_code = info.get('rarity', 1)
                rarity = RARITY_MAP.get(rarity_code, 'N')
                
                # 创建式神
                shikigami = Shikigami(
                    name=name,
                    english_name='',
                    rarity=rarity,
                    description='',
                    skill_1='',
                    skill_2='',
                    skill_3=''
                )
                
                db.session.add(shikigami)
                success_count += 1
                rarity_stats[rarity] += 1
                
                # 每50条提交一次
                if success_count % 50 == 0:
                    db.session.commit()
                    print(f'>>> 已提交 {success_count} 条...')
                
            except Exception as e:
                error_count += 1
                print(f'导入式神 {shikigami_id} 失败: {e}')
                db.session.rollback()
        
        # 最后提交
        if success_count > 0:
            db.session.commit()
            print(f'>>> 最终提交完成')
        
        print(f'\n{"="*50}')
        print(f'导入完成！')
        print(f'{"="*50}')
        print(f'成功: {success_count}')
        print(f'失败: {error_count}')
        print(f'\n各稀有度统计:')
        for rarity, count in rarity_stats.items():
            if count > 0:
                print(f'  {rarity}: {count} 个')
        
        # 验证导入结果
        total = Shikigami.query.count()
        print(f'\n数据库中共有 {total} 个式神')
        
        # 显示前10个验证
        print('\n验证前10个式神:')
        shikigamis = Shikigami.query.limit(10).all()
        for s in shikigamis:
            print(f'  {s.name} ({s.rarity})')

if __name__ == '__main__':
    reimport_shikigami()
