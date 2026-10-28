/* ===== Calculateur de talents wowforever ===== */
(() => {
const CLASSES = [
  ["warrior","Guerrier"],["paladin","Paladin"],["hunter","Chasseur"],["rogue","Voleur"],["priest","Prêtre"],
  ["shaman","Chaman"],["mage","Mage"],["warlock","Démoniste"],["druid","Druide"]
];
const TREE_FR = {
  "Arms":"Armes","Fury":"Fureur","Protection":"Protection","Holy":"Sacré","Retribution":"Vindicte",
  "Beast Mastery":"Maîtrise des bêtes","Marksmanship":"Précision","Survival":"Survie",
  "Assassination":"Assassinat","Combat":"Combat","Subtlety":"Finesse",
  "Discipline":"Discipline","Shadow":"Ombre","Elemental":"Élémentaire","Enhancement":"Amélioration","Restoration":"Restauration",
  "Arcane":"Arcanes","Fire":"Feu","Frost":"Givre","Affliction":"Affliction","Demonology":"Démonologie","Destruction":"Destruction",
  "Balance":"Équilibre","Feral Combat":"Combat farouche"
};
const STATUS = {new:["Nouveau dans Forever","new"],changed:["Modifié dans Forever","chg"],moved:["Déplacé dans Forever","mov"],unchanged:["Identique à Classic","same"]};
const MAX = 51, START = 10, PER_ROW = 5;
const B36 = "0123456789abcdefghijklmnopqrstuvwxyz";

const $ = s => document.querySelector(s);
let cls = "warrior", alloc = {};   // alloc["treeIndex:talentId"] = rang
let tipKey = null;

const trees = () => TALENTS[cls].trees;
const key = (ti, t) => ti + ":" + t.id;
const rank = (ti, t) => alloc[key(ti, t)] || 0;
const spent = () => Object.values(alloc).reduce((a, b) => a + b, 0);
const treeSpent = ti => trees()[ti].t.reduce((a, t) => a + rank(ti, t), 0);
const rowsBefore = (ti, row) => trees()[ti].t.reduce((a, t) => a + (t.r < row ? rank(ti, t) : 0), 0);
const find = (ti, id) => trees()[ti].t.find(t => t.id === id);

function prereqOk(ti, t) { return t.p.every(([id, r]) => rank(ti, find(ti, id)) >= r); }
function canAdd(ti, t) {
  return spent() < MAX && rank(ti, t) < t.m && rowsBefore(ti, t.r) >= t.r * PER_ROW && prereqOk(ti, t);
}
/* Retirer un point est permis seulement si toute la construction reste valide ensuite */
function valid() {
  return trees().every((tr, ti) => tr.t.every(t => {
    const r = rank(ti, t);
    return !r || (rowsBefore(ti, t.r) >= t.r * PER_ROW && prereqOk(ti, t));
  }));
}
function canRemove(ti, t) {
  if (!rank(ti, t)) return false;
  alloc[key(ti, t)]--; const ok = valid(); alloc[key(ti, t)]++;
  return ok;
}
function change(ti, t, d) {
  if (d > 0 ? !canAdd(ti, t) : !canRemove(ti, t)) return flash(ti, t);
  const k = key(ti, t); alloc[k] = rank(ti, t) + d; if (!alloc[k]) delete alloc[k];
  render(); save();
}
function flash(ti, t) {
  const el = document.querySelector(`[data-k="${key(ti, t)}"]`);
  if (el) { el.classList.remove("nope"); void el.offsetWidth; el.classList.add("nope"); }
}

/* ----- Lien de partage : #classe-arbre1-arbre2-arbre3 (un caractère par talent) ----- */
function encode() {
  return cls + "-" + trees().map((tr, ti) => tr.t.map(t => B36[rank(ti, t)]).join("").replace(/0+$/, "")).join("-");
}
function decode(h) {
  const [c, ...parts] = decodeURIComponent(h).replace(/^#/, "").split("-");
  if (!TALENTS[c]) return false;
  cls = c; alloc = {};
  TALENTS[c].trees.forEach((tr, ti) => tr.t.forEach((t, i) => {
    const r = Math.min(t.m, B36.indexOf((parts[ti] || "")[i] || "0"));
    if (r > 0) alloc[key(ti, t)] = r;
  }));
  if (!valid() || spent() > MAX) alloc = {};
  return true;
}
function save() { history.replaceState(null, "", "#" + encode()); }

/* ----- Affichage ----- */
const initials = n => n.replace(/[^A-Za-z ]/g, "").split(" ").filter(w => w.length > 2 || w === w.toUpperCase()).slice(0, 2).map(w => w[0]).join("").toUpperCase() || n.slice(0, 2).toUpperCase();

function renderClasses() {
  $("#classes").innerHTML = CLASSES.map(([id, fr]) =>
    `<button class="cbtn${id === cls ? " on" : ""}" data-c="${id}" style="--c:${TALENTS[id].color}"><img src="images/icons/class_${id}.jpg" alt="">${fr}</button>`).join("");
}

function render() {
  renderClasses();
  const s = spent(), color = TALENTS[cls].color;
  document.documentElement.style.setProperty("--cc", color);
  $("#points").textContent = `${s} / ${MAX}`;
  $("#left").textContent = MAX - s;
  $("#level").textContent = s ? s + START - 1 : "–";
  $("#split").textContent = trees().map((_, ti) => treeSpent(ti)).join(" / ");

  $("#trees").innerHTML = trees().map((tr, ti) => {
    const cells = tr.t.map(t => {
      const r = rank(ti, t), k = key(ti, t);
      const state = r === t.m ? "max" : r ? "part" : canAdd(ti, t) ? "open" : "lock";
      return `<button class="tal ${state}${t.a ? " active" : ""}" data-k="${k}" data-ti="${ti}" data-id="${t.id}"
        style="grid-row:${t.r + 1};grid-column:${t.c + 1}" aria-label="${t.n}, rang ${r} sur ${t.m}">
        <img src="images/icons/${t.i}.jpg" alt="" loading="lazy" onerror="this.remove()"><span class="ini">${initials(t.n)}</span><span class="rk">${r}/${t.m}</span>
        ${t.s === "new" ? '<i class="dot" title="Nouveau"></i>' : ""}</button>`;
    }).join("");
    const arrows = tr.t.flatMap(t => t.p.map(([id]) => {
      const p = find(ti, id); const on = rank(ti, p) >= 1;
      return `<line x1="${p.c + .5}" y1="${p.r + .5}" x2="${t.c + .5}" y2="${t.r + .5}" class="${on ? "on" : ""}"/>`;
    })).join("");
    return `<section class="tree">
      <header>${tr.i ? `<img class="ticon" src="images/icons/${tr.i}.jpg" alt="">` : ""}<h2>${TREE_FR[tr.n] || tr.n}</h2><span class="tp">${treeSpent(ti)}</span>
        <button class="treset" data-ti="${ti}" title="Vider cet arbre">↺</button></header>
      <div class="grid" style="--cols:${tr.cols};--rows:${tr.rows}">
        <svg class="arrows" viewBox="0 0 ${tr.cols} ${tr.rows}" preserveAspectRatio="none">${arrows}</svg>
        ${cells}
      </div>
    </section>`;
  }).join("");
  if (tipKey) showTip(tipKey, true);
}

/* ----- Infobulle / fiche du talent ----- */
function showTip(k, keep) {
  const [ti, id] = k.split(":"); const t = find(+ti, id); if (!t) return hideTip();
  tipKey = k;
  const r = rank(+ti, t), st = STATUS[t.s] || null;
  const reqs = [];
  if (t.r) reqs.push(`${t.r * PER_ROW} points en ${TREE_FR[trees()[ti].n] || trees()[ti].n}`);
  t.p.forEach(([pid, pr]) => reqs.push(`${pr} point${pr > 1 ? "s" : ""} en ${find(+ti, pid).n}`));
  const cur = r ? t.t[r - 1] : null, next = r < t.m ? t.t[r] : null;
  $("#tip").innerHTML = `
    <button class="tclose" aria-label="Fermer">×</button>
    <div class="thead"><img src="images/icons/${t.i}.jpg" alt=""><h3>${t.n}</h3></div>
    <div class="trank">Rang ${r}/${t.m}${t.a ? " · Sort actif" : ""}${st ? ` · <span class="st ${st[1]}">${st[0]}</span>` : ""}</div>
    ${reqs.length ? `<div class="treq">Requiert : ${reqs.join(", ")}</div>` : ""}
    ${t.q ? `<div class="treq">${t.q}</div>` : ""}
    ${cur ? `<p>${cur}</p>` : ""}
    ${next ? `<div class="tnext">${r ? "Rang suivant :" : ""}</div><p class="${r ? "dim" : ""}">${next}</p>` : ""}
    ${t.o ? `<details><summary>Version Classic</summary><p class="dim">${t.o}</p></details>` : ""}
    <div class="tbtns"><button data-d="-1" ${canRemove(+ti, t) ? "" : "disabled"}>− Retirer</button><button data-d="1" ${canAdd(+ti, t) ? "" : "disabled"}>+ Ajouter</button></div>`;
  $("#tip").hidden = false;
}
function hideTip() { tipKey = null; $("#tip").hidden = true; }

/* ----- Interactions ----- */
const touch = matchMedia("(hover: none)").matches;
document.addEventListener("click", e => {
  const c = e.target.closest(".cbtn");
  if (c) { if (c.dataset.c !== cls) { cls = c.dataset.c; alloc = {}; hideTip(); render(); save(); } return; }
  const r = e.target.closest(".treset");
  if (r) { trees()[r.dataset.ti].t.forEach(t => delete alloc[key(+r.dataset.ti, t)]); render(); save(); return; }
  const b = e.target.closest(".tal");
  if (b) {
    const t = find(+b.dataset.ti, b.dataset.id);
    if (touch) showTip(b.dataset.k); else change(+b.dataset.ti, t, e.shiftKey ? -1 : 1);
    return;
  }
  const d = e.target.closest("#tip [data-d]");
  if (d && tipKey) { const [ti, id] = tipKey.split(":"); change(+ti, find(+ti, id), +d.dataset.d); return; }
  if (e.target.closest(".tclose")) hideTip();
});
document.addEventListener("contextmenu", e => {
  const b = e.target.closest(".tal"); if (!b) return;
  e.preventDefault(); change(+b.dataset.ti, find(+b.dataset.ti, b.dataset.id), -1);
});
if (!touch) {
  document.body.classList.add("hover");
  const place = b => {
    const r = b.getBoundingClientRect(), tip = $("#tip"), w = tip.offsetWidth, h = tip.offsetHeight;
    let x = r.right + 12, y = r.top;
    if (x + w > innerWidth - 8) x = r.left - w - 12;
    if (y + h > innerHeight - 8) y = innerHeight - h - 8;
    tip.style.left = Math.max(8, x) + "px"; tip.style.top = Math.max(8, y) + "px";
  };
  document.addEventListener("mouseover", e => { const b = e.target.closest(".tal"); if (b) { showTip(b.dataset.k); place(b); } });
  document.addEventListener("mouseout", e => { const b = e.target.closest(".tal"); if (b && !e.relatedTarget?.closest?.(".tal")) hideTip(); });
}
$("#reset").onclick = () => { alloc = {}; render(); save(); };
$("#copy").onclick = async () => {
  save();
  try { await navigator.clipboard.writeText(location.href); $("#copy").textContent = "Lien copié !"; }
  catch { prompt("Copie ce lien :", location.href); }
  setTimeout(() => $("#copy").textContent = "Copier le lien", 1800);
};
window.addEventListener("hashchange", () => { if (location.hash.slice(1) !== encode()) { decode(location.hash); render(); } });

if (location.hash.length > 1) decode(location.hash);
render();
})();
