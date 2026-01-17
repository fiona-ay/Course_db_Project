"""
预约 API 路由
实现预约的 RESTful API
"""
from flask import Blueprint, request
from flasgger import swag_from
from app.services import reservation_service
from app.api.v1.schemas.reservation_schema import (
    ReservationSchema, ReservationCreateSchema, ReservationQuerySchema
)
from app.utils.response import success, fail
from app.utils.exceptions import NotFoundError, ValidationError
from app.utils.auth import login_required, get_current_user
from app.utils.redis_client import redis_client

# 创建蓝图
reservation_bp = Blueprint('reservation', __name__)

# 实例化 Schema
reservation_schema = ReservationSchema()
reservation_create_schema = ReservationCreateSchema()
reservation_query_schema = ReservationQuerySchema()


@reservation_bp.route('/', methods=['POST'])
@login_required
@swag_from({
    'tags': ['预约管理'],
    'summary': '创建预约',
    'description': '学生或教师创建设备预约（需要登录）',
    'security': [{'Bearer': []}],
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'required': ['equip_id'],
            'properties': {
                'equip_id': {'type': 'integer', 'example': 1, 'description': '设备ID'},
                'price': {'type': 'number', 'format': 'decimal', 'example': 100.50, 'description': '价格'},
                'start_time': {'type': 'string', 'format': 'date-time', 'description': '开始时间'},
                'end_time': {'type': 'string', 'format': 'date-time', 'description': '结束时间'}
            }
        }
    }],
    'responses': {
        200: {
            'description': '成功创建预约',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 200},
                    'msg': {'type': 'string', 'example': '创建成功'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'equip_id': {'type': 'integer', 'example': 1},
                            'status': {'type': 'integer', 'example': 0}
                        }
                    }
                }
            }
        },
        401: {
            'description': '未授权'
        },
        422: {
            'description': '数据验证失败'
        }
    }
})
def create_reservation():
    """创建预约"""
    try:
        json_data = request.get_json()
        if not json_data:
            return fail(code=400, msg='请求体不能为空')
        
        # 验证数据
        errors = reservation_create_schema.validate(json_data)
        if errors:
            return fail(code=422, msg='数据验证失败', data=errors)
        
        validated_data = reservation_create_schema.load(json_data)
        
        # 获取当前用户
        current_user = get_current_user()
        
        # 创建预约
        reservation = reservation_service.create_reservation(validated_data, current_user)
        
        # 序列化返回
        data = reservation_schema.dump(reservation)
        return success(data=data, msg='创建成功')
    except ValidationError as e:
        return fail(code=422, msg=e.message, data=e.payload)
    except Exception as e:
        return fail(code=500, msg=f'创建失败: {str(e)}')


@reservation_bp.route('/', methods=['GET'])
@login_required
@swag_from({
    'tags': ['预约管理'],
    'summary': '获取我的预约列表',
    'description': '获取当前用户的预约列表（需要登录）',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'in': 'query',
            'name': 'equip_id',
            'type': 'integer',
            'required': False,
            'description': '设备ID筛选'
        },
        {
            'in': 'query',
            'name': 'status',
            'type': 'integer',
            'required': False,
            'description': '状态筛选 (0:待审, 1:通过, 2:拒绝, 3:已取消)'
        }
    ],
    'responses': {
        200: {
            'description': '成功返回预约列表',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 200},
                    'msg': {'type': 'string', 'example': '查询成功'},
                    'data': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'example': 1},
                                'equip_id': {'type': 'integer', 'example': 1},
                                'status': {'type': 'integer', 'example': 0},
                                'user_name': {'type': 'string', 'example': '张三'},
                                'equip_name': {'type': 'string', 'example': '扫描电子显微镜'}
                            }
                        }
                    }
                }
            }
        },
        401: {
            'description': '未授权'
        }
    }
})
def get_my_reservations():
    """获取我的预约列表"""
    try:
        # 获取查询参数
        equip_id = request.args.get('equip_id', type=int)
        status = request.args.get('status', type=int)
        
        # 获取当前用户
        current_user = get_current_user()
        
        # 构建缓存键
        cache_key = f'api:reservation:list:user_{current_user["user_id"]}:type_{current_user["user_type"]}:equip_{equip_id}:status_{status}'
        
        # 尝试从缓存获取
        cached_data = redis_client.get(cache_key)
        if cached_data is not None:
            return success(data=cached_data, msg='查询成功')
        
        # 查询预约列表
        reservations = reservation_service.get_reservation_list(
            user_id=current_user['user_id'],
            user_type=current_user['user_type'],
            equip_id=equip_id,
            status=status
        )
        
        # 序列化
        data = reservation_schema.dump(reservations, many=True)
        
        # 存入缓存（5分钟过期）
        redis_client.set(cache_key, data, ex=300)
        
        return success(data=data, msg='查询成功')
    except Exception as e:
        return fail(code=500, msg=f'查询失败: {str(e)}')


