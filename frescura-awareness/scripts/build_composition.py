#!/usr/bin/env python3
"""Generates the FRESCURA BODY awareness film (HyperFrames project) from the edited transcript."""
import json, os, sys
P = sys.argv[1]
W = json.load(open(os.path.join(P, "transcript.json")))
DUR = 44.0
os.makedirs(os.path.join(P, "compositions"), exist_ok=True)

FONTS = """
@font-face{font-family:'Bodoni Moda';src:url('assets/fonts/bodoni-moda-latin-400-normal.woff2') format('woff2');font-weight:400;font-style:normal}
@font-face{font-family:'Bodoni Moda';src:url('assets/fonts/bodoni-moda-latin-500-normal.woff2') format('woff2');font-weight:500;font-style:normal}
@font-face{font-family:'Bodoni Moda';src:url('assets/fonts/bodoni-moda-latin-700-normal.woff2') format('woff2');font-weight:700;font-style:normal}
@font-face{font-family:'Bodoni Moda';src:url('assets/fonts/bodoni-moda-latin-400-italic.woff2') format('woff2');font-weight:400;font-style:italic}
@font-face{font-family:'Bodoni Moda';src:url('assets/fonts/bodoni-moda-latin-500-italic.woff2') format('woff2');font-weight:500;font-style:italic}
@font-face{font-family:'Bodoni Moda';src:url('assets/fonts/bodoni-moda-latin-700-italic.woff2') format('woff2');font-weight:700;font-style:italic}
@font-face{font-family:'Italiana';src:url('assets/fonts/italiana-latin-400-normal.woff2') format('woff2');font-weight:400}
@font-face{font-family:'Manrope';src:url('assets/fonts/manrope-latin-400-normal.woff2') format('woff2');font-weight:400}
@font-face{font-family:'Manrope';src:url('assets/fonts/manrope-latin-600-normal.woff2') format('woff2');font-weight:600}
@font-face{font-family:'Manrope';src:url('assets/fonts/manrope-latin-800-normal.woff2') format('woff2');font-weight:800}
"""
TOKENS = """
--ivory:#F4EFE8; --paper:#FBF8F3; --ink:#171212; --wine:#6E0F1F; --rose:#C23A4B;
--gold:#B89463; --sea:#0F2E37; --sea2:#1D5361; --muted:#8B8079; --yellow:#F2C230;
"""
BASE = """
.lbl{font-family:'Manrope';font-weight:600;font-size:30px;letter-spacing:.32em;text-transform:uppercase}
.disp{font-family:'Bodoni Moda';font-weight:500;line-height:.95;letter-spacing:-.01em}
.it{font-family:'Bodoni Moda';font-style:italic;font-weight:400}
.ital{font-family:'Italiana';letter-spacing:.42em;text-transform:uppercase}
.abs{position:absolute}
.hair{position:absolute;height:2px;background:var(--gold);transform-origin:left center}
"""

def word(text, i=0):
    """film time of the i-th occurrence of a transcript word"""
    hits = [x for x in W if x["text"] == text]
    return hits[i]["start"]

def scene(sid, start, end, css, html, js, bg="transparent"):
    body = f"""<template>
  <style>
{FONTS}
    #root{{position:absolute;inset:0;overflow:hidden;background:{bg};{TOKENS}}}
{BASE}
{css}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
{'<div class="abs" style="left:0;top:1180px;width:1080px;height:740px;background:linear-gradient(180deg,rgba(23,18,18,0) 0%,rgba(23,18,18,.62) 45%,rgba(23,18,18,.7) 100%)"></div>' if bg=="transparent" else ''}
{html}
  </div>
  <script>
  (function(){{
    const T0={start};
    const at=t=>Math.max(0,+(t-T0).toFixed(3));
    const tl=gsap.timeline({{paused:true}});
    let seed=7; const rnd=()=>{{seed=(seed*16807)%2147483647;return (seed-1)/2147483646;}};
{js}
    tl.set({{}},{{}},{round(end-start,3)});
    window.__timelines["{sid}"]=tl;
  }})();
  </script>
</template>
"""
    open(os.path.join(P, "compositions", f"{sid}.html"), "w").write(body)
    return dict(id=sid, start=start, end=end)

SC = []

# ---------------------------------------------------------------- S1 HOOK
t_tak = word("tak"); t_sama = word("sama")
SC.append(scene("hook", 0.0, word("Garam", 1), """
#h-top{left:0;top:-60px;width:1080px;height:1030px;background:radial-gradient(120% 90% at 50% 30%, var(--sea2) 0%, var(--sea) 70%)}
#h-bot{left:0;top:960px;width:1080px;height:960px;background:var(--ivory)}
#h-l1{left:0;width:1080px;top:470px;text-align:center;color:var(--ivory);font-size:150px}
#h-l2{left:0;width:1080px;top:1110px;text-align:center;color:var(--ink);font-size:150px}
#h-k1{left:0;width:1080px;top:395px;text-align:center;color:var(--gold)}
#h-k2{left:0;width:1080px;top:1300px;text-align:center;color:var(--wine)}
#h-neq{left:430px;top:850px;width:220px;height:220px;border-radius:50%;background:var(--wine);color:var(--ivory);
  display:flex;align-items:center;justify-content:center;font-family:'Bodoni Moda';font-size:150px;line-height:1;padding-bottom:18px;box-shadow:0 20px 60px rgba(0,0,0,.25)}
#h-brand{left:0;width:1080px;top:215px;text-align:center;color:rgba(244,239,232,.8);font-size:30px}
#h-q{left:0;width:1080px;top:1380px;text-align:center;color:var(--muted);font-size:30px}
.h-grain{position:absolute;width:10px;height:10px;background:rgba(244,239,232,.55);transform:rotate(45deg)}
""", """
    <div id="h-top" class="abs"></div><div id="h-bot" class="abs"></div>
    <div id="h-grains" class="abs" style="inset:0"></div>
    <div id="h-brand" class="abs ital">Frescura Body</div>
    <div id="h-k1" class="abs lbl">Sea salt</div>
    <div id="h-l1" class="abs disp it">Garam Laut</div>
    <div id="h-k2" class="abs lbl">Table salt</div>
    <div id="h-l2" class="abs disp">Garam Dapur</div>
    <div id="h-neq" class="abs">&ne;</div>
    <div id="h-q" class="abs lbl">tak sama.</div>
""", f"""
    const g=document.getElementById('h-grains');
    for(let i=0;i<26;i++){{const d=document.createElement('div');d.className='h-grain';d.id='h-g'+i;
      d.style.left=(60+rnd()*960)+'px';d.style.top=(120+rnd()*720)+'px';const s=4+rnd()*10;d.style.width=s+'px';d.style.height=s+'px';g.appendChild(d);}}
    // frame 0 already shows the hook line (thumbnail)
    tl.fromTo('#h-l1',{{y:30,scale:1.06}},{{y:0,scale:1,duration:1.2,ease:'expo.out'}},0);
    tl.fromTo('#h-l2',{{y:40,scale:1.06}},{{y:0,scale:1,duration:1.2,ease:'expo.out'}},0);
    tl.fromTo('#h-k2',{{opacity:0}},{{opacity:1,duration:.3}},at({word("dapur")}));
    tl.fromTo('#h-neq',{{scale:0,rotation:-90}},{{scale:1,rotation:0,duration:.5,ease:'back.out(1.6)'}},at({t_tak}));
    tl.fromTo('#h-q',{{opacity:0,scale:1.3,filter:'blur(8px)'}},{{opacity:1,scale:1,filter:'blur(0px)',duration:.4,ease:'power3.out'}},at({word('itu')}));
    for(let i=0;i<26;i++) tl.fromTo('#h-g'+i,{{y:0,opacity:.9}},{{y:-60-rnd()*90,opacity:.2,duration:2.3,ease:'none'}},0);
    tl.to('#h-top',{{y:-30,duration:2.3,ease:'none'}},0);
"""))

