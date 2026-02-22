#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

app = create_app('development')

@app.route('/')
def index():
    return {'status': 'running'}

if __name__ == '__main__':
    print("启动服务...")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
