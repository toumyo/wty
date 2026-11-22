#!/usr/bin/env python3
"""Generate the clean, light trilingual homepage (zh-Hant / ja / en).

Writes site/index.html, site/ja/index.html, site/en/index.html and site/clean.css.
The private nav (site/n/) and news pages are handled elsewhere and are not touched.
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
BASE = "https://wangtaiyang.com"
EMAIL = "wangtaiyang369@gmail.com"
ADSENSE = ('<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9381195976626834"\n'
           '     crossorigin="anonymous"></script>\n')

# tools Taiyang built himself -> landing page slug (see scripts/build_tools.py)
OWN = {"hl": "currency-converter", "ip": "ip-lookup", "r": "resume-builder", "mbti": "mbti-test",
       "zhouyi": "i-ching", "lifecode": "numerology", "saolei": "minesweeper", "link": "short-link"}

# host, group index, zh name, zh desc, ja name, ja desc, en name, en desc
TOOLS = [
    ("ai", 0, "AI導航", "常用 AI 工具分類整理", "AIナビ", "よく使うAIツールを分類整理", "AI Navigator", "Curated AI tools by use case"),
    ("mind", 0, "思維導圖", "線上繪製思維導圖", "マインドマップ", "オンラインでマインドマップを作成", "Mind Map", "Draw mind maps online"),
    ("draw", 0, "線上草圖", "快速繪製流程圖與草稿", "オンラインスケッチ", "フローチャートや下書きをすばやく", "Online Sketch", "Quick flowcharts and sketches"),
    ("tools", 0, "設計工具", "常用設計小工具集合", "デザインツール", "よく使うデザイン小ツール集", "Design Tools", "A set of small design utilities"),
    ("api", 0, "詞元", "文字詞元相關工具與接口", "トークン", "テキストトークン関連ツールとAPI", "Tokens", "Text token utilities and API"),
    ("hl", 1, "匯率換算", "多幣別即時換算", "為替換算", "多通貨のリアルタイム換算", "Currency Converter", "Multi-currency conversion"),
    ("calculation", 1, "線上計算機", "科學計算與日常換算", "オンライン電卓", "科学計算と日常の換算", "Online Calculator", "Scientific and everyday math"),
    ("ip", 1, "IP 查詢", "查看公網 IP 與基本資訊", "IPアドレス確認", "公開IPと基本情報を確認", "IP Lookup", "Check your public IP details"),
    ("ittools", 1, "IT 工具箱", "開發者常用的編碼與格式工具", "ITツールボックス", "開発者向けのエンコード・整形ツール", "IT Toolbox", "Encoding and formatting for developers"),
    ("link", 1, "短鏈接", "產生簡潔的短網址", "短縮URL", "簡潔な短縮リンクを作成", "Short Links", "Create clean short links"),
    ("r", 2, "簡歷製作", "線上製作並匯出履歷", "履歴書作成", "オンラインで履歴書を作成・書き出し", "Resume Builder", "Build and export résumés online"),
    ("sports", 2, "健身記錄", "記錄訓練內容與進度", "フィットネス記録", "トレーニング内容と進捗を記録", "Fitness Log", "Track workouts and progress"),
    ("mbti", 2, "MBTI 測試", "人格類型測試", "MBTIテスト", "性格タイプ診断", "MBTI Test", "Personality type quiz"),
    ("zhouyi", 2, "周易", "周易卦象查詢，僅供參考", "易経", "易の卦を調べる（参考程度）", "I Ching", "Hexagram lookup, for reference only"),
    ("lifecode", 2, "數字命理學", "數字命理查詢，僅供參考", "数秘術", "数字による占い（参考程度）", "Numerology", "Number-based reading, for reference only"),
    ("saolei", 2, "掃雷", "經典掃雷小遊戲", "マインスイーパー", "定番の地雷探しゲーム", "Minesweeper", "The classic puzzle game"),
    ("radio", 2, "線上收音機", "收聽網路電台", "オンラインラジオ", "インターネットラジオを聴く", "Online Radio", "Listen to web radio"),
]

T = {
    "zh": dict(
        lang="zh-Hant", path="/", label="繁體", og_locale="zh_TW",
        title="王太陽 Taiyang Wang｜網站、工具與財經新聞 · 大阪 Web 設計 | wangtaiyang.com",
        desc="王太陽（Taiyang Wang）的個人網站，位於大阪。提供免費線上工具、每日世界財經新聞，以及中日英多語網站設計、SEO 與 GEO 服務。",
        nav=[("工具", "#tools"), ("網站與頻道", "#sites"), ("新聞", "#news"), ("關於", "#about"), ("服務", "#services"), ("聯絡", "#contact")],
        eyebrow="大阪 · 網站設計", meishi_alt="王太陽的名片：東緲合同會社（Toubyou Godo Kaisha），大阪，網站製作、小程式開發、軟體開發、系統維運、影片剪輯",
        h1="王太陽", h1_en="Taiyang Wang",
        lead="網站設計者，也是工具開發者。用中文、日文與英文，做結構清楚、看得懂、搜得到的網站。",
        btn_primary="看工具", btn_secondary="聯絡我",
        tools_title="線上工具", tools_sub="免費使用，無需註冊。", own_badge="自製", own_link="我自製的工具 →",
        news_title="每日財經新聞", news_sub="每天整理美股、日股與重要財經新聞，附原始來源。",
        news_empty="第一篇新聞即將發布。",
        news_all="查看全部新聞 →",
        about_title="關於我", about_sub="Taiyang Wang（王太陽）",
        bio=[
            "我住在大阪，日常用中文、日文與英文工作。經營網站設計公司「東緲合同會社」，負責從需求整理、介面設計、前端開發，到上線後的 SEO 與 AI 搜尋可見度優化。",
            "我做事的方式偏向實作：先做出能用的版本，再依照數據修正。這個網站本身，就是我拿來驗證這些做法的地方。",
        ],
        facts=[("所在地", "日本 · 大阪"), ("語言", "中文 · 日文 · 英文"), ("公司", "東緲合同會社"), ("業務", "網站設計 · SEO · GEO")],
        services_title="服務", services_sub="面向中國與日本市場的網站設計與搜尋優化。",
        services=[
            ("網站設計與開發", "企業官網、作品集、產品落地頁。響應式設計，支援中日英多語言。"),
            ("SEO 優化", "技術 SEO、關鍵字結構、站內內容與結構化資料，並接上百度、Google、Bing 站長工具。"),
            ("GEO（AI 搜尋優化）", "讓內容更容易被 ChatGPT、Perplexity、Google AI Overviews 引用，包括 llms.txt 與實體資訊建設。"),
        ],
        contact_title="聯絡", contact_lead="目前接受新的案件。告訴我你卡在哪裡，我們一起找出路。",
        contact_label="電郵",
        footer_blurb="網站設計者與工具開發者，把人的直覺與工程邏輯連起來。獨立工作室，大阪。",
        base_l="© 2026 王太陽 Taiyang Wang · 東緲合同會社", base_r="大阪 · Japan",
        skip="跳到正文", back_top="返回頂部",
        group_labels=["AI 與效率", "計算與查詢", "生活與趣味"],
    ),
    "ja": dict(
        lang="ja", path="/ja/", label="日本語", og_locale="ja_JP",
        title="王太陽 Taiyang Wang｜ウェブ制作・ツール・経済ニュース · 大阪 | wangtaiyang.com",
        desc="大阪在住のウェブデザイナー、王太陽（Taiyang Wang）の個人サイトです。無料のオンラインツール、毎日の世界経済ニュース、中国語・日本語・英語のウェブ制作・SEO・GEOを紹介しています。",
        nav=[("ツール", "#tools"), ("サイト・チャンネル", "#sites"), ("ニュース", "#news"), ("プロフィール", "#about"), ("サービス", "#services"), ("連絡", "#contact")],
        eyebrow="大阪 · ウェブ制作", meishi_alt="王太陽の名刺：東緲合同会社（Toubyou Godo Kaisha）、大阪。ウェブサイト制作・ミニプログラム開発・ソフトウェア開発・システム運用保守・動画編集",
        h1="王 太陽", h1_en="Taiyang Wang",
        lead="ウェブデザイナー兼ツール開発者。中国語・日本語・英語で、構造が分かりやすく、検索されるサイトを作ります。",
        btn_primary="ツールを見る", btn_secondary="お問い合わせ",
        tools_title="オンラインツール", tools_sub="無料で使えます。登録は不要です。", own_badge="自作", own_link="自作ツール一覧 →",
        news_title="毎日の経済ニュース", news_sub="米国株・日本株と重要な経済ニュースを毎日まとめ、元の情報源を掲載しています。",
        news_empty="最初のニュースはまもなく公開されます。",
        news_all="すべてのニュースを見る →",
        about_title="プロフィール", about_sub="Taiyang Wang（王太陽）",
        bio=[
            "大阪在住で、中国語・日本語・英語を使って仕事をしています。ウェブ制作会社「東緲合同会社」を経営し、要件整理、デザイン、フロントエンド開発から、公開後の SEO と AI 検索での見つけやすさまで担当しています。",
            "実装を先に進める方針です。まず使えるものを作り、データを見ながら直していきます。このサイト自体が、その方法を試している場所です。",
        ],
        facts=[("拠点", "日本・大阪"), ("言語", "中国語・日本語・英語"), ("会社", "東緲合同会社"), ("業務", "ウェブ制作・SEO/GEO")],
        services_title="サービス", services_sub="中国と日本の市場に向けた、ウェブ制作と検索最適化。",
        services=[
            ("ウェブサイト制作", "企業サイト、ポートフォリオ、製品のランディングページ。レスポンシブ対応、中日英の多言語に対応。"),
            ("SEO 最適化", "テクニカル SEO、キーワード構造、サイト内コンテンツと構造化データ。百度・Google・Bing の管理ツールにも接続します。"),
            ("GEO（AI 検索最適化）", "ChatGPT、Perplexity、Google AI Overviews に引用されやすい内容づくり。llms.txt や実体情報の整備も含みます。"),
        ],
        contact_title="お問い合わせ", contact_lead="現在、新規案件を受け付けています。お困りのことを教えてください。一緒に解決策を考えます。",
        contact_label="メール",
        footer_blurb="人の直感とエンジニアリングの論理をつなぐデジタル体験を作るウェブデザイナーです。独立系、大阪。",
        base_l="© 2026 王太陽 Taiyang Wang · 東緲合同会社", base_r="大阪 · Japan",
        skip="本文へ移動", back_top="トップへ戻る",
        group_labels=["AI・効率", "計算・検索", "暮らし・遊び"],
    ),
    "en": dict(
        lang="en", path="/en/", label="English", og_locale="en_US",
        title="Taiyang Wang｜Web Design, Free Tools & Finance News · Osaka | wangtaiyang.com",
        desc="Personal site of Taiyang Wang, a web designer in Osaka. Free online tools, daily world finance news with sources, and multilingual website design, SEO and GEO in Chinese, Japanese and English.",
        nav=[("Tools", "#tools"), ("Sites & channels", "#sites"), ("News", "#news"), ("About", "#about"), ("Services", "#services"), ("Contact", "#contact")],
        eyebrow="Osaka · Web design", meishi_alt="Business card of Taiyang Wang (王太陽), 東緲合同会社 (Toubyou Godo Kaisha), Osaka: websites, mini programs, software development, system operations and video editing",
        h1="Taiyang", h1_en="Wang",
        lead="Web designer and tool builder. I make multilingual sites in Chinese, Japanese and English that are clear to read and easy to find.",
        btn_primary="Browse tools", btn_secondary="Contact me",
        tools_title="Online tools", tools_sub="Free to use, no sign-up.", own_badge="Built by me", own_link="Tools I built →",
        news_title="Daily finance news", news_sub="Daily highlights on US stocks, Japanese stocks and major economic news, with original sources.",
        news_empty="The first digest will be published soon.",
        news_all="All news →",
        about_title="About", about_sub="Taiyang Wang",
        bio=[
            "I live in Osaka and work in Chinese, Japanese and English. I run a web design company, Toubyou Godo Kaisha, covering requirements, interface design, front-end development, and after launch, SEO and visibility in AI search.",
            "I prefer to build first: ship something usable, then refine it with data. This site is where I test these methods myself.",
        ],
        facts=[("Based", "Osaka, Japan"), ("Languages", "Chinese · Japanese · English"), ("Company", "Toubyou Godo Kaisha"), ("Services", "Web design · SEO · GEO")],
        services_title="Services", services_sub="Website design and search optimization for the Chinese and Japanese markets.",
        services=[
            ("Website design & development", "Corporate sites, portfolios and product landing pages. Responsive, with multilingual support in Chinese, Japanese and English."),
            ("SEO optimization", "Technical SEO, keyword structure, on-page content and structured data, connected to Baidu, Google and Bing webmaster tools."),
            ("GEO (AI search visibility)", "Content built to be cited by ChatGPT, Perplexity and Google AI Overviews, including llms.txt and entity setup."),
        ],
        contact_title="Contact", contact_lead="Currently booking new projects. Tell me where you're stuck, and we'll map the way out.",
        contact_label="Email",
        footer_blurb="A web designer connecting human intuition with engineering logic. Independent studio, Osaka.",
        base_l="© 2026 Taiyang Wang · Toubyou Godo Kaisha", base_r="Osaka · Japan",
        skip="Skip to content", back_top="Back to top",
        group_labels=["AI & productivity", "Calculate & look up", "Life & fun"],
    ),
}


# Other sites and channels Taiyang runs. Descriptions come from each site's own pages.
SITES_TEXT = {
    "zh": dict(title="我的網站與頻道", sub="我經營的其他網站，以及影片頻道。", sites="網站", channels="頻道",
               wechat_hint="在微信搜尋「{name}」", visit="前往"),
    "ja": dict(title="運営サイト・チャンネル", sub="運営しているほかのサイトと動画チャンネルです。", sites="サイト", channels="チャンネル",
               wechat_hint="WeChat で「{name}」を検索", visit="開く"),
    "en": dict(title="My sites & channels", sub="Other sites I run, and my video channels.", sites="Sites", channels="Channels",
               wechat_hint="Search \u201c{name}\u201d in WeChat", visit="Visit"),
}
SITES = [
    dict(url="https://toumyou.com/", host="toumyou.com", name=dict(zh="東緲合同會社", ja="東緲合同会社", en="東緲合同会社 (Toumyou)"),
         desc=dict(zh="公司官網：網站製作、系統開發、設計與 IT 維運，支援日、中、英三語。",
                   ja="会社の公式サイト。Webサイト制作、システム開発、デザイン、IT運用保守。日本語・中国語・英語に対応。",
                   en="Company site: websites, software development, design and IT operations, in Japanese, Chinese and English.")),
    dict(url="https://kobox.ai/", host="kobox.ai", name=dict(zh="Kobox AI", ja="Kobox AI", en="Kobox AI"),
         desc=dict(zh="用 AI 對話練習英語與日語的學習應用。",
                   ja="AIとの会話で英語と日本語を実践的に学べる学習アプリ。",
                   en="A learning app for practising English and Japanese by talking with AI.")),
    dict(url="https://xojoj.com/", host="xojoj.com", name=dict(zh="小蝦米 Xiami", ja="小蝦米 Xiami", en="Xiami"),
         desc=dict(zh="免費線上鬥地主、象棋、麻將、五子棋與 2048 等小遊戲，可與 AI 或真人對戰。",
                   ja="闘地主・中国象棋・麻雀・五目並べ、2048 などのミニゲームを無料で。AIや他のプレイヤーと対戦できます。",
                   en="Free online Dou Dizhu, xiangqi, mahjong, gomoku and casual games like 2048, against AI or real players.")),
]
CHANNELS = [
    dict(url="https://www.youtube.com/@maliquankai", platform="YouTube", name=dict(zh="碼力全開", ja="碼力全開", en="碼力全開"),
         desc=dict(zh="AI 主題頻道：AI 工具、開源軟體與科技新聞。",
                   ja="AIがテーマのチャンネル。AIツール、オープンソースソフト、テックニュース。",
                   en="An AI channel: AI tools, open-source software and tech news.")),
    dict(url="https://www.youtube.com/@moneypassword", platform="YouTube", name=dict(zh="財富密碼world", ja="財富密碼world", en="財富密碼world"),
         desc=dict(zh="財經解讀、企業歷史，以及日語學習影片。",
                   ja="お金と経済の解説、企業の歴史、日本語学習の動画。",
                   en="Finance explainers, company histories and Japanese-learning videos.")),
    dict(url=None, platform="微信視頻號", name=dict(zh="財富密碼world", ja="財富密碼world", en="財富密碼world"),
         platform_l=dict(zh="微信視頻號", ja="WeChat チャンネル", en="WeChat Channels"),
         desc=dict(zh="日本新聞與中文翻譯，以及日語學習（JLPT 詞彙）影片。",
                   ja="日本のニュースと中国語訳、日本語学習（JLPT 語彙）の動画。",
                   en="Japanese news with Chinese translation, plus Japanese-learning (JLPT vocabulary) videos.")),
]


def esc(s):
    return html.escape(s, quote=True)


def jsonld(lang):
    t = T[lang]
    url = BASE + t["path"]
    graph = [
        {"@type": "WebSite", "@id": BASE + "/#website", "url": BASE + "/", "name": "wangtaiyang.com",
         "inLanguage": t["lang"], "publisher": {"@id": BASE + "/#person"}},
        {"@type": "Person", "@id": BASE + "/#person", "name": "王太陽",
         "alternateName": ["Taiyang Wang", "Taiyang"], "url": BASE + "/",
         "knowsLanguage": ["zh", "ja", "en"], "jobTitle": "Web Designer",
         "worksFor": {"@id": BASE + "/#org"}, "email": "mailto:" + EMAIL,
         "sameAs": [c["url"] for c in CHANNELS if c["url"]],
         "address": {"@type": "PostalAddress", "addressLocality": "Osaka", "addressCountry": "JP"}},
        {"@type": "Organization", "@id": BASE + "/#org", "name": "東緲合同會社",
         "alternateName": ["Toubyou Godo Kaisha", "Toumyou"], "url": "https://toumyou.com/",
         "founder": {"@id": BASE + "/#person"},
         "address": {"@type": "PostalAddress", "addressLocality": "Osaka", "addressCountry": "JP"}},
        {"@type": "WebPage", "@id": url, "url": url, "inLanguage": t["lang"], "name": t["title"],
         "description": t["desc"], "about": {"@id": BASE + "/#person"},
         "primaryImageOfPage": BASE + "/og.png"},
        {"@type": "ItemList", "name": "Online tools",
         "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": x[6],
                              "url": f"https://{x[0]}.wangtaiyang.com/"} for i, x in enumerate(TOOLS)]},
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)


def head(lang):
    t = T[lang]
    url = BASE + t["path"]
    return f"""<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(t['title'])}</title>
