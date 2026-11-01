"""Génère les données de la carte interactive (carte.html).

Usage : python3 tools/carte.py <clone de Polestar> <clone de Factoruide>
- positions : forever-db de Polestar (CC BY 4.0, voir son NOTICE.md)
- noms français : module Polestar_frFR
- fonds de carte : data/maps/forever/*.webp de Factoruide (images du client du jeu, © Blizzard Entertainment)
"""
import json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.abspath(__file__)) + "/.."
PS, FA = sys.argv[1], sys.argv[2]
os.chdir(ROOT)

ZONES = {1411: "Durotar", 1412: "Mulgore", 1413: "Les Tarides", 1416: "Montagnes d'Alterac", 1417: "Hautes-terres d'Arathi",
 1418: "Terres ingrates", 1419: "Terres foudroyées", 1420: "Clairières de Tirisfal", 1421: "Forêt des Pins-Argentés",
 1422: "Maleterres de l'Ouest", 1423: "Maleterres de l'Est", 1424: "Contreforts de Hautebrande", 1425: "Les Hinterlands",
 1426: "Dun Morogh", 1427: "Gorge des Vents brûlants", 1428: "Steppes ardentes", 1429: "Forêt d'Elwynn", 1430: "Défilé de Deuillevent",
 1431: "Bois de la Pénombre", 1432: "Loch Modan", 1433: "Les Carmines", 1434: "Vallée de Strangleronce", 1435: "Marais des Chagrins",
 1436: "Marche de l'Ouest", 1437: "Les Paluns", 1438: "Teldrassil", 1439: "Sombrivage", 1440: "Orneval", 1441: "Mille pointes",
 1442: "Les Serres-Rocheuses", 1443: "Désolace", 1444: "Féralas", 1445: "Marécage d'Âprefange", 1446: "Tanaris", 1447: "Azshara",
 1448: "Gangrebois", 1449: "Cratère d'Un'Goro", 1450: "Reflet-de-Lune", 1451: "Silithus", 1452: "Berceau-de-l'Hiver",
 1453: "Hurlevent", 1454: "Orgrimmar", 1455: "Forgefer", 1456: "Les Pitons-du-Tonnerre", 1457: "Darnassus", 1458: "Fossoyeuse",
 2521: "Île de Zéphras", 2482: "Mont Hyjal", 2524: "Îles des Sombrelances", 2548: "Riverglades"}
CONT = {1411: "k", 1412: "k", 1413: "k", 1438: "k", 1439: "k", 1440: "k", 1441: "k", 1442: "k", 1443: "k", 1444: "k", 1445: "k",
 1446: "k", 1447: "k", 1448: "k", 1449: "k", 1450: "k", 1451: "k", 1452: "k", 1454: "k", 1456: "k", 1457: "k", 2482: "k", 2524: "k", 2521: "z"}

CLASS_T = {"Warrior Trainer": "Maître des guerriers", "Paladin Trainer": "Maître des paladins", "Hunter Trainer": "Maître des chasseurs",
 "Rogue Trainer": "Maître des voleurs", "Priest Trainer": "Maître des prêtres", "Shaman Trainer": "Maître des chamans",
 "Mage Trainer": "Maître des mages", "Warlock Trainer": "Maître des démonistes", "Druid Trainer": "Maître des druides",
 "Pet Trainer": "Maître des familiers", "Demon Trainer": "Maître des démons"}
PROF = {"Alchemy": "alchimie", "Blacksmith": "forge", "Enchant": "enchantement", "Engineer": "ingénierie", "Herbalis": "herboristerie",
 "Leatherwork": "travail du cuir", "Mining": "minage", "Miner": "minage", "Skinning": "dépeçage", "Tailor": "couture", "Cook": "cuisine",
 "First Aid": "secourisme", "Fishing": "pêche", "Fisherman": "pêche", "Physician": "secourisme", "Surgeon": "secourisme"}
FLY = ("Gryphon Master", "Wind Rider Master", "Hippogryph Master", "Bat Handler", "Flight Master")
OTHER = {"Innkeeper": ("inn", "Aubergiste"), "Banker": ("bank", "Banquier"), "Auctioneer": ("bank", "Commissaire-priseur"),
 "Stable Master": ("inn", "Maître des écuries")}
HERBS = r"Peacebloom|Silverleaf|Earthroot|Mageroyal|Briarthorn|Stranglekelp|Bruiseweed|Steelbloom|Grave Moss|Kingsblood|Liferoot|Fadeleaf|Goldthorn|Khadgar's Whisker|Wintersbite|Firebloom|Purple Lotus|Arthas' Tears|Sungrass|Blindweed|Ghost Mushroom|Gromsblood|Golden Sansam|Dreamfoil|Mountain Silversage|Plaguebloom|Icecap|Black Lotus|Star Lotus"
ORES = r"(Vein|Deposit)$"

