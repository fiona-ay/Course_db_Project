"""
设备 API 路由
实现设备的 RESTful API（读写分离：普通用户读，管理员写）
"""
from flask import Blueprint, request
from flasgger import swag_from
from app.services import equipment_service
from app.api.v1.schemas.equipment_schema import EquipmentSchema
from app.utils.response import success, fail
from app.utils.exceptions import NotFoundError
from app.utils.auth import login_required
from app.utils.redis_client import redis_client

# 创建蓝图
equipment_bp = Blueprint('equipment', __name__)

# 实例化 Schema
equipment_schema = EquipmentSchema()


@equipment_bp.route('/', methods=['GET'])
@equipment_bp.route('', methods=['GET'])  # 同时支持带斜杠和不带斜杠的 URL
@login_required
@swag_from({
    'tags': ['设备管理'],
    'summary': '获取设备列表',
    'description': '获取设备列表，支持按实验室ID和关键词筛选（普通用户可访问）',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'in': 'query',
            'name': 'lab_id',
            'type': 'integer',
            'required': False,
            'description': '实验室ID筛选'
        },
        {
            'in': 'query',
            'name': 'keyword',
            'type': 'string',
            'required': False,
            'description': '关键词搜索（设备名称）'
        },
        {
            'in': 'query',
            'name': 'category',
            'type': 'integer',
            'required': False,
            'description': '设备类别筛选 (1:学院, 2:实验室)'
        },
        {
            'in': 'query',
            'name': 'status',
            'type': 'integer',
            'required': False,
            'description': '设备状态筛选'
        }
    ],
    'responses': {
        200: {
            'description': '成功返回设备列表',
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
                                'id': {'type': 'integer', 'example': 1},
                                'name': {'type': 'string', 'example': '扫描电子显微镜'},
                                'lab_id': {'type': 'integer', 'example': 1},
                                'category': {'type': 'integer', 'example': 2},
                                'status': {'type': 'integer', 'example': 1}
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
def get_equipments():
    """获取设备列表（支持筛选）"""
    try:
        # 获取查询参数
        lab_id = request.args.get('lab_id', type=int)
        keyword = request.args.get('keyword', type=str)
        category = request.args.get('category', type=int)
        status = request.args.get('status', type=int)
        
        # 构建缓存键（包含所有筛选条件）
        cache_key = f'api:equipment:list:lab_{lab_id}:kw_{keyword}:cat_{category}:st_{status}'
        
        # 尝试从缓存获取
        cached_data = redis_client.get(cache_key)
        if cached_data is not None:
            return success(data=cached_data, msg='查询成功')
        
        # 查询设备列表
        equipments = equipment_service.get_equipment_list(
            lab_id=lab_id,
            keyword=keyword,
            category=category,
            status=status
        )
        
        # 序列化
        data = equipment_schema.dump(equipments, many=True)
        
        # 存入缓存（5分钟过期）
        redis_client.set(cache_key, data, ex=300)
        
        return success(data=data, msg='查询成功')
    except Exception as e:
        return fail(code=500, msg=f'查询失败: {str(e)}')


@equipment_bp.route('/<int:equip_id>', methods=['GET'])
@login_required
@swag_from({
    'tags': ['设备管理'],
    'summary': '获取设备详情',
    'description': '获取指定设备的详细信息（普通用户可访问）',
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
            'description': '成功返回设备详情',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 200},
                    'msg': {'type': 'string', 'example': 'success'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'name': {'type': 'string', 'example': '扫描电子显微镜'},
                            'lab_id': {'type': 'integer', 'example': 1},
                            'category': {'type': 'integer', 'example': 2},
                            'status': {'type': 'integer', 'example': 1}
                        }
                    }
                }
            }
        },
        404: {
            'description': '设备不存在'
        }
    }
})
def get_equipment(equip_id):
    """获取设备详情"""
    try:
        # 尝试从缓存获取
        cache_key = f'api:equipment:detail:{equip_id}'
        cached_data = redis_client.get(cache_key)
        if cached_data is not None:
            return success(data=cached_data, msg='查询成功')
        
        # 查询设备
        equipment = equipment_service.get_equipment_by_id(equip_id)
        
        # 序列化
        data = equipment_schema.dump(equipment)
        
        # 存入缓存（10分钟过期）
        redis_client.set(cache_key, data, ex=600)
        
        return success(data=data, msg='查询成功')
    except NotFoundError as e:
        return fail(code=404, msg=e.message)
    except Exception as e:
        return fail(code=500, msg=f'查询失败: {str(e)}')



