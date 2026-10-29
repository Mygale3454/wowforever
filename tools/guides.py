import json, re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")
B = json.load(open("tools/builds.json"))

STAT = {"Hit":"Toucher","Armor":"Armure","Weapon Damage":"Dégâts de l'arme","Agility":"Agilité","Bonus Healing":"Bonus aux soins",
 "Defense":"Défense","Spell Power (Shadow)":"Puissance des sorts d'ombre","Intellect":"Intelligence","Spell Power":"Puissance des sorts",
 "Attack Power":"Puissance d'attaque","Weapon DPS":"DPS de l'arme","Critical Strike":"Coup critique","Crit":"Coup critique",
 "Expertise":"Expertise","Strength":"Force","Spirit":"Esprit","Haste":"Hâte","Spell Power (Fire)":"Puissance des sorts de feu",
 "Block":"Blocage","Stamina":"Endurance","Healing Power":"Puissance des soins","MP5":"Mana toutes les 5 s"}
RACE = {"troll":"Troll","undead":"Mort-vivant","tauren":"Tauren","gnome":"Gnome","dwarf":"Nain","human":"Humain","night-elf":"Elfe de la nuit","orc":"Orc"}
RACEID = {"troll":"troll","undead":"mortvivant","tauren":"tauren","gnome":"gnome","dwarf":"nain","human":"humain","night-elf":"elfe","orc":"orc"}
CLASS = [("warrior","Guerrier","#C69B6D"),("paladin","Paladin","#D9619C"),("hunter","Chasseur","#7FAE3E"),("rogue","Voleur","#D4B82A"),
 ("priest","Prêtre","#9A9A9A"),("shaman","Chaman","#0070DD"),("mage","Mage","#2BA9CC"),("warlock","Démoniste","#7072D6"),("druid","Druide","#E86E08")]

