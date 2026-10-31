"""Génère les pages « Leveling pas à pas » à partir des guides de Polestar (GPL-3.0).

Usage : python3 tools/pas_a_pas.py <chemin du clone de https://github.com/fitzforge/polestar>
Les textes des guides et leur traduction française viennent de Polestar ; les noms
français (quêtes, PNJ, objets) de son module Polestar_frFR.
"""
import html, json, os, re, shlex, sys

ROOT = os.path.dirname(os.path.abspath(__file__)) + "/.."
PS = sys.argv[1] if len(sys.argv) > 1 else "polestar"
os.chdir(ROOT)

GUIDES = [  # (slug page, fichier guide, race(s), faction)
    ("elwynn", "forever/alliance/human/01-elwynn-forest", "Humain", "a"),
    ("dun-morogh", "forever/alliance/dwarf-gnome/01-dun-morogh", "Nain et Gnome", "a"),
    ("teldrassil", "forever/alliance/nightelf/01-teldrassil", "Elfe de la nuit", "a"),
    ("zephras-alliance", "forever/alliance/skyborne/01-zephras-isle", "Éolide (Alliance)", "a"),
    ("durotar", "forever/horde/orc-troll/01-durotar", "Orc et Troll", "h"),
    ("mulgore", "forever/horde/tauren/01-mulgore", "Tauren", "h"),
    ("tirisfal", "forever/horde/undead/01-tirisfal-glades", "Mort-vivant", "h"),
    ("zephras-horde", "forever/horde/skyborne/01-zephras-isle", "Éolide (Horde)", "h"),
]
ZONES = {"Alterac Mountains": "Montagnes d'Alterac", "Darkshore": "Sombrivage", "Darnassus": "Darnassus", "Dun Morogh": "Dun Morogh",
 "Durotar": "Durotar", "Elwynn Forest": "Forêt d'Elwynn", "Ironforge": "Forgefer", "Loch Modan": "Loch Modan", "Moonglade": "Reflet-de-Lune",
 "Mulgore": "Mulgore", "Orgrimmar": "Orgrimmar", "Stormwind City": "Hurlevent", "Teldrassil": "Teldrassil", "The Barrens": "Les Tarides",
 "Thunder Bluff": "Les Pitons-du-Tonnerre", "Tirisfal Glades": "Clairières de Tirisfal", "Undercity": "Fossoyeuse", "Zephras Isle": "Île de Zéphras"}
PLACES = {"Auberdine": "Auberdine", "Crossroads": "La Croisée", "The Crossroads": "La Croisée", "Ironforge": "Forgefer",
 "Rut'theran Village": "Rut'theran", "Thunder Bluff": "Les Pitons-du-Tonnerre", "Moonglade": "Reflet-de-Lune", "Thelsamar": "Thelsamar",
 "Bloodhoof Village": "Sabot-de-Sang", "Dolanaar": "Dolanaar", "Gallows' End Tavern": "l'auberge de Brill", "Goldshire": "Comté-de-l'Or",
 "Thunderbrew Distillery": "l'auberge de Kharanos", "Razor Hill": "Tranchecolline", "Stormwind": "Hurlevent", "Orgrimmar": "Orgrimmar"}
ZONES.update({"Westfall": "Marche de l'Ouest", "Redridge Mountains": "Les Carmines", "Duskwood": "Bois de la Pénombre", "Wetlands": "Les Paluns",
 "Silverpine Forest": "Forêt des Pins-Argentés", "Stonetalon Mountains": "Les Serres-Rocheuses", "Ashenvale": "Orneval", "Hillsbrad Foothills": "Contreforts de Hautebrande",
 "Stormwind": "Hurlevent", "Thousand Needles": "Mille pointes", "Desolace": "Désolace", "Dustwallow Marsh": "Marécage d'Âprefange", "Feralas": "Féralas",
 "Stranglethorn Vale": "Vallée de Strangleronce", "Arathi Highlands": "Hautes-terres d'Arathi", "Badlands": "Terres ingrates", "Searing Gorge": "Gorge des Vents brûlants",
 "Burning Steppes": "Steppes ardentes", "Felwood": "Gangrebois", "Winterspring": "Berceau-de-l'Hiver", "Azshara": "Azshara", "Tanaris": "Tanaris", "Silithus": "Silithus",
 "Un'Goro Crater": "Cratère d'Un'Goro", "The Hinterlands": "Les Hinterlands", "Western Plaguelands": "Maleterres de l'Ouest", "Eastern Plaguelands": "Maleterres de l'Est",
 "Swamp of Sorrows": "Marais des Chagrins", "Blasted Lands": "Terres foudroyées", "Deadwind Pass": "Défilé de Deuillevent", "Dun Morogh": "Dun Morogh", "Loch Modan": "Loch Modan"})
