import streamlit as st
import pandas as pd
import random
import time
import base64

# 1. 基礎設定
st.set_page_config(page_title="萌萌言語森林", page_icon="🐾", layout="centered")

# 2. 介面美化 CSS
st.markdown("""
    <style>
    .stApp { background-color: #F1F8E9; }
    /* 讓輸入框大一點，雖然是明文但盡力關閉建議 */
    input {
        font-size: 1.2rem !important;
        autocomplete: off !important;
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

# 3. 資料庫
U1_RAW = """ignore,[ɪgˋnor],忽視\nill,[ɪl],生病的\nimagine,[ɪˋmædʒɪn],想像\nimportance,[ɪmˋpɔrtns],重要性\nimprove,[ɪˋpruvmənt],改善\ninclude,[ɪnˋklud],包含\nincome,[ˋɪn͵kʌm],收入\nincrease,[ɪnˋkris],增加\nindependence,[͵ɪndɪˋpɛndəns],獨立\nindependent,[͵ɪndɪˋpɛndənt],獨立的\nindicate,[ˋɪndə͵ket],指出\nindustry,[ˋɪndəstrɪ],工業\ninfluence,[ˋɪnflʊəns],影響\nink,[ɪŋk],墨水\ninsect,[ˋɪnsɛkt],昆蟲\ninsist,[ɪnˋsɪst],堅持\ninstance,[ˋɪnstəns],例子\ninstant,[ˋɪnstənt],即刻的\ninstrument,[ˋɪnstrəmənt],儀器/樂器\ninternational,[͵ɪntɚˋnæʃən!],國際性的\ninterview,[ˋɪntɚ͵vju],訪談\nintroduce,[͵ɪntrəˋdjus],介紹\ninvent,[ɪnˋvɛnt],發明\ninvitation,[͵ɪnvəˋteʃən],邀請\ninvite,[ɪnˋvaɪt],邀請\nisland,[ˋaɪlənd],島\nitem,[ˋaɪtəm],項目\njacket,[ˋdʒækɪt],夾克\njam,[dʒæm],塞滿/果醬\njazz,[dʒæz],爵士樂\njeans,[dʒinz],牛仔褲\njeep,[dʒip],吉普車\njog,[dʒɑg],慢跑\njoint,[dʒɔɪnt],關節\njudge,[dʌdʒ],法官/判決\njuicy,[ˋdʒusɪ],多汁的\nketchup,[ˋkɛtʃəp],番茄醬\nkindergarten,[ˋkɪndɚ͵gɑrtn],幼稚園\nkingdom,[ˋkɪŋdəm],王國\nknock,[nɑk],相撞/敲門\nknowledge,[ˋnɑlɪdʒ],知識\nkoala,[koˋɑlə],無尾熊\nladybug,[ˋledɪ͵bʌg],瓢蟲"""
U2_RAW = """lane,[len],小路\nlanguage,[ˋlæŋgwɪdʒ],語言\nlantern,[ˋlæntɚn],燈籠\nlap,[læp],重疊部分\nlatest,[ˋletɪst],最新的\nlawyer,[ˋlɔjɚ],律師\nleadership,[ˋlidɚʃɪp],領導\nlegal,[ˋlig!],法律上的\nlemon,[ˋlɛmən],檸檬\nlemonade,[͵lɛmənˋed],檸檬水\nlend,[lɛnd],把……借給\nlength,[lɛŋθ],長度\nleopard,[ˋlɛpɚd],豹\nlettuce,[ˋlɛtɪs],萵苣\nlibrary,[ˋlaɪ͵brɛrɪ],圖書館\nlick,[lɪk],舔\nlid,[lɪd],蓋子\nlightning,[ˋlaɪtnɪŋ],閃電\nlimit,[ˋlɪmɪt],界限/限制\nlink,[lɪŋk],聯繫\nliquid,[ˋlɪkwɪd],液體\nlistener,[ˋlɪsnɚ],傾聽者\nloaf,[lof],一條\nlocal,[ˋlok!],地方性的\nlocate,[loˋket],確定……的地點\nlock,[lɑk],鎖\nlog,[lɔg],圓木\nlone,[lon],孤單的\nlonely,[ˋlonlɪ],孤獨的\nlose,[luz],丟失\nloser,[ˋluzɚ],失敗者\nloss,[lɔs],遺失\nlovely,[ˋlʌvlɪ],可愛的\nlover,[ˋlʌvɚ],戀人\nlower,[ˋloɚ],較低的\nluck,[lʌk],運氣\nmagazine,[͵mægəˋzin],雜誌\nmagic,[ˋmædʒɪk],魔法\nmagician,[məˋdʒɪʃən],魔術師\nmain,[men],主要的\nmaintain,[menˋten],保持\nmale,[mel],男性\nMandarin,[ˋmændərɪn],華語"""
U3_RAW = """mango,[ˋmæŋgo],芒果\nmanner,[ˋmænɚ],方法/舉止\nmark,[mɑrk],標記/痕跡\nmarriage,[ˋmærɪdʒ],婚姻\nmask,[mæsk],口罩/假面具\nmass,[mæsk],大眾的/眾多\nmat,[mæt],墊子\nmatch,[mætʃ],相配/比賽\nmate,[met],伙伴\nmaterial,[məˋtɪrɪəl],材料\nmeal,[mil],一餐\nmeaning,[ˋminɪŋ],含義\nmeans,[minz],手段/方法\nmeasurable,[ˋmɛʒərəb!],可測量的\nmeasure,[ˋmɛʒɚ],測量\nmedicine,[ˋmɛdəsn],藥\nmeeting,[ˋmitɪŋ],會議\nmelody,[ˋmɛlədɪ],旋律\nmelon,[ˋmɛlən],瓜\nmember,[ˋmɛmbɚ],成員\nmemory,[ˋmɛmərɪ],記憶\nmenu,[ˋmɛnju],菜單\nmessage,[ˋmɛsɪdʒ],消息\nmetal,[ˋmɛt!],金屬\nmeter,[ˋmitɚ],計量器\nmethod,[ˋmɛθəd],方法\nmilitary,[ˋmɪlə͵tɛrɪ],軍事的\nmillion,[ˋmɪljən],百萬\nmine,[maɪn],我的/礦山\nminus,[ˋmaɪnəs],減去/負的\nmirror,[ˋmɪrɚ],鏡子\nmix,[mɪks],混和\nmodel,[ˋmɑd!],模型\nmodern,[ˋmɑdɚn],現代的\nmonster,[ˋmɑnstɚ],怪物\nmosquito,[məsˋkito],蚊子\moth,[mɔθ],蛾\nmotion,[ˋmoʃən],姿態/示意\nmotorcycle,[ˋmotɚ͵saɪk!],摩托車\nmovable,[ˋmuvəb!],可移動的\nMRT,[MRT],大眾捷運系統\nsubway,[ˋsʌb͵we],地下鐵\nunderground,[ˋʌndɚ͵graʊnd],地下鐵\nmetro,[ˋmɛtro],地鐵\nmule,[mjul],騾"""

def parse_data(raw):
    lines = [l.strip() for l in raw.strip().split('\n') if l.strip()]
    return pd.DataFrame([l.split(',') for l in lines], columns=["英文", "音標", "中文"])

# 語音核心：改用 iframe 觸發或更直接的播放方式
def text_to_speech(text):
    word = text.replace(" ", "%20")
    tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={word}&tl=en&client=tw-ob"
    # 使用 Iframe 或是 Audio 標籤，並加上隨機數確保每次都觸發
    st.components.v1.html(f"""
        <audio id="audio_player" src="{tts_url}" type="audio/mpeg"></audio>
        <script>
            var audio = document.getElementById('audio_player');
            audio.play().catch(function(error) {{
                console.log("播放失敗:", error);
                // 備用方案：如果自動播放失敗，提示用戶
            }});
        </script>
    """, height=0)

if 'page' not in st.session_state: st.session_state.page = "cover"
if 'show_cn' not in st.session_state: st.session_state.show_cn = True
if 'show_ipa' not in st.session_state: st.session_state.show_ipa = True

# --- 封面選單 (包含書籤) ---
if st.session_state.page == "cover":
    st.markdown('<p class="cute-title">🐾 拼字森林挑戰 🌲</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    def start_game(raw, name):
        st.session_state.current_df = parse_data(raw)
        st.session_state.unit_name = name
        st.session_state.remaining_indices = list(range(len(st.session_state.current_df)))
        st.session_state.idx = st.session_state.remaining_indices.pop(random.randrange(len(st.session_state.remaining_indices)))
        st.session_state.score = 0
        st.session_state.page = "study"
        st.rerun()

    with col1:
        if st.button("🌱 第一單元"): start_game(U1_RAW, "第一單元")
    with col2:
        if st.button("🌿 第二單元"): start_game(U2_RAW, "第二單元")
    with col3:
        if st.button("🌳 第三單元"): start_game(U3_RAW, "第三單元")

    st.divider()
    st.write("### 📖 森林單字書籤")
    tab1, tab2, tab3 = st.tabs(["第一單元", "第二單元", "第三單元"])
    with tab1: st.dataframe(parse_data(U1_RAW), hide_index=True, use_container_width=True)
    with tab2: st.dataframe(parse_data(U2_RAW), hide_index=True, use_container_width=True)
    with tab3: st.dataframe(parse_data(U3_RAW), hide_index=True, use_container_width=True)

# --- 拼字挑戰 ---
elif st.session_state.page == "study":
    c_back, c_t1, c_t2 = st.columns([1, 1, 1])
    with c_back:
        if st.button("⬅️ 返回"): st.session_state.page = "cover"; st.rerun()
    with c_t1: st.session_state.show_cn = st.toggle("顯示中文", value=st.session_state.show_cn)
    with c_t2: st.session_state.show_ipa = st.toggle("顯示音標", value=st.session_state.show_ipa)

    row = st.session_state.current_df.iloc[st.session_state.idx]
    current_word = row['英文'].strip()

    st.write(f"🌟 **{st.session_state.unit_name}** | 進度：{st.session_state.score} / {len(st.session_state.current_df)}")
    st.progress(min(st.session_state.score / len(st.session_state.current_df), 1.0))

    if st.session_state.get('success_trigger', False):
        st.balloons()
        st.success(f"🎯 答對了！答案：{current_word}")
        time.sleep(1.2)
        if not st.session_state.remaining_indices:
            st.session_state.page = "cover"
        else:
            st.session_state.idx = st.session_state.remaining_indices.pop(random.randrange(len(st.session_state.remaining_indices)))
        st.session_state.success_trigger = False
        st.rerun()

    with st.container():
        if st.session_state.show_cn: st.info(f"💡 中文：{row['中文']}")
        else: st.info("💡 中文已隱藏")

        c_ipa_val, c_play_btn = st.columns([3, 1])
        with c_ipa_val:
            if st.session_state.show_ipa: st.write(f"🎧 音標：{row['音標']}")
            else: st.write("🎧 音標已隱藏")
        with c_play_btn:
            # 這裡我們換一個觸發語音的方式
            if st.button("🔊 播放", key=f"p_{time.time()}"):
                text_to_speech(current_word)

        # 改回明文輸入框 (移除 type="password")
        d_key = f"input_text_{st.session_state.score}_{st.session_state.idx}"
        with st.form(key=f"form_{d_key}", clear_on_submit=True):
            user_input = st.text_input(
                "拼寫單字", 
                value="",
                label_visibility="collapsed", 
                placeholder="請拼出單字...", 
                key=d_key,
                autocomplete="off" # 嘗試關閉自動完成
            ).strip()
            if st.form_submit_button("檢查答案 ✨"):
                if user_input.lower() == current_word.lower():
                    st.session_state.score += 1
                    st.session_state.success_trigger = True
                    st.rerun()
                else:
                    st.error("❌ 再試一次唷！")
    
