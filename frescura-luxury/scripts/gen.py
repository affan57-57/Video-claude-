# Generates the Frescura Body HyperFrames project (index.html + compositions/*.html)
import json, os, sys, random
P = sys.argv[1]
os.makedirs(P + "/compositions", exist_ok=True)
VO = 0.15            # voice starts here
TOTAL = 34.6

FONTS = """
@font-face{font-family:'Bodoni Moda';src:url('assets/fonts/BodoniModa.woff2') format('woff2');font-weight:400 900;font-style:normal}
@font-face{font-family:'Bodoni Moda';src:url('assets/fonts/BodoniModa-Italic.woff2') format('woff2');font-weight:400 900;font-style:italic}
@font-face{font-family:'Jost';src:url('assets/fonts/Jost.woff2') format('woff2');font-weight:300 800;font-style:normal}
"""
TOK = """
#root{position:absolute;inset:0;overflow:hidden;--ivory:#F7F0E6;--gold:#D9B97E;--gold2:#F3DDAE;--esp:#120C0A;--rose:#C0212E;--violet:#7A55E0;--bag:#FFC629;font-family:'Jost',sans-serif;color:var(--ivory)}
.abs{position:absolute}
.lbl{font-family:'Jost';font-weight:500;letter-spacing:.42em;text-transform:uppercase;color:var(--gold);font-size:29px}
.serif{font-family:'Bodoni Moda'}
.it{font-family:'Bodoni Moda';font-style:italic}
.goldtxt{background:linear-gradient(100deg,#B98F4F 0%,#F3DDAE 38%,#D9B97E 60%,#FFF1CF 80%,#B98F4F 100%);-webkit-background-clip:text;background-clip:text;color:transparent}
.row{left:0;width:1080px;text-align:center}
"""

def scene(cid, body, script, extra_css=""):
    return f"""<template>
<style>{FONTS}{TOK}{extra_css}</style>
<div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
{body}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{script}
window.__timelines["{cid}"] = tl;
</script>
</template>
"""

def bottles_svg_podium(prefix, top=1150):
    # marble podium (decorative) + gold rim
    return f"""
<div id="{prefix}-pod" class="abs" style="left:150px;top:{top-40}px;width:780px;height:600px">
  <div class="abs" style="left:0;top:0;width:780px;height:90px;border-radius:50%;background:radial-gradient(ellipse at 50% 40%,#fbf5ec 0%,#e7dccd 55%,#c9b8a3 100%);box-shadow:0 0 0 2px rgba(217,185,126,.85),0 30px 60px rgba(0,0,0,.5)"></div>
  <div class="abs" style="left:0;top:45px;width:780px;height:520px;background:linear-gradient(90deg,#a99782 0%,#efe6da 30%,#fbf6ef 50%,#e3d7c7 70%,#9d8b77 100%);-webkit-mask:linear-gradient(#000 0%,#000 40%,transparent 100%);mask:linear-gradient(#000 0%,#000 40%,transparent 100%)"></div>
  <svg class="abs" style="left:0;top:45px" width="780" height="300" viewBox="0 0 780 300"><path d="M90 0 C 140 60, 70 120, 180 210 M420 0 C 380 90, 470 150, 430 300 M640 0 C 690 70, 610 160, 700 240" stroke="rgba(120,100,80,.25)" stroke-width="2" fill="none"/></svg>
</div>"""

# ------------------------------------------------------------------ MALL BACKDROP
rnd = random.Random(7)
bokeh = []
for i in range(22):
    x = rnd.uniform(-60, 1080); y = rnd.uniform(80, 1500); s = rnd.uniform(40, 170)
    c = rnd.choice(["255,226,170", "255,240,215", "240,200,140", "255,214,180"])
    o = rnd.uniform(.10, .32); b = rnd.uniform(6, 22); dx = rnd.uniform(-90, 90)
    bokeh.append((x, y, s, c, o, b, dx))
mall_body = """
<div id="m-bg" class="abs" style="inset:0;background:radial-gradient(ellipse 90% 60% at 50% 32%,#47332a 0%,#22170f 45%,#0b0706 100%)"></div>
<div id="m-arch" class="abs" style="left:170px;top:250px;width:740px;height:1150px;border:2px solid rgba(217,185,126,.35);border-bottom:none;border-radius:370px 370px 0 0"></div>
<div id="m-arch2" class="abs" style="left:200px;top:280px;width:680px;height:1120px;border:1px solid rgba(217,185,126,.18);border-bottom:none;border-radius:340px 340px 0 0;background:radial-gradient(ellipse at 50% 20%,rgba(255,230,190,.10),rgba(0,0,0,0) 70%)"></div>
<div id="m-pl" class="abs" style="left:-20px;top:0;width:130px;height:1920px;background:linear-gradient(90deg,#3b2c22,#c9b9a4 40%,#efe5d7 55%,#8f7a65);opacity:.55"></div>
<div id="m-pr" class="abs" style="left:970px;top:0;width:130px;height:1920px;background:linear-gradient(90deg,#8f7a65,#efe5d7 45%,#c9b9a4 60%,#3b2c22);opacity:.55"></div>
<div class="abs" style="left:110px;top:0;width:2px;height:1920px;background:linear-gradient(#0000,#D9B97E 30%,#D9B97E 70%,#0000);opacity:.6"></div>
<div class="abs" style="left:968px;top:0;width:2px;height:1920px;background:linear-gradient(#0000,#D9B97E 30%,#D9B97E 70%,#0000);opacity:.6"></div>
<div id="m-floor" class="abs" style="left:0;top:1400px;width:1080px;height:520px;background:linear-gradient(#2a1d16,#0d0907);"></div>
<div class="abs" style="left:0;top:1400px;width:1080px;height:2px;background:linear-gradient(90deg,#0000,#D9B97E,#0000);opacity:.7"></div>
"""
for i, (x, y, s, c, o, b, dx) in enumerate(bokeh):
    mall_body += f'<div id="m-b{i}" class="abs" style="left:{x:.0f}px;top:{y:.0f}px;width:{s:.0f}px;height:{s:.0f}px;border-radius:50%;background:radial-gradient(circle,rgba({c},{o:.2f}) 0%,rgba({c},{o*0.6:.2f}) 55%,rgba({c},0) 72%);filter:blur({b:.0f}px)"></div>\n'
