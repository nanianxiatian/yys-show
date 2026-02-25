"""
检查同步能力 - 测试不同日期的同步
"""
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import WeiboPost, Blogger

def check_sync_ability():
    """检查同步能力"""
    app = create_app()
    
    with app.app_context():
        print("=== 检查同步能力 ===\n")
        
        # 检查数据库中各日期的微博数量
        dates = ['2026-02-17', '2026-02-18', '2026-02-19', '2026-02-20', '2026-02-21', '2026-02-22', '2026-02-23']
        
        print("数据库中各日期的微博数量:\n")
        for date in dates:
            count = WeiboPost.query.filter(
                WeiboPost.guess_date == date
            ).count()
            print(f"  {date}: {count} 条")
        
        # 检查Mico林木森的数据
        print("\n\nMico林木森各日期的微博:\n")
        mico = Blogger.query.filter_by(nickname='Mico林木森').first()
        if mico:
            for date in dates:
                posts = WeiboPost.query.filter(
                    WeiboPost.blogger_id == mico.id,
                    WeiboPost.guess_date == date
                ).all()
                if posts:
                    print(f"  {date}: {len(posts)} 条")
                    for post in posts:
                        print(f"    - 轮次{post.guess_round}: {post.weibo_id}")
                else:
                    print(f"  {date}: 0 条")
        
        # 检查是否有2月17日的数据
        feb_17_count = WeiboPost.query.filter(
            WeiboPost.guess_date == '2026-02-17'
        ).count()
        
        print(f"\n\n2026-02-17 数据: {feb_17_count} 条")
        
        if feb_17_count > 0:
            print("\n✓ 2月17日的数据确实存在！")
            print("  这说明API可以获取到较早期的数据")
            print("  问题可能在于:")
            print("  1. 特定时间段的数据确实不存在")
            print("  2. 爬虫的翻页逻辑有问题")
            print("  3. 数据被标记为转发或其他原因被过滤")

if __name__ == '__main__':
    check_sync_ability()
