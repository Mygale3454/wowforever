/* ===== Fil de news wowforever =====
   Pour ajouter une news : ajoute une ligne EN HAUT de la liste.
   type : "actu" (actualité du jeu), "guide" (guide ou article), "site" (nouveauté sur le site)
   La plus récente s'affiche automatiquement en grand en haut de la page. */
const NEWS = [
  { date: "2026-10-30", type: "actu", lien: "races.html", img: "images/skyborne.jpg",
    titre: "Derniers changements des raciaux avant la sortie",
    texte: "Impitoyable passe à 1 %, l'Esprit humain à 10 %, le nain gagne +1 % de toucher, l'orc retrouve Commandement et les Éolides passent à 2 % de hâte. La page Races est à jour." },
  { date: "2026-10-30", type: "guide", lien: "leveling.html", img: "images/galerie/05.jpg",
    titre: "Leveling 1 à 60 : le parcours zone par zone",
    texte: "Ta zone de départ, puis les zones à enchaîner par tranche de niveau, pour l'Alliance et la Horde, avec les guides de quêtes Polestar." },
  { date: "2026-10-30", type: "actu", lien: "news-stats-beta.html", img: "images/galerie/08.jpg",
    titre: "Bêta fermée : près de 9 millions de personnages créés",
    texte: "1,9 million d'Éolides, 612 000 paladins morts-vivants et plus d'un million de morts par chute : Blizzard partage les chiffres de la bêta." },
  { date: "2026-10-30", type: "guide", lien: "news-montures.html", img: "images/galerie/03.jpg",
    titre: "Montures : ce qui change dans WoW Forever",
    texte: "Monte au niveau 40, montures liées au compte, trotteurs des Éolides, kodo de bât et ours spectral : l'essentiel avant de galoper." },
  { date: "2026-10-29", type: "guide", lien: "guides.html", img: "images/classes.jpg",
    titre: "Les guides des 27 spécialisations sont en ligne",
    texte: "Rôle, points forts et faibles, build de talents à ouvrir en un clic dans le calculateur, priorité des statistiques et races conseillées." },
  { date: "2026-10-29", type: "site", lien: "races.html", img: "images/skyborne.jpg",
    titre: "Quelle race choisir ? Le comparatif des 9 races",
    texte: "Capacités raciales, classes jouables et sorts de prêtre propres à chaque race, avec les nouveaux Skyborne." },
  { date: "2026-10-29", type: "site", lien: "metiers.html", img: "images/camping.jpg",
    titre: "Nouvelle page Métiers : nouveautés et guides 1 à 300",
    texte: "Les 12 métiers de Forever, leurs objets de camp, la Faveur marchande et les meilleurs guides pour les monter, en français et en anglais." },
  { date: "2026-10-29", type: "actu", lien: "news-destinations.html", img: "images/galerie/02.jpg",
    titre: "Norfendre, Pandarie, Gilnéas : où ira WoW Forever ?",
    texte: "Les développeurs partagent leurs idées pour les futures destinations du jeu, dont un Norfendre de niveau 60 avant l'arrivée du roi-liche. Rien n'est confirmé, mais les pistes font rêver." },
  { date: "2026-10-29", type: "actu", lien: "news-graphismes.html", img: "images/galerie/04.jpg",
    titre: "Les graphismes de Forever pourraient arriver sur le WoW moderne",
    texte: "Brouillard volumétrique, lumière, ombres et eau : Blizzard envisage de porter ces améliorations sur Retail." },
  { date: "2026-10-29", type: "site", lien: "legacy.html", img: "images/legacy.jpg",
    titre: "La page Héritage fait peau neuve",
    texte: "Les 65 défis à cocher pour compter tes points, les 21 avantages des trois arbres, les récompenses de l'ours spectral et le mode Extrême." },
  { date: "2026-10-28", type: "site", lien: "pvp.html", img: "images/jcj.jpg",
    titre: "Nouvel onglet PvP : honneur, rangs et champs de bataille",
    texte: "Les 14 rangs et leurs récompenses, le PvP sauvage et les quatre champs de bataille, dont les nouvelles Îles des Sombrelances." },
  { date: "2026-10-28", type: "guide", lien: "article-addons.html", img: "images/galerie/18.jpg",
    titre: "Les meilleurs addons pour WoW Forever",
    texte: "Questie, Polestar, TomTom, EllesmereUI, Auctionator… notre sélection pour bien démarrer le 4 novembre." },
  { date: "2026-10-28", type: "site", lien: "talents.html", img: "images/classes.jpg",
    titre: "Le calculateur de talents est en ligne",
    texte: "Les 466 talents des 9 classes, avec icônes, règles de Forever et lien pour partager ton build." },
  { date: "2026-10-28", type: "actu", lien: "news-bande-annonce.html", img: "images/une.jpg",
    titre: "« Sentier de la guerre » : la bande-annonce de lancement",
    texte: "Un clip animé façon anime : l'Alliance et la Horde s'affrontent sur les pentes du Mont Hyjal." },
  { date: "2026-10-28", type: "site", lien: "addons.html", img: "images/galerie/18.jpg",
    titre: "La page Addons s'agrandit : 11 addons classés par usage",
    texte: "Leveling, exploration, interface, donjons et hôtel des ventes, avec les liens officiels de chaque addon." },
  { date: "2026-10-26", type: "site", lien: "donjons.html", img: "images/donjons.jpg",
    titre: "Les 29 donjons de Forever, avec des liens vers les meilleurs guides",
    texte: "Niveaux, emplacements et une sélection de guides en français et en anglais pour chaque donjon." },
  { date: "2026-10-26", type: "site", lien: "classes.html", img: "images/galerie/17.jpg",
    titre: "Une fiche pour chacune des 9 classes",
    texte: "Rôles, races jouables, nouvelles combinaisons de Forever et spécialisations préférées des joueurs." },
  { date: "2026-10-26", type: "site", lien: "galerie.html", img: "images/galerie/03.jpg",
    titre: "Ouverture de la galerie",
    texte: "Nos plus belles captures d'Azeroth, à agrandir d'un clic." },
  { date: "2026-10-26", type: "actu", lien: "article-recap.html", img: "images/actus.jpg",
    titre: "WoW Forever : le récap avant le lancement",
    texte: "Niveau 60 bloqué, race Skyborne, neuf donjons inédits, Héritage, camping : tout ce qu'il faut savoir sur le « Classic+ » de Blizzard." },
  { date: "2026-10-26", type: "guide", lien: "debuter.html", img: "images/debuter.jpg",
    titre: "Guide : bien débuter sur WoW Forever",
    texte: "Accès, modes de jeu, changements de gameplay et camping : le guide pour ton premier personnage." },
  { date: "2026-10-26", type: "actu", lien: "calendrier.html", img: "images/raids.jpg",
    titre: "Les raids ouvrent le 9 décembre",
    texte: "Un peu plus d'un mois après le lancement, place aux raids 10 et 20 joueurs." },
  { date: "2026-10-26", type: "actu", lien: "calendrier.html", img: "images/hardcore.jpg",
    titre: "Le mode Hardcore prévu cet hiver",
    texte: "Une seule vie par personnage, arrivée attendue fin 2026 ou début 2027." },
  { date: "2026-10-26", type: "actu", lien: "debuter.html", img: "images/camping.jpg",
    titre: "Camping et 600 nouvelles recettes",
    texte: "Les métiers sont repensés avec un système de camp à construire." }
];

