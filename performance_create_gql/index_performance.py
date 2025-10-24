import time
import urllib3
from mutation import login, get_network_interfaces
from graphql_request import get_cookie_from_login, get_interface_id
from createRoute import RouteManager

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 创建多通道一进一出脚本，srt输入、rtmp输出、ipmx输出
# 以下参数都要改:graphql_url,localports(SRT),networkInterfaceId,start,end
# 还有request的cookie也要改
start = 45
end = 46
remotehost = "192.168.11.191"
rtsp_url = "192.168.11.211"
rtsp_port = "554"
# rtsp_paths = "live/av0"
rtsp_paths = [f'live_{i}_1' for i in range(start, end)]
mpegip_add = [f'239.182.0.1{i}' for i in range(start, end)]
mpegip_port = [f'100{i}' for i in range(start, end)]
localPorts = [f'400{i}' for i in range(start, end)]
routeNames = [f'rtmp{i}' for i in range(start, end)]
rtmp_urls = [f'rtmp://10.200.1.154:1935/o{i}' for i in range(start, end)]
videoAdds1 = [f'232.177.0.1{i}' for i in range(start, end)]
audioAdds1 = [f'232.177.1.1{i}' for i in range(start, end)]
videoAdds = [f'232.174.0.1{i}' for i in range(start, end)]
audioAdds = [f'232.174.1.1{i}' for i in range(start, end)]
inputvideoadd = "239.4.11.55"
inputaudioadd = "239.5.11.55"

graphql_url = "https://192.168.11.191/graphql"
# graphql_url = "https://192.168.11.185/graphql"
# graphql_url = "https://192.168.11.190/graphql"
interface_name = "eth0"

cookie = get_cookie_from_login(graphql_url, login())
if not cookie:
    print("Failed to get cookie")
    exit(1)
networkInterfaceId = get_interface_id(get_network_interfaces(), graphql_url, interface_name, cookie)
if not networkInterfaceId:
    print("Failed to get networkInterfaceId")
    exit(1)

# 创建路由管理器实例
route_manager = RouteManager(graphql_url, cookie, networkInterfaceId)


def main():
    ## 1. 创建route,并获取route_id
    route_dict = route_manager.createRoute(routeNames)
    # time.sleep(1)
    ## 2. 创建Source
    # source_dict = route_manager.createSrtSource(routeNames, localPorts)
    # source_dict = route_manager.createIpmxSource(routeNames, inputvideoadd, inputaudioadd)
    # source_dict = route_manager.createSrtIpmxSource(routeNames, localPorts)
    # source_dict = route_manager.createRtspSource(routeNames, rtsp_paths, rtsp_url, rtsp_port)
    source_dict = route_manager.createMpegIpSource(routeNames, mpegip_add, mpegip_port)
    ## 3. 更新Source
    time.sleep(1)
    route_manager.updateRouteSource(route_dict, source_dict)
    ## 4. 创建Destination
    # destination_dict = route_manager.createIpmxDestination(routeNames, videoAdds, audioAdds)
    # destination_dict = route_manager.createSrtDestination(routeNames, localPorts, remotehost)
    # destination_dict = route_manager.createSrtIpmxDestination(routeNames, localPorts, remotehost)
    # destination_dict = route_manager.createRtmpDestination(routeNames, rtmp_urls)
    ## 5. 更新Destination
    time.sleep(1)
    # route_manager.updateRouteDestination(route_dict, destination_dict)

    # print(route_dict)
    # updateRouteSource({"aa":"Um91dGU6MTY1N2U4NTAtY2JjYi00YThiLWE3ZTctYmNmNjM0ZTlmMjEy"},{"aa": "UnRzcFNvdXJjZTpmYmI0NGUxNS0xNWU5LTRmY2QtOGMwMS1lYTAzNDRhZWE0MWU="})
    route_manager.updateRouteDestination({"aa": "Um91dGU6Y2M5YzJlNmQtZWJiYy00YTYwLTgwYmUtNDM4ZmExMjc5MWMw"}, {
        "aa": "SXBteERlc3RpbmF0aW9uOjVmZWI3ZjkyLWY2MDgtNGM4YS05ZTg1LWYxM2MxZjkwYWQ4MQ=="})


if __name__ == "__main__":
    main()

