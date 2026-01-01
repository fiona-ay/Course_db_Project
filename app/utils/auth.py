"""
JWT 认证工具类
提供 JWT token 生成、验证和用户认证功能
"""
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, current_app, g
from app.utils.exceptions import UnauthorizedError, ForbiddenError


def generate_token(user_id: str, user_type: str, lab_id: int = None) -> str:
    """
    生成 JWT token
    
    Args:
        user_id: 用户ID
        user_type: 用户类型 ('student', 'teacher', 'admin')
        lab_id: 实验室ID（可选）
    
    Returns:
        str: JWT token
    """
    payload = {
        'user_id': user_id,
        'user_type': user_type,
        'lab_id': lab_id,
        'exp': datetime.utcnow() + timedelta(days=7),  # 7天过期
        'iat': datetime.utcnow()
    }
    
    secret_key = current_app.config.get('SECRET_KEY', 'dev-secret-key')
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token


def verify_token(token: str) -> dict:
    """
    验证 JWT token
    
    Args:
        token: JWT token 字符串
    
    Returns:
        dict: token 载荷（payload）
    
    Raises:
        UnauthorizedError: token 无效或过期
    """
    try:
        secret_key = current_app.config.get('SECRET_KEY', 'dev-secret-key')
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise UnauthorizedError('Token 已过期')
    except jwt.InvalidTokenError:
        raise UnauthorizedError('Token 无效')


def get_current_user():
    """
    从 token 中获取当前用户信息
    
    Returns:
        dict: 用户信息，包含 user_id, user_type, lab_id
    """
    if not hasattr(g, 'current_user'):
        # 调试：打印所有请求头
        # Flask 的 request.headers 是大小写不敏感的，但为了兼容性，我们检查多种可能
        auth_header = (
            request.headers.get('Authorization', '') or 
            request.headers.get('authorization', '') or
            request.headers.get('AUTHORIZATION', '')
        )
        
        if not auth_header:
            # 调试：打印所有请求头，帮助排查
            print(f"[DEBUG] 请求头中没有 Authorization")
            print(f"[DEBUG] 所有请求头 keys: {list(request.headers.keys())}")
            print(f"[DEBUG] 所有请求头 (原始): {dict(request.headers)}")
            print(f"[DEBUG] Authorization (大写): {request.headers.get('Authorization', 'NOT FOUND')}")
            print(f"[DEBUG] authorization (小写): {request.headers.get('authorization', 'NOT FOUND')}")
            print(f"[DEBUG] 请求方法: {request.method}")
            print(f"[DEBUG] 请求 URL: {request.url}")
            raise UnauthorizedError('缺少认证 token')
        
        # 移除 'Bearer ' 前缀（如果存在）
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
        else:
            token = auth_header
        
        print(f"[DEBUG] 收到 token: {token[:20]}...")
        try:
            payload = verify_token(token)
            print(f"[DEBUG] Token 验证成功: {payload}")
            g.current_user = payload
        except Exception as e:
            print(f"[DEBUG] Token 验证失败: {str(e)}")
            raise
    
    return g.current_user


def login_required(f):
    """
    登录验证装饰器
    要求用户必须登录
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # OPTIONS 预检请求不需要验证
        if request.method == 'OPTIONS':
            return f(*args, **kwargs)
        
        try:
            get_current_user()
        except UnauthorizedError as e:
            from app.utils.response import fail
            return fail(code=401, msg=e.message)
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """
    管理员权限验证装饰器
    要求用户必须是管理员
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            user = get_current_user()
            if user.get('user_type') != 'admin':
                raise ForbiddenError('需要管理员权限')
        except (UnauthorizedError, ForbiddenError) as e:
            from app.utils.response import fail
            status_code = 401 if isinstance(e, UnauthorizedError) else 403
            return fail(code=status_code, msg=e.message)
        return f(*args, **kwargs)
    return decorated_function


def get_user_by_id(user_id: str, user_type: str):
    """
    根据用户ID和类型获取用户对象
    
    Args:
        user_id: 用户ID
        user_type: 用户类型 ('student', 'teacher', 'admin')
    
    Returns:
        Student, Teacher 或 Admin 对象
    """
    # 延迟导入，避免循环依赖
    from app.models.student import Student
    from app.models.teacher import Teacher
    from app.models.admin import Admin
    
    if user_type == 'student':
        return Student.query.get(user_id)
    elif user_type == 'teacher':
        return Teacher.query.get(user_id)
    elif user_type == 'admin':
        return Admin.query.get(user_id)
    return None