mall_body += """
<div id="m-sp1" class="abs" style="left:140px;top:-200px;width:420px;height:1700px;transform-origin:50% 0%;background:linear-gradient(rgba(255,236,200,.22),rgba(255,236,200,0) 85%);clip-path:polygon(45% 0,55% 0,100% 100%,0 100%);filter:blur(10px)"></div>
<div id="m-sp2" class="abs" style="left:520px;top:-200px;width:420px;height:1700px;transform-origin:50% 0%;background:linear-gradient(rgba(255,236,200,.18),rgba(255,236,200,0) 85%);clip-path:polygon(45% 0,55% 0,100% 100%,0 100%);filter:blur(10px)"></div>
<div id="m-vig" class="abs" style="inset:0;background:radial-gradient(ellipse 80% 70% at 50% 45%,rgba(0,0,0,0) 55%,rgba(0,0,0,.55) 100%)"></div>
"""
mall_js = ""
for i, (x, y, s, c, o, b, dx) in enumerate(bokeh):
    mall_js += f'tl.fromTo("#m-b{i}",{{x:0}},{{x:{dx:.0f},duration:{TOTAL},ease:"none"}},0);\n'
mall_js += f"""
tl.fromTo("#m-sp1",{{rotation:-7}},{{rotation:6,duration:{TOTAL},ease:"sine.inOut"}},0);
tl.fromTo("#m-sp2",{{rotation:7}},{{rotation:-5,duration:{TOTAL},ease:"sine.inOut"}},0);
tl.fromTo("#m-arch",{{y:0}},{{y:-40,duration:{TOTAL},ease:"none"}},0);
tl.fromTo("#m-arch2",{{y:0}},{{y:-55,duration:{TOTAL},ease:"none"}},0);
"""
open(P + "/compositions/mall.html", "w").write(scene("mall", mall_body, mall_js))

# ------------------------------------------------------------------ S1 HOOK 0 - 4.2
s1 = """
<div id="s1-wrap" class="abs" style="inset:0">
 <div id="s1-top" class="abs row lbl" style="top:262px">— Sebelum Terlambat —</div>
 <div id="s1-chip" class="abs" style="left:340px;top:318px;width:400px;height:76px;border-radius:38px;background:linear-gradient(90deg,#8e1520,#c0212e);box-shadow:0 10px 40px rgba(192,33,46,.45);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:34px;letter-spacing:.24em">SEKEJAP, ABANG!</div>
 <div id="s1-h1" class="abs row serif" style="top:450px;font-size:124px;font-weight:700;line-height:1;letter-spacing:-.01em">
   <span id="s1-w1" style="display:inline-block">Jangan</span> <span id="s1-w2" style="display:inline-block">tunggu</span></div>
 <div id="s1-h2" class="abs row it" style="top:590px;font-size:132px;font-weight:600;line-height:1.05">
   <span id="s1-w3" class="goldtxt" style="display:inline-block;padding:0 6px">isteri</span><br><span id="s1-w4" class="goldtxt" style="display:inline-block;padding:0 10px">merajuk.</span></div>
 <svg id="s1-heart" class="abs" style="left:440px;top:950px" width="200" height="180" viewBox="0 0 200 180">
   <g id="s1-hl"><path id="s1-hlp" d="M100 168 L22 92 C-8 60 10 12 52 12 C74 12 90 26 100 42 L88 70 L108 92 L92 120 Z" fill="none" stroke="#D9B97E" stroke-width="5" stroke-linejoin="round"/></g>
   <g id="s1-hr"><path id="s1-hrp" d="M100 168 L178 92 C208 60 190 12 148 12 C126 12 110 26 100 42 L88 70 L108 92 L92 120 Z" fill="none" stroke="#D9B97E" stroke-width="5" stroke-linejoin="round"/></g>
 </svg>
 <div id="s1-l3" class="abs row" style="top:1150px;font-size:46px;font-weight:400;letter-spacing:.06em;color:#e9dccb">baru nak tunjuk</div>
 <div id="s1-l4" class="abs row it" style="top:1205px;font-size:104px;font-weight:600;color:#ff5b68;text-shadow:0 0 40px rgba(255,60,80,.45)">kasih sayang?</div>
</div>
"""
w = lambda t: round(t + VO, 2)   # voice-time -> film time
s1js = f"""
tl.fromTo("#s1-chip",{{scale:0.4,opacity:0}},{{scale:1,opacity:1,duration:0.45,ease:"back.out(2.2)"}},{w(0.0)});
tl.fromTo("#s1-top",{{opacity:0,y:-14,filter:"blur(8px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.8,ease:"expo.out"}},0.05);
tl.fromTo("#s1-h1",{{scale:1.12}},{{scale:1,duration:0.5,ease:"expo.out"}},{w(0.0)});
tl.fromTo(["#s1-w1","#s1-w2","#s1-w3","#s1-w4"],{{opacity:0.28,filter:"blur(0px)"}},{{opacity:0.28,duration:0.01}},0);
tl.to("#s1-w1",{{opacity:1,duration:0.12}},{w(0.54)});
tl.to("#s1-w2",{{opacity:1,duration:0.12}},{w(0.92)});
tl.fromTo("#s1-w3",{{opacity:0.28,y:20}},{{opacity:1,y:0,duration:0.25,ease:"expo.out"}},{w(1.24)});
tl.fromTo("#s1-w4",{{opacity:0.28,y:20}},{{opacity:1,y:0,duration:0.25,ease:"expo.out"}},{w(1.80)});
tl.fromTo("#s1-heart",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2)"}},{w(1.62)});
tl.fromTo(["#s1-hlp","#s1-hrp"],{{strokeDasharray:520,strokeDashoffset:520}},{{strokeDashoffset:0,duration:0.4,ease:"power2.out"}},{w(1.62)});
tl.fromTo("#s1-hl",{{x:0,rotation:0}},{{x:-26,rotation:-12,transformOrigin:"50% 100%",duration:0.3,ease:"power3.out"}},{w(1.95)});
tl.fromTo("#s1-hr",{{x:0,rotation:0}},{{x:26,rotation:12,transformOrigin:"50% 100%",duration:0.3,ease:"power3.out"}},{w(1.95)});
tl.fromTo("#s1-l3",{{opacity:0,filter:"blur(8px)"}},{{opacity:1,filter:"blur(0px)",duration:0.2}},{w(2.24)});
tl.fromTo("#s1-l4",{{opacity:0,scale:1.25,filter:"blur(10px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:0.35,ease:"expo.out"}},{w(3.48)});
tl.to("#s1-hl",{{x:0,rotation:0,duration:0.35,ease:"back.out(2)"}},{w(3.5)});
tl.to("#s1-hr",{{x:0,rotation:0,duration:0.35,ease:"back.out(2)"}},{w(3.5)});
tl.to(["#s1-hlp","#s1-hrp"],{{fill:"#e2283a",stroke:"#ff8f99",duration:0.25}},{w(3.5)});
tl.to("#s1-wrap",{{y:-140,opacity:0,filter:"blur(14px)",duration:0.22,ease:"power3.in"}},4.0);
"""
open(P + "/compositions/s1.html", "w").write(scene("s1", s1, s1js))

