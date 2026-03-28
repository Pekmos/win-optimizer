"""
启动项管理页面
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

import winreg
import os


class StartupTab(QWidget):
    def __init__(self):
        super().__init__()
        self.startup_items = []
        self.init_ui()
        self.load_startup_items()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # 标题
        title = QLabel("🚀 启动项管理")
        title.setFont(QFont("Microsoft YaHei", 18, QFont.Weight.Bold))
        layout.addWidget(title)
        
        desc = QLabel("管理系统开机启动项，加快系统启动速度")
        desc.setStyleSheet("color: #666;")
        layout.addWidget(desc)
        
        # 按钮区域
        btn_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("🔄 刷新列表")
        self.refresh_btn.clicked.connect(self.load_startup_items)
        btn_layout.addWidget(self.refresh_btn)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # 表格
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["名称", "路径", "状态", "操作"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(3, 100)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.table)
        
        # 提示
        tip = QLabel("💡 提示：禁用不必要的启动项可以加快系统启动速度")
        tip.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(tip)
        
        layout.addStretch()
    
    def load_startup_items(self):
        self.startup_items.clear()
        
        # 从注册表读取启动项
        reg_paths = [
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
        ]
        
        for hkey, path in reg_paths:
            try:
                with winreg.OpenKey(hkey, path, 0, winreg.KEY_READ) as key:
                    i = 0
                    while True:
                        try:
                            name, value, _ = winreg.EnumValue(key, i)
                            self.startup_items.append({
                                'name': name,
                                'path': value,
                                'enabled': True,
                                'hkey': hkey,
                                'reg_path': path
                            })
                            i += 1
                        except WindowsError:
                            break
            except:
                pass
        
        self.update_table()
    
    def update_table(self):
        self.table.setRowCount(len(self.startup_items))
        
        for i, item in enumerate(self.startup_items):
            # 名称
            name_item = QTableWidgetItem(item['name'])
            self.table.setItem(i, 0, name_item)
            
            # 路径
            path_item = QTableWidgetItem(item['path'])
            path_item.setToolTip(item['path'])
            self.table.setItem(i, 1, path_item)
            
            # 状态
            status = "启用" if item['enabled'] else "禁用"
            status_item = QTableWidgetItem(status)
            status_item.setForeground(
                Qt.GlobalColor.darkGreen if item['enabled'] else Qt.GlobalColor.red
            )
            self.table.setItem(i, 2, status_item)
            
            # 操作按钮
            btn = QPushButton("禁用" if item['enabled'] else "启用")
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #f0f0f0;
                    border: 1px solid #ccc;
                    padding: 5px 15px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
            """)
            btn.clicked.connect(lambda checked, idx=i: self.toggle_startup(idx))
            self.table.setCellWidget(i, 3, btn)
    
    def toggle_startup(self, index):
        item = self.startup_items[index]
        
        try:
            if item['enabled']:
                # 禁用：从Run删除，添加到Run-（简化版本）
                with winreg.OpenKey(item['hkey'], item['reg_path'], 0, winreg.KEY_WRITE) as key:
                    winreg.DeleteValue(key, item['name'])
                item['enabled'] = False
            else:
                # 启用：添加回Run
                with winreg.OpenKey(item['hkey'], item['reg_path'], 0, winreg.KEY_WRITE) as key:
                    winreg.SetValueEx(key, item['name'], 0, winreg.REG_SZ, item['path'])
                item['enabled'] = True
            
            self.update_table()
        except Exception as e:
            QMessageBox.warning(self, "操作失败", f"修改启动项失败：{str(e)}\n\n可能需要以管理员身份运行程序。")
