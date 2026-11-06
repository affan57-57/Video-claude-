// Shared deterministic helpers for the Frescura #4 sub-compositions.
window.HF = {
  rng(seed) { let s = seed >>> 0; return () => ((s = (s * 1664525 + 1013904223) % 4294967296) / 4294967296); },
  at(T0) { return (t) => Math.max(0, +(t - T0).toFixed(3)); },
  glyphs(el) {
    const txt = el.textContent.trim().replace(/\s+/g, " "); el.textContent = "";
    txt.split("").forEach((ch) => { const m = document.createElement("span"); m.className = "mask"; const s = document.createElement("span"); s.textContent = ch === " " ? " " : ch; m.appendChild(s); el.appendChild(m); });
    return el.querySelectorAll(".mask > span");
  },
  smoke(container, n, rnd, color) {
    const out = [];
    for (let i = 0; i < n; i++) {
      const b = document.createElement("div"); const r = 380 + rnd() * 420;
      Object.assign(b.style, { position: "absolute", width: r + "px", height: r + "px", left: -200 + rnd() * 1100 + "px", top: rnd() * 1700 + "px", borderRadius: "50%", background: `radial-gradient(circle, ${color} 0%, rgba(0,0,0,0) 65%)`, filter: "blur(30px)" });
      container.appendChild(b); out.push(b);
    }
    return out;
  },
  bubbles(container, n, area, rnd) {
    const out = [];
    for (let i = 0; i < n; i++) {
      const b = document.createElement("div"); const r = 14 + rnd() * 46; b.className = "bub";
      Object.assign(b.style, { width: r + "px", height: r + "px", left: area.x + rnd() * area.w + "px", top: area.y + rnd() * area.h + "px" });
      container.appendChild(b); out.push(b);
    }
    return out;
  },
};
window.E = "expo.out"; window.P = "power3.out"; window.B = "back.out(1.7)";