# ------------------------------------------------------------------ S2 4.2 - 9.1  (local)
S2 = 4.2
L = lambda t, s: round(t + VO - s, 2)
s2 = """
<div id="s2-wrap" class="abs" style="inset:0">
 <div id="s2-lbl" class="abs row lbl" style="top:250px">Tip 01 · Hargai Selagi Ada</div>
 <div id="s2-frame" class="abs" style="left:250px;top:300px;width:580px;height:700px;border-radius:290px 290px 28px 28px;border:2px solid rgba(217,185,126,.7)"></div>
 <div id="s2-card" class="abs" style="left:270px;top:320px;width:540px;height:660px;border-radius:270px 270px 22px 22px;overflow:hidden;box-shadow:0 40px 80px rgba(0,0,0,.55)">
   <img id="s2-img" src="assets/img/flatlay-linen.jpg" style="position:absolute;left:-40px;top:-70px;width:620px;height:1097px;object-fit:cover">
 </div>
 <div id="s2-line" class="abs" style="left:220px;top:1066px;width:640px;height:2px;background:linear-gradient(90deg,#D9B97E,#F3DDAE,#D9B97E);transform-origin:0 50%"></div>
 <div id="s2-n1" class="abs" style="left:90px;top:1048px;width:300px;text-align:center"><div style="margin:0 auto;width:38px;height:38px;border-radius:50%;background:#F7F0E6;box-shadow:0 0 24px rgba(255,236,200,.7)"></div><div style="margin-top:16px;font-size:28px;font-weight:600;letter-spacing:.08em">PERKARA KECIL</div></div>
 <div id="s2-n2" class="abs" style="left:380px;top:1048px;width:320px;text-align:center"><div style="margin:0 auto;width:38px;height:38px;border-radius:50%;background:#F7F0E6;box-shadow:0 0 24px rgba(255,236,200,.7)"></div><div style="margin-top:16px;font-size:28px;font-weight:600;letter-spacing:.08em">HARI INI</div></div>
 <div id="s2-n3" class="abs" style="left:700px;top:1048px;width:320px;text-align:center"><div style="margin:0 auto;width:38px;height:38px;border-radius:50%;background:#D9B97E;box-shadow:0 0 30px rgba(243,221,174,.9)"></div><div class="it goldtxt" style="margin-top:6px;font-size:40px;font-weight:600">kenangan manis</div></div>
</div>
"""
s2js = f"""
tl.fromTo("#s2-lbl",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:0.5,ease:"expo.out"}},0.05);
tl.fromTo("#s2-card",{{clipPath:"inset(100% 0% 0% 0% round 270px 270px 22px 22px)"}},{{clipPath:"inset(0% 0% 0% 0% round 270px 270px 22px 22px)",duration:0.6,ease:"expo.out"}},0.0);
tl.fromTo("#s2-frame",{{opacity:0,scale:1.08}},{{opacity:1,scale:1,duration:0.8,ease:"expo.out"}},0.15);
tl.fromTo("#s2-img",{{scale:1.18,y:30}},{{scale:1.0,y:0,duration:4.9,ease:"power1.out"}},0);
tl.fromTo("#s2-line",{{scaleX:0}},{{scaleX:1,duration:3.2,ease:"power2.inOut"}},{L(4.52,S2)});
tl.fromTo("#s2-n1",{{opacity:0,y:24,scale:0.7}},{{opacity:1,y:0,scale:1,duration:0.4,ease:"back.out(2)"}},{L(4.52,S2)});
tl.fromTo("#s2-n2",{{opacity:0,y:24,scale:0.7}},{{opacity:1,y:0,scale:1,duration:0.4,ease:"back.out(2)"}},{L(6.0,S2)});
tl.fromTo("#s2-n3",{{opacity:0,y:24,scale:0.7}},{{opacity:1,y:0,scale:1,duration:0.45,ease:"back.out(2)"}},{L(7.44,S2)});
tl.to("#s2-wrap",{{scale:0.86,opacity:0,filter:"blur(12px)",duration:0.3,ease:"power3.in"}},4.6);
"""
open(P + "/compositions/s2.html", "w").write(scene("s2", s2, s2js))

