"""
时间段 Schema 定义
"""
from marshmallow import fields, pre_load, ValidationError as MarshmallowValidationError
from app.utils.schemas import BaseSchema, BaseCreateSchema, BaseUpdateSchema


def _normalize_time_string(value):
    """
    将  HH:MM  填充为 HH:MM:SS，确保后续解析一致
    """
    if value is None:
        return value
    if isinstance(value, str):
        value = value.strip()
        if len(value) == 5:
            return f"{value}:00"
        return value
    return value


class TimeSlotSchema(BaseSchema):
    """时间段响应 Schema"""
    slot_id = fields.Integer(dump_only=True, description='时间段ID')
    equip_id = fields.Integer(required=True, description='设备ID')
    start_time = fields.Time(required=True, format='%H:%M:%S', description='开始时间')
    end_time = fields.Time(required=True, format='%H:%M:%S', description='结束时间')
    is_active = fields.Integer(required=True, description='是否激活 (1:激活 0:禁用)')

    @pre_load
    def _fill_seconds(self, data, **kwargs):
        for key in ['start_time', 'end_time']:
            if key in data:
                data[key] = _normalize_time_string(data[key])
        return data


class TimeSlotCreateSchema(BaseCreateSchema):
    """创建时间段请求 Schema"""
    equip_id = fields.Integer(required=True, description='设备ID')
    start_time = fields.Time(required=True, format='%H:%M:%S', description='开始时间')
    end_time = fields.Time(required=True, format='%H:%M:%S', description='结束时间')
    is_active = fields.Integer(missing=1, description='是否激活 (1:激活 0:禁用)')

    @pre_load
    def _fill_seconds(self, data, **kwargs):
        for key in ['start_time', 'end_time']:
            if key in data:
                data[key] = _normalize_time_string(data[key])
        return data


class TimeSlotUpdateSchema(BaseUpdateSchema):
    """更新时间段请求 Schema"""
    equip_id = fields.Integer(description='设备ID')
    start_time = fields.Time(format='%H:%M:%S', description='开始时间')
    end_time = fields.Time(format='%H:%M:%S', description='结束时间')
    is_active = fields.Integer(description='是否激活 (1:激活 0:禁用)')

    @pre_load
    def _fill_seconds(self, data, **kwargs):
        for key in ['start_time', 'end_time']:
            if key in data:
                data[key] = _normalize_time_string(data[key])
        return data
