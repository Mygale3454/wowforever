/* ===== wowforever – éléments communs à toutes les pages =====
   Pour ajouter une page au menu : ajoute une ligne dans MENU ci-dessous. */
const MENU = [
  ["index.html", "News"],
  ["Classes / Races", [["classes.html", "Classes"], ["guides.html", "Guides de spé"], ["tier-list.html", "Tier lists niveau 60"], ["quetes-de-classe.html", "Quêtes de classe"], ["talents.html", "Calculateur de talents"], ["races.html", "Races"]]],
  ["Leveling", [["leveling.html", "Parcours 1-60"], ["pas-a-pas.html", "Guide pas à pas"]]],
  ["Monde", [["debuter.html", "Bien débuter"], ["donjons.html", "Donjons & Raids"], ["pvp.html", "PvP"], ["reputations.html", "Réputations"], ["montures.html", "Montures"], ["legacy.html", "Héritage (Legacy)"]]],
  ["Métiers", [["metiers.html", "Les métiers"], ["metiers-pas-a-pas.html", "Métiers pas à pas 1-300"]]],
  ["Équipement", [["bis.html", "BiS niveau 60"]]],
  ["Officiel", [["calendrier.html", "Roadmap"], ["videos.html", "Vidéos officielles"], ["https://worldofwarcraft.blizzard.com/forever", "Site officiel ↗"]]],
  ["Outils", [["talents.html", "Calculateur de talents"], ["carte.html", "Carte interactive"], ["pseudo.html", "Générateur de pseudo"], ["addons.html", "Addons"], ["feu-de-camp.html", "Feu de Camp <sup class=\"dbeta\">Bêta</sup>"]]],
  ["Communauté", [["galerie.html", "Galerie"], ["liens.html", "Liens & chaînes"], ["contact.html", "Contact"]]]
];

const POPULAIRES = [
  ["debuter.html", "images/debuter.jpg", "Bien débuter sur WoW Forever"],
  ["donjons.html", "images/donjons.jpg", "Les 9 nouveaux donjons"],
  ["legacy.html", "images/legacy.jpg", "Le système Legacy expliqué"],
  ["races.html", "images/skyborne.jpg", "Quelle race choisir ? Le comparatif"],
  ["article-addons.html", "images/news/addons.jpg", "Les meilleurs addons pour WoW Forever"],
  ["calendrier.html", "images/calendrier.jpg", "Roadmap 2026-2027"]
];

/* Thème : "gris" (par défaut) ou "parchemin", mémorisé dans le navigateur */
const THEME_KEY = "wowforever-theme";
let theme = "gris";
try { theme = localStorage.getItem(THEME_KEY) || "gris"; } catch (e) {}
document.documentElement.dataset.theme = theme;

const current = location.pathname.split("/").pop() || "index.html";

document.getElementById("site-header").outerHTML = `
<div class="topbar"><div class="wrap">
  <span class="live" id="topbar-cd">Sortie de WoW Forever bientôt</span>
  <span><span class="hide-m">Site de fan non officiel · Guides en français</span><button class="themebtn" id="themebtn" type="button"></button></span>
</div></div>
<div class="banner">
  <img src="images/bandeau2.jpg" alt="">
  <div class="wrap banner-in">
    <a class="fwlogo-img" href="index.html"><img src="images/logo-foreverwow.webp" alt="ForeverWoW.fr – Guides &amp; outils pour WoW Forever" width="900" height="468" fetchpriority="high"></a>
  </div>
</div>
<header class="navbar"><div class="wrap">
  <a class="logo mini-logo" href="index.html"><img src="images/emblem.svg" alt="" class="mini-em">Forever<span>WoW</span></a>
  <nav class="menu" id="menu">
    ${MENU.map(([a, b]) => Array.isArray(b)
      ? `<div class="sub${b.some(([h]) => h === current) ? " active" : ""}"><button class="subbtn" type="button">${a} ▾</button><div class="subm">${b.map(([h, l]) => `<a href="${h}"${h === current ? ' class="active"' : ""}${/^https?:/.test(h) ? ' target="_blank" rel="noopener"' : ""}>${l}</a>`).join("")}</div></div>`
      : `<a href="${a}"${a === current ? ' class="active"' : ""}>${b}</a>`).join("")}
  </nav>
  <button class="burger" id="burger" aria-label="Menu">☰</button>
</div></header>`;

