"""
Redis 客户端工具类
提供 Redis 连接和常用操作方法
"""
import json
from typing import Any, Optional, Union
from redis import Redis, ConnectionPool
from flask import current_app


class RedisClient:
    """Redis 客户端封装类"""
    
    def __init__(self, app=None):
        self.redis_client: Optional[Redis] = None
        self.pool: Optional[ConnectionPool] = None
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """初始化 Redis 连接"""
        config = app.config
        
        # 创建连接池
        self.pool = ConnectionPool(
            host=config.get('REDIS_HOST', 'localhost'),
            port=config.get('REDIS_PORT', 6379),
            password=config.get('REDIS_PASSWORD'),
            db=config.get('REDIS_DB', 0),
            decode_responses=config.get('REDIS_DECODE_RESPONSES', True),
            socket_timeout=config.get('REDIS_SOCKET_TIMEOUT', 5),
            socket_connect_timeout=config.get('REDIS_SOCKET_CONNECT_TIMEOUT', 5),
            max_connections=50
        )
        
        # 创建 Redis 客户端
        self.redis_client = Redis(connection_pool=self.pool)
        
        # 测试连接
        try:
            self.redis_client.ping()
            app.logger.info('Redis 连接成功')
        except Exception as e:
            app.logger.error(f'Redis 连接失败: {e}')
    
    def get_client(self) -> Redis:
        """获取 Redis 客户端实例"""
        if self.redis_client is None:
            raise RuntimeError('Redis 未初始化，请先调用 init_app()')
        return self.redis_client
    
    # ========== 基础操作 ==========
    
    def set(self, key: str, value: Any, ex: Optional[int] = None) -> bool:
        """
        设置键值对
        
        Args:
            key: 键名
            value: 值（会自动序列化）
            ex: 过期时间（秒）
        
        Returns:
            bool: 是否设置成功
        """
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value, ensure_ascii=False)
            return self.redis_client.set(key, value, ex=ex)
        except Exception as e:
            current_app.logger.error(f'Redis set 失败: {e}')
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取键值
        
        Args:
            key: 键名
            default: 默认值
        
        Returns:
            值（会自动反序列化）
        """
        try:
            value = self.redis_client.get(key)
            if value is None:
                return default
            
            # 尝试解析 JSON
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return value
        except Exception as e:
            current_app.logger.error(f'Redis get 失败: {e}')
            return default
    
    def delete(self, *keys: str) -> int:
        """
        删除键
        
        Args:
            *keys: 要删除的键名
        
        Returns:
            int: 删除的键数量
        """
        try:
            return self.redis_client.delete(*keys)
        except Exception as e:
            current_app.logger.error(f'Redis delete 失败: {e}')
            return 0
    
    def exists(self, key: str) -> bool:
        """检查键是否存在"""
        try:
            return bool(self.redis_client.exists(key))
        except Exception as e:
            current_app.logger.error(f'Redis exists 失败: {e}')
            return False
    
    def expire(self, key: str, time: int) -> bool:
        """设置键的过期时间"""
        try:
            return self.redis_client.expire(key, time)
        except Exception as e:
            current_app.logger.error(f'Redis expire 失败: {e}')
            return False
    
    # ========== 缓存装饰器 ==========
    
    def cache(self, timeout: int = 300, key_prefix: str = 'cache:'):
        """
        缓存装饰器
        
        Args:
            timeout: 缓存过期时间（秒）
            key_prefix: 键前缀
        
        Usage:
            @redis_client.cache(timeout=600)
            def get_lab_list():
                return Lab.query.all()
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                # 生成缓存键
                cache_key = f"{key_prefix}{func.__name__}:{str(args)}:{str(kwargs)}"
                
                # 尝试从缓存获取
                cached_value = self.get(cache_key)
                if cached_value is not None:
                    return cached_value
                
                # 执行函数并缓存结果
                result = func(*args, **kwargs)
                self.set(cache_key, result, ex=timeout)
                return result
            
            wrapper.__name__ = func.__name__
            return wrapper
        return decorator
    
    # ========== 哈希操作 ==========
    
    def hset(self, name: str, key: str, value: Any) -> int:
        """设置哈希字段"""
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value, ensure_ascii=False)
            return self.redis_client.hset(name, key, value)
        except Exception as e:
            current_app.logger.error(f'Redis hset 失败: {e}')
            return 0
    
    def hget(self, name: str, key: str, default: Any = None) -> Any:
        """获取哈希字段"""
        try:
            value = self.redis_client.hget(name, key)
            if value is None:
                return default
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return value
        except Exception as e:
            current_app.logger.error(f'Redis hget 失败: {e}')
            return default
    
    def hgetall(self, name: str) -> dict:
        """获取所有哈希字段"""
        try:
            return self.redis_client.hgetall(name)
        except Exception as e:
            current_app.logger.error(f'Redis hgetall 失败: {e}')
            return {}
    
    # ========== 列表操作 ==========
    
    def lpush(self, name: str, *values: Any) -> int:
        """从左侧推入列表"""
        try:
            serialized_values = [
                json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v
                for v in values
            ]
            return self.redis_client.lpush(name, *serialized_values)
        except Exception as e:
            current_app.logger.error(f'Redis lpush 失败: {e}')
            return 0
    
    def rpush(self, name: str, *values: Any) -> int:
        """从右侧推入列表"""
        try:
            serialized_values = [
                json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v
                for v in values
            ]
            return self.redis_client.rpush(name, *serialized_values)
        except Exception as e:
            current_app.logger.error(f'Redis rpush 失败: {e}')
            return 0
    
    def lrange(self, name: str, start: int = 0, end: int = -1) -> list:
        """获取列表范围"""
        try:
            return self.redis_client.lrange(name, start, end)
        except Exception as e:
            current_app.logger.error(f'Redis lrange 失败: {e}')
            return []


# 创建全局 Redis 客户端实例
redis_client = RedisClient()