# def createRoute():
#     route_dict = {}
#     for routename in routeNames:
#         print(routename)
#         response = send_graphql_mutation(create_route(routename), graphql_url, cookie)
#         if response and 'data' in response:
#             print(f"createRoute{routename}:\n{response}")
#             route_id = response['data']['createRouteFromTemplate']['route']['id']
#             route_dict[routename] = route_id
#             save_to_txt(route_dict, "createRoute.txt")
#         else:
#             print(f"Failed to create route {routename}")
#     return route_dict
#
#
# def updateRouteSource(route_dict, source_dict):
#     for route_id, source_id, source_id_num in zip(route_dict.values(), source_dict.values(), source_dict.values()):
#         response = send_graphql_mutation(update_route_source(route_id, source_id, source_id_num), graphql_url, cookie)
#         print(f"updateRouteSource:{response}")
#
#
# def updateRouteDestination(route_dict, destination_dict):
#     for route_id, destination_id_num in zip(route_dict.values(), destination_dict.values()):
#         response = send_graphql_mutation(update_route_destination(route_id, destination_id_num), graphql_url, cookie)
#         print(f"updateRouteDestination:{response}")
#
#
# def createSrtIpmxSource():
#     source_dict = {}
#     for routename, localport in zip(routeNames, localPorts):
#         response = send_graphql_mutation(create_srt_ipmx_source(routename, localport, networkInterfaceId), graphql_url,
#                                          cookie)
#         if response:
#             print(f"createSrtIpmxSource{routename}:\n{response}")
#             source_id = response['data']['createSrtIpmxSource']['srtIpmxSource']['id']
#             source_dict[routename] = source_id
#             save_to_txt(source_dict, "createSrtIpmxSource.txt")
#         else:
#             print(f"Failed to create srt source: {routename}")
#     return source_dict
#
#
# def createSrtSource():
#     source_dict = {}
#     for routename, localport in zip(routeNames, localPorts):
#         response = send_graphql_mutation(create_srt_source(routename, localport, networkInterfaceId), graphql_url,
#                                          cookie)
#         if response:
#             print(f"createSrtSource{routename}:\n{response}")
#             source_id = response['data']['createSrtSource']['srtSource']['id']
#             source_dict[routename] = source_id
#             save_to_txt(source_dict, "createSrtSource.txt")
#         else:
#             print(f"Failed to create srt source: {routename}")
#     return source_dict
#
#
# def createRtspSource():
#     source_dict = {}
#     # for routename in routeNames:
#     for routename, rtsp_path in zip(routeNames, rtsp_paths):
#         response = send_graphql_mutation(create_rtsp_source(routename, rtsp_url, rtsp_port, rtsp_path), graphql_url,
#                                          cookie)
#         if response:
#             print(f"createRtspSource{routename}:\n{response}")
#             source_id = response['data']['createRtspSource']['rtspSource']['id']
#             source_dict[routename] = source_id
#             save_to_txt(source_dict, "createRtspSource.txt")
#         else:
#             print(f"Failed to create rtsp source: {routename}")
#     return source_dict
#
#
# def createMpegIpSource():
#     source_dict = {}
#     for routename, address, port in zip(routeNames, mpegip_add, mpegip_port):
#         response = send_graphql_mutation(
#             create_mpegip_source(routename, address, port, networkInterfaceId), graphql_url, cookie)
#         if response:
#             print(f"createMpegIpSource{routename}:\n{response}")
#             source_id = response['data']['createMpegIpSource']['mpegIpSource']['id']
#             source_dict[routename] = source_id
#             save_to_txt(source_dict, "createMpegIpSource.txt")
#         else:
#             print(f"Failed to create mpegip source: {routename}")
#     return source_dict
#
#
# def createIpmxSource():
#     source_dict = {}
#     for routename in routeNames:
#     # for routename, inputvideoadd, inputaudioadd in zip(routeNames, videoAdds, audioAdds):
#     # for routename, inputvideoadd, inputaudioadd in zip(routeNames, videoAdds1, audioAdds1):
#         response = send_graphql_mutation(
#             create_ipmx_source(routename, inputvideoadd, inputaudioadd, networkInterfaceId),
#             graphql_url, cookie)
#         if response:
#             print(f"createIpmxSource{routename}:\n{response}")
#             source_id = response['data']['createIpmxSource']['ipmxSource']['id']
#             source_dict[routename] = source_id
#             save_to_txt(source_dict, "createIpmxSource.txt")
#     return source_dict
#
#
# def createSrtIpmxDestination():
#     destination_dict = {}
#     for routename, remoteport in zip(routeNames, localPorts):
#         response = send_graphql_mutation(
#             create_srt_ipmx_destination(routename, networkInterfaceId, remotehost, remoteport), graphql_url,
#             cookie)
#         if response:
#             print(f"createSrtIpmxDestination{routename}:\n{response}")
#             destination_id = response['data']['createSrtIpmxDestination']['srtIpmxDestination']['id']
#             destination_dict[routename] = destination_id
#             save_to_txt(destination_dict, "createSrtIpmxDestination.txt")
#     return destination_dict
#
#
# def createSrtDestination():
#     destination_dict = {}
#     for routename, remoteport in zip(routeNames, localPorts):
#         response = send_graphql_mutation(create_srt_destination(routename, networkInterfaceId, remotehost, remoteport),
#                                          graphql_url, cookie)
#         if response:
#             print(f"createSrtDestination{routename}:\n{response}")
#             destination_id = response['data']['createSrtDestination']['srtDestination']['id']
#             destination_dict[routename] = destination_id
#             save_to_txt(destination_dict, "createSrtDestination.txt")
#     return destination_dict
#
#
# def createRtmpDestination():
#     destination_dict = {}
#     for routename, rtmpurl in zip(routeNames, rtmp_urls):
#         response = send_graphql_mutation(create_rtmp_destination(rtmpurl, routename, networkInterfaceId), graphql_url,
#                                          cookie)
#         if response:
#             print(f"createRtmpDestination{routename}:\n{response}")
#             destination_id = response['data']['createRtmpDestination']['rtmpDestination']['id']
#             destination_dict[routename] = destination_id
#             save_to_txt(destination_dict, "createRtmpDestination.txt")
#         else:
#             print(f"Failed to create rtmp destination: {routename}")
#     return destination_dict
#
#
# def createIpmxDestination():
#     destination_dict = {}
#     for routename, videoadd, audioadd in zip(routeNames, videoAdds1, audioAdds1):
#         response = send_graphql_mutation(create_ipmx_destination(routename, videoadd, audioadd, networkInterfaceId),
#                                          graphql_url, cookie)
#         if response:
#             print(f"createIpmxDestination{routename}:\n{response}")
#             destination_id = response['data']['createIpmxDestination']['ipmxDestination']['id']
#             destination_dict[routename] = destination_id
#             save_to_txt(destination_dict, "createIpmxDestination.txt")
#         else:
#             print(f"Failed to create ipmx destination: {routename}")
#     return destination_dict
#
#
# def save_to_txt(dict, filename):
#     with open(filename, 'w', encoding='utf-8') as file:
#         for routename, route_id in dict.items():
#             file.write(f"{routename}: {route_id}\n")
