import os, sys
P = sys.argv[1]
os.makedirs(P + "/compositions", exist_ok=True)

def comp(cid, T0, body, css, js, seed):
    return f'''<!-- HyperFrames sub-composition "{cid}" — mounted at root {T0}s. data-start values and timeline positions are local. -->
<template id="{cid}-template">
  <div data-composition-id="{cid}" data-width="1080" data-height="1920">
    <div id="{cid}-root" class="fill">
{body}
    </div>
    <style>
{css}
    </style>
    <script>
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
        const at = HF.at({T0});
        const rnd = HF.rng({seed});
        const q = (s) => document.querySelector("#{cid}-root " + s);
        const qa = (s) => Array.from(document.querySelectorAll("#{cid}-root " + s));
{js}
        window.__timelines = window.__timelines || {{}};
        window.__timelines["{cid}"] = tl;
      }})();
    </script>
  </div>
</template>
'''
C = {}
SMOKE_JS = '''        const sm = HF.smoke(q(".smk"), 5, rnd, "rgba(200,190,170,.10)");
        sm.forEach((b, i) => tl.fromTo(b, { x: 0, y: 0 }, { x: (rnd() - 0.5) * 300, y: -120 - rnd() * 160, duration: DUR, ease: "none" }, 0));'''

# ---------------- HOOK 0–4.02
C["hook"] = (0, 3.3, '''      <img class="clip bg hero" data-start="0" data-duration="3.3" src="assets/img/noir_hero.jpg" alt="" />
      <div class="fill" style="background: linear-gradient(180deg, rgba(10,10,11,.92) 0%, rgba(10,10,11,.55) 45%, rgba(10,10,11,.2) 70%, rgba(10,10,11,.6) 100%)"></div>
      <div class="beam bm"></div>
      <div class="abs cx cin a1" style="top: 230px; font-size: 104px">KULIT LEMBUT</div>
      <div class="abs cx it a2 gold" style="top: 350px; font-size: 84px">macam lepas spa?</div>
      <div class="abs rule r1" style="left: 340px; width: 400px; top: 485px"></div>
      <div class="abs cx cin b1" style="top: 530px; font-size: 104px">BADAN WANGI</div>
      <div class="abs cx it b2 gold" style="top: 650px; font-size: 72px">macam baru pakai perfume?</div>''',
'',
'''        tl.fromTo(q(".hero"), { scale: 1.25 }, { scale: 1.05, duration: 3.3, ease: "power2.out" }, 0);
        tl.fromTo(q(".bm"), { rotate: -28, opacity: 0 }, { rotate: 6, opacity: 1, duration: 2.2, ease: "power2.out" }, 0);
        tl.to(q(".bm"), { rotate: 14, opacity: 0.6, duration: 1.1, ease: "sine.inOut" }, 2.2);
        tl.fromTo(HF.glyphs(q(".a1")), { yPercent: 110 }, { yPercent: 0, duration: 0.45, stagger: 0.022, ease: E }, at(0.1));
        tl.fromTo(q(".a2"), { autoAlpha: 0, y: 30, filter: "blur(10px)" }, { autoAlpha: 1, y: 0, filter: "blur(0px)", duration: 0.4, ease: E }, at(0.5));
        tl.fromTo(q(".r1"), { scaleX: 0 }, { scaleX: 1, duration: 0.5, ease: P }, at(1.2));
        tl.fromTo(HF.glyphs(q(".b1")), { yPercent: 110 }, { yPercent: 0, duration: 0.45, stagger: 0.022, ease: E }, at(1.45));
        tl.fromTo(q(".b2"), { autoAlpha: 0, y: 30, filter: "blur(10px)" }, { autoAlpha: 1, y: 0, filter: "blur(0px)", duration: 0.4, ease: E }, at(2.3));''')

# ---------------- MANDI 4.02–6.84
C["mandi"] = (3.3, 2.28, '''      <video id="v-mandi" class="clip bg" data-start="0" data-duration="2.28" data-media-start="0.4" muted playsinline src="assets/video/spa.mp4" style="filter: brightness(.5) saturate(.8)"></video>
      <div class="fill ripples"></div>
      <div class="abs cx lab l0" style="top: 420px; color: var(--gold2)">Semua tu boleh dapat</div>
      <div class="abs cx cin l1" style="top: 480px; font-size: 64px">HANYA DENGAN</div>
      <div class="abs cx cin l2 gold" style="top: 580px; font-size: 230px; font-weight: 600">MANDI</div>''',
'''      #mandi-root .rp { position: absolute; left: 540px; top: 700px; width: 120px; height: 120px; margin: -60px 0 0 -60px; border-radius: 50%; border: 2px solid rgba(240,217,164,.7); }''',
'''        tl.fromTo(q("#v-mandi"), { scale: 1.2 }, { scale: 1.05, duration: 2.28, ease: "power1.out" }, 0);
        tl.fromTo(q(".l0"), { autoAlpha: 0, y: 14 }, { autoAlpha: 1, y: 0, duration: 0.35 }, 0.05);
        tl.fromTo(q(".l1"), { autoAlpha: 0, scale: 1.2 }, { autoAlpha: 1, scale: 1, duration: 0.35, ease: E }, at(4.35));
        tl.fromTo(HF.glyphs(q(".l2")), { yPercent: 110 }, { yPercent: 0, duration: 0.5, stagger: 0.04, ease: E }, at(4.9));
        for (let i = 0; i < 4; i++) {
          const r = document.createElement("div"); r.className = "rp"; q(".ripples").appendChild(r);
          tl.fromTo(r, { scale: 0.3, opacity: 0.9 }, { scale: 9, opacity: 0, duration: 1.2, ease: "power2.out" }, at(4.95) + i * 0.15);
        }''')

