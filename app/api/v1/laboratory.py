"""
实验室 API 路由
实现实验室的 RESTful API
"""
from flask import Blueprint, request
from flasgger import swag_from

from app.services import lab_service
from app.api.v1.schemas.lab_schema import (
    LaboratorySchema, LaboratoryCreateSchema, LaboratoryUpdateSchema
)
from app.utils.response import success, fail
from app.utils.exceptions import NotFoundError, ValidationError
from app.utils.redis_client import redis_client

# 创建蓝图
lab_bp = Blueprint('laboratory', __name__)

# 实例化 Schema（用于序列化和验证）
lab_schema = LaboratorySchema()
lab_create_schema = LaboratoryCreateSchema()
lab_update_schema = LaboratoryUpdateSchema()


@lab_bp.route('/', methods=['GET'])
@swag_from({
    'tags': ['实验室管理'],
    'summary': '获取实验室列表',
    'description': '获取所有实验室的列表',
    'responses': {
        200: {
            'description': '成功返回实验室列表',
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
                                'name': {'type': 'string', 'example': '计算机实验室'},
                                'location': {'type': 'string', 'example': '教学楼A101'}
                            }
                        }
                    }
                }
            }
        }
    }
})
def get_labs():
    """获取所有实验室（带缓存）"""
    try:
        # 尝试从缓存获取序列化后的数据
        cache_key = 'api:lab:list'
        cached_data = redis_client.get(cache_key)
        if cached_data is not None:
            # 缓存命中，直接返回（完全跳过数据库查询和序列化）
            return success(data=cached_data, msg='查询成功')
        
        # 缓存未命中，查询数据库并序列化
        labs = lab_service.get_lab_list()
        data = lab_schema.dump(labs, many=True)
        
        # 存入缓存（10分钟过期）
        redis_client.set(cache_key, data, ex=600)
        
        return success(data=data, msg='查询成功')
    except Exception as e:
        return fail(code=500, msg=f'查询失败: {str(e)}')


@lab_bp.route('/', methods=['POST'])
@swag_from({
    'tags': ['实验室管理'],
    'summary': '创建实验室',
    'description': '创建一个新的实验室',
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'required': ['name'],
            'properties': {
                'name': {'type': 'string', 'example': '计算机实验室', 'description': '实验室名称'},
                'location': {'type': 'string', 'example': '教学楼A101', 'description': '实验室位置'}
            }
        }
    }],
    'responses': {
        200: {
            'description': '成功创建实验室',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 200},
                    'msg': {'type': 'string', 'example': 'success'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'name': {'type': 'string', 'example': '计算机实验室'},
                            'location': {'type': 'string', 'example': '教学楼A101'}
                        }
                    }
                }
            }
        },
        422: {
            'description': '数据验证失败'
        }
    }
})
def create_lab():
    """创建实验室"""
    try:
        # 验证请求数据
        json_data = request.get_json()
        if not json_data:
            return fail(code=400, msg='请求体不能为空')
        
        # 使用 Schema 验证数据
        errors = lab_create_schema.validate(json_data)
        if errors:
            return fail(code=422, msg='数据验证失败', data=errors)
        
        validated_data = lab_create_schema.load(json_data)
        
        # 调用 Service 层创建实验室
        lab = lab_service.create_lab(validated_data)
        
        # 清除相关缓存
        redis_client.delete('api:lab:list')
        
        # 序列化返回
        data = lab_schema.dump(lab)
        return success(data=data, msg='创建成功')
    except ValidationError as e:
        return fail(code=422, msg=e.message, data=e.payload)
    except Exception as e:
        return fail(code=500, msg=f'创建失败: {str(e)}')


@lab_bp.route('/<int:lab_id>', methods=['PUT'])
@swag_from({
    'tags': ['实验室管理'],
    'summary': '更新实验室',
    'description': '更新指定实验室的信息（会同步更新学生表中的冗余字段）',
    'parameters': [
        {
            'in': 'path',
            'name': 'lab_id',
            'type': 'integer',
            'required': True,
            'description': '实验室ID'
        },
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'example': '计算机实验室', 'description': '实验室名称'},
                    'location': {'type': 'string', 'example': '教学楼A101', 'description': '实验室位置'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': '成功更新实验室',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 200},
                    'msg': {'type': 'string', 'example': 'success'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'name': {'type': 'string', 'example': '计算机实验室'},
                            'location': {'type': 'string', 'example': '教学楼A101'}
                        }
                    }
                }
            }
        },
        404: {
            'description': '实验室不存在'
        },
        422: {
            'description': '数据验证失败'
        }
    }
})
def update_lab(lab_id):
    """更新实验室"""
    try:
        # 验证请求数据
        json_data = request.get_json()
        if not json_data:
            return fail(code=400, msg='请求体不能为空')
        
        # 使用 Schema 验证数据
        errors = lab_update_schema.validate(json_data)
        if errors:
            return fail(code=422, msg='数据验证失败', data=errors)
        
        validated_data = lab_update_schema.load(json_data)
        
        # 调用 Service 层更新实验室（会自动更新学生表的冗余字段）
        lab = lab_service.update_lab(lab_id, validated_data)
        
        # 清除相关缓存
        redis_client.delete('api:lab:list')
        redis_client.delete(f'api:lab:detail:{lab_id}')
        
        # 序列化返回
        data = lab_schema.dump(lab)
        return success(data=data, msg='更新成功')
    except NotFoundError as e:
        return fail(code=404, msg=e.message)
    except ValidationError as e:
        return fail(code=422, msg=e.message, data=e.payload)
    except Exception as e:
        return fail(code=500, msg=f'更新失败: {str(e)}')


@lab_bp.route('/<int:lab_id>', methods=['DELETE'])
@swag_from({
    'tags': ['实验室管理'],
    'summary': '删除实验室',
    'description': '删除指定的实验室',
    'parameters': [{
        'in': 'path',
        'name': 'lab_id',
        'type': 'integer',
        'required': True,
        'description': '实验室ID'
    }],
    'responses': {
        200: {
            'description': '成功删除实验室',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 200},
                    'msg': {'type': 'string', 'example': '删除成功'}
                }
            }
        },
        404: {
            'description': '实验室不存在'
        },
        422: {
            'description': '删除失败（如存在关联数据）'
        }
    }
})
def delete_lab(lab_id):
    """删除实验室"""
    try:
        lab_service.delete_lab(lab_id)
        
        # 清除相关缓存
        redis_client.delete('api:lab:list')
        redis_client.delete(f'api:lab:detail:{lab_id}')
        
        return success(msg='删除成功')
    except NotFoundError as e:
        return fail(code=404, msg=e.message)
    except ValidationError as e:
        return fail(code=422, msg=e.message, data=e.payload)
    except Exception as e:
        return fail(code=500, msg=f'删除失败: {str(e)}')

