def create_route(routename):
    mutation = f'''
    mutation {{
        createRouteFromTemplate(input: {{
            label: "{routename}",
            active: true
        }}) {{
            route {{
                id
            }}
        }}
    }}
    '''
    return mutation


def update_route_source(routeid, sourceid, sourceid_num):
    mutation = f'''
    mutation{{
      updateRoute(input:{{
        id:"{routeid}",
        primarySourceId:"{sourceid}",
        sourceIds:["{sourceid_num}"]
      }}){{
        errorType{{
          code
          message
        }}
      }}
    }}
    '''
    return mutation


def update_route_destination(routeid, destinationid_num):
    mutation = f'''
    mutation {{
      updateRoute(input: {{
        id:"{routeid}",
        destinationIds: ["{destinationid_num}"]
      }}) {{
        errorType {{
          code
          message
        }}
      }}
    }}
    '''
    return mutation


def create_rtmp_destination(url, routename, networkInterfaceId):
    mutation = f'''

    mutation {{
      createRtmpDestination(input: {{
        url: "{url}",
        streamKey: "",
        active: true,
        label: "{routename}",
        networkInterfaceId: "{networkInterfaceId}"
      }}
    
      ) {{
        rtmpDestination {{
          id
        }}
        errorType {{
          code
          message
        }}
      }}
    }}
    '''
    return mutation


def create_srt_ipmx_source(routename, localPort, networkInterfaceId):
    mutation = f'''
    mutation {{
      createSrtIpmxSource(input: {{   
        callMode: LISTENER,
        discoveryTimeout: 3000,
        latency: 20,
        bondingMode: DISABLED,
        links: [
          {{
            networkInterfaceId: "{networkInterfaceId}"
            # networkInterfaceId: "TmV0d29ya0ludGVyZmFjZTo0MmQ5Y2RlMS03NzE5LTRiY2ItYTQ5Yy1iMWViNDY4NWVmZDQ=",
            localPortMode: MANUAL,
            localPort: {localPort},
            remoteHost: "1.1.1.1",
            remotePort: 10000,
            priority: 10,
            reset: false
          }}
        ],
        active: true,
        label: "{routename}"
      
      }}) {{
        srtIpmxSource {{
          id
        }}
        errorType {{
          code
          message
        }}
      }}
    }}
    '''
    return mutation


def create_ipmx_destination(routename, videoIpAddress, audioIpAddress, networkInterfaceId):
    mutation = f'''
    mutation {{
      createIpmxDestination(input: {{
            videoNetworkInterfaceId: "{networkInterfaceId}",
            videoIpAddress: "{videoIpAddress}",
            videoPort: 5004,
            audioNetworkInterfaceId: "{networkInterfaceId}",
            audioIpAddress: "{audioIpAddress}",
            audioPort: 5004,
            active: true,
            label: "{routename}"
      }}) {{
        ipmxDestination {{
          id
        }}
        errorType {{
          code
          message
        }}
      }}
    }}
    '''
    return mutation


def create_rtsp_source(routename, address, port, path):
    mutation = f'''
    mutation {{
      createRtspSource(input: {{
        address: "{address}",
        port: {port},
        userName: "",
        passphrase: "",
        path: "{path}",
        active: true,
        label: "{routename}"
      }}) {{
        rtspSource {{
          id
        }}
        errorType {{
          code
          message
        }}
      }}
    }}
    '''
    return mutation
