"""
项目配置文件
支持从环境变量读取配置，适用于开发、测试和生产环境
"""
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()


class Config:
    """基础配置类"""
    # Flask 基础配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # SQLAlchemy 配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO', 'False').lower() == 'true'
    
    # TiDB Cloud 数据库配置
    # URL 格式: mysql+pymysql://user:password@host:4000/db_name?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '4000')
    DB_NAME = os.getenv('DB_NAME', 'instrument_booking')
    
    # 构建数据库 URI
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'SQLALCHEMY_DATABASE_URI',
        f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4'
    )
    
    # TiDB Cloud SSL 连接配置
    # 构建 SSL 配置
    _ssl_verify_cert = os.getenv('SSL_VERIFY_CERT', 'True').lower() == 'true'
    _connect_args = {}
    if _ssl_verify_cert:
        _ssl_config = {
            'ssl_verify_cert': True,
            'ssl_verify_identity': os.getenv('SSL_VERIFY_IDENTITY', 'True').lower() == 'true'
        }
        # 如果提供了 SSL CA 证书路径，则添加
        _ssl_ca = os.getenv('SSL_CA', None)
        if _ssl_ca:
            _ssl_config['ssl_ca'] = _ssl_ca
        _connect_args['ssl'] = _ssl_config
    
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'connect_args': _connect_args
    }
    
    # Flask-Migrate 配置
    MIGRATE_DIRECTORY = os.getenv('MIGRATE_DIRECTORY', 'migrations')
    
    # API 文档配置 (Flasgger/Swagger)
    SWAGGER = {
        'title': '高校仪器预约系统 API',
        'uiversion': 3,
        'version': '1.0.0',
        'description': '高校仪器预约系统后端 API 文档',
        'termsOfService': '',
        'tags': [
            {
                'name': '用户管理',
                'description': '用户相关的 API'
            },
            {
                'name': '仪器管理',
                'description': '仪器相关的 API'
            },
            {
                'name': '预约管理',
                'description': '预约相关的 API'
            }
        ]
    }

    # Redis 配置
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)
    REDIS_DB = int(os.getenv('REDIS_DB', 0))
    REDIS_DECODE_RESPONSES = True  # 自动解码响应为字符串
    
    # Redis 连接池配置
    REDIS_SOCKET_TIMEOUT = int(os.getenv('REDIS_SOCKET_TIMEOUT', 5))
    REDIS_SOCKET_CONNECT_TIMEOUT = int(os.getenv('REDIS_SOCKET_CONNECT_TIMEOUT', 5))
    
    # Redis 缓存配置
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = REDIS_HOST
    CACHE_REDIS_PORT = REDIS_PORT
    CACHE_REDIS_PASSWORD = REDIS_PASSWORD
    CACHE_REDIS_DB = REDIS_DB
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', 300))  # 默认5分钟


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'TEST_DATABASE_URI',
        'sqlite:///:memory:'
    )


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    SQLALCHEMY_ECHO = False


# 配置字典，便于根据环境变量选择配置
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

