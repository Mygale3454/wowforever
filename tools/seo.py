"""Remet à jour, sur chaque page, l'adresse officielle (canonical), les balises de partage et le sitemap.
À lancer après toute génération de pages : python3 tools/seo.py"""
import glob, html, os, re, datetime
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")
BASE = "https://foreverwow.fr/"
pages = sorted(f for f in glob.glob("*.html") if f != "actualites.html")
for f in pages:
    t = open(f, encoding="utf-8").read()
    t = re.sub(r'<link rel="canonical"[^>]*>\n?|<meta property="og:[^>]*>\n?|<meta name="twitter:card"[^>]*>\n?', "", t)
    title = html.unescape(re.search(r"<title>(.*?)</title>", t, re.S).group(1)).strip()
    m = re.search(r'<meta name="description" content="(.*?)"', t)
    desc = html.unescape(m.group(1)) if m else "Guides, actualités et outils en français pour World of Warcraft: Forever."
    url = BASE if f == "index.html" else BASE + f
    e = lambda s: html.escape(s, quote=True)
    tags = (f'<link rel="canonical" href="{url}">\n<meta property="og:type" content="website">\n<meta property="og:site_name" content="ForeverWoW.fr">\n'
            f'<meta property="og:locale" content="fr_FR">\n<meta property="og:title" content="{e(title)}">\n<meta property="og:description" content="{e(desc)}">\n'
            f'<meta property="og:url" content="{url}">\n<meta property="og:image" content="https://foreverwow.fr/images/partage.jpg">\n<meta name="twitter:card" content="summary_large_image">\n')
    t = t.replace("</head>", tags + "</head>", 1)
    open(f, "w", encoding="utf-8").write(t)
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
sm += [f"  <url><loc>{BASE if f == 'index.html' else BASE + f}</loc><lastmod>{datetime.date.today()}</lastmod></url>" for f in pages]
open("sitemap.xml", "w").write("\n".join(sm + ["</urlset>"]) + "\n")
print(len(pages), "pages")
