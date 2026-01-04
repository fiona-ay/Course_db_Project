# 高校大型仪器设备共享服务平台

一个基于 Flask + Vue 3 的前后端分离的高校仪器设备预约管理系统，为师生提供便捷、高效的仪器设备预约服务。

## 项目简介

此为HNU数据库系统大作业项目，由七人小组共同开发。在未来希望将本系统开发为一个完整的仪器设备预约管理平台，支持学生、教师和管理员三种角色，提供实验室管理、设备管理、预约管理、用户管理等功能。系统采用前后端分离架构，后端提供 RESTful API，前端使用现代化的 Vue 3 框架构建用户界面。

## 技术栈

### 后端

- **Web 框架**: Flask 3.0.0
- **ORM**: Flask-SQLAlchemy 3.1.1
- **数据库迁移**: Flask-Migrate 4.0.5
- **序列化**: Marshmallow 3.20.1 / Flask-Marshmallow 0.15.0
- **API 文档**: Flasgger 0.9.7.1 (Swagger UI)
- **数据库**: MySQL (TiDB Cloud Serverless)
- **数据库驱动**: PyMySQL 1.1.0
- **缓存**: Redis 5.0.1
- **认证**: PyJWT 2.8.0 (JWT Token)
- **跨域**: Flask-CORS 4.0.0
- **环境变量管理**: python-dotenv 1.0.0

### 前端

- **框架**: Vue 3.4.15
- **路由**: Vue Router 4.2.5
- **状态管理**: Pinia 2.1.7
- **UI 组件库**: Element Plus 2.5.6
- **HTTP 客户端**: Axios 1.6.5
- **构建工具**: Vite 5.0.11
- **样式预处理**: Sass 1.69.5
- **动画库**: Animate.css 4.1.1
- **图标库**: @element-plus/icons-vue 2.3.1

## 项目结构

```
.
├── app/                    # 后端应用核心代码
│   ├── __init__.py        # Application Factory
│   ├── models/            # 数据库模型
│   │   ├── laboratory.py  # 实验室模型
│   │   ├── equipment.py   # 设备模型
│   │   ├── student.py     # 学生模型
│   │   ├── teacher.py     # 教师模型
│   │   ├── admin.py       # 管理员模型
│   │   ├── reservation.py # 预约模型
│   │   ├── timeslot.py    # 时间段模型
│   │   ├── auditlog.py    # 审计日志模型
│   │   └── mixins.py      # 模型混入类
│   ├── api/               # API 蓝图
│   │   └── v1/           # API v1 版本
│   │       ├── __init__.py    # API 蓝图注册
│   │       ├── laboratory.py  # 实验室 API
│   │       ├── equipment.py   # 设备 API（读写分离）
│   │       ├── auth.py        # 认证 API
│   │       ├── users.py       # 用户信息 API
│   │       ├── admin.py       # 管理员 API
│   │       └── schemas/       # API 序列化模式
│   ├── services/          # 业务逻辑层
│   │   ├── lab_service.py # 实验室服务
│   │   └── equipment_service.py # 设备服务
│   ├── utils/             # 工具类
│   │   ├── response.py    # 统一响应格式
│   │   ├── exceptions.py # 异常处理
│   │   ├── schemas.py     # 通用模式
│   │   ├── auth.py        # JWT 认证工具
│   │   └── redis_client.py # Redis 客户端
│   └── commands/          # Flask CLI 命令
│       └── seed.py        # 数据初始化命令
├── frontend/              # 前端应用
│   ├── src/
│   │   ├── api/          # API 请求封装
│   │   │   ├── request.js    # Axios 实例配置
│   │   │   ├── auth.js       # 认证 API
│   │   │   ├── users.js      # 用户 API
│   │   │   ├── equipment.js  # 设备 API
│   │   │   └── laboratory.js # 实验室 API
│   │   ├── components/   # Vue 组件
│   │   ├── views/        # 页面视图
│   │   │   ├── Home.vue      # 首页（含登录）
│   │   │   ├── Equipment.vue # 设备列表
│   │   │   └── EquipmentDetail.vue # 设备详情
│   │   ├── stores/       # Pinia 状态管理
│   │   │   └── user.js       # 用户状态
│   │   ├── router/       # 路由配置
│   │   ├── assets/       # 静态资源
│   │   └── App.vue       # 根组件
│   ├── package.json      # 前端依赖
│   └── vite.config.js    # Vite 配置
├── migrations/            # 数据库迁移文件
├── config.py              # 后端配置文件
├── run.py                 # 后端启动入口
├── requirements.txt       # 后端依赖包
├── env.example           # 环境变量示例
└── README.md             # 项目说明
```

