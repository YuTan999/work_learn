import asyncio
import time
from typing import Dict, Any

import aiohttp
import pandas as pd
import streamlit as st
from graphql_mutations import get_sid, update_ipmx_input, update_fan_speed
from graphql_queries import (
    get_device_info, get_decode_ipmx, get_video_and_audio_input_format,
    get_hdmi_output, get_fan_speed
)

# Constants
COLUMNS = ['result', 'interface', 'subscribe', 'log', 'time(s)']
INTERFACES = ['', 'ETH2', 'Fan Speed']
SUBSCRIPTIONS = ['gain device info', 'Video&Audio Input and HDMI Output', '10%->100%->auto']

# Initialize DataFrame
df = pd.DataFrame(columns=COLUMNS, index=[1, 2, 3])
df['interface'] = INTERFACES
df['subscribe'] = SUBSCRIPTIONS


@st.cache(ttl=600)
async def get_sid(session: aiohttp.ClientSession, graphql_url: str) -> str:
    """Get session ID."""
    try:
        async with session.post(graphql_url, json={"query": get_sid()}) as response:
            data = await response.json()
            if data and 'data' in data and 'login' in data['data']:
                return data['data']['login']['sid']
    except aiohttp.ClientError:
        st.error('Login failed. Please check the address.')
    return ''


async def get_device_info(session: aiohttp.ClientSession, sid: str, graphql_url: str) -> None:
    """Get and update device information."""
    start_time = time.time()
    try:
        async with session.post(graphql_url, json={"query": get_device_info(sid)}) as response:
            data = await response.json()
            if data and 'data' in data:
                nmos_name = data['data']['common']['getNmos']['nmos'][0]['nmos_name']
                update_current_version = data['data']['system']['getImageUpdate']['imageUpdate'][0][
                    'update_current_version']

                if nmos_name and update_current_version:
                    df.loc[1, 'result'] = 'TRUE'
                    df.loc[1, 'log'] = f'Device Name: {nmos_name}, Version: {update_current_version}'
                else:
                    df.loc[1, 'result'] = 'FAILED'
                    df.loc[1, 'log'] = 'Failed to get device information'
    except aiohttp.ClientError:
        df.loc[1, 'result'] = 'FAILED'
        df.loc[1, 'log'] = 'Network error occurred'

    df.loc[1, 'time(s)'] = time.time() - start_time


async def change_interface(session: aiohttp.ClientSession, sid: str, value: str, graphql_url: str) -> None:
    """Change interface and update status."""
    start_time = time.time()
    inputs = f'{{ipmxinputConnector:{value}}}'

    async def update_input(endpoint: str):
        try:
            await session.post(graphql_url, json={"query": update_ipmx_input(sid, endpoint, inputs)})
        except aiohttp.ClientError:
            st.error(f"Failed to update input for {endpoint}")

    await asyncio.gather(
        update_input(".1.1.1.1"),
        update_input(".1.1.2.1")
    )

    await asyncio.sleep(2)  # Reduced sleep time

    results = await asyncio.gather(
        get_decode_ipmx(session, sid, value, graphql_url),
        get_input_format(session, sid, graphql_url),
        get_hdmi_output(session, sid, graphql_url)
    )

    ipmx_log, format_log, output_log = results

    df.loc[2, 'result'] = 'TRUE' if all(
        [ipmx_log == '网口切换成功', format_log == '音视频格式正确', output_log == 'HDMI输出正常']) else 'FALSE'
    df.loc[2, 'log'] = f"{ipmx_log} {format_log} {output_log}"
    df.loc[2, 'time(s)'] = time.time() - start_time


async def get_decode_ipmx(session: aiohttp.ClientSession, sid: str, value: str, graphql_url: str) -> str:
    """Get IPMX decode status."""
    try:
        async with session.post(graphql_url, json={"query": get_decode_ipmx(sid)}) as response:
            data = await response.json()
            if data and 'data' in data:
                video_input = data['data']['transceiver']['getIpmxInput']['ipmxInput'][0]['ipmxinputConnector']
                audio_input = data['data']['transceiver']['getIpmxInput']['ipmxInput'][1]['ipmxinputConnector']
                return '网口切换成功' if video_input == value and audio_input == value else '网口切换失败'
    except aiohttp.ClientError:
        return '获取IPMX解码状态失败'