COND = {"Warrior": "Guerrier", "Paladin": "Paladin", "Hunter": "Chasseur", "Rogue": "Voleur", "Priest": "Prêtre", "Shaman": "Chaman",
 "Mage": "Mage", "Warlock": "Démoniste", "Druid": "Druide", "Human": "Humain", "Dwarf": "Nain", "Gnome": "Gnome", "Night Elf": "Elfe de la nuit",
 "NightElf": "Elfe de la nuit", "Orc": "Orc", "Troll": "Troll", "Tauren": "Tauren", "Undead": "Mort-vivant", "Skyborne": "Éolide", "Alliance": "Alliance", "Horde": "Horde"}
CLASSES = ["Warrior", "Paladin", "Hunter", "Rogue", "Priest", "Shaman", "Mage", "Warlock", "Druid"]
FILTER = [CLASSES]
PROF = {"Alchemy": "Alchimie", "Blacksmithing": "Forge", "Cooking": "Cuisine", "Enchanting": "Enchantement", "Engineering": "Ingénierie",
 "First Aid": "Secourisme", "Fishing": "Pêche", "Herbalism": "Herboristerie", "Leatherworking": "Travail du cuir", "Mining": "Minage",
 "Skinning": "Dépeçage", "Tailoring": "Couture", "Riding": "Monte"}
SKILL_FR = {"171": "Alchimie", "164": "Forge", "185": "Cuisine", "333": "Enchantement", "202": "Ingénierie", "129": "Secourisme", "356": "Pêche",
 "182": "Herboristerie", "165": "Travail du cuir", "186": "Minage", "393": "Dépeçage", "197": "Couture", "762": "Monte"}
RANK = {"Apprentice": "Apprenti", "Journeyman": "Compagnon", "Expert": "Expert", "Artisan": "Artisan"}

# Lieux sans traduction dans les données (noms français du jeu)
PLACES_EXTRA = {}
_pe = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lieux_fr.json")
if os.path.exists(_pe): PLACES_EXTRA = json.load(open(_pe, encoding="utf-8"))
for _k, _v in PLACES_EXTRA.items(): PLACES.setdefault(_k, _v)

AREA_FR = {}

# ---------- noms français et anglais ----------
CRAFT, LEARN = {}, {}

FR = {}
txt = open(f"{PS}/addon/Polestar_frFR/Names.lua", encoding="utf-8").read()
for kind, body in re.findall(r'R\("(\w+)",\s*\d+,\s*\d+,\s*\[\[(.*?)\]\]\)', txt, re.S):
    for line in body.split("\n"):
        if "\t" in line:
            i, n = line.split("\t", 1)
            FR[(kind, i)] = re.sub(r"%([0-9A-Fa-f]{2})", lambda m: chr(int(m.group(1), 16)), n)
EN = {}
for kind, tab, key in [("quest", "quest", "title"), ("npc", "npc", "name"), ("item", "item", "name"), ("object", "object", "name")]:
    for line in open(f"{PS}/forever-db/data/{tab}.jsonl", encoding="utf-8"):
        r = json.loads(line)
        if key in r: EN[(kind, str(r["id"]))] = r[key]
KMAP = {"zone": "map"}
import glob as _gl
for _g in _gl.glob(f"{PS}/addon/Polestar_Guides*/Guides.lua"):
    _t = open(_g, encoding="utf-8").read()
    for m in re.finditer(r't = "craft", spell = (\d+), spellName = "[^"]*", item = (\d+)[^\n]*?reagents = \{(.*?)\} \}', _t):
        CRAFT[m.group(1)] = (m.group(2), re.findall(r"item = (\d+), itemName = \"[^\"]*\", count = (\d+)", m.group(3)))
    for m in re.finditer(r't = "craft", spell = (\d+), spellName = "[^"]*", item = (\d+)', _t):
        CRAFT.setdefault(m.group(1), (m.group(2), []))
    for m in re.finditer(r't = "learn", spell = (\d+), spellName = "([^"]*)"', _t):
        LEARN[m.group(1)] = m.group(2)

def fr_name(kind, i, fallback=""):
    return FR.get((KMAP.get(kind, kind), str(i))) or FR.get((kind, str(i))) or EN.get((kind, str(i))) or fallback or f"{kind} {i}"

def lua_str(s):
    return re.sub(r"\\(.)", lambda m: {"n": "\n", "t": "\t"}.get(m.group(1), m.group(1)), s)

