from . import db
from datetime import datetime


class BloggerStats(db.Model):
    """博主竞猜统计模型"""
    __tablename__ = 'blogger_stats'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    blogger_id = db.Column(db.Integer, db.ForeignKey('bloggers.id'), nullable=False, comment='博主ID')
    stat_date = db.Column(db.Date, nullable=False, comment='统计日期')
    total_guesses = db.Column(db.Integer, default=0, comment='总预测次数')
    correct_guesses = db.Column(db.Integer, default=0, comment='正确次数')
    wrong_guesses = db.Column(db.Integer, default=0, comment='错误次数')
    unknown_guesses = db.Column(db.Integer, default=0, comment='未知/未预测次数')
    accuracy_rate = db.Column(db.Numeric(5, 2), default=0.00, comment='准确率(%)')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'blogger_id': self.blogger_id,
            'blogger_nickname': self.blogger.nickname if self.blogger else None,
            'stat_date': self.stat_date.strftime('%Y-%m-%d') if self.stat_date else None,
            'total_guesses': self.total_guesses,
            'correct_guesses': self.correct_guesses,
            'wrong_guesses': self.wrong_guesses,
            'unknown_guesses': self.unknown_guesses,
            'accuracy_rate': float(self.accuracy_rate) if self.accuracy_rate else 0.00,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
    
    def calculate_accuracy(self):
        """计算准确率"""
        valid_guesses = self.correct_guesses + self.wrong_guesses
        if valid_guesses > 0:
            self.accuracy_rate = round((self.correct_guesses / valid_guesses) * 100, 2)
        else:
            self.accuracy_rate = 0.00
        return self.accuracy_rate
    
    def __repr__(self):
        return f'<BloggerStats {self.blogger_id} {self.stat_date}>'
