from graphql_queries import get_hdmi_output, get_video_and_audio_input_format, get_device_info, get_decode_ipmx
from graphql_mutations import update_fan_speed, get_sid
from graphql_requests import send_graphql_query, send_graphql_mutation

graphql_url = "http://10.200.8.52/graphql"
def fanSpeedInput(mode, speed):
    fanspeedinput = f'{{fanspeedControlMode:FAN_SPEED_CONTROL_MODE_{mode},fanspeedPercentage:{speed}}}'
    return fanspeedinput

gets = get_sid()
data = send_graphql_mutation(get_sid(), graphql_url)
Sid = data['data']['login']['sid']
# query = update_fan_speed(Sid)
# print(query)
# result = send_graphql_query(query, graphql_url)
print(update_fan_speed(Sid, fanSpeedInput('MANUAL', '100')))
send_graphql_mutation(update_fan_speed(Sid, fanSpeedInput('MANUAL', '100')), graphql_url)


# if result:
#     print(result)
    # print(result['data']['transceiver']['St2110InputAudio'][0]['st2110inputaudioMode'])
    # print(result['data']['transceiver']['St2110InputAudio'][0]['st2110inputaudioSampleRate'])
    # print(result['data']['transceiver']['getIpmxInput']['ipmxInput'][0]['ipmxinputConnector'])
    # print(result['data']['transceiver']['getIpmxInput']['ipmxInput'][1]['ipmxinputConnector'])

# fanspeedinput_test = f'{{fanspeedControlMode:FAN_SPEED_CONTROL_MODE_{mode},fanspeedPercentage:{speed}}}'
#
# fstest = fanspeedinput_test(mode='AUTO', speed=100)
# print(fstest)


# #
# # const[getInputFormat] = useLazyQuery(GET_VIDEO_AND_AUDIO_INPUT_FORMAT, {
# #     ...
# # option,
# # onCompleted: (data) = > {
# #     const
# # videoDecode = data?.transceiver?.getVideoDecode?.videoDecode[0];
# # const
# # St2110InputAudio = data?.transceiver?.getSt2110InputAudio?.St2110InputAudio[0];
# # const[isValid, msg] = checkVideoAndAudioInput(videoDecode, St2110InputAudio);
# # if (!isValid)
# # {
# #     genLogs('FAILED', [msg]);
# # } else {
# #     genLogs('', [msg]);
# # handleNext();
# # }
# # }
# # });
# # const[getHdmiOutput] = useLazyQuery(GET_HDMI_OUTPUT, {
# #     ...
# # option,
# # onCompleted: async (data) = > {
# #     const
# # hdmiOutput = data?.transceiver?.getHdmiOutput?.hdmiOutput[0];
# # const[isValid, msg] = checkHdmiOutput(hdmiOutput);
# # if (!isValid)
# # {
# #     genLogs('FAILED', [msg]);
# # } else {
# #     genLogs('WAIT_AND_SEE', [msg]);
# # await delay(list[getIndex(step)].wait);
# # genLogs('OK');
# # handleNext();
# # }
# # }
# # });
# #
# # const[getUsbIp] = useLazyQuery(GET_USB_IP, {
# #     ...
# # option,
# # onCompleted: (data) = > {
# #     const
# # kvm = data?.transceiver?.getUsbIpServer?.usbIpServer[0];
# # const
# # isKvmLink =
# # kvm.usbipserverClientIpAddress == = temp.current.nmosdeviceIp & &
# #                                     kvm.usbipserverEnable == = 'ENABLED' & &
# #                                                                kvm.usbipserverConnectStatus == = 'STATUS_OK';
# # if (isKvmLink)
# # {
# #     handleNext();
# # } else {
# #     genLogs('FAILED', ['Kvm Link 失败']);
# # }
# # }
# # });
# # const[getDecodeIpmx] = useLazyQuery(GET_DECODE_IPMX, {
# #     ...
# # option,
# # onCompleted: (data) = > {
# #     const
# # ipmxs = data?.transceiver?.getIpmxInput?.ipmxInput;
# # const
# # targetVideo = ipmxs.find((item) = > item.inst == = '.1.1.1.1');
# # const
# # targetAudio = ipmxs.find((item) = > item.inst == = '.1.1.2.1');
# #
# # if (!targetVideo | | targetVideo.ipmxinputConnector != = temp.current) {
# # genLogs('FAILED', ['视频切换网口失败']);
# # return;
# # }
# # if (!targetAudio | | targetAudio.ipmxinputConnector != = temp.current) {
# # genLogs('FAILED', ['音频切换网口失败']);
# # return;
# # }
# #
# # handleNext();
# # }
# # });