def load_tr(guide):
    """Dictionnaire texte anglais (noms en clair) -> texte français (avec jetons {kind:id})."""
    p = f"{PS}/guides/locales/frFR/{guide}.lua"
    tr, names = {}, {}
    if not os.path.exists(p): return tr
    lines = open(p, encoding="utf-8").read().split("\n")
    for l in lines:
        for k, i, n in re.findall(r"\{(\w+):(\d+)\} ([^·{]+?)(?= ·|$)", l if re.match(r"\s*-- \{", l) and '"] =' not in l else ""):
            names[(k, i)] = n.strip()
            NAMES_EN[(k, i)] = n.strip()
    plural = {}
    for l in lines:
        m = re.match(r"\s*-- plural, as words: (.+?) = \{(\w+):(\d+)\}", l)
        if m: plural[m.group(1)] = 1
    for m in re.finditer(r'\["((?:[^"\\]|\\.)*)"\]\s*=\s*"((?:[^"\\]|\\.)*)"', "\n".join(lines)):
        k, v = lua_str(m.group(1)), lua_str(m.group(2))
        if not v: continue
        en = re.sub(r"\{(\w+):(\d+)\}", lambda t: names.get((t.group(1), t.group(2))) or EN.get((t.group(1), t.group(2)), t.group(0)), k)
        tr[en.strip()] = v
        tr[k.strip()] = v
        parts = re.split(r"(\{\w+:\d+\})", k.strip())
        rx = "".join("(.+?)" if re.fullmatch(r"\{\w+:\d+\}", x) else re.escape(x) for x in parts)
        toks = [x for x in parts if re.fullmatch(r"\{\w+:\d+\}", x)]
        PATTERNS.setdefault(guide, []).append((re.compile(rx + r"\.?$"), toks, v))
    return tr
PATTERNS = {}
NAMES_EN = {}
CUR = [None]

def render_fr(s, raw=None):
    s = html.escape(s, quote=False)
    raw = raw or {}
    def tok(t):
        k, i = t.group(1), t.group(2)
        if k == "skill":
            return html.escape(SKILL_FR.get(i, raw.get(t.group(0)) or NAMES_EN.get((k, i)) or f"métier {i}"))
        if k in ("zone", "area"):
            en = NAMES_EN.get((k, i)) or raw.get(t.group(0)) or ""
            n = html.escape(ZONES.get(en) or PLACES_EXTRA.get(en) or PLACES.get(en) or en or f"{k} {i}")
        else:
            n = html.escape(FR.get((k, i)) or raw.get(t.group(0)) or NAMES_EN.get((k, i)) or fr_name(k, i))
        if k == "quest": return f'<a class="q" href="https://www.wowhead.com/forever/quest={i}" target="_blank" rel="noopener">{n}</a>'
        return f"<b>{n}</b>"
    return re.sub(r"\{(\w+):(\d+)\}", tok, s)

REV = {}
for (k, i), n in EN.items():
    if (k, i) in FR or (KMAP.get(k, k), i) in FR:
        REV.setdefault(n.lower(), fr_name(k, i))
for en_, fr_ in PLACES_EXTRA.items():
    REV[en_.lower()] = fr_

def rev(en):
    """Nom anglais seul (PNJ, objet, quête, lieu) -> nom français, sinon None."""
    e = en.lower()
    for cand in (e, e[:-1] if e.endswith("s") else e, e[:-2] if e.endswith("es") else e):
        if cand in REV: return REV[cand]
    return None

def T(tr, en):
    en = en.strip().strip('"')
    for rx, toks, v in PATTERNS.get(CUR[0], []):
        m = rx.match(en)
        if m and len(m.groups()) == len(toks):
            okm = True
            for tk, cap in zip(toks, m.groups()):
                kk, ii = re.match(r"\{(\w+):(\d+)\}", tk).groups()
                known = NAMES_EN.get((kk, ii)) or EN.get((kk, ii))
                fw = lambda x: re.sub(r"('s|’s|s)$", "", (x.strip().lower().split() or [""])[0])
                if known and fw(cap) != fw(known) and fw(cap) not in known.lower() and fw(known) not in cap.lower():
                    okm = False; break
            if okm:
                return render_fr(v, dict(zip(toks, m.groups())))
    if en in tr: return render_fr(tr[en])
    r = rev(en)
    if r: return html.escape(r)
    if en in PLACES_EXTRA: return html.escape(PLACES_EXTRA[en])
    m = re.match(r"^(.+?) & (.+?): (.+?) \((\d+-\d+)\)$", en)
    if m:
        a, b, z, r_ = m.groups()
        return html.escape(f"{rev(a) or a} et {rev(b) or b} : {ZONES.get(z, PLACES_EXTRA.get(z, z))} ({r_})")
    for sep in (": ", ", "):
      if sep in en:
        a, b = en.split(sep, 1)
        ra, rb = rev(a) or PLACES_EXTRA.get(a), rev(b) or PLACES_EXTRA.get(b)
        if ra or rb: return html.escape((ra or a) + (" : " if sep == ": " else ", ") + (rb or b))
    MISS.add(en)
    return html.escape(en)