# ---------------- SECRET 6.84–13.08
C["secret"] = (5.58, 8.96, '''      <div class="fill" style="background: radial-gradient(70% 45% at 50% 45%, #1e1d22 0%, #0a0a0b 70%)"></div>
      <div class="fill smk"></div>
      <div class="beam bm" style="left: 90px"></div>
      <div class="abs cx lab t0" style="top: 210px; color: var(--gold2)">Rahsianya ada pada</div>
      <div class="abs cx cin t1" style="top: 260px; font-size: 130px">GARAM <span class="it gold" style="font-size: .95em; letter-spacing: 0">laut</span></div>
      <svg class="abs key" style="left: 390px; top: 520px" width="300" height="420" viewBox="0 0 300 420" fill="none" stroke="#d8b56a" stroke-width="4"><circle cx="150" cy="140" r="110" /><path d="M110 210 L80 400 H220 L190 210" /></svg>
      <div class="abs scene3d" style="left: 390px; top: 600px; width: 300px; height: 300px; perspective: 1200px">
        <div class="cube" style="position: absolute; inset: 0; transform-style: preserve-3d">
          <i style="transform: translateZ(150px)"></i><i style="transform: rotateY(180deg) translateZ(150px)"></i><i style="transform: rotateY(90deg) translateZ(150px)"></i><i style="transform: rotateY(-90deg) translateZ(150px)"></i><i style="transform: rotateX(90deg) translateZ(150px)"></i><i style="transform: rotateX(-90deg) translateZ(150px)"></i>
        </div>
      </div>
      <div class="abs proc" style="left: 60px; right: 60px; top: 560px; display: flex; justify-content: space-between">
        <div class="pi p1"><svg viewBox="0 0 160 160" fill="none" stroke="#d8b56a" stroke-width="4" stroke-linecap="round"><circle cx="80" cy="80" r="74" stroke-opacity=".4" stroke-width="2" /><path d="M28 74 q13 -15 26 0 t26 0 t26 0 t26 0" /><path d="M28 98 q13 -15 26 0 t26 0 t26 0 t26 0" /></svg><b>AIR LAUT</b></div>
        <div class="pa a1">→</div>
        <div class="pi p2"><svg viewBox="0 0 160 160" fill="none" stroke="#d8b56a" stroke-width="4" stroke-linecap="round"><circle cx="80" cy="80" r="74" stroke-opacity=".4" stroke-width="2" /><circle cx="80" cy="80" r="22" /><path d="M80 36v-12M80 136v-12M36 80h-12M136 80h-12M49 49l-8 -8M119 119l-8 -8M49 111l-8 8M119 41l-8 8" /></svg><b>DISEJAT</b></div>
        <div class="pa a2">→</div>
        <div class="pi p3"><svg viewBox="0 0 160 160" fill="none" stroke="#d8b56a" stroke-width="4" stroke-linejoin="round"><circle cx="80" cy="80" r="74" stroke-opacity=".4" stroke-width="2" /><path d="M80 38 L116 58 L116 100 L80 120 L44 100 L44 58 Z" /><path d="M44 58 L80 78 L116 58 M80 78 L80 120" /></svg><b>SEMULA JADI</b></div>
      </div>
      <div class="abs cx lab kaya" style="top: 1000px; color: var(--gold2)">Kaya mineral</div>
      <svg class="abs lns" style="left: 0; top: 0" width="1080" height="1920" fill="none" stroke="#d8b56a" stroke-width="2" stroke-dasharray="6 8"><path class="ln1" d="M540 750 L230 820" /><path class="ln2" d="M540 750 L850 820" /></svg>
      <div class="abs el e1" style="left: 120px; top: 740px"><div class="sy">Mg</div><div class="nm">Magnesium</div></div>
      <div class="abs el e2" style="left: 740px; top: 740px"><div class="sy">Ca</div><div class="nm">Kalsium</div></div>''',
'''      #secret-root .cube i { position: absolute; inset: 0; border: 2px solid rgba(240,217,164,.9); background: linear-gradient(135deg, rgba(255,255,255,.22), rgba(255,255,255,.04)); box-shadow: inset 0 0 40px rgba(255,255,255,.15); }
      #secret-root .pi { width: 250px; text-align: center; }
      #secret-root .pi svg { width: 170px; height: 170px; }
      #secret-root .pi b { display: block; margin-top: 12px; font-family: var(--cin); font-weight: 400; font-size: 32px; letter-spacing: .08em; color: var(--ivory); }
      #secret-root .pa { font-family: var(--cin); font-size: 60px; color: var(--gold2); margin-top: 50px; }
      #secret-root .el { width: 220px; height: 220px; border-radius: 50%; border: 2px solid var(--gold); background: radial-gradient(circle at 35% 30%, rgba(240,217,164,.25), rgba(10,10,11,.8)); text-align: center; }
      #secret-root .el .sy { font-family: var(--it); font-style: italic; font-size: 96px; margin-top: 40px; color: var(--gold2); line-height: 1; }
      #secret-root .el .nm { font-size: 20px; font-weight: 700; letter-spacing: .2em; text-transform: uppercase; margin-top: 8px; }''',
'''        const DUR = 8.96;
''' + SMOKE_JS + '''
        tl.fromTo(q(".bm"), { rotate: 20, opacity: 0 }, { rotate: -6, opacity: 0.9, duration: 1.5, ease: "power2.out" }, 0);
        tl.fromTo(q(".t0"), { autoAlpha: 0, y: 14 }, { autoAlpha: 1, y: 0, duration: 0.35 }, 0.05);
        const kp = qa(".key circle, .key path");
        kp.forEach((p) => { const L = p.getTotalLength(); tl.fromTo(p, { attr: { "stroke-dasharray": L, "stroke-dashoffset": L } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.7, ease: "power2.inOut" }, 0.15); });
        tl.fromTo(q(".t1"), { autoAlpha: 0, scale: 1.25, filter: "blur(14px)" }, { autoAlpha: 1, scale: 1, filter: "blur(0px)", duration: 0.5, ease: E }, at(6.7));
        tl.to(q(".key"), { scale: 3, opacity: 0, duration: 0.5, ease: "power3.in", transformOrigin: "50% 33%" }, at(7.15));
        [[".p1", 8.6], [".a1", 9.1], [".p2", 9.4], [".a2", 10.2], [".p3", 10.45]].forEach(([c, t]) => tl.fromTo(q(c), { autoAlpha: 0, y: 40, scale: 0.85 }, { autoAlpha: 1, y: 0, scale: 1, duration: 0.4, ease: B }, at(t)));
        tl.fromTo(q(".p2 svg"), { rotate: -40 }, { rotate: 0, duration: 0.8, ease: E }, at(9.4));
        tl.to(q(".proc"), { autoAlpha: 0, y: -40, duration: 0.3, ease: "power2.in" }, at(11.0));
        tl.set(qa(".pi, .pa"), { autoAlpha: 0 }, 0);
        tl.fromTo(q(".scene3d"), { autoAlpha: 0, scale: 0.4 }, { autoAlpha: 1, scale: 1, duration: 0.6, ease: B }, at(11.2));
        tl.fromTo(q(".cube"), { rotationX: -20, rotationY: 0 }, { rotationX: -28, rotationY: 300, duration: 3.35, ease: "none" }, at(11.2));
        tl.fromTo(q(".kaya"), { autoAlpha: 0, y: 14 }, { autoAlpha: 1, y: 0, duration: 0.35 }, at(11.72));
        tl.fromTo(q(".ln1"), { opacity: 0 }, { opacity: 1, duration: 0.2 }, at(12.55));
        tl.fromTo(q(".e1"), { autoAlpha: 0, scale: 0.3 }, { autoAlpha: 1, scale: 1, duration: 0.45, ease: "back.out(2.2)" }, at(12.64));
        tl.fromTo(q(".ln2"), { opacity: 0 }, { opacity: 1, duration: 0.2 }, at(13.75));
        tl.fromTo(q(".e2"), { autoAlpha: 0, scale: 0.3 }, { autoAlpha: 1, scale: 1, duration: 0.45, ease: "back.out(2.2)" }, at(13.84));
        tl.set([q(".scene3d"), q(".kaya"), q(".e1"), q(".e2"), q(".t1")], { autoAlpha: 0 }, 0);''')

