#!/usr/bin/env python3
"""Generate the HyperFrames project for the Frescura Body vertical ad.
Voice is the clock: every beat is anchored to a word time from words_out.json (+VOFF)."""
import json, os, html

ROOT = "/home/user/work/film"
VOFF = 0.15                      # voice starts 0.15 s in
TOTAL = 38.4                     # root duration (voice ends ~36.9, end-card hold)
W = json.load(open("/home/user/work/words_out.json"))
for w in W:
    w["start"] = round(w["start"] + VOFF, 3); w["end"] = round(w["end"] + VOFF, 3)
def ws(i): return W[i]["start"]
def we(i): return W[i]["end"]

FONTS = """
@font-face{font-family:'Bodoni Moda';src:url('assets/fonts/BodoniModa.woff2') format('woff2');font-weight:400 900;font-style:normal}
@font-face{font-family:'Bodoni Moda';src:url('assets/fonts/BodoniModa-Italic.woff2') format('woff2');font-weight:400 900;font-style:italic}
@font-face{font-family:'Manrope';src:url('assets/fonts/Manrope.woff2') format('woff2');font-weight:200 800;font-style:normal}
"""
BASE_CSS = FONTS + """
#root{position:absolute;inset:0;overflow:hidden;font-family:'Manrope',sans-serif;color:#F4EEE3}
.abs{position:absolute}
.full{position:absolute;left:0;top:0;width:1080px;height:1920px}
.serif{font-family:'Bodoni Moda',serif}
.ital{font-family:'Bodoni Moda',serif;font-style:italic}
.label{font-family:'Manrope',sans-serif;font-weight:700;letter-spacing:.34em;text-transform:uppercase;font-size:30px;color:#D9BD86}
.gold{background:linear-gradient(100deg,#8C6A2E 0%,#E9CF94 28%,#FFF4D6 46%,#D2AE68 62%,#8C6A2E 100%);background-size:220% 100%;-webkit-background-clip:text;background-clip:text;color:transparent}
.center{left:0;width:1080px;text-align:center}
.onyx{background:radial-gradient(120% 70% at 50% 18%,#2A2320 0%,#141110 46%,#090808 100%)}
.grain{opacity:.07;mix-blend-mode:overlay}
.hair{stroke:#D9BD86;stroke-width:1.5;fill:none}
"""
GRAIN = """<svg class="full grain" viewBox="0 0 1080 1920" data-layout-ignore><filter id="{id}-n"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7"/></filter><rect width="1080" height="1920" filter="url(#{id}-n)"/></svg>"""
FRAME = """<svg class="full" viewBox="0 0 1080 1920" data-layout-ignore><rect id="{id}-frame" x="44" y="44" width="992" height="1832" rx="2" class="hair" stroke-dasharray="5648" stroke-dashoffset="5648" opacity=".55"/></svg>"""

def scene(sid, dur, body, script, extra_css=""):
    return f"""<template>
<style>{BASE_CSS}{extra_css}</style>
<div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920" data-duration="{dur:.3f}">
{body}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{script}
window.__timelines["{sid}"] = tl;
</script>
</template>
"""

def words_split(sid, text, cls=""):
    """Split text into word spans for staggered reveals."""
    out = []
    for k, t in enumerate(text.split(" ")):
        out.append(f'<span class="w {cls}" style="display:inline-block">{html.escape(t)}</span>')
    return " ".join(out)

scenes = []   # (sid, start, dur, html)

# ---------------------------------------------------------------- S1 HOOK
s, e = 0.0, round(ws(15) - 0.07, 3)       # until "Dia"
t = lambda x: round(x - s, 3)
body = f"""
<div class="full onyx"></div>
<img class="full" src="assets/img/flatlay_wood_blur.jpg" style="object-fit:cover;opacity:.35" id="s1-bg">
<div id="s1-beam" class="abs" style="left:-300px;top:-200px;width:520px;height:2400px;background:linear-gradient(90deg,rgba(255,236,196,0),rgba(255,236,196,.16),rgba(255,236,196,0));transform-origin:50% 0"></div>
{GRAIN.format(id='s1')}
{FRAME.format(id='s1')}
<div id="s1-tag" class="abs label center" style="top:300px">Pesanan untuk para suami</div>
<div id="s1-suami" class="abs center ital gold" style="top:360px;font-size:250px;line-height:1.1;font-weight:500">Suami,</div>
<div id="s1-l2" class="abs center serif" style="top:700px;font-size:60px;font-weight:500;letter-spacing:.01em">{words_split('s1','jangan sesekali anggap')}</div>
<div id="s1-isteri" class="abs center serif" style="top:770px;font-size:190px;font-weight:700;letter-spacing:.18em;color:#F7F1E6">ISTERI</div>
<div id="s1-chips" class="abs center" style="top:1000px;font-size:0">
  <span class="chip">Rumah</span><span class="chip">Anak</span><span class="chip">Sepanjang hari</span>
</div>
<div id="s1-penat" class="abs center" style="top:870px;height:170px">
  <span class="ital" style="font-size:150px;font-weight:500;position:relative;display:inline-block"><span id="s1-tak">tak</span> penat?<span id="s1-strike" class="abs" style="left:-10px;top:92px;width:262px;height:9px;background:#E3C27F;transform-origin:0 50%"></span></span>
</div>
"""
css1 = """.chip{display:inline-block;margin:0 10px;padding:16px 30px;border:1.5px solid rgba(217,189,134,.7);border-radius:999px;font-size:34px;font-weight:700;letter-spacing:.08em;color:#F4EEE3;background:rgba(20,16,14,.55)}"""
scr = f"""
tl.fromTo("#s1-bg",{{scale:1.12}},{{scale:1,duration:{e-s:.2f},ease:"none"}},0);
tl.fromTo("#s1-beam",{{x:-200,rotation:18}},{{x:1500,rotation:18,duration:2.6,ease:"power2.inOut"}},0.05);
tl.fromTo("#s1-frame",{{strokeDashoffset:5648}},{{strokeDashoffset:0,duration:1.6,ease:"power3.inOut"}},0);
tl.fromTo("#s1-suami",{{opacity:.85,scale:1.14,filter:"blur(6px)",backgroundPosition:"100% 0"}},{{opacity:1,scale:1,filter:"blur(0px)",backgroundPosition:"0% 0",duration:.55,ease:"expo.out"}},0);
tl.fromTo("#s1-tag",{{opacity:0}},{{opacity:1,duration:.7,ease:"power3.out"}},0.05);
tl.to("#s1-suami",{{y:-60,scale:.62,duration:.6,ease:"power4.inOut"}},{t(ws(1))-0.12});
tl.fromTo("#s1-l2 .w",{{opacity:0,y:40,filter:"blur(8px)"}},{{opacity:1,y:-30,filter:"blur(0px)",duration:.45,stagger:{{each:.28}},ease:"power3.out"}},{t(ws(1))});
tl.fromTo("#s1-isteri",{{opacity:0,scale:1.08}},{{opacity:1,scale:1,duration:.6,ease:"expo.out"}},{t(ws(4))-0.05});
tl.to("#s1-isteri",{{y:-90,duration:.5,ease:"power3.inOut"}},{t(ws(7))-0.25});
tl.to("#s1-l2",{{y:-110,opacity:.55,duration:.5,ease:"power3.inOut"}},{t(ws(7))-0.25});
tl.fromTo("#s1-chips .chip",{{opacity:0,y:30,scale:.9}},{{opacity:1,y:-60,scale:1,duration:.4,stagger:{{each:{(ws(10)-ws(7))/2:.2f}}},ease:"back.out(2)"}},{t(ws(7))-0.05});
tl.to("#s1-chips",{{opacity:0,y:-40,duration:.25,ease:"power2.in"}},{t(ws(13))-0.3});
tl.fromTo("#s1-penat",{{opacity:0,y:40,scale:.94}},{{opacity:1,y:0,scale:1,duration:.4,ease:"expo.out"}},{t(ws(13))-0.08});
tl.fromTo("#s1-strike",{{scaleX:0}},{{scaleX:1,duration:.28,ease:"power4.out"}},{t(ws(14))+0.05});
tl.to("#s1-tak",{{opacity:.35,duration:.2}},{t(ws(14))+0.1});
tl.to("#s1-penat",{{scale:1.06,duration:.4,ease:"power2.out"}},{t(ws(14))+0.35});
"""
scenes.append(("s1", s, e - s, scene("s1", e - s, body, scr, css1)))

