"""Génère une page par donjon (donjon-<slug>.html) : emplacement sur la carte, boss et butin, quêtes.
Données : dictionnaire DONJONS ci-dessous. Noms des quêtes, PNJ et objets en français d'après Polestar (données du jeu, CC BY 4.0) ;
taux de butin relevés pendant la bêta (sources citées dans chaque entrée).
Lancer : python3 tools/donjons_pages.py puis python3 tools/seo.py"""
import re, os, html
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")
e = html.escape
QCOL = {2: "#1eff00", 3: "#0070dd", 4: "#a335ee", 5: "#ff8000"}
def item(n, i=None):
    i = i or ITEMS.get(n)
    return f'<a class="wh" href="https://www.wowhead.com/forever/fr/item={i}" target="_blank" rel="noopener" data-wowhead="item={i}&domain=fr.forever">{e(n)}</a>' if i else e(n)

# Identifiants des objets (données du jeu) : servent aux liens et aux info-bulles Wowhead
ITEMS = {'Drapé spectresprit': 271097, 'Sautoir éphémère': 270227, 'Brassards brindecieux': 271096, 'Canne cœur-de-golem': 270228, 'Bottines du golem protecteur': 270229, 'Plastron de garde golem': 271098, 'Hache-croissant de Durgen': 270256, 'Jambières de Dirgehammer': 270260, 'Robe de thane déshonoré': 270261, 'Tête de Durgen Mornemartel': 274286, 'Tromblon calibré': 279894, 'Grand marteau de Forgefer': 279895, 'Cœur-de-brasier': 279896, 'Ceinture poussiéreuse': 279897, 'Brassards du marcheur des cryptes': 280095, 'Tome nain': 279898, 'Gants de pillage de tombes': 280096, 'Cape des catacombes': 279899, 'Chausses creuses-tombes': 279900}

DONJONS = {
"salle-des-thanes": {
  "nom": "La Salle des Thanes", "en": "The Hall of Thanes", "niv": "13 à 18", "joueurs": 5, "nouveau": True,
  "intro": "Sous le vieux Forgefer dorment les tombeaux des anciens rois nains. Des pilleurs ont forcé les portes, et les esprits des thanes ne trouvent plus le repos. C'est l'un des neuf nouveaux donjons de Forever, et le premier que croiseront les nains, les gnomes et les humains vers le niveau 15.",
  "zone": "Forgefer", "carte": 1455, "x": 43.5, "y": 52.0,
  "acces": "L'entrée se trouve en plein cœur de Forgefer. Le donjon est accessible dès le niveau 13 par la recherche de groupe ; ses quêtes demandent le niveau 15. Les quêtes sont surtout côté Alliance.",
  "boss": [
    ("Faldrim Courbenclume", "Faldrim Anvilmar", "L'esprit d'un ancien thane, qu'une des quêtes demande d'apaiser.",
     [("Drapé spectresprit", "Cape", 37.6), ("Sautoir éphémère", "Cou", 31.2), ("Brassards brindecieux", "Poignets", 31.2)]),
    ("Infurnus", "Infurnus", "Le deuxième boss du tombeau.", []),
    ("Pilleur", "Plunder", "Le troisième boss, dont le butin est taillé dans des pièces de golem gardien.",
     [("Canne cœur-de-golem", "Bâton", 37.3), ("Bottines du golem protecteur", "Pieds", 34.1), ("Plastron de garde golem", "Torse", 28.6)]),
    ("Durgen Mornemartel", "Durgen Dirgehammer", "Le chef des pilleurs, dernier boss. Sa tête est demandée par le roi Magni.",
     [("Hache-croissant de Durgen", "Arme", 28.5), ("Jambières de Dirgehammer", "Jambes", 24.6), ("Robe de thane déshonoré", "Torse", 21.5), ("Tête de Durgen Mornemartel", "Objet de quête", 58.5)]),
  ],
  "butin_note": "Taux relevés sur 126 à 157 victoires pendant la bêta (build 1.60.1.70205) : ils donnent un ordre d'idée et peuvent changer. Emplacements déduits des noms des objets.",
  "quetes": [
    ("Incursion dans le Vieux Forgefer", 16, "Alliance", "Terre-voyant Farsen, Dun Morogh (64.9, 58.5)", "Rapporter la tête de Durgen Mornemartel au roi Magni Bronzebeard, à Forgefer.",
     ["Tromblon calibré", "Grand marteau de Forgefer", "Cœur-de-brasier"], "Forgefer et Exilés de Gnomeregan",
     "Deuxième étape : elle suit « La carte souterraine », qui commence en ramassant la Carte sombrefer."),
    ("Les morts sans repos", 15, "Alliance", "Afadra Mur-de-Dun, Forgefer (33, 48)", "Vaincre les apparitions enragées et les âmes tourmentées du tombeau, puis apaiser l'esprit de Courbenclume.",
     ["Ceinture poussiéreuse", "Brassards du marcheur des cryptes"], "Forgefer", ""),
    ("Précieux héritages", 15, "Alliance", "Thom Filch, dans le donjon", "Récupérer des héritages nains dans les tombeaux.",
     ["Tome nain", "Gants de pillage de tombes"], "Gadgetzan", ""),
    ("Une rancune ancestrale", 15, "Alliance et Horde", "Domestique fantomatique, dans le donjon", "Apaiser l'esprit de Faldrim Courbenclume.",
     ["Cape des catacombes", "Chausses creuses-tombes"], "", ""),
  ],
  "conseils": ["Les quêtes de donjon de Forever rapportent beaucoup plus d'expérience qu'en Classic, surtout lors du premier passage : prends-les toutes avant d'entrer.",
               "Deux quêtes se prennent à l'intérieur : regarde autour de toi dès l'entrée.",
               "Garde la tête de Durgen (58,5 % de chances) pour le roi Magni, au palais de Forgefer."],
  "sources": [("Kami Labs", "https://kami-labs.fr/la-salle-des-thanes-wow-forever/")],
},
}

