// Shared helpers for Frescura sub-compositions.
// HF.shift lets a scene keep root-time positions while its own timeline stays local (t - T0).
window.HF = {
  shift(base, T0) {
    const w = {
      fromTo(a, b, c, t) {
        base.fromTo(a, b, c, t - T0);
        return w;
      },
      to(a, b, t) {
        base.to(a, b, t - T0);
        return w;
      },
      set(a, b, t) {
        base.set(a, b, t - T0);
        return w;
      },
    };
    return w;
  },
  rng(seed) {
    let s = seed >>> 0;
    return () => (s = (s * 1664525 + 1013904223) % 4294967296) / 4294967296;
  },
};
var $ = (s) => document.querySelector(s);
var $$ = (s) => Array.from(document.querySelectorAll(s));
var E = "expo.out",
  P = "power3.out",
  B = "back.out(1.7)";
