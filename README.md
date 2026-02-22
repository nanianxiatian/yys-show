# 阴阳师对弈竞猜分析系统

一个用于分析阴阳师手游对弈竞猜活动的系统，支持微博数据爬取、竞猜结果预测与统计分析。

## 功能特性

- **微博数据爬取** - 自动抓取指定博主的微博内容
- **智能解析** - 自动识别对弈竞猜相关内容
- **结果预测** - 基于历史数据分析预测竞猜结果
- **统计分析** - 多维度统计博主预测准确率
- **定时任务** - 自动定时爬取和统计
- **批量操作** - 支持批量删除等管理功能

## 技术栈

### 后端
- Python 3.9+
- Flask 3.0.0
- Flask-SQLAlchemy
- PyMySQL
- APScheduler (定时任务)
- BeautifulSoup4 (网页解析)
- python-dotenv (环境变量管理)

### 前端
- React 18
- Ant Design 5.x
- Zustand (状态管理)
- Axios (HTTP请求)
- Vite (构建工具)

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/nanianxiatian/yys-show.git
cd yys-show
```

### 2. 后端配置

#### 2.1 创建虚拟环境

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### 2.2 安装依赖

```bash
pip install -r requirements.txt
```

#### 2.3 配置环境变量

复制示例配置文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的真实配置：

```env
# MySQL数据库配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=你的数据库密码
MYSQL_DB=yys_guess

# Flask密钥（建议使用随机字符串）
SECRET_KEY=你的密钥

# 微博Cookie（可选，也可以在系统设置中配置）
WEIBO_COOKIE=你的微博Cookie
```

#### 2.4 初始化数据库

```bash
python init_db.py
```

#### 2.5 启动后端服务

```bash
python run.py
```

后端服务将在 http://127.0.0.1:5000 启动

### 3. 前端配置

#### 3.1 安装依赖

```bash
cd frontend
npm install
```

#### 3.2 启动开发服务器

```bash
npm run dev
```

前端服务将在 http://localhost:5173 启动

### 4. 访问系统

打开浏览器访问：http://localhost:5173

## 项目结构

```
yys-show/
├── backend/                 # 后端代码
│   ├── app/                 # 应用主目录
│   │   ├── __init__.py      # Flask应用初始化
│   │   ├── config.py        # 配置文件
│   │   ├── models/          # 数据模型
│   │   ├── routes/          # API路由
│   │   └── services/        # 业务逻辑
│   ├── spider/              # 爬虫模块
│   │   ├── weibo_crawler.py # 微博爬虫
│   │   └── parser.py        # 内容解析器
│   ├── .env                 # 环境变量（本地配置，不提交到Git）
│   ├── .env.example         # 环境变量示例
│   ├── requirements.txt     # Python依赖
│   └── run.py               # 启动脚本
├── frontend/                # 前端代码
│   ├── src/                 # 源代码
│   │   ├── pages/           # 页面组件
│   │   ├── services/        # API服务
│   │   └── App.jsx          # 应用入口
│   ├── package.json         # Node依赖
│   └── vite.config.js       # Vite配置
└── README.md                # 项目说明
```

## 环境变量说明

项目使用 `.env` 文件管理敏感配置，**请勿将 `.env` 文件提交到Git**。

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| MYSQL_HOST | MySQL主机地址 | localhost |
| MYSQL_PORT | MySQL端口 | 3306 |
| MYSQL_USER | MySQL用户名 | root |
| MYSQL_PASSWORD | MySQL密码 | 必填 |
| MYSQL_DB | 数据库名 | yys_guess |
| SECRET_KEY | Flask密钥 | 必填 |
| WEIBO_COOKIE | 微博Cookie | 可选 |

## 安全说明

- ✅ 敏感信息（密码、密钥等）存储在本地 `.env` 文件中
- ✅ `.env` 文件已被 `.gitignore` 排除，不会上传到GitHub
- ✅ GitHub上的代码只包含占位符，保护你的真实配置
- ⚠️ 请勿手动将 `.env` 文件内容暴露到公开渠道

## 定时任务配置

系统默认配置以下定时任务：

- **自动爬虫**：每天 11:30, 13:30, 15:30, 17:30, 19:30, 21:30, 23:30 执行
- **每日统计**：每天 01:00 执行

可在 `backend/app/config.py` 中修改定时任务配置。

## API文档

启动后端服务后，访问：http://127.0.0.1:5000/api/docs

## 常见问题

### 1. 数据库连接失败

检查 `.env` 文件中的数据库配置是否正确，确保MySQL服务已启动。

### 2. 微博爬取失败

- 检查微博Cookie是否有效
- 可在系统设置页面更新Cookie
- 注意Cookie有有效期，过期需要重新获取

### 3. 前端无法连接后端

- 确认后端服务已启动
- 检查前端 `vite.config.js` 中的代理配置
- 确认端口未被占用

## 更新日志

### 2026-02-23
- 添加环境变量支持，使用 `.env` 文件管理敏感配置
- 移除代码中的硬编码密码，提升安全性
- 完善项目文档

## 贡献指南

欢迎提交Issue和Pull Request！

## 许可证

MIT License

## 联系方式

如有问题，请通过 GitHub Issues 联系。

---

**注意**：本项目仅供学习交流使用，请遵守相关法律法规和平台规则。
