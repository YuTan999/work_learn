# from graphql_queries import get_hdmi_output, get_video_and_audio_input_format, get_device_info, get_decode_ipmx
# from graphql_mutations import update_fan_speed, get_sid
# from graphql_requests import send_graphql_query
#
# graphql_url = "http://10.200.1.40/graphql"
#
# # get_sid = get_sid()
# query = get_hdmi_output('kvZ5QLLl8B5lSjiq50OzPNwMEtZ7TWRC')
# print(query)
# result = send_graphql_query(query, graphql_url)
# if result:
#     print(result)
#     # print(result['data']['transceiver']['St2110InputAudio'][0]['st2110inputaudioMode'])
#     # print(result['data']['transceiver']['St2110InputAudio'][0]['st2110inputaudioSampleRate'])
#     # print(result['data']['transceiver']['getIpmxInput']['ipmxInput'][0]['ipmxinputConnector'])
#     # print(result['data']['transceiver']['getIpmxInput']['ipmxInput'][1]['ipmxinputConnector'])
#
# # fanspeedinput_test = f'{{fanspeedControlMode:FAN_SPEED_CONTROL_MODE_{mode},fanspeedPercentage:{speed}}}'
# #
# # fstest = fanspeedinput_test(mode='AUTO', speed=100)
# # print(fstest)
#
#
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


import time
import pandas as pd
import streamlit as st
from graphql_mutations import get_sid, update_ipmx_input, update_fan_speed
from graphql_queries import get_device_info, get_decode_ipmx, get_video_and_audio_input_format, get_hdmi_output, \
    get_fan_speed
from graphql_requests import send_graphql_query, send_graphql_mutation

# Constants
COLUMNS = ['result', 'interface', 'subscribe', 'log', 'time(s)']
INTERFACES = ['', 'ETH2', 'Fan Speed']
SUBSCRIPTIONS = ['gain device info', 'Video&Audio Input and HDMI Output', '10%->100%->auto']

# Initialize DataFrame
df = pd.DataFrame(columns=COLUMNS, index=[1, 2, 3])
df['interface'] = INTERFACES
df['subscribe'] = SUBSCRIPTIONS


def getSid(graphql_url: str) -> str:
    """Get session ID."""
    data = send_graphql_mutation(get_sid(), graphql_url)
    if data and 'data' in data and 'login' in data['data']:
        return data['data']['login']['sid']
    st.write('Login failed. Please check the address.')
    return ''


def getDeviceInfo(sid: str, graphql_url: str) -> None:
    """Get and update device information."""
    start_time = time.time()
    data = send_graphql_query(get_device_info(sid), graphql_url)
    if data and 'data' in data:
        nmos_name = data['data']['common']['getNmos']['nmos'][0]['nmosName']
        update_current_version = data['data']['system']['getImageUpdate']['imageUpdate'][0]['updateCurrentVersion']

        if nmos_name and update_current_version:
            df.loc[1, 'result'] = 'TRUE'
            df.loc[1, 'log'] = f'Device Name: {nmos_name}, Version: {update_current_version}'
        else:
            df.loc[1, 'result'] = 'FAILED'
            df.loc[1, 'log'] = 'Failed to get device information'

    df.loc[1, 'time(s)'] = time.time() - start_time


def changeInterface(sid: str, value: str, graphql_url: str) -> None:
    """Change interface and update status."""
    start_time = time.time()
    inputs = f'{{ipmxinputConnector:{value}}}'
    send_graphql_mutation(update_ipmx_input(sid, ".1.1.1.1", inputs), graphql_url)
    send_graphql_mutation(update_ipmx_input(sid, ".1.1.2.1", inputs), graphql_url)

    time.sleep(max(0, 8 - (time.time() - start_time)))

    ipmx_log = getDecodeIpmx(sid, value, graphql_url)
    format_log = getInputFormat(sid, graphql_url)
    output_log = getHdmiOutput(sid, graphql_url)

    df.loc[2, 'result'] = 'TRUE' if all(
        [ipmx_log == '网口切换成功', format_log == '音视频格式正确', output_log == 'HDMI输出正常']) else 'FALSE'
    df.loc[2, 'log'] = f"{ipmx_log} {format_log} {output_log}"
    df.loc[2, 'time(s)'] = time.time() - start_time


