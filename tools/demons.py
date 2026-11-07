"""Génère familiers-demoniste.html (guide des démons du démoniste).
Chiffres des sorts (rangs, niveaux, prix des grimoires, mana) : guide des familiers de JudgeHype (30/10/2026), cité en bas de page.
Talents : js/talents-data.js (patch en vigueur). Textes rédigés pour ForeverWoW.
Lancer : python3 tools/demons.py puis python3 tools/seo.py"""
import re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")

def table(cols, rows):
    th = "".join(f"<th>{c}</th>" for c in cols)
    tr = "".join("<tr>" + "".join(f"<td>{v}</td>" for v in r) + "</tr>" for r in rows)
    return f'<div class="table-wrap dm-t"><table class="rtable"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'

def sort(nom, desc, cols=None, rows=None):
    return f'<div class="dm-s"><h4>{nom}</h4><p>{desc}</p>{table(cols, rows) if cols else ""}</div>'

def demon(id_, nom, en, niv, role, quand, sorts, note=""):
    return f'''<section class="dm" id="{id_}">
  <div class="dm-h"><h2>{nom} <span class="dm-en">{en}</span></h2><span class="dm-niv">{niv}</span></div>
  <p class="dm-role">{role}</p>
  <div class="dm-when"><b>Quand le sortir ?</b> {quand}</div>
  {"".join(sorts)}
  {f'<p class="small">{note}</p>' if note else ''}
</section>'''

