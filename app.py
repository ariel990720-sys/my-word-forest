import streamlit as st
import pandas as pd
import random
import time
import requests
import streamlit.components.v1 as components
from streamlit_lottie import st_lottie

# 1. 基礎設定
st.set_page_config(page_title="萌萌言語森林", page_icon="🐾", layout="centered")

# 2. 深度封殺建議 CSS
st.markdown("""
    <style>
    .stApp { background-color: #F1F8E9; }
    div[data-testid="stVerticalBlock"] > div:has(div.stInfo) {
        background: white; padding: 30px !important; border-radius: 30px !important;
        box-shadow: 0 10px 30px rgba(76, 175, 80, 0.1); border: 4px solid #C8E6C9;
    }
    .cute-title {
        font-size: 3.5rem; color: #388E3C; text-align: center; font-weight: bold;
        font-family: 'Microsoft JhengHei', cursive;
    }
    /* 暴力隱藏所有瀏覽器可能的彈窗 */
    input { 
        autocomplete: off !important; 
        -webkit-autocomplete: off !important;
        -moz-autocomplete: off !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 第一單元資料庫 (43 個單字)
LEVEL_1_WORDS = """
ignore,[ɪgˋnor],忽視
ill,[ɪl],生病的
imagine,[ɪˋmædʒɪn],想像
importance,[ɪmˋpɔrtns],重要性
improve,[ɪˋpruvmənt],改善
include,[ɪnˋklud],包含
income,[ˋɪn͵kʌm],收入
increase,[ɪnˋkris],增加
independence,[͵ɪndɪˋpɛndəns],獨立
independent,[͵ɪndɪˋpɛndənt],獨立的
indicate,[ˋɪndə͵ket],指出
industry,[ˋɪndəstrɪ],工業
influence,[ˋɪnflʊəns],影響
ink,[ɪŋk],墨水
insect,[ˋɪnsɛkt],昆蟲
insist,[ɪnˋsɪst],堅持
instance,[ˋɪnstəns],例子
instant,[ˋɪnstənt],即刻的
instrument,[ˋɪnstrəmənt],儀器/樂器
international,[͵ɪntɚˋnæʃən!],國際性的
interview,[ˋɪntɚ͵vju],訪談
introduce,[͵ɪntrəˋdjus],介紹
invent,[ɪnˋvɛnt],發明
invitation,[͵ɪnvəˋteʃən],邀請
invite,[ɪnˋvaɪt],邀請
island,[ˋaɪlənd],島
item,[ˋaɪtəm],項目
jacket,[ˋdʒækɪt],夾克
jam,[dʒæm],塞滿/果醬
jazz,[dʒæz],爵士樂
jeans,[dʒinz],牛仔褲
jeep,[dʒip],吉普車
jog,[dʒɑg],慢跑
joint,[dʒɔɪnt],關節
judge,[dʒʌdʒ],法官/判決
juicy,[ˋdʒusɪ],多汁的
ketchup,[ˋkɛtʃəp],番茄醬
kindergarten,[ˋkɪndɚ͵gɑrtn],幼稚園
kingdom,[ˋkɪŋdəm],王國
knock,[nɑk],相撞/敲門
knowledge,[ˋnɑlɪdʒ],知識
koala,[koˋɑlə],無尾熊
ladybug,[ˋledɪ͵bʌg],瓢蟲
"""

def load_data(raw_text):
    lines = [l.strip() for l in raw_text.strip().split('\n') if l.strip()]
    data = [l.split(',') for l in lines]
    return pd.DataFrame(data, columns=["英文", "音標", "中文"])

def text_to_speech(text):
    js = f"<script>var m = new SpeechSynthesisUtterance('{text}'); m.lang='en-US'; window.speechSynthesis.speak(m);</script>"
    components.html(js, height=0)

@st.cache_data
def get_lottie(url):
    try: return requests.get(url).json()
    except: return None

bear_anim = get_lottie("https://assets10.lottiefiles.com/packages/lf20_stfayfky.json")
welcome_anim = get_lottie("https://assets9.lottiefiles.com/packages/lf20_myejig9v.json")

if 'page' not in st.session_state: st.session_state.page = "cover"

# --- 模式 A：封面選單 ---
if st.session_state.page == "cover":
    st.markdown('<p class="cute-title">🐶 言語森林 🌲</p>', unsafe_allow_html=True)
    if welcome_anim: st_lottie(welcome_anim, height=220, key="welcome")
    
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button("🌟 開始第一單元挑戰 🌟", use_container_width=True):
        st.session_state.current_df = load_data(LEVEL_1_WORDS)
        st.session_state.remaining_indices = list(range(len(st.session_state.current_df)))
        st.session_state.idx = st.session_state.remaining_indices.pop(random.randrange(len(st.session_state.remaining_indices)))
        st.session_state.score = 0
        st.session_state.page = "study"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- 模式 B：挑戰模式 ---
elif st.session_state.page == "study":
    if st.button("⬅️ 回主選單"):
        st.session_state.page = "cover"
        st.rerun()

    df = st.session_state.current_df
    row = df.iloc[st.session_state.idx]
    current_word = row['英文'].strip()

    st.write(f"🌟 已收集碎片：{st.session_state.score} / {len(df)}")
    st.progress(min(st.session_state.score / len(df), 1.0))

    if st.session_state.get('success_trigger', False):
        if bear_anim: st_lottie(bear_anim, height=150, key="bear")
        st.balloons()
        st.success("🎯 收集成功！")
        time.sleep(1.2)
        
        if not st.session_state.remaining_indices:
            st.warning("🎉 恭喜完成！")
            time.sleep(2)
            st.session_state.page = "cover"
        else:
            next_pos = random.randrange(len(st.session_state.remaining_indices))
            st.session_state.idx = st.session_state.remaining_indices.pop(next_pos)
            
        st.session_state.success_trigger = False
        st.rerun()

    with st.container():
        st.markdown(f"### 💡 中文：{row['中文']}")
        c1, c2 = st.columns([3, 1])
        with c1: st.write(f"🎧 音標：{row['音標']}")
        with c2: 
            if st.button("🔊 播放音檔"): text_to_speech(current_word)

        # 這裡的關鍵：用隨機數當 Key，讓瀏覽器記不住這個輸入框
        random_key = f"input_{st.session_state.score}_{st.session_state.idx}"
        
        with st.form(key=f"form_{random_key}", clear_on_submit=True):
            user_input = st.text_input(
                "Secret Input", 
                label_visibility="collapsed", 
                placeholder="請拼出單字...",
                key=random_key  # 動態 Key
            ).strip().lower()
            
            if st.form_submit_button("提交 ✨"):
                if user_input == current_word.lower():
                    st.session_state.score += 1
                    st.session_state.success_trigger = True
                    st.rerun()
                else:
                    st.error("❌ 拼錯了唷！")
