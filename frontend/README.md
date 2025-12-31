# 高校仪器预约系统 - 前端项目 🎨

基于 Vue3 + Vite + Element Plus 的现代化、可爱活泼风格前端应用

## ✨ 设计特色

### 🎨 视觉效果
- **渐变背景**: 紫色到粉色的动态渐变背景，营造温馨氛围
- **毛玻璃效果**: 使用 backdrop-filter 实现现代化的毛玻璃卡片
- **浮动动画**: 背景装饰元素使用浮动动画，增加动态感
- **渐变文字**: 标题使用渐变色，更加醒目
- **柔和阴影**: 多层次的阴影系统，增强层次感

### 🎭 动画效果
- **页面过渡**: 流畅的页面切换动画
- **悬浮效果**: 卡片和按钮的悬浮交互效果
- **加载动画**: 优雅的加载状态提示
- **微交互**: 按钮点击、表单输入等细节动画

### 🎪 交互体验
- **圆角设计**: 统一的圆角设计语言，更加友好
- **响应式布局**: 完美适配各种屏幕尺寸
- **视觉反馈**: 每个操作都有明确的视觉反馈
- **友好提示**: 使用 Element Plus 的消息提示系统

## 🛠 技术栈

- **框架**: Vue 3.4
- **构建工具**: Vite 5.0
- **路由**: Vue Router 4.2
- **状态管理**: Pinia 2.1
- **UI 框架**: Element Plus 2.5
- **HTTP 客户端**: Axios 1.6
- **动画库**: Animate.css 4.1
- **工具库**: @vueuse/core 10.7

## 📦 项目结构

```
frontend/
├── src/
│   ├── api/                    # API 请求封装
│   │   ├── request.js          # Axios 封装和拦截器
│   │   └── laboratory.js       # 实验室 API
│   ├── assets/
│   │   └── styles/
│   │       └── global.css      # 全局样式（动画、主题色等）
│   ├── components/             # 公共组件
│   │   └── LoadingSpinner.vue  # 加载动画组件
│   ├── router/                 # 路由配置
│   │   └── index.js
│   ├── views/                  # 页面组件
│   │   ├── LaboratoryList.vue  # ✅ 实验室管理（完整实现）
│   │   ├── Equipment.vue       # ⏳ 设备管理（待实现）
│   │   └── Reservations.vue    # ⏳ 预约管理（待实现）
│   ├── App.vue                 # 根组件（导航栏）
│   └── main.js                 # 入口文件
├── index.html
├── package.json
├── vite.config.js
└── README.md
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd frontend
npm install
```

### 2. 启动后端服务

确保后端 Flask 应用已启动：

```bash
# 在项目根目录
python run.py
```

后端服务默认运行在 `http://localhost:5000`

### 3. 启动前端开发服务器

```bash
cd frontend
npm run dev
```

前端服务将在 `http://localhost:3000` 启动

## 🎯 功能说明

### ✅ 已实现功能

- **实验室管理**
  - ✨ 精美的列表展示（带动画效果）
  - ➕ 新增实验室（弹窗表单）
  - ✏️ 编辑实验室信息
  - 🗑️ 删除实验室（带确认提示）
  - 📊 实时数据加载
  - 🎨 优雅的空状态提示

### ⏳ 待实现功能

- 设备管理
- 预约管理
- 用户管理
- 更多动画效果...

## 🎨 设计系统

### 颜色主题

```css
/* 主色调 - 紫色渐变 */
--primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* 次要色 - 粉色渐变 */
--secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);

/* 成功色 - 蓝色渐变 */
--success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
```

### 动画效果

- **浮动动画** (float): 3s 循环，上下浮动
- **脉冲动画** (pulse): 2s 循环，缩放效果
- **滑动进入** (slideInUp): 从下往上滑入
- **页面过渡**: 0.4s 缓动过渡

### 圆角系统

- `--radius-sm`: 8px
- `--radius-md`: 12px
- `--radius-lg`: 16px
- `--radius-xl`: 24px

## 📝 开发说明

### API 请求

所有 API 请求都封装在 `src/api/` 目录下，使用统一的 `request.js` 进行 axios 封装。

后端 API 基础路径为 `/api/v1`，通过 Vite 的 proxy 配置代理到 `http://localhost:5000`。

### 响应格式

后端统一响应格式：
```json
{
  "code": 200,
  "msg": "success",
  "data": {}
}
```

### 添加新页面

1. 在 `src/views/` 创建新的 Vue 组件
2. 在 `src/router/index.js` 添加路由
3. 如需 API，在 `src/api/` 创建对应的 API 文件
4. 使用统一的样式类和动画效果

### 样式开发

- 使用 SCSS 进行样式编写
- 遵循设计系统中的颜色和圆角规范
- 利用全局 CSS 中的动画类
- 使用 Element Plus 的主题定制功能

## 🎬 动画使用示例

```vue
<!-- 使用 animate.css 类 -->
<div class="animate__animated animate__fadeInUp">
  <!-- 内容 -->
</div>

<!-- 使用自定义动画类 -->
<div class="float">
  <!-- 浮动效果 -->
</div>

<!-- 页面过渡 -->
<transition name="page">
  <router-view />
</transition>
```

## 🏗 构建部署

### 开发环境
```bash
npm run dev
```

### 生产构建
```bash
npm run build
```

构建产物在 `dist/` 目录，可以部署到任何静态文件服务器。

### 预览生产构建
```bash
npm run preview
```

## 💡 设计理念

本项目采用"可爱有趣、轻松活泼"的设计理念：

1. **色彩**: 使用柔和的渐变色，避免过于强烈的对比
2. **动画**: 适度的动画效果，增强交互体验但不干扰使用
3. **圆角**: 大量使用圆角，让界面更加友好
4. **反馈**: 每个操作都有明确的视觉反馈
5. **细节**: 注重细节，如阴影、边框、间距等

## 📄 许可证

MIT License
