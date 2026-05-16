import streamlit as st
import pandas as pd
import random
import time
import streamlit.components.v1 as components

# 1. 基礎設定
st.set_page_config(page_title="言語森林：高中單字特訓", page_icon="🐾", layout="centered")

# 2. 介面美化
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; }
    .cute-title { font-size: 2.5rem; color: #1E3A8A; text-align: center; font-weight: bold; margin-bottom: 20px; }
    .review-tag { 
        color: #DC2626; background-color: #FEF2F2; padding: 5px 12px; 
        border-radius: 20px; font-weight: bold; border: 1px solid #FCA5A5; font-size: 0.9rem;
    }
    .combo-box { font-size: 1.5rem; color: #EA580C; font-weight: bold; text-align: center; }
    .stat-box {
        padding: 25px; background-color: #FFFFFF; border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); text-align: center; margin-bottom: 20px;
        border-top: 6px solid #1E3A8A;
    }
    .badge { font-size: 1.8rem; color: #1D4ED8; font-weight: bold; margin-top: 10px; }
    .example-box {
        background-color: #F0FDF4; border-left: 5px solid #16A34A; padding: 15px; 
        border-radius: 4px; text-align: left; margin-top: 15px;
    }
    .word-title { color: #1E3A8A; font-size: 3.5rem; font-weight: 800; letter-spacing: 1px; margin-bottom: 5px; }
    .hint-text { font-size: 1.4rem; letter-spacing: 3px; color: #4B5563; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

# 3. 資料庫（已擴充第4欄：例句*例句中文）
U1_RAW = """ignore,[ɪgˋnor],忽視,You should not ignore the doctor's advice if you want to get well soon.*如果你想早點康復，就不該忽視醫生的建議。
ill,[ɪl],生病的,The star player missed the final game because he fell ill suddenly.*這位明星球員因為突然生病而錯過了決賽。
imagine,[ɪˋmædʒɪn],想像,Can you imagine what life would be like without internet access?*你能想像沒有網路可用的生活會變怎樣嗎？
importance,[ɪmˋpɔrtns],重要性,Our English teacher always emphasizes the importance of reading every day.*我們的英文老師總是強調每天閱讀的重要性。
improve,[ɪmˋpruv],改善,The high school runner practiced hard to improve his speed and endurance.*這位高中跑者努力練習以改善他的速度與耐力。
include,[ɪnˋklud],包含,The registration fee for the camp does not include lunch and transportation.*這個營隊的報名費並不包含午餐及交通費。
income,[ˋɪn͵kʌm],收入,Many university students do part-time jobs to earn their own income.*許多大學生打工來賺取他們自己的收入。
increase,[ɪnˋkris],增加,Due to inflation, the price of movie tickets has seen a significant increase recently.*由於通貨膨脹，電影票價最近有了顯著的增加。
independence,[͵ɪndɪˋpɛndəns],獨立,The country celebrated its independence with a grand parade in the capital.*這個國家在首都舉行了盛大的遊行來慶祝其獨立。
independent,[͵ɪndɪˋpɛndənt],獨立的,Moving out to live alone helped him become more mature and independent.*搬出去一個人住幫助他變得更加成熟與獨立。"""

# 預備其餘單元結構（可依此格式填入）
U2_RAW = """lane,[len],小路,The country lane was surrounded by beautiful sunflowers.*這條鄉間小路被美麗的向日葵包圍著。
language,[ˋlæŋgwɪdʒ],語言,Learning a foreign language requires time, patience, and constant practice.*學習一門外語需要時間、耐心和不斷的練習。"""
U3_RAW = """mango,[ˋmæŋgo],芒果,Summer is the best season to enjoy fresh and juicy mango shaved ice in Taiwan.*夏天是在台灣享受新鮮多汁芒果雪花冰的最佳季節。"""

def parse_data(raw):
    lines = [l.strip() for l in raw.strip().split('\n') if l.strip()]
    data = []
    for l in lines:
        parts = l.split(',', 3)
        if len(parts) == 4:
            eng, ipa, ch, example_all = parts
            ex_en, ex_ch = example_all.split('*') if '*' in example_all else (example_all, "（暫無翻譯）")
            data.append([eng, ipa, ch, ex_en, ex_ch])
        else:
            # 防呆
            data.append([parts[0], "", parts[1] if len(parts)>1 else "", "No example.", "無例句"])
    return pd.DataFrame(data, columns=["英文", "音標", "中文", "英文例句", "例句中文"])

def text_to_speech(text):
    text = text.replace("'", "\\'")
    js = f"""<script>window.speechSynthesis.cancel(); var msg = new SpeechSynthesisUtterance('{text}'); msg.lang = 'en-US'; window.speechSynthesis.speak(msg);</script>"""
    components.html(js, height=0)

# 初始化 Session State
if 'page' not in st.session_state: st.session_state.page = "cover"
if 'show_cn' not in st.session_state: st.session_state.show_cn = True
if 'show_ipa' not in st.session_state: st.session_state.show_ipa = True
if 'show_len' not in st.session_state: st.session_state.show_len = True
if 'show_ex_hint' not in st.session_state: st.session_state.show_ex_hint = True # 新增：挑戰時是否顯示例句挖空
if 'auto_play' not in st.session_state: st.session_state.auto_play = True
if 'combo' not in st.session_state: st.session_state.combo = 0
if 'global_wrongs' not in st.session_state: st.session_state.global_wrongs = [] 

def setup_unit(df, name, mode="normal"):
    st.session_state.current_df = df.copy()
    st.session_state.unit_name = name
    st.session_state.study_idx = 0 
    st.session_state.combo = 0
    st.session_state.wrong_indices = set()
    st.session_state.first_try_correct = 0
    st.session_state.challenge_mode = mode 
    st.session_state.skipped_indices = set() 
    
    st.session_state.page = "pre_study"
    st.session_state.pre_study_audio = True
    st.rerun()


# --- 1. 封面頁 ---
if st.session_state.page == "cover":
    st.markdown('<p class="cute-title">📝 高中學測 1080 單字特訓艙</p>', unsafe_allow_html=True)
    
    wrong_count = len(st.session_state.global_wrongs)
    if wrong_count > 0:
        st.error(f"🚨 警告：目前累積 {wrong_count} 個未消滅弱點單字！")
        if st.button("🔥 進入【弱點特訓：全面消滅錯題】", use_container_width=True):
            wrong_df = pd.DataFrame(st.session_state.global_wrongs)
            setup_unit(wrong_df, "🎯 弱點特訓班", mode="wrong_notebook")
        st.divider()

    st.write("### 📂 選擇單元開始預習（核心語境單字卡）")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🌱 Level 1 (U1)"): setup_unit(parse_data(U1_RAW), "Level 1 (U1)")
    with col2:
        if st.button("🌿 Level 1 (U2)"): setup_unit(parse_data(U2_RAW), "Level 1 (U2)")
    with col3:
        if st.button("🌳 Level 1 (U3)"): setup_unit(parse_data(U3_RAW), "Level 1 (U3)")

    st.divider()
    st.write("### 📖 單字索引書籤 (含學測模擬句)")
    tab1, tab2, tab3 = st.tabs(["U1 清單", "U2 清單", "U3 清單"])
    with tab1: st.dataframe(parse_data(U1_RAW), hide_index=True, use_container_width=True)
    with tab2: st.dataframe(parse_data(U2_RAW), hide_index=True, use_container_width=True)
    with tab3: st.dataframe(parse_data(U3_RAW), hide_index=True, use_container_width=True)


# --- 2. 預習環節（融入語境閱讀） ---
elif st.session_state.page == "pre_study":
    st.markdown(f"## 📖 {st.session_state.unit_name} · 核心記憶卡")
    
    df = st.session_state.current_df
    s_idx = st.session_state.study_idx
    row = df.iloc[s_idx]
    
    st.caption(f"進度： {s_idx + 1} / {len(df)} | 已標記跳過：{len(st.session_state.skipped_indices)} 個")
    st.progress((s_idx + 1) / len(df))
    
    is_this_skipped = s_idx in st.session_state.skipped_indices
    card_bg = "#F3F4F6" if is_this_skipped else "#FFFFFF"
    card_border = "#9CA3AF" if is_this_skipped else "#2563EB"
    
    # 呈現單字本體
    st.markdown(f"""
        <div style="padding: 30px 20px; background-color: {card_bg}; border-radius: 16px;
        border-top: 8px solid {card_border}; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center;">
            <h1 class="word-title">{row['英文']}</h1>
            <p style="font-size: 1.2rem; color: #4B5563; margin-bottom: 5px;">🎧 {row['音標']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 🚀 重點升級：預習時主動秀出英文例句
    st.markdown(f"""
        <div class="example-box">
            <b style="color: #16A34A;">📝 學測語境模擬句：</b><br>
            <span style="font-size: 1.15rem; font-style: italic; color: #1E293B;">{row['英文例句']}</span>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.get('pre_study_audio', True):
        text_to_speech(row['英文'].strip())
        st.session_state.pre_study_audio = False

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔊 播放發音", use_container_width=True):
            text_to_speech(row['英文'].strip())
    with c2:
        with st.popover("👁️ 解鎖中文翻譯", use_container_width=True):
            st.info(f"💡 字義：{row['中文']}")
            st.caption(f"🎯 例句翻譯：{row['例句中文']}")
    with c3:
        if not is_this_skipped:
            if st.button("✅ 這題我會了 (跳過)", type="secondary", use_container_width=True):
                st.session_state.skipped_indices.add(s_idx)
                st.rerun()
        else:
            if st.button("🔄 取消跳過 (納入測驗)", type="secondary", use_container_width=True):
                st.session_state.skipped_indices.remove(s_idx)
                st.rerun()
            
    st.divider()
    
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
        active_count = len(df) - len(st.session_state.skipped_indices)
        btn_label = f"⚔️ 啟動學測模擬挑戰 ({active_count}題)" if active_count > 0 else "❌ 無可挑戰單字"
        
        if st.button(btn_label, type="primary", use_container_width=True, disabled=(active_count == 0)):
            final_indices = [i for i in range(len(df)) if i not in st.session_state.skipped_indices]
            random.shuffle(final_indices)
            
            st.session_state.remaining_indices = final_indices
            st.session_state.total_count = len(final_indices) 
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
    # 控制列（新增例句開關）
    c_back, c_t1, c_t2, c_t3, c_t4, c_t5 = st.columns([1, 1, 1, 1.2, 1.2, 1.2])
    with c_back:
        if st.button("⬅️ 放棄"): st.session_state.page = "pre_study"; st.rerun()
    with c_t1: st.session_state.show_cn = st.toggle("中文", value=st.session_state.show_cn)
    with c_t2: st.session_state.show_ipa = st.toggle("音標", value=st.session_state.show_ipa)
    with c_t3: st.session_state.auto_play = st.toggle("🔊 自動發音", value=st.session_state.auto_play)
    with c_t4: st.session_state.show_len = st.toggle("📝 字數提示", value=st.session_state.show_len)
    with c_t5: st.session_state.show_ex_hint = st.toggle("📖 文意句提示", value=st.session_state.show_ex_hint)

    row = st.session_state.current_df.iloc[st.session_state.idx]
    current_word = row['英文'].strip()
    
    done_count = st.session_state.total_count - (len(st.session_state.remaining_indices) + 1)
    progress_val = max(0.0, min(1.0, done_count / st.session_state.total_count))
    
    col_info, col_combo = st.columns([3, 1])
    with col_info:
        st.write(f"⚔️ **{st.session_state.unit_name} 戰場** | 剩餘：{len(st.session_state.remaining_indices) + 1} 題")
        st.progress(progress_val)
    with col_combo:
        if st.session_state.combo > 1:
            st.markdown(f'<div class="combo-box">🔥 {st.session_state.combo} Combo</div>', unsafe_allow_html=True)

    if st.session_state.auto_play and st.session_state.get('trigger_audio', False):
        text_to_speech(current_word)
        st.session_state.trigger_audio = False

    if st.session_state.is_review:
        st.markdown('<span class="review-tag">🔄 弱點修正重練中</span>', unsafe_allow_html=True)

    if st.session_state.get('success_trigger', False):
        st.success("🎯 答對了！")
        time.sleep(0.5)
        if not st.session_state.remaining_indices:
            st.session_state.page = "result"
        else:
            st.session_state.idx = st.session_state.remaining_indices.pop(0)
            st.session_state.is_review = st.session_state.idx in st.session_state.wrong_indices
            st.session_state.trigger_audio = True
        st.session_state.success_trigger = False
        st.rerun()

    with st.container():
        # 🚀 重點升級：學測大題模擬（挖空例句提示）
        if st.session_state.show_ex_hint:
            raw_sentence = row['英文例句']
            # 不分大小寫將目標單字替換為學測式底線
            import re
            blind_word = " " + ("_" * len(current_word)) + " "
            # 防呆：精準比對單字
            pattern = re.compile(r'\b' + re.escape(current_word) + r'\b', re.IGNORECASE)
            masked_sentence = pattern.sub(f" **{blind_word}** ", raw_sentence)
            
            st.markdown(f"""
                <div style="background-color: #EFF6FF; border-left: 5px solid #3B82F6; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                    <b style="color: #2563EB;">📝 108課綱 文意字彙模擬題：</b><br>
                    <span style="font-size: 1.2rem; line-height: 1.6; color: #1E293B;">{masked_sentence}</span>
                </div>
            """, unsafe_allow_html=True)
            
        if st.session_state.show_len:
            underscores = " ".join(["_"] * len(current_word))
            st.markdown(f'<p class="hint-text">長度提示：{underscores}  ({len(current_word)} 字)</p>', unsafe_allow_html=True)
            
        if st.session_state.show_cn: st.info(f"💡 中文提示：{row['中文']}")
        if st.session_state.show_ipa: st.write(f"🎧 音標：{row['音標']}")
        
        if st.button("🔊 手動播放發音", key=f"spk_{st.session_state.idx}"):
            text_to_speech(current_word)

        with st.form(key=f"q_{st.session_state.idx}", clear_on_submit=True):
            u_in = st.text_input("輸入拼寫英文答案", label_visibility="collapsed", placeholder="根據文意在此填入拼寫單字...").strip()
            if st.form_submit_button("檢查答案 (Enter)"):
                if u_in.lower() == current_word.lower():
                    if st.session_state.idx not in st.session_state.wrong_indices:
                        st.session_state.first_try_correct += 1
                        
                    if st.session_state.challenge_mode == "wrong_notebook":
                        item_dict = row.to_dict()
                        if item_dict in st.session_state.global_wrongs:
                            st.session_state.global_wrongs.remove(item_dict)
                            
                    st.session_state.combo += 1
                    st.session_state.success_trigger = True
                    st.rerun()
                else:
                    st.error(f"❌ 答錯了！正確答案是： {current_word}")
                    # 答錯加強顯示翻譯，加深印象
                    st.warning(f"💡 句意：{row['例句中文']}")
                    st.session_state.combo = 0
                    
                    item_dict = row.to_dict()
                    if item_dict not in st.session_state.global_wrongs:
                        st.session_state.global_wrongs.append(item_dict)
                        
                    st.session_state.wrong_indices.add(st.session_state.idx)
                    st.session_state.remaining_indices.append(st.session_state.idx)
                    time.sleep(2.0) # 留時間讓學生看錯誤詳情
                    st.session_state.idx = st.session_state.remaining_indices.pop(0)
                    st.session_state.is_review = st.session_state.idx in st.session_state.wrong_indices
                    st.session_state.trigger_audio = True 
                    st.rerun()


# --- 4. 結果結算頁 ---
elif st.session_state.page == "result":
    st.markdown('<p class="cute-title">📊 戰力特訓結算</p>', unsafe_allow_html=True)
    
    accuracy = int((st.session_state.first_try_correct / st.session_state.total_count) * 100) if st.session_state.total_count > 0 else 100
    
    if accuracy == 100: badge = "👑 頂標 · 核心守護神"
    elif accuracy >= 85: badge = "🦁 前標 · 森林高材生"
    elif accuracy >= 70: badge = "🦊 均標 · 衝刺期狐狸"
    else: badge = "🌱 后標 · 需加強灌溉的小樹苗"
        
    st.markdown(f"""
        <div class="stat-box">
            <h3>本次核心單字記憶率</h3>
            <h1 style="color: #1E3A8A; font-size: 3.5rem;">{accuracy}%</h1>
            <p>首刷即答對：<b>{st.session_state.first_try_correct}</b> / {st.session_state.total_count} (已排除主動跳過題)</p>
            <div class="badge">{badge}</div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.global_wrongs:
        st.write(f"🎒 **目前累積未消滅的錯題數：{len(st.session_state.global_wrongs)}**")
        st.dataframe(pd.DataFrame(st.session_state.global_wrongs)[["英文", "中文", "英文例句"]], hide_index=True, use_container_width=True)
        st.info("💡 秘訣：返回首頁點擊【弱點特訓】，直接針對這些錯題重新預習、挑戰，直到完全消滅它們！")
    else:
        st.balloons()
        st.success("終極目標達成！你的錯題本現在是乾淨的！")
    
    if st.button("🍎 回到特訓選單"):
        st.session_state.page = "cover"
        st.rerun()
