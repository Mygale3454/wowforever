"""Génère bis.html (meilleur équipement pré-raid niveau 60, par classe).
Listes d'objets d'après wow4ever.quest (BiS calculé, 4 novembre 2026), noms français et identifiants
d'après la base Factoruide (table l10n). Usage : python3 tools/bis.py <f.sqlite de Factoruide>"""
import html, json, os, re, sqlite3, sys
ROOT = os.path.dirname(os.path.abspath(__file__)) + "/.."
os.chdir(ROOT); e = html.escape
DB = sqlite3.connect(sys.argv[1])

S = ["Tête", "Cou", "Épaules", "Dos", "Torse", "Poignets", "Mains", "Taille", "Jambes", "Pieds", "Doigt", "Doigt", "Bijou", "Bijou", "Main droite", "Main gauche", "À distance"]
# classe : (nom FR, couleur, image, spé, 17 objets [nom EN, source EN] dans l'ordre de S)
BIS = {
"warrior": ("Guerrier", "#C69B6D", "guerrier", "Dégâts (Fureur / Armes)", [
 ("Lionheart Helm", "Blacksmithing (295)"), ("Imperial Jewel", "Emperor Dagran Thaurissan, Blackrock Depths"), ("Shoulderplates of Dread", "Blacksmithing (225)"),
 ("Cape of the Black Baron", "Baron Rivendare, Stratholme"), ("Breastplate of Valor", "General Drakkisath, Upper Blackrock Spire"), ("Battleborn Armbraces", "Warchief Rend Blackhand, Upper Blackrock Spire"),
 ("Reiver Claws", "Overlord Wyrmthalak, Lower Blackrock Spire"), ("Brigam Girdle", "General Drakkisath, Upper Blackrock Spire"), ("Titanic Leggings", "Blacksmithing (295)"),
 ("Battlechaser's Greaves", "Trash mobs, Blackrock Depths"), ("Painweaver Band", "General Drakkisath, Upper Blackrock Spire"), ("Blackstone Ring", "Princess Theradras, Maraudon"),
 ("Counterattack Lodestone", "Tribute, Dire Maul - North"), ("Frozen Heart of the Mountain", "Enchanting (260)"), ("Treant's Bane", "Tribute, Dire Maul - North"), None,
 ("Blackcrow", "Shadow Hunter Vosh'gajin, Lower Blackrock Spire")]),
"paladin": ("Paladin", "#D9619C", "paladin", "Tank (Protection)", [
 ("Enchanted Thorium Helm", "Blacksmithing (295)"), ("Verek's Collar", "Verek, Blackrock Depths"), ("Bulky Iron Spaulders", "Trash mobs, Dire Maul - East"),
 ("Shifting Cloak", "Leatherworking (295)"), ("Enchanted Thorium Breastplate", "Blacksmithing (295)"), ("Sentinel's Wristguards", "Blacksmithing (225)"),
 ("Stronghold Gauntlets", "Blacksmithing (295)"), ("Sentinel's Waistguard", "Blacksmithing (245)"), ("Warmaster Legguards", "Warchief Rend Blackhand, Upper Blackrock Spire"),
 ("Shalehusk Boots", "Panzor the Invincible, Blackrock Depths"), ("Band of Flesh", "Ramstein the Gorger, Stratholme"), ("Band of the Ogre King", "King Gordok, Dire Maul - North"),
 ("Vigilance Charm", "Immol'thar, Dire Maul - West"), ("Counterattack Lodestone", "Tribute, Dire Maul - North"), ("Timeworn Mace", "Prince Tortheldrin, Dire Maul - West"),
 ("Draconian Deflector", "General Drakkisath, Upper Blackrock Spire"), ("Excavated Dagger", "Trash mobs, Excavation Site: Wetlands")]),
"hunter": ("Chasseur", "#7FAE3E", "chasseur", "Dégâts", [
 ("Black Dragonscale Helm", "Leatherworking (295)"), ("Emberfury Talisman", "Pyroguard Emberseer, Upper Blackrock Spire"), ("Stratholme Militia Shoulderguard", "Trash mobs, Stratholme"),
 ("Mastercrafted Shifting Cloak", "Leatherworking (295)"), ("Savage Gladiator Chain", "Gorosh the Dervish, Blackrock Depths"), ("Swift Flight Vambraces", "Leatherworking (295)"),
 ("Gauntlets of Accuracy", "Illyanna Ravenoak, Dire Maul - West"), ("Marksman's Girdle", "Urok Doomhowl, Lower Blackrock Spire"), ("Leggings of Destruction", "King Gordok, Dire Maul - North"),
 ("Windreaver Greaves", "Kirtonos the Herald, Scholomance"), ("Tarnished Elven Ring", "Tribute, Dire Maul - North"), ("Painweaver Band", "General Drakkisath, Upper Blackrock Spire"),
 ("Frozen Heart of the Mountain", "Enchanting (260)"), ("Counterattack Lodestone", "Tribute, Dire Maul - North"), ("Treant's Bane", "Tribute, Dire Maul - North"), None,
 ("Flawless Arcanite Rifle", "Engineering (295)")]),
"rogue": ("Voleur", "#D4B82A", "voleur", "Dégâts", [
 ("Mask of the Unforgiven", "The Unforgiven, Stratholme"), ("Imperial Jewel", "Emperor Dagran Thaurissan, Blackrock Depths"), ("Truestrike Shoulders", "Pyroguard Emberseer, Upper Blackrock Spire"),
 ("Cape of the Black Baron", "Baron Rivendare, Stratholme"), ("Dawn Armor", "Leatherworking (295)"), ("Void-Powered Slayer's Vambraces", "Engineering (225)"),
 ("Devilsaur Gauntlets", "Leatherworking (260)"), ("Might of the Timbermaw", "Leatherworking (260)"), ("Plaguehound Leggings", "Trash mobs, Stratholme"),
 ("Mongoose Boots", "Leatherworking (285)"), ("Tarnished Elven Ring", "Tribute, Dire Maul - North"), ("Painweaver Band", "General Drakkisath, Upper Blackrock Spire"),
 ("Counterattack Lodestone", "Tribute, Dire Maul - North"), ("Frozen Heart of the Mountain", "Enchanting (260)"), ("Persuader", "Blacksmithing (295)"),
 ("Persuader", "Blacksmithing (295)"), ("Blackcrow", "Shadow Hunter Vosh'gajin, Lower Blackrock Spire")]),
"priest": ("Prêtre", "#9A9A9A", "pretre", "Soins (Sacré)", [
 ("Incandescent Mooncloth Circlet", "Tailoring (290)"), ("Animated Chain Necklace", "Ramstein the Gorger, Stratholme"), ("Mooncloth Shoulders", "Tailoring (265)"),
 ("Hide of the Wild", "Leatherworking (295)"), ("Truefaith Vestments", "Tailoring (285)"), ("Nethergeld Cuffs", "Tailoring (195)"),
 ("Hands of the Exalted Herald", "Princess Moira Bronzebeard, Blackrock Depths"), ("Whipvine Cord", "Alzzin the Wildshaper, Dire Maul - East"), ("Padre's Trousers", "Illyanna Ravenoak, Dire Maul - West"),
 ("Swarmtender's Footpads", "Tailoring (270)"), ("Band of Mending", "Balnazzar, Stratholme"), ("Rosewine Circle", "Urok Doomhowl, Lower Blackrock Spire"),
 ("Briarwood Reed", "Jed Runewatcher, Upper Blackrock Spire"), ("Second Wind", "Golem Lord Argelmach, Blackrock Depths"), ("Royal Diplomatic Scepter", "Dark Iron Ambassador, Gnomeregan"),
 ("Brightly Glowing Stone", "King Gordok, Dire Maul - North"), ("Bonecreeper Stylus", "Darkmaster Gandling, Scholomance")]),
"shaman": ("Chaman", "#0070DD", "chaman", "Dégâts à distance (Élémentaire)", [
 ("Blue Dragonscale Helm", "Leatherworking (295)"), ("Dark Advisor's Pendant", "Vectus, Scholomance"), ("Honed Blue Dragonscale Shoulders", "Leatherworking (290)"),
 ("Hide of the Wild", "Leatherworking (295)"), ("Honed Blue Dragonscale Breastplate", "Leatherworking (280)"), ("Modest Armguards", "Trash mobs, Dire Maul - East"),
 ("Storm Gauntlets", "Leatherworking (265)"), ("Barrage Girdle", "Cannon Master Willey, Stratholme"), ("Pristine Scorpid Leggings", "Leatherworking (295)"),
 ("Skycaller's Mail Sabatons", "Leatherworking (230)"), ("Flaming Band", "Pyroguard Emberseer, Upper Blackrock Spire"), ("Cyclopean Band", "Ok'thor the Breaker, Blackrock Depths"),
 ("Briarwood Reed", "Jed Runewatcher, Upper Blackrock Spire"), ("Burst of Knowledge", "Ambassador Flamelash, Blackrock Depths"), ("Lightning's Grasp", "Shaman quest: The Tempest's Weapons"),
 ("Tome of the Lost", "General Drakkisath, Upper Blackrock Spire"), None]),
"mage": ("Mage", "#2BA9CC", "mage", "Dégâts", [
 ("Spellweaver's Turban", "General Drakkisath, Upper Blackrock Spire"), ("Dark Advisor's Pendant", "Vectus, Scholomance"), ("Mantle of the Timbermaw", "Tailoring (280)"),
 ("Hide of the Wild", "Leatherworking (295)"), ("Robe of Winter Night", "Tailoring (235)"), ("Void-Powered Invoker's Vambraces", "Engineering (225)"),
 ("Gloves of Spell Mastery", "Tailoring (285)"), ("Belt of the Archmage", "Tailoring (285)"), ("Skyshroud Leggings", "Highlord Omokk, Lower Blackrock Spire"),
 ("Maleki's Footwraps", "Maleki the Pallid, Stratholme"), ("Flaming Band", "Pyroguard Emberseer, Upper Blackrock Spire"), ("Cyclopean Band", "Ok'thor the Breaker, Blackrock Depths"),
 ("Briarwood Reed", "Jed Runewatcher, Upper Blackrock Spire"), ("Burst of Knowledge", "Ambassador Flamelash, Blackrock Depths"), ("Radiant Staff", "Enchanting (200)"), None,
 ("Bonecreeper Stylus", "Darkmaster Gandling, Scholomance")]),
"warlock": ("Démoniste", "#7072D6", "demoniste", "Dégâts", [
 ("Spellweaver's Turban", "General Drakkisath, Upper Blackrock Spire"), ("Dark Advisor's Pendant", "Vectus, Scholomance"), ("Mantle of the Timbermaw", "Tailoring (280)"),
 ("Hide of the Wild", "Leatherworking (295)"), ("Robe of Winter Night", "Tailoring (235)"), ("Void-Powered Invoker's Vambraces", "Engineering (225)"),
 ("Gloves of Spell Mastery", "Tailoring (285)"), ("Belt of the Archmage", "Tailoring (285)"), ("Skyshroud Leggings", "Highlord Omokk, Lower Blackrock Spire"),
 ("Maleki's Footwraps", "Maleki the Pallid, Stratholme"), ("Flaming Band", "Pyroguard Emberseer, Upper Blackrock Spire"), ("Cyclopean Band", "Ok'thor the Breaker, Blackrock Depths"),
 ("Briarwood Reed", "Jed Runewatcher, Upper Blackrock Spire"), ("Burst of Knowledge", "Ambassador Flamelash, Blackrock Depths"), ("Radiant Staff", "Enchanting (200)"), None,
 ("Bonecreeper Stylus", "Darkmaster Gandling, Scholomance")]),
"druid": ("Druide", "#E86E08", "druide", "Tank (Combat farouche, ours)", [
 ("Warbear Helm", "Leatherworking (295)"), ("Verek's Collar", "Verek, Blackrock Depths"), ("Golden Mantle of the Dawn", "Leatherworking (290)"),
 ("Shifting Cloak", "Leatherworking (295)"), ("Warbear Harness", "Leatherworking (245)"), ("Blackmist Armguards", "The Beast, Upper Blackrock Spire"),
 ("Quickdraw Gloves", "Immol'thar, Dire Maul - West"), ("Might of the Timbermaw", "Leatherworking (260)"), ("Warstrife Leggings", "General Angerforge, Blackrock Depths"),
 ("Ash Covered Boots", "Archivist Galford, Stratholme"), ("Band of Flesh", "Ramstein the Gorger, Stratholme"), ("Band of the Ogre King", "King Gordok, Dire Maul - North"),
 ("Vigilance Charm", "Immol'thar, Dire Maul - West"), ("Counterattack Lodestone", "Tribute, Dire Maul - North"), ("Headmaster's Charge", "Darkmaster Gandling, Scholomance"), None,
 ("Excavated Dagger", "Trash mobs, Excavation Site: Wetlands")]),
}
PROF = {"Blacksmithing": "Forge", "Leatherworking": "Travail du cuir", "Tailoring": "Couture", "Engineering": "Ingénierie", "Enchanting": "Enchantement"}
ZONE = {"Blackrock Depths": "Profondeurs de Rochenoire", "Upper Blackrock Spire": "Pic Rochenoire supérieur", "Lower Blackrock Spire": "Pic Rochenoire inférieur",
        "Stratholme": "Stratholme", "Scholomance": "Scholomance", "Dire Maul - North": "Hache-Tripes Nord", "Dire Maul - East": "Hache-Tripes Est",
        "Dire Maul - West": "Hache-Tripes Ouest", "Maraudon": "Maraudon", "Gnomeregan": "Gnomeregan", "Excavation Site: Wetlands": "Site de fouilles des Paluns"}
