"""Met à jour js/talents-data.js (calculateur de talents) depuis les données extraites du client de jeu.

Usage : git clone --depth 1 https://github.com/brainw0rm/forge /tmp/forge
        python3 tools/talents.py /tmp/forge
Source : public/data/classes/<classe>.json de forever-forge.com (tables du client WoW Forever).
Les noms, rangs, positions et textes des talents sont des données du jeu (© Blizzard Entertainment).
Ensuite : python3 tools/talents.py --builds pour recalculer les codes de tools/builds.json.
"""
import json, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.abspath(__file__)) + "/.."
os.chdir(ROOT)
CLASSES = ["warrior", "paladin", "hunter", "rogue", "priest", "shaman", "mage", "warlock", "druid"]
STATUS = {"new": "new", "unchanged": "unchanged", "moved": "moved", "tuned": "changed", "expanded": "changed", "reworked": "changed"}
B36 = "0123456789abcdefghijklmnopqrstuvwxyz"
slug = lambda n: re.sub(r"[^a-z0-9]+", "-", n.lower()).strip("-")

def load_js():
    out = subprocess.run(["node", "-e", "const fs=require('fs');eval(fs.readFileSync('js/talents-data.js','utf8').replace('const TALENTS','globalThis.TALENTS'));console.log(JSON.stringify(TALENTS))"],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)

def convert(src):
    old = load_js(); new = {}; build = None
    for c in CLASSES:
        d = json.load(open(f"{src}/public/data/classes/{c}.json", encoding="utf-8"))
        build = d["build"]
        trees = []
        for tr in d["trees"]:
            # un même sort présent deux fois dans un arbre = ancien nœud resté dans le client : on garde le plus récent
            best = {}
            for x in tr["talents"]:
                k = tuple(x["spells"][:1]) or x["id"]
                if k not in best or x["id"] > best[k]["id"]: best[k] = x
            tr["talents"] = [x for x in tr["talents"] if best[tuple(x["spells"][:1]) or x["id"]] is x]
            ids = {x["id"]: slug(x["name"]) for x in tr["talents"]}
            ts = []
            for x in sorted(tr["talents"], key=lambda x: (x["tier"], x["col"])):
                cl = x.get("classic") or {}
                o = cl["ranks"][-1] if cl.get("ranks") and cl["ranks"][-1] != x["ranks"][-1] else None
                if o and cl.get("name") and cl["name"] != x["name"]: o = f'{cl["name"]} : {o}'
                p = [[ids[x["prereq"]["id"]], x["prereq"]["rank"]]] if x.get("prereq") else []
                ts.append({"id": slug(x["name"]), "n": x["name"], "r": x["tier"], "c": x["col"], "m": len(x["ranks"]), "p": p,
                           "t": x["ranks"], "s": STATUS.get(x["status"], "changed"), "a": 1 if x.get("active") else 0, "q": None, "o": o,
                           "i": (x.get("icon") or "").rstrip(".")})
            trees.append({"n": tr["name"], "cols": 4, "rows": max(t["r"] for t in ts) + 1, "i": tr["icon"], "t": ts})
        new[c] = {"color": old[c]["color"], "trees": trees}
    num = build.split(".")[-1]
    head = (f"/* Données de talents WoW Forever (build {num}, mises à jour le {__import__('datetime').date.today().strftime('%d/%m/%Y')})\n"
            "   Source : données du client du jeu extraites par forever-forge.com. Textes des talents en anglais.\n"
            "   Talents et icônes : World of Warcraft © Blizzard Entertainment. */\n")
    open("js/talents-data.js", "w", encoding="utf-8").write(head + "const TALENTS=" + json.dumps(new, ensure_ascii=False, separators=(",", ":")) + ";\n")
    json.dump(old, open("/tmp/talents-old.json", "w"))
    # résumé des changements
    for c in CLASSES:
        for to, tn in zip(old[c]["trees"], new[c]["trees"]):
            a = {t["id"]: t for t in to["t"]}; b = {t["id"]: t for t in tn["t"]}
            gone = sorted(set(a) - set(b)); added = sorted(set(b) - set(a))
            mod = [k for k in set(a) & set(b) if (a[k]["r"], a[k]["c"], a[k]["m"], a[k]["t"]) != (b[k]["r"], b[k]["c"], b[k]["m"], b[k]["t"])]
            if gone or added or mod: print(f"{c}/{tn['n']}: -{gone} +{added} ~{len(mod)}")
    print("build", build)

def decode(T, code):
    c, *parts = code.split("-")
    alloc = {}
    for ti, tr in enumerate(T[c]["trees"]):
        s = parts[ti] if ti < len(parts) else ""
        for i, t in enumerate(tr["t"]):
            r = B36.index(s[i]) if i < len(s) else 0
            if r: alloc[(ti, t["id"])] = min(r, t["m"])
    return c, alloc

def encode(T, c, alloc):
    return c + "-" + "-".join("".join(B36[alloc.get((ti, t["id"]), 0)] for t in tr["t"]).rstrip("0") for ti, tr in enumerate(T[c]["trees"]))

def check(T, c, alloc):
    errs = []
    for ti, tr in enumerate(T[c]["trees"]):
        byid = {t["id"]: t for t in tr["t"]}
        for t in tr["t"]:
            r = alloc.get((ti, t["id"]), 0)
            if not r: continue
            below = sum(v for (i, k), v in alloc.items() if i == ti and byid.get(k) and byid[k]["r"] < t["r"])
            if below < t["r"] * 5: errs.append(f'{t["n"]}: palier ({below}/{t["r"]*5})')
            for pid, pr in t["p"]:
                if alloc.get((ti, pid), 0) < pr: errs.append(f'{t["n"]}: prérequis {pid} {pr}')
    return errs

def builds():
    old = json.load(open("/tmp/talents-old.json")); new = load_js()
    B = json.load(open("tools/builds.json", encoding="utf-8"))
    for k, b in B.items():
        c, a = decode(old, b["code"])
        ids = {(ti, t["id"]) for ti, tr in enumerate(new[c]["trees"]) for t in tr["t"]}
        mx = {(ti, t["id"]): t["m"] for ti, tr in enumerate(new[c]["trees"]) for t in tr["t"]}
        where = {t["id"]: ti for ti, tr in enumerate(new[c]["trees"]) for t in tr["t"]}
        a = {(kk if kk in ids else (where.get(kk[1], kk[0]), kk[1])): v for kk, v in a.items()}  # talent passé dans un autre arbre
        lost = {kk: v for kk, v in a.items() if kk not in ids}
        na = {kk: min(v, mx[kk]) for kk, v in a.items() if kk in ids}
        total = sum(na.values()); errs = check(new, c, na)
        b["new_code"] = encode(new, c, na)
        print(k, "OK" if not lost and total == 51 and not errs else "À REVOIR", total, "perdus:", lost, errs[:4])
    json.dump(B, open("/tmp/builds-remap.json", "w"), ensure_ascii=False, indent=1)

if __name__ == "__main__":
    builds() if sys.argv[1] == "--builds" else convert(sys.argv[1])