(() => {
  const TYPES = { actu: ["Actu", "red"], guide: ["Guide", ""], site: ["Nouveau sur le site", "green"] };
  const MOIS = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"];
  const fmt = d => { const [y, m, j] = d.split("-").map(Number); return `${j} ${MOIS[m - 1]} ${y}`; };
  const recent = d => (Date.now() - new Date(d + "T12:00:00")) / 864e5 < 2.5;
  const list = NEWS.map((n, i) => ({ ...n, i })).sort((a, b) => b.date.localeCompare(a.date) || a.i - b.i);
  const badge = n => `<span class="badge ${TYPES[n.type][1]}">${TYPES[n.type][0]}</span>`;

  const f = list[0];
  document.getElementById("featured").innerHTML = `
    <a class="hero" href="${f.lien}">
      <img src="${f.img}" alt="">
      <div class="hero-body">${badge(f)} <span class="date">${fmt(f.date)}</span>
        <h1>${f.titre}</h1><p>${f.texte}</p></div>
    </a>`;

  let filtre = "all", shown = 8;
  function render() {
    const items = list.slice(1).filter(n => filtre === "all" || n.type === filtre);
    document.getElementById("feed").innerHTML = items.slice(0, shown).map(n => `
      <a class="nitem" href="${n.lien}">
        <div class="nthumb"><img src="${n.img}" alt="" loading="lazy"></div>
        <div class="nbody">
          <div class="nmeta">${badge(n)}<span class="date">${fmt(n.date)}</span>${recent(n.date) ? '<span class="nnew">Nouveau</span>' : ""}</div>
          <h3>${n.titre}</h3><p>${n.texte}</p>
        </div>
      </a>`).join("") +
      (items.length > shown ? `<button class="nmore" id="nmore">Plus de news (${items.length - shown})</button>` : "");
    const more = document.getElementById("nmore");
    if (more) more.onclick = () => { shown += 8; render(); };
  }
  document.getElementById("nfilters").addEventListener("click", e => {
    if (e.target.tagName !== "BUTTON") return;
    document.querySelectorAll("#nfilters button").forEach(b => b.classList.toggle("on", b === e.target));
    filtre = e.target.dataset.f; shown = 8; render();
  });
  render();
})();