DPAGE = {"Profondeurs de Rochenoire": "profondeurs-de-rochenoire", "Pic Rochenoire supérieur": "pic-rochenoire", "Pic Rochenoire inférieur": "pic-rochenoire",
         "Stratholme": "stratholme", "Scholomance": "scholomance", "Hache-Tripes Nord": "hache-tripes", "Hache-Tripes Est": "hache-tripes", "Hache-Tripes Ouest": "hache-tripes",
         "Maraudon": "maraudon", "Gnomeregan": "gnomeregan", "Site de fouilles des Paluns": "site-de-fouilles-des-paluns"}

FRI = {i: n for i, n in DB.execute("select id,name from l10n where entity_type='item' and locale='frFR'")}
FRN = {}
for i, n in DB.execute("select n.id, l.name from m_npc n join l10n l on l.entity_type='npc' and l.locale='frFR' and l.id=n.id"):
    pass
NPCEN = {}
for i, en in DB.execute("select id,name from m_npc"): NPCEN.setdefault(en, i)
FRNPC = {i: n for i, n in DB.execute("select id,name from l10n where entity_type='npc' and locale='frFR'")}
QUAL = {i: q for i, q in DB.execute("select id,quality from m_item_stats")}
FORGE = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else {}   # index nom anglais -> [id, qualité] des objets de Forever (forever-forge)
_t = open(sys.argv[3], encoding="utf-8").read() if len(sys.argv) > 3 else ""   # noms français de Polestar
for body in re.findall(r'R\("item",\s*\d+,\s*\d+,\s*\[\[(.*?)\]\]\)', _t, re.S):
    for line in body.split("\n"):
        if "\t" in line:
            i, n = line.split("\t", 1); FRI.setdefault(int(i), re.sub(r"%([0-9A-Fa-f]{2})", lambda m: chr(int(m.group(1), 16)), n))
