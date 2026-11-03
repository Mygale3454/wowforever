"""Extrait des bases du jeu les données des pages de donjon (tools/donjons_auto.json).
Usage : python3 tools/donjons_extract.py <f.sqlite de Factoruide> <clone de Polestar>
- entrée : table dungeon de Factoruide (coordonnées Questie) ; carte : client_uimapassignment
- boss et butin : m_boss_loot (données Classic/VMaNGOS) ; noms français : table l10n
- quêtes : m_quest (zone du donjon), donneurs (m_quest_relation), récompenses (m_quest_reward)"""
import json, os, sqlite3, sys, collections
ROOT = os.path.dirname(os.path.abspath(__file__)) + "/.."
DB = sqlite3.connect(sys.argv[1])
q = lambda s, *a: list(DB.execute(s, a))

# slug, nom, niveaux, zones (aires), nouveau, intro
LISTE = [
 ("gouffre-de-ragefeu", "Le Gouffre de Ragefeu", "13 à 18", [2437], False, "Sous Orgrimmar, des cultistes de la Lame ardente et des troggs ont envahi les cavernes de lave. C'est le premier donjon de la Horde."),
 ("ruines-de-lordaeron", "Les Ruines de Lordaeron", "15 à 20", [16611], True, "Au-dessus de Fossoyeuse, les ruines de la capitale déchue de Lordaeron deviennent un donjon. Nouveau dans Forever, il s'adresse surtout aux joueurs de la Horde."),
 ("mortemines", "Les Mortemines", "15 à 22", [1581], False, "Sous Ruisselune, la Confrérie défias d'Edwin VanCleef prépare sa vengeance contre Hurlevent dans une ancienne mine, jusqu'au navire caché au fond."),
 ("cavernes-des-lamentations", "Les Cavernes des lamentations", "17 à 24", [718], False, "Dans une oasis des Tarides, les druides du Croc ont été corrompus par le Cauchemar. Il faut réveiller Naralex, endormi au fond des cavernes."),
 ("donjon-d-ombrecroc", "Le Donjon d'Ombrecroc", "20 à 26", [209], False, "Le château d'Arugal, le mage fou de Dalaran, au nord de Pins-Argentés, peuplé de worgens et de morts-vivants."),
 ("profondeurs-de-brassenoire", "Les Profondeurs de Brassenoire", "22 à 28", [719], False, "Un ancien temple elfique englouti sur la côte d'Orneval, aux mains des Nagas et des adorateurs du Marteau du crépuscule."),
 ("site-de-fouilles-des-paluns", "Le Site de fouilles des Paluns", "24 à 29", [16732, 17732], True, "Un nouveau donjon de Forever, ouvert dans les fouilles naines des Paluns."),
 ("la-prison", "La Prison", "25 à 29", [717], False, "La prison de Hurlevent, où les détenus défias se sont révoltés."),
 ("cite-de-dalaran", "La Cité de Dalaran", "28 à 33", [16544, 16560], True, "Nouveau dans Forever : la cité des mages, cachée derrière son dôme dans les montagnes d'Alterac, devient un donjon."),
 ("gnomeregan", "Gnomeregan", "29 à 38", [721], False, "L'ancienne capitale des gnomes, irradiée et envahie par les troggs, sous Dun Morogh."),
 ("kraal-de-tranchebauge", "Le Kraal de Tranchebauge", "29 à 38", [491], False, "Le labyrinthe de ronces des huttins, au sud des Tarides."),
 ("monastere-ecarlate", "Le Monastère écarlate", "30 à 46", [796], False, "La forteresse de la Croisade écarlate dans les Clairières de Tirisfal, en quatre ailes : cimetière, bibliothèque, armurerie et cathédrale."),
 ("uldaman", "Uldaman", "36 à 45", [1337, 1517], False, "Un site titan enfoui sous les Terres ingrates, où nains Sombrefer et troggs se disputent les secrets des créateurs."),
 ("souilles-de-tranchebauge", "Les Souilles de Tranchebauge", "37 à 46", [722], False, "Le cœur des huttins des Tarides, tombé sous la coupe du Fléau."),
 ("zul-farrak", "Zul'Farrak", "40 à 47", [1176, 978], False, "La cité des trolls des sables, au cœur du désert de Tanaris."),
 ("maraudon", "Maraudon", "45 à 51", [2100], False, "Les grottes sacrées des centaures de Désolace, où repose la princesse Theradras."),
 ("temple-englouti", "Le Temple englouti", "50 à 55", [1477, 1417], False, "Le temple d'Atal'Hakkar, englouti dans le Marais des Chagrins, où les trolls veulent invoquer le dieu sanguinaire Hakkar."),
 ("profondeurs-de-rochenoire", "Les Profondeurs de Rochenoire", "52 à 60", [1584, 1585], False, "La cité des nains Sombrefer au cœur du Mont Rochenoire, le plus grand donjon du jeu."),
 ("pic-rochenoire", "Le Pic Rochenoire", "57 à 60", [1583], False, "Le sommet du Mont Rochenoire, en deux parties : le pic inférieur (orcs et ogres) et le pic supérieur (le chef de guerre Rend et les dragons)."),
 ("hache-tripes", "Hache-Tripes", "58 à 60", [2557], False, "L'ancienne cité elfe d'Eldre'Thalas, au cœur de Féralas, en trois ailes : Est, Nord et Ouest."),
 ("stratholme", "Stratholme", "58 à 60", [2017], False, "La ville martyre des Maleterres de l'Est, partagée entre le Fléau du baron Vaillefendre et la Croisade écarlate."),
 ("scholomance", "Scholomance", "58 à 60", [2057], False, "L'école de nécromancie du Fléau, dans les cryptes de Caer Darrow, aux Maleterres de l'Ouest."),
]
SLOT = {1: "Tête", 2: "Cou", 3: "Épaules", 4: "Chemise", 5: "Torse", 6: "Taille", 7: "Jambes", 8: "Pieds", 9: "Poignets", 10: "Mains", 11: "Doigt",
        12: "Bijou", 13: "Une main", 14: "Bouclier", 15: "Distance", 16: "Dos", 17: "Deux mains", 19: "Tabard", 20: "Torse", 21: "Main droite",
        22: "Main gauche", 23: "Main gauche", 25: "Jet", 26: "Distance", 28: "Relique"}