# ------------------------------------------------------------------ S3 9.1 - 14.75
S3 = 9.1
BH, BW_B, BW_N = 680, round(680*372/1138), round(680*371/1146)
s3 = f"""
<div id="s3-beam1" class="abs" style="left:110px;top:-150px;width:520px;height:1500px;transform-origin:50% 0;background:linear-gradient(rgba(255,240,210,.42),rgba(255,240,210,0) 90%);clip-path:polygon(44% 0,56% 0,100% 100%,0 100%);filter:blur(14px);transform:rotate(-14deg)"></div>
<div id="s3-beam2" class="abs" style="left:450px;top:-150px;width:520px;height:1500px;transform-origin:50% 0;background:linear-gradient(rgba(255,240,210,.42),rgba(255,240,210,0) 90%);clip-path:polygon(44% 0,56% 0,100% 100%,0 100%);filter:blur(14px);transform:rotate(14deg)"></div>
<div id="s3-stage" class="abs" style="inset:0">
 {bottles_svg_podium("s3", 1150)}
 <div id="s3-glow" class="abs" style="left:240px;top:520px;width:600px;height:700px;border-radius:50%;background:radial-gradient(ellipse,rgba(255,228,180,.35),rgba(0,0,0,0) 65%)"></div>
 <img id="s3-bb" class="abs" src="assets/img/bombshell-cut.png" style="left:{540-BW_B-18}px;top:{1150-BH}px;width:{BW_B}px;height:{BH}px;filter:drop-shadow(0 30px 30px rgba(0,0,0,.6))">
 <img id="s3-nb" class="abs" src="assets/img/noche-cut.png" style="left:{540+18}px;top:{1150-BH}px;width:{BW_N}px;height:{BH}px;filter:drop-shadow(0 30px 30px rgba(0,0,0,.6))">
 <img id="s3-bbr" class="abs" src="assets/img/bombshell-cut.png" style="left:{540-BW_B-18}px;top:1152px;width:{BW_B}px;height:{BH}px;transform:scaleY(-1);opacity:.22;-webkit-mask:linear-gradient(to top,#000 0%,transparent 35%);mask:linear-gradient(to top,#000 0%,transparent 35%)">
 <img id="s3-nbr" class="abs" src="assets/img/noche-cut.png" style="left:{540+18}px;top:1152px;width:{BW_N}px;height:{BH}px;transform:scaleY(-1);opacity:.22;-webkit-mask:linear-gradient(to top,#000 0%,transparent 35%);mask:linear-gradient(to top,#000 0%,transparent 35%)">
 <div id="s3-lbl" class="abs row lbl" style="top:250px">Frescura Body</div>
 <div id="s3-title" class="abs row it" style="top:292px;font-size:92px;font-weight:600;line-height:1"><span id="s3-t1" class="goldtxt" style="display:inline-block;padding:0 6px">Foaming</span> <span id="s3-t2" style="display:inline-block">Body Wash</span></div>
 <div id="s3-c1" class="abs" style="left:36px;top:560px;width:220px;height:62px;border:1.5px solid #D9B97E;border-radius:31px;background:rgba(18,12,10,.65);display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:600;letter-spacing:.1em">OCEAN SALT</div>
 <div id="s3-c2" class="abs" style="top:700px;left:800px;width:250px;height:62px;border:1.5px solid #D9B97E;border-radius:31px;background:rgba(18,12,10,.65);display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:600;letter-spacing:.04em">AROMATHERAPY</div>
 <div id="s3-c3" class="abs" style="left:26px;top:860px;width:240px;height:62px;border:1.5px solid #D9B97E;border-radius:31px;background:rgba(18,12,10,.65);display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:600;letter-spacing:.06em">GENTLE FOAM</div>
</div>
<div id="s3-arch" class="abs" style="left:0;top:0;width:1080px;height:1920px;overflow:hidden">
 <video id="s3-vid" class="clip" src="assets/video/foam.mp4" muted playsinline data-start="3.2" data-duration="2.45" data-media-start="11.3" style="position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover"></video>
 <div class="abs" style="inset:0;background:linear-gradient(rgba(12,8,7,.78) 0%,rgba(12,8,7,0) 26%,rgba(12,8,7,0) 52%,rgba(12,8,7,.8) 78%)"></div>
 <div id="s3-vl" class="abs row lbl" style="top:262px;color:#F3DDAE">Busa lembut · terus dari pam</div>
 <div id="s3-vt" class="abs row it" style="top:310px;font-size:84px;font-weight:600"><span class="goldtxt" style="padding:0 6px">Tanda</span> menghargai</div>
</div>
"""
s3js = f"""
tl.fromTo(["#s3-beam1","#s3-beam2"],{{opacity:0}},{{opacity:1,duration:0.25,ease:"power2.out",stagger:0.12}},0.0);
tl.fromTo("#s3-pod",{{y:260,opacity:0}},{{y:0,opacity:1,duration:0.7,ease:"expo.out"}},0.05);
tl.fromTo("#s3-glow",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.9,ease:"expo.out"}},0.3);
tl.fromTo(["#s3-bb","#s3-nb"],{{y:-120,opacity:0,filter:"blur(12px) drop-shadow(0 30px 30px rgba(0,0,0,.6))"}},{{y:0,opacity:1,filter:"blur(0px) drop-shadow(0 30px 30px rgba(0,0,0,.6))",duration:0.55,ease:"power4.out",stagger:0.14}},0.3);
tl.fromTo(["#s3-bbr","#s3-nbr"],{{opacity:0}},{{opacity:0.22,duration:0.4,stagger:0.14}},0.65);
tl.fromTo("#s3-lbl",{{opacity:0,y:-14,filter:"blur(8px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.7,ease:"expo.out"}},0.6);
tl.fromTo("#s3-t1",{{opacity:0,filter:"blur(10px)",scale:1.3}},{{opacity:1,filter:"blur(0px)",scale:1,duration:0.3,ease:"expo.out"}},{L(10.1,S3)});
tl.fromTo("#s3-t2",{{opacity:0,filter:"blur(10px)"}},{{opacity:1,filter:"blur(0px)",duration:0.2}},{L(10.32,S3)});
tl.fromTo("#s3-c1",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.8)"}},{L(10.88,S3)});
tl.fromTo("#s3-c2",{{opacity:0,x:60}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.8)"}},{L(11.42,S3)});
tl.fromTo("#s3-c3",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.8)"}},{L(11.76,S3)});
tl.fromTo("#s3-arch",{{clipPath:"inset(46% 40% 30% 40% round 200px 200px 24px 24px)",opacity:0}},{{clipPath:"inset(0% 0% 0% 0% round 0px 0px 0px 0px)",opacity:1,duration:0.65,ease:"power3.inOut"}},3.05);
tl.to("#s3-stage",{{scale:1.15,opacity:0,filter:"blur(15px)",duration:0.45,ease:"power2.in"}},3.1);
tl.fromTo("#s3-vl",{{opacity:0,y:-16}},{{opacity:1,y:0,duration:0.4,ease:"expo.out"}},3.5);
tl.fromTo("#s3-vt",{{opacity:0,filter:"blur(8px)"}},{{opacity:1,filter:"blur(0px)",duration:0.2}},3.6);
tl.to("#s3-arch",{{x:-1080,duration:0.28,ease:"power3.in"}},5.37);
"""
open(P + "/compositions/s3.html", "w").write(scene("s3", s3, s3js))