def getDecodeIpmx(sid: str, value: str, graphql_url: str) -> str:
    """Get IPMX decode status."""
    data = send_graphql_query(get_decode_ipmx(sid), graphql_url)
    if data and 'data' in data:
        video_input = data['data']['transceiver']['getIpmxInput']['ipmxInput'][0]['ipmxinputConnector']
        audio_input = data['data']['transceiver']['getIpmxInput']['ipmxInput'][1]['ipmxinputConnector']
        return '网口切换成功' if video_input == value and audio_input == value else '网口切换失败'
    return '获取IPMX解码状态失败'


def getInputFormat(sid: str, graphql_url: str) -> str:
    """Get input format status."""
    data = send_graphql_query(get_video_and_audio_input_format(sid), graphql_url)
    if data and 'data' in data:
        video_decode = data['data']['transceiver']['getVideoDecode']['videoDecode'][0]
        audio_input = data['data']['transceiver']['getSt2110InputAudio']['St2110InputAudio'][0]

        video_status = video_decode['videodecodeStatus'] == "STATUS_OK" and video_decode[
            'videodecodeNativeFormat'] == 'DISPLAY_TYPE_3840X2160P_6000'
        audio_status = audio_input['st2110inputaudioMode'] == 'AUDIO_SOURCE_TYPE_PCM' and audio_input[
            'st2110inputaudioSampleRate'] == 'AUDIO_SAMPLERATE_48000'

        if video_status and audio_status:
            return '音视频格式正确'
        return '视频格式错误' if not video_status else '音频格式错误'
    return '获取输入格式失败'


def getHdmiOutput(sid: str, graphql_url: str) -> str:
    """Get HDMI output status."""
    data = send_graphql_query(get_hdmi_output(sid), graphql_url)
    if data and 'data' in data:
        status = data['data']['transceiver']['getHdmiOutput']['hdmiOutput'][0]['hdmioutputConnectionStatus']
        return 'HDMI输出正常' if status == 'LOCKED' else 'HDMI输出异常'
    return 'HDMI输出状态获取失败'


def updateFanSpeed(sid: str, graphql_url: str) -> None:
    """Update fan speed and check status."""
    start_time = time.time()
    log = []

    for mode, speed in [('MANUAL', '10'), ('MANUAL', '100'), ('AUTO', '10')]:
        print(update_fan_speed(sid, fanSpeedInput(mode, speed)))
        send_graphql_mutation(update_fan_speed(sid, fanSpeedInput(mode, speed)), graphql_url)
        time.sleep(2)
        if not getFanSpeed(sid, mode, int(speed), graphql_url):
            log.append(f'转速切换至{speed}%时失败' if mode == 'MANUAL' else '转速切换至auto时失败')

    df.loc[3, 'result'] = 'TRUE' if not log else 'FALSE'
    df.loc[3, 'log'] = ' '.join(log)
    df.loc[3, 'time(s)'] = time.time() - start_time


def fanSpeedInput(mode: str, speed: str) -> str:
    """Generate fan speed input string."""
    return f'{{fanspeedControlMode:FAN_SPEED_CONTROL_MODE_{mode},fanspeedPercentage:{speed}}}'


def getFanSpeed(sid: str, mode: str, speed: int, graphql_url: str) -> bool:
    """Get and check fan speed status."""
    data = send_graphql_query(get_fan_speed(sid), graphql_url)
    if data and 'data' in data:
        fan_speed = data['data']['system']['getFanSpeed']['fanSpeed'][0]
        return (fan_speed['fanspeedControlMode'] == f'FAN_SPEED_CONTROL_MODE_{mode}' and
                (mode == 'AUTO' or fan_speed['fanspeedStatus'] == speed))
    return False


def main():
    st.set_page_config(page_title="P-AVN-4", layout="wide")
    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

    st.title("Auto Testing")
    st.write('Notice: Make sure you are normal')

    col1, col2, col3, col4 = st.columns(4)
    ipaddr = col1.text_input('ip address', '10.200.1.40')
    graphql_url = f"http://{ipaddr}/graphql"

    if col3.button('Start Test'):
        session_id = getSid(graphql_url)
        if session_id:
            getDeviceInfo(session_id, graphql_url)
            changeInterface(session_id, 'NETWORK_CONNECTOR_1', graphql_url)
            updateFanSpeed(session_id, graphql_url)

    if col4.button('Test Again'):
        st.session_state.ipaddr = '10.200.1.3'

    st.dataframe(df, use_container_width=True)


if __name__ == "__main__":
    main()