# ---------------------------------------------------------------- S2 ENDLESS CHORES
s, e = scenes[-1][1] + scenes[-1][2], round(ws(28) - 0.07, 3)
t = lambda x: round(x - s, 3)
chores = ["Siapkan sarapan", "Hantar anak ke sekolah", "Basuh &amp; lipat baju", "Kemas rumah", "Masak makan tengah hari",
          "Ambil anak", "Teman anak belajar", "Masak makan malam", "Cuci pinggan", "Tidurkan anak", "Siapkan esok…"]
cards = "\n".join(f'<div class="card"><span class="tick"><svg viewBox="0 0 40 40" width="40" height="40"><circle cx="20" cy="20" r="18" class="hair"/><path class="ck" d="M11 21 l6 6 l12 -14" stroke="#E3C27F" stroke-width="3" fill="none" stroke-dasharray="30" stroke-dashoffset="30"/></svg></span>{c}</div>' for c in chores)
body = f"""
<div class="full onyx"></div>
{GRAIN.format(id='s2')}
<div id="s2-top" class="abs center" style="top:290px">
  <div class="label">Bukan kerja 9 ke 5</div>
  <div class="ital" style="font-size:66px;margin-top:22px;color:#F4EEE3">Tak keluar bekerja&hellip;</div>
</div>
<div id="s2-mask" class="abs" style="left:150px;top:450px;width:780px;height:430px;overflow:hidden;-webkit-mask-image:linear-gradient(180deg,transparent 0%,#000 20%,#000 80%,transparent 100%);mask-image:linear-gradient(180deg,transparent 0%,#000 20%,#000 80%,transparent 100%)" data-layout-allow-overflow>
  <div id="s2-list" class="abs" style="left:0;top:0;width:780px" data-layout-ignore>{cards}</div>
</div>
<div id="s2-bottom" class="abs center" style="top:890px">
  <div class="serif" style="font-size:72px;font-weight:600">Kerja rumah</div>
  <div style="display:flex;justify-content:center;align-items:center;gap:26px;margin-top:6px">
    <span class="ital gold" style="font-size:96px;font-weight:500">tak pernah habis</span>
    <span id="s2-inf" style="display:inline-block;width:120px;height:60px"><svg viewBox="0 0 120 60" width="120" height="60"><path d="M60 30 C45 5 10 5 10 30 C10 55 45 55 60 30 C75 5 110 5 110 30 C110 55 75 55 60 30Z" stroke="#E9CF94" stroke-width="6" fill="none"/></svg></span>
  </div>
</div>
"""
css2 = """.card{display:flex;align-items:center;gap:26px;height:96px;margin-bottom:14px;padding:0 34px;border-radius:22px;background:linear-gradient(120deg,rgba(255,255,255,.08),rgba(255,255,255,.02));border:1px solid rgba(217,189,134,.35);font-size:40px;font-weight:600;color:#F4EEE3}
.tick{display:inline-flex;width:40px;height:40px}"""
n = len(chores); step = 110; listdur = e - s
scr = f"""
tl.fromTo("#s2-top",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.45,ease:"power3.out"}},0.02);
tl.fromTo("#s2-list",{{y:180}},{{y:{-(n*step)+480},duration:{listdur:.2f},ease:"power1.in"}},0);
"""
for k in range(n):
    scr += f'tl.fromTo("#s2-list .card:nth-child({k+1}) .ck",{{strokeDashoffset:30}},{{strokeDashoffset:0,duration:.18,ease:"power2.out"}},{0.25 + k*0.27:.2f});\n'
scr += f"""
tl.fromTo("#s2-bottom",{{opacity:0,y:50,filter:"blur(10px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.5,ease:"expo.out"}},{t(ws(23))-0.05});
tl.fromTo("#s2-inf",{{rotation:-90,scale:.4}},{{rotation:0,scale:1,duration:.7,ease:"back.out(2.2)"}},{t(ws(25))});
"""
scenes.append(("s2", s, e - s, scene("s2", e - s, body, scr, css2)))
CHORE_TICKS = [round(s + 0.25 + k*0.27 + 0.05, 3) for k in range(n)]

