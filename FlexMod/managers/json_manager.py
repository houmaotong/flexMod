"""JSON管理器"""
import json
import os
from typing import Dict, Any, Optional
from .block_manager import BlockManager
from .group_manager import GroupManager


class JsonManager:
    """JSON管理器"""
    
    def __init__(self, file_path: str, block_manager: BlockManager, group_manager: GroupManager):
        self.file_path = file_path
        self.block_manager = block_manager
        self.group_manager = group_manager
    
    def load(self) -> bool:
        """加载JSON文件"""
        if not os.path.exists(self.file_path):
            return False
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'groups' in data:
                self.group_manager.load_from_json_groups(data['groups'])
            
            if 'configs' in data:
                self.block_manager.load_from_json_configs(data['configs'])
            
            return True
        except Exception as e:
            print(f"加载JSON文件失败: {e}")
            return False
    
    def save(self) -> bool:
        """保存JSON文件"""
        try:
            data = {
                'groups': self.group_manager.to_json_groups(),
                'configs': self.block_manager.to_json_configs()
            }
            
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"保存JSON文件失败: {e}")
            return False
    
    def get_json_content(self) -> str:
        """获取JSON内容"""
        data = {
            'groups': self.group_manager.to_json_groups(),
            'configs': self.block_manager.to_json_configs()
        }
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    def validate_and_fix(self) -> bool:
        """验证并修复JSON文件"""
        if not os.path.exists(self.file_path):
            return False
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'groups' not in data:
                data['groups'] = []
            
            if 'configs' not in data:
                data['configs'] = []
            
            has_default_group = any(g.get('groupName') == 'Default' for g in data['groups'])
            if not has_default_group:
                data['groups'].insert(0, {
                    'groupName': 'Default',
                    'groupDesc': ''
                })
            
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"验证JSON文件失败: {e}")
            return False
