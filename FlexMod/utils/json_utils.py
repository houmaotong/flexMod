"""JSON工具"""
import json
from typing import Dict, Any, Optional


class JsonUtils:
    """JSON工具类"""
    
    @staticmethod
    def format_json(data: Dict[str, Any], indent: int = 2) -> str:
        """格式化JSON"""
        return json.dumps(data, ensure_ascii=False, indent=indent)
    
    @staticmethod
    def parse_json(json_str: str) -> Optional[Dict[str, Any]]:
        """解析JSON字符串"""
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"JSON解析失败: {e}")
            return None
    
    @staticmethod
    def validate_json(data: Dict[str, Any]) -> bool:
        """验证JSON数据结构"""
        if not isinstance(data, dict):
            return False
        
        if 'groups' not in data or not isinstance(data['groups'], list):
            return False
        
        if 'configs' not in data or not isinstance(data['configs'], list):
            return False
        
        return True
    
    @staticmethod
    def merge_json(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """合并JSON数据"""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = JsonUtils.merge_json(result[key], value)
            else:
                result[key] = value
        return result
    
    @staticmethod
    def deep_copy(data: Any) -> Any:
        """深拷贝数据"""
        return json.loads(json.dumps(data))