## 功能模块

### 核心功能

- **用户认证**: JWT Token 认证、用户登录、权限管理
- **实验室管理**: 实验室信息管理、实验室列表查询（带缓存）
- **设备管理**: 设备信息管理、设备状态跟踪、读写分离（普通用户读，管理员写）
- **预约管理**: 设备预约申请、预约审批、预约查询（待实现）
- **用户管理**: 学生、教师、管理员三种角色管理
- **时间段管理**: 设备可用时间段配置（待实现）
- **审计日志**: 操作记录追踪（待实现）
- **缓存机制**: Redis 缓存，提升 API 响应速度

### 用户角色

- **学生**: 查看设备信息、提交预约申请、查看预约状态
- **教师**: 查看设备信息、提交预约申请、查看预约状态
- **管理员**: 实验室管理、设备管理（增删改）、预约审批、用户管理

### 认证与授权

- **JWT Token**: 使用 JWT 进行用户认证
- **登录验证**: `@login_required` 装饰器，要求用户登录
- **管理员权限**: `@admin_required` 装饰器，要求管理员权限
- **密码加密**: 使用 `werkzeug.security` 进行密码哈希存储

## 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- MySQL 或 TiDB Cloud
- Redis 5.0+ (用于缓存)

### 后端启动

#### 1. 安装依赖

```bash
pip install -r requirements.txt
```

#### 2. 配置环境变量

复制 `env.example` 为 `.env` 并填写配置：

```bash
# Windows
copy env.example .env

# Linux/Mac
cp env.example .env
```

编辑 `.env` 文件，配置数据库连接信息（具体配置见doc目录下开发说明书）：

```env
# Flask 环境配置
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# Flask 密钥（生产环境请务必修改）
SECRET_KEY=your-secret-key-here

# TiDB Cloud 数据库配置
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=your_tidb_host
DB_PORT=4000
DB_NAME=instrument_booking

# SSL 配置（TiDB Cloud 需要）
SSL_VERIFY_CERT=True
SSL_VERIFY_IDENTITY=True

# Redis 配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0
```

#### 3. 运行后端服务

```bash
python run.py
```

或使用 Flask CLI：

```bash
flask run
```

后端服务将在 `http://localhost:5000` 启动。

#### 4. 访问 API 文档

启动应用后，访问 Swagger UI 文档：

```
http://localhost:5000/apidocs
```

### 前端启动

#### 1. 安装依赖

```bash
cd frontend
npm install
```

#### 2. 配置 API 地址

编辑 `frontend/src/api/request.js`，配置后端 API 地址（默认已配置为 `http://localhost:5000/api/v1`）。

**注意**: 如果使用 Vite 代理，可以保持 `baseURL` 为相对路径 `/api/v1`，Vite 会自动代理到后端。

#### 3. 启动开发服务器

```bash
npm run dev
```

前端应用将在 `http://localhost:3000` 启动（Vite 配置的端口）。

#### 4. 构建生产版本

```bash
npm run build
```

构建产物将输出到 `frontend/dist` 目录。

> 记得开启redis，否则无法使用。需要在本地下载redis并运行redis-server.exe

## 环境变量说明

