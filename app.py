import streamlit as st
import pandas as pd
import random
import time
import io
import streamlit.components.v1 as components

# 1. 網頁基礎配置
st.set_page_config(page_title="高中英檢/學測 1080 單字特訓", page_icon="📝", layout="centered")

# 2. 核心日系美感 CSS ( Japanese Minimalist Design )
st.markdown("""
    <style>
    /* 背景色：砂色/米白 */
    .stApp { background-color: #F7F5F0; color: #2B3A4A; }
    
    /* 封面標題區塊 */
    .hero-section {
        text-align: center;
        padding: 40px 0;
        border-bottom: 1px solid #D1C7BD;
        margin-bottom: 30px;
    }
    .main-title { 
        font-size: 2.8rem; color: #2B3A4A; 
        font-weight: 700; letter-spacing: 3px; margin-bottom: 10px;
    }
    .sub-title {
        font-size: 1rem; color: #6B7280; letter-spacing: 4px; text-transform: uppercase;
    }
    
    /* 數據儀表板 */
    .dashboard-box {
        display: flex; justify-content: space-around;
        background-color: #FFFFFF; padding: 20px; border-radius: 8px;
        border: 1px solid #E4DFD5; margin-bottom: 30px;
    }
    .stat-item { text-align: center; }
    .stat-value { font-size: 1.8rem; font-weight: 700; color: #4A5E6B; }
    .stat-label { font-size: 0.8rem; color: #9CA3AF; margin-top: 5px; }

    /* 遊戲元素極簡化 */
    .review-tag { 
        color: #B23B3B; background-color: #FBEBEB; padding: 8px 15px; 
        border-radius: 4px; font-weight: bold; border: 1px solid #E8C1C1; font-size: 0.9rem;
        margin-bottom: 20px; text-align: center;
    }
    
    /* 單字卡風格 */
    .study-card {
        padding: 40px 25px; background-color: #FFFFFF; border-radius: 8px;
        border: 1px solid #E4DFD5; border-top: 8px solid #4A5E6B; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.02); text-align: center;
    }
    .word-title { color: #2B3A4A; font-size: 3.6rem; font-weight: 700; letter-spacing: 1px; }
    
    .example-box {
        background-color: #F2F5F3; border-left: 4px solid #6B8E78; padding: 20px; 
        border-radius: 6px; text-align: left; margin-top: 20px; line-height: 1.7;
    }
    
    .hint-text { font-size: 1.3rem; letter-spacing: 3px; color: #5A6673; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

def text_to_speech(text):
    text = text.replace("'", "\\'")
    js = f"""<script>window.speechSynthesis.cancel(); var msg = new SpeechSynthesisUtterance('{text}'); msg.lang = 'en-US'; window.speechSynthesis.speak(msg);</script>"""
    components.html(js, height=0)

# 🚀 數據庫內嵌
RAW_CSV_DATA = """單元,英文,音標,中文,英文例句,例句中文
Level 1 (U1),ignore,[ɪgˋnor],忽視,You should not ignore the doctor's advice if you want to get well soon.,如果你想早點康復，就不該忽視醫生的建議。
ill,[ɪl],生病的,The star player missed the final game because he fell ill suddenly.,這位明星球員因為突然生病而錯過了決賽。
imagine,[ɪˋmædʒɪn],想像,Can you imagine what life would be like without internet access?,你能想像沒有網路可用的生活會變怎樣嗎？
importance,[ɪmˋpɔrtns],重要性,Our English teacher always emphasizes the importance of reading every day.,我們的英文老師總是強調每天閱讀的重要性。
improve,[ɪmˋpruv],改善,The high school runner practiced hard to improve his speed and endurance.,這位高中跑者努力練習以改善他的速度與耐力。
include,[ɪnˋklud],包含,The registration fee for the camp does not include lunch and transportation.,這個營隊的報名費並不包含午餐及交通費。
income,[ˋɪn͵kʌm],收入,Many university students do part-time jobs to earn their own income.,許多大學生打工來賺取他們自己的收入。
increase,[ɪnˋkris],增加,Due to inflation, the price of movie tickets has seen a significant increase recently.,由於通貨膨脹，電影票價最近有了顯著的增加。
independence,[͵ɪndɪˋpɛndəns],獨立,The country celebrated its independence with a grand parade in the capital.,這個國家在首都舉行了盛大的遊行來慶祝其獨立。
independent,[͵ɪndɪˋpɛndənt],獨立的,Moving out to live alone helped him become more mature and independent.,搬出去一個人住幫助他變得更加成熟與獨立。
indicate,[ˋɪndə͵ket],指出,Studies indicate that getting enough sleep can greatly boost your memory.,研究指出，獲得充足的睡眠可以大大提升你的記憶力。
industry,[ˋɪndəstrɪ],工業,The tech industry has been developing rapidly in Taiwan over the past decade.,過去十年來，科技工業在台灣發展得非常迅速。
influence,[ˋɪnflʊəns],影響,Parents have a huge influence on their children's habits and behavior.,父母對孩子的習慣和行為有著巨大的影響。
ink,[ɪŋk],墨水,The printer ran out of black ink so I couldn't print my English essay.,印表機的黑色墨水用完了，所以我無法列印我的英文作文。
insect,[ˋɪnsɛkt],昆蟲,We saw many unique species of insect during our field trip in the mountains.,我們在山區的戶外教學中看到了許多獨特種類的昆蟲。
insist,[ɪnˋsɪst],堅持,My classmates insist on finishing the group project before Friday.,我的同學們堅持要在星期五之前完成這項分組報告。
instance,[ˋnstəns],例子,For instance learning how to cook is a very useful skill for high schoolers.,例如，學習如何下廚對高中生來說是一項非常實用的技能。
instant,[ˋɪnstənt],即刻的,The movie was an instant success and attracted millions of viewers worldwide.,這部電影獲得了即刻的成功，吸引了全球數百萬觀眾。
instrument,[ˋɪnstrəmənt],儀器/樂器,The guitar is one of the most popular musical instruments among teenagers.,吉他是青少年當中最受歡迎的樂器之一。
international,[͵ɪntɚˋnæʃən!],國際性的,Taking part in international exchange programs can broaden your horizons.,參加國際交流計畫可以開拓你的視野。
interview,[ˋɪntɚ͵vju],訪談,The manager will interview five applicants for the part-time job tomorrow.,經理明天將會面試五位前來應徵這份兼職工作的人。
introduce,[͵ɪntrəˋdjus],介紹,Let me introduce my best friend to you; he just transferred to our school.,讓我向你介紹我最好的朋友，他剛轉學到我們學校。
invent,[ɪnˋvɛnt],發明,Thomas Edison managed to invent many devices that changed human life.,湯瑪斯·愛迪生成功發明了許多改變人類生活的裝置。
invitation,[͵ɪnvəˋteʃən],邀請,Thank you for the invitation to your birthday party next Saturday.,謝謝你邀請我參加下星期六的生日派對。
invite,[ɪnˋvaɪt],邀請,We plan to invite our homeroom teacher to join our graduation dinner.,我們計劃邀請我們的導師來參加我們的畢業聚餐。
island,[ˋaɪlənd],島,Taiwan is a beautiful island known for its friendly people and delicious food.,台灣是一座美麗的島嶼，以友善的人民和美食聞名。
item,[ˋaɪtəm],項目,Please check every single item on the list before packing your schoolbag.,在整理書包之前，請檢查清單上的每一個項目。
jacket,[ˋdʒækɪt],夾克,You should wear a heavy jacket because it's going to be freezing outside.,你應該穿件厚夾克，因為外面會非常冷。
jam,[dʒæm],塞滿/果醬,We got stuck in a terrible traffic jam on our way to the airport.,我們在去機場的路上遇到了嚴重的交通堵塞。
jazz,[dʒæz],爵士樂,My grandfather loves listening to smooth jazz while reading newspapers.,我的祖父喜歡在看報紙時聆聽溫和的爵士樂。
jeans,[dʒinz],牛仔褲,Blue jeans are durable and never seem to go out of fashion.,藍色牛仔褲很耐穿，而且似乎永遠不會退流行。
jeep,[dʒip],吉普車,They rented a powerful jeep to drive through the rough mountain roads.,他們租了一輛馬力強大的吉普車來開過崎嶇的山路。
jog,[dʒɑg],慢跑,I usually jog around the park in the evening to keep myself fit.,我通常在傍晚繞著公園慢跑以保持身體健康。
joint,[dʒɔɪnt],關節,Regular exercise keeps your joints flexible and your muscles strong.,規律的運動可以保持你的關節靈活與肌肉強壯。
judge,[dʌdʒ],法官/判決,You should not judge a person based entirely on their appearance.,你不應該完全根據一個人的外表來評判他。
juicy,[ˋdʒusɪ],多汁的,The watermelon we bought from the night market was extremely sweet and juicy.,我們從夜市買的西瓜非常甜而且多汁。
ketchup,[ˋkɛtʃəp],番茄醬,Would you like some ketchup or mustard to go with your French fries?,你要來點番茄醬或芥末醬搭配你的薯條嗎？
kindergarten,[ˋkɪndɚ͵gɑrtn],幼稚園,My little sister still remembers her favorite teacher in kindergarten.,我妹妹仍然記得她幼稚園裡最喜歡的老師。
kingdom,[ˋkɪŋdəm],王國,The old castle was once the center of a powerful and wealthy kingdom.,這座古老的城堡曾經是一個強大且富有王國的中心。
knock,[nɑk],相撞/敲門,Please knock on the door before you enter the teacher's office.,在進入老師辦公室之前請先敲門。
knowledge,[ˋnɑlɪdʒ],知識,Reading books is an excellent way to acquire new knowledge and vocabulary.,讀書是獲取新知識和字彙的絕佳方式。
koala,[koˋɑlə],無尾熊,The tourist took a lot of photos of the sleeping koala at the zoo.,這位遊客在動物園拍了許多那隻正在睡覺的無尾熊的照片。
ladybug,[ˋledɪ͵bʌg],瓢蟲,A small ladybug with black spots landed gently on my shoulder.,一隻帶有黑點的小瓢蟲輕輕地停在我的肩膀上。
Level 1 (U2),lane,[len],小路,The narrow country lane was surrounded by beautiful golden sunflowers.,這條狹窄的鄉間小路被美麗的金黃色向日葵包圍著。
Level 1 (U2),language,[ˋlæŋgwɪdʒ],語言,Learning a foreign language requires time patience and constant practice.,學習一門外語需要時間、耐心和不斷的練習。
Level 1 (U2),lantern,[ˋlæntɚn],燈籠,During the Lantern Festival we released sky lanterns to pray for good luck.,在元宵節期間，我們施放天燈來祈求好運。
Level 1 (U2),lap,[læp],重疊部分,The kitten climbed onto my lap and purred itself to sleep.,小貓爬到我膝蓋上，發出呼嚕聲睡著了。
Level 1 (U2),latest,[ˋletɪst],最新的,Have you heard the latest news about the upcoming school concert?,你聽說了關於即將到來的學校音樂會的最新消息嗎？
Level 1 (U2),lawyer,[ˋlɔjɚ],律師,She is studying law at university because she wants to be a helpful lawyer.,她正在大學攻讀法律，因為她想成為一名能提供幫助的律師。
Level 1 (U2),leadership,[ˋlidɚʃɪp],領導,The president of the student council showed great leadership in organizing the event.,學生會長在籌辦這項活動中展現了極佳的領導能力。
Level 1 (U2),legal,[ˋlig!],法律上的,You should seek legal advice before signing any official contracts.,在簽署任何正式合同之前，你應該尋求法律建議。
Level 1 (U2),lemon,[ˋlɛmən],檸檬,Adding a slice of fresh lemon can make the water taste much better.,加一片新鮮檸檬可以讓水喝起來味道更好。
Level 1 (U2),lemonade,[͵lɛmənˋed],檸檬水,Nothing is more refreshing than a glass of ice-cold lemonade in the summer.,夏天沒有什麼比一杯冰涼的檸檬水更消暑的了。
Level 1 (U2),lend,[lɛnd],把……借給,Could you please lend me your eraser? I forgot to bring mine today.,可以請你借我你的橡皮擦嗎？我今天忘了帶我的。
Level 1 (U2),length,[lɛŋθ],長度,The English teacher asked us to write an essay of at least two pages in length.,英文老師要求我們寫一篇長度至少兩頁的作文。
Level 1 (U2),leopard,[ˋlɛpɚd],豹,The leopard is known for its incredible speed and beautiful spotted coat.,豹以其驚人的速度和美麗的斑點毛皮而聞名。
Level 1 (U2),lettuce,[ˋlɪs],萵苣,I always add plenty of fresh lettuce and tomatoes to my homemade sandwiches.,我總是精心地在我自製的三明治裡加入大量新鮮萵苣和番茄。
Level 1 (U2),library,[ˋlaɪ͵brɛrɪ],圖書館,The school library provides a quiet environment for students to study after class.,學校圖書館為學生們提供了課後複習的安靜環境。
Level 1 (U2),lick,[lɪk],舔,The dog tried to lick my hand to show its friendliness and warmth.,這隻狗試圖舔我的手以展現它的友善與熱情。
Level 1 (U2),lid,[lɪd],蓋子,Make sure the lid of the bottle is tightly closed so that it won't leak.,確保瓶子的蓋子緊閉，這樣它才不會漏水。
Level 1 (U2),lightning,[ˋlaɪtnɪŋ],閃電,A bright flash of lightning suddenly illuminated the whole night sky.,一束明亮的閃電突然照亮了整個夜空。
Level 1 (U2),limit,[ˋlɪmɪt],界限/限制,There is a strict speed limit on this highway to ensure driver safety.,這條高速公路上有嚴格的速度限制以確保駕駛安全。
Level 1 (U2),link,[lɪŋk],聯繫,The police managed to find a link between the two suspicious incidents.,警方成功找到了這兩起可疑事件之間的聯繫。
Level 1 (U2),liquid,[ˋlɪkwɪd],液體,Water is a type of liquid that changes its shape depending on the container.,水是一種會根據容器改變形狀的液體。
Level 1 (U2),listener,[ˋlɪsnɚ],傾聽者,An effective counselor must first be a patient and empathetic listener.,一位有效的輔導老師首先必須是一位有耐心且具同理心的傾聽者。
Level 1 (U2),loaf,[lof],一條,My mom bought a fresh loaf of bread from the bakery for our breakfast.,我媽媽從麵包店買了一整條新鮮麵包作為我們的早餐。
Level 1 (U2),local,[ˋlok!],地方性的,We love to visit local night markets to taste traditional Taiwanese snacks.,我們喜歡逛地方夜市來品嚐傳統的台灣小吃。
Level 1 (U2),locate,[loˋket],確定……的地點,The map helped us locate the famous historical site in the old town.,這張地圖幫助我們確認了舊城區內那處著名歷史古蹟的地點。
Level 1 (U2),lock,[lɑk],鎖,Don't forget to lock the back door before you leave the house.,在你離開房子之前，別忘了鎖上後門。
Level 1 (U2),log,[lɔg],圓木,They sat on a large fallen log near the campfire to stay warm.,他們坐在營火旁一根倒下的巨大圓木上以保持溫暖。
Level 1 (U2),lone,[lon],孤單的,A lone traveler walked quietly along the endless desert path.,一位孤單的旅人靜靜地走在無盡的沙漠小徑上。
Level 1 (U2),lonely,[ˋlonlɪ],孤獨的,Living alone in a foreign country can be quite lonely at first.,剛開始獨自居住在外國可能會感到相當孤獨。
Level 1 (U2),lose,[luz],丟失,Be careful with your wallet or you might lose all your pocket money.,小心你的錢包，否則你可能會弄丟所有的零用錢。
Level 1 (U2),loser,[ˋluzɚ],失敗者,In a fair game there will always be a winner and a graceful loser.,在公平的比賽中，總會有一個贏家和一個有風度的失敗者。
Level 1 (U2),loss,[lɔs],遺失,The sudden death of the beloved pet was a great loss to the whole family.,這隻心愛寵物的突然離世對全家人來說是一個巨大的損失。
Level 1 (U2),lovely,[ˋlʌvlɪ],可愛的,What a lovely weather we are having today for an outdoor picnic!,今天辦戶外野餐的天氣真是太完美、太美好了！
Level 1 (U2),lover,[ˋlʌvɚ],戀人,He is a great lover of classical music and attends concerts regularly.,他是古典音樂的狂熱愛好者，並且定期參加音樂會。
Level 1 (U2),lower,[ˋloɚ],較低的,The department store offers lower prices during the anniversary sale.,這家百貨公司在週年慶特賣期間提供較低的價格。
Level 1 (U2),luck,[lʌk],運氣,I wish you the best of luck on your upcoming university entrance exam!,祝你在即將到來的大學入學考試中運氣絕佳、金榜題名！
Level 1 (U2),magazine,[͵mægəˋzin],雜誌,This monthly magazine covers interesting topics about science and technology.,這本月刊雜誌涵蓋了關於科學與科技的有趣主題。
Level 1 (U2),magic,[ˋmædʒɪk],魔法,The kids watched in awe as if the street performer had real magic.,孩子們驚奇地看著，彷彿那位街頭藝人真的擁有魔法一般。
Level 1 (U2),magician,[məˋdʒɪʃən],魔術師,The magician pulled a white rabbit out of his empty hat surprising everyone.,魔術師從他空空如也的帽子裡拉出了一隻白兔，驚艷了所有人。
Level 1 (U2),main,[men],主要的,The main reason she failed the English quiz was a lack of vocabulary study.,她英文小考不及格的主要原因在於缺乏字彙複習。
Level 1 (U2),maintain,[menˋten],保持,It is important to maintain a healthy balance between study and relaxation.,在課業與放鬆之間保持健康的平衡是非常重要的。
Level 1 (U2),male,[mel],男性,The beautiful peacock we saw at the park was actually a male bird.,我們在公園看到的那隻美麗孔雀實際上是一隻雄性的鳥。
Level 1 (U2),Mandarin,[ˋmændərɪn],華語,More and more high schools abroad are starting to offer Mandarin courses.,越來越多國外的高中開始提供華語課程。
Level 1 (U3),mango,[ˋmæŋgo],芒果,Summer is the best season to enjoy fresh and juicy mango shaved ice in Taiwan.,夏天是在台灣享受新鮮多汁芒果雪花冰的最佳季節。
Level 1 (U3),manner,[ˋmænɚ],方法/舉止,It is considered good manners to say thank you when someone helps you.,當有人幫助你時，說聲謝謝被視為是有禮貌的舉止。
Level 1 (U3),mark,[mɑrk],標記/痕跡,The teacher used a red pen to correct the errors and mark the grade.,老師用紅筆來修正錯誤並打上分數標記。
Level 1 (U3),marriage,[ˋmærɪdʒ],婚姻,The happy couple celebrated their tenth year of marriage with a trip to Japan.,這對幸福的夫妻用一趟日本之旅來慶祝他們結婚十週年的婚姻生活。
Level 1 (U3),mask,[mæsk],口罩/假面具,Wearing a face mask can effectively protect you from spreading germs.,配戴口罩可以有效地保護你免於散播病菌。
Level 1 (U3),mass,[mæs],大眾的,Social media has a huge impact on mass communication in modern society.,社群媒體對現代社會的大眾傳播有著巨大的影響。
Level 1 (U3),mat,[mæt],墊子,We placed a small welcome mat at the entrance of our classroom.,我們在教室門口放置了一塊小小的歡迎地墊。
Level 1 (U3),match,[mætʃ],相配/比賽,Our school basketball team won the final match after a tight competition.,我們學校籃球隊在一場緊張的競爭後贏得了決賽。
Level 1 (U3),mate,[met],夥伴,My classmates are not just classmates; they are also my lifelong mates.,我的同學們不只是同學，他們也是我一輩子的夥伴。
Level 1 (U3),material,[məˋtɪrɪəl],材料,You can find all the necessary study materials on the school website.,你可以在學校網站上找到所有必需的學習材料。
Level 1 (U3),meal,[mil],一餐,Breakfast is often considered the most important meal of the whole day.,早餐通常被認為是整天當中最重要的一餐。
Level 1 (U3),meaning,[ˋminɪŋ],含義,If you don't know the exact meaning of a word you should consult a dictionary.,如果你不知道一個單字的確切含義，你應該查閱字典。
Level 1 (U3),means,[minz],手段,For many high school students riding a bicycle is their main means of transport.,對許多高中生來說，騎腳踏車是他們主要的交通工具。
Level 1 (U3),measurable,[ˋmɛʒərəb!],可測量的,Setting measurable goals can make your study plan much more effective.,設定可測量的目標可以讓你的讀書計畫有效得多。
Level 1 (U3),measure,[ˋmɛʒɚ],測量,The tailor used a tape to measure his waist before making the school uniform.,裁縫師在製作校服之前，用捲尺測量了他的腰圍。
Level 1 (U3),medicine,[ˋmɛdəsn],藥,Take this cough medicine three times a day after meals as directed.,按照指示，這種感冒咳嗽藥一天在飯後服用三次。
Level 1 (U3),meeting,[ˋmitɪŋ],會議,The principal called a brief meeting to discuss the graduation ceremony.,校長召開了一場簡短的會議來討論畢業典禮的事宜。
Level 1 (U3),melody,[ˋmɛlədɪ],旋律,The catchy melody of the new song immediately captured the students' attention.,這首新歌朗朗上口的旋律立刻吸引了學生們的注意。
Level 1 (U3),melon,[ˋmɛlən],瓜,We love to eat iced sweet melon on hot summer afternoons to cool down.,我們喜歡在炎熱的夏天下午吃冰鎮甜瓜來消暑。
Level 1 (U3),member,[ˋmɛmbɚ],成員,She is an active member of the school dance club and practices every day.,她是學校熱舞社的活躍成員，並且每天進行練習。
Level 1 (U3),memory,[ˋm&mərɪ],記憶,Traveling with best friends always locally creates unforgettable high school memories.,與好朋友一起旅遊總是能創造難忘的高中記憶。
Level 1 (U3),menu,[ˋm&nju],菜單,The waiter handed us the menu as soon as we sat down at the restaurant.,我們一在餐廳坐下，服務生就遞給了我們菜單。
Level 1 (U3),message,[ˋm&sɪdʒ],消息,He left a text message saying that he would be ten minutes late for class.,他留下一則簡訊消息，說他上課會遲到十分鐘。
Level 1 (U3),metal,[ˋm&t!],金屬,These sturdy classroom desks are made of a strong combination of wood and metal.,這些堅固的教室課桌是由木頭與金屬的強力組合製成的。
Level 1 (U3),meter,[ˋmitɚ],計量器,The runner finished the one-hundred-meter race in less than eleven seconds.,這位跑者在不到十一秒的時間內完成了百米賽跑。
Level 1 (U3),method,[ˋm#θəd],方法,Using flashcards is a very popular method for memorizing English vocabulary.,使用字卡是記憶英文單字一種非常受歡迎的方法。
Level 1 (U3),military,[ˋmɪlə͵tɛrɪ],軍事的,In some countries young people are required to complete compulsory military service.,在某些國家，年輕人被要求完成義務性的軍事服役。
Level 1 (U3),million,[ˋmɪljən],百萬,The video of the school festival performance received over one million views.,這段學校慶典表演的影片獲得了超過一百萬次的觀看數。
Level 1 (U3),mine,[maɪn],我的,That English dictionary on the desk is mine; thank you for finding it.,桌上的那本英文字典是我的，謝謝你幫我找到它。
Level 1 (U3),minus,[ˋmaɪnəs],減去,Ten minus three equals seven which is a very simple math problem.,十減去三等於七，這是一道非常簡單的數學題。
Level 1 (U3),mirror,[ˋmɪrɚ],鏡子,She took a quick look in the mirror to check her hair before the presentation.,在簡報之前，她快速地照了一下鏡子以檢查她的頭髮。
Level 1 (U3),mix,[mɪks],混和,You can mix blue and yellow paint together to create a beautiful green.,你可以將藍色和黃色顏料混和在一起來創造出美麗的綠色。
Level 1 (U3),model,[ˋmɑd!],模型,The students worked in pairs to build a miniature model of a solar car.,學生們兩人一組，共同製作了一台太陽能汽車的微型模型。
Level 1 (U3),modern,[ˋmɑdɚn],現代的,The new library building features a highly modern design with glass walls.,新圖書館大樓採用了帶有玻璃牆的極具現代感的設計。
Level 1 (U3),monster,[ˋmɑnstɚ],怪物,The young child was scared to sleep because he dreamed of a scary monster.,這個幼童不敢睡覺，因為他夢到了一隻可怕的怪物。
Level 1 (U3),mosquito,[məsˋkito],蚊子,Remember to close the windows or mosquitoes will come in and bite you.,記得關上窗戶，否則子會進來咬你。
Level 1 (U3),moth,[mɔθ],蛾,A large brown moth was flying around the bright light bulb on the porch.,一隻褐色的蛾正在門廊明亮的燈泡周圍飛來飛去。
Level 1 (U3),motion,[ˋmoʃən],姿態,The slow-motion replay clearly showed how the athlete caught the ball.,慢動作姿態重播清楚地顯示了這位運動員是如何接住球的。
Level 1 (U3),motorcycle,[ˋmotɚ͵saɪk!],摩托車,Riding a motorcycle without a helmet is strictly illegal in Taiwan.,在台灣，騎摩托車不戴安全帽是嚴格違法的。
Level 1 (U3),movable,[ˋmuvəb!],可移動的,The classroom partition walls are movable allowing us to merge spaces.,教室的隔間牆是可移動的，讓我們能夠合併空間。
Level 1 (U3),MRT,[MRT],大眾捷運系統,Taking the MRT is a highly convenient way to travel around Taipei city.,搭乘大眾捷運系統是在台北市內旅遊一種非常方便的方式。
Level 1 (U3),subway,[ˋsʌb͵we],地下鐵,The New York subway system is famous for being incredibly large and busy.,紐約地下鐵系統以極其龐大和繁忙而聞名。
Level 1 (U3),underground,[ˋʌndɚ͵graʊnd],地下鐵,Londoners often refer to their famous underground railway system as the Tube.,倫敦人經常將他們著名的地下鐵路系統稱為 Tube。
Level 1 (U3),metro,[ˋmetro],地鐵,The Paris metro is well-known for its beautiful and artistic station entrances.,巴黎地鐵以其美麗且具藝術感的車站入口而聞名。
Level 1 (U3),mule,[mjul],騾,The farmer used a sturdy mule to carry heavy bags of corn up the hill.,農夫使用一隻強壯的騾子將沉重的玉米袋扛上山。"""

# 解析與緩存資料庫
@st.cache_data
def load_vocabulary_db():
    return pd.read_csv(io.StringIO(RAW_CSV_DATA), encoding="utf-8")

ALL_VOCAB = load_vocabulary_db()

# --- 初始化 Session ---
if 'page' not in st.session_state: st.session_state.page = "cover"
if 'show_cn' not in st.session_state: st.session_state.show_cn = True
if 'show_ipa' not in st.session_state: st.session_state.show_ipa = True
if 'show_len' not in st.session_state: st.session_state.show_len = True
if 'auto_play' not in st.session_state: st.session_state.auto_play = True
if 'combo' not in st.session_state: st.session_state.combo = 0
if 'global_wrongs' not in st.session_state: st.session_state.global_wrongs = [] 
if 'skipped_total' not in st.session_state: st.session_state.skipped_total = 0

def setup_unit(df, name, mode="normal"):
    st.session_state.current_df = df.copy().reset_index(drop=True)
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

# --- 1. 優化版封面頁 ---
if st.session_state.page == "cover":
    # 頂部視覺區
    st.markdown("""
        <div class="hero-section">
            <p class="sub-title">CORE VOCABULARY SPECIAL TRAINING</p>
            <h1 class="main-title">高中學測 1080 核心字彙特訓</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # 數據儀表板 (模擬進度)
    skipped_count = st.session_state.skipped_total
    wrong_count = len(st.session_state.global_wrongs)
    st.markdown(f"""
        <div class="dashboard-box">
            <div class="stat-item">
                <div class="stat-value">1088</div>
                <div class="stat-label">總單字量</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" style="color: #6B8E78;">{skipped_count}</div>
                <div class="stat-label">已熟記字數</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" style="color: #B23B3B;">{wrong_count}</div>
                <div class="stat-label">待消滅錯題</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 弱點特訓區
    if wrong_count > 0:
        st.markdown('<div class="review-tag">💡 目前仍有弱點尚未消滅，建議先進行弱點回溫</div>', unsafe_allow_html=True)
        if st.button("🔥 啟動【弱點特訓】（單獨強化錯題）", use_container_width=True):
            setup_unit(pd.DataFrame(st.session_state.global_wrongs), "🎯 弱點特訓班", mode="wrong_notebook")
        st.divider()

    st.write("### 📂 特訓進度選擇")
    units = ALL_VOCAB["單元"].unique()
    cols = st.columns(3)
    for idx, u_name in enumerate(units):
        with cols[idx % 3]:
            if st.button(u_name, use_container_width=True):
                unit_df = ALL_VOCAB[ALL_VOCAB["單元"] == u_name]
                setup_unit(unit_df, u_name)

    st.divider()
    st.write("### 📖 全單字快速索引")
    tabs = st.tabs([f"{u} 清單" for u in units])
    for idx, u_name in enumerate(units):
        with tabs[idx]:
            st.dataframe(ALL_VOCAB[ALL_VOCAB["單元"] == u_name][["英文", "音標", "中文"]], hide_index=True, use_container_width=True)

# --- 2. 學習環節 ---
elif st.session_state.page == "pre_study":
    st.markdown(f"## 📖 {st.session_state.unit_name} · 記憶卡預習")
    df = st.session_state.current_df
    s_idx = st.session_state.study_idx
    row = df.iloc[s_idx]
    st.progress((s_idx + 1) / len(df))
    
    is_this_skipped = s_idx in st.session_state.skipped_indices
    card_bg = "#FAFAFA" if is_this_skipped else "#FFFFFF"
    
    st.markdown(f"""
        <div class="study-card" style="background-color: {card_bg};">
            <h1 class="word-title">{row['英文']}</h1>
            <p style="font-size: 1.1rem; color: #6B7280; margin-bottom: 8px;">{row['音標']}</p>
            <p style="font-size: 1.25rem; color: #2B3A4A; font-weight: 600;">字義：{row['中文']}</p>
        </div>
        <div class="example-box">
            <b style="color: #4A5E6B;">📝 語境模擬句：</b><br>
            <span style="font-size: 1.1rem; color: #1F2937; display:block; margin-bottom:8px;">{row['英文例句']}</span>
            <span style="font-size: 1rem; color: #4B5563; display:block; border-top: 1px dashed #D1C7BD; padding-top:6px;"><b>句意翻譯：</b>{row['例句中文']}</span>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.get('pre_study_audio', True):
        text_to_speech(row['英文'].strip())
        st.session_state.pre_study_audio = False

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔊 播放發音", use_container_width=True):
            text_to_speech(row['英文'].strip())
    with c2:
        if not is_this_skipped:
            if st.button("✅ 已熟記 (本次跳過測驗)", type="secondary", use_container_width=True):
                st.session_state.skipped_indices.add(s_idx)
                st.session_state.skipped_total += 1 # 累計到全域
                st.rerun()
        else:
            if st.button("🔄 取消跳過 (重回測驗群)", type="secondary", use_container_width=True):
                st.session_state.skipped_indices.remove(s_idx)
                st.session_state.skipped_total -= 1
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
        btn_label = f"⚔️ 開始拼字挑戰 ({active_count} 題)" if active_count > 0 else "已無可挑戰單字"
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
            
    if st.button("返回首頁選單", use_container_width=True):
        st.session_state.page = "cover"
        st.rerun()

# --- 3. 挑戰測驗頁 ---
elif st.session_state.page == "study":
    c_back, c_t1, c_t2, c_t3, c_t4 = st.columns([1, 1, 1, 1.2, 1.2])
    with c_back:
        if st.button("⬅️ 中斷"): st.session_state.page = "pre_study"; st.rerun()
    with c_t1: st.session_state.show_cn = st.toggle("中文提示", value=st.session_state.show_cn)
    with c_t2: st.session_state.show_ipa = st.toggle("音標", value=st.session_state.show_ipa)
    with c_t3: st.session_state.auto_play = st.toggle("自動發音", value=st.session_state.auto_play)
    with c_t4: st.session_state.show_len = st.toggle("字數底線", value=st.session_state.show_len)

    row = st.session_state.current_df.iloc[st.session_state.idx]
    current_word = row['英文'].strip()
    
    done_count = st.session_state.total_count - (len(st.session_state.remaining_indices) + 1)
    progress_val = max(0.0, min(1.0, done_count / st.session_state.total_count))
    
    col_info, col_combo = st.columns([3, 1])
    with col_info:
        st.write(f"**{st.session_state.unit_name} 特訓中** | 剩餘：{len(st.session_state.remaining_indices) + 1} 題")
        st.progress(progress_val)
    with col_combo:
        if st.session_state.combo > 1:
            st.markdown(f'<div class="combo-box">🔥 {st.session_state.combo} Combo</div>', unsafe_allow_html=True)

    if st.session_state.auto_play and st.session_state.get('trigger_audio', False):
        text_to_speech(current_word)
        st.session_state.trigger_audio = False

    if st.session_state.is_review:
        st.markdown('<span class="review-tag">🔄 弱點重新修正中</span>', unsafe_allow_html=True)

    with st.container():
        if st.session_state.show_len:
            underscores = " ".join(["_"] * len(current_word))
            st.markdown(f'<p class="hint-text">結構提示：{underscores}  ({len(current_word)} 字元)</p>', unsafe_allow_html=True)
            
        if st.session_state.show_cn: st.info(f"中文意思：{row['中文']}")
        if st.session_state.show_ipa: st.write(f"音標發音：{row['音標']}")
        
        if st.button("🔊 手動播放音訊", key=f"spk_{st.session_state.idx}"):
            text_to_speech(current_word)

        u_in = st.text_input(
            "輸入英文單字回答", label_visibility="collapsed", placeholder="請輸入答案並按 Enter...", key=f"input_box_{st.session_state.idx}"
        )
        
        if u_in:
            if u_in.strip().lower() == current_word.lower():
                if st.session_state.idx not in st.session_state.wrong_indices:
                    st.session_state.first_try_correct += 1
                if st.session_state.challenge_mode == "wrong_notebook":
                    item_dict = row.to_dict()
                    if item_dict in st.session_state.global_wrongs:
                        st.session_state.global_wrongs.remove(item_dict)
                st.session_state.combo += 1
                st.toast("🎯 正確！", icon="✅")
                time.sleep(0.4)
                if not st.session_state.remaining_indices:
                    st.session_state.page = "result"
                else:
                    st.session_state.idx = st.session_state.remaining_indices.pop(0)
                    st.session_state.is_review = st.session_state.idx in st.session_state.wrong_indices
                    st.session_state.trigger_audio = True
                st.rerun()
            else:
                st.error(f"錯誤。正確拼寫應為： {current_word}")
                st.warning(f"📖 複習句意：{row['英文例句']}\n\n🎯 句意翻譯：{row['例句中文']}")
                st.session_state.combo = 0
                item_dict = row.to_dict()
                if item_dict not in st.session_state.global_wrongs:
                    st.session_state.global_wrongs.append(item_dict)
                st.session_state.wrong_indices.add(st.session_state.idx)
                st.session_state.remaining_indices.append(st.session_state.idx)
                time.sleep(2.5) 
                st.session_state.idx = st.session_state.remaining_indices.pop(0)
                st.session_state.is_review = st.session_state.idx in st.session_state.wrong_indices
                st.session_state.trigger_audio = True 
                st.rerun()

# --- 4. 結算頁 ---
elif st.session_state.page == "result":
    st.markdown('<p class="main-title">特訓結果結算</p>', unsafe_allow_html=True)
    accuracy = int((st.session_state.first_try_correct / st.session_state.total_count) * 100) if st.session_state.total_count > 0 else 100
    
    if accuracy == 100: badge = "👑 頂標 · 核心完全掌握"
    elif accuracy >= 85: badge = "🥈 前標 · 字彙掌握度高"
    elif accuracy >= 70: badge = "🥉 均標 · 持續加強衝刺"
    else: badge = "🌱 後標 · 建議重新完整複習"
        
    st.markdown(f"""
        <div class="stat-box">
            <h3>本次字彙首刷正確率</h3>
            <h1 style="color: #2B3A4A; font-size: 3.5rem;">{accuracy}%</h1>
            <p>首刷即答對題數：<b>{st.session_state.first_try_correct}</b> / {st.session_state.total_count}</p>
            <div class="badge">{badge}</div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.global_wrongs:
        st.write(f"### 🎒 待複習的弱點清單 ({len(st.session_state.global_wrongs)})")
        st.dataframe(pd.DataFrame(st.session_state.global_wrongs)[["英文", "音標", "中文"]], hide_index=True, use_container_width=True)
    
    if st.button("確認並返回首頁選單", type="primary", use_container_width=True):
        st.session_state.page = "cover"
        st.rerun()