# ------------------------------------------------------------------ S4 14.75 - 19.9
S4 = 14.75
BH4 = 600; bw4b = round(BH4*372/1138); bw4n = round(BH4*371/1146)
s4 = f"""
<div id="s4-wrap" class="abs" style="inset:0">
 <div id="s4-two" class="abs it goldtxt" style="left:0;top:330px;width:1080px;text-align:center;font-size:560px;font-weight:700;line-height:1;transform-origin:50% 50%">2</div>
 <div id="s4-sub" class="abs row lbl" style="top:1000px;font-size:34px">Pilihan Haruman</div>
 <div id="s4-head" class="abs row" style="top:236px;font-size:34px;font-weight:600;letter-spacing:.34em;color:#F3DDAE">2 PILIHAN HARUMAN</div>
 <div id="s4-pl" class="abs" style="left:40px;top:290px;width:490px;height:830px;border-radius:30px;overflow:hidden;background:radial-gradient(ellipse at 50% 70%,#d4303e 0%,#7b0f19 55%,#2a0508 100%);box-shadow:0 30px 70px rgba(0,0,0,.5)">
   <div class="abs" style="left:0;top:40px;width:490px;text-align:center;font-size:28px;letter-spacing:.3em;font-weight:500;color:#ffd9dc">WOMAN GLORY</div>
   <div class="abs it" style="left:0;top:76px;width:490px;text-align:center;font-size:70px;font-weight:600;color:#fff">Bombshell</div>
   <img id="s4-bb" class="abs" src="assets/img/bombshell-cut.png" style="left:{245-bw4b//2}px;top:200px;width:{bw4b}px;height:{BH4}px;filter:drop-shadow(0 30px 30px rgba(0,0,0,.55))">
 </div>
 <div id="s4-pr" class="abs" style="left:550px;top:290px;width:490px;height:830px;border-radius:30px;overflow:hidden;background:radial-gradient(ellipse at 50% 70%,#8a63ff 0%,#3a1f86 55%,#0f0726 100%);box-shadow:0 30px 70px rgba(0,0,0,.5)">
   <div class="abs" style="left:0;top:40px;width:490px;text-align:center;font-size:28px;letter-spacing:.3em;font-weight:500;color:#e2d6ff">NOCHE</div>
   <div class="abs it" style="left:0;top:80px;width:490px;text-align:center;font-size:54px;font-weight:600;line-height:1.05;color:#fff">Midnight Fantasy</div>
   <img id="s4-nb" class="abs" src="assets/img/noche-cut.png" style="left:{245-bw4n//2}px;top:200px;width:{bw4n}px;height:{BH4}px;filter:drop-shadow(0 30px 30px rgba(0,0,0,.55))">
 </div>
</div>
"""
s4js = f"""
tl.fromTo("#s4-two",{{opacity:0,scale:0.5,filter:"blur(20px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:0.45,ease:"expo.out"}},{L(14.94,S4)-0.1});
tl.fromTo("#s4-sub",{{opacity:0,y:-14,filter:"blur(8px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.6,ease:"expo.out"}},{L(15.24,S4)});
tl.to(["#s4-two","#s4-sub"],{{opacity:0,scale:0.7,filter:"blur(14px)",duration:0.25,ease:"power3.in"}},{L(16.5,S4)-0.2});
tl.fromTo("#s4-head",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:0.4,ease:"expo.out"}},{L(16.5,S4)});
tl.fromTo("#s4-pl",{{clipPath:"inset(0% 100% 0% 0% round 30px)"}},{{clipPath:"inset(0% 0% 0% 0% round 30px)",duration:0.5,ease:"expo.out"}},{L(16.7,S4)});
tl.fromTo("#s4-bb",{{y:80,opacity:0,scale:0.9}},{{y:0,opacity:1,scale:1,duration:0.6,ease:"expo.out"}},{L(16.8,S4)});
tl.fromTo("#s4-pr",{{clipPath:"inset(0% 0% 0% 100% round 30px)"}},{{clipPath:"inset(0% 0% 0% 0% round 30px)",duration:0.5,ease:"expo.out"}},{L(18.3,S4)});
tl.fromTo("#s4-nb",{{y:80,opacity:0,scale:0.9}},{{y:0,opacity:1,scale:1,duration:0.6,ease:"expo.out"}},{L(18.4,S4)});
tl.to("#s4-wrap",{{y:-1920,duration:0.35,ease:"power3.in"}},4.8);
"""
open(P + "/compositions/s4.html", "w").write(scene("s4", s4, s4js))

# ------------------------------------------------------------------ S5 19.9 - 23.35
S5 = 19.9
s5 = """
<video id="s5-vid" class="clip" src="assets/video/foam.mp4" muted playsinline data-start="0" data-duration="3.45" data-media-start="17.3" style="position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover"></video>
<div class="abs" style="inset:0;background:linear-gradient(rgba(12,8,7,.86) 0%,rgba(12,8,7,.35) 38%,rgba(12,8,7,.35) 55%,rgba(12,8,7,.88) 80%)"></div>
<div id="s5-wrap" class="abs" style="inset:0">
 <div id="s5-lbl" class="abs row lbl" style="top:250px">Ingat, Abang</div>
 <div id="s5-t1" class="abs row it" style="top:295px;font-size:124px;font-weight:600;line-height:1"><span class="goldtxt" style="padding:0 8px">Bahagia</span> isteri</div>
 <div id="s5-t2" class="abs row" style="top:440px;font-size:40px;font-weight:500;letter-spacing:.3em">TAK SEMESTINYA</div>
 <div id="s5-tag" class="abs" style="left:250px;top:560px;width:580px;height:300px;transform-origin:50% -60px">
   <div class="abs" style="left:288px;top:-70px;width:2px;height:80px;background:#D9B97E"></div>
   <div class="abs" style="left:0;top:0;width:580px;height:300px;border-radius:26px;background:linear-gradient(135deg,#f9f2e7,#e8d9c2);box-shadow:0 30px 60px rgba(0,0,0,.55);color:#1b120d">
     <div class="abs" style="left:270px;top:22px;width:40px;height:40px;border-radius:50%;background:#1b120d;opacity:.85"></div>
     <div class="abs" style="left:0;top:92px;width:580px;text-align:center;font-size:30px;letter-spacing:.35em;font-weight:500">HADIAH</div>
     <div class="abs serif" style="left:0;top:140px;width:580px;text-align:center;font-size:88px;font-weight:800;letter-spacing:.02em">MAHAL</div>
     <div id="s5-strike" class="abs" style="left:60px;top:196px;width:460px;height:7px;border-radius:6px;background:#c0212e;transform-origin:0 50%"></div>
   </div>
 </div>
</div>
"""
s5js = f"""
tl.fromTo("#s5-lbl",{{opacity:0,y:-16}},{{opacity:1,y:0,duration:0.4,ease:"expo.out"}},0.0);
tl.fromTo("#s5-t1",{{opacity:0,filter:"blur(10px)",scale:1.1}},{{opacity:1,filter:"blur(0px)",scale:1,duration:0.3,ease:"expo.out"}},{L(19.95,S5)});
tl.fromTo("#s5-t2",{{opacity:0,y:-14,filter:"blur(8px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.4,ease:"expo.out"}},{L(20.85,S5)});
tl.fromTo("#s5-tag",{{opacity:0,rotation:-24,y:-80}},{{opacity:1,rotation:0,y:0,duration:0.8,ease:"elastic.out(1,0.55)"}},{L(21.55,S5)});
tl.fromTo("#s5-strike",{{scaleX:0,rotation:-6}},{{scaleX:1,rotation:-6,duration:0.18,ease:"power3.out"}},{L(22.6,S5)});
tl.to("#s5-tag",{{rotation:6,duration:0.12,ease:"power2.out"}},{L(22.68,S5)});
tl.to("#s5-tag",{{rotation:0,duration:0.4,ease:"elastic.out(1,0.5)"}},{L(22.8,S5)});
tl.to("#s5-wrap",{{x:-200,opacity:0,filter:"blur(12px)",duration:0.22,ease:"power3.in"}},3.2);
"""
open(P + "/compositions/s5.html", "w").write(scene("s5", s5, s5js))

