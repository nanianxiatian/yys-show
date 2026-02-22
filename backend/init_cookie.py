from app import create_app
from app.models import SystemConfig
from app.config import Config

app = create_app()
with app.app_context():
    # 从配置文件读取Cookie
    cookie = Config.WEIBO_COOKIE

    if cookie:
        # 保存到数据库
        SystemConfig.set_value('weibo_cookie', cookie)
        print(f"Cookie已初始化到数据库，长度: {len(cookie)}")

        # 设置其他默认配置
        SystemConfig.set_value('spider_cron_hours', '11,13,15,17,19,21,23')
        SystemConfig.set_value('spider_cron_minute', '30')
        SystemConfig.set_value('spider_auto_enabled', 'true')
        print("系统配置已初始化")
    else:
        print("配置文件中没有Cookie")
