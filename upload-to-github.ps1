# GitHub 自动上传脚本
# 用户名: Pekmos
# 仓库: win-optimizer

# 配置 Git
git config --global user.name "Pekmos"
git config --global user.email "pekmos@example.com"

# 进入项目目录
cd C:\Users\1\.openclaw\workspace\win-optimizer

# 初始化 Git
if (!(Test-Path .git)) {
    git init
    Write-Host "✓ Git 初始化完成" -ForegroundColor Green
}

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: WinOptimizer v1.0.0

功能特性:
- 垃圾清理: 清理临时文件、系统日志、回收站
- 启动项管理: 查看/启用/禁用开机启动项
- 系统信息: 实时显示CPU、内存、磁盘使用
- 网络优化: DNS优化、刷新DNS、重置网络

技术栈: Python + PyQt6
开源协议: MIT"

# 关联远程仓库
git remote remove origin 2>$null
git remote add origin https://github.com/Pekmos/win-optimizer.git

# 推送（需要输入密码）
Write-Host "`n正在推送到 GitHub..." -ForegroundColor Cyan
Write-Host "用户名: Pekmos" -ForegroundColor Yellow
Write-Host "密码: qhr112233" -ForegroundColor Yellow
Write-Host "`n如果提示输入密码，请手动输入`n" -ForegroundColor Red

git push -u origin main

Write-Host "`n✓ 上传完成！" -ForegroundColor Green
Write-Host "项目地址: https://github.com/Pekmos/win-optimizer" -ForegroundColor Cyan
