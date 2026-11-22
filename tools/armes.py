"""Génère armes.html : les armes utilisables par classe et les maîtres d'armes.
Sources : Warcraft Tavern et RankedBoost (guides WoW Forever, novembre 2026), données du jeu pour les compétences de départ.
Lancer : python3 tools/armes.py puis python3 tools/seo.py"""
import os, re, html
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")
e = html.escape
CL = [("warrior", "Guerrier"), ("paladin", "Paladin"), ("hunter", "Chasseur"), ("rogue", "Voleur"), ("priest", "Prêtre"),
      ("shaman", "Chaman"), ("mage", "Mage"), ("warlock", "Démoniste"), ("druid", "Druide")]
# Y = oui, N = non, ? = à confirmer ; ordre des colonnes = CL
ARMES = [
 ("Une main", [
  ("Dagues",              "YNYYYYYYY"),
  ("Épées à une main",    "YYYYNNYYN"),
  ("Haches à une main",   "YYYYNYNNN"),
  ("Masses à une main",   "YYNYYYNNY"),
  ("Armes de pugilat",    "YNYYNYNNY"),
 ]),
 ("Deux mains", [
  ("Épées à deux mains",  "YYYNNNNNN"),
  ("Haches à deux mains", "YYYNNYNNN"),
  ("Masses à deux mains", "YYNNNYNNY"),
  ("Armes d'hast",        "YYYNNNNN?"),
  ("Bâtons",              "YNYNYYYYY"),
 ]),
 ("Distance", [
  ("Arcs",                "YNYYNNNNN"),
  ("Arbalètes",           "YNYYNNNNN"),
  ("Armes à feu",         "YNYYNNNNN"),
  ("Armes de jet",        "YNYYNNNNN"),
  ("Baguettes",           "NNNNYNYYN"),
 ]),
 ("Défense et style", [
  ("Bouclier",            "YYNNNYNNN"),
  ("Ambidextrie (deux armes)", "YNYYN?NNN"),
 ]),
]
NOTE = {("Haches à une main", "rogue"): "Nouveau dans Forever",
        ("Haches à deux mains", "shaman"): "Acquis de base",
        ("Masses à deux mains", "shaman"): "Acquis de base",
        ("Armes d'hast", "druid"): "Annoncé, à confirmer",
        ("Ambidextrie (deux armes)", "warrior"): "Niveau 20",
        ("Ambidextrie (deux armes)", "hunter"): "Niveau 20",
        ("Ambidextrie (deux armes)", "rogue"): "Niveau 10",
        ("Ambidextrie (deux armes)", "shaman"): "À confirmer"}
CELL = {"Y": ('<td class="aw-y" title="Utilisable">✓</td>'), "N": '<td class="aw-n" title="Non">–</td>', "?": '<td class="aw-q" title="À confirmer">?</td>'}

head = "".join(f'<th><a href="classes.html#{c}"><img src="images/icons/class_{c}.jpg" alt="" width="28" height="28"><span>{n}</span></a></th>' for c, n in CL)
rows = ""
for grp, lst in ARMES:
    rows += f'<tr class="aw-g"><th colspan="{len(CL)+1}">{e(grp)}</th></tr>'
    for nom, v in lst:
        tds = ""
        for (c, _), x in zip(CL, v):
            n = NOTE.get((nom, c))
            td = CELL[x]
            if n: td = td.replace("</td>", f'<small>{e(n)}</small></td>')
            tds += td
        rows += f'<tr><th class="rname">{e(nom)}</th>{tds}</tr>'

TR = [("Alliance", "Hurlevent", "Woo Ping", "Arsenal de Weller, quartier commerçant", "63.8, 69.0", "Dagues, épées à une et deux mains, armes d'hast, bâtons, arbalètes"),
      ("Alliance", "Forgefer", "Buliwyf Stonehand", "Quartier militaire, même boutique que Bixi", "vers 62, 89", "Haches et masses à une et deux mains, armes de pugilat, armes à feu"),
      ("Alliance", "Forgefer", "Bixi Wobblebonk", "Quartier militaire", "62.2, 89.6", "Dagues, arbalètes, armes de jet"),
      ("Alliance", "Darnassus", "Ilyenia Moonfire", "Terrasse des guerriers", "57.6, 46.7", "Dagues, armes de pugilat, bâtons, arcs, armes de jet"),
      ("Horde", "Orgrimmar", "Sayoc", "Vallée de l'Honneur", "81.5, 19.6", "Dagues, armes de pugilat, haches à une et deux mains, bâtons, arcs, armes de jet"),
      ("Horde", "Orgrimmar", "Hanashi", "Vallée de l'Honneur, même boutique que Sayoc", "81.5, 19.6", "Haches à une et deux mains, bâtons, arcs, armes de jet"),
      ("Horde", "Les Pitons-du-Tonnerre", "Ansekhwa", "Bas de la mesa", "40.9, 62.7", "Masses à une et deux mains, bâtons, armes à feu"),
      ("Horde", "Fossoyeuse", "Archibald", "Quartier de la Guerre", "57.3, 32.8", "Dagues, épées à une et deux mains, armes d'hast, arbalètes")]
