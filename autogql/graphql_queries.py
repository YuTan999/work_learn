def get_device_info(sid):
    query = f"""
    query{{
      common{{
        getNmos(sid:"{sid}"){{
          nmos{{
            nmosName
          }}
        }}   
      }}
      system{{
        getImageUpdate(sid:"{sid}"){{
          imageUpdate{{
            updateCurrentVersion
          }}
        }}
      }}
    }}
   """
    return query


def get_network_info(sid):
    query = f"""
        query{{
          csp{{
            getNetworkAdapter(sid:"{sid}"){{
              networkAdapter{{
                networkadapterName
                networkadapterAlias
                networkadapterIpAddress
                networkadapterMacAddress
              }}
            }}
          }}
        }}
   """
    return query


def get_input_selection(sid):
    query = f"""
        query{{
          transceiver{{
            getInputSelection(sid:"{sid}"){{
              inputSelection{{
               inst
               inputselectionPrimary
               inputselectionAudioSource
              }}
            }}
          }}
        }}
   """
    return query


def get_decode_ipmx(sid):
    query = f"""
        query{{
          transceiver{{
            getIpmxInput(sid:"{sid}"){{
              ipmxInput  {{
               inst
               ipmxinputConnector
              }}
            }}
          }}
        }}
   """
    return query


def get_video_and_audio_input_format(sid):
    query = f"""
    query{{
      transceiver{{
        getVideoDecode(sid:"{sid}"){{
          videoDecode{{
            videodecodeStatus
            videodecodeNativeFormat
          }}
        }}
        getSt2110InputAudio(sid:"{sid}"){{
          St2110InputAudio{{
            st2110inputaudioMode
            st2110inputaudioSampleRate
            st2110inputaudioChannelNumber
          }}
        }}
      }}
    }}
   """
    return query


def get_hdmi_output(sid):
    query = f"""
        query{{
          transceiver{{
            getHdmiOutput(sid:"{sid}"){{
              hdmiOutput {{
               hdmioutputHdcpType
               hdmioutputAudioSourceType
               hdmioutputAudioChannelNumber
               hdmioutputAudioChannelSamples
               hdmioutputConnectionStatus
               hdmioutputVideoFormat
              }}
            }}
          }}
        }}
   """
    return query


def get_fan_speed(sid):
    query = f"""
    query{{
     system{{
       getFanSpeed(sid:"{sid}"){{
         fanSpeed{{
           fanspeedStatus
           fanspeedControlMode
         }}
       }}
     }}
   }}
   """
    return query
