/* ===== wowforever – éléments communs à toutes les pages =====
   Pour ajouter une page au menu : ajoute une ligne dans MENU ci-dessous. */
const MENU = [
  ["index.html", "News"],
  ["Classes / Races", [["classes.html", "Classes"], ["guides.html", "Guides de spé"], ["tier-list.html", "Tier lists niveau 60"], ["quetes-de-classe.html", "Quêtes de classe"], ["talents.html", "Calculateur de talents"], ["races.html", "Races"]]],
  ["Leveling", [["leveling.html", "Parcours 1-60"], ["pas-a-pas.html", "Guide de leveling 1-60"]]],
  ["Monde", [["debuter.html", "Bien débuter"], ["donjons.html", "Donjons & Raids"], ["pvp.html", "PvP"], ["reputations.html", "Réputations"], ["montures.html", "Montures"], ["legacy.html", "Héritage (Legacy)"]]],
  ["Métiers", [["metiers.html", "Les métiers"], ["metiers-pas-a-pas.html", "Métiers pas à pas 1-300"]]],
  ["Équipement", [["bis.html", "BiS niveau 60"]]],
  ["Officiel", [["calendrier.html", "Roadmap"], ["videos.html", "Vidéos"], ["https://worldofwarcraft.blizzard.com/forever", "Site officiel ↗"]]],
  ["Outils", [["talents.html", "Calculateur de talents"], ["carte.html", "Carte interactive"], ["pseudo.html", "Générateur de pseudo"], ["addons.html", "Addons"], ["feu-de-camp.html", "Feu de Camp · planificateur <sup class=\"dbeta\">Bêta</sup>"]]],
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
    <div><h5>Guides</h5><a href="debuter.html">Bien débuter</a><a href="leveling.html">Parcours 1-60</a><a href="pas-a-pas.html">Guide de leveling</a><a href="classes.html">Classes</a><a href="guides.html">Guides de spé</a><a href="tier-list.html">Tier lists 60</a><a href="quetes-de-classe.html">Quêtes de classe</a><a href="talents.html">Calculateur de talents</a><a href="donjons.html">Donjons & Raids</a><a href="pvp.html">PvP</a><a href="reputations.html">Réputations</a><a href="montures.html">Montures</a><a href="metiers.html">Métiers</a><a href="metiers-pas-a-pas.html">Métiers pas à pas</a><a href="legacy.html">Legacy</a><a href="bis.html">BiS niveau 60</a><a href="addons.html">Addons</a></div>
    <div><h5>Infos</h5><a href="index.html">News</a><a href="calendrier.html">Roadmap</a><a href="videos.html">Vidéos</a><a href="galerie.html">Galerie</a><a href="liens.html">Liens &amp; chaînes</a><a href="contact.html">Contact</a><a href="rss.xml">Flux RSS des news</a></div>
    <div><h5>Le site</h5><a href="a-propos.html">À propos</a><a href="mentions-legales.html">Mentions légales</a><a href="confidentialite.html">Confidentialité</a></div>
  </div>
  <div class="legal">ForeverWoW.fr est un site de fan non officiel, sans lien avec Blizzard Entertainment. World of Warcraft est une marque de Blizzard Entertainment, Inc. Captures et visuels de World of Warcraft © Blizzard Entertainment.</div>
</div></footer>`;

document.querySelectorAll("[data-sidebar]").forEach(a => a.innerHTML = `
  <div class="box lore-box" data-lore></div>
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
    return clearInterval(timer);
  }
  const v = [Math.floor(diff / 864e5), pad(Math.floor(diff / 36e5) % 24), pad(Math.floor(diff / 6e4) % 60), pad(Math.floor(diff / 1e3) % 60)];
  top.textContent = `Sortie de WoW Forever dans ${v[0]} j ${v[1]} h ${v[2]} min`;
}
const timer = setInterval(tick, 1000); tick();

/* ----- Encadré « Le saviez-vous ? » (colonne de droite) -----
   Une astuce de jeu ou l'histoire d'un personnage, tirée au hasard.
   Pour en ajouter : une ligne dans ASTUCES, ou un objet dans PERSOS. */