# spec : (nom FR, rôle, description, [points forts], [points faibles])
G = {
"warrior-arms":("Armes","Dégâts en mêlée","Le guerrier à l'arme à deux mains : de gros coups, Frappe mortelle pour réduire les soins de la cible et beaucoup de contrôle en JcJ. Très apprécié pour monter de niveau grâce à ses dégâts réguliers.",
 ["Frappe mortelle, redoutable en JcJ","Bon pour le leveling en solo","Simple à prendre en main"],["Dépend beaucoup de son arme","Peu de soins personnels entre deux combats"]),
"warrior-fury":("Fureur","Dégâts en mêlée","Le guerrier aux deux armes : un flot continu de coups alimenté par la rage. C'est l'une des spécialisations de dégâts les plus fortes en donjon et en raid, une fois bien équipé.",
 ["Dégâts très élevés en groupe","Excellent avec un bon équipement","Très recherché en raid"],["Fragile en solo","Exigeant sur le placement et la gestion de la menace"]),
"warrior-protection":("Protection","Tank","Le tank de référence : bouclier au bras, Heurt de bouclier pour générer énormément de menace et de nombreuses capacités défensives. Le rôle le plus demandé en donjon.",
 ["Menace très élevée","Groupes trouvés en quelques secondes","Grande résistance"],["Dégâts faibles en solo","Coûteux en réparations au début"]),
"paladin-holy":("Sacré","Soins","Le soigneur en plaque : des soins directs puissants sur une seule cible, parfaits pour garder le tank en vie. Robuste et difficile à tuer, il encaisse là où d'autres soigneurs tomberaient.",
 ["Soins puissants sur le tank","Très résistant grâce à la plaque","Bénédictions utiles au groupe"],["Peu de soins de groupe","Lent pour monter de niveau en solo"]),
"paladin-protection":("Protection","Tank","Un tank qui excelle face à plusieurs ennemis grâce à ses dégâts sacrés de zone et au Bouclier sacré. Il régénère facilement son mana et tient très bien les groupes de monstres.",
 ["Excellent contre plusieurs ennemis","Très solide","Autonome en mana"],["Moins d'outils pour reprendre la menace d'urgence","Dépend de son équipement de sorts"]),
"paladin-retribution":("Vindicte","Dégâts en mêlée","Le paladin offensif à l'arme à deux mains : sceaux et jugements pour frapper fort, avec la possibilité de soigner en dépannage. Un hybride robuste, très agréable pour monter de niveau.",
 ["Robuste et polyvalent","Peut soigner en dépannage","Agréable en solo"],["Dégâts un cran en dessous des meilleures spés","Rotation peu variée"]),
"hunter-beast-mastery":("Maîtrise des bêtes","Dégâts à distance","Le chasseur et son familier ne font qu'un : la bête encaisse les coups pendant que tu attaques à distance. C'est la façon la plus simple et la plus efficace de monter un personnage.",
 ["Le meilleur pour le leveling","Familier très résistant","Très autonome"],["Dégâts moins élevés en raid","Dépend de la santé du familier"]),
"hunter-marksmanship":("Précision","Dégâts à distance","Le tireur d'élite : de gros tirs à distance et une aura qui renforce la puissance d'attaque à distance du groupe. Un classique apprécié pour son style et son efficacité.",
 ["Gros dégâts à distance","Aura utile au groupe","Très mobile"],["Moins de survie que la Maîtrise des bêtes","Vulnérable au corps à corps"]),
"hunter-survival":("Survie","Dégâts à distance","Pièges, contrôle et réflexes : le chasseur de survie brille en donjon et en JcJ grâce à ses outils de contrôle et à ses dégâts réguliers. Une spé très solide dans Forever.",
 ["Beaucoup de contrôle","Très efficace en donjon","Bonne survie"],["Plus technique à jouer","Demande de bien gérer ses pièges"]),
"rogue-assassination":("Assassinat","Dégâts en mêlée","Poisons et coups critiques : l'assassin enchaîne les points de combo pour libérer des finisseurs dévastateurs. C'est la spécialisation de voleur la plus forte en donjon.",
 ["Très gros dégâts sur une cible","Poisons puissants","Excellent en donjon"],["Peu de dégâts de zone","Fragile s'il est ciblé"]),
"rogue-combat":("Combat","Dégâts en mêlée","Le bretteur : des dégâts constants avec deux armes, simples à jouer, et des capacités pour frapper encore plus fort pendant de courtes périodes. Idéal pour monter de niveau.",
 ["Dégâts réguliers","Simple à jouer","Bon pour le leveling"],["Moins de contrôle que les autres spés","Peu de dégâts de zone"]),
"rogue-subtlety":("Finesse","Dégâts en mêlée","Le maître de l'ombre : ouvertures depuis le camouflage, contrôle et disparitions. Une spécialisation taillée pour le JcJ, plus en retrait en donjon.",
 ["Redoutable en JcJ","Beaucoup de contrôle","Très mobile"],["Plus faible en donjon","Demande de l'expérience"]),
"priest-discipline":("Discipline","Soins","Le prêtre protecteur : boucliers, prévention des dégâts et nouveaux sorts comme Penance. Très efficace en donjon pour empêcher les dégâts avant même qu'ils n'arrivent.",
 ["Boucliers très puissants","Excellent en donjon","Bonne gestion du mana"],["Moins de soins de groupe que le Sacré","Demande d'anticiper"]),
"priest-holy":("Sacré","Soins","Le soigneur de groupe par excellence : soins de zone, Prière de soins et nouveaux sorts comme Prayer of Mending ou Binding Heal. L'un des meilleurs soigneurs de Forever.",
 ["Soins de groupe excellents","Très polyvalent","Recherché en raid"],["Fragile en solo","Lent pour monter de niveau"]),
"priest-shadow":("Ombre","Dégâts à distance","Le prêtre de l'ombre : dégâts sur la durée, Fouet mental et forme d'ombre. Il rend du mana et de la vie à son groupe et reste très agréable pour progresser seul.",
 ["Bon en solo","Soutien en mana et en vie au groupe","Solide en JcJ"],["Moins de dégâts immédiats","Dépend de la durée des combats"]),
"shaman-elemental":("Élémentaire","Dégâts à distance","Le chaman des éclairs : Éclair, Chaîne d'éclairs et Lava Burst, avec de très gros coups critiques. Des dégâts de sorts élevés et des totems utiles à tout le groupe.",
 ["Gros dégâts de sorts","Totems utiles au groupe","Peut soigner en dépannage"],["Gourmand en mana","Peu mobile pendant les incantations"]),
"shaman-enhancement":("Amélioration","Dégâts en mêlée","Le chaman au corps à corps : Frappe-tempête, armes enchantées et Maelstrom Weapon pour lancer des sorts instantanés. Des dégâts explosifs et un style très apprécié.",
 ["Dégâts explosifs","Très populaire","Polyvalent"],["Dépend de la chance (Windfury, critiques)","Gourmand en mana en solo"]),
"shaman-restoration":("Restauration","Soins","Le soigneur aux totems : Salve de guérison qui rebondit sur le groupe, Riptide et des totems qui soutiennent tout le monde. Le soigneur de groupe idéal.",
 ["Soins de groupe excellents","Totems précieux","Très recherché"],["Moins efficace sur une seule cible","Peu de dégâts en solo"]),
"mage-arcane":("Arcanes","Dégâts à distance","Le mage des arcanes : le Pouvoir des arcanes pour des phases de dégâts énormes et une excellente gestion du mana. Souvent classé comme la spé de dégâts la plus forte.",
 ["Dégâts parmi les plus élevés","Phases de burst énormes","Très bonne gestion du mana"],["Fragile","Demande de bien gérer ses temps de recharge"]),
"mage-fire":("Feu","Dégâts à distance","Le pyromancien : boules de feu, gros coups critiques et brûlures sur la durée. Très puissant en raid une fois équipé, avec des dégâts de zone impressionnants.",
 ["Gros coups critiques","Puissant en raid","Bons dégâts de zone"],["Certains boss résistent au feu","Fragile"]),
"mage-frost":("Givre","Dégâts à distance","Le mage du givre : ralentissements, immobilisations et sécurité. La référence pour monter de niveau en tirant des groupes de monstres, et excellent en JcJ.",
 ["Le plus sûr pour le leveling","Beaucoup de contrôle","Excellent en JcJ"],["Moins de dégâts en raid","Rotation répétitive"]),
"warlock-affliction":("Affliction","Dégâts à distance","Le démoniste des malédictions : dégâts sur la durée sur plusieurs cibles et une excellente survie grâce au drain de vie. Parfait pour progresser seul.",
 ["Excellente survie en solo","Dégâts sur plusieurs cibles","Bon en JcJ"],["Démarrage lent sur un combat court","Gestion des sorts sur la durée"]),
"warlock-demonology":("Démonologie","Dégâts à distance","Le maître des démons : des familiers renforcés qui encaissent et frappent. Une spécialisation solide en donjon et rassurante pour progresser.",
 ["Familiers puissants","Très résistant","Solide en donjon"],["Dégâts moins élevés en burst","Dépend du familier"]),
"warlock-destruction":("Destruction","Dégâts à distance","Le démoniste du feu : Trait de l'ombre, Conflagration et gros coups critiques. Des dégâts immédiats élevés, efficaces en JcJ comme en raid.",
 ["Gros dégâts immédiats","Efficace en JcJ","Puissant en raid"],["Moins de survie que l'Affliction","Gourmand en mana"]),
"druid-balance":("Équilibre","Dégâts à distance","Le druide sélénien : Courroux et Feu stellaire, et une aura qui augmente les critiques de tout le groupe. Un lanceur de sorts capable de dépanner en tank ou en soins.",
 ["Aura de critique pour le groupe","Peut dépanner dans un autre rôle","Bons dégâts de sorts"],["Peu de contrôle et pas d'interruption","Peu mobile pendant les incantations"]),
"druid-feral-combat":("Combat farouche","Tank ou dégâts en mêlée","Le druide métamorphe : ours pour tanker, félin pour frapper. Une spé très souple qui peut changer de rôle d'un combat à l'autre, avec le même équipement.",
 ["Tank et dégâts avec un seul build","Très mobile en forme de voyage","Polyvalent"],["Moins spécialisé que les vrais tanks","Gestion des formes"]),
"druid-restoration":("Restauration","Soins","Le druide soigneur : soins sur la durée, Croissance sauvage pour tout le groupe et la possibilité de ressusciter en combat. Un excellent soigneur de groupe.",
 ["Soins de groupe sur la durée","Très mobile","Résurrection en combat"],["Moins de soins immédiats","Demande d'anticiper"]),
}

