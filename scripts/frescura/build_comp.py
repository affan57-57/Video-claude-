"""Writes the HyperFrames composition (index.html) for the Frescura Body 'hadiah kecil' ad.
Usage: python build_comp.py PROJECT_DIR [--preview]"""
import sys, json, html

PROJ = sys.argv[1]
PREVIEW = "--preview" in sys.argv
TOTAL = 34.0

# ---------- captions: (start, end, text) ; *word* = luxe highlight ----------
CAPS = [
    (0.00, 1.24, "Dulu masa *bercinta*,"),
    (1.28, 2.84, "bukan main lagi kita *berusaha*"),
    (2.86, 4.02, "nak buat dia *tersenyum*."),
    (4.08, 5.48, "Bila kita dah *kahwin*,"),
    (5.52, 6.44, "jangan sampai *lupa*"),
    (6.46, 7.46, "perkara *kecil*"),
    (7.48, 8.86, "yang pernah buat dia *bahagia*."),
    (8.90, 9.78, "Abang, apa kata"),
    (9.80, 10.64, "*hidupkan* semula"),
    (10.66, 11.82, "rasa *dihargai* itu"),
    (11.84, 13.10, "dengan *hadiah* *kecil*"),
    (13.12, 14.70, "untuk isteri abang."),
    (14.74, 15.52, "*Foaming* body shower"),
    (15.54, 16.62, "daripada *Frescura* *Body*"),
    (16.64, 17.68, "ini ada pakai perfume"),
    (17.70, 18.58, "*Bombshell*, abang."),
    (18.62, 19.26, "Bayangkan mandi"),
    (19.28, 20.40, "pakai perfume *Bombshell*"),
    (20.42, 22.30, "dan dia juga ada bau"),
    (22.32, 23.32, "*Midnight* *Fantasy*."),
    (23.36, 24.66, "Buat dia rasa *istimewa*,"),
    (24.68, 26.30, "walaupun dah *bertahun-tahun*"),
    (26.32, 27.38, "kita bersama dengan dia."),
    (27.40, 28.96, "*Stok* sangat-sangat *terhad*"),
    (28.98, 29.78, "tekan *beg* *kuning* sekarang"),
    (29.80, 31.10, "& *checkout* sekarang!"),
]

def cap_html():
    out = []
    for i, (s, e, t) in enumerate(CAPS):
        words = []
        for w in t.split():
            hl = w.startswith("*")
            core = w.strip("*") if hl else w
            # keep punctuation after closing star
            if hl and "*" in w[1:]:
                core, tail = w[1:].split("*", 1)
                core = core + tail
            cls = "w hl" if hl else "w"
            words.append(f'<span class="{cls}">{html.escape(core)}</span>')
        out.append(f'<div class="cap clip" id="cap{i}" data-start="{s}" data-duration="{e - s + 0.04:.2f}" data-track-index="20">'
                   f'<div class="capin">{" ".join(words)}</div></div>')
    return "\n".join(out)

CAP_JSON = json.dumps([[s, e] for s, e, _ in CAPS])

# scene timings
S = dict(hook=(0, 4.05), rings=(4.05, 8.86), gift=(8.86, 14.70), mall=(14.70, 16.64), pump=(16.64, 18.60),
         glory=(18.60, 20.42), noche=(20.42, 23.34), hold=(23.34, 24.68), years=(24.68, 26.30),
         flat=(26.30, 27.40), cta=(27.40, 31.06), outro=(31.06, TOTAL))
def a(k): s, e = S[k]; return f'data-start="{s}" data-duration="{e - s:.2f}"'

