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
    t = re.sub(r'<link rel="alternate" type="application/rss\+xml"[^>]*>\n?', "", t)
    tags += '<link rel="alternate" type="application/rss+xml" title="ForeverWoW.fr – News" href="https://foreverwow.fr/rss.xml">\n'
    t = t.replace("</head>", tags + "</head>", 1)
    open(f, "w", encoding="utf-8").write(t)
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
sm += [f"  <url><loc>{BASE if f == 'index.html' else BASE + f}</loc><lastmod>{datetime.date.today()}</lastmod></url>" for f in pages]
open("sitemap.xml", "w").write("\n".join(sm + ["</urlset>"]) + "\n")
print(len(pages), "pages")

# ----- Flux RSS des news (à partir de js/news.js) -----
from email.utils import format_datetime
from xml.sax.saxutils import escape as x
src = open("js/news.js", encoding="utf-8").read()
items = []
for m in re.finditer(r'\{\s*date:\s*"([^"]+)",\s*type:\s*"([^"]+)",\s*lien:\s*"([^"]+)",\s*img:\s*"([^"]+)",\s*titre:\s*"((?:[^"\\]|\\.)*)",\s*texte:\s*"((?:[^"\\]|\\.)*)"\s*\}', src):
    d, typ, lien, img, titre, texte = m.groups()
    items.append((d, lien, img, titre.replace('\\"', '"'), texte.replace('\\"', '"'), typ))
items.sort(key=lambda i: i[0], reverse=True)
CAT = {"actu": "Actualité", "guide": "Guide", "site": "Nouveau sur le site"}
out = ['<?xml version="1.0" encoding="UTF-8"?>', '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">', "<channel>",
       "<title>ForeverWoW.fr – News</title>", f"<link>{BASE}</link>",
       "<description>Actualités, guides et nouveautés de ForeverWoW.fr, le site de fan français de World of Warcraft: Forever.</description>",
       "<language>fr-fr</language>", f'<atom:link href="{BASE}rss.xml" rel="self" type="application/rss+xml"/>',
       f"<image><url>{BASE}images/logo-carre.png</url><title>ForeverWoW.fr – News</title><link>{BASE}</link></image>"]
seen = {}
for i, (d, lien, img, titre, texte, typ) in enumerate(items[:40]):
    y, mo, j = map(int, d.split("-"))
    dt = datetime.datetime(y, mo, j, 12, 0, tzinfo=datetime.timezone.utc) - datetime.timedelta(minutes=i)
    url = BASE + lien
    guid = f"{url}#{d}-{re.sub(r'[^a-z0-9]+', '-', titre.lower())[:40]}"
    out.append(f"<item><title>{x(titre)}</title><link>{x(url)}</link><guid isPermaLink=\"false\">{x(guid)}</guid>"
               f"<pubDate>{format_datetime(dt)}</pubDate><category>{CAT.get(typ, typ)}</category>"
               f"<description>{x(texte)}</description><enclosure url=\"{x(BASE + img)}\" type=\"image/jpeg\" length=\"0\"/></item>")
out += ["</channel>", "</rss>"]
open("rss.xml", "w", encoding="utf-8").write("\n".join(out) + "\n")
print(len(items), "news dans le flux RSS (40 max)")
