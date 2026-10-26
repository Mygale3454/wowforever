/* ===== wowforever – éléments communs à toutes les pages =====
   Pour ajouter une page au menu : ajoute une ligne dans MENU ci-dessous. */
const MENU = [
  ["index.html", "Accueil"],
  ["actualites.html", "Actualités"],
  ["debuter.html", "Bien débuter"],
  ["classes.html", "Classes"],
  ["donjons.html", "Donjons & Raids"],
  ["legacy.html", "Legacy"],
  ["calendrier.html", "Calendrier"],
  ["galerie.html", "Galerie"]
];

const POPULAIRES = [
  ["debuter.html", "images/debuter.jpg", "Bien débuter sur WoW Forever"],
  ["donjons.html", "images/donjons.jpg", "Les 9 nouveaux donjons"],
  ["legacy.html", "images/legacy.jpg", "Le système Legacy expliqué"],
  ["classes.html", "images/classes.jpg", "Races et classes : les nouveautés"],
  ["calendrier.html", "images/calendrier.jpg", "Roadmap 2026-2027"]
];

const current = location.pathname.split("/").pop() || "index.html";

document.getElementById("site-header").outerHTML = `
<div class="topbar"><div class="wrap">
  <span class="live" id="topbar-cd">Sortie de WoW Forever bientôt</span>
  <span class="hide-m">Site de fan non officiel · Guides en français</span>
</div></div>
<header><div class="wrap">
  <a class="logo" href="index.html">wow<span>forever</span></a>
  <nav class="menu" id="menu">
    ${MENU.map(([href, label]) => `<a href="${href}"${href === current ? ' class="active"' : ""}>${label}</a>`).join("")}
  </nav>
  <button class="burger" id="burger" aria-label="Menu">☰</button>
</div></header>`;

document.getElementById("site-footer").outerHTML = `
<footer><div class="wrap">
  <div class="cols">
    <div><div class="logo">wow<span>forever</span></div><p>Guides, actualités et outils en français pour World of Warcraft: Forever.</p></div>
    <div><h5>Guides</h5><a href="debuter.html">Bien débuter</a><a href="classes.html">Classes</a><a href="donjons.html">Donjons & Raids</a><a href="legacy.html">Legacy</a></div>
    <div><h5>Infos</h5><a href="actualites.html">Actualités</a><a href="calendrier.html">Calendrier</a><a href="galerie.html">Galerie</a></div>
  </div>
  <div class="legal">wowforever est un site de fan non officiel, sans lien avec Blizzard Entertainment. World of Warcraft est une marque de Blizzard Entertainment, Inc. Captures et visuels de World of Warcraft © Blizzard Entertainment.</div>
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
      <a href="classes.html">Skyborne</a><a href="donjons.html">Donjons</a><a href="donjons.html">Raids</a><a href="legacy.html">Legacy</a><a href="debuter.html">Camping</a><a href="calendrier.html">Hardcore</a><a href="debuter.html">Métiers</a><a href="actualites.html">JcJ</a>
    </div>
  </div>`);

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