# ------------------------------------------------------------------ S6 23.2 - 28.05
S6 = 23.2
bag = """<svg width="110" height="110" viewBox="0 0 64 64"><path d="M14 22 h36 l-3 32 h-30 z" fill="#1b120d"/><path d="M24 24 v-6 a8 8 0 0 1 16 0 v6" fill="none" stroke="#1b120d" stroke-width="4" stroke-linecap="round"/></svg>"""
s6 = f"""
<video id="s6-vid" class="clip" src="assets/video/foam.mp4" muted playsinline data-start="0" data-duration="4.85" data-media-start="24.6" style="position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover"></video>
<div class="abs" style="inset:0;background:rgba(12,8,7,.74)"></div>
<div id="s6-wrap" class="abs" style="inset:0">
 <div id="s6-h" class="abs row" style="top:250px;font-size:96px;font-weight:800;letter-spacing:.05em;line-height:1">STOK <span id="s6-hw" style="display:inline-block;color:#ff4d5a">TERHAD</span></div>
 <div class="abs" style="left:140px;top:380px;width:800px;height:16px;border-radius:8px;background:rgba(247,240,230,.15)"></div>
 <div id="s6-bar" class="abs" style="left:140px;top:380px;width:800px;height:16px;border-radius:8px;background:linear-gradient(90deg,#ff4d5a,#D9B97E);transform-origin:0 50%"></div>
 <div id="s6-bl" class="abs" style="left:140px;top:410px;font-size:28px;letter-spacing:.24em;font-weight:500;color:#e9dccb">BAKI STOK</div>
 <div id="s6-hamp" class="abs" style="left:600px;top:410px;width:300px;text-align:right;font-size:28px;letter-spacing:.2em;font-weight:700;color:#ff4d5a">HAMPIR HABIS</div>
 <div id="s6-card" class="abs" style="left:150px;top:500px;width:780px;height:560px;border-radius:40px;background:rgba(247,240,230,.07);border:1.5px solid rgba(217,185,126,.55)">
   <img class="abs" src="assets/img/bombshell-cut.png" style="left:190px;top:40px;width:{round(300*372/1138)}px;height:300px">
   <img class="abs" src="assets/img/noche-cut.png" style="left:490px;top:40px;width:{round(300*371/1146)}px;height:300px">
   <div class="abs" style="left:0;top:360px;width:780px;text-align:center;font-size:26px;letter-spacing:.3em;color:#F3DDAE">FRESCURA BODY · 500ML</div>
 </div>
 <div id="s6-btn" class="abs" style="left:210px;top:920px;width:660px;height:150px;border-radius:75px;background:linear-gradient(180deg,#ffd451,#ffb800);box-shadow:0 20px 60px rgba(255,190,0,.45);display:flex;align-items:center;justify-content:center;gap:24px;color:#1b120d;font-size:38px;font-weight:800;letter-spacing:.06em">{bag}<span>TEKAN SEKARANG</span></div>
 <div id="s6-btn2" class="abs" style="left:210px;top:920px;width:660px;height:150px;border-radius:75px;background:linear-gradient(100deg,#B98F4F,#F3DDAE 45%,#D9B97E);box-shadow:0 20px 60px rgba(217,185,126,.55);display:flex;align-items:center;justify-content:center;gap:20px;color:#1b120d;font-size:46px;font-weight:800;letter-spacing:.12em">
   <svg width="56" height="56" viewBox="0 0 24 24"><path d="M4 12.5 L9.5 18 L20 6.5" fill="none" stroke="#1b120d" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg><span>CHECKOUT</span></div>
 <div id="s6-tap" class="abs" style="left:720px;top:1000px;width:90px;height:90px;border-radius:50%;background:rgba(255,255,255,.85);box-shadow:0 0 0 10px rgba(255,255,255,.25)"></div>
 <div id="s6-warn" class="abs" style="left:700px;top:870px;padding:12px 26px;border-radius:30px;background:#c0212e;font-size:28px;font-weight:700;letter-spacing:.12em;transform-origin:0 100%">SEBELUM HABIS!</div>
</div>
"""
s6js = f"""
tl.fromTo("#s6-h",{{opacity:0,scale:1.4,filter:"blur(14px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:0.3,ease:"expo.out"}},0.0);
tl.fromTo("#s6-bar",{{scaleX:1}},{{scaleX:0.13,duration:1.4,ease:"power2.inOut"}},0.15);
tl.fromTo("#s6-bl",{{opacity:0}},{{opacity:1,duration:0.3}},0.15);
tl.fromTo("#s6-hamp",{{opacity:0,x:30}},{{opacity:1,x:0,duration:0.3,ease:"expo.out"}},1.45);
tl.fromTo("#s6-hw",{{scale:1}},{{scale:1.18,duration:0.08,ease:"power2.out"}},{L(24.12,S6)});
tl.to("#s6-hw",{{scale:1,duration:0.4,ease:"elastic.out(1,0.4)"}},{L(24.12,S6)+0.08});
tl.fromTo("#s6-h",{{x:0}},{{x:12,duration:0.04,yoyo:true,repeat:5,ease:"none"}},{L(24.12,S6)});
tl.fromTo("#s6-card",{{opacity:0,y:60}},{{opacity:1,y:0,duration:0.5,ease:"expo.out"}},0.5);
tl.fromTo("#s6-btn",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.45,ease:"back.out(2)"}},{L(24.5,S6)});
tl.fromTo("#s6-tap",{{opacity:0,x:160,y:220,scale:1.4}},{{opacity:1,x:0,y:0,scale:1,duration:0.4,ease:"power3.out"}},{L(24.6,S6)});
tl.to("#s6-tap",{{scale:0.7,duration:0.08,ease:"power2.in"}},{L(25.14,S6)-0.04});
tl.to("#s6-btn",{{scale:0.93,duration:0.08,ease:"power2.in"}},{L(25.14,S6)-0.04});
tl.to("#s6-btn",{{scale:1,duration:0.35,ease:"back.out(3)"}},{L(25.14,S6)+0.04});
tl.to("#s6-tap",{{scale:1,opacity:0,duration:0.35,ease:"power2.out"}},{L(25.14,S6)+0.04});
tl.fromTo("#s6-btn2",{{opacity:0,scale:0.9}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2.5)"}},{L(26.28,S6)});
tl.to("#s6-btn",{{opacity:0,duration:0.15}},{L(26.28,S6)});
tl.fromTo("#s6-warn",{{opacity:0,scale:0.3,rotation:-14}},{{opacity:1,scale:1,rotation:-6,duration:0.35,ease:"back.out(2.5)"}},{L(27.16,S6)});
tl.to("#s6-wrap",{{opacity:0,scale:0.9,filter:"blur(12px)",duration:0.25,ease:"power3.in"}},4.6);
"""
open(P + "/compositions/s6.html", "w").write(scene("s6", s6, s6js, "#s6-btn2{opacity:0}"))

