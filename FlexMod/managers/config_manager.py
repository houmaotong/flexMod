"""FlexMod配置管理器"""
import json
import os
from typing import Any, Dict, List, Optional


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config_data = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if not os.path.exists(self.config_file):
            default_config = {
                'mods_dir': '',
                'lang': 0,
                'Enabled_FlexMod': []
            }
            self._save_config(default_config)
            return default_config
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return {
                'mods_dir': '',
                'lang': 0,
                'Enabled_FlexMod': []
            }
    
    def _save_config(self, config_data: Dict[str, Any]) -> None:
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    def get_mods_dir(self) -> str:
        """获取模组目录"""
        return self.config_data.get('mods_dir', '')
    
    def set_mods_dir(self, mods_dir: str) -> None:
        """设置模组目录"""
        self.config_data['mods_dir'] = mods_dir
        self._save_config(self.config_data)
    
    def get_lang(self) -> int:
        """获取语言设置 (0=英文, 1=中文)"""
        return self.config_data.get('lang', 0)
    
    def set_lang(self, lang: int) -> None:
        """设置语言"""
        self.config_data['lang'] = lang
        self._save_config(self.config_data)
    
    def get_enabled_flexmod(self) -> List[str]:
        """获取启用的FlexMod列表
        
        严谨地检查每个FlexMod的有效性：
        1. 检查Mods目录下的每个文件夹
        2. 验证是否存在FlexMod/FlexMod.json文件
        3. 自动添加有效的FlexMod，移除无效的FlexMod
        """
        mods_dir = self.get_mods_dir()
        valid_flexmods = []
        
        # 检查Mods目录是否存在
        if mods_dir and os.path.exists(mods_dir):
            try:
                # 获取Mods目录下的所有文件夹
                folders = [f for f in os.listdir(mods_dir) 
                          if os.path.isdir(os.path.join(mods_dir, f))]
                
                # 检查每个文件夹是否有FlexMod\FlexMod.json文件
                for folder in folders:
                    flexmod_json_path = os.path.join(mods_dir, folder, 'FlexMod', 'FlexMod.json')
                    if os.path.exists(flexmod_json_path):
                        valid_flexmods.append(folder)
            except Exception as e:
                print(f"检查Mods目录失败: {e}")
        
        # 更新配置文件中的Enabled_FlexMod数组
        if self.config_data.get('Enabled_FlexMod') != valid_flexmods:
            self.config_data['Enabled_FlexMod'] = valid_flexmods
            self._save_config(self.config_data)
        
        return valid_flexmods
    
    def add_enabled_flexmod(self, flexmod_name: str) -> None:
        """添加启用的FlexMod"""
        enabled_list = self.get_enabled_flexmod()
        if flexmod_name not in enabled_list:
            enabled_list.append(flexmod_name)
            self.config_data['Enabled_FlexMod'] = enabled_list
            self._save_config(self.config_data)
    
    def remove_enabled_flexmod(self, flexmod_name: str) -> None:
        """移除启用的FlexMod"""
        enabled_list = self.get_enabled_flexmod()
        if flexmod_name in enabled_list:
            enabled_list.remove(flexmod_name)
            self.config_data['Enabled_FlexMod'] = enabled_list
            self._save_config(self.config_data)
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """获取配置项"""
        return self.config_data.get(key, default)
    
    def update_config(self, key: str, value: Any) -> None:
        """更新配置项"""
        self.config_data[key] = value
        self._save_config(self.config_data)
