"""
导师模型
"""
from app import db
from app.models.mixins import ToDictMixin


class Teacher(db.Model, ToDictMixin):
    """导师表"""
    __tablename__ = 'teacher'
    
    id = db.Column(db.String(10), primary_key=True, comment='导师ID')
    name = db.Column(db.String(50), nullable=False, comment='导师姓名')
    password_hash = db.Column(db.String(255), nullable=True, comment='密码Hash值')
    dept = db.Column(db.String(50), nullable=True, comment='所属部门')
    lab_id = db.Column(db.Integer, db.ForeignKey('laboratory.id'), nullable=False, comment='所属实验室ID')
    
    # 关系定义
    students = db.relationship('Student', backref='teacher', lazy='dynamic', foreign_keys='Student.t_id')
    reservations = db.relationship('Reservation', backref='teacher', lazy='dynamic', foreign_keys='Reservation.teacher_id')
    
    # 添加索引：优化查询性能
    __table_args__ = (
        db.Index('idx_teacher_lab_id', 'lab_id'),
    )
    
    def __repr__(self):
        return f'<Teacher {self.id}: {self.name}>'

