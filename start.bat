@echo off
chcp 65001 >nul
echo =========================================
echo  阴阳师对弈竞猜分析系统启动脚本
echo =========================================
echo.

:: 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请确保已安装Python并添加到环境变量
    pause
    exit /b 1
)

:: 检查Node.js环境
node --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Node.js，请确保已安装Node.js并添加到环境变量
    pause
    exit /b 1
)

echo [1/5] 检查环境... 通过
echo.

:: 安装后端依赖
echo [2/5] 安装后端依赖...
cd backend
if not exist venv (
    echo 创建虚拟环境...
    python -m venv venv
)
call venv\Scripts\activate
pip install -r requirements.txt -q
if errorlevel 1 (
    echo [错误] 后端依赖安装失败
    pause
    exit /b 1
)
echo 后端依赖安装完成
echo.

:: 初始化数据库
echo [3/5] 初始化数据库...
python -c "from app import create_app; from app.models import db; app = create_app(); app.app_context().push(); db.create_all()" 2>nul
echo 数据库初始化完成
echo.

cd ..

:: 安装前端依赖
echo [4/5] 安装前端依赖...
cd frontend
if not exist node_modules (
    npm install
    if errorlevel 1 (
        echo [错误] 前端依赖安装失败
        pause
        exit /b 1
    )
)
echo 前端依赖安装完成
echo.

cd ..

:: 启动服务
echo [5/5] 启动服务...
echo.
echo =========================================
echo  系统启动中...
echo  后端地址: http://localhost:5000
echo  前端地址: http://localhost:5173
echo =========================================
echo.

:: 启动后端（在新窗口）
start "后端服务" cmd /k "cd backend && call venv\Scripts\activate && python run.py"

:: 等待后端启动
timeout /t 3 /nobreak >nul

:: 启动前端（在新窗口）
start "前端服务" cmd /k "cd frontend && npm run dev"

echo 服务已启动，请稍候...
echo 前端页面将在浏览器中打开（可能需要手动刷新）
echo.
echo 按任意键关闭此窗口（服务将继续运行）
pause >nul
