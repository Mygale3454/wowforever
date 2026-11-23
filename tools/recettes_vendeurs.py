"""Marchands qui vendent les patrons/recettes achetés dans les guides de métiers (tools/recettes_vendeurs.json).
Usage : python3 tools/recettes_vendeurs.py <f_new.sqlite de Factoruide> <clone de Polestar>"""
import json, os, re, sqlite3, sys, glob
ROOT = os.path.dirname(os.path.abspath(__file__)) + "/.."
DB = sqlite3.connect(sys.argv[1]); PS = sys.argv[2]
q = lambda s, *a: list(DB.execute(s, a))
NAMES = {}
for l in open(f"{PS}/forever-db/data/item.jsonl", encoding="utf-8"):
    d = json.loads(l); NAMES[d["id"]] = d.get("name", "")
FR = {(t, i): n for t, i, n in q("select entity_type,id,name from l10n where locale='frFR'")}
ZFIX = {331: "Orneval", 28: "Maleterres de l'Ouest", 139: "Maleterres de l'Est", 1519: "Hurlevent", 1537: "Forgefer", 1657: "Darnassus", 1637: "Orgrimmar", 1638: "Les Pitons-du-Tonnerre", 1497: "Fossoyeuse"}
def zone(a): return ZFIX.get(a) or FR.get(("zone", a)) or (q("select AreaName_lang from client_areatable where ID=?", a) or [[str(a)]])[0][0]
REC = re.compile(r"^(Pattern|Recipe|Formula|Plans|Schematic|Manual|Design|Expert|Artisan)\b")
ids = set()
for g in glob.glob(f"{PS}/guides/forever/professions/*.guide"):
    for m in re.finditer(r"^\s*buy (\d+)", open(g, encoding="utf-8").read(), re.M): ids.add(int(m.group(1)))
out = {}
for i in sorted(ids):
    nm = NAMES.get(i) or (q("select name from m_item where id=?", i) or [[""]])[0][0]
    if not REC.match(nm or ""): continue
    vs = []
    for nid, n, fac in q("select v.npc_id,n.name,n.friendly_to from m_vendor_stock v join m_npc n on n.id=v.npc_id where v.item_id=?", i):
        sp = q("select zone_id,round(avg(x),1),round(avg(y),1) from m_spawn where entity_type='npc' and entity_id=? and x>=0 group by zone_id order by count(*) desc limit 1", nid)
        if not sp: continue
        z, x, y = sp[0]
        f = "Alliance" if fac == "A" else "Horde" if fac == "H" else "Les deux"
        vs.append({"nom": FR.get(("npc", nid)) or n, "faction": f, "zone": zone(z), "x": x, "y": y})
    out[i] = {"nom": nm, "vendeurs": vs}
json.dump(out, open(f"{ROOT}/tools/recettes_vendeurs.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), "recettes,", sum(1 for v in out.values() if v["vendeurs"]), "avec marchand connu")