# ---------------------------------------------------------------- S3 DAY DIAL -> REST
s, e = scenes[-1][1] + scenes[-1][2], round(ws(49) - 0.07, 3)
t = lambda x: round(x - s, 3)
ticks = "".join(f'<line class="dt" x1="540" y1="{400-300}" x2="540" y2="{400-272 if k%5 else 400-262}" transform="rotate({k*6} 540 400)" stroke="#D9BD86" stroke-width="{3 if k%5==0 else 1.6}" opacity=".18"/>' for k in range(60))
body = f"""
<div class="full onyx"></div>
<div id="s3-glow" class="abs" style="left:90px;top:330px;width:900px;height:900px;border-radius:50%;background:radial-gradient(closest-side,rgba(255,226,170,.55),rgba(255,226,170,.12) 55%,rgba(255,226,170,0))"></div>
{GRAIN.format(id='s3')}
<div id="s3-dialwrap" class="abs" style="left:0;top:180px;width:1080px;height:800px">
 <svg viewBox="0 0 1080 800" width="1080" height="800" style="position:absolute;left:0;top:0;overflow:visible">
  <circle cx="540" cy="400" r="300" class="hair" opacity=".5"/>
  {ticks}
  <path id="s3-arc" d="M240 400 A300 300 0 0 1 840 400" stroke="#E9CF94" stroke-width="4" fill="none" stroke-dasharray="943" stroke-dashoffset="943" stroke-linecap="round"/>
 </svg>
 <div id="s3-orb" class="abs" style="left:200px;top:360px;width:80px;height:80px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#FFF6DA,#F2C46B 60%,#B9852D);box-shadow:0 0 60px 18px rgba(242,196,107,.55)"></div>
 <div id="s3-moon" class="abs" style="left:800px;top:360px;width:80px;height:80px;border-radius:50%;background:radial-gradient(circle at 70% 30%,#F4EEE3,#B7B3C9 70%);box-shadow:0 0 50px 12px rgba(200,200,255,.35);opacity:0"></div>
 <div id="s3-time" class="abs center serif" style="top:330px;font-size:120px;font-weight:600;letter-spacing:.04em">06:00</div>
 <div class="abs label" style="left:150px;top:470px">Pagi</div>
 <div class="abs label" style="left:760px;top:470px">Malam</div>
 <div id="s3-sub" class="abs center ital" style="top:475px;font-size:46px;color:#D9BD86;opacity:0">ada saja yang perlu diurus</div>
</div>
<div id="s3-rest" class="abs center" style="top:300px;opacity:0">
  <div class="label">Self-care itu keperluan</div>
  <div id="s3-need" class="serif" style="font-size:64px;font-weight:500;margin-top:34px">Isteri pun perlukan masa</div>
  <div id="s3-berehat" class="ital gold" style="font-size:200px;font-weight:500;line-height:1.15;margin-top:10px">berehat</div>
  <div id="s3-diri" class="serif" style="font-size:60px;font-weight:500;margin-top:6px">&amp; menjaga <span class="ital gold" style="font-size:76px">diri sendiri</span></div>
</div>
"""
dial_end = t(ws(32))
scr = f"""
tl.fromTo("#s3-dialwrap",{{opacity:0,scale:.9}},{{opacity:1,scale:1,duration:.5,ease:"expo.out"}},0);
tl.fromTo("#s3-arc",{{strokeDashoffset:943}},{{strokeDashoffset:0,duration:{dial_end:.2f},ease:"power1.inOut"}},0.05);
tl.fromTo("#s3-orb",{{x:0,y:0}},{{x:300,y:-300,duration:{dial_end/2:.2f},ease:"sine.out"}},0.05);
tl.to("#s3-orb",{{x:600,y:0,duration:{dial_end/2:.2f},ease:"sine.in"}},{0.05+dial_end/2:.2f});
tl.to("#s3-orb",{{opacity:0,duration:.2}},{dial_end:.2f});
tl.to("#s3-moon",{{opacity:1,duration:.25}},{dial_end-0.05:.2f});
const clk={{v:6}};
tl.fromTo(clk,{{v:6}},{{v:23,duration:{dial_end:.2f},ease:"power1.inOut",onUpdate:()=>{{const h=Math.floor(clk.v);document.querySelector("#s3-time").textContent=String(h).padStart(2,"0")+":"+(clk.v-h<.5?"00":"30");}}}},0.05);
tl.fromTo("#s3-dialwrap .dt",{{opacity:.18}},{{opacity:1,duration:.05,stagger:{{each:{(t(ws(37))-dial_end)/60:.3f}}}}},{dial_end:.2f});
tl.fromTo("#s3-sub",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.35}},{dial_end:.2f});
tl.to("#s3-dialwrap",{{opacity:0,scale:.2,duration:.45,ease:"power4.in"}},{t(ws(37))-0.2});
tl.fromTo("#s3-glow",{{opacity:0,scale:.2}},{{opacity:1,scale:1,duration:1.2,ease:"expo.out"}},{t(ws(37))+0.1});
tl.fromTo("#s3-rest",{{opacity:0}},{{opacity:1,duration:.3}},{t(ws(39))-0.2});
tl.fromTo("#s3-need",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.4,ease:"power3.out"}},{t(ws(39))-0.2});
tl.fromTo("#s3-berehat",{{opacity:0,scale:1.25,filter:"blur(14px)",backgroundPosition:"100% 0"}},{{opacity:1,scale:1,filter:"blur(0px)",backgroundPosition:"0% 0",duration:.7,ease:"expo.out"}},{t(ws(44))-0.05});
tl.fromTo("#s3-diri",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.45,ease:"power3.out"}},{t(ws(46))-0.05});
tl.to("#s3-glow",{{scale:1.1,duration:1.5,ease:"sine.inOut"}},{t(ws(44))});
"""
scenes.append(("s3", s, e - s, scene("s3", e - s, body, scr)))

# ---------------------------------------------------------------- S4 PAMPER (B-roll lather)
s, e = scenes[-1][1] + scenes[-1][2], round(ws(56) - 0.05, 3)
t = lambda x: round(x - s, 3)
body = f"""
<div class="full" style="background:#0b0a0a"></div>
<div id="s4-vw" class="full"><video id="s4-v" class="clip full" src="assets/video/pump.mp4" data-start="0" data-duration="{e-s:.3f}" data-media-start="29.6" data-playback-rate="0.8" muted playsinline style="object-fit:cover"></video></div>
<div class="full" style="background:linear-gradient(180deg,rgba(8,7,7,.85) 0%,rgba(8,7,7,.25) 38%,rgba(8,7,7,.2) 55%,rgba(8,7,7,.9) 100%)"></div>
{GRAIN.format(id='s4')}
<div id="s4-txt" class="abs center" style="top:300px">
  <div class="label">Berikan dia</div>
  <div class="serif" style="font-size:78px;font-weight:500;margin-top:22px">sedikit masa</div>
  <div id="s4-manja" class="ital gold" style="font-size:104px;font-weight:500;line-height:1.1">untuk manjakan</div>
  <div class="ital" style="font-size:96px;font-weight:500">dirinya.</div>
</div>
<div id="s4-flash" class="full" style="background:#FFF3DA;opacity:0"></div>
"""
scr = f"""
tl.fromTo("#s4-vw",{{scale:1.18}},{{scale:1.02,duration:{e-s:.2f},ease:"power1.out"}},0);
tl.fromTo("#s4-txt .label",{{opacity:0}},{{opacity:1,duration:.5}},0.05);
tl.fromTo("#s4-txt .serif",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.4,ease:"power3.out"}},{t(ws(51))-0.1});
tl.fromTo("#s4-manja",{{opacity:0,y:30,clipPath:"inset(0 100% 0 0)"}},{{opacity:1,y:0,clipPath:"inset(0 0% 0 0)",duration:.6,ease:"power3.out"}},{t(ws(54))-0.08});
tl.fromTo("#s4-txt .ital:last-child",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.4,ease:"power3.out"}},{t(ws(55))-0.05});
tl.fromTo("#s4-flash",{{opacity:0}},{{opacity:.55,duration:.12}},{e-s-0.14:.2f});
"""
scenes.append(("s4", s, e - s, scene("s4", e - s, body, scr)))