MISS = set()

# ---------- lecture d'un guide ----------
def parse(guide):
    head, steps, cur = {}, [], None
    for raw in open(f"{PS}/guides/{guide}.guide", encoding="utf-8"):
        line = raw.rstrip("\n")
        if not line.strip() or line.strip().startswith("#"): continue
        if not line.startswith(" "):
            w, _, rest = line.partition(" ")
            if w == "step":
                cur = {"title": rest.strip(), "items": [], "only": None, "tip": None}
                steps.append(cur)
            else:
                head[w] = rest.strip()
            continue
        body, _, comment = line.strip().partition(" -- ")
        cur["items"].append((body.strip(), comment.strip()))
    return head, steps

def split_only(parts):
    if "only" in parts:
        i = parts.index("only")
        return parts[:i], " ".join(parts[i + 1:])
    return parts, None

def cond_fr(c):
    out = []
    for x in [y.strip() for y in c.split(",") if y.strip()]:
        out.append(COND.get(x, x))
    return out

def goal(body, comment, tr):
    """Renvoie (html, classes concernées ou None) ; None si la ligne n'est pas affichée."""
    try: parts = shlex.split(body.replace("'", "’"))
    except ValueError: parts = body.split()
    parts = [p.replace("’", "'") for p in parts]
    parts, only = split_only(parts)
    kw, args = parts[0], parts[1:]
    num = next((a[1:] for a in args if re.fullmatch(r"x\d+", a)), None)
    at = next((a[1:] for a in args if a.startswith("@")), None)
    ident = args[0] if args and re.fullmatch(r"\d+", args[0]) else None
    quoted = next((a for a in args if not re.fullmatch(r"[@x]?[\d.,]+|quest|npc|object|item|nearest|r|lvl|class|map|era|live|choose|reward|xp|money", a)), None)
    ctext = T(tr, comment) if comment else ""
    cm = f' <span class="gc">— {ctext}</span>' if comment else ""
    pos = f' <span class="xy">{at.replace(",", ", ")}</span>' if at else ""
    q = lambda i: f'<a class="q" href="https://www.wowhead.com/forever/quest={i}" target="_blank" rel="noopener">{html.escape(fr_name("quest", i))}</a>'
    n = f"{num} × " if num else ""
    if kw == "accept" and ident: h = f'<span class="k acc">Accepter</span> {q(ident)}{cm}'
    elif kw == "turnin" and ident: h = f'<span class="k tin">Rendre</span> {q(ident)}{cm}'
    elif kw == "complete" and ident: h = f'<span class="k cpl">Terminer</span> {q(ident)}{pos}{cm}'
    elif kw == "abandon" and ident: h = f'<span class="k">Abandonner</span> {q(ident)}{cm}'
    elif kw == "kill":
        name = html.escape(fr_name("npc", ident)) if ident else html.escape(quoted or "")
        h = f'<span class="k kil">Tuer</span> {n}<b>{name}</b>{pos}{cm}'
    elif kw == "collect":
        name = html.escape(fr_name("item", ident)) if ident else html.escape(quoted or "")
        h = f'<span class="k col">Récupérer</span> {n}<b>{name}</b>{pos}{cm}'
    elif kw == "buy":
        name = html.escape(fr_name("item", ident)) if ident else html.escape(quoted or "")
        h = f'<span class="k">Acheter</span> {n}<b>{name}</b>{cm}'
    elif kw == "use": h = f'<span class="k">Utiliser</span> <b>{html.escape(fr_name("item", ident))}</b>{pos}{cm}'
    elif kw == "interact": h = f'<span class="k">Cliquer sur</span> <b>{html.escape(fr_name("object", ident))}</b>{pos}{cm}'
    elif kw == "talk": h = f'<span class="k">Parler à</span> <b>{html.escape(fr_name("npc", ident))}</b>{cm}'
    elif kw == "goto":
        xy = args[0].replace(",", ", ") if args else ""
        h = f'<span class="k go">Aller</span> {("à <b>" + T(tr, quoted) + "</b> ") if quoted else ""}<span class="xy">{xy}</span>{cm}'
    elif kw == "train" and args and args[0] in PROF:
        rk = RANK.get(args[1], args[1]) if len(args) > 1 else ""
        h = f'<span class="k">Apprendre</span> <b>{PROF[args[0]]}</b> ({rk}) auprès d\'un maître du métier{cm}'
    elif kw == "train": h = f'<span class="k">Voir</span> le maître de classe et apprendre les nouveaux sorts{cm}'
    elif kw == "skill":
        pr = " ".join(a for a in args if not a.isdigit()); lvn = next((a for a in args if a.isdigit()), "")
        h = f'<span class="k">Atteindre</span> <b>{PROF.get(pr, pr)} {lvn}</b>{cm}'
    elif kw == "craft" and ident:
        it, reag = CRAFT.get(ident, (None, []))
        nm = html.escape(fr_name("item", it)) if it else f"recette {ident}"
        till = args[args.index("until") + 1] if "until" in args else None
        how = f" jusqu'à {till}" if till else (f" ×{num}" if num else "")
        rg = ", ".join(f"{c} {html.escape(fr_name('item', i))}" for i, c in reag)
        h = f'<span class="k craft">Fabriquer</span> <b>{nm}</b>{how}' + (f' <span class="gc">(par fabrication : {rg})</span>' if rg else "") + cm
    elif kw == "learn" and ident:
        it = CRAFT.get(ident, (None, []))[0]
        nm = fr_name("item", it) if it else (rev(LEARN.get(ident, "")) or LEARN.get(ident) or f"recette {ident}")
        h = f'<span class="k">Apprendre</span> la recette <b>{html.escape(nm)}</b>{cm}'
    elif kw == "vendor": h = f'<span class="k">Vendre et réparer</span>{cm}'
    elif kw == "sethome": h = f'<span class="k">Pierre de foyer</span> à lier à {html.escape(PLACES.get(quoted, quoted or ""))}{cm}'
    elif kw == "hearth": h = f'<span class="k">Utiliser</span> la pierre de foyer vers {html.escape(PLACES.get(quoted, quoted or ""))}{cm}'
    elif kw == "getfp": h = f'<span class="k">Apprendre</span> le trajet aérien de {html.escape(PLACES.get(quoted, quoted or ""))}{cm}'
    elif kw == "fly": h = f'<span class="k">S\'envoler</span> vers {html.escape(PLACES.get(quoted, quoted or ""))}{cm}'
    elif kw == "level": h = f'<span class="k">Atteindre</span> le niveau {args[0]}{cm}'
    elif kw == "note": h = f'<span class="k">Note</span> {T(tr, " ".join(args))}'
    else: return None
    if ctext and ident and kw in ("accept", "turnin"):
        qn = html.escape(fr_name("quest", ident))
        if ctext.endswith(" : " + qn):
            ctext2 = ctext[: -len(" : " + qn)]
            h = h.replace(cm, f' <span class="gc">— {ctext2}</span>'); cm = f' <span class="gc">— {ctext2}</span>'; ctext = ctext2
    if ctext:
        plain = re.sub(r"<[^>]+>", "", ctext).strip().lower()
        body_plain = re.sub(r"<[^>]+>", "", h.replace(cm, "")).lower()
        if plain and (plain in body_plain or plain.rstrip("s") in body_plain): h = h.replace(cm, "")
    return h, only

