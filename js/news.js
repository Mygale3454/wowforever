/* ===== Fil de news wowforever =====
   Pour ajouter une news : ajoute une ligne EN HAUT de la liste.
   type : "actu" (actualité du jeu), "guide" (guide ou article), "site" (nouveauté sur le site)
   La plus récente s'affiche automatiquement en grand en haut de la page. */
const NEWS = [
  { date: "2026-11-04", type: "guide", lien: "news-build-mage.html", img: "images/news/build-mage.jpg",
    titre: "Mon build de leveling : mage Arcanes 36/12/3",
    texte: "Le build que je vais suivre dès ce soir, d'après JudgeHype : ordre des talents, rotation et conseils. Sortie de WoW Forever à minuit !" },
  { date: "2026-11-04", type: "site", lien: "bis.html", img: "images/bis/mage.webp",
    titre: "Nouveau menu Équipement : le BiS du niveau 60",
    texte: "Pour chaque classe, la meilleure pièce de chaque emplacement avant les raids, où l'obtenir, et les caractéristiques au survol." },
  { date: "2026-11-03", type: "actu", lien: "news-notes-lancement.html", img: "images/une.jpg",
    titre: "Notes de lancement : toutes les classes renforcées",
    texte: "223 changements avant la sortie : poisons du voleur doublés, Explosion de lave retirée au chaman, gros bonus pour le druide farouche… Calculateur de talents et builds déjà à jour." },
  { date: "2026-11-02", type: "guide", lien: "familiers-demoniste.html", img: "images/montures/demoniste.webp",
    titre: "Guide des familiers du démoniste",
    texte: "Diablotin, marcheur du Vide, succube, nouvel incube, chasseur corrompu, infernal et garde funeste : à quoi sert chaque démon, ses sorts, le prix des grimoires et les talents qui le renforcent." },
  { date: "2026-11-01", type: "guide", lien: "montures.html", img: "images/monture-eolide.jpg",
    titre: "Guide des montures : où les acheter et comment les obtenir",
    texte: "Montures de chaque race et leurs marchands, trotteurs des trombes des Éolides, montures de classe, de réputation, de JcJ et de raid." },
  { date: "2026-11-01", type: "guide", lien: "talents.html", img: "images/news/talents.jpg",
    titre: "Calculateur de talents à jour du patch de sortie",
    texte: "Les arbres de talents passent au patch 1.60.1.70707 : talents ajoutés, retirés et retouchés, surtout chez le mage, le chaman élémentaire et le prêtre ombre. Les builds des guides de spé ont été adaptés." },
  { date: "2026-11-01", type: "guide", lien: "tier-list.html", img: "images/news/tier-list.jpg",
    titre: "Tier lists niveau 60 : dégâts, tanks, soigneurs et JcJ",
    texte: "Les spés les plus fortes au niveau 60 d'après la bêta, avec la date et le patch de chaque classement. Les builds affichent aussi leur date de création et leur patch." },
  { date: "2026-11-01", type: "site", lien: "carte.html", img: "images/news/carte.jpg",
    titre: "Nouvel outil : la carte interactive",
    texte: "50 zones avec les maîtres de classe et de métiers, les maîtres de vol, les aubergistes, les herbes et les filons de minerai, et un bouton pour copier les coordonnées dans TomTom." },
  { date: "2026-11-01", type: "site", lien: "addons.html", img: "images/news/addons.jpg",
    titre: "Deux addons de plus : ElvUI et Baganator",
    texte: "ElvUI, la célèbre refonte d'interface, prend désormais en charge WoW Forever, et Baganator réunit tous tes sacs dans une seule fenêtre triée." },
  { date: "2026-10-31", type: "guide", lien: "quetes-de-classe.html", img: "images/news/quetes-de-classe.jpg",
    titre: "Toutes les quêtes de classe, pas à pas",
    texte: "Forme d'ours et de félin, Poisons, totems du chaman, montures du paladin et du démoniste : 66 guides en français, rangés par classe et par niveau." },
  { date: "2026-10-31", type: "guide", lien: "metiers-pas-a-pas.html", img: "images/news/metiers.jpg",
    titre: "Les 12 métiers de 1 à 300, pas à pas",
    texte: "Où apprendre, quoi récolter ou acheter, quoi fabriquer à chaque palier, avec les composants par recette et un filtre Alliance / Horde." },
  { date: "2026-10-31", type: "site", lien: "pseudo.html", img: "images/galerie/16.jpg",
    titre: "Nouvel outil : le générateur de pseudo",
    texte: "Des noms originaux pour chaque race, masculins ou féminins, qui respectent les règles du jeu. Prépare tes idées avant le 4 novembre !" },
  { date: "2026-10-31", type: "guide", lien: "pas-a-pas.html", img: "images/galerie/09.jpg",
    titre: "Le leveling pas à pas va maintenant jusqu'au niveau 60",
    texte: "36 nouvelles zones pour les niveaux 30 à 60, de Désolace à Silithus : 57 zones en tout, en français, à enchaîner de la création du personnage jusqu'au niveau maximum." },
  { date: "2026-10-31", type: "guide", lien: "pas-a-pas.html", img: "images/galerie/11.jpg",
    titre: "Leveling pas à pas : les zones 10 à 30 sont en ligne",
    texte: "Marche de l'Ouest, Sombrivage, Les Tarides, Pins-Argentés, Orneval… 13 nouvelles zones en français, avec un bouton « zone suivante » pour enchaîner." },
  { date: "2026-10-31", type: "guide", lien: "pas-a-pas.html", img: "images/galerie/05.jpg",
    titre: "Nouveau : le leveling pas à pas, en français",
    texte: "Les 8 zones de départ quête par quête, avec cases à cocher, filtre par classe et progression mémorisée." },
  { date: "2026-10-30", type: "guide", lien: "reputations.html", img: "images/galerie/12.jpg",
    titre: "Toutes les réputations de WoW Forever",
    texte: "La Faveur marchande et les caisses égarées, une quinzaine de nouvelles factions et les guides des factions de Classic." },
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
  { date: "2026-10-29", type: "guide", lien: "guides.html", img: "images/news/talents.jpg",
    titre: "Les guides des 27 spécialisations sont en ligne",
    texte: "Rôle, points forts et faibles, build de talents à ouvrir en un clic dans le calculateur, priorité des statistiques et races conseillées." },
  { date: "2026-10-29", type: "site", lien: "races.html", img: "images/skyborne.jpg",
    titre: "Quelle race choisir ? Le comparatif des 9 races",
    texte: "Capacités raciales, classes jouables et sorts de prêtre propres à chaque race, avec les nouveaux Skyborne." },
  { date: "2026-10-29", type: "site", lien: "metiers.html", img: "images/news/metiers.jpg",
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
  { date: "2026-10-28", type: "guide", lien: "article-addons.html", img: "images/news/addons.jpg",
    titre: "Les meilleurs addons pour WoW Forever",
    texte: "Questie, Polestar, TomTom, EllesmereUI, Auctionator… notre sélection pour bien démarrer le 4 novembre." },
  { date: "2026-10-28", type: "site", lien: "talents.html", img: "images/news/talents.jpg",
    titre: "Le calculateur de talents est en ligne",
    texte: "Les 466 talents des 9 classes, avec icônes, règles de Forever et lien pour partager ton build." },
  { date: "2026-10-28", type: "actu", lien: "news-bande-annonce.html", img: "images/une.jpg",
    titre: "« Sentier de la guerre » : la bande-annonce de lancement",
    texte: "Un clip animé façon anime : l'Alliance et la Horde s'affrontent sur les pentes du Mont Hyjal." },
  { date: "2026-10-28", type: "site", lien: "addons.html", img: "images/news/addons.jpg",
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
