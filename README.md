# wangtaiyang.com

- `site/`：静态站点（繁体 / 日文 / 英文）。`site/n/` 是私人导航页，单独部署到 n.wangtaiyang.com。
- `news/items/YYYY-MM-DD.json`：每日新闻数据（每天一个文件，三语，附来源）。
- `news/examples/`：格式示例，不会被发布。
- `scripts/build_news.py`：把 items 渲染成页面，并刷新首页列表和 sitemap。

## 本地预览

```sh
python3 scripts/build_news.py
cd site && python3 -m http.server 8000
```

## 发布

推送到 `main` 分支后，GitHub Actions 自动部署到 Cloudflare Pages。需要在仓库 Secrets 中设置：

- `CLOUDFLARE_API_TOKEN`（只授予 Pages 编辑权限）
- `CLOUDFLARE_ACCOUNT_ID`
