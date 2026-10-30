/* Leveling pas à pas : cases à cocher mémorisées, filtre par classe, progression */
(() => {
  const bar = document.querySelector(".pp-bar");
  if (!bar) return;
  const KEY = "wowforever-pas-a-pas-" + bar.dataset.guide;
  const CKEY = "wowforever-pas-a-pas-classe";
  const get = (k, d) => { try { return JSON.parse(localStorage.getItem(k)) ?? d; } catch (e) { return d; } };
  const set = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} };
  const steps = [...document.querySelectorAll(".pp > .pp-st")];
  let done = get(KEY, []);
  const sel = document.getElementById("pp-class");
  sel.value = get(CKEY, "");

  function refresh() {
    const c = sel.value;
    let n = 0, total = 0, ok = 0;
    steps.forEach((s, i) => {
      const show = !c || !s.dataset.only || s.dataset.only.split(" ").includes(c);
      s.hidden = !show;
      s.querySelectorAll("li[data-only]").forEach(li => li.hidden = !!c && !li.dataset.only.split(" ").includes(c));
      if (!show) return;
      n++; total++;
      s.querySelector(".st-n").textContent = n;
      const cb = s.querySelector("input");
      cb.checked = done.includes(i);
      s.classList.toggle("done", cb.checked);
      if (cb.checked) ok++;
    });
    bar.querySelector(".pp-fill").style.width = (total ? 100 * ok / total : 0) + "%";
    bar.querySelector(".pp-count").textContent = `${ok} / ${total} étapes`;
  }
  steps.forEach((s, i) => s.querySelector("input").addEventListener("change", e => {
    done = done.filter(x => x !== i);
    if (e.target.checked) done.push(i);
    set(KEY, done); refresh();
    if (e.target.checked) {
      const next = steps.slice(i + 1).find(x => !x.hidden && !x.classList.contains("done"));
      if (next && next.getBoundingClientRect().top > innerHeight * 0.8) next.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  }));
  sel.addEventListener("change", () => { set(CKEY, sel.value); refresh(); });
  document.getElementById("pp-reset").addEventListener("click", () => { done = []; set(KEY, done); refresh(); });
  refresh();
})();
