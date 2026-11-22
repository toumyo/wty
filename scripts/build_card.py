#!/usr/bin/env python3
"""Digital business card at /card/ for sharing (WeChat, LINE, email).

Writes:
  site/card/index.html                 mobile-first card page
  site/card/taiyang-wang.vcf           contact file ("save to contacts")
  site/assets/img/card-share.png       600x600 thumbnail for link previews
  site/assets/img/card-poster.png      card + QR code, to send as an image in WeChat

Run:  python3 scripts/build_card.py
"""
import html
import io
import os
import sys

import qrcode
import qrcode.image.svg
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_site import ADSENSE  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
IMG = os.path.join(SITE, "assets", "img")
CARD_URL = "https://wangtaiyang.com/card/"

# Details exactly as printed on the card (and on toumyou.com).
NAME = "王太陽"
NAME_EN = "Taiyang Wang"
COMPANY = "東緲合同会社"
COMPANY_EN = "Toubyou Godo Kaisha"
TEL = "070-1846-1357"
TEL_INTL = "+81-70-1846-1357"
MAIL = "hello@toumyou.com"
WEB = "https://toumyou.com/"
SITE_URL = "https://wangtaiyang.com/"
POSTCODE = "558-0022"
ADDRESS = "大阪府大阪市住吉区杉本2-1-35"
SERVICES_JA = "ウェブサイト制作 ・ ミニプログラム開発 ・ ソフトウェア開発 ・ システム運用保守 ・ 動画編集"
SERVICES_ZH = "网站制作 · 小程序开发 · 软件开发 · 系统运维 · 视频剪辑"

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"


def esc(s):
    return html.escape(s, quote=True)


def qr_svg(data):
    img = qrcode.make(data, image_factory=qrcode.image.svg.SvgPathImage, box_size=10, border=2)
    buf = io.BytesIO()
    img.save(buf)
    svg = buf.getvalue().decode("utf-8")
    return svg[svg.index("<svg"):]


def vcard():
    lines = [
        "BEGIN:VCARD", "VERSION:3.0",
        f"N;CHARSET=UTF-8:王;太陽;;;",
        f"FN;CHARSET=UTF-8:{NAME}",
        f"ORG;CHARSET=UTF-8:{COMPANY}",
        f"TEL;TYPE=CELL,VOICE:{TEL_INTL}",
        f"EMAIL;TYPE=INTERNET,WORK:{MAIL}",
        f"URL;TYPE=WORK:{WEB}",
        f"URL:{SITE_URL}",
        f"ADR;TYPE=WORK;CHARSET=UTF-8:;;杉本2-1-35;大阪市住吉区;大阪府;{POSTCODE};日本",
        f"NOTE;CHARSET=UTF-8:{SERVICES_JA}",
        "END:VCARD",
    ]
    return "\r\n".join(lines) + "\r\n"


