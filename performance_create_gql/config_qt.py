import sys
import time
import urllib3
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QFormLayout, QLineEdit, QPushButton, QProgressBar,
                             QMessageBox, QLabel, QTextEdit, QTabWidget, QGroupBox,
                             QHBoxLayout, QSplitter)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont, QPalette

# 导入你的业务逻辑模块
from mutation import login, get_network_interfaces
from graphql_request import send_graphql_mutation, get_cookie_from_login, get_interface_id
from createRoute import RouteManager

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ConfigThread(QThread):
    """配置线程，防止界面卡死"""
    progress_signal = pyqtSignal(int)
    message_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(dict)
    error_signal = pyqtSignal(str)

    def __init__(self, config_params):
        super().__init__()
        self.config_params = config_params

    # def run(self):
    #     try:
    #         self.message_signal.emit("开始登录系统...")
    #         self.progress_signal.emit(10)
    #
    #         # 调用配置函数
    #         results = create_seven_routes(**self.config_params)
    #
    #         self.message_signal.emit("配置完成！")
    #         self.progress_signal.emit(100)
    #         self.finished_signal.emit(results)
    #
    #     except Exception as e:
    #         self.error_signal.emit(f"配置失败: {str(e)}")

    def run(self):
        try:
            self.message_signal.emit("开始登录系统...")
            self.progress_signal.emit(10)

            # 调用配置函数，传递日志回调
            results = create_seven_routes(
                **self.config_params,
                log_callback=self.message_signal.emit,  # 传递日志回调
                error_callback=self.error_signal.emit  # 传递错误回调
            )

            self.message_signal.emit("配置完成！")
            self.progress_signal.emit(100)
            self.finished_signal.emit(results)

        except Exception as e:
            self.error_signal.emit(f"配置失败: {str(e)}")


# def create_seven_routes(graphql_url, eth1, ipmx_address_video, ipmx_address_audio,
#                         mpeg_address, mpeg_port, bolin_address, minray_address, avonic_address):
#
#     """创建七条预定义链路 - 重构后的版本"""
#
#     # 登录获取cookie
#     cookie = get_cookie_from_login(graphql_url, login())
#     if not cookie:
#         raise Exception("登录失败，无法获取cookie")
#
#     # 获取网络接口ID
#     interface_name_0 = "eth0"
#     interface_name_1 = "eth1"
#     networkInterfaceId = get_interface_id(get_network_interfaces(), graphql_url, interface_name_0, cookie)
#     networkInterfaceId_1 = get_interface_id(get_network_interfaces(), graphql_url, interface_name_1, cookie)
#     if not networkInterfaceId:
#         raise Exception("无法获取网络接口ID")
#
#     # 创建路由管理器实例
#     route_manager = RouteManager(graphql_url, cookie, networkInterfaceId)

