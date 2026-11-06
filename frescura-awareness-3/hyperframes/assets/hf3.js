// Shared helpers for the Frescura #3 sub-compositions (deterministic only).
window.HF = {
  rng(seed) {
    let s = seed >>> 0;
    return () => ((s = (s * 1664525 + 1013904223) % 4294967296) / 4294967296);
  },
  // root-time → local-time converter for a composition mounted at T0
  at(T0) {
    return (t) => Math.max(0, +(t - T0).toFixed(3));
  },
  // split text into masked glyph spans for reveal animations
  glyphs(el) {
    const txt = el.textContent;
    el.textContent = "";
    txt.split("").forEach((ch) => {
      const m = document.createElement("span");
      m.className = "mask";
      const s = document.createElement("span");
      s.textContent = ch === " " ? " " : ch;
      m.appendChild(s);
      el.appendChild(m);
    });
    return el.querySelectorAll(".mask > span");
  },
  bubbles(container, n, area, rnd) {
    const out = [];
    for (let i = 0; i < n; i++) {
      const b = document.createElement("div");
      const r = 14 + rnd() * 48;
      b.className = "bub";
      Object.assign(b.style, { width: r + "px", height: r + "px", left: area.x + rnd() * area.w + "px", top: area.y + rnd() * area.h + "px" });
      container.appendChild(b);
      out.push(b);
    }
    return out;
  },
};
window.E = "expo.out";
window.P = "power3.out";
window.B = "back.out(1.7)";
