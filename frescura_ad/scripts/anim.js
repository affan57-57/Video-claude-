const tl = gsap.timeline({ paused: true });
const $ = (s) => document.querySelector(s);
const $$ = (s) => Array.from(document.querySelectorAll(s));
const INIT = new Map();
const ft = (t, el, from, to) => {
  const m = INIT.get(el) || {}; Object.keys(from).forEach((k) => { if (!(k in m) || t < m[k][0]) m[k] = [t, from[k]]; }); INIT.set(el, m);
  return tl.fromTo(el, from, Object.assign({ immediateRender: false }, to), t);
};
const IN = (t, el, d = 0.5, extra = {}) => ft(t, el, Object.assign({ opacity: 0, y: 40, filter: "blur(14px)" }, extra.from || {}),
  Object.assign({ opacity: 1, y: 0, x: 0, scale: 1, filter: "blur(0px)", duration: d, ease: "expo.out" }, extra.to || {}));
const OUT = (t, el, d = 0.3, extra = {}) => tl.to(el, Object.assign({ opacity: 0, y: -40, filter: "blur(12px)", duration: d, ease: "power2.in" }, extra), t);
const flash = (t, a = 0.85, d = 0.28) => ft(t, "#flash", { opacity: a }, { opacity: 0, duration: d, ease: "power2.out" });
const punch = (t, el, s = 1.06) => ft(t, el, { scale: s }, { scale: 1, duration: 0.45, ease: "expo.out" });

// ---------- global: grain jitter, slow pushes on footage ----------
tl.fromTo("#grain", { x: 0, y: 0 }, { x: 180, y: -140, duration: C.TOTAL, ease: "steps(" + Math.round(C.TOTAL * 12) + ")", immediateRender: false }, 0);
ft(0, "#v_hook1", { scale: 1.28 }, { scale: 1.08, duration: 2.66, ease: "power2.out" });
ft(2.66, "#v_hook2", { scale: 1.25 }, { scale: 1.05, duration: 2.84, ease: "power1.out" });
ft(C.FB_OUT, "#v_fb", { scale: 1.12 }, { scale: 1.0, duration: C.FB_END - C.FB_OUT, ease: "none" });
ft(C.CL, "#i_cta", { scale: 1.0 }, { scale: 1.14, duration: C.S2 - C.CL, ease: "none" });
ft(C.S2, "#v_stock", { scale: 1.35, rotation: -2 }, { scale: 1.15, rotation: 0, duration: C.S3 - C.S2, ease: "none" });
ft(C.S3, "#v_voucher", { scale: 1.3 }, { scale: 1.1, duration: C.S4 - C.S3, ease: "none" });