<meta name="description" content="{esc(t['desc'])}">
<meta name="author" content="Taiyang Wang">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="zh-Hant" href="{BASE}/">
<link rel="alternate" hreflang="ja" href="{BASE}/ja/">
<link rel="alternate" hreflang="en" href="{BASE}/en/">
<link rel="alternate" hreflang="x-default" href="{BASE}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="wangtaiyang.com">
<meta property="og:title" content="{esc(t['title'])}">
<meta property="og:description" content="{esc(t['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="{t['og_locale']}">
<meta property="og:image" content="{BASE}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE}/og.png">
<meta name="theme-color" content="#ffffff">
<script type="application/ld+json">
{jsonld(lang)}
</script>
<link rel="preload" as="image" type="image/webp" href="/assets/img/meishi-1280.webp" imagesrcset="/assets/img/meishi-1280.webp 1280w, /assets/img/meishi-2464.webp 2464w" imagesizes="(max-width: 1040px) 100vw, 1000px">
<link rel="stylesheet" href="/clean.css">
{ADSENSE}</head>"""


def lang_dropdown(current, links):
    """links: list of (lang_key, href, hreflang, label). Shared by the homepage and tool pages."""
    cur_label = next(label for k, _, _, label in links if k == current)
    items = "".join(
        f'<a href="{href}" hreflang="{hl}" lang="{hl}"' + (' aria-current="page"' if k == current else "") + f'>{label}</a>'
        for k, href, hl, label in links
    )
    return ('<details class="lang-dd"><summary aria-label="Language">'
            '<svg viewBox="0 0 24 24" width="15" height="15" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.6" '
            'd="M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18Zm-9 9h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3Z"/></svg>'
            f'<span>{cur_label}</span><svg class="chev" viewBox="0 0 24 24" width="12" height="12" aria-hidden="true">'
            '<path fill="none" stroke="currentColor" stroke-width="2" d="m6 9 6 6 6-6"/></svg></summary>'
            f'<div class="lang-menu">{items}</div></details>' + LANG_DD_JS)


LANG_DD_JS = ("<script>document.addEventListener('click',function(e){document.querySelectorAll('details.lang-dd[open]')"
              ".forEach(function(d){if(!d.contains(e.target))d.removeAttribute('open')})});"
              "document.addEventListener('keydown',function(e){if(e.key==='Escape')document.querySelectorAll('details.lang-dd[open]')"
              ".forEach(function(d){d.removeAttribute('open')})});</script>")


def lang_switch(current):
    return lang_dropdown(current, [(k, T[k]["path"], T[k]["lang"], T[k]["label"]) for k in ["zh", "ja", "en"]])


def tool_groups(lang):
    t = T[lang]
    out = []
    for gi, label in enumerate(t["group_labels"]):
        cards = []
        for host, g, zn, zd, jn, jd, en_, ed in TOOLS:
            if g != gi:
                continue
            name, desc = {"zh": (zn, zd), "ja": (jn, jd), "en": (en_, ed)}[lang]
            href = (t["path"] + "tools/" + OWN[host] + "/") if host in OWN else f"https://{host}.wangtaiyang.com/"
            mine = f'<span class="mine">{esc(t["own_badge"])}</span>' if host in OWN else ""
            cards.append(
                f'<a class="tool" href="{href}">{mine}'
                f'<span class="tool-host">{esc(host)}</span>'
                f'<strong>{esc(name)}</strong><span class="muted">{esc(desc)}</span></a>'
            )
        out.append(f'<h3 class="group">{esc(label)}</h3><div class="tools">{"".join(cards)}</div>')
    return "".join(out)


def sites_section(lang):
    st = SITES_TEXT[lang]
    site_cards = "".join(
        f'<a class="tool" href="{x["url"]}"><span class="tool-host">{esc(x["host"])}</span>'
        f'<strong>{esc(x["name"][lang])}</strong><span class="muted">{esc(x["desc"][lang])}</span></a>'
        for x in SITES
    )
    ch_cards = []
    for x in CHANNELS:
        plat = x.get("platform_l", {}).get(lang, x["platform"])
        inner = (f'<span class="tool-host">{esc(plat)}</span><strong>{esc(x["name"][lang])}</strong>'
                 f'<span class="muted">{esc(x["desc"][lang])}</span>')
        if x["url"]:
            ch_cards.append(f'<a class="tool" href="{x["url"]}">{inner}</a>')
        else:
            hint = st["wechat_hint"].format(name=x["name"][lang])
            ch_cards.append(f'<div class="tool tool-static">{inner}<span class="hint">{esc(hint)}</span></div>')
    return (f'<section class="block wrap" id="sites">\n  <h2>{esc(st["title"])}</h2>\n'
            f'  <p class="muted sub">{esc(st["sub"])}</p>\n'
            f'  <h3 class="group">{esc(st["sites"])}</h3><div class="tools">{site_cards}</div>\n'
            f'  <h3 class="group">{esc(st["channels"])}</h3><div class="tools">{"".join(ch_cards)}</div>\n'
            f'</section>')


def page(lang):
    t = T[lang]
    nav = "".join(f'<a href="{h}">{esc(n)}</a>' for n, h in t["nav"])
    facts = "".join(f"<li><span>{esc(k)}</span><strong>{esc(v)}</strong></li>" for k, v in t["facts"])
    bio = "".join(f"<p>{p}</p>" for p in t["bio"])
    services = "".join(
        f'<article class="service"><h3>{esc(h)}</h3><p class="muted">{esc(p)}</p></article>'
        for h, p in t["services"]
    )
    return f"""{head(lang)}
