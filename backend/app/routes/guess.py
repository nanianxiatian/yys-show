from flask import request, jsonify
from datetime import datetime, date
from sqlalchemy import func, case as sql_case
from app.models import db, BloggerStats
from app.services import GuessAnalyzerService
from . import guess_bp


@guess_bp.route('/analysis', methods=['GET'])
def get_guess_analysis():
    """获取竞猜分析结果"""
    # 查询参数
    target_date = request.args.get('date')
    
    if target_date:
        try:
            target_date = datetime.strptime(target_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({
                'success': False,
                'message': '日期格式错误，应为 YYYY-MM-DD'
            }), 400
    else:
        target_date = date.today()
    
    result = GuessAnalyzerService.analyze_daily_guesses(target_date)
    
    return jsonify({
        'success': True,
        'data': result
    })


@guess_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    """获取博主排行榜"""
    date_range = request.args.get('range', '7d')  # 7d, 30d, all
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # 如果提供了自定义日期范围，优先使用
    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            leaderboard = GuessAnalyzerService.get_leaderboard_custom(start_date, end_date)
            return jsonify({
                'success': True,
                'data': leaderboard,
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d')
            })
        except ValueError:
            return jsonify({
                'success': False,
                'message': '日期格式错误，应为 YYYY-MM-DD'
            }), 400
    
    # 使用预设范围
    if date_range not in ['7d', '30d', 'all']:
        return jsonify({
            'success': False,
            'message': '时间范围参数错误，可选: 7d, 30d, all'
        }), 400
    
    leaderboard = GuessAnalyzerService.get_leaderboard(date_range)
    
    return jsonify({
        'success': True,
        'data': leaderboard,
        'range': date_range
    })


@guess_bp.route('/blogger/<int:blogger_id>/stats', methods=['GET'])
def get_blogger_stats(blogger_id):
    """获取单个博主统计"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # 解析日期
    if start_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({
                'success': False,
                'message': '开始日期格式错误'
            }), 400
    
    if end_date:
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({
                'success': False,
                'message': '结束日期格式错误'
            }), 400
    
    stats = GuessAnalyzerService.get_blogger_stats(blogger_id, start_date, end_date)
    
    if not stats:
        return jsonify({
            'success': False,
            'message': '博主不存在或无统计数据'
        }), 404
    
    return jsonify({
        'success': True,
        'data': stats
    })


@guess_bp.route('/stats/update', methods=['POST'])
def update_stats():
    """手动更新统计数据"""
    data = request.get_json() or {}
    target_date = data.get('date')
    
    if target_date:
        try:
            target_date = datetime.strptime(target_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({
                'success': False,
                'message': '日期格式错误'
            }), 400
    else:
        target_date = date.today()
    
    count = GuessAnalyzerService.update_daily_stats(target_date)
    
    return jsonify({
        'success': True,
        'message': f'已更新 {count} 条统计记录',
        'data': {
            'updated_count': count,
            'date': target_date.strftime('%Y-%m-%d')
        }
    })


@guess_bp.route('/history', methods=['GET'])
def get_guess_history():
    """获取历史竞猜记录"""
    blogger_id = request.args.get('blogger_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    from app.models import WeiboPost, OfficialResult
    from sqlalchemy import func
    
    # 构建查询
    query = db.session.query(
        WeiboPost,
        OfficialResult.result.label('official_result')
    ).outerjoin(
        OfficialResult,
        (WeiboPost.guess_date == OfficialResult.guess_date) &
        (WeiboPost.guess_round == OfficialResult.guess_round)
    )
    # 不再限制is_guess_related，统计所有微博
    
    if blogger_id:
        query = query.filter(WeiboPost.blogger_id == blogger_id)
    
    if start_date:
        query = query.filter(WeiboPost.guess_date >= start_date)
    
    if end_date:
        query = query.filter(WeiboPost.guess_date <= end_date)
    
    results = query.order_by(WeiboPost.guess_date.desc(), WeiboPost.guess_round.asc()).all()
    
    data = []
    for post, official_result in results:
        item = post.to_dict()
        item['official_result'] = official_result
        
        # 判断预测状态
        if official_result:
            if post.guess_prediction == 'unknown':
                item['status'] = 'unknown'
            elif post.guess_prediction == official_result:
                item['status'] = 'correct'
            else:
                item['status'] = 'wrong'
        else:
            item['status'] = 'pending'
        
        data.append(item)
    
    return jsonify({
        'success': True,
        'data': data,
        'total': len(data)
    })


@guess_bp.route('/red-blue-stats', methods=['GET'])
def get_red_blue_stats():
    """获取红蓝方胜率统计"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # 解析日期
    if start_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({
                'success': False,
                'message': '开始日期格式错误，应为 YYYY-MM-DD'
            }), 400
    else:
        # 默认2026-02-17
        start_date = datetime.strptime('2026-02-17', '%Y-%m-%d').date()
    
    if end_date:
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({
                'success': False,
                'message': '结束日期格式错误，应为 YYYY-MM-DD'
            }), 400
    else:
        # 默认2026-02-23
        end_date = datetime.strptime('2026-02-23', '%Y-%m-%d').date()
    
    from app.models import OfficialResult
    
    # 查询每日红蓝方统计
    daily_stats = db.session.query(
        OfficialResult.guess_date,
        func.count(sql_case((OfficialResult.result == 'left', 1), else_=None)).label('red_wins'),
        func.count(sql_case((OfficialResult.result == 'right', 1), else_=None)).label('blue_wins'),
        func.count(OfficialResult.id).label('total')
    ).filter(
        OfficialResult.guess_date >= start_date,
        OfficialResult.guess_date <= end_date
    ).group_by(
        OfficialResult.guess_date
    ).order_by(
        OfficialResult.guess_date.asc()
    ).all()
    
    # 计算总计
    total_red = 0
    total_blue = 0
    total_count = 0
    
    data = []
    for stat in daily_stats:
        date_str = stat.guess_date.strftime('%Y-%m-%d')
        red_rate = round((stat.red_wins / stat.total * 100), 2) if stat.total > 0 else 0
        blue_rate = round((stat.blue_wins / stat.total * 100), 2) if stat.total > 0 else 0
        
        data.append({
            'date': date_str,
            'red_wins': stat.red_wins,
            'blue_wins': stat.blue_wins,
            'total': stat.total,
            'red_rate': red_rate,
            'blue_rate': blue_rate
        })
        
        total_red += stat.red_wins
        total_blue += stat.blue_wins
        total_count += stat.total
    
    # 计算总体胜率
    overall_red_rate = round((total_red / total_count * 100), 2) if total_count > 0 else 0
    overall_blue_rate = round((total_blue / total_count * 100), 2) if total_count > 0 else 0
    
    return jsonify({
        'success': True,
        'data': {
            'daily_stats': data,
            'summary': {
                'total_red': total_red,
                'total_blue': total_blue,
                'total_count': total_count,
                'overall_red_rate': overall_red_rate,
                'overall_blue_rate': overall_blue_rate
            },
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d')
        }
    })
