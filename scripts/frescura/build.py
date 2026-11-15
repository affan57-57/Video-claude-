#!/usr/bin/env python3
"""Generates the Frescura Body HyperFrames project (index.html + compositions/*.html)."""
import json, os, sys

P = sys.argv[1]
W, H, DUR = 1080, 1920, 30.5

FONTS = """
@font-face{font-family:'Bodoni Moda';src:url('assets/fonts/bodoni-500.woff2') format('woff2');font-weight:500;font-style:normal}
@font-face{font-family:'Bodoni Moda';src:url('assets/fonts/bodoni-800.woff2') format('woff2');font-weight:800;font-style:normal}
@font-face{font-family:'Bodoni Moda';src:url('assets/fonts/bodoni-500i.woff2') format('woff2');font-weight:500;font-style:italic}
@font-face{font-family:'Jakarta';src:url('assets/fonts/pjs-500.woff2') format('woff2');font-weight:500}
@font-face{font-family:'Jakarta';src:url('assets/fonts/pjs-800.woff2') format('woff2');font-weight:800}
@font-face{font-family:'Tenor Sans';src:url('assets/fonts/tenor.woff2') format('woff2');font-weight:400}
"""

BASE = """
#root{position:absolute;inset:0;overflow:hidden;--ink:#F6EFE4;--gold:#D9B77E;--gold2:#F3DDB0;--noir:#0A0807;--rose:#C0213A;--violet:#7A5CFF;}
#root *{box-sizing:border-box}
.full{position:absolute;inset:0}
.bg-noir{background:radial-gradient(120% 70% at 50% 38%,#2A1F17 0%,#120D0A 55%,#060504 100%)}
.label{font-family:'Tenor Sans',serif;letter-spacing:.42em;text-transform:uppercase;color:var(--gold);font-size:30px}
.disp{font-family:'Bodoni Moda',serif;font-weight:500;color:var(--ink);line-height:.98;letter-spacing:-.01em}
.it{font-style:italic}
.gold{color:var(--gold)}
.goldgrad{background:linear-gradient(100deg,#B98F4E 0%,#F6E3B8 45%,#C99D5C 70%,#F3DDB0 100%);-webkit-background-clip:text;background-clip:text;color:transparent}
.center{position:absolute;left:0;right:0;text-align:center}
.hair{position:absolute;height:2px;background:linear-gradient(90deg,transparent,var(--gold),transparent)}
.vign{position:absolute;inset:0;background:radial-gradient(90% 60% at 50% 45%,transparent 40%,rgba(0,0,0,.75) 100%);pointer-events:none}
.media{position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover}
"""


