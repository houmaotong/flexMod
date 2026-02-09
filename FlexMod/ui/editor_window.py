"""编辑器窗口"""
import os
import sys
import random
import string
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QListWidget, QListWidgetItem, QPushButton, QLabel,
                             QScrollArea, QFrame, QSplitter, QPlainTextEdit,
                             QLineEdit, QComboBox, QStackedWidget, QFileDialog,
                             QWidgetAction, QMessageBox, QSizePolicy, QApplication)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QIcon

from ..models import Block, BlockType, Group
from ..managers import BlockManager, GroupManager, JsonManager, resource_manager
from ..ui import CustomListItemWidget, CodeEditorWindow
from ..ui.collapsible_widgets import ExecUnitCard, OptionCard
from ..ui.text_editor import TextEditorDialog
from ..ui.notification_widget import NotificationWidget

from ..utils.lang import get_text, get_lang


class FilePathComboBox(QWidget):
    """文件路径下拉输入框"""
    
    def __init__(self, lang: int = 0, parent=None):
        super().__init__(parent)
        self.lang = lang
        self._init_ui()
    
    def _init_ui(self):
        """初始化UI"""
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
        
        self.input = QLineEdit()
        self.input.setPlaceholderText(get_text('placeholder_config_path', self.lang))
        self.input.setStyleSheet("""
            QLineEdit {
                padding: 8px 10px;
                background-color: #2f2f2f;
                border: 1px solid #444;
                border-radius: 3px 0 0 3px;
                color: white;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 1px solid #0e639c;
            }
        """)
        layout.addWidget(self.input)
        
        self.combo = QComboBox()
        self.combo.setFixedWidth(40)
        self.combo.setEditable(False)
        self.combo.addItems(["▼"])
        self.combo.setStyleSheet("""
            QComboBox {
                padding: 8px 5px;
                background-color: #2f2f2f;
                border: 1px solid #444;
                border-left: none;
                border-radius: 0 3px 3px 0;
                color: white;
                font-size: 12px;
            }
            QComboBox:hover {
                background-color: #3f3f3f;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
                background-color: transparent;
            }
            QComboBox::down-arrow {
                width: 10px;
                height: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: #2f2f2f;
                border: 1px solid #444;
                selection-background-color: #0e639c;
                selection-color: white;
            }
        """)
        self.combo.currentIndexChanged.connect(self._on_combo_changed)
        layout.addWidget(self.combo)
    
    def setText(self, text: str):
        """设置文本"""
        self.input.setText(text)
    
    def text(self) -> str:
        """获取文本"""
        return self.input.text()
    
    def setPlaceholderText(self, text: str):
        """设置占位符文本"""
        self.input.setPlaceholderText(text)
    
    def setObjectName(self, name: str):
        """设置对象名称"""
        self.input.setObjectName(name)
    
    def load_config_files(self, config_dir: str):
        """加载Config目录下的文件"""
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
        
        self.combo.clear()
        self.combo.addItem("▼")
        
        for file in files:
            self.combo.addItem(file)
    
    def _on_combo_changed(self, index: int):
        """下拉框选项改变"""
        if index > 0:
            file_name = self.combo.itemText(index)
            
            self.input.setText(file_name)
            
            self.combo.setCurrentIndex(0)
            
            if hasattr(self, 'text_changed_callback') and self.text_changed_callback:
                self.text_changed_callback()
    
    def textChanged(self, callback):
        """设置文本改变回调"""
        self.text_changed_callback = callback




