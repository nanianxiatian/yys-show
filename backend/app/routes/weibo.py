from flask import request, jsonify
from app.models import db, WeiboPost, Blogger
from . import weibo_bp


@weibo_bp.route('', methods=['GET'])
def get_weibo_list():
    """获取微博列表"""
    # 查询参数
    blogger_id = request.args.get('blogger_id', type=int)
    guess_date = request.args.get('date')
    guess_round = request.args.get('round', type=int)
    is_guess_related = request.args.get('is_guess_related', type=lambda x: x.lower() == 'true')
    guess_prediction = request.args.get('guess_prediction')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # 调试日志
    print(f"[DEBUG] guess_prediction参数: {guess_prediction}", flush=True)
    print(f"[DEBUG] 所有参数: {dict(request.args)}", flush=True)
    
    query = WeiboPost.query
    
    if blogger_id:
        query = query.filter_by(blogger_id=blogger_id)
    if guess_date:
        query = query.filter_by(guess_date=guess_date)
    if guess_round:
        query = query.filter_by(guess_round=guess_round)
    if is_guess_related is not None:
        query = query.filter_by(is_guess_related=is_guess_related)
    if guess_prediction is not None and guess_prediction != '':
        print(f"[DEBUG] 应用筛选条件: guess_prediction={guess_prediction}", flush=True)
        query = query.filter(WeiboPost.guess_prediction == guess_prediction)
    
    # 分页
    pagination = query.order_by(WeiboPost.publish_time.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'data': [post.to_dict() for post in pagination.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    })


@weibo_bp.route('/<int:post_id>', methods=['GET'])
def get_weibo(post_id):
    """获取单个微博"""
    post = WeiboPost.query.get(post_id)

    if not post:
        return jsonify({
            'success': False,
            'message': '微博不存在'
        }), 404

    return jsonify({
        'success': True,
        'data': post.to_dict()
    })


@weibo_bp.route('/<int:post_id>', methods=['DELETE'])
def delete_weibo(post_id):
    """删除微博"""
    post = WeiboPost.query.get(post_id)

    if not post:
        return jsonify({
            'success': False,
            'message': '微博不存在'
        }), 404

    db.session.delete(post)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': '删除成功'
    })


@weibo_bp.route('/batch-delete', methods=['POST'])
def batch_delete_weibo():
    """批量删除微博"""
    data = request.get_json() or {}
    ids = data.get('ids', [])

    if not ids or not isinstance(ids, list):
        return jsonify({
            'success': False,
            'message': '请提供要删除的微博ID列表'
        }), 400

    if len(ids) == 0:
        return jsonify({
            'success': False,
            'message': '删除列表不能为空'
        }), 400

    deleted_count = 0
    failed_ids = []

    for post_id in ids:
        post = WeiboPost.query.get(post_id)
        if post:
            db.session.delete(post)
            deleted_count += 1
        else:
            failed_ids.append(post_id)

    db.session.commit()

    return jsonify({
        'success': True,
        'message': f'成功删除 {deleted_count} 条微博',
        'data': {
            'deleted_count': deleted_count,
            'failed_count': len(failed_ids),
            'failed_ids': failed_ids
        }
    })


@weibo_bp.route('/<int:post_id>/prediction', methods=['PUT'])
def update_prediction(post_id):
    """手动更新微博预测结果"""
    post = WeiboPost.query.get(post_id)

    if not post:
        return jsonify({
            'success': False,
            'message': '微博不存在'
        }), 404

    data = request.get_json()
    prediction = data.get('prediction')

    if prediction not in ['left', 'right', 'unknown']:
        return jsonify({
            'success': False,
            'message': '无效的预测结果，必须是 left、right 或 unknown'
        }), 400

    post.guess_prediction = prediction
    db.session.commit()

    return jsonify({
        'success': True,
        'message': '预测结果更新成功',
        'data': post.to_dict()
    })


