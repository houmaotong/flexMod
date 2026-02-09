"""可折叠组件模块"""
import os
import random
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QPlainTextEdit, QComboBox, 
                             QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal, QPoint
from PyQt6.QtGui import QFont

from ..utils.lang import get_text
from .text_editor import TextEditorDialog


class CardStyles:
    """卡片样式常量类"""
    # 颜色常量
    COLORS = {
        "HEADER_BG": "#353535",
        "CARD_BG": "#2f2f2f",
        "INPUT_BG": "#252525",
        "BORDER": "#444",
        "BORDER_HOVER": "#555",
        "BORDER_FOCUS": "#0e639c",
        "TEXT": "#eee",
        "TEXT_LIGHT": "#ddd",
        "TEXT_DARK": "#777",
        "BUTTON_BG": "#333",
        "BUTTON_BG_HOVER": "#3a3a3a",
        "TOGGLE_BG": "#444",
        "TOGGLE_BG_HOVER": "#555",
        "SELECTION_BG": "#0e639c",
        "SELECTION_TEXT": "white"
    }

    # 公共样式常量
    HEADER_STYLE = f"""
        QWidget {{
            background-color: {COLORS['HEADER_BG']};
            border: none;
            padding: 8px 12px;
        }}
    """

    TITLE_LABEL_STYLE = f"""
        QLabel {{
            font-size: 12px;
            font-weight: 500;
            color: {COLORS['TEXT_LIGHT']};
        }}
    """

    TOGGLE_BUTTON_STYLE = f"""
        QPushButton {{
            background-color: {COLORS['TOGGLE_BG']};
            border: none;
            border-radius: 2px;
            color: {COLORS['TEXT']};
            font-size: 10px;
            padding: 0;
        }}
        QPushButton:hover {{
            background-color: {COLORS['TOGGLE_BG_HOVER']};
        }}
    """

    CARD_STYLE = f"""
        QWidget {{
            background-color: {COLORS['CARD_BG']};
            border: 1px solid {COLORS['BORDER']};
            border-radius: 3px;
        }}
    """

    HEADER_EXTRA_LABEL_STYLE = f"""
        QLabel {{
            font-size: 12px;
            color: {COLORS['TEXT_DARK']};
            background-color: transparent;
        }}
    """

    DELETE_BUTTON_STYLE = f"""
        QPushButton {{
            padding: 2px 4px;
            background-color: {COLORS['TOGGLE_BG']};
            border: none;
            border-radius: 2px;
            color: {COLORS['TEXT']};
            font-size: 10px;
        }}
        QPushButton:hover {{
            background-color: {COLORS['TOGGLE_BG_HOVER']};
        }}
    """

    INPUT_STYLE = f"""
        QLineEdit {{
            padding: 6px 8px;
            background-color: {COLORS['INPUT_BG']};
            border: 1px solid {COLORS['BORDER']};
            border-radius: 2px;
            color: {COLORS['TEXT']};
            font-size: 11px;
        }}
        QLineEdit:hover {{
            border: 1px solid {COLORS['BORDER_HOVER']};
        }}
        QLineEdit:focus {{
            border: 1px solid {COLORS['BORDER_FOCUS']};
        }}
    """

    BUTTON_STYLE = f"""
        QPushButton {{
            padding: 8px 16px;
            background-color: {COLORS['BUTTON_BG']};
            border: 1px solid {COLORS['BORDER']};
            border-radius: 3px;
            color: {COLORS['TEXT']};
            font-size: 12px;
        }}
        QPushButton:hover {{
            background-color: {COLORS['BUTTON_BG_HOVER']};
        }}
    """

    COMBOBOX_STYLE = f"""
        QComboBox {{
            padding: 6px 8px;
            background-color: {COLORS['INPUT_BG']};
            border: 1px solid {COLORS['BORDER']};
            border-radius: 2px;
            color: {COLORS['TEXT']};
            font-size: 11px;
        }}
        QComboBox:hover {{
            border: 1px solid {COLORS['BORDER_HOVER']};
        }}
        QComboBox:focus {{
            border: 1px solid {COLORS['BORDER_FOCUS']};
        }}
        QComboBox QAbstractItemView {{
            background-color: {COLORS['INPUT_BG']};
            border: 1px solid {COLORS['BORDER']};
            selection-background-color: {COLORS['SELECTION_BG']};
            selection-color: {COLORS['SELECTION_TEXT']};
        }}
    """

    PLAINTEXT_EDIT_STYLE = f"""
        QPlainTextEdit {{
            padding: 8px;
            background-color: {COLORS['INPUT_BG']};
            border: 1px solid {COLORS['BORDER']};
            border-radius: 2px;
            color: {COLORS['TEXT']};
            font-family: "Courier New", monospace;
            font-size: 11px;
        }}
    """

    # 为了方便直接使用，也定义一些常用颜色的直接引用
    BORDER_COLOR = COLORS['BORDER']
    BORDER_HOVER_COLOR = COLORS['BORDER_HOVER']
    BORDER_FOCUS_COLOR = COLORS['BORDER_FOCUS']
    TEXT_COLOR = COLORS['TEXT']
    BACKGROUND_COLOR = COLORS['CARD_BG']
    INPUT_BACKGROUND_COLOR = COLORS['INPUT_BG']


# 创建样式实例
styles = CardStyles()



