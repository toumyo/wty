#!/usr/bin/env python3
"""Generate trilingual landing pages for the tools Taiyang built himself.

Writes:
  site/tools/index.html, site/tools/<slug>/index.html          (zh-Hant)
  site/ja/tools/index.html, site/ja/tools/<slug>/index.html    (ja)
  site/en/tools/index.html, site/en/tools/<slug>/index.html    (en)

Only describe what each tool actually does. When a tool changes, edit TOOLS below
and rerun:  python3 scripts/build_tools.py && python3 scripts/build_news.py
"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_site import ADSENSE, BASE, EMAIL  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
LANGS = ["zh", "ja", "en"]
PREFIX = {"zh": "/", "ja": "/ja/", "en": "/en/"}
HREFLANG = {"zh": "zh-Hant", "ja": "ja", "en": "en"}
LANG_LABEL = {"zh": "繁體", "ja": "日本語", "en": "English"}
OG_LOCALE = {"zh": "zh_TW", "ja": "ja_JP", "en": "en_US"}

UI = {
    "zh": dict(home="首頁", tools="自製工具", open="打開工具", free="免費 · 免註冊 · 瀏覽器直接使用",
               features="功能", how="使用方法", faq="常見問題", related="其他自製工具",
               ui_lang="介面語言", author="作者", all_tools="查看全部工具 →",
               index_title="自製線上工具｜王太陽 Taiyang Wang",
               index_h1="自製線上工具",
               index_desc="王太陽（Taiyang Wang）自己開發的免費線上工具：匯率換算、IP 查詢、AI 簡歷製作、MBTI 測試、周易占卜、數字命理、掃雷與短網址。",
               index_lead="這些工具都由我自己設計與開發，免費使用，打開網頁即可。",
               more="首頁還有更多常用工具", note="說明", skip="跳到正文"),
    "ja": dict(home="ホーム", tools="自作ツール", open="ツールを開く", free="無料 · 登録不要 · ブラウザで使えます",
               features="機能", how="使い方", faq="よくある質問", related="ほかの自作ツール",
               ui_lang="画面の言語", author="制作", all_tools="すべてのツールを見る →",
               index_title="自作オンラインツール｜王太陽 Taiyang Wang",
               index_h1="自作オンラインツール",
               index_desc="王太陽（Taiyang Wang）が自分で開発した無料オンラインツール：為替換算、IPアドレス確認、AI履歴書作成、MBTI診断、易経占い、数秘術、マインスイーパー、短縮URL。",
               index_lead="どれも自分で設計・開発したツールです。無料で、ブラウザを開くだけで使えます。",
               more="トップページにはほかのツールもあります", note="ご注意", skip="本文へ移動"),
    "en": dict(home="Home", tools="My tools", open="Open the tool", free="Free · No sign-up · Runs in your browser",
               features="Features", how="How to use", faq="FAQ", related="More tools I built",
               ui_lang="Interface language", author="Built by", all_tools="All tools →",
               index_title="Free Online Tools Built by Taiyang Wang",
               index_h1="Tools I built",
               index_desc="Free online tools designed and built by Taiyang Wang: currency converter, IP lookup, AI résumé builder, MBTI test, I Ching reading, numerology, Minesweeper and short links.",
               index_lead="I designed and built each of these myself. They are free and run in your browser.",
               more="More tools on the homepage", note="Note", skip="Skip to content"),
}

# Facts come from each tool's own page (checked 2026-11-07). Do not add features here
# that the tool does not have.
TOOLS = [
    dict(
        slug="currency-converter", host="hl", category="FinanceApplication",
        zh=dict(name="匯率換算",
                title="線上匯率換算｜即時匯率、免費免註冊 | wangtaiyang.com",
                desc="免費線上匯率換算工具：輸入金額與幣別即可即時換算，自動從多個匯率來源中選擇較穩定的一個，無需註冊。",
                lead="輸入金額、選擇幣別，就能即時換算。工具會在多個匯率來源中自動選擇較穩定的一個。",
                ui="繁體中文",
                features=["即時匯率換算", "多個匯率來源，自動選擇較穩定的來源", "打開網頁即可使用，無需註冊或安裝"],
                steps=["輸入要換算的金額", "選擇原幣別與目標幣別", "按「開始換算」查看結果"],
                faq=[("匯率資料來自哪裡？", "工具會從多個匯率 API 中自動選擇較穩定的來源。結果僅供參考，實際交易請以銀行或支付平台的牌價為準。"),
                     ("需要註冊嗎？", "不需要，打開網頁即可使用。")]),
        ja=dict(name="為替換算",
                title="為替換算ツール｜リアルタイムレート・無料・登録不要 | wangtaiyang.com",
                desc="無料のオンライン為替換算ツールです。金額と通貨を入力するとすぐに換算できます。複数のレート取得元から安定したものを自動で選びます。登録は不要です。",
                lead="金額を入力して通貨を選ぶだけで、すぐに換算できます。複数のレート取得元から、安定したものを自動で選びます。",
                ui="中国語（繁体字）",
                features=["リアルタイムの為替換算", "複数のレート取得元から安定したものを自動選択", "ブラウザで開くだけ。登録もインストールも不要"],
                steps=["換算したい金額を入力", "元の通貨と換算先の通貨を選択", "「開始換算」を押して結果を確認"],
                faq=[("レートはどこから取得していますか？", "複数の為替 API から、安定しているものを自動で選んでいます。結果は参考値です。実際の取引では銀行や決済サービスのレートをご確認ください。"),
                     ("登録は必要ですか？", "不要です。ページを開けばすぐに使えます。")]),
        en=dict(name="Currency Converter",
                title="Free Online Currency Converter｜Real-time Rates, No Sign-up | wangtaiyang.com",
                desc="A free online currency converter. Enter an amount and pick currencies to convert instantly. It automatically picks the more stable of several rate sources. No sign-up.",
                lead="Enter an amount, pick the currencies, and convert instantly. The tool automatically picks the more stable of several exchange-rate sources.",
                ui="Traditional Chinese",
                features=["Real-time currency conversion", "Several rate sources, with the more stable one picked automatically", "Works in the browser, with no sign-up or install"],
                steps=["Enter the amount to convert", "Choose the source and target currencies", "Press the convert button (開始換算) to see the result"],
                faq=[("Where do the rates come from?", "The tool picks the more stable of several exchange-rate APIs. Results are for reference; check your bank or payment provider for the rate you will actually get."),
                     ("Do I need an account?", "No. Open the page and use it.")]),
    ),
    dict(
        slug="ip-lookup", host="ip", category="UtilitiesApplication",
        zh=dict(name="IP 查詢",
                title="IP 查詢｜查看我的公網 IP 與所在位置 | wangtaiyang.com",
                desc="免費 IP 查詢工具：即時顯示你目前的公網 IP 與大致地理位置，並在地圖上標示。基於 Cloudflare 邊緣網路。",
                lead="打開頁面，即可看到你目前的公網 IP 與大致地理位置，並在地圖上標示。資料來自 Cloudflare 邊緣網路。",
                ui="簡體中文",
                features=["即時顯示目前的公網 IP", "顯示大致地理位置與地圖", "基於 Cloudflare 邊緣網路"],
                steps=["打開頁面", "等待載入完成，查看 IP 與位置資訊"],
                faq=[("顯示的位置準確嗎？", "IP 定位只能看到大致的地區，不代表你的確切地址。"),
                     ("為什麼位置和我實際所在地不同？", "如果你使用 VPN、代理或某些行動網路，顯示的會是出口伺服器的位置。")]),
        ja=dict(name="IPアドレス確認",
                title="IPアドレス確認｜自分のグローバルIPと位置を表示 | wangtaiyang.com",
                desc="無料のIPアドレス確認ツールです。現在のグローバルIPとおおよその位置を表示し、地図上にも示します。Cloudflare のエッジネットワークを利用しています。",
                lead="ページを開くと、現在のグローバルIPとおおよその位置が表示され、地図上にも示されます。情報は Cloudflare のエッジネットワークから取得しています。",
                ui="中国語（簡体字）",
                features=["現在のグローバルIPをすぐに表示", "おおよその位置と地図を表示", "Cloudflare のエッジネットワークを利用"],
                steps=["ページを開く", "読み込みが終わったら、IPと位置情報を確認"],
                faq=[("位置は正確ですか？", "IPから分かるのはおおよその地域だけで、正確な住所ではありません。"),
                     ("実際の場所と違うのはなぜですか？", "VPN やプロキシ、一部のモバイル回線を使っている場合は、出口サーバーの位置が表示されます。")]),
        en=dict(name="IP Lookup",
                title="IP Lookup｜See Your Public IP and Location | wangtaiyang.com",
                desc="A free IP lookup tool. See your current public IP address and approximate location on a map. Powered by Cloudflare's edge network.",
                lead="Open the page to see your current public IP address and its approximate location on a map. The data comes from Cloudflare's edge network.",
                ui="Simplified Chinese",
                features=["Shows your current public IP right away", "Approximate location with a map", "Powered by Cloudflare's edge network"],
                steps=["Open the page", "Wait for it to load, then read your IP and location"],
                faq=[("How accurate is the location?", "IP geolocation only shows a rough area, not your exact address."),
                     ("Why does it show a different place from where I am?", "If you use a VPN, a proxy or some mobile networks, you will see the location of the exit server.")]),
    ),
    dict(
        slug="resume-builder", host="r", category="BusinessApplication",
        zh=dict(name="AI 簡歷製作",
                title="AI 簡歷製作｜50+ 模板，自動翻譯成日文與英文 | wangtaiyang.com",
                desc="免費線上簡歷製作工具：50 多個模板，填寫內容後可用 AI 自動翻譯成日文與英文，並列印或存成 PDF。API Key 只在瀏覽器內處理。",
                lead="選一個模板，填好內容，再用 AI 自動翻譯成日文與英文版本。適合在日本或海外找工作時使用。",
                ui="中文、日文、英文",
                features=["50 多個模板，分為極簡、商務、科技、創意、高管、國際等類別",
                          "姓名、聯絡方式、自我介紹、技能、工作經歷、學歷、證照等欄位，也可以自訂欄位",
                          "AI 自動翻譯成日文與英文，以分頁切換",
                          "列印或存成 PDF",
                          "支援 Anthropic Claude、Google Gemini、DeepSeek 的 API Key"],
                steps=["選擇模板", "填寫簡歷內容", "設定自己的 AI API Key，產生日文與英文版本", "列印或存成 PDF"],
                faq=[("需要付費嗎？", "工具本身免費。AI 翻譯需要使用你自己的 API Key，費用由對應的 AI 服務商依用量收取。"),
                     ("API Key 安全嗎？", "依工具說明，API Key 以 AES-256 加密，只在你的瀏覽器內處理，不會上傳到伺服器；清除瀏覽器資料後就會刪除。"),
                     ("可以做日文履歷嗎？", "可以。填好內容後，能自動翻譯成日文與英文版本。")]),
        ja=dict(name="AI履歴書作成",
                title="AI履歴書作成｜50以上のテンプレート・日本語と英語に自動翻訳 | wangtaiyang.com",
                desc="無料のオンライン履歴書作成ツールです。50以上のテンプレートから選び、入力した内容をAIで日本語と英語に自動翻訳できます。印刷やPDF保存にも対応。APIキーはブラウザ内だけで処理されます。",
                lead="テンプレートを選んで内容を入力し、AIで日本語版と英語版を自動で作れます。日本や海外での就職活動に向いています。",
                ui="中国語・日本語・英語",
                features=["50以上のテンプレート（ミニマル、ビジネス、テック、クリエイティブ、エグゼクティブ、インターナショナル）",
                          "氏名、連絡先、自己紹介、スキル、職歴、学歴、資格などの項目。項目の追加も可能",
                          "AIで日本語と英語に自動翻訳。タブで切り替え",
                          "印刷・PDF保存",
                          "Anthropic Claude、Google Gemini、DeepSeek の APIキーに対応"],
                steps=["テンプレートを選ぶ", "履歴書の内容を入力", "自分のAI APIキーを設定し、日本語版と英語版を作成", "印刷またはPDFで保存"],
                faq=[("料金はかかりますか？", "ツール自体は無料です。AI翻訳にはご自身の APIキーを使うため、各AIサービスの利用料金がかかります。"),
                     ("APIキーは安全ですか？", "ツールの説明では、APIキーは AES-256 で暗号化され、ブラウザ内だけで処理されてサーバーには送信されません。ブラウザのデータを消去すると削除されます。"),
                     ("日本語の履歴書を作れますか？", "はい。入力した内容を日本語と英語に自動翻訳できます。")]),
        en=dict(name="AI Résumé Builder",
                title="AI Résumé Builder｜50+ Templates, Auto-translate to Japanese and English | wangtaiyang.com",
                desc="A free online résumé builder with 50+ templates. Write your résumé, auto-translate it into Japanese and English with AI, then print or save as PDF. Your API key stays in your browser.",
                lead="Pick a template, fill it in, and let AI create Japanese and English versions. Useful when job hunting in Japan or abroad.",
                ui="Chinese, Japanese, English",
                features=["50+ templates: minimal, business, tech, creative, executive and international",
                          "Sections for contact details, summary, skills, experience, education and certificates, plus custom sections",
                          "AI auto-translation into Japanese and English, shown in tabs",
                          "Print or save as PDF",
                          "Works with Anthropic Claude, Google Gemini and DeepSeek API keys"],
                steps=["Choose a template", "Fill in your résumé", "Add your own AI API key to generate Japanese and English versions", "Print or save as PDF"],
                faq=[("Is it free?", "The tool is free. AI translation uses your own API key, so the AI provider bills you for usage."),
                     ("Is my API key safe?", "According to the tool, your key is encrypted with AES-256 and handled only in your browser, never uploaded to a server. Clearing your browser data deletes it."),
                     ("Can it make a Japanese résumé?", "Yes. It can translate what you write into Japanese and English versions.")]),
    ),
    dict(
        slug="mbti-test", host="mbti", category="LifestyleApplication",
        zh=dict(name="MBTI 性格測試（200 題）",
                title="免費 MBTI 性格測試｜200 題細測、附信心度與成長計畫 | wangtaiyang.com",
                desc="免費線上 MBTI 風格性格測試，共 200 題。完成後顯示性格類型與信心度，可編輯成長計畫，並匯出 JSON。",
                lead="200 題的性格細測，幫助你了解自己的傾向。完成後會顯示類型與信心度，並附可編輯的成長計畫。",
                ui="簡體中文",
                features=["200 題細測", "顯示性格類型與信心度", "可編輯的成長計畫", "結果可匯出為 JSON"],
                steps=["打開測試並依序作答", "查看類型與信心度", "整理成長計畫，需要時匯出結果"],
                faq=[("這是官方 MBTI 測驗嗎？", "不是。這是參考 MBTI 類型架構做的自我了解工具，不是 The Myers-Briggs Company 的官方 MBTI® 測驗。"),
                     ("結果可以當作求職或診斷依據嗎？", "不建議。結果只適合用來自我反思。")],
                note="MBTI® 是 The Myers-Briggs Company 的註冊商標。本工具與該公司無關。"),
        ja=dict(name="MBTI性格診断（200問）",
                title="無料MBTI性格診断｜200問の詳細テスト・信頼度と成長プラン付き | wangtaiyang.com",
                desc="無料のオンラインMBTI風性格診断です。全200問。結果として性格タイプと信頼度を表示し、成長プランを編集したり、JSONで書き出したりできます。",
                lead="200問の詳しい性格テストで、自分の傾向を知るためのツールです。結果にはタイプと信頼度が表示され、編集できる成長プランも付きます。",
                ui="中国語（簡体字）",
                features=["200問の詳細テスト", "性格タイプと信頼度を表示", "編集できる成長プラン", "結果をJSONで書き出し"],
                steps=["テストを開いて順に回答", "タイプと信頼度を確認", "成長プランを整え、必要なら結果を書き出す"],
                faq=[("公式のMBTIですか？", "いいえ。MBTIのタイプ分類を参考にした自己理解のためのツールで、The Myers-Briggs Company による公式の MBTI® 検査ではありません。"),
                     ("就職や診断の根拠に使えますか？", "おすすめしません。自分を振り返るための参考としてお使いください。")],
                note="MBTI® は The Myers-Briggs Company の登録商標です。本ツールは同社とは関係ありません。"),
        en=dict(name="MBTI Personality Test (200 questions)",
                title="Free MBTI-style Personality Test｜200 Questions, Confidence Score and Growth Plan | wangtaiyang.com",
                desc="A free online MBTI-style personality test with 200 questions. See your type and a confidence level, edit a growth plan, and export results as JSON.",
                lead="A detailed 200-question personality test for self-reflection. You get a type, a confidence level and an editable growth plan.",
                ui="Simplified Chinese",
                features=["200 detailed questions", "Personality type with a confidence level", "Editable growth plan", "Export results as JSON"],
                steps=["Open the test and answer each question", "Read your type and confidence level", "Work on your growth plan and export if needed"],
                faq=[("Is this the official MBTI?", "No. It is a self-reflection tool based on the MBTI type framework, not the official MBTI® assessment from The Myers-Briggs Company."),
                     ("Can I use it for hiring or diagnosis?", "Not recommended. Use it for self-reflection only.")],
                note="MBTI® is a registered trademark of The Myers-Briggs Company. This tool is not affiliated with it."),
    ),
    dict(
        slug="i-ching", host="zhouyi", category="LifestyleApplication",
        zh=dict(name="周易 64 卦占卜",
                title="周易 64 卦線上占卜｜本卦、變卦、變爻解讀 | wangtaiyang.com",
                desc="免費線上周易占卜：輸入問題並選擇主題，得到本卦與變卦，以及卦辭、彖辭、變爻與綜合解讀。僅供參考。",
                lead="輸入你想問的事，選擇主題後起卦。結果會列出本卦（現狀）、變卦（結局），以及卦辭、變爻與綜合解讀。",
                ui="簡體中文",
                features=["涵蓋 64 卦", "六種主題：綜合、姓名／代碼、婚姻感情、事業、搬遷出行、財運投資",
                          "本卦（現狀）與變卦（結局）", "卦辭、彖辭與變爻解讀", "綜合指引"],
                steps=["輸入問題或關鍵字", "選擇主題", "起卦並閱讀解讀"],
                faq=[("結果準確嗎？", "周易占卜屬於傳統文化與自我反思的參考，不能作為醫療、法律或投資決策的依據。")],
                note="結果僅供參考與娛樂。"),
        ja=dict(name="易経64卦占い",
                title="易経64卦オンライン占い｜本卦・変卦・変爻の解説 | wangtaiyang.com",
                desc="無料のオンライン易経占いです。質問を入力してテーマを選ぶと、本卦と変卦、卦辞・彖辞・変爻、総合的な解説が表示されます。参考程度にお楽しみください。",
                lead="知りたいことを入力し、テーマを選んで卦を立てます。本卦（現状）と変卦（結末）、卦辞・変爻、総合的な解説が表示されます。",
                ui="中国語（簡体字）",
                features=["64卦すべてに対応", "6つのテーマ：総合、名前・番号、結婚・恋愛、仕事、引っ越し・旅行、金運・投資",
                          "本卦（現状）と変卦（結末）", "卦辞・彖辞と変爻の解説", "総合的なアドバイス"],
                steps=["質問やキーワードを入力", "テーマを選ぶ", "卦を立てて解説を読む"],
                faq=[("結果は当たりますか？", "易経の占いは伝統文化や自己を振り返るための参考です。医療・法律・投資の判断には使わないでください。")],
                note="結果は参考・娯楽としてお楽しみください。"),
        en=dict(name="I Ching 64 Hexagram Reading",
                title="Free I Ching Reading Online｜64 Hexagrams, Changing Lines Explained | wangtaiyang.com",
                desc="A free online I Ching reading. Enter a question, pick a topic, and get a primary and changed hexagram with the judgment, changing lines and an overall reading. For reference only.",
                lead="Type your question, pick a topic and cast. You get the primary hexagram (the present), the changed hexagram (the outcome), the judgment, the changing lines and an overall reading.",
                ui="Simplified Chinese",
                features=["All 64 hexagrams", "Six topics: general, name or number, love and marriage, career, moving and travel, money and investment",
                          "Primary hexagram (present) and changed hexagram (outcome)", "Judgment, commentary and changing lines", "Overall guidance"],
                steps=["Enter a question or keyword", "Choose a topic", "Cast and read the interpretation"],
                faq=[("Is it accurate?", "An I Ching reading is a cultural tradition and a prompt for reflection. Do not use it for medical, legal or investment decisions.")],
                note="For reference and entertainment only."),
    ),
    dict(
        slug="numerology", host="lifecode", category="LifestyleApplication",
        zh=dict(name="數字命理（生命密碼）",
                title="數字命理計算｜生命靈數、天賦九宮格、姓名數字 | wangtaiyang.com",
                desc="免費線上數字命理工具：輸入生日與姓名，產生生命靈數、天賦九宮格、人生金字塔、姓名數字與年月日運勢。參考 David A. Phillips 的數字命理體系。",
                lead="輸入出生日期與姓名（拼音或英文），產生一份完整的數字命理報告。內容參考 David A. Phillips 的《The Complete Book of Numerology》。",
                ui="簡體中文",
                features=["生命靈數（主命數）：天賦與人生課題", "天賦九宮格：1 到 9 的數字分佈與連線、缺數分析",
                          "人生金字塔：各階段的機會與挑戰", "姓名數字：表達數、靈魂數、人格數",
                          "年、月、日運勢", "綜合解讀與建議"],
                steps=["輸入出生日期", "輸入姓名（拼音或英文）", "產生報告並閱讀各部分"],
                faq=[("姓名要怎麼輸入？", "請用拼音或英文字母輸入全名，工具會依字母計算姓名數字。"),
                     ("結果有科學根據嗎？", "沒有。數字命理是一種傳統的解讀方式，適合用來自我探索與娛樂。")],
                note="結果僅供參考與娛樂。"),
        ja=dict(name="数秘術（ライフコード）",
                title="数秘術計算｜ライフパスナンバー・才能グリッド・名前の数字 | wangtaiyang.com",
                desc="無料のオンライン数秘術ツールです。生年月日と名前を入力すると、ライフパスナンバー、才能グリッド、人生のピラミッド、名前の数字、年・月・日の運勢を表示します。David A. Phillips の数秘術を参考にしています。",
                lead="生年月日と名前（ピンインまたは英字）を入力すると、数秘術のレポートを作成します。David A. Phillips の『The Complete Book of Numerology』を参考にしています。",
                ui="中国語（簡体字）",
                features=["ライフパスナンバー：才能と人生の課題", "才能グリッド：1〜9の数字の分布、つながりと欠けている数字の分析",
                          "人生のピラミッド：各時期のチャンスと試練", "名前の数字：表現数、ソウル数、パーソナリティ数",
                          "年・月・日の運勢", "総合的な解説とアドバイス"],
                steps=["生年月日を入力", "名前をピンインまたは英字で入力", "レポートを作成して各項目を読む"],
                faq=[("名前はどう入力しますか？", "フルネームをピンインまたはアルファベットで入力してください。文字から名前の数字を計算します。"),
                     ("科学的な根拠はありますか？", "ありません。数秘術は伝統的な読み解き方の一つで、自己探求や娯楽として楽しむものです。")],
                note="結果は参考・娯楽としてお楽しみください。"),
        en=dict(name="Numerology (Life Code)",
                title="Free Numerology Calculator｜Life Path Number, Talent Grid, Name Numbers | wangtaiyang.com",
                desc="A free online numerology tool. Enter your birth date and name to get your life path number, talent grid, pinnacles and challenges, name numbers and yearly, monthly and daily readings. Based on David A. Phillips' system.",
                lead="Enter your birth date and full name (in pinyin or English letters) to get a full numerology report, based on David A. Phillips' The Complete Book of Numerology.",
                ui="Simplified Chinese",
                features=["Life path number: talents and life challenges", "Talent grid: how digits 1 to 9 fall, with connections and missing numbers",
                          "Pinnacles and challenges for each stage of life", "Name numbers: expression, soul urge and personality",
                          "Yearly, monthly and daily readings", "An overall reading with advice"],
                steps=["Enter your birth date", "Enter your full name in pinyin or English letters", "Generate the report and read each part"],
                faq=[("How should I enter my name?", "Type your full name in pinyin or English letters. The name numbers are calculated from the letters."),
                     ("Is it scientific?", "No. Numerology is a traditional way of reading numbers, best used for self-exploration and fun.")],
                note="For reference and entertainment only."),
    ),
    dict(
        slug="minesweeper", host="saolei", category="GameApplication",
        zh=dict(name="掃雷",
                title="線上掃雷小遊戲｜三種難度、免下載 | wangtaiyang.com",
                desc="免費線上掃雷：簡單、中等、困難三種難度，附計時器與剩餘地雷數。瀏覽器直接玩，無需下載。",
                lead="經典掃雷，打開就能玩。有簡單、中等、困難三種難度，畫面上會顯示計時與剩餘地雷數。",
                ui="簡體中文",
                features=["簡單、中等、困難三種難度", "計時器與剩餘地雷數", "一鍵重新開始", "瀏覽器直接玩，無需下載"],
                steps=["選擇難度", "點擊格子翻開，數字代表周圍八格中的地雷數", "翻開所有安全格子即獲勝"],
                faq=[("規則是什麼？", "翻開的數字表示周圍八格中有幾顆地雷。根據數字推理，避開地雷，翻開所有安全的格子就贏了。")]),
        ja=dict(name="マインスイーパー",
                title="オンライン・マインスイーパー｜3つの難易度・ダウンロード不要 | wangtaiyang.com",
                desc="無料のオンライン・マインスイーパーです。初級・中級・上級の3つの難易度があり、タイマーと残りの地雷数を表示します。ブラウザですぐに遊べます。",
                lead="定番のマインスイーパーを、開いてすぐに遊べます。初級・中級・上級の3つの難易度があり、タイマーと残りの地雷数が表示されます。",
                ui="中国語（簡体字）",
                features=["初級・中級・上級の3つの難易度", "タイマーと残りの地雷数", "ワンクリックでやり直し", "ブラウザで遊べてダウンロード不要"],
                steps=["難易度を選ぶ", "マスをクリックして開く。数字は周囲8マスにある地雷の数", "安全なマスをすべて開けばクリア"],
                faq=[("ルールは？", "開いたマスの数字は、周りの8マスにある地雷の数です。数字から推理して地雷を避け、安全なマスをすべて開けばクリアです。")]),
        en=dict(name="Minesweeper",
                title="Play Minesweeper Online｜Three Difficulty Levels, No Download | wangtaiyang.com",
                desc="Play Minesweeper free in your browser. Three difficulty levels, a timer and a mine counter. No download needed.",
                lead="Classic Minesweeper that opens and plays right away. Choose easy, medium or hard, with a timer and a mine counter on screen.",
                ui="Simplified Chinese",
                features=["Easy, medium and hard levels", "Timer and mine counter", "One-click restart", "Runs in the browser, no download"],
                steps=["Choose a difficulty", "Click a square to reveal it. A number shows how many mines touch that square", "Reveal every safe square to win"],
                faq=[("What are the rules?", "Each number tells you how many of the eight surrounding squares hold a mine. Use the numbers to avoid the mines and reveal every safe square.")]),
    ),
    dict(
        slug="short-link", host="link", category="UtilitiesApplication",
        zh=dict(name="短網址",
                title="短網址產生器｜把長網址變短 | wangtaiyang.com",
                desc="免費短網址工具：把很長的網址轉成簡短的連結，方便分享。",
                lead="把很長的網址轉成簡短的連結，方便貼在訊息、社群或文件裡。",
                ui="中文",
                features=["把長網址轉成短網址", "打開網頁即可使用"],
                steps=["貼上要縮短的網址", "產生短網址並複製"],
                faq=[]),
        ja=dict(name="短縮URL",
                title="短縮URL作成｜長いURLを短く | wangtaiyang.com",
                desc="無料の短縮URLツールです。長いURLを短いリンクに変換して、共有しやすくします。",
                lead="長いURLを短いリンクに変換します。メッセージやSNS、資料に貼るときに便利です。",
                ui="中国語",
                features=["長いURLを短縮", "ブラウザで開くだけで使える"],
                steps=["短くしたいURLを貼り付ける", "短縮URLを作成してコピー"],
                faq=[]),
        en=dict(name="Short Link",
                title="Short Link Generator｜Make Long URLs Short | wangtaiyang.com",
                desc="A free URL shortener. Turn long links into short ones that are easy to share.",
                lead="Turn a long URL into a short link that is easy to paste into messages, social posts or documents.",
                ui="Chinese",
                features=["Shorten long URLs", "Works in the browser"],
                steps=["Paste the URL to shorten", "Create the short link and copy it"],
                faq=[]),
    ),
]


def esc(s):
    return html.escape(str(s), quote=True)


def tool_url(t):
    return f"https://{t['host']}.wangtaiyang.com/"


def page_path(lang, slug=None):
    base = PREFIX[lang] + "tools/"
    return base + (f"{slug}/" if slug else "")


def head(lang, title, desc, path, ld, alt_paths):
    url = BASE + path
    alts = "".join(
        f'<link rel="alternate" hreflang="{HREFLANG[k]}" href="{BASE}{alt_paths[k]}">' for k in LANGS
    ) + f'<link rel="alternate" hreflang="x-default" href="{BASE}{alt_paths["zh"]}">'
    return f"""<!doctype html>
