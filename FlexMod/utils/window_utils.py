"""窗口工具类"""
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt


class WindowUtils:
    """窗口工具类 - 提供常用的窗口操作功能"""
    
    @staticmethod
    def center_window(window: QWidget):
        """将窗口居中显示"""
        # 获取屏幕几何信息
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        
        # 计算窗口在屏幕中央的位置
        x = (screen_geometry.width() - window.width()) // 2
        y = (screen_geometry.height() - window.height()) // 2
        
        # 确保窗口不会超出屏幕边界
        x = max(0, min(x, screen_geometry.width() - window.width()))
        y = max(0, min(y, screen_geometry.height() - window.height()))
        
        window.move(x, y)
    
    @staticmethod
    def center_on_parent(window: QWidget, parent: QWidget = None):
        """将窗口相对于父窗口居中"""
        if parent is None:
            # 如果没有指定父窗口，则相对于屏幕居中
            WindowUtils.center_window(window)
            return
        
        # 获取父窗口的几何信息
        parent_geometry = parent.geometry()
        parent_center_x = parent_geometry.x() + parent_geometry.width() // 2
        parent_center_y = parent_geometry.y() + parent_geometry.height() // 2
        
        # 计算新窗口的位置
        x = parent_center_x - window.width() // 2
        y = parent_center_y - window.height() // 2
        
        # 确保窗口不会超出屏幕边界
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        x = max(0, min(x, screen_geometry.width() - window.width()))
        y = max(0, min(y, screen_geometry.height() - window.height()))
        
        window.move(x, y)
    
    @staticmethod
    def maximize_window(window: QWidget):
        """最大化窗口"""
        window.setWindowState(window.windowState() | Qt.WindowState.WindowMaximized)
    
    @staticmethod
    def restore_window(window: QWidget):
        """还原窗口大小"""
        window.setWindowState(window.windowState() & ~Qt.WindowState.WindowMaximized)
    
    @staticmethod
    def set_window_size(window: QWidget, width: int, height: int):
        """设置窗口大小并保持居中"""
        window.resize(width, height)
        WindowUtils.center_window(window)