# ---------------------------------------------------------------- S2 TABLE SALT (processed)
s, e = word("Garam", 1), word("Garam", 2)
t_proc = word("diproses"); t_keb = word("kebanyakan"); t_hil = word("hilang")
SC.append(scene("dapur", s, e, """
#d-num{left:90px;top:230px;color:var(--wine)}
#d-title{left:90px;top:285px;color:var(--ink);font-size:118px}
#d-belt{left:60px;top:880px;width:960px;height:4px;background:var(--ink)}
#d-gate{left:470px;top:600px;width:140px;height:300px;border:4px solid var(--ink);border-bottom:none;
  background:repeating-linear-gradient(135deg, transparent 0 14px, rgba(23,18,18,.14) 14px 18px)}
#d-gatel{left:400px;top:550px;width:280px;text-align:center;color:var(--ink);font-size:28px}
#d-cube{left:150px;top:700px;width:170px;height:170px;background:#fff;border:4px solid var(--ink);border-radius:18px;
  box-shadow:inset -18px -18px 0 rgba(23,18,18,.06)}
.d-chip{position:absolute;width:84px;height:84px;border-radius:50%;display:flex;align-items:center;justify-content:center;
  font-family:'Bodoni Moda';font-weight:700;font-size:34px;color:var(--ivory);background:var(--sea2)}
#d-meter{left:90px;top:990px;width:900px}
#d-mlbl{color:var(--ink);font-size:30px}
#d-track{margin-top:18px;width:900px;height:22px;border-radius:11px;background:rgba(23,18,18,.08);overflow:hidden}
#d-fill{width:900px;height:22px;border-radius:11px;background:var(--sea2);transform-origin:left center}
#d-lost{left:90px;top:1080px;color:var(--rose);font-size:62px}
""", """
    <div id="d-num" class="abs lbl">01 &mdash; Garam dapur</div>
    <div id="d-title" class="abs disp">Diproses<span class="it" style="color:var(--wine)">.</span></div>
    <div id="d-gatel" class="abs lbl">Proses</div>
    <div id="d-gate" class="abs"></div>
    <div id="d-belt" class="abs"></div>
    <div id="d-cube" class="abs"></div>
    <div id="d-c0" class="d-chip">Mg</div><div id="d-c1" class="d-chip">Ca</div><div id="d-c2" class="d-chip">K</div>
    <div id="d-meter" class="abs"><div id="d-mlbl" class="lbl">Mineral</div><div id="d-track"><div id="d-fill"></div></div></div>
    <div id="d-lost" class="abs disp it">kebanyakannya hilang</div>
""", f"""
    const pos=[[120,610],[300,610],[300,790]];
    pos.forEach((p,i)=>{{const c=document.getElementById('d-c'+i);c.style.left=p[0]+'px';c.style.top=p[1]+'px';}});
    tl.fromTo('#d-num',{{opacity:0,x:-30}},{{opacity:1,x:0,duration:.4,ease:'power3.out'}},0.05);
    tl.fromTo('#d-title',{{opacity:0,filter:'blur(10px)'}},{{opacity:1,filter:'blur(0px)',duration:.35,ease:'power3.out'}},0.12);
    tl.fromTo('#d-belt',{{scaleX:0}},{{scaleX:1,duration:.6,ease:'power3.inOut',transformOrigin:'left center'}},0.1);
    tl.fromTo(['#d-gate','#d-gatel'],{{opacity:0,y:-40}},{{opacity:1,y:0,duration:.5,ease:'expo.out'}},0.3);
    tl.fromTo('#d-cube',{{x:-260,rotation:-8}},{{x:0,rotation:0,duration:.6,ease:'expo.out'}},0.15);
    pos.forEach((p,i)=>tl.fromTo('#d-c'+i,{{x:-260,scale:0}},{{x:0,scale:1,duration:.5,ease:'back.out(1.7)'}},0.25+i*.08));
    tl.fromTo('#d-meter',{{opacity:0}},{{opacity:1,duration:.3}},0.5);
    // into the process gate
    tl.to('#d-cube',{{x:320,duration:.9,ease:'power2.inOut'}},at({t_proc}));
    pos.forEach((p,i)=>tl.to('#d-c'+i,{{x:320,duration:.9,ease:'power2.inOut'}},at({t_proc})));
    tl.to('#d-gate',{{backgroundPosition:'80px 0px',duration:.9,ease:'none'}},at({t_proc}));
    // stripped off: minerals fall and grey out
    pos.forEach((p,i)=>tl.to('#d-c'+i,{{y:520,rotation:(i-1)*40,backgroundColor:'#BDB4AC',opacity:0,duration:.9,ease:'power3.in'}},at({t_keb})+i*.1));
    tl.to('#d-cube',{{x:620,duration:.9,ease:'power2.inOut'}},at({t_keb}));
    tl.fromTo('#d-fill',{{scaleX:1}},{{scaleX:.08,backgroundColor:'#C23A4B',duration:1.0,ease:'power2.inOut'}},at({t_keb}));
    tl.fromTo('#d-lost',{{opacity:0,y:30}},{{opacity:1,y:0,duration:.35,ease:'power4.out'}},at({word('mineralnya')})-.1);
""", bg="var(--ivory)"))

