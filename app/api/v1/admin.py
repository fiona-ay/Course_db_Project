"""
管理员 API 路由
处理管理员相关的设备管理功能
"""
from flask import Blueprint, request
from flasgger import swag_from
from app.services import equipment_service
from app.api.v1.schemas.equipment_schema import (
    EquipmentSchema, EquipmentCreateSchema, EquipmentUpdateSchema
)
from app.utils.response import success, fail
from app.utils.exceptions import NotFoundError, ValidationError
from app.utils.auth import admin_required
from app.utils.redis_client import redis_client
# 在文件顶部添加导入
from app.utils.auth import admin_required, get_current_user
# 创建蓝图
admin_bp = Blueprint('admin', __name__)

# 实例化 Schema
equipment_schema = EquipmentSchema()
equipment_create_schema = EquipmentCreateSchema()
equipment_update_schema = EquipmentUpdateSchema()


@admin_bp.route('/equipments', methods=['POST'])
@admin_required
@swag_from({
    'tags': ['管理员设备管理'],
    'summary': '新增设备',
    'description': '管理员新增设备',
    'security': [{'Bearer': []}],
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'required': ['name', 'category'],
            'properties': {
                'name': {'type': 'string', 'example': '扫描电子显微镜', 'description': '设备名称'},
                'lab_id': {'type': 'integer', 'example': 1, 'description': '所属实验室ID'},
                'category': {'type': 'integer', 'example': 2, 'description': '设备类别 (1:学院, 2:实验室)'},
                'status': {'type': 'integer', 'example': 1, 'description': '设备状态'}
            }
        }
    }],
    'responses': {
        200: {
            'description': '成功创建设备',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 200},
                    'msg': {'type': 'string', 'example': '创建成功'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'name': {'type': 'string', 'example': '扫描电子显微镜'}
                        }
                    }
                }
            }
        },
        403: {
            'description': '需要管理员权限'
        },
        422: {
            'description': '数据验证失败'
        }
    }
})
def create_equipment():
    """管理员新增设备"""
    try:
        json_data = request.get_json()
        if not json_data:
            return fail(code=400, msg='请求体不能为空')
        
        # 验证数据
        errors = equipment_create_schema.validate(json_data)
        if errors:
            return fail(code=422, msg='数据验证失败', data=errors)
        
        validated_data = equipment_create_schema.load(json_data)
        
        # 创建设备
        equipment = equipment_service.create_equipment(validated_data)
        
        # 清除相关缓存（使用通配符删除所有相关缓存）
        _clear_equipment_cache()
        
        # 序列化返回
        data = equipment_schema.dump(equipment)
        return success(data=data, msg='创建成功')
    except ValidationError as e:
        return fail(code=422, msg=e.message, data=e.payload)
    except Exception as e:
        return fail(code=500, msg=f'创建失败: {str(e)}')


@admin_bp.route('/equipments/<int:equip_id>', methods=['PUT'])
@admin_required
@swag_from({
    'tags': ['管理员设备管理'],
    'summary': '修改设备信息',
    'description': '管理员修改设备信息或状态',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'equip_id',
            'type': 'integer',
            'required': True,
            'description': '设备ID'
        },
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'example': '扫描电子显微镜', 'description': '设备名称'},
                    'lab_id': {'type': 'integer', 'example': 1, 'description': '所属实验室ID'},
                    'category': {'type': 'integer', 'example': 2, 'description': '设备类别'},
                    'status': {'type': 'integer', 'example': 1, 'description': '设备状态'},
                    'next_avail_time': {'type': 'string', 'format': 'date-time', 'description': '下次可用时间'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': '成功更新设备',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 200},
                    'msg': {'type': 'string', 'example': '更新成功'}
                }
            }
        },
        403: {
            'description': '需要管理员权限'
        },
        404: {
            'description': '设备不存在'
        }
    }
})
def update_equipment(equip_id):
    """管理员修改设备信息"""
    try:
        json_data = request.get_json()
        if not json_data:
            return fail(code=400, msg='请求体不能为空')
        
        # 验证数据
        errors = equipment_update_schema.validate(json_data)
        if errors:
            return fail(code=422, msg='数据验证失败', data=errors)
        
        validated_data = equipment_update_schema.load(json_data)
        
        # 更新设备
        equipment = equipment_service.update_equipment(equip_id, validated_data)
        
        # 清除相关缓存
        _clear_equipment_cache(equip_id=equip_id)
        
        # 序列化返回
        data = equipment_schema.dump(equipment)
        return success(data=data, msg='更新成功')
    except NotFoundError as e:
        return fail(code=404, msg=e.message)
    except ValidationError as e:
        return fail(code=422, msg=e.message, data=e.payload)
    except Exception as e:
        return fail(code=500, msg=f'更新失败: {str(e)}')