def build(slug, guide, race, fac):
    head, steps = parse(guide)
    CUR[0] = guide
    tr = load_tr(guide)
    out, used = [], set()
    for idx, s in enumerate(steps, 1):
        items, step_only, tips, zone = [], None, [], None
        for body, comment in s["items"]:
            kw = body.split(" ")[0] if body else ""
            if kw == "tip": tips.append(T(tr, body[4:])); continue
            if kw == "only": step_only = body[5:]; continue
            if kw == "zone": zone = ZONES.get(body[5:].strip(), body[5:].strip()); continue
            if kw in ("when", "along", "loop", "label", "skipto", "coords", "r", "image", "until"): continue
            g = goal(body, comment, tr)
            if not g: continue
            h, only = g
            cls = cond_fr(only) if only else []
            data = " ".join(c for c in (only or "").replace(" ", "").split(",") if c in FILTER[0])
            used.update(data.split())
            tag = "".join(f'<span class="only">{c}</span>' for c in cls)
            items.append(f'<li{" data-only=\"" + data + "\"" if data else ""}>{h}{tag}</li>')
        if not items and not tips: continue
        sdata = " ".join(c for c in (step_only or "").replace(" ", "").split(",") if c in FILTER[0])
        stag = "".join(f'<span class="only">{c}</span>' for c in cond_fr(step_only)) if step_only else ""
        title = T(tr, s["title"]) if s["title"] else f"Étape {idx}"
        out.append(f'''<li class="pp-st"{" data-only=\"" + sdata + "\"" if sdata else ""}><label class="st-h"><input type="checkbox"><span class="st-n"></span><span class="st-t">{title}</span>{stag}{f' <span class="st-z">{zone}</span>' if zone else ""}</label>
{"".join(f'<p class="pp-tip">{t}</p>' for t in tips)}<ul class="ppg">{"".join(items)}</ul></li>''')
    return head, "\n".join(out)