# ---------------------------------------------------------------- S3 SEA SALT (evaporated)
s, e = word("Garam", 2), word("Jadi")
t_sej = word("disejat"); t_air = word("air"); t_min = word("mineral")
SC.append(scene("laut", s, e, """
#l-num{left:90px;top:230px;color:var(--gold)}
#l-title{left:90px;top:285px;color:var(--ivory);font-size:118px}
#l-sub{left:90px;top:420px;color:rgba(244,239,232,.75);font-size:52px}
#l-sun{left:760px;top:500px;width:180px;height:180px;border-radius:50%;background:radial-gradient(circle, #F1DDB4 0%, var(--gold) 60%, rgba(184,148,99,0) 72%)}
.l-wave{position:absolute;left:-1080px;width:3240px;height:220px}
.l-steam{position:absolute;width:8px;height:8px;border-radius:50%;background:rgba(244,239,232,.8)}
.l-cry{position:absolute;width:44px;height:44px;background:linear-gradient(135deg,#fff 0%, #E9DDC9 55%, var(--gold) 100%);transform:rotate(45deg);box-shadow:0 0 30px rgba(241,221,180,.6)}
#l-tag{left:0;width:1080px;top:1060px;text-align:center;color:var(--gold);font-size:64px}
""", """
    <div id="l-sun" class="abs"></div>
    <div id="l-steams" class="abs" style="inset:0"></div>
    <svg id="l-w1" class="l-wave" style="top:820px" viewBox="0 0 3240 220" preserveAspectRatio="none"><path fill="#1D5361" d="M0 80 Q 135 20 270 80 T 540 80 T 810 80 T 1080 80 T 1350 80 T 1620 80 T 1890 80 T 2160 80 T 2430 80 T 2700 80 T 2970 80 T 3240 80 V220 H0Z"/></svg>
    <svg id="l-w2" class="l-wave" style="top:880px" viewBox="0 0 3240 220" preserveAspectRatio="none"><path fill="#2A6B78" d="M0 70 Q 180 10 360 70 T 720 70 T 1080 70 T 1440 70 T 1800 70 T 2160 70 T 2520 70 T 2880 70 T 3240 70 V220 H0Z"/></svg>
    <div class="abs" style="left:0;top:1080px;width:1080px;height:840px;background:#2A6B78"></div>
    <div id="l-crys" class="abs" style="inset:0"></div>
    <div id="l-num" class="abs lbl">02 &mdash; Garam laut</div>
    <div id="l-title" class="abs disp it">Disejat terus</div>
    <div id="l-sub" class="abs disp">dari air laut</div>
    <div id="l-tag" class="abs disp it">= mineral</div>
""", f"""
    const st=document.getElementById('l-steams');
    for(let i=0;i<34;i++){{const d=document.createElement('div');d.className='l-steam';d.id='l-s'+i;d.style.left=(80+rnd()*920)+'px';d.style.top=(820+rnd()*60)+'px';st.appendChild(d);
      tl.fromTo('#l-s'+i,{{y:0,opacity:0,scale:.6}},{{y:-240-rnd()*200,opacity:.85,scale:1.3,duration:1.6+rnd(),ease:'power1.out'}},at({t_sej})+rnd()*1.2);}}
    const cr=document.getElementById('l-crys');
    const cp=[[250,690],[420,620],[600,700],[770,640],[520,560]];
    cp.forEach((p,i)=>{{const d=document.createElement('div');d.className='l-cry';d.id='l-c'+i;d.style.left=p[0]+'px';d.style.top=p[1]+'px';cr.appendChild(d);
      tl.fromTo('#l-c'+i,{{scale:0,rotation:0}},{{scale:1,rotation:45,duration:.5,ease:'back.out(2)'}},at({t_min})-.15+i*.06);}});
    tl.fromTo('#l-w1',{{x:0}},{{x:540,duration:{e-s:.2f},ease:'none'}},0);
    tl.fromTo('#l-w2',{{x:0}},{{x:-720,duration:{e-s:.2f},ease:'none'}},0);
    tl.fromTo('#l-sun',{{y:120,opacity:0}},{{y:0,opacity:1,duration:1.0,ease:'expo.out'}},0);
    tl.fromTo('#l-num',{{opacity:0,x:-30}},{{opacity:1,x:0,duration:.4,ease:'power3.out'}},0.05);
    tl.fromTo('#l-title',{{opacity:0,filter:'blur(10px)'}},{{opacity:1,filter:'blur(0px)',duration:.35,ease:'power3.out'}},at({t_sej})-.1);
    tl.fromTo('#l-sub',{{opacity:0,y:20}},{{opacity:1,y:0,duration:.35,ease:'power3.out'}},at({word('terus')}));
    tl.fromTo('#l-tag',{{opacity:0,scale:.8}},{{opacity:1,scale:1,duration:.4,ease:'expo.out'}},at({word('jadi')})-.1);
""", bg="radial-gradient(130% 80% at 50% 20%, #1D5361 0%, #0F2E37 70%)"))

# ---------------------------------------------------------------- S4 MINERALS STAY
s, e = word("Jadi"), word("Sebab")
t_m = word("mineral", 1); t_sem = word("semula"); t_mas = word("masih"); t_ada = word("ada")
SC.append(scene("mineral", s, e, """
#m-core{left:400px;top:520px;width:280px;height:280px;transform:rotate(45deg);
  background:linear-gradient(135deg,#fff 0%, #EFE5D6 50%, var(--gold) 100%);box-shadow:0 30px 80px rgba(110,15,31,.18)}
.m-el{position:absolute;width:250px;height:150px;border:2px solid var(--ink);border-radius:20px;background:var(--paper);padding:18px 22px}
.m-sym{font-family:'Bodoni Moda';font-weight:700;font-size:64px;color:var(--wine);line-height:1}
.m-nm{font-family:'Manrope';font-weight:600;font-size:28px;letter-spacing:.06em;text-transform:uppercase;color:var(--ink);margin-top:10px}
#m-title{left:0;width:1080px;top:230px;text-align:center;color:var(--ink);font-size:92px}
#m-stamp{left:290px;top:1050px;width:500px;height:120px;border:5px solid var(--wine);border-radius:60px;color:var(--wine);
  display:flex;align-items:center;justify-content:center;font-family:'Manrope';font-weight:800;font-size:48px;letter-spacing:.14em}
""", """
    <div id="m-title" class="abs disp">Mineral <span class="it" style="color:var(--wine)">semula jadi</span></div>
    <div id="m-core" class="abs"></div>
    <div id="m-e0" class="m-el"><div class="m-sym">Mg</div><div class="m-nm">Magnesium</div></div>
    <div id="m-e1" class="m-el"><div class="m-sym">Ca</div><div class="m-nm">Kalsium</div></div>
    <div id="m-e2" class="m-el"><div class="m-sym">K</div><div class="m-nm">Kalium</div></div>
    <div id="m-e3" class="m-el"><div class="m-sym">Na</div><div class="m-nm">Natrium</div></div>
    <div id="m-stamp" class="abs">&#10003; MASIH ADA</div>
""", f"""
    const P=[[90,440],[740,440],[90,780],[740,780]], F=[[-400,0],[400,0],[-400,0],[400,0]];
    P.forEach((p,i)=>{{const c=document.getElementById('m-e'+i);c.style.left=p[0]+'px';c.style.top=p[1]+'px';}});
    tl.fromTo('#m-core',{{scale:0,rotation:0}},{{scale:1,rotation:45,duration:.6,ease:'expo.out'}},0);
    tl.fromTo('#m-title',{{opacity:0,filter:'blur(10px)'}},{{opacity:1,filter:'blur(0px)',duration:.35}},at({t_m})-.1);
    P.forEach((p,i)=>tl.fromTo('#m-e'+i,{{x:F[i][0],opacity:0}},{{x:0,opacity:1,duration:.45,ease:'expo.out'}},at({t_sem})+i*.16));
    tl.fromTo('#m-stamp',{{scale:1.8,opacity:0,rotation:-8}},{{scale:1,opacity:1,rotation:-3,duration:.28,ease:'power4.in'}},at({t_mas})-.1);
""", bg="var(--ivory)"))

# ---------------------------------------------------------------- S5 SPA (footage overlay)
s, e = word("Sebab"), word("spa") + 0.32
t_kul = word("penjagaan"); t_spa = word("spa")
SC.append(scene("spa", s, e, """
#sp-scrim{left:0;top:0;width:1080px;height:760px;background:linear-gradient(180deg, rgba(23,18,18,.55) 0%, rgba(23,18,18,0) 100%)}
#sp-k{left:0;width:1080px;top:230px;text-align:center;color:var(--ivory);font-size:30px}
#sp-t{left:0;width:1080px;top:280px;text-align:center;color:var(--ivory);font-size:96px}
.sp-chip{position:absolute;left:0;width:1080px;text-align:center}
.sp-chip span{display:inline-block;padding:20px 40px;border-radius:60px;background:rgba(251,248,243,.92);color:var(--wine);
  font-family:'Manrope';font-weight:800;font-size:38px;letter-spacing:.16em;text-transform:uppercase}
""", """
    <div id="sp-scrim" class="abs"></div>
    <div id="sp-k" class="abs lbl">Sebab itu</div>
    <div id="sp-t" class="abs disp it">Rahsia spa.</div>
    <div id="sp-c1" class="sp-chip" style="top:470px"><span>Penjagaan kulit</span></div>
    <div id="sp-c2" class="sp-chip" style="top:590px"><span>Rawatan spa</span></div>
""", f"""
    tl.fromTo('#sp-k',{{opacity:0}},{{opacity:1,duration:.3}},0.05);
    tl.fromTo('#sp-t',{{opacity:0,y:30}},{{opacity:1,y:0,duration:.5,ease:'expo.out'}},0.15);
    tl.fromTo('#sp-c1',{{x:-1080}},{{x:0,duration:.5,ease:'expo.out'}},at({t_kul}));
    tl.fromTo('#sp-c2',{{x:1080}},{{x:0,duration:.5,ease:'expo.out'}},at({t_spa})-.15);
"""))

