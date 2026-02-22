import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app
from app.models import SystemConfig

app = create_app()
with app.app_context():
    cookie = SystemConfig.get_value('weibo_cookie', '')
    print(f"Cookie长度: {len(cookie)}")
