"""Génère une page par donjon (donjon-<slug>.html) : emplacement sur la carte, boss et butin, quêtes.
Données : dictionnaire DONJONS ci-dessous. Noms des quêtes, PNJ et objets en français d'après Polestar (données du jeu, CC BY 4.0) ;
taux de butin relevés pendant la bêta (sources citées dans chaque entrée).
Lancer : python3 tools/donjons_pages.py puis python3 tools/seo.py"""
import re, os, html, json
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")
e = html.escape
QCOL = {2: "#1eff00", 3: "#0070dd", 4: "#a335ee", 5: "#ff8000"}
def item(n, i=None):
    i = i or ITEMS.get(n)
    return f'<a class="wh" href="https://www.wowhead.com/forever/fr/item={i}" target="_blank" rel="noopener" data-wowhead="item={i}&domain=fr.forever">{e(n)}</a>' if i else e(n)

# Identifiants des objets (données du jeu) : servent aux liens et aux info-bulles Wowhead
ITEMS = {'Drapé spectresprit': 271097, 'Sautoir éphémère': 270227, 'Brassards brindecieux': 271096, 'Canne cœur-de-golem': 270228, 'Bottines du golem protecteur': 270229, 'Plastron de garde golem': 271098, 'Hache-croissant de Durgen': 270256, 'Jambières de Dirgehammer': 270260, 'Robe de thane déshonoré': 270261, 'Tête de Durgen Mornemartel': 274286, 'Tromblon calibré': 279894, 'Grand marteau de Forgefer': 279895, 'Cœur-de-brasier': 279896, 'Ceinture poussiéreuse': 279897, 'Brassards du marcheur des cryptes': 280095, 'Tome nain': 279898, 'Gants de pillage de tombes': 280096, 'Cape des catacombes': 279899, 'Chausses creuses-tombes': 279900, 'Bloodslash Axe': 274598, 'Oathbound Bracers': 274599, 'Berserker Shackles': 274600, "Linken's Boots of Iron": 271718, 'Ancient Gurubashi Idol': 276894, 'Knucklebone Ring': 274614, 'Viscera Spaulders': 274607, 'Bloodspine Staff': 274606, 'Serpentbane Crown': 274609, "Ritual-Binder's Gloves": 274610, "Maw of Min'loth": 274608, 'Harpoon of Command': 274601, 'Brinebelly Leggings': 274602, 'Priestess Cloak': 274613, 'Frosty Blunderbuss': 274604, 'Dreadfrost Saber': 274603, 'Briny Sash': 274605, 'Waterlogged Burial Shroud': 274612, 'Heart of the Primeval': 274615, 'Robe of the Drowned': 274611, 'Tidesoaked Leggings': 279888, "Naga Priestess's Mantle": 279889, 'Rusted Troll War Belt': 279882, "Saltseer's Helm": 279930, 'Mutinous Cuffs': 279883, 'South Seas Shroud': 279884}