// ---------- HOOK 0 – 2.66 ----------
flash(0, 1, 0.35);
ft(0, "#v_hook1", { filter: "blur(18px) brightness(1.6)" }, { filter: "blur(0px) brightness(1)", duration: 0.55, ease: "power3.out" });
IN(0.15, "#hk_eyebrow", 0.6, { from: { y: 0, letterSpacing: "1.2em" }, to: { letterSpacing: "0.42em" } });
$$("#hk1 .ch").forEach((c, i) => ft(0.02 + i * 0.035, c, { opacity: 0, scale: 2.4, filter: "blur(20px)", y: -30 }, { opacity: 1, scale: 1, filter: "blur(0px)", y: 0, duration: 0.42, ease: "expo.out" }));
IN(0.32, "#hk2", 0.7, { from: { y: 90, scale: 0.9 } });
ft(0.5, "#hk_line", { scaleX: 0, opacity: 0 }, { scaleX: 1, opacity: 1, duration: 0.8, ease: "expo.out" });
tl.to("#hk", { scale: 1.06, duration: 1.2, ease: "none" }, 0.35);
OUT(1.5, "#hk", 0.28, { y: -140 });
ft(1.5, "#v_hook1", { filter: "blur(0px) brightness(1)" }, { filter: "blur(10px) brightness(.55)", duration: 0.4, ease: "power2.out" });
ft(1.55, "#pc_word", { opacity: 0, letterSpacing: "1.1em" }, { opacity: 1, letterSpacing: "0.5em", duration: 0.9, ease: "expo.out" });
ft(1.58, "#pcard", { opacity: 0, y: 700, rotationX: 38, scale: 0.75 }, { opacity: 1, y: 0, rotationX: 0, scale: 1, duration: 0.75, ease: "expo.out" });
ft(2.05, "#pc_sheen", { x: "-120%" }, { x: "120%", duration: 0.7, ease: "power2.inOut" });
tl.to("#pcard", { scale: 1.04, duration: 0.9, ease: "none" }, 2.0);
tl.set("#pc_wrap", { opacity: 1 }, 0);
// whip into hook2
flash(2.62, 0.6, 0.2);
ft(2.66, "#s_hook2", { filter: "blur(16px)", scale: 1.15 }, { filter: "blur(0px)", scale: 1, duration: 0.35, ease: "expo.out" });
ft(2.72, "#tg1", { opacity: 0, clipPath: "inset(0 0 100% 0)", y: 60 }, { opacity: 1, clipPath: "inset(0 0 0% 0)", y: 0, duration: 0.5, ease: "expo.out" });
IN(2.95, "#tg2", 0.6, { from: { x: 120, y: 0 } });
ft(3.15, "#tg_line", { scaleX: 0 }, { scaleX: 1, duration: 0.7, ease: "expo.out" });
ft(3.92, "#rec", { opacity: 0, scale: 0.6, xPercent: -50, x: 0 }, { opacity: 1, scale: 1, xPercent: -50, duration: 0.45, ease: "back.out(2.2)" });
tl.to("#rec .dot", { opacity: 0.2, duration: 0.25, repeat: 5, yoyo: true, ease: "none" }, 4.0);
tl.to("#s_hook2 .center-stack", { scale: 1.08, duration: 2.6, ease: "none" }, 2.9);
// iris into feedback
ft(5.28, "#iris", { opacity: 0 }, { opacity: 1, duration: 0.2, ease: "power2.in" });
ft(5.5, "#iris", { opacity: 1 }, { opacity: 0, duration: 0.25, ease: "power2.out" });
ft(5.5, "#v_fb", { clipPath: "circle(0% at 50% 45%)" }, { clipPath: "circle(80% at 50% 45%)", duration: 0.55, ease: "expo.out" });