def create_seven_routes(graphql_url, eth1, ipmx_address_video, ipmx_address_audio,
                        mpeg_address, mpeg_port, bolin_address, minray_address, avonic_address,
                        log_callback=None, error_callback=None):  # 添加回调参数

    # 登录获取cookie
    cookie = get_cookie_from_login(graphql_url, login())
    if not cookie:
        error_msg = "登录失败，无法获取cookie"
        if error_callback:
            error_callback(error_msg)
        raise Exception(error_msg)

    # 获取网络接口ID
    interface_name_0 = "eth0"
    interface_name_1 = "eth1"
    networkInterfaceId = get_interface_id(get_network_interfaces(), graphql_url, interface_name_0, cookie)
    networkInterfaceId_1 = get_interface_id(get_network_interfaces(), graphql_url, interface_name_1, cookie)
    if not networkInterfaceId:
        error_msg = "无法获取网络接口ID"
        if error_callback:
            error_callback(error_msg)
        raise Exception(error_msg)

    # 创建路由管理器实例，传递回调函数
    route_manager = RouteManager(graphql_url, cookie, networkInterfaceId,
                                 log_callback=log_callback,
                                 error_callback=error_callback)

    # 定义链路的配置
    routes_config = [
        # 1. 1ts: mpeg输入, ipmx输出
        {
            "name": "flow1_mpegts",
            "route_name": "f1_ts_ipmx",
            "source_type": "mpeg",
            "source_params": {
                "address": mpeg_address,
                "port": mpeg_port,
            },
            "destination_type": "ipmx",
            "destination_params": {
                "videoIpAddress": "235.155.0.11",
                "audioIpAddress": "235.155.1.11",
            }
        },
        # 2. 2ndi_in: ndi输入, ipmx输出
        {
            "name": "flow2_7_ndi",
            "route_name": "f2_7_ndi_ipmx",
            "source_type": None,
            "source_params": {},
            "destination_type": "ipmx",
            "destination_params": {
                "videoIpAddress": "235.155.0.12",
                "audioIpAddress": "235.155.1.12",
            }
        },
        # 3. 3rtsp1: rtsp输入, ipmx输出
        {
            "name": "flow3_rtsp1",
            "route_name": "f3_rtsp1_bolin",
            "source_type": "rtsp",
            "source_params": {
                "address": bolin_address,
                "port": "554",
                "path": "media/video0"
            },
            "destination_type": "ipmx",
            "destination_params": {
                "videoIpAddress": "235.155.0.13",
                "audioIpAddress": "235.155.1.13",
            }
        },
        # 4. 4rtsp2: rtsp输入, ipmx输出
        {
            "name": "flow3_rtsp2",
            "route_name": "f3_rtsp2_avonic",
            "source_type": "rtsp",
            "source_params": {
                "address": avonic_address,
                "port": "554",
                "path": "live/av0"
            },
            "destination_type": "ipmx",
            "destination_params": {
                "videoIpAddress": "235.155.0.14",
                "audioIpAddress": "235.155.1.14",
            }
        },
        # 5. 5rtsp3: rtsp输入, ipmx输出
        {
            "name": "flow3_rtsp3",
            "route_name": "f3_rtsp3_minray",
            "source_type": "rtsp",
            "source_params": {
                "address": minray_address,
                "port": "554",
                "path": "live/av0"
            },
            "destination_type": "ipmx",
            "destination_params": {
                "videoIpAddress": "235.155.0.15",
                "audioIpAddress": "235.155.1.15",
            }
        },
        # 6. 6ipmx: ipmx输入, srt ts输出
        {
            "name": "flow4_ipmx",
            "route_name": "f4_ipmx_srt",
            "source_type": "ipmx",
            "source_params": {
                "videoIpAddress": ipmx_address_video,
                "audioIpAddress": ipmx_address_audio
            },
            "destination_type": "srt",
            "destination_params": {
                "remotehost": eth1,
                "remoteport": "46666",
            }
        },
        # 7. 7ipmx: ipmx输入, srt ipmx输出
        {
            "name": "flow5_ipmx",
            "route_name": "f5_ipmx_srt_ipmx",
            "source_type": "ipmx",
            "source_params": {
                "videoIpAddress": ipmx_address_video,
                "audioIpAddress": ipmx_address_audio
            },
            "destination_type": "srt_ipmx",
            "destination_params": {
                "remotehost": eth1,
                "remoteport": "42222",
                "networkInterfaceId": networkInterfaceId
            }
        },
        # 8. 8ndi_out: ipmx输入, ndi输出
        {
            "name": "ndi_out",
            "route_name": "ndi_out",
            "source_type": "ipmx",
            "source_params": {
                "videoIpAddress": ipmx_address_video,
                "audioIpAddress": ipmx_address_audio
            },
            "destination_type": "ndi",
            "destination_params": {
                "ndiName": "test"
            }
        },
        # 9. 9srt_ts: srt_ts输入, ipmx输出
        # {
        #     "name": "flow6_srt",
        #     "route_name": "f4_6_srt",
        #     "source_type": "srt",
        #     "source_params": {
        #         "localport": "46666",
        #         "networkInterfaceId": networkInterfaceId_1
        #     },
        #     "destination_type": "ipmx",
        #     "destination_params": {
        #         "videoIpAddress": "235.155.0.16",
        #         "audioIpAddress": "235.155.1.16",
        #     }
        # },
        # 10. 10srt: srt输入, ipmx输出
        # {
        #     "name": "flow6_srt_ipmx",
        #     "route_name": "f5_6_srt_ipmx",
        #     "source_type": "srt_ipmx",
        #     "source_params": {
        #         "localport": "42222",
        #         "networkInterfaceId": networkInterfaceId_1
        #     },
        #     "destination_type": "ipmx",
        #     "destination_params": {
        #         "videoIpAddress": "235.155.0.17",
        #         "audioIpAddress": "235.155.1.17",
        #     }
        # }
    ]

    results = {}

    # for i, config in enumerate(routes_config):
    #     print(f"\n=== 创建链路: {config['name']} ===")

    for i, config in enumerate(routes_config):
        if log_callback:
            log_callback(f"\n=== 创建链路: {config['name']} ===")

        # 1. 创建路由
        # route_dict = route_manager.createRoute([config['route_name']])
        # if not route_dict:
        #     print(f"Failed to create route for {config['name']}")
        #     results[config['name']] = {"status": "failed", "reason": "route_creation_failed"}
        #     continue

        route_dict = route_manager.createRoute([config['route_name']])
        if not route_dict:
            error_msg = f"Failed to create route for {config['name']}"
            if error_callback:
                error_callback(error_msg)
            results[config['name']] = {"status": "failed", "reason": "route_creation_failed"}
            continue

        route_id = route_dict[config['route_name']]
        time.sleep(1)

        # 2. 创建源
        source_dict = {}
        if config['source_type'] == "mpeg":
            source_dict = route_manager.createMpegIpSource(
                [config['route_name']],
                [config['source_params']['address']],
                [config['source_params']['port']],
            )
        elif config['source_type'] == "rtsp":
            source_dict = route_manager.createRtspSource(
                [config['route_name']],
                [config['source_params']['path']],
                config['source_params']['address'],
                config['source_params']['port']
            )
        elif config['source_type'] == "ipmx":
            source_dict = route_manager.createIpmxSource(
                [config['route_name']],
                config['source_params']['videoIpAddress'],
                config['source_params']['audioIpAddress'],
            )
        elif config['source_type'] == "srt":
            source_dict = route_manager.createSrtSource(
                [config['route_name']],
                [config['source_params']['localport']],
                config['source_params']['networkInterfaceId'],
            )
        elif config['source_type'] == "srt_ipmx":
            source_dict = route_manager.createSrtIpmxSource(
                [config['route_name']],
                [config['source_params']['localport']],
                config['source_params']['networkInterfaceId'],
            )

        time.sleep(1)

        # 3. 创建目的地
        destination_dict = {}
        if config['destination_type'] == "ipmx":
            destination_dict = route_manager.createIpmxDestination(
                [config['route_name']],
                [config['destination_params']['videoIpAddress']],
                [config['destination_params']['audioIpAddress']],
            )
        elif config['destination_type'] == "srt":
            destination_dict = route_manager.createSrtDestination(
                [config['route_name']],
                [config['destination_params']['remoteport']],
                config['destination_params']['remotehost'],
            )
        elif config['destination_type'] == "srt_ipmx":
            destination_dict = route_manager.createSrtIpmxDestination(
                [config['route_name']],
                [config['destination_params']['remoteport']],
                config['destination_params']['remotehost'],
            )
        elif config['destination_type'] == "ndi":
            destination_dict = route_manager.createNdiDestination(
                [config['route_name']],
                [config['destination_params']['ndiName']],
            )

        time.sleep(1)

        # 4. 更新路由配置
        if source_dict:
            route_manager.updateRouteSource(route_dict, source_dict)
            time.sleep(1)

        if destination_dict:
            route_manager.updateRouteDestination(route_dict, destination_dict)
            time.sleep(1)

        results[config['name']] = {
            "status": "success",
            "route_id": route_id,
            "source_id": source_dict.get(config['route_name']) if source_dict else None,
            "destination_id": destination_dict.get(config['route_name']) if destination_dict else None
        }

    return results


class ConfigWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.config_thread = None

    def init_ui(self):
        self.setWindowTitle("SCG路由初始化工具")
        self.setGeometry(100, 100, 900, 600)

        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QVBoxLayout(central_widget)

        # 创建标签页
        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)

        # 配置标签页
        self.setup_config_tab(tab_widget)

        # 日志标签页
        self.setup_log_tab(tab_widget)

        # 进度条
        self.setup_progress_section(main_layout)

    def setup_config_tab(self, tab_widget):
        """配置参数标签页"""
        config_tab = QWidget()
        layout = QVBoxLayout(config_tab)

        # 参数分组
        server_group = self.create_server_group()
        network_group = self.create_network_group()
        camera_group = self.create_camera_group()

        layout.addWidget(server_group)
        layout.addWidget(network_group)
        layout.addWidget(camera_group)
        layout.addStretch() # 添加弹性空间

        # 按钮
        button_layout = QHBoxLayout()
        self.start_btn = QPushButton("开始配置")
        self.reset_btn = QPushButton("重置默认值")

        self.start_btn.clicked.connect(self.start_configuration)
        self.reset_btn.clicked.connect(self.reset_defaults)

        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.reset_btn)
        layout.addLayout(button_layout)

        tab_widget.addTab(config_tab, "配置参数")

    def create_server_group(self):
        """服务器参数组"""
        group = QGroupBox("服务器配置")
        layout = QFormLayout(group)

        self.fields = {}
        fields_config = [
            ('graphql_url', 'GraphQL URL', 'https://192.168.11.9/graphql'),
            ('eth1', 'ETH1地址', '192.168.11.192'),
        ]

        for field_id, label, default in fields_config:
            edit = QLineEdit()
            edit.setText(default)
            layout.addRow(f"{label}:", edit)
            self.fields[field_id] = edit

        return group

    def create_network_group(self):
        """网络参数组"""
        group = QGroupBox("IPMX配置")
        layout = QFormLayout(group)

        network_fields = [
            ('ipmx_video', 'IPMX视频地址', '239.155.0.55'),
            ('ipmx_audio', 'IPMX音频地址', '239.155.1.55'),
            ('mpeg_address', 'MPEG地址', '231.111.1.1'),
            ('mpeg_port', 'MPEG端口', '10011'),
        ]

        for field_id, label, default in network_fields:
            edit = QLineEdit()
            edit.setText(default)
            layout.addRow(f"{label}:", edit)
            self.fields[field_id] = edit

        return group

    def create_camera_group(self):
        """摄像头参数组"""
        group = QGroupBox("摄像头地址")
        layout = QFormLayout(group)

        camera_fields = [
            ('bolin_address', 'Bolin摄像头', '192.168.11.211'),
            ('minray_address', 'Minray摄像头', '192.168.11.212'),
            ('avonic_address', 'Avonic摄像头', '192.168.11.213'),
        ]

        for field_id, label, default in camera_fields:
            edit = QLineEdit()
            edit.setText(default)
            layout.addRow(f"{label}:", edit)
            self.fields[field_id] = edit

        return group

    def setup_log_tab(self, tab_widget):
        """日志显示标签页"""
        log_tab = QWidget()
        layout = QVBoxLayout(log_tab)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 9))

        layout.addWidget(QLabel("配置日志:"))
        layout.addWidget(self.log_text)

        tab_widget.addTab(log_tab, "运行日志")

    def setup_progress_section(self, main_layout):
        """进度条部分"""
        progress_layout = QHBoxLayout()

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)

        self.status_label = QLabel("就绪")

        progress_layout.addWidget(QLabel("进度:"))
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.status_label)

        main_layout.addLayout(progress_layout)

    def log_message(self, message):
        """添加日志消息"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")

    def start_configuration(self):
        """开始配置"""
        # 收集参数
        config_params = {
            'graphql_url': self.fields['graphql_url'].text(),
            'eth1': self.fields['eth1'].text(),
            'ipmx_address_video': self.fields['ipmx_video'].text(),
            'ipmx_address_audio': self.fields['ipmx_audio'].text(),
            'mpeg_address': self.fields['mpeg_address'].text(),
            'mpeg_port': self.fields['mpeg_port'].text(),
            'bolin_address': self.fields['bolin_address'].text(),
            'minray_address': self.fields['minray_address'].text(),
            'avonic_address': self.fields['avonic_address'].text(),
        }

        # 验证必填字段
        for key, value in config_params.items():
            if not value.strip():
                QMessageBox.warning(self, "输入错误", f"请填写所有必填字段")
                return

        # 禁用界面
        self.set_ui_enabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.log_text.clear()

        # 启动配置线程
        self.config_thread = ConfigThread(config_params)
        self.config_thread.progress_signal.connect(self.progress_bar.setValue)
        self.config_thread.message_signal.connect(self.log_message)
        self.config_thread.message_signal.connect(self.status_label.setText)
        self.config_thread.finished_signal.connect(self.on_config_finished)
        self.config_thread.error_signal.connect(self.on_config_error)
        self.config_thread.start()

        self.log_message("开始配置路由...")

    def set_ui_enabled(self, enabled):
        """启用/禁用界面控件"""
        for field in self.fields.values():
            field.setEnabled(enabled)
        self.start_btn.setEnabled(enabled)
        self.reset_btn.setEnabled(enabled)

    def on_config_finished(self, results):
        """配置完成回调"""
        self.set_ui_enabled(True)
        self.progress_bar.setVisible(False)
        self.status_label.setText("配置完成")

        # 统计结果
        success_count = sum(1 for r in results.values() if r["status"] == "success")
        total_count = len(results)

        self.log_message(f"配置完成！成功: {success_count}/{total_count}")

        # 显示详细结果
        result_text = "\n".join([
            f"{name}: {result['status']}"
            for name, result in results.items()
        ])

        QMessageBox.information(self, "完成",
                                f"配置完成！\n成功: {success_count}/{total_count}\n\n详细结果请看日志标签页")

    def on_config_error(self, error_message):
        """配置错误回调"""
        self.set_ui_enabled(True)
        self.progress_bar.setVisible(False)
        self.status_label.setText("配置失败")

        self.log_message(f"错误: {error_message}")
        QMessageBox.critical(self, "错误", error_message)

    def reset_defaults(self):
        """重置默认值"""
        defaults = {
            'graphql_url': 'https://192.168.11.9/graphql',
            'eth1': '192.168.11.192',
            'ipmx_video': '239.155.0.55',
            'ipmx_audio': '239.155.1.55',
            'mpeg_address': '231.111.1.1',
            'mpeg_port': '10011',
            'bolin_address': '192.168.11.211',
            'minray_address': '192.168.11.212',
            'avonic_address': '192.168.11.213',
        }

        for field_id, value in defaults.items():
            self.fields[field_id].setText(value)


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # 现代风格

    window = ConfigWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