# ---------------- MOIST 13.08–16.5
C["moist"] = (14.54, 2.58, '''      <div class="fill" style="background: radial-gradient(70% 45% at 50% 45%, #14202a 0%, #0a0a0b 70%)"></div>
      <div class="abs cx lab t0" style="top: 210px; color: var(--gold2)">Mineral bantu kulit</div>
      <div class="abs cx cin t1" style="top: 260px; font-size: 110px">KEKAL LEMBAP</div>
      <svg class="abs drop" style="left: 290px; top: 470px" width="500" height="560" viewBox="0 0 500 560" fill="none">
        <defs><linearGradient id="dg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#bfe3e6" /><stop offset="1" stop-color="#3f8b96" /></linearGradient></defs>
        <circle class="lock" cx="250" cy="300" r="225" stroke="#d8b56a" stroke-width="5" />
        <path class="dp" d="M250 110 C250 110 140 240 140 320 C140 382 190 430 250 430 C310 430 360 382 360 320 C360 240 250 110 250 110 Z" fill="url(#dg)" stroke="#f0d9a4" stroke-width="4" />
        <g class="pad" transform="translate(250 75)"><rect x="-28" y="-6" width="56" height="44" rx="8" fill="#d8b56a" /><path d="M-16 -6 V-20 a16 16 0 0 1 32 0 V-6" stroke="#d8b56a" stroke-width="7" /></g>
      </svg>
      <svg class="abs silk" style="left: 0; top: 1040px" width="1080" height="160" viewBox="0 0 1080 160" fill="none" stroke-linecap="round"><path class="s1" d="M-300 80 C-150 20 0 140 150 80 S450 20 600 80 S900 140 1050 80 S1350 20 1500 80" stroke="#f0d9a4" stroke-width="5" /><path class="s2" d="M-300 100 C-150 40 0 160 150 100 S450 40 600 100 S900 160 1050 100 S1350 40 1500 100" stroke="rgba(240,217,164,.4)" stroke-width="3" /></svg>
      <div class="abs cx it lb gold" style="top: 1170px; font-size: 96px">&amp; lembut</div>''',
'',
'''        tl.fromTo(q(".t0"), { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.3 }, 0.05);
        tl.fromTo(HF.glyphs(q(".t1")), { yPercent: 110 }, { yPercent: 0, duration: 0.45, stagger: 0.022, ease: E }, at(15.9));
        tl.fromTo(q(".dp"), { scale: 0, transformOrigin: "250px 430px" }, { scale: 1, duration: 0.6, ease: B }, 0.1);
        tl.to(q(".dp"), { y: -12, duration: 0.6, yoyo: true, repeat: 2, ease: "sine.inOut" }, 0.7);
        const lk = q(".lock"); const L = lk.getTotalLength();
        tl.fromTo(lk, { attr: { "stroke-dasharray": L, "stroke-dashoffset": L } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.6, ease: "power2.inOut" }, at(16.0));
        tl.fromTo(q(".pad"), { scale: 0, transformOrigin: "0 0" }, { scale: 1, duration: 0.35, ease: "back.out(2.5)" }, at(16.35));
        tl.fromTo(qa(".silk path"), { x: 0, opacity: 0 }, { x: -300, opacity: 1, duration: 0.9, ease: "power1.out" }, at(16.4));
        tl.fromTo(q(".lb"), { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: 0.35, ease: E }, at(16.6));
        tl.set(q(".t1"), { autoAlpha: 1 }, 0);''')

# ---------------- FORMULA 16.5–23.72
C["formula"] = (20.24, 5.98, '''      <img class="clip bg hero" data-start="0" data-duration="5.98" src="assets/img/noir_hero.jpg" alt="" />
      <div class="fill dark" style="background: rgba(10,10,11,.7)"></div>
      <div class="fill topg" style="background: linear-gradient(180deg, rgba(10,10,11,.9), rgba(10,10,11,0) 35%)"></div>
      <div class="beam bm" style="left: 300px"></div>
      <div class="abs cx cin br" style="top: 200px; font-size: 118px; letter-spacing: .14em">FRESCURA</div>
      <div class="abs cx lab sb" style="top: 340px; color: var(--gold2)">Body · Foaming Body Shower</div>
      <div class="abs eq" style="left: 0; right: 0; top: 520px; text-align: center">
        <div class="ck c1"><span class="cin">GARAM LAUT</span></div>
        <div class="op o1">+</div>
        <div class="ck c2"><span class="cin">WANGIAN PERFUME MEWAH</span></div>
        <div class="op o2">=</div>
        <div class="ck c3 res"><span class="cin">1 FOAMING BODY SHOWER</span></div>
      </div>''',
'''      #formula-root .ck { display: inline-block; padding: 26px 46px; border-radius: 16px; border: 2px solid var(--gold); background: rgba(10,10,11,.55); font-size: 46px; }
      #formula-root .res { background: var(--gold2); color: #0a0a0b; border-color: var(--gold2); }
      #formula-root .op { font-family: var(--cin); font-size: 90px; color: var(--gold2); line-height: 1.3; }''',
'''        tl.fromTo(q(".hero"), { scale: 1.18 }, { scale: 1.02, duration: 5.98, ease: "power1.out" }, 0);
        tl.fromTo(q(".hero"), { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: 0.8, ease: "power3.inOut" }, 0);
        tl.fromTo(q(".dark"), { opacity: 0 }, { opacity: 0, duration: 0.01 }, 0);
        tl.to(q(".dark"), { opacity: 1, duration: 0.4 }, at(21.9));
        tl.fromTo(q(".bm"), { rotate: -30, opacity: 0 }, { rotate: 22, opacity: 0.9, duration: 1.6, ease: "power2.inOut" }, 0.2);
        tl.to(q(".bm"), { opacity: 0.35, duration: 1 }, 1.8);
        tl.fromTo(HF.glyphs(q(".br")), { yPercent: 110 }, { yPercent: 0, duration: 0.5, stagger: 0.04, ease: E }, 0.1);
        tl.fromTo(q(".sb"), { autoAlpha: 0, y: 14 }, { autoAlpha: 1, y: 0, duration: 0.4 }, at(20.8));
        [[".c1", 22.2], [".o1", 22.85], [".c2", 23.2], [".o2", 24.7], [".c3", 25.05]].forEach(([c, t]) => tl.fromTo(q(c), { autoAlpha: 0, y: 40, scale: 0.85 }, { autoAlpha: 1, y: 0, scale: 1, duration: 0.4, ease: B }, at(t)));
        tl.to(q(".c3"), { scale: 1.06, duration: 0.25, yoyo: true, repeat: 2, ease: "sine.inOut" }, at(25.45));''')