def scene(cid, dur, css, body, js):
    return f"""<template>
  <style>{FONTS}{BASE}{css}</style>
  <div id="root" data-composition-id="{cid}" data-width="{W}" data-height="{H}" data-duration="{dur}">
{body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""


# ------------------------------------------------------------------ boutique (shared mall set)
def boutique(prefix, bottles=True, text=True):
    """A luxury mall boutique: perspective marble floor, storefront light pillars, bokeh,
    two spot cones, a glass vitrine with pedestals and the two bottles with floor reflections."""
    bokeh = []
    pts = [(80, 300, 90), (210, 520, 60), (930, 260, 110), (990, 610, 70), (160, 820, 80), (870, 860, 55),
           (540, 180, 70), (380, 420, 40), (700, 470, 50), (40, 640, 45), (1040, 420, 60), (620, 760, 35)]
    for i, (x, y, r) in enumerate(pts):
        bokeh.append(f'<div class="{prefix}-bk" style="left:{x - r}px;top:{y - r}px;width:{2*r}px;height:{2*r}px;opacity:{0.18 + (i % 4) * 0.08}"></div>')
    pillars = "".join(
        f'<div class="{prefix}-pil" style="left:{x}px;width:{w}px"></div>' for x, w in [(40, 26), (250, 14), (800, 14), (1010, 26)])
    b = f"""
    <div id="{prefix}-set" class="full" data-layout-allow-overflow data-layout-ignore>
      <div class="full {prefix}-wall"></div>
      {pillars}
      <div class="full" id="{prefix}-bokeh">{''.join(bokeh)}</div>
      <div id="{prefix}-floor"></div>
      <div id="{prefix}-cone1" class="{prefix}-cone"></div>
      <div id="{prefix}-cone2" class="{prefix}-cone"></div>
      <div id="{prefix}-vit"></div>"""
    if bottles:
        b += f"""
      <div id="{prefix}-ped1" class="{prefix}-ped"><div class="{prefix}-pedtop"></div></div>
      <div id="{prefix}-ped2" class="{prefix}-ped"><div class="{prefix}-pedtop"></div></div>
      <div id="{prefix}-b1" class="{prefix}-bot"><img src="assets/img/bottle_noche.png" alt=""><img class="{prefix}-ref" src="assets/img/bottle_noche.png" alt=""></div>
      <div id="{prefix}-b2" class="{prefix}-bot"><img src="assets/img/bottle_glory.png" alt=""><img class="{prefix}-ref" src="assets/img/bottle_glory.png" alt=""></div>
      <div id="{prefix}-glint"></div>"""
    b += "\n    </div>"
    css = f"""
    .{prefix}-wall{{background:linear-gradient(180deg,#1B1410 0%,#2B2019 48%,#120E0B 62%,#070605 100%)}}
    .{prefix}-pil{{position:absolute;top:0;height:1180px;background:linear-gradient(180deg,rgba(255,226,170,.0),rgba(255,226,170,.55) 30%,rgba(255,226,170,.15) 80%,transparent)}}
    .{prefix}-bk{{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(255,214,150,.9) 0%,rgba(255,200,120,.25) 45%,transparent 70%);}}
    #{prefix}-floor{{position:absolute;left:-400px;width:1880px;top:1120px;height:1300px;transform-origin:50% 0;
      background:repeating-linear-gradient(90deg,rgba(255,255,255,.035) 0 2px,transparent 2px 235px),
        radial-gradient(60% 40% at 50% 8%,rgba(255,220,170,.35),transparent 70%),
        linear-gradient(180deg,#3A2D24 0%,#1A1310 40%,#0B0807 100%)}}
    .{prefix}-cone{{position:absolute;top:-120px;width:620px;height:1500px;mix-blend-mode:screen;
      background:linear-gradient(180deg,rgba(255,236,200,.55),rgba(255,236,200,.08) 75%,transparent);
      clip-path:polygon(44% 0,56% 0,100% 100%,0 100%);filter:blur(10px)}}
    #{prefix}-cone1{{left:20px}} #{prefix}-cone2{{left:440px}}
    #{prefix}-vit{{position:absolute;left:95px;top:430px;width:890px;height:860px;border:2px solid rgba(217,183,126,.35);border-radius:6px;
      background:linear-gradient(115deg,rgba(255,255,255,.07) 0%,rgba(255,255,255,0) 30%,rgba(255,255,255,.05) 55%,rgba(255,255,255,0) 70%)}}
    .{prefix}-ped{{position:absolute;top:1100px;width:300px;height:250px;
      background:linear-gradient(90deg,#16110D 0%,#3E3127 35%,#5A4A3A 50%,#2C221B 75%,#120D0A 100%)}}
    .{prefix}-pedtop{{position:absolute;left:0;top:-26px;width:300px;height:52px;border-radius:50%;
      background:radial-gradient(60% 60% at 50% 40%,#E9D3A8,#8A7050 70%,#4A3A2C)}}
    #{prefix}-ped1{{left:150px}} #{prefix}-ped2{{left:630px}}
    .{prefix}-bot{{position:absolute;top:500px;width:270px;height:760px}}
    .{prefix}-bot img{{position:absolute;left:0;top:0;width:270px;height:760px;object-fit:contain;filter:drop-shadow(0 30px 40px rgba(0,0,0,.6))}}
    .{prefix}-bot img.{prefix}-ref{{top:760px;transform:scaleY(-1);opacity:.22;filter:blur(2px);
      -webkit-mask-image:linear-gradient(0deg,rgba(0,0,0,.9),transparent 35%);mask-image:linear-gradient(0deg,rgba(0,0,0,.9),transparent 35%)}}
    #{prefix}-b1{{left:165px}} #{prefix}-b2{{left:645px}}
    #{prefix}-glint{{position:absolute;left:-300px;top:400px;width:220px;height:1000px;mix-blend-mode:screen;
      background:linear-gradient(90deg,transparent,rgba(255,250,235,.35),transparent);filter:blur(8px)}}
    """
    js = f"""
    tl.set("#{prefix}-floor",{{rotationX:72,transformPerspective:900}},0);
    """
    return b, css, js


scenes = []  # (id, start, dur, html)

# ------------------------------------------------------------------ 1 HOOK 0 - 1.5
b_body, b_css, b_js = boutique("hk")
scenes.append(("hook", 0.0, 1.5, scene("hook", 1.5, b_css + """
  #hk-cam{position:absolute;inset:0}
  #hk-blur{position:absolute;inset:0;backdrop-filter:blur(14px);background:rgba(8,6,5,.45)}
  #hk-t1{top:470px;font-size:188px}
  #hk-t2{top:700px;font-size:150px}
  #hk-q{top:880px;font-size:300px;line-height:1}
  #hk-line{left:240px;width:600px;top:450px}
  #hk-flash{position:absolute;inset:0;background:radial-gradient(circle at 50% 45%,#FFF2D6,rgba(255,220,160,.0) 60%);mix-blend-mode:screen}
""", f"""
    <div id="hk-cam">{b_body}</div>
    <div id="hk-blur"></div>
    <div class="vign"></div>
    <div id="hk-line" class="hair"></div>
    <div id="hk-t1" class="center disp it goldgrad">Abang,</div>
    <div id="hk-t2" class="center disp">pernah <span class="it">terfikir</span></div>
    <div id="hk-q" class="center disp goldgrad">?</div>
    <div id="hk-flash"></div>
""", b_js + """
    tl.fromTo("#hk-cam",{scale:1.25},{scale:1.08,duration:1.5,ease:"power2.out"},0);
    tl.fromTo("#hk-flash",{opacity:.9},{opacity:0,duration:.45,ease:"power2.out"},0);
    tl.fromTo("#hk-t1",{opacity:1,scale:1.6,filter:"blur(0px)"},{scale:1,duration:.38,ease:"expo.out"},0);
    tl.fromTo("#hk-line",{scaleX:0},{scaleX:1,duration:.5,ease:"expo.out"},0.05);
    tl.fromTo("#hk-t2",{opacity:0,y:40,filter:"blur(10px)"},{opacity:1,y:0,filter:"blur(0px)",duration:.3,ease:"power4.out"},0.42);
    tl.fromTo("#hk-q",{opacity:0,scale:.3,rotation:-25},{opacity:1,scale:1,rotation:0,duration:.45,ease:"back.out(2)"},0.85);
    tl.to(["#hk-t1","#hk-t2","#hk-q"],{opacity:0,filter:"blur(10px)",y:-30,duration:.18,ease:"power3.in"},1.32);
""")))

# ------------------------------------------------------------------ 2 HADIAH 1.5 - 3.45  (gift box line art)
scenes.append(("gift", 1.5, 1.95, scene("gift", 1.95, """
  #gf-svg{position:absolute;left:290px;top:300px;width:500px;height:520px;overflow:visible}
  #gf-svg path,#gf-svg rect,#gf-svg line{fill:none;stroke:var(--gold);stroke-width:5;stroke-linecap:round;stroke-linejoin:round}
  #gf-k{top:300px;font-size:150px}
  #gf-x{position:absolute;left:250px;top:340px;width:580px;height:500px}
  #gf-x i{position:absolute;left:0;top:240px;width:580px;height:10px;background:var(--rose);border-radius:6px;box-shadow:0 0 30px rgba(192,33,58,.6)}
  #gf-l1{top:900px;font-size:56px}
  #gf-l2{top:975px;font-size:118px}
  #gf-ring{position:absolute;left:240px;top:250px;width:600px;height:600px;border-radius:50%;border:1px solid rgba(217,183,126,.25)}
""", """
    <div class="full bg-noir"></div>
    <div id="gf-ring"></div>
    <svg id="gf-svg" viewBox="0 0 500 520">
      <rect id="gf-box" x="60" y="230" width="380" height="270" rx="10" pathLength="1"/>
      <rect id="gf-lid" x="35" y="160" width="430" height="80" rx="10" pathLength="1"/>
      <line id="gf-rib" x1="250" y1="160" x2="250" y2="500" pathLength="1"/>
      <path id="gf-bow" d="M250 160 C 200 60, 120 90, 160 150 C 190 170, 230 165, 250 160 C 270 165, 310 170, 340 150 C 380 90, 300 60, 250 160" pathLength="1"/>
    </svg>
    <div id="gf-x"><i></i></div>
    <div id="gf-l1" class="center label">Isteri abang</div>
    <div id="gf-l2" class="center disp">tak pernah <span class="it goldgrad">minta</span></div>
""", """
    tl.fromTo("#gf-ring",{scale:.6,opacity:0},{scale:1,opacity:1,duration:.8,ease:"expo.out"},0);
    ["#gf-box","#gf-lid","#gf-rib","#gf-bow"].forEach((s,i)=>tl.fromTo(s,{strokeDasharray:1,strokeDashoffset:1},{strokeDashoffset:0,duration:.55,ease:"power2.inOut"},0.05+i*0.12));
    tl.fromTo("#gf-svg",{y:30,scale:.9},{y:0,scale:1,duration:.7,ease:"expo.out"},0);
    tl.fromTo("#gf-l1",{opacity:0,scale:1.14},{opacity:1,scale:1,duration:.5,ease:"expo.out"},0.1);
    tl.fromTo("#gf-l2",{opacity:0,filter:"blur(10px)"},{opacity:1,filter:"blur(0px)",duration:.2,ease:"power3.out"},0.9);
    tl.fromTo("#gf-x i",{scaleX:0,rotation:-18,transformOrigin:"0% 50%"},{scaleX:1,rotation:-18,duration:.25,ease:"power4.out"},1.25);
    tl.to("#gf-svg",{opacity:.35,duration:.25},1.25);
    tl.to(["#gf-l2","#gf-l1","#gf-x","#gf-svg","#gf-ring"],{opacity:0,filter:"blur(10px)",duration:.15,ease:"power2.in"},1.78);
""")))

# ------------------------------------------------------------------ 3 HATI 3.45 - 6.15 (heart + DIHARGAI)
petals = "".join(f'<div class="ht-p" id="ht-p{i}" style="left:{x}px;top:{y}px;transform:rotate({r}deg)"></div>'
                 for i, (x, y, r) in enumerate([(120, 300, 20), (880, 380, -30), (200, 900, 45), (930, 820, 10), (520, 220, -15), (70, 640, 60), (990, 560, -50), (640, 980, 30)]))
scenes.append(("heart", 3.45, 2.7, scene("heart", 2.7, """
  #ht-bg{background:radial-gradient(80% 55% at 50% 40%,#3A1418 0%,#160A0B 55%,#070405 100%)}
  #ht-svg{position:absolute;left:340px;top:250px;width:400px;height:380px;overflow:visible}
  #ht-svg path{fill:none;stroke:var(--gold);stroke-width:6;stroke-linecap:round}
  #ht-fill{fill:rgba(192,33,58,.0)!important;stroke:none!important}
  #ht-l1{top:700px;font-size:44px}
  #ht-big{top:770px;font-size:178px;font-weight:500}
  #ht-l3{top:980px;font-size:40px;color:rgba(246,239,228,.75)}
  .ht-p{position:absolute;width:34px;height:22px;border-radius:60% 0 60% 0;background:linear-gradient(135deg,#E0455C,#7A0F1E);opacity:.8}
  #ht-pulse{position:absolute;left:390px;top:280px;width:300px;height:300px;border-radius:50%;border:2px solid rgba(217,183,126,.6)}
""", f"""
    <div id="ht-bg" class="full"></div>
    {petals}
    <div id="ht-pulse"></div>
    <svg id="ht-svg" viewBox="0 0 400 380">
      <path id="ht-fill" d="M200 350 C 40 240, 10 140, 60 80 C 110 20, 180 40, 200 100 C 220 40, 290 20, 340 80 C 390 140, 360 240, 200 350 Z"/>
      <path id="ht-path" d="M200 350 C 40 240, 10 140, 60 80 C 110 20, 180 40, 200 100 C 220 40, 290 20, 340 80 C 390 140, 360 240, 200 350 Z" pathLength="1"/>
    </svg>
    <div id="ht-l1" class="center label">jauh di sudut hati</div>
    <div id="ht-big" class="center disp it goldgrad">dihargai</div>
    <div id="ht-l3" class="center label" style="letter-spacing:.3em">— itu yang dia mahu —</div>
""", """
    tl.fromTo("#ht-path",{strokeDasharray:1,strokeDashoffset:1},{strokeDashoffset:0,duration:.9,ease:"power2.inOut"},0.05);
    tl.fromTo("#ht-fill",{fill:"rgba(192,33,58,0)"},{fill:"rgba(192,33,58,.85)",duration:.5,ease:"power2.out"},0.9);
    tl.fromTo("#ht-svg",{scale:.85},{scale:1,duration:1.2,ease:"expo.out"},0);
    tl.fromTo("#ht-svg",{scale:1},{scale:1.08,duration:.12,yoyo:true,repeat:3,ease:"power1.inOut",immediateRender:false},1.3);
    tl.fromTo("#ht-pulse",{scale:.6,opacity:.9},{scale:1.9,opacity:0,duration:1.0,ease:"power2.out"},1.3);
    tl.fromTo("#ht-l1",{opacity:0,y:20},{opacity:1,y:0,duration:.4,ease:"expo.out"},0.15);
    tl.fromTo("#ht-big",{opacity:0,scale:1.18,filter:"blur(12px)"},{opacity:1,scale:1,filter:"blur(0px)",duration:.6,ease:"expo.out"},1.55);
    tl.fromTo("#ht-l3",{opacity:0},{opacity:1,duration:.3},1.95);
    for(let i=0;i<8;i++) tl.fromTo("#ht-p"+i,{y:-60,opacity:0},{y:260+i*25,x:(i%2?-40:40),rotation:(i%2?160:-160),opacity:.8,duration:2.7,ease:"none"},0);
    tl.to(["#ht-big","#ht-l1","#ht-l3","#ht-svg"],{opacity:0,filter:"blur(10px)",duration:.16,ease:"power2.in"},2.52);
""")))

# ------------------------------------------------------------------ 4 MAHAL 6.15 - 8.25 (price tag struck)
scenes.append(("pricey", 6.15, 2.1, scene("pricey", 2.1, """
  #pr-tag{position:absolute;left:230px;top:330px;width:620px;height:330px}
  #pr-card{position:absolute;inset:0;border-radius:24px;background:linear-gradient(135deg,#F3E6CF,#D9C39A);box-shadow:0 40px 80px rgba(0,0,0,.6)}
  #pr-hole{position:absolute;left:40px;top:145px;width:40px;height:40px;border-radius:50%;background:#100C09}
  #pr-cap{position:absolute;left:110px;top:56px;font-size:30px;color:#6B5233}
  #pr-num{position:absolute;left:105px;top:115px;font-family:'Bodoni Moda';font-weight:800;font-size:100px;color:#1A120C;white-space:nowrap}
  #pr-strike{position:absolute;left:80px;top:180px;width:480px;height:12px;border-radius:6px;background:var(--rose)}
  #pr-l1{top:780px;font-size:110px}
  #pr-l2{top:910px;font-size:46px}
  #pr-stamp{position:absolute;left:640px;top:240px;width:250px;height:250px;border-radius:50%;border:5px solid var(--rose);color:var(--rose);
    font-family:'Jakarta';font-weight:800;font-size:44px;display:flex;align-items:center;justify-content:center;text-align:center;line-height:1.05}
""", """
    <div class="full bg-noir"></div>
    <div id="pr-tag"><div id="pr-card"></div><div id="pr-hole"></div>
      <div id="pr-cap" class="label" style="color:#6B5233">harga</div>
      <div id="pr-num">RM9,999</div><div id="pr-strike"></div></div>
    <div id="pr-stamp">BUKAN<br>ITU</div>
    <div id="pr-l1" class="center disp">bukan yang <span class="it goldgrad">mahal</span></div>
    <div id="pr-l2" class="center label">yang dia harapkan</div>
""", """
    tl.fromTo("#pr-tag",{y:-500,rotation:-14},{y:0,rotation:-4,duration:.6,ease:"back.out(1.6)"},0);
    tl.fromTo("#pr-strike",{scaleX:0,transformOrigin:"0% 50%"},{scaleX:1,duration:.22,ease:"power4.out"},0.85);
    tl.to("#pr-num",{opacity:.4,duration:.2},0.95);
    tl.fromTo("#pr-stamp",{scale:2.4,opacity:0,rotation:-30},{scale:1,opacity:1,rotation:-12,duration:.28,ease:"power4.out"},0.9);
    tl.fromTo("#pr-l1",{opacity:0,filter:"blur(10px)"},{opacity:1,filter:"blur(0px)",duration:.2},0.25);
    tl.fromTo("#pr-l2",{opacity:0,scale:1.14},{opacity:1,scale:1,duration:.5,ease:"expo.out"},1.2);
    tl.to(["#pr-tag","#pr-stamp","#pr-l1","#pr-l2"],{opacity:0,x:-120,filter:"blur(12px)",duration:.18,ease:"power3.in"},1.9);
""")))

# ------------------------------------------------------------------ 5 KECIL 8.25 - 11.95 (b-roll p2 + small -> big)
scenes.append(("small", 8.25, 3.7, scene("small", 3.7, """
  #sm-wrap{position:absolute;inset:0}
  #sm-dim{position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,8,7,.85) 0%,rgba(10,8,7,.6) 45%,rgba(10,8,7,.92) 100%)}
  #sm-row{position:absolute;left:0;right:0;top:330px;height:330px}
  #sm-dot{position:absolute;left:230px;top:140px;width:44px;height:44px;border-radius:50%;background:var(--gold);box-shadow:0 0 30px rgba(217,183,126,.8)}
  #sm-arrow{position:absolute;left:330px;top:158px;width:250px;height:8px;background:linear-gradient(90deg,transparent,var(--gold))}
  #sm-big{position:absolute;left:620px;top:20px;width:290px;height:290px;border-radius:50%;
     background:radial-gradient(circle at 35% 30%,#FFF1D2,#D9B77E 45%,#8C6A3A);box-shadow:0 0 80px rgba(217,183,126,.55)}
  #sm-c1{position:absolute;left:150px;top:220px;width:210px;text-align:center;font-size:30px}
  #sm-c2{position:absolute;left:615px;top:330px;width:300px;text-align:center;font-size:24px}
  #sm-l1{top:760px;font-size:96px}
  #sm-l2{top:870px;font-size:124px}
""", """
    <div id="sm-wrap"><video id="sm-vid" class="clip media" data-start="0" data-duration="3.7" data-media-start="0" src="assets/video/p2.mp4" muted playsinline></video></div>
    <div id="sm-dim"></div>
    <div id="sm-row">
      <div id="sm-dot"></div><div id="sm-arrow"></div><div id="sm-big"></div>
      <div id="sm-c1" class="label">perhatian kecil</div>
      <div id="sm-c2" class="label">bahagia besar</div>
    </div>
    <div id="sm-l1" class="center disp">perhatian <span class="it">kecil</span></div>
    <div id="sm-l2" class="center disp it goldgrad">= bahagia</div>
""", """
    tl.fromTo("#sm-wrap",{scale:1.18},{scale:1.02,duration:3.7,ease:"power1.out"},0);
    tl.fromTo("#sm-dot",{scale:0},{scale:1,duration:.4,ease:"back.out(3)"},0.2);
    tl.fromTo("#sm-c1",{opacity:0},{opacity:1,duration:.3},0.35);
    tl.fromTo("#sm-l1",{opacity:0,filter:"blur(10px)"},{opacity:1,filter:"blur(0px)",duration:.22},0.4);
    tl.fromTo("#sm-arrow",{scaleX:0,transformOrigin:"0% 50%"},{scaleX:1,duration:.5,ease:"power3.inOut"},1.3);
    tl.fromTo("#sm-big",{scale:0},{scale:1,duration:.7,ease:"elastic.out(1,.6)"},1.7);
    tl.fromTo("#sm-c2",{opacity:0},{opacity:1,duration:.3},1.9);
    tl.fromTo("#sm-l2",{opacity:0,y:40},{opacity:1,y:0,duration:.5,ease:"expo.out"},2.35);
    tl.to(["#sm-row","#sm-l1","#sm-l2"],{opacity:0,scale:1.15,filter:"blur(14px)",duration:.22,ease:"power3.in"},3.45);
""")))

# ------------------------------------------------------------------ 6 REVEAL (mall boutique) 11.95 - 13.7
b_body, b_css, b_js = boutique("rv")
scenes.append(("reveal", 11.95, 1.75, scene("reveal", 1.75, b_css + """
  #rv-cam{position:absolute;inset:0}
  #rv-brand{top:220px;font-size:34px}
  #rv-t{top:270px;font-size:120px}
  #rv-black{position:absolute;inset:0;background:#000}
""", f"""
    <div id="rv-cam">{b_body}</div>
    <div class="vign"></div>
    <div id="rv-brand" class="center label">Frescura Body · Boutique</div>
    <div id="rv-t" class="center disp it goldgrad">hadiah mewah</div>
    <div id="rv-black"></div>
""", b_js + """
    tl.fromTo("#rv-black",{opacity:1},{opacity:0,duration:.25,ease:"power2.out"},0);
    tl.fromTo("#rv-cam",{scale:1.35,y:120},{scale:1,y:0,duration:1.6,ease:"power3.out"},0);
    tl.fromTo(".rv-cone",{opacity:0},{opacity:1,duration:.12,stagger:.18},0.05);
    tl.fromTo("#rv-b1",{y:220,opacity:0},{y:0,opacity:1,duration:.7,ease:"expo.out"},0.15);
    tl.fromTo("#rv-b2",{y:220,opacity:0},{y:0,opacity:1,duration:.7,ease:"expo.out"},0.3);
    tl.fromTo("#rv-glint",{x:0},{x:1700,duration:.9,ease:"power2.inOut"},0.6);
    tl.fromTo("#rv-brand",{opacity:0,scale:1.14},{opacity:1,scale:1,duration:.6,ease:"expo.out"},0.4);
    tl.fromTo("#rv-t",{opacity:0,filter:"blur(12px)",y:20},{opacity:1,filter:"blur(0px)",y:0,duration:.35,ease:"power3.out"},0.55);
    tl.fromTo("#rv-bokeh",{x:-30},{x:30,duration:1.75,ease:"none"},0);
""")))

# ------------------------------------------------------------------ 7 FOAM 13.7 - 17.3 (p1 + p3, feature chips)
chips = [("Ocean Salt", "garam laut"), ("Aromaterapi", "tenang & wangi"), ("Gentle Foaming", "lembut di kulit")]
chip_html = "".join(f'<div class="fm-chip" id="fm-c{i}"><b>{a}</b><span>{b}</span></div>' for i, (a, b) in enumerate(chips))
scenes.append(("foam", 13.7, 3.6, scene("foam", 3.6, """
  #fm-w1,#fm-w2{position:absolute;inset:0}
  #fm-grad{position:absolute;inset:0;background:linear-gradient(180deg,rgba(8,6,5,.75) 0%,rgba(8,6,5,0) 28%,rgba(8,6,5,.15) 50%,rgba(8,6,5,.7) 62%,rgba(8,6,5,.85) 100%)}
  #fm-tag{top:200px;font-size:30px}
  #fm-h{top:245px;font-size:112px}
  .fm-chip{position:absolute;left:70px;width:440px;padding:22px 30px;border-radius:999px;border:1.5px solid rgba(217,183,126,.7);
     background:rgba(15,11,8,.55);backdrop-filter:blur(12px);display:flex;flex-direction:column}
  .fm-chip b{font-family:'Jakarta';font-weight:800;font-size:38px;color:var(--ink)}
  .fm-chip span{font-family:'Tenor Sans';font-size:24px;letter-spacing:.25em;text-transform:uppercase;color:var(--gold)}
  #fm-c0{top:560px} #fm-c1{top:700px} #fm-c2{top:840px}
  #fm-frame{position:absolute;left:40px;top:40px;right:40px;bottom:40px;border:1.5px solid rgba(217,183,126,.45);border-radius:28px}
""", f"""
    <div id="fm-w1"><video id="fm-v1" class="clip media" data-start="0" data-duration="1.95" data-media-start="0.1" src="assets/video/p1.mp4" muted playsinline></video></div>
    <div id="fm-w2"><video id="fm-v2" class="clip media" data-start="1.95" data-duration="1.65" data-media-start="0.6" src="assets/video/p3.mp4" muted playsinline></video></div>
    <div id="fm-grad"></div>
    <div id="fm-frame"></div>
    <div id="fm-tag" class="center label">Foaming Body Shower</div>
    <div id="fm-h" class="center disp">buih <span class="it goldgrad">mewah</span></div>
    {chip_html}
""", """
    tl.fromTo("#fm-w1",{scale:1.0},{scale:1.12,duration:1.95,ease:"none"},0);
    tl.fromTo("#fm-w2",{scale:1.2},{scale:1.05,duration:1.65,ease:"power2.out"},1.95);
    tl.fromTo("#fm-frame",{opacity:0,scale:1.05},{opacity:1,scale:1,duration:.5,ease:"expo.out"},0);
    tl.fromTo("#fm-tag",{opacity:0,scale:1.14},{opacity:1,scale:1,duration:.6,ease:"expo.out"},0.05);
    tl.fromTo("#fm-h",{opacity:0,filter:"blur(10px)"},{opacity:1,filter:"blur(0px)",duration:.2},0.3);
    [0,1,2].forEach(i=>tl.fromTo("#fm-c"+i,{x:-520,opacity:0},{x:0,opacity:1,duration:.45,ease:"expo.out"},1.5+i*0.4));
    tl.to(["#fm-c0","#fm-c1","#fm-c2","#fm-h","#fm-tag"],{opacity:0,x:80,duration:.15,ease:"power2.in"},3.42);
""")))

# ------------------------------------------------------------------ 8 SCENTS 17.3 - 20.6
scenes.append(("scents", 17.3, 3.3, scene("scents", 3.3, """
  #sc-photo{position:absolute;inset:0}
  #sc-photo img{position:absolute;left:-36px;top:-64px;width:1152px;height:2048px}
  #sc-dim{position:absolute;inset:0;background:linear-gradient(180deg,rgba(8,6,5,.75),rgba(8,6,5,.0) 30%,rgba(8,6,5,.0) 60%,rgba(8,6,5,.8))}
  #sc-h{top:200px;font-size:110px}
  #sc-sub{top:330px;font-size:30px}
  .sc-panel{position:absolute;inset:0}
  #sc-red{background:radial-gradient(90% 60% at 50% 40%,#7A0E1F 0%,#2A0509 60%,#0C0203 100%)}
  #sc-vio{background:radial-gradient(90% 60% at 50% 40%,#3B2A8C 0%,#140C38 60%,#050311 100%)}
  .sc-bot{position:absolute;left:390px;top:380px;width:300px;height:760px;object-fit:contain;filter:drop-shadow(0 40px 60px rgba(0,0,0,.7))}
  .sc-name{top:205px;font-size:118px}
  .sc-k{top:150px;font-size:30px}
  .sc-notes{top:1050px;font-size:28px}
""", """
    <div id="sc-photo"><img src="assets/img/flatlay1.jpg" alt=""></div>
    <div id="sc-dim"></div>
    <div id="sc-h" class="center disp">pilih <span class="it goldgrad">haruman</span></div>
    <div id="sc-sub" class="center label">dua aroma · satu hadiah</div>
    <div id="sc-red" class="sc-panel">
      <div class="center label sc-k">Woman Glory</div>
      <div class="center disp it sc-name" style="color:#FFD9DF">Bombshell</div>
      <img class="sc-bot" id="sc-b1" src="assets/img/bottle_glory.png" alt="">
    </div>
    <div id="sc-vio" class="sc-panel">
      <div class="center label sc-k">Noche</div>
      <div class="center disp it sc-name" style="color:#E3DCFF">Midnight Fantasy</div>
      <img class="sc-bot" id="sc-b2" src="assets/img/bottle_noche.png" alt="">
    </div>
""", """
    tl.fromTo("#sc-photo",{scale:1.0},{scale:1.1,duration:1.5,ease:"none"},0);
    tl.fromTo("#sc-h",{opacity:0,filter:"blur(10px)"},{opacity:1,filter:"blur(0px)",duration:.2},0.12);
    tl.fromTo("#sc-sub",{opacity:0,scale:1.14},{opacity:1,scale:1,duration:.6,ease:"expo.out"},0.3);
    tl.fromTo("#sc-red",{clipPath:"inset(0 0 0 100%)"},{clipPath:"inset(0 0 0 0%)",duration:.4,ease:"power3.inOut"},1.45);
    tl.fromTo("#sc-b1",{y:160,rotation:6,scale:.9},{y:0,rotation:0,scale:1,duration:.7,ease:"expo.out"},1.55);
    tl.fromTo("#sc-red .sc-name",{opacity:0,scale:1.15},{opacity:1,scale:1,duration:.5,ease:"expo.out"},1.6);
    tl.fromTo("#sc-vio",{clipPath:"inset(0 100% 0 0)"},{clipPath:"inset(0 0% 0 0)",duration:.4,ease:"power3.inOut"},2.15);
    tl.fromTo("#sc-b2",{y:160,rotation:-6,scale:.9},{y:0,rotation:0,scale:1,duration:.7,ease:"expo.out"},2.25);
    tl.fromTo("#sc-vio .sc-name",{opacity:0,scale:1.15},{opacity:1,scale:1,duration:.5,ease:"expo.out"},2.3);
""")))

# ------------------------------------------------------------------ 9 STOCK 20.6 - 22.28
scenes.append(("stock", 20.6, 1.68, scene("stock", 1.68, """
  #st-k{top:300px;font-size:34px}
  #st-h{top:360px;font-size:170px}
  #st-bar{position:absolute;left:140px;top:640px;width:800px;height:22px;border-radius:12px;background:rgba(246,239,228,.12);overflow:hidden}
  #st-fill{position:absolute;left:0;top:0;bottom:0;width:800px;background:linear-gradient(90deg,var(--rose),#E5566C);border-radius:12px}
  #st-pct{position:absolute;left:140px;top:690px;width:800px;display:flex;justify-content:space-between;font-family:'Jakarta';font-weight:800;font-size:40px;color:var(--ink)}
  #st-pct span:last-child{color:#FF7B8E}
  #st-ring{position:absolute;left:340px;top:240px;width:400px;height:400px;border-radius:50%;border:2px solid rgba(192,33,58,.5)}
""", """
    <div class="full bg-noir"></div>
    <div id="st-ring"></div>
    <div id="st-k" class="center label">stok</div>
    <div id="st-h" class="center disp it goldgrad">terhad</div>
    <div id="st-bar"><div id="st-fill"></div></div>
    <div id="st-pct"><span>Baki stok</span><span id="st-n">tinggal sikit!</span></div>
""", """
    tl.fromTo("#st-h",{opacity:0,scale:1.5,filter:"blur(14px)"},{opacity:1,scale:1,filter:"blur(0px)",duration:.35,ease:"expo.out"},0);
    tl.fromTo("#st-k",{opacity:0},{opacity:1,duration:.3},0.1);
    tl.fromTo("#st-ring",{scale:.5,opacity:1},{scale:1.8,opacity:0,duration:1.2,ease:"power2.out"},0);
    tl.fromTo("#st-fill",{scaleX:1,transformOrigin:"0% 50%"},{scaleX:.12,duration:1.2,ease:"power3.inOut"},0.3);
    tl.fromTo("#st-pct",{opacity:0,y:20},{opacity:1,y:0,duration:.3},0.3);
    tl.to(["#st-h","#st-bar","#st-pct","#st-k"],{opacity:0,y:-60,filter:"blur(10px)",duration:.15,ease:"power2.in"},1.52);
""")))

# ------------------------------------------------------------------ 10 BUY 22.28 - 24.75 (p4 + yellow bag)
scenes.append(("buy", 22.28, 2.47, scene("buy", 2.47, """
  #by-w{position:absolute;inset:0}
  #by-dim{position:absolute;inset:0;background:rgba(8,6,5,.6)}
  #by-bag{position:absolute;left:400px;top:320px;width:280px;height:300px}
  #by-bag svg{width:100%;height:100%;overflow:visible}
  #by-h{top:680px;font-size:104px}
  #by-arrow{position:absolute;left:510px;top:1400px;width:60px;height:110px}
  #by-glow{position:absolute;left:340px;top:270px;width:400px;height:400px;border-radius:50%;background:radial-gradient(circle,rgba(255,204,0,.45),transparent 65%)}
  #by-pill{position:absolute;left:290px;top:830px;width:500px;height:96px;border-radius:999px;background:linear-gradient(90deg,#FFCF33,#F4B400);
     display:flex;align-items:center;justify-content:center;font-family:'Jakarta';font-weight:800;font-size:40px;color:#1A1205;letter-spacing:.06em}
""", """
    <div id="by-w"><video id="by-v" class="clip media" data-start="0" data-duration="2.47" data-media-start="0.3" src="assets/video/p4.mp4" muted playsinline></video></div>
    <div id="by-dim"></div>
    <div id="by-glow"></div>
    <div id="by-bag"><svg viewBox="0 0 280 300">
      <path d="M90 95 C 90 35, 190 35, 190 95" fill="none" stroke="#1A1205" stroke-width="14" stroke-linecap="round"/>
      <rect x="25" y="90" width="230" height="200" rx="26" fill="#FFC81F"/>
      <path d="M90 95 C 90 35, 190 35, 190 95" fill="none" stroke="#FFC81F" stroke-width="9" stroke-linecap="round"/>
      <path d="M95 175 l 30 30 l 60 -62" fill="none" stroke="#1A1205" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>
    </svg></div>
    <div id="by-h" class="center disp">tekan <span class="it" style="color:#FFC81F">beg kuning</span></div>
    <div id="by-pill">CHECKOUT SEKARANG</div>
""", """
    tl.fromTo("#by-w",{scale:1.15},{scale:1.0,duration:2.47,ease:"none"},0);
    tl.fromTo("#by-bag",{scale:0,rotation:-20},{scale:1,rotation:0,duration:.5,ease:"back.out(2.2)"},0.1);
    tl.fromTo("#by-glow",{opacity:0,scale:.6},{opacity:1,scale:1.1,duration:.6,ease:"power2.out"},0.1);
    tl.fromTo("#by-bag",{y:0},{y:-24,duration:.18,yoyo:true,repeat:3,ease:"power1.inOut",immediateRender:false},0.7);
    tl.fromTo("#by-h",{opacity:0,filter:"blur(10px)"},{opacity:1,filter:"blur(0px)",duration:.2},0.2);
    tl.fromTo("#by-pill",{opacity:0,scale:.7},{opacity:1,scale:1,duration:.4,ease:"back.out(2)"},0.95);
    tl.fromTo("#by-pill",{scale:1},{scale:1.06,duration:.2,yoyo:true,repeat:3,ease:"power1.inOut",immediateRender:false},1.4);
""")))

# ------------------------------------------------------------------ 11 OUTRO 24.75 - 30.5
b_body, b_css, b_js = boutique("ou")
scenes.append(("outro", 24.75, 5.75, scene("outro", 5.75, b_css + """
  #ou-cam{position:absolute;inset:0}
  #ou-photo{position:absolute;inset:0}
  #ou-photo img{position:absolute;left:-36px;top:-48px;width:1152px;height:2016px}
  #ou-logo{position:absolute;left:190px;top:150px;width:700px;height:700px;mix-blend-mode:screen}
  #ou-logo img{width:100%;height:100%}
  #ou-dim{position:absolute;inset:0;background:linear-gradient(180deg,rgba(6,5,4,.94) 0%,rgba(6,5,4,.72) 45%,rgba(6,5,4,.94) 100%)}
  #ou-h{top:840px;font-size:104px}
  #ou-sub{top:980px;font-size:30px}
  #ou-cta{position:absolute;left:240px;top:1100px;width:600px;height:100px;border-radius:999px;border:2px solid var(--gold);
    display:flex;align-items:center;justify-content:center;font-family:'Jakarta';font-weight:800;font-size:38px;color:var(--ink);letter-spacing:.12em;background:rgba(10,8,7,.5)}
  #ou-wipe{position:absolute;inset:0;background:#000}
""", f"""
    <div id="ou-cam">{b_body}</div>
    <div id="ou-photo"><img src="assets/img/flatlay2.jpg" alt=""></div>
    <div id="ou-dim"></div>
    <div id="ou-logo"><img src="assets/img/logo.jpg" alt=""></div>
    <div id="ou-h" class="center disp">hadiah <span class="it goldgrad">untuk dia</span></div>
    <div id="ou-sub" class="center label">Soft · Fragrant · 500 ml</div>
    <div id="ou-cta">BELI SEKARANG</div>
    <div id="ou-wipe"></div>
""", b_js + """
    tl.set("#ou-wipe",{opacity:0},0);
    tl.fromTo("#ou-cam",{scale:1.2},{scale:1.0,duration:2.4,ease:"power3.out"},0);
    tl.fromTo(".ou-cone",{opacity:0},{opacity:1,duration:.15,stagger:.15},0.1);
    tl.fromTo("#ou-b1",{y:200,opacity:0},{y:0,opacity:1,duration:.7,ease:"expo.out"},0.2);
    tl.fromTo("#ou-b2",{y:200,opacity:0},{y:0,opacity:1,duration:.7,ease:"expo.out"},0.35);
    tl.fromTo("#ou-glint",{x:0},{x:1700,duration:1.0,ease:"power2.inOut"},0.8);
    tl.fromTo("#ou-photo",{opacity:0,scale:1.15},{opacity:1,scale:1.0,duration:.6,ease:"power2.inOut"},2.4);
    tl.fromTo("#ou-dim",{opacity:0},{opacity:1,duration:.5},2.5);
    tl.fromTo("#ou-logo",{opacity:0,scale:.85,filter:"blur(12px)"},{opacity:1,scale:1,filter:"blur(0px)",duration:.7,ease:"expo.out"},2.6);
    tl.fromTo("#ou-h",{opacity:0,y:30},{opacity:1,y:0,duration:.5,ease:"expo.out"},2.85);
    tl.fromTo("#ou-sub",{opacity:0,scale:1.14},{opacity:1,scale:1,duration:.7,ease:"expo.out"},3.0);
    tl.fromTo("#ou-cta",{opacity:0,scale:.8},{opacity:1,scale:1,duration:.45,ease:"back.out(1.8)"},3.3);
    tl.fromTo("#ou-photo",{scale:1.0},{scale:1.06,duration:2.7,ease:"none",immediateRender:false},3.0);
    tl.to("#ou-wipe",{opacity:1,duration:.5,ease:"power2.in"},5.2);
""")))

# ------------------------------------------------------------------ CAPTIONS
words = json.load(open(sys.argv[2]))
words = [w for w in words if w["s"] < 25]
fix = {"istri": "isteri", "forming": "foaming", "membahagalkan.": "membahagiakan.", "stock": "stok", "terhat.": "terhad.",
       "perfy": "", "meminat": "Midnight", "fantasy.": "Fantasy.", "So,": "", "bombshell": "Bombshell", "Kadang-kadang": "Kadang-kadang", "atau": "ataupun"}
toks = []
for w in words:
    t = w["w"].strip()
    t = fix.get(t, t)
    if not t:
        continue
    if t.startswith("-"):  # kadang-kadang / sangat-sangat
        toks[-1]["t"] += t; toks[-1]["e"] = w["e"]; continue
    if t == "hargai." and toks and toks[-1]["t"] == "dia":
        toks[-1]["t"] = "dihargai."; toks[-1]["e"] = w["e"]; continue
    toks.append({"t": t, "s": w["s"], "e": w["e"]})
toks[0]["s"] = 0.25
print(len(toks), [t["t"] for t in toks])
groups_def = [4, 3, 4, 5, 5, 3, 3, 3, 3, 3, 4, 4, 3, 2, 1, 3, 4, 4, 5]
EMPH = {"hadiah", "hadiah,", "dihargai.", "mahal", "membahagiakan.", "foaming", "Bombshell", "Midnight", "Fantasy.", "terhad.", "kuning", "hadiahkan", "terfikir,", "kecil", "minta"}
groups = []; i = 0
for n in groups_def:
    groups.append(toks[i:i + n]); i += n
assert i == len(toks), (i, len(toks), [t["t"] for t in toks])
cap_html = []; cap_js = []
for gi, g in enumerate(groups):
    s = round(max(g[0]["s"] - 0.05, 0.2), 2)
    nxt = groups[gi + 1][0]["s"] - 0.05 if gi + 1 < len(groups) else g[-1]["e"] + 0.3
    e = round(min(g[-1]["e"] + 0.35, nxt), 2)
    spans = []
    for wi, w in enumerate(g):
        txt = w["t"].strip(",.?")
        if gi == 0 and wi == 3: txt += "?"
        cls = "cw em" if w["t"] in EMPH else "cw"
        spans.append(f'<span class="{cls}" id="cw{gi}_{wi}">{txt}</span>')
        cap_js.append(f'tl.fromTo("#cw{gi}_{wi}",{{opacity:.0,y:18,filter:"blur(6px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.14,ease:"power3.out"}},{max(w["s"]-0.04, s):.2f});')
    cap_html.append(f'<div class="cg clip" id="cg{gi}" data-start="{s}" data-duration="{round(e - s, 2)}"><div class="cgi">{" ".join(spans)}</div></div>')
    cap_js.append(f'tl.to("#cg{gi} .cgi",{{opacity:0,duration:.1,ease:"power2.in"}},{e - 0.1:.2f});')
captions = scene("captions", 24.75, """
  .cg{position:absolute;left:0;right:0;top:1170px;height:170px;display:flex;align-items:center;justify-content:center}
  .cgi{max-width:880px;text-align:center;font-family:'Jakarta';font-weight:800;font-size:66px;line-height:1.08;color:#FFFFFF;
       text-shadow:0 4px 24px rgba(0,0,0,.75),0 1px 2px rgba(0,0,0,.9)}
  .cw{display:inline-block}
  .cw.em{font-family:'Bodoni Moda';font-style:italic;font-weight:500;font-size:80px;color:#F3D9A4}
""", "\n".join(cap_html), "\n".join(cap_js))

# ------------------------------------------------------------------ WRITE
os.makedirs(f"{P}/compositions", exist_ok=True)
for cid, s, d, html in scenes:
    open(f"{P}/compositions/{cid}.html", "w").write(html)
open(f"{P}/compositions/captions.html", "w").write(captions)

hosts = "\n".join(
    f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{s}" data-duration="{d}" data-track-index="1" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:{2 if cid != "outro" else 2}"></div>'
    for cid, s, d, _ in scenes)
index = f"""<!doctype html>
<html lang="ms">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:#0A0807; }}
      #bg {{ position:absolute; inset:0; background:#0A0807; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="{W}" data-height="{H}">
{hosts}
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="24.75" data-track-index="2" data-track-kind="captions" data-width="{W}" data-height="{H}" style="z-index:5"></div>
      <audio id="mix" class="clip" data-start="0" data-duration="{DUR}" data-track-index="3" data-volume="1" src="assets/audio/mix.wav"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
open(f"{P}/index.html", "w").write(index)
print("ok", len(scenes), "scenes;", len(groups), "caption groups")
