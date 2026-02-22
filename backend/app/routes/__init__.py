from flask import Blueprint

# 创建蓝图
blogger_bp = Blueprint('blogger', __name__, url_prefix='/api/bloggers')
weibo_bp = Blueprint('weibo', __name__, url_prefix='/api/weibo')
guess_bp = Blueprint('guess', __name__, url_prefix='/api/guess')
official_bp = Blueprint('official', __name__, url_prefix='/api/official')
system_bp = Blueprint('system', __name__, url_prefix='/api/system')

# 导入路由
from . import blogger
from . import weibo
from . import guess
from . import official
from . import system


def register_blueprints(app):
    """注册所有蓝图"""
    app.register_blueprint(blogger_bp)
    app.register_blueprint(weibo_bp)
    app.register_blueprint(guess_bp)
    app.register_blueprint(official_bp)
    app.register_blueprint(system_bp)