# ---------------------------------------------------------------- S6 BRAND REVEAL (real logo)
s, e = word("spa") + 0.32, word("FRESCURA")
SC.append(scene("brand", s, e, """
#b-glow{left:140px;top:420px;width:800px;height:800px;border-radius:50%;background:radial-gradient(circle, rgba(64,170,255,.28) 0%, rgba(64,170,255,0) 65%)}
#b-logo{left:150px;top:420px;width:780px;height:780px}
#b-flash{left:0;top:0;width:1080px;height:1920px;background:#E8F4FF}
""", """
    <div id="b-glow" class="abs"></div>
    <img id="b-logo" class="abs" src="assets/img/logo.png" alt="FRESCURA BODY">
    <div id="b-flash" class="abs"></div>
""", """
    tl.fromTo('#b-flash',{opacity:.9},{opacity:0,duration:.3,ease:'power2.out'},0);
    tl.fromTo('#b-logo',{opacity:0,scale:1.35,filter:'blur(14px)'},{opacity:1,scale:1,filter:'blur(0px)',duration:.7,ease:'expo.out'},0.02);
    tl.fromTo('#b-glow',{scale:.6,opacity:0},{scale:1,opacity:1,duration:.9,ease:'expo.out'},0.05);
""", bg="#0B111C"))

# ---------------------------------------------------------------- S7 FORMULA (footage overlay)
s, e = word("FRESCURA"), word("Kulit")
t_g = word("garam", 2); t_dig = word("digabungkan"); t_p = word("perfume")
SC.append(scene("formula", s, e, """
#f-scrim{left:0;top:0;width:1080px;height:900px;background:linear-gradient(180deg, rgba(23,18,18,.6) 0%, rgba(23,18,18,0) 100%)}
#f-k{left:0;width:1080px;top:220px;text-align:center;color:var(--gold)}
#f-logo{left:0;width:1080px;top:262px;text-align:center;color:var(--ivory);font-size:74px;letter-spacing:.2em}
.f-pill{position:absolute;top:470px;width:380px;height:150px;border-radius:75px;background:rgba(251,248,243,.94);
  display:flex;flex-direction:column;align-items:center;justify-content:center}
.f-pill b{font-family:'Bodoni Moda';font-style:italic;font-weight:500;font-size:52px;color:var(--wine);line-height:1}
.f-pill i{font-style:normal;font-family:'Manrope';font-weight:600;font-size:28px;letter-spacing:.14em;color:var(--muted);margin-top:8px}
#f-plus{left:490px;top:495px;width:100px;height:100px;border-radius:50%;background:var(--wine);color:var(--ivory);
  font-family:'Manrope';font-weight:800;font-size:64px;display:flex;align-items:center;justify-content:center}
""", """
    <div id="f-scrim" class="abs"></div>
    <div id="f-k" class="abs lbl">Formula</div>
    <div id="f-logo" class="abs ital">Frescura Body</div>
    <div id="f-p1" class="f-pill" style="left:80px"><b>Garam laut</b><i>OCEAN SALT</i></div>
    <div id="f-plus" class="abs">+</div>
    <div id="f-p2" class="f-pill" style="left:620px"><b>Perfume</b><i>FRAGRANCE</i></div>
""", f"""
    tl.fromTo('#f-k',{{opacity:0}},{{opacity:1,duration:.3}},0.05);
    tl.fromTo('#f-logo',{{opacity:0,scale:1.3,filter:'blur(10px)'}},{{opacity:1,scale:1,filter:'blur(0px)',duration:.6,ease:'expo.out'}},0.05);
    tl.fromTo('#f-p1',{{x:-500,opacity:0}},{{x:0,opacity:1,duration:.5,ease:'expo.out'}},at({t_g}));
    tl.fromTo('#f-plus',{{scale:0}},{{scale:1,duration:.4,ease:'back.out(2)'}},at({t_dig}));
    tl.fromTo('#f-p2',{{x:500,opacity:0}},{{x:0,opacity:1,duration:.5,ease:'expo.out'}},at({t_p})-.12);
    // merge into one
    tl.to('#f-p1',{{x:90,scale:.9,duration:.45,ease:'power3.inOut'}},at({t_p})+.75);
    tl.to('#f-p2',{{x:-90,scale:.9,duration:.45,ease:'power3.inOut'}},at({t_p})+.75);
    tl.to('#f-plus',{{rotation:45,duration:.45,ease:'power3.inOut'}},at({t_p})+.75);
"""))

# ---------------------------------------------------------------- S8 FEEL (footage overlay)
s, e = word("Kulit"), word("mandi") + 0.45
t_lem = word("lembut"); t_wan = word("wangi")
SC.append(scene("feel", s, e, """
#fe-scrim{left:0;top:0;width:1080px;height:900px;background:linear-gradient(180deg, rgba(23,18,18,.5) 0%, rgba(23,18,18,0) 100%)}
.fe-w{position:absolute;left:0;width:1080px;text-align:center;color:var(--ivory)}
#fe-1{top:250px;font-size:190px}
#fe-2{top:470px;font-size:190px;color:#F6D9DE}
#fe-k1{left:0;width:1080px;top:215px;text-align:center;color:var(--ivory);text-shadow:0 2px 14px rgba(0,0,0,.6)}
""", """
    <div id="fe-scrim" class="abs"></div>
    <div id="fe-k1" class="abs lbl">Selepas mandi</div>
    <div id="fe-1" class="fe-w disp it">Lembut</div>
    <div id="fe-2" class="fe-w disp it">&amp; wangi</div>
""", f"""
    tl.fromTo('#fe-k1',{{opacity:0}},{{opacity:1,duration:.3}},0.05);
    tl.fromTo('#fe-1',{{opacity:0,filter:'blur(14px)',scale:1.08}},{{opacity:1,filter:'blur(0px)',scale:1,duration:.5,ease:'expo.out'}},at({t_lem})-.1);
    tl.fromTo('#fe-2',{{opacity:0,filter:'blur(14px)',scale:1.08}},{{opacity:1,filter:'blur(0px)',scale:1,duration:.5,ease:'expo.out'}},at({t_wan})-.1);
"""))

# ---------------------------------------------------------------- S9 ASMR foam break (footage overlay)
s, e = word("mandi") + 0.45, word("Dua")
SC.append(scene("asmr", s, e, """
#a-tag{left:0;width:1080px;top:1180px;text-align:center}
#a-tag span{display:inline-block;padding:16px 34px;border:2px solid rgba(244,239,232,.85);border-radius:50px;color:var(--ivory);
  font-family:'Manrope';font-weight:600;font-size:30px;letter-spacing:.24em;text-transform:uppercase;background:rgba(23,18,18,.3)}
#a-big{left:0;width:1080px;top:250px;text-align:center;color:var(--ivory);font-size:110px;text-shadow:0 6px 40px rgba(0,0,0,.35)}
""", """
    <div id="a-big" class="abs disp it">Foam mousse.</div>
    <div id="a-tag" class="abs"><span>Ocean salt &middot; Gentle foam</span></div>
""", """
    tl.fromTo('#a-big',{opacity:0,y:20},{opacity:1,y:0,duration:.6,ease:'expo.out'},0.1);
    tl.fromTo('#a-tag',{opacity:0,y:20},{opacity:1,y:0,duration:.4,ease:'expo.out'},0.12);
"""))

