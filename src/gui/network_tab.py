"""
网络优化页面
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QComboBox, QTextEdit, QGroupBox,
    QLineEdit, QMessageBox
)
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QFont

import socket
import subprocess
import os


class NetworkWorker(QThread):
    log = pyqtSignal(str)
    finished = pyqtSignal()
    
    def __init__(self, action, params=None):
        super().__init__()
        self.action = action
        self.params = params
    
    def run(self):
        if self.action == 'optimize_dns':
            self.optimize_dns()
        elif self.action == 'reset_network':
            self.reset_network()
        elif self.action == 'flush_dns':
            self.flush_dns()
        
        self.finished.emit()
    
    def optimize_dns(self):
        self.log.emit("正在优化DNS...")
        
        # 推荐的DNS服务器
        dns_servers = {
            '阿里DNS': '223.5.5.5',
            '腾讯DNS': '119.29.29.29',
            '114DNS': '114.114.114.114',
            'Google DNS': '8.8.8.8',
        }
        
        selected = self.params.get('dns', '阿里DNS')
        dns_ip = dns_servers.get(selected, '223.5.5.5')
        
        self.log.emit(f"设置DNS为: {selected} ({dns_ip})")
        
        # 这里简化处理，实际应该修改网络适配器设置
        self.log.emit("✓ DNS优化建议已生成（请以管理员身份手动设置）")
        self.log.emit(f"  首选DNS: {dns_ip}")
        self.log.emit(f"  备用DNS: 223.6.6.6")
    
    def reset_network(self):
        self.log.emit("正在重置网络...")
        
        commands = [
            'netsh winsock reset',
            'netsh int ip reset',
            'ipconfig /release',
            'ipconfig /renew',
            'ipconfig /flushdns',
        ]
        
        for cmd in commands:
            self.log.emit(f"执行: {cmd}")
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    self.log.emit("✓ 成功")
                else:
                    self.log.emit(f"⚠ 失败: {result.stderr[:100]}")
            except Exception as e:
                self.log.emit(f"✗ 错误: {str(e)}")
        
        self.log.emit("\n✓ 网络重置完成，建议重启计算机")
    
    def flush_dns(self):
        self.log.emit("正在刷新DNS缓存...")
        
        try:
            result = subprocess.run('ipconfig /flushdns', shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                self.log.emit("✓ DNS缓存已刷新")
            else:
                self.log.emit(f"⚠ 失败: {result.stderr}")
        except Exception as e:
            self.log.emit(f"✗ 错误: {str(e)}")


class NetworkTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # 标题
        title = QLabel("🌐 网络优化")
        title.setFont(QFont("Microsoft YaHei", 18, QFont.Weight.Bold))
        layout.addWidget(title)
        
        desc = QLabel("优化网络设置，提升上网速度")
        desc.setStyleSheet("color: #666;")
        layout.addWidget(desc)
        
        # DNS优化
        dns_group = QGroupBox("DNS优化")
        dns_layout = QHBoxLayout()
        
        dns_layout.addWidget(QLabel("选择DNS服务器:"))
        
        self.dns_combo = QComboBox()
        self.dns_combo.addItems(['阿里DNS', '腾讯DNS', '114DNS', 'Google DNS'])
        dns_layout.addWidget(self.dns_combo)
        
        self.dns_btn = QPushButton("应用")
        self.dns_btn.clicked.connect(self.optimize_dns)
        dns_layout.addWidget(self.dns_btn)
        
        dns_layout.addStretch()
        dns_group.setLayout(dns_layout)
        layout.addWidget(dns_group)
        
        # 网络工具
        tools_group = QGroupBox("网络工具")
        tools_layout = QHBoxLayout()
        
        self.flush_btn = QPushButton("🔄 刷新DNS缓存")
        self.flush_btn.clicked.connect(self.flush_dns)
        tools_layout.addWidget(self.flush_btn)
        
        self.reset_btn = QPushButton("🔧 重置网络")
        self.reset_btn.clicked.connect(self.reset_network)
        tools_layout.addWidget(self.reset_btn)
        
        tools_layout.addStretch()
        tools_group.setLayout(tools_layout)
        layout.addWidget(tools_group)
        
        # 日志区域
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setPlaceholderText("操作日志将显示在这里...")
        self.log_area.setStyleSheet("""
            QTextEdit {
                background-color: #f8f8f8;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.log_area)
        
        # 提示
        tip = QLabel("💡 提示：部分操作需要管理员权限，请以管理员身份运行本程序")
        tip.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(tip)
        
        layout.addStretch()
    
    def optimize_dns(self):
        self.dns_btn.setEnabled(False)
        self.log_area.clear()
        
        self.worker = NetworkWorker('optimize_dns', {'dns': self.dns_combo.currentText()})
        self.worker.log.connect(self.add_log)
        self.worker.finished.connect(lambda: self.dns_btn.setEnabled(True))
        self.worker.start()
    
    def flush_dns(self):
        self.flush_btn.setEnabled(False)
        self.log_area.clear()
        
        self.worker = NetworkWorker('flush_dns')
        self.worker.log.connect(self.add_log)
        self.worker.finished.connect(lambda: self.flush_btn.setEnabled(True))
        self.worker.start()
    
    def reset_network(self):
        reply = QMessageBox.question(
            self, '确认', 
            '重置网络将中断当前网络连接，是否继续？',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.reset_btn.setEnabled(False)
            self.log_area.clear()
            
            self.worker = NetworkWorker('reset_network')
            self.worker.log.connect(self.add_log)
            self.worker.finished.connect(lambda: self.reset_btn.setEnabled(True))
            self.worker.start()
    
    def add_log(self, message):
        self.log_area.append(message)