def item_id(en):
    rows = list(DB.execute("select id from m_item where name=? order by id", (en,)))
    if rows: return rows[0][0]
    if en in FORGE: QUAL.setdefault(FORGE[en][0], FORGE[en][1]); return FORGE[en][0]
    return None
def source(src):
    m = re.match(r"(\w+) \((\d+)\)$", src)
    if m: return f"{PROF.get(m.group(1), m.group(1))} ({m.group(2)})"
    if src.startswith("Shaman quest: "): return "Quête de chaman : Les armes de la tempête"
    who, _, where = src.rpartition(", ")
    zfr = ZONE.get(where, where); dl = DPAGE.get(zfr)
    zone = f'<a href="donjon-{dl}.html">{e(zfr)}</a>' if dl else e(zfr)
    if who == "Trash mobs": return f"Monstres de {zone}"
    if who == "Tribute": return f"Coffre du tribut, {zone}"
    nid = NPCEN.get(who)
    return f"{e(FRNPC.get(nid, who))}, {zone}"

missing = []
data = {}
for cid, (nom, col, img, spec, items) in BIS.items():
    out = []
    for slot, it in zip(S, items):
        if not it: out.append([slot, None]); continue
        en, src = it; iid = item_id(en)
        if not iid: missing.append(en)
        out.append([slot, {"n": FRI.get(iid, en) if iid else en, "id": iid, "q": QUAL.get(iid, 4), "s": source(src)}])
    data[cid] = {"nom": nom, "c": col, "img": img, "spec": spec, "slots": out}
