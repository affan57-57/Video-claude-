# Generates hf/frescura/index.html — Frescura Body 40s luxury educational ad (HyperFrames + GSAP)
import json, math, os, html
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.join(HERE, "hf", "frescura")
WORDS = json.load(open(os.path.join(HERE, "work", "words_final.json")))
DUR = 40.0

# ---------- scene timing (final film seconds) ----------
SC = {
    "hook": (0.0, 5.85), "edu": (5.85, 11.05), "small": (11.05, 14.05), "care": (14.05, 17.0),
    "logo": (17.0, 18.1), "shop": (18.1, 20.5), "foam": (20.5, 22.7), "scent": (22.7, 27.0),
    "smile": (27.0, 29.9), "cta": (29.9, 33.6), "stock": (33.6, 37.5), "end": (37.5, 40.0),
}
def clip(sid, extra="", z=1):
    s, e = SC[sid]
    return f'id="sc-{sid}" class="clip scene" data-start="{s}" data-duration="{round(e-s,3)}" data-track-index="1" style="z-index:{z}" {extra}'

# ---------- icons (thin-line luxury) ----------
ICON = {
 "chat": '<svg viewBox="0 0 64 64"><path d="M10 14h44v28H30l-12 10V42h-8z"/><path d="M22 28h20M22 34h12"/></svg>',
 "moon": '<svg viewBox="0 0 64 64"><path d="M40 10a22 22 0 1 0 14 34A18 18 0 0 1 40 10z"/><path d="M46 16l2 4 4 2-4 2-2 4-2-4-4-2 4-2z"/></svg>',
 "gift": '<svg viewBox="0 0 64 64"><rect x="10" y="26" width="44" height="28"/><rect x="7" y="18" width="50" height="9"/><path d="M32 18v36M32 18c-6-10-16-8-14-2 1 3 8 2 14 2zM32 18c6-10 16-8 14-2-1 3-8 2-14 2z"/></svg>',
 "home": '<svg viewBox="0 0 64 64"><path d="M10 30L32 12l22 18v24H10z"/><path d="M32 46s-9-6-9-11a5 5 0 0 1 9-2 5 5 0 0 1 9 2c0 5-9 11-9 11z"/></svg>',
}
BAG = '''<svg viewBox="0 0 120 120"><defs><linearGradient id="bagG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE07A"/><stop offset="1" stop-color="#F5B419"/></linearGradient></defs>
<path d="M22 40h76l-6 66H28z" fill="url(#bagG)" stroke="#1b1206" stroke-width="3" stroke-linejoin="round"/>
<path d="M42 50V34a18 18 0 0 1 36 0v16" fill="none" stroke="#1b1206" stroke-width="5" stroke-linecap="round"/></svg>'''

# ---------- captions ----------
HIDE = [(0.0, 5.84), (16.95, 18.12), (37.45, 99)]
def hidden(t): return any(a <= t < b for a, b in HIDE)
chunks, cur = [], []
for w in WORDS:
    cur.append(w)
    endp = w[0][-1] in ",."
    if len(cur) >= 4 or endp or (len(" ".join(x[0] for x in cur)) > 22):
        chunks.append(cur); cur = []
if cur: chunks.append(cur)
cap_html, cap_js = [], []
for i, ch in enumerate(chunks):
    s = ch[0][1] - 0.04
    nxt = chunks[i+1][0][1] - 0.04 if i + 1 < len(chunks) else ch[-1][2] + 0.4
    e = min(nxt, ch[-1][2] + 0.7)
    if hidden(s): continue
    for a, b in HIDE:
        if s < a < e: e = a
    spans = []
    for j, (w, ws, we) in enumerate(ch):
        txt = html.escape(w.rstrip(",."))
        spans.append(f'<span class="w" id="cw{i}_{j}">{txt}</span>')
        cap_js.append(f'tl.to("#cw{i}_{j}",{{opacity:1,color:"#E9C77E",scale:1.06,duration:.08}},{ws:.2f});'
                      f'tl.to("#cw{i}_{j}",{{color:"#FBF7EF",scale:1,duration:.15}},{max(we, ws+0.12):.2f});')
    cap_html.append(f'<div class="cap clip" id="cap{i}" data-start="{s:.2f}" data-duration="{e-s:.2f}" data-track-index="5">{" ".join(spans)}</div>')
    cap_js.append(f'tl.fromTo("#cap{i}",{{y:26,opacity:0,filter:"blur(6px)"}},{{y:0,opacity:1,filter:"blur(0px)",duration:.22,ease:"power3.out"}},{s:.2f});')

# ---------- bokeh particles (deterministic) ----------
def prng(seed):
    x = seed
    while True:
        x = (x * 1103515245 + 12345) & 0x7fffffff
        yield x / 0x7fffffff
R = prng(42)
bokeh, bokeh_js = [], []
for i in range(22):
    x, y, sz = next(R)*1080, next(R)*1920, 6 + next(R)*26
    op = .15 + next(R)*.45; dx, dy = (next(R)-.5)*160, -60 - next(R)*220
    bokeh.append(f'<i class="bk" id="bk{i}" style="left:{x:.0f}px;top:{y:.0f}px;width:{sz:.0f}px;height:{sz:.0f}px;opacity:{op:.2f}"></i>')
    bokeh_js.append(f'tl.fromTo("#bk{i}",{{x:0,y:0}},{{x:{dx:.0f},y:{dy:.0f},duration:{DUR},ease:"none"}},0);')

# ---------- scene-cut flashes ----------
cuts = [SC[k][0] for k in SC if SC[k][0] > 0]
flash_js = 'tl.set("#flash",{opacity:0},0);' + "".join(f'tl.to("#flash",{{opacity:.55,duration:.08,ease:"power2.out"}},{c-0.06:.2f});tl.to("#flash",{{opacity:0,duration:.32,ease:"power2.in"}},{c+0.02:.2f});' for c in cuts)
punch_js = "".join(f'tl.fromTo("#sc-{k}",{{scale:1.07,filter:"blur(8px)"}},{{scale:1,filter:"blur(0px)",duration:.42,ease:"expo.out"}},{SC[k][0]:.2f});' for k in SC if k not in ("hook",))

