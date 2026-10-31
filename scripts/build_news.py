#!/usr/bin/env python3
"""Render daily news digests (zh-Hant / ja / en) from news/items/*.json,
refresh the homepage lists and regenerate sitemap.xml.

Usage: python3 scripts/build_news.py
"""
import glob
import html
import json
import os
import re
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
ITEMS = os.path.join(ROOT, "news", "items")
BASE = "https://wangtaiyang.com"

L = {
    "zh": dict(hreflang="zh-Hant", news="news", label="每日經濟新聞", blurb="每日整理世界經濟與市場重點，附原始來源連結。",
               back="← 返回首頁", disclaimer="AI 輔助整理，僅供參考，不構成投資建議。", src="來源", og="zh_TW",
               index="index.html"),
    "ja": dict(hreflang="ja", news="ja/news", label="世界経済ニュース",
               blurb="世界経済と市場の重要ポイントを毎日まとめ、元の情報源へのリンクを付けています。",
               back="← トップへ戻る", disclaimer="AIによる整理です。参考情報であり、投資助言ではありません。",
               src="出典", og="ja_JP", index="ja/index.html"),
    "en": dict(hreflang="en", news="en/news", label="World Economy News",
               blurb="A daily digest of world economy and market highlights, with links to original sources.",
               back="← Back to home", disclaimer="AI-assisted summary for reference only. Not investment advice.",
               src="Sources", og="en_US", index="en/index.html"),
}
LANGS = ["zh", "ja", "en"]


def esc(s):
    return html.escape(str(s), quote=True)


def path_for(lang, date):
    return f"{L[lang]['news']}/{date}.html"


def validate(d):
    datetime.strptime(d["date"], "%Y-%m-%d")
    assert d["items"], f"{d['date']}: no items"
    for it in d["items"]:
        for lang in LANGS:
            assert it[lang]["title"] and it[lang]["summary"], f"{d['date']}: empty {lang} text"
        for s in it.get("sources", []):
            assert s["url"].startswith("https://"), f"{d['date']}: source must be https: {s['url']}"


def load_digests():
    out = []
    for path in sorted(glob.glob(os.path.join(ITEMS, "*.json")), reverse=True):
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        validate(d)
        out.append(d)
    return out


def render_digest(lang, d):
    c = L[lang]
    date = d["date"]
    blocks = []
    for it in d["items"]:
        t = it[lang]
        srcs = " · ".join(
            f'<a href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(s["name"])}</a>'
            for s in it.get("sources", [])
        )
        blocks.append(
            f'<article><h2>{esc(t["title"])}</h2><p>{esc(t["summary"])}</p>'
            f'<p class="src"><span>{esc(c["src"])}：</span>{srcs}</p></article>'
        )
    title = f'{c["label"]} · {date}'
    url = f"{BASE}/{path_for(lang, date)}"
    return f"""<!doctype html>
<html lang="{c['hreflang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} | wangtaiyang.com</title>
<meta name="description" content="{esc(c['blurb'])}">
<meta name="robots" content="index,follow">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(title)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="{c['og']}">
<link rel="stylesheet" href="/styles.css">
<link rel="stylesheet" href="/extras.css">
</head>
<body>
<div class="bg-base"></div>
<div class="bg-grid-wrap"><div class="bg-grid"></div></div>
<div class="bg-vignette"></div>
<main class="news-wrap">
<a class="back" href="/{c['index'] if c['index'] != 'index.html' else ''}">{esc(c['back'])}</a>
<h1>{esc(title)}</h1>
<p class="meta"><time datetime="{date}">{date}</time></p>
{''.join(blocks)}
<p class="disc">{esc(c['disclaimer'])}</p>
</main>
</body>
</html>
"""


def post_list_html(lang, digests):
    lis = []
    for d in digests[:7]:
        first = d["items"][0][lang]["title"]
        lis.append(
            f'<li><a href="/{path_for(lang, d["date"])}">{esc(d["date"])} · {esc(first)}</a>'
            f'<time datetime="{d["date"]}">{d["date"]}</time></li>'
        )
    return '<ul class="post-list">' + "".join(lis) + "</ul>"


def sitemap(digests):
    alt = "".join(
        f'<xhtml:link rel="alternate" hreflang="{L[k]["hreflang"]}" href="{BASE}/{L[k]["index"].replace("index.html", "")}"/>'
        for k in LANGS
    )
    urls = []
    for k in LANGS:
        loc = f"{BASE}/{L[k]['index'].replace('index.html', '')}"
        urls.append(f"<url><loc>{loc}</loc><changefreq>daily</changefreq><priority>1.0</priority>{alt}</url>")
    for d in digests:
        for k in LANGS:
            urls.append(f"<url><loc>{BASE}/{path_for(k, d['date'])}</loc><lastmod>{d['date']}</lastmod></url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n  ' + "\n  ".join(urls) + "\n</urlset>\n")


def main():
    digests = load_digests()
    for d in digests:
        for lang in LANGS:
            p = os.path.join(SITE, path_for(lang, d["date"]))
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(render_digest(lang, d))
    if digests:
        for lang in LANGS:
            p = os.path.join(SITE, L[lang]["index"])
            with open(p, encoding="utf-8") as f:
                s = f.read()
            s2 = re.sub(r'<ul class="post-list">.*?</ul>', lambda m: post_list_html(lang, digests),
                        s, count=1, flags=re.S)
            with open(p, "w", encoding="utf-8") as f:
                f.write(s2)
    with open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap(digests))
    print(f"built {len(digests)} digest(s) x {len(LANGS)} languages")


if __name__ == "__main__":
    main()
