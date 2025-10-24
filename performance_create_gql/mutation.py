def login():
    mutation = f'''
        mutation {{
          login(
            name: "admin"
            password: "proav101"
            remember: false
          ) {{
            cookie {{
              key
              value
            }}
          }}
        }}
    '''
    return mutation


def route_groupings():
    query = f'''
    query {{
      routeGroupings(
         orderBy: {{
            label: ASC
      }})  {{
        nodes {{
          id
          label
        }}
      }}
    }}
    '''
    return query


def get_network_interfaces():
    query = f'''
    query {{
      device {{
        id
        label
        hostname
        networkDefaultGateway {{
          id
          label
        }}
        networkInterfaces {{
          totalCount
          edges {{
            node {{
              id
              name
              label
              gateway
              igmp
              addresses {{
                label
                mode
                address
                prefixLength
              }}
              status
              ethernet {{
                mac
                duplex
                speed
              }}
            }}
          }}
        }}
      }}
    }}
    '''
    return query


def update_route(routeid, bitrate):
    mutation = f'''
    mutation{{
      updateRoute(input:{{
        id:"{routeid}",
        tsOutputBitrate:{bitrate}
      }}){{
        errorType{{
          message
        }}
      }}
    }}
    '''
    return mutation


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


def create_srt_source(routename, localPort, networkInterfaceId):
    mutation = f'''
    mutation {{
      createSrtSource(input: {{
    callMode: LISTENER,
    discoveryTimeout: 3000,
    latency: 1500,
    streamId: "",
    rtpTunnelMode: DISABLED,
    bondingMode: DISABLED,
    links: [
      {{
        networkInterfaceId: "{networkInterfaceId}",
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
        srtSource {{
          id
        }}
        errorType{{
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


def create_mpegip_source(routename, address, port, networkInterfaceId):
    mutation = f'''
    mutation {{
      createMpegIpSource(input: {{
        streamMode: MULTICAST,
        destinationAddress: "{address}",
        destinationPort: {port},
        igmpInput: {{
          mode: EXCLUDE,
          addresses: []
        }},
        fecInput: {{
          state: DISABLED
        }},
        active: true,
        label: "{routename}",
        networkInterfaceId: "{networkInterfaceId}"
      }}) {{
        mpegIpSource {{
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


def create_ipmx_source(routename, videoIpAddress, audioIpAddress, networkInterfaceId):
    mutation = f'''
    mutation {{
        createIpmxSource(input: {{
          videoNetworkInterfaceId: "{networkInterfaceId}",
          videoStreamMode: MULTICAST,
          videoIpAddress: "{videoIpAddress}",
          videoPort: 5004,
          audioNetworkInterfaceId: "{networkInterfaceId}",
          audioStreamMode: MULTICAST,
          audioIpAddress: "{audioIpAddress}",
          audioPort: 5004,
          selectedIpmxSource: null,
          active: true,
          label: "{routename}"
        }}) {{
            ipmxSource {{
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


def create_srt_destination(routename, networkInterfaceId, remotehost, remoteport):
    mutation = f'''
    mutation {{
      createSrtDestination(input: {{
        active: true,
        bandwidthOverhead: 25,
        bondingMode: DISABLED,
        callMode: CALLER,
        discoveryTimeout: 3000,
        encryptionMode: DISABLED,
        fecCols: 5,
        fecMode: DISABLED,
        fecRows: 5,
        label: "{routename}",
        latency: 1500,
        links: [
          {{
            localPort: 40000,
            localPortMode: AUTO,
            networkInterfaceId: "{networkInterfaceId}",
            priority: 10,
            remoteHost: "{remotehost}",
            remotePort: {remoteport},
            reset: false
          }}
        ],
        streamId: "",
        timeToLive: 64,
        tsPackets: 7,
        tsPacketsMode:MANUAL,        
        typeOfService: 0
      }}) {{
        srtDestination {{
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


def create_srt_ipmx_destination(routename, networkInterfaceId, remotehost, remoteport):
    mutation = f'''
    mutation {{
      createSrtIpmxDestination(input: {{
        callMode: CALLER,
        discoveryTimeout: 3000,
        latency: 125,
        bandwidthOverhead: 25,
        timeToLive: 64,
        typeOfService: 0,
        encryptionMode: DISABLED,
        fecMode: DISABLED,
        fecCols: 5,
        fecRows: 5,
        bondingMode: DISABLED,
        links: [
          {{
            networkInterfaceId: "{networkInterfaceId}",
            localPortMode: AUTO,
            localPort: 40000,
            remoteHost: "{remotehost}",
            remotePort: {remoteport},
            priority: 10,
            reset: false
          }}
        ],
        active: true,
        label: "{routename}"
      }}) {{
        srtIpmxDestination {{
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


def create_ndi_destination(routename, ndiname):
    mutation = f'''
    mutation {{
      createNdiDestination(input: {{   
          label: "{routename}",
          active: true,
          name: "{ndiname}",
          group: "public",
          enableVideo: true,
          enableAudio: true
      }}) {{
        ndiDestination {{
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
