"""Génère tier-list.html à partir de tools/tierlists.json.
Classements d'après Forever Meta (https://github.com/snibi/forever-meta, src/content/tierlists) ;
textes en français écrits à la main. Chaque liste porte sa date de création et son patch."""
import json, re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")
D = json.load(open("tools/tierlists.json", encoding="utf-8"))
G = re.findall(r'^"([a-z-]+)":\("([^"]+)","([^"]+)"', open("tools/guides.py", encoding="utf-8").read(), re.M)
SPEC = {k: n for k, n, r in G}
CLS = {"warrior": ("Guerrier", "#C69B6D"), "paladin": ("Paladin", "#D9619C"), "hunter": ("Chasseur", "#7FAE3E"), "rogue": ("Voleur", "#D4B82A"),
 "priest": ("Prêtre", "#9A9A9A"), "shaman": ("Chaman", "#0070DD"), "mage": ("Mage", "#2BA9CC"), "warlock": ("Démoniste", "#7072D6"), "druid": ("Druide", "#E86E08")}
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
def date_fr(d):
    a, m, j = d.split("-"); return f"{int(j)}{'er' if j == '01' else ''} {MOIS[int(m)-1]} {a}"
TIERS = ["S", "A", "B", "C", "D"]

def liste(L):
    rows = ""
    for t in TIERS:
        es = L["tiers"].get(t, [])
        if not es: continue
        chips = ""
        for ref, note in es:
            c = ref.split("-")[0]; cn, col = CLS[c]
            chips += f'''<li class="tl-e" style="--c:{col}"><a href="guides.html#{ref}"><img src="images/icons/class_{c}.jpg" alt="" width="28" height="28"><span><b>{SPEC[ref]}</b><i>{cn}</i></span></a><p>{note}</p></li>'''
        rows += f'<div class="tl-row"><div class="tl-t t{t}">{t}</div><ul class="tl-es">{chips}</ul></div>'
    return f'''<section class="tl" id="{L["id"]}">
  <h2>{L["titre"]}</h2>
  <p class="stamp"><span>📅 Créée le <b>{date_fr(L["cree"])}</b></span><span>🛠 Patch <b>{L["patch"]}</b> (bêta)</span><span>Fiabilité : <b>{L["fiab"]}</b></span></p>
  <p>{L["intro"]}</p>
  {rows}
  <p class="small"><b>Sur quoi repose ce classement :</b> {L["base"]}</p>
</section>'''

jumps = "".join(f'<a class="jump" href="#{L["id"]}">{L["titre"]}</a>' for L in D["listes"])
body = f'''<main><div class="wrap">
<div class="crumbs"><a href="index.html">News</a> › Classes / Races › Tier lists niveau 60</div>
<h1 class="page-title">Tier lists niveau 60</h1>
<p class="page-lead">Quelles spécialisations dominent au niveau 60 ? Quatre classements : dégâts, tanks, soigneurs et JcJ. Clique sur une spé pour voir son build, ses statistiques et ses races conseillées.</p>
<div class="info"><b>À lire avant tout :</b> ces classements ont été établis pendant la bêta, limitée au niveau 30. Ce sont des <b>projections</b> : chaque liste indique la date à laquelle elle a été créée et le patch utilisé. Elles seront refaites après la sortie, quand les premiers joueurs auront atteint le niveau 60 et que les raids auront ouvert. Et surtout : joue la classe qui te plaît, l'écart entre une spé S et une spé B compte peu en dehors des raids les plus durs.</div>
<nav class="jumps" style="margin-top:16px">{jumps}</nav>
{"".join(liste(L) for L in D["listes"])}
<p class="small">Classements d'après le projet <a href="https://snibi.github.io/forever-meta/" target="_blank" rel="noopener">Forever Meta</a> (données du 1er octobre 2026), qui recoupe les guides d'Icy Veins, les présentations de Blizzard et les classements publics. Explications rédigées par ForeverWoW. Les builds de chaque spé sont sur la page <a href="guides.html">Guides de spé</a>.</p>
</div>'''

tpl = open("legacy.html", encoding="utf-8").read()
head = tpl[:tpl.index("<main>")]
head = re.sub(r"<title>.*?</title>", "<title>Tier lists niveau 60 – ForeverWoW</title>", head)
head = re.sub(r'name="description" content=".*?"', 'name="description" content="Tier lists de WoW Forever au niveau 60 : meilleures spécialisations en dégâts, tank, soins et JcJ, avec la date et le patch de chaque classement."', head)
tail = re.sub(r'<script src="js/heritage\.js[^"]*"></script>\n?', '', tpl[tpl.index("</main>"):])
open("tier-list.html", "w", encoding="utf-8").write(head + body + tail)

js = open("js/site.js", encoding="utf-8").read()
if "tier-list.html" not in js:
    js = js.replace('["guides.html", "Guides de spé"], ', '["guides.html", "Guides de spé"], ["tier-list.html", "Tier lists niveau 60"], ', 1)
    js = js.replace('<a href="guides.html">Guides de spé</a>', '<a href="guides.html">Guides de spé</a><a href="tier-list.html">Tier lists 60</a>', 1)
    open("js/site.js", "w", encoding="utf-8").write(js)
print("ok", sum(len(v) for L in D["listes"] for v in L["tiers"].values()), "entrées")
