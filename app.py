# --- 修改後的發音函數 ---
def text_to_speech(text):
    if text:
        text = text.replace("'", "\\'")
        # 使用一個固定的 ID 或是確保它在頁面渲染時能被觸發
        js = f"""
        <script>
            (function() {{
                window.speechSynthesis.cancel();
                var msg = new SpeechSynthesisUtterance('{text}');
                msg.lang = 'en-US';
                msg.rate = 0.9; // 稍微慢一點點比較清晰
                window.speechSynthesis.speak(msg);
            }})();
        </script>
        """
        # 注意：這裡高度設為 0 且確保 key 隨文字變化
        components.html(js, height=0, width=0)

# --- 在拼字挑戰介面中的呼叫方式 ---
elif st.session_state.page == "study":
    row = st.session_state.current_df.iloc[st.session_state.idx]
    current_word = row['英文'].strip()

    # 💡 技巧：當使用者進入新題目時，自動播放一次（可選）
    # if 'last_played' not in st.session_state or st.session_state.last_played != current_word:
    #     text_to_speech(current_word)
    #     st.session_state.last_played = current_word

    # ... 中間的進度顯示代碼 ...

    with st.container():
        if st.session_state.show_cn: st.info(f"💡 中文：{row['中文']}")
        if st.session_state.show_ipa: st.write(f"🎧 音標：{row['音標']}")
        
        # 修正這裡：手動點擊播放
        if st.button("🔊 播放發音"):
            text_to_speech(current_word)