print("introuvables :", missing)

QC = {2: "#1eff00", 3: "#0070dd", 4: "#a335ee", 5: "#ff8000"}
def slotbox(slot, it):
    if not it: return f'<li class="bs empty"><span class="bs-s">{slot}</span><span class="bs-n">—</span></li>'
    a = (f'<a href="https://www.wowhead.com/forever/fr/item={it["id"]}" target="_blank" rel="noopener" data-wowhead="item={it["id"]}&domain=fr.forever" style="color:{QC.get(it["q"], "#a335ee")}">{e(it["n"])}</a>'
         if it["id"] else e(it["n"]))
    return f'<li class="bs"><span class="bs-s">{slot}</span><span class="bs-n">{a}</span><span class="bs-src">{it["s"]}</span></li>'
tabs = "".join(f'<button type="button" class="cbtn{" on" if i == 0 else ""}" data-c="{c}" style="--c:{d["c"]}"><img src="images/icons/class_{c}.jpg" alt="">{d["nom"]}</button>' for i, (c, d) in enumerate(data.items()))
panels = ""
for i, (c, d) in enumerate(data.items()):
    sl = d["slots"]
    left = "".join(slotbox(*x) for x in sl[:8]); right = "".join(slotbox(*x) for x in sl[8:14]); bottom = "".join(slotbox(*x) for x in sl[14:])
    panels += f'''<section class="bisp" id="bis-{c}" style="--c:{d["c"]}"{"" if i == 0 else " hidden"}>
  <h2>{d["nom"]} <span class="pp-lv">{e(d["spec"])}</span></h2>
  <div class="bisd"><ul class="bcol">{left}</ul><div class="bfig"><img src="images/bis/{d["img"]}.webp" alt="{d["nom"]} (illustration)" loading="lazy"></div><ul class="bcol">{right}</ul></div>
  <ul class="bbot">{bottom}</ul>
</section>'''

