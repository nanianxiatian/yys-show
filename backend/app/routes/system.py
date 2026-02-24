from flask import request, jsonify
from app.models import db, SystemConfig
from app.services import SchedulerService
from . import system_bp


@system_bp.route('/config', methods=['GET'])
def get_configs():
    """获取系统配置列表"""
    configs = SystemConfig.query.all()
    
    return jsonify({
        'success': True,
        'data': [c.to_dict() for c in configs]
    })


@system_bp.route('/config/<key>', methods=['GET'])
def get_config(key):
    """获取单个配置"""
    value = SystemConfig.get_value(key)
    
    return jsonify({
        'success': True,
        'data': {
            'key': key,
            'value': value
        }
    })


@system_bp.route('/config/<key>', methods=['PUT'])
def update_config(key):
    """更新配置"""
    data = request.get_json()
    
    if not data or 'value' not in data:
        return jsonify({
            'success': False,
            'message': '缺少value字段'
        }), 400
    
    config = SystemConfig.set_value(key, data['value'])
    
    return jsonify({
        'success': True,
        'message': '配置已更新',
        'data': config.to_dict()
    })


@system_bp.route('/cookie', methods=['POST'])
def update_cookie():
    """更新微博Cookie"""
    data = request.get_json()
    
    if not data or not data.get('cookie'):
        return jsonify({
            'success': False,
            'message': 'Cookie不能为空'
        }), 400
    
    from app.services import WeiboSpiderService
    
    spider_service = WeiboSpiderService()
    success = spider_service.update_cookie(data['cookie'])
    
    if success:
        return jsonify({
            'success': True,
            'message': 'Cookie更新成功'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Cookie无效或已过期'
        }), 400


@system_bp.route('/cookie/check', methods=['GET'])
def check_cookie():
    """检查Cookie状态"""
    from app.services import WeiboSpiderService
    from datetime import datetime
    
    spider_service = WeiboSpiderService()
    is_valid = spider_service.check_cookie()
    
    # 获取更新时间
    update_time = SystemConfig.get_value('cookie_expire_time')
    
    # 解析Cookie中的ALF字段获取真实过期时间
    cookie_expire_date = None
    days_left = None
    try:
        cookie = SystemConfig.get_value('weibo_cookie', '')
        if cookie:
            for part in cookie.split('; '):
                if part.startswith('ALF='):
                    alf_value = part.split('=', 1)[1]
                    # 处理格式如 "02_1774342769"
                    if '_' in alf_value:
                        _, timestamp_str = alf_value.split('_')
                        timestamp = int(timestamp_str)
                    else:
                        timestamp = int(alf_value)
                    
                    expire_dt = datetime.fromtimestamp(timestamp)
                    cookie_expire_date = expire_dt.strftime('%Y-%m-%d %H:%M:%S')
                    
                    now = datetime.now()
                    if expire_dt > now:
                        days_left = (expire_dt - now).days
                    break
    except Exception as e:
        print(f"解析Cookie过期时间失败: {e}")
    
    return jsonify({
        'success': True,
        'data': {
            'is_valid': is_valid,
            'expire_time': update_time,
            'cookie_expire_date': cookie_expire_date,
            'days_left': days_left
        }
    })


@system_bp.route('/jobs', methods=['GET'])
def get_scheduler_jobs():
    """获取定时任务列表"""
    scheduler = SchedulerService()
    jobs = scheduler.get_jobs()
    
    return jsonify({
        'success': True,
        'data': jobs
    })


@system_bp.route('/jobs/<job_id>/pause', methods=['POST'])
def pause_job(job_id):
    """暂停定时任务"""
    scheduler = SchedulerService()
    scheduler.pause_job(job_id)
    
    return jsonify({
        'success': True,
        'message': f'任务 {job_id} 已暂停'
    })


@system_bp.route('/jobs/<job_id>/resume', methods=['POST'])
def resume_job(job_id):
    """恢复定时任务"""
    scheduler = SchedulerService()
    scheduler.resume_job(job_id)
    
    return jsonify({
        'success': True,
        'message': f'任务 {job_id} 已恢复'
    })


@system_bp.route('/jobs/run-now', methods=['POST'])
def run_spider_now():
    """立即执行爬虫"""
    scheduler = SchedulerService()
    scheduler.run_spider_now()
    
    return jsonify({
        'success': True,
        'message': '爬虫任务已触发'
    })


@system_bp.route('/stats', methods=['GET'])
def get_system_stats():
    """获取系统统计信息"""
    from app.models import Blogger, WeiboPost, OfficialResult, SpiderLog
    from sqlalchemy import func
    
    # 统计数据
    blogger_count = Blogger.query.filter_by(is_active=True).count()
    weibo_count = WeiboPost.query.filter_by(is_guess_related=True).count()
    official_count = OfficialResult.query.count()
    
    # 最近爬虫记录
    latest_logs = SpiderLog.query.order_by(SpiderLog.created_at.desc()).limit(5).all()
    
    return jsonify({
        'success': True,
        'data': {
            'stats': {
                'blogger_count': blogger_count,
                'weibo_count': weibo_count,
                'official_count': official_count
            },
            'latest_logs': [log.to_dict() for log in latest_logs]
        }
    })
