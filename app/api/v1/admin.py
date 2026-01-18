"""
ç®¡çå API è·¯ç±
å¤çç®¡çåç¸å³çè®¾å¤ç®¡çåè½
"""
from flask import Blueprint, request
from flasgger import swag_from
from app.services import equipment_service
from app.api.v1.schemas.equipment_schema import (
    EquipmentSchema, EquipmentCreateSchema, EquipmentUpdateSchema
)
from app.api.v1.schemas.timeslot_schema import (
    TimeSlotSchema, TimeSlotCreateSchema, TimeSlotUpdateSchema
)
from app.utils.response import success, fail
from app.utils.exceptions import NotFoundError, ValidationError
from app.utils.auth import admin_required
from app.utils.redis_client import redis_client
from app.services import timeslot_service
from app.models.timeslot import TimeSlot

# åå»ºèå¾
admin_bp = Blueprint('admin', __name__)

# å®ä¾å Schema
equipment_schema = EquipmentSchema()
equipment_create_schema = EquipmentCreateSchema()
equipment_update_schema = EquipmentUpdateSchema()
timeslot_schema = TimeSlotSchema()
timeslot_create_schema = TimeSlotCreateSchema()
timeslot_update_schema = TimeSlotUpdateSchema()


@admin_bp.route('/equipments', methods=['POST'])
@admin_required
@swag_from({
    'tags': ['ç®¡çåè®¾å¤ç®¡ç'],
    'summary': 'æ°å¢è®¾å¤',
    'description': 'ç®¡çåæ°å¢è®¾å¤',
    'security': [{'Bearer': []}],
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'required': ['name', 'category'],
            'properties': {
                'name': {'type': 'string', 'example': 'æ«æçµå­æ¾å¾®é', 'description': 'è®¾å¤åç§°'},
                'lab_id': {'type': 'integer', 'example': 1, 'description': 'æå±å®éªå®¤ID'},
                'category': {'type': 'integer', 'example': 2, 'description': 'è®¾å¤ç±»å« (1:å­¦é¢, 2:å®éªå®¤)'},
                'status': {'type': 'integer', 'example': 1, 'description': 'è®¾å¤ç¶æ'}
            }
        }
    }],
    'responses': {
        200: {
            'description': 'æååå»ºè®¾å¤',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 200},
                    'msg': {'type': 'string', 'example': 'åå»ºæå'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'name': {'type': 'string', 'example': 'æ«æçµå­æ¾å¾®é'}
                        }
                    }
                }
            }
        },
        403: {
            'description': 'éè¦ç®¡çåæé'
        },
        422: {
            'description': 'æ°æ®éªè¯å¤±è´¥'
        }
    }
})
def create_equipment():
    """ç®¡çåæ°å¢è®¾å¤"""
    try:
        json_data = request.get_json()
        if not json_data:
            return fail(code=400, msg='è¯·æ±ä½ä¸è½ä¸ºç©º')
        
        # éªè¯æ°æ®
        errors = equipment_create_schema.validate(json_data)
        if errors:
            return fail(code=422, msg='æ°æ®éªè¯å¤±è´¥', data=errors)
        
        validated_data = equipment_create_schema.load(json_data)
        
        # åå»ºè®¾å¤
        equipment = equipment_service.create_equipment(validated_data)
        
        # æ¸é¤ç¸å³ç¼å­ï¼ä½¿ç¨ééç¬¦å é¤ææç¸å³ç¼å­ï¼
        _clear_equipment_cache()
        
        # åºååè¿å
        data = equipment_schema.dump(equipment)
        return success(data=data, msg='åå»ºæå')
    except ValidationError as e:
        return fail(code=422, msg=e.message, data=e.payload)
    except Exception as e:
        return fail(code=500, msg=f'åå»ºå¤±è´¥: {str(e)}')


@admin_bp.route('/equipments/<int:equip_id>', methods=['PUT'])
@admin_required
@swag_from({
    'tags': ['ç®¡çåè®¾å¤ç®¡ç'],
    'summary': 'ä¿®æ¹è®¾å¤ä¿¡æ¯',
    'description': 'ç®¡çåä¿®æ¹è®¾å¤ä¿¡æ¯æç¶æ',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'equip_id',
            'type': 'integer',
            'required': True,
            'description': 'è®¾å¤ID'
        },
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'example': 'æ«æçµå­æ¾å¾®é', 'description': 'è®¾å¤åç§°'},
                    'lab_id': {'type': 'integer', 'example': 1, 'description': 'æå±å®éªå®¤ID'},
                    'category': {'type': 'integer', 'example': 2, 'description': 'è®¾å¤ç±»å«'},
                    'status': {'type': 'integer', 'example': 1, 'description': 'è®¾å¤ç¶æ'},
                    'next_avail_time': {'type': 'string', 'format': 'date-time', 'description': 'ä¸æ¬¡å¯ç¨æ¶é´'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'æåæ´æ°è®¾å¤',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 200},
                    'msg': {'type': 'string', 'example': 'æ´æ°æå'}
                }
            }
        },
        403: {
            'description': 'éè¦ç®¡çåæé'
        },
        404: {
            'description': 'è®¾å¤ä¸å­å¨'
        }
    }
})
def update_equipment(equip_id):
    """ç®¡çåä¿®æ¹è®¾å¤ä¿¡æ¯"""
    try:
        json_data = request.get_json()
        if not json_data:
            return fail(code=400, msg='è¯·æ±ä½ä¸è½ä¸ºç©º')
        
        # éªè¯æ°æ®
        errors = equipment_update_schema.validate(json_data)
        if errors:
            return fail(code=422, msg='æ°æ®éªè¯å¤±è´¥', data=errors)
        
        validated_data = equipment_update_schema.load(json_data)
        
        # æ´æ°è®¾å¤
        equipment = equipment_service.update_equipment(equip_id, validated_data)
        
        # æ¸é¤ç¸å³ç¼å­
        _clear_equipment_cache(equip_id=equip_id)
        
        # åºååè¿å
        data = equipment_schema.dump(equipment)
        return success(data=data, msg='æ´æ°æå')
    except NotFoundError as e:
        return fail(code=404, msg=e.message)
    except ValidationError as e:
        return fail(code=422, msg=e.message, data=e.payload)
    except Exception as e:
        return fail(code=500, msg=f'æ´æ°å¤±è´¥: {str(e)}')