def generate_pastel_color() -> str:
    """生成清新低饱和的颜色"""
    # 预定义一些与深色主题协调的、饱和度适中的颜色
    pastel_colors = [
        "#4ECDC4",  # 青绿色
        "#45B7D1",  # 蓝色
        "#96CEB4",  # 淡绿色
        "#FECA57",  # 黄色
        "#FF6B6B",  # 珊瑚红
        "#FF8E53",  # 橙红色
        "#C44569",  # 玫红色
        "#5F27CD",  # 紫色
        "#10AC84",  # 深绿色
        "#0097E6",  # 深蓝色
        "#8C7AE6",  # 紫罗兰色
        "#EE5A24",  # 橙色
    ]
    return random.choice(pastel_colors)


class CollapsibleCard(QWidget):
    """可折叠卡片基类"""
    
    toggled = pyqtSignal(bool)
    copy_requested = pyqtSignal()
    delete_requested = pyqtSignal()
    
    def __init__(self, title: str, is_default: bool = False, color=None, parent=None):
        super().__init__(parent)
        self.title = title
        self.is_default = is_default
        self.is_expanded = False
        self.color = color
        self._init_ui()
    
    def _init_ui(self):
        """初始化UI"""
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
        
        self.header = self._create_header()
        layout.addWidget(self.header)
        
        self.content = QWidget()
        self.content.setVisible(False)
        layout.addWidget(self.content)
        
        self.update_style()
    
    def _create_header(self) -> QWidget:
        """创建头部（重写父类方法，移除额外按钮）"""
        header = QWidget()
        header.setStyleSheet(styles.HEADER_STYLE)
        
        # 固定header的高度，确保卡头不会被拉高
        header.setFixedHeight(36)
        
        # 为header添加单击事件处理
        header.mousePressEvent = self._on_header_click
        
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 8, 0)  # 左侧保持0，右侧添加8px边距
        layout.setSpacing(8)
        # 设置垂直对齐方式为顶部
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        header.setLayout(layout)
        
        # 添加左侧颜色块
        if self.color:
            color_block = QWidget()
            color_block.setStyleSheet(f"""
                QWidget {{
                    background-color: {self.color};
                    border: none;
                    border-radius: 2px;
                }}
            """)
            color_block.setFixedSize(4, 20)
            layout.addWidget(color_block)
            
            # 调整标题标签的间距
            layout.addSpacing(4)
        
        self.title_label = QLabel(self.title)
        self.title_label.setStyleSheet(styles.TITLE_LABEL_STYLE)
        layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignTop)
        
        # 添加拉伸空间
        layout.addStretch()
        
        self.toggle_btn = QPushButton("▼")
        self.toggle_btn.setFixedSize(20, 20)
        self.toggle_btn.setStyleSheet(styles.TOGGLE_BUTTON_STYLE)
        self.toggle_btn.clicked.connect(self._on_toggle)
        layout.addWidget(self.toggle_btn, alignment=Qt.AlignmentFlag.AlignTop)
    
        return header
    
    def _on_toggle(self):
        """切换折叠状态"""
        self.is_expanded = not self.is_expanded
        self.content.setVisible(self.is_expanded)
        self.toggle_btn.setText("▲" if self.is_expanded else "▼")
        
        # 移除固定高度限制，以便调整大小
        self.setMinimumHeight(0)
        self.setMaximumHeight(16777215)
        
        # 保存当前宽度，以便调整大小后恢复
        current_width = self.width()
        
        # 调整卡片大小以适应内容
        self.adjustSize()
        
        # 恢复原始宽度，确保卡片宽度保持不变
        self.resize(current_width, self.height())
        
        self.toggled.emit(self.is_expanded)
    
    def _on_header_click(self, event):
        """处理header单击事件，展开/折叠卡片"""
        self._on_toggle()
    
    def _adjust_height(self):
        """调整卡片高度（已废弃，使用adjustSize()）"""
        pass
    
    def set_title(self, title: str):
        """设置标题"""
        self.title = title
        self.title_label.setText(title)
    
    def update_style(self):
        """更新样式"""
        self.setStyleSheet(styles.CARD_STYLE)
    
    def resizeEvent(self, event):
        """处理窗口大小变化事件，确保卡片宽度始终适应父容器"""
        super().resizeEvent(event)
        # 当父容器大小改变时，确保卡片宽度适应父容器
        if self.parent():
            # 移除最小宽度限制，让卡片能够自由调整
            self.setMinimumWidth(0)
            # 移除最大宽度限制，让卡片能够自由调整
            self.setMaximumWidth(16777215)  # Qt的最大宽度值


