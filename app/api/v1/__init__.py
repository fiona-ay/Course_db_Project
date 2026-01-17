# """
# API v1 版本蓝图
# """
# from flask import Blueprint
# from app.api.v1 import reservation
# api_v1 = Blueprint('api_v1', __name__)

# # 导入并注册路由蓝图
# from app.api.v1 import laboratory, auth, users, equipment, admin

# # 注册路由蓝图
# api_v1.register_blueprint(laboratory.lab_bp, url_prefix='/laboratories')
# api_v1.register_blueprint(auth.auth_bp, url_prefix='/auth')
# api_v1.register_blueprint(users.users_bp, url_prefix='/users')
# api_v1.register_blueprint(equipment.equipment_bp, url_prefix='/equipments')
# api_v1.register_blueprint(admin.admin_bp, url_prefix='/admin')
# api_v1.register_blueprint(reservation.reservation_bp, url_prefix='/reservations')

# @api_v1.route('/health', methods=['GET'])
# def health_check():
#     """健康检查端点"""
#     return {'status': 'ok', 'version': '1.0.0'}, 200
"""
API v1 版本蓝图
"""
from flask import Blueprint

api_v1 = Blueprint('api_v1', __name__)

# 延迟导入路由蓝图，避免循环导入
# 注意：这里只导入蓝图对象，不执行路由函数
from app.api.v1.laboratory import lab_bp
from app.api.v1.auth import auth_bp
from app.api.v1.users import users_bp
from app.api.v1.equipment import equipment_bp
from app.api.v1.admin import admin_bp
from app.api.v1.reservation import reservation_bp

# 注册路由蓝图
api_v1.register_blueprint(lab_bp, url_prefix='/laboratories')
api_v1.register_blueprint(auth_bp, url_prefix='/auth')
api_v1.register_blueprint(users_bp, url_prefix='/users')
api_v1.register_blueprint(equipment_bp, url_prefix='/equipments')
api_v1.register_blueprint(admin_bp, url_prefix='/admin')
api_v1.register_blueprint(reservation_bp, url_prefix='/reservations')

@api_v1.route('/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return {'status': 'ok', 'version': '1.0.0'}, 200