# ---------------- PUMP 23.72–26.2
C["pump"] = (26.22, 1.98, '''      <video id="v-pump" class="clip bg" data-start="0" data-duration="0.9" data-media-start="0.5" muted playsinline src="assets/video/pump.mp4" style="filter: brightness(.75) contrast(1.05)"></video>
      <video id="v-palm" class="clip bg" data-start="0.9" data-duration="1.08" data-media-start="0.2" muted playsinline src="assets/video/palm.mp4" style="filter: brightness(.75) contrast(1.05)"></video>
      <div class="fill" style="background: linear-gradient(180deg, rgba(10,10,11,.75), rgba(10,10,11,0) 45%)"></div>
      <div class="abs cx cin x1 gold" style="top: 170px; font-size: 220px; font-weight: 600">1×</div>
      <div class="abs cx lab x2" style="top: 420px">Sekali pump</div>
      <div class="abs cx cin y1" style="top: 230px; font-size: 104px">BERBUIH</div>
      <div class="abs cx it y2 gold" style="top: 350px; font-size: 96px">lembut</div>
      <div class="bubs"></div>''',
'',
'''        tl.fromTo(q("#v-pump"), { scale: 1.2 }, { scale: 1.08, duration: 0.9, ease: "power1.out" }, 0);
        tl.fromTo(q("#v-palm"), { scale: 1.08 }, { scale: 1.2, duration: 1.08, ease: "power1.out" }, 0.9);
        tl.fromTo(q(".x1"), { autoAlpha: 0, scale: 2 }, { autoAlpha: 1, scale: 1, duration: 0.3, ease: "power4.out" }, 0.02);
        tl.fromTo(q(".x2"), { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.25 }, 0.2);
        tl.to([q(".x1"), q(".x2")], { autoAlpha: 0, y: -40, duration: 0.2 }, 0.85);
        tl.fromTo(HF.glyphs(q(".y1")), { yPercent: 110 }, { yPercent: 0, duration: 0.4, stagger: 0.03, ease: E }, at(27.4));
        tl.fromTo(q(".y2"), { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: 0.3, ease: E }, at(27.85));
        const bb = HF.bubbles(q(".bubs"), 18, { x: 60, y: 1100, w: 960, h: 600 }, rnd);
        bb.forEach((b, i) => tl.fromTo(b, { autoAlpha: 0, y: 150, scale: 0.3 }, { autoAlpha: 0.95, y: -520 - rnd() * 300, x: (rnd() - 0.5) * 120, scale: 1, duration: 1.2, ease: "power1.out" }, 0.85 + (i % 9) * 0.05));''')

def variant(cid, T0, d, img, glow, accent, num, sub, name, kw, kwt, starry):
    body = f'''      <div class="fill" style="background: radial-gradient(60% 40% at 50% 38%, {glow} 0%, #0a0a0b 70%)"></div>
      <div class="fill stars"></div>
      <div class="beam bm" style="left: 90px; opacity: .8"></div>
      <svg class="abs waves" style="left: 140px; top: 260px" width="800" height="700" viewBox="0 0 800 700" fill="none" stroke="{accent}" stroke-width="3" stroke-linecap="round" opacity=".7">
        <path d="M120 600 C80 500 160 420 110 320 S120 160 90 60" /><path d="M680 600 C720 500 640 420 690 320 S680 160 710 60" /><path d="M60 650 C20 520 110 430 50 300 S70 120 40 20" /><path d="M740 650 C780 520 690 430 750 300 S730 120 760 20" />
      </svg>
      <div class="abs prod" style="left: 330px; top: 230px; width: 420px; height: 960px; overflow: visible"><img src="assets/img/{img}" alt="" style="width: 420px; height: 960px; object-fit: cover; border-radius: 14px; -webkit-box-reflect: below 6px linear-gradient(transparent 70%, rgba(255,255,255,.22));" /></div>
      <div class="abs cx lab n" style="top: 1260px; color: {accent}">N° {num} · {sub}</div>
      <div class="abs cx cin nm" style="top: 1310px; font-size: 100px">{name}</div>
      <div class="abs cx it k1" style="top: 1440px; font-size: 104px; color: {accent}">{kw}</div>'''
    stars_js = '''        for (let i = 0; i < 40; i++) { const s = document.createElement("div"); const z = 2 + rnd() * 5; Object.assign(s.style, { position: "absolute", left: rnd() * 1080 + "px", top: rnd() * 1250 + "px", width: z + "px", height: z + "px", borderRadius: "50%", background: "#fff", boxShadow: "0 0 10px #fff" }); q(".stars").appendChild(s); tl.fromTo(s, { opacity: 0.1 }, { opacity: 1, duration: 0.5 + rnd(), yoyo: true, repeat: 3, ease: "sine.inOut" }, rnd()); }''' if starry else ''
    js = f'''        tl.fromTo(q(".prod"), {{ autoAlpha: 0, y: 80, scale: 0.9 }}, {{ autoAlpha: 1, y: 0, scale: 1, duration: 0.7, ease: E }}, 0);
        tl.to(q(".prod"), {{ y: -16, duration: {d - 0.7}, ease: "sine.inOut" }}, 0.7);
        tl.fromTo(q(".bm"), {{ rotate: -24, opacity: 0 }}, {{ rotate: 4, opacity: 0.85, duration: 1.4, ease: "power2.out" }}, 0);
        qa(".waves path").forEach((p, i) => {{ const L = p.getTotalLength(); tl.fromTo(p, {{ attr: {{ "stroke-dasharray": L, "stroke-dashoffset": L }} }}, {{ attr: {{ "stroke-dashoffset": 0 }}, duration: 1.2, ease: "power2.out" }}, 0.3 + i * 0.12); tl.to(p, {{ y: -40, opacity: 0.2, duration: 1.4 }}, 1.6 + i * 0.1); }});
        tl.fromTo(q(".n"), {{ autoAlpha: 0 }}, {{ autoAlpha: 1, duration: 0.3 }}, 0.35);
        tl.fromTo(HF.glyphs(q(".nm")), {{ yPercent: 110 }}, {{ yPercent: 0, duration: 0.45, stagger: 0.03, ease: E }}, 0.4);
        tl.fromTo(q(".k1"), {{ autoAlpha: 0, y: 30, filter: "blur(8px)" }}, {{ autoAlpha: 1, y: 0, filter: "blur(0px)", duration: 0.45, ease: E }}, at({kwt}));
{stars_js}'''
    return (T0, d, body, "", js)

