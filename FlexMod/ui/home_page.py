"""主页窗口"""
import os
import json
import logging
from typing import Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton,
    QMessageBox, QFileDialog, QLabel, QDialog, QDialogButtonBox,
    QSplitter, QGraphicsDropShadowEffect, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QColor

from ..utils.lang import get_text, get_lang
from .player_page import PlayerPage
from .flex_mod_color import (SS_home_splitter,
                             SS_home_splitter_left_widget,
                             SS_flexmod_list,
                             SS_btn)


class HomePage(QWidget):
    """主页窗口"""
    
    flexmod_opened = pyqtSignal(str)
    
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.lang = get_lang()
        self.player_mode_enabled = self.config_manager.get_config('player_mode_enabled', False)
        self.selected_flexmod = None
        self._init_ui()
        self._load_flexmod_list()
    
    def _init_ui(self):
        """初始化UI"""
        # 如果已经初始化过，只更新文本
        if hasattr(self, 'flexmod_list'):
            self._update_language()
            return
            
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        self.setLayout(layout)
        
        # 创建2列式布局
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.setStyleSheet(SS_home_splitter)
        
        # 左侧：FlexMod列表和控制按钮
        left_widget = QWidget()
        left_widget.setStyleSheet(SS_home_splitter_left_widget)
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(5, 5,5, 5)
        left_layout.setSpacing(5)
        left_widget.setLayout(left_layout)
        
        # FlexMod列表
        self.flexmod_list = QListWidget()
        self.flexmod_list.setStyleSheet(SS_flexmod_list)
        self.flexmod_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)# 单选模式
        self.flexmod_list.itemDoubleClicked.connect(self._on_item_double_clicked)
        self.flexmod_list.itemClicked.connect(self._on_item_clicked)
        

        
        flexmod_list_shadow = QGraphicsDropShadowEffect()    # 为导航栏容器添加柔化阴影
        flexmod_list_shadow.setBlurRadius(20)  # 模糊半径
        flexmod_list_shadow.setColor(QColor(0, 0, 0, 150))  # 阴影颜色，带透明度
        flexmod_list_shadow.setOffset(0, 5)  # 阴影偏移
        self.flexmod_list.setGraphicsEffect(flexmod_list_shadow) 


        left_layout.addWidget(self.flexmod_list) 

        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # 刷新按钮（图标按钮）
        self.refresh_btn = QPushButton()
        self.refresh_btn.setStyleSheet(SS_btn)
        # 设置固定大小，确保它不会扩展
        self.refresh_btn.setFixedSize(32, 32)
        # 加载图标
        try:
            from ..managers.resource_manager import resource_manager
            sync_icon = resource_manager.get_icon('sync.png')
            if not sync_icon.isNull():
                self.refresh_btn.setIcon(sync_icon)
        except Exception as e:
            pass
        self.refresh_btn.clicked.connect(self._load_flexmod_list)
        button_layout.addWidget(self.refresh_btn)
        
        # 添加按钮
        self.add_btn = QPushButton(get_text('add_flexmod_btn', self.lang))
        self.add_btn.setStyleSheet(SS_btn)
        # 设置按钮的大小策略为扩展，让它占据所有可用空间
        self.add_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        # 设置最小宽度，确保按钮有足够的空间显示文本
        self.add_btn.setMinimumWidth(100)
        self.add_btn.clicked.connect(self._add_flexmod)
        button_layout.addWidget(self.add_btn)
        
        # 玩家模式切换按钮（图标按钮）
        self.player_mode_btn = QPushButton()
        self.player_mode_btn.setStyleSheet(SS_btn)
        # 设置固定大小，确保它不会扩展
        self.player_mode_btn.setFixedSize(32, 32)
        self.player_mode_btn.setCheckable(True)
        self.player_mode_btn.setChecked(self.player_mode_enabled)
        # 加载图标
        try:
            # 动态导入 resource_manager 避免循环依赖
            from ..managers.resource_manager import resource_manager
            control_icon = resource_manager.get_icon('control.png')
            if not control_icon.isNull():
                self.player_mode_btn.setIcon(control_icon)
        except Exception as e:
            pass
        self.player_mode_btn.clicked.connect(self._toggle_player_mode)
        button_layout.addWidget(self.player_mode_btn)
        
        left_layout.addLayout(button_layout)

        # 设置伸缩因子，让列表占据主要空间
        left_layout.setStretch(0, 1)  # 列表
        left_layout.setStretch(1, 0)  # 按钮布局
        
        # 右侧：玩家页面
        self.player_page = PlayerPage(self.config_manager)
        # self.player_page.setMinimumWidth(400)
        
        # 添加到splitter
        self.splitter.addWidget(left_widget)
        self.splitter.addWidget(self.player_page)
        
        # 设置初始大小
        self.splitter.setSizes([300, 600])
        
        layout.addWidget(self.splitter, 1) # 占满剩余空间
        
        # 初始化玩家页面显示状态
        self._update_player_page_visibility()
    
    def _load_flexmod_list(self):
        """加载FlexMod列表"""
        self.flexmod_list.clear()
        enabled_flexmod = self.config_manager.get_enabled_flexmod()
        
        for flexmod_name in enabled_flexmod:
            self.flexmod_list.addItem(flexmod_name)
    
    def _update_language(self):
        """更新语言"""
        # 刷新按钮现在是图标按钮，不显示文本
        # 更新玩家页面的语言
        if hasattr(self, 'player_page'):
            self.player_page.update_language()
    
    def _on_item_double_clicked(self, item):
        """双击项目"""
        flexmod_name = item.text()
        self.flexmod_opened.emit(flexmod_name)
    
    def _on_item_clicked(self, item):
        """点击项目"""
        flexmod_name = item.text()
        self.selected_flexmod = flexmod_name
        # 如果玩家模式已激活，更新玩家页面
        if self.player_mode_enabled:
            self.player_page.set_current_flexmod(flexmod_name)
    
    def _toggle_player_mode(self):
        """切换玩家模式"""
        self.player_mode_enabled = not self.player_mode_enabled
        # 保存玩家模式状态到配置文件
        self.config_manager.update_config('player_mode_enabled', self.player_mode_enabled)
        # 更新玩家页面显示状态
        self._update_player_page_visibility()
        # 如果启用了玩家模式且有选中的FlexMod，更新玩家页面
        if self.player_mode_enabled and self.selected_flexmod:
            self.player_page.set_current_flexmod(self.selected_flexmod)
    
    def _update_player_page_visibility(self):
        """更新玩家页面显示状态"""
        # 获取splitter的大小
        sizes = self.splitter.sizes()
        if self.player_mode_enabled:
            # 启用玩家模式，显示右侧玩家页面
            self.splitter.setSizes([sizes[0], 600])
            self.player_page.setVisible(True)
        else:
            # 禁用玩家模式，隐藏右侧玩家页面
            self.splitter.setSizes([sizes[0] + sizes[1], 0])
            self.player_page.setVisible(False)
    
    def _add_flexmod(self):
        """添加FlexMod"""
        mods_dir = self.config_manager.get_mods_dir()
        
        if not mods_dir or not os.path.exists(mods_dir):
            QMessageBox.warning(self, get_text('warning', self.lang), get_text('please_set_mods_dir', self.lang))
            return
        
        # 获取Mods目录下的所有文件夹
        try:
            folders = [f for f in os.listdir(mods_dir) 
                      if os.path.isdir(os.path.join(mods_dir, f))]
        except Exception as e:
            QMessageBox.critical(self, get_text('error', self.lang), f"{get_text('error', self.lang)}: {e}")
            return
        
        # 过滤掉已经添加的FlexMod
        enabled_flexmod = self.config_manager.get_enabled_flexmod()
        available_folders = [f for f in folders if f not in enabled_flexmod]
        
        if not available_folders:
            QMessageBox.information(self, get_text('info', self.lang), get_text('no_available_mods', self.lang))
            return
        
        # 创建选择窗口
        dialog = QDialog(self)
        dialog.setWindowTitle(get_text('add_flexmod_win_title', self.lang))
        dialog.setMinimumSize(400, 300)
        
        dialog_layout = QVBoxLayout()
        dialog.setLayout(dialog_layout)
        
        list_widget = QListWidget()
        list_widget.setStyleSheet("""
            QListWidget {
                background-color: #2a2a2a;
                color: #eee;
                border: 1px solid #444;
                border-radius: 4px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 10px;
                margin: 2px;
                border-radius: 3px;
                background-color: #3a3a3a;
            }
            QListWidget::item:hover {
                background-color: #4a4a4a;
            }
            QListWidget::item:selected {
                background-color: #b42828;
            }
        """)
        list_widget.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        
        for folder in available_folders:
            list_widget.addItem(folder)
        
        dialog_layout.addWidget(list_widget)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.setStyleSheet("""
            QDialogButtonBox QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 12px;
                min-width: 80px;
            }
            QDialogButtonBox QPushButton:hover {
                background-color: #45a049;
            }
        """)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        dialog_layout.addWidget(buttons)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_items = list_widget.selectedItems()
            if selected_items:
                selected_folder = selected_items[0].text()
                self._create_flexmod_structure(selected_folder)
    
    def _create_flexmod_structure(self, folder_name: str):
        """创建FlexMod结构"""
        mods_dir = self.config_manager.get_mods_dir()
        flexmod_dir = os.path.join(mods_dir, folder_name, 'FlexMod')
        flexmod_file = os.path.join(flexmod_dir, 'FlexMod.json')
        
        # 创建FlexMod文件夹
        if not os.path.exists(flexmod_dir):
            os.makedirs(flexmod_dir)
            logging.info(f'Created FlexMod folder: {flexmod_dir}')
        
        # 创建FlexMod.json文件
        if not os.path.exists(flexmod_file):
            default_data = {
                "groups": [
                    {
                        "groupName": "Default",
                        "groupDesc": ""
                    }
                ],
                "configs": []
            }
            with open(flexmod_file, 'w', encoding='utf-8') as f:
                json.dump(default_data, f, indent=4, ensure_ascii=False)
            logging.info(f'Created FlexMod.json file: {flexmod_file}')
        
        # 添加到启用列表
        self.config_manager.add_enabled_flexmod(folder_name)
        
        # 刷新列表
        self._load_flexmod_list()
        
        QMessageBox.information(self, get_text('success', self.lang), f"{get_text('added_flexmod', self.lang)}: {folder_name}")
    