# ------------------------------------------------------------------ S7 28.05 - 34.6
S7 = 28.05
BH7 = 560; b7b = round(BH7*372/1138); b7n = round(BH7*371/1146)
s7 = f"""
<div id="s7-beam" class="abs" style="left:280px;top:-150px;width:520px;height:1500px;background:linear-gradient(rgba(255,240,210,.40),rgba(255,240,210,0) 90%);clip-path:polygon(44% 0,56% 0,100% 100%,0 100%);filter:blur(14px)"></div>
<div id="s7-stage" class="abs" style="inset:0">
 {bottles_svg_podium("s7", 1200)}
 <img id="s7-bb" class="abs" src="assets/img/bombshell-cut.png" style="left:{540-b7b-16}px;top:{1200-BH7}px;width:{b7b}px;height:{BH7}px;filter:drop-shadow(0 30px 30px rgba(0,0,0,.6))">
 <img id="s7-nb" class="abs" src="assets/img/noche-cut.png" style="left:{540+16}px;top:{1200-BH7}px;width:{b7n}px;height:{BH7}px;filter:drop-shadow(0 30px 30px rgba(0,0,0,.6))">
 <div id="s7-l1" class="abs row lbl" style="top:250px;font-size:30px">Demi kita, abang</div>
 <div id="s7-l2" class="abs row serif" style="top:292px;font-size:120px;font-weight:600;line-height:1">Jaga hati</div>
 <div id="s7-l3" class="abs row it" style="top:388px;font-size:158px;font-weight:600;line-height:1.05">""" + "".join(f'<span class="s7-ch goldtxt" style="display:inline-block;padding:0 2px">{c}</span>' for c in "bidadari") + f"""</div>
 <div id="s7-l4" class="abs row" style="top:572px;font-size:40px;font-weight:300;letter-spacing:.3em">YANG TERCINTA</div>
</div>
<div id="s7-end" class="abs" style="inset:0;background:radial-gradient(ellipse at 50% 40%,rgba(8,8,14,.97),rgba(2,2,5,1))">
 <img id="s7-logo" class="abs" src="assets/img/logo.jpg" style="left:190px;top:330px;width:700px;height:700px;mix-blend-mode:screen">
 <div id="s7-cta" class="abs" style="left:190px;top:1080px;width:700px;height:110px;border-radius:55px;background:linear-gradient(180deg,#ffd451,#ffb800);display:flex;align-items:center;justify-content:center;gap:18px;color:#1b120d;font-size:36px;font-weight:800;letter-spacing:.08em">{bag.replace('110','74')}<span>TEKAN BEG KUNING</span></div>
 <div id="s7-cta2" class="abs row" style="top:1215px;font-size:28px;letter-spacing:.32em;color:#F3DDAE">STOK TERHAD · 500ML</div>
</div>
"""
s7js = f"""
tl.fromTo("#s7-beam",{{opacity:0}},{{opacity:1,duration:0.4}},0.0);
tl.fromTo("#s7-pod",{{y:200,opacity:0}},{{y:0,opacity:1,duration:0.6,ease:"expo.out"}},0.0);
tl.fromTo(["#s7-bb","#s7-nb"],{{y:-100,opacity:0,filter:"blur(12px) drop-shadow(0 30px 30px rgba(0,0,0,.6))"}},{{y:0,opacity:1,filter:"blur(0px) drop-shadow(0 30px 30px rgba(0,0,0,.6))",duration:0.55,ease:"power4.out",stagger:0.12}},0.15);
tl.fromTo("#s7-l1",{{opacity:0,y:-14,filter:"blur(8px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.7,ease:"expo.out"}},0.05);
tl.fromTo("#s7-l2",{{opacity:0,filter:"blur(8px)"}},{{opacity:1,filter:"blur(0px)",duration:0.2}},{L(29.02,S7)});
tl.fromTo(".s7-ch",{{opacity:0.0,y:30,filter:"blur(6px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.2,stagger:0.05,ease:"expo.out"}},{L(30.26,S7)});
tl.fromTo("#s7-l4",{{opacity:0,y:-14,filter:"blur(8px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.5,ease:"expo.out"}},{L(30.72,S7)});
tl.fromTo("#s7-end",{{opacity:0}},{{opacity:1,duration:0.4,ease:"power2.inOut"}},3.45);
tl.fromTo("#s7-logo",{{opacity:0,scale:1.25,filter:"blur(16px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:0.7,ease:"expo.out"}},3.55);
tl.fromTo("#s7-cta",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.5,ease:"back.out(2)"}},4.1);
tl.fromTo("#s7-cta2",{{opacity:0}},{{opacity:1,duration:0.5}},4.35);
"""
open(P + "/compositions/s7.html", "w").write(scene("s7", s7, s7js))

# ------------------------------------------------------------------ CAPTIONS
words = json.load(open(sys.argv[2]))
fix = {12: "Kadang-kadang", 36: "kehadirannya", 40: "Dia", 46: "perfume", 50: "perfume", 51: "Midnight", 52: "Fantasy", 75: "checkout", 85: "bidadari", 88: "tercinta", 29: "Foaming", 30: "Body", 31: "Wash", 28: "abang", 54: "abang,"}
W = []
for i, w_ in enumerate(words):
    t = fix.get(i, w_["text"]).strip(",.")
    W.append(dict(i=i, text=t, start=w_["start"] + VO, end=w_["end"] + VO))
