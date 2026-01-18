"""
时间段 API 路由
"""
from flask import Blueprint, request
from flasgger import swag_from

from app.services import timeslot_service
from app.api.v1.schemas.timeslot_schema import TimeSlotSchema
from app.utils.response import success, fail
from app.utils.auth import login_required
from app.utils.exceptions import NotFoundError, ValidationError
from app.utils.redis_client import redis_client

timeslot_bp = Blueprint('timeslot', __name__)

timeslot_schema = TimeSlotSchema()


@timeslot_bp.route('/equipment/<int:equip_id>', methods=['GET'])
@login_required
@swag_from({
    'tags': ['时间段管理'],
    'summary': '获取设备时间段列表',
    'description': '返回指定设备的全部时间段，支持 only_active 过滤；默认包含禁用时间段，按开始时间升序。',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'equip_id',
            'required': True,
            'type': 'integer',
            'description': '设备ID'
        },
        {
            'in': 'query',
            'name': 'only_active',
            'required': False,
            'type': 'boolean',
            'description': '是否仅返回激活的时间段（true/false）'
        }
    ],
    'responses': {
        200: {
            'description': '成功返回时间段列表',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 200},
                    'msg': {'type': 'string', 'example': 'success'},
                    'data': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'slot_id': {'type': 'integer', 'example': 1},
                                'equip_id': {'type': 'integer', 'example': 1},
                                'start_time': {'type': 'string', 'example': '09:00:00'},
                                'end_time': {'type': 'string', 'example': '10:00:00'},
                                'is_active': {'type': 'integer', 'example': 1}
                            }
                        }
                    }
                }
            }
        }
    }
})
def get_timeslots(equip_id):
    try:
        only_active = str(request.args.get('only_active', '')).lower() in ('true', '1')

        # 仅对完整列表做缓存，only_active 时不使用缓存以避免歧义
        cache_key = f'timeslot:list:{equip_id}'
        if not only_active:
            cached_data = redis_client.get(cache_key)
            if cached_data is not None:
                return success(data=cached_data, msg='查询成功')

        slots = timeslot_service.get_timeslots_by_equipment(equip_id, only_active=only_active)
        data = timeslot_schema.dump(slots, many=True)

        if not only_active:
            redis_client.set(cache_key, data, ex=3600)

        return success(data=data, msg='查询成功')
    except NotFoundError as e:
        return fail(code=404, msg=e.message, data=e.payload)
    except ValidationError as e:
        return fail(code=422, msg=e.message, data=e.payload)
    except Exception as e:
        return fail(code=500, msg=f'查询失败: {str(e)}')


@timeslot_bp.route('/equipment/<int:equip_id>/available', methods=['GET'])
@login_required
@swag_from({
    'tags': ['时间段管理'],
    'summary': '获取设备可用时间段',
    'description': '返回设备可用时间段（当前仅返回 is_active=1 的时间段，后续需结合预约排除占用时间段）。',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'equip_id',
            'required': True,
            'type': 'integer',
            'description': '设备ID'
        }
    ],
    'responses': {
        200: {
            'description': '成功返回可用时间段列表',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 200},
                    'msg': {'type': 'string', 'example': 'success'},
                    'data': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'slot_id': {'type': 'integer', 'example': 1},
                                'equip_id': {'type': 'integer', 'example': 1},
                                'start_time': {'type': 'string', 'example': '09:00:00'},
                                'end_time': {'type': 'string', 'example': '10:00:00'},
                                'is_active': {'type': 'integer', 'example': 1}
                            }
                        }
                    }
                }
            }
        }
    }
})
def get_available_timeslots(equip_id):
    try:
        slots = timeslot_service.get_available_timeslots(equip_id)
        data = timeslot_schema.dump(slots, many=True)
        return success(data=data, msg='查询成功')
    except NotFoundError as e:
        return fail(code=404, msg=e.message, data=e.payload)
    except ValidationError as e:
        return fail(code=422, msg=e.message, data=e.payload)
    except Exception as e:
        return fail(code=500, msg=f'查询失败: {str(e)}')