class FlexModEditorWindow(QMainWindow):
    """FlexMod编辑器主窗口"""
    
    def __init__(self, mod_name: str, json_file_path: str):
        super().__init__()
        self.mod_name = mod_name
        self.json_file_path = json_file_path
        
        self.block_manager = BlockManager()
        self.group_manager = GroupManager()
        self.json_manager = JsonManager(json_file_path, self.block_manager, self.group_manager)

        
        self.current_block_id = None
        self.code_window = None
        self.lang = get_lang()  # 总是从配置文件中读取最新的语言设置
        # 构建并规范化配置目录路径
        self.config_dir = os.path.join(os.path.dirname(json_file_path), '..', 'Config')
        self.config_dir = os.path.normpath(self.config_dir)
        
        # 添加锁定状态，默认为锁定
        self.is_locked = True
        
        self._init_ui()
        self._load_data()
    
    def _init_ui(self):
        """初始化UI"""
        self.setWindowTitle(f"FlexMod - {self.mod_name}")
        self.setWindowIcon(resource_manager.get_app_icon())
        self.setGeometry(100, 100, 1600, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        header = self._create_header()
        main_layout.addWidget(header)
        
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        left_panel = self._create_left_panel()
        content_splitter.addWidget(left_panel)
        
        right_splitter = self._create_right_splitter()
        content_splitter.addWidget(right_splitter)
        
        content_splitter.setStretchFactor(0, 1)
        content_splitter.setStretchFactor(1, 3)
        
        main_layout.addWidget(content_splitter)
        
        central_widget.setLayout(main_layout)
        
        # 初始化时应用锁定状态
        self._set_editable(not self.is_locked)
        
        # 将窗口居中显示
        from ..utils.window_utils import WindowUtils
        WindowUtils.center_window(self)
    
    def _create_header(self) -> QFrame:
        """创建头部"""
        header = QFrame()
        header.setStyleSheet("background-color: #2d2d2d; border-bottom: 1px solid #3d3d3d;")
        header.setFixedHeight(50)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(16, 8, 16, 8)
        
        # 添加锁定/解锁按钮
        self.lock_btn = QPushButton()
        self.lock_btn.setFixedSize(24, 24)
        self.lock_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 30);
                border-radius: 12px;
            }
        """)
        # 设置默认为锁定图标
        self._update_lock_icon()
        self.lock_btn.clicked.connect(self._toggle_lock)
        layout.addWidget(self.lock_btn)
        
        title = QLabel(f"{get_text('flexmod_editor_title', self.lang)} - {self.mod_name}")
        title.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        
        layout.addStretch()
        
        self.code_btn = QPushButton(get_text('view_json_code', self.lang))
        self.code_btn.setStyleSheet("""
            QPushButton {
                background-color: #0e639c;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #1177bb;
            }
        """)
        self.code_btn.clicked.connect(self._toggle_json_preview)
        layout.addWidget(self.code_btn)
        
        # 添加验证数据按钮
        self.validate_btn = QPushButton(get_text('validate_data', self.lang))
        self.validate_btn.setStyleSheet("""
            QPushButton {
                background-color: #2d8f5a;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 13px;
                margin-left: 8px;
            }
            QPushButton:hover {
                background-color: #37a669;
            }
        """)
        self.validate_btn.clicked.connect(self._open_validate_window)
        layout.addWidget(self.validate_btn)
        
        # 初始化验证窗口引用
        self.validate_window = None
        
        header.setLayout(layout)
        return header
    
    def _update_lock_icon(self):
        """更新锁定图标"""
        from PyQt6.QtGui import QPixmap, QIcon
        if self.is_locked:
            # 显示锁定图标
            icon_path = self._get_resource_path("icons", "lock.png")
        else:
            # 显示解锁图标
            icon_path = self._get_resource_path("icons", "unlock.png")
        
        # 尝试加载图标
        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            icon = QIcon(pixmap)
            self.lock_btn.setIcon(icon)
        else:
            # 如果图标加载失败，使用文本表示
            if self.is_locked:
                self.lock_btn.setText("🔒")
            else:
                self.lock_btn.setText("🔓")
    
    def _get_resource_path(self, resource_type: str, filename: str) -> str:
        """获取资源文件路径"""
        from pathlib import Path
        from ..managers import resource_manager
        resource_dir = resource_manager._resources_dir / resource_type
        return str(resource_dir / filename)
    
    def _toggle_lock(self):
        """切换锁定状态"""
        self.is_locked = not self.is_locked
        self._update_lock_icon()
        
        # 根据锁定状态启用/禁用编辑功能
        self._set_editable(not self.is_locked)
    
    def _set_editable(self, editable: bool):
        """设置编辑状态"""
        # 禁用或启用左侧功能块列表的编辑功能
        self.block_list.setEnabled(editable)
        
        # 禁用或启用添加功能块区域
        for child in self.findChildren(QWidget):
            # 检查对象名称或文本中包含"add"或"添加"的控件
            obj_name = getattr(child, 'objectName', lambda: '')()
            text_val = getattr(child, 'text', lambda: '')()
            
            # 检查是否是添加类控件
            is_add_control = ('add' in obj_name.lower() or '添加' in obj_name.lower() or 
                              'add' in text_val.lower() or '添加' in text_val)
            
            # 排除锁定按钮，对添加类控件按编辑状态设置
            if child != self.lock_btn and is_add_control:
                child.setEnabled(editable)
        
        # 对于右侧详情面板，所有编辑相关的控件都由_apply_lock_to_widgets统一控制
        self._apply_lock_to_widgets(self.centralWidget(), editable)
        
        # 重要：确保锁定按钮始终可用，以便用户可以切换锁定状态
        self.lock_btn.setEnabled(True)
    
    def _apply_lock_to_widgets(self, widget: QWidget, editable: bool):
        """递归地应用锁定状态到所有子控件"""
        for child in widget.findChildren(QWidget):
            if isinstance(child, (QLineEdit, QPlainTextEdit, QComboBox, QPushButton)):
                # 特殊处理锁定按钮，始终让它保持可用
                if child == self.lock_btn:
                    continue  # 不改变锁定按钮的状态
                
                # 所有编辑控件都根据editable参数设置状态
                # 在锁定状态下(editable=False)，所有编辑控件都被禁用
                # 在解锁状态下(editable=True)，所有编辑控件都被启用
                child.setEnabled(editable)
    
    def _create_left_panel(self) -> QWidget:
        """创建左侧面板"""
        panel = QWidget()
        panel.setStyleSheet("background-color: #252526;")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        header = QLabel(get_text('block_list', self.lang))
        header.setStyleSheet("color: white; font-size: 12px; padding: 8px 16px; background-color: #2d2d2d;")
        layout.addWidget(header)
        
        self.block_list = QListWidget()
        self.block_list.setStyleSheet("""
            QListWidget {
                background-color: #252526;
                border: none;
            }
            QListWidget::item {
                padding: 4px 8px;
            }
            QScrollBar:vertical {
                background: #2d2d2d;
                width: 10px;
            }
            QScrollBar::handle:vertical {
                background: #4e4e52;
                border-radius: 5px;
            }
        """)
        self.block_list.itemClicked.connect(self._on_block_item_clicked)
        layout.addWidget(self.block_list)
        
        add_section = self._create_add_block_section()
        layout.addWidget(add_section)
        
        panel.setLayout(layout)
        return panel
    
    def _create_add_block_section(self) -> QWidget:
        """创建添加功能块区域"""
        section = QWidget()
        section.setStyleSheet("background-color: #2d2d2d; border-top: 1px solid #3d3d3d;")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 8, 12, 8)
        
        self.add_block_toggle = QPushButton(f"{get_text('add_block', self.lang)} ▾")
        self.add_block_toggle.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #ccc;
                border: none;
                padding: 4px 8px;
                font-size: 12px;
            }
            QPushButton:hover {
                color: white;
            }
        """)
        self.add_block_toggle.clicked.connect(self._toggle_add_block_section)
        layout.addWidget(self.add_block_toggle)
        
        self.add_block_buttons = QWidget()
        buttons_layout = QVBoxLayout()
        
        button_configs = [
            ('switch', f"⚡ {get_text('block_type_bool', self.lang)}"),
            ('option', f"📋 {get_text('block_type_dropdown', self.lang)}"),
            ('int-slider', f"🔢 {get_text('block_type_int_slider', self.lang)}"),
            ('float-slider', f"📊 {get_text('block_type_float_slider', self.lang)}")
        ]
        
        for block_type, text in button_configs:
            btn = QPushButton(text)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3e3e42;
                    color: white;
                    border: none;
                    padding: 8px 12px;
                    border-radius: 3px;
                    font-size: 12px;
                    margin-top: 4px;
                }
                QPushButton:hover {
                    background-color: #4e4e52;
                }
            """)
            btn.clicked.connect(lambda checked, bt=block_type: self._create_block(bt))
            buttons_layout.addWidget(btn)
        
        self.add_block_buttons.setLayout(buttons_layout)
        self.add_block_buttons.hide()
        layout.addWidget(self.add_block_buttons)
        
        section.setLayout(layout)
        return section
    
    def _create_right_panel(self) -> QWidget:
        """创建右侧面板"""
        panel = QWidget()
        panel.setStyleSheet("background-color: #1e1e1e;")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        header = QLabel(get_text('detail_params', self.lang))
        header.setStyleSheet("color: white; font-size: 12px; padding: 8px 16px; background-color: #2d2d2d;")
        layout.addWidget(header)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #1e1e1e;
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #4e4e52;
                border-radius: 5px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #6e6e72;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        self.detail_container = QWidget()
        self.detail_layout = QVBoxLayout()
        self.detail_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.detail_container.setLayout(self.detail_layout)
        scroll_area.setWidget(self.detail_container)
        
        layout.addWidget(scroll_area)
        panel.setLayout(layout)
        return panel
    
    def _create_right_splitter(self) -> QSplitter:
        """创建右侧分割器（包含详情面板和第三列）"""
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        detail_panel = self._create_right_panel()
        splitter.addWidget(detail_panel)
        
        # 创建第三列容器，用于切换显示JSON和验证内容
        self.third_column = QWidget()
        self.third_column.setStyleSheet("background-color: #1e1e1e; border-left: 1px solid #3d3d3d;")
        
        third_layout = QVBoxLayout()
        third_layout.setContentsMargins(0, 0, 0, 0)
        third_layout.setSpacing(0)
        self.third_column.setLayout(third_layout)
        
        # 创建JSON面板
        self.json_panel = self._create_json_panel()
        third_layout.addWidget(self.json_panel)
        
        # 创建验证面板
        self.validate_panel = self._create_validate_panel()
        third_layout.addWidget(self.validate_panel)
        self.validate_panel.hide()  # 默认隐藏验证面板
        
        splitter.addWidget(self.third_column)
        
        # 禁用第三列的自动拉伸
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 0)
        
        return splitter
    
    def _create_json_panel(self) -> QWidget:
        """创建JSON预览面板"""
        panel = QWidget()
        panel.setStyleSheet("background-color: #1e1e1e;")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        header = QLabel(get_text('json_preview', self.lang))
        header.setStyleSheet("color: white; font-size: 12px; padding: 8px 16px; background-color: #2d2d2d;")
        layout.addWidget(header)
        
        self.code_editor = QPlainTextEdit()
        self.code_editor.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
                border: none;
                padding: 8px;
            }
            QScrollBar:vertical {
                background: #2d2d2d;
                width: 10px;
            }
            QScrollBar::handle:vertical {
                background: #4e4e52;
                border-radius: 5px;
            }
        """)
        self.code_editor.setReadOnly(True)
        layout.addWidget(self.code_editor)
        
        panel.setLayout(layout)
        return panel
    
    def _create_validate_panel(self) -> QWidget:
        """创建验证面板"""
        panel = QWidget()
        panel.setStyleSheet("background-color: #1e1e1e;")
        
        layout = QVBoxLayout() # 垂直布局
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.validate_header = QLabel(get_text('validate_results', self.lang))
        self.validate_header.setStyleSheet("color: white; font-size: 12px; padding: 8px 16px; background-color: #2d2d2d;")
        layout.addWidget(self.validate_header)
        
        # 点击全部折叠/展开按钮
        self.toggle_all_btn = QPushButton(get_text('toggle_all', self.lang))
        self.toggle_all_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #eee;
                border: none;
                padding: 4px 8px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        self.toggle_all_btn.clicked.connect(self._toggle_all_cards)
        layout.addWidget(self.toggle_all_btn)
        
        # 添加验证结果卡片容器
        results_container = QWidget()
        results_container.setStyleSheet("background-color: #1e1e1e;")
        self.results_layout = QVBoxLayout()
        self.results_layout.setContentsMargins(16, 16, 16, 16)
        self.results_layout.setSpacing(15)
        self.results_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        results_container.setLayout(self.results_layout)
        
        # 添加滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #1e1e1e;
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #4e4e52;
                border-radius: 5px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #6e6e72;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        scroll_area.setWidget(results_container)
        
        layout.addWidget(scroll_area)
        panel.setLayout(layout)
        return panel
    
    def _toggle_all_cards(self):
        """切换所有验证结果卡片的展开/折叠状态"""
        from ..utils.lang import get_text
        from ..ui.collapsible_widgets import InfoCard
        
        # 确保is_expanded属性存在
        if not hasattr(self, 'is_expanded'):
            self.is_expanded = True
        
        # 切换状态
        self.is_expanded = not self.is_expanded
        
        # 更新按钮文本
        self.toggle_all_btn.setText(get_text('toggle_all_collapsed' if self.is_expanded else 'toggle_all_expanded', self.lang))
        
        # 遍历所有验证结果卡片
        for i in range(self.results_layout.count()):
            widget = self.results_layout.itemAt(i).widget()
            if isinstance(widget, InfoCard):
                # 设置卡片状态
                widget.is_expanded = self.is_expanded
                widget.content.setVisible(self.is_expanded)
                widget.toggle_btn.setText("▲" if self.is_expanded else "▼")

                
    def _toggle_json_preview(self):
        """切换JSON预览显示"""
        # 隐藏验证面板，显示JSON面板
        self.validate_panel.hide()
        if self.json_panel.isVisible():
            self.json_panel.hide()
            self.third_column.hide()  # 隐藏第三列
        else:
            self.json_panel.show()
            self.third_column.show()  # 显示第三列
    
    def _open_validate_window(self):
        """显示验证面板并自动执行验证"""
        # 隐藏JSON面板，显示验证面板
        self.json_panel.hide()
        self.validate_panel.show()
        self.third_column.show()  # 显示第三列
        # 自动执行验证
        self._perform_validation()
    
    def _perform_validation(self):
        """执行验证操作"""
        import os
        from ..utils.lang import get_text, get_lang
        from ..utils.xml_operations import XmlOperations
        from ..ui.collapsible_widgets import InfoCard
        
        # 更新当前语言设置
        self.lang = get_lang()
        # 更新验证结果标题
        if hasattr(self, 'validate_header'):
            self.validate_header.setText(get_text('validate_results', self.lang))
        
        # 清空之前的验证结果
        for i in reversed(range(self.results_layout.count())):
            widget = self.results_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # 获取FlexMod JSON文件路径
        json_path = self.json_manager.file_path
        
        # 获取mod文件目录
        mod_files_dir = os.path.dirname(json_path)
        
        try:
            # 检查缺少的注释
            missing_comments = XmlOperations.check_missing_comments(json_path, mod_files_dir)
            
            # 添加缺少注释卡片
            if missing_comments:
                missing_card = InfoCard(
                    title=get_text('validate_missing_comments_title', self.lang),
                    content=get_text('validate_missing_comments_content', self.lang) + "\n\n",
                    color="#b42828"
                )
                content = get_text('validate_missing_comments_content', self.lang) + "\n\n"
                for file_path, ids in missing_comments.items():
                    for block_id in ids:
                        content += get_text('validate_missing_comment_item', self.lang).format(file_path, block_id) + "\n"
                missing_card.set_content(content)
                self.results_layout.addWidget(missing_card)
            
            # 检查多余的注释
            extra_comments = XmlOperations.check_extra_comments(json_path, mod_files_dir)
            
            # 添加多余注释卡片
            if extra_comments:
                extra_card = InfoCard(
                    title=get_text('validate_extra_comments_title', self.lang),
                    content=get_text('validate_extra_comments_content', self.lang) + "\n\n",
                    color="#b42828"
                )
                content = get_text('validate_extra_comments_content', self.lang) + "\n\n"
                for file_path, ids in extra_comments.items():
                    for block_id in ids:
                        content += get_text('validate_extra_comment_item', self.lang).format(file_path, block_id) + "\n"
                extra_card.set_content(content)
                self.results_layout.addWidget(extra_card)
            
            # 检查不存在的文件
            nonexistent_files = XmlOperations.check_nonexistent_files(json_path, mod_files_dir)
            
            # 添加不存在文件卡片
            if nonexistent_files:
                nonexistent_card = InfoCard(
                    title=get_text('validate_nonexistent_files_title', self.lang),
                    content=get_text('validate_nonexistent_files_content', self.lang) + "\n\n",
                    color="#b42828"
                )
                content = get_text('validate_nonexistent_files_content', self.lang) + "\n\n"
                for file_path, id_pairs in nonexistent_files.items():
                    for block_id, display_name in id_pairs:
                        content += get_text('validate_nonexistent_file_item', self.lang).format(file_path, block_id, display_name) + "\n"
                nonexistent_card.set_content(content)
                self.results_layout.addWidget(nonexistent_card)
            
            # 如果没有问题，添加成功卡片
            if not missing_comments and not extra_comments and not nonexistent_files:
                success_card = InfoCard(
                    title=get_text('validate_success_title', self.lang),
                    content=get_text('validate_success_content', self.lang),
                    color="#4ECDC4"
                )
                self.results_layout.addWidget(success_card)
        except Exception as e:
            # 显示错误信息
            error_card = InfoCard(
                title=get_text('validate_error_title', self.lang),
                content=f"{get_text('validate_error_content', self.lang)}\n\n{str(e)}",
                color="#b42828"
            )
            self.results_layout.addWidget(error_card)
    
    def _load_data(self):
        """加载数据"""
        self.json_manager.validate_and_fix()
        self.json_manager.load()
        
        self._refresh_block_list()
        self._update_code_editor()
    
    def _refresh_block_list(self):
        """刷新功能块列表"""
        self.block_list.clear()
        
        group_item = QListWidgetItem()
        group_widget = CustomListItemWidget(get_text('group_settings', self.lang), 'group')
        group_widget.delete_btn.hide()
        group_item.setSizeHint(group_widget.sizeHint())
        self.block_list.addItem(group_item)
        self.block_list.setItemWidget(group_item, group_widget)
        
        for block in self.block_manager.get_all_blocks():
            item = QListWidgetItem()
            widget = CustomListItemWidget(
                block.get_parameter('func_name', get_text('placeholder_unnamed_config', self.lang)),
                block.block_type.get_display_name(self.lang)
            )
            widget.delete_clicked.connect(lambda: self._delete_block(item))
            item.setSizeHint(widget.sizeHint())
            item.setData(1, block.block_id)
            self.block_list.addItem(item)
            self.block_list.setItemWidget(item, widget)
    
    def _update_code_editor(self):
        """更新代码编辑器"""
        content = self.json_manager.get_json_content()
        self.code_editor.setPlainText(content)
        
        if self.code_window:
            self.code_window.set_content(content)
    
    def _update_language(self):
        """更新UI语言"""
        # 更新窗口标题
        self.setWindowTitle(f"FlexMod - {self.mod_name}")
        
        # 更新头部
        header = self.findChild(QFrame)
        if header:
            title_label = header.findChild(QLabel)
            if title_label:
                title_label.setText(f"{get_text('flexmod_editor_title', self.lang)} - {self.mod_name}")
        
        # 更新代码按钮
        if hasattr(self, 'code_btn'):
            self.code_btn.setText(get_text('view_json_code', self.lang))
        
        # 更新左侧面板
        left_panel = self.findChild(QWidget)
        if left_panel:
            header_label = left_panel.findChild(QLabel)
            if header_label:
                header_label.setText(get_text('block_list', self.lang))
        
        # 更新右侧面板
        right_panel = self.findChild(QSplitter)
        if right_panel:
            for widget in right_panel.findChildren(QWidget):
                header_label = widget.findChild(QLabel)
                if header_label and header_label.text() in [get_text('detail_params', 0), get_text('detail_params', 1)]:
                    header_label.setText(get_text('detail_params', self.lang))
                elif header_label and header_label.text() in [get_text('json_preview', 0), get_text('json_preview', 1)]:
                    header_label.setText(get_text('json_preview', self.lang))
        
        # 刷新功能块列表
        if hasattr(self, '_refresh_block_list'):
            self._refresh_block_list()
        
        # 更新代码编辑器
        if hasattr(self, '_update_code_editor'):
            self._update_code_editor()
    
    def _highlight_block_in_json(self, block_id):
        """在JSON预览中滚动到指定的功能块ID所在行"""
        if not block_id:
            return
        
        # 获取功能块的func_id参数
        block = self.block_manager.get_block(block_id)
        if not block:
            return
        
        func_id = block.get_parameter('func_id', f'config_{block_id}')
        
        # 获取JSON内容
        json_content = self.code_editor.toPlainText()
        if not json_content:
            return
        
        # 尝试不同的搜索模式，以匹配不同的JSON格式
        search_patterns = [
            f'"uniqueId": "{func_id}"',
            f'"uniqueId": "{func_id}",',
            f'"uniqueId":\n"{func_id}"',
            f'"uniqueId":\n"{func_id}",',
            f'"uniqueId": "{func_id}"\n',
            f'"uniqueId": "{func_id}",\n'
        ]
        
        start_pos = -1
        
        # 尝试所有搜索模式
        for pattern in search_patterns:
            start_pos = json_content.find(pattern)
            if start_pos != -1:
                break
        
        if start_pos != -1:
            # 计算行号
            lines_before = json_content[:start_pos].count('\n')
            
            # 滚动到行并将其显示在顶部
            block = self.code_editor.document().findBlockByNumber(lines_before)
            if block.isValid():
                # 设置光标位置到目标行
                cursor = self.code_editor.textCursor()
                cursor.setPosition(block.position())
                self.code_editor.setTextCursor(cursor)
                
                # 使用滚动条将目标行滚动到顶部
                scroll_bar = self.code_editor.verticalScrollBar()
                scroll_bar.setValue(lines_before * 20)  # 估算每行高度为20像素
                
                # 再次确保可见
                self.code_editor.ensureCursorVisible()
    
    def _on_block_item_clicked(self, item):
        """处理列表项点击事件"""
        widget = self.block_list.itemWidget(item)
        if not widget:
            return
        
        item_text = widget.name
        block_id = item.data(1)
        

        
        if self.current_block_id:
            self._save_current_block_state()
        
        if widget.block_type == 'group':
            self._show_group_detail_panel()
        else:
            if block_id:
                self._show_block_detail_panel(block_id)
        
        self._update_code_editor()
        
        # 在JSON预览中高亮显示当前功能块
        if block_id:
            self._highlight_block_in_json(block_id)
        

    
    def _save_current_block_state(self):
        """保存当前功能块状态"""
        if not self.current_block_id:
            return
        
        block = self.block_manager.get_block(self.current_block_id)
        if not block:
            return
        
        old_name = block.get_parameter('func_name', '')
        parameters = block.parameters.copy()
        
        for i in range(self.detail_layout.count()):
            widget = self.detail_layout.itemAt(i).widget()
            if widget:
                for child in widget.findChildren(QLineEdit):
                    parameters[child.objectName()] = child.text()
                for child in widget.findChildren(QComboBox):
                    parameters[child.objectName()] = child.currentText()
                for child in widget.findChildren(QPlainTextEdit):
                    parameters[child.objectName()] = child.toPlainText()
                for child in widget.findChildren(FilePathComboBox):
                    parameters[child.objectName()] = child.text()
        
        true_exec_units = []
        false_exec_units = []
        option_items = []
        
        # 只查找当前详细布局中的ExecUnitCard，避免包含旧卡片
        for i in range(self.detail_layout.count()):
            widget = self.detail_layout.itemAt(i).widget()
            if widget:
                for child in widget.findChildren(ExecUnitCard):
                    parent_container = child.parent()
                    while parent_container:
                        if parent_container.layout() and parent_container.layout().indexOf(child) >= 0:
                            break
                        parent_container = parent_container.parent()
                    
                    if parent_container:
                        grandparent = parent_container.parent()
                        if grandparent:
                            group_label = None
                            for sibling in grandparent.findChildren(QLabel):
                                if sibling.text() in [get_text('true_code', self.lang), get_text('false_code', self.lang)]:
                                    group_label = sibling.text()
                                    break
                            
                            if group_label == get_text('true_code', self.lang):
                                true_exec_units.append(child.get_data())
                            elif group_label == get_text('false_code', self.lang):
                                false_exec_units.append(child.get_data())
        
        # 获取当前块的类型
        block_type = block.block_type
        
        # 只查找当前详细布局中的OptionCard，避免包含旧卡片
        current_option_cards = []
        for i in range(self.detail_layout.count()):
            widget = self.detail_layout.itemAt(i).widget()
            if widget:
                current_option_cards.extend(widget.findChildren(OptionCard))
        
        # 如果是OPTION类型的块（对应selectConfig），需要特殊处理option_items
        # 避免因界面未完全加载导致option_items被清空
        if block_type == BlockType.OPTION and len(current_option_cards) == 0:
            # 如果当前没有找到OptionCard，保留原有的option_items数据
            option_items = block.get_parameter('option_items', [])
        else:
            # 否则正常收集当前OptionCard的数据
            for child in current_option_cards:
                option_items.append(child.get_data())
        
        parameters['true_exec_units'] = true_exec_units
        parameters['false_exec_units'] = false_exec_units
        parameters['option_items'] = option_items
        
        # 收集XpathCard数据
        from ..ui.collapsible_widgets import XpathCard
        xpath_cards = []
        # 只查找当前详细布局中的XpathCard，避免包含旧卡片
        for i in range(self.detail_layout.count()):
            widget = self.detail_layout.itemAt(i).widget()
            if widget:
                xpath_cards.extend(widget.findChildren(XpathCard))
        xpath_sets = []
        for card in xpath_cards:
            xpath_sets.append(card.get_data())
        parameters['XpathSet'] = xpath_sets
        
        block.parameters = parameters
        new_name = block.get_parameter('func_name', '')
        if old_name != new_name:
            self._refresh_block_list()
        self.json_manager.save()
    
    def _show_group_detail_panel(self):
        """显示分组设置面板"""
        self._clear_detail_layout()
        self.current_block_id = None
        
        title = QLabel(f"📁 {get_text('group_settings', self.lang)}")
        title.setStyleSheet("font-size: 16px; color: white; margin-bottom: 20px;")
        self.detail_layout.addWidget(title)
        
        for group in self.group_manager.get_all_groups():
            self._add_group_card(group)
        
        add_btn = QPushButton(f"+ {get_text('add_group', self.lang)}")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #0e639c;
                color: white;
                border: none;
                padding: 10px 16px;
                border-radius: 4px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #1177bb;
            }
        """)
        add_btn.clicked.connect(self._add_group)
        self.detail_layout.addWidget(add_btn)
    
    def _add_group_card(self, group: Group):
        """添加分组卡片"""
        card = QWidget()
        card.setStyleSheet("""
            QWidget {
                background-color: #2a2a2a;
                border: 1px solid #444;
                border-radius: 3px;
                margin-bottom: 8px;
            }
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(0)
        
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(8)
        
        inputs_layout = QVBoxLayout()
        inputs_layout.setContentsMargins(0, 0, 0, 10)
        inputs_layout.setSpacing(0)
        
        name_input = QLineEdit(group.name)
        name_input.setReadOnly(group.is_default)
        name_input.setObjectName(f"group_name_{group.name}")
        name_input.setStyleSheet("""
            QLineEdit {
                background-color: #1e1e1e;
                color: white;
                border: 1px solid #444;
                padding: 6px 8px;
                border-radius: 3px;
                font-size: 12px;
                margin: 0px;
            }
        """)
        if not group.is_default:
            name_input.returnPressed.connect(lambda: self._save_group_state(group.name, card))
            name_input.editingFinished.connect(lambda: self._save_group_state(group.name, card))
        inputs_layout.addWidget(name_input)
        
        desc_input = QLineEdit(group.desc)
        desc_input.setPlaceholderText(get_text('placeholder_group_desc', self.lang))
        desc_input.setObjectName(f"group_desc_{group.name}")
        desc_input.setStyleSheet("""
            QLineEdit {
                background-color: #1e1e1e;
                color: white;
                border: 1px solid #444;
                padding: 6px 8px;
                border-radius: 3px;
                font-size: 10px;
                margin: 0px;
            }
        """)
        if not group.is_default:
            desc_input.returnPressed.connect(lambda: self._save_group_state(group.name, card))
            desc_input.editingFinished.connect(lambda: self._save_group_state(group.name, card))
            # 添加双击事件处理
            desc_input.mouseDoubleClickEvent = lambda event, g=group, d=desc_input: self._on_desc_double_click(event, g, d)
        inputs_layout.addWidget(desc_input)
        
        content_layout.addLayout(inputs_layout)
        
        if not group.is_default:
            delete_btn = QPushButton(get_text('delete', self.lang))
            delete_btn.setStyleSheet("""
                QPushButton {
                    padding: 4px 8px;
                    background-color: #b42828;
                    border: none;
                    border-radius: 2px;
                    color: #fff;
                    font-size: 10px;
                }
                QPushButton:hover {
                    background-color: #d43838;
                }
            """)
            delete_btn.clicked.connect(lambda: self._remove_group(group.name, card))
            content_layout.addWidget(delete_btn)
        
        main_layout.addLayout(content_layout)
        card.setLayout(main_layout)
        self.detail_layout.addWidget(card)
    
    def _add_group(self):
        """添加分组"""
        group_name = self.group_manager.generate_group_name()
        group = Group(name=group_name, desc='', is_default=False)
        self.group_manager.add_group(group)
        self._show_group_detail_panel()
        self.json_manager.save()
        self._update_code_editor()
    
    def _remove_group(self, group_name: str, card: QWidget):
        """移除分组"""
        self.group_manager.remove_group(group_name)
        self.detail_layout.removeWidget(card)
        card.deleteLater()
        self.json_manager.save()
        self._update_code_editor()
    
    def _on_desc_double_click(self, event, group, desc_input):
        """描述输入框双击事件"""
        dialog = TextEditorDialog(desc_input.text(), get_text('text_editor_title', self.lang), self.lang, self)
        if dialog.exec() == dialog.DialogCode.Accepted:
            new_desc = dialog.get_text()
            desc_input.setText(new_desc)
            self._save_group_state(group.name, desc_input.parent().parent())
    
    def _on_block_desc_double_click(self, event, desc_input):
        """功能块描述输入框双击事件"""
        dialog = TextEditorDialog(desc_input.text(), get_text('text_editor_title', self.lang), self.lang, self)
        if dialog.exec() == dialog.DialogCode.Accepted:
            new_desc = dialog.get_text()
            desc_input.setText(new_desc)
            self._save_current_block_state()
    
    def _save_group_state(self, old_group_name: str, card: QWidget):
        """保存分组状态"""
        group = self.group_manager.get_group(old_group_name)
        if not group:
            return
        
        new_name = None
        new_desc = None
        
        for child in card.findChildren(QLineEdit):
            if child.objectName() == f"group_name_{old_group_name}":
                new_name = child.text()
            elif child.objectName() == f"group_desc_{old_group_name}":
                new_desc = child.text()
        
        if new_name and new_name != old_group_name:
            # 检查新组名是否已经存在
            if self.group_manager.get_group(new_name):
                # 如果新组名已存在，显示错误消息
                QMessageBox.warning(self, get_text('warning', self.lang), get_text('group_name_exists', self.lang))
                # 恢复原来的组名
                for child in card.findChildren(QLineEdit):
                    if child.objectName() == f"group_name_{old_group_name}":
                        child.setText(old_group_name)
                return
            
            # 如果新组名不存在，更新组名
            group.name = new_name
            self.block_manager.update_group_name(old_group_name, new_name)
            self._refresh_block_list()
        
        if new_desc is not None:
            group.desc = new_desc
        
        self.json_manager.save()
        self._update_code_editor()
    
    def _show_block_detail_panel(self, block_id: str):
        """显示功能块详细参数面板"""
        self._save_current_block_state()
        
        self._clear_detail_layout()
        self.current_block_id = block_id
        
        block = self.block_manager.get_block(block_id)
        if not block:
            return
        
        title = QLabel(f"⚡ {block.block_type.get_display_name(self.lang)}")
        title.setStyleSheet("font-size: 16px; color: white; margin-bottom: 20px;")
        self.detail_layout.addWidget(title)
        
        self._add_common_parameters(block)
        self._add_type_specific_parameters(block)
    
    def _add_common_parameters(self, block: Block):
        """添加公共参数"""
        params_widget = QWidget()
        params_widget.setStyleSheet("""
            QWidget {background-color: rgba(38, 38, 38, 0.3);border: 1px solid #444;border-radius: 4px;padding: 8px;}
            QLabel {border: none;}""")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(2)
        
        func_id_label = QLabel(get_text('unique_id', self.lang))
        func_id_label.setStyleSheet("font-size: 12px; font-weight: 500; width: 100px;")
        func_id_label.setFixedWidth(100)
        func_id_input = QLineEdit(block.get_parameter('func_id', ''))
        func_id_input.setObjectName("func_id")
        func_id_input.setPlaceholderText(get_text('placeholder_unique_id', self.lang))
        func_id_input.setStyleSheet("""
            QLineEdit {
                padding: 6px 8px;
                background-color: #2f2f2f;
                border: 1px solid #444;
                border-radius: 3px;
                color: white;
                font-size: 12px;
            }
        """)
        
        # 添加 func_id 验证
        def validate_func_id():
            from ..ui.notification_widget import NotificationWidget
            
            current_id = func_id_input.text()
            original_id = block.get_parameter('func_id', '')
            
            # 验证不能为空
            if not current_id:
                func_id_input.setStyleSheet("""
                    QLineEdit {
                        padding: 6px 8px;
                        background-color: #2f2f2f;
                        border: 1px solid #b42828;
                        border-radius: 3px;
                        color: white;
                        font-size: 12px;
                    }
                """)
                func_id_input.setText(original_id)
                notification = NotificationWidget(
                    NotificationWidget.TYPE_ERROR,
                    get_text('func_id_empty_error', self.lang),
                    self.lang,
                    timeout=0
                )
                notification.show()
                return False
            
            # 验证不能有特殊符号（只能是字母、数字、下划线）
            if not all(c.isalnum() or c == '_' for c in current_id):
                func_id_input.setStyleSheet("""
                    QLineEdit {
                        padding: 6px 8px;
                        background-color: #2f2f2f;
                        border: 1px solid #b42828;
                        border-radius: 3px;
                        color: white;
                        font-size: 12px;
                    }
                """)
                func_id_input.setText(original_id)
                notification = NotificationWidget(
                    NotificationWidget.TYPE_ERROR,
                    get_text('func_id_special_chars_error', self.lang),
                    self.lang,
                    timeout=0
                )
                notification.show()
                return False
            
            # 验证不能数字开头
            if current_id[0].isdigit():
                func_id_input.setStyleSheet("""
                    QLineEdit {
                        padding: 6px 8px;
                        background-color: #2f2f2f;
                        border: 1px solid #b42828;
                        border-radius: 3px;
                        color: white;
                        font-size: 12px;
                    }
                """)
                func_id_input.setText(original_id)
                notification = NotificationWidget(
                    NotificationWidget.TYPE_ERROR,
                    get_text('func_id_digit_start_error', self.lang),
                    self.lang,
                    timeout=0
                )
                notification.show()
                return False
            
            # 验证不能下划线开头和下划线结尾
            if current_id.startswith('_') or current_id.endswith('_'):
                func_id_input.setStyleSheet("""
                    QLineEdit {
                        padding: 6px 8px;
                        background-color: #2f2f2f;
                        border: 1px solid #b42828;
                        border-radius: 3px;
                        color: white;
                        font-size: 12px;
                    }
                """)
                func_id_input.setText(original_id)
                notification = NotificationWidget(
                    NotificationWidget.TYPE_ERROR,
                    get_text('func_id_underscore_error', self.lang),
                    self.lang,
                    timeout=0
                )
                notification.show()
                return False
            
            # 验证不能出现连续下划线
            if '__' in current_id:
                func_id_input.setStyleSheet("""
                    QLineEdit {
                        padding: 6px 8px;
                        background-color: #2f2f2f;
                        border: 1px solid #b42828;
                        border-radius: 3px;
                        color: white;
                        font-size: 12px;
                    }
                """)
                func_id_input.setText(original_id)
                notification = NotificationWidget(
                    NotificationWidget.TYPE_ERROR,
                    get_text('func_id_double_underscore_error', self.lang),
                    self.lang,
                    timeout=0
                )
                notification.show()
                return False
            
            # 验证id不能和已存在的id同名，包括大小写不敏感的情况
            for other_block in self.block_manager.get_all_blocks():
                if other_block.block_id != block.block_id:
                    other_func_id = other_block.get_parameter('func_id')
                    if other_func_id == current_id:
                        func_id_input.setStyleSheet("""
                            QLineEdit {
                                padding: 6px 8px;
                                background-color: #2f2f2f;
                                border: 1px solid #b42828;
                                border-radius: 3px;
                                color: white;
                                font-size: 12px;
                            }
                        """)
                        func_id_input.setText(original_id)
                        notification = NotificationWidget(
                            NotificationWidget.TYPE_ERROR,
                            get_text('func_id_duplicate_error', self.lang),
                            self.lang,
                            timeout=0
                        )
                        notification.show()
                        return False
                    elif other_func_id and current_id and other_func_id.lower() == current_id.lower():
                        func_id_input.setStyleSheet("""
                            QLineEdit {
                                padding: 6px 8px;
                                background-color: #2f2f2f;
                                border: 1px solid #b42828;
                                border-radius: 3px;
                                color: white;
                                font-size: 12px;
                            }
                        """)
                        func_id_input.setText(original_id)
                        # 构造错误信息，提到与已有的哪个 ID 相似
                        error_message = get_text('func_id_case_insensitive_error', self.lang).format(other_func_id)
                        notification = NotificationWidget(
                            NotificationWidget.TYPE_ERROR,
                            error_message,
                            self.lang,
                            timeout=0
                        )
                        notification.show()
                        return False
            
            # 验证通过，恢复默认样式
            func_id_input.setStyleSheet("""
                QLineEdit {
                    padding: 6px 8px;
                    background-color: #2f2f2f;
                    border: 1px solid #444;
                    border-radius: 3px;
                    color: white;
                    font-size: 12px;
                }
            """)
            # 保存当前状态
            self._save_current_block_state()
            return True
        
        # 使用editingFinished信号触发验证
        func_id_input.editingFinished.connect(validate_func_id)
        # 为 func_id_label 添加点击事件
        def on_func_id_label_clicked():
            from PyQt6.QtWidgets import QApplication
            from ..ui.notification_widget import NotificationWidget
            from ..utils.xml_operations import XmlOperations
            
            current_id = func_id_input.text()
            if current_id:
                # 生成内容定位注释
                start_comment, end_comment = XmlOperations.generate_positioning_comments(current_id)
                comments = f"{start_comment}\n{end_comment}"
                
                # 复制到剪贴板
                clipboard = QApplication.clipboard()
                clipboard.setText(comments)
                
                # 显示成功弹窗，3秒后自动关闭
                success_message = f"{start_comment}\n{end_comment}\n\n{get_text('copied_to_clipboard', self.lang)}"
                notification = NotificationWidget(
                    NotificationWidget.TYPE_SUCCESS,
                    success_message,
                    self.lang,
                    timeout=3000  # 3秒后自动关闭
                )
                notification.show()
        
        # 设置标签可点击
        func_id_label.setCursor(Qt.CursorShape.PointingHandCursor)
        func_id_label.mousePressEvent = lambda event: on_func_id_label_clicked()
        
        func_id_row = QHBoxLayout()
        func_id_row.setSpacing(8)
        func_id_row.addWidget(func_id_label)
        func_id_row.addWidget(func_id_input)
        layout.addLayout(func_id_row)
        
        func_name_label = QLabel(get_text('display_name', self.lang))
        func_name_label.setStyleSheet("font-size: 12px; font-weight: 500; width: 100px;")
        func_name_label.setFixedWidth(100)
        func_name_input = QLineEdit(block.get_parameter('func_name', ''))
        func_name_input.setObjectName("func_name")
        func_name_input.setPlaceholderText(get_text('placeholder_display_name', self.lang))
        func_name_input.setStyleSheet("""
            QLineEdit {
                padding: 6px 8px;
                background-color: #2f2f2f;
                border: 1px solid #444;
                border-radius: 3px;
                color: white;
                font-size: 12px;
            }
        """)
        
        # 添加 func_name 验证
        def validate_func_name():
            current_name = func_name_input.text()
            original_name = block.get_parameter('func_name', '')
            
            # 检查是否与其他功能块的display name重复
            for other_block in self.block_manager.get_all_blocks():
                if other_block.block_id == self.current_block_id:
                    continue
                
                other_name = other_block.get_parameter('func_name')
                if other_name == current_name:
                    func_name_input.setText(original_name)
                    from ..ui.notification_widget import NotificationWidget
                    notification = NotificationWidget(
                        NotificationWidget.TYPE_ERROR,
                        'Display name already exists. Please choose a different name.',
                        self.lang,
                        timeout=0
                    )
                    notification.show()
                    return
            
            # 保存当前状态
            self._save_current_block_state()
        
        func_name_input.editingFinished.connect(validate_func_name)
        func_name_row = QHBoxLayout()
        func_name_row.setSpacing(8)
        func_name_row.addWidget(func_name_label)
        func_name_row.addWidget(func_name_input)
        layout.addLayout(func_name_row)
        
        group_label = QLabel(get_text('group', self.lang))
        group_label.setStyleSheet("font-size: 12px; font-weight: 500; width: 100px;")
        group_label.setFixedWidth(100)
        group_select = QComboBox()
        group_select.setObjectName("group_name")
        for group in self.group_manager.get_all_groups():
            group_select.addItem(group.name)
        group_select.setCurrentText(block.get_parameter('group_name', 'Default'))
        group_select.setStyleSheet("""
            QComboBox {
                padding: 6px 8px;
                background-color: #2f2f2f;
                border: 1px solid #444;
                border-radius: 3px;
                color: white;
                font-size: 12px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #ccc;
            }
        """)
        group_row = QHBoxLayout()
        group_row.setSpacing(8)
        group_row.addWidget(group_label)
        group_row.addWidget(group_select)
        layout.addLayout(group_row)
        
        desc_row = QHBoxLayout()
        desc_row.setSpacing(8)
        desc_label = QLabel(get_text('description', self.lang))
        desc_label.setStyleSheet("font-size: 12px; font-weight: 500; width: 100px;")
        desc_label.setFixedWidth(100)
        desc_input = QLineEdit(block.get_parameter('description', ''))
        desc_input.setObjectName("description")
        desc_input.setPlaceholderText(get_text('placeholder_desc', self.lang))
        desc_input.setStyleSheet("""
            QLineEdit {
                padding: 6px 8px;
                background-color: #2f2f2f;
                border: 1px solid #444;
                border-radius: 3px;
                color: white;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 1px solid #0e639c;
            }
        """)
        # 添加双击事件处理
        desc_input.mouseDoubleClickEvent = lambda event, d=desc_input: self._on_block_desc_double_click(event, d)
        desc_row.addWidget(desc_label)
        desc_row.addWidget(desc_input)
        layout.addLayout(desc_row)
        
        params_widget.setLayout(layout)
        self.detail_layout.addWidget(params_widget)
    
    def _add_type_specific_parameters(self, block: Block):
        """添加类型特定参数"""
        if block.block_type == BlockType.SWITCH:
            self._add_switch_parameters(block)
        elif block.block_type == BlockType.OPTION:
            self._add_option_parameters(block)
        elif block.block_type == BlockType.INT_SLIDER:
            self._add_slider_parameters(block, is_int=True)
        elif block.block_type == BlockType.FLOAT_SLIDER:
            self._add_slider_parameters(block, is_int=False)
    
    def _add_switch_parameters(self, block: Block):
        """添加开关类型参数"""
        params_widget = QWidget()
        params_widget.setStyleSheet("""
            QWidget {background-color: rgba(38, 38, 38, 0.3);border: 1px solid #444;border-radius: 4px;padding: 8px;}
            QLabel {border: none;}""")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(0)
        
        default_label = QLabel(get_text('default_value', self.lang))
        default_label.setStyleSheet("font-size: 12px; font-weight: 500; margin-bottom: 4px;")
        layout.addWidget(default_label)
        
        default_select = QComboBox()
        default_select.setObjectName("default_value")
        default_select.addItem("true")
        default_select.addItem("false")
        default_select.setCurrentText(block.get_parameter('default_value', 'true'))
        default_select.currentTextChanged.connect(self._save_current_block_state)
        default_select.setStyleSheet("""
            QComboBox {
                padding: 6px 8px;
                background-color: #2f2f2f;
                border: 1px solid #444;
                border-radius: 3px;
                color: white;
                font-size: 12px;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(default_select)
        
        layout.addSpacing(16)
        
        on_exec_group = self._create_exec_unit_group(get_text('true_code', self.lang), 'on', block)
        layout.addWidget(on_exec_group)
        
        layout.addSpacing(16)
        
        off_exec_group = self._create_exec_unit_group(get_text('false_code', self.lang), 'off', block)
        layout.addWidget(off_exec_group)
        
        params_widget.setLayout(layout)
        self.detail_layout.addWidget(params_widget)
    
    def _create_exec_unit_group(self, label: str, group_type: str, block: Block) -> QWidget:
        """创建执行单元分组"""
        group_widget = QWidget()
        group_widget.setStyleSheet("""
            QWidget {
                background-color: transparent;
                border: none;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        group_widget.setLayout(layout)
        
        group_label = QLabel(label)
        group_label.setStyleSheet("font-size: 13px; color: #ddd;")
        layout.addWidget(group_label)
        
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(btn_layout)
        
        add_btn = QPushButton(get_text('add_exec_unit', self.lang))
        add_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        add_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                background-color: #333;
                border: 1px solid #444;
                border-radius: 3px;
                color: #eee;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
            }
        """)
        btn_layout.addWidget(add_btn)
        btn_layout.addStretch()
        
        container = QWidget()
        container.setStyleSheet("""
            QWidget {
                background-color: transparent;
                border: none;
            }
        """)
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(10)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        container.setLayout(container_layout)
        layout.addWidget(container)
        
        exec_units = []
        if group_type == 'on':
            exec_units = block.get_parameter('true_exec_units', [])
        else:
            exec_units = block.get_parameter('false_exec_units', [])
        
        if not exec_units:
            code = self._generate_unit_code()
            if group_type == 'on':
                unit_code = f"True_{code}"
            else:
                unit_code = f"False_{code}"
            exec_unit = ExecUnitCard(0, is_default=True, unit_code=unit_code, lang=self.lang)
            exec_unit.load_config_files(self.config_dir)
            exec_unit.set_default_values(unit_code)
            exec_unit.content_changed.connect(self._save_current_block_state)
            container_layout.addWidget(exec_unit)
        else:
            for i, unit_data in enumerate(exec_units):
                exec_unit = ExecUnitCard(i, is_default=(i == 0), lang=self.lang)
                exec_unit.load_config_files(self.config_dir)
                exec_unit.set_data(unit_data)
                exec_unit.delete_requested.connect(lambda u=exec_unit: self._remove_exec_unit(u, container))
                exec_unit.copy_requested.connect(lambda u=exec_unit: self._copy_exec_unit(u, container))
                exec_unit.content_changed.connect(self._save_current_block_state)
                container_layout.addWidget(exec_unit)
        
        add_btn.clicked.connect(lambda: self._add_exec_unit(container, group_type))
        
        return group_widget
    
    def _generate_unit_code(self) -> str:
        """生成6位随机码"""
        import random
        import string
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    def _add_exec_unit(self, container: QWidget, group_type: str):
        """添加执行单元"""
        layout = container.layout()
        units = [container.layout().itemAt(i).widget() for i in range(layout.count())]
        new_index = len(units)
        
        code = self._generate_unit_code()
        if group_type == 'on':
            unit_code = f"True_{code}"
        else:
            unit_code = f"False_{code}"
        
        exec_unit = ExecUnitCard(new_index, is_default=False, unit_code=unit_code, lang=self.lang)
        exec_unit.load_config_files(self.config_dir)
        exec_unit.set_default_values(unit_code)
        exec_unit.delete_requested.connect(lambda u=exec_unit: self._remove_exec_unit(u, container))
        exec_unit.copy_requested.connect(lambda u=exec_unit: self._copy_exec_unit(u, container))
        layout.addWidget(exec_unit)
    
    def _remove_exec_unit(self, exec_unit: ExecUnitCard, container: QWidget):
        """移除执行单元"""
        layout = container.layout()
        units = [layout.itemAt(i).widget() for i in range(layout.count())]
        
        if len(units) > 1 and not exec_unit.is_default:
            layout.removeWidget(exec_unit)
            exec_unit.deleteLater()
            self._update_exec_unit_indices(container)
    

    
    def _update_exec_unit_indices(self, container: QWidget):
        """更新执行单元索引"""
        layout = container.layout()
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if isinstance(widget, ExecUnitCard):
                widget.set_index(i)
    
    def _add_option_parameters(self, block: Block):
        """添加下拉选项类型参数"""
        params_widget = QWidget()
        params_widget.setStyleSheet("""
            QWidget {background-color: rgba(38, 38, 38, 0.3);border: 1px solid #444;border-radius: 4px;padding: 8px;}
            QLabel {border: none;}""")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(0)
        
        default_label = QLabel(get_text('default_value', self.lang))
        default_label.setStyleSheet("font-size: 12px; font-weight: 500; margin-bottom: 4px;")
        layout.addWidget(default_label)
        
        default_input = QComboBox()
        default_input.setObjectName("default_value")
        default_input.setEditable(False)
        default_input.setStyleSheet("""
            QComboBox {
                padding: 6px 8px;
                background-color: #2f2f2f;
                border: 1px solid #444;
                border-radius: 3px;
                color: white;
                font-size: 12px;
                margin-bottom: 10px;
            }
            QComboBox:hover {
                border: 1px solid #555;
            }
            QComboBox:focus {
                border: 1px solid #0e639c;
            }
            QComboBox QAbstractItemView {
                background-color: #2f2f2f;
                border: 1px solid #444;
                selection-background-color: #0e639c;
                selection-color: white;
            }
        """)
        default_input.currentTextChanged.connect(self._save_current_block_state)
        layout.addWidget(default_input)
        
        layout.addSpacing(16)
        
        options_group = self._create_options_group(block, default_input)
        layout.addWidget(options_group)
        
        params_widget.setLayout(layout)
        self.detail_layout.addWidget(params_widget)
    
    def _create_options_group(self, block: Block, default_combo: QComboBox) -> QWidget:
        """创建选项分组"""
        group_widget = QWidget()
        group_widget.setStyleSheet("""
            QWidget {
                background-color: transparent;
                border: none;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        group_widget.setLayout(layout)
        
        group_label = QLabel(get_text('options', self.lang))
        group_label.setStyleSheet("font-size: 13px; color: #ddd;")
        layout.addWidget(group_label)
        
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(btn_layout)
        
        add_btn = QPushButton(get_text('add_option', self.lang))
        add_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        add_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                background-color: #333;
                border: 1px solid #444;
                border-radius: 3px;
                color: #eee;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
            }
        """)
        btn_layout.addWidget(add_btn)
        btn_layout.addStretch()
        
        container = QWidget()
        container.setStyleSheet("""
            QWidget {
                background-color: transparent;
                border: none;
            }
        """)
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(10)
        container.setLayout(container_layout)
        layout.addWidget(container)
        
        options = block.get_parameter('option_items', [])
        
        if not options:
            option = OptionCard(0, is_default=True, lang=self.lang)
            option.load_config_files(self.config_dir)
            option.content_changed.connect(self._save_current_block_state)
            option.content_changed.connect(lambda: self._update_default_combo(default_combo, container))
            option.add_exec_unit_requested.connect(lambda o=option: self._add_option_exec_unit(o))
            container_layout.addWidget(option)
        else:
            for i, option_data in enumerate(options):
                option = OptionCard(i, is_default=(i == 0), lang=self.lang)
                option.set_data(option_data)
                option.load_config_files(self.config_dir)
                option.delete_requested.connect(lambda o=option: self._remove_option(o, container, default_combo))
                option.copy_requested.connect(lambda o=option: self._copy_option(o, container, default_combo))
                option.content_changed.connect(self._save_current_block_state)
                option.content_changed.connect(lambda: self._update_default_combo(default_combo, container))
                option.add_exec_unit_requested.connect(lambda o=option: self._add_option_exec_unit(o))
                container_layout.addWidget(option)
        
        add_btn.clicked.connect(lambda: self._add_option(container, default_combo))
        
        self._update_default_combo(default_combo, container)
        
        # 添加以下代码，检查 block 中是否有 default_value 参数
        default_value = block.get_parameter('default_value', '')
        if default_value and default_combo.findText(default_value) >= 0:
            default_combo.setCurrentText(default_value)
        
        return group_widget
    
    def _add_option(self, container: QWidget, default_combo: QComboBox):
        """添加选项"""
        layout = container.layout()
        units = [container.layout().itemAt(i).widget() for i in range(layout.count())]
        new_index = len(units)
        
        option = OptionCard(new_index, is_default=False, lang=self.lang)
        option.load_config_files(self.config_dir)
        option.content_changed.connect(lambda: self._update_default_combo(default_combo, container))
        option.delete_requested.connect(lambda o=option: self._remove_option(o, container, default_combo))
        option.copy_requested.connect(lambda o=option: self._copy_option(o, container, default_combo))
        option.add_exec_unit_requested.connect(lambda o=option: self._add_option_exec_unit(o))
        layout.addWidget(option)
        self._update_default_combo(default_combo, container)
    
    def _remove_option(self, option: OptionCard, container: QWidget, default_combo: QComboBox):
        """移除选项"""
        layout = container.layout()
        units = [layout.itemAt(i).widget() for i in range(layout.count())]
        
        if len(units) > 1 and not option.is_default:
            layout.removeWidget(option)
            option.deleteLater()
            self._update_option_indices(container)
            self._update_default_combo(default_combo, container)

    def _update_option_indices(self, container: QWidget):
        """更新选项索引"""
        layout = container.layout()
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if isinstance(widget, OptionCard):
                widget.set_index(i)
    
    def _update_default_combo(self, combo: QComboBox, container: QWidget):
        """更新默认值下拉框选项"""
        layout = container.layout()
        current_text = combo.currentText()
        
        combo.clear()
        
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if isinstance(widget, OptionCard):
                option_key = widget.name_input.text()
                if option_key:
                    combo.addItem(option_key)
        
        if current_text and combo.findText(current_text) >= 0:
            combo.setCurrentText(current_text)
        elif combo.count() > 0:
            combo.setCurrentIndex(0)
    
    def _add_option_exec_unit(self, option: OptionCard):
        """为选项添加执行单元"""
        code = self._generate_unit_code()
        
        exec_unit = ExecUnitCard(len(option.exec_units), is_default=False, unit_code=code, lang=self.lang)
        exec_unit.load_config_files(self.config_dir)
        exec_unit.set_default_values(code)
        exec_unit.content_changed.connect(self._save_current_block_state)
        option.add_exec_unit(exec_unit)
        self._save_current_block_state()
    
    def _validate_slider_inputs(self, min_input, max_input, step_input, default_input, is_int, valid_values):
        """验证滑块输入值"""
        # 标记是否有验证错误
        has_error = False
        error_type = None  # 错误类型：type, range, default, step
        
        # 定义输入控件和对应的值存储
        input_configs = [
            (min_input, 'min', 'min_val'),
            (max_input, 'max', 'max_val'),
            (step_input, 'step', 'step_val'),
            (default_input, 'default', 'default_val')
        ]
        
        # 初始化值
        values = {}
        type_error = False
        
        # 验证类型并转换值
        for input_widget, key, var_name in input_configs:
            text = input_widget.text()
            if text:
                try:
                    if is_int:
                        values[var_name] = int(text)
                    else:
                        values[var_name] = float(text)
                except ValueError:
                    input_widget.setText(valid_values[key])
                    has_error = True
                    type_error = True
            else:
                values[var_name] = None
        
        # 处理类型错误
        if type_error:
            error_type = 'type'
        else:
            min_val, max_val, step_val, default_val = values['min_val'], values['max_val'], values['step_val'], values['default_val']
            
            # 验证最大值大于最小值
            if min_val is not None and max_val is not None and max_val <= min_val:
                max_input.setText(valid_values['max'])
                min_input.setText(valid_values['min'])
                has_error = True
                error_type = 'range'
            
            # 验证步长
            elif step_val is not None and (step_val <= 0 or (max_val is not None and step_val >= max_val)):
                step_input.setText(valid_values['step'])
                has_error = True
                error_type = 'step'
            
            # 验证默认值在最小值和最大值之间
            elif default_val is not None and min_val is not None and max_val is not None and (default_val < min_val or default_val > max_val):
                default_input.setText(valid_values['default'])
                has_error = True
                error_type = 'default'
        
        # 更新有效值存储
        for input_widget, key, _ in input_configs:
            if input_widget.text() and self._is_valid_number(input_widget.text(), is_int):
                valid_values[key] = input_widget.text()
        
        # 如果有错误，显示相应的弹窗提示
        if has_error:
            from ..ui.notification_widget import NotificationWidget
            
            # 错误类型到消息键的映射
            error_message_map = {
                'type': 'slider_error_type_msg',
                'range': 'slider_error_range_msg',
                'default': 'slider_error_default_msg',
                'step': 'slider_error_step_msg'
            }
            
            # 获取对应的错误消息
            message_key = error_message_map.get(error_type, 'slider_param_validation')
            
            # 显示错误弹窗
            notification = NotificationWidget(
                NotificationWidget.TYPE_ERROR,
                get_text(message_key, self.lang),
                self.lang,
                timeout=0  # 设置为0表示不自动关闭
            )
            notification.show()
        
        # 定义输入控件和对应的值存储
        input_configs = [
            (min_input, 'min', 'min_val'),
            (max_input, 'max', 'max_val'),
            (step_input, 'step', 'step_val'),
            (default_input, 'default', 'default_val')
        ]
        
        # 初始化值
        values = {}
        type_error = False
        
        # 验证类型并转换值
        for input_widget, key, var_name in input_configs:
            text = input_widget.text()
            if text:
                try:
                    if is_int:
                        values[var_name] = int(text)
                    else:
                        values[var_name] = float(text)
                except ValueError:
                    input_widget.setText(valid_values[key])
                    has_error = True
                    type_error = True
            else:
                values[var_name] = None
        
        # 处理类型错误
        if type_error:
            error_type = 'type'
        else:
            min_val, max_val, step_val, default_val = values['min_val'], values['max_val'], values['step_val'], values['default_val']
            
            # 验证最大值大于最小值
            if min_val is not None and max_val is not None and max_val <= min_val:
                max_input.setText(valid_values['max'])
                min_input.setText(valid_values['min'])
                has_error = True
                error_type = 'range'
            
            # 验证步长
            elif step_val is not None and (step_val <= 0 or (max_val is not None and step_val >= max_val)):
                step_input.setText(valid_values['step'])
                has_error = True
                error_type = 'step'
            
            # 验证默认值在最小值和最大值之间
            elif default_val is not None and min_val is not None and max_val is not None and (default_val < min_val or default_val > max_val):
                default_input.setText(valid_values['default'])
                has_error = True
                error_type = 'default'
        
        # 更新有效值存储
        for input_widget, key, _ in input_configs:
            if input_widget.text() and self._is_valid_number(input_widget.text(), is_int):
                valid_values[key] = input_widget.text()
        
        # 如果有错误，显示相应的弹窗提示
        if has_error:
            from ..ui.notification_widget import NotificationWidget
            
            # 错误类型到消息键的映射
            error_message_map = {
                'type': 'slider_error_type_msg',
                'range': 'slider_error_range_msg',
                'default': 'slider_error_default_msg',
                'step': 'slider_error_step_msg'
            }
            
            # 获取对应的错误消息
            message_key = error_message_map.get(error_type, 'slider_param_validation')
            
            # 显示错误弹窗
            notification = NotificationWidget(
                NotificationWidget.TYPE_ERROR,
                get_text(message_key, self.lang),
                self.lang,
                timeout=0  # 设置为0表示不自动关闭
            )
            notification.show()
    
    def _is_valid_number(self, value, is_int):
        """检查值是否为有效的数字"""
        try:
            if is_int:
                int(value)
            else:
                # 浮点数滑块兼容整数输入
                float(value)
            return True
        except ValueError:
            return False
    
    def _add_slider_parameters(self, block: Block, is_int: bool):
        """添加滑块类型参数"""
        params_widget = QWidget()
        params_widget.setStyleSheet("""
            QWidget {background-color: rgba(38, 38, 38, 0.3);border: 1px solid #444;border-radius: 4px;padding: 8px;}
            QLabel {border: none;}""")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)
        
        # 第一行：默认值和步长
        row1_layout = QHBoxLayout()
        row1_layout.setSpacing(16)
        
        # 默认值
        default_layout = QHBoxLayout()
        default_layout.setSpacing(8)
        default_label = QLabel(get_text('default_value', self.lang))
        default_label.setStyleSheet("font-size: 12px; font-weight: 500; width: 80px;")
        default_label.setFixedWidth(80)
        default_input = QLineEdit(block.get_parameter('default_value', '100' if is_int else '1.0'))
        default_input.setObjectName("default_value")
        default_input.setPlaceholderText(get_text('placeholder_default_int', self.lang) if is_int else get_text('placeholder_default_float', self.lang))
        default_input.setStyleSheet("""
            QLineEdit {
                padding: 6px 8px;
                background-color: #2f2f2f;
                border: 1px solid #444;
                border-radius: 3px;
                color: white;
                font-size: 12px;
                min-width: 120px;
            }
        """)
        default_layout.addWidget(default_label)
        default_layout.addWidget(default_input)
        row1_layout.addLayout(default_layout)
        
        # 步长
        step_layout = QHBoxLayout()
        step_layout.setSpacing(8)
        step_label = QLabel(get_text('step', self.lang))
        step_label.setStyleSheet("font-size: 12px; font-weight: 500; width: 80px;")
        step_label.setFixedWidth(80)
        step_input = QLineEdit(block.get_parameter('step_value', '1' if is_int else '0.1'))
        step_input.setObjectName("step_value")
        step_input.setPlaceholderText(get_text('placeholder_step_int', self.lang) if is_int else get_text('placeholder_step_float', self.lang))
        step_input.setStyleSheet("""
            QLineEdit {
                padding: 6px 8px;
                background-color: #2f2f2f;
                border: 1px solid #444;
                border-radius: 3px;
                color: white;
                font-size: 12px;
                min-width: 120px;
            }
        """)
        step_layout.addWidget(step_label)
        step_layout.addWidget(step_input)
        row1_layout.addLayout(step_layout)
        row1_layout.addStretch()
        layout.addLayout(row1_layout)
        
        # 第二行：最小值和最大值
        row2_layout = QHBoxLayout()
        row2_layout.setSpacing(16)
        
        # 最小值
        min_layout = QHBoxLayout()
        min_layout.setSpacing(8)
        min_label = QLabel(get_text('min_value', self.lang))
        min_label.setStyleSheet("font-size: 12px; font-weight: 500; width: 80px;")
        min_label.setFixedWidth(80)
        min_input = QLineEdit(block.get_parameter('min_value', '1' if is_int else '0.5'))
        min_input.setObjectName("min_value")
        min_input.setPlaceholderText(get_text('placeholder_min_int', self.lang) if is_int else get_text('placeholder_min_float', self.lang))
        min_input.setStyleSheet("""
            QLineEdit {
                padding: 6px 8px;
                background-color: #2f2f2f;
                border: 1px solid #444;
                border-radius: 3px;
                color: white;
                font-size: 12px;
                min-width: 120px;
            }
        """)
        min_layout.addWidget(min_label)
        min_layout.addWidget(min_input)
        row2_layout.addLayout(min_layout)
        
        # 最大值
        max_layout = QHBoxLayout()
        max_layout.setSpacing(8)
        max_label = QLabel(get_text('max_value', self.lang))
        max_label.setStyleSheet("font-size: 12px; font-weight: 500; width: 80px;")
        max_label.setFixedWidth(80)
        max_input = QLineEdit(block.get_parameter('max_value', '100' if is_int else '2.0'))
        max_input.setObjectName("max_value")
        max_input.setPlaceholderText(get_text('placeholder_max_int', self.lang) if is_int else get_text('placeholder_max_float', self.lang))
        max_input.setStyleSheet("""
            QLineEdit {
                padding: 6px 8px;
                background-color: #2f2f2f;
                border: 1px solid #444;
                border-radius: 3px;
                color: white;
                font-size: 12px;
                min-width: 120px;
            }
        """)
        max_layout.addWidget(max_label)
        max_layout.addWidget(max_input)
        row2_layout.addLayout(max_layout)
        row2_layout.addStretch()
        layout.addLayout(row2_layout)
        
        
        # 存储有效值，使用默认值初始化，而不是输入框的当前文本
        valid_values = {
            'min': '1' if is_int else '0.5',
            'max': '100' if is_int else '2.0',
            'step': '1' if is_int else '0.1',
            'default': '100' if is_int else '1.0'
        }
        
        # 添加输入验证
        def on_input_changed():
            self._validate_slider_inputs(min_input, max_input, step_input, default_input, is_int, valid_values)
        
        # 使用editingFinished信号而不是textChanged，这样只有当用户完成输入时才会触发验证
        min_input.editingFinished.connect(on_input_changed)
        max_input.editingFinished.connect(on_input_changed)
        step_input.editingFinished.connect(on_input_changed)
        default_input.editingFinished.connect(on_input_changed)
        
        # 第三部分：XpathCard区域
        from ..ui.collapsible_widgets import XpathCard
        
        xpath_group_widget = QWidget()
        xpath_group_widget.setStyleSheet("""
            QWidget {
                background-color: transparent;
                border: none;
            }
        """)
        
        xpath_layout = QVBoxLayout()
        xpath_layout.setContentsMargins(0, 16, 0, 0)
        xpath_layout.setSpacing(8)
        xpath_group_widget.setLayout(xpath_layout)
        
        xpath_group_label = QLabel("Xpath")
        xpath_group_label.setStyleSheet("font-size: 13px; color: #ddd;")
        xpath_layout.addWidget(xpath_group_label)
        
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        xpath_layout.addLayout(btn_layout)
        
        add_xpath_btn = QPushButton("+ Add XpathCard")
        add_xpath_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        add_xpath_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                background-color: #333;
                border: 1px solid #444;
                border-radius: 3px;
                color: #eee;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
            }
        """)
        btn_layout.addWidget(add_xpath_btn)
        btn_layout.addStretch()
        
        xpath_container = QWidget()
        xpath_container.setStyleSheet("""
            QWidget {
                background-color: transparent;
                border: none;
            }
        """)
        xpath_container_layout = QVBoxLayout()
        xpath_container_layout.setContentsMargins(0, 0, 0, 0)
        xpath_container_layout.setSpacing(10)
        xpath_container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        xpath_container.setLayout(xpath_container_layout)
        xpath_layout.addWidget(xpath_container)
        
        # 加载现有的XpathCard数据
        xpath_sets = block.get_parameter('XpathSet', [])
        
        if not xpath_sets:
            # 默认添加一个不可删除的XpathCard
            xpath_card = XpathCard(0, is_default=True, lang=self.lang)
            xpath_card.load_config_files(self.config_dir)
            xpath_card.set_default_values()
            xpath_container_layout.addWidget(xpath_card)
        else:
            for i, xpath_data in enumerate(xpath_sets):
                xpath_card = XpathCard(i, is_default=(i == 0), lang=self.lang)
                xpath_card.load_config_files(self.config_dir)
                xpath_card.set_data(xpath_data)
                xpath_card.delete_requested.connect(lambda c=xpath_card: self._remove_xpath_card(c, xpath_container))
                xpath_card.copy_requested.connect(lambda c=xpath_card: self._copy_xpath_card(c, xpath_container))
                xpath_container_layout.addWidget(xpath_card)
        
        # 添加XpathCard的方法
        def add_xpath_card():
            layout = xpath_container.layout()
            cards = [layout.itemAt(i).widget() for i in range(layout.count())]
            new_index = len(cards)
            
            xpath_card = XpathCard(new_index, is_default=False, lang=self.lang)
            xpath_card.load_config_files(self.config_dir)
            xpath_card.set_default_values()
            xpath_card.delete_requested.connect(lambda c=xpath_card: self._remove_xpath_card(c, xpath_container))
            xpath_card.copy_requested.connect(lambda c=xpath_card: self._copy_xpath_card(c, xpath_container))
            layout.addWidget(xpath_card)
        
        add_xpath_btn.clicked.connect(add_xpath_card)
        
        layout.addWidget(xpath_group_widget)
        
        params_widget.setLayout(layout)
        self.detail_layout.addWidget(params_widget)
        
        # 初始验证
        on_input_changed()
    
    def _remove_xpath_card(self, xpath_card: 'XpathCard', container: QWidget):
        """移除XpathCard"""
        layout = container.layout()
        cards = [layout.itemAt(i).widget() for i in range(layout.count())]
        
        if len(cards) > 1 and not xpath_card.is_default:
            layout.removeWidget(xpath_card)
            xpath_card.deleteLater()
            self._update_xpath_card_indices(container)
    
    
    def _update_xpath_card_indices(self, container: QWidget):
        """更新XpathCard索引"""
        layout = container.layout()
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            from ..ui.collapsible_widgets import XpathCard
            if isinstance(widget, XpathCard):
                widget.set_index(i)
    
    def _clear_detail_layout(self):
        """清空详细布局"""
        while self.detail_layout.count():
            item = self.detail_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
    
    def _toggle_add_block_section(self):
        """切换添加功能块区域"""
        if self.add_block_buttons.isVisible():
            self.add_block_buttons.hide()
            self.add_block_toggle.setText(f"{get_text('add_block', self.lang)} ▾")
        else:
            self.add_block_buttons.show()
            self.add_block_toggle.setText(f"{get_text('add_block', self.lang)} ▴")
    
    def _create_block(self, block_type: str):
        """创建功能块"""
        if self.current_block_id:
            self._save_current_block_state()
        
        random_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        
        block = Block(
            block_id=self.block_manager.generate_block_id(),
            block_type=BlockType(block_type),
            parameters={
                'func_id': random_code,
                'func_name': f'DisplayName_{random_code}'
            }
        )
        
        self.block_manager.add_block(block)
        self._refresh_block_list()
        self._show_block_detail_panel(block.block_id)
        self.json_manager.save()
        self._update_code_editor()
    
    def _delete_block(self, item: QListWidgetItem):
        """删除功能块"""
        block_id = item.data(1)
        if not block_id:
            return
        
        block = self.block_manager.get_block(block_id)
        if not block:
            return
        
        block_name = block.get_parameter('func_name', 'Unnamed')
        
        reply = QMessageBox.question(
            self,
            get_text('warning', self.lang),
            get_text('confirm_delete', self.lang),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.block_manager.remove_block(block_id)
            self._refresh_block_list()
            self.json_manager.save()
            self._update_code_editor()
    
    def _open_code_window(self):
        """打开代码窗口"""
        if not self.code_window:
            self.code_window = CodeEditorWindow()
            self.code_window.show()
        else:
            self.code_window.show()
        
        self.code_window.set_content(self.json_manager.get_json_content())
    
    def closeEvent(self, event):
        """关闭事件"""
        # 在关闭前使用当前功能块触发保存机制
        self._save_current_block_state()
        
        # 执行原有的关闭逻辑
        self.json_manager.save()
        event.accept()
