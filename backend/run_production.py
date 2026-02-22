#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
生产环境启动脚本（无调试模式，无自动重载）
"""
import sys
sys.path.insert(0, r'f:\trace\work-space\yys-show\backend')

from app import create_app

app = create_app()

if __name__ == '__main__':
    print("=" * 50)
    print("阴阳师对弈竞猜系统 - 后端服务")
    print("=" * 50)
    print("API地址: http://127.0.0.1:5000")
    print("=" * 50)
    
    # 禁用调试模式，避免缓存问题
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
