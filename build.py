"""Builds the Plico privacy policy pages (in plico/) from the PRIVACY*.md files of the app: python3 build.py"""
import html
import pathlib
import re

import markdown

SRC = pathlib.Path.home() / "Projects/DocScanner"
OUT = pathlib.Path(__file__).parent / "plico"
EMAIL = "paduainformatics@gmail.com"
LANGS = [("en", "PRIVACY.en.md", "English"), ("it", "PRIVACY.md", "Italiano"), ("de", "PRIVACY.de.md", "Deutsch"),
         ("fr", "PRIVACY.fr.md", "Français"), ("es", "PRIVACY.es.md", "Español"), ("pt", "PRIVACY.pt.md", "Português"),
         ("ru", "PRIVACY.ru.md", "Русский")]

CSS = """
:root{--bg:#f7f8f8;--fg:#1b2125;--muted:#5b676e;--accent:#0f8a6d;--line:#dfe4e6;--card:#fff}
@media (prefers-color-scheme:dark){:root{--bg:#14181b;--fg:#eceff1;--muted:#9aa5ab;--accent:#2fd3a8;--line:#2a3237;--card:#1b2024}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
header{border-bottom:1px solid var(--line);background:var(--card)}
.bar{max-width:760px;margin:0 auto;padding:14px 16px;display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.logo{width:36px;height:36px;border-radius:9px;background:#0f8a6d;display:grid;place-items:center}
.brand{font-weight:700;font-size:20px;margin-right:auto}
nav{display:flex;flex-wrap:wrap;gap:4px 14px}
nav a{color:var(--muted);text-decoration:none;font-size:14px;white-space:nowrap}
nav a[aria-current]{color:var(--accent);font-weight:600}
main{max-width:760px;margin:0 auto;padding:24px 16px 64px}
h1{font-size:28px;line-height:1.25;margin:8px 0 4px}
h2{font-size:19px;margin:32px 0 8px}
a{color:var(--accent);overflow-wrap:anywhere}
main>p:first-of-type{color:var(--muted)}
footer{max-width:760px;margin:0 auto;padding:0 16px 32px;color:var(--muted);font-size:13px}
"""
LOGO = ('<svg width="20" height="22" viewBox="0 0 20 22"><path d="M2 1h11l5 5v15H2z" fill="#fff"/>'
        '<path d="M13 1v5h5" fill="#c5e8de"/><path d="M5 10h10M5 13.5h10M5 17h6" stroke="#0f8a6d" stroke-width="2"/></svg>')
# The English index sends first-time visitors to their browser's language, once per session.
REDIRECT = ("<script>try{var m={it:1,de:1,fr:1,es:1,pt:1,ru:1},l=(navigator.language||'').slice(0,2);"
            "if(!location.search&&!sessionStorage.getItem('s')&&m[l]){sessionStorage.setItem('s',1);"
            "location.replace(l+'.html')}}catch(e){}</script>")
MAIL = f'<a href="mailto:{EMAIL}">{EMAIL}</a>'

for code, name, _ in LANGS:
    body = markdown.markdown((SRC / name).read_text(encoding="utf-8"), extensions=["nl2br"])
    body = re.sub(r'(?<![">])(https://[^\s<]+)', r'<a href="\1">\1</a>', body).replace(EMAIL, MAIL)
    title = re.search(r"<h1>(.*?)</h1>", body).group(1)
    nav = "".join(f'<a href="{"./" if c == "en" else c + ".html"}" hreflang="{c}"'
                  f'{" aria-current=page" if c == code else ""}>{label}</a>' for c, _, label in LANGS)
    page = f"""<!doctype html>
<html lang="{code}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="color-scheme" content="light dark"><style>{CSS}</style>{REDIRECT if code == "en" else ""}</head>
<body><header><div class="bar"><div class="logo">{LOGO}</div><div class="brand">Plico</div><nav>{nav}</nav></div></header>
<main>{body}</main><footer>Padua Informatics · {MAIL}</footer></body></html>
"""
    (OUT / ("index.html" if code == "en" else code + ".html")).write_text(page, encoding="utf-8")
