"""
预约模型
"""
from datetime import datetime
from app import db
from app.models.mixins import ToDictMixin


class Reservation(db.Model, ToDictMixin):
    """预约表"""
    __tablename__ = 'reservation'
    
    id = db.Column(db.BigInteger, primary_key=True, comment='预约ID')
    student_id = db.Column(db.String(10), db.ForeignKey('student.id'), nullable=True, comment='学生ID')
    teacher_id = db.Column(db.String(10), db.ForeignKey('teacher.id'), nullable=True, comment='导师ID')
    equip_id = db.Column(db.BigInteger, db.ForeignKey('equipment.id'), nullable=False, comment='设备ID')
    status = db.Column(db.Integer, nullable=False, default=0, comment='预约状态 (0:待审, 1:通过...)')
    apply_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, comment='申请时间')
    approver_id = db.Column(db.String(10), nullable=True, comment='审批人ID')
    approve_time = db.Column(db.DateTime, nullable=True, comment='审批时间')
    
    # 冗余字段
    user_name = db.Column(db.String(50), nullable=True, comment='用户名（冗余字段）')
    equip_name = db.Column(db.String(100), nullable=True, comment='设备名称（冗余字段）')
    price = db.Column(db.Numeric(10, 2), nullable=True, comment='价格（冗余字段）')
    start_time = db.Column(db.DateTime, nullable=True, comment='开始时间（冗余字段）')
    end_time = db.Column(db.DateTime, nullable=True, comment='结束时间（冗余字段）')
    
    # 添加约束：student_id 和 teacher_id 必须有一个不为空，但不能同时为空
    # 添加索引：优化查询性能
    __table_args__ = (
        db.CheckConstraint(
            '(student_id IS NOT NULL AND teacher_id IS NULL) OR (student_id IS NULL AND teacher_id IS NOT NULL)',
            name='check_reservation_user'
        ),
        # 单列索引
        db.Index('idx_reservation_equip_id', 'equip_id'),
        db.Index('idx_reservation_student_id', 'student_id'),
        db.Index('idx_reservation_teacher_id', 'teacher_id'),
        db.Index('idx_reservation_status', 'status'),
        db.Index('idx_reservation_apply_time', 'apply_time'),
        # 组合索引：优化常见查询场景
        db.Index('idx_reservation_equip_status', 'equip_id', 'status'),
        db.Index('idx_reservation_student_status', 'student_id', 'status'),
        db.Index('idx_reservation_teacher_status', 'teacher_id', 'status'),
    )
    
    def __repr__(self):
        return f'<Reservation {self.id}: {self.equip_id}>'