FONTCSS = open(os.path.join(PROJ,"assets","fonts","fonts.css")).read().replace("url(./","url(assets/fonts/")
CSS = r"""
__FONTS__
:root{--ink:#0b0809;--plum:#1a0f1c;--gold:#d9b46a;--gold2:#f0d79a;--cham:#f3e6cc;--ivory:#fbf7ef;--rose:#b3122e;--violet:#6a4bd8;
 --serif:'Bodoni Moda',serif;--sans:'Manrope',sans-serif}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:var(--ink)}
#root{position:relative;width:1080px;height:1920px;overflow:hidden;background:radial-gradient(120% 80% at 50% 30%,#24142a 0%,#120a12 55%,#070506 100%);font-family:var(--sans);color:var(--ivory)}
.scene{position:absolute;inset:0;overflow:hidden;transform-origin:50% 45%}
.abs{position:absolute}
.cover{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.bk{position:absolute;border-radius:50%;background:rgba(243,217,155,.55);box-shadow:0 0 18px 6px rgba(217,180,106,.35);z-index:2}
.eyebrow{font:700 26px/1 var(--sans);letter-spacing:.42em;text-transform:uppercase;color:var(--gold)}
.serif,.serif *{font-family:var(--serif);font-optical-sizing:none;font-variation-settings:"opsz" 11}
.center{left:0;right:0;text-align:center}
.goldtxt{background:linear-gradient(100deg,#b8893e 0%,#f6e2a8 38%,#fff6da 50%,#d9b46a 62%,#a87a32 100%);background-size:220% 100%;-webkit-background-clip:text;background-clip:text;color:transparent}
.line{position:absolute;height:2px;background:linear-gradient(90deg,rgba(217,180,106,0),var(--gold),rgba(217,180,106,0));transform-origin:left center}
/* frame */
#frame{position:absolute;inset:34px;border:1px solid rgba(217,180,106,.38);z-index:40;pointer-events:none}
#frame:before,#frame:after{content:"";position:absolute;width:46px;height:46px;border:2px solid var(--gold)}
#frame:before{left:-6px;top:-6px;border-right:none;border-bottom:none}
#frame:after{right:-6px;bottom:-6px;border-left:none;border-top:none}
#grain{position:absolute;inset:-256px;background:url(assets/img/grain.png);opacity:.07;mix-blend-mode:overlay;z-index:45}
#vig{position:absolute;inset:0;background:radial-gradient(110% 75% at 50% 45%,rgba(0,0,0,0) 55%,rgba(0,0,0,.55) 100%);z-index:39}
#flash{position:absolute;inset:0;background:radial-gradient(70% 50% at 70% 30%,rgba(255,226,170,.95),rgba(255,180,120,.35) 45%,rgba(0,0,0,0) 75%);mix-blend-mode:screen;opacity:0;z-index:44}
#capband{position:absolute;left:0;right:0;top:1250px;height:380px;background:linear-gradient(180deg,rgba(8,5,8,0),rgba(8,5,8,.62) 35%,rgba(8,5,8,.62) 70%,rgba(8,5,8,0));z-index:30}
.cap{position:absolute;left:90px;right:90px;top:1335px;text-align:center;font:800 62px/1.18 var(--sans);letter-spacing:.005em;text-transform:uppercase;z-index:41;
 text-shadow:0 4px 18px rgba(0,0,0,.65),0 1px 2px rgba(0,0,0,.8)}
.cap .w{display:inline-block;margin:0 .05em;opacity:.42;color:var(--ivory);transform-origin:50% 70%}
/* glass card */
.card{position:absolute;left:90px;width:900px;height:200px;border-radius:28px;background:linear-gradient(120deg,rgba(255,255,255,.10),rgba(255,255,255,.03));
 border:1px solid rgba(217,180,106,.45);box-shadow:0 20px 60px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.12);backdrop-filter:blur(14px);overflow:hidden}
.card .num{position:absolute;left:38px;top:34px;font:italic 500 112px/1 var(--serif);color:var(--gold)}
.card .tx{position:absolute;left:200px;right:150px;top:0;bottom:0;display:flex;align-items:center;font:700 46px/1.15 var(--sans);color:var(--ivory)}
.card svg,.ico svg{position:absolute;right:42px;top:56px;width:88px;height:88px;fill:none;stroke:var(--gold);stroke-width:2.4;stroke-linejoin:round;stroke-linecap:round}
.card .sheen{position:absolute;top:0;bottom:0;width:180px;left:-220px;background:linear-gradient(100deg,rgba(255,255,255,0),rgba(255,240,200,.28),rgba(255,255,255,0));transform:skewX(-18deg)}
.pill{position:absolute;padding:20px 34px;border-radius:999px;font:800 34px/1 var(--sans);letter-spacing:.14em;text-transform:uppercase;
 background:rgba(12,8,12,.55);border:1px solid rgba(217,180,106,.6);color:var(--ivory);backdrop-filter:blur(10px);white-space:nowrap}
.pill b{display:inline-block;width:14px;height:14px;border-radius:50%;background:var(--gold);margin-right:16px;vertical-align:middle;box-shadow:0 0 14px var(--gold)}
"""

def esc(s): return html.escape(s)

body = []
js = []
A = js.append

