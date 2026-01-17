"""
预约 Schema 定义
用于数据验证和序列化
"""
from marshmallow import fields, validate
from app.utils.schemas import BaseCreateSchema, BaseUpdateSchema, BaseSchema


class ReservationSchema(BaseSchema):
    """预约 Schema（用于响应）"""
    id = fields.Integer(dump_only=True, description='预约ID')
    student_id = fields.String(allow_none=True, description='学生ID')
    teacher_id = fields.String(allow_none=True, description='导师ID')
    equip_id = fields.Integer(required=True, description='设备ID')
    status = fields.Integer(required=True, validate=validate.OneOf([0, 1, 2, 3]), description='预约状态 (0:待审, 1:通过, 2:拒绝, 3:已取消)')
    apply_time = fields.DateTime(dump_only=True, format='iso', description='申请时间')
    approver_id = fields.String(allow_none=True, description='审批人ID')
    approve_time = fields.DateTime(allow_none=True, format='iso', description='审批时间')
    
    # 冗余字段
    user_name = fields.String(allow_none=True, description='用户名')
    equip_name = fields.String(allow_none=True, description='设备名称')
    price = fields.Decimal(allow_none=True, places=2, description='价格')
    start_time = fields.DateTime(allow_none=True, format='iso', description='开始时间')
    end_time = fields.DateTime(allow_none=True, format='iso', description='结束时间')


class ReservationCreateSchema(BaseCreateSchema):
    """创建预约 Schema（用于 POST 请求）"""
    equip_id = fields.Integer(required=True, validate=validate.Range(min=1), error_messages={
        'required': '设备ID不能为空',
        'invalid': '设备ID必须为正整数'
    }, description='设备ID')
    price = fields.Decimal(allow_none=True, places=2, validate=validate.Range(min=0), description='价格')
    start_time = fields.DateTime(allow_none=True, format='iso', description='开始时间')
    end_time = fields.DateTime(allow_none=True, format='iso', description='结束时间')


class ReservationUpdateSchema(BaseUpdateSchema):
    """更新预约 Schema（用于 PUT 请求）"""
    status = fields.Integer(validate=validate.OneOf([0, 1, 2, 3]), description='预约状态')


class ReservationQuerySchema(BaseSchema):
    """预约查询 Schema（用于 GET 请求参数）"""
    equip_id = fields.Integer(allow_none=True, description='设备ID筛选')
    status = fields.Integer(allow_none=True, validate=validate.OneOf([0, 1, 2, 3]), description='状态筛选')