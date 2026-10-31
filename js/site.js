/* ===== wowforever – éléments communs à toutes les pages =====
   Pour ajouter une page au menu : ajoute une ligne dans MENU ci-dessous. */
const MENU = [
  ["index.html", "News"],
  ["Classes / Races", [["classes.html", "Classes"], ["guides.html", "Guides de spé"], ["talents.html", "Calculateur de talents"], ["races.html", "Races"]]],
  ["Leveling", [["leveling.html", "Parcours 1-60"], ["pas-a-pas.html", "Guide pas à pas"]]],
  ["Monde", [["debuter.html", "Bien débuter"], ["donjons.html", "Donjons & Raids"], ["pvp.html", "PvP"], ["reputations.html", "Réputations"]]],
  ["metiers.html", "Métiers"],
  ["legacy.html", "Legacy"],
  ["calendrier.html", "Calendrier"],
  ["Outils", [["talents.html", "Calculateur de talents"], ["pseudo.html", "Générateur de pseudo"], ["addons.html", "Addons"]]],
  ["galerie.html", "Galerie"]
];

const POPULAIRES = [
  ["debuter.html", "images/debuter.jpg", "Bien débuter sur WoW Forever"],
  ["donjons.html", "images/donjons.jpg", "Les 9 nouveaux donjons"],
  ["legacy.html", "images/legacy.jpg", "Le système Legacy expliqué"],
  ["races.html", "images/skyborne.jpg", "Quelle race choisir ? Le comparatif"],
  ["article-addons.html", "images/galerie/18.jpg", "Les meilleurs addons pour WoW Forever"],
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
  <img src="images/bandeau.jpg" alt="">
  <div class="wrap banner-in">
    <a class="fwlogo" href="index.html" aria-label="ForeverWoW.fr, accueil"><img src="images/emblem.svg" alt=""><span class="fw-wm"><span class="fw-name">Forever<span class="fw-w">WoW</span><span class="fw-tld">.fr</span></span><span class="fw-tag">Guides &amp; outils pour WoW Forever</span></span></a>
  </div>
</div>
<header class="navbar"><div class="wrap">
  <a class="logo mini-logo" href="index.html"><img src="images/emblem.svg" alt="" class="mini-em">Forever<span>WoW</span></a>
  <nav class="menu" id="menu">
    ${MENU.map(([a, b]) => Array.isArray(b)
      ? `<div class="sub${b.some(([h]) => h === current) ? " active" : ""}"><button class="subbtn" type="button">${a} ▾</button><div class="subm">${b.map(([h, l]) => `<a href="${h}"${h === current ? ' class="active"' : ""}>${l}</a>`).join("")}</div></div>`
      : `<a href="${a}"${a === current ? ' class="active"' : ""}>${b}</a>`).join("")}
  </nav>
  <button class="burger" id="burger" aria-label="Menu">☰</button>
</div></header>`;

document.getElementById("site-footer").outerHTML = `
<footer><div class="wrap">
  <div class="cols">
    <div><div class="logo"><img src="images/emblem.svg" alt="" class="mini-em">Forever<span>WoW</span>.fr</div><p>Guides, actualités et outils en français pour World of Warcraft: Forever.</p></div>
    <div><h5>Guides</h5><a href="debuter.html">Bien débuter</a><a href="leveling.html">Parcours 1-60</a><a href="pas-a-pas.html">Leveling pas à pas</a><a href="classes.html">Classes</a><a href="guides.html">Guides de spé</a><a href="talents.html">Calculateur de talents</a><a href="donjons.html">Donjons & Raids</a><a href="pvp.html">PvP</a><a href="reputations.html">Réputations</a><a href="metiers.html">Métiers</a><a href="legacy.html">Legacy</a><a href="addons.html">Addons</a></div>
    <div><h5>Infos</h5><a href="index.html">News</a><a href="calendrier.html">Calendrier</a><a href="galerie.html">Galerie</a></div>
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
    ${POPULAIRES.filter(p => p[0] !== current).map(([h, img, t]) => `<a class="mini" href="${h}"><img src="${img}" alt="">${t}</a>`).join("")}
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
    top.textContent = "WoW Forever est disponible !";
    document.querySelectorAll("[data-cd]").forEach(c => c.innerHTML = '<div style="grid-column:1/-1"><b>Disponible !</b></div>');
    return clearInterval(timer);
  }
  const v = [Math.floor(diff / 864e5), pad(Math.floor(diff / 36e5) % 24), pad(Math.floor(diff / 6e4) % 60), pad(Math.floor(diff / 1e3) % 60)];
  document.querySelectorAll("[data-cd]").forEach(c => c.querySelectorAll("b").forEach((b, i) => b.textContent = v[i]));
  top.textContent = `Sortie de WoW Forever dans ${v[0]} j ${v[1]} h ${v[2]} min`;
}
const timer = setInterval(tick, 1000); tick();