DEMONS = [
demon("diablotin", "Diablotin", "Imp", "Niveau 1 · sans fragment d'âme",
  "Petit lanceur de feu fragile, mais le seul démon qui ne coûte pas de fragment d'âme. Son Pacte de sang donne de l'Endurance à tout le groupe.",
  "Quand tu veux économiser tes fragments, en groupe pour le bonus d'Endurance, et en JcJ où il reste en retrait à distance.",
  [sort("Éclair de feu", "Son attaque principale, à distance (30 m, incantation 2 s).", ["Rang", "Niveau", "Grimoire", "Mana", "Dégâts"],
        [[1, 1, "inclus", 10, "4-5"], [2, 8, "1 pa", 20, "7-9"], [3, 18, "15 pa", 35, "13-15"], [4, 28, "50 pa", 50, "18-19"], [5, 38, "1 po", 70, "26-28"], [6, 48, "1 po 40 pa", 95, "36-39"], [7, 58, "2 po 40 pa", 115, "45-50"]]),
   sort("Pacte de sang", "Aura d'Endurance pour le groupe dans un rayon de 20 m.", ["Rang", "Niveau", "Grimoire", "Endurance"],
        [[1, 4, "1 pa", "+4"], [2, 14, "9 pa", "+12"], [3, 26, "40 pa", "+25"], [4, 38, "1 po", "+39"], [5, 50, "1 po 50 pa", "+54"]]),
   sort("Bouclier de feu", "À poser sur un allié (pas sur toi) : chaque attaque de mêlée qu'il reçoit brûle l'attaquant. Dure 3 min, portée 30 m. Pratique sur le tank ou sur le marcheur du Vide.", ["Rang", "Niveau", "Grimoire", "Mana", "Dégâts par coup"],
        [[1, 14, "9 pa", 60, 5], [2, 24, "30 pa", 90, 7], [3, 34, "80 pa", 115, 9], [4, 44, "1 po 20 pa", 140, 11], [5, 54, "2 po", 165, 13]]),
   sort("Changement de phase", "Niveau 12. Le diablotin passe dans une autre dimension : on ne peut plus l'attaquer tant qu'il n'attaque pas lui-même. 10 s entre deux utilisations. À activer en JcJ pour qu'il survive.")]),
demon("marcheur", "Marcheur du Vide", "Voidwalker", "Vers le niveau 10 · 1 fragment d'âme",
  "Le tank du démoniste : beaucoup de points de vie, une bonne armure et des provocations pour garder les monstres sur lui. Il récupère vite entre deux combats.",
  "Presque tout le temps en solo pendant la montée de niveau : il encaisse pendant que tes sorts sur la durée font le travail.",
  [sort("Tourment", "Provocation sur une cible (5 m, instantané, 5 s entre deux utilisations).", ["Rang", "Niveau", "Grimoire", "Mana"],
        [[1, 10, "inclus", 20], [2, 20, "20 pa", 40], [3, 30, "60 pa", 65], [4, 40, "1 po 10 pa", 90], [5, 50, "1 po 50 pa", 115], [6, 60, "2 po 60 pa", 145]]),
   sort("Consumer les ombres", "Il se soigne sur 10 s, hors combat uniquement.", ["Rang", "Niveau", "Grimoire", "Mana", "PV rendus"],
        [[1, 18, "15 pa", 85, 325], [2, 26, "40 pa", 150, 576], [3, 34, "80 pa", 215, 839], [4, 42, "1 po 10 pa", 285, "1 130"], [5, 50, "1 po 50 pa", 380, "1 528"], [6, 58, "2 po 40 pa", 480, "1 969"]]),
   sort("Sacrifice", "Le marcheur se sacrifie et te protège avec un bouclier pendant 30 s ; tant qu'il tient, les dégâts n'interrompent pas tes sorts. <b>Nouveau dans Forever :</b> le bouclier profite aussi de 10 % de ton bonus aux soins.", ["Rang", "Niveau", "Grimoire", "Absorption"],
        [[1, 16, "12 pa", 319], [2, 24, "30 pa", 529], [3, 32, "70 pa", 793], [4, 40, "1 po 10 pa", "1 123"], [5, 48, "1 po 40 pa", "1 503"], [6, 56, "2 po 20 pa", "1 943"]]),
   sort("Souffrance", "Provocation de zone (10 m), 2 min de recharge : pour récupérer plusieurs monstres d'un coup.", ["Rang", "Niveau", "Grimoire", "Mana"],
        [[1, 24, "30 pa", 150], [2, 36, "90 pa", 300], [3, 48, "1 po 40 pa", 450], [4, 60, "2 po 60 pa", 600]])]),
demon("succube", "Succube et Incube", "Succubus / Incubus", "Vers le niveau 20 · 1 fragment d'âme",
  "Démon de mêlée qui frappe fort et contrôle les humanoïdes. <b>L'Incube est nouveau dans Forever</b> : c'est la version masculine, avec exactement les mêmes techniques. Il s'obtient par une quête de classe dès le niveau 20.",
  "En solo pour plus de dégâts, et en groupe pour neutraliser un humanoïde avec Séduction. En JcJ, Séduction est redoutable, mais de moins en moins efficace si on la relance sur le même joueur.",
  [sort("Fouet de la douleur", "Coup d'ombre au contact, 12 s de recharge.", ["Rang", "Niveau", "Grimoire", "Mana", "Dégâts"],
        [[1, 20, "inclus", 65, 16], [2, 28, "50 pa", 80, 22], [3, 36, "90 pa", 105, 30], [4, 44, "1 po 20 pa", 125, 36], [5, 52, "1 po 80 pa", 145, 43], [6, 60, "2 po 60 pa", 160, 50]]),
   sort("Baiser apaisant", "Réduit la menace de la cible envers le démon (4 s de recharge).", ["Rang", "Niveau", "Grimoire", "Mana"],
        [[1, 22, "25 pa", 30], [2, 34, "80 pa", 50], [3, 46, "1 po 30 pa", 75], [4, 58, "2 po 40 pa", 100]]),
   sort("Séduction", "Niveau 26 (grimoire 40 pa). Neutralise un humanoïde jusqu'à 15 s ; le moindre dégât rompt l'effet. Incantation 1,5 s, portée 30 m. Idéal pour se faire un soin ou un bandage en paix."),
   sort("Invisibilité inférieure", "Niveau 32 (grimoire 70 pa, 100 mana). Le démon devient invisible pendant 5 min : pour approcher sans se faire repérer.")],
  'Quêtes de l\'Incube : <a href="classe-warlock-incubus-alliance.html">Alliance</a> · <a href="classe-warlock-incubus-horde.html">Horde</a>.'),
demon("chasseur", "Chasseur corrompu", "Felhunter", "Vers le niveau 30 · 1 fragment d'âme",
  "Le chasseur des lanceurs de sorts : il dévore la magie, coupe les sorts et réduit la puissance de ceux qui le frappent.",
  "Contre les lanceurs de sorts, en donjon pour retirer des malus au groupe, et surtout en JcJ.",
  [sort("Dévorer la magie", "Retire un effet magique néfaste d'un allié, ou un effet bénéfique d'un ennemi, et se soigne au passage (portée 30 m, 8 s de recharge).", ["Rang", "Niveau", "Grimoire", "Mana", "PV rendus"],
        [[1, 30, "inclus", 100, 258], [2, 38, "1 po", 130, 348], [3, 46, "1 po 30 pa", 170, 472], [4, 54, "2 po", 215, 619]]),
   sort("Corruption sanguine", "Pendant 60 s, chaque ennemi qui le frappe en mêlée perd de la puissance d'attaque pendant 10 s (cumulable 5 fois).", ["Rang", "Niveau", "Grimoire", "Mana", "Puissance retirée"],
        [[1, 32, "70 pa", 75, -17], [2, 40, "1 po 10 pa", 105, -23], [3, 48, "1 po 40 pa", 135, -32], [4, 56, "2 po 20 pa", 170, -40]]),
   sort("Verrou magique", "Interrompt un sort, réduit la cible au silence 3 s et bloque cette école de magie un moment (portée 30 m, 30 s de recharge).", ["Rang", "Niveau", "Grimoire", "Mana", "Blocage"],
        [[1, 36, "90 pa", 120, "6 s"], [2, 52, "1 po 80 pa", 200, "8 s"]]),
   sort("Paranoïa", "Niveau 42. Le groupe repère mieux les ennemis camouflés (voleurs, druides en rôdeur).")],
  'Quêtes du chasseur corrompu : <a href="classe-warlock-felhunter-alliance.html">Alliance</a> · <a href="classe-warlock-felhunter-horde.html">Horde</a>.'),
demon("infernal", "Infernal", "Infernal", "Niveau 50 · sort Inferno + pierre infernale",
  "Un géant de pierre et de feu, temporaire. Le sort <b>Inferno</b> le fait tomber du ciel (extérieur uniquement) : 200 dégâts de feu et 2 s d'étourdissement autour du point d'impact, puis il se bat pour toi pendant 5 min, entouré d'une aura de feu.",
  "Pour un gros combat en extérieur, ou pour sauver une situation mal engagée. Une heure entre deux Inferno.",
  [], "Attention : une fois les 5 min écoulées, il se retourne contre toi. Utilise <b>Asservir démon</b> pour le reprendre en main ou éloigne-toi."),
demon("garde-funeste", "Garde funeste", "Doomguard", "Niveau 60 · Rituel de malédiction ou Plaie funeste",
  "Le démon le plus puissant, lui aussi temporaire : énormément de points de vie et une grosse armure. Il lance Pluie de feu, Dissipation de la magie, Faiblesse (ralentit et frappe moins vite) et Choc martial (étourdissement de zone).",
  "Pour les combats difficiles du niveau 60, en groupe.",
  [sort("Comment l'invoquer", "Deux façons : le <b>Rituel de malédiction</b>, avec quatre autres joueurs et une figurine démoniaque (l'un des participants est sacrifié), ou la malédiction <b>Plaie funeste</b> : si la cible meurt de ses dégâts (au bout d'une minute), un garde funeste peut apparaître. Ne marche pas sur les joueurs.")],
  "Comme l'infernal, il peut t'échapper : garde Asservir démon sous la main."),
]

