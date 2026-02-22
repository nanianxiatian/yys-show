from . import db
from datetime import datetime


class Blogger(db.Model):
    """博主模型"""
    __tablename__ = 'bloggers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.String(100), nullable=False, unique=True, comment='博主昵称')
    weibo_uid = db.Column(db.String(50), comment='微博用户ID')
    profile_url = db.Column(db.String(500), comment='主页链接')
    avatar_url = db.Column(db.String(500), comment='头像URL')
    description = db.Column(db.Text, comment='博主描述')
    is_active = db.Column(db.Boolean, default=True, comment='是否启用')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关联关系
    weibo_posts = db.relationship('WeiboPost', backref='blogger', lazy=True, cascade='all, delete-orphan')
    stats = db.relationship('BloggerStats', backref='blogger', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'nickname': self.nickname,
            'weibo_uid': self.weibo_uid,
            'profile_url': self.profile_url,
            'avatar_url': self.avatar_url,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Blogger {self.nickname}>'
