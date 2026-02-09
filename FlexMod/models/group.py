"""分组数据模型"""
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class Group:
    """分组数据模型"""
    name: str
    desc: str
    is_default: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'name': self.name,
            'desc': self.desc,
            'is_default': self.is_default
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Group':
        """从字典创建"""
        return cls(
            name=data['name'],
            desc=data.get('desc', ''),
            is_default=data.get('is_default', False)
        )
    
    def to_json_group(self) -> Dict[str, Any]:
        """转换为JSON分组格式"""
        return {
            'groupName': self.name,
            'groupDesc': self.desc
        }
    
    @classmethod
    def from_json_group(cls, data: Dict[str, Any]) -> 'Group':
        """从JSON分组格式创建"""
        return cls(
            name=data['groupName'],
            desc=data.get('groupDesc', ''),
            is_default=data.get('groupName') == 'Default'
        )