<body>
<a class="skip" href="#main">{esc(t['skip'])}</a>

<header class="top">
  <div class="wrap bar">
    <a class="brand" href="#top">wangtaiyang<span>.com</span></a>
    <nav class="menu">{nav}</nav>
    {lang_switch(lang)}
  </div>
</header>

<main id="main">

<div class="meishi wrap">
  <picture>
    <source type="image/webp" srcset="/assets/img/meishi-1280.webp 1280w, /assets/img/meishi-2464.webp 2464w" sizes="(max-width: 1040px) 100vw, 1000px">
    <img src="/assets/img/meishi-1280.jpg" width="1280" height="774" alt="{esc(t['meishi_alt'])}" fetchpriority="high" decoding="async">
  </picture>
</div>

<section class="hero wrap" id="top">
  <p class="eyebrow">{esc(t['eyebrow'])}</p>
  <h1>{esc(t['h1'])} <span>{esc(t['h1_en'])}</span></h1>
  <p class="lead">{esc(t['lead'])}</p>
  <div class="cta">
    <a class="btn" href="#tools">{esc(t['btn_primary'])}</a>
    <a class="btn btn-ghost" href="#contact">{esc(t['btn_secondary'])}</a>
  </div>
</section>

<section class="block wrap" id="tools">
  <h2>{esc(t['tools_title'])}</h2>
  <p class="muted sub">{esc(t['tools_sub'])}</p>
  {tool_groups(lang)}
  <p class="all"><a href="{t['path']}tools/">{esc(t['own_link'])}</a></p>