# ======================= SC1 HOOK =======================
body.append(f'''<div {clip("hook")}>
  <img class="cover" id="h-bg" src="assets/img/duo_dark.jpg" style="filter:blur(22px) brightness(.32) saturate(1.1);transform:scale(1.2)">
  <div class="abs" id="h-spot" style="left:140px;top:860px;width:800px;height:1000px;background:radial-gradient(50% 50% at 50% 40%,rgba(255,226,170,.28),rgba(0,0,0,0) 70%)"></div>
  <div class="abs" id="h-bottles" style="left:0;right:0;top:1010px;height:700px">
     <img class="abs" id="h-b1" src="assets/img/cut_bombshell.png" style="left:250px;top:40px;height:600px;filter:drop-shadow(0 30px 40px rgba(0,0,0,.6))">
     <img class="abs" id="h-b2" src="assets/img/cut_noche.png" style="left:560px;top:40px;height:600px;filter:drop-shadow(0 30px 40px rgba(0,0,0,.6))">
     <div class="line" id="h-floor" style="left:120px;width:840px;top:640px"></div>
  </div>
  <div class="abs center" id="h-g1" style="top:250px">
     <div class="serif" id="h-suami" style="font-weight:800;font-size:178px;line-height:1;letter-spacing:.06em">SUAMI,</div>
     <div class="serif goldtxt" id="h-tahu" style="font-style:italic;font-weight:500;font-size:112px;line-height:1.15;margin-top:14px">korang tahu tak?</div>
  </div>
  <div class="abs center" id="h-g2" style="top:250px;opacity:0">
     <div class="eyebrow" id="h-ist" style="font-size:34px;color:var(--cham)">Isteri bukan nak</div>
     <div style="position:relative;display:inline-block;margin-top:26px">
        <div class="serif" id="h-mahal" style="font-weight:800;font-size:132px;line-height:1">HADIAH MAHAL</div>
        <div class="abs" id="h-strike" style="left:-14px;right:-14px;top:62px;height:8px;background:var(--rose);box-shadow:0 0 18px rgba(179,18,46,.8);transform-origin:left"></div>
     </div>
  </div>
  <div class="abs center" id="h-g3" style="top:240px;opacity:0">
     <div class="eyebrow" id="h-rasa" style="font-size:30px;color:var(--cham);line-height:1.6">Dia cuma nak rasa<br>suami masih</div>
     <div class="serif goldtxt" id="h-peduli" style="font-style:italic;font-weight:700;font-size:250px;line-height:1.05;margin-top:6px">peduli</div>
  </div>
</div>''')
A('tl.fromTo("#h-bg",{scale:1.25},{scale:1.08,duration:5.85,ease:"none"},0);')
A('tl.fromTo("#h-suami",{opacity:.35,scale:1.6,filter:"blur(14px)"},{opacity:1,scale:1,filter:"blur(0px)",duration:.4,ease:"expo.out"},0.0);')
A('tl.fromTo("#h-tahu",{opacity:0,y:60,clipPath:"inset(100% 0 0 0)"},{opacity:1,y:0,clipPath:"inset(0% 0 0 0)",duration:.4,ease:"power3.out"},0.6);')
A('tl.fromTo("#h-tahu",{backgroundPosition:"100% 0"},{backgroundPosition:"0% 0",duration:1.2,ease:"power1.inOut"},0.7);')
A('tl.fromTo("#h-bottles",{y:220,opacity:0},{y:0,opacity:1,duration:.9,ease:"expo.out"},0.15);')
A('tl.fromTo("#h-floor",{scaleX:0},{scaleX:1,duration:.8,ease:"power3.out"},0.4);')
A('tl.fromTo("#h-b1",{rotation:-4},{rotation:0,duration:5.6,ease:"sine.inOut"},0);tl.fromTo("#h-b2",{rotation:4},{rotation:0,duration:5.6,ease:"sine.inOut"},0);')
A('tl.fromTo("#h-spot",{opacity:.3},{opacity:1,duration:2,ease:"sine.inOut"},0);')
A('tl.to("#h-g1",{opacity:0,y:-80,filter:"blur(10px)",duration:.25,ease:"power2.in"},1.3);')
A('tl.fromTo("#h-g2",{opacity:0,y:70},{opacity:1,y:0,duration:.35,ease:"power3.out"},1.42);')
A('tl.fromTo("#h-mahal",{scale:.8,opacity:0},{scale:1,opacity:1,duration:.4,ease:"back.out(1.6)"},2.4);')
A('tl.fromTo("#h-strike",{scaleX:0},{scaleX:1,duration:.22,ease:"power4.out"},2.92);tl.to("#h-mahal",{opacity:.45,duration:.25},3.0);')
A('tl.to("#h-g2",{opacity:0,y:-80,filter:"blur(10px)",duration:.22,ease:"power2.in"},3.05);')
A('tl.fromTo("#h-g3",{opacity:0,y:60},{opacity:1,y:0,duration:.35,ease:"power3.out"},3.15);')
A('tl.fromTo("#h-peduli",{opacity:0,scale:.5,filter:"blur(20px)"},{opacity:1,scale:1,filter:"blur(0px)",duration:.5,ease:"expo.out"},4.52);')
A('tl.fromTo("#h-peduli",{backgroundPosition:"100% 0"},{backgroundPosition:"0% 0",duration:1.1,ease:"power2.inOut"},4.6);')
A('tl.fromTo("#h-bottles",{scale:1},{scale:1.08,duration:1.3,ease:"power2.out"},4.52);')

# ======================= SC2 EDUCATIONAL =======================
cards = [("01", "Tanya keadaan dirinya", "chat", 5.86), ("02", "Ambil tahu bila dia penat", "moon", 7.52), ("03", "Buat sesuatu tanpa diminta", "gift", 8.90)]
ch = "".join(f'''<div class="card" id="cd{i}" style="top:{500+i*240}px;opacity:0"><div class="sheen" id="cs{i}"></div><div class="num">{n}</div><div class="tx">{esc(t)}</div>{ICON[ic]}</div>''' for i, (n, t, ic, _) in enumerate(cards))
body.append(f'''<div {clip("edu")}>
  <img class="cover" id="e-bg" src="assets/img/flatlay2.jpg" style="filter:blur(26px) brightness(.38) saturate(.9)">
  <div class="abs center" style="top:205px"><div class="eyebrow" id="e-eb">Panduan Suami</div>
    <div class="serif" id="e-h" style="font-size:96px;font-weight:500;line-height:1.08;margin-top:22px">3 Tanda Suami <span class="goldtxt" style="font-style:italic">Peduli</span></div>
    <div class="line" id="e-ln" style="left:300px;width:480px;top:220px"></div></div>
  {ch}
</div>''')
A('tl.fromTo("#e-bg",{scale:1.15},{scale:1.02,duration:5.2,ease:"none"},5.85);')
A('tl.fromTo("#e-eb",{opacity:0,scaleX:1.4},{opacity:1,scaleX:1,duration:.5,ease:"power3.out"},5.9);')
A('tl.fromTo("#e-h",{opacity:0,y:40},{opacity:1,y:0,duration:.45,ease:"power3.out"},5.95);')
A('tl.fromTo("#e-ln",{scaleX:0},{scaleX:1,duration:.6,ease:"power3.out"},6.1);')
for i, (_, _, _, t) in enumerate(cards):
    A(f'tl.fromTo("#cd{i}",{{opacity:0,x:140,rotationY:-25}},{{opacity:1,x:0,rotationY:0,duration:.5,ease:"expo.out"}},{t:.2f});')
    A(f'tl.fromTo("#cs{i}",{{x:0}},{{x:1220,duration:.8,ease:"power2.inOut"}},{t+.15:.2f});')
    A(f'tl.fromTo("#cd{i} svg",{{strokeDasharray:300,strokeDashoffset:300}},{{strokeDashoffset:0,duration:.9,ease:"power2.out"}},{t+.1:.2f});')
    if i < 2:
        A(f'tl.to("#cd{i}",{{opacity:.5,scale:.97,duration:.3}},{cards[i+1][3]:.2f});')