def page(title, desc, body, extra=""):
    t = open("legacy.html", encoding="utf-8").read()
    h = t[:t.index("<main>")]
    h = re.sub(r"<title>.*?</title>", f"<title>{title} – ForeverWoW</title>", h)
    h = re.sub(r'name="description" content=".*?"', f'name="description" content="{desc}"', h)
    tail = re.sub(r'<script src="js/heritage\.js[^"]*"></script>\n?', extra, t[t.index("</main>"):])
    return h + body + tail

CREDIT = '''<p class="small" style="margin-top:22px">Route et textes : <a href="https://polestar.guide/guides" target="_blank" rel="noopener">Polestar</a>, addon communautaire gratuit (code source sur <a href="https://github.com/fitzforge/polestar" target="_blank" rel="noopener">GitHub</a>), traduction française de ses contributeurs. Ces pages reprennent ses guides et sont donc, comme eux, sous licence <a href="https://www.gnu.org/licenses/gpl-3.0.fr.html" target="_blank" rel="noopener">GNU GPL v3</a>. Noms des quêtes, PNJ et objets : données du jeu © Blizzard Entertainment. Routes de la bêta, susceptibles d'évoluer.</p>'''
SCRIPTS = '<script src="js/pasapas.js"></script>\n<script>const whTooltips = {colorLinks: true, iconizeLinks: true, renameLinks: false};</script>\n<script src="https://wow.zamimg.com/js/tooltips.js"></script>\n'

EXTRA = [  # niveaux 10-30 : (slug, guide, public, faction)
    ("barrens-orc-troll", "forever/horde/orc-troll/02-the-barrens", "Orc et Troll", "h"),
    ("marche-de-l-ouest", "forever/alliance/02-westfall", "Alliance", "a"),
    ("sombrivage", "forever/alliance/03-darkshore", "Alliance", "a"),
    ("carmines", "forever/alliance/04-redridge-mountains", "Alliance", "a"),
    ("bois-de-la-penombre", "forever/alliance/05-duskwood", "Alliance", "a"),
    ("orneval-alliance", "forever/alliance/06-ashenvale", "Alliance", "a"),
    ("mille-pointes-alliance", "forever/alliance/07-thousand-needles", "Alliance", "a"),
    ("tarides", "forever/horde/02-the-barrens", "Horde", "h"),
    ("pins-argentes", "forever/horde/03-silverpine-forest", "Horde", "h"),
    ("tarides-2", "forever/horde/04-the-barrens", "Horde", "h"),
    ("serres-rocheuses", "forever/horde/05-stonetalon-mountains", "Horde", "h"),
    ("hautebrande", "forever/horde/06-hillsbrad-foothills", "Horde", "h"),
    ("orneval-horde", "forever/horde/07-ashenvale", "Horde", "h"),
]
import glob as _glob
for _fac, _f in (("alliance", "a"), ("horde", "h")):
    for _t in ("30-40", "40-50", "50-60"):
        for _p in sorted(_glob.glob(f"{PS}/guides/forever/{_fac}/{_t}/*.guide")):
            _n = os.path.basename(_p)[:-6]
            EXTRA.append((f"{_fac}-{_t}-{_n}", f"forever/{_fac}/{_t}/{_n}", "Alliance" if _f == "a" else "Horde", _f))

def tranche(guide):
    lv = parse(guide)[0].get("levels", "1-1")
    lo = int(re.match(r"\d+", lv).group(0))
    return "1530" if lo < 30 else "3040" if lo < 40 else "4050" if lo < 50 else "5060"

ALL = [g + ("depart",) for g in GUIDES] + [g + (tranche(g[1]),) for g in EXTRA]
SLUG = {g[1]: g[0] for g in ALL}

def ztitle(t):
    parts = re.split(r", | & ", t)
    fr = [ZONES.get(x, PLACES_EXTRA.get(x, x)) for x in parts]
    return fr[0] if len(fr) == 1 else ", ".join(fr[:-1]) + " et " + fr[-1]

