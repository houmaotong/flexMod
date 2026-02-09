"""设置页面"""
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QMessageBox, QFileDialog, QApplication
)

from ..utils.lang import get_text, get_lang


class SettingPage(QWidget):
    """设置页面"""
    
    # 样式常量
    STYLES = {
        'label': """
            QLabel {
                font-size: 14px;
                color: #eee;
            }
        """,
        'info_label': """
            QLabel {
                color: #aaa;
                padding: 10px;
                background-color: #2a2a2a;
                border-radius: 4px;
            }
        """,
        'line_edit': """
            QLineEdit {
                background-color: #2a2a2a;
                color: #eee;
                border: 1px solid #444;
                border-radius: 4px;
                padding: 8px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 1px solid #b42828;
            }
        """,
        'button': """
            QPushButton {
                background-color: #2c2c2c;
                color: #eee;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #3c3c3c;
            }
            QPushButton:pressed {
                background-color: #1c1c1c;
            }
        """,
    }
    
    def __init__(self, config_manager, main_window=None):
        super().__init__()
        self.config_manager = config_manager 
        self.main_window = main_window
        self.lang = get_lang()
        self._initialize_ui()
        self._load_settings()
    
    def _initialize_ui(self):
        """初始化UI"""
        # 如果已经初始化过，只更新文本
        if hasattr(self, 'mods_dir_edit'):
            self._update_language()
            return
            
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        self.setLayout(main_layout)
        
        # 添加模组目录设置
        self._add_mods_dir_settings(main_layout)
        
        # 添加说明文本
        self._add_info_text(main_layout)
        
        # 添加弹簧
        main_layout.addStretch()
    
    def _add_mods_dir_settings(self, layout):
        """添加模组目录设置"""
        # 模组目录布局
        mods_dir_layout = QVBoxLayout()
        mods_dir_layout.setSpacing(10)
        
        # 标签
        self.mods_dir_label = QLabel(get_text('mods_dir_label', self.lang))
        self.mods_dir_label.setStyleSheet(self.STYLES['label'])
        mods_dir_layout.addWidget(self.mods_dir_label)
        
        # 输入框和按钮布局
        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)
        
        # 输入框
        self.mods_dir_edit = QLineEdit()
        self.mods_dir_edit.setStyleSheet(self.STYLES['line_edit'])
        self.mods_dir_edit.setPlaceholderText(get_text('mods_dir_sel_win_title', self.lang))
        input_layout.addWidget(self.mods_dir_edit)
        
        # 浏览按钮
        self.browse_btn = QPushButton(get_text('mods_dir_btn', self.lang))
        self.browse_btn.setStyleSheet(self.STYLES['button'])
        self.browse_btn.clicked.connect(self._browse_mods_directory)
        input_layout.addWidget(self.browse_btn)
        
        # 打开文件夹按钮
        self.open_folder_btn = QPushButton(get_text('mods_dir_open_btn', self.lang))
        self.open_folder_btn.setStyleSheet(self.STYLES['button'])
        self.open_folder_btn.clicked.connect(self._open_mods_directory)
        input_layout.addWidget(self.open_folder_btn)
        
        mods_dir_layout.addLayout(input_layout)
        
        layout.addLayout(mods_dir_layout)
    
    def _add_info_text(self, layout):
        """添加说明文本"""
        self.info_label = QLabel(get_text('mods_dir_description', self.lang))
        self.info_label.setStyleSheet(self.STYLES['info_label'])
        self.info_label.setWordWrap(True)
        layout.addWidget(self.info_label)
    
    def _load_settings(self):
        """加载设置"""
        try:
            mods_dir = self.config_manager.get_mods_dir()
            self.mods_dir_edit.setText(mods_dir)
        except Exception as e:
            print(f"加载设置失败: {e}")
            QMessageBox.warning(self, get_text('warning', self.lang), get_text('load_settings_failed', self.lang))
    
    def _update_language(self):
        """更新语言"""
        self.mods_dir_label.setText(get_text('mods_dir_label', self.lang))
        self.mods_dir_edit.setPlaceholderText(get_text('mods_dir_sel_win_title', self.lang))
        self.browse_btn.setText(get_text('mods_dir_btn', self.lang))
        self.open_folder_btn.setText(get_text('mods_dir_open_btn', self.lang))
        self.info_label.setText(get_text('mods_dir_description', self.lang))
    
    def _browse_mods_directory(self):
        """浏览模组目录"""
        while True:
            # 打开文件对话框
            folder_path = QFileDialog.getExistingDirectory(
                self,get_text('mods_dir_sel_win_title', self.lang))
            
            if folder_path:   # 验证路径  
                valid = self._validate_mods_dir(folder_path)
                if valid:  #验证通过，设置路径
                    self.mods_dir_edit.setText(folder_path)
                    # 自动保存设置
                    try:
                        self.config_manager.set_mods_dir(folder_path)
                        message = ("Settings saved successfully!\n设置保存成功！")
                        QMessageBox.information(self, get_text('success'), message)
                        
                    except Exception as e:
                        print(f"保存设置失败: {e}")
                        message = ("Failed to save settings.\n保存设置失败。")
                        QMessageBox.critical(self, get_text('error'), message)
                    
                    else:
                        # 无异常，说明保持成功，回到主页并刷新
                        if self.main_window:
                            self.main_window._show_home_page() # 切换到主页
                            if hasattr(self.main_window.home_page, '_load_flexmod_list'): 
                                self.main_window.home_page._load_flexmod_list() # 刷新主页

                    return
            
            #验证不通过，提示用户重试（重新选择） 或取消（退出软件）
            message = (
                "The selected directory must be ： '7 Days To Die/Mods' \n" 
                "选择的目录必须是：'7 Days To Die/Mods' \n\n"  
                "Click Retry to select again.\n"  
                "点击重试重新选择。\n\n"  
                "Click Cancel to exit the software.\n"  
                "点击取消退出软件。"  )
            reply = QMessageBox.warning( 
                self,
                "Warning/警告",
                message,
                QMessageBox.StandardButton.Retry | QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Cancel:   # 关闭应用程序
                from PyQt6.QtWidgets import QApplication
                QApplication.quit()
                return
    

    
    def _open_mods_directory(self):
        """在资源管理器中打开模组目录"""
        try:
            mods_dir = self.mods_dir_edit.text().strip()
            
            if not mods_dir:
                message = (
                    "Please set the mod directory first.\n"  # 英文提示
                    "请先设置模组目录。"  # 中文提示
                )
                QMessageBox.warning(self, get_text('warning'), message)
                return
            
            if not self._check_path_exists(mods_dir):
                message = (
                    f"The directory does not exist: {mods_dir} \n"  # 英文提示
                    f"目录不存在: {mods_dir}"  # 中文提示
                )
                QMessageBox.warning(self, get_text('warning'), message)
                return
            
            os.startfile(mods_dir)
        except Exception as e:
            print(f"打开目录失败: {e}")
            message = (
                "Failed to open the directory.\n"  # 英文提示
                "打开目录失败。"  # 中文提示
            )
            QMessageBox.critical(self, get_text('error'), message)
    
    def auto_open_browse_dialog(self):
        """自动打开文件选择器"""
        # 延迟调用，确保UI已经完全初始化
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(100, self._browse_mods_directory)
    
    def _validate_mods_dir(self, path):
        """验证模组目录路径
        
        Args:
            path: 要验证的路径
            
        Returns:
            bool: 验证是否通过
        """
        if not path:
            return False
        
        normalized_path = os.path.normpath(path)
        normalized_path_lower = normalized_path.lower()
        
        if not (normalized_path_lower.endswith(r"7 days to die\mods") or normalized_path_lower.endswith(r"7 days to die/mods")):
            return False
        
        return True
    
    def _check_path_exists(self, path):
        """检查路径是否存在
        
        Args:
            path: 要检查的路径
            
        Returns:
            bool: 路径是否存在
        """
        return os.path.exists(path)