DONJONS = {
"salle-des-thanes": {
  "nom": "La Salle des Thanes", "en": "The Hall of Thanes", "niv": "13 à 18", "joueurs": 5, "nouveau": True,
  "intro": "Sous le vieux Forgefer dorment les tombeaux des anciens rois nains. Des pilleurs ont forcé les portes, et les esprits des thanes ne trouvent plus le repos. C'est l'un des neuf nouveaux donjons de Forever, et le premier que croiseront les nains, les gnomes et les humains vers le niveau 15.",
  "zone": "Forgefer", "carte": 1455, "x": 43.5, "y": 52.0,
  "acces": "L'entrée se trouve en plein cœur de Forgefer. Le donjon est accessible dès le niveau 13 par la recherche de groupe ; ses quêtes demandent le niveau 15. Les quêtes sont surtout côté Alliance.",
  "boss": [
    ("Faldrim Courbenclume", "Faldrim Anvilmar", "L'esprit d'un ancien thane, qu'une des quêtes demande d'apaiser.",
     [("Drapé spectresprit", "Cape", 37.6), ("Sautoir éphémère", "Cou", 31.2), ("Brassards brindecieux", "Poignets", 31.2)]),
    ("Magmatus", "Magmatus", "Le deuxième boss du tombeau, un être de magma.", []),
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
"cite-submergee": {
  "nom": "La Cité submergée", "en": "The Drowned City", "niv": "35 à 40", "joueurs": 5, "nouveau": True,
  "intro": "Au large de Strangleronce, la vieille cité troll d'I'lalai est remontée des flots. Des trolls morts-vivants, les nagas Écaille-de-mer et les pirates sel-augures se la disputent, sous le regard de Min'loth le Serpent. C'est l'un des neuf nouveaux donjons de Forever, ouvert à l'Alliance comme à la Horde, sans clé.",
  "zone": "Vallée de Strangleronce", "carte": 1434, "x": 21.4, "y": 27.9,
  "acces": "L'entrée est sous l'eau, à l'ouest du Récif infâme : une grotte marquée par une grande tablette de pierre. Prévois une potion de respiration aquatique. Côté Horde, pars du campement Grom'gol ; côté Alliance, remonte la côte depuis Baie-du-Butin.",
  "boss": [
    ("Zul'Alai", "Zul'Alai", "Un troll mort-vivant. Sors de sa portée pendant Heurt monstrueux (étourdissement), dissipe Frappe moisie, et accélère sous 30 % : Serment immortel le soigne et le rend plus rapide.",
     [("Bloodslash Axe", "Hache à une main", 36), ("Oathbound Bracers", "Poignets (cuir)", 35), ("Berserker Shackles", "Poignets (mailles)", 30), ("Linken's Boots of Iron", "Pieds (mailles)", 1.8)]),
    ("Var'Taka", "Var'Taka", "Le chef des nagas Écaille-de-mer, avec deux prêtresses : contrôles-en une et tue l'autre. Le tank le tourne dos au groupe (Enchaînement) et revient vite s'il est harponné. Active la perle lumineuse après le combat.",
     [("Harpoon of Command", "Arme d'hast", 39), ("Brinebelly Leggings", "Jambes (cuir)", 37), ("Priestess Cloak", "Dos", 25)]),
    ("Capitaine Lèveffroi", "Captain Dreadrise", "Le chef des pirates, sur son épave. Nettoie les pirates autour avant, garde une interruption pour la Salve d'éclairs d'eau, et libère vite un joueur pris dans la Saumure. Il craint les étourdissements. Active la perle après le combat.",
     [("Frosty Blunderbuss", "Arme à feu", 38), ("Dreadfrost Saber", "Épée à une main", 33), ("Briny Sash", "Taille (tissu)", 29), ("Linken's Boots of Iron", "Pieds (mailles)", 1.4)]),
    ("Élémentaire primitif", "Primeval Elemental", "Boss facultatif, dans les tunnels noyés près des archives : détruis toutes les offrandes de sa salle pour le faire venir, et attention à son souffle.",
     [("Waterlogged Burial Shroud", "Dos", 36), ("Heart of the Primeval", "Bijou", 33), ("Robe of the Drowned", "Torse (tissu)", 31)]),
    ("Moelle impérissable", "Deathless Marrow", "Éclair de sang touche tout le groupe et des renforts arrivent sans cesse : le tank les regroupe, on tue d'abord les gardiens qui étourdissent, sans oublier le boss. Il porte l'Idole antique des Gurubashi.",
     [("Ancient Gurubashi Idol", "Objet de quête", 87), ("Knucklebone Ring", "Doigt", 28), ("Viscera Spaulders", "Épaules (mailles)", 26), ("Bloodspine Staff", "Bâton", 23)]),
    ("Min'loth le Serpent", "Min'loth the Serpent", "Le dernier boss, en deux phases. En troll : protège le tank contre Torrent et prépare les soins pour Déluge. En serpent, il revient avec toute sa vie : dissipe le poison et prévois les peurs (le Totem de séisme aide). Un coffre attend dans l'épave voisine.",
     [("Serpentbane Crown", "Tête (mailles)", 36), ("Ritual-Binder's Gloves", "Mains (cuir)", 34), ("Maw of Min'loth", "Bouclier", 30), ("Linken's Boots of Iron", "Pieds (mailles)", 2.8)]),
  ],
  "butin_note": "Taux relevés par Forever Changes. Les objets de ce nouveau donjon n'ont pas encore de nom français dans les données du jeu : on garde le nom anglais pour l'instant.",
  "quetes": [
    ("Le seul bon Écaille-de-mer…", 38, "Horde", "Commandant Aggro'gosh, Grom'gol, Strangleronce (32.2, 28.8)", "Tuer Var'Taka.",
     ["Tidesoaked Leggings", "Naga Priestess's Mantle"], "", "Suit « Des adversaires sous les flots », du même PNJ. Dès le niveau 30."),
    ("La cité Submergée", 40, "Horde", "Kin'weelay, Grom'gol, Strangleronce (32.2, 27.8)", "Faire des reproductions des quatre tablettes d'I'lalai avec la peau et le charbon.",
     [], "", "Au bout de la suite « Le Récif infâme », « Les anciennes légendes des Gurubashi » et « À la recherche de la cité perdue ». Dès le niveau 30."),
    ("L'idole des anciens Gurubashi", 40, "Horde", "Mazu'kon, Mulgore (32.6, 20.6)", "Rapporter l'Idole antique des Gurubashi, portée par la Moelle impérissable.",
     [], "", "Dès le niveau 30."),
    ("Cap sur les eaux troubles", 40, "Alliance", "Maître des traditions Dibbs, Austrivage, Contreforts de Hautebrande (50.6, 57.0)", "Faire des reproductions des quatre tablettes d'I'lalai.",
     [], "", "La suite commence au Camp des rebelles de Strangleronce (Sergent Yohwa, puis frère Nimetz) et mène à Dibbs. Dès le niveau 30."),
    ("Les magies de la cité Submergée", 40, "Alliance", "Maître des traditions Dibbs, Austrivage, Contreforts de Hautebrande (50.6, 57.0)", "Récupérer 5 fétiches d'I'lalai sur les trolls du donjon.",
     [], "", "Dès le niveau 30."),
    ("Les secrets des anciens Gurubashi", 40, "Alliance", "Archimage Timear, devant la Cité de Dalaran, Montagnes d'Alterac (15.6, 73.6)", "Rapporter l'Idole antique des Gurubashi, portée par la Moelle impérissable.",
     [], "", "Dès le niveau 34."),
    ("Sel-augures véreux", 40, "Alliance et Horde", "Krazek, Baie-du-Butin, Strangleronce (27.0, 77.2)", "Rapporter 10 artéfacts vaudou pris aux pirates sel-augures.",
     ["Rusted Troll War Belt", "Saltseer's Helm"], "", "Dès le niveau 34."),
    ("Le capitaine sel-augure", 40, "Alliance et Horde", "Krazek, Baie-du-Butin, Strangleronce (27.0, 77.2)", "Tuer le capitaine Lèveffroi et 3 légistes sel-augures.",
     ["Mutinous Cuffs", "South Seas Shroud"], "", "Dès le niveau 34."),
  ],
  "conseils": ["Prends toutes les quêtes avant d'entrer : elles rapportent près de 48 000 points d'expérience par faction.",
               "Il faut activer les deux perles lumineuses (après Var'Taka et après le capitaine Lèveffroi) pour ouvrir le chemin vers la fin : tuer les deux boss ne suffit pas.",
               "Évite Zin'aka, le requin qui tourne dans le grand bassin central.",
               "Les monstres reviennent deux heures après leur mort : pas de panique si tu dois ressortir.",
               "Trois boss rares peuvent apparaître : Umbra et son escorte, Gill (dans les tunnels de l'élémentaire, attention à sa dynamite) et « Pyromancien » Braxton chez les pirates."],
  "sources": [("JudgeHype", "https://wowforever.judgehype.com/article/cite-submergee/"), ("Forever Changes (butin)", "https://foreverchanges.pro/fr/dungeons/the-drowned-city")],
},
}

OBJ = json.load(open("tools/donjons_objets.json", encoding="utf-8")) if os.path.exists("tools/donjons_objets.json") else {}
# Repères de parcours ajoutés à la main (indices des quêtes, mécanismes)
PARCOURS = {
 "cite-submergee": ["Après Zul'Alai, la cité s'ouvre sur un grand bassin central : Var'Taka est dans le bâtiment au sud, l'épave du capitaine Lèveffroi dans le secteur des pirates.",
             "Les quatre tablettes d'I'lalai (quêtes « La cité Submergée » et « Cap sur les eaux troubles ») : en bas de l'escalier à gauche après Zul'Alai, près de la salle de Var'Taka, dans un grand crâne du secteur des pirates, et près de la salle de Min'loth.",
             "Une fois les deux perles activées, le chemin mène à la Moelle impérissable puis à Min'loth le Serpent."],
 "uldaman": ["Le Bâton de la Préhistoire ouvre la salle d'Ironaya : assemble la Hampe de Tsol (sur Revelosh) et le Médaillon de Gni'kiv (coffre de Baelog), puis utilise-le près de la maquette, dans la grande salle ronde.",
             "D'après le journal de quête : le rubis est dans une zone barricadée des nains Ombreforge, le topaze dans une urne d'une zone de troggs près des nains de l'Alliance, et le saphir sur Grimlok, le chef des troggs.",
             "Les restes du paladin (quête « Retour à Uldaman ») sont un squelette à cliquer, au sol, à l'intérieur de l'instance."],
}

# Vidéos de nos sorties (chaîne Mygale TV)
VIDEOS = {"salle-des-thanes": ("T45mZ8WVmXU", "La Salle des Thanes : donjon complet, avec les 4 boss jusqu'à Durgen Mornemartel"),
          "profondeurs-de-brassenoire": ("KybRsn7H104", "Les Profondeurs de Brassenoire : donjon complet, avec les 5 boss jusqu'à Aku'mai"),
          "souilles-de-tranchebauge": ("0Cvai40D_Lw", "Les Souilles de Tranchebauge : donjon complet, avec les 5 boss jusqu'à Pestegueule le Pourrissant"),
          "uldaman": ("NQFoRC2iX-4", "Uldaman : donjon complet, avec les 8 boss jusqu'à Archaedas"),
          "la-prison": ("10h7zMqJR-k", "La Prison : donjon complet, avec les 4 boss jusqu'à Dextren Ward"),
          "cite-submergee": ("1JFWQZr0nLY", "La Cité submergée : donjon complet, avec les 6 boss jusqu'à Min'loth le Serpent")}

def video(slug):
    if slug not in VIDEOS: return ""
    vid, titre = VIDEOS[slug]
    return f'''<div class="sec-title"><h2>La vidéo du donjon</h2></div>
<div class="article"><a class="dj-video" href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener"><img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="Vidéo : {e(titre)}" loading="lazy" width="480" height="360"><span class="vid-btn" aria-hidden="true">▶</span></a>
<p><b>{e(titre)}</b>, sur la chaîne YouTube <a href="https://www.youtube.com/@mygaletv8715" target="_blank" rel="noopener">Mygale TV</a>. Toutes nos vidéos sont sur la page <a href="videos.html">Vidéos</a>.</p></div>'''

def parcours(slug, d):
    o = OBJ.get(slug, {})
    noms = [b[0] for b in d["boss"]]
    ordre = "".join(f"<li>{e(n)}</li>" for n in noms)
    rows = ""
    for r in o.get("objets", []):
        cls = {"Alliance": "a", "Horde": "h"}.get(r["camp"], "s")
        camp = r["camp"] or "Les deux"
        nb = f'{r["nb"]} × ' if r["nb"] > 1 else ""
        rows += f'<tr><td><b>{nb}{item(r["objet"], r["id"])}</b></td><td>{e(", ".join(r["sur"]))}</td><td>{e(" · ".join(r["quetes"]))} <span class="race {cls}">{e(camp)}</span></td></tr>'
    tab = (f'<h3>Objets de quête à trouver dans l\'instance</h3><div class="table-wrap"><table class="rtable"><thead><tr><th>Objet</th><th>Sur quoi / sur qui</th><th>Quête</th></tr></thead><tbody>{rows}</tbody></table></div>') if rows else ""
    notes = "".join(f"<li>{e(t)}</li>" for t in PARCOURS.get(slug, []))
    img = f"images/donjons/{slug}.webp"
    if os.path.exists(img):
        carte = f'<figure class="dj-plan"><img src="{img}" alt="Carte du donjon {e(d["nom"])}" loading="lazy"><figcaption>Carte du donjon en jeu.</figcaption></figure>'
    else:
        carte = '<p class="small">Plan du donjon en jeu : capture à venir.</p>'
    wh = ""
    if not d.get("nouveau") and o.get("zone"):
        wh = f'<p>Carte interactive du donjon : <a href="https://www.wowhead.com/classic/fr/zone={o["zone"]}" target="_blank" rel="noopener">voir sur Wowhead</a> (version Classic, le plan est le même).</p>'
    return f'''<div class="sec-title"><h2>Carte et parcours</h2></div>
<div class="article">
{carte}{wh}
{f"<ul>{notes}</ul>" if notes else ""}
{tab}
</div>'''

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
             if d.get("carte") else '<div class="dj-map dj-nomap"><img src="images/ico/lib/monde.webp" alt="" width="96" height="96"><p>Emplacement exact à venir.</p></div>')
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
    <ul class="dj-facts"><li><img src="images/ico/lib/carte.webp" alt=""> <span><b>Entrée</b> {entree}</span></li>
      <li><img src="images/ico/lib/communaute.webp" alt=""> <span><b>{d.get("joueurs", 5)} joueurs</b> · niveaux {e(d["niv"])}</span></li>
      <li><img src="images/ico/lib/quete.webp" alt=""> <span><b>{len(d["quetes"])} quête{"s" if len(d["quetes"]) > 1 else ""}</b> · {len(d["boss"])} boss</span></li></ul>
    <p>{e(acces)}</p>
    <p class="small">Toutes les zones sont sur notre <a href="carte.html">carte interactive</a>.</p>
  </div>
</div>
{parcours(slug, d)}
{video(slug)}
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
