"""
WinOptimizer 打包脚本
使用 PyInstaller 打包成 exe
"""

import PyInstaller.__main__
import os

# 项目路径
project_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(project_dir, 'src')

# PyInstaller 参数
args = [
    os.path.join(src_dir, 'main.py'),  # 入口文件
    '--name=WinOptimizer',  # 应用名称
    '--windowed',  # 无控制台窗口
    '--onefile',  # 打包成单个文件
    '--icon=NONE',  # 暂时无图标
    '--clean',  # 清理临时文件
    '--noconfirm',  # 不确认覆盖
    f'--distpath={os.path.join(project_dir, "dist")}',
    f'--workpath={os.path.join(project_dir, "build")}',
    f'--specpath={project_dir}',
    # 添加数据文件
    f'--add-data={src_dir}/gui;gui',
    f'--add-data={src_dir}/core;core',
    # 隐藏导入
    '--hidden-import=PyQt6',
    '--hidden-import=psutil',
    '--hidden-import=winshell',
    '--hidden-import=pywin32',
]

print("开始打包 WinOptimizer...")
PyInstaller.__main__.run(args)
print("打包完成！")