def card(key):
    cls = key.split("-")[0]
    nom, role, desc, plus, moins = G[key]; b = B[key]
    stats = " › ".join(STAT.get(s, s) for s in b["stats"])
    races = " · ".join(f'<a href="races.html#{RACEID[r]}"><span class="race {"a" if f=="alliance" else "h"}">{RACE[r]}</span></a>' for f, r in b["races"].items() if r)
    key_t = ", ".join(b["key"][:6])
    return f'''<article class="sg" id="{key}">
  <div class="sg-h"><h3>{nom}</h3><span class="role">{role}</span></div>
  <p>{desc}</p>
  <div class="sg-cols">
    <div><h4>Points forts</h4><ul>{"".join(f"<li>{x}</li>" for x in plus)}</ul></div>
    <div><h4>Points faibles</h4><ul>{"".join(f"<li>{x}</li>" for x in moins)}</ul></div>
  </div>
  <h4>Build conseillé pour le niveau 60 (donjons et raids)</h4>
  <p class="sg-build"><b>{b["split"]}</b> · talents clés : {key_t}{" · <i>build adapté à la dernière bêta</i>" if b.get("adapted") else ""}</p>
  <a class="btn-link" href="talents.html#{b["code"]}">Ouvrir ce build dans le calculateur ↗</a>
  <h4>Priorité des statistiques</h4><p class="sg-stats">{stats}</p>
  <h4>Races conseillées</h4><p>{races}</p>
</article>'''

