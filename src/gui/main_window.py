"""
主窗口
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget, QFrame
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon

from .cleaner_tab import CleanerTab
from .startup_tab import StartupTab
from .system_tab import SystemTab
from .network_tab import NetworkTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WinOptimizer - Windows系统优化工具")
        self.setMinimumSize(900, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建侧边栏
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)
        
        # 创建内容区域
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack, 1)
        
        # 添加各个页面
        self.cleaner_tab = CleanerTab()
        self.startup_tab = StartupTab()
        self.system_tab = SystemTab()
        self.network_tab = NetworkTab()
        
        self.content_stack.addWidget(self.cleaner_tab)
        self.content_stack.addWidget(self.startup_tab)
        self.content_stack.addWidget(self.system_tab)
        self.content_stack.addWidget(self.network_tab)
        
        # 设置样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QPushButton {
                border: none;
                padding: 15px 20px;
                text-align: left;
                font-size: 14px;
                background-color: transparent;
                color: #333;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:checked {
                background-color: #0078d4;
                color: white;
            }
        """)
    
    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("background-color: #ffffff; border-right: 1px solid #ddd;")
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 20, 0, 20)
        layout.setSpacing(5)
        
        # 标题
        title = QLabel("WinOptimizer")
        title.setFont(QFont("Microsoft YaHei", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #0078d4; padding: 0 20px;")
        layout.addWidget(title)
        
        subtitle = QLabel("Windows系统优化工具")
        subtitle.setStyleSheet("color: #666; font-size: 12px; padding: 0 20px; margin-bottom: 20px;")
        layout.addWidget(subtitle)
        
        # 导航按钮
        self.nav_buttons = []
        
        nav_items = [
            ("🧹 垃圾清理", 0),
            ("🚀 启动项管理", 1),
            ("📊 系统信息", 2),
            ("🌐 网络优化", 3),
        ]
        
        for text, index in nav_items:
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, idx=index: self.switch_tab(idx))
            layout.addWidget(btn)
            self.nav_buttons.append(btn)
        
        # 默认选中第一个
        self.nav_buttons[0].setChecked(True)
        
        layout.addStretch()
        
        # 版本信息
        version = QLabel("v1.0.0")
        version.setStyleSheet("color: #999; padding: 0 20px;")
        layout.addWidget(version)
        
        return sidebar
    
    def switch_tab(self, index):
        # 更新按钮状态
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)
        
        # 切换页面
        self.content_stack.setCurrentIndex(index)