FR = {(t, i): n for t, i, n in q("select entity_type,id,name from l10n where locale='frFR'")}
ST = {r[0]: r for r in q("select id,quality,inventory_type,class from m_item_stats")}
NPC = {r[0]: r for r in q("select id,name,zone_id from m_npc")}
AREA2MAP = {}
for u, a in q("select UiMapID, AreaID from client_uimapassignment where OrderIndex=0"):
    if os.path.exists(f"{ROOT}/images/cartes/{u}.webp"): AREA2MAP.setdefault(a, u)
import re as _re
_src = open(f"{ROOT}/tools/carte.py", encoding="utf-8").read()
ZNAME = eval(_re.search(r"ZONES = (\{.*?\})\nCONT", _src, _re.S).group(1))
ZNAME.update({1453: "Hurlevent", 1454: "Orgrimmar", 1455: "Forgefer", 1458: "Fossoyeuse"})
ZFR = lambda a: ZNAME.get(AREA2MAP.get(a)) or FR.get(("zone", a)) or (q("select AreaName_lang from client_areatable where ID=?", a) or [[""]])[0][0]
DUNG = {r[0]: r for r in q("select area,name,entrance_zone,entrance_x,entrance_y from dungeon")}
ENT = collections.defaultdict(list)
for a, f, z, x, y in q("select area,faction,zone,x,y from dungeon_entrance"): ENT[a].append((f, z, x, y))

out = {}
for slug, nom, niv, areas, new, intro in LISTE:
    d = {"nom": nom, "niv": niv, "nouveau": new, "intro": intro, "boss": [], "quetes": []}
    a0 = areas[0]
    if a0 in DUNG and DUNG[a0][2]:
        _, en, z, x, y = DUNG[a0]
        d.update(en=en, zone=ZFR(z), carte=AREA2MAP.get(z), x=round(x, 1), y=round(y, 1))
    elif ENT.get(a0):
        f, z, x, y = ENT[a0][0]
        d.update(en=nom, zone=ZFR(z), carte=AREA2MAP.get(z), x=round(x, 1), y=round(y, 1))
    # boss : PNJ du donjon dont au moins un objet tombe souvent (≥ 8 %)
    loot = collections.defaultdict(list)
    for n, it, ch in q(f"select b.npc_id,b.item_id,b.chance from m_boss_loot b join m_npc n on n.id=b.npc_id where n.zone_id in ({','.join('?' * len(areas))})", *areas):
        loot[n].append((it, ch))
    for n, its in sorted(loot.items()):
        if max(ch for _, ch in its) < 0.08: continue
        items = []
        for it, ch in sorted(its, key=lambda t: -t[1]):
            s = ST.get(it)
            if not s or (s[1] or 0) < 2 or not FR.get(("item", it)): continue
            items.append([FR[("item", it)], SLOT.get(s[2], "Objet"), None, it, s[1]])
        if items: d["boss"].append([FR.get(("npc", n), NPC[n][1]), NPC[n][1], items])
    # quêtes
    for qid, en_n, lvl, mask in q(f"select id,name,level,races_mask from m_quest where zone_or_sort in ({','.join('?' * len(areas))}) and status='available' and hidden=0", *areas):
        nm = FR.get(("quest", qid)) or en_n
        m = (mask or 0) & 0xFFFFFFFF
        al, ho = bool(m & 77), bool(m & 178)
        camp = "Alliance et Horde" if (al and ho) or not m else ("Alliance" if al else "Horde")
        giv = []
        for et, eid in q("select entity_type,entity_id from m_quest_relation where quest_id=? and role='start'", qid):
            if et == "npc" and eid in NPC:
                z = NPC[eid][2]
                giv.append(f"{FR.get(('npc', eid), NPC[eid][1])}" + (f" ({ZFR(z)})" if z else ""))
            elif et == "item": giv.append(f"en ramassant {FR.get(('item', eid), 'un objet')}")
        rec = [[FR.get(("item", it)), it] for it, ch in q("select item_id,choice from m_quest_reward where quest_id=?", qid) if FR.get(("item", it))]
        d["quetes"].append([nm, lvl, camp, ", ".join(dict.fromkeys(giv)) or "—", rec])
    d["quetes"].sort(key=lambda t: (t[1] or 0, t[0]))
    out[slug] = d
    print(slug, d.get("zone"), len(d["boss"]), "boss", len(d["quetes"]), "quêtes")
json.dump(out, open(f"{ROOT}/tools/donjons_auto.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