def page(slug, d):
    auto = d.get("auto")
    boss = ""
    for i, b in enumerate(d["boss"], 1):
        if auto:
            fr, en, loot = b; desc = ""
            loot = [(n, t, None, iid) for n, t, _, iid, ql in loot]
        else:
            fr, en, desc, loot = b
            loot = [(n, t, p, None) for n, t, p in loot]
        pc = any(p is not None for _, _, p, _ in loot)
        rows = "".join(f'<tr><td><b>{item(n, iid)}</b></td><td>{e(t)}</td>' + (f'<td class="pct"><span class="pbar"><i style="width:{p}%"></i></span>{str(p).replace(".", ",")} %</td>' if pc else "") + '</tr>' for n, t, p, iid in loot)
        head = '<th>Objet</th><th>Type</th>' + ('<th>Chance</th>' if pc else '')
        tab = f'<div class="table-wrap"><table class="rtable dj-loot"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>' if loot else '<p class="small">Pas de butin relevé pendant la bêta.</p>'
        boss += f'<div class="dj-boss"><h3><span class="dj-n">{i}</span> {e(fr)}' + (f' <span class="dm-en">{e(en)}</span>' if en != fr else '') + f'</h3>{f"<p>{e(desc)}</p>" if desc else ""}{tab}</div>'
    qs = ""
    for qd in d["quetes"]:
        if auto:
            n, niv, camp, de, rec = qd; obj = rep = note = ""
            recs = " · ".join(item(r, iid) for r, iid in rec)
        else:
            n, niv, camp, de, obj, rec, rep, note = qd
            recs = " · ".join(item(r) for r in rec)
        cls = "a" if camp == "Alliance" else ("h" if camp == "Horde" else "s")
        qs += f'''<div class="dj-q"><h3>{e(n)} <span class="pp-lv">niveau {niv}</span> <span class="race {cls}">{e(camp)}</span></h3>
  <p><b>Donnée par :</b> {e(de)}</p>{f"<p><b>Objectif :</b> {e(obj)}</p>" if obj else ""}
  {f"<p><b>Récompense :</b> {recs}{f' · réputation {e(rep)}' if rep else ''}</p>" if recs else ""}{f'<p class="small">{e(note)}</p>' if note else ""}</div>'''
    tips = "".join(f"<li>{e(t)}</li>" for t in d.get("conseils", []))
    src = ", ".join(f'<a href="{u}" target="_blank" rel="noopener">{e(n)}</a>' for n, u in d.get("sources", []))
    carte = (f'<div class="dj-map"><img src="images/cartes/{d["carte"]}.webp" alt="Carte : {e(d["zone"])}" loading="lazy"><span class="dj-pin" style="left:{d["x"]}%;top:{d["y"]}%" title="Entrée"></span></div>'
             if d.get("carte") else '<div class="dj-map dj-nomap"><img src="images/ico/lib/carte.webp" alt="" width="96" height="96"><p>Emplacement exact à venir.</p></div>')
    entree = f'{e(d.get("zone", "À confirmer"))}' + (f' <span class="xy">{d["x"]}, {d["y"]}</span>' if d.get("carte") else "")
    acces = d.get("acces") or ("Le point rouge marque l'entrée du donjon." if d.get("carte") else "")
    if auto:
        bnote = ("Butin d'après les données de WoW Classic : Forever a ajouté de nouveaux objets dans les donjons, la liste sera complétée en jeu. "
                 "Seuls les objets de qualité inhabituelle et mieux sont listés.")
        if not d["boss"]: bnote = "Le butin de ce nouveau donjon sera ajouté dès qu'il sera connu."
        qnote = "" if d["quetes"] else '<p class="small">Pas de quête connue pour ce donjon pour l\'instant.</p>'
    else:
        bnote, qnote = d["butin_note"], ""
    bloc_tips = f'<div class="article" style="margin-top:18px"><h2>Conseils</h2><ul>{tips}</ul></div>' if tips else ""
    return f'''<main><div class="wrap">
<div class="crumbs"><a href="index.html">News</a> › <a href="donjons.html">Donjons &amp; Raids</a> › {e(d["nom"])}</div>
<h1 class="page-title">{e(d["nom"])} <span class="pp-lv">niveaux {e(d["niv"])}</span>{' <span class="badge">Nouveau</span>' if d.get("nouveau") else ''}</h1>
<p class="page-lead">{e(d["intro"])}</p>
<div class="dj-top">
  {carte}
  <div class="article dj-info">
    <h2>Accès</h2>
    <ul class="dj-facts"><li><img src="images/ico/lib/boussole.webp" alt=""> <span><b>Entrée</b> {entree}</span></li>
      <li><img src="images/ico/lib/groupe.webp" alt=""> <span><b>{d.get("joueurs", 5)} joueurs</b> · niveaux {e(d["niv"])}</span></li>
      <li><img src="images/ico/lib/quete.webp" alt=""> <span><b>{len(d["quetes"])} quête{"s" if len(d["quetes"]) > 1 else ""}</b> · {len(d["boss"])} boss</span></li></ul>
    <p>{e(acces)}</p>
    <p class="small">Toutes les zones sont sur notre <a href="carte.html">carte interactive</a>.</p>
  </div>
</div>
<div class="sec-title"><h2>Les boss et leur butin</h2></div>
{boss}
<p class="small">{e(bnote)} Passe la souris sur un objet pour voir ses caractéristiques (info-bulle Wowhead), ou clique pour ouvrir sa fiche.</p>
<div class="sec-title"><h2>Les quêtes du donjon</h2></div>
{qs}{qnote}
{bloc_tips}
<p class="small">Noms des quêtes, des PNJ et des objets d'après les données du jeu (Polestar, CC BY 4.0, et Factoruide/Questie){f" ; butin et informations complémentaires : {src}" if src else ""}.</p>
</div>'''