<html lang="{HREFLANG[lang]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="author" content="Taiyang Wang">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{url}">
{alts}
<meta property="og:type" content="website">
<meta property="og:site_name" content="wangtaiyang.com">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="{OG_LOCALE[lang]}">
<meta property="og:image" content="{BASE}/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE}/og.png">
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
<link rel="stylesheet" href="/clean.css">
{ADSENSE}</head>"""


def topbar(lang, alt_paths):
    u = UI[lang]
    current = ' aria-current="page"'
    switch = "".join(
        f'<a href="{alt_paths[k]}" hreflang="{HREFLANG[k]}"{current if k == lang else ""}>{LANG_LABEL[k]}</a>'
        for k in LANGS
    )
    return f"""<a class="skip" href="#main">{esc(u['skip'])}</a>
<header class="top">
  <div class="wrap bar">
    <a class="brand" href="{PREFIX[lang]}">wangtaiyang<span>.com</span></a>
    <nav class="menu"><a href="{PREFIX[lang]}">{esc(u['home'])}</a><a href="{page_path(lang)}">{esc(u['tools'])}</a></nav>
    <div class="lang">{switch}</div>
  </div>
</header>"""


def footer(lang):
    return f"""<footer class="foot">
  <div class="wrap">
    <div class="foot-row">
      <span class="muted">© 2026 王太陽 Taiyang Wang · <a href="mailto:{EMAIL}">{EMAIL}</a></span>
      <a href="{page_path(lang)}">{esc(UI[lang]['all_tools'])}</a>
    </div>
  </div>
