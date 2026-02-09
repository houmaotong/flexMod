"""功能块管理器"""
from typing import Dict, List, Optional
import random
import string
from ..models.block import Block, BlockType


class BlockManager:
    """功能块管理器"""
    
    def __init__(self):
        self.blocks: Dict[str, Block] = {}
    
    def add_block(self, block: Block) -> None:
        """添加功能块"""
        self.blocks[block.block_id] = block
    
    def remove_block(self, block_id: str) -> bool:
        """移除功能块"""
        if block_id in self.blocks:
            del self.blocks[block_id]
            return True
        return False
    
    def get_block(self, block_id: str) -> Optional[Block]:
        """获取功能块"""
        return self.blocks.get(block_id)
    
    def get_all_blocks(self) -> List[Block]:
        """获取所有功能块"""
        return list(self.blocks.values())
    
    def get_blocks_by_type(self, block_type: BlockType) -> List[Block]:
        """根据类型获取功能块"""
        return [block for block in self.blocks.values() if block.block_type == block_type]
    
    def update_block(self, block_id: str, parameters: Dict) -> bool:
        """更新功能块参数"""
        block = self.get_block(block_id)
        if block:
            block.parameters.update(parameters)
            return True
        return False
    
    def update_group_name(self, old_name: str, new_name: str) -> None:
        """更新所有功能块的分组名称"""
        for block in self.blocks.values():
            if block.get_parameter('group_name') == old_name:
                block.parameters['group_name'] = new_name
    
    def clear(self) -> None:
        """清空所有功能块"""
        self.blocks.clear()
    
    def generate_block_id(self) -> str:
        """生成唯一的功能块ID"""
        return f"block_{''.join(random.choices(string.ascii_letters + string.digits, k=8))}"
    
    def to_json_configs(self) -> List[Dict]:
        """转换为JSON配置列表"""
        return [block.to_json_config() for block in self.blocks.values()]
    
    def load_from_json_configs(self, configs: List[Dict]) -> None:
        """从JSON配置列表加载"""
        self.clear()
        for i, config in enumerate(configs):
            block_id = f"block_{i}"
            block = Block.from_json_config(config, block_id)
            self.add_block(block)
