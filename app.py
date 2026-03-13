"""
主应用入口
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER, LEFT, RIGHT
from toga.constants import Direction

from .views.main_view import MainView
from .views.test_view import TestView
from .views.result_view import ResultView
from .views.map_view import MapView
from .utils.device_info import DeviceInfoManager
from .utils.call_manager import CallManager
from .utils.location_manager import LocationManager
from .utils.sms_manager import SMSManager


class PhoneTesterApp(toga.App):
    """电话拨打测试应用主类"""
    
    def startup(self):
        """应用启动时调用"""
        # 初始化管理器
        self.device_manager = DeviceInfoManager(self)
        self.call_manager = CallManager(self)
        self.location_manager = LocationManager(self)
        self.sms_manager = SMSManager(self)
        
        # 存储测试结果
        self.test_results = []
        self.current_test = None
        
        # 创建主界面
        self.main_window = toga.MainWindow(title=self.formal_name)
        
        # 创建底部导航
        self._create_bottom_nav()
        
        # 创建内容容器
        self.content_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
        
        # 创建各个视图
        self.views = {
            'main': MainView(self),
            'test': TestView(self),
            'result': ResultView(self),
            'map': MapView(self),
        }
        
        # 组装主界面
        main_box = toga.Box(
            style=Pack(direction=COLUMN, flex=1),
            children=[self.content_box, self.nav_box]
        )
        
        self.main_window.content = main_box
        self.main_window.show()
        
        # 默认显示主界面
        self.show_view('main')
        
        # 请求必要权限
        self._request_permissions()
    
    def _create_bottom_nav(self):
        """创建底部导航栏"""
        nav_style = Pack(
            direction=ROW,
            height=56,
            background_color='#2196F3',
            alignment=CENTER,
            padding=(4, 0)
        )
        
        btn_style = Pack(
            flex=1,
            height=48,
            background_color='#2196F3',
            color='white',
            font_size=11,
            text_align=CENTER,
        )
        
        self.nav_box = toga.Box(style=nav_style)
        
        # 导航按钮
        nav_items = [
            ('🏠 首页', 'main'),
            ('📞 测试', 'test'),
            ('📊 结果', 'result'),
            ('🗺️ 地图', 'map'),
        ]
        
        self.nav_buttons = {}
        for label, view_name in nav_items:
            btn = toga.Button(
                label,
                style=btn_style,
                on_press=lambda w, name=view_name: self.show_view(name)
            )
            self.nav_buttons[view_name] = btn
            self.nav_box.add(btn)
    
    def show_view(self, view_name):
        """切换视图"""
        # 清空内容区域
        self.content_box.children.clear()
        
        # 添加新视图
        view = self.views[view_name]
        self.content_box.add(view.get_content())
        
        # 更新导航按钮状态
        for name, btn in self.nav_buttons.items():
            if name == view_name:
                btn.style.background_color = '#1976D2'  # 选中状态加深
            else:
                btn.style.background_color = '#2196F3'  # 默认状态
        
        # 触发视图刷新
        view.on_show()
    
    def _request_permissions(self):
        """请求必要的Android权限"""
        # BeeWare会在打包时自动处理权限声明
        # 这里可以添加运行时权限检查
        pass
    
    def show_info_dialog(self, title, message):
        """显示信息对话框"""
        self.main_window.info_dialog(title, message)
    
    def show_error_dialog(self, title, message):
        """显示错误对话框"""
        self.main_window.error_dialog(title, message)
    
    def show_confirm_dialog(self, title, message, on_confirm):
        """显示确认对话框"""
        def handle_confirm(confirmed):
            if confirmed:
                on_confirm()
        
        self.main_window.confirm_dialog(
            title, 
            message,
            on_result=handle_confirm
        )


def main():
    """应用入口"""
    return PhoneTesterApp()
