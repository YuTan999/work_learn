import time
import urllib3
from mutation import create_route, create_srt_ipmx_source, update_route_source, update_route_destination, \
    create_rtmp_destination, create_ipmx_destination
from graphql_request import send_graphql_mutation

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 创建多通道一进一出脚本，srt输入、rtmp输出、ipmx输出
# 以下参数都要改:graphql_url,localports(SRT),networkInterfaceId,start,end
# 还有request的cookie也要改
graphql_url = "https://192.168.1.191/graphql"
# networkInterfaceId = "TmV0d29ya0ludGVyZmFjZTphZWFhOTBhNC01NzllLTQ3OTItOTY2OS1hYzQ2OTA5MjY3ZGE="
networkInterfaceId = "TmV0d29ya0ludGVyZmFjZTo0MmQ5Y2RlMS03NzE5LTRiY2ItYTQ5Yy1iMWViNDY4NWVmZDQ="
start = 11
end = 49
localports = [f'400{i}' for i in range(start, end)]
routenames = [f'route{i}' for i in range(start, end)]
rtmpurls = [f'rtmp://10.200.1.183:1935/o{i}' for i in range(start, end)]
videoadds = [f'237.177.0.1{i}' for i in range(start, end)]
audioadds = [f'237.177.1.1{i}' for i in range(start, end)]


def createRoute():
    route_dict = {}
    for routename in routenames:
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


def updateRouteSource(routeid, sourceid, sourceid_num):
    response = send_graphql_mutation(update_route_source(routeid, sourceid, sourceid_num), graphql_url)
    print(f"updateRouteSource{response}")


def updateRouteDestination(routeid, destinationid_num):
    response = send_graphql_mutation(update_route_destination(routeid, destinationid_num), graphql_url)
    print(f"updateRouteDestination{response}")


def createSrtIpmxSource():
    source_dict = {}
    for routename, localport in zip(routenames, localports):
        response = send_graphql_mutation(create_srt_ipmx_source(routename, localport, networkInterfaceId), graphql_url)
        if response:
            print(f"createSrtIpmxSource{routename}:{response}")
            sourceid = response['data']['createSrtIpmxSource']['srtIpmxSource']['id']
            source_dict[routename] = sourceid
            save_to_txt(source_dict, "createSrtIpmxSource.txt")
        else:
            print(f"Failed to create srt source: {routename}")
    return source_dict


def createRtmpDestination():
    destination_dict = {}
    for routename, rtmpurl in zip(routenames, rtmpurls):
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
    for routename, videoadd, audioadd in zip(routenames, videoadds, audioadds):
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
        for routename, routeid in dict.items():
            file.write(f"{routename}: {routeid}\n")


def main():
    # 1. 创建route,并获取routeid
    route_dict = createRoute()
    time.sleep(1)
    # 2. 创建srt source
    srt_source_dict = createSrtIpmxSource()
    time.sleep(1)
    for routeid, sourceid in zip(route_dict.values(), srt_source_dict.values()):
        updateRouteSource(routeid, sourceid, sourceid)
    time.sleep(1)
    # # 3. 创建rtmp destination
    # rtmp_destination_dict = createRtmpDestination()
    # time.sleep(1)
    # for routeid, destination_id in zip(route_dict.values(), rtmp_destination_dict.values()):
    #     updateRouteDestination(routeid, destination_id)
    # time.sleep(1)
    # 4. 创建ipmx destination
    ipmx_destination_dict = createIpmxDestination()
    time.sleep(1)
    for routeid, destination_id in zip(route_dict.values(), ipmx_destination_dict.values()):
        updateRouteDestination(routeid, destination_id)
    print(route_dict)
    # print(rtmp_destination_dict)
    print(srt_source_dict)
    print(ipmx_destination_dict)


if __name__ == "__main__":
    main()
