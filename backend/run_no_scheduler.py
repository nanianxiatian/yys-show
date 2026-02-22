#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
阴阳师对弈竞猜系统 - 后端启动入口（无定时任务版）
"""
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_cors import CORS
from app.config import config_map
from app.models import db
from app.routes import register_blueprints


def create_app(config_name='default'):
    """创建Flask应用"""
    app = Flask(__name__)

    # 加载配置
    config_class = config_map.get(config_name, config_map['default'])
    app.config.from_object(config_class)

    # 启用CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # 初始化数据库
    db.init_app(app)

    # 注册蓝图
    register_blueprints(app)

    return app


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
                'GET /api/guess/bloggers': '获取博主竞猜统计',
                'GET /api/guess/rounds': '获取轮次列表'
            },
            '官方结果': {
                'GET /api/official/results': '获取官方结果列表',
                'POST /api/official/results': '创建官方结果',
                'PUT /api/official/results/<id>': '更新官方结果',
                'DELETE /api/official/results/<id>': '删除官方结果'
            },
            '系统配置': {
                'GET /api/system/config': '获取系统配置',
                'PUT /api/system/config': '更新系统配置',
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
        use_reloader=False
    )
