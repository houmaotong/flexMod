"""信息通知模块"""
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QColor, QCursor
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QTimer
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.lang import get_text


class NotificationWidget(QMainWindow):
    """信息通知组件"""
    
    # 通知类型
    TYPE_DEFAULT = "default"  # 普通信息
    TYPE_WARNING = "warning"  # 注意
    TYPE_SUCCESS = "success"  # 成功
    TYPE_ERROR = "error"  # 错误
    
    # 颜色定义
    COLORS = {
        TYPE_DEFAULT: "#409eff",    # 蓝色
        TYPE_WARNING: "#e6a23c",    # 黄色
        TYPE_SUCCESS: "#67c23a",    # 绿色
        TYPE_ERROR: "#f56c6c"       # 红色
    }
    
    # 样式表定义
    STYLES = {
        "central_widget": """
            QWidget {
                background-color: #2d2d42;
                border-radius: 16px;
            }
        """,
        "header": """
            QWidget {
                background-color: #252538;
            }
        """,
        "body": """
            QWidget {
                background-color: #2d2d42;
                border: none;
            }
        """,
        "close_button": """
            QPushButton {
                color: #a0a0b0;
                font-size: 16px;
                font-weight: bold;
                background: none;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                color: #e0e0e0;
                background-color: rgba(255, 255, 255, 0.1);
            }
        """,
        "desc_label": """
            QLabel {
                color: #a0a0b0;
                font-size: 13px;
                font-family: 'Microsoft YaHei', sans-serif;
                line-height: 1.4;
            }
        """
    }
    
    @classmethod
    def get_title_label_style(cls, color):
        """获取标题标签样式"""
        return f"""
            QLabel {{
                color: {color};
                font-size: 16px;
                font-weight: 600;
                font-family: 'Microsoft YaHei', sans-serif;
            }}
        """
    
    @classmethod
    def get_dot_style(cls, color):
        """获取圆点样式"""
        return f"background-color: {color}; border-radius: 5px;"
    
    def __init__(self, notification_type: str = TYPE_DEFAULT, message: str = "", lang: int = 0, timeout: int = 5000, parent=None):
        """初始化通知组件
        
        Args:
            notification_type: 通知类型：
                可选值：TYPE_DEFAULT（普通信息）、TYPE_WARNING（警告）、TYPE_SUCCESS（成功）、TYPE_ERROR（错误）
            message: 通知内容，支持多行文本
            lang: 语言设置，0=英文, 1=中文
            timeout: 自动关闭超时时间（毫秒），0 表示不自动关闭，默认值为5000毫秒（5秒）
            parent: 父组件，默认为None
        """
        super().__init__(parent)
        
        # 参数验证
        valid_types = [self.TYPE_DEFAULT, self.TYPE_WARNING, self.TYPE_SUCCESS, self.TYPE_ERROR]
        if notification_type not in valid_types:
            notification_type = self.TYPE_DEFAULT
        
        if not isinstance(lang, int) or lang not in [0, 1]:
            lang = 0
        
        if not isinstance(message, str):
            message = str(message)
        
        if not isinstance(timeout, int) or timeout < 0:
            timeout = 5000
        
        self.notification_type = notification_type
        self.lang = lang
        self.title = self._get_title_by_type(notification_type, lang)
        self.message = message
        self.timeout = timeout
        
        # 组件引用
        self._dot = None
        self._title_label = None
        self._desc_label = None
        self._timer = None
        
        # 完全移除标题栏
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Window
        )
        
        # 设置窗口背景透明
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        # 初始化UI
        self._init_ui()
        
        # 计算并设置窗口大小
        self._adjust_window_size()
    
    def closeEvent(self, event):
        """关闭事件"""
        # 停止定时器
        if self._timer:
            self._timer.stop()
            self._timer.deleteLater()
            self._timer = None
        
        # 停止动画
        if hasattr(self, 'animation') and self.animation:
            self.animation.stop()
        
        event.accept()
    
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_start_position)
            event.accept()
    
    def _get_title_by_type(self, notification_type: str, lang: int) -> str:
        """根据通知类型获取对应语言的标题
        
        Args:
            notification_type: 通知类型
            lang: 语言 (0=英文, 1=中文)
            
        Returns:
            对应语言的通知标题
        """
        type_to_key = {
            self.TYPE_DEFAULT: 'notification_info',
            self.TYPE_WARNING: 'notification_warning',
            self.TYPE_SUCCESS: 'notification_success',
            self.TYPE_ERROR: 'notification_error'
        }
        key = type_to_key.get(notification_type, 'notification_info')
        return get_text(key, lang)
    
    def _init_ui(self):
        """初始化UI"""
        # 创建中心部件
        central_widget = QWidget()
        central_widget.setStyleSheet(self.STYLES["central_widget"])
        
        # 设置主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建头部
        header = self._create_header()
        main_layout.addWidget(header)
        
        # 创建内容
        body = self._create_body()
        main_layout.addWidget(body)
        
        # 设置中心部件
        self.setCentralWidget(central_widget)
    
    def _create_header(self) -> QWidget:
        """创建头部"""
        header = QWidget()
        header.setFixedHeight(40)
        header.setStyleSheet(self.STYLES["header"])
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(18, 0, 18, 0)
        layout.setSpacing(10)
        
        # 添加彩色圆点
        self._dot = QWidget()
        self._dot.setFixedSize(10, 10)
        color = self.COLORS.get(self.notification_type, self.COLORS[self.TYPE_DEFAULT])
        self._dot.setStyleSheet(self.get_dot_style(color))
        layout.addWidget(self._dot, alignment=Qt.AlignmentFlag.AlignVCenter)
        
        # 添加标题
        self._title_label = QLabel(self.title)
        self._title_label.setStyleSheet(self.get_title_label_style(color))
        layout.addWidget(self._title_label, alignment=Qt.AlignmentFlag.AlignVCenter)
        
        layout.addStretch()
        
        # 添加关闭按钮
        close_btn = QPushButton("×")
        close_btn.setFixedSize(20, 20)
        close_btn.setStyleSheet(self.STYLES["close_button"])
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignVCenter)
        
        return header
    
    def _create_body(self) -> QWidget:
        """创建内容"""
        body = QWidget()
        body.setStyleSheet(self.STYLES["body"])
        
        layout = QVBoxLayout(body)
        layout.setContentsMargins(18, 18, 18, 18)
        
        # 添加描述文本
        self._desc_label = QLabel(self.message)
        self._desc_label.setStyleSheet(self.STYLES["desc_label"])
        self._desc_label.setWordWrap(True)
        layout.addWidget(self._desc_label)
        
        return body
    
    def _adjust_window_size(self):
        """根据内容调整窗口大小"""
        # 设置最大宽度
        max_width = 450
        
        # 计算标题所需宽度
        title_width = self._title_label.fontMetrics().boundingRect(self.title).width() + 40  # 加上边距和圆点宽度
        
        # 计算消息所需宽度
        message_width = self._desc_label.fontMetrics().boundingRect(self.message).width() + 36  # 加上左右边距
        
        # 确定最终宽度
        width = min(max(title_width, message_width, 300), max_width)  # 最小宽度300
        
        # 设置标签最大宽度以触发换行
        self._title_label.setMaximumWidth(width - 40)  # 减去边距和圆点宽度
        self._desc_label.setMaximumWidth(width - 36)  # 减去左右边距
        
        # 重新计算高度
        title_height = self._title_label.sizeHint().height()
        message_height = self._desc_label.sizeHint().height()
        
        # 计算总高度
        header_height = 40  # 固定头部高度
        body_height = message_height + 36  # 消息高度加上上下边距
        total_height = header_height + body_height
        
        # 确保最小高度
        total_height = max(total_height, 120)
        
        # 设置窗口大小
        self.setFixedSize(width, total_height)
    
    def set_message(self, message: str):
        """设置通知内容"""
        # 参数验证
        if not isinstance(message, str):
            message = str(message)
        
        self.message = message
        # 更新UI
        if self._desc_label:
            self._desc_label.setText(message)
            # 重新调整窗口大小
            self._adjust_window_size()
    
    def set_type(self, notification_type: str):
        """设置通知类型"""
        # 参数验证
        valid_types = [self.TYPE_DEFAULT, self.TYPE_WARNING, self.TYPE_SUCCESS, self.TYPE_ERROR]
        if notification_type not in valid_types:
            notification_type = self.TYPE_DEFAULT
        
        self.notification_type = notification_type
        # 更新标题
        self.title = self._get_title_by_type(notification_type, self.lang)
        # 更新UI
        color = self.COLORS.get(notification_type, self.COLORS[self.TYPE_DEFAULT])
        
        # 更新圆点颜色
        if self._dot:
            self._dot.setStyleSheet(self.get_dot_style(color))
        
        # 更新标题
        if self._title_label:
            self._title_label.setText(self.title)
            self._title_label.setStyleSheet(self.get_title_label_style(color))
            # 重新调整窗口大小
            self._adjust_window_size()
    
    def show(self):
        """显示通知"""
        # 获取鼠标当前位置
        mouse_pos = QCursor.pos()
        mouse_x = mouse_pos.x()
        mouse_y = mouse_pos.y()
        
        # 计算窗口最终位置（鼠标所在位置）
        window_width = self.width()
        window_height = self.height()
        final_x = mouse_x - window_width // 2
        final_y = mouse_y - window_height // 2
        
        # 计算初始位置（鼠标位置偏下）
        initial_x = final_x
        initial_y = mouse_y + 100  # 鼠标位置偏下100像素，增加距离使动画更明显
        initial_width = window_width // 2
        initial_height = window_height // 2
        
        # 确保窗口在屏幕内
        screen = self.screen().geometry()
        initial_x = max(0, min(initial_x, screen.width() - initial_width))
        initial_y = max(0, min(initial_y, screen.height() - initial_height))
        final_x = max(0, min(final_x, screen.width() - window_width))
        final_y = max(0, min(final_y, screen.height() - window_height))
        
        # 设置初始几何属性
        self.setGeometry(initial_x, initial_y, initial_width, initial_height)
        
        # 显示窗口
        super().show()
        self.raise_()
        self.activateWindow()
        
        # 创建动画并存储为实例变量，防止被垃圾回收
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)  # 增加动画持续时间，使动画更明显
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)  # 添加缓动效果
        self.animation.setStartValue(self.geometry())
        self.animation.setEndValue(QRect(final_x, final_y, window_width, window_height))
        self.animation.start()
        
        # 设置自动关闭定时器
        if self.timeout > 0:
            # 先停止之前可能存在的定时器
            if self._timer:
                self._timer.stop()
                self._timer.deleteLater()
            
            # 创建新的定时器
            self._timer = QTimer(self)
            self._timer.setSingleShot(True)
            self._timer.timeout.connect(self.close)
            self._timer.start(self.timeout)


