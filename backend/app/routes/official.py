from flask import request, jsonify
from datetime import datetime
from app.models import db, OfficialResult
from . import official_bp


@official_bp.route('', methods=['GET'])
def get_official_results():
    """获取官方结果列表"""
    # 查询参数
    guess_date = request.args.get('date')
    guess_round = request.args.get('round', type=int)
    
    query = OfficialResult.query
    
    if guess_date:
        query = query.filter_by(guess_date=guess_date)
    if guess_round:
        query = query.filter_by(guess_round=guess_round)
    
    results = query.order_by(OfficialResult.guess_date.desc(), OfficialResult.guess_round.asc()).all()
    
    return jsonify({
        'success': True,
        'data': [r.to_dict() for r in results],
        'total': len(results)
    })


@official_bp.route('/<int:result_id>', methods=['GET'])
def get_official_result(result_id):
    """获取单个官方结果"""
    result = OfficialResult.query.get(result_id)
    
    if not result:
        return jsonify({
            'success': False,
            'message': '记录不存在'
        }), 404
    
    return jsonify({
        'success': True,
        'data': result.to_dict()
    })


@official_bp.route('', methods=['POST'])
def create_official_result():
    """创建官方结果"""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'message': '数据不能为空'
        }), 400
    
    # 必填字段验证
    required_fields = ['guess_date', 'guess_round', 'result']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'success': False,
                'message': f'缺少必填字段: {field}'
            }), 400
    
    # 检查是否已存在
    existing = OfficialResult.query.filter_by(
        guess_date=data['guess_date'],
        guess_round=data['guess_round']
    ).first()
    
    if existing:
        return jsonify({
            'success': False,
            'message': '该轮次的官方结果已存在，请使用更新接口'
        }), 400
    
    result = OfficialResult(
        guess_date=data['guess_date'],
        guess_round=data['guess_round'],
        result=data['result'],
        left_team=data.get('left_team'),
        right_team=data.get('right_team'),
        description=data.get('description'),
        created_by=data.get('created_by', 'admin')
    )
    
    # 设置左侧式神
    for i in range(1, 6):
        field = f'left_shikigami_{i}'
        if field in data:
            setattr(result, field, data[field])
    
    # 设置右侧式神
    for i in range(1, 6):
        field = f'right_shikigami_{i}'
        if field in data:
            setattr(result, field, data[field])
    
    db.session.add(result)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '创建成功',
        'data': result.to_dict()
    }), 201


@official_bp.route('/<int:result_id>', methods=['PUT'])
def update_official_result(result_id):
    """更新官方结果"""
    result = OfficialResult.query.get(result_id)
    
    if not result:
        return jsonify({
            'success': False,
            'message': '记录不存在'
        }), 404
    
    data = request.get_json()
    
    if 'result' in data:
        result.result = data['result']
    if 'left_team' in data:
        result.left_team = data['left_team']
    if 'right_team' in data:
        result.right_team = data['right_team']
    if 'description' in data:
        result.description = data['description']
    
    # 更新左侧式神
    for i in range(1, 6):
        field = f'left_shikigami_{i}'
        if field in data:
            setattr(result, field, data[field])
    
    # 更新右侧式神
    for i in range(1, 6):
        field = f'right_shikigami_{i}'
        if field in data:
            setattr(result, field, data[field])
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '更新成功',
        'data': result.to_dict()
    })


@official_bp.route('/<int:result_id>', methods=['DELETE'])
def delete_official_result(result_id):
    """删除官方结果"""
    result = OfficialResult.query.get(result_id)
    
    if not result:
        return jsonify({
            'success': False,
            'message': '记录不存在'
        }), 404
    
    db.session.delete(result)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '删除成功'
    })


@official_bp.route('/batch', methods=['POST'])
def batch_create_official_results():
    """批量创建官方结果(用于一天录入所有轮次)"""
    data = request.get_json()
    
    if not data or not isinstance(data, list):
        return jsonify({
            'success': False,
            'message': '数据格式错误，应为数组'
        }), 400
    
    created_count = 0
    updated_count = 0
    errors = []
    
    for item in data:
        try:
            # 检查必填字段
            if not all(k in item for k in ['guess_date', 'guess_round', 'result']):
                errors.append(f"数据缺失必填字段: {item}")
                continue
            
            # 检查是否已存在
            existing = OfficialResult.query.filter_by(
                guess_date=item['guess_date'],
                guess_round=item['guess_round']
            ).first()
            
            if existing:
                # 更新现有记录
                existing.result = item['result']
                existing.left_team = item.get('left_team', existing.left_team)
                existing.right_team = item.get('right_team', existing.right_team)
                existing.description = item.get('description', existing.description)
                updated_count += 1
            else:
                # 创建新记录
                result = OfficialResult(
                    guess_date=item['guess_date'],
                    guess_round=item['guess_round'],
                    result=item['result'],
                    left_team=item.get('left_team'),
                    right_team=item.get('right_team'),
                    description=item.get('description'),
                    created_by=item.get('created_by', 'admin')
                )
                db.session.add(result)
                created_count += 1
                
        except Exception as e:
            errors.append(f"处理数据失败 {item}: {str(e)}")
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'批量处理完成: 创建 {created_count} 条, 更新 {updated_count} 条',
        'data': {
            'created': created_count,
            'updated': updated_count,
            'errors': errors
        }
    })


@official_bp.route('/dates', methods=['GET'])
def get_available_dates():
    """获取有官方结果的日期列表"""
    from sqlalchemy import func
    
    dates = db.session.query(
        OfficialResult.guess_date,
        func.count(OfficialResult.id).label('round_count')
    ).group_by(OfficialResult.guess_date).order_by(OfficialResult.guess_date.desc()).all()
    
    return jsonify({
        'success': True,
        'data': [
            {
                'date': d.guess_date.strftime('%Y-%m-%d'),
                'round_count': d.round_count
            }
            for d in dates
        ]
    })
