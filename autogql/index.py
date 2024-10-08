import streamlit as st
import time
import pandas as pd
import graphql

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
col1, col2 = st.columns(2)
if col1.button('Start Test'):
    a=graphql.getsid()
if col2.button('Test Again'):
    a=2


df = pd.DataFrame(columns=['interface','subscribe','log','status','time(s)'],index=[1,2,3])
df['interface']= ['','ETH2','Fan Speed']
df['subscribe']=['gain device info','Video&Audio Input and HDMI Output','10%->100%->auto']
st.dataframe(df, use_container_width=True)