sections = ""
for cid, cname, col in CLASS:
    keys = [k for k in G if k.startswith(cid + "-")]
    sections += f'''<section class="sgc" id="{cid}" style="--c:{col}">
  <div class="sgc-head"><img src="images/icons/class_{cid}.jpg" alt=""><h2>{cname}</h2><a href="classes.html">Fiche de la classe</a></div>
  <div class="sgs">{"".join(card(k) for k in keys)}</div>
</section>'''
jumps = "".join(f'<a class="jump" href="#{c}" style="--c:{col}"><img src="images/icons/class_{c}.jpg" alt="" style="width:18px;height:18px;border-radius:4px;vertical-align:-3px;margin-right:4px">{n}</a>' for c, n, col in CLASS)

body = f'''<main><div class="wrap">
<div class="crumbs"><a href="index.html">News</a> › Classes / Races › Guides de spé</div>
<h1 class="page-title">Guides des spécialisations</h1>
<p class="page-lead">Les 27 spécialisations de WoW Forever en un coup d'œil : rôle, points forts et faibles, build de talents pour le niveau 60, priorité des statistiques et races conseillées. Chaque build s'ouvre en un clic dans notre calculateur de talents.</p>
<div class="info">Ces conseils viennent de la bêta : les valeurs exactes ne seront connues qu'au niveau 60, après la sortie. Prends-les comme une base solide, à ajuster selon ton style de jeu.</div>
<nav class="jumps" style="margin-top:16px">{jumps}</nav>
{sections}
<p class="small">Répartitions de talents, priorités de statistiques et races d'après le projet <a href="https://snibi.github.io/forever-meta/" target="_blank" rel="noopener">Forever Meta</a>, qui s'appuie notamment sur les guides d'Icy Veins et les présentations de Blizzard. Les builds ont été vérifiés et, si besoin, complétés pour respecter les règles de la dernière bêta (build 70291). Noms des talents en anglais.</p>
</div>'''

tpl = open("legacy.html").read()
head = tpl[:tpl.index("<main>")]
head = re.sub(r"<title>.*?</title>", "<title>Guides des spécialisations – wowforever</title>", head)
head = re.sub(r'name="description" content=".*?"', 'name="description" content="Guides des 27 spécialisations de WoW Forever : build de talents, priorité des statistiques, races conseillées, points forts et faibles."', head)
tail = re.sub(r'<script src="js/heritage\.js[^"]*"></script>\n?', '', tpl[tpl.index("</main>"):])
open("guides.html", "w").write(head + body + tail)

js = open("js/site.js").read()
js = js.replace('[["classes.html", "Classes"], ["races.html", "Races"]]', '[["classes.html", "Classes"], ["guides.html", "Guides de spé"], ["races.html", "Races"]]')
open("js/site.js", "w").write(js)

c = open("classes.html").read()
MAP = {"guerrier":"warrior","paladin":"paladin","chasseur":"hunter","voleur":"rogue","pretre":"priest","chaman":"shaman","mage":"mage","demoniste":"warlock","druide":"druid"}
for fr, en in MAP.items():
    old = f'<a class="btn-link" href="talents.html#{en}">Ouvrir l\'arbre de talents ↗</a>'
    if old in c and f'guides.html#{en}' not in c:
        c = c.replace(old, old + f'\n    <a class="btn-link" href="guides.html#{en}">Guides des spécialisations ↗</a>')
open("classes.html", "w").write(c)

n = open("js/news.js").read()
if "guides.html" not in n:
    n = n.replace("const NEWS = [\n", '''const NEWS = [
  { date: "2026-10-29", type: "guide", lien: "guides.html", img: "images/classes.jpg",
    titre: "Les guides des 27 spécialisations sont en ligne",
    texte: "Rôle, points forts et faibles, build de talents à ouvrir en un clic dans le calculateur, priorité des statistiques et races conseillées." },
''', 1)
open("js/news.js", "w").write(n)
print("ok", len(G))