document.getElementById("site-footer").outerHTML = `
<footer><div class="wrap">
  <div class="cols">
    <div><div class="logo"><img src="images/emblem.svg" alt="" class="mini-em">Forever<span>WoW</span>.fr</div><p>Guides, actualités et outils en français pour World of Warcraft: Forever.</p></div>
    <div><h5>Guides</h5><a href="debuter.html">Bien débuter</a><a href="leveling.html">Parcours 1-60</a><a href="pas-a-pas.html">Leveling pas à pas</a><a href="classes.html">Classes</a><a href="guides.html">Guides de spé</a><a href="tier-list.html">Tier lists 60</a><a href="quetes-de-classe.html">Quêtes de classe</a><a href="talents.html">Calculateur de talents</a><a href="donjons.html">Donjons & Raids</a><a href="pvp.html">PvP</a><a href="reputations.html">Réputations</a><a href="montures.html">Montures</a><a href="metiers.html">Métiers</a><a href="metiers-pas-a-pas.html">Métiers pas à pas</a><a href="legacy.html">Legacy</a><a href="bis.html">BiS niveau 60</a><a href="addons.html">Addons</a></div>
    <div><h5>Infos</h5><a href="index.html">News</a><a href="calendrier.html">Roadmap</a><a href="videos.html">Vidéos officielles</a><a href="galerie.html">Galerie</a><a href="liens.html">Liens &amp; chaînes</a><a href="contact.html">Contact</a><a href="rss.xml">Flux RSS des news</a></div>
  </div>
  <div class="legal">ForeverWoW.fr est un site de fan non officiel, sans lien avec Blizzard Entertainment. World of Warcraft est une marque de Blizzard Entertainment, Inc. Captures et visuels de World of Warcraft © Blizzard Entertainment.</div>
</div></footer>`;

document.querySelectorAll("[data-sidebar]").forEach(a => a.innerHTML = `
  <div class="box">
    <h4>Sortie de WoW Forever</h4>
    <div class="cdown" data-cd><div><b>--</b><span>Jours</span></div><div><b>--</b><span>Heures</span></div><div><b>--</b><span>Min</span></div><div><b>--</b><span>Sec</span></div></div>
    <p class="small">4 novembre 2026 · minuit heure de Paris</p>
  </div>
  <div class="box">
    <h4>Les plus lus</h4>
    ${POPULAIRES.filter(p => p[0] !== current).map(([h, img, t]) => `<a class="mini" href="${h}"><img src="${img}" alt="" loading="lazy" width="64" height="40">${t}</a>`).join("")}
  </div>
  <div class="box">
    <h4>Thèmes</h4>
    <div class="tags">
      <a href="classes.html">Skyborne</a><a href="donjons.html">Donjons</a><a href="donjons.html">Raids</a><a href="legacy.html">Legacy</a><a href="metiers.html">Camping</a><a href="calendrier.html">Hardcore</a><a href="metiers.html">Métiers</a><a href="pvp.html">JcJ</a><a href="reputations.html">Réputations</a><a href="addons.html">Addons</a>
    </div>
  </div>`);

document.querySelectorAll(".subbtn").forEach(b => b.onclick = e => { e.stopPropagation(); const p = b.parentElement, o = p.classList.contains("open"); document.querySelectorAll(".sub.open").forEach(x => x.classList.remove("open")); if (!o) p.classList.add("open"); });
document.addEventListener("click", () => document.querySelectorAll(".sub.open").forEach(x => x.classList.remove("open")));
const tb = document.getElementById("themebtn");
const setTb = () => tb.textContent = document.documentElement.dataset.theme === "gris" ? "Thème parchemin" : "Thème gris";
setTb();
tb.onclick = () => {
  const t = document.documentElement.dataset.theme === "gris" ? "parchemin" : "gris";
  document.documentElement.dataset.theme = t;
  try { localStorage.setItem(THEME_KEY, t); } catch (e) {}
  setTb();
};
document.getElementById("burger").onclick = () => document.getElementById("menu").classList.toggle("open");

