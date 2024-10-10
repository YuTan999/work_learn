import streamlit as st
import time
import pandas as pd
from graphql_mutations import get_sid, update_fan_speed
from graphql_queries import get_device_info, get_fan_speed
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
    elapsed_time = time.time() - start_time
    # if elapsed_time < 5:
    #     time.sleep(5 - elapsed_time)
    nmosName = data['data']['common']['getNmos']['nmos'][0]['nmosName']
    updateCurrentVersion = data['data']['system']['getImageUpdate']['imageUpdate'][0]['updateCurrentVersion']
    if nmosName and updateCurrentVersion:
        df.loc[1, 'result'] = 'TRUE'
        df.loc[1, 'log'] = f'设备名称: {nmosName}`, 设备版本: {updateCurrentVersion}'
    else:
        df.loc[1, 'result'] = 'FAILED'
        df.loc[1, 'log'] = '获取设备信息失败'
    df.loc[1, 'time(s)'] = elapsed_time


def updateFanSpeed(sid):
    start_time = time.time()
    result = 0
    send_graphql_mutation(update_fan_speed(sid, fanspeedInput('MANUAL','10')), graphql_url)
    time.sleep(2)
    if getFanSpeed(sid,'MANUAL','10'):
        result += 1
    send_graphql_mutation(update_fan_speed(sid, fanspeedInput('MANUAL','100')), graphql_url)
    time.sleep(2)
    if getFanSpeed(sid,'MANUAL','100'):
        result +=1
    send_graphql_mutation(update_fan_speed(sid, fanspeedInput('AUTO','10')), graphql_url)
    time.sleep(2)
    if getFanSpeed(sid,'AUTO','10'):
        result +=1
    print(result)
    if result == 3:
        df.loc[2, 'result'] = 'TRUE'
    else:
        df.loc[2, 'result'] = 'FALSE'
    elapsed_time = time.time() - start_time
    df.loc[2, 'time(s)'] = elapsed_time

def fanspeedInput(mode,speed):
    fanspeedinput= f'{{fanspeedControlMode:FAN_SPEED_CONTROL_MODE_{mode},fanspeedPercentage:{speed}}}'
    return fanspeedinput

def getFanSpeed(sid,mode,speed):
    data = send_graphql_query(get_fan_speed(sid), graphql_url)
    if data:
        fanspeedStatus = data['data']['system']['getFanSpeed']['fanSpeed'][0]['fanspeedStatus']
        fanspeedControlMode = data['data']['system']['getFanSpeed']['fanSpeed'][0]['fanspeedControlMode']

        fanspeedStatus_compare=f'FAN_SPEED_CONTROL_MODE_{mode}'
        print(fanspeedControlMode)
        print(fanspeedStatus_compare)
        print(fanspeedStatus)
        print(speed)
        print(fanspeedControlMode == fanspeedStatus_compare and fanspeedStatus == speed)
        if fanspeedControlMode == fanspeedStatus_compare and fanspeedStatus == speed:
            return True
    else:
        return False