# ======================= SC3 SMALL -> BIG =======================
rings = "".join(f'<div class="abs rg" id="rg{i}" style="left:540px;top:760px;width:{760-i*170}px;height:{760-i*170}px;margin:-{380-i*85}px 0 0 -{380-i*85}px;opacity:0;border-radius:50%;border:2px solid rgba(217,180,106,{.9-i*.25:.2f})"></div>' for i in range(3))
body.append(f'''<div {clip("small")}>
  <div class="abs center" id="s-t1" style="top:250px"><div class="eyebrow">Perkara</div>
     <div class="serif" style="font-size:120px;font-style:italic;line-height:1.1;margin-top:10px;color:var(--cham)">kecil</div></div>
  <div class="abs" id="s-dot" style="left:525px;top:745px;width:30px;height:30px;border-radius:50%;background:var(--gold);box-shadow:0 0 30px var(--gold)"></div>
  {rings}
  <div class="abs center" id="s-big" style="top:640px;opacity:0"><div class="serif goldtxt" style="font-weight:800;font-size:128px;line-height:1">MAKNA</div>
     <div class="serif goldtxt" style="font-weight:800;font-size:128px;line-height:1.05">BESAR</div></div>
  <div class="abs center ico" id="s-fam" style="top:1120px;opacity:0;height:120px"><div class="eyebrow" style="color:var(--cham);font-size:30px">dalam keluarga</div>
     <div style="position:relative;width:88px;height:88px;margin:18px auto 0">{ICON["home"].replace('<svg','<svg style="right:0;top:0"')}</div></div>
</div>''')
A('tl.fromTo("#s-t1",{opacity:0,y:40},{opacity:1,y:0,duration:.4,ease:"power3.out"},11.08);')
A('tl.fromTo("#s-dot",{scale:0},{scale:1,duration:.4,ease:"back.out(3)"},11.25);')
A('tl.to("#s-dot",{scale:.6,duration:.4,yoyo:true,repeat:1,ease:"sine.inOut"},11.65);')
A('tl.to("#s-t1",{opacity:.35,y:-30,duration:.3},12.5);')
A('tl.to("#s-dot",{scale:26,opacity:0,duration:.8,ease:"expo.out"},12.55);')
for i in range(3):
    A(f'tl.fromTo("#rg{i}",{{scale:.03,opacity:1}},{{scale:1,opacity:{.9-i*.2:.2f},duration:{.9+i*.15:.2f},ease:"expo.out"}},{12.55+i*.07:.2f});')
A('tl.fromTo("#s-big",{opacity:0,scale:.55,filter:"blur(16px)"},{opacity:1,scale:1,filter:"blur(0px)",duration:.5,ease:"expo.out"},12.6);')
A('tl.fromTo("#s-big div",{backgroundPosition:"100% 0"},{backgroundPosition:"0% 0",duration:1.2,ease:"power2.inOut"},12.7);')
A('tl.fromTo("#s-fam",{opacity:0,y:30},{opacity:1,y:0,duration:.4,ease:"power3.out"},13.2);')
A('tl.fromTo("#s-fam svg",{strokeDasharray:300,strokeDashoffset:300},{strokeDashoffset:0,duration:.8},13.25);')

# ======================= SC4 CARE (B-roll photo) =======================
body.append(f'''<div {clip("care")}>
  <img class="cover" id="c-bg" src="assets/img/flatlay1.jpg" style="filter:brightness(.82) saturate(1.05)">
  <div class="abs" style="inset:0;background:linear-gradient(180deg,rgba(8,5,8,.85) 0%,rgba(8,5,8,.25) 34%,rgba(8,5,8,0) 55%,rgba(8,5,8,.4) 100%)"></div>
  <div class="abs center" style="top:200px"><div class="eyebrow" id="c-eb">Jangan lupa beri</div>
    <div class="serif" id="c-h" style="font-style:italic;font-size:150px;line-height:1.05;margin-top:16px">Perhatian</div>
    <div class="line" id="c-ln" style="left:260px;width:560px;top:230px;height:3px"></div>
    <div class="eyebrow" id="c-k" style="margin-top:46px;color:var(--cham);font-size:28px">kepada isteri</div></div>
  <div class="pill ico" id="c-gift" style="left:330px;top:1130px;opacity:0;padding-left:96px">Hadiahkan
     <div style="position:absolute;left:24px;top:8px;width:58px;height:58px">{ICON["gift"].replace('<svg','<svg style="right:0;top:0;width:58px;height:58px"')}</div></div>
</div>''')
A('tl.fromTo("#sc-care",{clipPath:"circle(0% at 50% 45%)"},{clipPath:"circle(80% at 50% 45%)",duration:.55,ease:"power3.inOut"},14.05);')
A('tl.fromTo("#c-bg",{scale:1.22,x:30},{scale:1.04,x:-20,duration:2.95,ease:"none"},14.05);')
A('tl.fromTo("#c-eb",{opacity:0,y:20},{opacity:1,y:0,duration:.4},14.3);')
A('tl.fromTo("#c-h",{opacity:0,y:50,filter:"blur(12px)"},{opacity:1,y:0,filter:"blur(0px)",duration:.5,ease:"expo.out"},15.0);')
A('tl.fromTo("#c-ln",{scaleX:0},{scaleX:1,duration:.5,ease:"power3.out"},15.35);')
A('tl.fromTo("#c-k",{opacity:0},{opacity:1,duration:.3},15.7);')
A('tl.fromTo("#c-gift",{opacity:0,scale:.6},{opacity:1,scale:1,duration:.4,ease:"back.out(2)"},16.5);')

# ======================= SC5 LOGO =======================
body.append(f'''<div {clip("logo")} >
  <div class="abs" style="inset:0;background:#000"></div>
  <img class="abs" id="l-logo" src="assets/img/logo.jpg" style="left:90px;top:510px;width:900px;height:900px;mix-blend-mode:screen">
  <div class="abs" id="l-sweep" style="left:-400px;top:0;width:260px;height:1920px;background:linear-gradient(90deg,rgba(255,255,255,0),rgba(190,240,255,.35),rgba(255,255,255,0));transform:skewX(-14deg);mix-blend-mode:screen"></div>
</div>''')
A('tl.fromTo("#l-logo",{opacity:0,scale:.75,filter:"blur(24px) brightness(2)"},{opacity:1,scale:1,filter:"blur(0px) brightness(1.15)",duration:.55,ease:"expo.out"},17.02);')
A('tl.to("#l-logo",{scale:1.06,duration:.55,ease:"none"},17.57);')
A('tl.fromTo("#l-sweep",{x:0},{x:1700,duration:.75,ease:"power2.inOut"},17.25);')