</footer>"""


def tool_page(lang, t):
    u = UI[lang]
    c = t[lang]
    path = page_path(lang, t["slug"])
    alt_paths = {k: page_path(k, t["slug"]) for k in LANGS}
    faq_ld = [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in c["faq"]
    ]
    graph = [
        {"@type": "WebApplication", "@id": BASE + path + "#app", "name": c["name"], "url": tool_url(t),
         "description": c["desc"], "applicationCategory": t["category"], "operatingSystem": "Web browser",
         "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
         "author": {"@id": BASE + "/#person"}, "mainEntityOfPage": BASE + path},
        {"@type": "Person", "@id": BASE + "/#person", "name": "王太陽", "alternateName": "Taiyang Wang", "url": BASE + "/"},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": u["home"], "item": BASE + PREFIX[lang]},
            {"@type": "ListItem", "position": 2, "name": u["tools"], "item": BASE + page_path(lang)},
            {"@type": "ListItem", "position": 3, "name": c["name"], "item": BASE + path},
        ]},
    ]
    if faq_ld:
        graph.append({"@type": "FAQPage", "mainEntity": faq_ld})
    ld = {"@context": "https://schema.org", "@graph": graph}

    features = "".join(f"<li>{esc(x)}</li>" for x in c["features"])
    steps = "".join(f"<li>{esc(x)}</li>" for x in c["steps"])
    faq = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in c["faq"])
    faq_block = f'<section class="tp-sec"><h2>{esc(u["faq"])}</h2><div class="faq">{faq}</div></section>' if faq else ""
    note = f'<p class="tp-note"><strong>{esc(u["note"])}：</strong>{esc(c["note"])}</p>' if c.get("note") else ""
    related = "".join(
        f'<a class="tool" href="{page_path(lang, o["slug"])}"><span class="tool-host">{esc(o["host"])}</span>'
        f'<strong>{esc(o[lang]["name"])}</strong></a>'
        for o in [x for x in TOOLS if x["slug"] != t["slug"]][:4]
    )
    return f"""{head(lang, c['title'], c['desc'], path, ld, alt_paths)}
