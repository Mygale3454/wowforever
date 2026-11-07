/* Dernières annonces officielles de Blizzard sur WoW Forever (page Roadmap).
   Pour en ajouter une : une ligne EN HAUT de la liste. date au format AAAA-MM-JJ, ou "" si inconnue.
   La veille quotidienne prépare ces lignes sur une branche ; elles sont publiées après l'accord de Mygale. */
const ANNONCES = [
  { date: "2026-11-06", titre: "L'aventure commence dans World of Warcraft: Forever : le résumé hebdomadaire", url: "https://worldofwarcraft.blizzard.com/fr-fr/news/24316097" },
  { date: "2026-11-05", titre: "World of Warcraft: Forever – Découvrez la vidéo « Forging Forever »", url: "https://worldofwarcraft.blizzard.com/fr-fr/news/24317865/world-of-warcraft-forever-d%C3%A9couvrez-la-vid%C3%A9o-forging-forever" },
  { date: "2026-11-03", titre: "Explorez WoW: Forever à une manette", url: "https://worldofwarcraft.blizzard.com/fr-fr/news/24316974/explorez-wow-forever-%C3%A0-une-manette" },
  { date: "", titre: "Préparez-vous pour Forever : le résumé hebdomadaire de World of Warcraft", url: "https://news.blizzard.com/fr-fr/article/24316094" },
  { date: "", titre: "World of Warcraft: Forever sort partout dans le monde le 5 novembre !", url: "https://news.blizzard.com/fr-fr/article/24315820" },
  { date: "", titre: "Retournez sur Azeroth dans World of Warcraft: Forever", url: "https://worldofwarcraft.blizzard.com/fr-fr/news/24315643" },
  { date: "", titre: "Guide de démarrage pour les novices", url: "https://worldofwarcraft.blizzard.com/fr-fr/news/24315280" },
  { date: "", titre: "Votre prochaine aventure dans WoW: Forever commence dans la WoW Portal Room", url: "https://worldofwarcraft.blizzard.com/fr-fr/news/24315203" },
  { date: "", titre: "Le système d'Héritage en détail", url: "https://worldofwarcraft.blizzard.com/fr-fr/news/24307383" },
  { date: "", titre: "Battez-vous pour les îles des Sombrelances", url: "https://worldofwarcraft.blizzard.com/fr-fr/news/24307308" },
  { date: "2026-09-17", titre: "La bêta de World of Warcraft: Forever est désormais disponible", url: "https://news.blizzard.com/fr-fr/article/24304160" },
  { date: "", titre: "Fonctionnement de la progression JcJ dans World of Warcraft: Forever", url: "https://worldofwarcraft.blizzard.com/fr-fr/news/24303316" },
  { date: "", titre: "Aperçu des raids de World of Warcraft: Forever", url: "https://worldofwarcraft.blizzard.com/fr-fr/news/24303009" },
  { date: "", titre: "Découvrez les nouveaux donjons de World of Warcraft: Forever", url: "https://worldofwarcraft.blizzard.com/fr-fr/news/24301455" }
];
(() => {
  const el = document.getElementById("annonces"); if (!el) return;
  const M = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."];
  const d = s => { if (!s) return ""; const [a, m, j] = s.split("-"); return `${+j} ${M[m - 1]} ${a}`; };
  const esc = s => s.replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  el.innerHTML = ANNONCES.slice(0, 8).map(a =>
    `<li><a href="${esc(a.url)}" target="_blank" rel="noopener">${esc(a.titre)} ↗</a>${a.date ? `<span>${d(a.date)}</span>` : ""}</li>`).join("");
})();
