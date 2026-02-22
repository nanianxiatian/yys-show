import os
from datetime import timedelta


class Config:
    """应用配置类"""
    
    # 数据库配置
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'yys20260217')
    MYSQL_DB = os.getenv('MYSQL_DB', 'yys_guess')
    
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
        f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'yys-guess-secret-key-2024')
    
    # 爬虫配置
    SPIDER_KEYWORDS = ['对弈竞猜']
    SPIDER_AUTO_ENABLED = True
    # 每天11:30, 13:30, 15:30, 17:30, 19:30, 21:30, 23:30 执行
    SPIDER_CRON_HOURS = '11,13,15,17,19,21,23'
    SPIDER_CRON_MINUTE = 30
    
    # 微博Cookie(从数据库读取，这里仅作默认值)
    WEIBO_COOKIE = 'XSRF-TOKEN=LcqynfhAKEtFPjA08Eu7Y117; SCF=AqjLV3yZGS1rCbjCcJK81FWviTM2cZVNdfiUlqZxfPSxtPGAOaV_4Vo_AsTiVt11z1FdBCERl3Tl4Mc0_tTbpt0.; SUB=_2A25EnrUhDeRhGeRH7lEU-S7JyDmIHXVn0kjprDV8PUNbmtANLWTlkW9NTbK8KEIZwlRZSsNLwS5ajEwjjylbzs9s; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW736dHaUwl9.7aeJTmoAIk5JpX5KzhUgL.Foz4SKef1K5fe0-2dJLoIE._i--4iKnEi-20i--fi-z4i-zXi--fi-2XiKysi--fi-2Xi-24KN9lTBtt; ALF=02_1774342769; _s_tentry=passport.weibo.com; Apache=9942779390541.094.1771750769386; SINAGLOBAL=9942779390541.094.1771750769386; ULV=1771750769391:1:1:1:9942779390541.094.1771750769386:; WBPSESS=jL8_-Pbne-c53OiMZ6t-8voMCp0BT3vcHuXJ0s7i7kfU65kfiTgIYeI9i0qZyrtVzfm94fvn95YUZweAQMwAeN91OPpJHoM0tkzaE_6CWAdtikIdCXI4XnyIYUEZxMR7d0yoCla8weUGjCG2nRXJWg=='
    
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
