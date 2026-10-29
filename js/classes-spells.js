/* Liste dépliable des sorts de chaque classe (page Classes).
   Les noms renvoient vers Wowhead, qui affiche la description au survol. */
(() => {
  const ST = { new: '<span class="rtag new">Nouveau</span>', chg: '<span class="rtag chg">Modifié</span>', "": "" };
  document.querySelectorAll("details.spells").forEach(d => {
    d.addEventListener("toggle", () => {
      if (!d.open || d.dataset.done) return;
      d.dataset.done = 1;
      const L = ((typeof SPELLS !== "undefined" && SPELLS) || {})[d.dataset.class] || [];
      const by = {};
      L.forEach(s => (by[s.l] = by[s.l] || []).push(s));
      d.querySelector(".spl").innerHTML =
        `<div class="spl-tools"><input type="search" placeholder="Chercher un sort…" aria-label="Chercher un sort">
          <label><input type="checkbox" data-new> Nouveautés et changements seulement</label><span class="spl-count">${L.length} sorts</span></div>
         <div class="spl-list">${Object.keys(by).sort((a, b) => a - b).map(l => `
          <div class="spl-lvl"><b>Niv. ${l}</b><div>${by[l].map(s => `
            <a class="spl-item${s.s ? " is-" + s.s : ""}" data-n="${s.n.toLowerCase()}" href="https://www.wowhead.com/forever/spell=${s.id}" target="_blank" rel="noopener">${s.n}${s.r > 1 ? ` <small>${s.r} rangs</small>` : ""}${s.p ? " <small>passif</small>" : ""} ${ST[s.s]}</a>`).join("")}</div></div>`).join("")}</div>`;
      if (window.$WowheadPower) try { $WowheadPower.refreshLinks(); } catch (e) {}
      const q = d.querySelector('input[type="search"]'), nw = d.querySelector("[data-new]");
      const filt = () => {
        const t = q.value.trim().toLowerCase();
        d.querySelectorAll(".spl-item").forEach(a => a.hidden = (t && !a.dataset.n.includes(t)) || (nw.checked && !/is-(new|chg)/.test(a.className)));
        d.querySelectorAll(".spl-lvl").forEach(g => g.hidden = ![...g.querySelectorAll(".spl-item")].some(a => !a.hidden));
      };
      q.oninput = filt; nw.onchange = filt;
    });
  });
})();
