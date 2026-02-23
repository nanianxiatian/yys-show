"""
调试式神分析
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db, OfficialResult
from datetime import date
from sqlalchemy import and_

def debug():
    """调试"""
    app = create_app()
    
    with app.app_context():
        start_date = date(2026, 2, 22)
        end_date = date(2026, 2, 23)
        
        print(f"查询日期范围: {start_date} 到 {end_date}")
        
        # 查询所有官方结果
        results = OfficialResult.query.filter(
            and_(
                OfficialResult.guess_date >= start_date,
                OfficialResult.guess_date <= end_date,
                OfficialResult.result.isnot(None)
            )
        ).all()
        
        print(f"找到 {len(results)} 条官方结果")
        
        for r in results:
            print(f"\n日期:{r.guess_date} 轮次:{r.guess_round} 结果:{r.result}")
            
            # 检查左侧式神
            print("  左侧式神:")
            for i in range(1, 6):
                shiki = getattr(r, f'left_shikigami_{i}')
                print(f"    left_shikigami_{i}: {shiki}")
            
            # 检查右侧式神
            print("  右侧式神:")
            for i in range(1, 6):
                shiki = getattr(r, f'right_shikigami_{i}')
                print(f"    right_shikigami_{i}: {shiki}")

if __name__ == '__main__':
    debug()
