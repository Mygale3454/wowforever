"""Remet à jour, sur chaque page, l'adresse officielle (canonical), les balises de partage et le sitemap.
À lancer après toute génération de pages : python3 tools/seo.py"""
import glob, html, json, os, re, datetime, subprocess
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")
BASE = "https://foreverwow.fr/"
pages = sorted(f for f in glob.glob("*.html") if f != "actualites.html" and 'http-equiv="refresh"' not in open(f, encoding="utf-8").read())
NEWSDATE = dict((l, d) for d, l in re.findall(r'date:\s*"([^"]+)",\s*type:\s*"[^"]+",\s*lien:\s*"([^"]+)"', open("js/news.js", encoding="utf-8").read()))
ORG = {"@type": "Organization", "name": "ForeverWoW.fr", "url": BASE, "logo": {"@type": "ImageObject", "url": BASE + "images/logo-carre.png"}}
def gitdate(f):
    try: return subprocess.run(["git", "log", "-1", "--format=%cs", "--", f], capture_output=True, text=True).stdout.strip() or str(datetime.date.today())
    except Exception: return str(datetime.date.today())
LASTMOD = {f: gitdate(f) for f in pages}

# ----- Tampon « Mise à jour le … · Patch … » sous l'introduction de chaque page -----
# Date = dernier commit qui a vraiment changé le contenu de la page (on ignore les numéros de version ?v=,
# les balises ajoutées par ce script et le tampon lui-même). Patch = build du jeu en vigueur à cette date.
PATCHES = [("2026-10-01", "1.60.1.70124"), ("2026-10-14", "1.60.1.70291"), ("2026-11-01", "1.60.1.70707"), ("2026-11-02", "1.60.1.70753"), ("2026-11-04", "1.60.1.70755"), ("2026-11-07", "1.60.1.70862"), ("2026-11-11", "1.60.1.70888"), ("2026-11-13", "1.60.1.70938")]
NOSTAMP = {"index.html", "galerie.html", "actualites.html", "a-propos.html", "mentions-legales.html", "confidentialite.html", "contact.html"}
def _norm(l):
    l = re.sub(r'<p class="stamp auto">.*?</p>', "", l)
    if re.search(r'<link rel="canonical"|<meta property="og:|<meta name="twitter:|application/ld\+json|<meta name="robots"|application/rss\+xml', l): return ""
    return re.sub(r"\?v=\d+", "", l).strip()
def _real(diff):
    import collections
    add, rem = collections.Counter(), collections.Counter()
    for l in diff.splitlines():
        if l.startswith(("+++", "---")) or l[:1] not in "+-": continue
        n = _norm(l[1:])
        if n: (add if l[0] == "+" else rem)[n] += 1
    return add != rem
def contentdate(f):
    try:
        if _real(subprocess.run(["git", "diff", "HEAD", "--", f], capture_output=True, text=True).stdout): return str(datetime.date.today())
        log = subprocess.run(["git", "log", "-p", "--format=@@COMMIT %cs", "--", f], capture_output=True, text=True).stdout
        for chunk in log.split("@@COMMIT ")[1:]:
            d, _, diff = chunk.partition("\n")
            if _real(diff): return d.strip()
    except Exception: pass
    return str(datetime.date.today())
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
def stamp(d):
    patch = "1.60.1 (bêta)"
    for pd, p in PATCHES:
        if d >= pd: patch = p
    a, m, j = d.split("-")
    return (f'<p class="stamp auto"><span>📅 Mise à jour le <b>{int(j)}{"er" if j == "01" else ""} {MOIS[int(m)-1]} {a}</b></span>'
            f'<span>🛠 Patch <b>{patch}</b></span></p>')
for f in pages:
    if f in NOSTAMP or f.startswith("news-"): continue
    t = open(f, encoding="utf-8").read()
    t2 = re.sub(r'\n?<p class="stamp auto">.*?</p>', "", t)
    m = re.search(r'<p class="page-lead">.*?</p>', t2, re.S)
    if not m or t2[m.end():m.end() + 40].lstrip().startswith('<p class="stamp'): continue
    t2 = t2[:m.end()] + "\n" + stamp(contentdate(f)) + t2[m.end():]
    if t2 != t: open(f, "w", encoding="utf-8").write(t2)