# merge sangat + -sangat ; cek + ke
W[65]["text"] = "sangat-sangat"; W[65]["end"] = W[66]["end"]; W[66]["skip"] = True
W[75]["text"] = "checkout"; W[75]["end"] = W[76]["end"]; W[76]["skip"] = True
W[78]["text"] = "habis"
groups = [
 ([12,13,14],[]),([15,16,17],[]),([18,19,20],[]),([21,22,23,24],[23,24]),([25,26],[]),
 ([27,28],[27]),([29,30,31],[29,30,31]),([32,33,34],[]),([35,36],[35]),([37,38,39],[]),
 ([40,41,42,43],[42]),([44,45],[44]),([46,47],[47]),([48,49],[]),([50,51,52],[51,52]),
 ([53,54],[]),([55,56],[55]),([57,58,59],[]),([60,61,62],[62]),
 ([63,64,65],[]),([67,68],[67]),([69,70,71,72],[70,71]),([73,74,75],[75]),([77,78,79],[78,79]),
]
cap_body = ""; cap_js = ""
for gi, (idx, emph) in enumerate(groups):
    g0 = W[idx[0]]["start"] - 0.06; g1 = W[idx[-1]]["end"] + 0.02
    if gi + 1 < len(groups): g1 = min(g1 + 0.25, W[groups[gi+1][0][0]]["start"] - 0.06)
    spans = ""
    for k in idx:
        cls = "cw em" if k in emph else "cw"
        spans += f'<span id="cw{k}" class="{cls}">{W[k]["text"]}</span> '
    cap_body += f'<div id="cg{gi}" class="cg">{spans.strip()}</div>\n'
    cap_js += f'tl.set("#cg{gi}",{{visibility:"visible",opacity:1}},{g0:.2f});\n'
    cap_js += f'tl.fromTo("#cg{gi}",{{y:26,scale:0.94}},{{y:0,scale:1,duration:0.22,ease:"expo.out"}},{g0:.2f});\n'
    for k in idx:
        st = W[k]["start"]
        sc = 1.12 if k in emph else 1.0
        cap_js += f'tl.fromTo("#cw{k}",{{opacity:0.35,scale:{sc*0.9:.2f}}},{{opacity:1,scale:{sc},duration:0.14,ease:"back.out(3)"}},{max(st-0.03,g0):.2f});\n'
    cap_js += f'tl.to("#cg{gi}",{{opacity:0,duration:0.1,ease:"power2.in"}},{g1-0.1:.2f});\n'
    cap_js += f'tl.set("#cg{gi}",{{opacity:0,visibility:"hidden"}},{g1:.2f});\n'
cap_css = """
.cg{position:absolute;left:90px;width:900px;top:1120px;text-align:center;visibility:hidden;opacity:0;line-height:1.15;overflow:visible}
.cw{display:inline-block;font-family:'Jost';font-weight:700;font-size:66px;color:#FFF8EE;letter-spacing:.01em;text-shadow:0 4px 18px rgba(0,0,0,.85),0 0 2px rgba(0,0,0,.9);margin:0 9px}
.em{font-family:'Bodoni Moda';font-style:italic;font-weight:700;font-size:74px;color:#F3D493;text-shadow:0 4px 18px rgba(0,0,0,.9),0 0 26px rgba(217,185,126,.45);margin:0 14px}
"""
open(P + "/compositions/captions.html", "w").write(scene("captions", cap_body, cap_js, cap_css))

# ------------------------------------------------------------------ SFX + ROOT
peak = {"impact-bass-1":0.07,"impact-bass-2":0.79,"riser":3.47,"whoosh":0.16,"whoosh-lo":0.2,"whoosh-hi":0.14,"whoosh-cinematic":2.5,
        "pop":0.11,"pop-hi":0.09,"click":0.07,"click-soft":0.07,"sparkle":0.02,"ping":0.32,"chime":0.41,"notification":0.24}
sfx = [  # (name, film time of hit, volume)
 ("impact-bass-1", 0.17, 1.0), ("whoosh-hi", 0.15, 0.6),
 ("whoosh-lo", w(1.95), 0.55), ("sparkle", w(3.5), 0.8),
 ("whoosh", 4.15, 0.8), ("pop", w(4.52), 0.75), ("pop-hi", w(6.0), 0.75), ("chime", w(7.44), 0.7),
 ("riser", 10.25, 0.55), ("whoosh-cinematic", 9.2, 0.45), ("impact-bass-2", w(10.1), 0.95), ("click-soft", 9.75, 0.6),
 ("pop", w(10.88), 0.6), ("pop-hi", w(11.42), 0.6), ("pop", w(11.76), 0.6),
 ("whoosh", 12.3, 0.75), ("whoosh-hi", 14.55, 0.7),
 ("impact-bass-1", w(14.94), 0.7), ("whoosh-lo", w(16.7), 0.7), ("sparkle", w(16.86), 0.6),
 ("whoosh", w(18.3), 0.7), ("chime", w(18.6), 0.6),
 ("whoosh-hi", 19.85, 0.7), ("click", w(21.55), 0.7), ("whoosh-lo", w(22.6), 0.6), ("impact-bass-1", w(22.68), 0.8),
 ("whoosh", 23.1, 0.7), ("impact-bass-2", w(24.12), 0.9), ("ping", 23.3, 0.6),
 ("pop", w(24.5), 0.6), ("click", w(25.14), 1.0), ("notification", w(26.28), 0.75), ("pop-hi", w(27.16), 0.7),
 ("whoosh-lo", 28.0, 0.7), ("sparkle", w(30.26), 0.8), ("whoosh-cinematic", 31.6, 0.4), ("impact-bass-2", 31.6, 0.9), ("sparkle", 31.75, 0.7), ("pop", 32.2, 0.6),
]
audio = f"""
  <audio id="a-voice" class="clip" src="assets/audio/voice.wav" data-start="{VO}" data-duration="31.44" data-track-index="20" data-volume="1.15"></audio>
  <audio id="a-music" class="clip" src="assets/audio/music.wav" data-start="0" data-duration="{TOTAL}" data-track-index="21" data-volume="0.2" data-fade-out="1.8"></audio>
"""
import soundfile as _sf
lanes = []
for n, (name, t, vol) in enumerate(sorted(sfx, key=lambda x: x[1] - peak[x[0]])):
    st = round(max(0, t - peak[name]), 2)
    d = round(_sf.info(P + f"/assets/sfx/{name}.wav").duration, 2)
    d = round(min(d, TOTAL - st), 2)
    for li, end in enumerate(lanes):
        if end <= st: lanes[li] = st + d; break
    else: lanes.append(st + d); li = len(lanes) - 1
    audio += f'  <audio id="fx{n}" class="clip" src="assets/sfx/{name}.wav" data-start="{st}" data-duration="{d}" data-track-index="{22 + li}" data-volume="{vol}"></audio>\n'

hosts = [("mall", 0, TOTAL, 1), ("s1", 0, 4.25, 2), ("s2", 4.2, 4.95, 3), ("s3", 9.1, 5.7, 4), ("s4", 14.75, 5.2, 5),
         ("s5", 19.9, 3.45, 6), ("s6", 23.2, 4.88, 7), ("s7", 28.05, TOTAL - 28.05, 8)]
hh = ""
for cid, s, d, z in hosts:
    hh += f'  <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{s}" data-duration="{round(d,2)}" data-track-index="{z}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:{z}"></div>\n'
hh += f'  <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="10" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:30"></div>\n'
index = f"""<!doctype html>
<html lang="ms">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ margin:0; width:1080px; height:1920px; overflow:hidden; background:#0b0706; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920" data-fps="30">
{hh}{audio}</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
open(P + "/index.html", "w").write(index)
print("ok", len(groups), "caption groups", len(sfx), "sfx")
