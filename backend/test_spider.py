from spider import WeiboCrawler
from app import create_app
from app.models import SystemConfig

# 创建应用上下文
app = create_app()
with app.app_context():
    # 获取Cookie
    cookie = SystemConfig.get_value('weibo_cookie', '')
    print(f"Cookie长度: {len(cookie)}")
    print(f"Cookie前100字符: {cookie[:100]}...")

    # 创建爬虫实例
    crawler = WeiboCrawler(cookie=cookie)

    # 测试搜索用户
    nickname = "春秋霸主徐清林"
    print(f"\n开始搜索用户: {nickname}")

    user_info = crawler.get_user_info(nickname)
    if user_info:
        print(f"找到用户: {user_info}")
    else:
        print("未找到用户")

    # 测试Cookie是否有效
    print(f"\n测试Cookie有效性...")
    is_valid = crawler.check_cookie_valid()
    print(f"Cookie有效: {is_valid}")
