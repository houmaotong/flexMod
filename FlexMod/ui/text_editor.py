"""通用文本编辑器模块"""
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QPlainTextEdit
from PyQt6.QtCore import Qt
from ..utils.lang import get_text


class TextEditorDialog(QDialog):
    """通用文本编辑器对话框"""
    
    def __init__(self, text: str, title: str = None, lang: int = 0, parent=None):
        super().__init__(parent)
        self.text = text
        self.lang = lang
        self.title = title or get_text('text_editor_title', self.lang)
        self.drag_position = None
        self._init_ui()
    
    def _init_ui(self):
        """初始化UI"""
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setModal(True)
        self.setFixedSize(800, 600)
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
        
        title_bar = QWidget()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                border-bottom: 1px solid #3d3d3d;
            }
        """)
        title_bar.mousePressEvent = self._on_title_bar_press
        title_bar.mouseMoveEvent = self._on_title_bar_move
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(15, 0, 15, 0)
        title_bar.setLayout(title_layout)
        
        title_label = QLabel(self.title)
        title_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 13px;
                font-weight: 500;
                border: none;
                background: transparent;
            }
        """)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(30, 30)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #888;
                font-size: 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
                color: #ffffff;
            }
        """)
        close_btn.clicked.connect(self.reject)
        title_layout.addWidget(close_btn)
        
        layout.addWidget(title_bar)
        
        self.text_edit = QPlainTextEdit()
        self.text_edit.setPlainText(self.text)
        self.text_edit.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1e1e1e;
                border: none;
                color: #d4d4d4;
                font-family: "Courier New", monospace;
                font-size: 13px;
                line-height: 1.5;
                padding: 15px;
            }
            QPlainTextEdit:focus {
                border: none;
            }
        """)
        layout.addWidget(self.text_edit)
        
        button_bar = QWidget()
        button_bar.setFixedHeight(50)
        button_bar.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                border-top: 1px solid #3d3d3d;
            }
        """)
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(15, 0, 15, 0)
        button_bar.setLayout(button_layout)
        button_layout.addStretch()
        
        cancel_btn = QPushButton(get_text('cancel', self.lang))
        cancel_btn.setFixedSize(80, 32)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #3d3d3d;
                border: 1px solid #4d4d4d;
                border-radius: 4px;
                color: #d4d4d4;
                font-size: 12px;
                padding: 6px 16px;
            }
            QPushButton:hover {
                background-color: #4d4d4d;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        confirm_btn = QPushButton(get_text('confirm', self.lang))
        confirm_btn.setFixedSize(80, 32)
        confirm_btn.setStyleSheet("""
            QPushButton {
                background-color: #0e639c;
                border: 1px solid #0e639c;
                border-radius: 4px;
                color: #ffffff;
                font-size: 12px;
                padding: 6px 16px;
            }
            QPushButton:hover {
                background-color: #1177bb;
            }
        """)
        confirm_btn.clicked.connect(self.accept)
        button_layout.addWidget(confirm_btn)
        
        layout.addWidget(button_bar)
    
    def get_text(self) -> str:
        """获取编辑后的文本"""
        return self.text_edit.toPlainText()
    
    def _on_title_bar_press(self, event):
        """标题栏鼠标按下事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def _on_title_bar_move(self, event):
        """标题栏鼠标移动事件"""
        if self.drag_position is not None and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
