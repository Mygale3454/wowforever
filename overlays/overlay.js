/* ===== Overlays wowforever – réglages par l'adresse =====
   ?nom=TonPseudo      → ton pseudo affiché sur les overlays
   ?min=10             → durée du compte à rebours (écran d'attente), en minutes
   ?prochain=Jeudi 21h → date du prochain live (écran de fin)
   Exemple : attente.html?nom=Mygale&min=5                                    */
const P = new URLSearchParams(location.search);
const NOM = P.get("nom") || "wowforever";
document.querySelectorAll("[data-nom]").forEach(e => e.textContent = NOM);
if (P.get("prochain")) document.querySelectorAll("[data-prochain]").forEach(e => e.textContent = P.get("prochain"));

/* Braises */
document.querySelectorAll(".embers").forEach(box => {
  for (let i = 0; i < 28; i++) {
    const e = document.createElement("i");
    e.style.left = Math.random() * 100 + "%";
    e.style.animationDuration = 9 + Math.random() * 10 + "s";
    e.style.animationDelay = -Math.random() * 18 + "s";
    const s = 3 + Math.random() * 5; e.style.width = e.style.height = s + "px";
    box.appendChild(e);
  }
});

/* Astuces WoW Forever qui défilent */
const TIPS = [
  "Le niveau maximum de <b>WoW Forever</b> restera à <b>60</b> : pas d'extension qui rend ton équipement obsolète.",
  "Les <b>Skyborne</b> sont la nouvelle race jouable, avec leur départ sur l'île de Zephras.",
  "La Horde a enfin ses <b>paladins</b> : les morts-vivants !",
  "Les nains peuvent désormais devenir <b>chamans</b> côté Alliance.",
  "<b>Neuf nouveaux donjons</b> attendent les aventuriers, du niveau 13 au 60.",
  "Les <b>raids</b> ouvrent le 9 décembre, en format 10 et 20 joueurs.",
  "Pense à installer un feu de <b>camp</b> : c'est un vrai lieu de rencontre dans Forever.",
  "Les points <b>Legacy</b> sont partagés sur tout ton compte : varie tes personnages !",
  "Le mode <b>Hardcore</b> (une seule vie) arrive cet hiver.",
  "Pas de montures volantes : <b>bateaux et zeppelins</b> restent les rois du voyage."
];
document.querySelectorAll("[data-tips]").forEach(el => {
  let i = Math.floor(Math.random() * TIPS.length);
  const show = () => { el.style.opacity = 0; setTimeout(() => { el.innerHTML = TIPS[i++ % TIPS.length]; el.style.opacity = 1; }, 600); };
  show(); setInterval(show, 12000);
});

/* Compte à rebours de l'écran d'attente */
const timer = document.querySelector("[data-timer]");
if (timer) {
  const end = Date.now() + (parseFloat(P.get("min")) || 10) * 60000;
  const b = timer.querySelectorAll("b"), pad = n => String(n).padStart(2, "0");
  const tick = () => {
    const d = Math.max(0, end - Date.now());
    b[0].textContent = pad(Math.floor(d / 60000)); b[1].textContent = pad(Math.floor(d / 1000) % 60);
    if (d === 0) { document.querySelector("[data-ready]").textContent = "C'est parti !"; clearInterval(t); }
  };
  const t = setInterval(tick, 250); tick();
}

/* Compte à rebours jusqu'à la sortie de WoW Forever (overlay de jeu) */
document.querySelectorAll("[data-sortie]").forEach(el => {
  const target = Date.UTC(2026, 10, 4, 23, 0, 0);
  const tick = () => {
    const d = target - Date.now();
    if (d <= 0) { el.innerHTML = "WoW Forever <span>est sorti !</span>"; return; }
    el.innerHTML = `Sortie de WoW Forever dans <span>${Math.floor(d / 864e5)} j ${Math.floor(d / 36e5) % 24} h</span>`;
  };
  tick(); setInterval(tick, 30000);
});