trs = "".join(f'<tr><td><span class="race {"a" if f == "Alliance" else "h"}">{f}</span></td><td>{e(v)}</td><td><b>{e(n)}</b><br><small>{e(l)}</small></td><td class="xy">{x}</td><td>{e(t)}</td></tr>' for f, v, n, l, x, t in TR)

body = f'''<main><div class="wrap">
<div class="crumbs"><a href="index.html">News</a> › <a href="classes.html">Classes</a> › Armes par classe</div>
<h1 class="page-title">Armes utilisables par classe</h1>
<p class="page-lead">Quelles armes chaque classe peut porter dans WoW Forever, et où apprendre celles qui te manquent. Forever apporte quelques nouveautés par rapport au jeu d'origine : haches pour le voleur, armes à deux mains de base pour le chaman.</p>
<p class="stamp auto"></p>
<div class="table-wrap rc"><table class="rtable aw"><thead><tr><th></th>{head}</tr></thead><tbody>{rows}</tbody></table></div>
<p class="small">✓ utilisable · – impossible · ? pas encore confirmé. Le bouclier et l'ambidextrie ne sont pas des armes, mais ils comptent dans le choix de ton équipement.</p>
<div class="article" style="margin-top:18px">
<h2>Comment ça marche</h2>
<ul><li>Chaque personnage commence avec <b>quelques armes</b>, selon sa classe et parfois sa race. Par exemple, un chasseur nain ou tauren débute avec les armes à feu, un chasseur humain, orc, elfe de la nuit ou troll avec les arcs.</li>
<li>Pour porter un autre type d'arme, il faut l'<b>apprendre chez un maître d'armes</b> : <b>10 pièces d'argent</b> par arme, <b>1 pièce d'or</b> pour les armes d'hast, à partir du niveau 20.</li>
<li>Une arme apprise commence à <b>1 en compétence</b> : tes coups ratent souvent au début. La compétence monte en frappant des monstres avec cette arme, jusqu'à 5 points par niveau de personnage.</li>
<li>Dans Forever, <b>aucune race n'a de bonus d'arme</b> : les humains ont à la place Impitoyable, +1 % de chances de critique avec toutes les armes.</li>
<li>Les <b>baguettes</b> sont acquises dès le départ pour le prêtre, le mage et le démoniste. Le druide a aussi le <b>combat farouche</b>, qui monte en forme d'ours et de félin.</li></ul>
</div>
<div class="sec-title"><h2>Les maîtres d'armes</h2></div>
<div class="table-wrap"><table class="rtable aw-tr"><thead><tr><th>Faction</th><th>Ville</th><th>Maître d'armes</th><th>Position</th><th>Enseigne</th></tr></thead><tbody>{trs}</tbody></table></div>
<p class="small">Un maître de l'autre faction ne t'enseignera rien. On ne sait pas encore où le voleur apprend les haches à une main, ni où le chasseur apprend les dagues : si tu as la réponse en jeu, <a href="contact.html">dis-le-nous</a>.</p>
<div class="info">Pour choisir ton arme selon ta spécialisation, vois nos <a href="guides.html">guides de spé</a> et les <a href="classes.html">fiches de classe</a>.</div>
<p class="small">Sources : <a href="https://www.warcrafttavern.com/forever/guides/weapon-trainers/" target="_blank" rel="noopener">Warcraft Tavern</a> et <a href="https://rankedboost.com/world-of-warcraft/forever/weapon-trainers/" target="_blank" rel="noopener">RankedBoost</a> (novembre 2026), données du jeu pour les compétences de départ.</p>
</div></main>'''

tpl = open("a-propos.html", encoding="utf-8").read()
h = tpl[:tpl.index("<main>")]
h = re.sub(r"<title>.*?</title>", "<title>Armes utilisables par classe dans WoW Forever – ForeverWoW</title>", h)
h = re.sub(r'name="description" content=".*?"', 'name="description" content="Quelles armes chaque classe peut utiliser dans WoW Forever (épées, haches, masses, dagues, bâtons, arcs, armes d&#x27;hast…) et où les apprendre : tous les maîtres d&#x27;armes avec leurs positions."', h)
t = tpl[tpl.index("</main>") + len("</main>"):]
open("armes.html", "w", encoding="utf-8").write(h + body + t)
print("ok")
