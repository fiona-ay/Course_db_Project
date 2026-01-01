"""
时间段模型
"""
from app import db
from app.models.mixins import ToDictMixin


class TimeSlot(db.Model, ToDictMixin):
    """时间段表"""
    __tablename__ = 'timeslot'
    
    slot_id = db.Column(db.BigInteger, primary_key=True, comment='时间段ID')
    equip_id = db.Column(db.BigInteger, db.ForeignKey('equipment.id'), nullable=False, comment='设备ID')
    start_time = db.Column(db.Time, nullable=False, comment='开始时间')
    end_time = db.Column(db.Time, nullable=False, comment='结束时间')
    is_active = db.Column(db.Integer, nullable=False, default=1, comment='是否激活 (1:激活, 0:禁用)')
    
    # 添加索引：优化查询性能
    __table_args__ = (
        db.Index('idx_timeslot_equip_id', 'equip_id'),
        db.Index('idx_timeslot_is_active', 'is_active'),
        db.Index('idx_timeslot_equip_active', 'equip_id', 'is_active'),
    )
    
    def __repr__(self):
        return f'<TimeSlot {self.slot_id}: {self.start_time}-{self.end_time}>'

