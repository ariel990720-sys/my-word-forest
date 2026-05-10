import streamlit as st
import pandas as pd
import random
import time
import requests
import streamlit.components.v1 as components
from streamlit_lottie import st_lottie

# 1. 基礎設定
st.set_page_config(page_title="萌萌言語森林", page_icon="🐾", layout="centered")

# 2. 可愛 CSS (增加封面樣式)
st.markdown("""
    <style>
    .stApp { background-color: #F1F8E9; }
    .cover-card {
        background: white; padding: 40px; border-radius: 30px;
        text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        border: 5px solid #C8E6C9; margin-top: 50px;
    }
    .cute-title {
        font-size: 3.5rem; color: #388E3C; text-align: center; font-weight: bold;
        font-family: 'Comic Sans MS', 'Microsoft JhengHei', cursive;
    }
    .stButton > button {
        background-color: #4CAF50 !important; color: white !important;
        border-radius: 50px !important; font-weight: bold !important;
        padding: 15px 30px !important; font-size: 1.2rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 初始狀態與資料
if 'page' not in st.session_state:
    st.session_state.page = "cover"  # 預設為封面模式

@st.cache_data
def load_data():
    raw_data = """ill,[ɪl],生病的\nimagine,[ɪˋmædʒɪn],想像\nimportance,[ɪˋpɔrtns],重要性\nimprove,[ɪˋpruvmənt],改善\ninclude,[ɪnˋklud],包含\nincome,[ˋɪn͵kʌm],收入\njudge,[dʒʌdʒ],法官/判決\nkoala,[koˋɑlə],無尾熊\nladybug,[ˋledɪ͵bʌg],瓢蟲"""
    data_list = [line.split(',') for line in raw_data.strip().split('\n')]
    return pd.DataFrame(data_list, columns=["英文", "音標", "中文"])

def text_to_speech(text):
    js = f"<script>var m = new SpeechSynthesisUtterance('{text}'); m.lang='en-US'; window.speechSynthesis.speak(m);</script>"
    components.html(js, height=0)

def get_lottie_anim(url):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except: return None

bear_anim = get_lottie_anim("https://assets10.lottiefiles.com/packages/lf20_stfayfky.json")
welcome_anim = get_lottie_anim("https://assets9.lottiefiles.com/packages/lf20_myejig9v.json") # 可愛歡迎動畫
df = load_data()

# --- 模式切換 ---

# A. 封面模式
if st.session_state.page == "cover":
    st.markdown('<p class="cute-title">🐶 言語森林 🌲</p>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="cover-card">', unsafe_allow_html=True)
        # 顯示歡迎動畫
        if welcome_anim:
            st_lottie(welcome_anim, height=250, key="welcome")
        
        st.markdown("### 歡迎來到萌萌單字森林！")
        st.write("準備好收集森林碎片，讓這裡恢復生機了嗎？")
        
        if st.button("🌟 開始冒險 🌟"):
            st.session_state.page = "study"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# B. 練習模式 (原本的內容)
elif st.session_state.page == "study":
    if 'idx' not in st.session_state:
        st.session_state.idx = random.randint(0, len(df)-1)
        st.session_state.score = 0
        st.session_state.success_trigger = False

    # 返回按鈕 (放在左上角)
    if st.button("⬅️ 返回主選單"):
        st.session_state.page = "cover"
        st.rerun()

    st.markdown('<p class="cute-title">🍃 森林冒險中</p>', unsafe_allow_html=True)

    # (中間放你原本的學習程式碼內容...)
    col_set1, col_set2 = st.columns(2)
    with col_set1:
        show_cn = st.toggle("顯示中文 🐱", value=True)
    with col_set2:
        show_ipa = st.toggle("顯示音標 🎧", value=True)

    st.write(f"🌟 碎片收集：{st.session_state.score} / 10")
    st.progress(min(st.session_state.score / 10, 1.0))

    if st.session_state.success_trigger:
        if bear_anim: st_lottie(bear_anim, height=150, key="bear")
        st.balloons()
        st.success("🎯 答對了！")
        time.sleep(1.2)
        st.session_state.idx = random.randint(0, len(df)-1)
        st.session_state.success_trigger = False
        st.rerun()

    row = df.iloc[st.session_state.idx]
    current_word = row['英文'].strip()

    with st.container():
        if show_cn: st.info(f"💡 **中文提示：** {row['中文']}")
        else: st.info("💡 **中文提示：已隱藏**")
        
        c_ipa, c_voice = st.columns([3, 1])
        with c_ipa:
            if show_ipa: st.write(f"🎧 **音標：** {row['音標']}")
        with c_voice:
            if st.button("🔊 播放"): text_to_speech(current_word)

        with st.form(key="cute_form", clear_on_submit=True):
            user_input = st.text_input("輸入英文單字...").strip().lower()
            if st.form_submit_button("提交答案 ✨"):
                if user_input == current_word.lower():
                    st.session_state.score += 1
                    st.session_state.success_trigger = True
                    st.rerun()
                else:
                    st.error("❌ 錯了唷，再試一次！🐻")
                    text_to_speech(current_word)