@weibo_bp.route('/sync-all', methods=['POST'])
def sync_all_weibo():
    """手动触发同步，支持选择博主"""
    from app.services import WeiboSpiderService
    
    data = request.get_json() or {}
    blogger_id = data.get('blogger_id')  # 如果指定了博主ID，则只同步该博主
    
    spider_service = WeiboSpiderService()
    result = spider_service.spider_all_bloggers(spider_type='manual', blogger_id=blogger_id)
    
    if result['success']:
        return jsonify({
            'success': True,
            'message': f'同步完成，共爬取 {result["total_posts"]} 条微博',
            'data': {
                'total_posts': result['total_posts'],
                'bloggers_count': result['bloggers_count'],
                'errors': result.get('errors', [])
            }
        })
    else:
        return jsonify({
            'success': False,
            'message': result.get('error', '同步失败')
        }), 500


@weibo_bp.route('/spider-logs', methods=['GET'])
def get_spider_logs():
    """获取爬虫日志"""
    from app.models import SpiderLog
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    spider_type = request.args.get('type')  # auto/manual
    
    query = SpiderLog.query
    
    if spider_type:
        query = query.filter_by(spider_type=spider_type)
    
    pagination = query.order_by(SpiderLog.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'data': [log.to_dict() for log in pagination.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages
        }
    })


@weibo_bp.route('/sync-time-range', methods=['POST'])
def sync_by_time_range():
    """按时间段同步微博（异步版本）"""
    from app.services import WeiboSpiderService
    from app.services.task_manager import task_manager
    
    data = request.get_json() or {}
    blogger_id = data.get('blogger_id')  # 可选，指定博主ID
    date = data.get('date')  # 日期，格式：YYYY-MM-DD
    time_slot = data.get('time_slot')  # 时间段，格式：HH:MM-HH:MM
    async_mode = data.get('async', True)  # 默认异步模式
    
    if not date or not time_slot:
        return jsonify({
            'success': False,
            'message': '请提供日期和时间段'
        }), 400
    
    # 解析时间段
    try:
        start_time, end_time = time_slot.split('-')
        start_datetime = f"{date} {start_time}:00"
        
        # 处理24:00的情况（转换为23:59:59）
        if end_time == '24:00':
            end_datetime = f"{date} 23:59:59"
        else:
            end_datetime = f"{date} {end_time}:00"
    except Exception:
        return jsonify({
            'success': False,
            'message': '时间段格式错误，应为 HH:MM-HH:MM'
        }), 400
    
    # 异步模式：创建后台任务
    if async_mode:
        task_id = task_manager.create_task(
            task_type='sync_time_range',
            params={
                'blogger_id': blogger_id,
                'date': date,
                'time_slot': time_slot,
                'start_time': start_datetime,
                'end_time': end_datetime
            }
        )
        
        def run_sync_task():
            spider_service = WeiboSpiderService()
            return spider_service.spider_by_time_range(
                blogger_id=blogger_id,
                start_time=start_datetime,
                end_time=end_datetime,
                spider_type='manual'
            )
        
        task_manager.run_task_async(task_id, run_sync_task)
        
        return jsonify({
            'success': True,
            'message': '同步任务已创建',
            'data': {
                'task_id': task_id,
                'status': 'pending'
            }
        })
    
    # 同步模式（保持兼容）
    spider_service = WeiboSpiderService()
    result = spider_service.spider_by_time_range(
        blogger_id=blogger_id,
        start_time=start_datetime,
        end_time=end_datetime,
        spider_type='manual'
    )
    
    if result['success']:
        return jsonify({
            'success': True,
            'message': f'同步完成，共爬取 {result["total_posts"]} 条微博',
            'data': {
                'total_posts': result['total_posts'],
                'bloggers_count': result['bloggers_count'],
                'errors': result.get('errors', [])
            }
        })
    else:
        return jsonify({
            'success': False,
            'message': result.get('error', '同步失败')
        }), 500


@weibo_bp.route('/sync-task/<task_id>', methods=['GET'])
def get_sync_task_status(task_id):
    """获取同步任务状态"""
    from app.services.task_manager import task_manager
    
    task = task_manager.get_task(task_id)
    
    if not task:
        return jsonify({
            'success': False,
            'message': '任务不存在'
        }), 404
    
    return jsonify({
        'success': True,
        'data': {
            'task_id': task['id'],
            'status': task['status'],
            'progress': task['progress'],
            'result': task['result'],
            'error': task['error'],
            'created_at': task['created_at'].isoformat() if task['created_at'] else None,
            'completed_at': task['completed_at'].isoformat() if task['completed_at'] else None
        }
    })
