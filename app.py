import streamlit as st
import pandas as pd
import random
import time
import requests
import streamlit.components.v1 as components
from streamlit_lottie import st_lottie

# 1. 基礎設定
st.set_page_config(page_title="萌萌言語森林", page_icon="🐾", layout="centered")

# 2. 可愛 CSS
st.markdown("""
    <style>
    .stApp { background-color: #F1F8E9; }
    div[data-testid="stVerticalBlock"] > div:has(div.stInfo) {
        background: white; padding: 30px !important; border-radius: 30px !important;
        box-shadow: 0 10px 30px rgba(76, 175, 80, 0.1); border: 4px solid #C8E6C9;
    }
    .cute-title {
        font-size: 3rem; color: #388E3C; text-align: center; font-weight: bold;
        font-family: 'Microsoft JhengHei', cursive;
    }
    /* 隱藏建議單字與不必要的框框 */
    .stTextInput>div>div>input {
        autocomplete: off;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 多分類資料庫 (你可以隨時增加單字，現在已經分好類了)
DATA_DICT = {
    "🐾 森林動物": [
        "koala,[koˋɑlə],無尾熊", "ladybug,[ˋledɪ͵bʌg],瓢蟲", "rabbit,[ˋræbɪt],兔子",
        "squirrel,[ˋskwɝəl],松鼠", "deer,[dɪr],鹿", "owl,[aʊl],貓頭鷹",
        "fox,[fɑks],狐狸", "bear,[bɛr],熊", "monkey,[ˋmʌŋkɪ],猴子", "tiger,[ˋtaɪgɚ],老虎"
    ],
    "🌲 綠色植物": [
        "flower,[ˋflaʊɚ],花", "grass,[græs],草", "forest,[ˋfɔrɪst],森林",
        "mushroom,[ˋmʌʃrum],蘑菇", "branch,[bræntʃ],樹枝", "leaf,[lif],葉子",
        "root,[rut],根", "seed,[sid],種子", "bamboo,[bæmˋbu],竹子", "pine,[paɪn],松樹"
    ],
    "🏠 日常生活": [
        "imagine,[ɪˋmædʒɪn],想像", "improve,[ɪˋpruvmənt],改善", "judge,[dʒʌdʒ],判斷",
        "income,[ˋɪn͵kʌm],收入", "office,[ˋɑfɪs],辦公室", "school,[skul],學校",
        "friend,[frɛnd],朋友", "happy,[ˋhæpɪ],快樂", "coffee,[ˋkɔfɪ],咖啡", "bread,[brɛd],麵包"
    ]
}

# 4. 功能函數
def text_to_speech(text):
    js = f"<script>var m = new SpeechSynthesisUtterance('{text}'); m.lang='en-US'; window.speechSynthesis.speak(m);</script>"
    components.html(js, height=0)

@st.cache_data
def get_lottie_anim(url):
    try: return requests.get(url).json()
    except: return None

bear_anim = get_lottie_anim("https://assets10.lottiefiles.com/packages/lf20_stfayfky.json")
welcome_anim = get_lottie_anim("https://assets9.lottiefiles.com/packages/lf20_myejig9v.json")

# 5. 初始化 Session State
if 'page' not in st.session_state: st.session_state.page = "cover"
if 'score' not in st.session_state: st.session_state.score = 0
if 'remaining_indices' not in st.session_state: st.session_state.remaining_indices = []

# --- 模式 A：封面選單 ---
if st.session_state.page == "cover":
    st.markdown('<p class="cute-title">🐶 言語森林：關卡選擇 🌲</p>', unsafe_allow_html=True)
    if welcome_anim: st_lottie(welcome_anim, height=200, key="welcome")
    
    st.write("### 🔑 請選擇你想挑戰的關卡：")
    for category in DATA_DICT.keys():
        if st.button(f"{category} (10 個單字)"):
            # 轉換資料
            data_list = [line.split(',') for line in DATA_DICT[category]]
            st.session_state.current_df = pd.DataFrame(data_list, columns=["英文", "音標", "中文"])
            # 初始化「不重複」索引包
            st.session_state.remaining_indices = list(range(len(st.session_state.current_df)))
            st.session_state.idx = st.session_state.remaining_indices.pop(random.randrange(len(st.session_state.remaining_indices)))
            st.session_state.page = "study"
            st.session_state.score = 0
            st.rerun()

# --- 模式 B：練習模式 ---
elif st.session_state.page == "study":
    if st.button("⬅️ 回主選單"):
        st.session_state.page = "cover"
        st.rerun()

    df = st.session_state.current_df
    row = df.iloc[st.session_state.idx]
    current_word = row['英文'].strip()

    st.write(f"🌟 目前關卡進度：{st.session_state.score} / {len(df)}")
    st.progress(min(st.session_state.score / len(df), 1.0))

    # 答對邏輯
    if st.session_state.get('success_trigger', False):
        if bear_anim: st_lottie(bear_anim, height=150, key="bear")
        st.balloons()
        st.success("🎯 答對了！")
        time.sleep(1.5)
        
        # 檢查是否還有剩下單字
        if not st.session_state.remaining_indices:
            st.warning("🎉 恭喜！本關卡單字全數通關！")
            time.sleep(2)
            st.session_state.page = "cover"
        else:
            # 從「剩餘清單」中抽下一題
            next_idx_pos = random.randrange(len(st.session_state.remaining_indices))
            st.session_state.idx = st.session_state.remaining_indices.pop(next_idx_pos)
            
        st.session_state.success_trigger = False
        st.rerun()

    # 題目卡片
    with st.container():
        st.info(f"💡 **中文提示：** {row['中文']}")
        c1, c2 = st.columns([3, 1])
        with c1: st.write(f"🎧 **音標：** {row['音標']}")
        with c2: 
            if st.button("🔊 播放"): text_to_speech(current_word)

        # 這裡不顯示建議單字
        with st.form(key="game_form", clear_on_submit=True):
            # 使用 label_visibility 隱藏標籤，讓畫面更乾淨
            user_input = st.text_input("請拼出單字", label_visibility="collapsed", placeholder="請在此輸入英文...").strip().lower()
            if st.form_submit_button("提交 ✨"):
                if user_input == current_word.lower():
                    st.session_state.score += 1
                    st.session_state.success_trigger = True
                    st.rerun()
                else:
                    st.error("❌ 再試一次看看？")
                    text_to_speech(current_word)
                    
