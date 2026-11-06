import os, sys
P = sys.argv[1]
os.makedirs(P + "/compositions", exist_ok=True)

def comp(cid, T0, body, css, js, seed):
    return f'''<!-- HyperFrames sub-composition "{cid}" — mounted at root {T0}s. All data-start values and timeline positions here are local. -->
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

# ---------------------------------------------------------------- HOOK 0–5.04
C["hook"] = (0, '''      <div class="fill ocean"></div>
      <div class="ring r1" style="left: 130px; top: 470px; width: 820px; height: 820px; color: rgba(156,195,201,.35)"></div>
      <div class="ring r2" style="left: 80px; top: 420px; width: 920px; height: 920px; color: rgba(156,195,201,.18)"></div>
      <div class="port pt" style="left: 180px; top: 520px; width: 720px; height: 720px"><img src="assets/img/duo_far.jpg" alt="" /></div>
      <div class="abs cx lab l0" style="top: 200px; color: var(--aqua)">Ramai tahu</div>
      <div class="abs cx disp t1" style="top: 250px; font-size: 150px">Garam laut</div>
      <div class="abs cx idx three" style="top: 330px; font-size: 900px; color: var(--copper2)">3</div>
      <div class="abs cx it keb" style="top: 1100px; font-size: 120px; color: #fff">kebaikan</div>
      <div class="abs cx lab jar" style="top: 1250px; color: var(--aqua)">yang jarang orang sebut</div>
      <div class="abs dots" style="left: 0; right: 0; top: 230px; display: flex; justify-content: center; gap: 26px"><i></i><i></i><i></i></div>''',
'''      #hook-root .dots i { width: 22px; height: 22px; border-radius: 50%; background: var(--copper2); display: block; }''',
'''        tl.fromTo(q(".pt"), { scale: 0, rotate: -30 }, { scale: 1, rotate: 0, duration: 0.9, ease: E }, 0);
        tl.fromTo(q(".pt img"), { scale: 1.5 }, { scale: 1.1, duration: 2.6, ease: "power2.out" }, 0);
        tl.fromTo(qa(".ring"), { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 1.0, stagger: 0.12, ease: E }, 0.1);
        tl.to(qa(".ring"), { rotate: 25, duration: 2.5, ease: "none" }, 0.3);
        tl.fromTo(q(".l0"), { autoAlpha: 0, y: 16 }, { autoAlpha: 1, y: 0, duration: 0.35 }, 0.02);
        tl.fromTo(HF.glyphs(q(".t1")), { yPercent: 110 }, { yPercent: 0, duration: 0.55, stagger: 0.03, ease: E }, at(0.42));
        tl.to(q(".l0") , { autoAlpha: 0, duration: 0.2 }, at(2.2));
        tl.to(q(".t1"), { autoAlpha: 0, y: -40, duration: 0.25 }, at(2.2));
        tl.to(q(".pt"), { scale: 0, rotate: 40, duration: 0.45, ease: "power3.in" }, at(2.22));
        tl.to(qa(".ring"), { opacity: 0, duration: 0.3 }, at(2.22));
        tl.fromTo(q(".three"), { autoAlpha: 0, scale: 0.4, filter: "blur(20px)" }, { autoAlpha: 1, scale: 1, filter: "blur(0px)", duration: 0.6, ease: E }, at(2.72));
        tl.fromTo(qa(".dots i"), { scale: 0 }, { scale: 1, duration: 0.3, stagger: 0.1, ease: "back.out(3)" }, at(2.8));
        tl.fromTo(q(".keb"), { autoAlpha: 0, y: 40 }, { autoAlpha: 1, y: 0, duration: 0.45, ease: E }, at(3.18));
        tl.fromTo(q(".jar"), { autoAlpha: 0, y: 20 }, { autoAlpha: 1, y: 0, duration: 0.4, ease: E }, at(3.9));
        tl.to(q(".three"), { scale: 1.06, duration: 2, ease: "none" }, at(3.3));
        tl.set([q(".three"), q(".keb"), q(".jar")], { autoAlpha: 0 }, 0);''')

def index_scene(cid, T0, num, label, title, it, graphic_html, graphic_css, graphic_js):
    body = f'''      <div class="fill paper"></div>
      <div class="grid"></div>
      <div class="abs idx num" style="left: 70px; top: 200px; font-size: 400px; color: var(--copper)">{num}</div>
      <div class="abs lab lb" style="left: 560px; top: 260px; color: var(--copper)">{label}</div>
      <div class="abs hr" style="left: 560px; top: 310px; width: 420px; height: 2px; background: var(--char)"></div>
      <div class="abs disp tt" style="left: 70px; top: 630px; font-size: 128px; color: var(--char)">{title}</div>
      <div class="abs it ti" style="left: 74px; top: 760px; font-size: 104px; color: var(--copper)">{it}</div>
{graphic_html}'''
    js = f'''        tl.fromTo(q(".num"), {{ autoAlpha: 0, x: -120 }}, {{ autoAlpha: 1, x: 0, duration: 0.6, ease: E }}, 0);
        tl.fromTo(q(".lb"), {{ autoAlpha: 0 }}, {{ autoAlpha: 1, duration: 0.3 }}, 0.15);
        tl.fromTo(q(".hr"), {{ scaleX: 0, transformOrigin: "0 50%" }}, {{ scaleX: 1, duration: 0.6, ease: P }}, 0.15);
        tl.fromTo(q(".grid"), {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6 }}, 0);
        tl.fromTo(HF.glyphs(q(".tt")), {{ yPercent: 110 }}, {{ yPercent: 0, duration: 0.5, stagger: 0.025, ease: E }}, 0.35);
{graphic_js}'''
    return (T0, body, graphic_css, js)

