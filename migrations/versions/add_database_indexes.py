"""Add database indexes - 添加数据库索引

Revision ID: add_indexes_001
Revises: cac671f41ffb
Create Date: 2025-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_indexes_001'
down_revision = 'cac671f41ffb'
branch_labels = None
depends_on = None


def upgrade():
    # ### 为 reservation 表添加索引 ###
    # 单列索引
    op.create_index('idx_reservation_equip_id', 'reservation', ['equip_id'], 
                     unique=False)
    op.create_index('idx_reservation_student_id', 'reservation', ['student_id'], 
                     unique=False)
    op.create_index('idx_reservation_teacher_id', 'reservation', ['teacher_id'], 
                     unique=False)
    op.create_index('idx_reservation_status', 'reservation', ['status'], 
                     unique=False)
    op.create_index('idx_reservation_apply_time', 'reservation', ['apply_time'], 
                     unique=False)
    
    # 组合索引
    op.create_index('idx_reservation_equip_status', 'reservation', ['equip_id', 'status'], 
                     unique=False)
    op.create_index('idx_reservation_student_status', 'reservation', ['student_id', 'status'], 
                     unique=False)
    op.create_index('idx_reservation_teacher_status', 'reservation', ['teacher_id', 'status'], 
                     unique=False)
    
    # ### 为 equipment 表添加索引 ###
    op.create_index('idx_equipment_lab_id', 'equipment', ['lab_id'], 
                     unique=False)
    op.create_index('idx_equipment_status', 'equipment', ['status'], 
                     unique=False)
    op.create_index('idx_equipment_category', 'equipment', ['category'], 
                     unique=False)
    op.create_index('idx_equipment_lab_status', 'equipment', ['lab_id', 'status'], 
                     unique=False)
    
    # ### 为 student 表添加索引 ###
    op.create_index('idx_student_lab_id', 'student', ['lab_id'], 
                     unique=False)
    op.create_index('idx_student_t_id', 'student', ['t_id'], 
                     unique=False)
    op.create_index('idx_student_lab_t', 'student', ['lab_id', 't_id'], 
                     unique=False)
    
    # ### 为 teacher 表添加索引 ###
    op.create_index('idx_teacher_lab_id', 'teacher', ['lab_id'], 
                     unique=False)
    
    # ### 为 timeslot 表添加索引 ###
    op.create_index('idx_timeslot_equip_id', 'timeslot', ['equip_id'], 
                     unique=False)
    op.create_index('idx_timeslot_is_active', 'timeslot', ['is_active'], 
                     unique=False)
    op.create_index('idx_timeslot_equip_active', 'timeslot', ['equip_id', 'is_active'], 
                     unique=False)
    
    # ### 为 auditlog 表添加索引 ###
    op.create_index('idx_auditlog_operator_id', 'auditlog', ['operator_id'], 
                     unique=False)
    op.create_index('idx_auditlog_action_time', 'auditlog', ['action_time'], 
                     unique=False)
    op.create_index('idx_auditlog_action_type', 'auditlog', ['action_type'], 
                     unique=False)
    op.create_index('idx_auditlog_operator_time', 'auditlog', ['operator_id', 'action_time'], 
                     unique=False)


def downgrade():
    # ### 删除 auditlog 表的索引 ###
    op.drop_index('idx_auditlog_operator_time', table_name='auditlog')
    op.drop_index('idx_auditlog_action_type', table_name='auditlog')
    op.drop_index('idx_auditlog_action_time', table_name='auditlog')
    op.drop_index('idx_auditlog_operator_id', table_name='auditlog')
    
    # ### 删除 timeslot 表的索引 ###
    op.drop_index('idx_timeslot_equip_active', table_name='timeslot')
    op.drop_index('idx_timeslot_is_active', table_name='timeslot')
    op.drop_index('idx_timeslot_equip_id', table_name='timeslot')
    
    # ### 删除 teacher 表的索引 ###
    op.drop_index('idx_teacher_lab_id', table_name='teacher')
    
    # ### 删除 student 表的索引 ###
    op.drop_index('idx_student_lab_t', table_name='student')
    op.drop_index('idx_student_t_id', table_name='student')
    op.drop_index('idx_student_lab_id', table_name='student')
    
    # ### 删除 equipment 表的索引 ###
    op.drop_index('idx_equipment_lab_status', table_name='equipment')
    op.drop_index('idx_equipment_category', table_name='equipment')
    op.drop_index('idx_equipment_status', table_name='equipment')
    op.drop_index('idx_equipment_lab_id', table_name='equipment')
    
    # ### 删除 reservation 表的索引 ###
    op.drop_index('idx_reservation_teacher_status', table_name='reservation')
    op.drop_index('idx_reservation_student_status', table_name='reservation')
    op.drop_index('idx_reservation_equip_status', table_name='reservation')
    op.drop_index('idx_reservation_apply_time', table_name='reservation')
    op.drop_index('idx_reservation_status', table_name='reservation')
    op.drop_index('idx_reservation_teacher_id', table_name='reservation')
    op.drop_index('idx_reservation_student_id', table_name='reservation')
    op.drop_index('idx_reservation_equip_id', table_name='reservation')

