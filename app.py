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
        font-size: 3.5rem; color: #388E3C; text-align: center; font-weight: bold;
        font-family: 'Microsoft JhengHei', cursive;
    }
    input { autocomplete: off !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. 資料庫：這就是你的 40 個核心單字
# 你以後可以按格式增加新的變數，例如 LEVEL_2_WORDS
LEVEL_1_WORDS = """
ill,[ɪl],生病的
imagine,[ɪˋmædʒɪn],想像
importance,[ɪˋpɔrtns],重要性
improve,[ɪˋpruvmənt],改善
include,[ɪnˋklud],包含
income,[ˋɪn͵kʌm],收入
increase,[ɪnˋkris],增加
independent,[͵ɪndɪˋpɛndənt],獨立的
indicate,[ˋɪndɪ͵ket],指示
influence,[ˋɪnflʊəns],影響
information,[͵ɪnfɚˋmeʃən],資訊
ink,[ɪŋk],墨水
insect,[ˋɪnsɛkt],昆蟲
insist,[ɪnˋsɪst],堅持
instance,[ˋɪnstəns],例子
instant,[ˋɪnstənt],瞬間的
instrument,[ˋɪnstrʊmənt],儀器
intelligent,[ɪnˋtɛlədʒənt],聰明的
intent,[ɪnˋtɛnt],意圖
interest,[ˋɪntrɪst],興趣
international,[͵ɪntɚˋnæʃənəl],國際的
interview,[ˋɪntɚ͵vju],面試
into,[ˋɪntu],進入
introduce,[͵ɪntrəˋdjus],介紹
invent,[ɪnˋvɛnt],發明
invite,[ɪnˋvaɪt],邀請
iron,[ˋaɪɚn],鐵/燙衣服
island,[ˋaɪlənd],島嶼
it,[ɪt],它
its,[ɪts],它的
itself,[ɪtˋsɛlf],它自己
jacket,[ˋdʒækɪt],夾克
jam,[dʒæm],果醬
january,[ˋdʒænju͵ɛrɪ],一月
jazz,[dʒæz],爵士樂
jealous,[ˋdʒɛləs],嫉妒的
jeans,[dʒinz],牛仔褲
jeep,[dʒip],吉普車
job,[dʒɑb],工作
jog,[dʒɑg],慢跑
join,[dʒɔɪn],加入
joke,[dʒok],笑話
journal,[ˋdʒɝnəl],期刊
journey,[ˋdʒɝnɪ],旅行
joy,[dʒɔɪ],歡樂
judge,[dʒʌdʒ],法官/判決
juice,[dʒus],果汁
july,[dʒuˋlaɪ],七月
jump,[dʒʌmp],跳
june,[dʒun],六月
junior,[ˋdʒunjɚ],資淺的
just,[dʒʌst],剛才/僅僅
kangaroo,[͵kæŋɡəˋru],袋鼠
keep,[kip],保持
key,[ki],鑰匙
kick,[kɪk],踢
kid,[kɪd],小孩
kill,[kɪl],殺
kind,[kaɪnd],種類/親切的
king,[kɪŋ],國王
kiss,[kɪs],親吻
kitchen,[ˋkɪtʃɪn],廚房
kite,[kaɪt],風箏
knee,[ni],膝蓋
knife,[naɪf],刀子
knight,[naɪt],騎士
knock,[nɑk],敲門
know,[no],知道
knowledge,[ˋnɑlɪdʒ],知識
koala,[koˋɑlə],無尾熊
ladybug,[ˋledɪ͵bʌg],瓢蟲
"""

# 4. 初始化函數
def load_and_format(raw_text):
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

# --- 模式 A：封面模式 ---
if st.session_state.page == "cover":
    st.markdown('<p class="cute-title">🐶 言語森林 🌲</p>', unsafe_allow_html=True)
    if welcome_anim: st_lottie(welcome_anim, height=250, key="welcome")
    
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.write("### 準備好開始第一階段的冒險了嗎？")
    
    # 這裡就是你的 40 個單字大關卡
    if st.button("🌟 挑戰核心 40 單字 🌟", use_container_width=True):
        st.session_state.current_df = load_and_format(LEVEL_1_WORDS)
        st.session_state.remaining_indices = list(range(len(st.session_state.current_df)))
        st.session_state.idx = st.session_state.remaining_indices.pop(random.randrange(len(st.session_state.remaining_indices)))
        st.session_state.score = 0
        st.session_state.page = "study"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- 模式 B：練習模式 ---
elif st.session_state.page == "study":
    if st.button("⬅️ 回主選單"):
        st.session_state.page = "cover"
        st.rerun()

    df = st.session_state.current_df
    row = df.iloc[st.session_state.idx]
    current_word = row['英文'].strip()

    st.write(f"🌟 碎片收集進度：{st.session_state.score} / {len(df)}")
    st.progress(min(st.session_state.score / len(df), 1.0))

    if st.session_state.get('success_trigger', False):
        if bear_anim: st_lottie(bear_anim, height=150, key="bear")
        st.balloons()
        st.success("🎯 答對了！")
        time.sleep(1.2)
        
        if not st.session_state.remaining_indices:
            st.balloons()
            st.warning("🎉 恭喜！你已完成所有 40 個單字的挑戰！")
            time.sleep(2)
            st.session_state.page = "cover"
        else:
            next_pos = random.randrange(len(st.session_state.remaining_indices))
            st.session_state.idx = st.session_state.remaining_indices.pop(next_pos)
            
        st.session_state.success_trigger = False
        st.rerun()

    with st.container():
        st.info(f"💡 **中文提示：** {row['中文']}")
        c1, c2 = st.columns([3, 1])
        with c1: st.write(f"🎧 **音標：** {row['音標']}")
        with c2: 
            if st.button("🔊 播放"): text_to_speech(current_word)

        with st.form(key="game_form", clear_on_submit=True):
            user_input = st.text_input("輸入框", label_visibility="collapsed", placeholder="請拼出單字...").strip().lower()
            if st.form_submit_button("提交 ✨"):
                if user_input == current_word.lower():
                    st.session_state.score += 1
                    st.session_state.success_trigger = True
                    st.rerun()
                else:
                    st.error("❌ 差一點點，再試試看！")
                    text_to_speech(current_word)