### 后端环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `FLASK_ENV` | Flask 环境 (development/testing/production) | development |
| `FLASK_DEBUG` | 是否开启调试模式 | True |
| `FLASK_HOST` | 监听地址 | 0.0.0.0 |
| `FLASK_PORT` | 监听端口 | 5000 |
| `SECRET_KEY` | Flask 密钥 | dev-secret-key-change-in-production |
| `DB_USER` | 数据库用户名 | root |
| `DB_PASSWORD` | 数据库密码 | - |
| `DB_HOST` | 数据库主机 | localhost |
| `DB_PORT` | 数据库端口 | 4000 |
| `DB_NAME` | 数据库名称 | instrument_booking |
| `SQLALCHEMY_DATABASE_URI` | 数据库连接 URI（可选，覆盖单独配置） | - |
| `SQLALCHEMY_ECHO` | 是否打印 SQL 语句 | False |
| `SSL_VERIFY_CERT` | 是否验证 SSL 证书 | True |
| `SSL_VERIFY_IDENTITY` | 是否验证 SSL 身份 | True |
| `SSL_CA` | SSL CA 证书路径（可选） | - |
| `MIGRATE_DIRECTORY` | 迁移文件目录 | migrations |
| `REDIS_HOST` | Redis 主机地址 | localhost |
| `REDIS_PORT` | Redis 端口 | 6379 |
| `REDIS_PASSWORD` | Redis 密码（可选） | - |
| `REDIS_DB` | Redis 数据库编号 | 0 |

## 数据库模型

### 核心模型

- **Laboratory**: 实验室信息
- **Equipment**: 设备信息
- **Student**: 学生信息
- **Teacher**: 教师信息
- **Admin**: 管理员信息
- **Reservation**: 预约记录
- **TimeSlot**: 时间段配置
- **AuditLog**: 审计日志

所有模型都继承自 `ToDictMixin`，提供统一的序列化方法。

## 开发规范

### Application Factory 模式

项目采用 Flask Application Factory 模式，所有扩展都在 `create_app()` 函数中初始化，便于测试和部署。

### 目录说明

