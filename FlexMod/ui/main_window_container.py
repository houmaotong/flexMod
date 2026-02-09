"""主窗口"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QColor

from ..utils.lang import get_text, get_lang, set_lang

from .flex_mod_color import *



class MainWindow(QWidget):
    """主窗口"""
    
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.lang = get_lang()
        
        # 存储已打开的编辑器窗口
        self.open_editors = {}
        
        self._init_ui()
        self._init_pages()
        
        self.setWindowTitle(get_text('main_window_title', self.lang))
        self.resize(1200, 800)
        
        # 使用窗口工具类居中显示
        from ..utils.window_utils import WindowUtils
        WindowUtils.center_window(self)
    
    def _init_ui(self):
        """初始化UI"""
        self.setStyleSheet(SS_window)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)
        
        # 导航栏容器的父容器，用于容纳阴影
        nav_shadow_container = QWidget()
        nav_shadow_layout = QVBoxLayout(nav_shadow_container)
        nav_shadow_layout.setSpacing(0)
        nav_shadow_layout.setContentsMargins(0, 0, 0, 10)
        nav_container = QWidget() # 导航栏容器
        nav_container.setFixedHeight(50)
        nav_container.setStyleSheet(SS_nav_grad_fill)
        shadow = QGraphicsDropShadowEffect()    # 为导航栏容器添加柔化阴影
        shadow.setBlurRadius(20)  # 模糊半径
        shadow.setColor(QColor(0, 0, 0, 150))  # 阴影颜色，带透明度
        shadow.setOffset(0, 0)  # 阴影偏移
        nav_container.setGraphicsEffect(shadow) 
        nav_shadow_layout.addWidget(nav_container)# 将导航栏容器添加到父容器中
        
        # 导航栏布局
        nav_layout = QHBoxLayout(nav_container)
        nav_layout.setSpacing(10)
        nav_layout.setContentsMargins(10, 10, 10, 10)
        
        # 主页按钮
        self.home_btn = QPushButton(get_text('home', self.lang))
        self.home_btn.setStyleSheet(SS_nav_btn_normal)
        self.home_btn.clicked.connect(self._show_home_page)
        self.home_btn.setFlat(True)
        nav_layout.addWidget(self.home_btn)
        
        # 设置按钮
        self.setting_btn = QPushButton(get_text('setting', self.lang))
        self.setting_btn.setStyleSheet(SS_nav_btn_normal)
        self.setting_btn.clicked.connect(self._show_setting_page)
        self.setting_btn.setFlat(True)
        nav_layout.addWidget(self.setting_btn)
        
        # 语言按钮
        self.lang_btn = QPushButton(get_text('lang', self.lang))
        self.lang_btn.setStyleSheet(SS_nav_btn_normal)
        self.lang_btn.clicked.connect(self._toggle_language)
        self.lang_btn.setFlat(True)
        nav_layout.addWidget(self.lang_btn)
        
        # 添加弹簧
        nav_layout.addStretch()
        
        main_layout.addWidget(nav_shadow_container)
        
        # 页面容器
        self.page_stack = QStackedWidget()
        self.page_stack.setStyleSheet(SS_page_stack)
        main_layout.addWidget(self.page_stack)
    
    def _init_pages(self):
        """初始化页面"""
        from .home_page import HomePage
        from .setting_page import SettingPage
        from ..utils.lang import get_text
        from PyQt6.QtWidgets import QMessageBox
        
        # 创建主页
        self.home_page = HomePage(self.config_manager)
        self.page_stack.addWidget(self.home_page)
        
        # 创建设置页面
        self.setting_page = SettingPage(self.config_manager, self)
        self.page_stack.addWidget(self.setting_page)
        
        # 连接主页信号
        self.home_page.flexmod_opened.connect(self._open_flexmod_editor)
        
        # 检查模组目录路径是否为空
        mods_dir = self.config_manager.get_mods_dir()
        if not mods_dir:
            # 显示温馨提示消息
            QMBOX_info=QMessageBox.information(
                self,
                " Tips/温馨提示",
                ("Welcome to FlexMod!\n欢迎使用FlexMod！\n\n" 
                "Please set the correct mod directory path first to use the software functions properly.\n"
                "请先设置正确的模组目录路径，以便正常使用软件功能。")
            )
            # QMBOX_info.setStyleSheet(SS_QMessageBox_information)

            self._show_setting_page()# 自动切换到设置页面  
            self.setting_page.auto_open_browse_dialog()# 自动打开文件选择器
        else:
            self._show_home_page() # 默认显示主页
    
    def _show_home_page(self):
        """显示主页"""
        self.page_stack.setCurrentWidget(self.home_page)
        self._update_button_style(self.home_btn)
    
    def _show_setting_page(self):
        """显示设置页面"""
        self.page_stack.setCurrentWidget(self.setting_page)
        self._update_button_style(self.setting_btn)
    
    def _toggle_language(self):
        """切换语言"""
        self.lang = 1 - self.lang
        set_lang(self.lang)
        self._update_ui_language()
    
    def _update_ui_language(self):
        """更新UI语言"""
        self.setWindowTitle(get_text('main_window_title', self.lang))
        self.home_btn.setText(get_text('home', self.lang))
        self.setting_btn.setText(get_text('setting', self.lang))
        self.lang_btn.setText(get_text('lang', self.lang))
        
        # 更新主页语言
        self.home_page.lang = self.lang
        self.home_page._update_language()
        
        # 更新设置页面语言
        self.setting_page.lang = self.lang
        self.setting_page._update_language()
        
    
    def _update_button_style(self, active_btn):
        """更新按钮样式"""
        # 为所有按钮重置为默认的透明样式
        buttons = [self.home_btn, self.setting_btn, self.lang_btn]
        for btn in buttons:
            btn.setStyleSheet(SS_nav_btn_normal)
            btn.setFlat(True)
        
        # 为激活的按钮设置激活样式
        if active_btn:
            active_btn.setStyleSheet(SS_nav_btn_active)
            active_btn.setFlat(False)
    
    def _open_flexmod_editor(self, flexmod_name: str):
        """打开FlexMod编辑器"""
        from .editor_window import FlexModEditorWindow
        
        # 检查是否已经打开了该FlexMod的编辑器
        if flexmod_name in self.open_editors:
            # 如果已经打开，激活并显示窗口
            editor = self.open_editors[flexmod_name]
            editor.show()
            editor.raise_()
            editor.activateWindow()
        else:
            # 如果没有打开，创建新的编辑器窗口
            mods_dir = self.config_manager.get_mods_dir()
            json_file_path = f"{mods_dir}/{flexmod_name}/FlexMod/FlexMod.json"
            
            editor = FlexModEditorWindow(flexmod_name, json_file_path)
            # 设置窗口关闭时自动销毁，这样当用户关闭窗口时，destroyed 信号会被发出
            editor.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
            editor.show()
            
            # 存储打开的编辑器窗口
            self.open_editors[flexmod_name] = editor
            
            # 连接窗口销毁信号，以便从存储中移除
            editor.destroyed.connect(lambda obj=None, name=flexmod_name: self._on_editor_closed(name))
    
    def _on_editor_closed(self, flexmod_name: str):
        """当编辑器窗口关闭时调用"""
        if flexmod_name in self.open_editors:
            del self.open_editors[flexmod_name]
    
