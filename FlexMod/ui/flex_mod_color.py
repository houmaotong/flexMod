# 软件的颜色方案


import ssl


BG_100 = "#050505"    # 最底层背景 - 近乎纯黑
BG_200 = "#0d0d0d"    # 页面主背景 - 深炭黑
BG_300 = "#171717"    # 卡片/区块背景 - 暗灰黑
BG_400 = "#232323"    # 控件背景 - 工业灰黑
BG_500 = "#2e2e2e"    # 悬停/激活背景 - 浅灰黑

# 文本色 - 低对比度废土风格
TEXT_100 = "#f0f0f0"  # 高亮文本 - 米白（非纯白）
TEXT_200 = "#d0d0d0"  # 主要文本 - 浅灰
TEXT_300 = "#888888"  # 次要文本 - 中灰
TEXT_400 = "#555555"  # 提示/禁用文本 - 深灰

# 核心血腥红（末日丧尸主题）- 低饱和暗猩红
PRIMARY_500 = "#900000"    # 核心血腥红 - 暗红（主色）
PRIMARY_600 = "#780000"    # 血腥红hover态 - 更深的红
PRIMARY_700 = "#600000"    # 血腥红激活态 - 暗褐红
PRIMARY_LIGHT = "rgba(144, 0, 0, 0.15)"  # 血腥红浅背景 - 低透明度
PRIMARY_HOVER = "rgba(144, 0, 0, 0.25)"  # 血腥红hover背景 - 中透明度

# 辅助血腥色（丧尸主题）
RED_400 = "#802020"    # 暗红棕 - 伤口色
RED_500 = "#701010"    # 深褐红 - 干血色

# 功能色 - 废土风格低饱和
SUCCESS_500 = "#3a6e3a"  # 暗军绿 - 废土安全色
SUCCESS_600 = "#2d582d"
WARNING_500 = "#806020"  # 暗土黄 - 废土警告色
WARNING_600 = "#685018"
DANGER_500 = "#801010"   # 深血红 - 危险色
DANGER_600 = "#680808"
INFO_500 = "#204060"     # 暗钢蓝 - 废土信息色
INFO_600 = "#183048"

# 边框与阴影 - 粗糙废土质感
BORDER_100 = "#1a1a1a"   # 暗边框
BORDER_200 = "#282828"   # 中边框
BORDER_300 = "#353535"   # 亮边框
SHADOW_SM = "0 2px 8px rgba(0, 0, 0, 0.4)"    # 更深阴影
SHADOW_MD = "0 4px 12px rgba(0, 0, 0, 0.5)"   # 中深阴影
SHADOW_LG = "0 8px 24px rgba(0, 0, 0, 0.6)"   # 极深阴影
SHADOW_FOCUS = f"0 0 0 3px {PRIMARY_LIGHT}"   # 血腥红聚焦阴影

# 过渡动画 - 更慢更沉的质感
TRANSITION_FAST = "0.2s ease"
TRANSITION_NORMAL = "0.3s ease"
TRANSITION_SLOW = "0.4s ease"


#-------------------------------StyleSheet----------------------------------

def _NO_BBBO(bg_none: int, bg_transparent: int, border_none: int, outline_none: int) -> str:
    """
    1=添加该属性，0=不添加
        background: none ; 
        background-color: transparent; 
        border: none;
        outline: none;
    :return: 拼接后的样式字符串
    """
    style_parts = []
    if bg_none:
        style_parts.append("background: none")
    if bg_transparent:
        style_parts.append("background-color: transparent")
    if border_none:
        style_parts.append("border: none")
    if outline_none:
        style_parts.append("outline: none")
    return "; ".join(style_parts) + (";" if style_parts else "")

# 主窗口
SS_window = f"""
        QWidget {{background: {BG_200};}}
        QLabel {{_NO_BBBO(1, 1, 1, 1)}}
        """

# 导航栏
SS_nav_grad_fill = f"""
                QWidget {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {BG_300}, stop:1 {BG_400});
                    height: 60px;
                    }}"""

# 导航栏按钮
_nav_btn_shape = "width:100px; height: 20px; padding: 5px 5px; border-radius: 15px; "
_nav_btn_text_size = f" font-size: 12px; font-weight: bold;"
_nav_btn_normal_text = f"color: {TEXT_400};{_nav_btn_text_size }"
_nav_btn_active_text = f"color: {TEXT_100};{_nav_btn_text_size }"

