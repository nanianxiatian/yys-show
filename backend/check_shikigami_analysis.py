"""
检查式神分析数据
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db, Shikigami, OfficialResult, WeiboPost
from datetime import date

def check_data():
    """检查数据"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("1. 检查式神表数据")
        print("=" * 60)
        
        shikigami_count = Shikigami.query.count()
        print(f"式神总数: {shikigami_count}")
        
        print("\n" + "=" * 60)
        print("2. 检查22-23号官方结果数据")
        print("=" * 60)
        
        official_results = OfficialResult.query.filter(
            OfficialResult.guess_date.in_([date(2026, 2, 22), date(2026, 2, 23)])
        ).all()
        
        print(f"22-23号官方结果总数: {len(official_results)}")
        
        for r in official_results:
            print(f"\n  日期:{r.guess_date} 轮次:{r.guess_round} 结果:{r.result}")
            left_shikigamis = [r.left_shikigami_1, r.left_shikigami_2, r.left_shikigami_3, r.left_shikigami_4, r.left_shikigami_5]
            right_shikigamis = [r.right_shikigami_1, r.right_shikigami_2, r.right_shikigami_3, r.right_shikigami_4, r.right_shikigami_5]
            print(f"    左方式神: {[s for s in left_shikigamis if s]}")
            print(f"    右方式神: {[s for s in right_shikigamis if s]}")
        
        print("\n" + "=" * 60)
        print("3. 检查22-23号微博数据")
        print("=" * 60)
        
        posts = WeiboPost.query.filter(
            WeiboPost.guess_date.in_([date(2026, 2, 22), date(2026, 2, 23)])
        ).all()
        
        print(f"22-23号微博总数: {len(posts)}")
        
        for p in posts:
            print(f"  {p.blogger.nickname if p.blogger else '未知'}: 日期={p.guess_date} 轮次={p.guess_round} 预测={p.guess_prediction}")

if __name__ == '__main__':
    check_data()