GROUPS = [("depart", "Zones de départ (niveaux 1 à 15)"), ("1530", "Niveaux 15 à 30"), ("3040", "Niveaux 30 à 40"), ("4050", "Niveaux 40 à 50"), ("5060", "Niveaux 50 à 60")]
cards = {g: {"a": "", "h": ""} for g, _ in GROUPS}
SEEN = {}
for slug, guide, race, fac, grp in ALL:
    head, steps = build(slug, guide, race, fac)
    zone = ztitle(head.get("title", ""))
    _k = (fac, zone)
    if race != "Orc et Troll":
        SEEN[_k] = SEEN.get(_k, 0) + 1
        if SEEN[_k] > 1: zone += f" ({SEEN[_k]}e passage)"
    lv = head.get("levels", "")
    nx = head.get("next", "")
    if nx in SLUG:
        nhead, _ = parse(nx)
        nxt, nlabel = f"pas-a-pas-{SLUG[nx]}.html", f"Zone suivante : {ztitle(nhead.get('title', ''))} →"
    else:
        nxt, nlabel = "leveling.html", "La suite du parcours 1-60 →"
    lead = "La route complète de ta zone de départ, étape par étape." if grp == "depart" else "La route complète de cette étape du leveling, quête par quête."
    body = f'''<main><div class="wrap">
<div class="crumbs"><a href="index.html">News</a> › <a href="pas-a-pas.html">Leveling pas à pas</a> › {html.escape(zone)}</div>
<h1 class="page-title">{html.escape(zone)} <span class="pp-lv">niveaux {lv}</span></h1>
<p class="page-lead"><span class="race {fac}">{race}</span> {lead} Coche chaque étape terminée : ta progression est gardée dans ton navigateur.</p>
<div class="pp-bar" data-guide="{slug}">
  <label>Ta classe : <select id="pp-class"><option value="">Toutes</option>{"".join(f'<option value="{c}">{COND[c]}</option>' for c in CLASSES)}</select></label>
  <div class="pp-prog"><div class="pp-fill"></div></div><span class="pp-count"></span>
  <button type="button" id="pp-reset">Tout décocher</button>
</div>
<div class="info">Les coordonnées (comme <span class="xy">48.9, 41.6</span>) se lisent sur la carte du jeu ou avec un addon comme <a href="addons.html">TomTom</a>. Passe la souris sur une quête pour voir sa description.</div>
<ol class="pp">{steps}</ol>
<div class="pp-next"><a class="btn-link" href="pas-a-pas.html">← Toutes les zones</a> <a class="btn-link" href="{nxt}">{html.escape(nlabel)}</a></div>
{CREDIT}
</div>'''
    open(f"pas-a-pas-{slug}.html", "w", encoding="utf-8").write(page(f"{zone} pas à pas", f"Guide de leveling pas à pas de {zone} ({race}) dans WoW Forever, niveaux {lv}.", body, SCRIPTS))
    cards[grp][fac] += f'<a class="pp-card" href="pas-a-pas-{slug}.html"><span class="race {fac}">{race}</span><b>{html.escape(zone)}</b><span class="small">niveaux {lv}</span></a>'
    print(slug, steps.count('class="pp-st"'), "étapes")

hub = f'''<main><div class="wrap">
<div class="crumbs"><a href="index.html">News</a> › Leveling pas à pas</div>
<h1 class="page-title">Leveling pas à pas</h1>
<p class="page-lead">Chaque quête dans le bon ordre, avec les monstres à tuer, les objets à ramasser et les endroits où aller. Commence par la zone de départ de ta race : à la fin de chaque page, un bouton t'emmène à la zone suivante. Le <a href="leveling.html">parcours 1-60</a> donne la vue d'ensemble jusqu'au niveau 60.</p>
{"".join(f'<h2 id="t{g}">{t}</h2><h3 class="pp-fac">Alliance</h3><div class="pp-cards">{cards[g]["a"]}</div><h3 class="pp-fac">Horde</h3><div class="pp-cards">{cards[g]["h"]}</div>' for g, t in GROUPS)}
<div class="info" style="margin-top:20px">Tu préfères être guidé directement en jeu ? Installe l'addon <a href="addons.html">Polestar</a> : les mêmes routes s'affichent avec une flèche vers chaque objectif.</div>
{CREDIT}
</div>'''
open("pas-a-pas.html", "w", encoding="utf-8").write(page("Leveling pas à pas", "Guides de leveling pas à pas de WoW Forever en français : du niveau 1 au niveau 60, pour l'Alliance et la Horde.", hub))
# ---------- Métiers pas à pas ----------
FILTER[0] = ["Alliance", "Horde"]
METIERS = [("alchimie", "alchemy", "Alchimie"), ("forge", "blacksmithing", "Forge"), ("enchantement", "enchanting", "Enchantement"),
 ("ingenierie", "engineering", "Ingénierie"), ("travail-du-cuir", "leatherworking", "Travail du cuir"), ("couture", "tailoring", "Couture"),
 ("herboristerie", "herbalism", "Herboristerie"), ("minage", "mining", "Minage"), ("depecage", "skinning", "Dépeçage"),
 ("cuisine", "cooking", "Cuisine"), ("secourisme", "first-aid", "Secourisme"), ("peche", "fishing", "Pêche")]