</section>

{sites_section(lang)}

<section class="block wrap" id="news">
  <h2>{esc(t['news_title'])}</h2>
  <p class="muted sub">{esc(t['news_sub'])}</p>
  <ul class="post-list"><li class="empty">{esc(t['news_empty'])}</li></ul>
  <p class="all"><a href="#news">{esc(t['news_all'])}</a></p>
</section>

<section class="block wrap" id="about">
  <h2>{esc(t['about_title'])}</h2>
  <p class="muted sub">{esc(t['about_sub'])}</p>
  <div class="about">
    <div class="bio">{bio}</div>
    <ul class="facts">{facts}</ul>
  </div>
</section>

<section class="block wrap" id="services">
  <h2>{esc(t['services_title'])}</h2>
  <p class="muted sub">{esc(t['services_sub'])}</p>
  <div class="services">{services}</div>
</section>

<section class="block wrap contact" id="contact">
  <h2>{esc(t['contact_title'])}</h2>
  <p class="lead">{esc(t['contact_lead'])}</p>
  <p><span class="muted">{esc(t['contact_label'])}</span><br>
     <a class="mail" href="mailto:{EMAIL}">{EMAIL}</a></p>
</section>

</main>

<footer class="foot">
  <div class="wrap">
    <p class="muted">{esc(t['footer_blurb'])}</p>
    <div class="foot-row">
      <span class="muted">{esc(t['base_l'])}</span>
      <span class="muted">{esc(t['base_r'])}</span>
      <a href="#top">↑ {esc(t['back_top'])}</a>
    </div>
  </div>
