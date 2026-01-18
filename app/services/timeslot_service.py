"""
时间段服务层，处理时间段相关的业务逻辑
"""
from datetime import time
from sqlalchemy import and_

from app import db
from app.models.equipment import Equipment
from app.models.timeslot import TimeSlot
from app.utils.exceptions import NotFoundError, ValidationError


def _normalize_time(value):
    """
    将字符串时间规范为 time 对象，支持 HH:MM 或 HH:MM:SS
    """
    if isinstance(value, time):
        return value

    if isinstance(value, str):
        parts = value.strip().split(':')
        if len(parts) == 2:
            parts.append('00')
        if len(parts) != 3:
            raise ValidationError('时间格式必须为 HH:MM:SS', payload={'field': 'time'})
        try:
            h, m, s = map(int, parts)
            return time(hour=h, minute=m, second=s)
        except Exception:
            raise ValidationError('时间格式必须为 HH:MM:SS', payload={'field': 'time'})

    raise ValidationError('时间格式必须为 HH:MM:SS', payload={'field': 'time'})


def _validate_time_range(start_time, end_time):
    """
    校验时间范围是否合法
    """
    if start_time >= end_time:
        raise ValidationError('开始时间必须早于结束时间', payload={'field': 'time_range'})


def _check_overlap(equip_id, start_time, end_time, exclude_slot_id=None):
    """
    检查同一设备下时间段是否与现有时间段重叠
    """
    query = TimeSlot.query.filter(TimeSlot.equip_id == equip_id)
    if exclude_slot_id:
        query = query.filter(TimeSlot.slot_id != exclude_slot_id)

    # 重叠条件：max(start1, start2) < min(end1, end2)
    conflict = query.filter(
        and_(TimeSlot.start_time < end_time, TimeSlot.end_time > start_time)
    ).first()

    if conflict:
        raise ValidationError('时间段与已有配置冲突', payload={'conflict_slot_id': conflict.slot_id})


def _check_equipment_exists(equip_id):
    equipment = Equipment.query.get(equip_id)
    if not equipment:
        raise NotFoundError('设备不存在', payload={'field': 'equip_id'})
    return equipment


def get_timeslots_by_equipment(equip_id, only_active=False):
    """
    获取设备的时间段列表
    """
    _check_equipment_exists(equip_id)
    query = TimeSlot.query.filter(TimeSlot.equip_id == equip_id)
    if only_active:
        query = query.filter(TimeSlot.is_active == 1)
    return query.order_by(TimeSlot.start_time.asc()).all()


def get_available_timeslots(equip_id):
    """
    获取设备可用时间段（当前阶段仅返回激活的时间段）
    """
    # TODO: 关联 Reservation 表，排除状态为 Pending(0) 和 Approved(1) 的时间段
    return get_timeslots_by_equipment(equip_id, only_active=True)


def check_slot_usage(slot_id):
    """
    预留：检查时间段是否已有预约占用
    当前阶段返回 False，后续实现时用于阻止删除/修改时间范围
    """
    return False


def create_timeslot(data):
    """
    创建时间段
    """
    equip_id = data.get('equip_id')
    start_time = _normalize_time(data.get('start_time'))
    end_time = _normalize_time(data.get('end_time'))
    is_active = data.get('is_active', 1)

    _check_equipment_exists(equip_id)
    _validate_time_range(start_time, end_time)
    _check_overlap(equip_id, start_time, end_time)

    slot = TimeSlot(
        equip_id=equip_id,
        start_time=start_time,
        end_time=end_time,
        is_active=is_active
    )
    try:
        db.session.add(slot)
        db.session.commit()
        return slot
    except Exception as e:
        db.session.rollback()
        raise ValidationError(f'创建时间段失败: {str(e)}')


def update_timeslot(slot_id, data):
    """
    更新时间段
    """
    slot = TimeSlot.query.get(slot_id)
    if not slot:
        raise NotFoundError('时间段不存在')

    # 预留占用检查
    if check_slot_usage(slot_id):
        raise ValidationError('该时间段已有关联预约，禁止修改时间范围', payload={'slot_id': slot_id})

    if 'equip_id' in data:
        equip_id = data.get('equip_id')
        _check_equipment_exists(equip_id)
        slot.equip_id = equip_id
    else:
        equip_id = slot.equip_id

    start_time = slot.start_time
    end_time = slot.end_time

    if 'start_time' in data:
        start_time = _normalize_time(data.get('start_time'))
    if 'end_time' in data:
        end_time = _normalize_time(data.get('end_time'))
    if start_time != slot.start_time or end_time != slot.end_time:
        _validate_time_range(start_time, end_time)
        _check_overlap(equip_id, start_time, end_time, exclude_slot_id=slot.slot_id)
        slot.start_time = start_time
        slot.end_time = end_time

    if 'is_active' in data:
        slot.is_active = data.get('is_active')

    try:
        db.session.commit()
        return slot
    except Exception as e:
        db.session.rollback()
        raise ValidationError(f'更新时间段失败: {str(e)}')


def delete_timeslot(slot_id):
    """
    删除时间段
    """
    slot = TimeSlot.query.get(slot_id)
    if not slot:
        raise NotFoundError('时间段不存在')

    # 预留占用检查
    if check_slot_usage(slot_id):
        raise ValidationError('该时间段已有关联预约，禁止删除', payload={'slot_id': slot_id})

    try:
        equip_id = slot.equip_id
        db.session.delete(slot)
        db.session.commit()
        return equip_id
    except Exception as e:
        db.session.rollback()
        raise ValidationError(f'删除时间段失败: {str(e)}')
