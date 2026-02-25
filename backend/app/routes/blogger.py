from flask import request, jsonify
from app.models import db, Blogger
from . import blogger_bp


@blogger_bp.route('', methods=['GET'])
def get_bloggers():
    """获取博主列表"""
    # 查询参数
    is_active = request.args.get('is_active', type=lambda x: x.lower() == 'true')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    query = Blogger.query
    if is_active is not None:
        query = query.filter_by(is_active=is_active)
    
    # 获取总数
    total = query.count()
    
    # 分页查询
    bloggers = query.order_by(Blogger.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'data': [b.to_dict() for b in bloggers.items],
        'pagination': {
            'page': bloggers.page,
            'per_page': bloggers.per_page,
            'total': total,
            'pages': bloggers.pages
        }
    })


@blogger_bp.route('/<int:blogger_id>', methods=['GET'])
def get_blogger(blogger_id):
    """获取单个博主信息"""
    blogger = Blogger.query.get(blogger_id)
    
    if not blogger:
        return jsonify({
            'success': False,
            'message': '博主不存在'
        }), 404
    
    return jsonify({
        'success': True,
        'data': blogger.to_dict()
    })


@blogger_bp.route('', methods=['POST'])
def create_blogger():
    """创建博主"""
    data = request.get_json()
    
    if not data or not data.get('nickname'):
        return jsonify({
            'success': False,
            'message': '博主昵称不能为空'
        }), 400
    
    # 检查是否已存在
    existing = Blogger.query.filter_by(nickname=data['nickname']).first()
    if existing:
        return jsonify({
            'success': False,
            'message': '该博主已存在'
        }), 400
    
    blogger = Blogger(
        nickname=data['nickname'],
        weibo_uid=data.get('weibo_uid'),
        profile_url=data.get('profile_url'),
        avatar_url=data.get('avatar_url'),
        description=data.get('description'),
        is_active=data.get('is_active', True)
    )
    
    db.session.add(blogger)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '创建成功',
        'data': blogger.to_dict()
    }), 201


@blogger_bp.route('/<int:blogger_id>', methods=['PUT'])
def update_blogger(blogger_id):
    """更新博主信息"""
    blogger = Blogger.query.get(blogger_id)
    
    if not blogger:
        return jsonify({
            'success': False,
            'message': '博主不存在'
        }), 404
    
    data = request.get_json()
    
    if 'nickname' in data:
        # 检查新昵称是否已存在
        existing = Blogger.query.filter(
            Blogger.nickname == data['nickname'],
            Blogger.id != blogger_id
        ).first()
        if existing:
            return jsonify({
                'success': False,
                'message': '该昵称已被使用'
            }), 400
        blogger.nickname = data['nickname']
    
    if 'weibo_uid' in data:
        blogger.weibo_uid = data['weibo_uid']
    if 'profile_url' in data:
        blogger.profile_url = data['profile_url']
    if 'avatar_url' in data:
        blogger.avatar_url = data['avatar_url']
    if 'description' in data:
        blogger.description = data['description']
    if 'is_active' in data:
        blogger.is_active = data['is_active']
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '更新成功',
        'data': blogger.to_dict()
    })


@blogger_bp.route('/<int:blogger_id>', methods=['DELETE'])
def delete_blogger(blogger_id):
    """删除博主及其所有相关数据"""
    from app.models import WeiboPost, SpiderLog
    
    blogger = Blogger.query.get(blogger_id)
    
    if not blogger:
        return jsonify({
            'success': False,
            'message': '博主不存在'
        }), 404
    
    # 先删除该博主的所有微博
    weibo_count = WeiboPost.query.filter_by(blogger_id=blogger_id).count()
    WeiboPost.query.filter_by(blogger_id=blogger_id).delete()
    
    # 删除该博主的爬虫日志
    log_count = SpiderLog.query.filter_by(blogger_id=blogger_id).count()
    SpiderLog.query.filter_by(blogger_id=blogger_id).delete()
    
    # 再删除博主
    db.session.delete(blogger)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'删除成功，同时删除了 {weibo_count} 条微博和 {log_count} 条日志'
    })


@blogger_bp.route('/<int:blogger_id>/sync', methods=['POST'])
def sync_blogger(blogger_id):
    """手动同步单个博主信息（只同步头像、UID等，不爬取微博）"""
    from app.services import WeiboSpiderService
    
    spider_service = WeiboSpiderService()
    result = spider_service.sync_blogger_info(blogger_id)
    
    if result['success']:
        return jsonify({
            'success': True,
            'message': result.get('message', '同步成功'),
            'data': result.get('data')
        })
    else:
        return jsonify({
            'success': False,
            'message': result.get('error', '同步失败')
        }), 500


@blogger_bp.route('/<int:blogger_id>/sync-weibo', methods=['POST'])
def sync_blogger_weibo(blogger_id):
    """手动同步单个博主的微博（异步）"""
    from app.services import WeiboSpiderService, TaskManager
    
    # 创建异步任务
    task_id = TaskManager.create_task('sync_weibo', {'blogger_id': blogger_id})
    
    # 异步执行同步
    def do_sync():
        spider_service = WeiboSpiderService()
        return spider_service.spider_single_blogger(blogger_id)
    
    TaskManager.run_task_async(task_id, do_sync)
    
    return jsonify({
        'success': True,
        'message': '同步任务已启动',
        'task_id': task_id
    })


@blogger_bp.route('/sync-task/<task_id>', methods=['GET'])
def get_sync_task_status(task_id):
    """获取同步任务状态"""
    from app.services import TaskManager
    
    task = TaskManager.get_task(task_id)
    if not task:
        return jsonify({
            'success': False,
            'message': '任务不存在'
        }), 404
    
    return jsonify({
        'success': True,
        'data': task
    })
