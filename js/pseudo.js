/* Générateur de pseudo WoW Forever : syllabes originales par race, règles de nommage du jeu */
(() => {
  const R = {
    humain: { d: ["Al", "Bren", "Cael", "Dar", "Ed", "Gar", "Hal", "Mar", "Ros", "Wil", "Tor", "Ced", "Ar", "Bel", "Cor", "Lan", "Ves", "Rod"],
      m: ["ric", "wyn", "ford", "ton", "bert", "mund", "ard", "ell", "an", "ias", "en", "dric", "mar", "rick", "ias", "wald"],
      f: ["a", "elle", "ine", "wyn", "ara", "ette", "ia", "eline", "ise", "anne", "ora", "ynn"] },
    nain: { d: ["Bal", "Brom", "Dur", "Grim", "Thor", "Mag", "Kar", "Bof", "Thra", "Grun", "Hrod", "Bram", "Dag", "Ost", "Rur", "Kaz"],
      m: ["in", "ar", "dur", "grim", "nir", "rak", "olf", "ek", "dain", "bek", "mir", "gar", "dok", "rum"],
      f: ["a", "ra", "hilda", "dis", "una", "gret", "ild", "wyn", "bera", "dra", "ana"] },
    elfe: { d: ["Ael", "Syl", "Ith", "Lor", "Mae", "Shan", "Thal", "Ely", "Ny", "Ari", "Cel", "Faer", "Il", "Ma", "Tyr", "Va"],
      m: ["andris", "ithil", "orn", "anor", "ael", "dris", "ion", "alas", "erin", "oran", "ethas", "iel", "anar"],
      f: ["ara", "elle", "iel", "yssa", "ana", "ria", "athe", "ienne", "ira", "eth", "ya", "aria"] },
    gnome: { d: ["Fizz", "Bink", "Gim", "Tink", "Nix", "Wiz", "Spark", "Pip", "Zap", "Cog", "Bop", "Mek", "Jin", "Wob", "Fid"],
      m: ["le", "wick", "bolt", "sprock", "gig", "ix", "bit", "fuse", "nut", "zap", "dle", "ble", "mo"],
      f: ["le", "ette", "bit", "y", "ina", "pip", "ia", "wick", "sy", "ella", "ix"] },
    eolide: { d: ["Aer", "Zeph", "Ven", "Lyr", "Cir", "Ael", "Sha", "Ra", "Ny", "Ha", "Ilu", "Eo", "Vaa", "Thae", "Ori", "Sae"],
      m: ["aal", "aris", "ondo", "aan", "iel", "oras", "eel", "uun", "ael", "andor", "ith", "aar"],
      f: ["yra", "aa", "iel", "elia", "aara", "ynn", "aleh", "ia", "eela", "ora", "ina", "aya"] },
    orc: { d: ["Gro", "Thra", "Kar", "Mok", "Zug", "Dur", "Nar", "Grak", "Ur", "Gul", "Rok", "Brak", "Dra", "Zar", "Gor", "Kro"],
      m: ["gash", "thar", "rok", "nash", "gor", "ak", "zug", "dan", "mok", "grim", "tar", "ruk", "gul", "nak"],
      f: ["a", "ka", "ra", "ga", "sha", "ruka", "gra", "za", "dra", "kha", "na"] },
    troll: { d: ["Zul", "Vol", "Jin", "Ra", "Zal", "Tak", "Mo", "Kaz", "Ze", "Ju", "Shi", "Ven", "Ha", "Ro", "Ya"],
      m: ["jin", "kaz", "zan", "tah", "mu", "ji", "jak", "rok", "zek", "dok", "tal", "mon"],
      f: ["ja", "ka", "ri", "zi", "la", "jah", "shi", "na", "ra", "tali", "mah"] },
    tauren: { d: ["Ha", "Ma", "Ta", "Ka", "Ne", "Te", "Ho", "Ba", "Mu", "To", "Hu", "Sa", "Ko", "Ahu"],
      m: ["ruk", "wak", "lo", "tah", "nok", "mah", "kon", "rak", "tu", "gan", "hoka", "wan"],
      f: ["la", "ni", "wa", "mah", "ra", "na", "hee", "ka", "tie", "ya", "lu"] },
    mortvivant: { d: ["Mor", "Vex", "Sil", "Grav", "Ash", "Mal", "Cre", "Del", "Vor", "Nec", "Bel", "Cal", "Dre", "Lur", "Sev"],
      m: ["ius", "wick", "ane", "ith", "ex", "ard", "ys", "ric", "on", "gar", "ath", "ren"],
      f: ["ora", "ia", "ys", "elle", "ine", "ith", "ane", "ette", "ara", "ys", "ina"] }
  };
  const NOMS = { humain: "Humain", nain: "Nain", elfe: "Elfe de la nuit", gnome: "Gnome", eolide: "Éolide", orc: "Orc", troll: "Troll", tauren: "Tauren", mortvivant: "Mort-vivant" };
  const FAC = { humain: "a", nain: "a", elfe: "a", gnome: "a", eolide: "s", orc: "h", troll: "h", tauren: "h", mortvivant: "h" };
  const pick = a => a[Math.floor(Math.random() * a.length)];
  const ok = n => n.length >= 3 && n.length <= 12 && !/(.)\1\1/i.test(n) && !/[aeiouy]{3}/i.test(n) && !/([a-z]{2,})\1/i.test(n) && !BAD.test(n);
  const BAD = /moron|nazi|pute|merd|bite|^cul|cul$|^con|conn|fuck|shit|niqu|salop|nigg|rape|sex|porn|anus|penis|pd$|pede|kkk|hitler|chier|crott|zizi|negr/i;
  const V = /[aeiouy]$/i, V0 = /^[aeiouy]/i;
  const join = (a, b) => a + (V.test(a) && V0.test(b) ? pick(["l", "r", "n", "th", "s", "v"]) : "") + b;

  function nom(race, sexe) {
    const r = R[race];
    for (let i = 0; i < 50; i++) {
      let n = pick(r.d);
      if (Math.random() < 0.2) n = join(n, pick(r.d).toLowerCase());
      n = join(n, pick(sexe === "f" ? r.f : r.m));
      n = n.charAt(0).toUpperCase() + n.slice(1).toLowerCase();
      if (ok(n)) return n;
    }
    return "Aventurier";
  }

  const $ = id => document.getElementById(id);
  const KEY = "wowforever-pseudos-favoris";
  const get = () => { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { return []; } };
  const save = v => { try { localStorage.setItem(KEY, JSON.stringify(v)); } catch (e) {} };
  let favs = get();

  function copier(n, el) {
    const done = () => { el.classList.add("copied"); setTimeout(() => el.classList.remove("copied"), 900); };
    if (navigator.clipboard) navigator.clipboard.writeText(n).then(done, done); else done();
  }
  function renderFavs() {
    $("ps-favs").innerHTML = favs.length
      ? favs.map(f => `<span class="ps-fav"><b>${f.n}</b> <span class="race ${FAC[f.r]}">${NOMS[f.r]}</span><button type="button" data-del="${f.n}" aria-label="Retirer">×</button></span>`).join("")
      : '<span class="small">Clique sur ☆ à côté d\'un pseudo pour le garder ici.</span>';
  }
  function generer() {
    const race = $("ps-race").value, sexe = $("ps-sexe").value;
    const races = race === "toutes" ? Object.keys(R) : [race];
    const set = new Set();
    const out = [];
    while (out.length < 12) {
      const r = pick(races), s = sexe === "x" ? pick(["m", "f"]) : sexe, n = nom(r, s);
      if (!set.has(n)) { set.add(n); out.push({ n, r }); }
    }
    $("ps-list").innerHTML = out.map(o => `<li><button type="button" class="ps-name" data-n="${o.n}" title="Copier">${o.n}</button><span class="race ${FAC[o.r]}">${NOMS[o.r]}</span><button type="button" class="ps-star" data-n="${o.n}" data-r="${o.r}" aria-label="Garder">${favs.some(f => f.n === o.n) ? "★" : "☆"}</button></li>`).join("");
  }
  $("ps-go").addEventListener("click", generer);
  $("ps-race").addEventListener("change", generer);
  $("ps-sexe").addEventListener("change", generer);
  $("ps-list").addEventListener("click", e => {
    const b = e.target.closest("button"); if (!b) return;
    if (b.classList.contains("ps-name")) copier(b.dataset.n, b);
    if (b.classList.contains("ps-star")) {
      const n = b.dataset.n;
      if (favs.some(f => f.n === n)) { favs = favs.filter(f => f.n !== n); b.textContent = "☆"; }
      else { favs.unshift({ n, r: b.dataset.r }); favs = favs.slice(0, 30); b.textContent = "★"; }
      save(favs); renderFavs();
    }
  });
  $("ps-favs").addEventListener("click", e => {
    const d = e.target.dataset.del; if (!d) return;
    favs = favs.filter(f => f.n !== d); save(favs); renderFavs(); generer();
  });
  generer(); renderFavs();
})();