import json
AUTO = json.load(open("tools/donjons_auto.json", encoding="utf-8"))
for k, v in AUTO.items():
    if k not in DONJONS:
        v["auto"] = True; DONJONS[k] = v
tpl = open("legacy.html", encoding="utf-8").read()
for slug, d in DONJONS.items():
    head = tpl[:tpl.index("<main>")]
    head = re.sub(r"<title>.*?</title>", f"<title>{e(d['nom'])} : guide du donjon de WoW Forever – ForeverWoW</title>", head)
    head = re.sub(r'name="description" content=".*?"', f'name="description" content="{e(d["nom"])} ({d.get("en", d["nom"])}), donjon de WoW Forever niveaux {d["niv"]} : emplacement, boss et butin, quêtes et conseils."', head)
    tail = re.sub(r'<script src="js/heritage\.js[^"]*"></script>\n?', '', tpl[tpl.index("</main>"):])
    tail = tail.replace("</body>", '<script>const whTooltips = {colorLinks: true, iconizeLinks: true, renameLinks: false, iconSize: "small"};</script>\n<script src="https://wow.zamimg.com/js/tooltips.js"></script>\n</body>', 1)
    open(f"donjon-{slug}.html", "w", encoding="utf-8").write(head + page(slug, d) + tail)
print(len(DONJONS), "donjon(s)")