@admin_bp.route('/equipments/<int:equip_id>', methods=['DELETE'])
@admin_required
@swag_from({
    'tags': ['ç®¡çåè®¾å¤ç®¡ç'],
    'summary': 'å é¤è®¾å¤',
    'description': 'ç®¡çåå é¤è®¾å¤',
    'security': [{'Bearer': []}],
    'parameters': [{
        'in': 'path',
        'name': 'equip_id',
        'type': 'integer',
        'required': True,
        'description': 'è®¾å¤ID'
    }],
    'responses': {
        200: {
            'description': 'æåå é¤è®¾å¤',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 200},
                    'msg': {'type': 'string', 'example': 'å é¤æå'}
                }
            }
        },
        403: {
            'description': 'éè¦ç®¡çåæé'
        },
        404: {
            'description': 'è®¾å¤ä¸å­å¨'
        },
        422: {
            'description': 'å é¤å¤±è´¥ï¼å¦å­å¨å³èæ°æ®ï¼'
        }
    }
})
def delete_equipment(equip_id):
    """ç®¡çåå é¤è®¾å¤"""
    try:
        equipment_service.delete_equipment(equip_id)
        
        # æ¸é¤ç¸å³ç¼å­
        _clear_equipment_cache(equip_id=equip_id)
        
        return success(msg='å é¤æå')
    except NotFoundError as e:
        return fail(code=404, msg=e.message)
    except ValidationError as e:
        return fail(code=422, msg=e.message, data=e.payload)
    except Exception as e:
        return fail(code=500, msg=f'å é¤å¤±è´¥: {str(e)}')


@admin_bp.route('/timeslots', methods=['POST'])
@admin_required
@swag_from({
    'tags': ['ç®¡çåæ¶é´æ®µç®¡ç'],
    'summary': 'åå»ºæ¶é´æ®µ',
    'description': 'ç®¡çåä¸ºè®¾å¤æ°å¢æ¶é´æ®µï¼ä¸¥æ ¼æ ¡éªæ¶é´æ ¼å¼ä¸å²çªã',
    'security': [{'Bearer': []}],
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'required': ['equip_id', 'start_time', 'end_time'],
            'properties': {
                'equip_id': {'type': 'integer', 'example': 1, 'description': 'è®¾å¤ID'},
                'start_time': {'type': 'string', 'example': '09:00:00', 'description': 'å¼å§æ¶é´(HH:MM:SS)'},
                'end_time': {'type': 'string', 'example': '10:00:00', 'description': 'ç»ææ¶é´(HH:MM:SS)'},
                'is_active': {'type': 'integer', 'example': 1, 'description': 'æ¯å¦æ¿æ´»(1/0)'}
            }
        }
    }],
    'responses': {
        200: {'description': 'åå»ºæå'},
        422: {'description': 'æ ¡éªå¤±è´¥'},
    }
})
def create_timeslot():
    """ç®¡çååå»ºæ¶é´æ®µ"""
    try:
        json_data = request.get_json()
        if not json_data:
            return fail(code=400, msg='è¯·æ±ä½ä¸è½ä¸ºç©º')

        errors = timeslot_create_schema.validate(json_data)
        if errors:
            return fail(code=422, msg='æ°æ®æ ¡éªå¤±è´¥', data=errors)

        validated_data = timeslot_create_schema.load(json_data)
        slot = timeslot_service.create_timeslot(validated_data)

        _clear_timeslot_cache(slot.equip_id)

        data = timeslot_schema.dump(slot)
        return success(data=data, msg='åå»ºæå')
    except NotFoundError as e:
        return fail(code=404, msg=e.message, data=e.payload)
    except ValidationError as e:
        return fail(code=422, msg=e.message, data=e.payload)
    except Exception as e:
        return fail(code=500, msg=f'åå»ºå¤±è´¥: {str(e)}')