TAL = [("Unholy Power", "+10 % de dégâts pour tous tes démons permanents."),
       ("Fel Vitality", "+15 % de vie et de mana pour tes démons, et +15 % de mana pour toi."),
       ("Improved Imp / Improved Voidwalker / Improved Sayaad / Improved Felhunter", "Renforcent les techniques de chaque démon (dégâts, soins, durée des contrôles, recharge du Verrou magique)."),
       ("Demonic Energies", "Tes sorts soignent ton démon (15 % des dégâts infligés), et Connexion lui donne aussi du mana."),
       ("Master Summoner et Fel Domination", "Invocations bien plus rapides et moins chères : vital en JcJ ou si ton démon meurt en combat."),
       ("Soul Link", "30 % des dégâts que tu subis sont encaissés par ton démon, et vous infligez tous les deux 3 % de dégâts en plus."),
       ("Demonic Knowledge", "Augmente tes dégâts des sorts et ceux de ton démon tant qu'il est invoqué."),
       ("Master Demonologist", "Un bonus pour toi et ton démon selon celui qui est sorti : +10 % de dégâts de feu (diablotin), -10 % de dégâts physiques subis (marcheur), +10 % de dégâts d'ombre (succube/incube), -10 % de dégâts magiques subis (chasseur)."),
       ("Demonic Sacrifice", "Sacrifie ton démon contre un bonus de 2 h : +15 % d'ombre (diablotin), régénération de mana (marcheur), +15 % de feu (succube/incube), régénération de vie (chasseur)."),
       ("Demonic Pact", "Talent final : ton Sacrifice démoniaque n'est plus annulé quand tu invoques un autre démon. Tu cumules le bonus du sacrifice et un démon actif.")]
tal = "".join(f"<li><b>{n}</b> : {d}</li>" for n, d in TAL)

