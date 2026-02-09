"""分组管理器"""
from typing import List, Optional
import random
import string
from ..models.group import Group


class GroupManager:
    """分组管理器"""
    
    def __init__(self):
        self.groups: List[Group] = []
        self._ensure_default_group()
    
    def _ensure_default_group(self) -> None:
        """确保默认分组存在"""
        if not any(g.name == 'Default' for g in self.groups):
            self.groups.insert(0, Group(name='Default', desc='', is_default=True))
    
    def add_group(self, group: Group) -> bool:
        """添加分组"""
        if any(g.name == group.name for g in self.groups):
            return False
        self.groups.append(group)
        return True
    
    def remove_group(self, group_name: str) -> bool:
        """移除分组"""
        for i, group in enumerate(self.groups):
            if group.name == group_name and not group.is_default:
                self.groups.pop(i)
                return True
        return False
    
    def get_group(self, group_name: str) -> Optional[Group]:
        """获取分组"""
        for group in self.groups:
            if group.name == group_name:
                return group
        return None
    
    def get_all_groups(self) -> List[Group]:
        """获取所有分组"""
        return self.groups.copy()
    
    def update_group(self, group_name: str, new_name: str, new_desc: str) -> bool:
        """更新分组"""
        group = self.get_group(group_name)
        if group:
            if group.is_default:
                return False
            if new_name != group_name and any(g.name == new_name for g in self.groups):
                return False
            group.name = new_name
            group.desc = new_desc
            return True
        return False
    
    def clear(self) -> None:
        """清空所有分组（保留默认分组）"""
        self.groups = [Group(name='Default', desc='', is_default=True)]
    
    def generate_group_name(self) -> str:
        """生成唯一的分组名称"""
        while True:
            random_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            group_name = f"NewGroup_{random_code}"
            if not any(g.name == group_name for g in self.groups):
                return group_name
    
    def to_json_groups(self) -> List[Dict]:
        """转换为JSON分组列表"""
        return [group.to_json_group() for group in self.groups]
    
    def load_from_json_groups(self, groups: List[Dict]) -> None:
        """从JSON分组列表加载"""
        self.groups = []
        has_default_group = False
        for group_data in groups:
            group = Group.from_json_group(group_data)
            if group.is_default:
                has_default_group = True
            self.groups.append(group)
        
        if not has_default_group:
            self.groups.insert(0, Group(name='Default', desc='', is_default=True))
    
    def deduplicate(self) -> None:
        """去重分组（保留第一个出现的）"""
        unique_groups = []
        seen_names = set()
        for group in self.groups:
            if group.name not in seen_names:
                seen_names.add(group.name)
                unique_groups.append(group)
        self.groups = unique_groups