@admin_bp.route('/timeslots/<int:slot_id>', methods=['PUT'])
@admin_required
@swag_from({
    'tags': ['ç®¡çåæ¶é´æ®µç®¡ç'],
    'summary': 'æ´æ°æ¶é´æ®µ',
    'description': 'ç®¡çåæ´æ°æ¶é´æ®µï¼åå«æ¶é´å²çªä¸è®¾å¤æ ¡éªã',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'slot_id',
            'required': True,
            'type': 'integer',
            'description': 'æ¶é´æ®µID'
        },
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'equip_id': {'type': 'integer', 'example': 1, 'description': 'è®¾å¤ID'},
                    'start_time': {'type': 'string', 'example': '09:00:00', 'description': 'å¼å§æ¶é´(HH:MM:SS)'},
                    'end_time': {'type': 'string', 'example': '10:00:00', 'description': 'ç»ææ¶é´(HH:MM:SS)'},
                    'is_active': {'type': 'integer', 'example': 1, 'description': 'æ¯å¦æ¿æ´»(1/0)'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'æ´æ°æå'},
        404: {'description': 'æ¶é´æ®µä¸å­å¨'},
        422: {'description': 'æ ¡éªå¤±è´¥'}
    }
})
def update_timeslot(slot_id):
    """ç®¡çåæ´æ°æ¶é´æ®µ"""
    try:
        json_data = request.get_json()
        if not json_data:
            return fail(code=400, msg='è¯·æ±ä½ä¸è½ä¸ºç©º')

        errors = timeslot_update_schema.validate(json_data)
        if errors:
            return fail(code=422, msg='æ°æ®æ ¡éªå¤±è´¥', data=errors)

        validated_data = timeslot_update_schema.load(json_data)

        old_slot = TimeSlot.query.get(slot_id)
        old_equip_id = old_slot.equip_id if old_slot else None

        slot = timeslot_service.update_timeslot(slot_id, validated_data)

        _clear_timeslot_cache(slot.equip_id)
        if old_equip_id and old_equip_id != slot.equip_id:
            _clear_timeslot_cache(old_equip_id)

        data = timeslot_schema.dump(slot)
        return success(data=data, msg='æ´æ°æå')
    except NotFoundError as e:
        return fail(code=404, msg=e.message, data=e.payload)
    except ValidationError as e:
        return fail(code=422, msg=e.message, data=e.payload)
    except Exception as e:
        return fail(code=500, msg=f'æ´æ°å¤±è´¥: {str(e)}')


@admin_bp.route('/timeslots/<int:slot_id>', methods=['DELETE'])
@admin_required
@swag_from({
    'tags': ['ç®¡çåæ¶é´æ®µç®¡ç'],
    'summary': 'å é¤æ¶é´æ®µ',
    'description': 'ç®¡çåå é¤æ¶é´æ®µï¼åç»­è¥æå³èé¢çº¦éé»æ­¢å é¤ã',
    'security': [{'Bearer': []}],
    'parameters': [{
        'in': 'path',
        'name': 'slot_id',
        'required': True,
        'type': 'integer',
        'description': 'æ¶é´æ®µID'
    }],
    'responses': {
        200: {'description': 'å é¤æå'},
        404: {'description': 'æ¶é´æ®µä¸å­å¨'},
        422: {'description': 'å é¤å¤±è´¥'}
    }
})
def delete_timeslot(slot_id):
    """ç®¡çåå é¤æ¶é´æ®µ"""
    try:
        equip_id = timeslot_service.delete_timeslot(slot_id)
        _clear_timeslot_cache(equip_id)
        return success(msg='å é¤æå')
    except NotFoundError as e:
        return fail(code=404, msg=e.message, data=e.payload)
    except ValidationError as e:
        return fail(code=422, msg=e.message, data=e.payload)
    except Exception as e:
        return fail(code=500, msg=f'å é¤å¤±è´¥: {str(e)}')


def _clear_equipment_cache(equip_id=None):
    """
    æ¸é¤è®¾å¤ç¸å³ç¼å­
    
    Args:
        equip_id: è®¾å¤IDï¼å¦ææä¾åæ¸é¤è¯¥è®¾å¤çè¯¦æç¼å­
    """
    # æ¸é¤è¯¦æç¼å­
    if equip_id:
        redis_client.delete(f'api:equipment:detail:{equip_id}')
    
    # æ³¨æï¼Redis ä¸æ¯æééç¬¦å é¤ï¼åè¡¨ç¼å­ä¼å¨è¿æåèªå¨æ¸é¤
    # å¦æéè¦ç«å³æ¸é¤ææåè¡¨ç¼å­ï¼å¯ä»¥ä½¿ç¨ Redis SCAN å½ä»¤éåå é¤
    # è¿éç®åå¤çï¼è®©åè¡¨ç¼å­èªç¶è¿æï¼5åéï¼

def _clear_timeslot_cache(equip_id):
    """
    Çå³ýÊ±¼ä¶ÎÁÐ±í»º´æ
    """
    redis_client.delete(f'timeslot:list:{equip_id}')
