from mutation import create_route, create_srt_ipmx_source, update_route_source, update_route_destination, \
    create_rtmp_destination, create_ipmx_destination, create_rtsp_source, create_mpegip_source, create_srt_source, \
    create_srt_ipmx_destination, create_ipmx_source, create_srt_destination, create_ndi_destination
from graphql_request import send_graphql_mutation


class RouteManager:
    def __init__(self, graphql_url, cookie, networkInterfaceId):
        self.graphql_url = graphql_url
        self.cookie = cookie
        self.networkInterfaceId = networkInterfaceId

    def createRoute(self, routeNames):
        route_dict = {}
        for routename in routeNames:
            print(routename)
            response = send_graphql_mutation(create_route(routename), self.graphql_url, self.cookie)
            if response and 'data' in response:
                print(f"createRoute{routename}:\n{response}")
                route_id = response['data']['createRouteFromTemplate']['route']['id']
                route_dict[routename] = route_id
                self.save_to_txt(route_dict, "createRoute.txt")
            else:
                print(f"Failed to create route {routename}")
        return route_dict

    def createSrtSource(self, routeNames, localPorts, networkInterfaceId=None):
        source_dict = {}
        interface_id = networkInterfaceId or self.networkInterfaceId
        for routename, localport in zip(routeNames, localPorts):
            response = send_graphql_mutation(create_srt_source(routename, localport, interface_id),
                                             self.graphql_url,
                                             self.cookie)
            if response:
                print(f"createSrtSource{routename}:\n{response}")
                source_id = response['data']['createSrtSource']['srtSource']['id']
                source_dict[routename] = source_id
                self.save_to_txt(source_dict, "createSrtSource.txt")
            else:
                print(f"Failed to create srt source: {routename}")
        return source_dict

    def createIpmxSource(self, routeNames, inputvideoadd, inputaudioadd):
        source_dict = {}
        for routename in routeNames:
            # for routename, inputvideoadd, inputaudioadd in zip(routeNames, videoAdds, audioAdds):
            # for routename, inputvideoadd, inputaudioadd in zip(routeNames, videoAdds1, audioAdds1):
            response = send_graphql_mutation(
                create_ipmx_source(routename, inputvideoadd, inputaudioadd, self.networkInterfaceId),
                self.graphql_url, self.cookie)
            if response:
                print(f"createIpmxSource{routename}:\n{response}")
                source_id = response['data']['createIpmxSource']['ipmxSource']['id']
                source_dict[routename] = source_id
                self.save_to_txt(source_dict, "createIpmxSource.txt")
        return source_dict

    def createSrtIpmxSource(self, routeNames, localPorts, networkInterfaceId=None):
        source_dict = {}
        interface_id = networkInterfaceId or self.networkInterfaceId
        for routename, localport in zip(routeNames, localPorts):
            response = send_graphql_mutation(create_srt_ipmx_source(routename, localport, interface_id),
                                             self.graphql_url,
                                             self.cookie)
            if response:
                print(f"createSrtIpmxSource{routename}:\n{response}")
                source_id = response['data']['createSrtIpmxSource']['srtIpmxSource']['id']
                source_dict[routename] = source_id
                self.save_to_txt(source_dict, "createSrtIpmxSource.txt")
            else:
                print(f"Failed to create srt source: {routename}")
        return source_dict

    def createRtspSource(self, routeNames, rtsp_paths, rtsp_url, rtsp_port):
        source_dict = {}
        # for routename in routeNames:
        for routename, rtsp_path in zip(routeNames, rtsp_paths):
            response = send_graphql_mutation(create_rtsp_source(routename, rtsp_url, rtsp_port, rtsp_path),
                                             self.graphql_url,
                                             self.cookie)
            if response:
                print(f"createRtspSource{routename}:\n{response}")
                source_id = response['data']['createRtspSource']['rtspSource']['id']
                source_dict[routename] = source_id
                self.save_to_txt(source_dict, "createRtspSource.txt")
            else:
                print(f"Failed to create rtsp source: {routename}")
        return source_dict

    def createMpegIpSource(self, routeNames, mpegip_add, mpegip_port):
        source_dict = {}
        for routename, address, port in zip(routeNames, mpegip_add, mpegip_port):
            response = send_graphql_mutation(
                create_mpegip_source(routename, address, port, self.networkInterfaceId), self.graphql_url, self.cookie)
            if response:
                print(f"createMpegIpSource{routename}:\n{response}")
                source_id = response['data']['createMpegIpSource']['mpegIpSource']['id']
                source_dict[routename] = source_id
                self.save_to_txt(source_dict, "createMpegIpSource.txt")
            else:
                print(f"Failed to create mpegip source: {routename}")
        return source_dict

    def updateRouteSource(self, route_dict, source_dict):
        for route_id, source_id, source_id_num in zip(route_dict.values(), source_dict.values(), source_dict.values()):
            response = send_graphql_mutation(update_route_source(route_id, source_id, source_id_num), self.graphql_url,
                                             self.cookie)
            print(f"updateRouteSource:{response}")

    def updateRouteDestination(self, route_dict, destination_dict):
        for route_id, destination_id_num in zip(route_dict.values(), destination_dict.values()):
            response = send_graphql_mutation(update_route_destination(route_id, destination_id_num), self.graphql_url,
                                             self.cookie)
            print(f"updateRouteDestination:{response}")

    def createIpmxDestination(self, routeNames, videoAdds, audioAdds):
        destination_dict = {}
        for routename, videoadd, audioadd in zip(routeNames, videoAdds, audioAdds):
            response = send_graphql_mutation(
                create_ipmx_destination(routename, videoadd, audioadd, self.networkInterfaceId),
                self.graphql_url, self.cookie)
            if response:
                print(f"createIpmxDestination{routename}:\n{response}")
                destination_id = response['data']['createIpmxDestination']['ipmxDestination']['id']
                destination_dict[routename] = destination_id
                self.save_to_txt(destination_dict, "createIpmxDestination.txt")
            else:
                print(f"Failed to create ipmx destination: {routename}")
        return destination_dict

    def createSrtDestination(self, routeNames, localPorts, remotehost):
        destination_dict = {}
        for routename, remoteport in zip(routeNames, localPorts):
            response = send_graphql_mutation(
                create_srt_destination(routename, self.networkInterfaceId, remotehost, remoteport),
                self.graphql_url, self.cookie)
            if response:
                print(f"createSrtDestination{routename}:\n{response}")
                destination_id = response['data']['createSrtDestination']['srtDestination']['id']
                destination_dict[routename] = destination_id
                self.save_to_txt(destination_dict, "createSrtDestination.txt")
        return destination_dict

    def createSrtIpmxDestination(self, routeNames, localPorts, remotehost):
        destination_dict = {}
        for routename, remoteport in zip(routeNames, localPorts):
            response = send_graphql_mutation(
                create_srt_ipmx_destination(routename, self.networkInterfaceId, remotehost, remoteport),
                self.graphql_url,
                self.cookie)
            if response:
                print(f"createSrtIpmxDestination{routename}:\n{response}")
                destination_id = response['data']['createSrtIpmxDestination']['srtIpmxDestination']['id']
                destination_dict[routename] = destination_id
                self.save_to_txt(destination_dict, "createSrtIpmxDestination.txt")
        return destination_dict

    def createRtmpDestination(self, routeNames, rtmp_urls):
        destination_dict = {}
        for routename, rtmpurl in zip(routeNames, rtmp_urls):
            response = send_graphql_mutation(create_rtmp_destination(rtmpurl, routename, self.networkInterfaceId),
                                             self.graphql_url,
                                             self.cookie)
            if response:
                print(f"createRtmpDestination{routename}:\n{response}")
                destination_id = response['data']['createRtmpDestination']['rtmpDestination']['id']
                destination_dict[routename] = destination_id
                self.save_to_txt(destination_dict, "createRtmpDestination.txt")
            else:
                print(f"Failed to create rtmp destination: {routename}")
        return destination_dict

    def createNdiDestination(self, routeNames, ndiname):
        destination_dict = {}
        for routename in routeNames:
            response = send_graphql_mutation(create_ndi_destination(routename, ndiname),
                                             self.graphql_url,
                                             self.cookie)
            if response:
                print(f"createNdiDestination{routename}:\n{response}")
                destination_id = response['data']['createNdiDestination']['ndiDestination']['id']
                destination_dict[routename] = destination_id
                self.save_to_txt(destination_dict, "createNdiDestination.txt")
            else:
                print(f"Failed to create ndi destination: {routename}")
        return destination_dict

    def save_to_txt(self, dict, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            for routename, route_id in dict.items():
                file.write(f"{routename}: {route_id}\n")