# ---------------------------------------------------------------- S5 BOUTIQUE -> LOGO -> HERO PODIUM
s, e = scenes[-1][1] + scenes[-1][2], round(ws(69) - 0.06, 3)
t = lambda x: round(x - s, 3)
arches = "".join(f'<div class="arch" id="s5-a{k}"></div>' for k in range(6))
body = f"""
<div class="full" style="background:linear-gradient(180deg,#120F0E 0%,#1C1715 52%,#0A0908 100%)"></div>
<div id="s5-corr" class="full" style="perspective:900px;perspective-origin:50% 42%">
  <div class="abs" style="left:0;top:0;width:1080px;height:1920px;transform-style:preserve-3d">{arches}</div>
  <div class="abs" style="left:0;top:960px;width:1080px;height:960px;background:repeating-linear-gradient(90deg,rgba(217,189,134,.0) 0 88px,rgba(217,189,134,.18) 88px 90px),linear-gradient(180deg,#2a2320,#0b0a09);transform:none;-webkit-mask-image:linear-gradient(180deg,transparent,#000 40%)"></div>
</div>
<div id="s5-pasti" class="abs center ital" style="top:300px;font-size:84px;font-weight:500">Pastinya,</div>
<div id="s5-burst" class="abs" style="left:-460px;top:-60px;width:2000px;height:2000px;border-radius:50%;background:radial-gradient(closest-side,rgba(120,220,255,.35),rgba(80,140,255,.08) 45%,rgba(0,0,0,0));opacity:0"></div>
<img id="s5-logo" class="abs" src="assets/img/logo.jpg" style="left:140px;top:300px;width:800px;height:800px;mix-blend-mode:screen;opacity:0">
<div id="s5-hero" class="full" style="opacity:0">
  <div class="abs" style="left:0;top:0;width:1080px;height:1920px;background:radial-gradient(60% 40% at 50% 46%,#3A2E27 0%,#16110F 60%,#080707 100%)"></div>
  <div class="spot" style="left:150px"></div><div class="spot" style="left:560px"></div>
  <div id="s5-wordmark" class="abs center label" style="top:290px;font-size:30px;color:#E9D3A0">Frescura Body</div>
  <div class="abs" style="left:240px;top:880px;width:600px;height:110px;border-radius:50%;background:linear-gradient(180deg,#3b322c,#15110f);box-shadow:0 -2px 0 rgba(233,207,148,.6) inset, 0 40px 80px rgba(0,0,0,.7)"></div>
  <div class="abs" style="left:240px;top:935px;width:600px;height:60px;background:linear-gradient(180deg,#221c19,#0d0b0a);border-radius:0 0 50% 50%/0 0 40% 40%"></div>
  <div id="s5-bottles" class="abs" style="left:0;top:0;width:1080px;height:1920px">
    <div class="btl" id="s5-b1" style="left:320px;top:370px"><img src="assets/img/noche_cut.png"><div class="sheen" style="-webkit-mask-image:url(assets/img/noche_cut.png);mask-image:url(assets/img/noche_cut.png)"></div></div>
    <div class="btl" id="s5-b2" style="left:560px;top:370px"><img src="assets/img/glory_cut.png"><div class="sheen" style="-webkit-mask-image:url(assets/img/glory_cut.png);mask-image:url(assets/img/glory_cut.png)"></div></div>
  </div>
  <div id="s5-copy" class="abs center" style="top:985px">
    <div class="label" style="color:#F4EEE3;letter-spacing:.22em">Nikmati pengalaman mandi</div>
    <div class="ital gold" style="font-size:60px;font-weight:500;line-height:1.15;margin-top:6px">buih lembut terus dari botol</div>
  </div>
</div>
"""
css5 = """
.arch{position:absolute;left:240px;top:420px;width:600px;height:1080px;border:2px solid rgba(233,207,148,.7);border-radius:300px 300px 0 0;box-shadow:0 0 40px rgba(233,207,148,.25), inset 0 0 60px rgba(233,207,148,.12)}
.spot{position:absolute;top:-40px;width:370px;height:1100px;background:linear-gradient(180deg,rgba(255,240,210,.28),rgba(255,240,210,0));clip-path:polygon(42% 0,58% 0,100% 100%,0 100%);mix-blend-mode:screen}
.btl{position:absolute;width:200px;height:571px}
.btl img{width:200px;height:571px;filter:drop-shadow(0 30px 40px rgba(0,0,0,.6))}
.sheen{position:absolute;left:0;top:0;width:200px;height:571px;-webkit-mask-size:100% 100%;mask-size:100% 100%;background:linear-gradient(105deg,rgba(255,255,255,0) 35%,rgba(255,255,255,.55) 48%,rgba(255,255,255,0) 60%);background-size:300% 100%;background-position:100% 0;mix-blend-mode:screen}
"""
logo_t = t(ws(57)) - 0.03
hero_t = t(ws(61)) - 0.35
scr = ""
for k in range(6):
    scr += f'tl.fromTo("#s5-a{k}",{{z:{-2400 + k*420},opacity:{0.15 + k*0.12:.2f}}},{{z:{-2400 + k*420 + 1900},opacity:1,duration:{logo_t:.2f},ease:"power2.in"}},0);\n'
scr += f"""
tl.fromTo("#s5-pasti",{{opacity:0,y:30,}},{{opacity:1,y:0,duration:.4,ease:"power3.out"}},0.0);
tl.to("#s5-pasti",{{opacity:0,y:-20,duration:.2}},{logo_t-0.2:.2f});
tl.to("#s5-corr",{{opacity:0,duration:.15}},{logo_t:.2f});
tl.fromTo("#s5-burst",{{opacity:0,scale:.3}},{{opacity:1,scale:1,duration:.5,ease:"expo.out"}},{logo_t:.2f});
tl.fromTo("#s5-logo",{{opacity:0,scale:1.35,filter:"blur(12px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:.45,ease:"expo.out"}},{logo_t:.2f});
tl.to("#s5-logo",{{scale:1.06,duration:1.0,ease:"none"}},{logo_t+0.45:.2f});
tl.to(["#s5-logo","#s5-burst"],{{opacity:0,duration:.25}},{hero_t:.2f});
tl.fromTo("#s5-hero",{{opacity:0}},{{opacity:1,duration:.3}},{hero_t:.2f});
tl.fromTo("#s5-b1",{{y:260,opacity:0,rotation:-4}},{{y:0,opacity:1,rotation:-3,duration:.7,ease:"expo.out"}},{hero_t:.2f});
tl.fromTo("#s5-b2",{{y:260,opacity:0,rotation:4}},{{y:0,opacity:1,rotation:3,duration:.7,ease:"expo.out"}},{hero_t+0.1:.2f});
tl.to("#s5-bottles",{{y:-14,duration:1.6,ease:"sine.inOut"}},{hero_t+0.7:.2f});
tl.fromTo("#s5-b1 .sheen",{{backgroundPosition:"100% 0"}},{{backgroundPosition:"0% 0",duration:.9,ease:"power2.inOut"}},{hero_t+0.6:.2f});
tl.fromTo("#s5-b2 .sheen",{{backgroundPosition:"100% 0"}},{{backgroundPosition:"0% 0",duration:.9,ease:"power2.inOut"}},{hero_t+0.8:.2f});
tl.fromTo("#s5-wordmark",{{opacity:0}},{{opacity:1,duration:.6}},{hero_t:.2f});
tl.fromTo("#s5-copy .label",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.35}},{hero_t+0.15:.2f});
tl.fromTo("#s5-copy .ital",{{opacity:0,y:30,backgroundPosition:"100% 0"}},{{opacity:1,y:0,backgroundPosition:"0% 0",duration:.8,ease:"power3.out"}},{t(ws(64))-0.08});
"""
scenes.append(("s5", s, e - s, scene("s5", e - s, body, scr, css5)))
S5_LOGO = s + logo_t; S5_HERO = s + hero_t