NOART = {"index.html", "talents.html", "pseudo.html", "galerie.html", "a-propos.html", "mentions-legales.html", "confidentialite.html", "contact.html"}
def ld(f, t, title, desc, url):
    name = re.sub(r"\s+–\s+ForeverWoW(\.fr)?$", "", title)
    if f == "index.html":
        return [{"@context": "https://schema.org", "@type": "WebSite", "name": "ForeverWoW.fr", "alternateName": "ForeverWoW", "url": BASE, "inLanguage": "fr-FR", "description": desc, "publisher": ORG},
                dict({"@context": "https://schema.org"}, **ORG)]
    out = []
    m = re.search(r'<div class="crumbs">(.*?)</div>', t, re.S)
    if m:
        parts = [p.strip() for p in m.group(1).split("›")]
        items = []
        for i, p in enumerate(parts, 1):
            a = re.search(r'href="([^"]+)"', p); nm = html.unescape(re.sub(r"<[^>]+>", "", p)).strip()
            if not nm: continue
            it = {"@type": "ListItem", "position": len(items) + 1, "name": "Accueil" if nm == "News" else nm}
            href = a.group(1) if a else (f if i == len(parts) else None)
            if not href: continue
            if href: it["item"] = BASE if href == "index.html" else BASE + href.split("#")[0]
            items.append(it)
        if items: out.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items})
    if f not in NOART:
        im = re.search(r'<div class="cover"><img src="([^"]+)"', t)
        d0 = NEWSDATE.get(f)
        out.append({"@context": "https://schema.org", "@type": "NewsArticle" if f.startswith(("news-", "article-")) else "Article",
                    "headline": name[:110], "description": desc, "inLanguage": "fr-FR", "mainEntityOfPage": url,
                    "image": [(lambda u: u if u.startswith("http") else BASE + u)(im.group(1) if im else "images/partage.jpg")],
                    "datePublished": d0 or LASTMOD[f], "dateModified": LASTMOD[f], "author": ORG, "publisher": ORG})
    else:
        out.append({"@context": "https://schema.org", "@type": "WebApplication" if f in ("talents.html", "pseudo.html") else "WebPage",
                    "name": name, "description": desc, "url": url, "inLanguage": "fr-FR", **({"applicationCategory": "GameApplication", "operatingSystem": "Tous navigateurs", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}} if f in ("talents.html", "pseudo.html") else {})})
    return out
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
    t = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', "", t, flags=re.S)
    t = re.sub(r'<meta name="robots"[^>]*>\n?', "", t)
    t = re.sub(r'<script async src="https://pagead2\.googlesyndication\.com[^>]*></script>\n?', "", t)
    tags += '<meta name="robots" content="index, follow, max-image-preview:large">\n'
    tags += '<script type="application/ld+json">' + json.dumps(ld(f, t, title, desc, url), ensure_ascii=False) + '</script>\n'
    tags += '<link rel="alternate" type="application/rss+xml" title="ForeverWoW.fr – News" href="https://foreverwow.fr/rss.xml">\n'
    tags += '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5144798644718811" crossorigin="anonymous"></script>\n'
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S)
    if h1:
        alt = html.escape(html.unescape(re.sub(r"<[^>]+>", " ", h1.group(1))).split("  ")[0].strip(), quote=True)
        t = re.sub(r'(<div class="cover"><img src="[^"]+") alt=""', lambda m_: m_.group(1) + f' alt="{alt}"', t)
    t = t.replace("</head>", tags + "</head>", 1)
    open(f, "w", encoding="utf-8").write(t)
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
sm += [f"  <url><loc>{BASE if f == 'index.html' else BASE + f}</loc><lastmod>{LASTMOD[f]}</lastmod></url>" for f in pages]
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

# ----- Version sans JavaScript (robots, lecteurs) : menu, pied de page et news de l'accueil écrits en dur -----
# Le JavaScript du site remplace ces blocs par la version interactive ; les robots qui n'exécutent pas
# le JavaScript voient quand même la navigation et le contenu.
menu_src = open("js/site.js", encoding="utf-8").read()
links = re.findall(r'\["([a-z0-9-]+\.html)", "([^"]+?)"\]', menu_src[:menu_src.index("const POPULAIRES")])
nav = " · ".join(f'<a href="{h}">{html.escape(re.sub(r"<[^>]+>", "", l).strip())}</a>' for h, l in dict.fromkeys(links))
foot = ('<a href="a-propos.html">À propos</a> · <a href="contact.html">Contact</a> · <a href="mentions-legales.html">Mentions légales</a> · '
        '<a href="confidentialite.html">Confidentialité</a> · ForeverWoW.fr est un site de fan non officiel, sans lien avec Blizzard Entertainment.')
for f in pages:
    s = open(f, encoding="utf-8").read()
    s2 = re.sub(r'<div id="site-header">.*?</div><!--/site-header-->|<div id="site-header"></div>',
                f'<div id="site-header"><noscript><nav><a href="index.html">ForeverWoW.fr</a> · {nav}</nav></noscript></div><!--/site-header-->', s, count=1, flags=re.S)
    s2 = re.sub(r'<div id="site-footer">.*?</div><!--/site-footer-->|<div id="site-footer"></div>',
                f'<div id="site-footer"><noscript><p>{foot}</p></noscript></div><!--/site-footer-->', s2, count=1, flags=re.S)
    if f == "index.html":
        MOISF = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
        fmt = lambda d: f"{int(d[8:])} {MOISF[int(d[5:7]) - 1]} {d[:4]}"
        TYP = {"actu": ("Actu", "red"), "guide": ("Guide", ""), "site": ("Nouveau sur le site", "green")}
        order = sorted(enumerate(items), key=lambda p: (p[1][0], -p[0]), reverse=True)
        lst = [it for _, it in order]
        badge = lambda typ: f'<span class="badge {TYP[typ][1]}">{TYP[typ][0]}</span>'
        d0, l0, i0, t0, x0, y0 = lst[0]
        feat = (f'<a class="hero" href="{l0}"><img src="{i0}" alt=""><div class="hero-body">{badge(y0)} <span class="date">{fmt(d0)}</span>'
                f'<h1>{html.escape(t0)}</h1><p>{html.escape(x0)}</p></div></a>')
        feed = "".join(f'<a class="nitem" href="{l}"><div class="nthumb"><img src="{i}" alt="" loading="lazy"></div><div class="nbody"><div class="nmeta">{badge(y)}<span class="date">{fmt(d)}</span></div><h3>{html.escape(ti)}</h3><p>{html.escape(tx)}</p></div></a>'
                       for d, l, i, ti, tx, y in lst[1:9])
        s2 = re.sub(r'<div id="featured">.*?</div><!--/featured-->|<div id="featured"></div>', f'<div id="featured">{feat}</div><!--/featured-->', s2, count=1, flags=re.S)
        s2 = re.sub(r'<div class="feed" id="feed">.*?</div><!--/feed-->|<div class="feed" id="feed"></div>', f'<div class="feed" id="feed">{feed}</div><!--/feed-->', s2, count=1, flags=re.S)
    if s2 != s: open(f, "w", encoding="utf-8").write(s2)
print("navigation sans JavaScript ajoutée")
