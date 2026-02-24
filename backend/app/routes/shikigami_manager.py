"""
式神管理路由
"""
from flask import request, jsonify
from ..models import db
from ..models.shikigami import Shikigami
from . import shikigami_manager_bp


@shikigami_manager_bp.route('', methods=['GET'])
def get_shikigami_list():
    """获取式神列表"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        keyword = request.args.get('keyword', '')
        rarity = request.args.get('rarity', '')
        
        query = Shikigami.query
        
        if keyword:
            query = query.filter(Shikigami.name.contains(keyword))
        
        if rarity:
            query = query.filter(Shikigami.rarity == rarity)
        
        pagination = query.order_by(Shikigami.id.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'success': True,
            'data': [s.to_dict() for s in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取式神列表失败: {str(e)}'
        }), 500


@shikigami_manager_bp.route('/all', methods=['GET'])
def get_all_shikigami():
    """获取所有式神（用于下拉选择）"""
    try:
        shikigamis = Shikigami.query.order_by(Shikigami.name).all()
        return jsonify({
            'success': True,
            'data': [s.to_dict() for s in shikigamis]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取式神列表失败: {str(e)}'
        }), 500


@shikigami_manager_bp.route('/<int:id>', methods=['GET'])
def get_shikigami(id):
    """获取单个式神详情"""
    try:
        shikigami = Shikigami.query.get(id)
        if not shikigami:
            return jsonify({
                'success': False,
                'message': '式神不存在'
            }), 404
        
        return jsonify({
            'success': True,
            'data': shikigami.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取式神详情失败: {str(e)}'
        }), 500


@shikigami_manager_bp.route('', methods=['POST'])
def create_shikigami():
    """创建式神"""
    try:
        data = request.get_json()
        
        # 检查必填字段
        if not data.get('name'):
            return jsonify({
                'success': False,
                'message': '式神名称不能为空'
            }), 400
        
        # 检查是否已存在
        existing = Shikigami.query.filter_by(name=data['name']).first()
        if existing:
            return jsonify({
                'success': False,
                'message': '该式神已存在'
            }), 400
        
        shikigami = Shikigami(
            name=data['name'],
            english_name=data.get('english_name', ''),
            rarity=data.get('rarity', 'SR'),
            skill_1=data.get('skill_1', ''),
            skill_2=data.get('skill_2', ''),
            skill_3=data.get('skill_3', ''),
            description=data.get('description', '')
        )
        
        db.session.add(shikigami)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '创建成功',
            'data': shikigami.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'创建式神失败: {str(e)}'
        }), 500


@shikigami_manager_bp.route('/<int:id>', methods=['PUT'])
def update_shikigami(id):
    """更新式神"""
    try:
        shikigami = Shikigami.query.get(id)
        if not shikigami:
            return jsonify({
                'success': False,
                'message': '式神不存在'
            }), 404
        
        data = request.get_json()
        
        # 检查名称是否被其他式神使用
        if data.get('name') and data['name'] != shikigami.name:
            existing = Shikigami.query.filter_by(name=data['name']).first()
            if existing:
                return jsonify({
                    'success': False,
                    'message': '该式神名称已被使用'
                }), 400
            shikigami.name = data['name']
        
        shikigami.english_name = data.get('english_name', shikigami.english_name)
        shikigami.rarity = data.get('rarity', shikigami.rarity)
        shikigami.skill_1 = data.get('skill_1', shikigami.skill_1)
        shikigami.skill_2 = data.get('skill_2', shikigami.skill_2)
        shikigami.skill_3 = data.get('skill_3', shikigami.skill_3)
        shikigami.description = data.get('description', shikigami.description)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '更新成功',
            'data': shikigami.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'更新式神失败: {str(e)}'
        }), 500


@shikigami_manager_bp.route('/<int:id>', methods=['DELETE'])
def delete_shikigami(id):
    """删除式神"""
    try:
        shikigami = Shikigami.query.get(id)
        if not shikigami:
            return jsonify({
                'success': False,
                'message': '式神不存在'
            }), 404
        
        db.session.delete(shikigami)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '删除成功'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'删除式神失败: {str(e)}'
        }), 500


@shikigami_manager_bp.route('/batch', methods=['POST'])
def batch_create_shikigami():
    """批量创建式神"""
    try:
        data = request.get_json()
        names = data.get('names', [])
        
        if not names:
            return jsonify({
                'success': False,
                'message': '式神名称列表不能为空'
            }), 400
        
        created_count = 0
        skipped_count = 0
        
        for name in names:
            name = name.strip()
            if not name:
                continue
            
            existing = Shikigami.query.filter_by(name=name).first()
            if existing:
                skipped_count += 1
                continue
            
            shikigami = Shikigami(name=name, rarity='SR')
            db.session.add(shikigami)
            created_count += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'批量创建完成，成功{created_count}个，跳过{skipped_count}个',
            'created_count': created_count,
            'skipped_count': skipped_count
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'批量创建失败: {str(e)}'
        }), 500