- **models/**: 数据库模型定义，使用 SQLAlchemy ORM
- **api/v1/**: API 路由，按版本组织，使用 Flask Blueprint
- **services/**: 业务逻辑层，处理复杂业务逻辑，与数据库操作分离
- **utils/**: 工具类，包括统一响应格式、异常处理、通用模式等

### 统一响应格式

使用 `app/utils/response.py` 中的工具函数：

```python
from app.utils.response import success, fail

# 成功响应
return success(data={...}, msg='操作成功')

# 错误响应
return fail(code=400, msg='操作失败')
```

所有 API 响应格式统一为：
```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {...}
}
```

### 异常处理

使用 `app/utils/exceptions.py` 中定义的异常类：

```python
from app.utils.exceptions import ValidationError, NotFoundError

raise ValidationError('数据验证失败', errors={...})
raise NotFoundError('资源未找到')
```

### API 版本管理

API 按版本组织在 `app/api/v1/` 目录下，便于后续版本升级和维护。

### 认证与授权

使用 `app/utils/auth.py` 中的装饰器：

```python
from app.utils.auth import login_required, admin_required

@login_required  # 要求登录
def get_equipments():
    ...

@admin_required  # 要求管理员权限
def create_equipment():
    ...
```

### 缓存机制

使用 Redis 缓存提升 API 性能，缓存策略：
- **实验室列表**: 10 分钟过期
- **设备列表**: 5 分钟过期（根据筛选条件）
- **设备详情**: 10 分钟过期
- **缓存失效**: 写操作（增删改）时自动清除相关缓存

```python
from app.utils.redis_client import redis_client

# 设置缓存
redis_client.set('key', data, ex=600)  # 10分钟过期

# 获取缓存
cached_data = redis_client.get('key')

# 删除缓存
redis_client.delete('key')
```

## 数据库迁移

```bash
# 创建迁移
flask db migrate -m "描述信息"

# 应用迁移
flask db upgrade

# 回滚迁移
flask db downgrade

# 查看迁移历史
flask db history
```

## API 接口

### 基础路径

所有 API 接口的基础路径为：`/api/v1`

### 认证接口

- `POST /api/v1/auth/login` - 用户登录（返回 JWT Token）
  - 请求体: `{ "username": "学号/工号", "password": "密码" }`
  - 响应: `{ "code": 200, "data": { "token": "...", "user": {...} } }`

### 用户接口

- `GET /api/v1/users/me` - 获取当前登录用户信息（需要登录）

### 实验室接口

- `GET /api/v1/laboratories/` - 获取实验室列表（带缓存）
- `GET /api/v1/laboratories/<id>` - 获取实验室详情
- `POST /api/v1/laboratories/` - 创建实验室
- `PUT /api/v1/laboratories/<id>` - 更新实验室
- `DELETE /api/v1/laboratories/<id>` - 删除实验室

### 设备接口（读写分离）

#### 普通用户（需要登录）

- `GET /api/v1/equipments/` - 获取设备列表（支持筛选：`lab_id`, `keyword`, `category`, `status`）
- `GET /api/v1/equipments/<id>` - 获取设备详情

#### 管理员（需要管理员权限）

- `POST /api/v1/admin/equipments` - 创建设备
- `PUT /api/v1/admin/equipments/<id>` - 更新设备
- `DELETE /api/v1/admin/equipments/<id>` - 删除设备

### 请求认证

所有需要认证的接口，请在请求头中添加：

```
Authorization: Bearer <JWT_TOKEN>
```

### 更多接口

完整 API 文档请查看 Swagger UI：`http://localhost:5000/apidocs`

## 前端路由

- `/` 或 `/home` - 首页（含登录功能）
- `/equipment` - 设备列表（需要登录）
- `/equipment/:id` - 设备详情（需要登录）
- `/reservations` - 预约管理（待实现）
- `/help` - 帮助中心（待实现）

### 路由保护

部分路由需要登录才能访问，未登录用户会被重定向到首页。

## 数据库索引优化

为了提高查询性能，项目在关键字段上创建了 B+ 树索引：

- **设备表**: `lab_id`, `status`, `category`, `name`, 复合索引 `(lab_id, status)`
- **预约表**: `equip_id`, `student_id`, `teacher_id`, `status`, `apply_time`, 复合索引 `(equip_id, status)`
- **学生表**: `lab_id`, `t_id`, 复合索引 `(lab_id, t_id)`
- **教师表**: `lab_id`
- **管理员表**: `lab_id`
- **时间段表**: `equip_id`, `is_active`, 复合索引 `(equip_id, is_active)`
- **审计日志表**: `operator_id`, `action_time`, `action_type`, 复合索引 `(operator_id, action_time)`

## 常见问题

### 1. 登录后立即被重定向回首页

**原因**: 可能是 URL 斜杠不一致导致的重定向问题。

**解决方案**: 
- 确保前端请求 URL 与后端路由匹配（都带斜杠或都不带）
- 检查浏览器 Network 面板，查看是否有 308 重定向

### 2. 401 Unauthorized 错误

**原因**: 
- Token 未正确发送（检查请求头中的 `Authorization`）
- Token 已过期
- Vite 代理未正确转发 `Authorization` header

**解决方案**:
- 检查 `frontend/src/api/request.js` 中的 token 设置
- 确认后端 CORS 配置允许 `Authorization` header
- 如果使用 Vite 代理，确保代理配置正确转发请求头

### 3. Redis 连接失败

**原因**: Redis 服务未启动或配置错误。

**解决方案**:
- 确保 Redis 服务正在运行
- 检查 `.env` 文件中的 Redis 配置
- 测试 Redis 连接: `redis-cli ping`

## 开发计划

- [x] 用户认证（JWT）
- [x] 设备管理（读写分离）
- [x] Redis 缓存
- [x] 数据库索引优化
- [ ] 预约管理功能
- [ ] 时间段管理
- [ ] 审计日志
- [ ] 前端预约页面
- [ ] 管理员后台

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