/* ----- Compte à rebours : 4 nov. 2026, 15:00 heure du Pacifique = 23:00 UTC ----- */
const target = Date.UTC(2026, 10, 4, 23, 0, 0);
const pad = n => String(n).padStart(2, "0");
function tick() {
  const diff = target - Date.now();
  const top = document.getElementById("topbar-cd");
  if (diff <= 0) {
    top.textContent = "WoW Forever est disponible : let's go !";
    document.querySelectorAll("[data-cd]").forEach(c => {
      const box = c.closest(".box");
      box.classList.add("poll-box");
      box.innerHTML = '<small>Sondage</small><b class="poll-q">Tu joues Horde ou Alliance&nbsp;?</b>'
        + '<div class="poll-btns"><button type="button" class="pb h" data-v="horde"><span>Horde</span></button><button type="button" class="pb a" data-v="alliance"><span>Alliance</span></button></div>'
        + '<div class="poll-res" hidden><div class="pl-bar"><i class="h"></i><i class="a"></i></div><div class="plab"><span class="ph"></span><span class="pa"></span></div><small class="ptot"></small></div>'
        + '<button type="button" class="poll-see">Voir les résultats</button>';
      poll(box);
    });
    return clearInterval(timer);
  }
  const v = [Math.floor(diff / 864e5), pad(Math.floor(diff / 36e5) % 24), pad(Math.floor(diff / 6e4) % 60), pad(Math.floor(diff / 1e3) % 60)];
  document.querySelectorAll("[data-cd]").forEach(c => c.querySelectorAll("b").forEach((b, i) => b.textContent = v[i]));
  top.textContent = `Sortie de WoW Forever dans ${v[0]} j ${v[1]} h ${v[2]} min`;
}
const timer = setInterval(tick, 1000); tick();

/* ----- Sondage « Horde ou Alliance ? » (colonne de droite) -----
   Compteur gratuit abacus.jasoncameron.dev (sans compte). Un vote par navigateur (mémorisé localement). */
function poll(box) {
  const API = "https://abacus.jasoncameron.dev", NS = "foreverwow-fr", KEY = { horde: "faction-horde", alliance: "faction-alliance" };
  const VK = "fw_vote_faction";
  let mine = null; try { mine = localStorage.getItem(VK); } catch (e) {}
  const res = box.querySelector(".poll-res"), btns = box.querySelector(".poll-btns"), see = box.querySelector(".poll-see");
  const get = k => fetch(`${API}/get/${NS}/${KEY[k]}`).then(r => r.ok ? r.json() : { value: 0 }).then(j => j.value || 0).catch(() => null);
  function show(h, a, msg) {
    btns.hidden = true; see.hidden = true; res.hidden = false;
    const tot = (h || 0) + (a || 0);
    if (h === null || a === null || !tot) {
      res.querySelector(".pl-bar").hidden = true; res.querySelector(".plab").hidden = true;
      res.querySelector(".ptot").textContent = msg || "Résultats indisponibles pour le moment.";
      return;
    }
    const ph = Math.round(h * 100 / tot);
    res.querySelector("i.h").style.width = ph + "%"; res.querySelector("i.a").style.width = (100 - ph) + "%";
    res.querySelector(".ph").textContent = `Horde ${ph} %`; res.querySelector(".pa").textContent = `${100 - ph} % Alliance`;
    res.querySelector(".ptot").textContent = `${tot} vote${tot > 1 ? "s" : ""}` + (msg ? ` · ${msg}` : "");
  }
  const load = msg => Promise.all([get("horde"), get("alliance")]).then(([h, a]) => show(h, a, msg));
  if (mine) load(mine === "horde" ? "Pour la Horde !" : "Pour l'Alliance !");
  see.onclick = () => load("");
  btns.querySelectorAll(".pb").forEach(b => b.onclick = () => {
    const v = b.dataset.v;
    btns.querySelectorAll(".pb").forEach(x => x.disabled = true);
    try { localStorage.setItem(VK, v); } catch (e) {}
    const merci = v === "horde" ? "Pour la Horde !" : "Pour l'Alliance !";
    fetch(`${API}/hit/${NS}/${KEY[v]}`).then(r => r.json()).then(j => {
      const other = v === "horde" ? "alliance" : "horde";
      return get(other).then(o => v === "horde" ? show(j.value, o, merci) : show(o, j.value, merci));
    }).catch(() => show(null, null, "Merci pour ton vote ! " + merci));
  });
}
