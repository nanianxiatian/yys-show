from . import db
from datetime import datetime


class WeiboPost(db.Model):
    """微博帖子模型"""
    __tablename__ = 'weibo_posts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    blogger_id = db.Column(db.Integer, db.ForeignKey('bloggers.id'), nullable=False, comment='博主ID')
    weibo_id = db.Column(db.String(50), nullable=False, unique=True, comment='微博ID')
    content = db.Column(db.Text, nullable=False, comment='微博内容')
    guess_prediction = db.Column(
        db.Enum('left', 'right', 'unknown', name='prediction_enum'),
        default='unknown',
        comment='预测结果:左/右/未知'
    )
    guess_round = db.Column(db.Integer, comment='竞猜轮次(1-7)')
    guess_date = db.Column(db.Date, comment='竞猜日期')
    publish_time = db.Column(db.DateTime, comment='发布时间')
    reposts_count = db.Column(db.Integer, default=0, comment='转发数')
    comments_count = db.Column(db.Integer, default=0, comment='评论数')
    attitudes_count = db.Column(db.Integer, default=0, comment='点赞数')
    is_guess_related = db.Column(db.Boolean, default=False, comment='是否包含对弈竞猜')
    pic_urls = db.Column(db.Text, comment='微博图片URL列表(JSON数组)')
    weibo_url = db.Column(db.String(500), comment='微博原链接')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'blogger_id': self.blogger_id,
            'blogger_nickname': self.blogger.nickname if self.blogger else None,
            'weibo_id': self.weibo_id,
            'content': self.content,
            'guess_prediction': self.guess_prediction,
            'guess_prediction_text': self.get_prediction_text(),
            'guess_round': self.guess_round,
            'guess_date': self.guess_date.strftime('%Y-%m-%d') if self.guess_date else None,
            'publish_time': self.publish_time.strftime('%Y-%m-%d %H:%M:%S') if self.publish_time else None,
            'reposts_count': self.reposts_count,
            'comments_count': self.comments_count,
            'attitudes_count': self.attitudes_count,
            'is_guess_related': self.is_guess_related,
            'pic_urls': self.get_pic_urls_list(),
            'weibo_url': self.weibo_url,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }

    def get_pic_urls_list(self):
        """获取图片URL列表"""
        import json
        if not self.pic_urls:
            return []
        try:
            return json.loads(self.pic_urls)
        except:
            return []
    
    def get_prediction_text(self):
        """获取预测结果文本"""
        mapping = {
            'left': '左',
            'right': '右',
            'unknown': '未知'
        }
        return mapping.get(self.guess_prediction, '未知')
    
    def __repr__(self):
        return f'<WeiboPost {self.weibo_id}>'