</footer>
</body>
</html>
"""


CLEAN_CSS = """/* wangtaiyang.com - clean light theme */
:root {
  --bg: #ffffff;
  --soft: #f6f7f9;
  --text: #15171c;
  --muted: #5e6572;
  --line: #e7e9ee;
  --accent: #2563eb;
  --accent-soft: #eaf1ff;
  --radius: 14px;
  --max: 1040px;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; -webkit-text-size-adjust: 100%; }
body {
  margin: 0; background: var(--bg); color: var(--text);
  font: 16px/1.75 -apple-system, BlinkMacSystemFont, "Inter", "Helvetica Neue",
        "Noto Sans TC", "Noto Sans JP", "Noto Sans CJK TC", "PingFang TC", "Hiragino Sans",
        "Yu Gothic", "Microsoft JhengHei", sans-serif;
}
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
h1, h2, h3 { line-height: 1.3; margin: 0; font-weight: 700; letter-spacing: -.01em; }
p { margin: 0 0 12px; }
.muted { color: var(--muted); }
.wrap { max-width: var(--max); margin: 0 auto; padding: 0 20px; }
.skip { position: absolute; left: -999px; }
.skip:focus { left: 12px; top: 12px; background: #fff; padding: 8px 12px; z-index: 9; }

/* top bar */
.top { position: sticky; top: 0; z-index: 10; background: rgba(255,255,255,.92); backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--line); }
.bar { display: flex; align-items: center; gap: 20px; height: 60px; }
.brand { color: var(--text); font-weight: 700; font-size: 17px; }
.brand span { color: var(--muted); font-weight: 400; }
.menu { display: flex; gap: 18px; margin-left: auto; flex-wrap: wrap; }
.menu a { color: var(--muted); font-size: 14px; }
.menu a:hover { color: var(--text); text-decoration: none; }
/* language dropdown */
.lang-dd { position: relative; font-size: 13px; }
.lang-dd summary { list-style: none; display: inline-flex; align-items: center; gap: 6px; cursor: pointer;
  padding: 6px 10px; border: 1px solid var(--line); border-radius: 999px; color: var(--text); user-select: none; }
