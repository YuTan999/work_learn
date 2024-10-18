import time
import pandas as pd
import streamlit as st
from graphql_mutations import get_sid, update_ipmx_input, update_fan_speed
from graphql_queries import get_device_info, get_decode_ipmx, get_video_and_audio_input_format, get_hdmi_output, \
    get_fan_speed
from graphql_requests import send_graphql_query, send_graphql_mutation

df = pd.DataFrame(columns=['result', 'interface', 'subscribe', 'log', 'time(s)'], index=[1, 2, 3])
df['interface'] = ['', 'ETH2', 'Fan Speed']
df['subscribe'] = ['gain device info', 'Video&Audio Input and HDMI Output', '10%->100%->auto']


def getSid():
    data = send_graphql_mutation(get_sid(), graphql_url)
    if data:
        sid = data['data']['login']['sid']
        # st.write(sid)
        return sid
    else:
        st.write('登陆失败，请检查地址是否正确')
        return 0


def getDeviceInfo(sid):
    start_time = time.time()
    data = send_graphql_query(get_device_info(sid), graphql_url)
    nmos_name = data['data']['common']['getNmos']['nmos'][0]['nmosName']
    update_current_version = data['data']['system']['getImageUpdate']['imageUpdate'][0]['updateCurrentVersion']
    if nmos_name and update_current_version:
        df.loc[1, 'result'] = 'TRUE'
        df.loc[1, 'log'] = f'设备名称: {nmos_name}`, 设备版本: {update_current_version}'
    else:
        df.loc[1, 'result'] = 'FAILED'
        df.loc[1, 'log'] = '获取设备信息失败'
    elapsed_time = time.time() - start_time
    df.loc[1, 'time(s)'] = elapsed_time


# 切换到ipin？update_input_selection
# 获取ip输入选择?get_input_selection
# handleUpdateOutput?UPDATE_RX_VIDEO_DECODE（还没写

def changeInterface(sid, value):
    start_time = time.time()
    inputs = f'{{ipmxinputConnector:{value}}}'
    send_graphql_mutation(update_ipmx_input(sid, ".1.1.1.1", inputs), graphql_url)
    send_graphql_mutation(update_ipmx_input(sid, ".1.1.2.1", inputs), graphql_url)
    elapsed_time = time.time() - start_time
    if elapsed_time < 15:
        time.sleep(8 - elapsed_time)
    ipmxlog = getDecodeIpmx(sid, value)
    formatlog = getInputFormat(sid)
    outputlog = getHdmiOutput(sid)
    if ipmxlog == '网口切换成功' and formatlog == '音视频格式正确' and outputlog == 'HDMI输出正常':
        df.loc[2, 'result'] = 'TRUE'
    else:
        df.loc[2, 'result'] = 'FALSE'
    df.loc[2, 'log'] = ipmxlog + formatlog + outputlog
    elapsed_time = time.time() - start_time
    df.loc[2, 'time(s)'] = elapsed_time


def getDecodeIpmx(sid, value):
    data = send_graphql_query(get_decode_ipmx(sid), graphql_url)
    video_input_selection = data['data']['transceiver']['getIpmxInput']['ipmxInput'][0]['ipmxinputConnector']
    audio_input_selection = data['data']['transceiver']['getIpmxInput']['ipmxInput'][1]['ipmxinputConnector']
    if video_input_selection == value and audio_input_selection == value:
        return '网口切换成功'
    else:
        return '网口切换失败'