# ---------------------------------------------------------------- S10 VARIANTS
s, e = word("Dua"), word("Stok")
t_var = word("varian"); t_wo = word("Woman"); t_bo = word("Bombshell"); t_na = word("Noche"); t_fa = word("Fantasy")
SC.append(scene("variants", s, e, """
#v-k{left:0;width:1080px;top:215px;text-align:center;color:var(--wine)}
#v-t{left:0;width:1080px;top:260px;text-align:center;color:var(--ink);font-size:110px}
.v-card{position:absolute;top:440px;width:450px;height:700px;border-radius:34px;overflow:hidden;box-shadow:0 30px 80px rgba(23,18,18,.22)}
#v-c1{left:55px;background:#0E1621}
#v-c2{left:575px;background:#0E1621}
.v-img{position:absolute;left:0;top:10px;width:450px;height:500px;object-fit:contain}
.v-cap{position:absolute;left:0;bottom:0;width:450px;height:200px;padding:28px 30px;background:var(--paper)}
.v-cap b{display:block;font-family:'Bodoni Moda';font-style:italic;font-weight:500;font-size:50px;color:var(--ink);line-height:1}
.v-cap i{display:block;font-style:normal;font-family:'Manrope';font-weight:800;font-size:28px;letter-spacing:.3em;margin-top:16px}
#v-bot{position:absolute;left:150px;top:120px;width:150px;height:330px;border-radius:22px;
  background:linear-gradient(160deg, rgba(244,239,232,.22), rgba(244,239,232,.05));border:2px solid rgba(244,239,232,.5)}
#v-pump{position:absolute;left:190px;top:60px;width:70px;height:60px;border-radius:12px 12px 0 0;background:rgba(244,239,232,.85)}
#v-bl{position:absolute;left:150px;top:260px;width:150px;text-align:center;color:var(--ivory);font-family:'Italiana';font-size:18px;letter-spacing:.3em}
.v-no{position:absolute;top:30px;left:30px;color:var(--ivory);font-family:'Manrope';font-weight:800;font-size:28px;letter-spacing:.2em}
""", """
    <div id="v-k" class="abs lbl">Pilih aroma anda</div>
    <div id="v-t" class="abs disp">2 <span class="it" style="color:var(--wine)">varian</span></div>
    <div id="v-c1" class="v-card"><img id="v-img" class="v-img" src="assets/img/bottle_womanglory.jpg" alt="">
      <div class="v-no">01</div>
      <div class="v-cap"><b>Woman Glory</b><i style="color:var(--rose)">BOMBSHELL</i></div></div>
    <div id="v-c2" class="v-card"><img id="v-img2" class="v-img" src="assets/img/bottle_noche.jpg" alt="">
      <div class="v-no" data-layout-allow-overlap>02</div>
      <div class="v-cap"><b>Noche</b><i style="color:#5B3FA0">MIDNIGHT FANTASY</i></div></div>
""", f"""
    tl.fromTo('#v-k',{{opacity:0}},{{opacity:1,duration:.3}},0.02);
    tl.fromTo('#v-t',{{opacity:0,filter:'blur(10px)'}},{{opacity:1,filter:'blur(0px)',duration:.35}},0.02);
    tl.fromTo('#v-c1',{{y:1800,rotation:-6}},{{y:0,rotation:-2,duration:.7,ease:'expo.out'}},at({t_wo})-.25);
    tl.fromTo('#v-img',{{scale:1.25}},{{scale:1,duration:2.5,ease:'power2.out'}},at({t_wo})-.25);
    tl.fromTo('#v-c2',{{y:1800,rotation:6}},{{y:0,rotation:2,duration:.7,ease:'expo.out'}},at({t_na})-.25);
    tl.fromTo('#v-img2',{{scale:1.25}},{{scale:1,duration:2.0,ease:'power2.out'}},at({t_na})-.25);
""", bg="var(--ivory)"))

# ---------------------------------------------------------------- S11 STOCK LIMITED (over footage)
s, e = word("Stok"), word("Bila")
t_ter = word("terhad")
SC.append(scene("stok", s, e, """
#k-bg{left:0;top:0;width:1080px;height:1920px;background:rgba(110,15,31,.82)}
#k-k{left:0;width:1080px;top:330px;text-align:center;color:var(--gold)}
#k-t{left:0;width:1080px;top:390px;text-align:center;color:var(--ivory);font-size:200px;letter-spacing:.06em}
#k-s{left:0;width:1080px;top:610px;text-align:center;color:#F6D9DE;font-size:96px}
#k-track{left:140px;top:820px;width:800px;height:26px;border-radius:13px;background:rgba(244,239,232,.2);overflow:hidden}
#k-fill{width:800px;height:26px;border-radius:13px;background:var(--ivory);transform-origin:left center}
#k-lbl{left:140px;top:870px;width:800px;color:rgba(244,239,232,.85);font-size:28px}
""", """
    <div id="k-bg" class="abs"></div>
    <div id="k-k" class="abs lbl">Perhatian</div>
    <div id="k-t" class="abs disp">STOK</div>
    <div id="k-s" class="abs disp it">sangat terhad</div>
    <div id="k-track" class="abs"><div id="k-fill"></div></div>
    <div id="k-lbl" class="abs lbl">Batch semasa</div>
""", f"""
    tl.fromTo('#k-bg',{{clipPath:'circle(0% at 50% 45%)'}},{{clipPath:'circle(150% at 50% 45%)',duration:.4,ease:'power3.out'}},0);
    tl.fromTo('#k-t',{{scale:1.6,opacity:0}},{{scale:1,opacity:1,duration:.3,ease:'power4.in'}},0.05);
    tl.fromTo('#k-k',{{opacity:0}},{{opacity:1,duration:.3}},0.2);
    tl.fromTo('#k-s',{{opacity:0,y:30}},{{opacity:1,y:0,duration:.4,ease:'expo.out'}},at({t_ter})-.15);
    tl.fromTo(['#k-track','#k-lbl'],{{opacity:0}},{{opacity:1,duration:.3}},0.3);
    tl.fromTo('#k-fill',{{scaleX:.42}},{{scaleX:.07,duration:{e-s-.3:.2f},ease:'power2.inOut'}},0.3);
"""))