class ExecUnitCard(CollapsibleCard):
    """执行单元卡片"""
    
    content_changed = pyqtSignal()
    
    def __init__(self, index: int, is_default: bool = False, unit_code: str = None, lang: int = 0, parent=None):
        # 为ExecUnitCard添加固定的深色色块
        fixed_color = "#555555"  # 固定的深色
        super().__init__(f"#{index}", is_default, fixed_color, parent)
        self.index = index
        self.lang = lang
        self.unit_code = unit_code or self._generate_unit_code()
        self.content_height = 160
        self.config_dir = None
        self._pending_file_path = None
        self._saved_file_path = ""  # 保存当前设置的文件路径
        
        # 创建额外的标签来显示文件路径
        from PyQt6.QtWidgets import QLabel
        self.extra_label = QLabel()
        self.extra_label.setStyleSheet("font-size: 12px; color: #777; background-color: transparent;")  # 更小的字体，更淡的颜色，透明背景
        self.extra_label.setContentsMargins(5, 0, 5, 0)  # 添加一些边距
        self.extra_label.setMinimumWidth(100)  # 设置最小宽度以避免布局问题
        
        # 将额外标签插入到标题标签之后，这样标题和文件名就会一起显示在左侧
        # 布局顺序：颜色块 → #数字 → 文件名 → 拉伸空间 → 操作按钮
        layout = self.header.layout()
        
        # 找到标题标签的位置
        title_label_index = layout.indexOf(self.title_label)
        if title_label_index != -1:
            # 插入到标题标签之后
            layout.insertWidget(title_label_index + 1, self.extra_label)
        else:
            # 如果找不到标题标签，就插入到布局末尾
            layout.addWidget(self.extra_label)
        
        # 找到切换按钮的位置
        toggle_btn_index = layout.indexOf(self.toggle_btn)
        
        # 添加删除按钮
        if not self.is_default:
            # 删除按钮
            delete_btn = QPushButton("X")
            delete_btn.setFixedSize(20, 20)
            delete_btn.setStyleSheet(styles.DELETE_BUTTON_STYLE)
            delete_btn.clicked.connect(self.delete_requested.emit)
            
            if toggle_btn_index != -1:
                # 插入到切换按钮之后
                layout.insertWidget(toggle_btn_index + 1, delete_btn, alignment=Qt.AlignmentFlag.AlignTop)
            else:
                # 如果找不到切换按钮，就插入到布局末尾
                layout.addWidget(delete_btn, alignment=Qt.AlignmentFlag.AlignTop)
        
        self._init_content()
        self.setFixedHeight(36)
    
    def _generate_unit_code(self) -> str:
        """生成6位随机码"""
        import random
        import string
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    def _init_content(self):
        """初始化内容区域"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(0)
        self.content.setLayout(layout)
        
        # 自定义QComboBox，禁用滚轮事件
        class NoWheelComboBox(QComboBox):
            def wheelEvent(self, event):
                # 忽略滚轮事件，不进行任何操作
                event.ignore()
        
        self.file_path_input = NoWheelComboBox()
        self.file_path_input.setPlaceholderText(get_text('operation_file_path'))
        self.file_path_input.setFixedHeight(32)
        self.file_path_input.setEditable(True)  # 改为可编辑，以便显示JSON中的值
        self.file_path_input.setStyleSheet(styles.COMBOBOX_STYLE)
        self.file_path_input.currentTextChanged.connect(self._on_content_changed)
        layout.addWidget(self.file_path_input)
        
        self.code_input = QPlainTextEdit()
        self.code_input.setPlaceholderText(get_text('exec_code', self.lang))
        self.code_input.setFixedHeight(88)
        self.code_input.setStyleSheet(styles.PLAINTEXT_EDIT_STYLE)
        self.code_input.textChanged.connect(self._on_content_changed)
        self.code_input.mouseDoubleClickEvent = self._on_code_double_click
        layout.addWidget(self.code_input)
        
        self.content.setFixedHeight(160)
    
    def set_index(self, index: int):
        """设置索引"""
        self.index = index
        self.set_title(f"#{index}")
    
    def get_data(self) -> dict:
        """获取数据"""
        return {
            "filePath": self.file_path_input.currentText(),
            "execCode": self.code_input.toPlainText()
        }
    
    def set_data(self, data: dict):
        """设置数据"""
        self._pending_file_path = data.get("filePath", "")
        self._saved_file_path = self._pending_file_path  # 保存当前设置的文件路径
        self.code_input.setPlainText(data.get("execCode", ""))
        
        # 如果已经有配置目录，则重新加载文件列表以应用文件路径
        if self.config_dir:
            self.load_config_files(self.config_dir)
        else:
            # 如果还没有配置目录，直接更新标签
            file_path = data.get("filePath", "")
            if file_path:
                self.extra_label.setText(file_path)
            else:
                self.extra_label.setText("")
    
    def load_config_files(self, config_dir: str):
        """加载Config目录下的文件"""
        self.config_dir = config_dir
        if not os.path.exists(config_dir):
            return
        
        files = []
        try:
            for item in os.listdir(config_dir):
                item_path = os.path.join(config_dir, item)
                if os.path.isfile(item_path):
                    files.append(item)
        except Exception as e:
            print(f"读取Config目录失败: {e}")
            return
        
        files.sort()
        
        # 保存当前的文件路径（来自JSON的数据）
        current_file_path = self._pending_file_path if self._pending_file_path else self._saved_file_path
        
        self.file_path_input.clear()
        
        for file in files:
            self.file_path_input.addItem(file)
        
        # 严格按照JSON中的值设置文件路径，不管文件是否存在
        if current_file_path:
            self.file_path_input.setCurrentText(current_file_path)
            # 只有在使用了_pending_file_path后才清除它
            if self._pending_file_path:
                self._pending_file_path = None
        
        # 更新额外标签显示的文件路径
        if current_file_path:
            self.extra_label.setText(current_file_path)
        else:
            self.extra_label.setText("")
    
    def set_default_values(self, prefix: str):
        """设置默认值"""
        # 保持文件路径为空
        self.file_path_input.clear()
        # 保持代码内容为空
        self.code_input.setPlainText("")
        
        # 清空额外标签显示的文件路径
        self.extra_label.setText("")
    
    def _on_content_changed(self):
        """内容改变时触发信号"""
        # 更新额外标签显示的文件路径
        current_path = self.file_path_input.currentText()
        if current_path:
            self.extra_label.setText(current_path)
        else:
            self.extra_label.setText("")
        self.content_changed.emit()
    
    def _on_code_double_click(self, event):
        """双击代码框打开编辑窗口"""
        event.accept()
        dialog = TextEditorDialog(self.code_input.toPlainText(), get_text('code_editor_title', self.lang), self.lang, self)
        if dialog.exec() == dialog.DialogCode.Accepted:
            self.code_input.setPlainText(dialog.get_text())
            self.content_changed.emit()





class InfoCard(CollapsibleCard):
    """信息卡片控件"""
    
    def __init__(self, title: str, content: str = "", color=None, parent=None):
        """初始化信息卡片
        
        Args:
            title: 卡片标题
            content: 卡片内容
            color: 卡片颜色
            parent: 父控件
        """
        super().__init__(title, is_default=True, color=color, parent=parent)
        self.content_text = content
        self._init_content()
        # 设置最小高度和最小宽度
        self.setMinimumHeight(36)
        self.setMinimumWidth(500)
        
        # 默认展开信息卡片
        self.is_expanded = True
        self.content.setVisible(True)
        self.toggle_btn.setText("▲")
    
    def _create_header(self) -> QWidget:
        """创建头部（重写父类方法，移除额外按钮）"""
        header = QWidget()
        header.setStyleSheet(styles.HEADER_STYLE)
        
        # 为header添加单击事件处理
        header.mousePressEvent = self._on_header_click
        
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 8, 0)  # 左侧保持0，右侧添加8px边距
        layout.setSpacing(8)
        # 设置垂直对齐方式为顶部
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        header.setLayout(layout)
        
        # 添加左侧颜色块
        if self.color:
            color_block = QWidget()
            color_block.setStyleSheet(f"""
                QWidget {{
                    background-color: {self.color};
                    border: none;
                    border-radius: 2px;
                }}
            """)
            color_block.setFixedSize(4, 20)
            layout.addWidget(color_block)
            
            # 调整标题标签的间距
            layout.addSpacing(4)
        
        self.title_label = QLabel(self.title)
        self.title_label.setStyleSheet(styles.TITLE_LABEL_STYLE)
        layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignTop)
        
        # 添加拉伸空间
        layout.addStretch()
        
        self.toggle_btn = QPushButton("▼")
        self.toggle_btn.setFixedSize(20, 20)
        self.toggle_btn.setStyleSheet(styles.TOGGLE_BUTTON_STYLE)
        self.toggle_btn.clicked.connect(self._on_toggle)
        layout.addWidget(self.toggle_btn, alignment=Qt.AlignmentFlag.AlignTop)
        
        return header
    
    def _init_content(self):
        """初始化内容区域"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(0)
        self.content.setLayout(layout)
        
        self.content_label = QLabel(self.content_text)
        self.content_label.setStyleSheet("""
            QLabel {
                color: #ddd;
                font-size: 12px;
                line-height: 1.4;
            }
        """)
        self.content_label.setWordWrap(True)
        self.content_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.content_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(self.content_label)
        
        # 移除固定高度，让内容自动调整
        self.content.setMinimumHeight(80)
    
    def set_content(self, content: str):
        """设置内容"""
        self.content_text = content
        self.content_label.setText(content)
        # 调整内容区域大小以适应新内容
        self.content.adjustSize()
        # 调整整个卡片的大小
        self.adjustSize()
    
    def set_color(self, color: str):
        """设置颜色"""
        self.color = color
        # 重新创建header以应用新颜色
        old_header = self.header
        layout = self.layout()
        layout.removeWidget(old_header)
        old_header.deleteLater()
        
        self.header = self._create_header()
        layout.insertWidget(0, self.header)