CHOIX = [("Montée de niveau", "Marcheur du Vide", "marcheur"), ("Affliction en donjon", "Diablotin (Pacte de sang) ou succube", "diablotin"),
         ("Démonologie", "Succube ou chasseur corrompu, avec Soul Link", "succube"), ("Destruction", "Diablotin, ou Sacrifice démoniaque de la succube", "diablotin"),
         ("JcJ", "Chasseur corrompu (Verrou magique)", "chasseur"), ("Gros combat en extérieur", "Infernal", "infernal")]
choix = "".join(f'<tr><td><b>{a}</b></td><td><a href="#{h}">{b}</a></td></tr>' for a, b, h in CHOIX)
jumps = "".join(f'<a class="jump" href="#{i}">{n}</a>' for i, n in [("diablotin", "Diablotin"), ("marcheur", "Marcheur du Vide"), ("succube", "Succube / Incube"), ("chasseur", "Chasseur corrompu"), ("infernal", "Infernal"), ("garde-funeste", "Garde funeste"), ("talents", "Talents")])

body = f'''<main><div class="wrap">
<div class="crumbs"><a href="index.html">News</a> › <a href="classes.html">Classes</a> › Familiers du démoniste</div>
<h1 class="page-title"><img src="images/icons/class_warlock.jpg" alt="" class="dm-ic"> Les familiers du démoniste</h1>
<p class="page-lead">Diablotin, marcheur du Vide, succube, incube, chasseur corrompu, infernal et garde funeste : à quoi sert chaque démon, quand le sortir et ce que coûte chaque rang de ses techniques dans WoW Forever.</p>
<nav class="jumps">{jumps}</nav>

<div class="article">
  <h2>Quel démon choisir ?</h2>
  <div class="table-wrap dm-t"><table class="rtable"><thead><tr><th>Situation</th><th>Démon conseillé</th></tr></thead><tbody>{choix}</tbody></table></div>
  <ul>
    <li>Dans Forever, <b>tes démons profitent de tes caractéristiques</b> : mieux tu es équipé, plus ils sont forts.</li>
    <li>Les techniques s'achètent sous forme de <b>grimoires</b> chez le maître des démons, en général à côté de ton maître des démonistes. Les prix ci-dessous sont sans réduction de réputation. Depuis les notes de lancement, le prix des grimoires est déduit du coût d'entraînement du démoniste.</li>
    <li>Depuis les notes de lancement, chaque point d'Endurance donne <b>2 points de vie</b> à tes démons (7,5 auparavant) : ils sont moins résistants qu'en bêta. Le correctif du 6 novembre a ajouté environ <b>40 points de vie de base</b> au marcheur du Vide, et Blizzard prévoit de rendre les familiers plus solides (proches de Classic Era) avec l'équilibrage du 10 novembre.</li>
    <li>Les valeurs indiquées sont celles de base, sans talents ni équipement ; le niveau est celui où le rang devient disponible.</li>
  </ul>
</div>

{"".join(DEMONS)}

<section class="dm" id="talents">
  <div class="dm-h"><h2>Les talents qui renforcent tes démons</h2><span class="dm-niv">Arbre Démonologie</span></div>
  <p class="dm-role">Noms des talents en anglais, comme dans notre <a href="talents.html#warlock">calculateur</a>. Les builds conseillés sont dans les <a href="guides.html#warlock">guides de spé</a>.</p>
  <ul class="dm-tal">{tal}</ul>
</section>

<p class="small">Chiffres des techniques (rangs, niveaux, prix des grimoires, mana) d'après le guide des familiers du démoniste de <a href="https://wowforever.judgehype.com/article/familiers-du-demoniste-sur-wow-forever/" target="_blank" rel="noopener">JudgeHype</a> (30 octobre 2026). Talents d'après les données du jeu. Textes : ForeverWoW.</p>
</div>'''

tpl = open("legacy.html", encoding="utf-8").read()
head = tpl[:tpl.index("<main>")]
head = re.sub(r"<title>.*?</title>", "<title>Familiers du démoniste dans WoW Forever : tous les démons et leurs sorts – ForeverWoW</title>", head)
head = re.sub(r'name="description" content=".*?"', 'name="description" content="Guide des démons du démoniste dans WoW Forever : diablotin, marcheur du Vide, succube, incube, chasseur corrompu, infernal, garde funeste, leurs sorts, les grimoires et les talents."', head)
tail = re.sub(r'<script src="js/heritage\.js[^"]*"></script>\n?', '', tpl[tpl.index("</main>"):])
open("familiers-demoniste.html", "w", encoding="utf-8").write(head + body + tail)
print("ok")
