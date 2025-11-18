from mutation import create_route, create_srt_ipmx_source, update_route_source, update_route_destination, \
    create_rtmp_destination, create_ipmx_destination, create_rtsp_source, create_mpegip_source, create_srt_source, \
    create_srt_ipmx_destination, create_ipmx_source, create_srt_destination, create_ndi_destination
from graphql_request import send_graphql_mutation


class RouteManager:
    def __init__(self, graphql_url, cookie, networkInterfaceId, log_callback=None, error_callback=None):
        self.graphql_url = graphql_url
        self.cookie = cookie
        self.networkInterfaceId = networkInterfaceId
        self.log_callback = log_callback
        self.error_callback = error_callback

    def _log(self, message):
        if self.log_callback:
            self.log_callback(message)
        else:
            print(f"[INFO] {message}")

    def _log_error(self, message):
        if self.error_callback:
            self.error_callback(message)
        else:
            print(f"[ERROR] {message}")

    def createRoute(self, routeNames):
        route_dict = {}
        for routename in routeNames:
            self._log(f"创建路由: {routename}")
            result = send_graphql_mutation(create_route(routename), self.graphql_url, self.cookie, "RouteFromTemplate")
            if result["success"]:
                route_id = result['data']['createRouteFromTemplate']['route']['id']
                route_dict[routename] = route_id
                self.save_to_txt(route_dict, "createRoute.txt")
                self._log(f"路由创建成功: {routename}")
            else:
                self._log_error(f"路由创建失败: {routename} - {result['error']}")
                route_dict[routename] = None
        return route_dict

    def createSrtSource(self, routeNames, localPorts, networkInterfaceId=None):
        source_dict = {}
        interface_id = networkInterfaceId or self.networkInterfaceId
        for routename, localport in zip(routeNames, localPorts):
            self._log(f"创建SRT源: {routename}")
            result = send_graphql_mutation(create_srt_source(routename, localport, interface_id),
                                           self.graphql_url, self.cookie, "SrtSource")
            if result["success"]:
                source_id = result['data']['createSrtSource']['srtSource']['id']
                source_dict[routename] = source_id
                self.save_to_txt(source_dict, "createSrtSource.txt")
                self._log(f"SRT源创建成功: {routename}")
            else:
                self._log_error(f"SRT源创建失败: {routename} - {result['error']}")
                source_dict[routename] = None
        return source_dict

    # def createIpmxSource(self, routeNames, inputvideoadds, inputaudioadds):
    #     source_dict = {}
    #     # for routename in routeNames:
    #     for routename, inputvideoadd, inputaudioadd in zip(routeNames, inputvideoadds, inputaudioadds):
    #         response = send_graphql_mutation(
    #             create_ipmx_source(routename, inputvideoadd, inputaudioadd, self.networkInterfaceId),
    #             self.graphql_url, self.cookie)
    #         if response:
    #             print(f"createIpmxSource{routename}:\n{response}")
    #             source_id = response['data']['createIpmxSource']['ipmxSource']['id']
    #             source_dict[routename] = source_id
    #             self.save_to_txt(source_dict, "createIpmxSource.txt")
    #     return source_dict

    def createIpmxSource(self, routeNames, inputvideoadd, inputaudioadd):
        source_dict = {}
        for routename in routeNames:
        # for routename, inputvideoadd, inputaudioadd in zip(routeNames, inputvideoadds, inputaudioadds):
            self._log(f"创建IPMX源: {routename}")
            result = send_graphql_mutation(
                create_ipmx_source(routename, inputvideoadd, inputaudioadd, self.networkInterfaceId),
                self.graphql_url, self.cookie, "IpmxSource")
            if result["success"]:
                source_id = result['data']['createIpmxSource']['ipmxSource']['id']
                source_dict[routename] = source_id
                self.save_to_txt(source_dict, "createIpmxSource.txt")
                self._log(f"IPMX源创建成功: {routename}")
            else:
                self._log_error(f"IPMX源创建失败: {routename} - {result['error']}")
                source_dict[routename] = None
        return source_dict

    def createSrtIpmxSource(self, routeNames, localPorts, networkInterfaceId=None):
        source_dict = {}
        interface_id = networkInterfaceId or self.networkInterfaceId
        for routename, localport in zip(routeNames, localPorts):
            self._log(f"创建SRT IPMX源: {routename}")
            result = send_graphql_mutation(create_srt_ipmx_source(routename, localport, interface_id),
                                           self.graphql_url, self.cookie, "SrtIpmxSource")
            if result["success"]:
                source_id = result['data']['createSrtIpmxSource']['srtIpmxSource']['id']
                source_dict[routename] = source_id
                self.save_to_txt(source_dict, "createSrtIpmxSource.txt")
                self._log(f"SRT IPMX源创建成功: {routename}")
            else:
                self._log_error(f"SRT IPMX源创建失败: {routename} - {result['error']}")
                source_dict[routename] = None
        return source_dict

    def createRtspSource(self, routeNames, rtsp_paths, rtsp_url, rtsp_port):
        source_dict = {}
        # for routename in routeNames:
        for routename, rtsp_path in zip(routeNames, rtsp_paths):
            self._log(f"创建RTSP源: {routename}")
            result = send_graphql_mutation(create_rtsp_source(routename, rtsp_url, rtsp_port, rtsp_path),
                                           self.graphql_url, self.cookie, "RtspSource")
            if result["success"]:
                source_id = result['data']['createRtspSource']['rtspSource']['id']
                source_dict[routename] = source_id
                self.save_to_txt(source_dict, "createRtspSource.txt")
                self._log(f"RTSP源创建成功: {routename}")
            else:
                self._log_error(f"RTSP源创建失败: {routename} - {result['error']}")
                source_dict[routename] = None
        return source_dict

    def createMpegIpSource(self, routeNames, mpegip_add, mpegip_port):
        source_dict = {}
        for routename, address, port in zip(routeNames, mpegip_add, mpegip_port):
            self._log(f"创建MPEG IP源: {routename}")
            result = send_graphql_mutation(
                create_mpegip_source(routename, address, port, self.networkInterfaceId),
                self.graphql_url, self.cookie, "MpegIpSource")
            if result["success"]:
                source_id = result['data']['createMpegIpSource']['mpegIpSource']['id']
                source_dict[routename] = source_id
                self.save_to_txt(source_dict, "createMpegIpSource.txt")
                self._log(f"MPEG IP源创建成功: {routename}")
            else:
                self._log_error(f"MPEG IP源创建失败: {routename} - {result['error']}")
                source_dict[routename] = None
        return source_dict

    def updateRouteSource(self, route_dict, source_dict):
        for route_id, source_id, source_id_num in zip(route_dict.values(), source_dict.values(), source_dict.values()):
            self._log(f"更新路由源: {route_id}")
            result = send_graphql_mutation(update_route_source(route_id, source_id, source_id_num),
                                           self.graphql_url, self.cookie, )
            if result["success"]:
                self._log(f"路由源更新成功: {source_id}")
            else:
                self._log_error(f"路由源更新失败: {source_id} - {result['error']}")

    def updateRouteDestination(self, route_dict, destination_dict):
        for route_id, destination_id_num in zip(route_dict.values(), destination_dict.values()):
            self._log(f"更新路由目的地: {route_id}")
            result = send_graphql_mutation(update_route_destination(route_id, destination_id_num),
                                           self.graphql_url, self.cookie, )
            if result["success"]:
                self._log(f"路由目的地更新成功: {destination_id_num}")
            else:
                self._log_error(f"路由目的地更新失败: {destination_id_num} - {result['error']}")

    def createIpmxDestination(self, routeNames, videoAdds, audioAdds):
        destination_dict = {}
        for routename, videoadd, audioadd in zip(routeNames, videoAdds, audioAdds):
            self._log(f"创建IPMX目的地: {routename}")
            result = send_graphql_mutation(
                create_ipmx_destination(routename, videoadd, audioadd, self.networkInterfaceId),
                self.graphql_url, self.cookie, "IpmxDestination")
            if result["success"]:
                destination_id = result['data']['createIpmxDestination']['ipmxDestination']['id']
                destination_dict[routename] = destination_id
                self.save_to_txt(destination_dict, "createIpmxDestination.txt")
                self._log(f"IPMX目的地创建成功: {routename}")
            else:
                self._log_error(f"IPMX目的地创建失败: {routename} - {result['error']}")
                destination_dict[routename] = None
        return destination_dict

    def createSrtDestination(self, routeNames, localPorts, remotehost):
        destination_dict = {}
        for routename, remoteport in zip(routeNames, localPorts):
            self._log(f"创建SRT目的地: {routename}")
            result = send_graphql_mutation(
                create_srt_destination(routename, self.networkInterfaceId, remotehost, remoteport),
                self.graphql_url, self.cookie, "SrtDestination")
            if result["success"]:
                destination_id = result['data']['createSrtDestination']['srtDestination']['id']
                destination_dict[routename] = destination_id
                self.save_to_txt(destination_dict, "createSrtDestination.txt")
                self._log(f"SRT目的地创建成功: {routename}")
            else:
                self._log_error(f"SRT目的地创建失败: {routename} - {result['error']}")
                destination_dict[routename] = None
        return destination_dict

    def createSrtIpmxDestination(self, routeNames, localPorts, remotehost):
        destination_dict = {}
        for routename, remoteport in zip(routeNames, localPorts):
            self._log(f"创建SRT IPMX目的地: {routename}")
            result = send_graphql_mutation(
                create_srt_ipmx_destination(routename, self.networkInterfaceId, remotehost, remoteport),
                self.graphql_url, self.cookie, "SrtIpmxDestination")
            if result["success"]:
                destination_id = result['data']['createSrtIpmxDestination']['srtIpmxDestination']['id']
                destination_dict[routename] = destination_id
                self.save_to_txt(destination_dict, "createSrtIpmxDestination.txt")
                self._log(f"SRT IPMX目的地创建成功: {routename}")
            else:
                self._log_error(f"SRT IPMX目的地创建失败: {routename} - {result['error']}")
                destination_dict[routename] = None
        return destination_dict

    def createRtmpDestination(self, routeNames, rtmp_urls):
        destination_dict = {}
        for routename, rtmpurl in zip(routeNames, rtmp_urls):
            self._log(f"创建RTMP目的地: {routename}")
            result = send_graphql_mutation(create_rtmp_destination(rtmpurl, routename, self.networkInterfaceId),
                                           self.graphql_url, self.cookie, "RtmpDestination")
            if result["success"]:
                destination_id = result['data']['createRtmpDestination']['rtmpDestination']['id']
                destination_dict[routename] = destination_id
                self.save_to_txt(destination_dict, "createRtmpDestination.txt")
                self._log(f"RTMP目的地创建成功: {routename}")
            else:
                self._log_error(f"RTMP目的地创建失败: {routename} - {result['error']}")
                destination_dict[routename] = None
        return destination_dict

    # def createNdiDestination(self, routeNames, ndiname):
    #     destination_dict = {}
    #     for routename in routeNames:
    #         response = send_graphql_mutation(create_ndi_destination(routename, ndiname),
    #                                          self.graphql_url,
    #                                          self.cookie)
    #         if response:
    #             print(f"createNdiDestination{routename}:\n{response}")
    #             destination_id = response['data']['createNdiDestination']['ndiDestination']['id']
    #             destination_dict[routename] = destination_id
    #             self.save_to_txt(destination_dict, "createNdiDestination.txt")
    #         else:
    #             print(f"Failed to create ndi destination: {routename}")
    #     return destination_dict

    def createNdiDestination(self, routeNames, ndiname):
        destination_dict = {}
        for routename in routeNames:
            self._log(f"创建NDI目的地: {routename}")
            result = send_graphql_mutation(create_ndi_destination(routename, ndiname),
                                           self.graphql_url, self.cookie, "NdiDestination")

            if result["success"]:
                destination_id = result["data"]["createNdiDestination"]["ndiDestination"]["id"]
                destination_dict[routename] = destination_id
                self.save_to_txt(destination_dict, "createNdiDestination.txt")
                self._log(f"NDI目的地创建成功: {routename}")
            else:
                self._log_error(f"NDI目的地创建失败: {routename} - {result['error']}")
                destination_dict[routename] = None

        return destination_dict

    def save_to_txt(self, dict, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            for routename, route_id in dict.items():
                file.write(f"{routename}: {route_id}\n")