# ---------------------------------------------------------------- 01 oil 5.04–9.2
C["one"] = index_scene("one", 5.04, "01", "Kebaikan pertama", "Kawal minyak", "berlebihan",
'''      <div class="abs skin" style="left: 90px; top: 1090px; width: 900px; height: 130px; border-radius: 30px; background: linear-gradient(180deg, #ecc9ad, #d9a98a)"></div>
      <div class="drops"></div>
      <div class="salt"></div>
      <div class="abs meter" style="left: 90px; top: 960px; width: 900px; color: var(--char)">
        <div style="display: flex; justify-content: space-between; font-weight: 800; font-size: 26px; letter-spacing: .2em"><span>MINYAK</span><span class="pc" style="color: var(--copper)">BERLEBIHAN</span></div>
        <div style="margin-top: 14px; height: 16px; border-radius: 8px; background: rgba(18,18,18,.1); overflow: hidden"><div class="bar" style="height: 100%; background: linear-gradient(90deg, #d8a94a, #c08457); transform-origin: 0 50%"></div></div>
      </div>''',
'''      #one-root .drop { position: absolute; border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%; background: radial-gradient(circle at 35% 30%, #fff6d6 0 12%, #e4b84c 40%, #b8862a 100%); box-shadow: 0 6px 14px rgba(120, 80, 20, 0.35); }
      #one-root .cube { position: absolute; width: 26px; height: 26px; background: #fff; border: 2px solid #c9c2b5; transform: rotate(45deg); }''',
'''        tl.fromTo(q(".ti"), { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: 0.45, ease: E }, at(7.76));
        tl.fromTo(q(".skin"), { scaleX: 0, transformOrigin: "0 50%" }, { scaleX: 1, duration: 0.6, ease: E }, 0.4);
        tl.fromTo(q(".meter"), { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.3 }, 0.6);
        tl.fromTo(q(".bar"), { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: P }, 0.6);
        const drops = [];
        for (let i = 0; i < 8; i++) {
          const d = document.createElement("div"); d.className = "drop"; const r = 46 + rnd() * 30;
          Object.assign(d.style, { width: r + "px", height: r * 1.1 + "px", left: 120 + i * 108 + rnd() * 20 + "px", top: 1090 - r * 0.9 + "px" });
          q(".drops").appendChild(d); drops.push(d);
        }
        tl.fromTo(drops, { scale: 0, transformOrigin: "50% 100%" }, { scale: 1, duration: 0.35, stagger: 0.06, ease: "back.out(2.5)" }, 0.8);
        const cubes = [];
        for (let i = 0; i < 14; i++) {
          const c = document.createElement("div"); c.className = "cube";
          Object.assign(c.style, { left: 110 + rnd() * 860 + "px", top: 840 + rnd() * 60 + "px" });
          q(".salt").appendChild(c); cubes.push(c);
        }
        tl.fromTo(cubes, { autoAlpha: 0, y: -80 }, { autoAlpha: 1, y: 180, duration: 0.5, stagger: 0.03, ease: "power2.in" }, at(7.0));
        tl.to(cubes, { autoAlpha: 0, duration: 0.2, stagger: 0.03 }, at(7.5));
        tl.to(drops, { scale: 0.25, opacity: 0.35, duration: 0.6, stagger: 0.05, ease: "power2.inOut" }, at(7.45));
        tl.to(q(".bar"), { scaleX: 0.28, duration: 0.8, ease: "power3.inOut" }, at(7.5));
        tl.to(q(".skin"), { filter: "brightness(1.08) saturate(0.9)", duration: 0.6 }, at(7.9));''')

# ---------------------------------------------------------------- 02 calm 9.2–12.88
C["two"] = index_scene("two", 9.2, "02", "Kebaikan kedua", "Tenangkan", "kulit gatal &amp; merah",
'''      <div class="abs patch" style="left: 290px; top: 900px; width: 500px; height: 330px; border-radius: 40px; background: #efd2bd; overflow: hidden">
        <div class="red" style="position: absolute; left: 90px; top: 40px; width: 320px; height: 250px; border-radius: 50%; background: radial-gradient(circle, rgba(214,60,60,.75), rgba(214,60,60,0) 70%)"></div>
        <div class="calm" style="position: absolute; inset: 0; background: radial-gradient(circle at 50% 50%, rgba(156,195,201,.55), rgba(156,195,201,0) 70%)"></div>
      </div>
      <svg class="abs lines" style="left: 290px; top: 900px" width="500" height="330" viewBox="0 0 500 330" fill="none" stroke-linecap="round" stroke-linejoin="round">
        <path class="zig" d="M30 165 L70 105 L110 225 L150 105 L190 225 L230 105 L270 225 L310 105 L350 225 L390 105 L430 225 L470 165" stroke="#b3263a" stroke-width="7" />
        <path class="sine" d="M30 165 C90 115 130 115 170 165 S250 215 290 165 S370 115 410 165 S450 200 470 165" stroke="#3c7c86" stroke-width="7" />
      </svg>
      <div class="abs tagA" style="left: 290px; top: 1240px; font-weight: 800; font-size: 28px; letter-spacing: .16em; color: #b3263a">✕ GATAL · MERAH</div>
      <div class="abs tagB" style="left: 560px; top: 1240px; font-weight: 800; font-size: 28px; letter-spacing: .16em; color: #3c7c86">✓ TENANG</div>''',
'',
'''        tl.fromTo(q(".ti"), { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: 0.45, ease: E }, at(11.6));
        tl.fromTo(q(".patch"), { autoAlpha: 0, scale: 0.8 }, { autoAlpha: 1, scale: 1, duration: 0.5, ease: E }, 0.4);
        tl.fromTo(q(".red"), { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1.1, duration: 0.6, ease: P }, at(11.0));
        tl.fromTo(q(".calm"), { opacity: 0 }, { opacity: 1, duration: 0.6 }, at(12.25));
        tl.to(q(".red"), { opacity: 0, scale: 0.5, duration: 0.6, ease: "power2.inOut" }, at(12.25));
        const zig = q(".zig"), sine = q(".sine"); const Lz = zig.getTotalLength(), Ls = sine.getTotalLength();
        tl.fromTo(zig, { attr: { "stroke-dasharray": Lz, "stroke-dashoffset": Lz } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.5, ease: "power2.out" }, at(11.74));
        tl.fromTo(q(".tagA"), { autoAlpha: 0, y: 14 }, { autoAlpha: 1, y: 0, duration: 0.3 }, at(11.8));
        tl.to(zig, { opacity: 0, duration: 0.25 }, at(12.25));
        tl.fromTo(sine, { attr: { "stroke-dasharray": Ls, "stroke-dashoffset": Ls } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.5, ease: "power2.out" }, at(12.3));
        tl.to(q(".tagA"), { autoAlpha: 0.25, duration: 0.2 }, at(12.3));
        tl.fromTo(q(".tagB"), { autoAlpha: 0, y: 14 }, { autoAlpha: 1, y: 0, duration: 0.3 }, at(12.35));''')

