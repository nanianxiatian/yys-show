# 阴阳师对弈竞猜分析系统 - PowerShell 启动脚本
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  阴阳师对弈竞猜分析系统 - 调试启动" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# 检查Python环境
Write-Host "[检查] Python环境..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[错误] 未找到Python，请确保已安装Python并添加到环境变量" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}
Write-Host "[通过] Python已安装: $pythonVersion" -ForegroundColor Green
Write-Host ""

# 检查Node.js环境
Write-Host "[检查] Node.js环境..." -ForegroundColor Yellow
$nodeVersion = node --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[错误] 未找到Node.js，请确保已安装Node.js并添加到环境变量" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}
Write-Host "[通过] Node.js已安装: $nodeVersion" -ForegroundColor Green
Write-Host ""

# 进入后端目录
Set-Location backend

# 检查虚拟环境
Write-Host "[检查] Python虚拟环境..." -ForegroundColor Yellow
if (-not (Test-Path venv)) {
    Write-Host "[信息] 创建虚拟环境..." -ForegroundColor Cyan
    python -m venv venv
}

# 激活虚拟环境
Write-Host "[信息] 激活虚拟环境..." -ForegroundColor Cyan
& venv\Scripts\Activate.ps1

# 安装后端依赖
Write-Host "[安装] 后端依赖..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "[错误] 后端依赖安装失败" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}
Write-Host "[通过] 后端依赖安装完成" -ForegroundColor Green
Write-Host ""

# 检查 .env 文件
Write-Host "[检查] 环境变量文件..." -ForegroundColor Yellow
if (-not (Test-Path .env)) {
    Write-Host "[警告] 未找到 .env 文件，正在从示例创建..." -ForegroundColor Yellow
    if (Test-Path .env.example) {
        Copy-Item .env.example .env
        Write-Host "[信息] 已创建 .env 文件，请编辑它填入你的真实配置" -ForegroundColor Cyan
        Write-Host "[信息] 特别是 MYSQL_PASSWORD 和 SECRET_KEY" -ForegroundColor Cyan
        notepad .env
    } else {
        Write-Host "[错误] 未找到 .env.example 文件" -ForegroundColor Red
        Read-Host "按回车键退出"
        exit 1
    }
} else {
    Write-Host "[通过] .env 文件已存在" -ForegroundColor Green
}
Write-Host ""

# 初始化数据库
Write-Host "[初始化] 数据库..." -ForegroundColor Yellow
python -c "from app import create_app; from app.models import db; app = create_app(); app.app_context().push(); db.create_all()" 2>$null
Write-Host "[通过] 数据库初始化完成" -ForegroundColor Green
Write-Host ""

Set-Location ..

# 安装前端依赖
Set-Location frontend
Write-Host "[检查] 前端依赖..." -ForegroundColor Yellow
if (-not (Test-Path node_modules)) {
    Write-Host "[安装] 安装前端依赖，请稍候..." -ForegroundColor Cyan
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[错误] 前端依赖安装失败" -ForegroundColor Red
        Read-Host "按回车键退出"
        exit 1
    }
} else {
    Write-Host "[通过] 前端依赖已安装" -ForegroundColor Green
}
Write-Host ""

Set-Location ..

# 启动服务
Write-Host "=========================================" -ForegroundColor Green
Write-Host "  所有检查通过，正在启动服务..." -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""
Write-Host "后端地址: http://localhost:5000" -ForegroundColor Cyan
Write-Host "前端地址: http://localhost:5173" -ForegroundColor Cyan
Write-Host ""

# 启动后端（在新窗口）
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; & venv\Scripts\Activate.ps1; python run.py" -WindowTitle "后端服务"

# 等待后端启动
Start-Sleep -Seconds 5

# 启动前端（在新窗口）
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev" -WindowTitle "前端服务"

Write-Host ""
Write-Host "[成功] 服务已启动！" -ForegroundColor Green
Write-Host ""
Write-Host "说明：" -ForegroundColor Yellow
Write-Host "- 后端服务窗口：显示API服务日志" -ForegroundColor White
Write-Host "- 前端服务窗口：显示前端开发服务器日志" -ForegroundColor White
Write-Host "- 请等待几秒钟后访问 http://localhost:5173" -ForegroundColor White
Write-Host ""
Read-Host "按回车键关闭此窗口（服务将继续运行）"