# ======================= SC6 MALL BOUTIQUE =======================
slats = "repeating-linear-gradient(90deg,rgba(201,162,92,.0) 0px,rgba(201,162,92,.0) 54px,rgba(214,176,104,.55) 56px,rgba(120,88,40,.6) 58px,rgba(201,162,92,0) 60px)"
body.append(f'''<div {clip("shop")}>
 <div class="abs" id="b-world" style="inset:0;transform-origin:50% 62%">
  <div class="abs" style="inset:0;background:linear-gradient(180deg,#140d0c 0%,#22160f 45%,#1a110c 70%)"></div>
  <div class="abs" style="inset:0 0 560px 0;background:{slats};opacity:.85"></div>
  <div class="abs" id="b-arch" style="left:190px;top:330px;width:700px;height:1050px;border-radius:350px 350px 0 0;background:radial-gradient(80% 60% at 50% 35%,#5a3b22 0%,#2a1a10 60%,#140c08 100%);border:3px solid rgba(217,180,106,.7);box-shadow:inset 0 0 120px rgba(0,0,0,.6),0 0 60px rgba(217,180,106,.15)"></div>
  <div class="abs center serif" id="b-sign" style="top:460px;font-size:56px;letter-spacing:.32em;font-weight:500" ><span class="goldtxt">FRESCURA BODY</span></div>
  <div class="abs center eyebrow" id="b-sub" style="top:550px;font-size:20px;letter-spacing:.6em;color:var(--cham);opacity:.8">soft | fragrant</div>
  <div class="abs" id="b-c1" style="left:150px;top:0;width:340px;height:1500px;background:linear-gradient(180deg,rgba(255,232,190,.36),rgba(255,232,190,0) 85%);clip-path:polygon(42% 0,58% 0,100% 100%,0 100%);mix-blend-mode:screen"></div>
  <div class="abs" id="b-c2" style="left:590px;top:0;width:340px;height:1500px;background:linear-gradient(180deg,rgba(255,232,190,.36),rgba(255,232,190,0) 85%);clip-path:polygon(42% 0,58% 0,100% 100%,0 100%);mix-blend-mode:screen"></div>
  <div class="abs" style="left:0;right:0;top:1380px;bottom:0;background:linear-gradient(180deg,#d9d2c6 0%,#a39a8d 40%,#3a332c 100%)"></div>
  <div class="abs" style="left:0;right:0;top:1380px;bottom:0;background:repeating-linear-gradient(115deg,rgba(255,255,255,0) 0 90px,rgba(120,110,100,.25) 92px,rgba(255,255,255,0) 96px 180px);opacity:.7"></div>
  <div class="abs" id="b-pod" style="left:240px;top:1240px;width:600px;height:200px">
     <div class="abs" style="left:0;top:40px;width:600px;height:160px;background:linear-gradient(90deg,#9b9286,#efe9df 45%,#cfc7bb 70%,#8a8176);border-radius:0 0 300px 300px/0 0 50px 50px"></div>
     <div class="abs" style="left:0;top:0;width:600px;height:90px;border-radius:50%;background:radial-gradient(60% 60% at 45% 40%,#fffaf2,#ddd5c8 70%,#b7ae a0);background:radial-gradient(60% 60% at 45% 40%,#fffaf2,#ddd5c8 70%,#b7aea0);border:2px solid rgba(217,180,106,.8)"></div>
  </div>
  <img class="abs" id="b-b1" src="assets/img/cut_bombshell.png" style="left:290px;top:742px;height:560px;filter:drop-shadow(0 18px 24px rgba(0,0,0,.55))">
  <img class="abs" id="b-b2" src="assets/img/cut_noche.png" style="left:560px;top:742px;height:560px;filter:drop-shadow(0 18px 24px rgba(0,0,0,.55))">
  <div class="abs" id="b-glint" style="left:-300px;top:700px;width:160px;height:640px;background:linear-gradient(100deg,rgba(255,255,255,0),rgba(255,255,255,.45),rgba(255,255,255,0));transform:skewX(-16deg);mix-blend-mode:overlay"></div>
 </div>
 <div class="abs" style="left:0;right:0;top:150px" ><div class="abs center eyebrow" id="b-eb" style="top:60px;font-size:24px">Ritual mandi istimewa</div></div>
</div>''')
A('tl.fromTo("#b-world",{scale:1.0,y:40},{scale:1.13,y:-10,duration:2.4,ease:"power1.inOut"},18.1);')
A('tl.fromTo("#b-b1,#b-b2",{y:-60,opacity:0},{y:0,opacity:1,duration:.55,ease:"bounce.out",stagger:.12},18.15);')
A('tl.fromTo("#b-c1,#b-c2",{opacity:0},{opacity:1,duration:.3,stagger:.1},18.2);')
A('tl.fromTo("#b-sign",{opacity:0,scaleX:1.3},{opacity:1,scaleX:1,duration:.7,ease:"power3.out"},18.3);')
A('tl.fromTo("#b-sign span",{backgroundPosition:"100% 0"},{backgroundPosition:"0% 0",duration:1.5},18.4);')
A('tl.fromTo("#b-eb",{opacity:0},{opacity:1,duration:.4},18.6);')
A('tl.fromTo("#b-glint",{x:0},{x:1500,duration:1.0,ease:"power2.inOut"},19.1);')

# ======================= SC7 FOAM B-ROLL =======================
body.append(f'''<div {clip("foam", z=3)}>
  <video class="clip cover" id="v-palm" src="assets/video/f_palm.mp4" data-start="20.5" data-duration="0.82" data-media-start="0.1" data-track-index="2" muted playsinline></video>
  <video class="clip cover" id="v-pump" src="assets/video/f_pump.mp4" data-start="21.3" data-duration="1.42" data-media-start="0.35" data-track-index="2" muted playsinline style="z-index:2"></video>
  <div class="abs" style="inset:0;background:linear-gradient(180deg,rgba(8,5,8,.55),rgba(8,5,8,0) 30%);z-index:3"></div>
  <div class="abs" id="f-l1" style="left:90px;top:220px;z-index:4"><div class="eyebrow">Tekstur</div><div class="serif" style="font-size:118px;font-style:italic;line-height:1.05">Buih Lembut</div></div>
  <div class="abs" id="f-l2" style="left:90px;top:220px;z-index:4;opacity:0"><div class="eyebrow">Sekali tekan</div><div class="serif" style="font-size:112px;font-style:italic;line-height:1.05">Terus Berbuih</div></div>
  <div class="abs" id="f-ripa" style="left:520px;top:640px;width:40px;height:40px;margin:-20px;border-radius:50%;border:3px solid #fff;z-index:4;opacity:0"></div>
  <div class="abs" id="f-ripb" style="left:520px;top:640px;width:40px;height:40px;margin:-20px;border-radius:50%;border:3px solid var(--gold);z-index:4;opacity:0"></div>
  <div class="abs" id="f-ripc" style="left:520px;top:640px;width:40px;height:40px;margin:-20px;border-radius:50%;border:3px solid #fff;z-index:4;opacity:0"></div>
  <div class="abs" id="f-ripd" style="left:520px;top:640px;width:40px;height:40px;margin:-20px;border-radius:50%;border:3px solid var(--gold);z-index:4;opacity:0"></div>

  <div class="pill" id="f-p0" style="left:90px;top:960px;z-index:5;opacity:0"><b></b>Gentle Foaming</div>
  <div class="pill" id="f-p1" style="left:90px;top:1060px;z-index:5;opacity:0"><b></b>Ocean Salt</div>
  <div class="pill" id="f-p2" style="left:90px;top:1160px;z-index:5;opacity:0"><b></b>Aromatherapy</div>
</div>''')
A('tl.fromTo("#v-palm",{scale:1.12},{scale:1.0,duration:.82,ease:"none"},20.5);')
A('tl.fromTo("#v-pump",{scale:1.0,clipPath:"inset(0 0 0 100%)"},{scale:1.1,clipPath:"inset(0 0 0 0%)",duration:.28,ease:"power3.out"},21.3);')
A('tl.to("#v-pump",{scale:1.16,duration:1.1,ease:"none"},21.6);')
A('tl.fromTo("#f-l1",{opacity:0,x:-40},{opacity:1,x:0,duration:.3,ease:"power3.out"},20.55);')
A('tl.to("#f-l1",{opacity:0,duration:.15},21.28);')
A('tl.fromTo("#f-l2",{opacity:0,x:-40},{opacity:1,x:0,duration:.3,ease:"power3.out"},21.34);')
for k, tt in (("a", 21.32), ("c", 21.52)):
    k2 = "b" if k == "a" else "d"
    A(f'tl.fromTo("#f-rip{k}",{{opacity:1,scale:.5}},{{opacity:0,scale:7,duration:.45,ease:"power2.out"}},{tt});')
    A(f'tl.fromTo("#f-rip{k2}",{{opacity:1,scale:.5}},{{opacity:0,scale:4.5,duration:.5,ease:"power2.out"}},{tt+.05:.2f});')