# ---------------------------------------------------------------- 03 foot soak 12.88–18.46
C["three"] = index_scene("three", 12.88, "03", "Kebaikan ketiga", "Rendam kaki", "air suam + garam laut",
'''      <svg class="abs bowl" style="left: 190px; top: 900px" width="700" height="360" viewBox="0 0 700 360" fill="none">
        <g class="steam" stroke="#9cc3c9" stroke-width="5" stroke-linecap="round"><path d="M240 120 c-20 -30 20 -50 0 -80" /><path d="M350 110 c-20 -30 20 -50 0 -80" /><path d="M460 120 c-20 -30 20 -50 0 -80" /></g>
        <path d="M60 170 H640 C630 280 540 340 350 340 C160 340 70 280 60 170 Z" fill="#ffffff" stroke="#121212" stroke-width="4" />
        <clipPath id="bowlclip"><path d="M64 172 H636 C626 278 538 336 350 336 C162 336 74 278 64 172 Z" /></clipPath>
        <g clip-path="url(#bowlclip)"><path class="water" d="M-200 190 q50 -18 100 0 t100 0 t100 0 t100 0 t100 0 t100 0 t100 0 t100 0 t100 0 t100 0 t100 0 V360 H-200 Z" fill="#9cc3c9" /></g>
        <ellipse cx="350" cy="170" rx="290" ry="26" fill="none" stroke="#121212" stroke-width="4" />
        <g class="grains" fill="#ffffff" stroke="#b9b0a2" stroke-width="2"></g>
      </svg>
      <div class="abs cmp" style="left: 90px; top: 960px; width: 900px; color: var(--char); display: flex; justify-content: space-between; align-items: center">
        <div style="text-align: center"><svg width="360" height="120" viewBox="0 0 360 120"><path class="rough" d="M10 70 L30 52 L45 80 L62 48 L80 84 L96 50 L118 82 L136 46 L152 86 L172 52 L190 80 L210 46 L228 84 L248 50 L266 82 L286 48 L304 80 L324 54 L350 70" fill="none" stroke="#8a5a3a" stroke-width="7" stroke-linejoin="round" /></svg><div style="font-weight: 800; font-size: 28px; letter-spacing: .16em">TUMIT KERAS</div></div>
        <div class="arw" style="font-size: 70px; color: var(--copper)">→</div>
        <div style="text-align: center"><svg width="360" height="120" viewBox="0 0 360 120"><path class="smooth" d="M10 70 C90 50 270 50 350 70" fill="none" stroke="#3c7c86" stroke-width="7" stroke-linecap="round" /></svg><div style="font-weight: 800; font-size: 28px; letter-spacing: .16em; color: #3c7c86">LEMBUT</div></div>
      </div>''',
'',
'''        tl.fromTo(q(".ti"), { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: 0.45, ease: E }, at(14.8));
        tl.fromTo(q(".bowl"), { autoAlpha: 0, y: 80 }, { autoAlpha: 1, y: 0, duration: 0.55, ease: E }, at(13.5));
        tl.fromTo(q(".water"), { x: 0 }, { x: -200, duration: 3.4, ease: "none" }, at(13.5));
        tl.fromTo(qa(".steam path"), { opacity: 0, y: 30 }, { opacity: 1, y: -20, duration: 0.9, stagger: 0.12, ease: "power1.out" }, at(14.8));
        tl.to(qa(".steam path"), { opacity: 0, y: -60, duration: 0.6, stagger: 0.1 }, at(15.8));
        const g = q(".grains");
        for (let i = 0; i < 16; i++) {
          const r = document.createElementNS("http://www.w3.org/2000/svg", "rect"); const x = 140 + rnd() * 420;
          r.setAttribute("x", x); r.setAttribute("y", -20); r.setAttribute("width", 16); r.setAttribute("height", 16); r.setAttribute("transform", `rotate(45 ${x + 8} -12)`); g.appendChild(r);
          tl.fromTo(r, { y: -40, opacity: 0 }, { y: 220 + rnd() * 30, opacity: 1, duration: 0.5, ease: "power2.in" }, at(15.4) + i * 0.03);
          tl.to(r, { opacity: 0, duration: 0.2 }, at(15.95) + i * 0.03);
        }
        tl.to(q(".bowl"), { autoAlpha: 0, y: -60, duration: 0.35, ease: "power2.in" }, at(16.2));
        tl.fromTo(q(".cmp"), { autoAlpha: 0, y: 60 }, { autoAlpha: 1, y: 0, duration: 0.45, ease: E }, at(16.4));
        const rough = q(".rough"), smooth = q(".smooth"); const Lr = rough.getTotalLength(), Lm = smooth.getTotalLength();
        tl.fromTo(rough, { attr: { "stroke-dasharray": Lr, "stroke-dashoffset": Lr } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.5 }, at(16.5));
        tl.fromTo(q(".arw"), { x: -40, opacity: 0 }, { x: 0, opacity: 1, duration: 0.35 }, at(16.9));
        tl.fromTo(smooth, { attr: { "stroke-dasharray": Lm, "stroke-dashoffset": Lm } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.5 }, at(17.1));''')

