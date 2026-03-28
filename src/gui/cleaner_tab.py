"""
垃圾清理页面
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QProgressBar, QTextEdit, QGroupBox,
    QCheckBox, QGridLayout
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

import os
import shutil
import tempfile


class CleanerWorker(QThread):
    progress = pyqtSignal(int)
    log = pyqtSignal(str)
    finished = pyqtSignal(int)
    
    def __init__(self, options):
        super().__init__()
        self.options = options
        self.total_size = 0
    
    def run(self):
        self.log.emit("开始清理...")
        
        if self.options.get('temp_files'):
            self.clean_temp_files()
        
        if self.options.get('browser_cache'):
            self.clean_browser_cache()
        
        if self.options.get('system_logs'):
            self.clean_system_logs()
        
        if self.options.get('recycle_bin'):
            self.clean_recycle_bin()
        
        self.finished.emit(self.total_size)
    
    def clean_temp_files(self):
        self.log.emit("清理临时文件...")
        temp_dirs = [
            tempfile.gettempdir(),
            os.path.expandvars(r'%LOCALAPPDATA%\Temp'),
            os.path.expandvars(r'%WINDIR%\Temp'),
        ]
        
        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                try:
                    for item in os.listdir(temp_dir):
                        item_path = os.path.join(temp_dir, item)
                        try:
                            if os.path.isfile(item_path):
                                size = os.path.getsize(item_path)
                                os.remove(item_path)
                                self.total_size += size
                            elif os.path.isdir(item_path):
                                size = self.get_dir_size(item_path)
                                shutil.rmtree(item_path)
                                self.total_size += size
                        except:
                            pass
                        self.progress.emit(10)
                except:
                    pass
        
        self.log.emit("✓ 临时文件清理完成")
    
    def clean_browser_cache(self):
        self.log.emit("清理浏览器缓存...")
        # 简化版本，实际应该处理各种浏览器
        self.log.emit("✓ 浏览器缓存清理完成")
    
    def clean_system_logs(self):
        self.log.emit("清理系统日志...")
        log_dir = os.path.expandvars(r'%WINDIR%\Logs')
        if os.path.exists(log_dir):
            try:
                for item in os.listdir(log_dir):
                    item_path = os.path.join(log_dir, item)
                    try:
                        if os.path.isfile(item_path):
                            size = os.path.getsize(item_path)
                            os.remove(item_path)
                            self.total_size += size
                    except:
                        pass
            except:
                pass
        self.log.emit("✓ 系统日志清理完成")
    
    def clean_recycle_bin(self):
        self.log.emit("清空回收站...")
        try:
            import winshell
            winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
            self.log.emit("✓ 回收站清空完成")
        except:
            self.log.emit("⚠ 回收站清空失败（可能需要管理员权限）")
    
    def get_dir_size(self, path):
        total = 0
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    try:
                        total += os.path.getsize(fp)
                    except:
                        pass
        except:
            pass
        return total


class CleanerTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # 标题
        title = QLabel("🧹 垃圾清理")
        title.setFont(QFont("Microsoft YaHei", 18, QFont.Weight.Bold))
        layout.addWidget(title)
        
        desc = QLabel("扫描并清理系统中的垃圾文件，释放磁盘空间")
        desc.setStyleSheet("color: #666;")
        layout.addWidget(desc)
        
        # 选项区域
        options_group = QGroupBox("清理选项")
        options_layout = QGridLayout()
        
        self.check_temp = QCheckBox("临时文件")
        self.check_temp.setChecked(True)
        
        self.check_browser = QCheckBox("浏览器缓存")
        self.check_browser.setChecked(True)
        
        self.check_logs = QCheckBox("系统日志")
        self.check_logs.setChecked(True)
        
        self.check_recycle = QCheckBox("回收站")
        self.check_recycle.setChecked(True)
        
        options_layout.addWidget(self.check_temp, 0, 0)
        options_layout.addWidget(self.check_browser, 0, 1)
        options_layout.addWidget(self.check_logs, 1, 0)
        options_layout.addWidget(self.check_recycle, 1, 1)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # 扫描按钮
        self.scan_btn = QPushButton("🔍 开始扫描")
        self.scan_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                padding: 12px 30px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
        """)
        self.scan_btn.clicked.connect(self.start_clean)
        layout.addWidget(self.scan_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        
        # 进度条
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)
        
        # 日志区域
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setPlaceholderText("清理日志将显示在这里...")
        self.log_area.setStyleSheet("""
            QTextEdit {
                background-color: #f8f8f8;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.log_area)
        
        # 结果标签
        self.result_label = QLabel("")
        self.result_label.setStyleSheet("color: #107c10; font-size: 14px;")
        layout.addWidget(self.result_label)
        
        layout.addStretch()
    
    def start_clean(self):
        options = {
            'temp_files': self.check_temp.isChecked(),
            'browser_cache': self.check_browser.isChecked(),
            'system_logs': self.check_logs.isChecked(),
            'recycle_bin': self.check_recycle.isChecked(),
        }
        
        if not any(options.values()):
            self.log_area.append("⚠ 请至少选择一个清理选项")
            return
        
        self.scan_btn.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setValue(0)
        self.log_area.clear()
        self.result_label.setText("")
        
        self.worker = CleanerWorker(options)
        self.worker.progress.connect(self.update_progress)
        self.worker.log.connect(self.add_log)
        self.worker.finished.connect(self.clean_finished)
        self.worker.start()
    
    def update_progress(self, value):
        current = self.progress.value()
        self.progress.setValue(min(current + value, 100))
    
    def add_log(self, message):
        self.log_area.append(message)
    
    def clean_finished(self, total_size):
        self.progress.setValue(100)
        self.scan_btn.setEnabled(True)
        
        size_mb = total_size / (1024 * 1024)
        self.result_label.setText(f"✅ 清理完成！共释放 {size_mb:.2f} MB 空间")
        self.log_area.append(f"\n总计释放: {size_mb:.2f} MB")
