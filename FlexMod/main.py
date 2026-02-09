"""FlexMod重构版本 - 主程序入口"""
import sys
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .managers import ConfigManager, resource_manager
from .ui import MainWindow
from .utils.lang import get_text


def get_config_file_path(): 
    """获取配置文件路径"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'config.json')


def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setWindowIcon(resource_manager.get_app_icon())
    
    try:
        config_file_path = get_config_file_path()
        config_manager = ConfigManager(config_file_path)
        window = MainWindow(config_manager)
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        QMessageBox.critical(None, get_text('error'), f"程序启动失败: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