# ---------------------------------------------------------------- ritual 18.46–21.88
C["ritual"] = (18.46, '''      <video id="v-ritual" class="clip bg" data-start="0" data-duration="3.42" data-media-start="0" muted playsinline src="assets/video/spa.mp4"></video>
      <div class="fill" style="background: linear-gradient(180deg, rgba(14,39,53,.75), rgba(14,39,53,.15) 55%, rgba(14,39,53,0))"></div>
      <div class="abs pills" style="left: 90px; top: 260px; display: flex; flex-direction: column; gap: 18px">
        <div class="chip pl" style="background: rgba(243,240,234,.92); color: var(--char)"><b style="font-family: var(--disp); font-weight: 400; color: var(--copper)">01</b>Kawal minyak</div>
        <div class="chip pl" style="background: rgba(243,240,234,.92); color: var(--char)"><b style="font-family: var(--disp); font-weight: 400; color: var(--copper)">02</b>Tenangkan kulit</div>
        <div class="chip pl" style="background: rgba(243,240,234,.92); color: var(--char)"><b style="font-family: var(--disp); font-weight: 400; color: var(--copper)">03</b>Lembutkan tumit</div>
      </div>
      <div class="abs cx lab sh" style="top: 300px; color: var(--aqua2)">Rutin paling ringkas</div>
      <div class="abs cx it sh2" style="top: 340px; font-size: 96px">setiap hari…</div>
      <div class="abs cx disp md" style="top: 470px; font-size: 230px">MANDI</div>''',
'',
'''        tl.fromTo(q("#v-ritual"), { scale: 1.25 }, { scale: 1.05, duration: 3.42, ease: "power1.out" }, 0);
        tl.fromTo(qa(".pl"), { autoAlpha: 0, x: -80 }, { autoAlpha: 1, x: 0, duration: 0.4, stagger: 0.12, ease: E }, 0.05);
        tl.to(qa(".pl"), { autoAlpha: 0, x: 60, duration: 0.3, stagger: 0.06, ease: "power2.in" }, at(19.3));
        tl.fromTo(q(".sh"), { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.3 }, at(19.5));
        tl.fromTo(q(".sh2"), { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: 0.45, ease: E }, at(20.1));
        tl.fromTo(HF.glyphs(q(".md")), { yPercent: 110 }, { yPercent: 0, duration: 0.5, stagger: 0.05, ease: E }, at(21.2));
        tl.set([q(".sh"), q(".sh2")], { autoAlpha: 0 }, 0);''')

# ---------------------------------------------------------------- product 21.88–27.82
C["product"] = (21.88, '''      <div class="fill ocean"></div>
      <div class="abs iris" style="inset: 0; clip-path: circle(0% at 50% 50%)"><img class="bg" src="assets/img/duo_marble.jpg" alt="" /></div>
      <div class="abs topg" style="left: 0; right: 0; top: 0; height: 620px; background: linear-gradient(180deg, rgba(14,39,53,.8), rgba(14,39,53,0))"></div>
      <div class="abs cx lab pre" style="top: 240px; color: var(--aqua2)">Jadikan waktu mandi lebih bermakna</div>
      <div class="abs cx disp brand" style="top: 270px; font-size: 168px; letter-spacing: .12em">FRESCURA</div>
      <div class="abs cx lab sub" style="top: 450px; color: #fff">Body · Gentle Foaming Body Shower</div>
      <div class="abs tick" style="left: 0; top: 1150px; width: 1080px; height: 86px; background: var(--paper); overflow: hidden; transform: rotate(-4deg)"><div class="tk" style="white-space: nowrap; font-family: var(--disp); font-size: 52px; line-height: 86px; color: var(--char)">OCEAN SALT ✦ AROMATHERAPY ✦ GENTLE FOAMING ✦ OCEAN SALT ✦ AROMATHERAPY ✦ GENTLE FOAMING ✦ OCEAN SALT ✦ AROMATHERAPY ✦</div></div>
      <video id="v-pump" class="clip bg" data-start="3.66" data-duration="2.28" data-media-start="0.3" muted playsinline src="assets/video/pump.mp4"></video>
      <div class="abs chips" style="left: 70px; top: 300px; display: flex; flex-direction: column; gap: 20px; align-items: flex-start">
        <div class="chip c1" style="background: var(--paper); color: var(--char)"><i style="width:22px;height:22px;border-radius:50%;background:var(--aqua);display:block"></i>Tekstur ringan</div>
        <div class="chip c2" style="background: var(--paper); color: var(--char)"><i style="width:22px;height:22px;border-radius:50%;background:var(--aqua);display:block"></i>Senang dibilas</div>
      </div>''',
'',
'''        tl.fromTo(q(".pre"), { autoAlpha: 0, y: 16 }, { autoAlpha: 1, y: 0, duration: 0.4 }, 0.05);
        tl.to(q(".pre"), { autoAlpha: 0, duration: 0.2 }, at(24.3));
        tl.fromTo(q(".iris"), { clipPath: "circle(0% at 50% 55%)" }, { clipPath: "circle(36% at 50% 55%)", duration: 0.6, ease: E }, at(22.3));
        tl.to(q(".iris"), { clipPath: "circle(80% at 50% 55%)", duration: 0.8, ease: "power3.inOut" }, at(24.2));
        tl.fromTo(q(".iris img"), { scale: 1.3 }, { scale: 1.04, duration: 3.6, ease: "power1.out" }, at(22.3));
        tl.fromTo(HF.glyphs(q(".brand")), { yPercent: 110 }, { yPercent: 0, duration: 0.55, stagger: 0.04, ease: E }, at(24.5));
        tl.fromTo(q(".sub"), { autoAlpha: 0, y: 14 }, { autoAlpha: 1, y: 0, duration: 0.4 }, at(24.95));
        tl.fromTo(q(".tick"), { autoAlpha: 0, y: 40 }, { autoAlpha: 1, y: 0, duration: 0.4, ease: E }, at(24.9));
        tl.fromTo(q(".tk"), { x: 0 }, { x: -700, duration: 3.0, ease: "none" }, at(23.0));
        tl.fromTo(q("#v-pump"), { scale: 1.2 }, { scale: 1.05, duration: 2.28, ease: "power1.out" }, 3.66);
        tl.fromTo(q(".c1"), { autoAlpha: 0, x: -100 }, { autoAlpha: 1, x: 0, duration: 0.4, ease: E }, at(26.2));
        tl.fromTo(q(".c2"), { autoAlpha: 0, x: -100 }, { autoAlpha: 1, x: 0, duration: 0.4, ease: E }, at(26.9));
        tl.set([q(".sub"), q(".tick")], { autoAlpha: 0 }, 0);
        tl.set([q(".brand"), q(".sub"), q(".tick"), q(".topg")], { autoAlpha: 0 }, 3.66);''')

