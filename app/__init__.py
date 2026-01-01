"""
Flask Application Factory
使用工厂模式创建 Flask 应用实例
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger
from flask_cors import CORS

from config import config
from app.utils.redis_client import redis_client

# 初始化扩展（但不绑定到特定应用）
db = SQLAlchemy()
migrate = Migrate()
swagger = Swagger()


def create_app(config_name='default'):
    """
    应用工厂函数
    
    Args:
        config_name: 配置名称，可选值: 'development', 'testing', 'production', 'default'
    
    Returns:
        Flask 应用实例
    """
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)

    # 配置 CORS（允许跨域请求）
    CORS(app, 
         resources={r"/api/*": {
             "origins": "*",
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"],
             "expose_headers": ["Content-Type"]
         }})

    # 初始化 Redis
    redis_client.init_app(app)
    
    # 初始化 Flasgger（配置已在 config 中设置）
    swagger.init_app(app)
    
    # 导入模型（让 Flask-Migrate 能够检测到表结构）
    from app import models
    
    # 注册蓝图
    from app.api.v1 import api_v1
    app.register_blueprint(api_v1, url_prefix='/api/v1')
    
    # 注册错误处理器
    from app.utils.exceptions import register_error_handlers
    register_error_handlers(app)
    
    # 注册CLI命令
    from app.commands.seed import register_commands
    register_commands(app)
    
    # 创建数据库表（仅用于开发环境）
    with app.app_context():
        # 注意：生产环境应该使用 Flask-Migrate 进行数据库迁移
        # db.create_all()
        pass
    
    return app