# ---------------------------------------------------------------- S6 PUMP B-ROLL
s, e = scenes[-1][1] + scenes[-1][2], round(ws(78) - 0.05, 3)
t = lambda x: round(x - s, 3)
cutB = t(ws(73)) - 0.05
body = f"""
<div class="full" style="background:#0b0a0a"></div>
<div id="s6-wa" class="full"><video id="s6-va" class="clip full" src="assets/video/pump.mp4" data-start="0" data-duration="{cutB:.3f}" data-media-start="10.3" data-playback-rate="1.15" muted playsinline style="object-fit:cover"></video></div>
<div id="s6-wb" class="full"><video id="s6-vb" class="clip full" src="assets/video/pump.mp4" data-start="{cutB:.3f}" data-duration="{e-s-cutB:.3f}" data-media-start="15.4" data-playback-rate="0.9" muted playsinline style="object-fit:cover"></video></div>
<div class="full" style="background:linear-gradient(180deg,rgba(8,7,7,.7) 0%,rgba(8,7,7,0) 30%,rgba(8,7,7,0) 58%,rgba(8,7,7,.85) 100%)"></div>
<div id="s6-ring1" class="ring" style="left:800px;top:690px"></div><div id="s6-ring2" class="ring" style="left:800px;top:690px"></div>
<div id="s6-tekan" class="abs" style="left:110px;top:620px;text-align:left">
  <div id="s6-t1" class="stamp">TEKAN.</div><div id="s6-t2" class="stamp ital gold" style="margin-top:-30px">tekan.</div>
</div>
<div id="s6-keluar" class="abs center ital" style="top:1060px;font-size:64px;font-weight:500;opacity:0">terus keluar buih</div>
<div id="s6-callouts" class="full" style="opacity:0">
  <svg class="full" viewBox="0 0 1080 1920"><path id="s6-l1" d="M520 760 L360 560 L170 560" class="hair" stroke-width="2.5" stroke-dasharray="460" stroke-dashoffset="460"/><path id="s6-l2" d="M640 900 L790 700 L930 700" class="hair" stroke-width="2.5" stroke-dasharray="400" stroke-dashoffset="400"/>
  <circle id="s6-d1" cx="520" cy="760" r="10" fill="#E9CF94"/><circle id="s6-d2" cx="640" cy="900" r="10" fill="#E9CF94"/></svg>
  <div id="s6-c1" class="abs co" style="left:130px;top:470px"><div class="label" style="font-size:28px">Tekstur</div><div class="ital gold" style="font-size:82px;font-weight:500;line-height:1">Lembut</div></div>
  <div id="s6-c2" class="abs co" style="left:700px;top:610px"><div class="label" style="font-size:28px">Buih</div><div class="ital gold" style="font-size:82px;font-weight:500;line-height:1">Gebu</div></div>
  <div id="s6-chip" class="abs center" style="top:300px"><span class="pill">Gentle Foaming &middot; Siap dari pam</span></div>
</div>
"""
css6 = """
.stamp{display:block;text-shadow:0 6px 30px rgba(0,0,0,.8);font-family:'Bodoni Moda',serif;font-weight:700;font-size:150px;letter-spacing:.02em;color:#F7F1E6;text-shadow:0 10px 40px rgba(0,0,0,.5)}
.co{padding:14px 26px;border-radius:22px;background:rgba(14,11,10,.62);border:1px solid rgba(233,207,148,.45)}
.ring{position:absolute;width:300px;height:300px;margin:-150px 0 0 -150px;border-radius:50%;border:3px solid rgba(233,207,148,.9)}
.pill{display:inline-block;padding:16px 34px;border-radius:999px;background:rgba(15,12,11,.62);border:1px solid rgba(233,207,148,.6);font-size:30px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#F4EEE3}
"""
p1, p2 = t(ws(69)), t(ws(70))
scr = f"""
tl.fromTo("#s6-wa",{{scale:1.12}},{{scale:1.0,duration:{cutB:.2f},ease:"power2.out"}},0);
tl.fromTo("#s6-wb",{{scale:1.0}},{{scale:1.14,duration:{e-s-cutB:.2f},ease:"power1.inOut"}},{cutB:.2f});
tl.fromTo("#s6-t1",{{opacity:0,scale:1.8}},{{opacity:1,scale:1,duration:.22,ease:"power4.out"}},{p1-0.02:.2f});
tl.fromTo("#s6-t2",{{opacity:0,scale:1.8}},{{opacity:1,scale:1,duration:.22,ease:"power4.out"}},{p2-0.02:.2f});
tl.fromTo("#s6-ring1",{{scale:.2,opacity:1}},{{scale:1.6,opacity:0,duration:.6,ease:"power2.out"}},{p1:.2f});
tl.fromTo("#s6-ring2",{{scale:.2,opacity:1}},{{scale:1.6,opacity:0,duration:.6,ease:"power2.out"}},{p2:.2f});
tl.to("#s6-tekan",{{y:-40,opacity:.0,duration:.3,ease:"power2.in"}},{t(ws(72))-0.1});
tl.fromTo("#s6-keluar",{{opacity:0,y:30}},{{opacity:1,y:-60,duration:.35,ease:"power3.out"}},{t(ws(71))-0.05});
tl.to("#s6-keluar",{{opacity:0,duration:.2}},{cutB-0.05:.2f});
tl.fromTo("#s6-callouts",{{opacity:0}},{{opacity:1,duration:.2}},{cutB:.2f});
tl.fromTo("#s6-chip",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:.4,ease:"power3.out"}},{cutB+0.1:.2f});
tl.fromTo("#s6-d1",{{scale:0,transformOrigin:"50% 50%"}},{{scale:1,duration:.25,ease:"back.out(3)"}},{t(ws(75))-0.2:.2f});
tl.fromTo("#s6-l1",{{strokeDashoffset:460}},{{strokeDashoffset:0,duration:.35,ease:"power2.out"}},{t(ws(75))-0.15:.2f});
tl.fromTo("#s6-c1",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:.35,ease:"power3.out"}},{t(ws(75))-0.02:.2f});
tl.fromTo("#s6-d2",{{scale:0,transformOrigin:"50% 50%"}},{{scale:1,duration:.25,ease:"back.out(3)"}},{t(ws(77))-0.2:.2f});
tl.fromTo("#s6-l2",{{strokeDashoffset:400}},{{strokeDashoffset:0,duration:.35,ease:"power2.out"}},{t(ws(77))-0.15:.2f});
tl.fromTo("#s6-c2",{{opacity:0,x:30}},{{opacity:1,x:0,duration:.35,ease:"power3.out"}},{t(ws(77))-0.02:.2f});
"""
scenes.append(("s6", s, e - s, scene("s6", e - s, body, scr, css6)))
S6_P1, S6_P2, S6_CUT = s + p1, s + p2, s + cutB

# ---------------------------------------------------------------- S7 TWO SCENTS
s, e = scenes[-1][1] + scenes[-1][2], round(ws(85) - 0.06, 3)
t = lambda x: round(x - s, 3)
body = f"""
<div class="full onyx"></div>
{GRAIN.format(id='s7')}
<div id="s7-head" class="abs center" style="top:260px">
  <div class="label">Dua wangian eksklusif</div>
  <div class="ital gold" style="font-size:96px;font-weight:500;margin-top:10px">bauan perfume</div>
</div>
<div id="s7-c1" class="scard" style="top:450px;background:linear-gradient(120deg,#5E0E18 0%,#2A070C 70%)">
  <img src="assets/img/glory_cut.png" class="sbtl">
  <div class="sinfo"><div class="label" style="font-size:28px;color:#F2C9CF">Woman Glory</div><div class="ital" style="font-size:84px;font-weight:600;line-height:1.05">Bombshell</div><div class="snote">Ros &middot; Aromatherapy</div></div>
</div>
<div id="s7-c2" class="scard" style="top:800px;background:linear-gradient(120deg,#2E1F5E 0%,#110B26 70%)">
  <img src="assets/img/noche_cut.png" class="sbtl">
  <div class="sinfo"><div class="label" style="font-size:28px;color:#CFC4F2">Noche</div><div class="ital" style="font-size:56px;font-weight:600;line-height:1.05">Midnight Fantasy</div><div class="snote">Ocean Salt &middot; Aromatherapy</div></div>
</div>
"""
css7 = """
.scard{position:absolute;left:100px;width:860px;height:330px;border-radius:34px;border:1px solid rgba(233,207,148,.45);overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.55)}
.sbtl{position:absolute;left:46px;top:28px;width:150px;height:428px;filter:drop-shadow(0 18px 24px rgba(0,0,0,.6))}
.sinfo{position:absolute;left:230px;top:66px;width:520px}
.snote{margin-top:16px;font-size:28px;letter-spacing:.04em;font-weight:600;letter-spacing:.1em;color:rgba(244,238,227,.8)}
"""
scr = f"""
tl.fromTo("#s7-head .label",{{opacity:0}},{{opacity:1,duration:.45}},0.02);
tl.fromTo("#s7-head .ital",{{opacity:0,y:30,backgroundPosition:"100% 0"}},{{opacity:1,y:0,backgroundPosition:"0% 0",duration:.7,ease:"power3.out"}},{max(0.05,t(ws(79))-0.05):.2f});
tl.fromTo("#s7-c1",{{opacity:0,x:-700,rotation:-4}},{{opacity:1,x:0,rotation:0,duration:.55,ease:"expo.out"}},{t(ws(81))-0.12:.2f});
tl.fromTo("#s7-c1 .sbtl",{{y:120}},{{y:0,duration:.8,ease:"expo.out"}},{t(ws(81))-0.05:.2f});
tl.fromTo("#s7-c2",{{opacity:0,x:700,rotation:4}},{{opacity:1,x:0,rotation:0,duration:.55,ease:"expo.out"}},{t(ws(83))-0.12:.2f});
tl.fromTo("#s7-c2 .sbtl",{{y:120}},{{y:0,duration:.8,ease:"expo.out"}},{t(ws(83))-0.05:.2f});
"""
scenes.append(("s7", s, e - s, scene("s7", e - s, body, scr, css7)))
S7_C1, S7_C2 = s + t(ws(81)) - 0.12, s + t(ws(83)) - 0.12