.lang-dd summary::-webkit-details-marker { display: none; }
.lang-dd summary:hover { border-color: var(--accent); }
.lang-dd .chev { transition: transform .15s; }
.lang-dd[open] .chev { transform: rotate(180deg); }
.lang-menu { position: absolute; right: 0; top: calc(100% + 6px); min-width: 132px; background: var(--bg);
  border: 1px solid var(--line); border-radius: 12px; box-shadow: 0 10px 30px rgba(15,23,42,.10); padding: 6px; z-index: 30; }
.lang-menu a { display: block; padding: 8px 12px; border-radius: 8px; color: var(--text); }
.lang-menu a:hover { background: var(--soft); text-decoration: none; }
.lang-menu a[aria-current="page"] { color: var(--accent); font-weight: 600; }

/* static cards (no link), e.g. WeChat Channels */
.tool-static { cursor: default; }
.tool-static:hover { border-color: var(--line); box-shadow: none; }
.tool .hint { font-size: 12px; color: var(--accent); margin-top: 4px; }

/* hero */
.hero { padding: 88px 20px 56px; }
.eyebrow { color: var(--accent); font-size: 14px; font-weight: 600; letter-spacing: .02em; margin-bottom: 14px; }
.hero h1 { font-size: clamp(36px, 6vw, 56px); }
.hero h1 span { color: var(--muted); font-weight: 500; }
.lead { color: var(--muted); font-size: 18px; max-width: 640px; margin-top: 18px; }
.cta { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 26px; }
.btn { display: inline-block; padding: 11px 20px; border-radius: 999px; background: var(--accent); color: #fff;
  font-weight: 600; font-size: 15px; }