def getInputFormat(sid):
    log = ''
    data = send_graphql_query(get_video_and_audio_input_format(sid), graphql_url)
    videodecode_status = data['data']['transceiver']['getVideoDecode']['videoDecode'][0]['videodecodeStatus']
    videodecode_mative_format = data['data']['transceiver']['getVideoDecode']['videoDecode'][0]['videodecodeNativeFormat']
    inputaudio_mode = data['data']['transceiver']['getSt2110InputAudio']['St2110InputAudio'][0]['st2110inputaudioMode']
    inputaudio_sample_rate = data['data']['transceiver']['getSt2110InputAudio']['St2110InputAudio'][0][
        'st2110inputaudioSampleRate']
    if videodecode_status != "STATUS_OK" or videodecode_mative_format != 'DISPLAY_TYPE_3840X2160P_6000':
        log += '视频格式错误'
    if inputaudio_mode != 'AUDIO_SOURCE_TYPE_PCM' or inputaudio_sample_rate != 'AUDIO_SAMPLERATE_48000':
        log += '音频格式错误'
    if log == '':
        return '音视频格式正确'
    else:
        return log


def getHdmiOutput(sid):
    data = send_graphql_query(get_hdmi_output(sid), graphql_url)
    status = data['data']['transceiver']['getHdmiOutput']['hdmiOutput'][0]['hdmioutputConnectionStatus']
    if status == 'LOCKED':
        return 'HDMI输出正常'
    else:
        return 'HDMI输出异常'


def updateFanSpeed(sid):
    start_time = time.time()
    log = ''
    # speed=10
    send_graphql_mutation(update_fan_speed(sid, fanSpeedInput('MANUAL', '10')), graphql_url)
    time.sleep(2)
    if getFanSpeed(1, sid, 'MANUAL', 10):
        log += '转速切换至10%时失败'
    # speed=100
    send_graphql_mutation(update_fan_speed(sid, fanSpeedInput('MANUAL', '100')), graphql_url)
    time.sleep(2)
    if getFanSpeed(2, sid, 'MANUAL', 100):
        log += '转速切换至100%时失败'
    # speed=auto
    send_graphql_mutation(update_fan_speed(sid, fanSpeedInput('AUTO', '10')), graphql_url)
    time.sleep(2)
    if getFanSpeed(3, sid, 'AUTO', 10):
        log += '转速切换至auto时失败'
    if log == '':
        df.loc[3, 'result'] = 'TRUE'
    else:
        df.loc[3, 'log'] = log
        df.loc[3, 'result'] = 'FALSE'
    elapsed_time = time.time() - start_time
    df.loc[3, 'time(s)'] = elapsed_time


def fanSpeedInput(mode, speed):
    fanspeedinput = f'{{fanspeedControlMode:FAN_SPEED_CONTROL_MODE_{mode},fanspeedPercentage:{speed}}}'
    return fanspeedinput


def getFanSpeed(step, sid, mode, speed):
    data = send_graphql_query(get_fan_speed(sid), graphql_url)
    if data:
        fanspeed_status = data['data']['system']['getFanSpeed']['fanSpeed'][0]['fanspeedStatus']
        fanspeed_control_mode = data['data']['system']['getFanSpeed']['fanSpeed'][0]['fanspeedControlMode']
        fanspeed_status_compare = f'FAN_SPEED_CONTROL_MODE_{mode}'
        if step == 1 or step == 2:
            if fanspeed_control_mode != fanspeed_status_compare or fanspeed_status != speed:
                return False
        elif step == 3:
            if fanspeed_control_mode != fanspeed_status_compare:
                return False


# 设置网页标题，以及使用宽屏模式
st.set_page_config(
    page_title="P-AVN-4",
    layout="wide"
)
# 隐藏右边的菜单以及页脚
hide_streamlit_style = """
<style>

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
# 左边导航栏

st.title("Auto Testing")
st.write('Notice:Make sure you are normal')
# 第一行
col1, col2, col3, col4 = st.columns(4)
ipaddr = col1.text_input('ip address', '10.200.1.40')
graphql_url = f"https://{ipaddr}/graphql"

if col3.button('Start Test'):
    session_id = getSid()
    if session_id:
        getDeviceInfo(session_id)
        changeInterface(session_id, 'NETWORK_CONNECTOR_2')
        updateFanSpeed(session_id)
if col4.button('Test Again'):
    ipaddr = '10.200.1.3'

st.dataframe(df, use_container_width=True)