class NotificationGroupWidget(QWidget):
    """通知组组件，用于管理多个通知实例"""
    
    def __init__(self, title: str = "", parent=None):
        """初始化通知组
        
        Args:
            title: 组标题，为空时不显示标题
            parent: 父组件
        """
        super().__init__(parent)
        self.title = title
        self._notifications = []  # 存储通知实例的列表
        self._init_ui()
    
    def _init_ui(self):
        """初始化UI布局"""
        # 创建垂直布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # 移除默认边距
        layout.setSpacing(16)  # 设置通知之间的间距
        
        # 添加标题标签（如果有标题）
        if self.title:
            title_label = QLabel(self.title)
            title_label.setStyleSheet("""
                QLabel {
                    color: #e0e0e0;
                    font-size: 18px;
                    font-weight: 600;
                    font-family: 'Microsoft YaHei', sans-serif;
                    margin-bottom: 8px;
                    padding-left: 2px;
                }
            """)
            layout.addWidget(title_label)
    
    def add_notification(self, notification: NotificationWidget):
        """添加通知到组中
        
        Args:
            notification: 要添加的通知实例
        """
        # 将通知添加到列表中
        self._notifications.append(notification)
        # 将通知添加到布局中
        self.layout().addWidget(notification)
    
    def get_notifications(self) -> list:
        """获取组中所有通知
        
        Returns:
            通知实例列表
        """
        return self._notifications


