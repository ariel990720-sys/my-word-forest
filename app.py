import streamlit as st
import pandas as pd
import random
import time
import requests
import streamlit.components.v1 as components
from streamlit_lottie import st_lottie

# 1. 基礎設定
st.set_page_config(page_title="萌萌言語森林", page_icon="🐾", layout="centered")

# 2. 可愛與對對碰專用 CSS
st.markdown("""
    <style>
    .stApp { background-color: #F1F8E9; }
    .cute-title {
        font-size: 3rem; color: #388E3C; text-align: center; font-weight: bold;
        font-family: 'Microsoft JhengHei', cursive;
    }
    /* 卡片樣式 */
    .stButton > button {
        border-radius: 15px !important;
        height: 80px !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 資料庫 (第一單元)
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

def load_data():
    lines = [l.strip() for l in LEVEL_1_WORDS.strip().split('\n') if l.strip()]
    data = [l.split(',') for l in lines]
    return pd.DataFrame(data, columns=["en", "ipa", "cn"])

df = load_data()

# 4. Session State 初始化
if 'page' not in st.session_state: st.session_state.page = "cover"
if 'matches' not in st.session_state: st.session_state.matches = []
if 'selected_cards' not in st.session_state: st.session_state.selected_cards = []

# --- 模式 A：封面選單 ---
if st.session_state.page == "cover":
    st.markdown('<p class="cute-title">🐶 言語森林 🌲</p>', unsafe_allow_html=True)
    st.write("### 🔑 選擇冒險方式：")
    
    if st.button("✍️ 拼字挑戰 (第一單元)", use_container_width=True):
        st.session_state.remaining_indices = list(range(len(df)))
        st.session_state.idx = st.session_state.remaining_indices.pop(random.randrange(len(st.session_state.remaining_indices)))
        st.session_state.score = 0
        st.session_state.page = "spell_game"
        st.rerun()

    if st.button("🧩 對對碰遊戲 (Matching)", use_container_width=True):
        # 隨機挑 6 個單字做成 12 張牌
        sample = df.sample(6)
        cards = []
        for _, row in sample.iterrows():
            cards.append({"text": row['en'], "pair_id": row['en'], "type": "en"})
            cards.append({"text": row['cn'], "pair_id": row['en'], "type": "cn"})
        random.shuffle(cards)
        st.session_state.match_cards = cards
        st.session_state.matches = []
        st.session_state.selected_cards = []
        st.session_state.page = "match_game"
        st.rerun()

# --- 模式 B：對對碰遊戲模式 ---
elif st.session_state.page == "match_game":
    st.markdown('<p class="cute-title">🧩 單字對對碰</p>', unsafe_allow_html=True)
    if st.button("⬅️ 放棄返回"): 
        st.session_state.page = "cover"
        st.rerun()

    # 顯示 3x4 網格
    cards = st.session_state.match_cards
    cols = st.columns(3)
    
    for i, card in enumerate(cards):
        with cols[i % 3]:
            # 如果已經配對成功，顯示空位或打勾
            if card['text'] in st.session_state.matches:
                st.button(f"✅", key=f"btn_{i}", disabled=True, use_container_width=True)
            else:
                # 判斷是否為目前選中的卡片
                is_selected = i in st.session_state.selected_cards
                label = card['text']
                
                if st.button(label, key=f"btn_{i}", type="primary" if is_selected else "secondary", use_container_width=True):
                    if i not in st.session_state.selected_cards:
                        st.session_state.selected_cards.append(i)
                    
                    # 當選了兩張
                    if len(st.session_state.selected_cards) == 2:
                        idx1, idx2 = st.session_state.selected_cards
                        # 檢查 pair_id 是否相同
                        if cards[idx1]['pair_id'] == cards[idx2]['pair_id'] and cards[idx1]['type'] != cards[idx2]['type']:
                            st.toast("🎯 配對成功！", icon="⭐")
                            st.session_state.matches.append(cards[idx1]['text'])
                            st.session_state.matches.append(cards[idx2]['text'])
                        else:
                            st.toast("❌ 不對喔！", icon="🐻")
                        
                        time.sleep(0.5)
                        st.session_state.selected_cards = []
                        st.rerun()
    
    if len(st.session_state.matches) == 12:
        st.balloons()
        st.success("🎉 太厲害了！全部配對完成！")
        if st.button("再玩一次"): 
            st.session_state.page = "cover"
            st.rerun()

# (這裡下面維持你原本的 spell_game 拼字挑戰邏輯...)