# ---------------------------------------------------------------- S12 NEXT BATCH
s, e = word("Bila"), word("Klik")
t_hab = word("habis"); t_tun = word("tunggu"); t_bat = word("batch")
SC.append(scene("batch", s, e, """
#n-card{left:290px;top:300px;width:500px;height:500px;border-radius:40px;background:rgba(244,239,232,.08);border:2px solid rgba(244,239,232,.35);overflow:hidden}
#n-img{position:absolute;left:0;top:0;width:500px;height:500px;object-fit:cover;object-position:50% 50%;opacity:.85}
#n-stamp{left:250px;top:480px;width:580px;height:140px;border:7px solid var(--ivory);border-radius:20px;color:var(--ivory);
  display:flex;align-items:center;justify-content:center;font-family:'Manrope';font-weight:800;font-size:76px;letter-spacing:.12em;background:rgba(110,15,31,.55)}
#n-line{left:140px;top:960px;width:800px;height:3px;background:rgba(244,239,232,.35)}
.n-dot{position:absolute;top:944px;width:36px;height:36px;border-radius:50%;border:3px solid var(--ivory)}
.n-tx{position:absolute;top:1000px;width:300px;color:var(--ivory);font-size:28px}
#n-run{left:122px;top:952px;width:20px;height:20px;border-radius:50%;background:var(--gold)}
#n-t{left:0;width:1080px;top:860px;text-align:center;color:#F6D9DE;font-size:58px}
""", """
    <div id="n-card" class="abs"><img id="n-img" src="assets/img/duo_dark.jpg" alt=""></div>
    <div id="n-stamp" class="abs">HABIS</div>
    <div id="n-line" class="abs"></div>
    <div id="n-d1" class="n-dot" style="left:122px;background:var(--ivory)"></div>
    <div id="n-d2" class="n-dot" style="left:922px"></div>
    <div id="n-run" class="abs"></div>
    <div class="n-tx lbl" style="left:100px">Batch ini</div>
    <div class="n-tx lbl" style="left:740px;text-align:right">Seterusnya</div>
    <div id="n-t" class="abs disp it">tunggu batch seterusnya&hellip;</div>
""", f"""
    tl.fromTo('#n-card',{{y:60,opacity:0}},{{y:0,opacity:1,duration:.4,ease:'expo.out'}},0);
    tl.fromTo('#n-img',{{scale:1.3}},{{scale:1.1,duration:{e-s:.2f},ease:'none'}},0);
    tl.fromTo('#n-stamp',{{scale:2,opacity:0,rotation:-14}},{{scale:1,opacity:1,rotation:-8,duration:.22,ease:'power4.in'}},at({t_hab})+.05);
    tl.to('#n-img',{{filter:'grayscale(1)',opacity:.45,duration:.3}},at({t_hab})+.25);
    tl.fromTo('#n-t',{{opacity:0}},{{opacity:1,duration:.35}},at({t_tun})-.2);
    tl.fromTo('#n-run',{{x:0}},{{x:800,duration:1.4,ease:'power2.inOut'}},at({t_tun}));
""", bg="var(--wine)"))

# ---------------------------------------------------------------- S13 CTA phone
s, e = word("Klik"), word("terlambat") + 0.42
t_link = word("link"); t_bawah = word("bawah"); t_tek = word("tekan"); t_kun = word("kuning"); t_chk = word("check"); t_sek = word("sekarang"); t_seb = word("sebelum")
SC.append(scene("cta", s, e, """
#c-phone{left:240px;top:250px;width:600px;height:1000px;border-radius:70px;background:var(--paper);border:12px solid var(--ink);overflow:hidden;box-shadow:0 40px 100px rgba(23,18,18,.25)}
#c-img{position:absolute;left:0;top:0;width:576px;height:560px;object-fit:cover;object-position:50% 52%}
#c-ttl{position:absolute;left:36px;top:590px;font-family:'Italiana';font-size:40px;letter-spacing:.24em;color:var(--ink)}
#c-sub{position:absolute;left:36px;top:650px;font-family:'Manrope';font-weight:600;font-size:28px;color:var(--muted);letter-spacing:.06em}
#c-bag{position:absolute;left:36px;top:760px;width:504px;height:110px;border-radius:55px;background:var(--yellow);
  display:flex;align-items:center;justify-content:center;gap:16px;font-family:'Manrope';font-weight:800;font-size:32px;color:var(--ink);letter-spacing:.06em}
#c-co{position:absolute;left:36px;top:760px;width:504px;height:110px;border-radius:55px;background:var(--ink);color:var(--ivory);
  display:flex;align-items:center;justify-content:center;font-family:'Manrope';font-weight:800;font-size:32px;letter-spacing:.12em}
#c-badge{position:absolute;left:470px;top:745px;width:56px;height:56px;border-radius:50%;background:var(--rose);color:#fff;
  display:flex;align-items:center;justify-content:center;font-family:'Manrope';font-weight:800;font-size:28px}
#c-finger{left:640px;top:1200px;width:96px;height:96px;border-radius:50%;background:rgba(23,18,18,.18);border:4px solid var(--ink)}
#c-k{left:0;width:1080px;top:190px;text-align:center;color:var(--wine)}
#c-arrow{left:0;width:1080px;top:1255px;text-align:center;color:var(--wine);font-family:'Manrope';font-weight:800;font-size:30px;letter-spacing:.25em}
#c-now{left:0;width:1080px;top:560px;text-align:center}
#c-now span{display:inline-block;padding:18px 44px;background:var(--wine);color:var(--ivory);border-radius:60px;font-family:'Bodoni Moda';font-style:italic;font-size:64px}
""", """
    <div id="c-k" class="abs lbl">Cara beli</div>
    <div id="c-phone" class="abs">
      <img id="c-img" src="assets/img/duo_lifestyle.jpg" alt="">
      <div id="c-ttl">FRESCURA BODY</div>
      <div id="c-sub">Ocean Salt &middot; Perfumed Foam Shower</div>
      <div id="c-bag" data-layout-allow-overlap>&#128717; TEKAN BEG KUNING</div>
      <div id="c-co" data-layout-allow-overlap>&#10003; CHECK OUT</div>
      <div id="c-badge">1</div>
    </div>
    <div id="c-finger" class="abs"></div>
    <div id="c-now" class="abs"><span>Sekarang.</span></div>
    <div id="c-arrow" class="abs">&darr; KLIK LINK DI BAWAH &darr;</div>
""", f"""
    tl.fromTo('#c-phone',{{y:1100,rotation:4}},{{y:0,rotation:0,duration:.7,ease:'expo.out'}},0);
    tl.fromTo('#c-k',{{opacity:0}},{{opacity:1,duration:.3}},0.1);
    tl.fromTo('#c-arrow',{{opacity:0,y:-20}},{{opacity:1,y:0,duration:.35,ease:'power3.out'}},at({t_link}));
    tl.to('#c-arrow',{{y:14,duration:.25,ease:'power2.inOut',yoyo:true,repeat:5}},at({t_bawah}));
    tl.fromTo('#c-co',{{opacity:0}},{{opacity:0,duration:.01}},0);
    tl.fromTo('#c-badge',{{scale:0}},{{scale:0,duration:.01}},0);
    // finger goes to the yellow bag and taps on "kuning"
    tl.fromTo('#c-finger',{{x:200,y:200,opacity:0}},{{x:-160,y:-170,opacity:1,duration:.6,ease:'power3.out'}},at({t_tek}));
    tl.to('#c-finger',{{scale:.75,duration:.08}},at({t_kun}));
    tl.to('#c-finger',{{scale:1,duration:.15}},at({t_kun})+.08);
    tl.to('#c-bag',{{scale:.94,duration:.08}},at({t_kun}));
    tl.to('#c-bag',{{scale:1,duration:.2,ease:'back.out(3)'}},at({t_kun})+.08);
    tl.to('#c-badge',{{scale:1,duration:.3,ease:'back.out(3)'}},at({t_kun})+.1);
    // check out
    tl.to('#c-finger',{{scale:.75,duration:.08}},at({t_chk}));
    tl.to('#c-finger',{{scale:1,opacity:0,duration:.25}},at({t_chk})+.08);
    tl.to('#c-co',{{opacity:1,duration:.15}},at({t_chk})+.02);
    tl.fromTo('#c-now',{{opacity:0,scale:.7}},{{opacity:1,scale:1,duration:.35,ease:'back.out(2)'}},at({t_sek}));
""", bg="var(--ivory)"))