# ---------------------------------------------------------------- clean 27.82–30.0
C["clean"] = (27.82, '''      <video id="v-lather" class="clip bg" data-start="0" data-duration="2.18" data-media-start="0" muted playsinline src="assets/video/lather.mp4"></video>
      <div class="fill" style="background: linear-gradient(180deg, rgba(14,39,53,.7), rgba(14,39,53,0) 45%)"></div>
      <div class="abs cx disp a" style="top: 250px; font-size: 120px">Tak melekat</div>
      <div class="abs cx b" style="top: 420px"><span class="chip" style="background: var(--paper); color: var(--char); position: relative">rasa licin<i class="st" style="position:absolute;left:20px;right:20px;top:50%;height:5px;background:#b3263a;transform-origin:0 50%"></i></span></div>''',
'',
'''        tl.fromTo(q("#v-lather"), { scale: 1.15 }, { scale: 1.02, duration: 2.18, ease: "power1.out" }, 0);
        tl.fromTo(HF.glyphs(q(".a")), { yPercent: 110 }, { yPercent: 0, duration: 0.45, stagger: 0.03, ease: E }, 0.1);
        tl.fromTo(q(".b"), { autoAlpha: 0, y: 20 }, { autoAlpha: 1, y: 0, duration: 0.35 }, at(28.8));
        tl.fromTo(q(".st"), { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power3.inOut" }, at(29.45));''')

def variant(cid, T0, d, img, top_panel, color_bg, accent, num, name, sub, kws, kw_times):
    if top_panel:  # text panel on top, photo bottom
        body = f'''      <div class="abs panel" style="left: 0; right: 0; top: 0; height: 960px; background: {color_bg}"></div>
      <div class="abs photo" style="left: 0; right: 0; top: 960px; height: 960px; overflow: hidden"><img class="bg" src="assets/img/duo_wood.jpg" alt="" style="height: 960px; filter: blur(14px) brightness(.55)" /><div class="port pp" style="left: 250px; top: 90px; width: 580px; height: 580px; border: 3px solid rgba(255,255,255,.7)"><img src="assets/img/{img}" alt="" style="object-position: 50% 55%" /></div></div>
      <div class="abs cx lab n" style="top: 210px; color: {accent}">Varian {num}</div>
      <div class="abs cx disp nm" style="top: 270px; font-size: 150px">{name}</div>
      <div class="abs cx lab sb" style="top: 440px; color: {accent}">{sub}</div>
      <div class="abs cx lab w0" style="top: 560px; color: #fff; letter-spacing: .3em">wangian malam yang</div>
      <div class="abs cx it k1" style="top: 610px; font-size: 120px; color: {accent}">{kws[0]}</div>
      <div class="abs cx it k2" style="top: 740px; font-size: 120px">{kws[1]}</div>'''
    else:
        body = f'''      <div class="abs photo" style="left: 0; right: 0; top: 0; height: 1000px; overflow: hidden"><img class="bg" src="assets/img/duo_wood.jpg" alt="" style="height: 1000px; filter: blur(14px) brightness(.55)" /><div class="port pp" style="left: 220px; top: 250px; width: 640px; height: 640px; border: 3px solid rgba(255,255,255,.7)"><img src="assets/img/{img}" alt="" style="object-position: 50% 55%" /></div></div>
      <div class="abs panel" style="left: 0; right: 0; top: 1000px; height: 920px; background: {color_bg}"></div>
      <div class="abs cx lab n" style="top: 1060px; color: {accent}">Varian {num}</div>
      <div class="abs cx disp nm" style="top: 1110px; font-size: 124px">{name}</div>
      <div class="abs cx lab sb" style="top: 1270px; color: {accent}">{sub}</div>
      <div class="abs cx lab w0" style="top: 1370px; color: #fff; letter-spacing: .3em">wangian yang</div>
      <div class="abs cx it k1" style="top: 1420px; font-size: 120px; color: {accent}">{kws[0]}</div>
      <div class="abs cx it k2" style="top: 1550px; font-size: 120px">{kws[1]}</div>'''
    ydir = -1 if top_panel else 1
    js = f'''        tl.fromTo(q(".panel"), {{ yPercent: {100 * ydir} }}, {{ yPercent: 0, duration: 0.55, ease: "expo.inOut" }}, 0);
        tl.fromTo(q(".photo"), {{ yPercent: {-100 * ydir} }}, {{ yPercent: 0, duration: 0.55, ease: "expo.inOut" }}, 0);
        tl.fromTo(q(".pp"), {{ scale: 0.5, rotate: -20 }}, {{ scale: 1, rotate: 0, duration: 0.7, ease: E }}, 0.15);
        tl.fromTo(q(".pp img"), {{ scale: 1.12 }}, {{ scale: 1.0, duration: {d}, ease: "power1.out" }}, 0);
        tl.fromTo(q(".n"), {{ autoAlpha: 0 }}, {{ autoAlpha: 1, duration: 0.3 }}, 0.35);
        tl.fromTo(HF.glyphs(q(".nm")), {{ yPercent: 110 }}, {{ yPercent: 0, duration: 0.5, stagger: 0.03, ease: E }}, 0.4);
        tl.fromTo(q(".sb"), {{ autoAlpha: 0, y: 14 }}, {{ autoAlpha: 1, y: 0, duration: 0.4 }}, 0.75);
        tl.fromTo(q(".w0"), {{ autoAlpha: 0 }}, {{ autoAlpha: 1, duration: 0.3 }}, at({kw_times[0] - 0.5}));
        tl.fromTo(q(".k1"), {{ autoAlpha: 0, y: 40 }}, {{ autoAlpha: 1, y: 0, duration: 0.4, ease: E }}, at({kw_times[0]}));
        tl.fromTo(q(".k2"), {{ autoAlpha: 0, y: 40 }}, {{ autoAlpha: 1, y: 0, duration: 0.4, ease: E }}, at({kw_times[1]}));'''
    return (T0, body, "", js)