C["glory"] = variant("glory", 28.2, 2.94, "glory_n.jpg", "#4a0d16", "#ff9fae", "I", "Bombshell", "WOMAN GLORY", "manis &amp; menggoda", 29.9, False)
C["noche"] = variant("noche", 31.14, 2.78, "noche_n.jpg", "#1d1650", "#c4b5ff", "II", "Midnight Fantasy", "NOCHE", "lembut &amp; misteri", 32.5, True)

# ---------------- LISTEN 33.12–36.76
C["listen"] = (33.92, 2.9, '''      <div class="fill" style="background: #0a0a0b"></div>
      <div class="fill rings"></div>
      <div class="abs cx lab t0" style="top: 360px; color: var(--gold2)">Tapi</div>
      <div class="abs cx cin t1" style="top: 410px; font-size: 128px">DENGAR SINI</div>
      <div class="abs cx lab s0" style="top: 760px; color: var(--gold2)">Stok batch ni</div>
      <div class="abs bars" style="left: 190px; top: 820px; width: 700px; height: 240px; display: flex; align-items: flex-end; justify-content: space-between"></div>
      <div class="abs cx cin s1" style="top: 1100px; font-size: 92px; color: #ff5a6a">TERHAD</div>''',
'''      #listen-root .rg { position: absolute; left: 540px; top: 480px; width: 160px; height: 160px; margin: -80px 0 0 -80px; border-radius: 50%; border: 2px solid rgba(240,217,164,.6); }
      #listen-root .bar { width: 50px; border-radius: 8px; background: var(--gold2); transform-origin: 50% 100%; }''',
'''        tl.fromTo(q(".t0"), { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.2 }, 0.0);
        tl.fromTo(q(".t1"), { autoAlpha: 0, scale: 1.4, filter: "blur(14px)" }, { autoAlpha: 1, scale: 1, filter: "blur(0px)", duration: 0.4, ease: "power4.out" }, at(34.15));
        for (let i = 0; i < 5; i++) { const r = document.createElement("div"); r.className = "rg"; q(".rings").appendChild(r); tl.fromTo(r, { scale: 0.5, opacity: 0.9 }, { scale: 9, opacity: 0, duration: 1.3, ease: "power2.out" }, at(34.2) + i * 0.16); }
        tl.fromTo(q(".s0"), { autoAlpha: 0, y: 14 }, { autoAlpha: 1, y: 0, duration: 0.3 }, at(34.85));
        const bars = [];
        for (let i = 0; i < 10; i++) { const b = document.createElement("div"); b.className = "bar"; b.style.height = 120 + Math.sin(i * 0.9) * 50 + 60 + "px"; q(".bars").appendChild(b); bars.push(b); }
        tl.fromTo(bars, { scaleY: 0 }, { scaleY: 1, duration: 0.3, stagger: 0.03, ease: B }, at(35.0));
        bars.slice(2).reverse().forEach((b, i) => tl.to(b, { scaleY: 0.05, opacity: 0.25, duration: 0.12 }, at(35.6) + i * 0.1));
        tl.to(bars.slice(0, 2), { background: "#ff5a6a", duration: 0.2 }, at(36.4));
        tl.fromTo(q(".s1"), { autoAlpha: 0, scale: 1.6 }, { autoAlpha: 1, scale: 1, duration: 0.3, ease: "power4.in" }, at(36.5));''')

# ---------------- SOLD OUT 36.76–39.86
C["soldout"] = (45.94, 2.46, '''      <img class="clip bg bgi" data-start="0" data-duration="2.46" src="assets/img/noir_smoke.jpg" alt="" style="filter: blur(14px) brightness(.4)" />
      <div class="abs cx cin t1" style="top: 330px; font-size: 96px">JANGAN TUNGGU</div>
      <div class="abs cx lab t2" style="top: 460px; color: var(--gold2)">Sampai tulisan ni keluar</div>
      <div class="abs sign" style="left: 150px; top: 600px; width: 780px; height: 260px; border: 6px solid #ff3b4f; border-radius: 24px; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 40px rgba(255,59,79,.6), inset 0 0 30px rgba(255,59,79,.4)">
        <div class="tx" style="font-family: var(--sans); font-weight: 800; font-size: 104px; letter-spacing: .08em; white-space: nowrap; color: #ff5a6a; text-shadow: 0 0 24px rgba(255,59,79,.9)">SOLD OUT</div>
      </div>''',
'',
'''        tl.fromTo(q(".bgi"), { scale: 1.2 }, { scale: 1.08, duration: 2.46, ease: "none" }, 0);
        tl.fromTo(HF.glyphs(q(".t1")), { yPercent: 110 }, { yPercent: 0, duration: 0.45, stagger: 0.025, ease: E }, 0.02);
        tl.fromTo(q(".t2"), { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.3 }, at(46.5));
        tl.fromTo(q(".sign"), { autoAlpha: 0, scale: 0.8 }, { autoAlpha: 1, scale: 1, duration: 0.25, ease: B }, at(46.95));
        const letters = HF.glyphs(q(".tx"));
        tl.fromTo(letters, { opacity: 0 }, { opacity: 1, duration: 0.02, stagger: 0.06 }, at(47.35));
        [47.95, 48.03, 48.11, 48.19].forEach((t, i) => tl.to(q(".sign"), { opacity: i % 2 ? 1 : 0.35, duration: 0.03 }, at(t)));''')