class OptionCard(CollapsibleCard):
    """选项卡片"""
    
    content_changed = pyqtSignal()
    add_exec_unit_requested = pyqtSignal()
    
    def __init__(self, index: int, is_default: bool = False, lang: int = 0, parent=None):
        # 生成随机颜色
        random_color = generate_pastel_color()
        # 先传递空标题，稍后设置
        super().__init__(f"", is_default, random_color, parent)
        self.index = index
        self.lang = lang
        self.exec_units = []
        self.config_dir = None
        
        # 创建额外的标签来显示选项名称
        from PyQt6.QtWidgets import QLabel
        self.extra_label = QLabel()
        self.extra_label.setStyleSheet("font-size: 12px; color: #777; background-color: transparent;")  # 与标题相同大小的字体，透明颜色
        self.extra_label.setContentsMargins(5, 0, 5, 0)  # 添加一些边距
        self.extra_label.setMinimumWidth(100)  # 设置最小宽度以避免布局问题
        
        # 将额外标签插入到标题标签之后，这样标题和选项名称就会一起显示在左侧
        # 布局顺序：颜色块 → 选项 #数字 → 选项名称 → 拉伸空间 → 操作按钮
        layout = self.header.layout()
        
        # 找到标题标签的位置
        title_label_index = layout.indexOf(self.title_label)
        if title_label_index != -1:
            # 插入到标题标签之后
            layout.insertWidget(title_label_index + 1, self.extra_label)
        else:
            # 如果找不到标题标签，就插入到布局末尾
            layout.addWidget(self.extra_label)
        
        # 设置标题为 "选项 #{index}"（使用国际化）
        self.set_title(f"{get_text('option', self.lang)} #{index}")
        
        # 找到切换按钮的位置
        toggle_btn_index = layout.indexOf(self.toggle_btn)
        
        # 添加删除按钮
        if not self.is_default:
            # 删除按钮
            delete_btn = QPushButton("X")
            delete_btn.setFixedSize(20, 20)
            delete_btn.setStyleSheet(styles.DELETE_BUTTON_STYLE)
            delete_btn.clicked.connect(self.delete_requested.emit)
            
            if toggle_btn_index != -1:
                # 插入到切换按钮之后
                layout.insertWidget(toggle_btn_index + 1, delete_btn, alignment=Qt.AlignmentFlag.AlignTop)
            else:
                # 如果找不到切换按钮，就插入到布局末尾
                layout.addWidget(delete_btn, alignment=Qt.AlignmentFlag.AlignTop)
        
        self._init_content()
        self._set_default_name()
    
    def _generate_option_code(self) -> str:
        """生成6位随机码"""
        import random
        import string
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    def _set_default_name(self):
        """设置默认名称"""
        code = self._generate_option_code()
        self.name_input.setText(f"YourOptionName_{code}")
        
        # 更新额外标签显示的选项名称
        self.extra_label.setText(self.name_input.text())
    
    def _init_content(self):
        """初始化内容区域"""
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        self.content.setLayout(layout)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(get_text('placeholder_option_name', self.lang))
        self.name_input.setStyleSheet(styles.INPUT_STYLE)
        self.name_input.textChanged.connect(self._on_content_changed)
        layout.addWidget(self.name_input)
        
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(btn_layout)
        
        self.add_exec_btn = QPushButton(get_text('add_exec_unit', self.lang))
        self.add_exec_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.add_exec_btn.setStyleSheet(styles.BUTTON_STYLE)
        self.add_exec_btn.clicked.connect(self.add_exec_unit_requested.emit)
        btn_layout.addWidget(self.add_exec_btn)
        btn_layout.addStretch()
        
        self.exec_units_container = QWidget()
        exec_layout = QVBoxLayout()
        exec_layout.setContentsMargins(0, 0, 0, 0)
        exec_layout.setSpacing(10)
        exec_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.exec_units_container.setLayout(exec_layout)
        self.exec_units_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.exec_units_container)
    
    def set_index(self, index: int):
        """设置索引"""
        self.index = index
        self.set_title(f"{get_text('option', self.lang)} #{index}")
    
    def add_exec_unit(self, exec_unit: ExecUnitCard):
        """添加执行单元"""
        self.exec_units.append(exec_unit)
        self.exec_units_container.layout().addWidget(exec_unit)
        exec_unit.content_changed.connect(self._on_content_changed)
        exec_unit.delete_requested.connect(lambda u=exec_unit: self.remove_exec_unit(u))
        exec_unit.copy_requested.connect(lambda u=exec_unit: self.copy_exec_unit(u))
        self._update_exec_unit_indices()
    
    def remove_exec_unit(self, exec_unit: ExecUnitCard):
        """移除执行单元"""
        if exec_unit in self.exec_units:
            self.exec_units.remove(exec_unit)
            self.exec_units_container.layout().removeWidget(exec_unit)
            exec_unit.deleteLater()
            self._update_exec_unit_indices()
    
    def copy_exec_unit(self, exec_unit: ExecUnitCard):
        """复制执行单元"""
        import random
        import string
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        new_unit = ExecUnitCard(len(self.exec_units), is_default=False, unit_code=code, lang=self.lang)
        new_unit.set_data(exec_unit.get_data())
        self.add_exec_unit(new_unit)
    
    def _update_exec_unit_indices(self):
        """更新执行单元索引"""
        for i, unit in enumerate(self.exec_units):
            unit.set_index(i)
    
    def get_data(self) -> dict:
        """获取数据"""
        return {
            "optionKey": self.name_input.text(),
            "execUnits": [unit.get_data() for unit in self.exec_units]
        }
    
    def set_data(self, data: dict):
        """设置数据"""
        # 设置选项名称
        self.name_input.setText(data.get("optionKey", ""))
        
        # 更新额外标签显示的选项名称
        option_key = data.get("optionKey", "")
        if option_key:
            self.extra_label.setText(option_key)
        else:
            self.extra_label.setText("")
        
        # 清空现有的执行单元
        for exec_unit in self.exec_units[:]:  # 使用切片复制列表以避免在迭代时修改列表
            self.remove_exec_unit(exec_unit)
        
        # 添加新的执行单元
        exec_units_data = data.get("execUnits", [])
        for i, unit_data in enumerate(exec_units_data):
            exec_unit = ExecUnitCard(i, is_default=(i == 0), lang=self.lang)
            exec_unit.set_data(unit_data)
            self.add_exec_unit(exec_unit)
    
    def load_config_files(self, config_dir: str):
        """加载Config目录下的文件"""
        self.config_dir = config_dir
        for exec_unit in self.exec_units:
            exec_unit.load_config_files(config_dir)
    
    def _on_content_changed(self):
        """内容改变时触发信号"""
        # 更新额外标签显示的选项名称
        option_name = self.name_input.text()
        if option_name:
            self.extra_label.setText(option_name)
        else:
            self.extra_label.setText("")
        self.content_changed.emit()