SS_nav_btn_normal = f"""
                QPushButton {{
                    {_nav_btn_shape}
                    {_nav_btn_normal_text}
                    {_NO_BBBO(1, 1, 1, 1)}
                }}
                QPushButton:hover {{
                    border: 1px solid {PRIMARY_500}; 
                    {_nav_btn_active_text}}}
                QPushButton:pressed {{{_NO_BBBO(1, 1, 1, 1)}}}"""

SS_nav_btn_active = f"""
                QPushButton {{ 
                    {_nav_btn_shape}
                    {_nav_btn_active_text}
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {PRIMARY_500}, stop:1 {PRIMARY_600});
                    {_NO_BBBO(0, 0, 1, 1)}
                }}
                QPushButton:hover {{
                    border: 1px solid {TEXT_400};
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 rgba(180, 50, 50, 0.9),
                                stop:0.4 {PRIMARY_500},stop:0.6 {PRIMARY_600},stop:1 rgba(60, 0, 0, 0.9)); }}   
                QPushButton:pressed {{{_NO_BBBO(0, 0, 1, 1)}}} """

#主窗口-页面容器
SS_page_stack = f"""QStackedWidget {{_NO_BBBO(1, 1, 1, 1)}}"""


SS_home_splitter = f"""
        QSplitter {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1 ,stop:0 {BG_300},stop:1 {BG_400});  
            border-radius: 8px;
            border: 1px solid {BORDER_100};
            padding: 20px;
        }}
        QSplitter:hover {{border: 1px solid {BORDER_200};}}
        QSplitter::handle {{
            background-color: {BORDER_100};
            width: 10px;
        }}
        QSplitter::handle:hover {{background-color: {BORDER_300};}}
        """

SS_home_splitter_left_widget = f"""QWidget {{ {_NO_BBBO(1, 1, 1, 1)}}}"""

SS_flexmod_list =f"""
            QListWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1 ,stop:0 {BG_400},stop:1 {BG_300});
                color: {TEXT_100};
                border-radius: 8px;
                padding: 10px;
                border: 1px solid {BORDER_200};
            }}

            QListWidget::item {{
                padding: 10px;
                border-radius: 4px;
                margin: 5px 0;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1 ,stop:0 {BG_400},stop:1 {BG_500});
                border: 1px solid {BORDER_200};
                {_NO_BBBO(0, 0, 0, 1)}
                
            }}
            QListWidget::item:hover {{
                border: 1px solid {PRIMARY_500}; 
            }}
            QListWidget::item:selected {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {PRIMARY_500}, stop:1 {PRIMARY_600}); 
            
            }}"""