@reservation_bp.route('/<int:reservation_id>', methods=['GET'])
@login_required
@swag_from({
    'tags': ['预约管理'],
    'summary': '获取预约详情',
    'description': '获取指定预约的详细信息（需要登录）',
    'security': [{'Bearer': []}],
    'parameters': [{
        'in': 'path',
        'name': 'reservation_id',
        'type': 'integer',
        'required': True,
        'description': '预约ID'
    }],
    'responses': {
        200: {
            'description': '成功返回预约详情',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 200},
                    'msg': {'type': 'string', 'example': '查询成功'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'equip_id': {'type': 'integer', 'example': 1},
                            'status': {'type': 'integer', 'example': 0},
                            'user_name': {'type': 'string', 'example': '张三'},
                            'equip_name': {'type': 'string', 'example': '扫描电子显微镜'}
                        }
                    }
                }
            }
        },
        404: {
            'description': '预约不存在'
        }
    }
})
def get_reservation(reservation_id):
    """获取预约详情"""
    try:
        # 尝试从缓存获取
        cache_key = f'api:reservation:detail:{reservation_id}'
        cached_data = redis_client.get(cache_key)
        if cached_data is not None:
            return success(data=cached_data, msg='查询成功')
        
        # 查询预约
        reservation = reservation_service.get_reservation_by_id(reservation_id)
        
        # 序列化
        data = reservation_schema.dump(reservation)
        
        # 存入缓存（10分钟过期）
        redis_client.set(cache_key, data, ex=600)
        
        return success(data=data, msg='查询成功')
    except NotFoundError as e:
        return fail(code=404, msg=e.message)
    except Exception as e:
        return fail(code=500, msg=f'查询失败: {str(e)}')


@reservation_bp.route('/<int:reservation_id>/cancel', methods=['PUT'])
@login_required
@swag_from({
    'tags': ['预约管理'],
    'summary': '取消预约',
    'description': '取消自己的预约（需要登录，只能取消自己的预约）',
    'security': [{'Bearer': []}],
    'parameters': [{
        'in': 'path',
        'name': 'reservation_id',
        'type': 'integer',
        'required': True,
        'description': '预约ID'
    }],
    'responses': {
        200: {
            'description': '成功取消预约',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 200},
                    'msg': {'type': 'string', 'example': '取消成功'}
                }
            }
        },
        403: {
            'description': '只能取消自己的预约'
        },
        404: {
            'description': '预约不存在'
        }
    }
})
def cancel_reservation(reservation_id):
    """取消预约"""
    try:
        # 获取当前用户
        current_user = get_current_user()
        
        # 查询预约
        reservation = reservation_service.get_reservation_by_id(reservation_id)
        
        # 验证权限：只能取消自己的预约
        user_id = current_user['user_id']
        user_type = current_user['user_type']
        
        if user_type == 'student' and reservation.student_id != user_id:
            return fail(code=403, msg='只能取消自己的预约')
        elif user_type == 'teacher' and reservation.teacher_id != user_id:
            return fail(code=403, msg='只能取消自己的预约')
        
        # 取消预约（状态改为3-已取消）
        reservation_service.update_reservation_status(reservation_id, 3)
        
        return success(msg='取消成功')
    except NotFoundError as e:
        return fail(code=404, msg=e.message)
    except ValidationError as e:
        return fail(code=422, msg=e.message, data=e.payload)
    except Exception as e:
        return fail(code=500, msg=f'取消失败: {str(e)}')