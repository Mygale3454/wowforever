"""Génère montures.html (guide des montures de WoW Forever).
Noms français des montures : traductions du module Polestar_frFR (CC BY 4.0, données du client du jeu).
Lancer : python3 tools/montures.py puis python3 tools/seo.py"""
import re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")

def chips(*noms, swift=False):
    return "".join(f'<li class="mt-m{" sw" if swift else ""}">{n}</li>' for n in noms)

def racial(img, race, fac, pnj, lieu, coords, normales, rapides, note=""):
    pic = f'<img class="mt-pic" src="images/montures/{img}.webp" alt="Monture {race.split(" :")[0].lower()} (illustration)" width="437" height="315" loading="lazy">' if os.path.exists(f"images/montures/{img}.webp") else ""
    return f'''<article class="mt-card {fac}{" pic" if pic else ""}">{pic}
  <img class="mt-face" src="images/races/{img}.webp" alt="" width="64" height="64">
  <div>
    <h3>{race}</h3>
    <p class="mt-where"><b>{pnj}</b> · {lieu}{f' <span class="xy">{coords}</span>' if coords else ''}</p>
    <ul class="mt-list">{chips(*normales)}{chips(*rapides, swift=True)}</ul>
    {f'<p class="small">{note}</p>' if note else ''}
  </div>
</article>'''

ALLIANCE = [
    racial("humain", "Humain : chevaux", "a", "Katie Hunter", "Forêt d'Elwynn, ferme de l'Est", "84.2, 65.5",
           ["Bride d'étalon noir", "Bride de pinto", "Bride de jument alezane", "Bride de cheval bai"], ["Palefroi bai rapide", "Palefroi blanc rapide"]),
    racial("nain", "Nain : béliers", "a", "Veron Amberstill", "Dun Morogh, ranch d'Amberstill", "63.5, 50.6",
           ["Bélier gris", "Bélier brun", "Bélier blanc"], ["Bélier gris rapide", "Bélier brun rapide", "Bélier blanc rapide"]),
    racial("gnome", "Gnome : mécanotrotteurs", "a", "Milli Featherwhistle", "Dun Morogh, dépôt de Steelgrill", "49.1, 48.0",
           ["Mécanotrotteur rouge", "Mécanotrotteur bleu", "Mécanotrotteur vert", "Mécanotrotteur brut"], ["Mécanotrotteur vert rapide", "Mécanotrotteur blanc rapide", "Mécanotrotteur jaune rapide"]),
    racial("elfe", "Elfe de la nuit : sabres", "a", "Lelanai", "Darnassus, terrasse des Guerriers", "38.3, 15.3",
           ["Rênes de sabre-de-nuit rayé", "Rênes de sabre-de-givre rayé", "Rênes de sabre-de-givre tacheté"], ["Rênes de sabre-de-givre rapide", "Rênes de sabre-de-brume rapide", "Rênes de sabre-tempête rapide"]),
]
HORDE = [
    racial("orc", "Orc : loups", "h", "Ogunaro Wolfrunner", "Orgrimmar, vallée de l'Honneur", "69.4, 12.2",
           ["Cor du loup des bois", "Cor du loup redoutable", "Cor du loup brun"], ["Cor du loup brun rapide", "Cor du loup des bois rapide", "Cor du loup gris rapide"]),
    racial("troll", "Troll : raptors", "h", "Zjolnir", "Durotar, village de Sen'jin", "55.2, 75.7",
           ["Sifflet de raptor émeraude", "Sifflet de raptor turquoise", "Sifflet de raptor violet"], ["Raptor bleu rapide", "Raptor vert olive rapide", "Raptor orange rapide"]),
    racial("tauren", "Tauren : kodos", "h", "Harb Clawhoof", "Mulgore, village de Sabot-de-Sang", "47.5, 58.5",
           ["Kodo gris", "Kodo brun"], ["Grand kodo blanc", "Grand kodo brun", "Grand kodo gris"]),
    racial("mortvivant", "Mort-vivant : chevaux squelettes", "h", "Zachariah Post", "Clairières de Tirisfal, Brill", "61, 52",
           ["Cheval squelette rouge", "Cheval squelette bleu", "Cheval squelette bai"], ["Cheval de guerre squelette vert", "Cheval de guerre squelette violet"]),
]
EOLIDE = racial("skyborne", "Éolides : trotteurs des trombes", "s", "Genn Beautemps", "Île de Zéphras", "53.8, 81.3",
                ["Trotteur des trombes empyréen", "Trotteur des trombes tempêtueux", "Trotteur des trombes ombreux"],
                ["Trotteur des trombes empyréen rapide", "Trotteur des trombes tempêtueux rapide", "Trotteur des trombes ombreux rapide"],
                "Le <b>trotteur des trombes régalien</b> (et sa version rapide) existe aussi dans le jeu, mais on ne sait pas encore comment l'obtenir.")