# ---------------------------------------------------------------- S8 GIFT FOR HER (arrows reverse)
s, e = scenes[-1][1] + scenes[-1][2], round(ws(99) - 0.08, 3)
t = lambda x: round(x - s, 3)
nodes = [("Suami", 230, 380), ("Anak", 850, 380), ("Rumah", 230, 860), ("Keluarga", 850, 860)]
cx, cy = 540, 620
svg_lines = ""
node_html = ""
for k, (nm, x, y) in enumerate(nodes):
    svg_lines += f'<line id="s8-ln{k}" x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="#E9CF94" stroke-width="2.5" stroke-dasharray="10 10" opacity=".8"/>'
    node_html += f'<div class="node" id="s8-n{k}" style="left:{x-110}px;top:{y-44}px">{nm}</div>'
# travelling dots: from centre outward (she gives) then reversed (to her)
dots = "".join(f'<div class="dot" id="s8-dt{k}" style="left:{cx-9}px;top:{cy-9}px"></div>' for k in range(4))
body = f"""
<div class="full" style="background:#0c0a09"></div>
<img id="s8-bg" class="full" src="assets/img/flatlay_linen_blur.jpg" style="object-fit:cover;opacity:.55">
{GRAIN.format(id='s8')}
<div id="s8-diagram" class="full">
  <div class="abs label center" style="top:290px">Siapa jaga siapa?</div>
  <svg class="full" viewBox="0 0 1080 1920">{svg_lines}</svg>
  {node_html}{dots}
  <div id="s8-her" class="abs" style="left:{cx-120}px;top:{cy-120}px;width:240px;height:240px;border-radius:50%;background:radial-gradient(circle at 40% 35%,#F7E3B5,#C9A25E 70%,#8C6A2E);display:flex;align-items:center;justify-content:center;box-shadow:0 0 70px rgba(233,207,148,.5)"><span class="ital" style="font-size:58px;font-weight:600;color:#1A1210">Isteri</span></div>
  <div id="s8-q" class="abs center serif" style="top:960px;font-size:56px;font-weight:500">Dia jaga <span class="ital gold" style="font-size:70px">semua orang</span></div>
</div>
<div id="s8-gift" class="full" style="opacity:0">
  <img id="s8-photo" class="full" src="assets/img/flatlay_linen_1080.jpg" style="object-fit:cover">
  <div class="full" style="background:linear-gradient(180deg,rgba(10,8,7,.82) 0%,rgba(10,8,7,.35) 30%,rgba(10,8,7,0) 45%,rgba(10,8,7,0) 62%,rgba(10,8,7,.88) 100%)"></div>
  <div id="s8-k1" class="abs center label" style="top:300px;color:#F4EEE3">Kali ini, belikan sesuatu</div>
  <div id="s8-k2" class="abs center ital gold" style="top:350px;font-size:150px;font-weight:500;line-height:1.1">untuk dia.</div>
</div>
"""
css8 = """
.node{position:absolute;width:220px;height:88px;border-radius:999px;border:1.5px solid rgba(233,207,148,.7);background:rgba(18,14,12,.7);display:flex;align-items:center;justify-content:center;font-size:36px;font-weight:700;letter-spacing:.04em}
.dot{position:absolute;width:18px;height:18px;border-radius:50%;background:#FFF1CC;box-shadow:0 0 18px 6px rgba(255,226,160,.8)}
"""
rev = t(ws(92)) - 0.1            # "Kali ini" -> flip to gift
scr = f"""
tl.fromTo("#s8-bg",{{scale:1.1}},{{scale:1,duration:{e-s:.2f},ease:"none"}},0);
tl.fromTo("#s8-her",{{scale:0}},{{scale:1,duration:.5,ease:"back.out(2)"}},0.0);
"""
for k, (nm, x, y) in enumerate(nodes):
    scr += f'tl.fromTo("#s8-n{k}",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.35,ease:"back.out(2)"}},{0.25 + k*0.18:.2f});\n'
    scr += f'tl.fromTo("#s8-ln{k}",{{strokeDashoffset:0}},{{strokeDashoffset:-80,duration:{rev:.2f},ease:"none"}},0);\n'
    scr += f'tl.fromTo("#s8-dt{k}",{{x:0,y:0,opacity:1}},{{x:{x-cx},y:{y-cy},duration:.6,ease:"power2.in",repeat:2,repeatDelay:.05}},{0.5 + k*0.12:.2f});\n'
scr += f"""
tl.fromTo("#s8-q",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.45,ease:"power3.out"}},{t(ws(89))-0.1:.2f});
tl.to("#s8-her",{{scale:1.12,duration:.3,ease:"power2.out"}},{rev-0.35:.2f});
tl.to("#s8-diagram",{{opacity:0,scale:1.1,duration:.35,ease:"power2.in"}},{rev:.2f});
tl.fromTo("#s8-gift",{{opacity:0}},{{opacity:1,duration:.35}},{rev:.2f});
tl.fromTo("#s8-photo",{{scale:1.15}},{{scale:1.02,duration:{e-s-rev:.2f},ease:"power1.out"}},{rev:.2f});
tl.fromTo("#s8-k1",{{opacity:0}},{{opacity:1,duration:.5}},{rev+0.1:.2f});
tl.fromTo("#s8-k2",{{opacity:0,y:40,filter:"blur(12px)",backgroundPosition:"100% 0"}},{{opacity:1,y:0,filter:"blur(0px)",backgroundPosition:"0% 0",duration:.8,ease:"expo.out"}},{t(ws(96))-0.1:.2f});
"""
scenes.append(("s8", s, e - s, scene("s8", e - s, body, scr, css8)))
S8_REV, S8_DIA = s + rev, s + t(ws(96)) - 0.1

