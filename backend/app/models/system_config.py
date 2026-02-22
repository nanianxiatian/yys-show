from . import db
from datetime import datetime


class SystemConfig(db.Model):
    """系统配置模型"""
    __tablename__ = 'system_config'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    config_key = db.Column(db.String(100), nullable=False, unique=True, comment='配置键')
    config_value = db.Column(db.Text, comment='配置值')
    description = db.Column(db.String(500), comment='配置说明')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    @classmethod
    def get_value(cls, key, default=None):
        """获取配置值"""
        config = cls.query.filter_by(config_key=key).first()
        return config.config_value if config else default
    
    @classmethod
    def set_value(cls, key, value):
        """设置配置值"""
        config = cls.query.filter_by(config_key=key).first()
        if config:
            config.config_value = value
        else:
            config = cls(config_key=key, config_value=value)
            db.session.add(config)
        db.session.commit()
        return config
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'config_key': self.config_key,
            'config_value': self.config_value,
            'description': self.description,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<SystemConfig {self.config_key}>'