.btn:hover { text-decoration: none; opacity: .92; }
.btn-ghost { background: transparent; color: var(--text); border: 1px solid var(--line); }

/* blocks */
.block { padding: 56px 20px; border-top: 1px solid var(--line); }
.block h2 { font-size: 28px; }
.sub { margin: 8px 0 28px; }
.group { font-size: 13px; color: var(--muted); font-weight: 600; letter-spacing: .06em; text-transform: uppercase;
  margin: 30px 0 12px; }
.tools { display: grid; gap: 12px; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); }
.tool { display: flex; flex-direction: column; gap: 4px; padding: 16px 18px; border: 1px solid var(--line);
  border-radius: var(--radius); color: var(--text); background: var(--bg); transition: border-color .15s, box-shadow .15s; }
.tool:hover { border-color: var(--accent); box-shadow: 0 6px 20px rgba(37,99,235,.08); text-decoration: none; }
.tool strong { font-size: 16px; }
.tool .muted { font-size: 14px; }
.tool-host { font-family: ui-monospace, Menlo, monospace; font-size: 12px; color: var(--accent); }

/* news list on homepage */
.post-list { list-style: none; margin: 0; padding: 0; border-top: 1px solid var(--line); }
.post-list li { display: flex; justify-content: space-between; gap: 16px; padding: 14px 0; border-bottom: 1px solid var(--line); }
.post-list li.empty { color: var(--muted); border-bottom: 0; }
.post-list a { color: var(--text); }
.post-list a:hover { color: var(--accent); }
.post-list time { color: var(--muted); font-size: 14px; white-space: nowrap; }
.all { margin-top: 18px; }

/* about */
.about { display: grid; gap: 36px; }
@media (min-width: 760px) { .about { grid-template-columns: 1.4fr 1fr; } }
.bio p { color: var(--text); }
.facts { list-style: none; margin: 0; padding: 0; border: 1px solid var(--line); border-radius: var(--radius); }
.facts li { display: flex; justify-content: space-between; gap: 12px; padding: 13px 18px; border-bottom: 1px solid var(--line); font-size: 15px; }
.facts li:last-child { border-bottom: 0; }
.facts span { color: var(--muted); }

/* services */
.services { display: grid; gap: 14px; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); }
.service { padding: 22px; border-radius: var(--radius); background: var(--soft); }
.service h3 { font-size: 17px; margin-bottom: 8px; }
.service p { font-size: 15px; margin: 0; }

/* contact */
.contact .lead { margin-bottom: 18px; }
.mail { font-size: 22px; font-weight: 600; }

/* footer */
.foot { border-top: 1px solid var(--line); padding: 36px 0 48px; font-size: 14px; }
.foot p { margin-bottom: 14px; }
.foot-row { display: flex; gap: 18px; flex-wrap: wrap; align-items: center; }
.foot-row a { margin-left: auto; }