# ---------------- CTA 39.86–45
C["cta"] = (48.4, 4.6, '''      <img class="clip bg bgi" data-start="0" data-duration="4.6" src="assets/img/noir_hero.jpg" alt="" style="filter: brightness(.45)" />
      <div class="beam bm" style="left: 100px"></div>
      <div class="abs cx cin t1" style="top: 210px; font-size: 92px">KLIK LINK</div>
      <div class="abs cx it t2 gold" style="top: 320px; font-size: 90px">di bawah</div>
      <svg class="abs arw" style="left: 510px; top: 460px" width="60" height="110" viewBox="0 0 60 110" fill="none" stroke="#f0d9a4" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"><path d="M30 6 V100 M8 76 L30 100 L52 76" /></svg>
      <div class="abs cx co" style="top: 620px"><span class="chip" style="border: 2px solid var(--gold2); color: var(--gold2); font-family: var(--cin); font-weight: 600; letter-spacing: .1em">CHECK OUT SEKARANG</span></div>
      <div class="abs btn" style="left: 110px; right: 110px; top: 780px; height: 170px; border-radius: 85px; background: #ffc21a; color: #0a0a0b; display: flex; align-items: center; justify-content: center; gap: 24px; font-weight: 800; font-size: 54px; box-shadow: 0 0 60px rgba(255,194,26,.35), 0 30px 80px rgba(0,0,0,.5)">
        <svg width="80" height="90" viewBox="0 0 280 330"><path d="M85 110 V80 a55 55 0 0 1 110 0 V110" fill="none" stroke="#0a0a0b" stroke-width="24" stroke-linecap="round" /><rect x="20" y="100" width="240" height="220" rx="40" fill="#0a0a0b" /></svg>TEKAN BEG KUNING
      </div>
      <div class="abs rp" style="left: 540px; top: 865px; width: 40px; height: 40px; margin: -20px 0 0 -20px; border-radius: 50%; border: 4px solid #ffc21a"></div>
      <div class="abs cx it ru gold" style="top: 1010px; font-size: 80px">sebelum anda rugi</div>''',
'',
'''        tl.fromTo(q(".bgi"), { scale: 1.2 }, { scale: 1.03, duration: 4.6, ease: "power1.out" }, 0);
        tl.fromTo(q(".bm"), { rotate: -25, opacity: 0 }, { rotate: 10, opacity: 0.8, duration: 2, ease: "power2.out" }, 0);
        tl.fromTo(HF.glyphs(q(".t1")), { yPercent: 110 }, { yPercent: 0, duration: 0.45, stagger: 0.03, ease: E }, 0.02);
        tl.fromTo(q(".t2"), { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: 0.35, ease: E }, at(48.75));
        tl.fromTo(q(".arw"), { autoAlpha: 0, y: -20 }, { autoAlpha: 1, y: 0, duration: 0.3 }, at(48.85));
        tl.to(q(".arw"), { y: 22, duration: 0.25, yoyo: true, repeat: 13, ease: "sine.inOut" }, at(49.1));
        tl.fromTo(q(".co"), { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: 0.35, ease: B }, at(49.28));
        tl.fromTo(q(".btn"), { autoAlpha: 0, scale: 0.5 }, { autoAlpha: 1, scale: 1, duration: 0.5, ease: "elastic.out(1,0.6)" }, at(50.1));
        tl.to(q(".btn"), { scale: 1.06, duration: 0.24, yoyo: true, repeat: 9, ease: "sine.inOut" }, at(50.6));
        tl.set(q(".rp"), { autoAlpha: 0 }, 0);
        [50.6, 51.4, 52.2].forEach((t) => tl.fromTo(q(".rp"), { autoAlpha: 0.9, scale: 1 }, { autoAlpha: 0, scale: 24, duration: 0.6, ease: "power2.out", immediateRender: false }, at(t)));
        tl.fromTo(q(".ru"), { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: 0.35, ease: E }, at(51.3));''')


# ---------------- SPA 17.12–20.24 (restored line)
C["spa"] = (17.12, 3.12, '''      <video id="v-spa" class="clip bg" data-start="0" data-duration="3.12" data-media-start="0" muted playsinline src="assets/video/lather.mp4" style="filter: blur(10px) brightness(.35) saturate(.7)"></video>
      <div class="fill" style="background: radial-gradient(50% 30% at 50% 52%, rgba(240,217,164,.18), rgba(10,10,11,0) 70%)"></div>
      <div class="abs cx lab t0" style="top: 260px; color: var(--gold2)">Sebab itu</div>
      <div class="abs cx it t1 gold" style="top: 310px; font-size: 96px">garam laut jadi pilihan</div>
      <svg class="abs lotus" style="left: 290px; top: 520px" width="500" height="420" viewBox="0 0 500 420" fill="none" stroke="#f0d9a4" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
        <path d="M250 330 C200 260 200 170 250 90 C300 170 300 260 250 330 Z" />
        <path d="M250 330 C170 300 120 230 120 150 C190 170 240 230 250 330 Z" />
        <path d="M250 330 C330 300 380 230 380 150 C310 170 260 230 250 330 Z" />
        <path d="M250 330 C150 330 70 290 40 230 C120 220 200 260 250 330 Z" />
        <path d="M250 330 C350 330 430 290 460 230 C380 220 300 260 250 330 Z" />
        <path d="M80 370 H420" />
        <g class="steam" stroke-width="3" opacity=".8"><path d="M190 70 c-14 -22 14 -36 0 -58" /><path d="M250 50 c-14 -22 14 -36 0 -58" /><path d="M310 70 c-14 -22 14 -36 0 -58" /></g>
      </svg>
      <div class="abs cx lab t2" style="top: 990px; color: var(--gold2)">Dalam</div>
      <div class="abs cx cin t3" style="top: 1040px; font-size: 118px">RAWATAN SPA</div>''',
'',
'''        tl.fromTo(q("#v-spa"), { scale: 1.15 }, { scale: 1.3, duration: 3.12, ease: "none" }, 0);
        tl.fromTo(q(".t0"), { autoAlpha: 0, y: 14 }, { autoAlpha: 1, y: 0, duration: 0.3 }, 0.02);
        tl.fromTo(q(".t1"), { autoAlpha: 0, y: 30, filter: "blur(8px)" }, { autoAlpha: 1, y: 0, filter: "blur(0px)", duration: 0.4, ease: E }, at(17.65));
        qa(".lotus > path").forEach((p, i) => { const L = p.getTotalLength(); tl.fromTo(p, { attr: { "stroke-dasharray": L, "stroke-dashoffset": L } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.8, ease: "power2.inOut" }, 0.2 + i * 0.1); });
        tl.fromTo(qa(".steam path"), { opacity: 0, y: 20 }, { opacity: 0.9, y: -20, duration: 1.0, stagger: 0.15, ease: "power1.out" }, at(18.5));
        tl.fromTo(q(".t2"), { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.25 }, at(18.95));
        tl.fromTo(HF.glyphs(q(".t3")), { yPercent: 110 }, { yPercent: 0, duration: 0.45, stagger: 0.03, ease: E }, at(19.3));''')

