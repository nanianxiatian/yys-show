"""
式神分析路由
"""
from flask import request, jsonify
from ..models import db
from ..models.official_result import OfficialResult
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from . import shikigami_bp


@shikigami_bp.route('/analysis', methods=['GET'])
def get_shikigami_analysis():
    """
    获取式神出场次数及胜率分析
    参数:
    - start_date: 开始日期 (可选，默认30天前)
    - end_date: 结束日期 (可选，默认今天)
    """
    try:
        # 获取日期参数
        end_date_str = request.args.get('end_date')
        start_date_str = request.args.get('start_date')
        
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        else:
            end_date = datetime.now().date()
        
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        else:
            start_date = end_date - timedelta(days=30)
        
        # 查询所有官方结果
        results = OfficialResult.query.filter(
            and_(
                OfficialResult.guess_date >= start_date,
                OfficialResult.guess_date <= end_date,
                OfficialResult.result.isnot(None)
            )
        ).all()
        
        # 统计式神数据
        shikigami_stats = {}
        
        for result in results:
            # 左侧式神
            for i in range(1, 6):
                shiki_name = getattr(result, f'left_shikigami_{i}')
                if shiki_name:
                    if shiki_name not in shikigami_stats:
                        shikigami_stats[shiki_name] = {
                            'name': shiki_name,
                            'appearances': 0,
                            'wins': 0,
                            'losses': 0
                        }
                    shikigami_stats[shiki_name]['appearances'] += 1
                    if result.result == 'left':
                        shikigami_stats[shiki_name]['wins'] += 1
                    else:
                        shikigami_stats[shiki_name]['losses'] += 1
            
            # 右侧式神
            for i in range(1, 6):
                shiki_name = getattr(result, f'right_shikigami_{i}')
                if shiki_name:
                    if shiki_name not in shikigami_stats:
                        shikigami_stats[shiki_name] = {
                            'name': shiki_name,
                            'appearances': 0,
                            'wins': 0,
                            'losses': 0
                        }
                    shikigami_stats[shiki_name]['appearances'] += 1
                    if result.result == 'right':
                        shikigami_stats[shiki_name]['wins'] += 1
                    else:
                        shikigami_stats[shiki_name]['losses'] += 1
        
        # 转换为列表并计算胜率
        analysis_list = []
        for name, stats in shikigami_stats.items():
            win_rate = round((stats['wins'] / stats['appearances']) * 100, 2) if stats['appearances'] > 0 else 0
            analysis_list.append({
                'name': name,
                'appearances': stats['appearances'],
                'wins': stats['wins'],
                'losses': stats['losses'],
                'win_rate': win_rate
            })
        
        # 按出场次数降序排序
        analysis_list.sort(key=lambda x: x['appearances'], reverse=True)
        
        return jsonify({
            'success': True,
            'data': analysis_list,
            'total': len(analysis_list),
            'date_range': {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d')
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'分析失败: {str(e)}'
        }), 500


@shikigami_bp.route('/list', methods=['GET'])
def get_shikigami_list():
    """获取所有式神名称列表（用于下拉选择）"""
    try:
        # 从数据库中提取所有唯一的式神名称
        shikigami_set = set()
        
        for i in range(1, 6):
            # 左侧式神
            left_results = db.session.query(
                getattr(OfficialResult, f'left_shikigami_{i}')
            ).filter(
                getattr(OfficialResult, f'left_shikigami_{i}').isnot(None)
            ).distinct().all()
            
            for result in left_results:
                if result[0]:
                    shikigami_set.add(result[0])
            
            # 右侧式神
            right_results = db.session.query(
                getattr(OfficialResult, f'right_shikigami_{i}')
            ).filter(
                getattr(OfficialResult, f'right_shikigami_{i}').isnot(None)
            ).distinct().all()
            
            for result in right_results:
                if result[0]:
                    shikigami_set.add(result[0])
        
        return jsonify({
            'success': True,
            'data': sorted(list(shikigigami_set))
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取式神列表失败: {str(e)}'
        }), 500
