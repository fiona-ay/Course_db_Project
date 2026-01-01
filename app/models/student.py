"""
学生模型
"""
from app import db
from app.models.mixins import ToDictMixin


class Student(db.Model, ToDictMixin):
    """学生表"""
    __tablename__ = 'student'
    
    id = db.Column(db.String(10), primary_key=True, comment='学生ID')
    name = db.Column(db.String(50), nullable=False, comment='学生姓名')
    password_hash = db.Column(db.String(255), nullable=True, comment='密码Hash值')
    dept = db.Column(db.String(50), nullable=False, default='本院', comment='所属部门')
    lab_id = db.Column(db.Integer, db.ForeignKey('laboratory.id'), nullable=True, comment='所属实验室ID')
    t_id = db.Column(db.String(10), db.ForeignKey('teacher.id'), nullable=True, comment='导师ID')
    
    # 冗余字段
    lab_name = db.Column(db.String(50), nullable=True, comment='实验室名称（冗余字段）')
    
    # 关系定义
    reservations = db.relationship('Reservation', backref='student', lazy='dynamic', foreign_keys='Reservation.student_id')
    
    # 添加索引：优化查询性能
    __table_args__ = (
        db.Index('idx_student_lab_id', 'lab_id'),
        db.Index('idx_student_t_id', 't_id'),
        db.Index('idx_student_lab_t', 'lab_id', 't_id'),
    )
    
    def __repr__(self):
        return f'<Student {self.id}: {self.name}>'