# ---------------- RESTOCK 36.82–38.98 (restored line)
C["restock"] = (36.82, 2.16, '''      <div class="fill" style="background: radial-gradient(70% 45% at 50% 45%, #1c1416 0%, #0a0a0b 70%)"></div>
      <div class="abs cx cin t1" style="top: 230px; font-size: 104px">BILA DAH HABIS</div>
      <svg class="abs btl" style="left: 140px; top: 470px" width="260" height="560" viewBox="0 0 250 560" fill="none">
        <clipPath id="bclip"><path d="M95 20 h70 v40 h-20 v40 h40 a20 20 0 0 1 20 20 v400 a20 20 0 0 1 -20 20 h-120 a20 20 0 0 1 -20 -20 v-400 a20 20 0 0 1 20 -20 h40 v-40 h-30z" /></clipPath>
        <g clip-path="url(#bclip)"><rect class="liq" x="0" y="120" width="250" height="440" fill="#c0283c" /></g>
        <path d="M95 20 h70 v40 h-20 v40 h40 a20 20 0 0 1 20 20 v400 a20 20 0 0 1 -20 20 h-120 a20 20 0 0 1 -20 -20 v-400 a20 20 0 0 1 20 -20 h40 v-40 h-30z" stroke="#f0d9a4" stroke-width="4" />
      </svg>
      <div class="abs cal" style="left: 500px; top: 520px; width: 440px; height: 440px; border: 3px solid #f0d9a4; border-radius: 28px; overflow: hidden; text-align: center">
        <div style="height: 90px; background: #f0d9a4; color: #0a0a0b; font-weight: 800; font-size: 30px; letter-spacing: .3em; line-height: 90px">RESTOCK</div>
        <div class="days" style="position: relative; height: 350px"></div>
      </div>
      <div class="abs cx it t2 gold" style="top: 1080px; font-size: 90px">kena tunggu lama…</div>''',
'''      #restock-root .days span { position: absolute; left: 0; right: 0; top: 60px; font-family: var(--cin); font-size: 190px; color: var(--ivory); opacity: 0; }''',
'''        tl.fromTo(HF.glyphs(q(".t1")), { yPercent: 110 }, { yPercent: 0, duration: 0.4, stagger: 0.02, ease: E }, 0.02);
        tl.fromTo(q(".btl"), { autoAlpha: 0, x: -60 }, { autoAlpha: 1, x: 0, duration: 0.4, ease: E }, 0.1);
        tl.fromTo(q(".liq"), { attr: { y: 120 } }, { attr: { y: 560 }, duration: 0.6, ease: "power2.in" }, at(37.0));
        tl.fromTo(q(".cal"), { autoAlpha: 0, scale: 0.8 }, { autoAlpha: 1, scale: 1, duration: 0.35, ease: B }, at(37.5));
        const days = q(".days"); const N = 14;
        for (let i = 0; i < N; i++) { const s = document.createElement("span"); s.textContent = String(1 + i * 2); days.appendChild(s); const t = at(37.75) + i * 0.08; tl.set(s, { opacity: 1 }, t); if (i < N - 1) tl.set(s, { opacity: 0 }, t + 0.08); }
        tl.fromTo(q(".t2"), { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: 0.35, ease: E }, at(37.6));''')

# ---------------- COMPARE 38.98–45.94 (restored lines)
C["compare"] = (38.98, 6.96, '''      <img class="clip bg bgi" data-start="0" data-duration="6.96" src="assets/img/noir_curve.jpg" alt="" style="filter: blur(16px) brightness(.3)" />
      <div class="abs cx lab t0" style="top: 230px; color: var(--gold2)">Bayangkan</div>
      <div class="abs cx cin t1" style="top: 285px; font-size: 60px; white-space: nowrap">KETAHANAN WANGIAN</div>
      <div class="abs rows" style="left: 90px; right: 90px; top: 470px">
        <div class="row r1"><div class="lb"><b>ORANG LAIN</b><span>wangi setiap hari</span></div><div class="track"><i class="fill1"></i></div></div>
        <div class="row r2" style="margin-top: 70px"><div class="lb"><b>KAMU · SABUN BIASA</b><span>bau hilang cepat</span></div><div class="track"><i class="fill2"></i></div></div>
        <div class="axis" style="display: flex; justify-content: space-between; margin-top: 30px; font-weight: 700; font-size: 22px; letter-spacing: .25em; color: rgba(244,239,230,.6)"><span>MANDI</span><span>PINTU RUMAH</span><span>MALAM</span></div>
      </div>
      <svg class="abs door" style="left: 470px; top: 830px" width="140" height="180" viewBox="0 0 140 180" fill="none" stroke="#f0d9a4" stroke-width="5" stroke-linejoin="round"><rect x="20" y="10" width="100" height="160" rx="6" /><circle cx="96" cy="95" r="6" fill="#f0d9a4" /></svg>
      <div class="abs cx cin rugi" style="top: 1070px; font-size: 112px; white-space: nowrap; color: #ff5a6a">RUGI KAN?</div>''',
'''      #compare-root .lb { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 16px; }
      #compare-root .lb b { font-family: var(--cin); font-weight: 600; font-size: 38px; letter-spacing: .06em; }
      #compare-root .lb span { font-family: var(--it); font-style: italic; font-size: 40px; color: var(--gold2); }
      #compare-root .track { height: 38px; border-radius: 19px; background: rgba(255,255,255,.1); border: 1.5px solid rgba(255,255,255,.3); overflow: hidden; }
      #compare-root .track i { display: block; height: 100%; border-radius: 19px; transform-origin: 0 50%; }
      #compare-root .fill1 { background: linear-gradient(90deg, #b8913f, #f0d9a4); box-shadow: 0 0 24px rgba(240,217,164,.6); }
      #compare-root .fill2 { background: linear-gradient(90deg, #8a8a8a, #bdbdbd); }''',
'''        tl.fromTo(q(".bgi"), { scale: 1.15 }, { scale: 1.05, duration: 6.96, ease: "none" }, 0);
        tl.fromTo(q(".t0"), { autoAlpha: 0, y: 14 }, { autoAlpha: 1, y: 0, duration: 0.3 }, 0.02);
        tl.fromTo(HF.glyphs(q(".t1")), { yPercent: 110 }, { yPercent: 0, duration: 0.45, stagger: 0.02, ease: E }, 0.2);
        tl.fromTo(q(".r1"), { autoAlpha: 0, x: -60 }, { autoAlpha: 1, x: 0, duration: 0.4, ease: E }, at(39.5));
        tl.fromTo(q(".fill1"), { scaleX: 0 }, { scaleX: 1, duration: 1.2, ease: "power2.out" }, at(39.8));
        tl.fromTo(q(".axis"), { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.3 }, at(40.0));
        tl.fromTo(q(".r2"), { autoAlpha: 0, x: -60 }, { autoAlpha: 1, x: 0, duration: 0.4, ease: E }, at(41.0));
        tl.fromTo(q(".fill2"), { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: "power2.out" }, at(42.5));
        tl.to(q(".fill2"), { scaleX: 0.0, opacity: 0.4, duration: 1.0, ease: "power2.in" }, at(43.85));
        tl.fromTo(q(".door"), { autoAlpha: 0, scale: 0.5 }, { autoAlpha: 1, scale: 1, duration: 0.35, ease: B }, at(44.85));
        tl.fromTo(q(".rugi"), { autoAlpha: 0, scale: 1.8 }, { autoAlpha: 1, scale: 1, duration: 0.3, ease: "power4.in" }, at(45.35));''')