# ---------------------------------------------------------------- S14 END CARD (footage overlay)
s, e = word("terlambat") + 0.42, DUR
SC.append(scene("endcard", s, e, """
#e-scrim{left:0;top:0;width:1080px;height:1920px;background:linear-gradient(180deg, #0B111C 0%, #0B111C 14%, rgba(11,17,28,0) 32%, rgba(11,17,28,0) 62%, rgba(11,17,28,.75) 100%)}
#e-logo{left:320px;top:130px;width:440px;height:440px}
#e-body{left:0;width:1080px;top:440px;text-align:center;color:var(--ivory);font-size:34px}
#e-line{left:390px;top:500px;width:300px}
#e-tag{left:0;width:1080px;top:575px;text-align:center;color:var(--ivory);font-size:56px}
#e-cta{left:0;width:1080px;top:1200px;text-align:center}
#e-cta span{display:inline-block;padding:24px 48px;border-radius:70px;background:var(--yellow);color:var(--ink);font-family:'Manrope';font-weight:800;font-size:38px;letter-spacing:.08em}
#e-v{left:190px;width:700px;top:1300px;padding:12px 0;border-radius:40px;background:rgba(11,17,28,.72);text-align:center;color:rgba(244,239,232,.9);font-size:28px}
""", """
    <div id="e-scrim" class="abs"></div>
    <img id="e-logo" class="abs" src="assets/img/logo.png" alt="FRESCURA BODY">
    <div id="e-tag" class="abs disp it">Ocean salt &times; perfume</div>
    <div id="e-cta" class="abs"><span>&#128717; TEKAN BEG KUNING</span></div>
    <div id="e-v" class="abs lbl">Bombshell &middot; Midnight Fantasy</div>
""", """
    tl.fromTo('#e-logo',{opacity:0,scale:1.35,filter:'blur(12px)'},{opacity:1,scale:1,filter:'blur(0px)',duration:.9,ease:'expo.out'},0.05);
    tl.fromTo('#e-tag',{opacity:0,y:20},{opacity:1,y:0,duration:.5,ease:'expo.out'},0.7);
    tl.fromTo('#e-cta',{opacity:0,scale:.8},{opacity:1,scale:1,duration:.45,ease:'back.out(2)'},1.1);
    tl.fromTo('#e-v',{opacity:0},{opacity:1,duration:.4},1.4);
"""))

json.dump(SC, open(os.path.join(P, "scenes.json"), "w"), indent=1)

# ================================================================= CAPTIONS
KEY = {"garam", "laut", "dapur", "mineral", "mineralnya", "hilang", "spa", "frescura", "body", "perfume", "lembut", "wangi",
       "bombshell", "fantasy", "midnight", "noche", "terhad", "batch", "kuning", "beg", "sekarang", "terlambat", "kulit", "disejat", "diproses", "habis"}
words = [x for x in W]
groups = []; cur = []
for i, x in enumerate(words):
    if cur:
        gap = x["start"] - cur[-1]["end"]
        prev = cur[-1]["text"]
        if gap >= 0.15 or len(cur) >= 3 or len("".join(c["text"] for c in cur)) > 16:
            groups.append(cur); cur = []
    cur.append(x)
    if x["text"] in ("sama", "hilang", "mineral", "ada", "spa", "perfume", "lembut", "mandi", "dipilih", "Bombshell", "Fantasy", "terhad", "habis", "seterusnya", "bawah"):
        groups.append(cur); cur = []
if cur: groups.append(cur)

# no captions during the hook (the hook line is on screen) — but keep for the rest
LIGHT = [(SC[1]["start"], SC[1]["end"]), (SC[3]["start"], SC[3]["end"]), (SC[9]["start"], SC[9]["end"]), (SC[12]["start"], SC[12]["end"])]
def is_light(t): return any(a <= t < b for a, b in LIGHT)
cap_html = []; cap_js = []
gi = 0
for g in groups:
    st = g[0]["start"] - 0.06; en = g[-1]["end"] + 0.08
    if st < SC[0]["end"] - 0.05: continue
    nxt = None
    cls = "cg light" if is_light((st + en) / 2) else "cg dark"
    spans = "".join(f'<span id="cw{gi}_{k}" class="cw{" key" if x["text"].lower() in KEY else ""}">{x["text"]}</span> ' for k, x in enumerate(g))
    cap_html.append(f'    <div id="cg{gi}" class="{cls}">{spans.strip()}</div>')
    cap_js.append((gi, st, en, [(f"cw{gi}_{k}", x["start"]) for k, x in enumerate(g)]))
    gi += 1
# clamp ends to next group start
for i in range(len(cap_js) - 1):
    gi_, st, en, ws = cap_js[i]
    cap_js[i] = (gi_, st, min(en, cap_js[i + 1][1]), ws)
js = []
for gi_, st, en, ws in cap_js:
    js.append(f"tl.set('#cg{gi_}',{{opacity:1,visibility:'visible'}},{st:.3f});")
    for wid, wst in ws:
        js.append(f"tl.fromTo('#{wid}',{{opacity:0,y:18,filter:'blur(6px)'}},{{opacity:1,y:0,filter:'blur(0px)',duration:.16,ease:'power3.out'}},{max(wst-0.05,st):.3f});")
    js.append(f"tl.to('#cg{gi_}',{{opacity:0,duration:.1,ease:'power2.in'}},{en-0.1:.3f});")
    js.append(f"tl.set('#cg{gi_}',{{opacity:0,visibility:'hidden'}},{en:.3f});")

cap = f"""<template>
  <style>
{FONTS}
    #root{{position:absolute;inset:0;overflow:visible}}
    .cg{{position:absolute;left:60px;width:960px;top:1360px;text-align:center;opacity:0;visibility:hidden;
      font-family:'Manrope';font-weight:800;font-size:76px;line-height:1.08;letter-spacing:-.01em;overflow:visible}}
    .cg.dark{{color:#FBF8F3;text-shadow:0 4px 24px rgba(0,0,0,.55),0 1px 3px rgba(0,0,0,.5)}}
    .cg.light{{color:#171212}}
    .cw{{display:inline-block}}
    .cw.key{{font-family:'Bodoni Moda';font-style:italic;font-weight:500;font-size:88px;letter-spacing:0}}
    .cg.dark .cw.key{{color:#E9C98F}}
    .cg.light .cw.key{{color:#6E0F1F}}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920" data-layout-allow-caption-zone>
{chr(10).join(cap_html)}
  </div>
  <script>
    const tl=gsap.timeline({{paused:true}});
    {chr(10)+'    '.join(js)}
    tl.set({{}},{{}},{DUR});
    window.__timelines["captions"]=tl;
  </script>
</template>
"""
open(os.path.join(P, "compositions", "captions.html"), "w").write(cap)
print("groups", len(cap_js))
for gi_, st, en, ws in cap_js[:3]: print(gi_, st, en)

