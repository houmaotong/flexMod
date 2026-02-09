"""Xpath 操作处理模块"""
import xml.etree.ElementTree as ET


class CommentPreservingTreeBuilder(ET.TreeBuilder):
    """保留注释的 TreeBuilder"""
    def comment(self, text):
        self.start(ET.Comment, {})
        self.data(text)
        self.end(ET.Comment)


def parse_xml_with_comments(xml_file):
    """解析 XML 文件并保留注释
    
    Args:
        xml_file: XML 文件路径
        
    Returns:
        ET.ElementTree: 包含注释的 ElementTree 对象
    """
    parser = ET.XMLParser(target=CommentPreservingTreeBuilder())
    tree = ET.parse(xml_file, parser)
    return tree


def write_xml_with_comments(xml_file, tree):
    """写入 XML 文件并保留注释
    
    Args:
        xml_file: XML 文件路径
        tree: ElementTree 对象
    """
    # 自定义写入函数，保留注释
    def _write_element(elem, file, indent=""):
        # 写入注释
        if isinstance(elem, ET.Comment):
            file.write(f"{indent}<!-- {elem.text} -->\n")
            return
        
        # 写入元素开始标签
        file.write(f"{indent}<{elem.tag}")
        
        # 写入属性
        for key, value in elem.attrib.items():
            file.write(f" {key}='{value}'")
        
        # 检查是否有子元素
        children = list(elem)
        if children:
            file.write(">\n")
            # 递归写入子元素
            for child in children:
                _write_element(child, file, indent + "    ")
            file.write(f"{indent}</{elem.tag}>\n")
        else:
            # 写入空元素
            file.write(" / >\n")
    
    # 打开文件并写入
    with open(xml_file, 'w', encoding='utf-8') as f:
        # 写入 XML 声明
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        # 写入根元素
        _write_element(tree.getroot(), f)