C["glory"] = variant("glory", 30.0, 3.26, "glory_w.jpg", False, "linear-gradient(180deg, #7e1525, #3a0710)", "#ffb3bf", "01", "Woman Glory", "Bombshell", ["yakin", "&amp; menawan"], [32.2, 32.74])
C["noche"] = variant("noche", 33.26, 4.14, "noche_w.jpg", True, "linear-gradient(180deg, #120d3a, #2c1f78)", "#c9bcff", "02", "Noche", "Midnight Fantasy", ["lembut", "&amp; misteri"], [36.28, 36.82])

# ---------------------------------------------------------------- stock 37.4–41.2
C["stock"] = (37.4, '''      <div class="fill" style="background: radial-gradient(90% 60% at 50% 35%, #232323, #0b0b0b)"></div>
      <div class="port pt" style="left: 300px; top: 230px; width: 480px; height: 480px"><img src="assets/img/duo_diag.jpg" alt="" /></div>
      <div class="ring rr" style="left: 280px; top: 210px; width: 520px; height: 520px; color: rgba(224,181,143,.6)"></div>
      <div class="abs band b1" style="left: -200px; top: 820px; width: 1480px; height: 100px; background: var(--rouge); transform: rotate(-7deg); overflow: hidden"><div class="m1" style="white-space: nowrap; font-weight: 800; font-size: 54px; line-height: 100px; letter-spacing: .08em">STOK TERHAD ✦ STOK TERHAD ✦ STOK TERHAD ✦ STOK TERHAD ✦ STOK TERHAD ✦ STOK TERHAD ✦</div></div>
      <div class="abs band b2" style="left: -200px; top: 830px; width: 1480px; height: 90px; background: var(--paper); color: var(--char); transform: rotate(6deg); overflow: hidden"><div class="m2" style="white-space: nowrap; font-family: var(--disp); font-size: 52px; line-height: 90px">BATCH INI ✦ BATCH INI ✦ BATCH INI ✦ BATCH INI ✦ BATCH INI ✦ BATCH INI ✦ BATCH INI ✦</div></div>
      <div class="abs ppl" style="left: 140px; top: 1040px; width: 800px; height: 200px"></div>''',
'''      #stock-root .pp { position: absolute; top: 40px; width: 110px; height: 150px; }
      #stock-root .pp i { position: absolute; left: 30px; top: 0; width: 50px; height: 50px; border-radius: 50%; background: #e6e1d7; }
      #stock-root .pp b { position: absolute; left: 5px; top: 60px; width: 100px; height: 80px; border-radius: 50px 50px 12px 12px; background: #e6e1d7; }''',
'''        tl.fromTo(q(".pt"), { scale: 0, rotate: 20 }, { scale: 1, rotate: 0, duration: 0.6, ease: E }, 0);
        tl.fromTo(q(".pt img"), { scale: 1.4 }, { scale: 1.1, duration: 3.8, ease: "power1.out" }, 0);
        tl.fromTo(q(".rr"), { scale: 0.7, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.6, ease: E }, 0.1);
        tl.to(q(".rr"), { scale: 1.08, opacity: 0.3, duration: 0.4, yoyo: true, repeat: 5, ease: "sine.inOut" }, 0.7);
        tl.fromTo(q(".b1"), { xPercent: -110 }, { xPercent: 0, duration: 0.5, ease: E }, 0.05);
        tl.fromTo(q(".b2"), { xPercent: 110 }, { xPercent: 0, duration: 0.5, ease: E }, 0.15);
        tl.fromTo(q(".m1"), { x: 0 }, { x: -600, duration: 3.8, ease: "none" }, 0);
        tl.fromTo(q(".m2"), { x: -600 }, { x: 0, duration: 3.8, ease: "none" }, 0);
        const ppl = [];
        for (let i = 0; i < 3; i++) {
          const p = document.createElement("div"); p.className = "pp"; p.style.left = i * 130 + "px"; p.innerHTML = "<i></i><b></b>"; q(".ppl").appendChild(p); ppl.push(p);
        }
        const bag = document.createElement("div");
        bag.innerHTML = '<svg width="150" height="170" viewBox="0 0 280 330"><path d="M85 110 V80 a55 55 0 0 1 110 0 V110" fill="none" stroke="#ffc21a" stroke-width="22" stroke-linecap="round"/><rect x="20" y="100" width="240" height="220" rx="40" fill="#ffc21a"/></svg>';
        Object.assign(bag.style, { position: "absolute", left: "640px", top: "20px" }); q(".ppl").appendChild(bag);
        tl.fromTo(ppl, { autoAlpha: 0, x: -120 }, { autoAlpha: 1, x: 0, duration: 0.4, stagger: 0.1, ease: E }, at(39.3));
        tl.fromTo(bag, { autoAlpha: 0, scale: 0.4 }, { autoAlpha: 1, scale: 1, duration: 0.4, ease: B }, at(39.5));
        tl.to(ppl, { x: 230, duration: 0.6, stagger: 0.08, ease: "power2.in" }, at(40.3));
        tl.to(ppl, { autoAlpha: 0, duration: 0.2, stagger: 0.08 }, at(40.75));''')