FR = {}
t = open(f"{PS}/addon/Polestar_frFR/Names.lua", encoding="utf-8").read()
for kind, body in re.findall(r'R\("(\w+)",\s*\d+,\s*\d+,\s*\[\[(.*?)\]\]\)', t, re.S):
    for line in body.split("\n"):
        if "\t" in line:
            i, n = line.split("\t", 1)
            FR[(kind, i)] = re.sub(r"%([0-9A-Fa-f]{2})", lambda m: chr(int(m.group(1), 16)), n)

load = lambda f: [json.loads(l) for l in open(f"{PS}/forever-db/data/{f}.jsonl", encoding="utf-8")]
NPC = {r["id"]: r for r in load("npc")}
OBJ = {r["id"]: r for r in load("object")}
UM = {r["ui_map"]: r for r in load("ui_map")}

def category(kind, rid):
    if kind == "npc":
        n = NPC.get(rid, {}); sub = n.get("subname", "")
        if sub in CLASS_T: return "class", CLASS_T[sub]
        if any(f in sub for f in FLY): return "fly", "Maître de vol"
        if sub in OTHER: return OTHER[sub]
        if re.search(r"Trainer|Journeyman|Expert|Artisan|Master ", sub) or sub in ("Physician", "Surgeon"):
            for k, v in PROF.items():
                if k in sub: return "prof", f"Maître en {v}"
        return None
    n = OBJ.get(rid, {}).get("name", "")
    if re.search(HERBS, n): return "herb", "Herbe"
    if re.search(ORES, n): return "ore", "Minerai"
    return None

def name(kind, rid):
    k = "npc" if kind == "npc" else "object"
    en = (NPC if kind == "npc" else OBJ).get(rid, {}).get("name", "")
    return FR.get((k, str(rid))) or en

# Filtre par zone : la base de Factoruide (data/forever.sqlite.zst, décompressée en f.sqlite)
# dit dans quelle zone se trouve chaque apparition ; elle sert seulement à écarter les points
# des zones voisines visibles sur le même fond de carte.
import sqlite3, subprocess, collections
DB = os.path.join(os.path.dirname(os.path.abspath(FA)), "f.sqlite")
if not os.path.exists(DB):
    subprocess.run(["node", "-e", f"const z=require('zlib'),fs=require('fs');fs.writeFileSync('{DB}',z.zstdDecompressSync(fs.readFileSync('{FA}/data/forever.sqlite.zst')))"], check=True)
con = sqlite3.connect(DB)
AREA = {u: a for u, a in con.execute("select UiMapID, AreaID from client_uimapassignment where OrderIndex=0")}
INZONE = collections.defaultdict(list); KNOWN = set()
for t_, i_, a_, x_, y_ in con.execute("select entity_type, entity_id, zone_id, x, y from m_spawn"):
    if x_ is None: continue
    INZONE[(t_, i_, a_)].append((x_, y_)); KNOWN.add((t_, i_))
def in_zone(kind, rid, z, x, y):
    if (kind, rid) not in KNOWN or z not in AREA: return True
    return any(abs(x - a) < 1.5 and abs(y - b) < 1.5 for a, b in INZONE.get((kind, rid, AREA[z]), []))

pts = {z: [] for z in ZONES}
seen = set()
for s in load("spawn"):
    cat = category(s["kind"], s["id"])
    if not cat: continue
    for z in ZONES:
        m = UM.get(z)
        if not m or m["map"] != s["map"]: continue
        x = (m["left"] - s["y"]) / (m["left"] - m["right"]); y = (m["top"] - s["x"]) / (m["top"] - m["bottom"])
        if not (0.005 < x < 0.995 and 0.005 < y < 0.995): continue
        if not in_zone(s["kind"], s["id"], z, x * 100, y * 100): continue
        key = (z, s["kind"], s["id"], round(x, 3), round(y, 3))
        if key in seen: continue
        seen.add(key)
        pts[z].append([cat[0], round(x * 100, 1), round(y * 100, 1), name(s["kind"], s["id"]), cat[1] if cat[0] not in ("herb", "ore") else ""])

os.makedirs("images/cartes", exist_ok=True); os.makedirs("data/carte", exist_ok=True)
index = []
for z, nom in sorted(ZONES.items(), key=lambda kv: kv[1]):
    src = f"{FA}/data/maps/forever/{z}.webp"
    if not os.path.exists(src): continue
    shutil.copy(src, f"images/cartes/{z}.webp")
    json.dump(pts[z], open(f"data/carte/{z}.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    index.append({"id": z, "nom": nom, "c": CONT.get(z, "e"), "n": len(pts[z])})
json.dump(index, open("data/carte/zones.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print(len(index), "zones,", sum(len(v) for v in pts.values()), "points")