const ASTUCES = [
  "Parle à l'aubergiste de chaque nouvelle ville pour y lier ta pierre de foyer : elle te ramènera là-bas toutes les heures.",
  "Déconnecte-toi dans une auberge ou une capitale : tu accumules de l'expérience reposée, qui double l'XP gagnée sur les monstres.",
  "Dans chaque nouvelle ville, parle au maître de vol pour débloquer le trajet. Sans ça, impossible d'y revenir en griffon ou en wyverne.",
  "Manger et boire hors combat rend vie et mana bien plus vite que d'attendre : garde toujours de quoi te restaurer dans tes sacs.",
  "Après avoir lancé un sort, ta mana ne se régénère presque plus pendant 5 secondes. Espacer ses sorts permet de tenir plus longtemps.",
  "Ressusciter auprès du gardien des esprits abîme davantage ton équipement et t'affaiblit un moment. Mieux vaut courir jusqu'à ton corps.",
  "Tout le monde peut apprendre les premiers secours : les bandages soignent sans mana et sauvent bien des combats.",
  "Les objets gris ne servent qu'à être vendus. Vide tes sacs chez un marchand avant de repartir à l'aventure.",
  "Herboristerie, minage et dépeçage ne coûtent presque rien à monter et rapportent de l'or dès les premiers niveaux.",
  "Une quête grise ne rapporte presque plus d'expérience : passe à des quêtes jaunes ou orange pour avancer plus vite.",
  "Un dragon doré autour du portrait d'un monstre signale un élite : il est bien plus coriace qu'il n'en a l'air, viens en groupe.",
  "Tes compétences d'armes montent en les utilisant. Pour manier un nouveau type d'arme, rends-toi chez un maître d'armes.",
  "Shift + clic sur un objet l'insère dans la fenêtre de discussion : pratique pour montrer ce que tu viens de looter.",
  "La commande /assist suivie d'un nom te fait cibler ce que vise ton allié. Idéal pour taper tous ensemble la même cible.",
  "À l'hôtel des ventes, le dépôt est perdu si l'objet ne se vend pas : fixe un prix raisonnable et une durée adaptée.",
  "Les gardes des villes et des routes attaquent les ennemis de ta faction : en JcJ sauvage, rapproche-toi d'eux.",
  "En donjon, laisse le tank attirer les monstres et attends qu'il ait pris l'aggro avant de lancer tes plus gros sorts.",
  "Les métiers de récolte affichent les ressources sur la mini-carte : active le suivi des herbes ou des minerais dans ton grimoire.",
  "Un sac vaut de l'or : à bas niveau, investir dans des sacs de 6 ou 8 places évite des allers-retours chez le marchand.",
  "Les quêtes de classe donnent souvent des sorts ou des objets uniques : jette un œil à leur liste avant de les ignorer."
];
const PERSOS = [
  { nom: "Thrall", f: "h", txt: "Né sous le nom de Go'el, fils du chef Durotan, il est élevé comme esclave et gladiateur dans la forteresse de Durnholde. Une fois évadé, il libère les orcs des camps d'internement, mène la Horde jusqu'en Kalimdor et l'installe sur une terre qu'il baptise Durotar, en hommage à son père." },
  { nom: "Jaina Portvaillant", f: "a", txt: "Fille de l'amiral Daelin Portvaillant et élève de l'archimage Antonidas, elle fut proche du prince Arthas. Face au Fléau, elle conduit les survivants de Lordaeron en Kalimdor, s'allie à Thrall contre Archimonde puis fonde la cité de Theramore." },
  { nom: "Arthas Menethil", f: "n", txt: "Prince héritier de Lordaeron et paladin, il purge Stratholme pour empêcher la peste de se répandre. Sa traque de Mal'Ganis le mène au Norfendre, où il s'empare de l'épée maudite Deuillegivre, puis rentre tuer son propre père et finit par s'unir au Roi-liche." },
  { nom: "Sylvanas Coursevent", f: "h", txt: "Générale des rôdeurs de Quel'Thalas, elle tombe en défendant son royaume contre Arthas, qui fait d'elle une banshee à son service. Libérée de l'emprise du Roi-liche, elle rassemble les morts-vivants libres sous le nom de Réprouvés et règne depuis Fossoyeuse." },
  { nom: "Illidan Hurlorage", f: "n", txt: "Frère jumeau de Malfurion, il crée un second Puits d'éternité après la Guerre des Anciens et passe dix mille ans emprisonné. Libéré par Tyrande, il absorbe la puissance du crâne de Gul'dan, devient mi-elfe mi-démon et est banni de son peuple." },
  { nom: "Malfurion Hurlorage", f: "a", txt: "Premier druide elfe de la nuit, formé par le demi-dieu Cénarius, il mène la résistance contre la Légion ardente lors de la Guerre des Anciens. Il passe ensuite de longs siècles endormi dans le Rêve d'émeraude, d'où son peuple le tire pour affronter de nouvelles menaces." },
  { nom: "Tyrande Murmevent", f: "a", txt: "Grande prêtresse de la déesse lunaire Élune, elle guide les elfes de la nuit depuis des millénaires. C'est elle qui libère Illidan de sa prison et qui combat aux côtés de Malfurion contre Archimonde, au pied de l'Arbre-Monde." },
  { nom: "Cairne Sabot-de-Sang", f: "h", txt: "Grand chef des taurens, il unit les tribus dispersées de son peuple, menacées par les centaures. Allié de Thrall, il installe les taurens au sommet des Pitons-du-Tonnerre, en Mulgore, et reste l'une des voix les plus sages de la Horde." },
  { nom: "Uther le Porteur de Lumière", f: "a", txt: "Premier paladin de l'ordre de la Main d'argent, il forme le jeune Arthas aux voies de la Lumière. Il refuse de participer à la purge de Stratholme et sera plus tard tué par son ancien élève, devenu chevalier de la mort." },
  { nom: "Medivh", f: "n", txt: "Dernier Gardien de Tirisfal, il est possédé dès sa naissance par l'esprit de Sargeras. Sous cette emprise, il aide le démoniste Gul'dan à ouvrir la Porte des ténèbres, laissant les orcs envahir Azeroth, avant d'être abattu dans sa tour de Karazhan par Khadgar et Anduin Lothar." },
  { nom: "Grom Hurlenfer", f: "h", txt: "Chef du clan Chanteguerre, il est le premier orc à boire le sang du démon Mannoroth. Rechuté en Kalimdor, il tue le demi-dieu Cénarius, puis se rachète avec l'aide de Thrall en abattant Mannoroth, libérant les orcs de leur malédiction au prix de sa vie." },
  { nom: "Kel'Thuzad", f: "n", txt: "Archimage de Dalaran passionné de nécromancie, il fonde le Culte des damnés et répand la peste au service du Roi-liche. Tué par Arthas puis ramené à la vie sous forme de liche, il dirige désormais le Fléau depuis la nécropole de Naxxramas." },
  { nom: "Ragnaros", f: "r", txt: "Seigneur élémentaire du feu, il est arraché au plan élémentaire par le roi nain Thaurissan des Sombrefer. Son arrivée ravage la région, qui devient les Steppes ardentes et la Gorge des Vents brûlants, et il règne depuis le Cœur du Magma, sous le mont Rochenoire." },
  { nom: "Onyxia", f: "n", txt: "Fille d'Aile de mort, elle prend forme humaine sous le nom de Dame Katrana Prestor et manipule en secret la cour de Hurlevent. Démasquée, elle se réfugie dans son repaire du marécage d'Âprefange, où les aventuriers viennent la défier." },
  { nom: "Nefarian", f: "n", txt: "Fils aîné d'Aile de mort, il se fait appeler Lord Victor Nefarius sous forme humaine. Depuis le Repaire de l'Aile noire, au sommet du mont Rochenoire, il mène des expériences pour créer une nouvelle race de dragons chromatiques." },
  { nom: "Gul'dan", f: "n", txt: "Démoniste orc ambitieux, il livre son peuple à la Légion ardente en échange de pouvoir. Il crée le Conseil des ombres et les premiers chevaliers de la mort, puis trahit la Horde pour chercher la Tombe de Sargeras, où il trouve la mort." },
  { nom: "Orgrim Marteau-du-Destin", f: "h", txt: "Chef de guerre de la Horde pendant la deuxième guerre, il renverse Main-Noire et tue Anduin Lothar au pied du mont Rochenoire. Captif après la défaite, il s'évade, se bat aux côtés de Thrall pour libérer les orcs et tombe au combat en lui léguant son armure et son marteau. Thrall baptise Orgrimmar en son honneur." },
  { nom: "Anduin Lothar", f: "a", txt: "Champion de Hurlevent et dernier descendant des rois d'Arathor, il mène les réfugiés de son royaume détruit vers Lordaeron. Commandant suprême de l'Alliance lors de la deuxième guerre, il tombe face à Orgrim Marteau-du-Destin." },
  { nom: "Vol'jin", f: "h", txt: "Chef des trolls Sombrelance, il doit à Thrall la survie de sa tribu, menacée par des hommes-poissons et une sorcière des mers. Par reconnaissance, il rejoint la Horde et installe les siens en Durotar, sur les îles de l'Écho." },
  { nom: "Magni Barbe-de-Bronze", f: "a", txt: "Roi des nains de Forgefer, il règne depuis la grande forge creusée dans les montagnes de Dun Morogh. Fidèle allié de l'Alliance, il finance aussi les fouilles de la Ligue des explorateurs pour percer le mystère des origines de son peuple." }
];
document.querySelectorAll("[data-lore]").forEach(box => {
  const all = [...ASTUCES.map(t => ({ t: "Astuce", txt: t })), ...PERSOS.map(p => ({ t: "Personnage", nom: p.nom, f: p.f, txt: p.txt }))];
  let last = -1;
  function show() {
    let i; do { i = Math.floor(Math.random() * all.length); } while (i === last && all.length > 1);
    last = i; const x = all[i];
    box.dataset.f = x.f || "astuce";
    box.innerHTML = `<small>${x.t === "Astuce" ? "Astuce de jeu" : "Les grandes figures"}</small>`
      + (x.nom ? `<b class="lore-nom">${x.nom}</b>` : `<b class="lore-nom">Le saviez-vous&nbsp;?</b>`)
      + `<p>${x.txt}</p><button type="button" class="lore-next">Une autre ↻</button>`;
    box.querySelector(".lore-next").onclick = show;
  }
  show();
});