def make_images():
    card = Image.open(os.path.join(IMG, "meishi-2464.webp")).convert("RGB")

    # 600x600 thumbnail: the card centred on black, for link previews
    thumb = Image.new("RGB", (600, 600), "black")
    w = 600
    h = round(card.height * w / card.width)
    thumb.paste(card.resize((w, h), Image.LANCZOS), (0, (600 - h) // 2))
    thumb.save(os.path.join(IMG, "card-share.png"), optimize=True)

    # poster for WeChat: card on top, QR code panel below
    W = 1080
    ch = round(card.height * W / card.width)
    panel = 420
    poster = Image.new("RGB", (W, ch + panel), (12, 12, 14))
    poster.paste(card.resize((W, ch), Image.LANCZOS), (0, 0))
    qr = qrcode.QRCode(box_size=9, border=2)
    qr.add_data(CARD_URL)
    qr.make(fit=True)
    q = qr.make_image(fill_color="black", back_color="white").convert("RGB").resize((300, 300), Image.NEAREST)
    qx, qy = W - 64 - 300, ch + 60
    poster.paste(q, (qx, qy))
    d = ImageDraw.Draw(poster)
    big = ImageFont.truetype(FONT_BOLD, 46)
    mid = ImageFont.truetype(FONT, 30)
    small = ImageFont.truetype(FONT, 26)
    x = 64
    d.text((x, ch + 70), f"{NAME}  {NAME_EN}", font=big, fill="white")
    d.text((x, ch + 140), f"{COMPANY} · {COMPANY_EN}", font=mid, fill=(200, 200, 205))
    d.text((x, ch + 200), "长按识别二维码", font=mid, fill="white")
    d.text((x, ch + 246), "查看名片 · 一键保存联系人", font=small, fill=(170, 170, 178))
    d.text((x, ch + 300), "wangtaiyang.com/card", font=small, fill=(120, 170, 255))
    poster.save(os.path.join(IMG, "card-poster.png"), optimize=True)


PAGE = """<!doctype html>
<html lang="zh-Hans">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{name} · {company}｜名片</title>
<meta name="description" content="{name}（{name_en}）的名片：{company}（{company_en}），大阪。{services_zh}。电话、邮件、一键保存联系人。">
<link rel="canonical" href="{card_url}">
<meta name="theme-color" content="#000000">
<meta property="og:type" content="profile">
<meta property="og:title" content="{name} · {company}｜名片">
<meta property="og:description" content="{services_zh}。点开查看名片，一键保存联系人。">
<meta property="og:url" content="{card_url}">
<meta property="og:image" content="https://wangtaiyang.com/assets/img/card-share.png">
<meta property="og:image:width" content="600">
<meta property="og:image:height" content="600">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://wangtaiyang.com/assets/img/card-share.png">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"ProfilePage","url":"{card_url}","mainEntity":{{"@type":"Person","@id":"https://wangtaiyang.com/#person","name":"{name}","alternateName":"{name_en}","telephone":"{tel_intl}","email":"mailto:{mail}","url":"https://wangtaiyang.com/","worksFor":{{"@type":"Organization","name":"{company}","alternateName":"{company_en}","url":"{web}","address":{{"@type":"PostalAddress","postalCode":"{postcode}","addressRegion":"大阪府","addressLocality":"大阪市住吉区","streetAddress":"杉本2-1-35","addressCountry":"JP"}}}}}}}}
</script>
<style>
  :root {{ --bg:#000; --panel:#111214; --line:#25272c; --text:#f3f4f6; --muted:#a1a6b0; --accent:#7fb2ff; }}
  * {{ box-sizing:border-box; }}
  img, svg {{ max-width:100%; height:auto; }}
  html, body {{ margin:0; background:var(--bg); color:var(--text); }}
  body {{ font:16px/1.6 -apple-system,BlinkMacSystemFont,"PingFang SC","Hiragino Sans","Noto Sans CJK SC","Microsoft YaHei",sans-serif;
         padding: env(safe-area-inset-top) 0 env(safe-area-inset-bottom); }}
  .share-thumb {{ position:absolute; left:-9999px; top:0; width:300px; height:300px; }}
  .wrap {{ max-width:560px; margin:0 auto; padding:16px 16px 40px; }}
  .card img {{ display:block; width:100%; border-radius:14px; box-shadow:0 20px 60px rgba(255,255,255,.06); }}
  .who {{ text-align:center; margin:22px 0 18px; }}
  .who h1 {{ margin:0; font-size:28px; letter-spacing:.04em; }}
  .who h1 span {{ color:var(--muted); font-weight:400; font-size:18px; margin-left:8px; letter-spacing:0; }}
  .who p {{ margin:6px 0 0; color:var(--muted); font-size:14px; }}
  .actions {{ display:grid; grid-template-columns:1fr 1fr; gap:10px; }}
  .btn {{ display:flex; align-items:center; justify-content:center; gap:8px; min-height:52px; padding:10px 12px;
         border-radius:12px; background:var(--panel); border:1px solid var(--line); color:var(--text);
         text-decoration:none; font-size:15px; font-weight:600; cursor:pointer; font-family:inherit; }}
  .btn small {{ display:block; font-weight:400; color:var(--muted); font-size:11px; }}
  .btn.primary {{ background:#fff; color:#000; border-color:#fff; grid-column:1 / -1; }}
  .btn.primary small {{ color:#555; }}
  .btn:active {{ transform:scale(.98); }}
  .info {{ margin-top:22px; background:var(--panel); border:1px solid var(--line); border-radius:14px; }}
  .info div {{ display:flex; gap:12px; padding:13px 16px; border-bottom:1px solid var(--line); font-size:14px; }}
  .info div:last-child {{ border-bottom:0; }}
  .info span {{ flex:0 0 52px; color:var(--muted); }}
  .info a {{ color:var(--text); word-break:break-all; }}
  .qr {{ margin-top:22px; display:flex; gap:16px; align-items:center; background:var(--panel);
         border:1px solid var(--line); border-radius:14px; padding:16px; }}
  .qr .code {{ flex:0 0 120px; background:#fff; border-radius:8px; padding:6px; }}
  .qr p {{ margin:0; font-size:14px; color:var(--muted); }}
  .qr strong {{ color:var(--text); display:block; margin-bottom:4px; }}
  .tip {{ display:none; margin-top:14px; padding:12px 14px; border-radius:12px; background:#17233a; color:#cfe0ff; font-size:13px; }}
  .wx .tip {{ display:block; }}
  .toast {{ position:fixed; left:50%; bottom:28px; transform:translateX(-50%); background:#fff; color:#000; padding:10px 16px;
           border-radius:999px; font-size:14px; opacity:0; transition:opacity .2s; pointer-events:none; }}
  .toast.on {{ opacity:1; }}
  footer {{ text-align:center; margin-top:26px; font-size:12px; color:#6b7079; }}
  footer a {{ color:#8b919c; }}
  @media (min-width:900px) {{ .wrap {{ max-width:620px; padding-top:40px; }} }}
</style>
{adsense}</head>
<body>
<img class="share-thumb" src="/assets/img/card-share.png" width="300" height="300" alt="">
<main class="wrap">
  <div class="card">
    <picture>
      <source type="image/webp" srcset="/assets/img/meishi-1280.webp 1280w, /assets/img/meishi-2464.webp 2464w" sizes="(max-width: 620px) 100vw, 620px">
      <img src="/assets/img/meishi-1280.jpg" width="1280" height="774" alt="{name}的名片：{company}（{company_en}），大阪。{services_zh}" fetchpriority="high">
    </picture>
  </div>

  <div class="who">
    <h1>{name}<span>{name_en}</span></h1>
    <p>{company} · {company_en}</p>
  </div>

  <div class="actions">
    <a class="btn primary" href="/card/taiyang-wang.vcf" download="Taiyang-Wang.vcf">保存到通讯录 <small>連絡先に保存</small></a>
    <a class="btn" href="tel:{tel_intl}">打电话 <small>電話</small></a>
    <a class="btn" href="mailto:{mail}">发邮件 <small>メール</small></a>
    <a class="btn" href="{web}">公司官网 <small>toumyou.com</small></a>
    <button class="btn" type="button" id="copy">复制名片链接 <small>リンクをコピー</small></button>
  </div>

  <p class="tip">在微信里打开时：点右上角「···」→「发送给朋友」即可转发这张名片。保存联系人请先选「在浏览器打开」。</p>

  <section class="info" aria-label="联系方式">
    <div><span>电话</span><a href="tel:{tel_intl}">{tel}</a></div>
    <div><span>邮箱</span><a href="mailto:{mail}">{mail}</a></div>
    <div><span>官网</span><a href="{web}">toumyou.com</a></div>
    <div><span>个人</span><a href="{site_url}">wangtaiyang.com</a></div>
    <div><span>地址</span><a href="https://www.google.com/maps/search/?api=1&amp;query={address_q}">〒{postcode} {address}</a></div>
    <div><span>业务</span><span style="flex:1;color:var(--text)">{services_zh}</span></div>
  </section>

  <section class="qr" aria-label="二维码">
    <div class="code">{qr}</div>
    <p><strong>扫码查看这张名片</strong>用手机扫一扫，或长按保存二维码发给朋友。</p>
  </section>

  <footer>
    <a href="/assets/img/card-poster.png" download="Taiyang-Wang-card.png">下载名片海报（含二维码）</a> · <a href="/">wangtaiyang.com</a>
  </footer>
</main>
<div class="toast" id="toast">已复制链接</div>
<script>
(function () {{
  if (/MicroMessenger/i.test(navigator.userAgent)) document.documentElement.classList.add('wx');
  var url = '{card_url}', toast = document.getElementById('toast');
  function show(t) {{ toast.textContent = t; toast.classList.add('on'); setTimeout(function () {{ toast.classList.remove('on'); }}, 1600); }}
  document.getElementById('copy').addEventListener('click', function () {{
    if (navigator.share && !/MicroMessenger/i.test(navigator.userAgent)) {{
      navigator.share({{ title: document.title, url: url }}).catch(function () {{}});
      return;
    }}
    var done = function () {{ show('已复制链接'); }};
    if (navigator.clipboard) navigator.clipboard.writeText(url).then(done, function () {{ prompt('复制链接', url); }});
    else prompt('复制链接', url);
  }});
}})();
</script>
</body>
</html>
"""


def main():
    os.makedirs(os.path.join(SITE, "card"), exist_ok=True)
    make_images()
    with open(os.path.join(SITE, "card", "taiyang-wang.vcf"), "w", encoding="utf-8", newline="") as f:
        f.write(vcard())
    from urllib.parse import quote
    page = PAGE.format(
        name=esc(NAME), name_en=esc(NAME_EN), company=esc(COMPANY), company_en=esc(COMPANY_EN),
        tel=esc(TEL), tel_intl=esc(TEL_INTL), mail=esc(MAIL), web=esc(WEB), site_url=esc(SITE_URL),
        postcode=esc(POSTCODE), address=esc(ADDRESS), address_q=quote(f"〒{POSTCODE} {ADDRESS}"),
        services_zh=esc(SERVICES_ZH), card_url=CARD_URL, qr=qr_svg(CARD_URL), adsense=ADSENSE,
    )
    with open(os.path.join(SITE, "card", "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
    print("built /card/")


if __name__ == "__main__":
    main()
