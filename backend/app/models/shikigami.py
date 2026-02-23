"""
式神模型
"""
from . import db
from datetime import datetime


class Shikigami(db.Model):
    """式神模型"""
    __tablename__ = 'shikigamis'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True, comment='式神名称')
    english_name = db.Column(db.String(100), comment='式神英文简称')
    rarity = db.Column(db.Enum('N', 'R', 'SR', 'SSR', 'SP', 'UR', name='rarity_enum'), default='SR', comment='稀有度')
    skill_1 = db.Column(db.String(200), comment='一技能')
    skill_2 = db.Column(db.String(200), comment='二技能')
    skill_3 = db.Column(db.String(200), comment='三技能')
    description = db.Column(db.Text, comment='备注')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'english_name': self.english_name,
            'rarity': self.rarity,
            'skill_1': self.skill_1,
            'skill_2': self.skill_2,
            'skill_3': self.skill_3,
            'description': self.description,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Shikigami {self.name}>'