body = f'''<main><div class="wrap">
<div class="crumbs"><a href="index.html">News</a> › Équipement › BiS niveau 60</div>
<h1 class="page-title">Meilleur équipement (BiS) niveau 60</h1>
<p class="page-lead">Pour chaque classe, la meilleure pièce à viser dans chaque emplacement avant les raids : donjons du niveau 60, quêtes et métiers. Passe la souris sur un objet pour voir ses caractéristiques.</p>
<nav class="cls-tabs" id="bis-tabs">{tabs}</nav>
{panels}
<div class="info" style="margin-top:18px">Ces listes sont calculées avant le lancement, sans le butin de raid ni les objets au-dessus du niveau d'objet 63. Beaucoup de caractéristiques reprennent encore les valeurs de Classic : elles évolueront quand les joueurs atteindront le niveau 60.</div>
<p class="small">Listes d'après <a href="https://wow4ever.quest/en/bis/mage-dps" target="_blank" rel="noopener">wow4ever.quest</a>, noms français d'après les données du jeu, info-bulles Wowhead. Illustrations des classes : ForeverWoW.</p>
</div>'''
tpl = open("legacy.html", encoding="utf-8").read()
head = tpl[:tpl.index("<main>")]
head = re.sub(r"<title>.*?</title>", "<title>BiS niveau 60 : meilleur équipement par classe – ForeverWoW</title>", head)
head = re.sub(r'name="description" content=".*?"', 'name="description" content="Le meilleur équipement pré-raid (BiS) du niveau 60 pour chaque classe de WoW Forever : objets, où les obtenir, avec info-bulles."', head)
tail = re.sub(r'<script src="js/heritage\.js[^"]*"></script>\n?', '', tpl[tpl.index("</main>"):])
js = '''<script>document.getElementById("bis-tabs").addEventListener("click",e=>{const b=e.target.closest("button");if(!b)return;
document.querySelectorAll("#bis-tabs button").forEach(x=>x.classList.toggle("on",x===b));
document.querySelectorAll(".bisp").forEach(p=>p.hidden=p.id!=="bis-"+b.dataset.c);history.replaceState(null,"","#"+b.dataset.c)});
const h=location.hash.slice(1);if(h){const b=document.querySelector(`#bis-tabs [data-c="${h}"]`);if(b)b.click()}</script>
<script>const whTooltips = {colorLinks: false, iconizeLinks: true, renameLinks: false, iconSize: "small"};</script>
<script src="https://wow.zamimg.com/js/tooltips.js"></script>
</body>'''
tail = tail.replace("</body>", js, 1)
open("bis.html", "w", encoding="utf-8").write(head + body + tail)
