# 重启Flask服务脚本
Write-Host "正在重启Flask服务..." -ForegroundColor Yellow

# 查找并停止现有的Python/Flask进程
$processes = Get-Process | Where-Object { $_.ProcessName -like "*python*" -or $_.ProcessName -like "*flask*" }
if ($processes) {
    Write-Host "发现正在运行的Python进程，正在停止..." -ForegroundColor Yellow
    $processes | ForEach-Object { 
        Write-Host "  停止进程: $($_.ProcessName) (PID: $($_.Id))" -ForegroundColor Gray
        Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
    }
    Start-Sleep -Seconds 2
}

# 清除Python缓存
Write-Host "清除Python缓存..." -ForegroundColor Yellow
$cacheDirs = Get-ChildItem -Path "f:\trace\work-space\yys-show\backend" -Recurse -Filter "__pycache__" -Directory -ErrorAction SilentlyContinue
$cacheDirs | ForEach-Object { 
    Write-Host "  删除: $($_.FullName)" -ForegroundColor Gray
    Remove-Item -Path $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
}

$pycFiles = Get-ChildItem -Path "f:\trace\work-space\yys-show\backend" -Recurse -Filter "*.pyc" -File -ErrorAction SilentlyContinue
$pycFiles | ForEach-Object { 
    Write-Host "  删除: $($_.FullName)" -ForegroundColor Gray
    Remove-Item -Path $_.FullName -Force -ErrorAction SilentlyContinue
}

Write-Host "缓存清除完成" -ForegroundColor Green
Write-Host ""
Write-Host "请手动启动Flask服务:" -ForegroundColor Cyan
Write-Host "  cd f:\trace\work-space\yys-show\backend" -ForegroundColor White
Write-Host "  venv\Scripts\python run.py" -ForegroundColor White
