import streamlit as st
import pandas as pd
import random
import time
import streamlit.components.v1 as components

# 1. 基礎設定
st.set_page_config(page_title="言語森林", page_icon="🐾", layout="centered")

# 2. 介面美化
st.markdown("""
    <style>
    .stApp { background-color: #F1F8E9; }
    .cute-title { font-size: 2.5rem; color: #388E3C; text-align: center; font-weight: bold; margin-bottom: 20px; }
    .status-box { padding: 10px; border-radius: 10px; background-color: #E8F5E9; border-left: 5px solid #4CAF50; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 3. 資料庫
U1_RAW = """ignore,[ɪgˋnor],忽視\nill,[ɪl],生病的\nimagine,[ɪˋmædʒɪn],想像\nimportance,[ɪmˋpɔrtns],重要性\nimprove,[ɪˋpruvmənt],改善\ninclude,[ɪnˋklud],包含\nincome,[ˋɪn͵kʌm],收入\nincrease,[ɪnˋkris],增加\nindependence,[͵ɪndɪˋpɛndəns],獨立\nindependent,[͵ɪndɪˋpɛndnt],獨立的\nindicate,[ˋɪndə͵ket],指出\nindustry,[ˋɪndəstrɪ],工業\ninfluence,[ˋɪnflʊəns],影響\nink,[ɪŋk],墨水\ninsect,[ˋɪnsɛkt],昆蟲\ninsist,[ɪnˋsɪst],堅持\ninstance,[ˋɪnstəns],例子\ninstant,[ˋɪnstənt],即刻的\ninstrument,[ˋɪnstrəmənt],儀器/樂器\ninternational,[͵ɪntɚˋnæʃən!],國際性的\ninterview,[ˋɪntɚ͵vju],訪談\nintroduce,[͵ɪntrəˋdjus],介紹\ninvent,[ɪnˋvɛnt],發明\ninvitation,[͵ɪnvəˋteʃən],邀請\ninvite,[ɪnˋvaɪt],邀請\nisland,[ˋaɪlənd],島\nitem,[ˋaɪtəm],項目\njacket,[ˋdʒækɪt],夾克\njam,[dʒæm],塞滿/果醬\njazz,[dʒæz],爵士樂\njeans,[dʒinz],牛仔褲\njeep,[dʒip],夾克\njog,[dʒɑg],慢跑\njoint,[dʒɔɪnt],關節\njudge,[dʌdʒ],法官/判決\njuicy,[ˋdʒusɪ],多汁的\nketchup,[ˋkɛtʃəp],番茄醬\nkindergarten,[ˋkɪndɚ͵gɑrtn],幼稚園\nkingdom,[ˋkɪŋdəm],王國\nknock,[nɑk],相撞/敲門\nknowledge,[ˋnɑlɪdʒ],知識\nkoala,[koˋɑlə],無尾熊\nladybug,[ˋledɪ͵bʌg],瓢蟲"""
U2_RAW = """lane,[len],小路\nlanguage,[ˋlæŋgwɪdʒ],語言\nlantern,[ˋlæntɚn],燈籠\nlap,[læp],重疊部分\nlatest,[ˋletɪst],最新的\nlawyer,[ˋlɔjɚ],律師\nleadership,[ˋlidɚʃɪp],領導\nlegal,[ˋlig!],法律上的\nlemon,[ˋlɛmən],檸檬\nlemonade,[͵lɛmənˋed],檸檬水\nlend,[lɛnd],把……借給\nlength,[lɛŋθ],長度\nleopard,[ˋlɛpɚd],豹\nlettuce,[ˋlɪs],萵苣\nlibrary,[ˋlaɪ͵brɛrɪ],圖書館\nlick,[lɪk],舔\nlid,[lɪd],蓋子\nlightning,[ˋlaɪtnɪŋ],閃電\nlimit,[ˋlɪmɪt],界限/限制\nlink,[lŋk],聯繫\nliquid,[ˋlɪkwɪd],液體\nlistener,[ˋlɪsnɚ],傾聽者\nloaf,[lof],一條\nlocal,[ˋlok!],地方性的\nlocate,[loˋket],確定……的地點\nlock,[lɑk],鎖\nlog,[lɔg],圓木\nlone,[lon],孤單的\nlonely,[ˋlonlɪ],孤獨的\nlose,[luz],丟失\nloser,[ˋluzɚ],失敗者\nloss,[lɔs],遺失\nlovely,[ˋlʌvlɪ],可愛的\nlover,[ˋlʌvɚ],戀人\nlower,[ˋloɚ],較低的\nluck,[lʌk],運氣\nmagazine,[͵mægəˋzin],雜誌\nmagic,[ˋmædʒɪk],魔法\nmagician,[məˋdʒɪʃən],魔術師\nmain,[men],主要的\nmaintain,[menˋten],保持\nmale,[mel],男性\nMandarin,[ˋmændərɪn],華語"""
U3_RAW = """mango,[ˋmæŋgo],芒果\nmanner,[ˋmænɚ],方法/舉止\nmark,[mɑrk],標記/痕跡\nmarriage,[ˋmærɪdʒ],婚姻\nmask,[mæsk],口罩/假面具\nmass,[mæs],大眾的\nmat,[mæt],墊子\nmatch,[mætʃ],相配/比賽\nmate,[met],夥伴\nmaterial,[məˋtɪrɪəl],材料\nmeal,[mil],一餐\nmeaning,[ˋminɪŋ],含義\nmeans,[minz],手段\nmeasurable,[ˋmɛʒərəb!],可測量的\nmeasure,[ˋmɛʒɚ],測量\nmedicine,[ˋmɛdəsn],藥\nmeeting,[ˋmitɪŋ],會議\nmelody,[ˋmɛlədɪ],旋律\nmelon,[ˋmɛlən],瓜\nmember,[ˋmɛmbɚ],成員\nmemory,[ˋmɛmərɪ],記憶\nmenu,[ˋmɛnju],菜單\nmessage,[ˋmɛsɪdʒ],消息\nmetal,[ˋmɛt!],金屬\nmeter,[ˋmitɚ],計量器\nmethod,[ˋmɛθəd],方法\nmilitary,[ˋmɪlə͵tɛrɪ],軍事的\nmillion,[ˋmɪljən],百萬\nmine,[maɪn],我的\nminus,[ˋmaɪnəs],減去\nmirror,[ˋmɪrɚ],鏡子\nmix,[mɪks],混和\nmodel,[ˋmɑd!],模型\nmodern,[ˋmɑdɚn],現代的\nmonster,[ˋmɑnstɚ],怪物\nmosquito,[məsˋkito],蚊子\nmoth,[mɔθ],蛾\nmotion,[ˋmoʃən],姿態\nmotorcycle,[ˋmotɚ͵saɪk!],摩托車\nmovable,[ˋmuvəb!],可移動的\nMRT,[MRT],大眾捷運系統\nsubway,[ˋsʌb͵we],地下鐵\nunderground,[ˋʌndɚ͵graʊnd],地下鐵\nmetro,[ˋmɛtro],地鐵\nmule,[mjul],騾"""

def parse_data(raw):
    lines = [l.strip() for l in raw.strip().split('\n') if l.strip()]
    return [l.split(',', 2) for l in lines]

def text_to_speech(text):
    text = text.replace("'", "\\'")
    rand_id = random.randint(1, 1000000)
    js = f"""
    <div id="tts_{rand_id}">
        <script>
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance('{text}');
            msg.lang = 'en-US';
            window.speechSynthesis.speak(msg);
        </script>
    </div>
    """
    components.html(js, height=0)

# 初始化狀態
if 'page' not in st.session_state: st.session_state.page = "cover"
if 'quiz_list' not in st.session_state: st.session_state.quiz_list = []
if 'current_q' not in st.session_state: st.session_state.current_q = None

# --- 封面頁 ---
if st.session_state.page == "cover":
    st.markdown('<p class="cute-title">🐾 單字學習 🌲</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    def init_quiz(raw, name):
        data = parse_data(raw)
        random.shuffle(data)
        st.session_state.quiz_list = data # 這是我們的待練習清單
        st.session_state.unit_name = name
        st.session_state.total_count = len(data)
        st.session_state.page = "quiz"
        st.session_state.current_q = st.session_state.quiz_list.pop(0)
        st.rerun()

    with col1:
        if st.button("🌱 第一單元"): init_quiz(U1_RAW, "第一單元")
    with col2:
        if st.button("🌿 第二單元"): init_quiz(U2_RAW, "第二單元")
    with col3:
        if st.button("🌳 第三單元"): init_quiz(U3_RAW, "第三單元")

# --- 挑戰頁 ---
elif st.session_state.page == "quiz":
    st.write(f"📖 **{st.session_state.unit_name}**")
    
    # 顯示剩餘數量
    rem_count = len(st.session_state.quiz_list) + 1
    st.markdown(f"""<div class="status-box">🏃 剩餘單字數：<b>{rem_count}</b></div>""", unsafe_allow_html=True)

    q = st.session_state.current_q
    word, ipa, mean = q[0], q[1], q[2]

    # 顯示英文，要求中文 (或是反過來，這邊設定為顯示英文)
    st.subheader(f"請輸入此單字的中文：")
    st.title(f"👉 {word}")
    st.write(f"🎧 {ipa}")

    if st.button("🔊 聽發音"):
        text_to_speech(word)

    # 輸入框
    with st.form(key="ans_form", clear_on_submit=True):
        user_ans = st.text_input("輸入中文意思：").strip()
        submit = st.form_submit_button("送出答案")

    if submit:
        # 簡單判定：只要輸入的字有出現在中文解釋裡就算對（例如「忽視」對應「忽視」）
        if user_ans in mean or mean in user_ans:
            st.success("✅ 答對了！移除單字。")
            time.sleep(0.8)
            if st.session_state.quiz_list:
                st.session_state.current_q = st.session_state.quiz_list.pop(0)
                st.rerun()
            else:
                st.balloons()
                st.success("🎉 太強了！所有單字都背完了！")
                time.sleep(2)
                st.session_state.page = "cover"
                st.rerun()
        else:
            st.error(f"❌ 答錯了！正確答案是：{mean}")
            st.info("此單字已移至隊伍最後方，待會會再看到它。")
            # 答錯了：把這題塞回清單的最後面，形成循環
            st.session_state.quiz_list.append(q) 
            time.sleep(1.5)
            if st.session_state.quiz_list:
                st.session_state.current_q = st.session_state.quiz_list.pop(0)
                st.rerun()

    if st.button("⬅️ 放棄返回"):
        st.session_state.page = "cover"
        st.rerun()