async def get_input_format(session: aiohttp.ClientSession, sid: str, graphql_url: str) -> str:
    """Get input format status."""
    try:
        async with session.post(graphql_url, json={"query": get_video_and_audio_input_format(sid)}) as response:
            data = await response.json()
            if data and 'data' in data:
                video_decode = data['data']['transceiver']['getVideoDecode']['videoDecode'][0]
                audio_input = data['data']['transceiver']['getSt2110InputAudio']['St2110InputAudio'][0]

                video_status = video_decode['videodecode_status'] == "STATUS_OK" and video_decode[
                    'videodecode_mative_format'] == 'DISPLAY_TYPE_3840X2160P_6000'
                audio_status = audio_input['st2110inputaudio_mode'] == 'AUDIO_SOURCE_TYPE_PCM' and audio_input[
                    'st2110inputaudio_sample_rate'] == 'AUDIO_SAMPLERATE_48000'

                if video_status and audio_status:
                    return '音视频格式正确'
                return '视频格式错误' if not video_status else '音频格式错误'
    except aiohttp.ClientError:
        return '获取输入格式失败'


async def get_hdmi_output(session: aiohttp.ClientSession, sid: str, graphql_url: str) -> str:
    """Get HDMI output status."""
    try:
        async with session.post(graphql_url, json={"query": get_hdmi_output(sid)}) as response:
            data = await response.json()
            if data and 'data' in data:
                status = data['data']['transceiver']['getHdmiOutput']['hdmiOutput'][0]['hdmioutputConnectionStatus']
                return 'HDMI输出正常' if status == 'LOCKED' else 'HDMI输出异常'
    except aiohttp.ClientError:
        return 'HDMI输出状态获取失败'


async def update_fan_speed(session: aiohttp.ClientSession, sid: str, graphql_url: str) -> None:
    """Update fan speed and check status."""
    start_time = time.time()
    log = []

    async def update_and_check(mode: str, speed: str):
        try:
            await session.post(graphql_url, json={"query": update_fan_speed(sid, fan_speed_input(mode, speed))})
            await asyncio.sleep(2)
            if not await get_fan_speed(session, sid, mode, int(speed), graphql_url):
                return f'转速切换至{speed}%时失败' if mode == 'MANUAL' else '转速切换至auto时失败'
        except aiohttp.ClientError:
            return f'更新风扇速度失败: {mode} {speed}'

    results = await asyncio.gather(
        update_and_check('MANUAL', '10'),
        update_and_check('MANUAL', '100'),
        update_and_check('AUTO', '10')
    )

    log = [result for result in results if result]

    df.loc[3, 'result'] = 'TRUE' if not log else 'FALSE'
    df.loc[3, 'log'] = ' '.join(log)
    df.loc[3, 'time(s)'] = time.time() - start_time


def fan_speed_input(mode: str, speed: str) -> str:
    """Generate fan speed input string."""
    return f'{{fanspeed_control_mode:FAN_SPEED_CONTROL_MODE_{mode},fanspeedPercentage:{speed}}}'


async def get_fan_speed(session: aiohttp.ClientSession, sid: str, mode: str, speed: int, graphql_url: str) -> bool:
    """Get and check fan speed status."""
    try:
        async with session.post(graphql_url, json={"query": get_fan_speed(sid)}) as response:
            data = await response.json()
            if data and 'data' in data:
                fan_speed = data['data']['system']['getFanSpeed']['fanSpeed'][0]
                return (fan_speed['fanspeed_control_mode'] == f'FAN_SPEED_CONTROL_MODE_{mode}' and
                        (mode == 'AUTO' or fan_speed['fanspeed_status'] == speed))
    except aiohttp.ClientError:
        return False


async def main():
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
    graphql_url = f"https://{ipaddr}/graphql"

    if col3.button('Start Test'):
        async with aiohttp.ClientSession() as session:
            session_id = await get_sid(session, graphql_url)
            if session_id:
                await asyncio.gather(
                    get_device_info(session, session_id, graphql_url),
                    update_fan_speed(session, session_id, graphql_url),
                    change_interface(session, session_id, 'NETWORK_CONNECTOR_2', graphql_url)
                )

    if col4.button('Test Again'):
        st.session_state.ipaddr = '10.200.1.3'

    st.dataframe(df, use_container_width=True)


if __name__ == "__main__":
    asyncio.run(main())