/* Vidéos : la vignette est remplacée par le lecteur YouTube seulement au clic (pas de cookies ni de chargement avant) */
document.addEventListener("click", e => {
  const b = e.target.closest(".vid-play"); if (!b) return;
  const f = document.createElement("iframe");
  f.src = `https://www.youtube-nocookie.com/embed/${b.dataset.id}?autoplay=1&rel=0`;
  f.title = b.getAttribute("aria-label") || "Vidéo";
  f.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
  f.allowFullscreen = true;
  const w = document.createElement("div"); w.className = "video vid-frame"; w.appendChild(f);
  b.replaceWith(w);
});