for i in range(3):
    A(f'tl.fromTo("#f-p{i}",{{opacity:0,x:-80}},{{opacity:1,x:0,duration:.3,ease:"back.out(1.8)"}},{22.05+i*.15:.2f});')

# ======================= SC8 SCENTS =======================
body.append(f'''<div {clip("scent")}>
  <div class="abs" id="sc-l" style="left:0;top:0;width:540px;height:1920px;background:radial-gradient(90% 55% at 60% 45%,#5b0c1c 0%,#24060c 55%,#0b0809 100%)"></div>
  <div class="abs" id="sc-r" style="left:540px;top:0;width:540px;height:1920px;background:radial-gradient(90% 55% at 40% 45%,#2c1d6b 0%,#140d33 55%,#0b0809 100%)"></div>
  <div class="abs" id="sc-div" style="left:539px;top:420px;width:2px;height:900px;background:linear-gradient(180deg,rgba(217,180,106,0),var(--gold),rgba(217,180,106,0));transform-origin:50% 0"></div>
  <div class="abs center" id="sc-h" style="top:200px"><div class="serif" style="font-size:86px;line-height:1">2 Pilihan Wangian</div>
     <div class="eyebrow" style="margin-top:22px;letter-spacing:.7em">feminine</div></div>
  <img class="abs" id="sc-b1" src="assets/img/cut_bombshell.png" style="left:95px;top:440px;height:700px;filter:drop-shadow(0 30px 40px rgba(0,0,0,.7))">
  <img class="abs" id="sc-b2" src="assets/img/cut_noche.png" style="left:620px;top:440px;height:700px;filter:drop-shadow(0 30px 40px rgba(0,0,0,.7))">
  <div class="abs" id="sc-t1" style="left:60px;width:460px;top:1160px;text-align:center;opacity:0"><div class="eyebrow" style="font-size:22px">Woman Glory</div><div class="serif" style="font-size:78px;font-style:italic;line-height:1.1;color:#ffd0d6">Bombshell</div></div>
  <div class="abs" id="sc-t2" style="left:560px;width:460px;top:1160px;text-align:center;opacity:0"><div class="eyebrow" style="font-size:22px">Noche</div><div class="serif" style="font-size:66px;font-style:italic;line-height:1.1;color:#d9ceff">Midnight Fantasy</div></div>
  <div class="pill" id="sc-m1" style="left:560px;top:520px;opacity:0;font-size:30px"><b></b>Manis</div>
  <div class="pill" id="sc-m2" style="left:560px;top:620px;opacity:0;font-size:30px"><b style="background:#b9a6ff;box-shadow:0 0 14px #b9a6ff"></b>Misteri</div>
</div>''')
A('tl.fromTo("#sc-l",{x:-540},{x:0,duration:.45,ease:"expo.out"},22.7);tl.fromTo("#sc-r",{x:540},{x:0,duration:.45,ease:"expo.out"},22.7);')
A('tl.fromTo("#sc-div",{scaleY:0},{scaleY:1,duration:.6,ease:"power3.out"},22.85);')
A('tl.fromTo("#sc-h",{opacity:0,y:30},{opacity:1,y:0,duration:.4,ease:"power3.out"},22.8);')
A('tl.fromTo("#sc-b1",{opacity:0,y:200},{opacity:1,y:0,duration:.6,ease:"expo.out"},22.95);tl.fromTo("#sc-b2",{opacity:0,y:200},{opacity:1,y:0,duration:.6,ease:"expo.out"},23.1);')
A('tl.to("#sc-b1",{scale:1.1,x:60,duration:.4,ease:"power3.out"},24.2);tl.to("#sc-b2",{opacity:.25,filter:"blur(8px) drop-shadow(0 30px 40px rgba(0,0,0,.7))",duration:.4},24.2);')
A('tl.fromTo("#sc-t1",{opacity:0,y:30},{opacity:1,y:0,duration:.35,ease:"power3.out"},24.25);')
A('tl.to("#sc-l",{filter:"brightness(1.5)",duration:.4},24.2);')
A('tl.to("#sc-b1",{scale:.92,x:-10,opacity:.3,filter:"blur(8px) drop-shadow(0 30px 40px rgba(0,0,0,.7))",duration:.4,ease:"power3.out"},25.06);tl.to("#sc-t1",{opacity:0,duration:.25},25.06);tl.to("#sc-l",{filter:"brightness(.8)",duration:.4},25.06);')
A('tl.to("#sc-b2",{opacity:1,scale:1.1,x:-130,filter:"blur(0px) drop-shadow(0 30px 40px rgba(0,0,0,.7))",duration:.4,ease:"power3.out"},25.06);tl.to("#sc-r",{filter:"brightness(1.5)",duration:.4},25.06);')
A('tl.fromTo("#sc-t2",{opacity:0,y:30},{opacity:1,y:0,duration:.35,ease:"power3.out"},25.1);tl.to("#sc-t2",{x:-110,duration:.35},25.1);')
A('tl.fromTo("#sc-m1",{opacity:0,x:60},{opacity:1,x:150,duration:.35,ease:"back.out(2)"},25.8);')
A('tl.fromTo("#sc-m2",{opacity:0,x:60},{opacity:1,x:150,duration:.35,ease:"back.out(2)"},26.4);')

