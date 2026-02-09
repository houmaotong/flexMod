"""功能块数据模型"""
from enum import Enum
from typing import Dict, Any, Optional
from dataclasses import dataclass, field


class BlockType(Enum):
    """功能块类型枚举"""
    SWITCH = 'switch'
    OPTION = 'option'
    INT_SLIDER = 'int-slider'
    FLOAT_SLIDER = 'float-slider'
    
    def get_display_name(self, lang: int = 0) -> str:
        """获取显示名称"""
        display_names = {
            BlockType.SWITCH: ("Boolean", "开关功能"),
            BlockType.OPTION: ("Dropdown", "下拉选项"),
            BlockType.INT_SLIDER: ("Integer Slider", "整数滑块"),
            BlockType.FLOAT_SLIDER: ("Float Slider", "浮点滑块")
        }
        name_tuple = display_names[self]
        if len(name_tuple) > lang:
            return name_tuple[lang]
        return name_tuple[0]
    
    def get_config_type(self) -> str:
        """获取配置类型"""
        config_types = {
            BlockType.SWITCH: "boolConfig",
            BlockType.OPTION: "selectConfig",
            BlockType.INT_SLIDER: "intSlider",
            BlockType.FLOAT_SLIDER: "floatSlider"
        }
        return config_types[self]
    
    def get_default_value(self) -> Any:
        """获取默认值"""
        default_values = {
            BlockType.SWITCH: True,
            BlockType.OPTION: "option1",
            BlockType.INT_SLIDER: 100,
            BlockType.FLOAT_SLIDER: 1.0
        }
        return default_values[self]