SS_btn = f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1 ,stop:0 {BG_400},stop:1 {BG_500});
                border-radius: 4px;
                padding: 5px 5px;
                font-size: 12px;
                font-weight: bold;
                color: {TEXT_100};
                border: 1px solid {BORDER_200};
                {_NO_BBBO(0, 0, 0, 1)} }}
            QPushButton:hover {{
                border: 1px solid {PRIMARY_500}; 
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {PRIMARY_500}, stop:1 {PRIMARY_600}); 
            }}
            """

_preset_font_size ="font-size: 12px;"
SS_preset_label = f""" QLabel {{
                {_preset_font_size }
                color: {TEXT_300};
                {_NO_BBBO(1, 1, 1, 1)}
            }}"""
SS_preset_combo =f"""
        QComboBox {{
            width: 150px;
            padding: 5px 5px;
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1 ,stop:0 {BG_400},stop:1 {BG_500});
            border: 1px solid {BORDER_200};
            border-radius: 4px;
            color: {TEXT_200};
            {_preset_font_size }
        }}
        QComboBox:hover {{border: 1px solid {PRIMARY_500};  }}
        QComboBox:focus {{border: 1px solid {PRIMARY_500};  }}
        QComboBox QAbstractItemView {{ 
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1 ,stop:0 {BG_400},stop:1 {BG_300});
            padding: 5px;
        }}"""
    

SS_preset_btn = f""" QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1 ,stop:0 {BG_400},stop:1 {BG_500});
                border-radius: 4px;
                padding: 5px 5px;
                {_preset_font_size }
                color: {TEXT_200};
                border: 1px solid {BORDER_200};
                {_NO_BBBO(0, 0, 0, 1)} }}
            QPushButton:hover {{border: 1px solid {PRIMARY_500};  }}
            QPushButton:pressed {{background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {PRIMARY_500}, stop:1 {PRIMARY_600}); }}
            """
SS_player_scroll_area = f"""
        QWidget {{
            {_NO_BBBO(1, 1, 1, 1)}
        }}
        QScrollArea {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1 ,stop:0 {BG_200},stop:1 {BG_300});
            border-radius: 8px;
            border: 1px solid {BORDER_200};
            padding: 20px;
        }}
        QScrollBar:vertical {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1 ,stop:0 {BG_400},stop:1 {BG_300});
            border-radius: 4px;
            width: 8px;
            margin: 20px 0;
        }}
        QScrollBar::handle:vertical {{
            background-color: {BORDER_100};
            min-height: 20px;
            border-radius: 4px;
        }}
        QScrollBar::handle:vertical:hover {{
            background-color: {BORDER_300};
        }}"""

SS_player_SettingCard_big=f"""
                QWidget {{
                    {_NO_BBBO(0, 0, 0, 1)}
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1 ,stop:0 {BG_300},stop:1 {BG_400}); 
                    border: 2px solid {BORDER_200};  
                    border-radius: 8px;
                }}
                QLabel {{
                    {_NO_BBBO(1, 1, 1, 1)}
                }}
                """

SS_player_SettingCard_header=f""" 
                    QWidget {{
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0 ,stop:0 {BG_100},stop:1 {PRIMARY_500});
                        width: 100%;
                        height: 60px;
                        padding: 10px 20px;
                        font-size: 16px;
                        font-weight: bold;
                        color: {TEXT_100};
                        border: 2px solid {BORDER_200};
                    }}
                    QLabel {{{_NO_BBBO(1, 1, 1, 1)}font-size: 15px;font-weight: bold;color}}
                    QLabel:hover {{{_NO_BBBO(1, 1, 1, 1)}}}
                    """
SS_player_SettingCard_GroupDesc=f""" QLabel {{
                        {_NO_BBBO(1, 1, 1, 1)}
                        font-size: 11px
                        ;color: {TEXT_400};
                    }}
"""

SS_player_SettingCard_content=f""" QWidget {{{_NO_BBBO(1, 1, 1, 1)}}}"""
                    
SS_player_SettingItemCard  =f""" QWidget {{
                                background: qlineargradient(x1:0, y1:0, x2:1, y2:1 ,stop:0 {BG_300},stop:1 {BG_200});
                                border: 1px solid {BORDER_200};
                                padding: 0px;
                                border-radius: 8px; }}
                                QWidget:hover {{
                                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1 ,stop:0 {BG_200},stop:1 {BG_300});
                                    border: 1px solid {BORDER_300};
                                }}
                            QLabel {{{_NO_BBBO(1, 1, 1, 1)}}}
                            QLabel:hover {{{_NO_BBBO(1, 1, 1, 1)}}}
                            """   

SS_player_SettingItemCard_Title= f""" 
                            QLabel {{
                            {_NO_BBBO(1, 1, 1, 1)};
                            font-size: 13px; font-weight: bold; color: {TEXT_200};
                            }}"""

SS_player_SettingItemCard_Desc = f""" QLabel {{{_NO_BBBO(1, 1, 1, 1)}
                                font-size: 11px;color: {TEXT_400};
                            }}"""
SS_player_SettingItemCard_dropdown_widget = SS_preset_combo


SS_player_SettingItemCard_slider_widget = f"""
        QSlider {{
            background-color: transparent;
            min-width: 80px;
            height: 20px;
        }}
        QSlider::groove:horizontal {{
  
        }}
        QSlider::handle:horizontal {{
            background: {PRIMARY_500}; 
            width: 8px;
            height: 18px;
            border-radius: 4px;
            margin: 0;
        }}
        QSlider::handle:horizontal:hover {{
  
        }}   
        QSlider::sub-page:horizontal {{
            background: {PRIMARY_500};  
            height: 8px;
            border-radius: 4px;
            margin: 5px 0;
            
        }}
    """
SS_player_SettingItemCard_slider_widget_value_label = f"""
        QLabel {{
            {_NO_BBBO(1, 1, 1, 1)}
            font-size: 11px;
            color: {TEXT_400};
        }}
"""