<body>
{topbar(lang, alt_paths)}
<main id="main" class="wrap tp">
  <nav class="crumbs" aria-label="breadcrumb">
    <a href="{PREFIX[lang]}">{esc(u['home'])}</a><span>›</span><a href="{page_path(lang)}">{esc(u['tools'])}</a><span>›</span><span>{esc(c['name'])}</span>
  </nav>
  <header class="tp-head">
    <span class="tool-host">{esc(t['host'])}.wangtaiyang.com</span>
    <h1>{esc(c['name'])}</h1>
    <p class="lead">{esc(c['lead'])}</p>
    <div class="cta">
      <a class="btn" href="{tool_url(t)}">{esc(u['open'])} →</a>
    </div>
    <p class="muted tp-meta">{esc(u['free'])} · {esc(u['ui_lang'])}：{esc(c['ui'])} · {esc(u['author'])}：<a href="{PREFIX[lang]}#about">Taiyang Wang</a></p>
  </header>
  <section class="tp-sec"><h2>{esc(u['features'])}</h2><ul class="tp-list">{features}</ul></section>
  <section class="tp-sec"><h2>{esc(u['how'])}</h2><ol class="tp-steps">{steps}</ol></section>
  {faq_block}
  {note}
  <section class="tp-sec"><h2>{esc(u['related'])}</h2><div class="tools">{related}</div></section>