# ---------------- CAPTIONS
C["captions"] = (0, 53, '''      <div class="fill caps"></div>''',
'''      #captions-root .cap { position: absolute; left: 60px; right: 60px; top: 1330px; text-align: center; font-family: var(--sans); font-weight: 800; font-size: 86px; line-height: 1.1; letter-spacing: -0.03em; color: #fff; opacity: 0; text-shadow: 0 2px 4px rgba(0,0,0,.6), 0 4px 30px rgba(0,0,0,.7); }
      #captions-root .cap::before { content: ""; display: block; width: 110px; height: 2px; margin: 0 auto 22px; background: linear-gradient(90deg, rgba(216,181,106,0), #d8b56a, rgba(216,181,106,0)); }
      #captions-root .w { display: inline-block; margin: 0 0.13em; }
      #captions-root .w.e { color: #f0d9a4; font-family: var(--it); font-style: italic; font-weight: 400; font-size: 1.16em; letter-spacing: 0; line-height: 0.9; }''',
'''        const HIDE = [[28.2, 33.92]];
        window.CAPTIONS.forEach((chunk, i) => {
          const s = chunk[0][1];
          if (HIDE.some(([a, b]) => s >= a && s < b)) return;
          const d = document.createElement("div"); d.className = "cap";
          chunk.forEach(([w, ws, we, em]) => { const sp = document.createElement("span"); sp.className = "w" + (em ? " e" : ""); sp.textContent = w; sp.dataset.s = ws; d.appendChild(sp); });
          q(".caps").appendChild(d);
          const next = window.CAPTIONS[i + 1];
          let e = next ? Math.min(next[0][1], chunk[chunk.length - 1][2] + 0.6) : 52.8;
          HIDE.forEach(([a]) => { if (s < a && e > a) e = a; });
          tl.fromTo(d, { autoAlpha: 0, y: 24, scale: 0.97 }, { autoAlpha: 1, y: 0, scale: 1, duration: 0.16, ease: P }, s);
          tl.to(d, { autoAlpha: 0, duration: 0.07 }, Math.max(s + 0.2, e - 0.06));
          Array.from(d.children).forEach((w) => {
            const t = Math.max(s, +w.dataset.s - 0.03);
            tl.fromTo(w, { opacity: 0.35, y: 6 }, { opacity: 1, y: 0, duration: 0.12, ease: P }, t);
            tl.fromTo(w, { textShadow: "0 0 0 rgba(255,236,190,0)" }, { textShadow: "0 0 26px rgba(255,236,190,.85)", duration: 0.1, immediateRender: false }, t);
            tl.to(w, { textShadow: "0 2px 4px rgba(0,0,0,.6), 0 4px 30px rgba(0,0,0,.7)", duration: 0.2 }, t + 0.3);
          });
        });''')

# ---------------- HUD
C["hud"] = (0, 53, '''      <div class="abs cx cin logo" style="top: 76px; font-size: 30px; letter-spacing: .5em">FRESCURA</div>
      <div class="abs prog" style="left: 390px; width: 300px; top: 124px; height: 2px; background: rgba(240,217,164,.2)"><i class="pf" style="display:block; width:100%; height:100%; background: #d8b56a; transform-origin: 0 50%"></i></div>
      <div class="abs rn" style="left: 70px; top: 80px; font-family: var(--cin); font-size: 30px; color: var(--gold2)"></div>
      <div class="fill wipe" style="background: linear-gradient(100deg, rgba(255,240,210,0) 30%, rgba(255,240,210,.95) 50%, rgba(255,240,210,0) 70%); opacity: 0"></div>''',
'''      #hud-root .rn span { position: absolute; left: 0; top: 0; opacity: 0; white-space: nowrap; }''',
'''        tl.fromTo(q(".pf"), { scaleX: 0 }, { scaleX: 1, duration: 53, ease: "none" }, 0);
        const SC = [0, 3.3, 5.58, 14.54, 17.12, 20.24, 26.22, 28.2, 31.14, 33.92, 36.82, 38.98, 45.94, 48.4, 53];
        const RN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV"];
        RN.forEach((r, i) => {
          const sp = document.createElement("span"); sp.textContent = r; q(".rn").appendChild(sp);
          tl.fromTo(sp, { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.3, immediateRender: false }, SC[i] + 0.05);
          if (i < RN.length - 1) tl.to(sp, { opacity: 0, duration: 0.1 }, SC[i + 1] - 0.1);
        });
        const wipe = q(".wipe");
        tl.set(wipe, { xPercent: -120, opacity: 0 }, 0);
        [3.3, 20.24, 28.2, 33.92, 48.4].forEach((t) => {
          tl.set(wipe, { opacity: 1, xPercent: -120 }, t - 0.3);
          tl.to(wipe, { xPercent: 120, duration: 0.55, ease: "power2.inOut" }, t - 0.3);
          tl.set(wipe, { opacity: 0 }, t + 0.26);
        });''')

seeds = {k: 211 + i * 19 for i, k in enumerate(C)}
for cid, (T0, d, body, css, js) in C.items():
    open(f"{P}/compositions/{cid}.html", "w").write(comp(cid, T0, body, css, js, seeds[cid]))
print("wrote", len(C))
