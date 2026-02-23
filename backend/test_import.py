"""
测试导入
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.routes import shikigami_manager_bp

print('Blueprint imported:', shikigami_manager_bp)
print('URL prefix:', shikigami_manager_bp.url_prefix)
print('Routes:')
for rule in shikigami_manager_bp.url_map:
    print(' ', rule)
