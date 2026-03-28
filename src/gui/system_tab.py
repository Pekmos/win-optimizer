"""
系统信息页面
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QProgressBar, QGridLayout, QGroupBox
)
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont

import psutil
import platform


class SystemTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.start_timer()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # 标题
        title = QLabel("📊 系统信息")
        title.setFont(QFont("Microsoft YaHei", 18, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # 系统信息组
        sys_group = QGroupBox("系统信息")
        sys_layout = QGridLayout()
        
        sys_info = [
            ("操作系统:", f"{platform.system()} {platform.release()}"),
            ("版本:", platform.version()),
            ("处理器:", platform.processor()),
            ("架构:", platform.machine()),
            ("计算机名:", platform.node()),
        ]
        
        for i, (label, value) in enumerate(sys_info):
            sys_layout.addWidget(QLabel(label), i, 0)
            value_label = QLabel(value)
            value_label.setStyleSheet("color: #333; font-weight: bold;")
            sys_layout.addWidget(value_label, i, 1)
        
        sys_group.setLayout(sys_layout)
        layout.addWidget(sys_group)
        
        # CPU 信息
        cpu_group = QGroupBox("CPU 使用率")
        cpu_layout = QVBoxLayout()
        
        self.cpu_label = QLabel("0%")
        self.cpu_label.setFont(QFont("Microsoft YaHei", 24, QFont.Weight.Bold))
        self.cpu_label.setStyleSheet("color: #0078d4;")
        cpu_layout.addWidget(self.cpu_label)
        
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setMaximum(100)
        cpu_layout.addWidget(self.cpu_bar)
        
        self.cpu_cores = QLabel("核心数: --")
        cpu_layout.addWidget(self.cpu_cores)
        
        cpu_group.setLayout(cpu_layout)
        layout.addWidget(cpu_group)
        
        # 内存信息
        mem_group = QGroupBox("内存使用")
        mem_layout = QVBoxLayout()
        
        self.mem_label = QLabel("0%")
        self.mem_label.setFont(QFont("Microsoft YaHei", 24, QFont.Weight.Bold))
        self.mem_label.setStyleSheet("color: #107c10;")
        mem_layout.addWidget(self.mem_label)
        
        self.mem_bar = QProgressBar()
        self.mem_bar.setMaximum(100)
        mem_layout.addWidget(self.mem_bar)
        
        self.mem_detail = QLabel("已用: -- / 总计: --")
        mem_layout.addWidget(self.mem_detail)
        
        mem_group.setLayout(mem_layout)
        layout.addWidget(mem_group)
        
        # 磁盘信息
        disk_group = QGroupBox("磁盘使用")
        disk_layout = QVBoxLayout()
        
        self.disk_info = QLabel("加载中...")
        disk_layout.addWidget(self.disk_info)
        
        disk_group.setLayout(disk_layout)
        layout.addWidget(disk_group)
        
        layout.addStretch()
        
        # 初始更新
        self.update_system_info()
    
    def start_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_system_info)
        self.timer.start(2000)  # 每2秒更新一次
    
    def update_system_info(self):
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        self.cpu_label.setText(f"{cpu_percent:.1f}%")
        self.cpu_bar.setValue(int(cpu_percent))
        self.cpu_cores.setText(f"核心数: {psutil.cpu_count()} (逻辑: {psutil.cpu_count(logical=True)})")
        
        # 内存
        mem = psutil.virtual_memory()
        self.mem_label.setText(f"{mem.percent:.1f}%")
        self.mem_bar.setValue(int(mem.percent))
        
        used_gb = mem.used / (1024**3)
        total_gb = mem.total / (1024**3)
        self.mem_detail.setText(f"已用: {used_gb:.1f} GB / 总计: {total_gb:.1f} GB")
        
        # 磁盘
        disk_info_text = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                used_gb = usage.used / (1024**3)
                total_gb = usage.total / (1024**3)
                percent = usage.percent
                disk_info_text.append(
                    f"{partition.device} - 已用 {used_gb:.1f}GB / {total_gb:.1f}GB ({percent}%)"
                )
            except:
                pass
        
        self.disk_info.setText("\n".join(disk_info_text) if disk_info_text else "无法获取磁盘信息")
