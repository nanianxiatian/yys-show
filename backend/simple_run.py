#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_cors import CORS
from app.config import config_map
from app.models import db
from app.routes import register_blueprints

def create_simple_app(config_name='default'):
    app = Flask(__name__)
    config_class = config_map.get(config_name, config_map['default'])
    app.config.from_object(config_class)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)
    register_blueprints(app)
    return app

app = create_simple_app('development')

if __name__ == '__main__':
    print("=" * 50)
    print("后端服务启动中...")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
