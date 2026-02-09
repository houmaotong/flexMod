"""玩家页面"""
import os
import json
from re import S
from typing import Dict, List, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QComboBox, QStackedWidget, QGroupBox, QScrollArea,
    QMessageBox, QLineEdit, QSlider
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QBrush, QColor, QFont

from ..utils.lang import get_text, get_lang
from ..managers.config_manager import ConfigManager
from ..utils.xml_operations import XmlOperations

# 导入QInputDialog
from PyQt6.QtWidgets import QInputDialog
from .flex_mod_color import (SS_preset_label, SS_preset_btn,
                            SS_preset_combo,SS_player_scroll_area,

                            SS_player_SettingCard_big,
                            SS_player_SettingCard_header,
                            SS_player_SettingCard_content,
                            SS_player_SettingCard_GroupDesc,
                            SS_player_SettingItemCard,
                            SS_player_SettingItemCard_Title,
                            SS_player_SettingItemCard_Desc,
                            SS_player_SettingItemCard_slider_widget, 
                            SS_player_SettingItemCard_slider_widget_value_label
                            )

class ToggleSwitch(QWidget):
    """开关控件"""
    
    toggled = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(44, 24)
        self.is_checked = False
        
    def paintEvent(self, event):
        """绘制事件"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 绘制背景
        from .flex_mod_color import PRIMARY_500,BG_400
        bg_color = QColor(PRIMARY_500) if self.is_checked else QColor(BG_400)
        
        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(0, 0, 44, 24, 12, 12)
        
        # 绘制滑块
        slider_x = 22 if self.is_checked else 2
        painter.setBrush(QBrush(QColor('#ffffff')))
        painter.drawEllipse(slider_x, 2, 20, 20)
    
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        self.is_checked = not self.is_checked
        self.update()
        self.toggled.emit(self.is_checked)
    
    def setChecked(self, checked):
        """设置状态"""
        if self.is_checked != checked:
            self.is_checked = checked
            self.update()
    
    def isChecked(self):
        """获取状态"""
        return self.is_checked


class SettingCard(QWidget):
    """设置卡片基类"""
    
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.title = title
        self.is_expanded = True
        self._init_ui()
    
    def _init_ui(self):
        """初始化UI"""
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(SS_player_SettingCard_big)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)
        
        self.header = self._create_header()
        layout.addWidget(self.header)
        
        self.content = QWidget()
        self.content.setStyleSheet(SS_player_SettingCard_content)
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        #透明背景
        self.content.setLayout(content_layout)
        layout.addWidget(self.content)
        
        # 创建主布局，用于容纳描述容器和设置容器
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)  # 两个容器的父容器间距0
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.content.layout().addLayout(self.main_layout)
        
        # 创建描述容器
        self.desc_container = QWidget()
        self.desc_layout = QVBoxLayout()
        self.desc_layout.setContentsMargins(20, 10, 10, 20)  # 组描述容器：上2，左右下10
        self.desc_layout.setSpacing(0)
        self.desc_container.setLayout(self.desc_layout)
        
        # 创建设置容器
        self.cards_container = QWidget()
        self.cards_layout = QVBoxLayout()
        self.cards_layout.setContentsMargins(20, 10, 20, 20)  # 卡片放置容器：上10，左右下20
        self.cards_layout.setSpacing(10)  # 控件间距10
        self.cards_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.cards_container.setLayout(self.cards_layout)
        
        # 将容器添加到主布局
        self.main_layout.addWidget(self.desc_container)
        self.main_layout.addWidget(self.cards_container)
        
        self.update_style()
    
    def _create_header(self) -> QWidget:
        """创建头部"""
        header = QWidget()
        header.setFixedHeight(50)
        header.setCursor(Qt.CursorShape.PointingHandCursor)
        header.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        header.setStyleSheet(SS_player_SettingCard_header)
        # 为header添加单点击事件处理
        header.mousePressEvent = self._on_header_single_click
        
 
        layout = QHBoxLayout()
        layout.setContentsMargins(12, 0, 12, 0)  # 左侧添加12px边距，右侧添加8px边距
        layout.setSpacing(8)
        header.setLayout(layout)
        
        self.title_label = QLabel(self.title)
        # 设置标题标签的对齐方式
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.title_label)
        
        layout.addStretch()
        # 添加箭头图标
        self.arrow_label = QLabel("▼")
        layout.addWidget(self.arrow_label)
        
        return header
    
    def _on_header_single_click(self, event):
        """处理header单点击事件，展开/折叠卡片"""
        self.is_expanded = not self.is_expanded
        self.content.setVisible(self.is_expanded)
        # 更新箭头图标
        self.arrow_label.setText("▶" if not self.is_expanded else "▼")
    
    def set_title(self, title: str):
        """设置标题"""
        self.title = title
        self.title_label.setText(title)
    
    def update_style(self):
        """更新样式"""
        self.setStyleSheet(SS_player_SettingCard_big)
    
    def add_description(self, description: str):
        """添加组描述
        Args:
            description: 组描述文本
        """
        if description:
            # 清空描述容器，确保只显示最新的描述
            for i in range(self.desc_layout.count()):
                item = self.desc_layout.itemAt(i)
                if item.widget():
                    item.widget().deleteLater()
            
            # 创建描述标签
            group_desc_label = QLabel(description)
            group_desc_label.setStyleSheet(SS_player_SettingCard_GroupDesc)
            self.desc_layout.addWidget(group_desc_label)
    
    def add_setting_item(self, widget: QWidget):
        """添加设置项
        Args:
            widget: 设置项控件
        """
        if widget:
            self.cards_layout.addWidget(widget)


class SettingItemCard(QWidget):
    """设置项卡片"""
    
    def __init__(self, title: str, setting_name: str = None, setting_data: dict = None, parent=None):
        super().__init__(parent)
        self.title = title
        self.setting_name = setting_name
        self.setting_data = setting_data
        self._init_ui()
    
    def _init_ui(self):
        """初始化UI"""
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        # 整体垂直布局
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)  # items 4周内部间距为10px
        layout.setSpacing(0)  # 内部控件和控件间距为0
        self.setLayout(layout)
        
        # 第一行水平布局：放标题 做对齐 ，放控件 右对齐
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)
        layout.addLayout(header_layout)
        
        # 设置名称标签（左对齐）
        name_label = QLabel(self.title)
        name_label.setStyleSheet(SS_player_SettingItemCard_Title)
        header_layout.addWidget(name_label)
        
        header_layout.addStretch()# 左对齐的标题标签和右对齐的控件之间的间距
        
        # 控件布局（右对齐）
        self.control_layout = QHBoxLayout()
        self.control_layout.setContentsMargins(0, 0, 0, 0)
        self.control_layout.setSpacing(0)
        
        header_layout.addLayout(self.control_layout)
        
        # 第二行 放描述标签
        self.desc_label = QLabel()
        self.desc_label.setStyleSheet(SS_player_SettingItemCard_Desc)
        layout.addWidget(self.desc_label)
        
        self.update_style()
    
    def mousePressEvent(self, event):
        """处理鼠标点击事件"""
        if event.button() == Qt.MouseButton.MiddleButton:
            # 鼠标中键点击，恢复默认值
            self._reset_to_default()
        super().mousePressEvent(event)
    
    def _reset_to_default(self):
        """恢复默认值"""
        if not self.setting_name or not self.setting_data:
            return
        
        # 获取默认值
        default_value = self.setting_data.get('default', False)
        
        # 查找对应的控件
        player_page = None
        widget = self
        while widget:
            # 避免循环导入，使用字符串比较类名
            if widget.__class__.__name__ == 'PlayerPage':
                player_page = widget
                break
            widget = widget.parent()
        
        if player_page:
            # 检查当前值是否与默认值不同
            current_value = player_page.player_settings.get('finalSettings', {}).get(self.setting_name, False)
            
            # 如果当前值与默认值不同，才进行后续操作
            if current_value != default_value:
                # 更新控件值
                if self.setting_name in player_page.setting_widgets:
                    control = player_page.setting_widgets[self.setting_name]
                    
                    # 根据控件类型设置默认值
                    setting_type = self.setting_data.get('type', 'boolean')
                    if setting_type == 'boolean':
                        if hasattr(control, 'setChecked'):
                            control.setChecked(default_value)
                    elif setting_type == 'dropdown':
                        if hasattr(control, 'setCurrentText'):
                            control.setCurrentText(str(default_value))
                    elif setting_type == 'integer':
                        if hasattr(control, 'setValue'):
                            control.setValue(int(default_value))
                    elif setting_type in ['integer_slider', 'float_slider']:
                        # 对于滑块类型，需要找到实际的slider控件
                        slider = None
                        value_label = None
                        
                        # 检查control是否是容器
                        if hasattr(control, 'findChildren'):
                            # 查找slider控件
                            sliders = control.findChildren(QSlider)
                            if sliders:
                                slider = sliders[0]
                            # 查找value_label控件
                            labels = control.findChildren(QLabel)
                            if labels:
                                value_label = labels[0]
                        
                        if slider:
                            if setting_type == 'float_slider':
                                # 对于浮点滑块，需要进行缩放处理
                                # 查找缩放因子
                                scale = 1
                                min_val = float(self.setting_data.get('min', 0.0))
                                max_val = float(self.setting_data.get('max', 100.0))
                                step_val = float(self.setting_data.get('step', 0.1))
                                
                                # 计算缩放因子
                                while step_val * scale % 1 != 0:
                                    scale *= 10
                                
                                # 设置缩放后的值
                                slider.setValue(int(float(default_value) * scale))
                                
                                # 更新value_label
                                if value_label:
                                    # 计算小数位数
                                    decimal_places = len(str(step_val).split('.')[1]) if '.' in str(step_val) else 0
                                    value_label.setText(f"{float(default_value):.{decimal_places}f}")
                            else:
                                # 对于整数滑块，直接设置值
                                slider.setValue(int(default_value))
                                
                                # 更新value_label
                                if value_label:
                                    value_label.setText(str(int(default_value)))
                    
                    # 更新player_settings
                    if 'finalSettings' in player_page.player_settings:
                        player_page.player_settings['finalSettings'][self.setting_name] = default_value
                    
                    # 保存到文件
                    player_settings_path = getattr(player_page, 'player_settings_path', None)
                    if player_settings_path:
                        player_page._save_player_settings_to_file(player_page.player_settings, player_settings_path)
                    
                    # 调用update_all_configs函数更新所有配置
                    if player_settings_path:
                        from utils.xml_operations import XmlOperations
                        
                        # 从player_settings_path推导出flexmod_json_path和mod_files_dir
                        # 获取FlexMod目录
                        flexmod_dir = os.path.dirname(player_settings_path)
                        # 获取mod_files_dir
                        mod_files_dir = os.path.dirname(flexmod_dir)
                        # 获取flexmod_json_path
                        flexmod_json_path = os.path.join(flexmod_dir, 'FlexMod.json')
                        
                        # 调用XmlOperations.update_all_configs方法
                        XmlOperations.update_all_configs(player_settings_path, flexmod_json_path, mod_files_dir)
                        
                        # 显示成功通知
                        # 获取功能名称
                        setting_display_name = self.setting_data.get('showName', self.setting_name)
                        
                        # 获取语言设置
                        lang = get_lang()
                        
                        # 格式化默认值
                        formatted_value = default_value
                        if setting_type == 'boolean':
                            # 根据语言格式化布尔值
                            if lang == 0:
                                formatted_value = 'On' if default_value else 'Off'
                            else:
                                formatted_value = '开启' if default_value else '关闭'
                        elif setting_type == 'float_slider':
                            # 计算小数位数并格式化浮点值
                            step_val = float(self.setting_data.get('step', 0.1))
                            decimal_places = len(str(step_val).split('.')[1]) if '.' in str(step_val) else 0
                            formatted_value = f"{float(default_value):.{decimal_places}f}"
                        
                        # 获取多语言消息
                        reset_message = "reset to default value" if lang == 0 else "恢复到默认值"
                        
                        # 创建通知消息
                        message = f"[{setting_display_name}] {reset_message} [{formatted_value}]"
                        
                        # 显示通知（使用自定义的NotificationWidget）
                        from .notification_widget import NotificationWidget
                        notification = NotificationWidget(
                            notification_type=NotificationWidget.TYPE_SUCCESS,
                            message=message,
                            lang=lang,  
                            timeout=2000  # 2秒后自动关闭
                        )
                        notification.show()
    
    def set_description(self, description: str):
        """设置描述"""
        self.desc_label.setText(description)
        # 如果描述为空，隐藏描述标签
        self.desc_label.setVisible(bool(description))
    
    def add_control(self, widget):
        """添加控件"""
        # 设置控件的内部边距为0，背景为透明
        if hasattr(widget, 'setStyleSheet'):
            widget.setStyleSheet(widget.styleSheet() + "margin: 0; padding: 0; background-color: transparent;")
        self.control_layout.addWidget(widget)
    
    def update_style(self):
        """更新样式"""
        self.setStyleSheet(SS_player_SettingItemCard)


class PlayerPage(QWidget):
    """玩家页面
    
    用于显示和管理FlexMod的玩家设置，包括：
    - 预设管理（保存、删除、应用预设）
    - 设置调整（根据FlexMod配置显示不同类型的控件）
    - 实时更新最终设置
    - 支持设置分组显示
    
    Args:
        config_manager (ConfigManager): 配置管理器实例
    """
    
    def __init__(self, config_manager: ConfigManager):
        super().__init__()
        self.config_manager = config_manager
        self.lang = get_lang()
        self.current_flexmod = None
        self.presets = {}
        self.mods_dir = config_manager.get_mods_dir()
        self._init_ui()
    
    def _init_ui(self):
        """初始化UI
        
        构建玩家页面的UI布局，包括：
        - 预设管理区域（预设选择、保存、删除、应用按钮）
        - 设置显示区域（滚动区域，用于显示设置项）
        """
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        self.setLayout(layout)
        
        # 预设管理区域
        preset_layout = QHBoxLayout()
        preset_layout.setSpacing(10)
        preset_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # 添加预设标签
        self.preset_label = QLabel(get_text('preset', self.lang) + ':')
        
        self.preset_label.setStyleSheet(SS_preset_label)
        preset_layout.addWidget(self.preset_label)
        
        # 预设选择
        self.preset_combo = QComboBox()
        self.preset_combo.setStyleSheet(SS_preset_combo)
        preset_layout.addWidget(self.preset_combo)
        
        # 保存预设按钮
        self.save_preset_btn = QPushButton(get_text('save_as', self.lang))
        self.save_preset_btn.setStyleSheet(SS_preset_btn)
        self.save_preset_btn.setMaximumWidth(100)
        self.save_preset_btn.clicked.connect(self._save_preset)
        preset_layout.addWidget(self.save_preset_btn)
        
        # 删除预设按钮
        self.delete_preset_btn = QPushButton(get_text('delete', self.lang))
        self.delete_preset_btn.setStyleSheet(SS_preset_btn)
        self.delete_preset_btn.setMaximumWidth(100)
        self.delete_preset_btn.clicked.connect(self._delete_preset)
        preset_layout.addWidget(self.delete_preset_btn)
        
        
        
        # 应用预设按钮
        self.apply_preset_btn = QPushButton(get_text('use', self.lang))
        self.apply_preset_btn.setStyleSheet(SS_preset_btn)
        self.apply_preset_btn.setMaximumWidth(100)
        self.apply_preset_btn.clicked.connect(self._apply_preset)
        preset_layout.addWidget(self.apply_preset_btn)

        #添加弹簧
        preset_layout.addStretch()

        # 恢复默认预设按钮
        self.default_preset_btn = QPushButton(get_text('default', self.lang))
        self.default_preset_btn.setStyleSheet(SS_preset_btn)
        self.default_preset_btn.setMaximumWidth(200)
        self.default_preset_btn.clicked.connect(self._load_default_preset)
        preset_layout.addWidget(self.default_preset_btn)
        
        layout.addLayout(preset_layout)
        
        # FlexMod设置区域
        self.settings_scroll = QScrollArea()
        self.settings_scroll.setStyleSheet(SS_player_scroll_area)
        
        self.settings_container = QWidget()
        self.settings_layout = QVBoxLayout()
        self.settings_layout.setContentsMargins(10, 10, 10, 10)
        self.settings_layout.setSpacing(15)
        self.settings_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.settings_container.setLayout(self.settings_layout)
        
        self.settings_scroll.setWidget(self.settings_container)
        self.settings_scroll.setWidgetResizable(True)
        layout.addWidget(self.settings_scroll, 1)
        

    
    def set_current_flexmod(self, flexmod_name: str):
        """设置当前FlexMod"""
        self.current_flexmod = flexmod_name
        self._load_flexmod_settings()
        self._load_presets()
    
    def _load_flexmod_settings(self):
        """加载FlexMod设置
        
        加载并显示当前选择的FlexMod的设置，流程如下：
        1. 清空当前设置容器
        2. 检查Mods目录是否存在
        3. 检查并获取FlexMod.json文件路径
        4. 加载和解析配置文件
        5. 加载或创建玩家设置文件
        6. 验证和修复玩家设置（确保与FlexMod配置同步）
        7. 保存玩家设置到实例变量
        8. 按组组织设置并创建设置界面
        
        异常处理：
        - 捕获所有异常并显示错误信息，确保应用程序不会崩溃
        """
        if not self.current_flexmod:
            return
        
        try:
            # 清空设置容器
            self._clear_settings_container()
            
            # 检查Mods目录
            mods_dir = self._check_mods_directory()
            if not mods_dir:
                return
            
            # 检查并获取FlexMod.json路径
            flexmod_json_path = self._check_flexmod_json(mods_dir)
            if not flexmod_json_path:
                return
            
            # 加载和解析配置
            settings, groups = self._load_and_parse_config(flexmod_json_path)
            
            # 加载或创建玩家设置
            player_settings, player_settings_path = self._load_or_create_player_settings(mods_dir, settings)
            
            # 验证和修复玩家设置
            player_settings = self._validate_and_fix_player_settings(player_settings, settings, player_settings_path)
            
            # 保存玩家设置到实例变量
            self.player_settings = player_settings
            self.player_settings_path = player_settings_path
            
            # 按组组织设置并创建设置界面
            self._organize_and_create_settings(settings, groups)
            
        except Exception as e:
            # 显示错误信息
            self._show_error_message(f"{get_text('error_loading_settings', self.lang)}: {str(e)}")
    
    def _clear_settings_container(self):
        """清空设置容器"""
        while self.settings_layout.count() > 0:
            widget = self.settings_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()
    
    def _check_mods_directory(self):
        """检查Mods目录"""
        mods_dir = self.config_manager.get_mods_dir()
        if not mods_dir:
            self._show_error_message(get_text('please_set_mods_dir', self.lang))
            return None
        
        if not os.path.exists(mods_dir):
            self._show_error_message(get_text('mods_dir_not_exists', self.lang))
            return None
        
        return mods_dir
    
    def _check_flexmod_json(self, mods_dir):
        """检查并获取FlexMod.json路径"""
        flexmod_json_path = os.path.join(mods_dir, self.current_flexmod, 'FlexMod', 'FlexMod.json')
        
        if not os.path.exists(flexmod_json_path):
            self._show_error_message(get_text('flexmod_json_not_found', self.lang))
            return None
        
        return flexmod_json_path
    
    def _load_and_parse_config(self, flexmod_json_path):
        """加载和解析配置"""
        try:
            with open(flexmod_json_path, 'r', encoding='utf-8') as f:
                try:
                    flexmod_data = json.load(f)
                except json.JSONDecodeError as e:
                    self._show_error_message(f"JSON解析错误: {str(e)}")
                    return {}, {}
        except Exception as e:
            self._show_error_message(f"文件读取错误: {str(e)}")
            return {}, {}
        
        # 解析设置（只支持新格式）
        settings = {}
        groups = {}
        
        # 解析新格式
        if 'configs' in flexmod_data:
            try:
                self._parse_new_format(flexmod_data, settings, groups)
            except Exception as e:
                self._show_error_message(f"解析配置错误: {str(e)}")
                return {}, {}
        
        return settings, groups
    
    def _parse_new_format(self, flexmod_data, settings, groups):
        """解析新格式配置"""
        configs = flexmod_data.get('configs', [])
        # 解析组信息
        self._parse_groups(flexmod_data, groups)
        
        # 转换配置为settings格式
        for config in configs:
            self._parse_config_item(config, settings)
    
    def _parse_groups(self, flexmod_data, groups):
        """解析组信息"""
        raw_groups = flexmod_data.get('groups', [])
        for group in raw_groups:
            group_name = group.get('groupName', 'default')
            groups[group_name] = {
                'displayName': group.get('groupName', group_name),
                'groupDesc': group.get('groupDesc', '')
            }
    
    def _parse_config_item(self, config, settings):
        """解析单个配置项"""
        setting_name = config.get('uniqueId', '')
        if setting_name:
            # 映射类型
            config_type = config.get('configType', 'text')
            setting_type = self._map_config_type(config_type)
            
            setting_data = {
                'type': setting_type,
                'default': config.get('defaultValue', False),
                'showName': config.get('displayName', setting_name),
                'desc': config.get('desc', ''),
                'group': config.get('groupName', 'default')
            }
            
            # 处理特定类型的配置
            if setting_type == 'dropdown':
                self._parse_dropdown_config(config, setting_data)
            elif setting_type == 'integer_slider' or setting_type == 'float_slider':
                self._parse_slider_config(config, setting_data)
            
            settings[setting_name] = setting_data
    
    def _parse_dropdown_config(self, config, setting_data):
        """解析下拉菜单配置"""
        options = []
        option_items = config.get('optionItems', [])
        for item in option_items:
            option_key = item.get('optionKey', '')
            if option_key:
                options.append(option_key)
        setting_data['options'] = options
    
    def _parse_slider_config(self, config, setting_data):
        """解析滑块配置"""
        # 保持原始类型，不强制转换为整数
        setting_data['min'] = config.get('minValue', 0)
        setting_data['max'] = config.get('maxValue', 100)
        setting_data['step'] = config.get('stepValue', 1)
    

    
    def _map_config_type(self, config_type):
        """映射配置类型"""
        type_map = {
            'boolConfig': 'boolean',
            'stringConfig': 'text',
            'numberConfig': 'integer',
            'selectConfig': 'dropdown',
            'intSlider': 'integer_slider',
            'floatSlider': 'float_slider'
        }
        return type_map.get(config_type, 'text')
    
    def _load_or_create_player_settings(self, mods_dir, settings):
        """加载或创建玩家设置"""
        player_settings_path = os.path.join(mods_dir, self.current_flexmod, 'FlexMod', 'player_settings.json')
        player_settings = {}
        
        if os.path.exists(player_settings_path):
            # 加载现有文件
            try:
                with open(player_settings_path, 'r', encoding='utf-8') as f:
                    try:
                        player_settings = json.load(f)
                    except json.JSONDecodeError as e:
                        self._show_error_message(f"玩家设置文件解析错误: {str(e)}")
                        # 创建默认设置
                        player_settings = self._create_default_player_settings(settings)
                        # 保存默认设置
                        self._save_player_settings_to_file(player_settings, player_settings_path)
            except Exception as e:
                self._show_error_message(f"读取玩家设置文件错误: {str(e)}")
                # 创建默认设置
                player_settings = self._create_default_player_settings(settings)
                # 保存默认设置
                self._save_player_settings_to_file(player_settings, player_settings_path)
        else:
            # 创建默认文件
            player_settings = self._create_default_player_settings(settings)
            # 保存默认设置
            self._save_player_settings_to_file(player_settings, player_settings_path)
        
        return player_settings, player_settings_path
    
    def _create_default_player_settings(self, settings):
        """创建默认玩家设置"""
        default_settings = {}
        for setting_name, setting_data in settings.items():
            default_settings[setting_name] = setting_data.get('default', False)
        
        return {
            'finalSettings': default_settings.copy(),
            'defaultValues': default_settings.copy(),
            'presets': {}
        }
    
    def _save_player_settings_to_file(self, player_settings, player_settings_path):
        """保存玩家设置到文件"""
        try:
            # 确保FlexMod目录存在
            flexmod_dir = os.path.dirname(player_settings_path)
            if not os.path.exists(flexmod_dir):
                os.makedirs(flexmod_dir)
            
            # 写入文件
            with open(player_settings_path, 'w', encoding='utf-8') as f:
                json.dump(player_settings, f, indent=4, ensure_ascii=False)
        except Exception as e:
            self._show_error_message(f"保存玩家设置文件错误: {str(e)}")
    
    def _validate_and_fix_player_settings(self, player_settings, settings, player_settings_path):
        """验证和修复玩家设置"""
        try:
            # 1. 获取所有有效的设置名称
            valid_setting_names = set(settings.keys())
            
            # 2. 获取当前player_settings中的设置名称
            current_final_settings = player_settings.get('finalSettings', {})
            current_default_values = player_settings.get('defaultValues', {})
            current_setting_names = set(current_final_settings.keys())
            
            # 3. 找出需要添加的设置（FlexMod有但player_settings没有）
            settings_to_add = valid_setting_names - current_setting_names
            
            # 4. 找出需要删除的设置（FlexMod没有但player_settings有）
            settings_to_remove = current_setting_names - valid_setting_names
            
            # 5. 添加缺失的设置
            for setting_name in settings_to_add:
                setting_data = settings[setting_name]
                default_value = setting_data.get('default', False)
                current_final_settings[setting_name] = default_value
                current_default_values[setting_name] = default_value
            
            # 6. 删除多余的设置
            for setting_name in settings_to_remove:
                if setting_name in current_final_settings:
                    del current_final_settings[setting_name]
                if setting_name in current_default_values:
                    del current_default_values[setting_name]
            
            # 7. 检查并更新现有设置的默认值
            for setting_name in current_setting_names:
                if setting_name in valid_setting_names:
                    setting_data = settings[setting_name]
                    new_default_value = setting_data.get('default', False)
                    # 如果默认值发生变化，更新 player_settings
                    if current_default_values.get(setting_name) != new_default_value:
                        current_default_values[setting_name] = new_default_value
                        # 如果当前最终值等于旧默认值，也更新最终值
                        if current_final_settings.get(setting_name) == player_settings.get('defaultValues', {}).get(setting_name):
                            current_final_settings[setting_name] = new_default_value
            
            # 8. 更新player_settings
            player_settings['finalSettings'] = current_final_settings
            player_settings['defaultValues'] = current_default_values
            
            # 9. 保存到文件
            self._save_player_settings_to_file(player_settings, player_settings_path)
        except Exception as e:
            self._show_error_message(f"验证和修复玩家设置错误: {str(e)}")
        
        return player_settings
    
    def _organize_and_create_settings(self, settings, groups):
        """按组组织设置并创建设置界面"""
        # 按组组织设置
        settings_by_group = {}
        for setting_name, setting_data in settings.items():
            group = setting_data.get('group', 'default')
            if group not in settings_by_group:
                settings_by_group[group] = []
            settings_by_group[group].append((setting_name, setting_data))
        
        # 创建设置界面
        self.setting_widgets = {}
        for group_name, group_settings in settings_by_group.items():
            if group_name == 'default':
                # 没有组的设置，单独显示
                for setting_name, setting_data in group_settings:
                    widget = self._create_setting_widget(setting_name, setting_data)
                    self.setting_widgets[setting_name] = widget
            else:
                # 有组的设置，创建组卡片
                self._create_group_card(group_name, group_settings, groups)
    
    def _create_group_card(self, group_name, group_settings, groups):
        """创建组卡片"""
        # 查找组数据
        group_data = {}
        if isinstance(groups, list):
            # 如果 groups 是列表，遍历查找匹配的组
            for g in groups:
                if g.get('groupName') == group_name:
                    group_data = g
                    break
        else:
            # 如果 groups 是字典，直接通过键获取
            group_data = groups.get(group_name, {})
        
        # 获取组显示名称和描述
        group_display_name = group_data.get('displayName', group_data.get('groupName', group_name))
        # 如果组名为Default，显示为Default Group，以避免歧义
        if group_display_name == 'Default':
            group_display_name = 'Default Group'
        group_desc = group_data.get('groupDesc', '')
        
        # 创建组卡片容器
        group_card = SettingCard(group_display_name)
        
        # 添加组描述
        group_card.add_description(group_desc)
        
        # 添加组内的设置卡片
        for setting_name, setting_data in group_settings:
            # 获取设置的显示名称和描述
            setting_display_name = setting_data.get('showName', setting_name)
            setting_desc = setting_data.get('desc', '')
            
            # 创建设置项卡片
            setting_card = SettingItemCard(setting_display_name, setting_name, setting_data)
            setting_card.set_description(setting_desc)
            
            # 根据设置类型创建不同的控件
            setting_type = setting_data.get('type', 'text')
            
            # 获取当前值（从最终设置中加载）
            current_value = self.player_settings.get('finalSettings', {}).get(setting_name, setting_data.get('default', False))
            
            # 创建对应的控件
            if setting_type == 'boolean':
                widget = self._create_boolean_widget(setting_name, current_value)
            elif setting_type == 'dropdown':
                widget = self._create_dropdown_widget(setting_name, setting_data, current_value)
            elif setting_type == 'integer':
                widget = self._create_integer_widget(setting_name, current_value)
            elif setting_type == 'integer_slider' or setting_type == 'float_slider':
                widget = self._create_slider_widget(setting_name, setting_data, current_value, setting_type)
            else:
                # 默认布尔值控件
                widget = self._create_boolean_widget(setting_name, bool(current_value))
            
            # 添加控件到设置项卡片
            setting_card.add_control(widget)
            
            # 添加设置项卡片到组卡片
            group_card.add_setting_item(setting_card)
            
            # 保存控件引用
            self.setting_widgets[setting_name] = widget
        
        self.settings_layout.addWidget(group_card)
    
    def _show_error_message(self, message):
        """显示错误信息"""
        error_label = QLabel(message)
        error_label.setStyleSheet("color: #ff6b6b; font-size: 14px;")
        self.settings_layout.addWidget(error_label)
    

    
    def _create_setting_widget(self, setting_name: str, setting_data: Dict, parent_layout=None):
        """创建设置控件"""
        if parent_layout is None:
            parent_layout = self.settings_layout
        
        # 获取设置的显示名称和描述
        setting_display_name = setting_data.get('showName', setting_name)
        setting_desc = setting_data.get('desc', '')
        
        # 创建设置项卡片
        setting_card = SettingItemCard(setting_display_name, setting_name, setting_data)
        setting_card.set_description(setting_desc)
        
        # 根据设置类型创建不同的控件
        setting_type = setting_data.get('type', 'text')
        
        # 获取当前值（从最终设置中加载）
        current_value = self.player_settings.get('finalSettings', {}).get(setting_name, setting_data.get('default', False))
        
        # 创建对应的控件
        if setting_type == 'boolean':
            widget = self._create_boolean_widget(setting_name, current_value)
        elif setting_type == 'dropdown':
            widget = self._create_dropdown_widget(setting_name, setting_data, current_value)
        elif setting_type == 'integer':
            widget = self._create_integer_widget(setting_name, current_value)
        elif setting_type == 'integer_slider' or setting_type == 'float_slider':
            widget = self._create_slider_widget(setting_name, setting_data, current_value, setting_type)
    
        
        # 添加控件到卡片
        setting_card.add_control(widget)
        
        parent_layout.addWidget(setting_card)
        
        # 返回创建的控件
        return widget
    
    def _create_boolean_widget(self, setting_name: str, current_value: bool):
        """创建布尔值（开关）控件"""
        widget = ToggleSwitch()
        widget.setChecked(current_value)
        
        # 添加值变化信号
        def on_boolean_changed(checked):
            self.player_settings['finalSettings'][setting_name] = checked
            self._save_player_settings()
        
        widget.toggled.connect(on_boolean_changed)
        return widget
    
    def _create_dropdown_widget(self, setting_name: str, setting_data: Dict, current_value: str):
        """创建下拉选择控件"""
        widget = QComboBox()
        from .flex_mod_color import SS_player_SettingItemCard_dropdown_widget
        widget.setStyleSheet(SS_player_SettingItemCard_dropdown_widget)

        options = setting_data.get('options', [])
        for option in options:
            widget.addItem(option, option)
        default = setting_data.get('default', '')
        if current_value in options:
            # 找到当前值的索引
            for i in range(widget.count()):
                if widget.itemData(i) == current_value:
                    widget.setCurrentIndex(i)
                    break
        elif default in options:
            # 找到默认选项的索引S
            for i in range(widget.count()):
                if widget.itemData(i) == default:
                    widget.setCurrentIndex(i)
                    break
        
        # 添加值变化信号
        def on_dropdown_changed(index):
            selected_value = widget.itemData(index)
            self.player_settings['finalSettings'][setting_name] = selected_value
            self._save_player_settings()
        
        widget.currentIndexChanged.connect(on_dropdown_changed)
        return widget
    

    
    def _create_slider_widget(self, setting_name: str, setting_data: Dict, current_value, setting_type):
        """创建滑块控件（支持整数和浮点数）"""
        # 创建滑块容器
        slider_container = QWidget()
        from .flex_mod_color import _NO_BBBO
        slider_container.setStyleSheet(_NO_BBBO(1,1,1,1))
        slider_layout = QHBoxLayout()
        slider_layout.setContentsMargins(0, 0, 0, 0)
        slider_layout.setSpacing(4)
        slider_container.setLayout(slider_layout)
        
        # 创建滑块
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setStyleSheet(SS_player_SettingItemCard_slider_widget)
        
        # 根据滑块类型处理不同的逻辑
        if setting_type == 'integer_slider':
            # 整数滑块处理
            min_val = int(setting_data.get('min', 0))
            max_val = int(setting_data.get('max', 100))
            step_val = int(setting_data.get('step', 1))
            current_val = int(current_value)
            
            slider.setMinimum(min_val)
            slider.setMaximum(max_val)
            slider.setValue(current_val)
            slider.setSingleStep(step_val)
            
            # 创建值标签
            value_label = QLabel(str(current_val))

            value_label.setStyleSheet(SS_player_SettingItemCard_slider_widget_value_label)
            
            # 连接滑块值变化信号
            def on_slider_value_changed(value):
                value_label.setText(str(value))
                self.player_settings['finalSettings'][setting_name] = value
                self._save_player_settings()
                
        elif setting_type == 'float_slider':
            # 浮点滑块处理
            min_val = float(setting_data.get('min', 0.0))
            max_val = float(setting_data.get('max', 100.0))
            step_val = float(setting_data.get('step', 0.1))
            current_val = float(current_value)
            
            # 为了使用QSlider（只支持整数），我们需要进行缩放
            # 计算缩放因子，确保step_val * scale是整数
            scale = 1
            while step_val * scale % 1 != 0:
                scale *= 10
            
            slider.setMinimum(int(min_val * scale))
            slider.setMaximum(int(max_val * scale))
            slider.setValue(int(current_val * scale))
            slider.setSingleStep(int(step_val * scale))
            
            # 计算小数位数
            decimal_places = len(str(step_val).split('.')[1]) if '.' in str(step_val) else 0
            
            # 创建值标签
            value_label = QLabel(f"{current_val:.{decimal_places}f}")
            value_label.setStyleSheet(SS_player_SettingItemCard_slider_widget_value_label)
            
            # 连接滑块值变化信号
            def on_slider_value_changed(value):
                # 转换回浮点数
                float_value = value / scale
                # 四舍五入到合适的小数位数
                rounded_value = round(float_value, decimal_places)
                value_label.setText(f"{rounded_value:.{decimal_places}f}")
                self.player_settings['finalSettings'][setting_name] = rounded_value
                self._save_player_settings()
        
        slider.valueChanged.connect(on_slider_value_changed)
        
        # 添加到容器
        slider_layout.addWidget(slider)
        slider_layout.addWidget(value_label)
        
        return slider_container
    

    
    def _load_presets(self):
        """加载预设"""
        if not self.current_flexmod:
            return
        
        # 清空预设组合框
        self.preset_combo.clear()
        
        # 从player_settings中加载预设
        if hasattr(self, 'player_settings'):
            # 加载预设
            self.presets = self.player_settings.get('presets', {})
            
            # 添加预设到组合框
            for preset_name in self.presets:
                self.preset_combo.addItem(preset_name)
        else:
            self.presets = {}
    
    def _save_presets(self):
        """保存预设"""
        if not self.current_flexmod or not hasattr(self, 'player_settings'):
             # 检查是否有当前FlexMod实例和player_settings属性
            return
        
        # 将预设保存到player_settings中
        self.player_settings['presets'] = self.presets
        
        # 保存到文件
        self._save_player_settings()
    
    def _save_preset(self):
        """保存预设
        
        将当前的最终设置保存为新的预设，流程如下：
        1. 检查是否选择了FlexMod
        2. 弹出对话框获取预设名称
        3. 如果用户取消或未输入名称，则返回
        4. 从最终设置中收集当前值
        5. 将设置保存为预设
        6. 保存预设到玩家设置文件
        7. 更新预设列表
        8. 显示保存成功的提示信息
        """
        if not self.current_flexmod:
            return
        
        # 获取预设名称
        preset_name, ok = QInputDialog.getText(self, get_text('save_preset', self.lang), get_text('preset_name', self.lang))
        if not ok or not preset_name:
            return
        
        # 从最终设置中收集值
        settings = self.player_settings.get('finalSettings', {}).copy()
        
        # 保存预设
        self.presets[preset_name] = settings
        self._save_presets()
        
        self._load_presets()
        
        QMessageBox.information(self, get_text('info', self.lang), get_text('preset_saved', self.lang))
    

    
    def _delete_preset(self):
        """删除预设"""
        if not self.current_flexmod:
            return
        
        preset_name = self.preset_combo.currentText()
        if not preset_name:
            return
        
        if preset_name in self.presets:
            # 显示确认弹窗
            if self.lang == 'en':
                confirm_text = f"Are you sure you want to delete preset '{preset_name}'?"
            else:
                confirm_text = f"确定要删除预设 '{preset_name}' 吗？"
            reply = QMessageBox.question(self, get_text('confirm', self.lang), confirm_text,
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            
            if reply == QMessageBox.StandardButton.Yes:
                del self.presets[preset_name]
                self._save_presets()
                self._load_presets()
                QMessageBox.information(self, get_text('info', self.lang), get_text('preset_deleted', self.lang))
    
    def _load_default_preset(self):
        """加载默认预设"""
        if not self.current_flexmod:
            return
        
        #给个弹窗 询问用户是否把全部设置恢复到默认值
        if self.lang == 0:
            confirm_text = "Are you sure you want to reset all settings to default values?"
        else:
            confirm_text = "确定要把所有设置恢复到默认值吗？"
        reply = QMessageBox.question(self, get_text('confirm', self.lang), confirm_text,
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.No:
            return

        # 从默认值中加载
        default_settings = self.player_settings.get('defaultValues', {})
        
        # 更新最终设置
        self.player_settings['finalSettings'] = default_settings.copy()
        self._save_player_settings()
        
        # 重新加载设置界面以更新控件值
        self._load_flexmod_settings()
        
        QMessageBox.information(self, get_text('info', self.lang), get_text('default_preset_loaded', self.lang))
    
    def update_language(self):
        """更新语言"""
        self.lang = get_lang()
        
        # 更新预设管理区域的文本
        if hasattr(self, 'preset_label'):
            self.preset_label.setText(get_text('preset', self.lang) + ':')
        if hasattr(self, 'save_preset_btn'):
            self.save_preset_btn.setText(get_text('save_as', self.lang))
        if hasattr(self, 'delete_preset_btn'):
            self.delete_preset_btn.setText(get_text('delete', self.lang))
        if hasattr(self, 'default_preset_btn'):
            self.default_preset_btn.setText(get_text('default', self.lang))
        if hasattr(self, 'apply_preset_btn'):
            self.apply_preset_btn.setText(get_text('use', self.lang))
        
        # 重新加载预设列表
        self._load_presets()
        
        # 如果当前有选择的FlexMod，重新加载设置
        if self.current_flexmod:
            self._load_flexmod_settings()
    
    def _save_player_settings(self):
        """保存玩家设置到文件"""
        if not self.current_flexmod or not hasattr(self, 'player_settings_path'):
            return
        
        try:
            with open(self.player_settings_path, 'w', encoding='utf-8') as f:
                json.dump(self.player_settings, f, indent=4, ensure_ascii=False)
            
            # 执行更新全部的操作
            if hasattr(self, 'mods_dir') and hasattr(self, 'current_flexmod'):
                # 构建FlexMod JSON文件的路径
                flexmod_json_path = os.path.join(self.mods_dir, self.current_flexmod, 'FlexMod', 'FlexMod.json')
                # 构建mod文件所在的目录
                mod_files_dir = os.path.join(self.mods_dir, self.current_flexmod)
                # 调用update_all_configs函数
                XmlOperations.update_all_configs(self.player_settings_path, flexmod_json_path, mod_files_dir)
        except Exception as e:
            print(f"保存玩家设置失败: {e}")
    
    def _apply_preset(self):
        """应用预设"""
        if not self.current_flexmod:
            return
        
        preset_name = self.preset_combo.currentText()
        if not preset_name or preset_name not in self.presets:
            return
        
        # 应用预设设置
        preset_settings = self.presets[preset_name]
        
        # 更新最终设置
        self.player_settings['finalSettings'] = preset_settings.copy()
        self._save_player_settings()
        
        # 重新加载设置界面以更新控件值
        self._load_flexmod_settings()
        
        QMessageBox.information(self, get_text('info', self.lang), get_text('preset_applied', self.lang))

