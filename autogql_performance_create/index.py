import time
import urllib3
from mutation import create_route, create_srt_ipmx_source, update_route_source, update_route_destination, \
    create_rtmp_destination, create_ipmx_destination, create_rtsp_source
from graphql_request import send_graphql_mutation

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 创建多通道一进一出脚本，srt输入、rtmp输出、ipmx输出
# 以下参数都要改:graphql_url,localports(SRT),networkInterfaceId,start,end
# 还有request的cookie也要改
graphql_url = "https://10.200.1.192/graphql"
# networkInterfaceId = "TmV0d29ya0ludGVyZmFjZTpjMDM3NzliYi1iOGY1LTQyMGMtOWMzNS04OGQ1ZDhjZmE0MDI="
networkInterfaceId = "TmV0d29ya0ludGVyZmFjZTpjMDM3NzliYi1iOGY1LTQyMGMtOWMzNS04OGQ1ZDhjZmE0MDI="
rtsp_url = "10.200.0.206"
rtsp_port = "5540"
start = 80
end = 82
rtsp_paths = "live/av0"
localPorts = [f'400{i}' for i in range(start, end)]
routeNames = [f'srt{i}' for i in range(start, end)]
rtmp_urls = [f'rtmp://10.200.1.183:1935/o{i}' for i in range(start, end)]
videoAdds = [f'237.176.0.1{i}' for i in range(start, end)]
audioAdds = [f'237.176.1.1{i}' for i in range(start, end)]


def createRoute():
    route_dict = {}
    for routename in routeNames:
        print(routename)
        response = send_graphql_mutation(create_route(routename), graphql_url)
        if response and 'data' in response:
            print(f"createRoute{routename}:{routename}:{response}")
            route_id = response['data']['createRouteFromTemplate']['route']['id']
            route_dict[routename] = route_id
            save_to_txt(route_dict, "createRoute.txt")
        else:
            print(f"Failed to create route {routename}")
    return route_dict


def updateRouteSource(route_id, source_id, source_id_num):
    response = send_graphql_mutation(update_route_source(route_id, source_id, source_id_num), graphql_url)
    print(f"updateRouteSource{response}")


def updateRouteDestination(route_id, destination_id_num):
    response = send_graphql_mutation(update_route_destination(route_id, destination_id_num), graphql_url)
    print(f"updateRouteDestination{response}")


def createSrtIpmxSource():
    source_dict = {}
    for routename, localport in zip(routeNames, localPorts):
        response = send_graphql_mutation(create_srt_ipmx_source(routename, localport, networkInterfaceId), graphql_url)
        if response:
            print(f"createSrtIpmxSource{routename}:{response}")
            source_id = response['data']['createSrtIpmxSource']['srtIpmxSource']['id']
            source_dict[routename] = source_id
            save_to_txt(source_dict, "createSrtIpmxSource.txt")
        else:
            print(f"Failed to create srt source: {routename}")
    return source_dict


def createRtspSource():
    source_dict = {}
    # routename, address, path
    for routename in routeNames:
        response = send_graphql_mutation(create_rtsp_source(routename, rtsp_url, rtsp_port, rtsp_paths), graphql_url)
        if response:
            print(f"createRtspSource{routename}:{response}")
            source_id = response['data']['createRtspSource']['rtspSource']['id']
            source_dict[routename] = source_id
            save_to_txt(source_dict, "createRtspSource.txt")
        else:
            print(f"Failed to create rtsp source: {routename}")
    return source_dict


def createRtmpDestination():
    destination_dict = {}
    for routename, rtmpurl in zip(routeNames, rtmp_urls):
        response = send_graphql_mutation(create_rtmp_destination(rtmpurl, routename, networkInterfaceId), graphql_url)
        if response:
            print(f"createRtmpDestination{routename}:{response}")
            destination_id = response['data']['createRtmpDestination']['rtmpDestination']['id']
            destination_dict[routename] = destination_id
            save_to_txt(destination_dict, "createRtmpDestination.txt")
        else:
            print(f"Failed to create rtmp destination: {routename}")
    return destination_dict


def createIpmxDestination():
    destination_dict = {}
    for routename, videoadd, audioadd in zip(routeNames, videoAdds, audioAdds):
        response = send_graphql_mutation(create_ipmx_destination(routename, videoadd, audioadd, networkInterfaceId),
                                         graphql_url)
        if response:
            print(f"createIpmxDestination{routename}:{response}")
            destination_id = response['data']['createIpmxDestination']['ipmxDestination']['id']
            destination_dict[routename] = destination_id
            save_to_txt(destination_dict, "createIpmxDestination.txt")
        else:
            print(f"Failed to create ipmx destination: {routename}")
    return destination_dict


def save_to_txt(dict, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for routename, route_id in dict.items():
            file.write(f"{routename}: {route_id}\n")


def main():
    # 1. 创建route,并获取route_id
    route_dict = createRoute()
    time.sleep(1)
    # # 2. 创建rtmp destination
    # rtmp_destination_dict = createRtmpDestination()
    # time.sleep(1)
    # for route_id, destination_id in zip(route_dict.values(), rtmp_destination_dict.values()):
    #     updateRouteDestination(route_id, destination_id)
    # time.sleep(1)
    # 3. 创建ipmx destination
    ipmx_destination_dict = createIpmxDestination()
    time.sleep(1)
    for route_id, destination_id in zip(route_dict.values(), ipmx_destination_dict.values()):
        updateRouteDestination(route_id, destination_id)
    # # 4. 创建srt source
    # srt_source_dict = createSrtIpmxSource()
    # time.sleep(1)
    # for route_id, source_id in zip(route_dict.values(), srt_source_dict.values()):
    #     updateRouteSource(route_id, source_id, source_id)
    # time.sleep(1)
    # # 5. 创建rtsp source
    # rtsp_source_dict = createRtspSource()
    # time.sleep(1)
    # for route_id, source_id in zip(route_dict.values(), rtsp_source_dict.values()):
    #     updateRouteSource(route_id, source_id, source_id)
    print(route_dict)
    # print(rtmp_destination_dict)
    # print(srt_source_dict)
    # print(ipmx_destination_dict)


if __name__ == "__main__":
    main()