</main>
{footer(lang)}
</body>
</html>
"""


def index_page(lang):
    u = UI[lang]
    path = page_path(lang)
    alt_paths = {k: page_path(k) for k in LANGS}
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": BASE + path, "url": BASE + path, "name": u["index_h1"],
         "description": u["index_desc"], "inLanguage": HREFLANG[lang], "about": {"@id": BASE + "/#person"}},
        {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": t[lang]["name"], "url": BASE + page_path(lang, t["slug"])}
            for i, t in enumerate(TOOLS)
        ]},
    ]}
    cards = "".join(
        f'<a class="tool" href="{page_path(lang, t["slug"])}"><span class="tool-host">{esc(t["host"])}</span>'
        f'<strong>{esc(t[lang]["name"])}</strong><span class="muted">{esc(t[lang]["lead"])}</span></a>'
        for t in TOOLS
    )
    return f"""{head(lang, u['index_title'], u['index_desc'], path, ld, alt_paths)}
<body>
{topbar(lang, alt_paths)}
<main id="main" class="wrap tp">
  <nav class="crumbs" aria-label="breadcrumb"><a href="{PREFIX[lang]}">{esc(u['home'])}</a><span>›</span><span>{esc(u['tools'])}</span></nav>
  <header class="tp-head">
    <h1>{esc(u['index_h1'])}</h1>
    <p class="lead">{esc(u['index_lead'])}</p>
  </header>
  <div class="tools">{cards}</div>
  <p class="all"><a href="{PREFIX[lang]}#tools">{esc(u['more'])} →</a></p>
</main>
{footer(lang)}
</body>
</html>
"""


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    n = 0
    for lang in LANGS:
        write(os.path.join(SITE, page_path(lang).lstrip("/"), "index.html"), index_page(lang))
        n += 1
        for t in TOOLS:
            write(os.path.join(SITE, page_path(lang, t["slug"]).lstrip("/"), "index.html"), tool_page(lang, t))
            n += 1
    print(f"built {n} tool pages")


if __name__ == "__main__":
    main()
