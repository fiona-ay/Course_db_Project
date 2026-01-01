"""
设备 Schema 定义
用于数据验证和序列化
"""
from marshmallow import fields, validate
from app.utils.schemas import BaseCreateSchema, BaseUpdateSchema, BaseSchema


class EquipmentSchema(BaseSchema):
    """设备 Schema（用于响应）"""
    id = fields.Integer(dump_only=True, description='设备ID')
    name = fields.String(required=True, validate=validate.Length(min=1, max=100), description='设备名称')
    lab_id = fields.Integer(allow_none=True, description='所属实验室ID')
    category = fields.Integer(required=True, validate=validate.OneOf([1, 2]), description='设备类别 (1:学院, 2:实验室)')
    status = fields.Integer(required=True, validate=validate.Range(min=0, max=10), description='设备状态')
    next_avail_time = fields.DateTime(allow_none=True, format='iso', description='下次可用时间')


class EquipmentCreateSchema(BaseCreateSchema):
    """创建设备 Schema（用于 POST 请求）"""
    name = fields.String(required=True, validate=validate.Length(min=1, max=100), error_messages={
        'required': '设备名称不能为空',
        'invalid': '设备名称格式错误'
    }, description='设备名称')
    lab_id = fields.Integer(allow_none=True, description='所属实验室ID')
    category = fields.Integer(required=True, validate=validate.OneOf([1, 2]), error_messages={
        'required': '设备类别不能为空',
        'invalid': '设备类别必须是 1(学院) 或 2(实验室)'
    }, description='设备类别')
    status = fields.Integer(missing=1, validate=validate.Range(min=0, max=10), description='设备状态')


class EquipmentUpdateSchema(BaseUpdateSchema):
    """更新设备 Schema（用于 PUT 请求）"""
    name = fields.String(validate=validate.Length(min=1, max=100), error_messages={
        'invalid': '设备名称格式错误'
    }, description='设备名称')
    lab_id = fields.Integer(allow_none=True, description='所属实验室ID')
    category = fields.Integer(validate=validate.OneOf([1, 2]), error_messages={
        'invalid': '设备类别必须是 1(学院) 或 2(实验室)'
    }, description='设备类别')
    status = fields.Integer(validate=validate.Range(min=0, max=10), description='设备状态')
    next_avail_time = fields.DateTime(allow_none=True, format='iso', description='下次可用时间')


class EquipmentQuerySchema(BaseSchema):
    """设备查询 Schema（用于 GET 请求参数）"""
    lab_id = fields.Integer(allow_none=True, description='实验室ID筛选')
    keyword = fields.String(allow_none=True, description='关键词搜索（设备名称）')
    category = fields.Integer(allow_none=True, validate=validate.OneOf([1, 2]), description='设备类别筛选')
    status = fields.Integer(allow_none=True, validate=validate.Range(min=0, max=10), description='设备状态筛选')