if __name__ == "__main__":
    """测试代码"""
    import sys
    from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
    from PyQt6.QtCore import Qt
    
    class NotificationTestWindow(QMainWindow):
        """通知测试窗口"""
        
        def __init__(self):
            super().__init__()
            self.setWindowTitle("信息通知模块测试")
            self.setGeometry(100, 100, 600, 400)
            self.setStyleSheet("background-color: #1e1e2f;")
            
            # 存储通知窗口引用
            self.notifications = []
            
            # 创建中心部件
            central_widget = QWidget()
            central_layout = QVBoxLayout(central_widget)
            central_layout.setContentsMargins(50, 50, 50, 50)
            central_layout.setSpacing(20)
            
            # 添加标题
            title_label = QPushButton("通知测试")
            title_label.setStyleSheet("""
                QPushButton {
                    color: #e0e0e0;
                    font-size: 24px;
                    font-weight: 600;
                    font-family: 'Microsoft YaHei', sans-serif;
                    background: none;
                    border: none;
                    text-align: left;
                    padding: 0;
                    margin-bottom: 20px;
                }
            """)
            central_layout.addWidget(title_label)
            
            # 添加中文测试按钮
            chinese_label = QPushButton("中文测试")
            chinese_label.setStyleSheet("""
                QPushButton {
                    color: #a0a0b0;
                    font-size: 16px;
                    font-weight: 500;
                    font-family: 'Microsoft YaHei', sans-serif;
                    background: none;
                    border: none;
                    text-align: left;
                    padding: 0;
                    margin-bottom: 10px;
                }
            """)
            central_layout.addWidget(chinese_label)
            
            # 中文通知按钮
            chinese_buttons_layout = QVBoxLayout()
            chinese_buttons_layout.setSpacing(10)
            
            info_btn_zh = QPushButton("📢 信息通知")
            info_btn_zh.setStyleSheet("""
                QPushButton {
                    padding: 10px 16px;
                    background-color: #2d2d42;
                    color: #e0e0e0;
                    font-size: 14px;
                    font-family: 'Microsoft YaHei', sans-serif;
                    border: 1px solid #3a3a5a;
                    border-radius: 6px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #3a3a5a;
                }
            """)
            info_btn_zh.clicked.connect(lambda: self._show_notification_dialog(NotificationWidget.TYPE_DEFAULT, "这是一条普通的提示信息，用于告知用户常规内容，不涉及成功或错误状态。", 1))
            chinese_buttons_layout.addWidget(info_btn_zh)
            
            warning_btn_zh = QPushButton("⚠️ 注意通知")
            warning_btn_zh.setStyleSheet("""
                QPushButton {
                    padding: 10px 16px;
                    background-color: #2d2d42;
                    color: #e0e0e0;
                    font-size: 14px;
                    font-family: 'Microsoft YaHei', sans-serif;
                    border: 1px solid #3a3a5a;
                    border-radius: 6px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #3a3a5a;
                }
            """)
            warning_btn_zh.clicked.connect(lambda: self._show_notification_dialog(NotificationWidget.TYPE_WARNING, "这是一条注意提醒信息，用于提示用户需要留意的事项，避免后续出现问题。", 1))
            chinese_buttons_layout.addWidget(warning_btn_zh)
            
            success_btn_zh = QPushButton("✅ 成功通知")
            success_btn_zh.setStyleSheet("""
                QPushButton {
                    padding: 10px 16px;
                    background-color: #2d2d42;
                    color: #e0e0e0;
                    font-size: 14px;
                    font-family: 'Microsoft YaHei', sans-serif;
                    border: 1px solid #3a3a5a;
                    border-radius: 6px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #3a3a5a;
                }
            """)
            success_btn_zh.clicked.connect(lambda: self._show_notification_dialog(NotificationWidget.TYPE_SUCCESS, "恭喜你，操作已成功完成！相关数据已保存，你可以进行下一步操作。", 1))
            chinese_buttons_layout.addWidget(success_btn_zh)
            
            error_btn_zh = QPushButton("❌ 错误通知")
            error_btn_zh.setStyleSheet("""
                QPushButton {
                    padding: 10px 16px;
                    background-color: #2d2d42;
                    color: #e0e0e0;
                    font-size: 14px;
                    font-family: 'Microsoft YaHei', sans-serif;
                    border: 1px solid #3a3a5a;
                    border-radius: 6px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #3a3a5a;
                }
            """)
            error_btn_zh.clicked.connect(lambda: self._show_notification_dialog(NotificationWidget.TYPE_ERROR, "抱歉，操作失败了！请检查输入内容是否正确，或稍后重新尝试该操作。", 1))
            chinese_buttons_layout.addWidget(error_btn_zh)
            
            central_layout.addLayout(chinese_buttons_layout)
            
            # 添加英文测试按钮
            english_label = QPushButton("英文测试")
            english_label.setStyleSheet("""
                QPushButton {
                    color: #a0a0b0;
                    font-size: 16px;
                    font-weight: 500;
                    font-family: 'Microsoft YaHei', sans-serif;
                    background: none;
                    border: none;
                    text-align: left;
                    padding: 0;
                    margin-top: 20px;
                    margin-bottom: 10px;
                }
            """)
            central_layout.addWidget(english_label)
            
            # 英文通知按钮
            english_buttons_layout = QVBoxLayout()
            english_buttons_layout.setSpacing(10)
            
            info_btn_en = QPushButton("📢 Info Notification")
            info_btn_en.setStyleSheet("""
                QPushButton {
                    padding: 10px 16px;
                    background-color: #2d2d42;
                    color: #e0e0e0;
                    font-size: 14px;
                    font-family: 'Microsoft YaHei', sans-serif;
                    border: 1px solid #3a3a5a;
                    border-radius: 6px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #3a3a5a;
                }
            """)
            info_btn_en.clicked.connect(lambda: self._show_notification_dialog(NotificationWidget.TYPE_DEFAULT, "This is a normal prompt message for informing users of general content, without success or error status.", 0))
            english_buttons_layout.addWidget(info_btn_en)
            
            warning_btn_en = QPushButton("⚠️ Warning Notification")
            warning_btn_en.setStyleSheet("""
                QPushButton {
                    padding: 10px 16px;
                    background-color: #2d2d42;
                    color: #e0e0e0;
                    font-size: 14px;
                    font-family: 'Microsoft YaHei', sans-serif;
                    border: 1px solid #3a3a5a;
                    border-radius: 6px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #3a3a5a;
                }
            """)
            warning_btn_en.clicked.connect(lambda: self._show_notification_dialog(NotificationWidget.TYPE_WARNING, "This is a warning message to remind users of matters needing attention to avoid subsequent problems.", 0))
            english_buttons_layout.addWidget(warning_btn_en)
            
            success_btn_en = QPushButton("✅ Success Notification")
            success_btn_en.setStyleSheet("""
                QPushButton {
                    padding: 10px 16px;
                    background-color: #2d2d42;
                    color: #e0e0e0;
                    font-size: 14px;
                    font-family: 'Microsoft YaHei', sans-serif;
                    border: 1px solid #3a3a5a;
                    border-radius: 6px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #3a3a5a;
                }
            """)
            success_btn_en.clicked.connect(lambda: self._show_notification_dialog(NotificationWidget.TYPE_SUCCESS, "Congratulations, the operation has been completed successfully! Relevant data has been saved, and you can proceed to the next step.", 0))
            english_buttons_layout.addWidget(success_btn_en)
            
            error_btn_en = QPushButton("❌ Error Notification")
            error_btn_en.setStyleSheet("""
                QPushButton {
                    padding: 10px 16px;
                    background-color: #2d2d42;
                    color: #e0e0e0;
                    font-size: 14px;
                    font-family: 'Microsoft YaHei', sans-serif;
                    border: 1px solid #3a3a5a;
                    border-radius: 6px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #3a3a5a;
                }
            """)
            error_btn_en.clicked.connect(lambda: self._show_notification_dialog(NotificationWidget.TYPE_ERROR, "Sorry, the operation failed! Please check if the input content is correct, or try the operation again later.", 0))
            english_buttons_layout.addWidget(error_btn_en)
            
            central_layout.addLayout(english_buttons_layout)
            
            central_layout.addStretch()
            
            self.setCentralWidget(central_widget)
        
        def _show_notification_dialog(self, notification_type: str, message: str, lang: int):
            """显示通知对话框"""
            # 直接创建通知窗口
            notification = NotificationWidget(notification_type, message, lang)
            
            # 设置位置
            notification.move(200, 200)
            
            # 存储通知引用，防止被垃圾回收
            self.notifications.append(notification)
            
            # 连接关闭信号，移除引用
            def on_notification_closed():
                if notification in self.notifications:
                    self.notifications.remove(notification)
            
            notification.destroyed.connect(on_notification_closed)
            
            # 显示通知
            notification.show()
            notification.raise_()
            notification.activateWindow()
    
    app = QApplication(sys.argv)
    window = NotificationTestWindow()
    window.show()
    sys.exit(app.exec())
