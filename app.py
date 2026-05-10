import streamlit as st
import pandas as pd
import random
import time
import requests
import streamlit.components.v1 as components
from streamlit_lottie import st_lottie

# 1. 基礎設定
st.set_page_config(page_title="萌萌言語森林", page_icon="🐾", layout="centered")

# 2. 強效封殺建議 CSS (維持黑科技防禦，保護輸入隱私)
st.markdown("""
    <style>
    .stApp { background-color: #F1F8E9; }
    
    /* 強制關閉自動完成 */
    input {
        autocomplete: off !important;
        -webkit-autocomplete: off !important;
        -moz-autocomplete: off !important;
    }

    /* 終極防禦：讓 Password 類型的輸入框顯示為正常文字，防止瀏覽器記錄與建議 */
    input[type="password"] {
        -webkit-text-security: none !important;
        font-family: 'monospace' !important;
        font-size: 1.2rem !important;
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

# 3. 第三單元資料庫 (依據你提供的最新清單)
LEVEL_3_WORDS = """
mango,[ˋmæŋgo],芒果
manner,[ˋmænɚ],方法/舉止
mark,[mɑrk],標記/痕跡
marriage,[ˋmærɪdʒ],婚姻
mask,[mæsk],口罩/假面具
mass,[mæsk],大眾的/眾多
mat,[mæt],墊子
match,[mætʃ],相配/比賽
mate,[met],伙伴
material,[məˋtɪrɪəl],材料
meal,[mil],一餐
meaning,[ˋminɪŋ],含義
means,[minz],手段/方法
measurable,[ˋmɛʒərəb!],可測量的
measure,[ˋmɛʒɚ],測量
medicine,[ˋmɛdəsn],藥
meeting,[ˋmitɪŋ],會議
melody,[ˋmɛlədɪ],旋律
melon,[ˋmɛlən],瓜
member,[ˋmɛmbɚ],成員
memory,[ˋmɛmərɪ],記憶
menu,[ˋmɛnju],菜單
message,[ˋmɛsɪdʒ],消息
metal,[ˋmɛt!],金屬
meter,[ˋmitɚ],計量器
method,[ˋmɛθəd],方法
military,[ˋmɪlə͵tɛrɪ],軍事的
million,[ˋmɪljən],百萬
mine,[maɪn],我的/礦山
minus,[ˋmaɪnəs],減去/負的
mirror,[ˋmɪrɚ],鏡子
mix,[mɪks],混和
model,[ˋmɑd!],模型
modern,[ˋmɑdɚn],現代的
monster,[ˋmɑnstɚ],怪物
mosquito,[məsˋkito],蚊子
moth,[mɔθ],蛾
motion,[ˋmoʃən],姿態/示意
motorcycle,[ˋmotɚ͵saɪk!],摩托車
movable,[ˋmuvəb!],可移動的
MRT,[MRT],大眾捷運系統
subway,[ˋsʌb͵we],地下鐵
underground,[ˋʌndɚ͵graʊnd],地下鐵
metro,[ˋmɛtro],地鐵
mule,[mjul],騾
"""

@st.cache_data
def load_data():
    lines = [l.strip() for l in LEVEL_3_WORDS.strip().split('\n') if l.strip()]
    data = [l.split(',') for l in lines]
    return pd.DataFrame(data, columns=["en", "ipa", "cn"])

def text_to_speech(text):
    # 針對 MRT 等縮寫做語音優化
    text_for_speech = text.replace("MRT", "M R T")
    js = f"<script>var m = new SpeechSynthesisUtterance('{text_for_speech}'); m.lang='en-US'; window.speechSynthesis.speak(m);</script>"
    components.html(js, height=0)

@st.cache_data
def get_lottie(url):
    try: return requests.get(url).json()
    except: return None

bear_anim = get_lottie("https://assets10.lottiefiles.com/packages/lf20_stfayfky.json")
df_all = load_data()

if 'page' not in st.session_state: st.session_state.page = "cover"

# --- 封面 ---
if st.session_state.page == "cover":
    st.markdown('<p class="cute-title">🐾 第三單元：拼字森林 🌲</p>', unsafe_allow_html=True)
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    
    if st.button(f"🌟 開始挑戰第三單元 ({len(df_all)}字) 🌟", use_container_width=True):
        st.session_state.current_df = df_all.copy()
        st.session_state.remaining_indices = list(range(len(st.session_state.current_df)))
        st.session_state.idx = st.session_state.remaining_indices.pop(random.randrange(len(st.session_state.remaining_indices)))
        st.session_state.score = 0
        st.session_state.page = "study"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- 拼字挑戰模式 ---
elif st.session_state.page == "study":
    if st.button("⬅️ 返回選單"):
        st.session_state.page = "cover"
        st.rerun()

    df = st.session_state.current_df
    row = df.iloc[st.session_state.idx]
    current_word = row['en'].strip()

    st.write(f"🌟 達成進度：{st.session_state.score} / {len(df)}")
    st.progress(min(st.session_state.score / len(df), 1.0))

    if st.session_state.get('success_trigger', False):
        if bear_anim: st_lottie(bear_anim, height=120, key=f"win_{st.session_state.score}")
        st.balloons()
        st.success(f"答對了！答案就是 {current_word}")
        time.sleep(1.2)
        
        if not st.session_state.remaining_indices:
            st.warning("🎉 第三單元圓滿達成！")
            time.sleep(2)
            st.session_state.page = "cover"
        else:
            st.session_state.idx = st.session_state.remaining_indices.pop(random.randrange(len(st.session_state.remaining_indices)))
            
        st.session_state.success_trigger = False
        st.rerun()

    with st.container():
        st.info(f"💡 中文意思：{row['cn']}")
        c1, c2 = st.columns([3, 1])
        with c1: st.write(f"🎧 音標：{row['ipa']}")
        with c2: 
            if st.button("🔊 播放"): text_to_speech(current_word)

        # 核心防禦：動態 ID + Password 類型，防止鍵盤記憶
        d_key = f"v3_input_{st.session_state.score}_{st.session_state.idx}"
        
        with st.form(key=f"form_{d_key}", clear_on_submit=True):
            user_input = st.text_input(
                "Spell", 
                type="password", 
                label_visibility="collapsed", 
                placeholder="在此拼出單字...",
                key=d_key
            ).strip()
            
            # 拼字檢查 (不分大小寫)
            if st.form_submit_button("檢查 ✨"):
                if user_input.lower() == current_word.lower():
                    st.session_state.score += 1
                    st.session_state.success_trigger = True
                    st.rerun()
                else:
                    st.error("❌ 拼錯囉，再接再厲！")
