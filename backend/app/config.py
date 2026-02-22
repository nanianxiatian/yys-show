import os
from datetime import timedelta
from dotenv import load_dotenv

# 加载.env文件
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '..', '.env'))


class Config:
    """应用配置类"""
    
    # 数据库配置（请在本地的.env文件中配置真实值）
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'your_password_here')
    MYSQL_DB = os.getenv('MYSQL_DB', 'yys_guess')
    
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
        f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask配置（请在本地的.env文件中配置真实值）
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    
    # 爬虫配置
    SPIDER_KEYWORDS = ['对弈竞猜']
    SPIDER_AUTO_ENABLED = True
    # 每天11:30, 13:30, 15:30, 17:30, 19:30, 21:30, 23:30 执行
    SPIDER_CRON_HOURS = '11,13,15,17,19,21,23'
    SPIDER_CRON_MINUTE = 30
    
    # 微博Cookie（请在本地的.env文件中配置真实值，也可在系统设置中配置）
    WEIBO_COOKIE = os.getenv('WEIBO_COOKIE', 'your_weibo_cookie_here')
    
    # API配置
    JSON_AS_ASCII = False
    
    # 竞猜配置
    GUESS_ROUNDS_PER_DAY = 7  # 每天7轮竞猜
    GUESS_START_HOUR = 10     # 竞猜开始时间
    GUESS_INTERVAL_HOURS = 2  # 每2小时一轮


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False


# 配置映射
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