# ======================= SC9 SMILE =======================
body.append(f'''<div {clip("smile", z=3)}>
  <video class="clip cover" id="v-lather" src="assets/video/f_lather.mp4" data-start="27.0" data-duration="2.86" data-media-start="0" data-track-index="2" muted playsinline style="filter:brightness(.55) saturate(.85)"></video>
  <div class="abs" style="inset:0;background:radial-gradient(70% 45% at 50% 38%,rgba(8,5,8,.65),rgba(8,5,8,.1));z-index:2"></div>
  <div class="abs center" id="m-t" style="top:360px;z-index:3"><div class="eyebrow" style="color:var(--cham);font-size:32px">Nak isteri sentiasa</div>
    <div class="serif goldtxt" id="m-big" style="font-size:168px;font-style:italic;font-weight:700;line-height:1.1;margin-top:12px;opacity:0">tersenyum</div>
    <svg id="m-smile" viewBox="0 0 600 120" style="width:600px;height:120px;margin-top:-6px;fill:none;stroke:#e9c77e;stroke-width:6;stroke-linecap:round"><path d="M40 20 Q300 150 560 20"/></svg></div>
</div>''')
A('tl.fromTo("#v-lather",{scale:1.0},{scale:1.15,duration:2.9,ease:"none"},27.0);')
A('tl.fromTo("#m-t .eyebrow",{opacity:0,y:20},{opacity:1,y:0,duration:.4},27.15);')
A('tl.fromTo("#m-big",{opacity:0,scale:.7,filter:"blur(14px)"},{opacity:1,scale:1,filter:"blur(0px)",duration:.45,ease:"expo.out"},29.08);')
A('tl.fromTo("#m-smile path",{strokeDasharray:700,strokeDashoffset:700},{strokeDashoffset:0,duration:.55,ease:"power2.out"},29.15);')
A('tl.fromTo("#m-big",{backgroundPosition:"100% 0"},{backgroundPosition:"0% 0",duration:.8},29.2);')

# ======================= SC10 CTA / CHECKOUT =======================
body.append(f'''<div {clip("cta")}>
  <img class="cover" id="k-bg" src="assets/img/flatlay2.jpg" style="filter:brightness(.42) saturate(.95)">
  <div class="abs center" id="k-t" style="top:210px"><div class="eyebrow" style="color:var(--cham)">Mulakan dengan satu</div>
    <div class="serif" id="k-big" style="font-size:118px;font-style:italic;line-height:1.05;margin-top:16px;opacity:0">Penghargaan<br><span class="goldtxt">Kecil</span></div></div>
  <div class="abs" id="k-ui" style="left:130px;top:740px;width:820px;height:440px;border-radius:44px;background:linear-gradient(140deg,rgba(255,255,255,.14),rgba(255,255,255,.04));border:1px solid rgba(255,255,255,.25);backdrop-filter:blur(18px);box-shadow:0 40px 80px rgba(0,0,0,.5);opacity:0">
     <div class="abs" id="k-bag" style="left:60px;top:70px;width:190px;height:190px">{BAG}</div>
     <div class="abs" id="k-rip" style="left:155px;top:170px;width:60px;height:60px;margin:-30px;border-radius:50%;border:4px solid #FFD54A;opacity:0"></div>
     <div class="abs" style="left:290px;top:92px;font:800 50px/1.15 var(--sans);text-transform:uppercase">Tekan<br><span style="color:#FFD54A">beg kuning</span></div>
     <div class="abs" id="k-btn" style="left:60px;right:60px;top:300px;height:100px;border-radius:999px;background:linear-gradient(90deg,#f5b419,#ffe07a,#f5b419);color:#1b1206;font:800 44px/100px var(--sans);letter-spacing:.2em;text-align:center;box-shadow:0 10px 40px rgba(245,180,25,.45)">CHECK OUT</div>
     <div class="abs" id="k-tap" style="left:540px;top:350px;width:70px;height:70px;margin:-35px;border-radius:50%;background:rgba(255,255,255,.55);border:3px solid #fff;opacity:0"></div>
  </div>
</div>''')
A('tl.fromTo("#k-bg",{scale:1.2,y:40},{scale:1.04,y:0,duration:3.7,ease:"none"},29.9);')
A('tl.fromTo("#k-t .eyebrow",{opacity:0},{opacity:1,duration:.3},29.95);')
A('tl.fromTo("#k-big",{opacity:0,y:40,filter:"blur(10px)"},{opacity:1,y:0,filter:"blur(0px)",duration:.45,ease:"expo.out"},30.62);')
A('tl.fromTo("#k-ui",{opacity:0,y:120,rotationX:25},{opacity:1,y:0,rotationX:0,duration:.55,ease:"expo.out"},31.45);')
A('tl.fromTo("#k-bag",{scale:.4,rotation:-12},{scale:1,rotation:0,duration:.28,ease:"back.out(2.4)"},31.47);')
A('tl.to("#k-bag",{scale:.86,duration:.08},31.78);tl.to("#k-bag",{scale:1.08,duration:.18,ease:"back.out(3)"},31.86);')
A('tl.fromTo("#k-rip",{opacity:1,scale:.5},{opacity:0,scale:5,duration:.6,ease:"power2.out"},31.78);')
A('tl.fromTo("#k-tap",{opacity:0,scale:1.6},{opacity:1,scale:1,duration:.15},32.9);')
A('tl.to("#k-btn",{scale:.93,duration:.08},33.1);tl.to("#k-btn",{scale:1,duration:.25,ease:"back.out(3)"},33.18);tl.to("#k-tap",{opacity:0,scale:2.5,duration:.35},33.12);')

