"""
管理员模型
"""
from app import db
from app.models.mixins import ToDictMixin


class Admin(db.Model, ToDictMixin):
    """管理员表"""
    __tablename__ = 'admin'
    
    id = db.Column(db.String(10), primary_key=True, comment='管理员ID')
    name = db.Column(db.String(20), nullable=False, comment='管理员姓名')
    password_hash = db.Column(db.String(255), nullable=True, comment='密码Hash值')
    manage_scope = db.Column(db.Integer, db.ForeignKey('laboratory.id'), nullable=True, comment='管理范围（实验室ID）')
    
    def __repr__(self):
        return f'<Admin {self.id}: {self.name}>'

