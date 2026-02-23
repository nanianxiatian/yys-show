"""
导入SR式神到数据库
由于官网是动态加载，这里使用常见的SR式神列表
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models.shikigami import Shikigami
from app.models import db

# 常见的SR式神列表（根据阴阳师游戏整理）
SR_SHIKIGAMI = [
    # 经典SR式神
    "妖琴师", "樱花妖", "姑获鸟", "鬼使黑", "鬼使白",
    "桃花妖", "雪女", "鬼女红叶", "跳跳哥哥", "椒图",
    "镰鼬", "山兔", "食发鬼", "食梦貘", "傀儡师",
    "海坊主", "判官", "凤凰火", "雨女", "白狼",
    "清姬", "妖狐", "络新妇", "铁鼠", "跳跳妹妹",
    "兵俑", "丑时之女", "独眼小僧", "饿鬼", "巫蛊师",
    "座敷童子", "鲤鱼精", "河童", "童男", "童女",
    "管狐", "山童", "首无", "觉", "青蛙瓷器",
    "古笼火", "狸猫", "鸦天狗", "食人花", "灯笼鬼",
    "涂壁", "提灯小僧", "赤舌", "盗墓小鬼", "寄生魂",
    "唐纸伞妖", "天邪鬼绿", "天邪鬼赤", "天邪鬼青", "天邪鬼黄",
    "帚神", "涂壁", "一目连", "般若", "万年竹",
    "青坊主", "夜叉", "黑童子", "白童子", "书翁",
    "兔丸", "小松丸", "匣中少女", "鸩", "以津真天",
    "鸩", "弈", "猫掌柜", "薰", "化鲸",
    "久次良", "蟹姬", "纸舞", "星熊童子", "风狸",
    "蝎女", "入内雀", "饴细工", "川猿", "灵海蝶",
    "粉婆婆", "迦楼罗", "天逆每", "慧明灯", "萤草",
    "白藏主", "不知火", "大岳丸", "泷夜叉姬", "云外镜",
    "鬼童丸", "缘结神", "铃鹿御前", "紧那罗", "千姬",
    "帝释天", "阿修罗", "食灵", "饭笥", "铃彦姬",
    "不见岳", "须佐之男", "神启荒", "寻香行", "季",
    "月读", "流光追月神", "言灵", "孔雀明王", "天照",
    "渺念萤草", "闻人翊悬", "祸津神", "龙珏", "心友犬神",
    "遥念烟烟罗", "封阳君", "龙吟铃鹿御前", "心友犬神", "鬼金羊",
    " sp", "纺愿缘结神", "渺念萤草", "闻人翊悬", "祸津神"
]

def import_sr_shikigami():
    """导入SR式神"""
    app = create_app()
    with app.app_context():
        success_count = 0
        skip_count = 0
        
        for name in SR_SHIKIGAMI:
            try:
                # 检查是否已存在
                existing = Shikigami.query.filter_by(name=name).first()
                if existing:
                    print(f'跳过：式神 "{name}" 已存在')
                    skip_count += 1
                    continue
                
                # 创建式神
                shikigami = Shikigami(
                    name=name,
                    english_name='',
                    rarity='SR'
                )
                
                db.session.add(shikigami)
                success_count += 1
                print(f'准备添加: {name}')
                
                # 每10条提交一次
                if success_count % 10 == 0:
                    db.session.commit()
                    print(f'>>> 已提交 {success_count} 条...')
                
            except Exception as e:
                print(f'添加 "{name}" 失败: {e}')
                db.session.rollback()
        
        # 最后提交
        if success_count > 0:
            db.session.commit()
            print(f'>>> 最终提交完成')
        
        print(f'\n导入完成！')
        print(f'成功: {success_count}')
        print(f'跳过: {skip_count}')
        
        # 验证导入结果
        total = Shikigami.query.count()
        sr_count = Shikigami.query.filter_by(rarity='SR').count()
        print(f'\n数据库中共有 {total} 个式神')
        print(f'其中SR式神: {sr_count} 个')

if __name__ == '__main__':
    import_sr_shikigami()
