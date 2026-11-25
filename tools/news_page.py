"""Crée une page de news à partir du modèle news-patch-71091.html.
Usage (en Python) : from news_page import page ; page(fichier, titre, description, fil, h1, date_texte, chapo, image, alt, corps_html)"""
import re, html, os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")
TPL = "news-patch-71091.html"
def page(f, title, desc, crumb, h1, date, lead, img, alt, body):
    s = open(TPL, encoding="utf-8").read()
    ot = re.search(r"<title>(.*?) – ForeverWoW</title>", s).group(1)
    od = re.search(r'name="description" content="([^"]*)"', s).group(1)
    for a, b in [(ot, html.escape(title, quote=False)), (od, html.escape(desc))]:
        s = s.replace(a, b)
    s = s.replace(TPL, f)
    s = re.sub(r'(<div class="crumbs"><a href="index.html">News</a> › )[^<]*', lambda m: m.group(1) + crumb, s)
    s = re.sub(r'(<h1 class="page-title">)[^<]*', lambda m: m.group(1) + h1, s)
    s = re.sub(r'(<span class="date" style="margin:0">)[^<]*', lambda m: m.group(1) + date, s)
    s = re.sub(r'(<p class="page-lead">)[^<]*', lambda m: m.group(1) + lead, s)
    s = re.sub(r'<div class="cover"><img src="[^"]*" alt="[^"]*">', f'<div class="cover"><img src="{img}" alt="{alt}">', s)
    a = s.index('<div class="article">') + len('<div class="article">')
    b = s.index('\n    </div>\n  </div>\n  <aside data-sidebar>')
    s = s[:a] + "\n" + body + s[b:]
    open(f, "w", encoding="utf-8").write(s)
    print("ok", f)
