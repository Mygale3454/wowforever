/* Carte interactive WoW Forever (Leaflet, CRS simple, coordonnées 0-100 du jeu) */
(() => {
  const W = 1002, H = 668;
  const LAYERS = [
    ["class", "Maîtres de classe", "#e8b230", 7], ["prof", "Maîtres de métiers", "#8e5ac8", 7], ["fly", "Maîtres de vol", "#2f9be0", 8],
    ["inn", "Aubergistes et écuries", "#e06a2f", 7], ["bank", "Banque et enchères", "#3c9a4a", 7],
    ["herb", "Herbes", "#5fd35f", 3.5], ["ore", "Filons de minerai", "#c9c9c9", 3.5]
  ];
  const KEY = "wowforever-carte";
  const get = () => { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; } };
  const save = v => { try { localStorage.setItem(KEY, JSON.stringify(v)); } catch (e) {} };
  const st = Object.assign({ zone: 1429, off: ["herb", "ore"] }, get());
  const map = L.map("map", { crs: L.CRS.Simple, minZoom: -1, maxZoom: 3, zoomSnap: 0.25, attributionControl: false, preferCanvas: true });
  const bounds = [[0, 0], [H, W]];
  let img = null, groups = {}, zones = [];
  const toLL = (x, y) => [H - y / 100 * H, x / 100 * W];
  const esc = s => s.replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  const ui = document.getElementById("map-layers");
  ui.innerHTML = LAYERS.map(([k, n, c]) => `<label class="ml"><input type="checkbox" data-k="${k}" ${st.off.includes(k) ? "" : "checked"}><i style="background:${c}"></i>${n} <span class="mc" data-c="${k}"></span></label>`).join("");
  ui.addEventListener("change", e => {
    const k = e.target.dataset.k; if (!k) return;
    st.off = st.off.filter(x => x !== k); if (!e.target.checked) st.off.push(k);
    save(st); e.target.checked ? groups[k].addTo(map) : map.removeLayer(groups[k]);
  });

  function load(id) {
    st.zone = +id; save(st);
    Object.values(groups).forEach(g => map.removeLayer(g)); groups = {};
    if (img) map.removeLayer(img);
    img = L.imageOverlay(`images/cartes/${id}.webp`, bounds).addTo(map);
    map.setMaxBounds([[-80, -120], [H + 80, W + 120]]); map.fitBounds(bounds);
    fetch(`data/carte/${id}.json`).then(r => r.json()).then(pts => {
      LAYERS.forEach(([k, , c, r]) => groups[k] = L.layerGroup());
      const cnt = {};
      pts.forEach(([k, x, y, n, role]) => {
        const L0 = LAYERS.find(l => l[0] === k); if (!L0) return;
        cnt[k] = (cnt[k] || 0) + 1;
        const m = L.circleMarker(toLL(x, y), { radius: L0[3], color: "#111", weight: 1, fillColor: L0[2], fillOpacity: .95 });
        const way = `/way ${x} ${y} ${n}`;
        m.bindPopup(`<b>${esc(n)}</b>${role ? `<br><span class="mp-r">${esc(role)}</span>` : ""}<br><span class="mp-xy">${x}, ${y}</span><br><button type="button" class="mp-copy" data-w="${esc(way)}">Copier pour TomTom</button>`);
        m.bindTooltip(esc(n), { direction: "top", offset: [0, -4] });
        m.addTo(groups[k]);
      });
      LAYERS.forEach(([k]) => { if (!st.off.includes(k)) groups[k].addTo(map); const s = ui.querySelector(`[data-c="${k}"]`); s.textContent = cnt[k] ? `(${cnt[k]})` : "(0)"; });
    });
  }
  map.on("popupopen", e => {
    const b = e.popup.getElement().querySelector(".mp-copy"); if (!b) return;
    b.onclick = () => { const t = b.dataset.w; (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(() => b.textContent = "Copié !", () => b.textContent = t); };
  });
  const coord = document.getElementById("map-coord");
  map.on("mousemove", e => { const x = e.latlng.lng / W * 100, y = (H - e.latlng.lat) / H * 100; coord.textContent = x >= 0 && x <= 100 && y >= 0 && y <= 100 ? `${x.toFixed(1)}, ${y.toFixed(1)}` : ""; });

  const sel = document.getElementById("map-zone");
  fetch("data/carte/zones.json").then(r => r.json()).then(z => {
    zones = z;
    const grp = { e: "Royaumes de l'Est", k: "Kalimdor", z: "Île de Zéphras" };
    sel.innerHTML = Object.entries(grp).map(([g, n]) => `<optgroup label="${n}">${z.filter(x => x.c === g).map(x => `<option value="${x.id}">${x.nom}</option>`).join("")}</optgroup>`).join("");
    const q = new URLSearchParams(location.hash.slice(1)).get("zone");
    const start = z.some(x => x.id == q) ? q : (z.some(x => x.id == st.zone) ? st.zone : z[0].id);
    sel.value = start; load(start);
  });
  sel.addEventListener("change", () => { history.replaceState(null, "", "#zone=" + sel.value); load(sel.value); });
})();
