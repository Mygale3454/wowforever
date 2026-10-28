/* Compteur de points d'Héritage — progression gardée dans le navigateur du visiteur */
(() => {
  const KEY = "wowforever-heritage";
  let done = {};
  try { done = JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) {}
  const boxes = [...document.querySelectorAll("[data-h]")];
  boxes.forEach(b => { b.checked = !!done[b.dataset.h]; });

  function update() {
    const total = boxes.filter(b => b.checked).length;
    document.getElementById("htotal").textContent = total;
    document.querySelectorAll(".hcat").forEach(c => {
      const bs = [...c.querySelectorAll("[data-h]")], n = bs.filter(b => b.checked).length;
      const el = c.querySelector(".hpts"); el.textContent = `${n} / ${bs.length}`; el.classList.toggle("full", n === bs.length);
    });
    document.getElementById("hbarfill").style.width = (total / 65 * 100) + "%";
    let next = null;
    document.querySelectorAll(".hrew").forEach(r => {
      const ok = total >= +r.dataset.need; r.classList.toggle("ok", ok);
      r.querySelector(".hstate").textContent = ok ? "Débloqué !" : `Encore ${r.dataset.need - total} point${r.dataset.need - total > 1 ? "s" : ""}`;
      if (!ok && next === null) next = +r.dataset.need;
    });
    document.getElementById("hnext").textContent = next ? `Prochaine récompense : ${next} points` : "Toutes les récompenses sont débloquées !";
  }
  document.addEventListener("change", e => {
    if (!e.target.matches("[data-h]")) return;
    if (e.target.checked) done[e.target.dataset.h] = 1; else delete done[e.target.dataset.h];
    try { localStorage.setItem(KEY, JSON.stringify(done)); } catch (err) {}
    update();
  });
  document.getElementById("hreset").onclick = () => { boxes.forEach(b => b.checked = false); done = {}; try { localStorage.removeItem(KEY); } catch (e) {} update(); };
  update();
})();
