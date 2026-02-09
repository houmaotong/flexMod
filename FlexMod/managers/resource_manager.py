"""资源管理器"""
import os
from pathlib import Path
from PyQt6.QtGui import QIcon, QPixmap


class ResourceManager:
    """资源管理器 - 统一管理应用程序的所有资源"""
    
    _instance = None
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """初始化资源管理器"""
        if self._initialized:
            return
        
        self._initialized = True
        self._resources_dir = Path(__file__).parent.parent / "resources"
        self._icons_dir = self._resources_dir / "icons"
        self._images_dir = self._resources_dir / "images"
        
        self._cache = {}
    
    def _get_resource_path(self, resource_type: str, filename: str) -> Path:
        """获取资源文件路径"""
        resource_dir = self._resources_dir / resource_type
        if not resource_dir.exists():
            resource_dir.mkdir(parents=True, exist_ok=True)
        return resource_dir / filename
    
    def get_icon(self, filename: str) -> QIcon:
        """获取图标"""
        cache_key = f"icon_{filename}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        icon_path = self._get_resource_path("icons", filename)
        if icon_path.exists():
            icon = QIcon(str(icon_path))
            self._cache[cache_key] = icon
            return icon
        return QIcon()
    
    def get_pixmap(self, filename: str) -> QPixmap:
        """获取图片"""
        cache_key = f"pixmap_{filename}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        pixmap_path = self._get_resource_path("images", filename)
        if pixmap_path.exists():
            pixmap = QPixmap(str(pixmap_path))
            self._cache[cache_key] = pixmap
            return pixmap
        return QPixmap()
    
    def get_app_icon(self) -> QIcon:
        """获取应用程序图标"""
        return self.get_icon("logo_128.png")
    
    def clear_cache(self) -> None:
        """清空缓存"""
        self._cache.clear()


resource_manager = ResourceManager()