class XpathHandler:
    """Xpath 操作处理类"""
    
    @staticmethod
    def is_attribute_selector(xpath: str) -> bool:
        """检查 xpath 是否是属性选择器
        
        Args:
            xpath: xpath 字符串
            
        Returns:
            bool: True 表示是属性选择器，False 表示不是
        """
        # 用 / 分割路径，检查最后一个部分是否以 @ 开头
        parts = xpath.split('/')
        if parts:
            last_part = parts[-1]
            return last_part.startswith('@')
        return False
    
    @staticmethod
    def validate_attribute_xpath(xml_file: str, xpath: str) -> bool:
        """验证 xpath 是否是可访问的属性
        
        Args:
            xml_file: xml 文件路径
            xpath: xpath 字符串
            
        Returns:
            bool: True 表示是可访问的属性，False 表示不是
        """
        try:
            # 首先检查是否是属性选择器
            if not XpathHandler.is_attribute_selector(xpath):
                # 根据需求，如果不是属性选择器，直接返回 False
                # 不调用 validate_xpath，因为我们需要严格验证是否是属性
                return False
            
            # 提取元素路径和属性名
            if '/@' in xpath:
                parts = xpath.rsplit('/', 1)
                if len(parts) == 2:
                    elem_path = parts[0]
                    attr_name = parts[1].lstrip('@')
                    # 验证元素路径是否存在
                    if XpathHandler.validate_xpath(xml_file, elem_path):
                        # 解析 xml 文件，检查属性是否存在
                        tree = parse_xml_with_comments(xml_file)
                        root = tree.getroot()
                        # 处理绝对路径
                        if elem_path.startswith('/'):
                            # 去掉开头的 /，得到 configs/append/...
                            path_parts = elem_path[1:].split('/')
                            # 检查路径的第一个部分是否与根元素的标签相同
                            if path_parts and path_parts[0] == root.tag:
                                # 去掉第一个部分，得到 append/...
                                path_parts = path_parts[1:]
                            # 构建相对路径
                            if path_parts:
                                elem_path = './' + '/'.join(path_parts)
                            else:
                                elem_path = '.'
                        # 查找元素
                        elem_result = root.findall(elem_path)
                        if elem_result:
                            # 检查元素是否有指定属性
                            for elem in elem_result:
                                if attr_name in elem.attrib:
                                    return True
                        # 元素存在但没有指定属性
                        return False
            elif xpath.startswith('@'):
                # 直接选择根元素的属性
                attr_name = xpath.lstrip('@')
                # 验证根元素是否存在（总是存在）
                # 检查根元素是否有指定属性
                tree = parse_xml_with_comments(xml_file)
                root = tree.getroot()
                return attr_name in root.attrib
            
            return False
        except Exception:
            # 如果出现异常，返回 False
            return False
    
    @staticmethod
    def validate_xpath(xml_file: str, xpath: str) -> bool:
        """验证 xpath 是否可以访问
        
        Args:
            xml_file: xml 文件路径
            xpath: xpath 字符串
            
        Returns:
            bool: True 表示 xpath 可以访问，False 表示不能访问
        """
        try:
            # 解析 xml 文件
            tree = parse_xml_with_comments(xml_file)
            root = tree.getroot()
            
            # 处理绝对路径
            if xpath.startswith('/'):
                # 去掉开头的 /，得到 configs/append/...
                path_parts = xpath[1:].split('/')
                # 检查路径的第一个部分是否与根元素的标签相同
                if path_parts and path_parts[0] == root.tag:
                    # 去掉第一个部分，得到 append/...
                    path_parts = path_parts[1:]
                # 构建相对路径
                if path_parts:
                    xpath = './' + '/'.join(path_parts)
                else:
                    xpath = '.'
            
            # 尝试使用 xpath 查找元素
            result = root.findall(xpath)
            
            # 如果找到元素，返回 True
            return len(result) > 0
        except Exception:
            # 如果出现异常，返回 False
            return False
    
    @staticmethod
    def update_xml_by_xpath(xml_file: str, xpaths: list, value) -> bool:
        """根据 xpath 修改 xml 文件中的值
        
        Args:
            xml_file: xml 文件路径
            xpaths: xpath 列表
            value: 要设置的值
            
        Returns:
            bool: True 表示修改成功，False 表示修改失败
        """
        try:
            # 读取文件内容，保留所有注释和格式
            with open(xml_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 遍历所有 xpath
            for xpath in xpaths:
                # 首先验证 xpath 是否可访问
                if not XpathHandler.validate_attribute_xpath(xml_file, xpath):
                    continue
                
                # 检查是否是属性选择器
                if '/@' in xpath:
                    # 提取元素路径和属性名
                    parts = xpath.rsplit('/', 1)
                    if len(parts) == 2:
                        elem_path = parts[0]
                        attr_name = parts[1].lstrip('@')
                        
                        # 使用ElementTree来定位元素，确保路径正确
                        tree = ET.parse(xml_file)
                        root = tree.getroot()
                        
                        # 处理路径
                        processed_path = elem_path
                        if processed_path.startswith('/'):
                            # 转换为相对路径
                            path_parts = processed_path[1:].split('/')
                            if path_parts and path_parts[0] == root.tag:
                                path_parts = path_parts[1:]
                            if path_parts:
                                processed_path = './' + '/'.join(path_parts)
                            else:
                                processed_path = '.'
                        
                        # 查找元素
                        elements = root.findall(processed_path)
                        if elements:
                            import re
                            
                            # 对每个找到的元素，构建精确的正则表达式来匹配其属性
                            for elem in elements:
                                # 获取元素的所有属性
                                elem_attrs = elem.attrib
                                elem_tag = elem.tag
                                
                                # 构建用于匹配该元素的正则表达式
                                # 包含所有属性，除了要修改的那个
                                attr_patterns = []
                                for key, val in elem_attrs.items():
                                    if key != attr_name:
                                        attr_patterns.append(r'%s\s*=\s*["\']%s["\']' % (re.escape(key), re.escape(val)))
                                
                                # 构建完整的元素匹配模式
                                if attr_patterns:
                                    # 有其他属性，需要包含它们
                                    pattern = r'(<\s*%s\s+)(%s)(\s+)(%s\s*=\s*)(["\'])([^"\']*)(["\'])(\s*/?>)' % (
                                        re.escape(elem_tag),
                                        r'\s+'.join(attr_patterns),
                                        re.escape(attr_name)
                                    )
                                else:
                                    # 只有要修改的属性
                                    pattern = r'(<\s*%s\s+)(%s\s*=\s*)(["\'])([^"\']*)(["\'])(\s*/?>)' % (
                                        re.escape(elem_tag),
                                        re.escape(attr_name)
                                    )
                                
                                # 构建替换函数
                                def replace_func(match):
                                    # 保留原始格式
                                    if len(match.groups()) == 8:
                                        # 有其他属性的情况
                                        return match.group(1) + match.group(2) + match.group(3) + \
                                               match.group(4) + match.group(5) + str(value) + match.group(7) + match.group(8)
                                    else:
                                        # 只有要修改的属性的情况
                                        return match.group(1) + match.group(2) + match.group(3) + \
                                               str(value) + match.group(5) + match.group(6)
                                
                                # 执行替换
                                content = re.sub(pattern, replace_func, content, flags=re.DOTALL)
            
            # 写回文件，保留所有注释和格式
            with open(xml_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
        except Exception:
            # 如果出现异常，返回 False
            return False