HTML = f"""<!doctype html>
<html lang="ms" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
@font-face{{font-family:"Bodoni";src:url(assets/fonts/bodoni-moda-latin-500-normal.woff2) format("woff2");font-weight:500}}
@font-face{{font-family:"Bodoni";src:url(assets/fonts/bodoni-moda-latin-600-normal.woff2) format("woff2");font-weight:600}}
@font-face{{font-family:"Bodoni";src:url(assets/fonts/bodoni-moda-latin-500-italic.woff2) format("woff2");font-weight:500;font-style:italic}}
@font-face{{font-family:"Bodoni";src:url(assets/fonts/bodoni-moda-latin-400-italic.woff2) format("woff2");font-weight:400;font-style:italic}}
@font-face{{font-family:"Jost";src:url(assets/fonts/jost-latin-300-normal.woff2) format("woff2");font-weight:300}}
@font-face{{font-family:"Jost";src:url(assets/fonts/jost-latin-400-normal.woff2) format("woff2");font-weight:400}}
@font-face{{font-family:"Jost";src:url(assets/fonts/jost-latin-500-normal.woff2) format("woff2");font-weight:500}}
@font-face{{font-family:"Jost";src:url(assets/fonts/jost-latin-600-normal.woff2) format("woff2");font-weight:600}}
:root{{--noir:#0b0908;--ink:#f6f0e6;--champ:#d9b878;--champ2:#f3dfb4;--rose:#a3142a;--violet:#7b5cff;
  --gold:linear-gradient(100deg,#b8893f 0%,#f6e2b3 38%,#d4ab62 60%,#fff1cf 78%,#b8893f 100%)}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:var(--noir)}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:var(--noir);font-family:"Jost",sans-serif;color:var(--ink)}}
.clip{{position:absolute;inset:0}}
.scene{{overflow:hidden}}
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.abs{{position:absolute}}
.center{{left:0;right:0;text-align:center}}
.kicker{{font:400 30px/1 "Jost";letter-spacing:.42em;text-transform:uppercase;color:var(--champ2)}}
.serif{{font-family:"Bodoni";font-weight:500}}
.it{{font-family:"Bodoni";font-style:italic;font-weight:500}}
.goldtx{{background:var(--gold);background-size:220% 100%;-webkit-background-clip:text;background-clip:text;color:transparent}}
.line{{display:block;overflow:hidden;padding:0 0 .08em}}
.line>span{{display:inline-block}}
.hair{{position:absolute;height:2px;background:linear-gradient(90deg,transparent,var(--champ),transparent)}}
.chip{{position:absolute;left:50%;transform:translateX(-50%);padding:22px 40px;border:1.5px solid rgba(217,184,120,.55);border-radius:999px;
  font:500 36px/1 "Jost";letter-spacing:.08em;color:var(--ink);background:rgba(20,16,12,.55);backdrop-filter:blur(8px);white-space:nowrap}}
.chip b{{font-weight:600;color:var(--champ2)}}
.vign{{position:absolute;inset:0;background:radial-gradient(120% 80% at 50% 45%,transparent 45%,rgba(0,0,0,.78) 100%);pointer-events:none}}
/* captions */
.cap{{z-index:50;top:1395px;bottom:auto;height:260px;display:flex;align-items:center;justify-content:center;pointer-events:none}}
.capin{{max-width:960px;text-align:center;font:600 66px/1.16 "Jost";letter-spacing:.01em;color:#fffaf2;
  text-shadow:0 3px 0 rgba(0,0,0,.25),0 8px 34px rgba(0,0,0,.65)}}
.capin .w{{display:inline-block;margin:0 .06em}}
.capin .hl{{font-family:"Bodoni";font-style:italic;font-weight:500;font-size:1.32em;line-height:.9;letter-spacing:0;
  background:var(--gold);background-size:220% 100%;-webkit-background-clip:text;background-clip:text;color:transparent;
  filter:drop-shadow(0 6px 22px rgba(0,0,0,.7));padding:0 .04em}}
/* overlays */
#stripes{{position:absolute;inset:-40%;z-index:60;pointer-events:none;opacity:0;visibility:hidden;
  background:repeating-linear-gradient(118deg,rgba(255,236,200,0) 0 70px,rgba(255,236,200,.85) 70px 120px,rgba(255,236,200,0) 120px 210px);mix-blend-mode:screen;filter:blur(6px)}}
#flash{{position:absolute;inset:0;z-index:61;background:#fff6e6;opacity:0;visibility:hidden;pointer-events:none}}
#grain{{position:absolute;inset:-100px;z-index:70;background:url(assets/img/grain.png);opacity:.07;mix-blend-mode:overlay;pointer-events:none}}
#prog{{position:absolute;left:0;top:0;height:6px;width:1080px;z-index:72;transform-origin:0 50%;background:var(--gold)}}
#wm{{position:absolute;right:34px;top:40px;z-index:80;font:500 22px/1 "Jost";letter-spacing:.35em;color:rgba(255,255,255,.55);border:1px solid rgba(255,255,255,.35);padding:10px 14px}}
/* hook */
#hook .bg{{position:absolute;inset:-60px;background:url(assets/img/roses.jpg) center/cover;filter:blur(30px) brightness(.36) saturate(1.25)}}
#smile{{position:absolute;left:290px;top:930px;width:500px;height:160px}}
/* rings */
#rings .bg{{position:absolute;inset:0;background:radial-gradient(70% 50% at 50% 38%,#2a1f16 0%,#0b0908 70%)}}
.tl-dot{{position:absolute;width:26px;height:26px;border-radius:50%;background:var(--champ);box-shadow:0 0 24px var(--champ)}}
.tl-lbl{{position:absolute;font:500 28px/1 "Jost";letter-spacing:.3em;color:var(--champ2);transform:translateX(-50%)}}
/* gift */
#gift .bg{{position:absolute;inset:-60px;background:url(assets/img/flatlay_diag.jpg) center/cover;filter:blur(18px) brightness(.38)}}
#box{{position:absolute;left:290px;top:820px;width:500px;height:420px}}
#box .base{{position:absolute;left:0;bottom:0;width:500px;height:360px;background:linear-gradient(180deg,#f3ece2,#d9cfc2);border-radius:6px;box-shadow:0 40px 80px rgba(0,0,0,.55)}}
#box .rib{{position:absolute;left:225px;width:50px;top:0;bottom:0;background:var(--gold)}}
#box .lid{{position:absolute;left:-20px;top:0;width:540px;height:90px;background:linear-gradient(180deg,#fbf6ef,#e4dacd);border-radius:6px;transform-origin:20% 100%;box-shadow:0 14px 30px rgba(0,0,0,.35)}}
#box .bow{{position:absolute;left:190px;top:-70px;width:160px;height:80px}}
#rays{{position:absolute;left:-460px;top:-260px;width:2000px;height:2000px;border-radius:50%;opacity:0;
  background:repeating-conic-gradient(from 0deg,rgba(255,226,170,.28) 0 6deg,transparent 6deg 18deg);mask:radial-gradient(circle,#000 10%,transparent 60%);-webkit-mask:radial-gradient(circle,#000 10%,transparent 60%)}}
#giftprod{{position:absolute;left:340px;top:560px;width:400px;opacity:0;filter:drop-shadow(0 30px 40px rgba(0,0,0,.6))}}
/* mall boutique */
#mall .wall{{position:absolute;inset:0;background:
  linear-gradient(180deg,rgba(0,0,0,.0) 0%,rgba(0,0,0,.55) 100%),
  repeating-linear-gradient(90deg,#1b1612 0 46px,#251e18 46px 52px,#16120f 52px 98px);}}
#mall .arch{{position:absolute;left:140px;top:150px;width:800px;height:1180px;border-radius:400px 400px 0 0;
  background:radial-gradient(80% 60% at 50% 30%,#3a2d21 0%,#17120e 75%);box-shadow:inset 0 0 0 3px rgba(217,184,120,.55),inset 0 0 120px rgba(0,0,0,.8)}}
#mall .logo{{position:absolute;left:290px;top:250px;width:500px;mix-blend-mode:screen;filter:saturate(1.2)}}
#mall .floor{{position:absolute;left:0;right:0;top:1330px;bottom:0;background:linear-gradient(180deg,#2a221b 0%,#0e0b09 100%)}}
#mall .pod{{position:absolute;left:250px;top:1200px;width:580px;height:170px}}
#mall .pod .top{{position:absolute;left:0;top:0;width:580px;height:90px;border-radius:50%;background:radial-gradient(60% 70% at 45% 35%,#fffaf1,#d8cdbd 60%,#a69886)}}
#mall .pod .side{{position:absolute;left:0;top:45px;width:580px;height:125px;border-radius:0 0 290px 290px/0 0 45px 45px;background:linear-gradient(90deg,#8d8070,#efe6d8 45%,#b9ad9c 70%,#7a6e60)}}
#mall .prod{{position:absolute;left:300px;top:590px;width:480px;filter:drop-shadow(0 30px 30px rgba(0,0,0,.55))}}
#mall .refl{{position:absolute;left:300px;top:1380px;width:480px;transform:scaleY(-1);opacity:.18;filter:blur(3px);
  -webkit-mask:linear-gradient(0deg,#000 0%,transparent 40%);mask:linear-gradient(0deg,#000 0%,transparent 40%)}}
.beam{{position:absolute;top:-80px;width:360px;height:1500px;background:linear-gradient(180deg,rgba(255,232,190,.55),rgba(255,232,190,0) 85%);
  clip-path:polygon(42% 0,58% 0,100% 100%,0 100%);filter:blur(16px);mix-blend-mode:screen;transform-origin:50% 0}}
#glass{{position:absolute;left:-400px;top:0;width:260px;height:1920px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.16),transparent);transform:skewX(-16deg)}}
/* pump */
.callout{{position:absolute;font:500 34px/1.2 "Jost";letter-spacing:.14em;text-transform:uppercase;color:#fff;text-shadow:0 4px 20px rgba(0,0,0,.8)}}
.callout small{{display:block;font:400 26px/1.3 "Jost";letter-spacing:.2em;color:var(--champ2)}}
.ring{{position:absolute;border:2.5px solid var(--champ2);border-radius:50%;box-shadow:0 0 30px rgba(243,223,180,.6)}}
#bomb{{position:absolute;left:0;right:0;top:250px;text-align:center;font:italic 500 170px/1 "Bodoni";opacity:0}}
/* bottle heroes */
.hero .bg{{position:absolute;inset:0}}
.hero .bottle{{position:absolute;left:330px;top:300px;height:1080px;filter:drop-shadow(0 50px 60px rgba(0,0,0,.7))}}
.spec{{position:absolute;left:70px;top:140px;right:70px}}
.spec .t1{{font:400 30px/1 "Jost";letter-spacing:.42em;color:var(--champ2)}}
.spec .t2{{font:500 118px/1 "Bodoni";margin-top:22px}}
.spec .t3{{font:italic 500 64px/1 "Bodoni";margin-top:8px}}
.notes{{position:absolute;top:640px;font:500 30px/1 "Jost";letter-spacing:.22em;text-transform:uppercase}}
.notes div{{display:flex;align-items:center;gap:16px;margin-bottom:34px;white-space:nowrap}}
.notes i{{display:inline-block;width:54px;height:2px;background:var(--champ)}}
.star{{position:absolute;width:4px;height:4px;border-radius:50%;background:#fff;box-shadow:0 0 10px #cbbcff}}
/* years */
#yr{{position:absolute;left:0;right:0;top:300px;text-align:center}}
#yr .num{{font:500 300px/1 "Bodoni";height:300px;overflow:hidden;position:relative}}
#yr .roll{{position:absolute;left:0;right:0;top:0}}
#yr .roll div{{height:300px}}
/* cta */
#cta .bg{{position:absolute;inset:-60px;background:url(assets/img/duo.jpg) center/cover;filter:blur(22px) brightness(.32)}}
#meter{{position:absolute;left:140px;top:820px;width:800px}}
#meter .track{{height:22px;border-radius:99px;background:rgba(255,255,255,.12);overflow:hidden;border:1px solid rgba(255,255,255,.18)}}
#meter .fill{{height:100%;width:100%;border-radius:99px;background:linear-gradient(90deg,#e0384e,#ffb36b);transform-origin:0 50%}}
#meter .lab{{display:flex;justify-content:space-between;font:500 30px/1 "Jost";letter-spacing:.24em;margin-bottom:22px;color:var(--champ2)}}
#bag{{position:absolute;left:420px;top:1040px;width:240px;height:240px}}
#tap{{position:absolute;left:500px;top:1120px;width:80px;height:80px;border-radius:50%;border:4px solid #fff;opacity:0}}
#btn{{position:absolute;left:190px;top:1690px;width:700px;height:120px;border-radius:999px;background:var(--gold);background-size:200% 100%;
  display:flex;align-items:center;justify-content:center;font:600 44px/1 "Jost";letter-spacing:.2em;color:#1a120a;box-shadow:0 20px 60px rgba(217,184,120,.35)}}
/* outro */
#outro .bg{{position:absolute;inset:0;background:radial-gradient(60% 40% at 50% 40%,#1a1a2e 0%,#050507 70%)}}
#outro .logo{{position:absolute;left:140px;top:170px;width:800px;mix-blend-mode:screen}}
#outro .prod{{position:absolute;left:330px;top:860px;width:420px;filter:drop-shadow(0 40px 50px rgba(0,0,0,.7))}}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">

<audio id="mix" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="30" data-volume="1" src="assets/final_mix.wav"></audio>

<!-- 1 HOOK -->
<div id="hook" class="clip scene" {a('hook')} data-track-index="1">
  <div class="bg"></div><div class="vign"></div>
  <div class="abs center kicker" style="top:300px" id="hk0">Pesanan untuk abang</div>
  <div class="abs center" style="top:400px">
    <span class="line"><span id="hk1" style="font:500 60px/1.1 Jost;letter-spacing:.12em;text-transform:uppercase">Bila kali terakhir</span></span>
    <span class="line"><span id="hk2" class="it goldtx" style="font-size:150px;line-height:1.1">dia senyum</span></span>
    <span class="line"><span id="hk3" class="serif" style="font-size:112px;line-height:1.1">kerana abang?</span></span>
  </div>
  <svg id="smile" viewBox="0 0 500 160"><path id="smilep" d="M30 30 Q250 200 470 30" fill="none" stroke="url(#gg)" stroke-width="9" stroke-linecap="round"/>
   <defs><linearGradient id="gg"><stop offset="0" stop-color="#b8893f"/><stop offset=".5" stop-color="#fff1cf"/><stop offset="1" stop-color="#b8893f"/></linearGradient></defs></svg>
</div>

<!-- 2 RINGS / TIMELINE / FORMULA -->
<div id="rings" class="clip scene" {a('rings')} data-track-index="1">
  <div class="bg"></div>
  <svg id="ringsvg" class="abs" style="left:290px;top:250px" width="500" height="330" viewBox="0 0 500 330">
    <circle id="r1" cx="185" cy="165" r="130" fill="none" stroke="#d9b878" stroke-width="7"/>
    <circle id="r2" cx="315" cy="165" r="130" fill="none" stroke="#f3dfb4" stroke-width="7"/>
  </svg>
  <div id="tl" class="abs" style="left:0;top:700px;width:1080px;height:120px">
    <div class="hair" id="tlline" style="left:120px;width:840px;top:30px;transform-origin:0 50%"></div>
    <div class="tl-dot" id="td1" style="left:167px;top:18px"></div><div class="tl-lbl" id="tl1" style="left:180px;top:80px">Bercinta</div>
    <div class="tl-dot" id="td2" style="left:527px;top:18px"></div><div class="tl-lbl" id="tl2" style="left:540px;top:80px">Kahwin</div>
    <div class="tl-dot" id="td3" style="left:887px;top:18px"></div><div class="tl-lbl" id="tl3" style="left:900px;top:80px">Sekarang</div>
  </div>
  <div class="abs center kicker" id="fk" style="top:900px">Formula bahagia</div>
  <div class="chip" id="c1" style="top:975px">Ucapan <b>terima kasih</b></div>
  <div class="chip" id="c2" style="top:1080px">Pelukan <b>selepas kerja</b></div>
  <div class="chip" id="c3" style="top:1185px">Hadiah <b>kecil</b></div>
  <div class="abs center it goldtx" id="feq" style="top:1290px;font-size:84px;opacity:0">= bahagia</div>
</div>

<!-- 3 GIFT -->
<div id="gift" class="clip scene" {a('gift')} data-track-index="1">
  <div class="bg"></div><div class="vign"></div>
  <div class="abs center" style="top:230px">
    <div class="kicker" id="gk">Hidupkan semula</div>
    <span class="line" style="margin-top:26px"><span id="g1" class="serif" style="font-size:104px">rasa</span></span>
    <span class="line"><span id="g2" class="it goldtx" style="font-size:180px;line-height:1">dihargai.</span></span>
  </div>
  <div id="rays"></div>
  <img id="giftprod" src="assets/img/duo_cut.png" />
  <div id="box">
    <div class="base"><div class="rib"></div></div>
    <div class="lid"><div class="rib" style="left:245px"></div>
      <svg class="bow" viewBox="0 0 160 80"><path d="M80 70 C40 0 0 20 20 60 Z M80 70 C120 0 160 20 140 60 Z" fill="#e2bd7a" stroke="#b8893f" stroke-width="3"/></svg></div>
  </div>
  <div class="abs center kicker" id="gk2" style="top:1290px;opacity:0">Hadiah kecil · makna besar</div>
</div>

<!-- 4a LUXURY MALL BOUTIQUE -->
<div id="mall" class="clip scene" {a('mall')} data-track-index="1">
  <div id="mallcam" class="abs" style="inset:0;transform-origin:50% 60%">
    <div class="wall"></div>
    <div class="arch"></div>
    <img class="logo" src="assets/img/logo.jpg" />
    <div class="floor"></div>
    <div class="beam" id="bm1" style="left:180px;transform:rotate(9deg)"></div>
    <div class="beam" id="bm2" style="left:540px;transform:rotate(-9deg)"></div>
    <div class="pod"><div class="side"></div><div class="top"></div></div>
    <img class="refl" src="assets/img/duo_cut.png" />
    <img class="prod" id="mallprod" src="assets/img/duo_cut.png" />
    <div id="glass"></div>
  </div>
  <div class="vign"></div>
  <div class="abs center kicker" id="mk" style="top:120px">The Signature Collection</div>
</div>

<!-- 4b PUMP FOAM (real footage) -->
<video data-track-index="2" class="full" id="vpump" src="assets/clips/pump_palm.mp4" muted playsinline data-start="{S['pump'][0]}" data-duration="{S['pump'][1]-S['pump'][0]:.2f}" data-media-start="0.2"></video>
<div id="pump" class="clip scene" {a('pump')} data-track-index="1">
  <div class="vign"></div>
  <div class="ring" id="pr" style="left:250px;top:640px;width:420px;height:420px;opacity:0"></div>
  <div class="hair" id="pl" style="left:600px;top:760px;width:300px;transform-origin:0 50%"></div>
  <div class="callout" id="pc" style="left:620px;top:690px;opacity:0">Busa siap<small>terus dari pump</small></div>
  <div class="callout" id="pc2" style="left:80px;top:1180px;opacity:0">Tak perlu loofah<small>gentle foaming</small></div>
  <div id="bomb" class="goldtx">Bombshell</div>
</div>

<!-- 5a WOMAN GLORY -->
<div id="glory" class="clip scene hero" {a('glory')} data-track-index="1">
  <div class="bg" style="background:radial-gradient(70% 55% at 60% 45%,#5a0b18 0%,#1a0507 70%,#0b0303 100%)"></div>
  <div class="bg" style="background:url(assets/img/roses.jpg) center/cover;opacity:.12;filter:blur(6px)"></div>
  <img class="bottle" id="gb" src="assets/img/red_cut.png" style="left:560px;top:330px;height:1000px" />
  <div class="spec"><div class="t1" id="gs1">Woman Glory</div><div class="t2 goldtx" id="gs2" style="font-size:132px">Bomb-</div><div class="t2 goldtx" id="gs2b" style="font-size:132px;margin-top:0">shell</div><div class="t3" id="gs3">inspired scent</div></div>
  <div class="notes" style="left:70px" id="gn"><div><i></i>Aromatherapy</div><div><i></i>Ocean salt</div><div><i></i>Gentle foaming</div><div><i></i>500 ml</div></div>
</div>

<!-- 5b NOCHE -->
<div id="noche" class="clip scene hero" {a('noche')} data-track-index="1">
  <div class="bg" style="background:url(assets/img/night.jpg) center/cover;filter:blur(10px) brightness(.45) saturate(1.3)"></div>
  <div class="bg" style="background:radial-gradient(70% 55% at 40% 45%,rgba(91,63,209,.35) 0%,rgba(5,4,15,.85) 75%)"></div>
  <div id="stars" class="abs" style="inset:0"></div>
  <img class="bottle" id="nb" src="assets/img/noche_cut.png" style="left:150px;top:330px;height:1000px" />
  <div class="spec" style="text-align:right"><div class="t1" id="ns1">Noche</div><div class="t2" id="ns2" style="font-size:120px;color:#e9e3ff">Midnight</div><div class="t3 goldtx" id="ns3" style="font-size:96px">Fantasy</div></div>
  <div class="notes" style="right:70px;text-align:right" id="nn"><div style="justify-content:flex-end">Ocean salt<i></i></div><div style="justify-content:flex-end">Aromatherapy<i></i></div><div style="justify-content:flex-end">Soft · fragrant<i></i></div></div>
</div>

<!-- 6a FOAM HOLD -->
<video data-track-index="2" class="full" id="vhold" src="assets/clips/foam_hold.mp4" muted playsinline data-start="{S['hold'][0]}" data-duration="{S['hold'][1]-S['hold'][0]:.2f}" data-media-start="0.3"></video>
<div id="hold" class="clip scene" {a('hold')} data-track-index="1">
  <div class="vign"></div>
  <div class="abs center" style="top:230px"><div class="kicker" id="hk">Buat dia rasa</div>
  <span class="line" style="margin-top:14px"><span id="h1" class="it goldtx" style="font-size:170px">istimewa.</span></span></div>
</div>

<!-- 6b YEARS -->
<video data-track-index="2" class="full" id="vlather" src="assets/clips/lather.mp4" muted playsinline data-start="{S['years'][0]}" data-duration="{S['years'][1]-S['years'][0]:.2f}" data-media-start="0.2" style="filter:brightness(.55) saturate(.9)"></video>
<div id="years" class="clip scene" {a('years')} data-track-index="1">
  <div class="vign"></div>
  <div id="yr"><div class="kicker">Walaupun dah</div>
    <div class="num goldtx"><div class="roll" id="roll"><div>1</div><div>3</div><div>5</div><div>7</div><div>10+</div></div></div>
    <div class="serif" style="font-size:76px;margin-top:10px">tahun bersama</div></div>
</div>

<!-- 6c FLATLAY -->
<div id="flat" class="clip scene" {a('flat')} data-track-index="1">
  <img class="full" id="fimg" src="assets/img/flatlay_diag.jpg" style="transform-origin:60% 40%" />
  <div class="vign"></div><div class="abs" style="inset:0;background:linear-gradient(180deg,rgba(10,6,3,.72) 0%,rgba(10,6,3,0) 32%,rgba(10,6,3,0) 62%,rgba(10,6,3,.6) 82%)"></div>
  <div class="abs center" style="top:200px"><span class="line"><span id="f1" class="it" style="font-size:96px;color:#fff;text-shadow:0 8px 30px rgba(0,0,0,.6)">setiap hari,</span></span>
  <span class="line"><span id="f2" class="it goldtx" style="font-size:96px">setiap mandi.</span></span></div>
</div>

<!-- 7 CTA -->
<div id="cta" class="clip scene" {a('cta')} data-track-index="1">
  <div class="bg"></div><div class="vign"></div>
  <div class="abs center" style="top:220px">
    <span class="line"><span id="k1" class="serif goldtx" style="font-size:230px;line-height:1">Stok</span></span>
    <span class="line"><span id="k2" style="font:500 54px/1.2 Jost;letter-spacing:.3em;text-transform:uppercase">sangat-sangat terhad</span></span>
  </div>
  <div id="meter"><div class="lab"><span>Baki stok</span><span id="pct">100%</span></div><div class="track"><div class="fill" id="fill"></div></div></div>
  <svg id="bag" viewBox="0 0 240 240">
    <path d="M70 90 V70 a50 50 0 0 1 100 0 V90" fill="none" stroke="#1a120a" stroke-width="12" stroke-linecap="round"/>
    <rect x="30" y="85" width="180" height="140" rx="22" fill="#FFC531"/>
    <path d="M70 90 V70 a50 50 0 0 1 100 0 V90" fill="none" stroke="#FFC531" stroke-width="10" stroke-linecap="round" transform="translate(0,-2)"/>
    <circle cx="70" cy="112" r="8" fill="#1a120a"/><circle cx="170" cy="112" r="8" fill="#1a120a"/>
  </svg>
  <div id="tap"></div>
  <div id="btn">CHECKOUT SEKARANG</div>
</div>

<!-- 8 OUTRO -->
<div id="outro" class="clip scene" {a('outro')} data-track-index="1">
  <div class="bg"></div>
  <img class="logo" id="ol" src="assets/img/logo.jpg" />
  <img class="prod" id="op" src="assets/img/duo_cut.png" />
  <div class="abs center kicker" id="ok" style="top:1700px">Tekan beg kuning · sekarang</div>
</div>

{cap_html()}

<div id="stripes"></div><div id="flash"></div><div id="grain"></div><div id="prog"></div>
{'<div id="wm">PREVIEW</div>' if PREVIEW else ''}
</div>

<script>
const tl = gsap.timeline({{ paused: true }});
const CAPS = {CAP_JSON};
const E = "power3.out", EI = "expo.out";
// ---- global
tl.set(["#flash","#stripes"],{{autoAlpha:0}},0);
tl.fromTo("#prog", {{scaleX:0}}, {{scaleX:1, duration:{TOTAL}, ease:"none"}}, 0);
tl.fromTo("#grain", {{x:0,y:0}}, {{x:-60,y:40, duration:{TOTAL}, ease:"steps(160)"}}, 0);
function stripes(t){{ tl.fromTo("#stripes",{{autoAlpha:0,x:-500}},{{autoAlpha:1,x:0,duration:.22,ease:"power2.in",immediateRender:false}},t-.22)
  .fromTo("#stripes",{{autoAlpha:1,x:0}},{{autoAlpha:0,x:500,duration:.3,ease:"power2.out",immediateRender:false}},t); }}
function flash(t,o=.85){{ tl.fromTo("#flash",{{autoAlpha:o}},{{autoAlpha:0,duration:.35,ease:"power2.out",immediateRender:false}},t); }}
function sceneIn(sel,t,from){{ tl.fromTo(sel, from||{{scale:1.08,filter:"blur(14px)",opacity:0}}, {{scale:1,filter:"blur(0px)",opacity:1,duration:.5,ease:EI}}, t); }}
function lineUp(sel,t,d=.7){{ tl.fromTo(sel,{{yPercent:110,opacity:0}},{{yPercent:0,opacity:1,duration:d,ease:EI}},t); }}
// ---- captions: words rise in with blur, gold shimmer on highlights
CAPS.forEach(([s,e],i)=>{{
  const ws = document.querySelectorAll("#cap"+i+" .w"); const n = ws.length; const span = Math.min((e-s)*0.72, n*0.16);
  ws.forEach((w,j)=>{{ const t = s + (n>1? span*j/(n-1):0);
    tl.fromTo(w,{{y:46,opacity:0,filter:"blur(10px)",scale:.92}},{{y:0,opacity:1,filter:"blur(0px)",scale:1,duration:.34,ease:"back.out(1.6)"}},t);
    if(w.classList.contains("hl")) tl.fromTo(w,{{backgroundPosition:"100% 0"}},{{backgroundPosition:"0% 0",duration:.9,ease:"power2.out"}},t);
  }});
  tl.to("#cap"+i+" .capin",{{opacity:0,y:-18,duration:.12,ease:"power1.in"}},e-.1);
}});
// ---- 1 hook
tl.fromTo("#hook .bg",{{scale:1.25}},{{scale:1.02,duration:4.1,ease:"none"}},0);
flash(0,1);
tl.fromTo("#hk0",{{opacity:0,scale:1.18}},{{opacity:1,scale:1,duration:.8,ease:E}},0.05);
lineUp("#hk1",0.08); lineUp("#hk2",0.22,.8); lineUp("#hk3",0.4,.8);
tl.fromTo("#hk2",{{backgroundPosition:"100% 0"}},{{backgroundPosition:"0% 0",duration:2.5,ease:"none"}},0.3);
tl.set("#smilep",{{strokeDasharray:620,strokeDashoffset:620}},0).to("#smilep",{{strokeDashoffset:0,duration:.8,ease:"power2.inOut"}},2.86);
tl.to("#hook .abs, #hook svg",{{scale:1.06,opacity:.0,filter:"blur(10px)",duration:.3,ease:"power2.in"}},3.78);
stripes(4.05);
// ---- 2 rings
sceneIn("#rings .bg",4.05,{{opacity:0}});
tl.set(["#r1","#r2"],{{strokeDasharray:820,strokeDashoffset:820}},4.0);
tl.to("#r1",{{strokeDashoffset:0,duration:.9,ease:"power2.inOut"}},4.1).to("#r2",{{strokeDashoffset:0,duration:.9,ease:"power2.inOut"}},4.3);
tl.fromTo("#ringsvg",{{rotation:-12,scale:.86}},{{rotation:0,scale:1,duration:1.6,ease:E}},4.1);
tl.fromTo("#tlline",{{scaleX:0}},{{scaleX:1,duration:1.3,ease:"power2.inOut"}},4.45);
[["#td1","#tl1",4.5],["#td2","#tl2",4.9],["#td3","#tl3",5.6]].forEach(([d,l,t])=>{{tl.fromTo(d,{{scale:0}},{{scale:1,duration:.4,ease:"back.out(3)"}},t).fromTo(l,{{opacity:0,y:20}},{{opacity:1,y:0,duration:.4,ease:E}},t+.05);}});
tl.to("#td3",{{opacity:.25,scale:.6,duration:.4}},5.9).to("#tl3",{{opacity:.35,duration:.4}},5.9);
tl.fromTo("#fk",{{opacity:0}},{{opacity:1,duration:.4}},6.4);
[["#c1",6.46],["#c2",6.9],["#c3",7.3]].forEach(([c,t])=>tl.fromTo(c,{{opacity:0,y:40,scale:.9}},{{opacity:1,y:0,scale:1,duration:.45,ease:"back.out(2)"}},t));
tl.fromTo("#feq",{{opacity:0,scale:1.4,filter:"blur(12px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:.5,ease:EI}},8.15);
tl.fromTo("#feq",{{backgroundPosition:"100% 0"}},{{backgroundPosition:"0% 0",duration:.8}},8.2);
stripes(8.86);
// ---- 3 gift
tl.fromTo("#gift .bg",{{scale:1.2}},{{scale:1.0,duration:5.9,ease:"none"}},8.86);
tl.fromTo("#gk",{{opacity:0,scale:1.18}},{{opacity:1,scale:1,duration:.7,ease:E}},9.0);
lineUp("#g1",9.7); lineUp("#g2",10.66,.8);
tl.fromTo("#g2",{{backgroundPosition:"100% 0"}},{{backgroundPosition:"0% 0",duration:1.2}},10.8);
tl.fromTo("#box",{{y:700,rotation:6}},{{y:0,rotation:0,duration:.9,ease:"back.out(1.3)"}},9.3);
tl.to("#box .lid",{{keyframes:[{{rotation:-4,duration:.08}},{{rotation:3,duration:.08}},{{rotation:-2,duration:.08}},{{rotation:0,duration:.08}}]}},11.5);
tl.to("#box .lid",{{y:-260,x:-60,rotation:-28,opacity:0,duration:.7,ease:"power3.out"}},12.42);
tl.to("#rays",{{opacity:1,duration:.4}},12.42).fromTo("#rays",{{rotation:0}},{{rotation:40,duration:2.4,ease:"none"}},12.42);
flash(12.42,.6);
tl.fromTo("#giftprod",{{opacity:0,y:420,scale:.6}},{{opacity:1,y:0,scale:1,duration:.9,ease:"back.out(1.4)"}},12.5);
tl.to("#box",{{y:260,opacity:.0,duration:.7,ease:"power2.in"}},12.9);
tl.to(["#gk","#g1","#g2"],{{opacity:.0,y:-30,duration:.4}},12.5);
tl.fromTo("#giftprod",{{y:0}},{{y:-40,duration:1.2,ease:"sine.inOut"}},13.45);
tl.fromTo("#gk2",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.5}},13.1);
stripes(14.70);
// ---- 4a mall
tl.fromTo("#mallcam",{{scale:1.28,y:120}},{{scale:1.0,y:0,duration:1.95,ease:"power2.out"}},14.70);
tl.fromTo(["#bm1","#bm2"],{{opacity:0,scaleY:.3}},{{opacity:1,scaleY:1,duration:.5,stagger:.12,ease:E}},14.75);
tl.fromTo("#mall .logo",{{opacity:0,filter:"brightness(3) blur(8px)"}},{{opacity:1,filter:"brightness(1) blur(0px)",duration:.6,ease:"power2.out"}},15.54);
tl.to("#mall .logo",{{keyframes:[{{opacity:.6,duration:.05}},{{opacity:1,duration:.05}},{{opacity:.75,duration:.04}},{{opacity:1,duration:.06}}]}},15.62);
tl.fromTo("#mallprod",{{y:60,opacity:0}},{{y:0,opacity:1,duration:.7,ease:EI}},14.78);
tl.fromTo("#glass",{{x:0}},{{x:1700,duration:1.1,ease:"power2.inOut"}},15.3);
tl.fromTo("#mk",{{opacity:0,scale:1.18}},{{opacity:1,scale:1,duration:.8,ease:E}},14.9);
stripes(16.64);
// ---- 4b pump
tl.fromTo("#vpump",{{scale:1.15}},{{scale:1.0,duration:2,ease:"power2.out"}},16.64);
tl.fromTo("#pr",{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:.5,ease:"back.out(2)"}},16.8);
tl.fromTo("#pl",{{scaleX:0}},{{scaleX:1,duration:.4,ease:E}},16.95);
tl.fromTo("#pc",{{opacity:0,x:30}},{{opacity:1,x:0,duration:.4,ease:E}},17.05);
tl.fromTo("#pc2",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:.4,ease:E}},17.3);
tl.to(["#pr","#pl","#pc","#pc2"],{{opacity:0,duration:.2}},17.62);
tl.fromTo("#bomb",{{opacity:0,scale:1.5,filter:"blur(20px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:.55,ease:EI}},17.70);
tl.fromTo("#bomb",{{backgroundPosition:"100% 0"}},{{backgroundPosition:"0% 0",duration:.9}},17.75);
flash(17.70,.5);
stripes(18.60);
// ---- 5a glory
tl.fromTo("#gb",{{x:260,rotation:8,opacity:0}},{{x:0,rotation:-3,opacity:1,duration:.8,ease:EI}},18.6);
tl.fromTo("#gb",{{y:0}},{{y:-30,duration:1.8,ease:"sine.inOut"}},18.9);
lineUp("#gs1",18.65,.5); tl.fromTo(["#gs2","#gs2b"],{{opacity:0,x:-60}},{{opacity:1,x:0,duration:.6,stagger:.1,ease:EI}},19.28);
tl.fromTo(["#gs2","#gs2b"],{{backgroundPosition:"100% 0"}},{{backgroundPosition:"0% 0",duration:1.1}},19.3);
tl.fromTo("#gs3",{{opacity:0}},{{opacity:.85,duration:.5}},19.6);
tl.fromTo("#gn > div",{{opacity:0,x:-40}},{{opacity:1,x:0,duration:.35,stagger:.16,ease:E}},19.0);
tl.fromTo("#gn i",{{scaleX:0,transformOrigin:"0 50%"}},{{scaleX:1,duration:.35,stagger:.16,ease:E}},19.0);
// ---- 5b noche (diagonal clip wipe)
tl.fromTo("#noche",{{clipPath:"polygon(100% 0,100% 0,100% 100%,100% 100%)"}},{{clipPath:"polygon(-30% 0,100% 0,100% 100%,0% 100%)",duration:.6,ease:"power3.inOut"}},20.42);
tl.fromTo("#nb",{{x:-260,rotation:-8,opacity:0}},{{x:0,rotation:3,opacity:1,duration:.8,ease:EI}},20.55);
tl.fromTo("#nb",{{y:0}},{{y:-34,duration:2.4,ease:"sine.inOut"}},20.9);
lineUp("#ns1",20.7,.5); tl.fromTo("#ns2",{{opacity:0,x:60}},{{opacity:1,x:0,duration:.6,ease:EI}},22.32);
tl.fromTo("#ns3",{{opacity:0,x:60}},{{opacity:1,x:0,duration:.6,ease:EI}},22.5).fromTo("#ns3",{{backgroundPosition:"100% 0"}},{{backgroundPosition:"0% 0",duration:1}},22.5);
tl.fromTo("#nn > div",{{opacity:0,x:40}},{{opacity:1,x:0,duration:.35,stagger:.16,ease:E}},20.9);
tl.fromTo("#nn i",{{scaleX:0,transformOrigin:"100% 50%"}},{{scaleX:1,duration:.35,stagger:.16,ease:E}},20.9);
// deterministic star field
(function(){{ const box=document.getElementById("stars"); let s=7; const r=()=> (s=(s*16807)%2147483647)/2147483647;
  for(let i=0;i<70;i++){{ const d=document.createElement("div"); d.className="star"; d.style.left=(r()*1080)+"px"; d.style.top=(r()*1300)+"px";
    const sc=.4+r()*1.4; d.style.transform="scale("+sc+")"; box.appendChild(d);
    tl.fromTo(d,{{opacity:0}},{{opacity:.3+r()*.7,duration:.3,repeat:5,yoyo:true,ease:"sine.inOut"}},20.5+r()*1.2); }} }})();
stripes(23.34);
// ---- 6a hold
tl.fromTo("#vhold",{{scale:1.0}},{{scale:1.12,duration:1.4,ease:"none"}},23.34);
tl.fromTo("#hk",{{opacity:0,scale:1.18}},{{opacity:1,scale:1,duration:.6,ease:E}},23.36);
lineUp("#h1",23.9,.7); tl.fromTo("#h1",{{backgroundPosition:"100% 0"}},{{backgroundPosition:"0% 0",duration:.8}},23.95);
// ---- 6b years (slot roll)
tl.fromTo(["#years","#vlather"],{{clipPath:"inset(50% 0 50% 0)"}},{{clipPath:"inset(0% 0 0% 0)",duration:.45,ease:"power3.inOut"}},24.68);
tl.fromTo("#roll",{{y:0}},{{y:-1200,duration:1.25,ease:"power3.inOut"}},24.85);
tl.fromTo("#vlather",{{scale:1.15}},{{scale:1,duration:1.6}},24.68);
stripes(26.30);
// ---- 6c flat
tl.fromTo("#fimg",{{scale:1.2,rotation:-2}},{{scale:1.04,rotation:0,duration:1.15,ease:"power1.out"}},26.30);
lineUp("#f1",26.35,.55); lineUp("#f2",26.55,.55);
// ---- 7 CTA
flash(27.40,1);
tl.fromTo("#k1",{{scale:1.6,opacity:0,filter:"blur(18px)"}},{{scale:1,opacity:1,filter:"blur(0px)",duration:.5,ease:EI}},27.40);
tl.fromTo("#k1",{{backgroundPosition:"100% 0"}},{{backgroundPosition:"0% 0",duration:1.2}},27.45);
lineUp("#k2",27.84,.5);
tl.fromTo("#meter",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.4,ease:E}},27.6);
const P={{v:100}}; tl.to(P,{{v:9,duration:1.3,ease:"power2.out",onUpdate:()=>{{document.getElementById("pct").textContent=Math.round(P.v)+"%";}}}},27.9);
tl.fromTo("#fill",{{scaleX:1}},{{scaleX:.09,duration:1.3,ease:"power2.out"}},27.9);
tl.to("#meter .track",{{keyframes:[{{x:-6,duration:.05}},{{x:6,duration:.05}},{{x:-4,duration:.05}},{{x:0,duration:.05}}]}},29.2);
tl.fromTo("#bag",{{y:-700,rotation:-20,opacity:0}},{{y:0,rotation:0,opacity:1,duration:.6,ease:"bounce.out"}},28.98);
tl.to("#bag",{{scale:1.12,duration:.25,yoyo:true,repeat:5,ease:"sine.inOut"}},29.6);
tl.fromTo("#tap",{{opacity:.95,scale:.3}},{{immediateRender:false,opacity:0,scale:2.6,duration:.6,ease:"power2.out"}},29.35);
tl.fromTo("#btn",{{y:220,opacity:0}},{{y:0,opacity:1,duration:.5,ease:"back.out(1.6)"}},29.5);
tl.to("#btn",{{scale:.93,duration:.08,yoyo:true,repeat:1}},30.1).fromTo("#btn",{{backgroundPosition:"100% 0"}},{{backgroundPosition:"0% 0",duration:.8}},30.1);
stripes(31.06);
// ---- 8 outro
tl.fromTo("#ol",{{opacity:0,scale:.9,filter:"brightness(3) blur(10px)"}},{{opacity:1,scale:1,filter:"brightness(1) blur(0px)",duration:.8,ease:"power2.out"}},31.1);
tl.to("#ol",{{keyframes:[{{opacity:.55,duration:.05}},{{opacity:1,duration:.05}},{{opacity:.7,duration:.04}},{{opacity:1,duration:.08}}]}},31.3);
tl.fromTo("#op",{{y:240,opacity:0}},{{y:0,opacity:1,duration:.9,ease:EI}},31.35);
tl.fromTo("#op",{{scale:1}},{{scale:1.05,duration:2.4,ease:"none"}},31.6);
tl.fromTo("#ok",{{opacity:0,scale:1.18}},{{opacity:1,scale:1,duration:.8,ease:E}},31.8);
tl.to("#root",{{opacity:1,duration:.01}},{TOTAL - 0.01});
window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body>
</html>
"""
open(f"{PROJ}/index.html", "w").write(HTML)
print("wrote", f"{PROJ}/index.html")
