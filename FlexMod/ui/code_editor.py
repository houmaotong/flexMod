"""代码编辑器窗口"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPlainTextEdit, 
                             QPushButton, QHBoxLayout, QSplitter)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QColor
import re

from ..managers import resource_manager


class JsonSyntaxHighlighter(QSyntaxHighlighter):
    """JSON语法高亮"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._highlighting_rules = []
        
        key_format = QTextCharFormat()
        key_format.setForeground(QColor("#569cd6"))
        self._highlighting_rules.append((re.compile(r'"[^"]*"(?=\s*:)', re.MULTILINE), key_format))
        
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#ce9178"))
        self._highlighting_rules.append((re.compile(r'"[^"]*"', re.MULTILINE), string_format))
        
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#b5cea8"))
        self._highlighting_rules.append((re.compile(r'\b\d+\.?\d*\b', re.MULTILINE), number_format))
        
        boolean_format = QTextCharFormat()
        boolean_format.setForeground(QColor("#569cd6"))
        self._highlighting_rules.append((re.compile(r'\b(true|false|null)\b', re.MULTILINE), boolean_format))
    
    def highlightBlock(self, text):
        for pattern, format in self._highlighting_rules:
            for match in pattern.finditer(text):
                self.setFormat(match.start(), match.end() - match.start(), format)


class CodeEditorWindow(QMainWindow):
    """代码编辑器窗口"""
    
    content_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("FlexMod - JSON代码编辑器")
        self.setWindowIcon(resource_manager.get_app_icon())
        self.setGeometry(200, 200, 800, 600)
        self._init_ui()
        
        # 居中显示窗口
        from ..utils.window_utils import WindowUtils
        WindowUtils.center_window(self)
    
    def _init_ui(self):
        """初始化UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        toolbar = QWidget()
        toolbar.setStyleSheet("background-color: #2d2d2d; border-bottom: 1px solid #3d3d3d;")
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setContentsMargins(8, 4, 8, 4)
        
        self.save_btn = QPushButton("保存")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #0e639c;
                color: white;
                border: none;
                padding: 6px 16px;
                border-radius: 3px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #1177bb;
            }
        """)
        toolbar_layout.addWidget(self.save_btn)
        
        toolbar_layout.addStretch()
        toolbar.setLayout(toolbar_layout)
        layout.addWidget(toolbar)
        
        self.editor = QPlainTextEdit()
        self.editor.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 13px;
                border: none;
                padding: 8px;
            }
        """)
        self.editor.setFont(QFont("Consolas", 13))
        
        highlighter = JsonSyntaxHighlighter(self.editor.document())
        
        layout.addWidget(self.editor)
        central_widget.setLayout(layout)
    
    def set_content(self, content: str) -> None:
        """设置编辑器内容"""
        self.editor.setPlainText(content)
    
    def get_content(self) -> str:
        """获取编辑器内容"""
        return self.editor.toPlainText()
    
    def clear(self) -> None:
        """清空编辑器"""
        self.editor.clear()
