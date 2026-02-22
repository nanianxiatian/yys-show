from . import db
from datetime import datetime


class OfficialResult(db.Model):
    """官方竞猜结果模型"""
    __tablename__ = 'official_results'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    guess_date = db.Column(db.Date, nullable=False, comment='竞猜日期')
    guess_round = db.Column(db.Integer, nullable=False, comment='竞猜轮次(1-7)')
    result = db.Column(
        db.Enum('left', 'right', name='result_enum'),
        nullable=False,
        comment='官方结果:左/右'
    )
    left_team = db.Column(db.String(200), comment='左侧阵营描述')
    right_team = db.Column(db.String(200), comment='右侧阵营描述')
    description = db.Column(db.Text, comment='备注')
    created_by = db.Column(db.String(100), comment='录入人')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'guess_date': self.guess_date.strftime('%Y-%m-%d') if self.guess_date else None,
            'guess_round': self.guess_round,
            'result': self.result,
            'result_text': self.get_result_text(),
            'left_team': self.left_team,
            'right_team': self.right_team,
            'description': self.description,
            'created_by': self.created_by,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
    
    def get_result_text(self):
        """获取结果文本"""
        mapping = {
            'left': '左',
            'right': '右'
        }
        return mapping.get(self.result, '未知')
    
    def __repr__(self):
        return f'<OfficialResult {self.guess_date} Round{self.guess_round}>'