@admin_bp.route('/equipments/<int:equip_id>', methods=['DELETE'])
@admin_required
@swag_from({
    'tags': ['管理员设备管理'],
    'summary': '删除设备',
    'description': '管理员删除设备',
    'security': [{'Bearer': []}],
    'parameters': [{
        'in': 'path',
        'name': 'equip_id',
        'type': 'integer',
        'required': True,
        'description': '设备ID'
    }],
    'responses': {
        200: {
            'description': '成功删除设备',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 200},
                    'msg': {'type': 'string', 'example': '删除成功'}
                }
            }
        },
        403: {
            'description': '需要管理员权限'
        },
        404: {
            'description': '设备不存在'
        },
        422: {
            'description': '删除失败（如存在关联数据）'
        }
    }
})
def delete_equipment(equip_id):
    """管理员删除设备"""
    try:
        equipment_service.delete_equipment(equip_id)
        
        # 清除相关缓存
        _clear_equipment_cache(equip_id=equip_id)
        
        return success(msg='删除成功')
    except NotFoundError as e:
        return fail(code=404, msg=e.message)
    except ValidationError as e:
        return fail(code=422, msg=e.message, data=e.payload)
    except Exception as e:
        return fail(code=500, msg=f'删除失败: {str(e)}')


def _clear_equipment_cache(equip_id=None):
    """
    清除设备相关缓存
    
    Args:
        equip_id: 设备ID，如果提供则清除该设备的详情缓存
    """
    # 清除详情缓存
    if equip_id:
        redis_client.delete(f'api:equipment:detail:{equip_id}')
    
    # 注意：Redis 不支持通配符删除，列表缓存会在过期后自动清除
    # 如果需要立即清除所有列表缓存，可以使用 Redis SCAN 命令遍历删除
    # 这里简化处理，让列表缓存自然过期（5分钟）

# 在文件末尾添加以下代码

from app.services import reservation_service
from app.api.v1.schemas.reservation_schema import ReservationSchema, ReservationQuerySchema

# 实例化 Schema
reservation_schema = ReservationSchema()
reservation_query_schema = ReservationQuerySchema()


@admin_bp.route('/reservations', methods=['GET'])
@admin_required
@swag_from({
    'tags': ['管理员预约管理'],
    'summary': '获取所有预约列表',
    'description': '管理员获取所有预约列表',
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
        403: {
            'description': '需要管理员权限'
        }
    }
})
def get_all_reservations():
    """管理员获取所有预约列表"""
    try:
        # 获取查询参数
        equip_id = request.args.get('equip_id', type=int)
        status = request.args.get('status', type=int)
        
        # 构建缓存键
        cache_key = f'api:admin:reservation:list:equip_{equip_id}:status_{status}'
        
        # 尝试从缓存获取
        cached_data = redis_client.get(cache_key)
        if cached_data is not None:
            return success(data=cached_data, msg='查询成功')
        
        # 查询所有预约列表（管理员不限制用户）
        reservations = reservation_service.get_reservation_list(
            equip_id=equip_id,
            status=status
        )
        
        # 序列化
        data = reservation_schema.dump(reservations, many=True)
        
        # 存入缓存（3分钟过期）
        redis_client.set(cache_key, data, ex=180)
        
        return success(data=data, msg='查询成功')
    except Exception as e:
        return fail(code=500, msg=f'查询失败: {str(e)}')


@admin_bp.route('/reservations/<int:reservation_id>/approve', methods=['PUT'])
@admin_required
@swag_from({
    'tags': ['管理员预约管理'],
    'summary': '审批通过预约',
    'description': '管理员审批通过预约',
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
            'description': '成功审批通过',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 200},
                    'msg': {'type': 'string', 'example': '审批通过'}
                }
            }
        },
        403: {
            'description': '需要管理员权限'
        },
        404: {
            'description': '预约不存在'
        },
        422: {
            'description': '审批失败'
        }
    }
})
def approve_reservation(reservation_id):
    """管理员审批通过预约"""
    try:
        # 获取当前管理员
        current_user = get_current_user()
        
        # 审批通过（状态改为1-通过）
        reservation = reservation_service.update_reservation_status(
            reservation_id, 1, current_user['user_id']
        )
        
        # 序列化返回
        data = reservation_schema.dump(reservation)
        return success(data=data, msg='审批通过')
    except NotFoundError as e:
        return fail(code=404, msg=e.message)
    except ValidationError as e:
        return fail(code=422, msg=e.message, data=e.payload)
    except Exception as e:
        return fail(code=500, msg=f'审批失败: {str(e)}')


@admin_bp.route('/reservations/<int:reservation_id>/reject', methods=['PUT'])
@admin_required
@swag_from({
    'tags': ['管理员预约管理'],
    'summary': '审批拒绝预约',
    'description': '管理员审批拒绝预约',
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
            'description': '成功审批拒绝',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 200},
                    'msg': {'type': 'string', 'example': '审批拒绝'}
                }
            }
        },
        403: {
            'description': '需要管理员权限'
        },
        404: {
            'description': '预约不存在'
        },
        422: {
            'description': '审批失败'
        }
    }
})
def reject_reservation(reservation_id):
    """管理员审批拒绝预约"""
    try:
        # 获取当前管理员
        current_user = get_current_user()
        
        # 审批拒绝（状态改为2-拒绝）
        reservation = reservation_service.update_reservation_status(
            reservation_id, 2, current_user['user_id']
        )
        
        # 序列化返回
        data = reservation_schema.dump(reservation)
        return success(data=data, msg='审批拒绝')
    except NotFoundError as e:
        return fail(code=404, msg=e.message)
    except ValidationError as e:
        return fail(code=422, msg=e.message, data=e.payload)
    except Exception as e:
        return fail(code=500, msg=f'审批失败: {str(e)}')