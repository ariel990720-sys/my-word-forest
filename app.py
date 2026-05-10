import streamlit as st
import pandas as pd
import random
import time
import requests
import streamlit.components.v1 as components

# 1. 基礎設定
st.set_page_config(page_title="萌萌言語森林", page_icon="🐾", layout="centered")

# 2. CSS 樣式優化
st.markdown("""
    <style>
    .stApp { background-color: #F1F8E9; }
    .cute-title {
        font-size: 3rem; color: #388E3C; text-align: center; font-weight: bold;
        font-family: 'Microsoft JhengHei', cursive;
    }
    /* 隱藏建議：針對密碼框的特殊顯示 */
    input[type="password"] {
        -webkit-text-security: none !important;
        autocomplete: off !important;
    }
    .stButton > button {
        width: 100%; border-radius: 15px !important; font-weight: bold !important;
    }
    /* 搜查令字母按鈕專用 */
    .letter-btn > div > button {
        height: 50px !important;
        width: 50px !important;
        margin: 2px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 第一單元資料庫
LEVEL_1_WORDS = """
ignore,[ɪgˋnor],忽視
ill,[ɪl],生病的
imagine,[ɪˋmædʒɪn],想像
importance,[ɪmˋpɔrtns],重要性
improve,[ɪmˋpruvmənt],改善
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
if 'page' not in st.session_state: st.session_state.page = "cover"

# --- 模式 A：封面選單 ---
if st.session_state.page == "cover":
    st.markdown('<p class="cute-title">🐶 言語森林 🌲</p>', unsafe_allow_html=True)
    
    st.write("### ✍️ 模式一：拼字冒險")
    if st.button("🔥 挑戰全單元拼寫"):
        st.session_state.current_df = df_all.copy()
        st.session_state.remaining_indices = list(range(len(st.session_state.current_df)))
        st.session_state.idx = st.session_state.remaining_indices.pop(random.randrange(len(st.session_state.remaining_indices)))
        st.session_state.score = 0
        st.session_state.page = "spell_game"
        st.rerun()

    st.write("### 🧩 模式二：關卡對對碰")
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

    if c1.button("🌱 小 (4對)"): init_match(4); st.rerun()
    if c2.button("🌿 中 (8對)"): init_match(8); st.rerun()
    if c3.button("🌳 大 (12對)"): init_match(12); st.rerun()

    st.write("### 🔍 模式三：單字搜查令")
    if st.button("🔎 找出隱藏的 10 個單字"):
        target_df = df_all.sample(10)
        st.session_state.search_targets = target_df.to_dict('records')
        st.session_state.found_words = []
        st.session_state.current_guess = ""
        # 建立字母池
        all_chars = "".join([d['en'] for d in st.session_state.search_targets])
        char_list = list(all_chars.lower())
        random.shuffle(char_list)
        st.session_state.letter_pool = char_list
        st.session_state.page = "search_game"
        st.rerun()

# --- 模式 B：拼字挑戰 (防建議版) ---
elif st.session_state.page == "spell_game":
    if st.button("⬅️ 返回"): st.session_state.page = "cover"; st.rerun()
    row = st.session_state.current_df.iloc[st.session_state.idx]
    word = row['en'].strip()
    st.write(f"🌟 進度：{st.session_state.score} / {len(st.session_state.current_df)}")
    st.info(f"💡 中文：{row['cn']} \n\n 🎧 音標：{row['ipa']}")
    if st.button("🔊 播放"): text_to_speech(word)
    rk = f"pwd_{st.session_state.score}_{st.session_state.idx}"
    with st.form(key=f"f_{rk}", clear_on_submit=True):
        user_input = st.text_input("輸入", type="password", key=rk, label_visibility="collapsed").strip().lower()
        if st.form_submit_button("提交"):
            if user_input == word.lower():
                st.session_state.score += 1
                if not st.session_state.remaining_indices:
                    st.success("🎉 通關！"); time.sleep(2); st.session_state.page = "cover"
                else:
                    st.session_state.idx = st.session_state.remaining_indices.pop(random.randrange(len(st.session_state.remaining_indices)))
                st.rerun()
            else: st.error("❌ 拼錯囉！")

# --- 模式 C：對對碰 ---
elif st.session_state.page == "match_game":
    st.markdown(f'<p class="cute-title">🧩 對對碰</p>', unsafe_allow_html=True)
    if st.button("⬅️ 返回"): st.session_state.page = "cover"; st.rerun()
    cards = st.session_state.match_cards
    c_num = 2 if st.session_state.total_pairs == 4 else 3
    cols = st.columns(c_num)
    for i, card in enumerate(cards):
        with cols[i % c_num]:
            if card['text'] in st.session_state.matches: st.button("✅", key=f"m_{i}", disabled=True)
            else:
                sel = i in st.session_state.selected
                if st.button(card['text'], key=f"b_{i}", type="primary" if sel else "secondary"):
                    if i not in st.session_state.selected: st.session_state.selected.append(i)
                    if len(st.session_state.selected) == 2:
                        idx1, idx2 = st.session_state.selected
                        if cards[idx1]['pid'] == cards[idx2]['pid'] and cards[idx1]['type'] != cards[idx2]['type']:
                            st.session_state.matches.extend([cards[idx1]['text'], cards[idx2]['text']])
                        st.session_state.selected = []
                    st.rerun()
    if len(st.session_state.matches) == st.session_state.total_pairs * 2:
        st.balloons(); st.success("🎉 成功！"); time.sleep(2); st.session_state.page = "cover"; st.rerun()

# --- 模式 D：單字搜查令 (New!) ---
elif st.session_state.page == "search_game":
    st.markdown('<p class="cute-title">🔍 單字搜查令</p>', unsafe_allow_html=True)
    if st.button("⬅️ 放棄返回"): st.session_state.page = "cover"; st.rerun()

    # 顯示目前拼出的字母
    st.markdown(f"### 🎯 目前拼湊：`{st.session_state.current_guess}`")
    
    col_l, col_r = st.columns([2, 1])
    
    with col_l:
        st.write("從字母池點擊字母來拼字：")
        # 顯示字母按鈕矩陣
        l_cols = st.columns(5)
        for i, char in enumerate(st.session_state.letter_pool):
            with l_cols[i % 5]:
                if st.button(char.upper(), key=f"char_{i}_{st.session_state.current_guess}"):
                    st.session_state.current_guess += char
                    st.rerun()
        
        if st.button("🧹 清除重拼", use_container_width=True):
            st.session_state.current_guess = ""
            st.rerun()

    with col_r:
        st.write("📝 待找單字：")
        for item in st.session_state.search_targets:
            if item['en'] in st.session_state.found_words:
                st.write(f"✅ ~{item['en']}~ ({item['cn']})")
            else:
                st.write(f"❓ **{item['cn']}**")

    # 檢查是否拼對
    for item in st.session_state.search_targets:
        if st.session_state.current_guess.lower() == item['en'].lower() and item['en'] not in st.session_state.found_words:
            st.session_state.found_words.append(item['en'])
            st.session_state.current_guess = ""
            st.toast(f"找到單字：{item['en']}！", icon="🎉")
            st.rerun()

    if len(st.session_state.found_words) == 10:
        st.balloons()
        st.success("🎉 恭喜！你找齊了所有 10 個隱藏單字！")
        time.sleep(3)
        st.session_state.page = "cover"
        st.rerun()
