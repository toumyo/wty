# 部署说明（Cloudflare Pages）

目录结构：

- `index.html` / `ja/` / `en/` → 主站 wangtaiyang.com（三语）
- `n/` → 私人导航 n.wangtaiyang.com（建议单独的 Pages 项目）
- `sitemap.xml`、`robots.txt` → 放在主站根目录
- `styles.css`、`extras.css`、`main.js`、`assets/fonts/` → 主站静态资源

## 方法一：Dashboard 直接上传（最简单）

1. Cloudflare Dashboard → Workers & Pages → Create → Pages → Upload assets。
2. 项目名填 `wangtaiyang`，上传整个 `site/` 文件夹，**但先删除 `n/` 文件夹**（私人页单独部署）。
3. 部署完成后，进入项目 → Custom domains → 添加 `wangtaiyang.com`。
4. 私人导航：再新建一个 Pages 项目（例如 `wangtaiyang-nav`），只上传 `n/` 文件夹，然后绑定 `n.wangtaiyang.com`。
5. 在 Cloudflare Access 里为 `n.wangtaiyang.com` 添加访问策略（只允许你的邮箱登录）。

## 方法二：Wrangler 命令行

```sh
npm i -g wrangler
wrangler login

# 主站（不含 n/）
mkdir -p /tmp/site-main && rsync -a --exclude 'n/' site/ /tmp/site-main/
wrangler pages deploy /tmp/site-main --project-name wangtaiyang

# 私人导航
wrangler pages deploy site/n --project-name wangtaiyang-nav
```

## 部署后检查

- https://wangtaiyang.com/ 、/ja/ 、/en/ 能打开，语言切换正常
- https://wangtaiyang.com/sitemap.xml 、/robots.txt 可访问
- https://n.wangtaiyang.com/ 需要通过 Access 登录
- 在 Google Search Console、Bing 站长工具、百度搜索资源平台 提交 sitemap
- 上线前把页面里的"電郵待填"替换成真实邮箱（搜索 `CONTACT_TODO` 之前已经渲染为文字，直接改 `index.html`、`ja/index.html`、`en/index.html` 三处）
