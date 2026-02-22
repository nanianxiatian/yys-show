# 阴阳师对弈竞猜分析系统启动脚本 (PowerShell版本)
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  阴阳师对弈竞猜分析系统启动脚本" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# 检查Python环境
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) { throw }
    Write-Host "[1/5] 检查Python环境... 通过 ($pythonVersion)" -ForegroundColor Green
} catch {
    Write-Host "[错误] 未找到Python，请确保已安装Python并添加到环境变量" -ForegroundColor Red
    Read-Host "按任意键退出"
    exit 1
}

# 检查Node.js环境
try {
    $nodeVersion = node --version 2>&1
    if ($LASTEXITCODE -ne 0) { throw }
    Write-Host "[2/5] 检查Node.js环境... 通过 ($nodeVersion)" -ForegroundColor Green
} catch {
    Write-Host "[错误] 未找到Node.js，请确保已安装Node.js并添加到环境变量" -ForegroundColor Red
    Read-Host "按任意键退出"
    exit 1
}

Write-Host ""

# 安装后端依赖
Write-Host "[3/5] 安装后端依赖..." -ForegroundColor Yellow
Set-Location -Path "backend"

if (-not (Test-Path "venv")) {
    Write-Host "创建虚拟环境..."
    python -m venv venv
}

& .\venv\Scripts\Activate.ps1
$pipResult = pip install -r requirements.txt 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[错误] 后端依赖安装失败" -ForegroundColor Red
    Write-Host $pipResult
    Read-Host "按任意键退出"
    exit 1
}
Write-Host "后端依赖安装完成" -ForegroundColor Green
Write-Host ""

# 初始化数据库
Write-Host "初始化数据库..." -ForegroundColor Yellow
python -c "from app import create_app; from app.models import db; app = create_app(); app.app_context().push(); db.create_all()" 2>$null
Write-Host "数据库初始化完成" -ForegroundColor Green
Write-Host ""

Set-Location -Path ".."

# 安装前端依赖
Write-Host "[4/5] 安装前端依赖..." -ForegroundColor Yellow
Set-Location -Path "frontend"

if (-not (Test-Path "node_modules")) {
    $npmResult = npm install 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[错误] 前端依赖安装失败" -ForegroundColor Red
        Write-Host $npmResult
        Read-Host "按任意键退出"
        exit 1
    }
}
Write-Host "前端依赖安装完成" -ForegroundColor Green
Write-Host ""

Set-Location -Path ".."

# 启动服务
Write-Host "[5/5] 启动服务..." -ForegroundColor Yellow
Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "  系统启动中..." -ForegroundColor Green
Write-Host "  后端地址: http://localhost:5000" -ForegroundColor Green
Write-Host "  前端地址: http://localhost:5173" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

# 启动后端（在新窗口）
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; .\venv\Scripts\Activate.ps1; python run.py" -WindowStyle Normal

# 等待后端启动
Start-Sleep -Seconds 3

# 启动前端（在新窗口）
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; npm run dev" -WindowStyle Normal

Write-Host "服务已启动！" -ForegroundColor Green
Write-Host "- 后端服务窗口: Python Flask Server"
Write-Host "- 前端服务窗口: Vite Dev Server"
Write-Host ""
Write-Host "请在浏览器中访问: http://localhost:5173" -ForegroundColor Cyan
Write-Host ""
Read-Host "按任意键关闭此窗口（服务将继续运行）"