@dataclass
class Block:
    """功能块数据模型"""
    block_id: str
    block_type: BlockType
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    def get_parameter(self, key: str, default: Any = None) -> Any:
        """获取参数值"""
        return self.parameters.get(key, default)
    
    def set_parameter(self, key: str, value: Any) -> None:
        """设置参数值"""
        self.parameters[key] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'block_id': self.block_id,
            'block_type': self.block_type.value,
            'parameters': self.parameters
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Block':
        """从字典创建"""
        return cls(
            block_id=data['block_id'],
            block_type=BlockType(data['block_type']),
            parameters=data.get('parameters', {})
        )
    
    def to_json_config(self) -> Dict[str, Any]:
        """转换为JSON配置格式"""
        config = {
            'uniqueId': self.get_parameter('func_id', f'config_{self.block_id}'),
            'displayName': self.get_parameter('func_name', '未命名配置'),
            'groupName': self.get_parameter('group_name', 'Default'),
            'configType': self.block_type.get_config_type(),
            'desc': self.get_parameter('description', ''),
            'defaultValue': self._get_default_value()
        }
        
        if self.block_type == BlockType.SWITCH:
            config['optionItems'] = self._get_switch_option_items()
        elif self.block_type == BlockType.OPTION:
            config['optionItems'] = self.get_parameter('option_items', [])
        elif self.block_type == BlockType.INT_SLIDER:
            try:
                config['minValue'] = int(self.get_parameter('min_value', '1'))
            except (ValueError, TypeError):
                config['minValue'] = 1
            try:
                config['maxValue'] = int(self.get_parameter('max_value', '100'))
            except (ValueError, TypeError):
                config['maxValue'] = 100
            try:
                config['stepValue'] = int(self.get_parameter('step_value', '1'))
            except (ValueError, TypeError):
                config['stepValue'] = 1
            config['XpathSet'] = self.get_parameter('XpathSet', [])
        elif self.block_type == BlockType.FLOAT_SLIDER:
            try:
                config['minValue'] = float(self.get_parameter('min_value', '0.5'))
            except (ValueError, TypeError):
                config['minValue'] = 0.5
            try:
                config['maxValue'] = float(self.get_parameter('max_value', '2.0'))
            except (ValueError, TypeError):
                config['maxValue'] = 2.0
            try:
                config['stepValue'] = float(self.get_parameter('step_value', '0.1'))
            except (ValueError, TypeError):
                config['stepValue'] = 0.1
            config['XpathSet'] = self.get_parameter('XpathSet', [])
        
        return config
    
    def _get_default_value(self) -> Any:
        """获取默认值"""
        if self.block_type == BlockType.SWITCH:
            value = self.get_parameter('default_value', 'true')
            return value.lower() == 'true'
        elif self.block_type == BlockType.INT_SLIDER:
            try:
                return int(self.get_parameter('default_value', '100'))
            except (ValueError, TypeError):
                return 100
        elif self.block_type == BlockType.FLOAT_SLIDER:
            try:
                return float(self.get_parameter('default_value', '1.0'))
            except (ValueError, TypeError):
                return 1.0
        else:
            return self.get_parameter('default_value', 'option1')
    
    def _get_switch_option_items(self) -> list:
        """获取开关类型的选项项"""
        option_items = [
            {
                'optionKey': 'true',
                'execUnits': self.get_parameter('true_exec_units', [])
            },
            {
                'optionKey': 'false',
                'execUnits': self.get_parameter('false_exec_units', [])
            }
        ]
        
        return option_items
    
    @classmethod
    def from_json_config(cls, config: Dict[str, Any], block_id: str) -> 'Block':
        """从JSON配置创建"""
        config_type_map = {
            'boolConfig': BlockType.SWITCH,
            'selectConfig': BlockType.OPTION,
            'intSlider': BlockType.INT_SLIDER,
            'floatSlider': BlockType.FLOAT_SLIDER
        }
        
        block_type = config_type_map.get(config.get('configType'), BlockType.SWITCH)
        parameters = {
            'func_id': config.get('uniqueId', ''),
            'func_name': config.get('displayName', '未命名配置'),
            'group_name': config.get('groupName', 'Default'),
            'description': config.get('desc', '')
        }
        
        if block_type == BlockType.SWITCH:
            parameters['default_value'] = str(config.get('defaultValue', 'true'))
            if 'optionItems' in config:
                for option in config['optionItems']:
                    if option.get('optionKey') == 'true':
                        parameters['true_exec_units'] = option.get('execUnits', [])
                    elif option.get('optionKey') == 'false':
                        parameters['false_exec_units'] = option.get('execUnits', [])
        elif block_type == BlockType.OPTION:
            parameters['default_value'] = str(config.get('defaultValue', 'option1'))
            if 'optionItems' in config:
                parameters['option_items'] = config['optionItems']
        elif block_type == BlockType.INT_SLIDER:
            # 确保整数值正确处理，即使从JSON中读取到浮点数
            default_value = config.get('defaultValue', 100)
            min_value = config.get('minValue', 1)
            max_value = config.get('maxValue', 100)
            step_value = config.get('stepValue', 1)
            
            # 转换为整数
            if isinstance(default_value, float):
                default_value = int(default_value)
            if isinstance(min_value, float):
                min_value = int(min_value)
            if isinstance(max_value, float):
                max_value = int(max_value)
            if isinstance(step_value, float):
                step_value = int(step_value)
            
            parameters['default_value'] = str(default_value)
            parameters['min_value'] = str(min_value)
            parameters['max_value'] = str(max_value)
            parameters['step_value'] = str(step_value)
            parameters['XpathSet'] = config.get('XpathSet', [])
        elif block_type == BlockType.FLOAT_SLIDER:
            parameters['default_value'] = str(config.get('defaultValue', '1.0'))
            parameters['min_value'] = str(config.get('minValue', '0.5'))
            parameters['max_value'] = str(config.get('maxValue', '2.0'))
            parameters['step_value'] = str(config.get('stepValue', '0.1'))
            parameters['XpathSet'] = config.get('XpathSet', [])
        
        return cls(block_id=block_id, block_type=block_type, parameters=parameters)
