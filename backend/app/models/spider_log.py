from . import db
from datetime import datetime


class SpiderLog(db.Model):
    """爬虫日志模型"""
    __tablename__ = 'spider_logs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    spider_type = db.Column(db.String(50), nullable=False, comment='爬虫类型:auto/manual')
    blogger_id = db.Column(db.Integer, db.ForeignKey('bloggers.id'), comment='博主ID(手动同步时有)')
    status = db.Column(
        db.Enum('running', 'success', 'failed', name='spider_status_enum'),
        nullable=False,
        comment='状态'
    )
    start_time = db.Column(db.DateTime, comment='开始时间')
    end_time = db.Column(db.DateTime, comment='结束时间')
    posts_count = db.Column(db.Integer, default=0, comment='抓取帖子数')
    error_message = db.Column(db.Text, comment='错误信息')
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # 关联关系
    blogger = db.relationship('Blogger', backref='spider_logs', lazy=True)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'spider_type': self.spider_type,
            'blogger_id': self.blogger_id,
            'blogger_nickname': self.blogger.nickname if self.blogger else None,
            'status': self.status,
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S') if self.start_time else None,
            'end_time': self.end_time.strftime('%Y-%m-%d %H:%M:%S') if self.end_time else None,
            'duration': self.get_duration(),
            'posts_count': self.posts_count,
            'error_message': self.error_message,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
    
    def get_duration(self):
        """获取执行时长(秒)"""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None
    
    def __repr__(self):
        return f'<SpiderLog {self.spider_type} {self.status}>'