# ---------------------------------------------------------------- S9 CTA + END CARD
s, e = scenes[-1][1] + scenes[-1][2], TOTAL
t = lambda x: round(x - s, 3)
endc = t(we(111)) + 0.05
bag = """<svg viewBox="0 0 200 220" width="300" height="330"><path d="M30 70 h140 l12 140 h-164z" fill="#FFC629"/><path d="M30 70 h140 l12 140 h-164z" fill="url(#s9-bg)" opacity=".35"/><path d="M68 92 V58 a32 32 0 0 1 64 0 V92" stroke="#1A1210" stroke-width="10" fill="none" stroke-linecap="round"/><defs><linearGradient id="s9-bg" x1="0" x2="1"><stop offset="0" stop-color="#fff"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient></defs></svg>"""
body = f"""
<div class="full onyx"></div>
<img class="full" src="assets/img/flatlay_wood_blur.jpg" style="object-fit:cover;opacity:.3">
{GRAIN.format(id='s9')}
{FRAME.format(id='s9')}
<div id="s9-cta" class="full">
  <div id="s9-bagwrap" class="abs" style="left:390px;top:230px;width:300px;height:330px">{bag}
    <div id="s9-rip1" class="ring9"></div><div id="s9-rip2" class="ring9"></div>
  </div>
  <div id="s9-tekan" class="abs center serif" style="top:600px;font-size:70px;font-weight:600">Tekan <span class="ital" style="color:#FFC629">beg kuning</span></div>
  <div id="s9-btn" class="abs" style="left:190px;top:720px;width:700px;height:130px;border-radius:999px;background:linear-gradient(100deg,#B98C3E,#F1D79A 45%,#C79A4B);display:flex;align-items:center;justify-content:center;box-shadow:0 20px 60px rgba(201,162,94,.35)">
    <span style="font-size:44px;font-weight:800;letter-spacing:.2em;color:#16100C">CHECKOUT SEKARANG</span>
  </div>
  <div id="s9-tap" class="abs" style="left:700px;top:790px;width:70px;height:70px;border-radius:50%;background:rgba(255,255,255,.85);box-shadow:0 0 0 12px rgba(255,255,255,.25);opacity:0"></div>
  <div id="s9-stock" class="abs" style="left:190px;top:900px;width:700px">
    <div style="text-align:center"><div class="label" style="font-size:30px">Stok</div><div class="ital" style="font-size:56px;color:#F4EEE3;margin-top:6px">sangat-sangat <span class="gold" style="font-weight:700">terhad</span></div></div>
    <div style="margin-top:16px;height:14px;border-radius:999px;background:rgba(255,255,255,.12);overflow:hidden"><div id="s9-bar" style="height:14px;width:700px;border-radius:999px;background:linear-gradient(90deg,#C0392B,#E9CF94);transform-origin:0 50%"></div></div>
  </div>
</div>
<div id="s9-end" class="full" style="opacity:0">
  <img id="s9-logo" class="abs" src="assets/img/logo.jpg" style="left:240px;top:190px;width:600px;height:600px;mix-blend-mode:screen">
  <img class="abs" src="assets/img/noche_cut.png" style="left:300px;top:760px;width:190px;height:542px;transform:rotate(-4deg)">
  <img class="abs" src="assets/img/glory_cut.png" style="left:590px;top:760px;width:190px;height:542px;transform:rotate(4deg)">
</div>
"""
css9 = """.ring9{position:absolute;left:150px;top:180px;width:340px;height:340px;margin:-170px 0 0 -170px;border-radius:50%;border:3px solid rgba(255,198,41,.9)}"""
bag_t, chk_t, stk_t = t(ws(100)) - 0.12, t(ws(104)), t(ws(106)) - 0.1
scr = f"""
tl.fromTo("#s9-frame",{{strokeDashoffset:5648}},{{strokeDashoffset:0,duration:1.4,ease:"power3.inOut"}},0);
tl.fromTo("#s9-tekan",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.35,ease:"power3.out"}},0.02);
tl.fromTo("#s9-bagwrap",{{opacity:0,y:-160,scale:.6}},{{opacity:1,y:0,scale:1,duration:.55,ease:"back.out(2.4)"}},{bag_t:.2f});
tl.fromTo("#s9-rip1",{{scale:.5,opacity:1}},{{scale:1.5,opacity:0,duration:.8,ease:"power2.out"}},{bag_t+0.4:.2f});
tl.fromTo("#s9-rip2",{{scale:.5,opacity:1}},{{scale:1.5,opacity:0,duration:.8,ease:"power2.out"}},{bag_t+0.75:.2f});
tl.to("#s9-bagwrap",{{scale:1.06,duration:.25,ease:"power2.out",yoyo:true,repeat:5}},{bag_t+0.6:.2f});
tl.fromTo("#s9-btn",{{opacity:0,y:40,scale:.92}},{{opacity:1,y:0,scale:1,duration:.4,ease:"expo.out"}},{chk_t-0.45:.2f});
tl.fromTo("#s9-tap",{{opacity:0,scale:1.6}},{{opacity:1,scale:1,duration:.15}},{chk_t-0.15:.2f});
tl.to("#s9-btn",{{scale:.94,duration:.08,ease:"power2.in"}},{chk_t:.2f});
tl.to("#s9-btn",{{scale:1,duration:.25,ease:"back.out(3)"}},{chk_t+0.08:.2f});
tl.to("#s9-tap",{{opacity:0,duration:.25}},{chk_t+0.2:.2f});
tl.fromTo("#s9-stock",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.4,ease:"power3.out"}},{stk_t:.2f});
tl.fromTo("#s9-bar",{{scaleX:1}},{{scaleX:.12,duration:{t(we(111))-stk_t:.2f},ease:"power2.inOut"}},{stk_t+0.1:.2f});
tl.to("#s9-cta",{{opacity:0,scale:.96,duration:.3,ease:"power2.in"}},{endc:.2f});
tl.fromTo("#s9-end",{{opacity:0}},{{opacity:1,duration:.35}},{endc:.2f});
tl.fromTo("#s9-logo",{{scale:1.2,filter:"blur(10px)"}},{{scale:1,filter:"blur(0px)",duration:.6,ease:"expo.out"}},{endc:.2f});
"""
scenes.append(("s9", s, e - s, scene("s9", e - s, body, scr, css9)))
S9_BAG, S9_CHK, S9_END = s + bag_t, s + chk_t, s + endc

# ---------------------------------------------------------------- CAPTIONS
groups = [(0,0),(1,3),(4,6),(7,9),(10,12),(13,14),(15,18),(19,21),(22,24),(25,27),(28,31),(32,34),(35,36),(37,40),(41,43),(44,45),(46,48),
          (49,51),(52,53),(54,55),(56,56),(57,58),(59,62),(63,65),(66,68),(69,70),(71,73),(74,77),(78,80),(81,82),(83,84),(85,88),(89,91),(92,95),(96,98),
          (99,102),(103,105),(106,108),(109,111)]
FIX = {"istri": "isteri", "bombshell": "Bombshell", "korang": "korang,"}
KEY = {"penat.", "habis.", "berehat", "diri", "sendiri.", "manjakan", "dirinya.", "Frescura", "Body", "buih", "lembut", "gebu", "Bombshell", "Midnight", "Fantasy.", "dia", "pula.", "terhad.", "kuning", "checkout"}
# merge hyphen pairs / mis-heard words into display tokens: (first_idx, last_idx, text)
def tokens(a, b):
    out = []; i = a
    while i <= b:
        tx = W[i]["text"]
        if i + 1 <= b and W[i+1]["text"].startswith("-"):
            out.append((i, i+1, tx + W[i+1]["text"])); i += 2; continue
        if i == 59:  # whisper: "niat mati" = "nikmati"
            out.append((59, 60, "nikmati")); i += 2; continue
        out.append((i, i, FIX.get(tx, tx))); i += 1
    return out
