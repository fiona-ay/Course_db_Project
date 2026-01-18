"""
API v1 版本蓝图
"""
from flask import Blueprint

api_v1 = Blueprint('api_v1', __name__)

# 导入并注册路由蓝图
from app.api.v1 import laboratory, auth, users, equipment, admin, timeslot

# 注册路由蓝图
api_v1.register_blueprint(laboratory.lab_bp, url_prefix='/laboratories')
api_v1.register_blueprint(auth.auth_bp, url_prefix='/auth')
api_v1.register_blueprint(users.users_bp, url_prefix='/users')
api_v1.register_blueprint(equipment.equipment_bp, url_prefix='/equipments')
api_v1.register_blueprint(admin.admin_bp, url_prefix='/admin')
api_v1.register_blueprint(timeslot.timeslot_bp, url_prefix='/timeslots')


@api_v1.route('/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return {'status': 'ok', 'version': '1.0.0'}, 200