ICON = {"alchimie": "alchimie", "forge": "forge", "enchantement": "enchantement", "ingenierie": "ingenierie", "travail-du-cuir": "cuir",
 "couture": "couture", "herboristerie": "herboristerie", "minage": "minage", "depecage": "depecage", "cuisine": "cuisine", "secourisme": "secourisme", "peche": "peche"}
mcards = ""
for slug, src, nom in METIERS:
    g = f"forever/professions/{src}"
    if not os.path.exists(f"{PS}/guides/{g}.guide"): continue
    head, steps = build("metier-" + slug, g, nom, "a")
    lv = head.get("levels", "")
    body = f'''<main><div class="wrap">
<div class="crumbs"><a href="index.html">News</a> › <a href="metiers-pas-a-pas.html">Métiers pas à pas</a> › {nom}</div>
<h1 class="page-title">{nom} 1-300 <span class="pp-lv">pas à pas</span></h1>
<p class="page-lead">La montée complète de {nom.lower() if nom != "Ingénierie" else "l'ingénierie"}, de 1 à 300 : où apprendre, quoi acheter ou récolter, et quoi fabriquer à chaque palier. Coche chaque étape terminée : ta progression est gardée dans ton navigateur.</p>
<div class="pp-bar" data-guide="metier-{slug}" data-fkey="faction">
  <label>Ta faction : <select id="pp-class"><option value="">Les deux</option><option value="Alliance">Alliance</option><option value="Horde">Horde</option></select></label>
  <div class="pp-prog"><div class="pp-fill"></div></div><span class="pp-count"></span>
  <button type="button" id="pp-reset">Tout décocher</button>
</div>
<div class="info">Couleur des recettes : <b>orange</b> = un point à chaque fabrication, <b>jaune</b> = souvent, <b>vert</b> = rarement, <b>gris</b> = jamais. Les quantités sont des estimations : garde un peu de marge. Rappel : l'<a href="legacy.html">Héritage</a> récompense les paliers 150, 225 et 300.</div>
<ol class="pp">{steps}</ol>
<div class="pp-next"><a class="btn-link" href="metiers-pas-a-pas.html">← Tous les métiers</a> <a class="btn-link" href="metiers.html">La page Métiers →</a></div>
{CREDIT}
</div>'''
    open(f"metier-{slug}.html", "w", encoding="utf-8").write(page(f"{nom} 1-300 pas à pas", f"Guide pas à pas pour monter {nom} de 1 à 300 dans WoW Forever : recettes, composants, où apprendre.", body, SCRIPTS))
    img = f'<img src="images/metiers/{ICON[slug]}.png" alt="" class="mc-ic">' if os.path.exists(f"images/metiers/{ICON[slug]}.png") else ""
    nst = steps.count('class="pp-st"')
    mcards += f'<a class="pp-card" href="metier-{slug}.html">{img}<b>{nom}</b><span class="small">1 à 300 · {nst} étapes</span></a>'
    print("metier", slug, nst, "étapes")
hubm = f'''<main><div class="wrap">
<div class="crumbs"><a href="index.html">News</a> › <a href="metiers.html">Métiers</a> › Métiers pas à pas</div>
<h1 class="page-title">Métiers pas à pas 1-300</h1>
<p class="page-lead">Les 12 métiers de WoW Forever, de 1 à 300, étape par étape : où apprendre chaque rang, quels composants acheter ou récolter et quelles recettes fabriquer pour monter au plus vite. Choisis ta faction en haut de chaque guide pour ne voir que tes étapes.</p>
<div class="pp-cards">{mcards}</div>
<div class="info" style="margin-top:20px">Les nouveautés des métiers dans Forever (camping, Faveur marchande, objets de camp) sont expliquées sur la page <a href="metiers.html">Métiers</a> et la page <a href="reputations.html">Réputations</a>.</div>
{CREDIT}
</div>'''
open("metiers-pas-a-pas.html", "w", encoding="utf-8").write(page("Métiers pas à pas 1-300", "Guides pas à pas des 12 métiers de WoW Forever, de 1 à 300, en français : alchimie, forge, enchantement, ingénierie, couture, minage...", hubm))

json.dump(sorted(MISS), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lieux_manquants.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(len(MISS), "textes restés en anglais (tools/lieux_manquants.json)")
