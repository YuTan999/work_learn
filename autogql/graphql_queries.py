import requests
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

# GET_VIDEO_AND_AUDIO_INPUT_FORMAT = gql`
#    query getVideoInputFormat($sid: String!) {
#       transceiver {
#          getVideoDecode(sid: $sid) {
#             videoDecode {
#                videodecodeStatus
#                videodecodeNativeFormat
#             }
#          }
#          getSt2110InputAudio(sid: $sid) {
#             St2110InputAudio {
#                st2110inputaudioMode
#                st2110inputaudioSampleRate
#                st2110inputaudioChannelNumber
#             }
#          }
#       }
#    }
# `;
#
# export const GET_HDMI_OUTPUT = gql`
#    query getHdmiOutputAudioVolume($sid: String!) {
#       transceiver {
#          getHdmiOutput(sid: $sid) {
#             hdmiOutput {
#                hdmioutputHdcpType
#                hdmioutputAudioSourceType
#                hdmioutputAudioChannelNumber
#                hdmioutputAudioChannelSamples
#                hdmioutputConnectionStatus
#                hdmioutputVideoFormat
#             }
#          }
#       }
#    }
# `;
#
#
# export const GET_USB_IP = gql`
#    query getUsbIp($sid: String!) {
#       transceiver {
#          getUsbIpServer(sid: $sid) {
#             usbIpServer {
#                inst
#                usbipserverEnable
#                usbipserverClientIpAddress
#                usbipserverConnectStatus
#             }
#          }
#       }
#    }
# `;
#
#
# export const GET_DECODE_IPMX = gql`
#    query getDecodeIpmx($sid: String!) {
#       transceiver {
#          getIpmxInput(sid: $sid) {
#             ipmxInput {
#                inst
#                ipmxinputConnector
#             }
#          }
#       }
#    }
# `;


