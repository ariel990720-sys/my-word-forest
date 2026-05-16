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
    .cute-title { font-size: 2.5rem; color: #388E3C; text-align: center; font-weight: bold; }
    .review-tag { 
        color: #D32F2F; background-color: #FFEBEE; padding: 5px 10px; 
        border-radius: 5px; font-weight: bold; border: 1px solid #FFCDD2;
    }
    .combo-box {
        font-size: 1.5rem; color: #FF9800; font-weight: bold; text-align: center;
    }
    .stat-box {
        padding: 20px; background-color: #FFFFFF; border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; margin-bottom: 20px;
    }
    .badge {
        font-size: 1.8rem; color: #2E7D32; font-weight: bold; margin-top: 10px;
    }
    .study-card {
        padding: 30px; background-color: #FFFFFF; border-radius: 15px;
        border-left: 8px solid #4CAF50; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 資料庫
U1_RAW = """ignore,[ɪgˋnor],忽視\nill,[ɪl],生病的\nimagine,[ɪˋmædʒɪn],想像\nimportance,[ɪmˋpɔrtns],重要性\nimprove,[ɪmˋpruv],改善\ninclude,[ɪnˋklud],包含\nincome,[ˋɪn͵kʌm],收入\nincrease,[ɪnˋkris],增加\nindependence,[͵ɪndɪˋpɛndəns],獨立\nindependent,[͵ɪndɪˋpɛndənt],獨立的\nindicate,[ˋɪndə͵ket],指出\nindustry,[ˋɪndəstrɪ],工業\ninfluence,[ˋɪnflʊəns],影響\nink,[ɪŋk],墨水\ninsect,[ˋɪnsɛkt],昆蟲\ninsist,[ɪnˋsɪst],堅持\ninstance,[ˋɪnstəns],例子\ninstant,[ˋɪnstənt],即刻的\ninstrument,[ˋɪnstrəmənt],儀器/樂器\ninternational,[͵ɪntɚˋnæʃən!],國際性的\ninterview,[ˋɪntɚ͵vju],訪談\nintroduce,[͵ɪntrəˋdjus],介紹\ninvent,[ɪnˋvɛnt],發明\ninvitation,[͵ɪnvəˋteʃən],邀請\ninvite,[ɪnˋvaɪt],邀請\nisland,[ˋaɪlənd],島\nitem,[ˋaɪtəm],項目\njacket,[ˋdʒækɪt],夾克\njam,[dʒæm],塞滿/果醬\njazz,[dʒæz],爵士樂\njeans,[dʒinz],牛仔褲\njeep,[dʒip],吉普車\njog,[dʒɑg],慢跑\njoint,[dʒɔɪnt],關節\njudge,[dʌdʒ],法官/判決\njuicy,[ˋdʒusɪ],多汁的\nketchup,[ˋkɛtʃəp],番茄醬\nkindergarten,[ˋkɪndɚ͵gɑrtn],幼稚園\nkingdom,[ˋkɪŋdəm],王國\nknock,[nɑk],相撞/敲門\nknowledge,[ˋnɑlɪdʒ],知識\nkoala,[koˋɑlə],無尾熊\nladybug,[ˋledɪ͵bʌg],瓢蟲"""
U2_RAW = """lane,[len],小路\nlanguage,[ˋlæŋgwɪdʒ],語言\nlantern,[ˋlæntɚn],燈籠\nlap,[læp],重疊部分\nlatest,[ˋletɪst],最新的\nlawyer,[ˋlɔjɚ],律師\nleadership,[ˋlidɚʃɪp],領導\nlegal,[ˋlig!],法律上的\nlemon,[ˋlɛmən],檸檬\nlemonade,[͵lɛmənˋed],檸檬水\nlend,[lɛnd],把……借給\nlength,[lɛŋθ],長度\nleopard,[ˋlɛpɚd],豹\nlettuce,[ˋlɪs],萵苣\nlibrary,[ˋlaɪ͵brɛrɪ],圖書館\nlick,[lɪk],舔\nlid,[lɪd],蓋子\nlightning,[ˋlaɪtnɪŋ],閃電\nlimit,[ˋlɪmɪt],界限/限制\nlink,[lɪŋk],聯繫\nliquid,[ˋlɪkwɪd],液體\nlistener,[ˋlɪsnɚ],傾聽者\nloaf,[lof],一條\nlocal,[ˋlok!],地方性的\nlocate,[loˋket],確定……的地點\nlock,[lɑk],鎖\nlog,[lɔg],圓木\nlone,[lon],孤單的\nlonely,[ˋlonlɪ],孤獨的\nlose,[luz],丟失\nloser,[ˋluzɚ],失敗者\nloss,[lɔs],遺失\nlovely,[ˋlʌvlɪ],可愛的\nlover,[ˋlʌvɚ],戀人\nlower,[ˋloɚ],較低的\nluck,[lʌk],運氣\nmagazine,[͵mægəˋzin],雜誌\nmagic,[ˋmædʒɪk],魔法\nmagician,[məˋdʒɪʃən],魔術師\nmain,[men],主要的\nmaintain,[menˋten],保持\nmale,[mel],男性\nMandarin,[ˋmændərɪn],華語"""
U3_RAW = """mango,[ˋmæŋgo],芒果\nmanner,[ˋmænɚ],方法/舉止\nmark,[mɑrk],標記/痕跡\nmarriage,[ˋmærɪdʒ],婚姻\nmask,[mæsk],口罩/假面具\nmass,[mæs],大眾的\nmat,[mæt],墊子\nmatch,[mætʃ],相配/比賽\nmate,[met],夥伴\nmaterial,[məˋtɪrɪəl],材料\nmeal,[mil],一餐\nmeaning,[ˋminɪŋ],含義\nmeans,[minz],手段\nmeasurable,[ˋmɛʒərəb!],可測量的\nmeasure,[ˋmɛʒɚ],測量\nmedicine,[ˋmɛdəsn],藥\nmeeting,[ˋmitɪŋ],會議\nmelody,[ˋmɛlədɪ],旋律\nmelon,[ˋmɛlən],瓜\nmember,[ˋmɛmbɚ],成員\nmemory,[ˋmɛmərɪ],記憶\nmenu,[ˋmɛnju],菜單\nmessage,[ˋmɛsɪdʒ],消息\nmetal,[ˋmɛt!],金屬\nmeter,[ˋmitɚ],計量器\nmethod,[ˋmɛθəd],方法\nmilitary,[ˋmɪlə͵tɛrɪ],軍事的\nmillion,[ˋmɪljən],百萬\nmine,[maɪn],我的\nminus,[ˋmaɪnəs],減去\nmirror,[ˋmɪrɚ],鏡子\nmix,[mɪks],混和\nmodel,[ˋmɑd!],模型\nmodern,[ˋmɑdɚn],現代的\nmonster,[ˋmɑnstɚ],怪物\nmosquito,[məsˋkito],蚊子\nmoth,[mɔθ],蛾\nmotion,[ˋmoʃən],姿態\nmotorcycle,[ˋmotɚ͵saɪk!],摩托車\nmovable,[ˋmuvəb!],可移動的\nMRT,[MRT],大眾捷運系統\nsubway,[ˋsʌb͵we],地下鐵\nunderground,[ˋʌndɚ͵graʊnd],地下鐵\nmetro,[ˋmɛtro],地鐵\nmule,[mjul],騾"""

def parse_data(raw):
    lines = [l.strip() for l in raw.strip().split('\n') if l.strip()]
    return pd.DataFrame([l.split(',', 2) for l in lines], columns=["英文", "音標", "中文"])

def text_to_speech(text):
    text = text.replace("'", "\\'")
    js = f"""<script>window.speechSynthesis.cancel(); var msg = new SpeechSynthesisUtterance('{text}'); msg.lang = 'en-US'; window.speechSynthesis.speak(msg);</script>"""
    components.html(js, height=0)

# 初始化 Session State
if 'page' not in st.session_state: st.session_state.page = "cover"
if 'show_cn' not in st.session_state: st.session_state.show_cn = True
if 'show_ipa' not in st.session_state: st.session_state.show_ipa = True
if 'auto_play' not in st.session_state: st.session_state.auto_play = True
if 'combo' not in st.session_state: st.session_state.combo = 0
# 跨單元全域錯題本：儲存 dataframe 的 row 字典
if 'global_wrongs' not in st.session_state: st.session_state.global_wrongs = [] 

# --- 學習與挑戰初始化引導函數 ---
def setup_unit(df, name, mode="normal"):
    st.session_state.current_df = df
    st.session_state.unit_name = name
    st.session_state.total_count = len(df)
    st.session_state.study_idx = 0  # 預習用索引
    st.session_state.combo = 0
    st.session_state.wrong_indices = set()
    st.session_state.first_try_correct = 0
    st.session_state.challenge_mode = mode # "normal" 或 "wrong_notebook"
    
    # 產生隨機挑戰順序
    indices = list(range(len(df)))
    random.shuffle(indices)
    st.session_state.remaining_indices = indices
    
    st.session_state.page = "pre_study" # 先進入預習階段！
    st.rerun()


# --- 1. 封面頁 ---
if st.session_state.page == "cover":
    st.markdown('<p class="cute-title">🐾 拼字森林挑戰 🌲</p>', unsafe_allow_html=True)
    
    # 顯示全域錯題本按鈕
    wrong_count = len(st.session_state.global_wrongs)
    if wrong_count > 0:
        st.warning(f"🎒 偵測到你有 {wrong_count} 個錯題尚未消滅！")
        if st.button("🔥 進入【錯題特訓補習班】", use_container_width=True):
            wrong_df = pd.DataFrame(st.session_state.global_wrongs)
            setup_unit(wrong_df, "🎒 錯題特訓班", mode="wrong_notebook")
        st.divider()

    st.write("### 🌲 選擇單元進行預習")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🌱 第一單元"): setup_unit(parse_data(U1_RAW), "第一單元")
    with col2:
        if st.button("🌿 第二單元"): setup_unit(parse_data(U2_RAW), "第二單元")
    with col3:
        if st.button("🌳 第三單元"): setup_unit(parse_data(U3_RAW), "第三單元")

    st.divider()
    st.write("### 📖 森林單字書籤")
    tab1, tab2, tab3 = st.tabs(["第一單元", "第二單元", "第三單元"])
    with tab1: st.dataframe(parse_data(U1_RAW), hide_index=True, use_container_width=True)
    with tab2: st.dataframe(parse_data(U2_RAW), hide_index=True, use_container_width=True)
    with tab3: st.dataframe(parse_data(U3_RAW), hide_index=True, use_container_width=True)


# --- 2. 學習環節 (新功能) ---
elif st.session_state.page == "pre_study":
    st.markdown(f"## 📖 {st.session_state.unit_name} · 森林讀書會")
    st.write("在開始挑戰前，先來熟悉一下單字吧！可自由切換看中文與聽發音。")
    
    df = st.session_state.current_df
    s_idx = st.session_state.study_idx
    row = df.iloc[s_idx]
    
    # 進度提示
    st.caption(f"目前單字： {s_idx + 1} / {len(df)}")
    st.progress((s_idx + 1) / len(df))
    
    # 學習卡片
    st.markdown(f"""
        <div class="study-card">
            <h1 style="color: #2E7D32; font-size: 3.5rem; margin-bottom:10px;">{row['英文']}</h1>
            <p style="font-size: 1.3rem; color: #555;">🎧 音標：{row['音標']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 預習發音（進入單字自動發音）
    if st.session_state.get('pre_study_audio', True):
        text_to_speech(row['英文'].strip())
        st.session_state.pre_study_audio = False

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔊 播放發音", use_container_width=True):
            text_to_speech(row['英文'].strip())
    with c2:
        with st.popover("👁️ 顯示中文翻譯", use_container_width=True):
            st.info(f"💡 中文意思：{row['中文']}")
            
    st.divider()
    
    # 導覽按鈕
    b1, b2, b3 = st.columns([1, 1, 2])
    with b1:
        if st.button("⬅️ 上一個", disabled=(s_idx == 0), use_container_width=True):
            st.session_state.study_idx -= 1
            st.session_state.pre_study_audio = True
            st.rerun()
    with b2:
        if st.button("下一個 ➡️", disabled=(s_idx == len(df) - 1), use_container_width=True):
            st.session_state.study_idx += 1
            st.session_state.pre_study_audio = True
            st.rerun()
    with b3:
        if st.button("🐾 我準備好了，開始挑戰！", type="primary", use_container_width=True):
            # 正式進入挑戰，抽取第一個題目
            st.session_state.idx = st.session_state.remaining_indices.pop(0)
            st.session_state.is_review = False
            st.session_state.trigger_audio = True
            st.session_state.page = "study"
            st.rerun()
            
    if st.button("返回主選單", use_container_width=True):
        st.session_state.page = "cover"
        st.rerun()


# --- 3. 挑戰頁 ---
elif st.session_state.page == "study":
    c_back, c_t1, c_t2, c_t3 = st.columns([1, 1, 1, 1.2])
    with c_back:
        if st.button("⬅️ 返回預習"): st.session_state.page = "pre_study"; st.rerun()
    with c_t1: st.session_state.show_cn = st.toggle("中文", value=st.session_state.show_cn)
    with c_t2: st.session_state.show_ipa = st.toggle("音標", value=st.session_state.show_ipa)
    with c_t3: st.session_state.auto_play = st.toggle("🔊 自動發音", value=st.session_state.auto_play)

    row = st.session_state.current_df.iloc[st.session_state.idx]
    current_word = row['英文'].strip()
    
    done_count = st.session_state.total_count - (len(st.session_state.remaining_indices) + 1)
    progress_val = max(0.0, min(1.0, done_count / st.session_state.total_count))
    
    col_info, col_combo = st.columns([3, 1])
    with col_info:
        st.write(f"🌟 **{st.session_state.unit_name}** | 進度：{done_count + 1} / {st.session_state.total_count}")
        st.progress(progress_val)
    with col_combo:
        if st.session_state.combo > 1:
            st.markdown(f'<div class="combo-box">🔥 {st.session_state.combo} Combo</div>', unsafe_allow_html=True)

    if st.session_state.auto_play and st.session_state.get('trigger_audio', False):
        text_to_speech(current_word)
        st.session_state.trigger_audio = False

    if st.session_state.is_review:
        st.markdown('<span class="review-tag">🔄 錯題重練中</span>', unsafe_allow_html=True)

    if st.session_state.get('success_trigger', False):
        st.success("🎯 答對了！")
        time.sleep(0.6)
        if not st.session_state.remaining_indices:
            st.session_state.page = "result"
        else:
            st.session_state.idx = st.session_state.remaining_indices.pop(0)
            st.session_state.is_review = st.session_state.idx in st.session_state.wrong_indices
            st.session_state.trigger_audio = True
        st.session_state.success_trigger = False
        st.rerun()

    with st.container():
        if st.session_state.show_cn: st.info(f"💡 中文：{row['中文']}")
        if st.session_state.show_ipa: st.write(f"🎧 音標：{row['音標']}")
        
        if st.button("🔊 手動播放發音", key=f"spk_{st.session_state.idx}"):
            text_to_speech(current_word)

        with st.form(key=f"q_{st.session_state.idx}", clear_on_submit=True):
            u_in = st.text_input("拼寫單字", label_visibility="collapsed", placeholder="在此輸入...").strip()
            if st.form_submit_button("檢查答案"):
                if u_in.lower() == current_word.lower():
                    if st.session_state.idx not in st.session_state.wrong_indices:
                        st.session_state.first_try_correct += 1
                        
                    # 如果原本是全域錯題，且答對了，將其自全域錯題本移除 (限特訓班模式答對即消滅)
                    if st.session_state.challenge_mode == "wrong_notebook":
                        item_dict = row.to_dict()
                        if item_dict in st.session_state.global_wrongs:
                            st.session_state.global_wrongs.remove(item_dict)
                            
                    st.session_state.combo += 1
                    st.session_state.success_trigger = True
                    st.rerun()
                else:
                    st.error(f"❌ 答錯了！正確答案是：{current_word}")
                    st.session_state.combo = 0
                    
                    # 丟進全域錯題本 (不重複添加)
                    item_dict = row.to_dict()
                    if item_dict not in st.session_state.global_wrongs:
                        st.session_state.global_wrongs.append(item_dict)
                        
                    st.session_state.wrong_indices.add(st.session_state.idx)
                    st.session_state.remaining_indices.append(st.session_state.idx)
                    time.sleep(1.2)
                    st.session_state.idx = st.session_state.remaining_indices.pop(0)
                    st.session_state.is_review = st.session_state.idx in st.session_state.wrong_indices
                    st.session_state.trigger_audio = True 
                    st.rerun()


# --- 4. 結果結算頁 ---
elif st.session_state.page == "result":
    st.markdown('<p class="cute-title">🎊 挑戰完成！</p>', unsafe_allow_html=True)
    
    accuracy = int((st.session_state.first_try_correct / st.session_state.total_count) * 100)
    
    if accuracy == 100:
        badge = "👑 森林守護神 (完美無缺！)"
    elif accuracy >= 80:
        badge = "🦁 森林之王 (非常厲害！)"
    elif accuracy >= 60:
        badge = "🦊 聰明小狐狸 (再接再厲！)"
    else:
        badge = "🌱 迷路的小樹苗 (多加練習喔！)"
        
    st.markdown(f"""
        <div class="stat-box">
            <h3>本次練習統計</h3>
            <h1 style="color: #388E3C; font-size: 3.5rem;">{accuracy}%</h1>
            <p>第一次即答對：<b>{st.session_state.first_try_correct}</b> / {st.session_state.total_count}</p>
            <div class="badge">{badge}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 顯示目前累積留下的錯題
    if st.session_state.global_wrongs:
        st.write(f"🎒 **目前系統為你留下的總錯題數量：{len(st.session_state.global_wrongs)}**")
        st.dataframe(pd.DataFrame(st.session_state.global_wrongs), hide_index=True, use_container_width=True)
        st.info("💡 提示：回到首頁可以點選【錯題特訓補習班】專門複習並消滅這些單字！")
    else:
        st.balloons()
        st.success("恭喜！目前錯題本空空如也，你是最強的！")
    
    if st.button("🍎 回到森林首頁"):
        st.session_state.page = "cover"
        st.rerun()
