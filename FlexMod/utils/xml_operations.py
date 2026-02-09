import json
import os
import re

class XmlOperations:
    """XML操作模块，用于处理FlexMod的内容定位注释"""
    
    @staticmethod
    def generate_positioning_comments(id):
        """根据ID生成内容定位注释
        
        Args:
            id (str): 功能块的唯一标识符
            
        Returns:
            tuple: (开始注释, 结束注释)
        """
        start_comment = f"<!-- FlexMod__{id}__Start -->"
        end_comment = f"<!-- FlexMod__{id}__End -->"
        return start_comment, end_comment
    
    @staticmethod
    def _update_config_code(setting_id, setting_value, flexmod_data, mod_files_dir):
        """更新配置代码的通用方法
        
        Args:
            setting_id (str): 要更新的设置项的ID
            setting_value: 设置项的当前值
            flexmod_data (dict): FlexMod JSON数据
            mod_files_dir (str): mod文件所在目录
        """
        # 查找该设置项的配置
        target_block = None
        for block in flexmod_data.get('configs', []):
            if block.get('uniqueId') == setting_id:
                target_block = block
                break
        
        if not target_block:
            return
        
        # 查找当前值对应的选项
        selected_option = None
        for option in target_block.get('optionItems', []):
            option_value = option.get('optionKey')
            if str(option_value).lower() == str(setting_value).lower():
                selected_option = option
                break
        
        if not selected_option:
            return
        
        # 遍历该选项的所有执行单元
        for exec_unit in selected_option.get('execUnits', []):
            file_path = exec_unit.get('filePath')
            code = exec_unit.get('execCode', '')
            
            if not file_path:
                continue
            
            # 构建完整的文件路径，直接使用mod_files_dir、'Config'和文件名拼接
            full_path = os.path.join(mod_files_dir, 'Config', file_path)
            
            # 如果文件不存在，跳过
            if not os.path.exists(full_path):
                continue
            
            # 生成定位注释
            start_comment, end_comment = XmlOperations.generate_positioning_comments(setting_id)
            
            # 读取文件内容并更新
            XmlOperations._update_file_content(full_path, start_comment, end_comment, code.strip())
    
    @staticmethod
    def _update_file_content(file_path, start_comment, end_comment, code):
        """更新文件内容
        
        Args:
            file_path (str): 文件路径
            start_comment (str): 开始注释
            end_comment (str): 结束注释
            code (str): 要插入的代码
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 构建正则表达式，匹配定位注释之间的内容
            pattern = re.escape(start_comment) + r'.*?' + re.escape(end_comment)
            replacement = start_comment + '\n' + code + '\n' + end_comment
            new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            
            # 写回文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
        except Exception:
            pass
    

    
    @staticmethod
    def update_bool_config_code(setting_id, player_settings_path, flexmod_json_path, mod_files_dir):
        """更新布尔类型配置的代码
        
        Args:
            setting_id (str): 要更新的设置项的ID
            player_settings_path (str): player_settings.json文件路径
            flexmod_json_path (str): FlexMod JSON文件路径
            mod_files_dir (str): mod文件所在目录
        """
        # 读取player_settings.json文件
        with open(player_settings_path, 'r', encoding='utf-8') as f:
            player_settings = json.load(f)
        
        # 获取该设置项的当前值
        final_settings = player_settings.get('finalSettings', {})
        
        # 检查setting_id是否在finalSettings中
        if setting_id not in final_settings:
            return
        
        setting_value = final_settings[setting_id]
        
        # 读取FlexMod JSON文件
        with open(flexmod_json_path, 'r', encoding='utf-8') as f:
            flexmod_data = json.load(f)
        
        # 调用通用更新方法
        XmlOperations._update_config_code(setting_id, setting_value, flexmod_data, mod_files_dir)
    
    @staticmethod
    def update_select_config_code(setting_id, player_settings_path, flexmod_json_path, mod_files_dir):
        """更新选择类型配置的代码
        
        Args:
            setting_id (str): 要更新的设置项的ID
            player_settings_path (str): player_settings.json文件路径
            flexmod_json_path (str): FlexMod JSON文件路径
            mod_files_dir (str): mod文件所在目录
        """
        # 读取player_settings.json文件
        with open(player_settings_path, 'r', encoding='utf-8') as f:
            player_settings = json.load(f)
        
        # 获取该设置项的当前值
        final_settings = player_settings.get('finalSettings', {})
        
        # 检查setting_id是否在finalSettings中
        if setting_id not in final_settings:
            return
        
        setting_value = final_settings[setting_id]
        
        # 读取FlexMod JSON文件
        with open(flexmod_json_path, 'r', encoding='utf-8') as f:
            flexmod_data = json.load(f)
        
        # 调用通用更新方法
        XmlOperations._update_config_code(setting_id, setting_value, flexmod_data, mod_files_dir)
    
    @staticmethod
    def update_slider_config_code(setting_id, player_settings_path, flexmod_json_path, mod_files_dir):
        """更新滑块类型配置的代码
        
        Args:
            setting_id (str): 要更新的设置项的ID
            player_settings_path (str): player_settings.json文件路径
            flexmod_json_path (str): FlexMod JSON文件路径
            mod_files_dir (str): mod文件所在目录
        """
        from .xpath_handler import XpathHandler
        # 读取player_settings.json文件
        with open(player_settings_path, 'r', encoding='utf-8') as f:
            player_settings = json.load(f)
        
        # 获取该设置项的当前值
        final_settings = player_settings.get('finalSettings', {})
        
        # 检查setting_id是否在finalSettings中
        if setting_id not in final_settings:
            return
        
        setting_value = final_settings[setting_id]
        
        # 读取FlexMod JSON文件
        with open(flexmod_json_path, 'r', encoding='utf-8') as f:
            flexmod_data = json.load(f)
        
        # 查找该设置项的配置
        target_block = None
        for block in flexmod_data.get('configs', []):
            if block.get('uniqueId') == setting_id:
                target_block = block
                break
        
        if not target_block:
            return
        
        # 获取XpathSet
        xpath_set = target_block.get('XpathSet', [])
        
        if not xpath_set:
            return
        
        # 遍历XpathSet中的每个项
        for xpath_item in xpath_set:
            file_path = xpath_item.get('filePath')
            xpaths = xpath_item.get('xpath', [])
            
            if not file_path:
                continue
            
            # 构建完整的文件路径，直接使用mod_files_dir、'Config'和文件名拼接
            full_path = os.path.join(mod_files_dir, 'Config', file_path)
            
            # 如果文件不存在，跳过
            if not os.path.exists(full_path):
                continue
            
            # 直接根据xpath修改文件中的值
            XpathHandler.update_xml_by_xpath(full_path, xpaths, setting_value)
    
    @staticmethod
    def update_int_slider_config_code(setting_id, player_settings_path, flexmod_json_path, mod_files_dir):
        """更新整数滑块类型配置的代码
        
        Args:
            setting_id (str): 要更新的设置项的ID
            player_settings_path (str): player_settings.json文件路径
            flexmod_json_path (str): FlexMod JSON文件路径
            mod_files_dir (str): mod文件所在目录
        """
        XmlOperations.update_slider_config_code(setting_id, player_settings_path, flexmod_json_path, mod_files_dir)
    
    @staticmethod
    def update_float_slider_config_code(setting_id, player_settings_path, flexmod_json_path, mod_files_dir):
        """更新浮点数滑块类型配置的代码
        
        Args:
            setting_id (str): 要更新的设置项的ID
            player_settings_path (str): player_settings.json文件路径
            flexmod_json_path (str): FlexMod JSON文件路径
            mod_files_dir (str): mod文件所在目录
        """
        XmlOperations.update_slider_config_code(setting_id, player_settings_path, flexmod_json_path, mod_files_dir)
    
    @staticmethod
    def update_all_configs(player_settings_path, flexmod_json_path, mod_files_dir):
        """更新所有配置的代码
        
        Args:
            player_settings_path (str): player_settings.json文件路径
            flexmod_json_path (str): FlexMod JSON文件路径
            mod_files_dir (str): mod文件所在目录
        """
        # 读取player_settings.json文件
        with open(player_settings_path, 'r', encoding='utf-8') as f:
            player_settings = json.load(f)
        
        final_settings = player_settings.get('finalSettings', {})
        
        # 读取FlexMod JSON文件
        with open(flexmod_json_path, 'r', encoding='utf-8') as f:
            flexmod_data = json.load(f)
        
        blocks = flexmod_data.get('configs', [])
        
        # 创建配置块映射，key为uniqueId，value为配置块
        block_map = {}
        for block in blocks:
            block_id = block.get('uniqueId')
            if block_id:
                block_map[block_id] = block
        
        # 遍历finalSettings中的所有项，按顺序更新
        for setting_id in final_settings:
            if setting_id in block_map:
                block = block_map[setting_id]
                config_type = block.get('configType')
                
                # 根据配置类型调用对应的方法
                if config_type == 'boolConfig':
                    XmlOperations.update_bool_config_code(setting_id, player_settings_path, flexmod_json_path, mod_files_dir)
                elif config_type == 'selectConfig':
                    XmlOperations.update_select_config_code(setting_id, player_settings_path, flexmod_json_path, mod_files_dir)
                elif config_type in ['intSliderConfig', 'intSlider']:
                    XmlOperations.update_int_slider_config_code(setting_id, player_settings_path, flexmod_json_path, mod_files_dir)
                elif config_type in ['floatSliderConfig', 'floatSlider']:
                    XmlOperations.update_float_slider_config_code(setting_id, player_settings_path, flexmod_json_path, mod_files_dir)
    
    @staticmethod
    def check_missing_comments(json_path, mod_files_dir):
        """检查所有mod文件具体缺少哪些id定位注释
        
        Args:
            json_path (str): FlexMod JSON文件路径
            mod_files_dir (str): mod文件所在目录
            
        Returns:
            dict: 以文件路径为键，值为包含该文件中缺少注释的ID列表
        """
        # 从JSON中提取所有块
        blocks = {}
        block_types = {}
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for block in data.get('configs', []):
            block_id = block.get('uniqueId')
            if not block_id:
                continue
            
            # 获取块的类型
            block_type = block.get('configType', '')
            block_types[block_id] = block_type
            
            # 收集该块的所有文件路径
            file_paths = []
            
            # 检查是否有直接的filePath属性（适用于intSlider和floatSlider类型）
            direct_file_path = block.get('filePath')
            if direct_file_path:
                file_paths.append(direct_file_path)
            elif direct_file_path == '':
                # 捕捉路径为空的情况
                file_paths.append('')
            
            # 检查XpathSet（适用于新的intSlider和floatSlider类型）
            xpath_set = block.get('XpathSet', [])
            for xpath_item in xpath_set:
                xpath_file_path = xpath_item.get('filePath')
                if xpath_file_path:
                    file_paths.append(xpath_file_path)
                elif xpath_file_path == '':
                    # 捕捉路径为空的情况
                    file_paths.append('')
            
            # 检查选项项中的执行单元（适用于boolConfig和selectConfig类型）
            for option in block.get('optionItems', []):
                for exec_unit in option.get('execUnits', []):
                    file_path = exec_unit.get('filePath')
                    if file_path:
                        file_paths.append(file_path)
                    elif file_path == '':
                        # 捕捉路径为空的情况
                        file_paths.append('')
            
            # 去重并存储
            blocks[block_id] = list(set(file_paths))
        
        # 检查缺失的注释
        missing_comments = {}
        for block_id, file_paths in blocks.items():
            # 获取块的类型
            block_type = block_types.get(block_id, '')
            
            # 忽略整数/浮点功能块的定位注释检查
            if block_type in ['intSliderConfig', 'intSlider', 'floatSliderConfig', 'floatSlider']:
                continue
            
            for file_path in file_paths:
                # 尝试直接路径
                full_path = os.path.join(mod_files_dir, file_path)
                
                # 如果文件不存在，尝试向上一级目录的Config目录中查找
                if not os.path.exists(full_path):
                    # 获取mod_files_dir的上一级目录（即MOD根目录）
                    mod_root_dir = os.path.dirname(mod_files_dir)
                    config_path = os.path.join(mod_root_dir, 'Config', file_path)
                    if os.path.exists(config_path):
                        full_path = config_path
                    else:
                        # 文件不存在，也标记为缺少注释
                        if file_path not in missing_comments:
                            missing_comments[file_path] = []
                        missing_comments[file_path].append(block_id)
                        continue
                
                start_comment, end_comment = XmlOperations.generate_positioning_comments(block_id)
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                if start_comment not in content or end_comment not in content:
                    if file_path not in missing_comments:
                        missing_comments[file_path] = []
                    missing_comments[file_path].append(block_id)
        
        return missing_comments
    
    @staticmethod
    def check_extra_comments(json_path, mod_files_dir):
        """检查所有mod 文件具体多余哪些id定位注释
        
        Args:
            json_path (str): FlexMod JSON文件路径
            mod_files_dir (str): mod文件所在目录
            
        Returns:
            dict: 以文件路径为键，值为该文件中发现的多余ID列表
        """
        # 从JSON中提取所有已知的ID
        known_ids = []
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for block in data.get('configs', []):
            block_id = block.get('uniqueId')
            if block_id:
                # 获取块的类型
                block_type = block.get('configType', '')
                # 忽略整数/浮点功能块的定位注释检查
                if block_type not in ['intSliderConfig', 'intSlider', 'floatSliderConfig', 'floatSlider']:
                    known_ids.append(block_id)
        
        # 查找多余的注释
        extra_comments = {}
        pattern = r'<!-- FlexMod__(.+?)__Start -->'
        
        # 遍历所有XML文件
        # 首先遍历FlexMod目录
        for root, _, files in os.walk(mod_files_dir):
            for file in files:
                if file.endswith('.xml'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    # 查找所有FlexMod开始注释
                    matches = re.findall(pattern, content)
                    for found_id in matches:
                        if found_id not in known_ids:
                            relative_path = os.path.relpath(file_path, mod_files_dir)
                            if relative_path not in extra_comments:
                                extra_comments[relative_path] = []
                            extra_comments[relative_path].append(found_id)
        
        # 然后遍历MOD根目录的Config目录
        mod_root_dir = os.path.dirname(mod_files_dir)
        config_dir = os.path.join(mod_root_dir, 'Config')
        if os.path.exists(config_dir):
            for root, _, files in os.walk(config_dir):
                for file in files:
                    if file.endswith('.xml'):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                        
                        # 查找所有FlexMod开始注释
                        matches = re.findall(pattern, content)
                        for found_id in matches:
                            if found_id not in known_ids:
                                # 使用相对于MOD根目录的路径
                                relative_path = os.path.relpath(file_path, mod_root_dir)
                                if relative_path not in extra_comments:
                                    extra_comments[relative_path] = []
                                extra_comments[relative_path].append(found_id)
        
        return extra_comments
    
    @staticmethod
    def check_nonexistent_files(json_path, mod_files_dir):
        """检查FlexMod是否使用了不存在的文件
        
        Args:
            json_path (str): FlexMod JSON文件路径
            mod_files_dir (str): mod文件所在目录
            
        Returns:
            dict: 以文件路径为键，值为包含使用该不存在文件的(ID, displayName)元组列表
        """
        # 从JSON中提取所有块
        blocks = {}
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for block in data.get('configs', []):
            block_id = block.get('uniqueId')
            if not block_id:
                continue
            
            block_display_name = block.get('displayName', block_id)
            
            # 收集该块的所有文件路径
            file_paths = []
            
            # 检查是否有直接的filePath属性（适用于intSlider和floatSlider类型）
            direct_file_path = block.get('filePath')
            if direct_file_path:
                file_paths.append(direct_file_path)
            elif direct_file_path == '':
                # 捕捉路径为空的情况
                file_paths.append('')
            
            # 检查XpathSet（适用于新的intSlider和floatSlider类型）
            xpath_set = block.get('XpathSet', [])
            for xpath_item in xpath_set:
                xpath_file_path = xpath_item.get('filePath')
                if xpath_file_path:
                    file_paths.append(xpath_file_path)
                elif xpath_file_path == '':
                    # 捕捉路径为空的情况
                    file_paths.append('')
            
            # 检查选项项中的执行单元（适用于boolConfig和selectConfig类型）
            for option in block.get('optionItems', []):
                for exec_unit in option.get('execUnits', []):
                    file_path = exec_unit.get('filePath')
                    if file_path:
                        file_paths.append(file_path)
                    elif file_path == '':
                        # 捕捉路径为空的情况
                        file_paths.append('')
            
            # 去重并存储
            blocks[block_id] = (block_display_name, list(set(file_paths)))
        
        # 检查不存在的文件
        nonexistent_files = {}
        for block_id, (block_display_name, file_paths) in blocks.items():
            for file_path in file_paths:
                # 处理空路径情况
                if file_path == '':
                    if file_path not in nonexistent_files:
                        nonexistent_files[file_path] = []
                    nonexistent_files[file_path].append((block_id, block_display_name))
                    continue
                
                # 尝试直接路径
                full_path = os.path.join(mod_files_dir, file_path)
                file_exists = os.path.exists(full_path)
                
                # 如果文件不存在，尝试向上一级目录的Config目录中查找
                if not file_exists:
                    mod_root_dir = os.path.dirname(mod_files_dir)
                    config_path = os.path.join(mod_root_dir, 'Config', file_path)
                    file_exists = os.path.exists(config_path)
                
                # 检查文件是否存在
                if not file_exists:
                    if file_path not in nonexistent_files:
                        nonexistent_files[file_path] = []
                    nonexistent_files[file_path].append((block_id, block_display_name))
        
        return nonexistent_files
