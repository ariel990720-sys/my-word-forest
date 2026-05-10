import streamlit as st
import pandas as pd
import random
import time
import requests
import streamlit.components.v1 as components

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
    input[type="password"] {
        -webkit-text-security: none !important;
        autocomplete: off !important;
    }
    .stButton > button {
        border-radius: 12px !important;
        font-weight: bold !important;
    }
    /* 讓散落的字母更有層次感 */
    .letter-box {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 10px;
        padding: 20px;
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

if 'page' not in st.session_state: st.session_state.page = "cover"

# --- 封面與其他模式省略 (保持原本邏輯) ---
if st.session_state.page == "cover":
    st.markdown('<p class="cute-title">🐶 言語森林 🌲</p>', unsafe_allow_html=True)
    
    st.write("### ✍️ 拼字挑戰")
    if st.button("🔥 開始 42 單字挑戰"):
        st.session_state.current_df = df_all.copy()
        st.session_state.remaining_indices = list(range(len(st.session_state.current_df)))
        st.session_state.idx = st.session_state.remaining_indices.pop(random.randrange(len(st.session_state.remaining_indices)))
        st.session_state.score = 0
        st.session_state.page = "spell_game"
        st.rerun()

    st.write("### 🧩 對對碰關卡")
    c1, c2, c3 = st.columns(3)
    def init_match(num):
        sample = df_all.sample(num)
        cards = []
        for _, row in sample.iterrows():
            cards.append({"text": row['en'], "pid": row['en'], "type": "en"})
            cards.append({"text": row['cn'], "pid": row['en'], "type": "cn"})
        random.shuffle(cards)
        st.session_state.match_cards = cards
        st.session_state.matches = []
        st.session_state.selected = []
        st.session_state.total_pairs = num
        st.session_state.page = "match_game"
    if c1.button("🌱 小"): init_match(4); st.rerun()
    if c2.button("🌿 中"): init_match(8); st.rerun()
    if c3.button("🌳 大"): init_match(12); st.rerun()

    st.write("### 🔍 單字搜查令")
    if st.button("🔎 進入森林尋寶"):
        target_df = df_all.sample(10)
        st.session_state.search_targets = target_df.to_dict('records')
        st.session_state.found_words = []
        st.session_state.current_guess = ""
        # 混入隨機字母讓散落感更真實
        all_chars = "".join([d['en'] for d in st.session_state.search_targets])
        char_list = list(all_chars.lower())
        # 加入 10 個隨機干擾字母
        for _ in range(10): char_list.append(random.choice("abcdefghijklmnopqrstuvwxyz"))
        random.shuffle(char_list)
        st.session_state.letter_pool = char_list
        st.session_state.page = "search_game"
        st.session_state.hard_mode = False # 預設關閉屏蔽
        st.rerun()

# --- 拼字挑戰與對對碰代碼保持不變 (略) ---
elif st.session_state.page == "spell_game":
    if st.button("⬅️ 返回"): st.session_state.page = "cover"; st.rerun()
    row = st.session_state.current_df.iloc[st.session_state.idx]
    word = row['en'].strip()
    st.info(f"💡 中文：{row['cn']} \n\n 🎧 音標：{row['ipa']}")
    if st.button("🔊 播放"): text_to_speech(word)
    rk = f"p_{st.session_state.score}"
    with st.form(key=f"f_{rk}", clear_on_submit=True):
        ui = st.text_input("I", type="password", key=rk, label_visibility="collapsed").strip().lower()
        if st.form_submit_button("提交"):
            if ui == word.lower():
                st.session_state.score += 1
                if not st.session_state.remaining_indices: st.session_state.page = "cover"
                else: st.session_state.idx = st.session_state.remaining_indices.pop(random.randrange(len(st.session_state.remaining_indices)))
                st.rerun()
            else: st.error("❌")

elif st.session_state.page == "match_game":
    st.markdown('<p class="cute-title">🧩 對對碰</p>', unsafe_allow_html=True)
    if st.button("⬅️ 返回"): st.session_state.page = "cover"; st.rerun()
    cards = st.session_state.match_cards
    cols = st.columns(3)
    for i, card in enumerate(cards):
        with cols[i % 3]:
            if card['text'] in st.session_state.matches: st.button("✅", key=f"m_{i}", disabled=True)
            else:
                if st.button(card['text'], key=f"b_{i}", type="primary" if i in st.session_state.selected else "secondary"):
                    st.session_state.selected.append(i)
                    if len(st.session_state.selected) == 2:
                        idx1, idx2 = st.session_state.selected
                        if cards[idx1]['pid'] == cards[idx2]['pid'] and cards[idx1]['type'] != cards[idx2]['type']:
                            st.session_state.matches.extend([cards[idx1]['text'], cards[idx2]['text']])
                        st.session_state.selected = []
                    st.rerun()
    if len(st.session_state.matches) == st.session_state.total_pairs * 2:
        st.success("🎉"); time.sleep(1.5); st.session_state.page = "cover"; st.rerun()

# --- 模式 D：單字搜查令 (更新版：隨機散落 + 屏蔽功能) ---
elif st.session_state.page == "search_game":
    st.markdown('<p class="cute-title">🔍 單字搜查令</p>', unsafe_allow_html=True)
    
    col_back, col_toggle = st.columns([1, 2])
    with col_back:
        if st.button("⬅️ 返回"): st.session_state.page = "cover"; st.rerun()
    with col_toggle:
        # 屏蔽功能開關
        st.session_state.hard_mode = st.toggle("🌙 挑戰者模式 (隱藏中文與語音)", value=st.session_state.hard_mode)

    st.markdown(f"### 🎯 目前拼湊：`{st.session_state.current_guess}`")
    
    # 畫面布局
    area_main, area_side = st.columns([2, 1])
    
    with area_main:
        # 字母散落區：使用隨機寬度欄位來製造不規則感
        st.write("✨ 點擊散落的字母：")
        
        # 這裡用一個容器，裡面放很多小 column
        for i in range(0, len(st.session_state.letter_pool), 6):
            row_letters = st.session_state.letter_pool[i:i+6]
            cols = st.columns([random.randint(1,3) for _ in range(len(row_letters))])
            for idx, char in enumerate(row_letters):
                with cols[idx]:
                    if st.button(char.upper(), key=f"s_{i+idx}_{st.session_state.current_guess}"):
                        st.session_state.current_guess += char
                        st.rerun()

        if st.button("🧹 清除重拼"):
            st.session_state.current_guess = ""
            st.rerun()

    with area_side:
        st.write("📝 任務目標：")
        for item in st.session_state.search_targets:
            if item['en'] in st.session_state.found_words:
                st.write(f"✅ ~{item['en']}~")
            else:
                # 屏蔽邏輯：hard_mode 開啟時隱藏中文
                display_hint = "???" if st.session_state.hard_mode else item['cn']