# ================================================================= ROOT
sc = {x["id"]: x for x in SC}
def T(w, i=0, d=0.0): return round(word(w, i) + d, 3)
FOOT = [  # id, start, end, media_start, rate, zoom_from, zoom_to
    ("f-spa", sc["spa"]["start"], T("rawatan", 0, -.1), 17.0, 1.0, 1.0, 1.14),
    ("f-form", sc["formula"]["start"], sc["formula"]["end"], 2.4, 1.0, 1.0, 1.1),
    ("f-feel", sc["feel"]["start"], sc["feel"]["end"], 10.6, 1.0, 1.08, 1.2),
    ("f-asmr", sc["asmr"]["start"], sc["asmr"]["end"], 25.0, 0.8, 1.1, 1.0),
    ("f-stok", sc["stok"]["start"], sc["stok"]["end"], 28.0, 1.0, 1.1, 1.2),
]
SFX = [  # file, time, volume
    ("impact-bass-1", 0.0, .8), ("whoosh-short", T("tak", 0, -.15), .6), ("stamp", T("tak", 0, .02), .75),
    ("whoosh", sc["dapur"]["start"] - .1, .6), ("pop", sc["dapur"]["start"] + .3, .5),
    ("glitch-3", T("diproses", 0, -.1), .35), ("bubble", T("kebanyakan", 0, .05), .5), ("bubble", T("kebanyakan", 0, .17), .45),
    ("bubble", T("kebanyakan", 0, .29), .4), ("glitch-3", T("hilang", 0, -.15), .35),
    ("whoosh-short", sc["laut"]["start"] - .1, .6), ("waves", sc["laut"]["start"], .55), ("salt", T("disejat", 0, -.1), .3),
    ("sparkle", T("mineral", 0, -.15), .6),
    ("whoosh", sc["mineral"]["start"] - .1, .6),
    ("pop", T("semula", 0, -.1), .45), ("pop", T("semula", 0, .06), .45), ("pop", T("semula", 0, .22), .45), ("pop", T("semula", 0, .38), .45),
    ("stamp", T("masih", 0, .15), .8),
    ("whoosh-short", sc["spa"]["start"] - .1, .6), ("soapbub", sc["spa"]["start"] + .1, .5),
    ("whoosh-short", T("penjagaan", 0, -.05), .45), ("whoosh", T("spa", 0, -.25), .45),
    ("whoosh-cinematic", sc["brand"]["start"] - 2.45, .4), ("impact-bass-1", sc["brand"]["start"] - .05, .95), ("sparkle", sc["brand"]["start"] + .15, .5),
    ("pump", sc["formula"]["start"] + .2, .6), ("pop", T("garam", 2, -.05), .5), ("pop", T("digabungkan", 0), .5), ("pop", T("perfume", 0, -.1), .5),
    ("ping", T("perfume", 0, .5), .3),
    ("soapbub", sc["feel"]["start"] + .05, .5), ("sparkle", T("lembut", 0, -.1), .5), ("glitter", T("wangi", 0, -.2), .45),
    ("soapbub", sc["asmr"]["start"] + .05, .7), ("bubble", sc["asmr"]["start"] + .7, .4), ("bubble", sc["asmr"]["start"] + 1.2, .4),
    ("whoosh", sc["variants"]["start"] - .1, .6), ("whoosh-short", T("Woman", 0, -.3), .5), ("pop", T("Woman", 0, .05), .45),
    ("whoosh-short", T("Noche", 0, -.3), .5), ("pop", T("Noche", 0, .05), .45),
    ("impact-bass-2", sc["stok"]["start"] - 1.75, .55), ("stamp", T("terhad", 0, -.05), .6),
    ("stamp", T("habis", 0, .2), .9), ("whoosh-short", T("tunggu", 0, .2), .45),
    ("whoosh", sc["cta"]["start"] - .1, .6), ("click", T("kuning", 0, -.01), .9), ("pop", T("kuning", 0, .12), .55),
    ("click", T("check", 0, -.01), .9), ("cash", T("check", 0, -.15), .75), ("pop", T("sekarang", 0, .02), .5),
    ("impact-bass-1", sc["endcard"]["start"] - .05, .85), ("glitter", sc["endcard"]["start"] + .1, .45), ("whoosh-short", sc["endcard"]["start"] + 1.0, .5),
]
import soundfile as _sf
hosts = []
z = 5
for x in SC:
    hosts.append(f'''      <div id="{x["id"]}" data-composition-id="{x["id"]}" data-composition-src="compositions/{x["id"]}.html" data-start="{x["start"]:.3f}" data-duration="{x["end"]-x["start"]:.3f}" data-track-index="2" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:5"></div>''')
STILLS = [  # id, src, start, end, zoom_from, zoom_to, origin
    ("i-life", "duo_lifestyle.jpg", T("rawatan", 0, -.1), sc["spa"]["end"], 1.12, 1.0, "50% 60%"),
    ("i-end", "duo_dark.jpg", sc["endcard"]["start"], DUR, 1.02, 1.045, "50% 100%"),
]
vids = []; vjs = []
for iid, src, a, b, z0, z1, org in STILLS:
    vids.append(f'''      <div id="{iid}-w" class="fw" style="transform-origin:{org}"><img id="{iid}" class="clip" src="assets/img/{src}" alt="" data-start="{a:.3f}" data-duration="{b-a:.3f}" data-track-index="1"></div>''')
    dy = 290 if iid == "i-end" else 0
    vjs.append(f"tl.fromTo('#{iid}-w',{{scale:{z0},y:{dy}}},{{scale:{z1},y:{dy},duration:{b-a:.3f},ease:'none'}},{a:.3f});")
for vid, a, b, ms, rate, z0, z1 in FOOT:
    vids.append(f'''      <div id="{vid}-w" class="fw"><video id="{vid}" class="clip" src="assets/video/pump.mp4" data-start="{a:.3f}" data-duration="{b-a:.3f}" data-media-start="{ms}" data-playback-rate="{rate}" data-track-index="1" muted playsinline></video></div>''')
    vjs.append(f"tl.fromTo('#{vid}-w',{{scale:{z0}}},{{scale:{z1},duration:{b-a:.3f},ease:'none'}},{a:.3f});")
auds = [f'''      <audio id="voice" src="assets/audio/voice.wav" data-start="0" data-duration="{round(_sf.info(os.path.join(P,'assets/audio/voice.wav')).duration,3)}" data-track-index="10" data-volume="1"></audio>''',
        f'''      <audio id="music" src="assets/audio/music.wav" data-start="0" data-duration="{DUR}" data-track-index="11" data-volume="1"></audio>''']
import soundfile as _sf
lanes = []
for i, (f, t, v) in enumerate(sorted(SFX, key=lambda q: q[1])):
    t = max(0.0, t); d = round(_sf.info(os.path.join(P, "assets/sfx", f + ".wav")).duration, 3); d = min(d, DUR - t)
    li = next((k for k, end in enumerate(lanes) if end <= t), None)
    if li is None: lanes.append(0); li = len(lanes) - 1
    lanes[li] = t + d
    auds.append(f'''      <audio id="sfx{i:02d}-{f}" src="assets/sfx/{f}.wav" data-start="{t:.3f}" data-duration="{d}" data-track-index="{12 + li}" data-volume="{v}"></audio>''')

index = f"""<!doctype html>
<html lang="ms" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ margin:0; width:1080px; height:1920px; overflow:hidden; background:#171212; }}
      #root {{ width:100%; height:100%; position:relative; background:#0B111C; }}
      .fw {{ position:absolute; left:0; top:0; width:1080px; height:1920px; overflow:hidden; z-index:1; }}
      .fw video, .fw img {{ position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:cover; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
{chr(10).join(vids)}
{chr(10).join(hosts)}
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{DUR}" data-track-index="3" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:10"></div>
{chr(10).join(auds)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      {chr(10)+'      '.join(vjs)}
      tl.set({{}}, {{}}, {DUR});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(os.path.join(P, "index.html"), "w").write(index)
print("index written; scenes", [(x["id"], round(x["start"], 2), round(x["end"], 2)) for x in SC])
