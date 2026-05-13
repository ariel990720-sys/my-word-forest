import streamlit as st
import pandas as pd
import random
import time
import streamlit.components.v1 as components

# --- 1. 初始化與角色資料 ---
if 'unlocked_chars' not in st.session_state:
    st.session_state.unlocked_chars = [] # 儲存已解鎖的角色

# 角色圖鑑資料
CHARACTERS = {
    "第一單元": {"name": "小樹蛙 🐸", "desc": "跳躍吧！你是拼字小能手"},
    "第二單元": {"name": "松鼠司機 🐿️", "desc": "速度與激情！搬運單字飛快"},
    "第三單元": {"name": "森林之王 🦁", "desc": "吼！這片森林的單字都歸你管"}
}

st.set_page_config(page_title="萌萌言語森林", page_icon="🐾")

# --- 2. 語音功能 ---
def text_to_speech(text):
    text = text.replace("'", "\\'")
    js = f"""<script>window.speechSynthesis.cancel(); var msg = new SpeechSynthesisUtterance('{text}'); msg.lang = 'en-US'; window.speechSynthesis.speak(msg);</script>"""
    components.html(js, height=0)

# --- 3. 頁面切換邏輯 ---
if 'page' not in st.session_state: st.session_state.page = "cover"

# --- 封面頁 (新增角色圖鑑顯示) ---
if st.session_state.page == "cover":
    st.markdown("<h1 style='text-align: center;'>🌲 萌萌言語森林 🌲</h1>", unsafe_allow_html=True)
    
    # 顯示已解鎖角色
    if st.session_state.unlocked_chars:
        st.write("### 🏆 你的森林夥伴")
        cols = st.columns(len(st.session_state.unlocked_chars))
        for i, char_name in enumerate(st.session_state.unlocked_chars):
            with cols[i]:
                st.info(f"**{char_name}**")
    
    st.divider()
    st.write("### 🚀 開始挑戰解鎖角色")
    
    # 單元資料 (與之前相同)
    U1_RAW = "ignore,[ɪgˋnor],忽視\nill,[ɪl],生病的\nimagine,[ɪˋmædʒɪn],想像" # 範例縮短
    U2_RAW = "lane,[len],小路\nlanguage,[ˋlæŋgwɪdʒ],語言" 
    U3_RAW = "mango,[ˋmæŋgo],芒果\nmanner,[ˋmænɚ],方法"

    col1, col2, col3 = st.columns(3)
    def start_game(raw, name):
        lines = [l.strip() for l in raw.strip().split('\n') if l.strip()]
        st.session_state.current_df = pd.DataFrame([l.split(',', 2) for l in lines], columns=["英文", "音標", "中文"])
        st.session_state.unit_name = name
        st.session_state.remaining_indices = list(range(len(st.session_state.current_df)))
        random.shuffle(st.session_state.remaining_indices)
        st.session_state.idx = st.session_state.remaining_indices.pop(0)
        st.session_state.start_time = time.time()
        st.session_state.page = "study"
        st.rerun()

    with col1:
        if st.button("🐸 第一單元"): start_game(U1_RAW, "第一單元")
    with col2:
        if st.button("🐿️ 第二單元"): start_game(U2_RAW, "第二單元")
    with col3:
        if st.button("🦁 第三單元"): start_game(U3_RAW, "第三單元")

# --- 挑戰頁 (加入解鎖邏輯) ---
elif st.session_state.page == "study":
    elapsed = int(time.time() - st.session_state.start_time)
    st.write(f"⏱️ 時間：{elapsed}s | 📍 {st.session_state.unit_name}")
    
    row = st.session_state.current_df.iloc[st.session_state.idx]
    current_word = row['英文'].strip()

    if st.session_state.get('success_trigger', False):
        st.success("🎯 Correct!")
        time.sleep(0.5)
        if not st.session_state.remaining_indices:
            # --- 重點：解鎖角色邏輯 ---
            char_info = CHARACTERS[st.session_state.unit_name]
            if char_info['name'] not in st.session_state.unlocked_chars:
                st.session_state.unlocked_chars.append(char_info['name'])
                st.balloons()
                st.snow()
                st.markdown(f"""
                    <div style="background-color:#FFF9C4; padding:20px; border-radius:15px; border:2px solid #FBC02D; text-align:center;">
                        <h2>🎉 新夥伴加入！</h2>
                        <h1 style="font-size: 4rem;">{char_info['name']}</h1>
                        <p>{char_info['desc']}</p>
                    </div>
                """, unsafe_allow_html=True)
                time.sleep(4)
            st.session_state.page = "cover"
        else:
            st.session_state.idx = st.session_state.remaining_indices.pop(0)
        st.session_state.success_trigger = False
        st.rerun()

    # (中間拼字與表單邏輯與之前相同...)
    st.info(f"💡 中文提示：{row['中文']}")
    if st.button("🔊 聽發音"): text_to_speech(current_word)
    
    with st.form(key="quiz", clear_on_submit=True):
        user_in = st.text_input("輸入拼音").strip()
        if st.form_submit_button("送出"):
            if user_in.lower() == current_word.lower():
                st.session_state.success_trigger = True
                st.rerun()
            else:
                st.error(f"❌ 答錯了！答案是 {current_word}")
                st.session_state.remaining_indices.append(st.session_state.idx)
                time.sleep(1)
                st.session_state.idx = st.session_state.remaining_indices.pop(0)
                st.rerun()
