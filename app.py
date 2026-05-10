import streamlit as st
import pandas as pd
import random
import time
import requests
import streamlit.components.v1 as components
from streamlit_lottie import st_lottie

# 1. 基礎設定
st.set_page_config(page_title="萌萌言語森林", page_icon="🐾", layout="centered")

# 2. 強效封殺建議 CSS (核心重點)
st.markdown("""
    <style>
    .stApp { background-color: #F1F8E9; }
    
    /* 1. 針對所有輸入框強制關閉自動完成 */
    input {
        autocomplete: off !important;
        -webkit-autocomplete: off !important;
        -moz-autocomplete: off !important;
    }

    /* 2. 終極黑科技：讓 Password 類型的輸入框顯示為正常文字 */
    /* 這樣瀏覽器絕對不會對密碼框產生「單字建議」 */
    input[type="password"] {
        -webkit-text-security: none !important;
        font-family: 'monospace' !important;
    }

    div[data-testid="stVerticalBlock"] > div:has(div.stInfo) {
        background: white; padding: 30px !important; border-radius: 30px !important;
        box-shadow: 0 10px 30px rgba(76, 175, 80, 0.1); border: 4px solid #C8E6C9;
    }
    .cute-title {
        font-size: 3rem; color: #388E3C; text-align: center; font-weight: bold;
        font-family: 'Microsoft JhengHei', cursive;
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

@st.cache_data
def load_data():
    lines = [l.strip() for l in LEVEL_1_WORDS.strip().split('\n') if l.strip()]
    data = [l.split(',') for l in lines]
    return pd.DataFrame(data, columns=["en", "ipa", "cn"])

def text_to_speech(text):
    js = f"<script>var m = new SpeechSynthesisUtterance('{text}'); m.lang='en-US'; window.speechSynthesis.speak(m);</script>"
    components.html(js, height=0)

@st.cache_data
def get_lottie(url):
    try: return requests.get(url).json()
    except: return None

bear_anim = get_lottie("https://assets10.lottiefiles.com/packages/lf20_stfayfky.json")
df_all = load_data()

if 'page' not in st.session_state: st.session_state.page = "cover"

# --- 模式 A：封面選單 ---
if st.session_state.page == "cover":
    st.markdown('<p class="cute-title">🐶 萌萌拼單字 🌲</p>', unsafe_allow_html=True)
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    
    if st.button("🌟 開始挑戰第一單元 (43字) 🌟", use_container_width=True):
        st.session_state.current_df = df_all.copy()
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
    current_word = row['en'].strip()

    st.write(f"🌟 已收集碎片：{st.session_state.score} / {len(df)}")
    st.progress(min(st.session_state.score / len(df), 1.0))

    # 成功動畫與自動下一題
    if st.session_state.get('success_trigger', False):
        if bear_anim: st_lottie(bear_anim, height=150, key=f"bear_{st.session_state.score}")
        st.balloons()
        st.success("🎯 答對了！")
        time.sleep(1.2)
        
        if not st.session_state.remaining_indices:
            st.warning("🎉 全單元達成！")
            time.sleep(2)
            st.session_state.page = "cover"
        else:
            next_pos = random.randrange(len(st.session_state.remaining_indices))
            st.session_state.idx = st.session_state.remaining_indices.pop(next_pos)
            
        st.session_state.success_trigger = False
        st.rerun()

    # 題目卡片
    with st.container():
        st.info(f"💡 中文意思：{row['cn']}")
        c1, c2 = st.columns([3, 1])
        with c1: st.write(f"🎧 音標：{row['ipa']}")
        with c2: 
            if st.button("🔊 播放"): text_to_speech(current_word)

        # 這裡使用 type="password" 強制讓瀏覽器判定為密碼，不儲存歷史紀錄
        # 同時使用動態 Key，讓瀏覽器無法對應
        dynamic_key = f"input_step_{st.session_state.score}_{st.session_state.idx}"
        
        with st.form(key=f"form_{dynamic_key}", clear_on_submit=True):
            user_input = st.text_input(
                "Spell", 
                type="password", # 關鍵防禦 1
                label_visibility="collapsed", 
                placeholder="請拼出單字...",
                key=dynamic_key  # 關鍵防禦 2
            ).strip().lower()
            
            if st.form_submit_button("檢查答案 ✨"):
                if user_input == current_word.lower():
                    st.session_state.score += 1
                    st.session_state.success_trigger = True
                    st.rerun()
                else:
                    st.error("❌ 拼錯了唷，再試一次！")
