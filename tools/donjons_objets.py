"""Objets de quête à trouver dans chaque donjon (tools/donjons_objets.json).
Usage : python3 tools/donjons_objets.py <f_new.sqlite de Factoruide>
Pour chaque donjon : quêtes rattachées à ses aires, objets demandés, et sur quel monstre ou objet du donjon ils se trouvent."""
import json, os, re, sqlite3, sys
ROOT = os.path.dirname(os.path.abspath(__file__)) + "/.."
DB = sqlite3.connect(sys.argv[1])
q = lambda s, *a: list(DB.execute(s, a))
src = open(f"{ROOT}/tools/donjons_extract.py", encoding="utf-8").read()
LISTE = eval(re.search(r"LISTE = (\[.*?\n\])", src, re.S).group(1))
AREAS = {slug: areas for slug, _, _, areas, _, _ in LISTE}
AREAS["salle-des-thanes"] = [r[0] for r in q("select area from dungeon where name like '%Thanes%'")]
FR = {(t, i): n for t, i, n in q("select entity_type,id,name from l10n where locale='frFR'")}
ITEM = {n: i for i, n in q("select id,name from m_item")}
AM, HM = 4294967373, 8589934770
out = {}
for slug, areas in AREAS.items():
    if not areas: continue
    ph = ",".join("?" * len(areas))
    inside = lambda t, i: bool(q(f"select 1 from m_spawn where entity_type=? and entity_id=? and zone_id in ({ph}) limit 1", t, i, *areas)) or \
        (t == "npc" and bool(q(f"select 1 from m_npc where id=? and zone_id in ({ph})", i, *areas)))
    rows, seen = [], set()
    for qid, qn, req, races in q(f"select id,name,requirements,races_mask from m_quest where zone_or_sort in ({ph}) and hidden=0 and requirements is not null", *areas):
        for r in json.loads(req or "[]"):
            m = re.match(r"(.*?)(?: x (\d+))?$", r); n, cnt = m.group(1), int(m.group(2) or 1)
            iid = ITEM.get(n)
            if not iid or (iid, qn) in seen: continue
            if q("select count(*) from m_item_source where item_id=?", iid)[0][0] > 25 or q("select 1 from m_vendor_stock where item_id=? limit 1", iid): continue
            srcs = []
            for t, sid, ch in q("select from_type,from_id,chance from m_item_source where item_id=? order by chance desc", iid):
                if t not in ("npc", "object") or not inside(t, sid): continue
                en = (q(f"select name from m_{t} where id=?", sid) or [[None]])[0][0]
                fr = FR.get((t, sid)) or en
                if fr and fr not in srcs: srcs.append(fr)
            if not srcs: continue
            seen.add((iid, qn))
            camp = "Alliance" if races == AM else ("Horde" if races == HM else "")
            rows.append({"objet": FR.get(("item", iid)) or n, "id": iid, "nb": cnt, "quete": FR.get(("quest", qid)) or qn, "camp": camp, "sur": srcs[:4]})
    merged = {}
    for r in rows:
        k = (r["objet"], tuple(r["sur"]))
        if k in merged:
            m = merged[k]
            if r["quete"] not in m["quetes"]: m["quetes"].append(r["quete"])
            if m["camp"] != r["camp"]: m["camp"] = ""
        else:
            merged[k] = {**r, "quetes": [r["quete"]]}; del merged[k]["quete"]
    out[slug] = {"zone": areas[0], "objets": list(merged.values())}
json.dump(out, open(f"{ROOT}/tools/donjons_objets.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print({k: len(v["objets"]) for k, v in out.items()})
