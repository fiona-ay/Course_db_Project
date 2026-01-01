"""
认证 API 路由
处理用户登录、注册等认证相关功能
"""
from flask import Blueprint, request
from flasgger import swag_from
from werkzeug.security import check_password_hash
from app.utils.auth import generate_token, get_user_by_id
from app.utils.response import success, fail
from app.utils.exceptions import UnauthorizedError, ValidationError

# 创建蓝图
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
@swag_from({
    'tags': ['认证管理'],
    'summary': '用户登录',
    'description': '用户登录，返回 JWT token 和用户信息',
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'required': ['username', 'password', 'user_type'],
            'properties': {
                'username': {
                    'type': 'string',
                    'example': '2021001',
                    'description': '学号/工号'
                },
                'password': {
                    'type': 'string',
                    'example': '123456',
                    'description': '密码（使用Hash加密存储）'
                },
                'user_type': {
                    'type': 'string',
                    'enum': ['student', 'teacher', 'admin'],
                    'example': 'student',
                    'description': '用户类型'
                }
            }
        }
    }],
    'responses': {
        200: {
            'description': '登录成功',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 200},
                    'msg': {'type': 'string', 'example': '登录成功'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'token': {'type': 'string', 'example': 'eyJ0eXAiOiJKV1QiLCJhbGc...'},
                            'user': {
                                'type': 'object',
                                'properties': {
                                    'id': {'type': 'string', 'example': '2021001'},
                                    'name': {'type': 'string', 'example': '张三'},
                                    'user_type': {'type': 'string', 'example': 'student'},
                                    'lab_id': {'type': 'integer', 'example': 1}
                                }
                            }
                        }
                    }
                }
            }
        },
        401: {
            'description': '登录失败'
        }
    }
})
def login():
    """用户登录"""
    try:
        json_data = request.get_json()
        if not json_data:
            return fail(code=400, msg='请求体不能为空')
        
        username = json_data.get('username')
        password = json_data.get('password')
        user_type = json_data.get('user_type')
        
        if not all([username, password, user_type]):
            return fail(code=400, msg='缺少必要参数：username, password, user_type')
        
        if user_type not in ['student', 'teacher', 'admin']:
            return fail(code=400, msg='user_type 必须是 student, teacher 或 admin')
        
        # 根据用户类型查询用户
        user = get_user_by_id(username, user_type)
        if not user:
            raise UnauthorizedError('用户名或密码错误')
        
        # 验证密码Hash
        if not hasattr(user, 'password_hash') or not user.password_hash:
            raise UnauthorizedError('用户密码未设置')
        
        if not check_password_hash(user.password_hash, password):
            raise UnauthorizedError('用户名或密码错误')
        
        # 获取实验室ID
        lab_id = None
        if hasattr(user, 'lab_id'):
            lab_id = user.lab_id
        elif hasattr(user, 'manage_scope'):
            lab_id = user.manage_scope
        
        # 生成 token
        token = generate_token(username, user_type, lab_id)
        
        # 返回用户信息
        user_data = {
            'id': user.id,
            'name': user.name,
            'user_type': user_type,
            'lab_id': lab_id
        }
        
        # 如果是学生或教师，添加额外信息
        if user_type in ['student', 'teacher']:
            if hasattr(user, 'dept'):
                user_data['dept'] = user.dept
            if user_type == 'student' and hasattr(user, 't_id'):
                user_data['t_id'] = user.t_id
        
        return success(data={
            'token': token,
            'user': user_data
        }, msg='登录成功')
        
    except (UnauthorizedError, ValidationError) as e:
        return fail(code=e.status_code, msg=e.message)
    except Exception as e:
        return fail(code=500, msg=f'登录失败: {str(e)}')

