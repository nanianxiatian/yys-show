from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .blogger import Blogger
from .weibo_post import WeiboPost
from .official_result import OfficialResult
from .blogger_stats import BloggerStats
from .system_config import SystemConfig
from .spider_log import SpiderLog

__all__ = [
    'db',
    'Blogger',
    'WeiboPost', 
    'OfficialResult',
    'BloggerStats',
    'SystemConfig',
    'SpiderLog'
]
