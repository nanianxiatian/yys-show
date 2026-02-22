#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
阴阳师对弈竞猜系统 - 后端启动入口
"""
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

# 创建应用实例
app = create_app('development')


@app.route('/')
def index():
    """首页"""
    return {
        'name': '阴阳师对弈竞猜系统 API',
        'version': '1.0.0',
        'status': 'running',
        'docs': '/api/docs'
    }


@app.route('/api/docs')
def api_docs():
    """API文档"""
    return {
        'name': '阴阳师对弈竞猜系统 API',
        'version': '1.0.0',
        'endpoints': {
            '博主管理': {
                'GET /api/bloggers': '获取博主列表',
                'POST /api/bloggers': '创建博主',
                'GET /api/bloggers/<id>': '获取博主详情',
                'PUT /api/bloggers/<id>': '更新博主',
                'DELETE /api/bloggers/<id>': '删除博主',
                'POST /api/bloggers/<id>/sync': '手动同步博主微博'
            },
            '微博数据': {
                'GET /api/weibo': '获取微博列表',
                'POST /api/weibo/sync-all': '手动触发全量同步',
                'GET /api/weibo/spider-logs': '获取爬虫日志'
            },
            '竞猜分析': {
                'GET /api/guess/analysis': '获取竞猜分析',
                'GET /api/guess/leaderboard': '获取排行榜',
                'GET /api/guess/blogger/<id>/stats': '获取博主统计',
                'POST /api/guess/stats/update': '更新统计数据',
                'GET /api/guess/history': '获取历史记录'
            },
            '官方结果': {
                'GET /api/official': '获取官方结果列表',
                'POST /api/official': '创建官方结果',
                'POST /api/official/batch': '批量创建官方结果',
                'PUT /api/official/<id>': '更新官方结果',
                'DELETE /api/official/<id>': '删除官方结果',
                'GET /api/official/dates': '获取有结果的日期列表'
            },
            '系统管理': {
                'GET /api/system/config': '获取系统配置',
                'PUT /api/system/config/<key>': '更新配置',
                'POST /api/system/cookie': '更新Cookie',
                'GET /api/system/cookie/check': '检查Cookie',
                'GET /api/system/jobs': '获取定时任务',
                'POST /api/system/jobs/run-now': '立即执行爬虫',
                'GET /api/system/stats': '获取系统统计'
            }
        }
    }


if __name__ == '__main__':
    # 启动开发服务器
    print("=" * 50)
    print("阴阳师对弈竞猜系统 - 后端服务")
    print("=" * 50)
    print(f"API地址: http://127.0.0.1:5000")
    print(f"API文档: http://127.0.0.1:5000/api/docs")
    print("=" * 50)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False  # 禁用重载器以避免定时任务重复启动
    )
