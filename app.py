import streamlit as st
import pandas as pd
import random
import time
import requests
import streamlit.components.v1 as components
from streamlit_lottie import st_lottie

# 1. 基礎設定
st.set_page_config(page_title="萌萌言語森林", page_icon="🐾", layout="centered")

# 2. CSS 樣式
st.markdown("""
    <style>
    .stApp { background-color: #F1F8E9; }
    .cute-title {
        font-size: 3rem; color: #388E3C; text-align: center; font-weight: bold;
        font-family: 'Microsoft JhengHei', cursive;
    }
    input { autocomplete: off !important; }
    /* 讓按鈕變大好點擊 */
    .stButton > button {
        width: 100%;
        border-radius: 20px !important;
        height: 3em !important;
        font-size: 1.2rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 資料庫
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
    return pd.DataFrame([l.split(',') for l in lines], columns=["en", "ipa", "cn"])

def text_to_speech(text):
    js = f"<script>var m = new SpeechSynthesisUtterance('{text}'); m.lang='en-US'; window.speechSynthesis.speak(m);</script>"
    components.html(js, height=0)

df_all = load_data()

# 4. 初始化 Session State
if 'page' not in st.session_state:
    st.session_state.page = "cover"

# --- 模式 A：封面選單 ---
if st.session_state.page == "cover":
    st.markdown('<p class="cute-title">🐶 言語森林 🌲</p>', unsafe_allow_html=True)
    st.write("### 選擇你的冒險模式：")
    
    # 使用 callback 方式切換頁面，這種方式最穩定
    def go_spell():
        st.session_state.current_df = df_all.copy()
        st.session_state.remaining_indices = list(range(len(st.session_state.current_df)))
        st.session_state.idx = st.session_state.remaining_indices.pop(random.randrange(len(st.session_state.remaining_indices)))
        st.session_state.score = 0
        st.session_state.page = "spell_game"

    def go_match():
        sample = df_all.sample(6)
        cards = []
        for _, row in sample.iterrows():
            cards.append({"text": row['en'], "pair_id": row['en'], "type": "en"})
            cards.append({"text": row['cn'], "pair_id": row['en'], "type": "cn"})
        random.shuffle(cards)
        st.session_state.match_cards = cards
        st.session_state.matches = []
        st.session_state.selected_cards = []
        st.session_state.page = "match_game"

    st.button("✍️ 拼字挑戰", on_click=go_spell)
    st.button("🧩 對對碰遊戲", on_click=go_match)

# --- 模式 B：拼字挑戰 ---
elif st.session_state.page == "spell_game":
    if st.button("⬅️ 返回主選單"):
        st.session_state.page = "cover"
        st.rerun()

    row = st.session_state.current_df.iloc[st.session_state.idx]
    current_word = row['en'].strip()

    st.write(f"🌟 進度：{st.session_state.score} / {len(st.session_state.current_df)}")
    
    with st.container():
        st.markdown(f"### 💡 中文：{row['cn']}")
        st.write(f"🎧 音標：{row['ipa']}")
        if st.button("🔊 播放"): text_to_speech(current_word)

        rk = f"in_{st.session_state.score}"
        with st.form(key=f"f_{rk}", clear_on_submit=True):
            user_input = st.text_input("拼寫", label_visibility="collapsed", key=rk).strip().lower()
            if st.form_submit_button("提交 ✨"):
                if user_input == current_word.lower():
                    st.session_state.score += 1
                    if not st.session_state.remaining_indices:
                        st.success("🎉 完成！")
                        time.sleep(2)
                        st.session_state.page = "cover"
                    else:
                        st.session_state.idx = st.session_state.remaining_indices.pop(random.randrange(len(st.session_state.remaining_indices)))
                    st.rerun()
                else:
                    st.error("❌ 拼錯囉！")

# --- 模式 C：對對碰 ---
elif st.session_state.page == "match_game":
    st.markdown('<p class="cute-title">🧩 對對碰</p>', unsafe_allow_html=True)
    if st.button("⬅️ 返回"):
        st.session_state.page = "cover"
        st.rerun()

    cards = st.session_state.match_cards
    cols = st.columns(3)
    for i, card in enumerate(cards):
        with cols[i % 3]:
            if card['text'] in st.session_state.matches:
                st.button("✅", key=f"m_{i}", disabled=True)
            else:
                sel = i in st.session_state.selected_cards
                if st.button(card['text'], key=f"b_{i}", type="primary" if sel else "secondary"):
                    if i not in st.session_state.selected_cards:
                        st.session_state.selected_cards.append(i)
                    if len(st.session_state.selected_cards) == 2:
                        idx1, idx2 = st.session_state.selected_cards
                        if cards[idx1]['pair_id'] == cards[idx2]['pair_id'] and cards[idx1]['type'] != cards[idx2]['type']:
                            st.session_state.matches.extend([cards[idx1]['text'], cards[idx2]['text']])
                        st.session_state.selected_cards = []
                    st.rerun()
    
    if len(st.session_state.matches) == 12:
        st.success("🎉 太棒了！")
        if st.button("回首頁"):
            st.session_state.page = "cover"
            st.rerun()

