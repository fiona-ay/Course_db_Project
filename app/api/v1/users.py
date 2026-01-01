"""
用户 API 路由
处理用户信息相关功能
"""
from flask import Blueprint
from flasgger import swag_from
from app.utils.auth import login_required, get_current_user, get_user_by_id
from app.utils.response import success, fail
from app.utils.exceptions import NotFoundError

# 创建蓝图
users_bp = Blueprint('users', __name__)


@users_bp.route('/me', methods=['GET'])
@login_required
@swag_from({
    'tags': ['用户管理'],
    'summary': '获取当前登录用户详细信息',
    'description': '获取当前登录用户的详细信息，包含实验室ID等信息',
    'security': [{'Bearer': []}],
    'responses': {
        200: {
            'description': '成功返回用户信息',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 200},
                    'msg': {'type': 'string', 'example': 'success'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'string', 'example': '2021001'},
                            'name': {'type': 'string', 'example': '张三'},
                            'user_type': {'type': 'string', 'example': 'student'},
                            'lab_id': {'type': 'integer', 'example': 1},
                            'lab_name': {'type': 'string', 'example': '计算机实验室'}
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
def get_current_user_info():
    """获取当前登录用户详细信息"""
    try:
        current_user = get_current_user()
        user_id = current_user.get('user_id')
        user_type = current_user.get('user_type')
        
        # 获取用户对象
        user = get_user_by_id(user_id, user_type)
        if not user:
            raise NotFoundError('用户不存在')
        
        # 构建用户信息
        user_data = user.to_dict()
        user_data['user_type'] = user_type
        
        # 如果是学生，添加实验室名称
        if user_type == 'student' and hasattr(user, 'lab_name'):
            user_data['lab_name'] = user.lab_name
        
        return success(data=user_data, msg='获取成功')
        
    except NotFoundError as e:
        return fail(code=404, msg=e.message)
    except Exception as e:
        return fail(code=500, msg=f'获取用户信息失败: {str(e)}')

