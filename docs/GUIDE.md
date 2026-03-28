# WinOptimizer 使用指南

## 简介

WinOptimizer 是一个开源免费的 Windows 系统优化工具，帮助你轻松清理系统垃圾、管理启动项、监控系统状态。

## 功能特点

### 🧹 垃圾清理
- 清理 Windows 临时文件
- 清理系统日志文件
- 清空回收站
- 释放磁盘空间

### 🚀 启动项管理
- 查看所有开机启动程序
- 一键禁用不必要的启动项
- 加速系统启动速度

### 📊 系统信息
- 实时显示 CPU 使用率
- 监控内存占用情况
- 查看磁盘空间使用
- 显示系统详细信息

### 🌐 网络优化
- DNS 优化建议
- 刷新 DNS 缓存
- 重置网络设置（解决网络问题）

## 安装使用

### 方法一：下载安装包（推荐）

1. 访问 [Releases 页面](https://github.com/Pekmos/win-optimizer/releases)
2. 下载最新版本的 `WinOptimizer.exe`
3. 双击运行即可

### 方法二：从源码运行

需要安装 Python 3.8 或更高版本。

```bash
# 1. 克隆仓库
git clone https://github.com/Pekmos/win-optimizer.git

# 2. 进入目录
cd win-optimizer

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行
python src/main.py
```

## 使用说明

### 垃圾清理
1. 打开软件，点击"垃圾清理"
2. 选择要清理的项目（建议全选）
3. 点击"开始扫描"
4. 等待扫描完成，查看可释放空间
5. 确认清理

### 启动项管理
1. 点击"启动项管理"
2. 查看列表中的启动程序
3. 对不需要的程序点击"禁用"
4. 建议保留系统关键启动项

### 系统信息
- 实时查看 CPU、内存、磁盘使用情况
- 帮助了解系统运行状态

### 网络优化
- 如遇网络问题，可尝试"重置网络"
- DNS 优化可提升网页打开速度

## 注意事项

1. **管理员权限**：部分功能需要以管理员身份运行
2. **备份重要数据**：清理前建议备份重要文件
3. **谨慎禁用启动项**：不要禁用不认识的系统程序

## 常见问题

**Q: 软件收费吗？**  
A: 完全免费，开源软件。

**Q: 安全吗？**  
A: 代码完全开源，可查看审查。不上传任何数据。

**Q: 支持 Windows 7 吗？**  
A: 主要支持 Windows 10/11，Windows 7 可能部分功能不兼容。

**Q: 如何更新？**  
A: 关注 GitHub Releases 页面，下载最新版本。

## 技术支持

- GitHub Issues: https://github.com/Pekmos/win-optimizer/issues
- 邮件: [你的邮箱]

## 支持作者

如果这个工具帮到了你，欢迎支持：

- ⭐ GitHub Star
- 💰 支付宝打赏（见 README）
- ☕ GitHub Sponsors

## 许可证

MIT License - 详见 LICENSE 文件

---

**感谢使用 WinOptimizer！**