// ---------- FEEDBACK (long, customer stays on screen) ----------
IN(5.62, "#fb_tag", 0.5, { from: { x: -60, y: 0 } });
tl.to("#fb_tag .dot", { opacity: 0.2, duration: 0.3, repeat: 31, yoyo: true, ease: "none" }, 5.8);
ft(C.LEMBUT - 0.05, "#b_lembut", { opacity: 0, scale: 0.5, rotation: 8, filter: "blur(10px)" }, { opacity: 1, scale: 1, rotation: -3, filter: "blur(0px)", duration: 0.55, ease: "back.out(1.8)" });
tl.to("#b_lembut", { y: -20, duration: 1.0, ease: "sine.inOut" }, C.LEMBUT + 0.5);
OUT(C.LEMBUT + 1.9, "#b_lembut", 0.3, { scale: 0.85, y: -60 });
// pump/foam picture-in-picture while she explains "mula-mula ... lama-lama lembut"
const P0 = C.PIP0, P1 = C.PIP1;
ft(P0, ["#v_pip", "#pip_frame"], { opacity: 0, x: 420, rotation: 10, scale: 0.8 }, { opacity: 1, x: 0, rotation: 3, scale: 1, duration: 0.6, ease: "expo.out" });
ft(P0, "#v_pip", { filter: "blur(10px)" }, { filter: "blur(0px)", duration: 0.5 });
tl.to(["#v_pip", "#pip_frame"], { rotation: -1, y: -18, duration: P1 - P0 - 0.6, ease: "sine.inOut" }, P0 + 0.6);
IN(C.LEMBUT2 - 0.05, "#pip_res", 0.45, { from: { scale: 0.6, y: 20 } });
tl.to(["#v_pip", "#pip_frame"], { opacity: 0, x: 420, rotation: 12, duration: 0.4, ease: "expo.in" }, P1 - 0.4);
// wangi
ft(C.WANGI_Q - 0.1, "#glory", { opacity: 0, x: 380, rotation: 14 }, { opacity: 1, x: 0, rotation: 5, duration: 0.6, ease: "expo.out" });
["#sc1", "#sc2", "#sc3"].forEach((p, i) => {
  const L = 560; ft(C.WANGI - 0.1 + i * 0.08, p, { strokeDasharray: L, strokeDashoffset: L, opacity: 1 }, { strokeDashoffset: 0, duration: 0.9, ease: "power2.out" });
  tl.to(p, { opacity: 0, y: -60, duration: 0.5 }, C.WANGI + 0.9 + i * 0.08);
});
ft(C.WANGI - 0.05, "#b_wangi", { opacity: 0, scale: 0.5, rotation: -8 }, { opacity: 1, scale: 1, rotation: -4, duration: 0.5, ease: "back.out(2)" });
// stamp
ft(C.TIPU, "#stamp", { opacity: 0, scale: 2.6, rotation: -30 }, { opacity: 0.95, scale: 1, rotation: -12, duration: 0.22, ease: "power4.in" });
tl.to("#stamp", { rotation: -6, duration: 0.9, ease: "sine.out" }, C.TIPU + 0.25);
[[14, -10], [-12, 8], [8, -4], [-4, 2], [0, 0]].forEach(([x, y], i) => tl.to("#stage", { x, y, duration: 0.04, ease: "none" }, C.TIPU + 0.22 + i * 0.04));
flash(C.TIPU + 0.21, 0.35, 0.2);
tl.to(["#glory", "#b_wangi"], { opacity: 0, y: -40, filter: "blur(8px)", duration: 0.35, ease: "power2.in" }, C.TERIMA - 0.2);
OUT(C.TERIMA - 0.2, "#stamp", 0.35, { scale: 0.8 });
ft(C.TERIMA, "#thanks", { opacity: 0, scale: 0.6, y: 40 }, { opacity: 1, scale: 1, y: 0, duration: 0.6, ease: "back.out(2)" });
// whip into closing
flash(C.CL - 0.05, 0.9, 0.3);
ft(C.CL - 0.25, "#s_fb", { scale: 1, filter: "blur(0px)" }, { scale: 1.2, filter: "blur(16px)", duration: 0.25, ease: "power3.in" });
ft(C.CL - 0.25, "#v_fb", { scale: 1.0, filter: "blur(0px)" }, { scale: 1.2, filter: "blur(16px)", duration: 0.25, ease: "power3.in" });