body = f'''<main><div class="wrap">
<div class="crumbs"><a href="index.html">News</a> › Monde › Montures</div>
<h1 class="page-title">Les montures de WoW Forever</h1>
<p class="page-lead">Où acheter ta première monture, quelles bêtes chaque race propose, et comment obtenir les montures de classe, de réputation, de JcJ et de donjon. Tous les noms sont ceux du jeu en français.</p>
<p class="stamp"><span>📅 Mise à jour le <b>1er novembre 2026</b></span><span>🛠 Patch <b>1.60.1.70707</b></span></p>

<div class="article">
  <h2>L'essentiel avant de partir</h2>
  <div class="table-wrap" style="margin:12px 0"><table class="rtable"><thead><tr><th>Monte</th><th>Niveau</th><th>Vitesse</th><th>Prix (bêta)</th></tr></thead><tbody>
    <tr><td><b>Apprenti cavalier</b></td><td>40</td><td>+60 %</td><td>100 po</td></tr>
    <tr><td><b>Compagnon cavalier</b></td><td>60</td><td>+100 %</td><td>1 000 po</td></tr>
  </tbody></table></div>
  <ul>
    <li><b>Ta première monture est offerte</b> quand tu apprends la monte : le gros de la dépense, c'est l'apprentissage.</li>
    <li><b>Les montures sont liées au compte</b>, mais chaque personnage doit remplir les conditions (niveau, rang de monte, classe, faction).</li>
    <li><b>Plus de restriction de taille</b> : un gnome peut monter un sabre ou un bélier. Pour les montures d'une autre race de ta faction, il faut en général être <b>Exalté</b> auprès de sa capitale.</li>
    <li>Les montures « rapides » demandent la monte de niveau 60.</li>
  </ul>
</div>

<div class="sec-title"><h2>Les montures de race</h2></div>
<h3 class="pp-fac">Alliance</h3>
<div class="mt-grid">{"".join(ALLIANCE)}</div>
<h3 class="pp-fac">Horde</h3>
<div class="mt-grid">{"".join(HORDE)}</div>

<div class="sec-title"><h2>Les Éolides et leurs trotteurs des trombes</h2></div>
<div class="mt-eol">
  <figure><img src="images/monture-eolide.jpg" alt="Un trotteur des trombes en armure, la monture des Éolides" width="1200" height="968" loading="lazy"><figcaption>Un trotteur des trombes, la monture des Éolides (illustration).</figcaption></figure>
  <div>{EOLIDE}
  <p>Les Éolides, la nouvelle race de Forever, ne montent ni chevaux ni loups : ils ont leurs propres <b>trotteurs des trombes</b>, de grands oiseaux coureurs. Ils s'achètent auprès de <b>Genn Beautemps</b>, maître des écuries et instructeur de monte sur l'île de Zéphras, leur zone de départ. Comme les Éolides peuvent rejoindre l'Alliance ou la Horde, les trotteurs servent dans les deux camps.</p></div>
</div>

<div class="sec-title"><h2>Les montures de classe</h2></div>
<div class="mt-grid">
  <article class="mt-card pic"><img class="mt-pic" src="images/montures/paladin.webp" alt="Monture de classe (illustration)" width="643" height="284" style="aspect-ratio:643/284" loading="lazy"><img class="mt-face" src="images/icons/class_paladin.jpg" alt="" width="64" height="64"><div><h3>Paladin</h3>
    <ul class="mt-list"><li class="mt-m">Cheval de guerre (quête, niveau 40)</li><li class="mt-m sw">Destrier (longue quête, niveau 60)</li></ul>
    <p class="small">Le <b>paladin mort-vivant</b>, nouveau dans Forever, a sa propre monture et ses propres quêtes.</p></div></article>
  <article class="mt-card pic"><img class="mt-pic" src="images/montures/demoniste.webp" alt="Monture de classe (illustration)" width="665" height="284" style="aspect-ratio:665/284" loading="lazy"><img class="mt-face" src="images/icons/class_warlock.jpg" alt="" width="64" height="64"><div><h3>Démoniste</h3>
    <ul class="mt-list"><li class="mt-m">Palefroi corrompu (quête, niveau 40)</li><li class="mt-m sw">Destrier de l'effroi (longue quête, niveau 60)</li></ul>
    <p class="small">Ces montures s'invoquent comme des sorts : rien à acheter, mais la quête du niveau 60 coûte cher en composants.</p></div></article>
</div>

<div class="sec-title"><h2>Les montures à débloquer</h2></div>
<div class="mt-grid">
  <article class="mt-card"><div><h3>Rênes de kodo de bât</h3>
    <p>Réputation commerciale : environ <b>6 000 points de Faveur marchande</b> (en bêta), Exalté auprès de l'<a href="reputations.html">Autorité commerciale d'Azeroth</a> (Alliance) ou du Ravitaillement et logistique de Durotar (Horde), niveau 60 et monte rapide.</p></div></article>
  <article class="mt-card"><div><h3>Rênes d'ours spectral</h3>
    <p>Récompense du parcours <a href="legacy.html">Héritage</a> (55 points d'Héritage en bêta). Liée au compte comme les autres.</p></div></article>
  <article class="mt-card a"><div><h3>Rênes de sabre-de-givre de Berceau-de-l'Hiver</h3>
    <p>Alliance seulement : Exalté auprès des <b>Éleveurs de sabres-d'hiver</b> (Rivern Frostwind, Berceau-de-l'Hiver, <span class="xy">49.9, 9.8</span>). Une longue réputation à base de quêtes répétables.</p></div></article>
  <article class="mt-card"><div><h3>Nouvelles couleurs</h3>
    <p>Le jeu contient des montures inédites dont l'obtention n'est pas encore connue : <b>Rênes de sabre-de-l'aube rayé</b>, <b>Kodo blanc</b>, <b>Kodo lavande</b>, <b>Cheval squelette vert, sombre, violet et noir</b>, <b>Cheval de guerre squelette ocre</b>. Deux montures sont aussi liées aux éditions du jeu.</p></div></article>
</div>

<div class="sec-title"><h2>JcJ, donjons et raids</h2></div>
<div class="article">
  <h3>Montures de guerre (JcJ)</h3>
  <p>Au <b>rang 11</b> du <a href="pvp.html">système d'honneur</a> : <b>Bride de palefroi de guerre noir</b>, <b>Rênes de tigre de guerre noir</b>, <b>Trotteur de bataille noir</b> et <b>Bélier de guerre noir</b> côté Alliance ; <b>Cor du loup de guerre noir</b>, <b>Sifflet du raptor de guerre noir</b>, <b>Kodo de guerre noir</b> et <b>Cheval de guerre squelette rouge</b> côté Horde.</p>
  <p>Dans la vallée d'Alterac, l'Exalté donne le <b>Destrier de bataille foudrepique</b> (Alliance) ou le <b>Cor du hurleur loup-de-givre</b> (Horde).</p>
  <h3>Butin de donjon et de raid</h3>
  <ul>
    <li><b>Rênes de destrier de la mort</b> : le baron Vaillefendre à <a href="donjons.html">Stratholme</a>, avec une faible chance.</li>
    <li><b>Raptor razzashi rapide</b> et le tigre zulien rapide : Zul'Gurub, qui n'ouvre pas au lancement.</li>
    <li>Les montures d'Ahn'Qiraj arriveront avec ce raid, plus tard.</li>
  </ul>
</div>

<div class="info" style="margin-top:20px">Prix et conditions venant de la bêta : ils peuvent changer à la sortie. Les coordonnées se lisent sur la carte du jeu ou avec <a href="addons.html">TomTom</a>, et les marchands des capitales sont sur notre <a href="carte.html">carte interactive</a>.</div>
<p class="small">Noms des montures d'après les données du client de WoW Forever, via le projet <a href="https://github.com/fitzforge/polestar" target="_blank" rel="noopener">Polestar</a> (CC BY 4.0). Informations complémentaires : <a href="news-montures.html">notre news sur les montures</a>, le guide de JudgeHype et le <a href="https://www.wowhead.com/forever/fr/guide/collections/mounts-locations-appearances" target="_blank" rel="noopener">guide des apparences de Wowhead</a>. Illustrations des montures : Mygale.</p>
</div>'''

tpl = open("legacy.html", encoding="utf-8").read()
head = tpl[:tpl.index("<main>")]
head = re.sub(r"<title>.*?</title>", "<title>Montures de WoW Forever : où les acheter et comment les obtenir – ForeverWoW</title>", head)
head = re.sub(r'name="description" content=".*?"', 'name="description" content="Toutes les montures de WoW Forever : montures de race et leurs marchands, trotteurs des trombes des Éolides, montures de classe, de réputation, de JcJ et de raid."', head)
tail = re.sub(r'<script src="js/heritage\.js[^"]*"></script>\n?', '', tpl[tpl.index("</main>"):])
open("montures.html", "w", encoding="utf-8").write(head + body + tail)

js = open("js/site.js", encoding="utf-8").read()
if "montures.html" not in js:
    js = js.replace('["reputations.html", "Réputations"]]', '["reputations.html", "Réputations"], ["montures.html", "Montures"]]', 1)
    js = js.replace('<a href="reputations.html">Réputations</a>', '<a href="reputations.html">Réputations</a><a href="montures.html">Montures</a>', 1)
    open("js/site.js", "w", encoding="utf-8").write(js)
print("ok")