cap_html, cap_scr = [], []
for g, (a, b) in enumerate(groups):
    g0 = max(0.12, ws(a) - 0.06)
    nxt = ws(groups[g+1][0]) - 0.06 if g + 1 < len(groups) else we(b) + 0.5
    g1 = min(nxt, we(b) + 0.6)
    spans = []
    toks = tokens(a, b)
    for k, (i0, i1, tx) in enumerate(toks):
        cls = "cw key" if tx.strip(",.") in {x.strip(",.") for x in KEY} else "cw"
        spans.append(f'<span class="{cls}" id="cap-{g}-{k}">{html.escape(tx)}</span>')
    cap_html.append(f'<div class="cg" id="cap-{g}">{" ".join(spans)}</div>')
    cap_scr.append(f'tl.fromTo("#cap-{g}",{{opacity:0,y:18,visibility:"visible"}},{{opacity:1,y:0,duration:.14,ease:"power2.out"}},{g0:.3f});')
    for k, (i0, i1, tx) in enumerate(toks):
        cap_scr.append(f'tl.to("#cap-{g}-{k}",{{opacity:1,color:"#F0D49A",scale:1.06,duration:.08}},{ws(i0)-0.02:.3f});')
        cap_scr.append(f'tl.to("#cap-{g}-{k}",{{color:"#F7F1E6",scale:1,duration:.12}},{we(i1)+0.02:.3f});')
    cap_scr.append(f'tl.to("#cap-{g}",{{opacity:0,duration:.1,ease:"power2.in"}},{g1-0.1:.3f});')
    cap_scr.append(f'tl.set("#cap-{g}",{{opacity:0,visibility:"hidden"}},{g1:.3f});')
cap_css = BASE_CSS + """
#capbox{position:absolute;left:60px;width:960px;top:1125px;height:190px;display:flex;align-items:center;justify-content:center}
.cg{position:absolute;left:0;width:960px;top:0;height:190px;display:flex;flex-wrap:wrap;align-content:center;justify-content:center;column-gap:20px;row-gap:0;opacity:0;visibility:hidden;text-align:center}
.cw{display:inline-block;font-family:'Manrope',sans-serif;font-weight:800;font-size:68px;line-height:1.12;letter-spacing:-.01em;color:#F7F1E6;opacity:.6;text-shadow:0 4px 22px rgba(0,0,0,.75),0 1px 3px rgba(0,0,0,.6)}
.cw.key{font-family:'Bodoni Moda',serif;font-style:italic;font-weight:600;font-size:82px;letter-spacing:0}
"""
captions = f"""<template>
<style>{cap_css}</style>
<div id="root" data-composition-id="captions" data-width="1080" data-height="1920" data-duration="{TOTAL}">
<div id="capbox" data-layout-allow-overflow>
{chr(10).join(cap_html)}
</div>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(cap_scr)}
window.__timelines["captions"] = tl;
</script>
</template>
"""

# ---------------------------------------------------------------- SFX (peak lands ~1 frame after the picture)
DUR = {"chime":2.54,"click-soft":0.37,"click":0.37,"impact-bass-1":2.12,"key-press":0.43,"notification":2.46,"ping":1.32,"pop":0.72,"riser":10.03,"sparkle":1.80,"whoosh-short":0.57,"whoosh":0.57}
PEAK = {"impact-bass-1":0.073,"whoosh":0.162,"whoosh-short":0.162,"click":0.073,"click-soft":0.073,"ping":0.324,"chime":0.418,
        "sparkle":0.027,"pop":0.12,"riser":3.472,"notification":0.229,"key-press":0.076}
sfx = []
def fx(name, at, vol, dur=None, fade_out=None):
    st = round(at - PEAK[name] + 0.033, 3)
    sfx.append((name, max(0.0, st), vol, dur or DUR[name], fade_out))
s1 = 0
fx("impact-bass-1", 0.02, 0.42)
fx("whoosh", ws(1), 0.55)
fx("whoosh-short", ws(4)-0.05, 0.5)
for k, x in enumerate([ws(7)-0.05, ws(7)-0.05+(ws(10)-ws(7))/2, ws(7)-0.05+(ws(10)-ws(7))]): fx("pop", x, 0.75)
fx("click", ws(14)+0.05, 1.0)
fx("whoosh", scenes[1][1], 0.6)
for k, x in enumerate(CHORE_TICKS): fx("click-soft" if k % 2 else "key-press", x, 0.95 if k % 2 else 1.0)
fx("impact-bass-1", ws(25), 0.25)
fx("whoosh", scenes[2][1], 0.6)
fx("ping", ws(29), 0.6); fx("ping", ws(31), 0.5)
fx("whoosh-short", ws(37)-0.2, 0.45)
fx("chime", ws(44)-0.05, 0.9)
fx("whoosh", scenes[3][1], 0.6)
fx("sparkle", ws(54), 0.35)
fx("riser", S5_LOGO, 0.3, dur=round(PEAK["riser"]+0.1,2), fade_out=0.12)
fx("impact-bass-1", S5_LOGO, 0.5)
fx("sparkle", S5_LOGO+0.05, 0.35)
fx("whoosh", S5_HERO, 0.55)
fx("sparkle", ws(64), 0.3)
fx("whoosh-short", scenes[5][1], 0.55)
fx("pop", S6_P1, 1.0); fx("pop", S6_P2, 1.0)
fx("whoosh-short", S6_CUT, 0.45)
fx("pop", ws(75), 0.7); fx("sparkle", ws(77), 0.35)
fx("whoosh", scenes[6][1], 0.55)
fx("whoosh-short", S7_C1, 0.6); fx("ping", S7_C1+0.15, 0.5)
fx("whoosh-short", S7_C2, 0.6); fx("ping", S7_C2+0.15, 0.5)
fx("whoosh", scenes[7][1], 0.55)
for k in range(4): fx("pop", scenes[7][1] + 0.25 + k*0.18, 0.55)
fx("whoosh", S8_REV, 0.6)
fx("chime", S8_DIA, 0.9)
fx("whoosh-short", scenes[8][1], 0.55)
fx("notification", S9_BAG+0.2, 0.75)
fx("click", S9_CHK, 1.0)
fx("impact-bass-1", ws(111), 0.3, dur=1.8, fade_out=0.4)
fx("sparkle", S9_END, 0.4, dur=1.4, fade_out=0.3)

# ---------------------------------------------------------------- INDEX
hosts = "\n".join(
    f'      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{st:.3f}" data-duration="{du:.3f}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:1"></div>'
    for sid, st, du, _ in scenes)
audio = "\n".join(
    f'      <audio id="sfx{k}" class="clip" src="assets/sfx/{n}.mp3" data-start="{st:.3f}"' + (f' data-duration="{d}"' if d else "") +
    f' data-track-index="{4 + k % 3}" data-volume="{v}"' + (f' data-fade-out="{fo}"' if fo else "") + '></audio>'
    for k, (n, st, v, d, fo) in enumerate(sfx))
index = f"""<!doctype html>
<html lang="ms">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #090808; }}
      #main {{ position: relative; width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <div id="main" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920" data-fps="30">
{hosts}
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:5"></div>
      <audio id="voice" class="clip" src="assets/audio/voice.wav" data-start="{VOFF}" data-track-index="3" data-volume="1"></audio>
{audio}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
os.makedirs(f"{ROOT}/compositions", exist_ok=True)
for sid, st, du, h in scenes:
    open(f"{ROOT}/compositions/{sid}.html", "w").write(h)
open(f"{ROOT}/compositions/captions.html", "w").write(captions)
open(f"{ROOT}/index.html", "w").write(index)
for sid, st, du, _ in scenes: print(f"{sid}: {st:6.2f} -> {st+du:6.2f}")
print("sfx:", len(sfx), "captions:", len(groups))
