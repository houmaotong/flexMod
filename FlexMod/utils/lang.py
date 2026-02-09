"""语言管理模块 - 支持中英文双语"""


class Lang:
    """语言文本类"""
    
    # 主窗口
    main_window_title = ('FelxMod for 7Days to die ', 'FelxMod 七日杀可变模组')
    
    # 导航栏
    home = ('Home', '主界面')
    setting = ('Setting', '设置')
    lang = ('Language', '语言')
    
    # 警告和确认
    warning = ('Warning', '警告')
    confirm = ('Confirm', '确认')
    cancel = ('Cancel', '取消')
    
    # 验证面板
    toggle_all = ('Toggle All', '切换全部')
    toggle_all_expanded = ('Collapse All', '全部折叠')
    toggle_all_collapsed = ('Expand All', '全部展开')
    
    # 设置页面
    mods_dir_label = ('Mods Dir', '模组目录')
    mods_dir_btn = ('Re-set', '重新设置')
    mods_dir_open_btn = ('Show in Exp', '定位文件夹')
    mods_dir_sel_win_title = (
        'Please select the Mods folder of 7 Days to Die (./7DaysToDie/Mods)',
        '请选择7DaysToDie的Mods文件夹(./7DaysToDie/Mods)'
    )
    mods_dir_not_mods_dir = (
        'The selected folder is not the 7 Days to Die Mods folder (./7DaysToDie/Mods).\nThe program may not work correctly.\n\nClick OK to re-select, or Cancel to exit the program.',
        '现在的文件夹不是Mods文件夹（./7DaysToDie/Mods） \n程序可能无法正确运行\n\n点击确认重新选择，点击取消退出程序'
    )
    
    # 主页
    flexmod_list_title = ('FlexMod List', 'FlexMod 列表')
    add_flexmod_btn = ('+ FlexMod', '+ FlexMod')
    delete_btn = ('Delete', '删除')
    refresh_btn = ('Refresh', '刷新')
    add_flexmod_win_title = ('Add \'FlexMod\' in My Mod', '添加 \'FlexMod\' 到我的模组')
    
    # FlexMod编辑器
    flexmod_editor_title = ('FlexMod Editor', 'FlexMod 编辑器')
    gui_tab = ('Gui', 'Gui')
    code_tab = ('Code', 'Code')
    view_json_code = ('View JSON ', '查看JSON')
    validate_btn_text = ('Validate', '验证')
    validate_data = ('Validate Data', '验证数据')
    block_list = ('Block List', '功能块列表')
    detail_params = ('Detail Parameters', '详细参数')
    group_settings = ('Group Settings', '分组设置')
    file_path = ('File Path', '文件路径')
    true_code = ('Code when Enabled', '开启时执行代码')
    false_code = ('Code when Disabled', '关闭时执行代码')
    code_template = ('Code Template', '代码模板')
    
    # 功能块类型
    block_type_bool = ('Boolean', '开关')
    block_type_dropdown = ('Dropdown', '下拉选项')
    block_type_int_slider = ('Integer Slider', '整数滑块')
    block_type_float_slider = ('Float Slider', '浮点滑块')
    
    # 功能块操作
    add_block = ('Add Block', '添加功能块')
    delete_block = ('Delete Block', '删除功能块')
    edit_block = ('Edit Block', '编辑功能块')
    
    # 分组操作
    add_group = ('Add Group', '添加分组')
    delete_group = ('Delete Group', '删除分组')
    edit_group = ('Edit Group', '编辑分组')
    
    # 参数
    unique_id = ('Unique ID', '唯一标识符ID') 
    display_name = ('Display Name', '显示名称')
    description = ('Description', '描述')
    group = ('Group', '分组')
    default_value = ('Default Value', '默认值')
    min_value = ('Min Value', '最小值')
    max_value = ('Max Value', '最大值')
    step = ('Step', '步长')
    options = ('Options', '选项')
    
    # 提示信息
    success = ('Success', '成功')
    error = ('Error', '错误')
    info = ('Info', '提示')
    
    # XPath验证
    xpath_validation_failed = ('XPath validation failed!', 'XPath 验证失败！')
    xpath_validation_success = ('XPath validation success!', 'XPath 验证成功！')
    not_attribute_selector = ('Not attribute selector', '不是属性选择器')
    attribute_not_accessible = ('Attribute not accessible', '属性不可访问')
    file_not_exists = ('File not exists!', '文件不存在！')
    please_select_file_path = ('Please select file path first!', '请先选择文件路径！')
    
    # 警告信息
    please_select_item = ('Please select an item first!', '请先选择一个项目！')
    please_enter_value = ('Please enter a value!', '请输入值！')
    confirm_delete = ('Are you sure you want to delete this item?', '确定要删除这个项目吗？')
    group_name_exists = ('Group name already exists. Please choose a different name.', '分组名称已存在，请选择其他名称。')
    
    # 文件操作
    file_not_found = ('File not found', '文件未找到')
    save_success = ('Saved successfully', '保存成功')
    load_success = ('Loaded successfully', '加载成功')
    copy_success = ('Copied successfully!', '复制成功！')
    copied_to_clipboard = ('Copied to clipboard', '已经复制到剪切板')
    
    # 代码编辑器
    code_editor_title = ('Code Editor', '代码编辑器')
    text_editor_title = ('Code/Text Editor', '代码/文本编辑器')
    open_in_new_window = ('Open in New Window', '在新窗口打开')
    save_json = ('Save JSON', '保存JSON')
    
    # JSON预览
    json_preview = ('JSON Preview', 'JSON预览')
    
    # 操作日志
    operation_log = ('Operation Log', '操作日志')
    
    # 说明
    mods_dir_description = (
        'Description:\nThe mods directory should be the Mods folder in the 7 Days to Die game directory.\nExample: C:\\Program Files (x86)\\Steam\\steamapps\\common\\7 Days To Die\\Mods',
        '说明：\n模组目录应该是7 Days to Die游戏目录下的Mods文件夹。\n例如：C:\\Program Files (x86)\\Steam\\steamapps\\common\\7 Days To Die\\Mods'
    )
    
    # 添加FlexMod
    select_mod_folder = ('Select Mod Folder', '选择模组文件夹')
    no_mods_found = ('No mod folders found in the mods directory!', '模组目录下没有找到任何文件夹！')
    no_available_mods = ('All mods have been added!', '所有模组都已添加！')
    added_flexmod = ('Added FlexMod', '已添加 FlexMod')
    removed_flexmod = ('Removed FlexMod', '已从列表中移除 FlexMod')
    remove_warning = (
        'Are you sure you want to remove FlexMod \'{}\'?\n\nNote: This will only remove it from the list, not delete the files.',
        '确定要删除 FlexMod \'{}\' 吗？\n\n注意：这只会从列表中移除，不会删除文件。'
    )
    
    # 设置
    settings_saved = ('Settings saved!', '设置已保存！')
    please_set_mods_dir = ('Please set the mods directory first!', '请先设置模组目录！')
    directory_not_exist = ('Directory does not exist', '目录不存在')
    save_anyway = ('The directory does not exist: {}\n\nDo you still want to save?', '目录不存在：{}\n\n是否仍要保存？')
    open_folder_failed = ('Failed to open folder', '打开文件夹失败')
    load_settings_failed = ('Failed to load settings', '加载设置失败')
    save_settings_failed = ('Failed to save settings', '保存设置失败')
    open_directory_failed = ('Failed to open directory', '打开目录失败')
    
    # 其他
    default_group = ('Default', '默认')
    group_name = ('Group Name', '分组名称')
    group_desc = ('Group Description', '分组描述')
    option_key = ('Option Key', '选项键')
    option_value = ('Option Value', '选项值')
    option = ('Opt', '选项')
    exec_units = ('Exec Units', '执行单元')
    exec_code = ('Execution Code', '执行代码')
    add_exec_unit = ('+ Add Exec Unit', '+ 添加执行单元')
    add_option = ('+ Add Option', '+ 添加选项')
    option_name = ('Option Name', '选项名称')
    placeholder_option_name = ('Option name (e.g., Low Refresh Rate)', '选项名称（例：低刷新率）')
    
    # 滑块参数验证提示
    slider_param_error = ('Slider Parameter Error', '滑块参数错误')
    slider_param_validation = (
        'Please enter valid values for the slider parameters:\n\n' 
        '• Enter the correct type for the current block (integer/float)\n' 
        '• Minimum value < Maximum value\n' 
        '• Minimum value ≤ Default value ≤ Maximum value\n' 
        '• 0 < Step < Maximum value',
        '请为滑块参数输入有效值：\n\n' 
        '• 根据当前功能块类型输入正确的值类型（整数/浮点）\n' 
        '• 最小值 < 最大值\n' 
        '• 最小值 ≤ 默认值 ≤ 最大值\n' 
        '• 0 < 步长 < 最大值'
    )
    # 滑块参数错误类型提示
    slider_error_type = ('Invalid Input Type', '输入类型错误')
    slider_error_type_msg = (
        'Please enter the correct type for the current block:\n\n' 
        '• For Integer Slider: Enter integer values only\n' 
        '• For Float Slider: Enter number values (integers or decimals)',
        '请根据当前功能块类型输入正确的值：\n\n' 
        '• 整数滑块：仅输入整数值\n' 
        '• 浮点滑块：输入数字值（整数或小数）'
    )
    slider_error_range = ('Invalid Range', '范围错误')
    slider_error_range_msg = (
        'Minimum value must be less than Maximum value\n\n' 
        'Please adjust your values accordingly.',
        '最小值必须小于最大值\n\n' 
        '请相应调整您的值。'
    )
    slider_error_default = ('Invalid Default Value', '默认值错误')
    slider_error_default_msg = (
        'Default value must be between Minimum and Maximum values\n\n' 
        'Please adjust your default value accordingly.',
        '默认值必须在最小值和最大值之间\n\n' 
        '请相应调整您的默认值。'
    )
    slider_error_step = ('Invalid Step Value', '步长错误')
    slider_error_step_msg = (
        'Step value must be greater than 0 and less than Maximum value\n\n' 
        'Please adjust your step value accordingly.',
        '步长必须大于0且小于最大值\n\n' 
        '请相应调整您的步长值。'
    )
    
    # 功能块ID验证提示
    func_id_empty_error = ('Unique ID cannot be empty', '唯一标识符ID不能为空')
    func_id_special_chars_error = ('Unique ID can only contain letters, numbers, and underscores', '唯一标识符ID只能包含字母、数字和下划线')
    func_id_digit_start_error = ('Unique ID cannot start with a number', '唯一标识符ID不能以数字开头')
    func_id_underscore_error = ('Unique ID cannot start or end with an underscore', '唯一标识符ID不能以下划线开头或结尾')
    func_id_double_underscore_error = ('Unique ID cannot contain consecutive underscores', '唯一标识符ID不能包含连续的下划线')
    
    # 代码模板验证提示
    code_tpl_empty_error = ('Code template cannot be empty', '代码模板不能为空')
    code_tpl_missing_placeholder_error = ('Code template must contain "{0}" placeholder', '代码模板必须包含"{0}"占位符')
    
    # 验证面板
    validate_results = ('Validation Results', '验证结果')
    validate_missing_comments_title = ('Mod files have missing ID positioning comments', 'mod文件，存在未写的ID定位注释')
    validate_missing_comments_content = ('The following files are missing ID positioning comments:', '以下文件缺少ID定位注释：')
    validate_missing_comment_item = ('{} is missing {} positioning comment', '{} 缺少 {} 的定位注释')
    validate_extra_comments_title = ('Mod files have extra ID positioning comments', 'mod文件，存在多余ID定位注释')
    validate_extra_comments_content = ('The following files have extra ID positioning comments:', '以下文件存在多余的ID定位注释：')
    validate_extra_comment_item = ('{} has extra {} positioning comment', '{} 多余了 {} 的定位注释')
    validate_nonexistent_files_title = ('FlexMod uses files that do not exist in the Config directory', 'FlexMod,使用了Config目录不存在的文件')
    validate_nonexistent_files_content = ('The following files do not exist in the Config/ directory:', '以下文件在Config/目录中不存在：')
    validate_nonexistent_file_item = ('{} (used by: id: {}  name:{})', '{} (被使用：id: {}  name:{})')
    validate_success_title = ('Validation Completed', '验证完成')
    validate_success_content = ('All validation items passed, no issues found.', '所有验证项均通过，未发现任何问题。')
    validate_error_title = ('Validation Error', '验证错误')
    validate_error_content = ('An error occurred during validation:', '验证过程中发生错误：')
    func_id_duplicate_error = ('Unique ID already exists', '唯一标识符ID已存在')
    func_id_case_insensitive_error = ('Unique ID is case-insensitively duplicate with existing ID "{}". Please choose a different name.', '唯一标识符ID与已存在的ID "{}" 大小写不敏感重复。请选择一个不同的名称。')
    
    # 通知类型
    notification_info = ('Info', '信息')
    notification_warning = ('Warning', '注意')
    notification_success = ('Success', '成功')
    notification_error = ('Error', '错误')
    
    # 占位符文本
    placeholder_config_path = ('xxx.xml', 'xxx.xml')
    placeholder_group_desc = ('Group description', '分组描述')
    placeholder_unique_id = ('Unique ID (e.g., enable_night_vision)', '唯一标识（例：enable_night_vision）')
    placeholder_display_name = ('Display name (e.g., Player Night Vision)', '功能显示名称（例：玩家夜视）')
    placeholder_desc = ('Function description', '功能描述信息')
    placeholder_true_code = ('setNightVision(true)', 'setNightVision(true)')
    placeholder_false_code = ('setNightVision(false)', 'setNightVision(false)')
    placeholder_option1 = ('option1', 'option1')
    placeholder_default_int = ('100', '100')
    placeholder_default_float = ('1.0', '1.0')
    placeholder_min_int = ('1', '1')
    placeholder_min_float = ('0.5', '0.5')
    placeholder_max_int = ('100', '100')
    placeholder_max_float = ('2.0', '2.0')
    placeholder_step_int = ('1', '1')
    placeholder_step_float = ('0.1', '0.1')
    placeholder_code_tpl = ('<triggered_effect trigger xxxxxxxx value="{0}"/> {0} is a placeholder and must be filled in',
     '<triggered_effect trigger xxxxxxxx value=“{0}“/> {0}为占位符必须填写')
    placeholder_unnamed_config = ('Unnamed Config', '未命名配置')
    
    # 玩家模式
    player_mode = ('Player Mode', '玩家模式')

    preset = ('Player Preset', '玩家预设')
    save_as = ('Save As', '另存为')
    delete = ('Delete', '删除')
    default = ('Reset All To Default', '恢复所有到默认')
    use = ('Use', '使用')
    
    save_preset = ('Save Preset', '保存预设')
    delete_preset = ('Delete Preset', '删除预设')
    default_preset = ('Default Preset', '默认预设')
    apply_preset = ('Apply Preset', '应用预设')
    runtime_settings = ('Runtime Settings', '运行时设置')
    startup_apply_preset = ('Apply preset on startup', '启动时应用预设')
    preset_name = ('Preset Name', '预设名称')
    preset_saved = ('Preset saved successfully', '预设保存成功')
    preset_deleted = ('Preset deleted successfully', '预设删除成功')
    preset_applied = ('The current preset has been applied to final settings', '已把当前预设设置应用到最终设置')
    default_preset_loaded = ('Default values have been applied to final settings', '已把默认值应用到最终设置')
    flexmod_json_not_found = ('FlexMod.json not found', '未找到FlexMod.json文件')
    error_loading_settings = ('Error loading settings', '加载设置失败')
    please_set_mods_dir = ('Please set Mods directory', '请设置Mods目录')
    mods_dir_not_exists = ('Mods directory does not exist', 'Mods目录不存在')


def get_text(key: str, lang: int = 0) -> str:
    """
    获取指定语言的文本
    
    Args:
        key: 文本键名
        lang: 语言 (0=英文, 1=中文)
    
    Returns:
        对应语言的文本
    """
    if hasattr(Lang, key):
        text_tuple = getattr(Lang, key)
        if isinstance(text_tuple, tuple) and len(text_tuple) > lang:
            return text_tuple[lang]
        elif isinstance(text_tuple, tuple):
            return text_tuple[0]
        else:
            return str(text_tuple)
    return key


def get_lang() -> int:
    """获取当前语言设置"""
    import os
    import json
    
    config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('lang', 0)
        except:
            pass
    return 0


def set_lang(lang: int) -> None:
    """设置语言"""
    import os
    import json
    
    config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            config['lang'] = lang
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
        except:
            pass