# ---------------------------------------------------------------- CTA 41.2–45
C["cta"] = (41.2, '''      <img class="clip bg bgimg" data-start="0" data-duration="3.8" src="assets/img/duo_flat.jpg" alt="" style="filter: brightness(.55)" />
      <div class="abs cx disp t1" style="top: 200px; font-size: 120px">Klik link</div>
      <div class="abs cx it t2" style="top: 330px; font-size: 100px; color: var(--copper2)">di bawah</div>
      <svg class="abs arw" style="left: 510px; top: 480px" width="60" height="110" viewBox="0 0 60 110" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"><path d="M30 6 V100 M8 76 L30 100 L52 76" /></svg>
      <div class="abs btn" style="left: 110px; right: 110px; top: 640px; height: 170px; border-radius: 85px; background: #ffc21a; color: var(--char); display: flex; align-items: center; justify-content: center; gap: 24px; font-weight: 800; font-size: 54px; box-shadow: 0 30px 80px rgba(0,0,0,.45)">
        <svg width="80" height="90" viewBox="0 0 280 330"><path d="M85 110 V80 a55 55 0 0 1 110 0 V110" fill="none" stroke="#121212" stroke-width="24" stroke-linecap="round" /><rect x="20" y="100" width="240" height="220" rx="40" fill="#121212" /></svg>TEKAN BEG KUNING
      </div>
      <div class="ring rp" style="left: 540px; top: 725px; width: 40px; height: 40px; margin: -20px 0 0 -20px; color: #ffc21a; border-width: 4px"></div>
      <div class="abs cx co" style="top: 880px"><span class="chip" style="background: var(--paper); color: var(--char); font-size: 44px; padding: 22px 44px">CHECK OUT SEKARANG →</span></div>''',
'',
'''        tl.fromTo(q(".bgimg"), { scale: 1.2 }, { scale: 1.03, duration: 3.8, ease: "power1.out" }, 0);
        tl.fromTo(HF.glyphs(q(".t1")), { yPercent: 110 }, { yPercent: 0, duration: 0.45, stagger: 0.03, ease: E }, 0.02);
        tl.fromTo(q(".t2"), { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: 0.4, ease: E }, at(41.84));
        tl.fromTo(q(".arw"), { autoAlpha: 0, y: -20 }, { autoAlpha: 1, y: 0, duration: 0.3 }, at(41.9));
        tl.to(q(".arw"), { y: 24, duration: 0.25, yoyo: true, repeat: 9, ease: "sine.inOut" }, at(42.2));
        tl.fromTo(q(".btn"), { autoAlpha: 0, scale: 0.5 }, { autoAlpha: 1, scale: 1, duration: 0.5, ease: "elastic.out(1,0.6)" }, at(42.45));
        tl.to(q(".btn"), { scale: 1.06, duration: 0.24, yoyo: true, repeat: 7, ease: "sine.inOut" }, at(43.0));
        [42.95, 43.7, 44.4].forEach((t) => tl.fromTo(q(".rp"), { autoAlpha: 0.9, scale: 1 }, { autoAlpha: 0, scale: 24, duration: 0.6, ease: "power2.out", immediateRender: false }, at(t)));
        tl.set(q(".rp"), { autoAlpha: 0 }, 0);
        tl.fromTo(q(".co"), { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: 0.4, ease: B }, at(43.26));''')

