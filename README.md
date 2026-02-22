# 阴阳师对弈竞猜分析系统

## 启动方式

由于Windows脚本兼容性问题，建议按以下步骤手动启动：

### 第一步：启动后端

1. 打开 PowerShell 或 CMD 窗口
2. 进入 backend 目录：
   ```
   cd f:\trace\work-space\yys-show\backend
   ```
3. 创建虚拟环境（首次运行）：
   ```
   python -m venv venv
   ```
4. 激活虚拟环境：
   ```
   .\venv\Scripts\activate
   ```
5. 安装依赖（首次运行）：
   ```
   pip install -r requirements.txt
   ```
6. 初始化数据库（首次运行）：
   ```
   python -c "from app import create_app; from app.models import db; app = create_app(); app.app_context().push(); db.create_all()"
   ```
7. 启动后端服务：
   ```
   python run.py
   ```

后端启动成功后，会显示 `Running on http://localhost:5000`

### 第二步：启动前端

1. 再打开一个新的 PowerShell 或 CMD 窗口
2. 进入 frontend 目录：
   ```
   cd f:\trace\work-space\yys-show\frontend
   ```
3. 安装依赖（首次运行）：
   ```
   npm install
   ```
4. 启动前端服务：
   ```
   npm run dev
   ```

前端启动成功后，会显示 `Local: http://localhost:5173/`

### 第三步：访问系统

在浏览器中打开：http://localhost:5173

## 使用说明

1. **添加监控博主**：在"博主管理"页面添加要监控的微博博主昵称
2. **查看微博**：在"微博列表"页面查看爬取的微博数据
3. **录入官方结果**：在"官方结果录入"页面手动录入每轮竞猜的官方结果
4. **查看分析**：在"竞猜分析"页面查看博主的预测准确率

## 定时任务

系统会自动在以下时间爬取数据：
- 11:30, 13:30, 15:30, 17:30, 19:30, 21:30, 23:30

## 注意事项

- 如果微博Cookie过期，需要重新更新 `backend/app/config.py` 中的 `WEIBO_COOKIE`
- 数据库配置在 `backend/app/config.py` 中，默认使用本地MySQL
