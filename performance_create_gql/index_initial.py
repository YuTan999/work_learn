import time
import urllib3
from mutation import login, get_network_interfaces
from graphql_request import send_graphql_mutation, get_cookie_from_login, get_interface_id
from createRoute import RouteManager

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ndi输入、mpegts输出自己建
# 跑完脚本后，srt输出的码率要手动更新
# 手动配置参数：eth0和eth1地址、编码的h26x地址、ts推流地址、三个摄像头地址
graphql_url = "https://192.168.11.191/graphql"
eth1 = "192.168.11.192"
ipmx_address_video = "235.155.0.14"
ipmx_address_audio = "235.155.1.14"
mpeg_address = "231.111.1.1"
mpeg_port = "10011"
bolin_address = "192.168.11.211"
minray_address = "192.168.11.212"
avonic_address = "192.168.11.213"

# 登录获取cookie和网络接口
cookie = get_cookie_from_login(graphql_url, login())
if not cookie:
    print("Failed to get cookie")
    exit(1)
# 获取网络接口ID
interface_name_0 = "eth0"
interface_name_1 = "eth1"
networkInterfaceId = get_interface_id(get_network_interfaces(), graphql_url, interface_name_0, cookie)
networkInterfaceId_1 = get_interface_id(get_network_interfaces(), graphql_url, interface_name_1, cookie)
if not networkInterfaceId:
    print("Failed to get networkInterfaceId")
    exit(1)

# 创建路由管理器实例
route_manager = RouteManager(graphql_url, cookie, networkInterfaceId)


def create_seven_routes():
    """创建七条预定义链路"""

    # 定义七条链路的配置
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
        # 2. 2ndi_in: ndi输入, ipmx输出 (NDI输入暂不实现)
        {
            "name": "flow2_7_ndi",
            "route_name": "f2_7_ndi_ipmx",
            "source_type": None,  # 空表示不创建源
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
        # 6. 6ipmx: ipmx输入, srt ts输出 (ts+srt+ipmx)
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
        # 7. 7ipmx: ipmx输入, srt ipmx输出 (ts+srt+ipmx)
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
        {
            "name": "flow6_srt",
            "route_name": "f4_6_srt",
            "source_type": "srt",
            "source_params": {
                "localport": "46666",
                "networkInterfaceId": networkInterfaceId_1
            },
            "destination_type": "ipmx",
            "destination_params": {
                "videoIpAddress": "235.155.0.16",
                "audioIpAddress": "235.155.1.16",
            }
        },
        # 10. 10srt: srt输入, ipmx输出
        {
            "name": "flow6_srt_ipmx",
            "route_name": "f5_6_srt_ipmx",
            "source_type": "srt_ipmx",
            "source_params": {
                "localport": "42222",
                "networkInterfaceId": networkInterfaceId_1

            },
            "destination_type": "ipmx",
            "destination_params": {
                "videoIpAddress": "235.155.0.17",
                "audioIpAddress": "235.155.1.17",
            }
        }

    ]

    results = {}

    for config in routes_config:
        print(f"\n=== 创建链路: {config['name']} ===")

        # 1. 创建路由
        route_dict = route_manager.createRoute([config['route_name']])
        if not route_dict:
            print(f"Failed to create route for {config['name']}")
            results[config['name']] = {"status": "failed", "reason": "route_creation_failed"}
            continue

        route_id = route_dict[config['route_name']]
        time.sleep(1)

        # 2. 创建源（如果配置了源类型）
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
        # 可以添加其他源类型...

        time.sleep(1)

        # 3. 创建目的地（如果配置了目的地类型）
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
        elif config['destination_type'] == "rtmp":
            destination_dict = route_manager.createRtmpDestination(
                [config['route_name']],
                [config['destination_params']['url']],

            )
        elif config['destination_type'] == "ndi":
            destination_dict = route_manager.createNdiDestination(
                [config['route_name']],
                [config['destination_params']['ndiName']],
            )
        # 可以添加其他目的地类型...

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


def main():
    """主函数"""
    print("开始创建七条预定义链路...")
    results = create_seven_routes()

    print("\n=== 创建结果汇总 ===")
    for route_name, result in results.items():
        status = result["status"]
        print(f"{route_name}: {status}")
        if status == "success":
            print(f"  路由ID: {result['route_id']}")
            if result['source_id']:
                print(f"  源ID: {result['source_id']}")
            if result['destination_id']:
                print(f"  目的地ID: {result['destination_id']}")
        else:
            print(f"  失败原因: {result.get('reason', '未知错误')}")

    # 保存详细结果到文件
    with open("seven_routes_results.txt", "w") as f:
        f.write("七条链路创建结果:\n\n")
        for route_name, result in results.items():
            f.write(f"{route_name}:\n")
            f.write(f"  状态: {result['status']}\n")
            if result['status'] == "success":
                f.write(f"  路由ID: {result['route_id']}\n")
                if result['source_id']:
                    f.write(f"  源ID: {result['source_id']}\n")
                if result['destination_id']:
                    f.write(f"  目的地ID: {result['destination_id']}\n")
            else:
                f.write(f"  失败原因: {result.get('reason', '未知错误')}\n")
            f.write("\n")

    print("\n详细结果已保存到 seven_routes_results.txt")


if __name__ == "__main__":
    main()
