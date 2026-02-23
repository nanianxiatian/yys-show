"""
从阴阳师官网API获取式神列表并导入数据库
API: https://g37simulator.webapp.163.com/get_heroid_list
"""
import requests
import json
import re
import sys
import os

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

def fetch_shikigami_from_api():
    """从官网API获取式神数据"""
    
    # API接口
    api_url = "https://g37simulator.webapp.163.com/get_heroid_list"
    
    params = {
        'callback': 'jQuery_callback',
        'rarity': 0,  # 0表示所有稀有度
        'page': 1,
        'per_page': 300,  # 获取所有式神
        '_': '1771860675642'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://yys.163.com/'
    }
    
    try:
        print("正在请求式神数据...")
        response = requests.get(api_url, params=params, headers=headers, timeout=30)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            # 解析JSONP格式
            text = response.text
            print(f"响应长度: {len(text)}")
            
            # 提取JSON部分 (去掉jQuery_callback(和最后的))
            match = re.search(r'jQuery_callback\((.*)\)', text, re.DOTALL)
            if match:
                json_str = match.group(1)
                data = json.loads(json_str)
                
                if data.get('success'):
                    shikigami_list = data.get('data', {})
                    print(f"✓ 成功获取 {len(shikigami_list)} 个式神数据")
                    
                    # 保存原始数据
                    with open('shikigami_api_raw.json', 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    print("数据已保存到 shikigami_api_raw.json")
                    
                    return shikigami_list
                else:
                    print("API返回失败")
                    return None
            else:
                print("无法解析JSONP格式")
                print(f"响应内容: {text[:500]}")
                return None
        else:
            print(f"请求失败: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"获取失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def parse_shikigami_data(shikigami_dict):
    """解析式神数据"""
    shikigami_list = []
    
    for shikigami_id, info in shikigami_dict.items():
        try:
            # name是unicode编码字符串，如 "\u5deb\u86ca\u5e08"
            name_unicode = info.get('name', '')
            
            # 使用codecs解码unicode转义序列
            import codecs
            name = codecs.decode(name_unicode, 'unicode_escape')
            
            rarity_code = info.get('rarity', 1)
            rarity = RARITY_MAP.get(rarity_code, 'N')
            
            shikigami_list.append({
                'id': shikigami_id,
                'name': name,
                'rarity': rarity,
                'icon': info.get('icon', ''),
                'material_type': info.get('material_type', 0),
                'interactive': info.get('interactive', 0)
            })
            
        except Exception as e:
            print(f"解析式神 {shikigami_id} 失败: {e}, name={name_unicode}")
            continue
    
    return shikigami_list

def import_shikigami_to_db(shikigami_list):
    """将式神导入数据库"""
    app = create_app()
    
    with app.app_context():
        success_count = 0
        skip_count = 0
        error_count = 0
        
        # 统计各稀有度数量
        rarity_stats = {'N': 0, 'R': 0, 'SR': 0, 'SSR': 0, 'SP': 0, 'UR': 0}
        
        print(f"\n开始导入 {len(shikigami_list)} 个式神...")
        
        for shikigami in shikigami_list:
            try:
                name = shikigami['name']
                rarity = shikigami['rarity']
                
                # 检查是否已存在
                existing = Shikigami.query.filter_by(name=name).first()
                if existing:
                    skip_count += 1
                    continue
                
                # 创建式神
                new_shikigami = Shikigami(
                    name=name,
                    english_name='',
                    rarity=rarity,
                    description='',
                    skill_1='',
                    skill_2='',
                    skill_3=''
                )
                
                db.session.add(new_shikigami)
                success_count += 1
                rarity_stats[rarity] += 1
                
                # 每50条提交一次
                if success_count % 50 == 0:
                    db.session.commit()
                    print(f'>>> 已提交 {success_count} 条...')
                
            except Exception as e:
                error_count += 1
                print(f'添加 "{name}" 失败: {e}')
                db.session.rollback()
        
        # 最后提交
        if success_count > 0:
            db.session.commit()
            print(f'>>> 最终提交完成')
        
        print(f'\n{"="*50}')
        print(f'导入完成！')
        print(f'{"="*50}')
        print(f'成功: {success_count}')
        print(f'跳过: {skip_count}')
        print(f'失败: {error_count}')
        print(f'\n各稀有度统计:')
        for rarity, count in rarity_stats.items():
            if count > 0:
                print(f'  {rarity}: {count} 个')
        
        # 验证导入结果
        total = Shikigami.query.count()
        print(f'\n数据库中共有 {total} 个式神')

def main():
    """主函数"""
    # 获取数据
    shikigami_dict = fetch_shikigami_from_api()
    
    if shikigami_dict:
        # 解析数据
        shikigami_list = parse_shikigami_data(shikigami_dict)
        print(f"\n解析完成，共 {len(shikigami_list)} 个式神")
        
        # 显示前10个式神
        print("\n前10个式神预览:")
        for s in shikigami_list[:10]:
            print(f"  {s['name']} ({s['rarity']})")
        
        # 导入数据库
        import_shikigami_to_db(shikigami_list)
    else:
        print("获取数据失败")

if __name__ == '__main__':
    main()
