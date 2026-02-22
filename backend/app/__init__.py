from flask import Flask
from flask_cors import CORS
from app.config import config_map
from app.models import db
from app.routes import register_blueprints
from app.services import SchedulerService


def create_app(config_name='default'):
    """
    创建Flask应用
    
    Args:
        config_name: 配置名称(development/production/default)
        
    Returns:
        Flask: Flask应用实例
    """
    app = Flask(__name__)
    
    # 加载配置
    config_class = config_map.get(config_name, config_map['default'])
    app.config.from_object(config_class)
    
    # 启用CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # 初始化数据库
    db.init_app(app)
    
    # 注册蓝图
    register_blueprints(app)
    
    # 启动定时任务调度器
    scheduler = SchedulerService()
    scheduler.start()
    
    # 注册关闭钩子 - 只在应用关闭时执行
    import atexit
    def shutdown_scheduler():
        scheduler.shutdown()
    atexit.register(shutdown_scheduler)
    
    return app