# ---------------------------------------------------------------- captions 0–45
C["captions"] = (0, '''      <div class="fill caps"></div>''',
'''      #captions-root { --capc: #ffffff; --capem: #e0b58f; --capbox: #9cc3c9; --capon: #121212; --capshadow: 0 2px 4px rgba(0,0,0,.5), 0 4px 30px rgba(0,0,0,.6); }
      #captions-root .cap { position: absolute; left: 60px; right: 60px; top: 1320px; text-align: center; font-family: var(--sans); font-weight: 800; font-size: 84px; line-height: 1.12; letter-spacing: -0.025em; color: var(--capc); text-shadow: var(--capshadow); opacity: 0; }
      #captions-root .w { display: inline-block; position: relative; margin: 0 0.12em; padding: 0 0.08em; }
      #captions-root .w.e { color: var(--capem); font-family: var(--it); font-style: italic; font-weight: 700; font-size: 1.18em; letter-spacing: 0; line-height: 0.9; }
      #captions-root .w .bx { position: absolute; left: -6px; right: -6px; top: 8%; bottom: 4%; border-radius: 14px; background: var(--capbox); z-index: -1; transform: scaleX(0); transform-origin: 0 50%; }''',
'''        const root = q(".caps").parentElement;
        // paper scenes 5.04–18.46: dark ink captions; variant scenes 30–37.4: names shown on panels, captions hidden
        tl.set(root, { "--capc": "#121212", "--capem": "#a8683c", "--capbox": "#d6e8ea", "--capshadow": "0 0 0 rgba(0,0,0,0)" }, 5.04);
        tl.set(root, { "--capc": "#ffffff", "--capem": "#e0b58f", "--capbox": "#9cc3c9", "--capshadow": "0 2px 4px rgba(0,0,0,.5), 0 4px 30px rgba(0,0,0,.6)" }, 18.46);
        const HIDE = [[30.0, 37.4]];
        window.CAPTIONS.forEach((chunk, i) => {
          const s = chunk[0][1];
          if (HIDE.some(([a, b]) => s >= a && s < b)) return;
          const d = document.createElement("div"); d.className = "cap";
          chunk.forEach(([w, ws, we, em]) => {
            const sp = document.createElement("span"); sp.className = "w" + (em ? " e" : ""); sp.textContent = w; sp.dataset.s = ws;
            const bx = document.createElement("i"); bx.className = "bx"; sp.appendChild(bx); d.appendChild(sp);
          });
          q(".caps").appendChild(d);
          const next = window.CAPTIONS[i + 1];
          let e = next ? Math.min(next[0][1], chunk[chunk.length - 1][2] + 0.6) : 44.7;
          HIDE.forEach(([a]) => { if (s < a && e > a) e = a; });
          tl.fromTo(d, { autoAlpha: 0, y: 26, scale: 0.96 }, { autoAlpha: 1, y: 0, scale: 1, duration: 0.16, ease: P }, s);
          tl.to(d, { autoAlpha: 0, duration: 0.07 }, Math.max(s + 0.2, e - 0.06));
          Array.from(d.children).forEach((w) => {
            const t = Math.max(s, +w.dataset.s - 0.03);
            const bx = w.querySelector(".bx");
            tl.fromTo(w, { opacity: 0.45 }, { opacity: 1, duration: 0.1 }, t);
            if (!w.classList.contains("e")) {
              tl.fromTo(bx, { scaleX: 0 }, { scaleX: 1, duration: 0.14, ease: P, immediateRender: false }, t);
              const light = t >= 5.04 && t < 18.46;
              tl.to(w, { color: "#121212", textShadow: "0 0 0 rgba(0,0,0,0)", duration: 0.08 }, t + 0.04);
              tl.to(bx, { scaleX: 0, transformOrigin: "100% 50%", duration: 0.14 }, t + 0.34);
              tl.to(w, { color: light ? "#121212" : "#ffffff", textShadow: light ? "0 0 0 rgba(0,0,0,0)" : "0 2px 4px rgba(0,0,0,.5), 0 4px 30px rgba(0,0,0,.6)", duration: 0.08 }, t + 0.36);
            } else {
              tl.fromTo(w, { scale: 0.85 }, { scale: 1.06, duration: 0.2, ease: B, immediateRender: false }, t);
            }
          });
        });''')

# ---------------------------------------------------------------- HUD 0–45
C["hud"] = (0, '''      <div class="fill hud">
        <div class="abs logo" style="left: 70px; top: 80px; font-family: var(--disp); font-size: 34px; letter-spacing: .32em">FRESCURA</div>
        <div class="abs lab tag" style="right: 70px; top: 88px; font-size: 20px">Ocean salt series</div>
        <div class="abs rail" style="left: 40px; top: 330px; width: 3px; height: 1260px; background: rgba(255,255,255,.18)"><div class="rf" style="width: 100%; height: 100%; background: currentColor; transform-origin: 50% 0%"></div></div>
        <div class="abs ix" style="left: 70px; top: 130px; font-weight: 800; font-size: 26px; letter-spacing: .2em"><span>01 / 03</span><span>02 / 03</span><span>03 / 03</span></div>
      </div>
      <div class="fill iris" style="clip-path: circle(0% at 50% 50%)"></div>''',
'''      #hud-root .hud { color: var(--hudc, #ffffff); }
      #hud-root .ix span { position: absolute; left: 0; top: 0; white-space: nowrap; opacity: 0; }''',
'''        const hud = q(".hud");
        tl.fromTo(q(".rf"), { scaleY: 0 }, { scaleY: 1, duration: 45, ease: "none" }, 0);
        tl.set(hud, { "--hudc": "#121212" }, 5.04).set(hud, { "--hudc": "#ffffff" }, 18.46);
        tl.set(q(".rail"), { background: "rgba(18,18,18,.15)" }, 5.04).set(q(".rail"), { background: "rgba(255,255,255,.18)" }, 18.46);
        const ix = qa(".ix span");
        [[5.04, 9.2], [9.2, 12.88], [12.88, 18.46]].forEach(([a, b], i) => {
          tl.fromTo(ix[i], { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.3, immediateRender: false }, a + 0.05);
          tl.to(ix[i], { opacity: 0, duration: 0.12 }, b - 0.12);
        });
        // porthole iris transitions: close on the cut, open on the next scene
        const iris = q(".iris");
        [[5.04, "#f3f0ea"], [18.46, "#0e2735"], [21.88, "#0e2735"], [37.4, "#121212"], [41.2, "#0e2735"]].forEach(([t, c]) => {
          tl.set(iris, { background: c }, t - 0.34);
          tl.fromTo(iris, { clipPath: "circle(0% at 50% 50%)" }, { clipPath: "circle(75% at 50% 50%)", duration: 0.32, ease: "power2.in", immediateRender: false }, t - 0.33);
          tl.to(iris, { clipPath: "circle(0% at 50% 50%)", duration: 0.4, ease: "power3.out" }, t + 0.01);
        });''')

seeds = {k: 101 + i * 17 for i, k in enumerate(C)}
for cid, (T0, body, css, js) in C.items():
    open(f"{P}/compositions/{cid}.html", "w").write(comp(cid, T0, body, css, js, seeds[cid]))
print("wrote", len(C), "compositions")