@media (max-width: 640px) {
  .bar { height: auto; padding: 12px 20px; flex-wrap: wrap; gap: 10px; }
  .lang-dd { order: 2; margin-left: auto; }
  .menu { order: 3; width: 100%; margin-left: 0; gap: 14px; }
  .hero { padding: 56px 20px 40px; }
  .block { padding: 44px 20px; }
}

/* name card banner at the top of the homepage */
.meishi { padding-top: 24px; }
.meishi img { display: block; width: 100%; height: auto; border-radius: 18px; background: #000;
  box-shadow: 0 18px 50px rgba(15,23,42,.18); }
.meishi + .hero { padding-top: 48px; }
@media (max-width: 640px) { .meishi { padding-top: 14px; } .meishi img { border-radius: 12px; } .meishi + .hero { padding-top: 32px; } }

/* own-tool badge on homepage cards */
.tool { position: relative; }
.mine { position: absolute; top: 12px; right: 12px; font-size: 11px; font-weight: 600; color: var(--accent);
  background: var(--accent-soft); padding: 2px 8px; border-radius: 999px; }

/* ---- tool landing pages (scripts/build_tools.py) ---- */
.tp { padding-top: 28px; padding-bottom: 56px; max-width: 860px; }
.crumbs { display: flex; flex-wrap: wrap; gap: 8px; font-size: 13px; color: var(--muted); margin-bottom: 28px; }
.crumbs a { color: var(--muted); }
.tp-head { padding-bottom: 28px; border-bottom: 1px solid var(--line); margin-bottom: 8px; }
.tp-head h1 { font-size: clamp(30px, 5vw, 42px); margin-top: 8px; }
.tp-head .lead { margin-top: 14px; }
.tp-meta { font-size: 13px; margin-top: 16px; }
.tp-sec { padding: 28px 0 4px; }
.tp-sec h2 { font-size: 20px; margin-bottom: 14px; }
.tp-list, .tp-steps { margin: 0; padding-left: 22px; }
.tp-list li, .tp-steps li { margin-bottom: 8px; }
.faq details { border: 1px solid var(--line); border-radius: 10px; padding: 12px 16px; margin-bottom: 10px; }
.faq summary { cursor: pointer; font-weight: 600; }
.faq details p { margin: 10px 0 0; color: var(--muted); }
.tp-note { margin-top: 24px; padding: 14px 16px; background: var(--soft); border-radius: 10px; font-size: 14px; color: var(--muted); }
.tp .tools { margin-top: 4px; }

/* ---- daily news pages (used by scripts/build_news.py) ---- */
.news-wrap { max-width: 760px; margin: 0 auto; padding: 48px 20px 64px; }
.news-wrap .back { display: inline-block; font-size: 14px; color: var(--muted); margin-bottom: 28px; }
.news-head { margin-bottom: 32px; padding-bottom: 24px; border-bottom: 1px solid var(--line); }
.news-head .eyebrow { font-size: 13px; color: var(--accent); font-weight: 600; margin: 0 0 8px; }
.news-head h1 { font-size: clamp(32px, 6vw, 44px); }
.news-head .lead { font-size: 15px; margin-top: 12px; }
.cards { display: grid; gap: 14px; }
.news-wrap .card { display: grid; grid-template-columns: 44px 1fr; gap: 14px; padding: 20px; border: 1px solid var(--line);
  border-radius: var(--radius); background: var(--bg); }
.news-wrap .num { font-size: 13px; color: var(--accent); font-weight: 600; padding-top: 3px; }
.news-wrap .card h2 { font-size: 18px; margin-bottom: 8px; }
.news-wrap .card p { color: #2b3040; font-size: 15px; line-height: 1.8; margin-bottom: 12px; }
.chips { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
.chips .lbl { font-size: 12px; color: var(--muted); margin-right: 2px; }
.chip { font-size: 12px; padding: 3px 10px; border-radius: 999px; background: var(--accent-soft); color: var(--accent); }
.chip:hover { text-decoration: none; filter: brightness(.96); }
.news-wrap .disc { margin-top: 32px; font-size: 13px; color: var(--muted); border-top: 1px solid var(--line); padding-top: 16px; }
@media (max-width: 560px) { .news-wrap .card { grid-template-columns: 1fr; gap: 6px; } }
"""


def main():
    os.makedirs(os.path.join(SITE, "ja"), exist_ok=True)
    os.makedirs(os.path.join(SITE, "en"), exist_ok=True)
    with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as f:
        f.write(page("zh"))
    with open(os.path.join(SITE, "ja", "index.html"), "w", encoding="utf-8") as f:
        f.write(page("ja"))
    with open(os.path.join(SITE, "en", "index.html"), "w", encoding="utf-8") as f:
        f.write(page("en"))
    with open(os.path.join(SITE, "clean.css"), "w", encoding="utf-8") as f:
        f.write(CLEAN_CSS)
    print("ok")


if __name__ == "__main__":
    main()