#
# const[getInputFormat] = useLazyQuery(GET_VIDEO_AND_AUDIO_INPUT_FORMAT, {
#     ...
# option,
# onCompleted: (data) = > {
#     const
# videoDecode = data?.transceiver?.getVideoDecode?.videoDecode[0];
# const
# St2110InputAudio = data?.transceiver?.getSt2110InputAudio?.St2110InputAudio[0];
# const[isValid, msg] = checkVideoAndAudioInput(videoDecode, St2110InputAudio);
# if (!isValid)
# {
#     genLogs('FAILED', [msg]);
# } else {
#     genLogs('', [msg]);
# handleNext();
# }
# }
# });
# const[getHdmiOutput] = useLazyQuery(GET_HDMI_OUTPUT, {
#     ...
# option,
# onCompleted: async (data) = > {
#     const
# hdmiOutput = data?.transceiver?.getHdmiOutput?.hdmiOutput[0];
# const[isValid, msg] = checkHdmiOutput(hdmiOutput);
# if (!isValid)
# {
#     genLogs('FAILED', [msg]);
# } else {
#     genLogs('WAIT_AND_SEE', [msg]);
# await delay(list[getIndex(step)].wait);
# genLogs('OK');
# handleNext();
# }
# }
# });
#
# const[getUsbIp] = useLazyQuery(GET_USB_IP, {
#     ...
# option,
# onCompleted: (data) = > {
#     const
# kvm = data?.transceiver?.getUsbIpServer?.usbIpServer[0];
# const
# isKvmLink =
# kvm.usbipserverClientIpAddress == = temp.current.nmosdeviceIp & &
#                                     kvm.usbipserverEnable == = 'ENABLED' & &
#                                                                kvm.usbipserverConnectStatus == = 'STATUS_OK';
# if (isKvmLink)
# {
#     handleNext();
# } else {
#     genLogs('FAILED', ['Kvm Link 失败']);
# }
# }
# });
# const[getDecodeIpmx] = useLazyQuery(GET_DECODE_IPMX, {
#     ...
# option,
# onCompleted: (data) = > {
#     const
# ipmxs = data?.transceiver?.getIpmxInput?.ipmxInput;
# const
# targetVideo = ipmxs.find((item) = > item.inst == = '.1.1.1.1');
# const
# targetAudio = ipmxs.find((item) = > item.inst == = '.1.1.2.1');
#
# if (!targetVideo | | targetVideo.ipmxinputConnector != = temp.current) {
# genLogs('FAILED', ['视频切换网口失败']);
# return;
# }
# if (!targetAudio | | targetAudio.ipmxinputConnector != = temp.current) {
# genLogs('FAILED', ['音频切换网口失败']);
# return;
# }
#
# handleNext();
# }
# });
#
# const[getFanSpeed] = useLazyQuery(GET_FAN_SPEED, {
#     ...
# option,
# onCompleted: async (data) = > {
#     const
# fanSpeed = data?.system?.getFanSpeed?.fanSpeed[0];
# if (step === '7')
# {
# if (fanSpeed.fanspeedStatus !== 10) {
# genLogs('FAILED', ['转速切换至10%时失败']);
# return;
# }
# genLogs('WAIT_AND_SEE', ['成功切换至10%']);
# await delay(list[getIndex(step)].wait);
# genLogs('ONGOING');
# handleNext();
# }
#
# if (step === '7.1') {
# if (fanSpeed.fanspeedStatus != = 100) {
# genLogs('FAILED', ['转速切换至100%时失败']);
# return;
# }
# genLogs('WAIT_AND_SEE', ['成功切换至100%']);
# await delay(list[getIndex(step)].wait);
# genLogs('ONGOING');
# handleNext();
# }
#
# if (step === '7.2') {
# if (fanSpeed.fanspeedControlMode != = 'FAN_SPEED_CONTROL_MODE_AUTO') {
# genLogs('FAILED', ['转速切换至自动模式时失败']);
# return;
# }
# genLogs('WAIT_AND_SEE', ['成功切换到自动模式']);
# await delay(list[getIndex(step)].wait);
# genLogs('OK');
# handleNext();
# }
# }
# });
#
#
#
# const
# handleChangeFan = async (mode = 'FAN_SPEED_CONTROL_MODE_AUTO', value) = > {
#     updateFanSpeed({
#         variables: {
#             sid,
#             inst: '.0',
#     test: new Date().getTime(),
# input: {
# fanspeedControlMode: mode,
# ...(value ? {fanspeedPercentage: value}: {})
# }
# }
# });
# await delay();
# getFanSpeed({
#     variables: {
#         sid,
#         test: new
# Date().getTime()
# }
# });
# };


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
graphql_url = f"http://{ipaddr}/graphql"

if col3.button('Start Test'):
    sid = getSid()
    getDeviceInfo(sid)
    updateFanSpeed(sid)
if col4.button('Test Again'):
    ipaddr = '10.200.1.3'

st.dataframe(df, use_container_width=True)
