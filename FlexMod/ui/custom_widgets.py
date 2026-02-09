"""自定义UI控件"""
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class CustomListItemWidget(QWidget):
    """自定义列表项控件"""
    
    delete_clicked = pyqtSignal()
    
    def __init__(self, name: str, block_type: str):
        super().__init__()
        self.name = name
        self.block_type = block_type
        self._init_ui()
    
    def _init_ui(self):
        """初始化UI"""
        self.setFixedHeight(50)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(8)
        
        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)
        
        self.name_label = QLabel(self.name)
        self.name_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 13px;
                background-color: transparent;
                border: none;
            }
        """)
        text_layout.addWidget(self.name_label)
        
        self.type_label = QLabel(self.block_type)
        self.type_label.setStyleSheet("""
            QLabel {
                color: #888;
                font-size: 11px;
                background-color: transparent;
                border: none;
            }
        """)
        text_layout.addWidget(self.type_label)
        
        layout.addLayout(text_layout)
        
        layout.addStretch()
        
        # 创建删除按钮容器，确保即使按钮被隐藏也保留空间
        self.delete_btn_container = QWidget()
        self.delete_btn_container.setFixedSize(24, 24)
        
        self.delete_btn = QPushButton("✕")
        self.delete_btn.setFixedSize(24, 24)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #888;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #ff4444;
            }
        """)
        self.delete_btn.clicked.connect(self.delete_clicked.emit)
        
        container_layout = QHBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(self.delete_btn)
        self.delete_btn_container.setLayout(container_layout)
        
        layout.addWidget(self.delete_btn_container)
        
        self.setLayout(layout)
        
        self.setStyleSheet("""
            CustomListItemWidget {
                background-color: #2a2a2a;
                border: 1px solid #333;
                border-radius: 4px;
            }
            CustomListItemWidget:hover {
                background-color: #333;
                border-color: #444;
            }
        """)