class XpathCard(CollapsibleCard):
    """Xpath卡片"""
    
    content_changed = pyqtSignal()
    
    def __init__(self, index: int, is_default: bool = False, lang: int = 0, parent=None):
        # 为XpathCard添加固定的深色色块
        fixed_color = "#555555"  # 固定的深色
        super().__init__(f"#{index}", is_default, fixed_color, parent)
        self.index = index
        self.lang = lang
        self.content_height = 200
        self.config_dir = None
        self._pending_file_path = None
        self._saved_file_path = ""  # 保存当前设置的文件路径
        self.xpath_inputs = []  # 存储xpath输入框
        
        # 创建额外的标签来显示文件路径
        from PyQt6.QtWidgets import QLabel
        self.extra_label = QLabel()
        self.extra_label.setStyleSheet("font-size: 12px; color: #777; background-color: transparent;")  # 更小的字体，更淡的颜色，透明背景
        self.extra_label.setContentsMargins(5, 0, 5, 0)  # 添加一些边距
        self.extra_label.setMinimumWidth(100)  # 设置最小宽度以避免布局问题
        
        # 将额外标签插入到标题标签之后，这样标题和文件名就会一起显示在左侧
        # 布局顺序：颜色块 → #数字 → 文件名 → 拉伸空间 → 操作按钮
        layout = self.header.layout()
        
        # 找到标题标签的位置
        title_label_index = layout.indexOf(self.title_label)
        if title_label_index != -1:
            # 插入到标题标签之后
            layout.insertWidget(title_label_index + 1, self.extra_label)
        else:
            # 如果找不到标题标签，就插入到布局末尾
            layout.addWidget(self.extra_label)
        
        # 找到切换按钮的位置
        toggle_btn_index = layout.indexOf(self.toggle_btn)
        
        # 添加删除按钮
        if not self.is_default:
            # 删除按钮
            delete_btn = QPushButton("X")
            delete_btn.setFixedSize(20, 20)
            delete_btn.setStyleSheet(styles.DELETE_BUTTON_STYLE)
            delete_btn.clicked.connect(self.delete_requested.emit)
            
            if toggle_btn_index != -1:
                # 插入到切换按钮之后
                layout.insertWidget(toggle_btn_index + 1, delete_btn, alignment=Qt.AlignmentFlag.AlignTop)
            else:
                # 如果找不到切换按钮，就插入到布局末尾
                layout.addWidget(delete_btn, alignment=Qt.AlignmentFlag.AlignTop)
        
        self._init_content()
        self.setFixedHeight(36)
    
    def _init_content(self):
        """初始化内容区域"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        self.content.setLayout(layout)
        
        # 自定义QComboBox，禁用滚轮事件
        class NoWheelComboBox(QComboBox):
            def wheelEvent(self, event):
                # 忽略滚轮事件，不进行任何操作
                event.ignore()
        
        # 文件选择框
        self.file_path_input = NoWheelComboBox()
        self.file_path_input.setPlaceholderText(get_text('operation_file_path'))
        self.file_path_input.setFixedHeight(32)
        self.file_path_input.setEditable(True)  # 改为可编辑，以便显示JSON中的值
        self.file_path_input.setStyleSheet(styles.COMBOBOX_STYLE)
        self.file_path_input.currentTextChanged.connect(self._on_content_changed)
        layout.addWidget(self.file_path_input)
        
        # 添加Xpath按钮
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        layout.addLayout(btn_layout)
        
        self.add_xpath_btn = QPushButton("+ Add Xpath")
        self.add_xpath_btn.setFixedHeight(32)
        self.add_xpath_btn.setStyleSheet(styles.BUTTON_STYLE)
        self.add_xpath_btn.clicked.connect(self._add_xpath_input)
        btn_layout.addWidget(self.add_xpath_btn)
        btn_layout.addStretch()
        
        # Xpath输入框容器
        self.xpath_container = QWidget()
        self.xpath_container.setStyleSheet("background-color: transparent;border: none;")
        self.xpath_layout = QVBoxLayout()
        self.xpath_layout.setContentsMargins(8, 8, 8, 8)
        self.xpath_layout.setSpacing(4)
        self.xpath_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.xpath_container.setLayout(self.xpath_layout)
        layout.addWidget(self.xpath_container)
        
        # 添加一个不可删除的xpath输入框
        self._add_xpath_input(is_default=True)
        
        # 调整内容高度
        self._adjust_content_height()
    
    def _add_xpath_input(self, is_default=False):
        """添加xpath输入框"""
        from PyQt6.QtWidgets import QLineEdit, QPushButton, QHBoxLayout
        
        # 创建水平布局
        xpath_row_layout = QHBoxLayout()
        xpath_row_layout.setSpacing(8)
        
        # 创建xpath输入框
        xpath_input = QLineEdit()
        xpath_input.setPlaceholderText("Xpath")
        xpath_input.setFixedHeight(32)
        xpath_input.setStyleSheet(styles.INPUT_STYLE)
        xpath_input.textChanged.connect(self._on_content_changed)
        xpath_row_layout.addWidget(xpath_input)
        
        # 添加验证按钮
        validate_btn_text=get_text('validate')
        validate_btn = QPushButton(validate_btn_text)
        validate_btn.setFixedHeight(32)
        validate_btn.setStyleSheet(styles.BUTTON_STYLE)
        validate_btn.clicked.connect(lambda: self._validate_xpath(xpath_input))
        xpath_row_layout.addWidget(validate_btn)
        
        # 存储输入框和是否默认
        self.xpath_inputs.append((xpath_input, is_default))
        
        # 只有非默认的输入框才添加删除按钮
        if not is_default:
            # 删除按钮
            delete_btn = QPushButton("X")
            delete_btn.setFixedHeight(32)
            delete_btn.setFixedWidth(40)
            delete_btn.setStyleSheet(styles.DELETE_BUTTON_STYLE)
            delete_btn.clicked.connect(lambda: self._remove_xpath_input(xpath_input))
            xpath_row_layout.addWidget(delete_btn)
        
        # 添加到布局
        self.xpath_layout.addLayout(xpath_row_layout)
        
        # 调整内容高度
        self._adjust_content_height()
        
        # 触发内容改变信号
        self._on_content_changed()
    
    def _validate_xpath(self, xpath_input, show_notification=True):
        """验证xpath是否可访问
        
        Args:
            xpath_input: XPath输入框
            show_notification: 是否显示通知弹窗，默认True
        """
        from PyQt6.QtWidgets import QApplication
        from .notification_widget import NotificationWidget
        from ..utils import XpathHandler
        
        xpath = xpath_input.text().strip()
        if not xpath:
            return
        
        # 构建完整的文件路径
        file_name = self.file_path_input.currentText()
        if file_name and self.config_dir:
            full_file_path = os.path.join(self.config_dir, file_name)
            full_file_path = os.path.normpath(full_file_path)
            
            if os.path.exists(full_file_path):
                # 检查是否是属性选择器
                is_attribute = XpathHandler.is_attribute_selector(xpath)
                
                # 验证是否是可访问的属性
                is_valid_attribute = XpathHandler.validate_attribute_xpath(full_file_path, xpath)
                
                if is_valid_attribute:
                    # 验证通过且是属性，设置绿色边框
                    xpath_input.setStyleSheet("""
                        QLineEdit {
                            padding: 6px 8px;
                            background-color: #252525;
                            border: 1px solid #4CAF50;
                            border-radius: 2px;
                            color: #eee;
                            font-size: 11px;
                        }
                        QLineEdit:hover {
                            border: 1px solid #66BB6A;
                        }
                        QLineEdit:focus {
                            border: 1px solid #4CAF50;
                        }
                    """)
                    # 显示成功通知
                    if show_notification:
                        success_message = f"{get_text('xpath_validation_success')}\nXPath: {xpath}\nFile: {file_name}"
                        notification = NotificationWidget(
                            NotificationWidget.TYPE_SUCCESS,
                            success_message,
                            self.lang,
                            timeout=3000  # 3秒后自动关闭
                        )
                        notification.show()
                elif not is_attribute:
                    # 不是属性，设置红色边框
                    xpath_input.setStyleSheet("""
                        QLineEdit {
                            padding: 6px 8px;
                            background-color: #252525;
                            border: 1px solid #F44336;
                            border-radius: 2px;
                            color: #eee;
                            font-size: 11px;
                        }
                        QLineEdit:hover {
                            border: 1px solid #EF5350;
                        }
                        QLineEdit:focus {
                            border: 1px solid #F44336;
                        }
                    """)
                    # 显示失败通知
                    if show_notification:
                        error_message = f"{get_text('xpath_validation_failed')}\nXPath: {xpath}\n{get_text('error')}: {get_text('not_attribute_selector')}"
                        notification = NotificationWidget(
                            NotificationWidget.TYPE_ERROR,
                            error_message,
                            self.lang,
                            timeout=0  # 不自动关闭
                        )
                        notification.show()
                else:
                    # 是属性但验证失败，设置红色边框
                    xpath_input.setStyleSheet("""
                        QLineEdit {
                            padding: 6px 8px;
                            background-color: #252525;
                            border: 1px solid #F44336;
                            border-radius: 2px;
                            color: #eee;
                            font-size: 11px;
                        }
                        QLineEdit:hover {
                            border: 1px solid #EF5350;
                        }
                        QLineEdit:focus {
                            border: 1px solid #F44336;
                        }
                    """)
                    # 显示失败通知
                    if show_notification:
                        error_message = f"{get_text('xpath_validation_failed')}\nXPath: {xpath}\nFile: {file_name}\n{get_text('error')}: {get_text('attribute_not_accessible')}"
                        notification = NotificationWidget(
                            NotificationWidget.TYPE_ERROR,
                            error_message,
                            self.lang,
                            timeout=0  # 不自动关闭
                        )
                        notification.show()
            else:
                # 文件不存在，设置黄色边框
                xpath_input.setStyleSheet("""
                    QLineEdit {
                        padding: 6px 8px;
                        background-color: #252525;
                        border: 1px solid #FFC107;
                        border-radius: 2px;
                        color: #eee;
                        font-size: 11px;
                    }
                    QLineEdit:hover {
                        border: 1px solid #FFCA28;
                    }
                    QLineEdit:focus {
                        border: 1px solid #FFC107;
                    }
                """)
                # 显示警告通知
                if show_notification:
                    warning_message = f"{get_text('file_not_exists')}\nFile: {file_name}"
                    notification = NotificationWidget(
                        NotificationWidget.TYPE_WARNING,
                        warning_message,
                        self.lang,
                        timeout=3000  # 3秒后自动关闭
                    )
                    notification.show()
        else:
            # 文件路径为空，设置黄色边框
            xpath_input.setStyleSheet("""
                QLineEdit {
                    padding: 6px 8px;
                    background-color: #252525;
                    border: 1px solid #FFC107;
                    border-radius: 2px;
                    color: #eee;
                    font-size: 11px;
                }
                QLineEdit:hover {
                    border: 1px solid #FFCA28;
                }
                QLineEdit:focus {
                    border: 1px solid #FFC107;
                }
            """)
            # 显示警告通知
            if show_notification:
                warning_message = get_text('please_select_file_path')
                notification = NotificationWidget(
                    NotificationWidget.TYPE_WARNING,
                    warning_message,
                    self.lang,
                    timeout=3000  # 3秒后自动关闭
                )
                notification.show()
    
    def _remove_xpath_input(self, xpath_input):
        """移除xpath输入框"""
        # 找到输入框对应的布局
        for i, (input_widget, is_default) in enumerate(self.xpath_inputs):
            if input_widget == xpath_input:
                # 只允许删除非默认的输入框
                if not is_default:
                    # 找到对应的布局项
                    for j in range(self.xpath_layout.count()):
                        layout_item = self.xpath_layout.itemAt(j)
                        if layout_item and layout_item.layout():
                            row_layout = layout_item.layout()
                            for k in range(row_layout.count()):
                                if row_layout.itemAt(k).widget() == xpath_input:
                                    # 移除所有子控件
                                    while row_layout.count():
                                        item = row_layout.takeAt(0)
                                        widget = item.widget()
                                        if widget:
                                            widget.deleteLater()
                                    # 移除布局
                                    self.xpath_layout.removeItem(layout_item)
                                    # 从列表中移除
                                    self.xpath_inputs.pop(i)
                                    # 调整内容高度
                                    self._adjust_content_height()
                                    # 触发内容改变信号
                                    self._on_content_changed()
                                    break
                    break
    
    def _copy_xpath(self, xpath_input):
        """复制xpath表达式"""
        from PyQt6.QtWidgets import QApplication
        
        # 获取当前xpath表达式
        xpath_text = xpath_input.text()
        
        # 复制到剪贴板
        clipboard = QApplication.clipboard()
        clipboard.setText(xpath_text)
    
    def _adjust_content_height(self):
        """调整内容高度"""
        # 基础高度：文件选择框(32) + 按钮行(32) + 间距(10*2)
        base_height = 32 + 32 + 20
        # 每个xpath输入框高度：32 + 间距(8)
        xpath_height = len(self.xpath_inputs) * (32 + 8)
        # 加上上下边距 (20+20=40)
        margins = 40
        # 总高度
        total_height = base_height + xpath_height + margins
        # 设置内容高度
        self.content.setFixedHeight(total_height)
        self.content_height = total_height
    
    def set_index(self, index: int):
        """设置索引"""
        self.index = index
        self.set_title(f"#{index}")
    
    def get_data(self) -> dict:
        """获取数据"""
        # 收集所有xpath表达式
        xpath_list = [input_widget.text() for input_widget, _ in self.xpath_inputs]
        return {
            "filePath": self.file_path_input.currentText(),
            "xpath": xpath_list
        }
    
    def set_data(self, data: dict):
        """设置数据"""
        self._pending_file_path = data.get("filePath", "")
        self._saved_file_path = self._pending_file_path  # 保存当前设置的文件路径
        
        # 清空现有的xpath输入框
        for i in reversed(range(self.xpath_layout.count())):
            layout_item = self.xpath_layout.itemAt(i)
            if layout_item and layout_item.layout():
                row_layout = layout_item.layout()
                while row_layout.count():
                    item = row_layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.deleteLater()
                self.xpath_layout.removeItem(layout_item)
        self.xpath_inputs.clear()
        
        # 添加xpath输入框
        xpath_list = data.get("xpath", [])
        for i, xpath in enumerate(xpath_list):
            self._add_xpath_input(is_default=(i == 0))
            # 设置xpath值
            if self.xpath_inputs:
                input_widget, _ = self.xpath_inputs[i]
                input_widget.setText(xpath)
        
        # 如果没有xpath输入框，添加一个默认的
        if not self.xpath_inputs:
            self._add_xpath_input(is_default=True)
        
        # 如果已经有配置目录，则重新加载文件列表以应用文件路径
        if self.config_dir:
            self.load_config_files(self.config_dir)
        else:
            # 如果还没有配置目录，直接更新标签
            file_path = data.get("filePath", "")
            if file_path:
                self.extra_label.setText(file_path)
            else:
                self.extra_label.setText("")
        
        # 移除自动验证功能
        # 验证xpath是否可访问的代码已移除，现在需要点击验证按钮才会验证
    
    def load_config_files(self, config_dir: str):
        """加载Config目录下的文件"""
        self.config_dir = config_dir
        if not os.path.exists(config_dir):
            return
        
        files = []
        try:
            for item in os.listdir(config_dir):
                item_path = os.path.join(config_dir, item)
                if os.path.isfile(item_path):
                    files.append(item)
        except Exception as e:
            print(f"读取Config目录失败: {e}")
            return
        
        files.sort()
        
        # 保存当前的文件路径（来自JSON的数据）
        current_file_path = self._pending_file_path if self._pending_file_path else self._saved_file_path
        
        self.file_path_input.clear()
        
        for file in files:
            self.file_path_input.addItem(file)
        
        # 严格按照JSON中的值设置文件路径，不管文件是否存在
        if current_file_path:
            self.file_path_input.setCurrentText(current_file_path)
            # 只有在使用了_pending_file_path后才清除它
            if self._pending_file_path:
                self._pending_file_path = None
        
        # 更新额外标签显示的文件路径
        if current_file_path:
            self.extra_label.setText(current_file_path)
        else:
            self.extra_label.setText("")
    
    def set_default_values(self):
        """设置默认值"""
        # 只清除当前选择的文件路径，不清除文件列表
        self.file_path_input.setCurrentText("")
        # 清空xpath输入框
        for input_widget, _ in self.xpath_inputs:
            input_widget.clear()
        # 清空额外标签显示的文件路径
        self.extra_label.setText("")
    
    def _on_content_changed(self):
        """内容改变时触发信号"""
        # 更新额外标签显示的文件路径
        current_path = self.file_path_input.currentText()
        if current_path:
            self.extra_label.setText(current_path)
        else:
            self.extra_label.setText("")
        self.content_changed.emit()