# ======================= SC11 STOCK / URGENCY =======================
body.append(f'''<div {clip("stock")}>
  <div class="abs" style="inset:0;background:radial-gradient(80% 60% at 50% 42%,#3a0711 0%,#140508 55%,#060304 100%)"></div>
  <div class="abs center" id="u-h" style="top:240px"><div class="eyebrow" style="letter-spacing:.6em">Stok Frescura Body</div>
     <div class="serif" style="font-size:138px;font-weight:800;line-height:1.02;margin-top:22px">Sangat<br><span class="goldtxt" style="font-style:italic;font-weight:700">Terhad</span></div></div>
  <div class="abs" style="left:130px;top:860px;width:820px">
     <div class="eyebrow" style="font-size:22px;color:var(--cham);display:flex;justify-content:space-between"><span>Baki stok</span><span id="u-lab" style="color:#ff6b7f">hampir habis</span></div>
     <div style="position:relative;margin-top:22px;height:34px;border-radius:999px;border:1px solid rgba(217,180,106,.7);overflow:hidden;background:rgba(255,255,255,.05)">
       <div id="u-bar" style="position:absolute;left:0;top:0;bottom:0;width:100%;background:linear-gradient(90deg,#ff3355,#d9b46a);transform-origin:left"></div></div>
  </div>
  <div class="abs" id="u-stamp" style="left:300px;top:1000px;width:480px;padding:18px 0;text-align:center;border:6px solid #ff3355;color:#ff3355;font:800 70px/1 var(--sans);letter-spacing:.18em;transform:rotate(-8deg);opacity:0;border-radius:14px">TERHAD</div>
  <div class="abs" id="u-seal" style="left:690px;top:520px;width:300px;height:300px;opacity:0">
     <div class="abs" id="u-star" style="inset:0;border-radius:50%;background:repeating-conic-gradient(#e9c77e 0 6deg,#b8893e 6deg 12deg);"></div>
     <div class="abs" style="inset:22px;border-radius:50%;background:radial-gradient(circle at 40% 35%,#fff1c9,#d9b46a 60%,#a87a32);display:flex;align-items:center;justify-content:center;flex-direction:column;color:#1b1206;text-align:center">
        <div style="font:800 30px/1 var(--sans);letter-spacing:.18em">ADA</div><div class="serif" style="font:italic 700 66px/1 var(--serif)">Diskaun</div></div>
  </div>
</div>''')
A('tl.fromTo("#u-h",{opacity:0,scale:1.15},{opacity:1,scale:1,duration:.45,ease:"expo.out"},33.62);')
A('tl.fromTo("#u-bar",{scaleX:1},{scaleX:.12,duration:2.0,ease:"power2.inOut"},33.85);')
A('tl.fromTo("#u-lab",{opacity:0},{opacity:1,duration:.2,repeat:3,yoyo:true},35.2);')
A('tl.fromTo("#u-stamp",{opacity:0,scale:2.4},{opacity:1,scale:1,duration:.22,ease:"power4.in"},35.86);')
A('tl.fromTo("#sc-stock",{x:0},{x:12,duration:.05,repeat:5,yoyo:true},36.08);')
A('tl.fromTo("#u-seal",{opacity:0,scale:0,rotation:-90},{opacity:1,scale:1,rotation:0,duration:.45,ease:"back.out(2)"},37.2);')
A('tl.fromTo("#u-star",{rotation:0},{rotation:40,duration:1,ease:"none"},37.2);')

# ======================= SC12 END CARD =======================
body.append(f'''<div {clip("end")}>
  <img class="abs" id="z-bg" src="assets/img/duo_dark.jpg" style="left:0;top:330px;width:1080px;height:1590px;object-fit:cover;object-position:50% 70%">
  <div class="abs" style="inset:0;background:linear-gradient(180deg,rgba(6,4,6,1) 0%,rgba(6,4,6,1) 18%,rgba(6,4,6,.2) 32%,rgba(6,4,6,0) 55%,rgba(6,4,6,.85) 100%)"></div>
  <img class="abs" id="z-logo" src="assets/img/logo.jpg" style="left:330px;top:40px;width:420px;height:420px;mix-blend-mode:screen">
  <div class="abs" id="z-cta" style="left:110px;right:110px;top:1430px;height:130px;border-radius:999px;background:linear-gradient(90deg,#f5b419,#ffe07a 50%,#f5b419);display:flex;align-items:center;justify-content:center;gap:22px;color:#1b1206;font:800 40px/1 var(--sans);letter-spacing:.06em;box-shadow:0 18px 60px rgba(245,180,25,.5)">
     <div style="width:84px;height:84px">{BAG.replace('url(#bagG)','#1b1206').replace('stroke="#1b1206" stroke-width="3"','stroke="#1b1206" stroke-width="3"').replace('id="bagG"','id="bagG2"')}</div><span>TEKAN BEG KUNING<br><span style="font-size:30px;letter-spacing:.32em">&amp; CHECK OUT</span></span></div>
  <div class="abs" id="z-tap" style="left:760px;top:1495px;width:70px;height:70px;margin:-35px;border-radius:50%;background:rgba(255,255,255,.55);border:3px solid #fff;opacity:0"></div>
</div>''')
A('tl.fromTo("#z-bg",{scale:1.0},{scale:1.1,duration:2.5,ease:"none"},37.5);')
A('tl.fromTo("#z-logo",{opacity:0,scale:.8,filter:"blur(14px)"},{opacity:1,scale:1,filter:"blur(0px)",duration:.5,ease:"expo.out"},37.6);')
A('tl.fromTo("#z-cta",{opacity:0,y:120},{opacity:1,y:0,duration:.5,ease:"back.out(1.6)"},37.55);')
A('tl.to("#z-cta",{scale:1.05,duration:.3,yoyo:true,repeat:3,ease:"sine.inOut"},38.1);')
A('tl.fromTo("#z-tap",{opacity:0,scale:1.6},{opacity:1,scale:1,duration:.15},38.8);tl.to("#z-tap",{opacity:0,scale:2.6,duration:.4},38.98);')
A('tl.to("#root-fade",{opacity:1,duration:.5},39.5);')

# ---------- global ----------
A('tl.fromTo("#grain",{x:0,y:0},{x:256,y:-256,duration:40,ease:"steps(600)"},0);')
A('tl.fromTo("#frame",{opacity:0,scale:1.03},{opacity:1,scale:1,duration:.8,ease:"power2.out"},0.2);')
A('tl.set("#capband",{opacity:0},0);tl.set("#capband",{opacity:1},5.84);tl.set("#capband",{opacity:0},16.95);tl.set("#capband",{opacity:1},18.12);tl.set("#capband",{opacity:0},37.45);')

import re
vids = []
def _pull(m):
    vids.append(m.group(0)); return ""
body = [re.sub(r'\s*<video[^>]*></video>', _pull, b) for b in body]
doc = f'''<!doctype html>
<html lang="ms" data-resolution="portrait">
<head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>{CSS.replace("__FONTS__", FONTCSS)}</style></head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
  <audio id="mix" class="clip" src="assets/audio/mix.wav" data-start="0" data-duration="{DUR}" data-track-index="9" data-volume="1"></audio>
  {"".join(bokeh)}
  {"".join(vids)}
  {"".join(body)}
  <div id="capband"></div>
  {"".join(cap_html)}
  <div id="vig"></div><div id="frame"></div><div id="flash"></div><div id="grain"></div>
  <div id="root-fade" style="position:absolute;inset:0;background:#000;opacity:0;z-index:60"></div>
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
{chr(10).join(bokeh_js)}
{flash_js}
{punch_js}
{chr(10).join(cap_js)}
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body></html>'''
open(os.path.join(PROJ, "index.html"), "w").write(doc)
print("written", len(doc), "chars;", len(cap_html), "caption chunks")