// ---------- CTA 1 ----------
ft(C.CL, "#i_cta", { filter: "blur(20px) brightness(1.4)" }, { filter: "blur(0px) brightness(1)", duration: 0.5, ease: "power3.out" });
ft(C.CUBA - 1.0, "#nk1", { opacity: 0, scale: 1.8, filter: "blur(16px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.45, ease: "expo.out" });
IN(C.CUBA - 0.05, "#nk2", 0.55, { from: { y: 70 } });
punch(C.CUBA, "#nk1", 1.08);
ft(C.CHECK - 0.15, "#co_btn", { opacity: 0, scale: 0.5, xPercent: -50 }, { opacity: 1, scale: 1, xPercent: -50, duration: 0.5, ease: "back.out(2.2)" });
ft(C.CHECK + 0.1, "#co_ring", { opacity: 1, scale: 1 }, { opacity: 0, scale: 1.35, duration: 0.6, ease: "power2.out" });
tl.to("#co_btn span", { x: 16, duration: 0.18, repeat: 3, yoyo: true, ease: "sine.inOut" }, C.CHECK + 0.1);

// ---------- STOCK ----------
flash(C.S2 - 0.02, 0.5, 0.2);
ft(C.S2 + 0.02, "#st1", { opacity: 0, scale: 0.6, letterSpacing: "0.3em" }, { opacity: 1, scale: 1, letterSpacing: "0.02em", duration: 0.6, ease: "expo.out" });
ft(C.S2 + 0.25, "#stockbox", { opacity: 0, y: 80 }, { opacity: 1, y: 0, duration: 0.5, ease: "expo.out" });
ft(C.S2 + 0.3, "#s_fill", { scaleX: 1 }, { scaleX: 0.12, duration: 2.5, ease: "power2.inOut" });
ft(C.TERHAD - 0.05, "#st2", { opacity: 0, scale: 1.6, filter: "blur(12px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.3, ease: "expo.out" });
ft(C.S2 + 1.5, "#sb_hot", { opacity: 0 }, { opacity: 1, duration: 0.1 });
tl.to("#sb_hot", { opacity: 0.25, duration: 0.18, repeat: 7, yoyo: true, ease: "none" }, C.S2 + 1.7);
[[-14, 0.9], [10, 0.6], [-6, 0.8], [0, 0]].forEach(([x, o], i) => {
  tl.set("#glitchR", { opacity: o, x: x, y: 0 }, C.TERHAD + i * 0.05);
  tl.set("#glitchC", { opacity: o, x: -x, y: 0 }, C.TERHAD + i * 0.05);
});
[[12, -6], [-10, 6], [6, -2], [0, 0]].forEach(([x, y], i) => tl.to("#stage", { x, y, duration: 0.04, ease: "none" }, C.TERHAD + i * 0.04));

// ---------- VOUCHER ----------
ft(C.S3, "#s_voucher", { clipPath: "inset(0% 0% 100% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.4, ease: "expo.out" });
IN(C.S3 + 0.07, "#vc1", 0.5, { from: { y: 0, letterSpacing: "1em" }, to: { letterSpacing: "0.42em" } });
IN(C.BERAPA - 0.05, "#vc2", 0.5, { from: { y: 60, scale: 1.2 } });
ft(C.S3 + 0.12, "#ticket", { opacity: 0, y: 500, rotation: -16 }, { opacity: 1, y: 0, rotation: -4, duration: 0.7, ease: "expo.out" });
["#q1", "#q2", "#q3"].forEach((q, i) => {
  ft(C.BERAPA + i * 0.08, q, { y: -40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "back.out(3)" });
  tl.to(q, { y: -14, duration: 0.22, repeat: 3, yoyo: true, ease: "sine.inOut" }, C.BERAPA + 0.5 + i * 0.1);
});
ft(C.TIKTOK2, "#t_sheen", { x: "-120%" }, { x: "120%", duration: 0.7, ease: "power2.inOut" });
punch(C.TIKTOK2, "#ticket", 1.06);
tl.to("#ticket", { rotation: 2, duration: 1.4, ease: "sine.inOut" }, C.S3 + 0.87);

// ---------- BAG ----------
flash(C.S4 - 0.04, 0.5, 0.2);
ft(C.S4 + 0.02, "#tk1", { opacity: 0, scale: 1.8, filter: "blur(16px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.4, ease: "expo.out" });
ft(C.S4 + 0.06, "#bagwrap", { opacity: 0, scale: 0.3, y: 200, rotation: -12 }, { opacity: 1, scale: 1, y: 0, rotation: 0, duration: 0.55, ease: "back.out(1.8)" });
IN(C.BEG - 0.06, "#tk2", 0.45, { from: { y: 50, scale: 1.2 } });
ft(C.BEG - 0.25, "#finger", { opacity: 0, x: 120, y: 120, scale: 1.3 }, { opacity: 1, x: 0, y: 0, scale: 1, duration: 0.25, ease: "power2.out" });
ft(C.BEG, "#finger", { scale: 1 }, { scale: 0.8, duration: 0.08, yoyo: true, repeat: 1, ease: "power2.inOut" });
ft(C.BEG, "#bagwrap .bag", { scaleY: 1, scaleX: 1 }, { scaleY: 0.88, scaleX: 1.08, duration: 0.09, yoyo: true, repeat: 1, ease: "power2.inOut" });
ft(C.BEG, "#ripple1", { opacity: 1, scale: 0.3 }, { opacity: 0, scale: 2.4, duration: 0.7, ease: "power2.out" });
ft(C.BEG + 0.15, "#ripple2", { opacity: 1, scale: 0.3 }, { opacity: 0, scale: 2.8, duration: 0.8, ease: "power2.out" });
ft(C.BEG + 0.2, "#arrow", { opacity: 0, x: 60, y: -60 }, { opacity: 1, x: 0, y: 0, duration: 0.35, ease: "back.out(2)" });
tl.to("#arrow", { x: -18, y: 18, duration: 0.22, repeat: 3, yoyo: true, ease: "sine.inOut" }, C.BEG + 0.55);
ft(C.CHECK2 - 0.1, "#co2", { opacity: 0, scale: 0.5, xPercent: -50 }, { opacity: 1, scale: 1, xPercent: -50, duration: 0.45, ease: "back.out(2.2)" });
tl.to("#bagwrap", { y: -16, duration: 0.5, repeat: 1, yoyo: true, ease: "sine.inOut" }, C.BEG + 0.3);

// ---------- END CARD ----------
ft(C.END0, "#logo", { opacity: 0, scale: 0.82, filter: "blur(20px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.9, ease: "expo.out" });
ft(C.END0 + 0.2, "#logo_glow", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1.2, duration: 1.2, ease: "power2.out" });
tl.to("#logo_glow", { opacity: 0.55, duration: 0.6, repeat: 1, yoyo: true, ease: "sine.inOut" }, C.END0 + 1.4);
tl.to("#logo", { scale: 1.04, duration: 2.0, ease: "none" }, C.END0 + 0.9);
IN(C.END0 + 0.7, "#end_t1", 0.6, { from: { y: 0, letterSpacing: "1em" }, to: { letterSpacing: "0.42em" } });
IN(C.END0 + 0.95, "#end_t2", 0.6);
ft(C.END1 - 0.45, "#fadeout", { opacity: 0 }, { opacity: 1, duration: 0.45, ease: "power1.in" });

// ---------- CAPTIONS ----------
CAPS.forEach((g, i) => {
  const el = "#c" + i;
  ft(g.start, el, { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.18, ease: "power3.out" });
  tl.to(el, { opacity: 0, y: -16, duration: 0.12, ease: "power2.in" }, Math.max(g.start + 0.2, g.end - 0.12));
  g.words.forEach((w, j) => {
    const t = Math.max(g.start, w[1] - 0.03);
    const k = w[3];
    ft(t, "#c" + i + "w" + j, { opacity: 0, y: k ? 30 : 18, scale: k ? 1.35 : 1, filter: "blur(6px)" },
      { opacity: 1, y: 0, scale: 1, filter: "blur(0px)", duration: k ? 0.32 : 0.16, ease: k ? "back.out(2.4)" : "power3.out" });
  });
});

// pre-roll state: every element starts at its earliest "from" values (hidden until its cue)
INIT.forEach((m, el) => { const v = {}; Object.keys(m).forEach((k) => { if (m[k][0] > 0.001) v[k] = m[k][1]; }); if (Object.keys(v).length) tl.set(el, v, 0); });
tl.set(["#rec", "#co_btn", "#co2"], { xPercent: -50 }, 0);
window.__timelines = window.__timelines || {};
window.__timelines["main"] = tl;
tl.seek(0);
