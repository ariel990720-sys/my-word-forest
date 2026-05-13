import streamlit as st
import random

# 1. 頁面設定與美化
st.set_page_config(page_title="10B 尋夢單字挑戰", layout="centered")
st.markdown("""
    <style>
    .stTextInput>div>div>input { font-size: 24px; text-align: center; }
    .vocab-card { background-color: #f0f2f6; padding: 30px; border-radius: 15px; border-left: 10px solid #2196f3; text-align: center; margin: 20px 0; }
    .word-text { font-size: 48px; font-weight: bold; color: #0d47a1; }
    .status-text { font-size: 14px; color: #666; }
    </style>
""", unsafe_allow_html=True)

# 2. 初始化 Session State
if 'vocab_list' not in st.session_state:
    st.session_state.vocab_list = []      # 原始清單
    st.session_state.current_round = []   # 目前這輪要考的
    st.session_state.wrong_list = []      # 答錯待補考
    st.session_state.current_pair = None  # 目前題目
    st.session_state.is_started = False
    st.session_state.finished = False

# 3. 處理邏輯函數
def start_game(input_text):
    pairs = []
    for line in input_text.split('\n'):
        if ',' in line:
            eng, chi = line.split(',', 1)
            pairs.append({'eng': eng.strip(), 'chi': chi.strip()})
    
    if pairs:
        st.session_state.vocab_list = pairs
        st.session_state.current_round = random.sample(pairs, len(pairs))
        st.session_state.wrong_list = []
        st.session_state.current_pair = st.session_state.current_round.pop(0)
        st.session_state.is_started = True
        st.session_state.finished = False

def check_answer():
    user_ans = st.session_state.user_input.strip()
    correct_ans = st.session_state.current_pair['chi']
    
    if user_ans == correct_ans:
        st.toast("✅ 太棒了！答對了", icon="🎉")
    else:
        st.error(f"❌ 答錯囉！正確答案是：{correct_ans}")
        st.session_state.wrong_list.append(st.session_state.current_pair)
    
    # 準備下一題
    if st.session_state.current_round:
        st.session_state.current_pair = st.session_state.current_round.pop(0)
    else:
        # 當這輪考完，檢查有沒有錯題要進入下一輪
        if st.session_state.wrong_list:
            st.warning("⚠️ 第一輪結束，準備開始複習答錯的單字！")
            st.session_state.current_round = random.sample(st.session_state.wrong_list, len(st.session_state.wrong_list))
            st.session_state.wrong_list = []
            st.session_state.current_pair = st.session_state.current_round.pop(0)
        else:
            st.session_state.finished = True
            st.session_state.is_started = False
    
    st.session_state.user_input = "" # 清空輸入框

# 4. 畫面顯示
st.title("🎓 10B 尋夢單字挑戰")

if not st.session_state.is_started and not st.session_state.finished:
    st.subheader("第一步：輸入單字清單")
    input_data = st.text_area("格式請用「英文,中文」(每行一個)", "apple,蘋果\nbanana,香蕉\ncomputer,電腦", height=200)
    if st.button("🚀 開始挑戰", use_container_width=True):
        start_game(input_data)
        st.rerun()

elif st.session_state.is_started:
    # 顯示目前進度
    total_left = len(st.session_state.current_round) + 1
    wrong_count = len(st.session_state.wrong_list)
    st.markdown(f"<div class='status-text'>剩餘題目：{total_left} | 本輪錯題積累：{wrong_count}</div>", unsafe_allow_html=True)
    
    # 出題區
    st.markdown(f"""
        <div class="vocab-card">
            <div class="word-text">{st.session_state.current_pair['eng']}</div>
            <div style="margin-top:10px; color:#555;">請輸入對應的中文</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.text_input("在此輸入答案...", key="user_input", on_change=check_answer)
    st.info("提示：輸入完直接按 Enter 即可檢查並跳下一題")

elif st.session_state.finished:
    st.balloons()
    st.success("🎊 恭喜！你已經掌握了所有單字！")
    if st.button("重新開始新挑戰"):
        st.session_state.clear()
        st.rerun()
