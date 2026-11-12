# Generates index.html + compositions/*.html for the Frescura Body awareness ad (1080x1920, 30fps)
import json, os
OFF = 0.25          # voice starts 0.25 s into the film
TOTAL = 37.4
W, H = 1080, 1920
os.makedirs("compositions", exist_ok=True)

FONTS = """
@font-face{font-family:'Bodoni Moda';font-style:normal;font-weight:400 900;src:url('assets/fonts/BodoniModa-normal.woff2') format('woff2');}
@font-face{font-family:'Bodoni Moda';font-style:italic;font-weight:400 900;src:url('assets/fonts/BodoniModa-italic.woff2') format('woff2');}
@font-face{font-family:'Jost';font-style:normal;font-weight:300 800;src:url('assets/fonts/Jost-normal.woff2') format('woff2');}
"""
BASE = FONTS + """
#root{position:absolute;inset:0;overflow:hidden;font-family:'Jost',sans-serif;color:#f4eee6;}
.abs{position:absolute;}
.full{position:absolute;inset:0;}
.serif{font-family:'Bodoni Moda',serif;}
.it{font-family:'Bodoni Moda',serif;font-style:italic;}
.eyebrow{font-family:'Jost';font-weight:500;font-size:30px;letter-spacing:.42em;text-transform:uppercase;color:#d8b77a;}
.center{left:0;width:1080px;text-align:center;}
.gold{color:#d8b77a;}
.rule{height:2px;background:linear-gradient(90deg,transparent,#d8b77a,transparent);}
svg .ln{fill:none;stroke:#d8b77a;stroke-width:3.2;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1;}
"""
HELP = """
function rng(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;}}
function inBlur(tl,sel,t,d,extra){tl.fromTo(sel,Object.assign({opacity:0,filter:'blur(10px)'},extra&&extra.from||{}),Object.assign({opacity:1,filter:'blur(0px)',duration:d||0.35,ease:'expo.out'},extra&&extra.to||{}),t);}
function outBlur(tl,sel,t,d){tl.to(sel,{opacity:0,filter:'blur(8px)',duration:d||0.18,ease:'power2.in'},t);}
function slam(tl,sel,t,s){tl.fromTo(sel,{opacity:0,scale:s||1.35,filter:'blur(12px)'},{opacity:1,scale:1,filter:'blur(0px)',duration:0.42,ease:'expo.out'},t);}
function draw(tl,sel,t,d){tl.fromTo(sel,{strokeDashoffset:1},{strokeDashoffset:0,duration:d||0.5,ease:'power2.out'},t);}
function shake(tl,sel,t,amp,seed){var r=rng(seed||7);for(var i=0;i<8;i++){tl.to(sel,{x:(r()-.5)*amp*(1-i/8),y:(r()-.5)*amp*(1-i/8),duration:0.03,ease:'none'},t+i*0.03);}tl.to(sel,{x:0,y:0,duration:0.04},t+0.24);}
"""

def scene(sid, dur, css, html, js):
    doc = f"""<template>
<style>{BASE}{css}</style>
<div id="root" data-composition-id="{sid}" data-width="{W}" data-height="{H}" data-start="0" data-duration="{dur}">
{html}
</div>
<script>
(function(){{
{HELP}
const tl = gsap.timeline({{ paused: true }});
{js}
tl.set({{}}, {{}}, {dur - 0.01});
window.__timelines["{sid}"] = tl;
}})();
</script>
</template>
"""
    open(f"compositions/{sid}.html", "w").write(doc)

ICON = {
 'suami':'<circle class="ln" pathLength="1" cx="48" cy="30" r="14"/><path class="ln" pathLength="1" d="M18 84 C18 62 32 54 48 54 C64 54 78 62 78 84"/><path class="ln" pathLength="1" d="M48 56 L43 66 L48 80 L53 66 Z"/>',
 'anak':'<circle class="ln" pathLength="1" cx="48" cy="38" r="12"/><path class="ln" pathLength="1" d="M30 84 C30 68 38 60 48 60 C58 60 66 68 66 84"/><path class="ln" pathLength="1" d="M38 28 Q48 16 58 28"/>',
 'rumah':'<path class="ln" pathLength="1" d="M14 46 L48 18 L82 46"/><path class="ln" pathLength="1" d="M24 40 V82 H72 V40"/><path class="ln" pathLength="1" d="M41 82 V60 H55 V82"/>',
 'moon':'<path class="ln" pathLength="1" d="M58 18 A32 32 0 1 0 80 62 A26 26 0 1 1 58 18 Z"/>',
 'drop':'<path class="ln" pathLength="1" d="M48 12 C48 12 22 44 22 60 A26 26 0 0 0 74 60 C74 44 48 12 48 12 Z"/><path class="ln" pathLength="1" d="M36 62 A12 12 0 0 0 48 74"/>',
 'spark':'<path class="ln" pathLength="1" d="M48 10 L54 42 L86 48 L54 54 L48 86 L42 54 L10 48 L42 42 Z"/>',
 'check':'<path class="ln" pathLength="1" d="M28 50 L43 65 L70 34"/>',
}
def icon(name, cls="", size=96):
    return f'<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 96 96">{ICON[name]}</svg>'

# ---------------------------------------------------------------- S1 HOOK 0 - 7.0
rows = [('suami','Suami',0.25),('anak','Anak',1.77),('rumah','Rumah',2.83)]
s1_rows = "".join(f'''
<div id="s1-row{i}" class="abs s1-row" style="top:{640+i*150}px">
  <div class="s1-ic">{icon(k,'s1-svg'+str(i),78)}</div>
  <div class="s1-lab">{lab}</div>
  <div class="s1-ok"><span class="it">dapat</span> perhatian <svg width="44" height="44" viewBox="0 0 96 96">{ICON['check'].replace('class="ln"','class="ln s1-ck'+str(i)+'"')}</svg></div>
</div>''' for i,(k,lab,_) in enumerate(rows))
scene("s1", 7.0, """
#s1-bg{background:radial-gradient(900px 900px at 50% 38%,#2a1f17 0%,#120e0b 55%,#0b0908 100%);}
#s1-k{top:250px;}
#s1-t1{top:300px;font-size:84px;font-weight:500;}
#s1-t2{top:385px;font-size:150px;font-weight:800;letter-spacing:-.02em;line-height:1;}
.s1-row{left:110px;width:860px;height:124px;border:1.5px solid rgba(216,183,122,.35);border-radius:62px;background:linear-gradient(90deg,rgba(244,238,230,.07),rgba(244,238,230,.02));display:flex;align-items:center;padding:0 34px 0 22px;box-sizing:border-box;}
.s1-ic{width:84px;height:84px;border-radius:50%;background:rgba(216,183,122,.08);display:flex;align-items:center;justify-content:center;}
.s1-lab{margin-left:28px;font-size:50px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;}
.s1-ok{margin-left:auto;font-size:34px;color:#d8b77a;display:flex;align-items:center;gap:10px;font-weight:500;}
.s1-ok .it{font-size:36px;color:#f4eee6;opacity:.75}
#s1-me{top:440px;}
#s1-ring{left:390px;top:560px;width:300px;height:300px;}
#s1-q{left:390px;top:560px;width:300px;height:300px;font-size:190px;line-height:300px;text-align:center;color:#f4eee6;}
#s1-a1{top:880px;font-size:118px;font-weight:500;line-height:1;}
#s1-a2{top:1000px;font-size:104px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;line-height:1;}
""", f"""
<div id="s1-bg" class="full"></div>
<div id="s1-wrap" class="full">
  <div id="s1-k" class="abs center eyebrow">Realiti setiap wanita</div>
  <div id="s1-t1" class="abs center it">Semua dapat</div>
  <div id="s1-t2" class="abs center serif">perhatian.</div>
  {s1_rows}
  <div id="s1-me" class="abs center eyebrow" style="font-size:34px;color:#f4eee6;letter-spacing:.5em">Diri sendiri</div>
  <svg id="s1-ring" class="abs" viewBox="0 0 300 300"><circle cx="150" cy="150" r="140" fill="none" stroke="#d8b77a" stroke-width="3" stroke-dasharray="10 14"/></svg>
  <div id="s1-q" class="abs it">?</div>
  <div id="s1-a1" class="abs center it">Siapa</div>
  <div id="s1-a2" class="abs center gold">nak jaga?</div>
</div>
""", f"""
tl.fromTo('#s1-k',{{opacity:0,scaleX:1.3}},{{opacity:1,scaleX:1,duration:.9,ease:'expo.out'}},0);
tl.fromTo('#s1-t2',{{scale:1.08}},{{scale:1,duration:1.2,ease:'expo.out'}},0);
{''.join(f"tl.fromTo('#s1-row{i}',{{opacity:0,x:-60,clipPath:'inset(0 100% 0 0 round 62px)'}},{{opacity:1,x:0,clipPath:'inset(0 0% 0 0 round 62px)',duration:.55,ease:'expo.out'}},{t-0.05});draw(tl,'.s1-svg{i} .ln',{t},.6);draw(tl,'.s1-ck{i}',{t+0.45},.35);" for i,(_,_,t) in enumerate(rows))}
// collapse family rows, focus on self
tl.to('.s1-row',{{opacity:0,y:-40,filter:'blur(8px)',duration:.3,stagger:.05,ease:'power3.in'}},4.25);
outBlur(tl,'#s1-t1',4.25);outBlur(tl,'#s1-t2',4.28);outBlur(tl,'#s1-k',4.3);
tl.set(['#s1-me','#s1-ring','#s1-q','#s1-a1','#s1-a2'],{{opacity:0}},0);
inBlur(tl,'#s1-me',4.5,.4,{{from:{{scaleX:1.4}},to:{{scaleX:1}}}});
tl.fromTo('#s1-ring',{{opacity:0,scale:.6,rotation:-40}},{{opacity:1,scale:1,rotation:0,duration:.7,ease:'expo.out',immediateRender:false}},4.55);
tl.to('#s1-ring',{{rotation:40,duration:2.2,ease:'none'}},5.25);
slam(tl,'#s1-q',5.05,1.6);
slam(tl,'#s1-a1',5.71,1.3);
slam(tl,'#s1-a2',6.08,1.45);
shake(tl,'#s1-wrap',6.1,22,3);
// ring opens into the next world (S2 donut)
tl.to('#s1-ring',{{scale:3.2,opacity:0,duration:.35,ease:'power3.in'}},6.62);
tl.to(['#s1-q','#s1-me','#s1-a1','#s1-a2'],{{opacity:0,filter:'blur(10px)',duration:.25,ease:'power2.in'}},6.66);
""")

# ---------------------------------------------------------------- S2 24-HOUR DONUT 7.0 - 11.55
R0 = 250; C = 2*3.14159265*R0
segs = [("Keluarga",.40,"#d8b77a",1.69),("Rumah & kerja",.32,"#a8916b",2.19),("Tidur",.26,"#5d5246",2.6),("Diri sendiri",.02,"#e0566e",3.9)]
acc = 0; seg_svg = ""; seg_js = ""
for i,(n,p,c,t) in enumerate(segs):
    L = p*C - (6 if p>.05 else 0)
    seg_svg += f'<circle id="s2-seg{i}" cx="300" cy="300" r="{R0}" fill="none" stroke="{c}" stroke-width="{50 if i<3 else 64}" stroke-dasharray="0 {C}" transform="rotate({-90+acc*360} 300 300)" stroke-linecap="butt"/>'
    seg_js += f"tl.fromTo('#s2-seg{i}',{{attr:{{'stroke-dasharray':'0 {C:.1f}'}}}},{{attr:{{'stroke-dasharray':'{L:.1f} {C:.1f}'}},duration:{.55 if i<3 else .25},ease:'power3.out'}},{t});"
    acc += p
legend = "".join(f'<div class="s2-lg" id="s2-lg{i}"><i style="background:{c}"></i>{n} <b>{int(p*100)}%</b></div>' for i,(n,p,c,_) in enumerate(segs))
scene("s2", 4.55, """
#s2-bg{background:radial-gradient(800px 800px at 50% 42%,#1f1712,#0b0908 70%);}
#s2-k{top:240px;}
#s2-t{top:290px;font-size:120px;font-weight:500;line-height:1;}
#s2-t b{font-family:'Bodoni Moda';font-weight:800;font-style:normal;color:#d8b77a;font-size:150px;}
#s2-donut{left:240px;top:440px;width:600px;height:600px;}
#s2-c1{top:655px;font-size:28px;letter-spacing:.18em;text-transform:uppercase;color:#f4eee6;opacity:.8}
#s2-c2{top:690px;font-size:150px;font-weight:700;line-height:1;color:#e0566e;}
#s2-busy{top:695px;font-size:96px;font-weight:800;letter-spacing:.12em;}
#s2-legend{left:90px;top:1060px;width:900px;width:860px;display:flex;flex-wrap:wrap;gap:12px 34px;justify-content:center;font-size:30px;}
.s2-lg{display:flex;align-items:center;gap:12px;opacity:.9}.s2-lg i{width:18px;height:18px;border-radius:50%;display:inline-block}.s2-lg b{color:#d8b77a;font-weight:600}
#s2-note{top:1160px;font-size:20px;letter-spacing:.3em;opacity:.45;text-transform:uppercase}
""", f"""
<div id="s2-bg" class="full"></div>
<div id="s2-wrap" class="full">
<div id="s2-k" class="abs center eyebrow">Fakta harian · ilustrasi</div>
<div id="s2-t" class="abs center it"><b id="s2-num">24</b> jam sehari</div>
<svg id="s2-donut" class="abs" viewBox="0 0 600 600"><circle cx="300" cy="300" r="{R0}" fill="none" stroke="rgba(244,238,230,.07)" stroke-width="50"/>{seg_svg}</svg>
<div id="s2-busy" class="abs center serif">SIBUK.</div>
<div id="s2-c1" class="abs center">Masa untuk diri</div>
<div id="s2-c2" class="abs center serif">≈ 0</div>
<div id="s2-legend" class="abs">{legend}</div>

</div>
""", f"""
var cnt={{v:0}};var num=document.getElementById('s2-num');
tl.fromTo(cnt,{{v:0}},{{v:24,duration:.9,ease:'power2.out',onUpdate:function(){{num.textContent=Math.round(cnt.v)}}}},0.05);
inBlur(tl,'#s2-k',0,.4);inBlur(tl,'#s2-t',0.02,.45);
tl.fromTo('#s2-donut',{{opacity:0,scale:1.6,rotation:-30}},{{opacity:1,scale:1,rotation:0,duration:.8,ease:'expo.out'}},0);
{seg_js}
slam(tl,'#s2-busy',1.29,1.4);
outBlur(tl,'#s2-busy',3.05,.16);
inBlur(tl,'#s2-c1',3.15,.35);
slam(tl,'#s2-c2',4.0,1.6);
tl.fromTo('#s2-seg3',{{filter:'drop-shadow(0 0 0px #e0566e)'}},{{filter:'drop-shadow(0 0 22px #e0566e)',duration:.4,ease:'power2.out'}},3.95);
tl.fromTo('.s2-lg',{{opacity:0,y:16}},{{opacity:.9,y:0,duration:.35,stagger:.4,ease:'expo.out'}},1.75);

tl.to('#s2-wrap',{{x:-260,opacity:0,filter:'blur(14px)',duration:.25,ease:'power3.in'}},4.3);
""")

# ---------------------------------------------------------------- S3 NEEDS 11.55 - 15.85
cards = [('moon','Rehat','01',1.80),('drop','Kebersihan','02',2.52),('spark','Penampilan','03',3.42)]
s3c = "".join(f'''<div id="s3-c{i}" class="abs s3-card" style="top:{650+i*155}px"><span class="it s3-n">{n}</span><span class="s3-l">{l}</span><span class="s3-i">{icon(ic,'s3-svg'+str(i),70)}</span></div>''' for i,(ic,l,n,_) in enumerate(cards))
scene("s3", 4.3, """
#s3-vw{position:absolute;inset:0;}
#s3-v{position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover;}
#s3-sh{background:linear-gradient(180deg,rgba(11,9,8,.92) 0%,rgba(11,9,8,.62) 40%,rgba(11,9,8,.55) 70%,rgba(11,9,8,.9) 100%);}
#s3-k{top:240px;}
#s3-t1{top:290px;font-size:86px;font-weight:500;}
#s3-t2{top:405px;font-size:178px;font-weight:800;letter-spacing:.08em;line-height:1;}
.s3-card{left:110px;width:860px;height:128px;border-radius:24px;background:rgba(20,16,13,.55);border:1.5px solid rgba(216,183,122,.45);backdrop-filter:blur(18px);display:flex;align-items:center;padding:0 36px;box-sizing:border-box;}
.s3-n{font-size:58px;color:#d8b77a;width:110px}
.s3-l{font-size:54px;font-weight:600;letter-spacing:.06em}
.s3-i{margin-left:auto;display:flex}
""", f"""
<div id="s3-vw"><video id="s3-v" class="clip" src="assets/vid/lather.mp4" data-start="0" data-duration="4.3" muted playsinline></video></div>
<div id="s3-sh" class="full"></div>
<div id="s3-k" class="abs center eyebrow">Padahal</div>
<div id="s3-t1" class="abs center it">kita pun perlukan</div>
<div id="s3-t2" class="abs center serif gold">MASA</div>
{s3c}
""", f"""
tl.fromTo('#s3-vw',{{scale:1.18}},{{scale:1.02,duration:4.3,ease:'power1.out'}},0);
tl.fromTo('#s3-vw',{{x:260,filter:'blur(14px)'}},{{x:0,filter:'blur(0px)',duration:.4,ease:'expo.out'}},0);
inBlur(tl,'#s3-k',0.04,.35);
tl.fromTo('#s3-t1 ',{{opacity:0,y:0,filter:'blur(8px)'}},{{opacity:1,filter:'blur(0px)',duration:.3,ease:'expo.out'}},0.45);
tl.fromTo('#s3-t2',{{opacity:0,scaleX:1.6,filter:'blur(10px)'}},{{opacity:1,scaleX:1,filter:'blur(0px)',duration:.6,ease:'expo.out'}},1.1);
{''.join(f"tl.fromTo('#s3-c{i}',{{opacity:0,y:60,rotationX:-50,transformPerspective:900}},{{opacity:1,y:0,rotationX:0,duration:.5,ease:'expo.out'}},{t-0.08});draw(tl,'.s3-svg{i} .ln',{t},.6);" for i,(_,_,_,t) in enumerate(cards))}
tl.to('.s3-card',{{opacity:0,y:-50,filter:'blur(8px)',duration:.2,stagger:.04,ease:'power3.in'}},4.02);
tl.to(['#s3-t1','#s3-t2','#s3-k'],{{opacity:0,filter:'blur(8px)',duration:.2,ease:'power2.in'}},4.05);
""")

# ---------------------------------------------------------------- S4 PRIORITY LIST 15.85 - 19.28
items = ["Suami","Anak-anak","Rumah","Kerja","Diri sendiri"]
s4rows = "".join(f'<div id="s4-r{i}" class="abs s4-row"><span class="s4-no it" id="s4-no{i}">{i+1}</span><span class="s4-tx">{t}</span><span class="s4-fill" id="s4-f{i}"></span></div>' for i,t in enumerate(items))
scene("s4", 3.43, """
#s4-bg{background:linear-gradient(180deg,#0b0908,#17110d 60%,#0b0908);}
#s4-k{top:240px;}
#s4-t{top:290px;font-size:82px;font-weight:500;line-height:1.08}
.s4-row{left:150px;width:780px;height:92px;top:560px;border-bottom:1.5px solid rgba(244,238,230,.14);display:flex;align-items:center;font-size:52px;font-weight:500;box-sizing:border-box;padding-left:10px;overflow:hidden}
.s4-no{width:96px;font-size:56px;color:#d8b77a}
.s4-tx{position:relative;z-index:2}
.s4-fill{position:absolute;left:0;top:10px;bottom:10px;width:6px;background:#d8b77a;border-radius:3px}
#s4-strike{left:240px;top:0;width:420px;height:4px;background:#e0566e;transform-origin:left center}
#s4-stamp{top:1072px;font-size:58px;font-weight:800;letter-spacing:.3em;text-transform:uppercase;color:#d8b77a}
""", f"""
<div id="s4-bg" class="full"></div>
<div id="s4-k" class="abs center eyebrow">Peringatan</div>
<div id="s4-t" class="abs center it">Senarai keutamaan<br/>kamu hari ini</div>
{s4rows}
<div id="s4-strike" class="abs"></div>
<div id="s4-stamp" class="abs center">Jangan lupa.</div>
""", f"""
var Y=[0,100,200,300,400];
for(var i=0;i<5;i++){{tl.fromTo('#s4-r'+i,{{y:Y[i]+40,opacity:0}},{{y:Y[i],opacity:1,duration:.4,ease:'expo.out'}},0.1+i*0.07);}}
inBlur(tl,'#s4-k',0,.35);inBlur(tl,'#s4-t',0.05,.4);
// "dahulukan semua orang": highlight rows 1-4
for(var i=0;i<4;i++){{tl.fromTo('#s4-f'+i,{{width:6,opacity:.9}},{{width:780,opacity:.14,duration:.35,ease:'power3.out'}},0.88+i*0.12);}}
// "lupa diri sendiri": row 5 fades + strike
tl.to('#s4-r4',{{opacity:.28,duration:.3}},2.0);
tl.fromTo('#s4-strike',{{y:560+400+44,scaleX:0}},{{y:560+400+44,scaleX:1,duration:.3,ease:'power3.out'}},2.22);
// row 5 jumps to #1
tl.to('#s4-strike',{{opacity:0,duration:.12}},2.62);
tl.to('#s4-r4',{{y:-6,opacity:1,scale:1.06,duration:.45,ease:'expo.out'}},2.66);
for(var i=0;i<4;i++){{tl.to('#s4-r'+i,{{y:Y[i+1]+8,opacity:.45,duration:.45,ease:'expo.out'}},2.66);}}
tl.to('#s4-f4',{{width:780,opacity:.22,duration:.4,ease:'power3.out'}},2.7);
tl.set('#s4-no4',{{textContent:'1'}},2.7);
for(var i=0;i<4;i++){{tl.set('#s4-no'+i,{{textContent:String(i+2)}},2.7);}}
slam(tl,'#s4-stamp',2.9,1.4);
tl.to('#root',{{opacity:1}},0);
""")

# ---------------------------------------------------------------- S5 LUXURY MALL BOUTIQUE 19.28 - 24.6
r = __import__('random').Random(5)
bokeh = "".join(f'<div class="s5-bk" style="left:{r.randint(-60,1080)}px;top:{r.randint(80,1500)}px;width:{(s:=r.randint(30,120))}px;height:{s}px;opacity:{r.uniform(.15,.5):.2f};background:radial-gradient(circle,{r.choice(["#ffd9a0","#fff1d8","#f7c58a","#e8d1ff"])} 0%,transparent 70%)"></div>' for _ in range(26))
mull = "".join(f'<div class="s5-m" style="left:{x}%"></div>' for x in range(0,101,12))
scene("s5", 5.32, """
#s5-bg{background:linear-gradient(180deg,#0a0807 0%,#1a130e 34%,#2a1f16 40%,#120d0a 60%,#080706 100%);}
#s5-cam{position:absolute;inset:0;transform-origin:50% 40%;}
#s5-atr{left:240px;top:430px;width:600px;height:420px;background:radial-gradient(closest-side,rgba(255,232,190,.85),rgba(255,214,160,.25) 45%,transparent 75%);filter:blur(6px)}
.s5-plane{position:absolute;left:-600px;width:2280px;}
#s5-ceil{top:-1200px;height:1840px;transform-origin:50% 100%;transform:perspective(700px) rotateX(-72deg);
 background:repeating-linear-gradient(90deg,transparent 0 120px,rgba(255,236,200,.9) 120px 126px,transparent 126px 252px),
 repeating-linear-gradient(0deg,#120d09 0 160px,#1b140e 160px 164px);}
#s5-floor{top:640px;height:1840px;transform-origin:50% 0%;transform:perspective(700px) rotateX(72deg);
 background:radial-gradient(500px 900px at 50% 0%,rgba(255,226,180,.55),transparent 70%),
 repeating-linear-gradient(90deg,rgba(255,255,255,.03) 0 2px,transparent 2px 230px),
 repeating-linear-gradient(0deg,rgba(255,255,255,.035) 0 2px,transparent 2px 230px),
 linear-gradient(180deg,#3a2c20,#1a130e 40%,#0c0907);}
.s5-wall{position:absolute;top:120px;width:1200px;height:1100px;
 background:linear-gradient(180deg,rgba(255,220,170,.0),rgba(255,214,160,.22) 30%,rgba(255,214,160,.12) 70%,transparent),#140f0b;overflow:hidden}
#s5-wl{left:-1170px;transform-origin:100% 50%;transform:perspective(800px) rotateY(74deg);}
#s5-wr{left:1050px;transform-origin:0% 50%;transform:perspective(800px) rotateY(-74deg);}
.s5-m{position:absolute;top:0;bottom:0;width:6px;background:linear-gradient(180deg,#8a6a3c,#e4c68a,#8a6a3c);}
#s5-sign{left:200px;top:40px;width:680px;height:680px;mix-blend-mode:screen;}
#s5-sign img{width:100%;height:100%;}
#s5-beam{left:140px;top:300px;width:800px;height:1000px;background:linear-gradient(180deg,rgba(255,240,210,.0),rgba(255,240,210,.28) 50%,rgba(255,240,210,.0));clip-path:polygon(42% 0,58% 0,100% 100%,0 100%);mix-blend-mode:screen;filter:blur(8px)}
#s5-pl{left:180px;top:1110px;width:720px;height:330px;}
#s5-pl .top{position:absolute;left:0;top:0;width:720px;height:110px;border-radius:50%;background:radial-gradient(closest-side,#3c3026,#1d1612);box-shadow:0 0 0 3px #c9a86a inset,0 0 60px rgba(216,183,122,.35)}
#s5-pl .body{position:absolute;left:0;top:55px;width:720px;height:270px;background:linear-gradient(90deg,#0d0a08,#2a2018 35%,#3a2d22 50%,#2a2018 65%,#0d0a08);border-radius:0 0 50% 50%/0 0 60px 60px}
.s5-bt{position:absolute;bottom:810px;height:600px;filter:drop-shadow(0 30px 30px rgba(0,0,0,.55));}
#s5-g{left:330px}#s5-n{left:560px}
.s5-ref{position:absolute;top:1170px;height:600px;transform:scaleY(-1);opacity:.16;-webkit-mask-image:linear-gradient(0deg,rgba(0,0,0,.9),transparent 45%);mask-image:linear-gradient(0deg,rgba(0,0,0,.9),transparent 45%)}
.s5-bk{position:absolute;border-radius:50%;filter:blur(2px)}
#s5-pre{top:860px;font-size:76px;font-weight:500;}
.s5-lab{position:absolute;top:700px;width:270px;}
.s5-lab .nm{font-family:'Bodoni Moda';font-style:italic;font-size:50px;line-height:1.05}
.s5-lab .sub{font-size:28px;letter-spacing:.36em;text-transform:uppercase;color:#d8b77a;margin-top:12px}
#s5-lg{left:36px;text-align:right}#s5-ln{left:784px}
.s5-lk{position:absolute;top:760px;height:2px;background:#d8b77a}
#s5-lkg{left:240px;width:70px}#s5-lkn{left:770px;width:70px}
#s5-feat{top:540px;font-size:30px;letter-spacing:.42em;text-transform:uppercase;color:#d8b77a}
""", f"""
<div id="s5-bg" class="full"></div>
<div id="s5-cam">
  <div id="s5-ceil" class="s5-plane"></div>
  <div id="s5-floor" class="s5-plane"></div>
  <div id="s5-wl" class="s5-wall">{mull}</div>
  <div id="s5-wr" class="s5-wall">{mull}</div>
  <div id="s5-atr" class="abs"></div>
  <div id="s5-bks" class="full">{bokeh}</div>
  <div id="s5-sign" class="abs"><img src="assets/img/logo.jpg"/></div>
  <div id="s5-beam" class="abs"></div>
  <div id="s5-pl" class="abs"><div class="top"></div><div class="body"></div></div>
  <img id="s5-gr" class="s5-ref" src="assets/img/bt_glory.png" style="left:330px"/>
  <img id="s5-nr" class="s5-ref" src="assets/img/bt_noche.png" style="left:560px"/>
  <img id="s5-g" class="s5-bt" src="assets/img/bt_glory.png"/>
  <img id="s5-n" class="s5-bt" src="assets/img/bt_noche.png"/>
</div>
<div id="s5-pre" class="abs center it">Pastinya,</div>

<div id="s5-lg" class="s5-lab"><div class="nm">Bombshell</div><div class="sub">Woman Glory</div></div>
<div id="s5-ln" class="s5-lab"><div class="nm">Midnight<br/>Fantasy</div><div class="sub">Noche</div></div>

""", """
tl.fromTo('#s5-cam',{scale:1.45,y:220,filter:'blur(16px)'},{scale:1.0,y:0,filter:'blur(0px)',duration:1.3,ease:'expo.out'},0);
tl.to('#s5-cam',{scale:1.06,y:-30,duration:3.75,ease:'power1.inOut'},1.3);
tl.fromTo('#s5-ceil',{backgroundPosition:'0px 0px, 0px 0px'},{backgroundPosition:'0px 0px, 0px 820px',duration:5.32,ease:'power2.out'},0);
tl.fromTo('#s5-floor',{backgroundPosition:'0px 0px, 0px 0px, 0px -900px, 0px 0px'},{backgroundPosition:'0px 0px, 0px 0px, 0px 0px, 0px 0px',duration:5.32,ease:'power2.out'},0);
tl.fromTo('#s5-bks',{x:0},{x:-60,duration:5.32,ease:'none'},0);
// neon sign flicker on (Frescura)
tl.fromTo('#s5-sign',{opacity:0,scale:.92},{opacity:0,scale:.92,duration:.01},0);
[0,.06,.12,.2,.28].forEach(function(d,i){tl.to('#s5-sign',{opacity:i%2?0.25:1,scale:1,duration:.03,ease:'none'},0.58+d);});
tl.to('#s5-sign',{opacity:1,duration:.05},0.9);
tl.fromTo('#s5-beam',{opacity:0},{opacity:1,duration:.5,ease:'power2.out'},0.05);
tl.fromTo(['#s5-g','#s5-n'],{y:160,opacity:0,filter:'blur(10px)'},{y:0,opacity:1,filter:'blur(0px)',duration:.9,stagger:.12,ease:'expo.out'},0.05);
tl.fromTo(['#s5-gr','#s5-nr'],{y:-160,opacity:0},{y:0,opacity:.16,duration:.9,stagger:.12,ease:'expo.out'},0.05);
tl.fromTo('#s5-pre',{opacity:0,filter:'blur(10px)'},{opacity:1,filter:'blur(0px)',duration:.3,ease:'expo.out'},0.03);
tl.to('#s5-pre',{opacity:0,filter:'blur(8px)',duration:.2},0.85);
// fragrance labels (after the pump overlay, 3.47+)

tl.fromTo('#s5-lg',{opacity:0,x:-40,filter:'blur(8px)'},{opacity:1,x:0,filter:'blur(0px)',duration:.45,ease:'expo.out'},3.6);
tl.fromTo('#s5-ln',{opacity:0,x:40,filter:'blur(8px)'},{opacity:1,x:0,filter:'blur(0px)',duration:.45,ease:'expo.out'},3.75);

tl.to('#s5-cam',{opacity:0,filter:'blur(14px)',scale:1.25,duration:.22,ease:'power3.in'},5.08);
tl.to('.s5-lab',{opacity:0,duration:.18},5.08);
""")

# ---------------------------------------------------------------- S5b PUMP ARCH overlay 21.15 - 23.3
rb = __import__('random').Random(9)
bubbles = "".join(f'<div class="s6-b" id="s6-b{i}" style="left:{rb.randint(200,880)}px;top:{rb.randint(820,1080)}px;width:{(s:=rb.randint(14,46))}px;height:{s}px"></div>' for i in range(16))
scene("pump", 2.15, """
#pp-dim{background:rgba(8,7,6,.86)}
#pp-arch{left:100px;top:230px;width:880px;height:920px;overflow:hidden;border-radius:440px 440px 28px 28px;}
#pp-v{position:absolute;left:-100px;top:-230px;width:1080px;height:1920px;object-fit:cover;}
#pp-rim{left:100px;top:230px;width:880px;height:920px;border-radius:440px 440px 28px 28px;box-shadow:0 0 0 2px #d8b77a inset;}
#pp-tag{left:150px;top:560px;padding:16px 26px;background:rgba(11,9,8,.72);border:1.5px solid #d8b77a;border-radius:40px;font-size:28px;letter-spacing:.3em;text-transform:uppercase;color:#d8b77a}
#pp-h{top:1000px;font-size:96px;font-weight:600;text-shadow:0 6px 30px rgba(0,0,0,.6)}
.s6-b{position:absolute;border-radius:50%;background:radial-gradient(circle at 32% 30%,rgba(255,255,255,.95),rgba(255,255,255,.25) 35%,rgba(255,220,230,.08) 70%);box-shadow:0 0 0 1.5px rgba(255,255,255,.55) inset}
""", f"""
<div id="pp-dim" class="full"></div>
<div id="pp-arch" class="abs"><video id="pp-v" class="clip" src="assets/vid/pump_close.mp4" data-start="0" data-duration="2.15" muted playsinline></video></div>
<div id="pp-rim" class="abs"></div>
<div id="pp-tag" class="abs">1 pam · terus jadi buih</div>
<div id="pp-h" class="abs center it">buih lembut.</div>
<div id="pp-bub" class="full">{bubbles}</div>
""", """
tl.fromTo('#pp-dim',{opacity:0},{opacity:1,duration:.3,ease:'power2.out'},0);
tl.fromTo(['#pp-arch','#pp-rim'],{clipPath:'inset(48% 34% 6% 34% round 200px)',opacity:0},{clipPath:'inset(0% 0% 0% 0% round 0px)',opacity:1,duration:.55,ease:'expo.out'},0);
tl.fromTo('#pp-v',{scale:1.2},{scale:1.0,duration:2.15,ease:'power1.out'},0);
tl.fromTo('#pp-tag',{opacity:0,x:-30},{opacity:1,x:0,duration:.4,ease:'expo.out'},0.42);
tl.fromTo('#pp-h',{opacity:0,filter:'blur(10px)',scale:1.15},{opacity:1,filter:'blur(0px)',scale:1,duration:.4,ease:'expo.out'},0.3);
var r=rng(21);for(var i=0;i<16;i++){var t=0.25+r()*0.9,d=0.6+r()*.3;tl.fromTo('#s6-b'+i,{opacity:0,y:40,scale:.4},{opacity:1,y:-160-r()*260,scale:1,duration:d,ease:'power2.out'},t);tl.to('#s6-b'+i,{opacity:0,scale:1.3,duration:.12},t+d);}
tl.to(['#pp-arch','#pp-rim'],{clipPath:'inset(48% 34% 6% 34% round 200px)',opacity:0,duration:.3,ease:'power3.in'},1.82);
tl.to(['#pp-dim','#pp-tag','#pp-h'],{opacity:0,duration:.25,ease:'power2.in'},1.85);
""")

# ---------------------------------------------------------------- S6 GIRLS (light editorial) 24.6 - 27.9
scene("s6", 3.3, """
#s6-bg{background:radial-gradient(900px 1100px at 50% 40%,#f6f0e8,#e8ddcf 70%,#d9ccbb);}
#s6-hd{top:230px;font-size:210px;font-weight:600;color:#6e0f1d;line-height:1}
.s6-card{position:absolute;overflow:hidden;border-radius:18px;box-shadow:0 30px 60px rgba(60,40,20,.28);background:#ddd}
.s6-card img,.s6-card video{position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover}
#s6-a{left:70px;top:500px;width:440px;height:640px}
#s6-b{left:560px;top:470px;width:440px;height:660px}
#s6-pill{position:absolute;left:0;width:1080px;top:1020px;text-align:center}
#s6-pill span{display:inline-block;padding:20px 40px;background:#0d0b0a;color:#f4eee6;border-radius:60px;font-size:38px;font-weight:500;letter-spacing:.06em}
#s6-pill b{font-family:'Bodoni Moda';font-style:italic;color:#d8b77a;font-weight:600}
""", """
<div id="s6-bg" class="full"></div>
<div id="s6-hd" class="abs center it">Girls,</div>
<div id="s6-a" class="s6-card"><img src="assets/img/linen_diag.jpg" style="object-position:50% 40%"/></div>
<div id="s6-b" class="s6-card"><video id="s6-v" class="clip" src="assets/vid/foam_palm.mp4" data-start="0" data-duration="3.3" muted playsinline></video></div>
<div id="s6-pill"><span>Self-care itu <b>bukan</b> membazir.</span></div>
""", """
tl.fromTo('#s6-bg',{clipPath:'circle(0% at 50% 50%)'},{clipPath:'circle(80% at 50% 50%)',duration:.4,ease:'power3.out'},0);
tl.fromTo('#s6-hd',{opacity:0,scale:1.5,filter:'blur(14px)'},{opacity:1,scale:1,filter:'blur(0px)',duration:.45,ease:'expo.out'},0.05);
tl.fromTo('#s6-a',{opacity:0,y:120,rotation:-10},{opacity:1,y:0,rotation:-4,duration:.6,ease:'expo.out'},0.66);
tl.fromTo('#s6-b',{opacity:0,y:140,rotation:10},{opacity:1,y:0,rotation:4,duration:.6,ease:'expo.out'},1.18);
tl.to('#s6-a',{y:-30,duration:1.75,ease:'power1.inOut'},1.26);
tl.to('#s6-b',{y:-50,duration:1.25,ease:'power1.inOut'},1.78);
tl.fromTo('#s6-pill span',{opacity:0,scale:.8,rotation:-3},{opacity:1,scale:1,rotation:-2,duration:.45,ease:'back.out(1.4)'},1.55);
tl.to(['#s6-a','#s6-b','#s6-hd','#s6-pill'],{opacity:0,yPercent:-8,filter:'blur(8px)',duration:.22,ease:'power3.in'},3.06);
""")

# ---------------------------------------------------------------- S7 CTA 27.9 - 30.95
scene("s7", 3.05, """
#s7-bg{background:radial-gradient(800px 800px at 50% 35%,#2a2010,#0b0908 70%);}
#s7-t1{top:230px;font-size:92px;font-weight:500}
#s7-t2{top:330px;font-size:120px;font-weight:800;letter-spacing:.08em;color:#f2c94c;line-height:1}
#s7-btn{left:400px;top:520px;width:280px;height:280px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#ffe28a,#f2c94c 45%,#c99a1e);box-shadow:0 30px 80px rgba(242,201,76,.35);display:flex;align-items:center;justify-content:center}
#s7-btn svg path{fill:none;stroke:#0d0b0a;stroke-width:5;stroke-linecap:round;stroke-linejoin:round}
#s7-rip{left:400px;top:520px;width:280px;height:280px;border-radius:50%;border:3px solid #f2c94c}
#s7-tip{left:600px;top:760px;width:70px;height:70px;border-radius:50%;background:rgba(244,238,230,.92);box-shadow:0 10px 30px rgba(0,0,0,.5)}
#s7-card{left:110px;top:850px;width:860px;height:190px;border-radius:28px;background:rgba(244,238,230,.06);border:1.5px solid rgba(216,183,122,.4);display:flex;align-items:center;padding:0 28px;box-sizing:border-box;gap:22px}
#s7-card .th{display:flex;gap:4px;height:150px}#s7-card .th img{height:150px}
#s7-card .tx{flex:1}#s7-card .tx .a{font-family:'Bodoni Moda';font-style:italic;font-size:42px}#s7-card .tx .b{font-size:28px;letter-spacing:.3em;color:#d8b77a;text-transform:uppercase;margin-top:6px}
#s7-co{position:relative;padding:20px 30px;border-radius:40px;background:#f2c94c;color:#0d0b0a;font-weight:700;font-size:30px;letter-spacing:.08em;text-transform:uppercase;white-space:nowrap}
#s7-ok{position:absolute;inset:0;border-radius:40px;background:#2e7d4f;color:#fff;display:flex;align-items:center;justify-content:center;opacity:0}
#s7-stk{left:150px;top:1075px;width:780px}
#s7-stk .lb{display:flex;justify-content:space-between;font-size:30px;letter-spacing:.32em;text-transform:uppercase}
#s7-stk .lb b{color:#e0566e}
#s7-stk .bar{margin-top:12px;height:12px;border-radius:6px;background:rgba(244,238,230,.12);overflow:hidden}
#s7-fill{height:100%;width:100%;background:linear-gradient(90deg,#e0566e,#f2c94c);border-radius:6px;transform-origin:left center}
""", """
<div id="s7-bg" class="full"></div>
<div id="s7-t1" class="abs center it">Tekan</div>
<div id="s7-t2" class="abs center">BEG KUNING</div>
<div id="s7-rip" class="abs"></div>
<div id="s7-btn" class="abs"><svg width="140" height="140" viewBox="0 0 96 96"><path d="M22 36 H74 L78 84 H18 Z"/><path d="M36 36 V28 A12 12 0 0 1 60 28 V36"/></svg></div>
<div id="s7-tip" class="abs"></div>
<div id="s7-card" class="abs"><div class="th"><img src="assets/img/bt_glory.png"/><img src="assets/img/bt_noche.png"/></div><div class="tx"><div class="a">Frescura Body</div><div class="b">Foaming · 500 ml</div></div><div id="s7-co">Checkout<div id="s7-ok">✓ Done</div></div></div>
<div id="s7-stk" class="abs"><div class="lb"><span>Stok</span><b id="s7-pc">Terhad</b></div><div class="bar"><div id="s7-fill"></div></div></div>
""", """
tl.fromTo('#s7-t1',{opacity:0,filter:'blur(10px)'},{opacity:1,filter:'blur(0px)',duration:.3,ease:'expo.out'},0.02);
tl.fromTo('#s7-t2',{opacity:0,scaleX:1.5,filter:'blur(10px)'},{opacity:1,scaleX:1,filter:'blur(0px)',duration:.5,ease:'expo.out'},0.4);
tl.fromTo('#s7-btn',{scale:0,rotation:-30},{scale:1,rotation:0,duration:.45,ease:'back.out(1.6)'},0.1);
tl.fromTo('#s7-tip',{x:220,y:260,opacity:0},{x:0,y:0,opacity:1,duration:.4,ease:'power3.out'},0.2);
tl.to('#s7-tip',{scale:.8,duration:.07},0.6);tl.to('#s7-tip',{scale:1,duration:.12},0.67);
tl.to('#s7-btn',{scale:.9,duration:.07},0.6);tl.to('#s7-btn',{scale:1,duration:.28,ease:'back.out(2)'},0.67);
tl.fromTo('#s7-rip',{scale:1,opacity:.9},{scale:1.7,opacity:0,duration:.6,ease:'power2.out'},0.62);
tl.fromTo('#s7-card',{opacity:0,y:80},{opacity:1,y:0,duration:.5,ease:'expo.out'},0.95);
tl.to('#s7-tip',{x:330,y:175,duration:.4,ease:'power3.inOut'},1.0);
tl.to('#s7-co',{scale:.92,duration:.07},1.44);tl.to('#s7-co',{scale:1,duration:.25,ease:'back.out(2)'},1.51);
tl.to('#s7-ok',{opacity:1,duration:.15},1.52);
tl.to('#s7-tip',{opacity:0,duration:.2},1.75);
tl.fromTo('#s7-stk',{opacity:0,y:30},{opacity:1,y:0,duration:.35,ease:'expo.out'},2.3);
tl.fromTo('#s7-fill',{scaleX:1},{scaleX:.12,duration:.55,ease:'power3.out'},2.5);
tl.to(['#s7-card','#s7-stk','#s7-btn','#s7-t1','#s7-t2'],{opacity:0,filter:'blur(10px)',duration:.2,ease:'power2.in'},2.84);
""")

# ---------------------------------------------------------------- S8 CHOOSE 30.95 - 33.1
rs = __import__('random').Random(4)
stars = "".join(f'<i style="left:{rs.randint(0,540)}px;top:{rs.randint(0,1920)}px;opacity:{rs.uniform(.3,1):.2f};width:{(z:=rs.choice([2,2,3,4]))}px;height:{z}px"></i>' for _ in range(90))
scene("s8", 2.15, """
.s8-p{position:absolute;top:0;width:540px;height:1920px;overflow:hidden}
#s8-l{left:0;background:radial-gradient(500px 900px at 50% 45%,#8d1a2c,#3a0610 70%,#1b0307)}
#s8-r{left:540px;background:radial-gradient(500px 900px at 50% 45%,#4b37a8,#160f3d 70%,#07051a)}
#s8-r i{position:absolute;border-radius:50%;background:#fff}
.s8-bt{position:absolute;left:125px;top:520px;height:600px;filter:drop-shadow(0 30px 40px rgba(0,0,0,.6))}
#s8-bn{left:110px}
.s8-nm{position:absolute;left:0;width:540px;top:350px;text-align:center;font-family:'Bodoni Moda';font-style:italic;font-size:64px;line-height:1.02}
.s8-sb{position:absolute;left:0;width:540px;top:295px;text-align:center;font-size:28px;letter-spacing:.4em;text-transform:uppercase;color:#d8b77a}
#s8-or{left:470px;top:740px;width:140px;height:140px;border-radius:50%;background:#0d0b0a;border:2px solid #d8b77a;display:flex;align-items:center;justify-content:center;font-family:'Bodoni Moda';font-style:italic;font-size:44px;color:#d8b77a}
""", f"""
<div id="s8-l" class="s8-p"><div class="s8-sb">Woman Glory</div><div class="s8-nm">Bombshell</div><img id="s8-bg" class="s8-bt" src="assets/img/bt_glory.png"/></div>
<div id="s8-r" class="s8-p">{stars}<div class="s8-sb">Noche</div><div class="s8-nm" style="top:335px;font-size:56px">Midnight<br/>Fantasy</div><img id="s8-bn" class="s8-bt" src="assets/img/bt_noche.png"/></div>
<div id="s8-or" class="abs">atau</div>
""", """
tl.fromTo('#s8-l',{y:-1920},{y:0,duration:.45,ease:'expo.out'},0);
tl.fromTo('#s8-r',{y:1920},{y:0,duration:.45,ease:'expo.out'},0);
tl.fromTo(['#s8-bg','#s8-bn'],{scale:.85,opacity:0},{scale:1,opacity:1,duration:.5,ease:'expo.out',stagger:.08},0.2);
tl.fromTo('#s8-r i',{opacity:0},{opacity:.8,duration:.6,stagger:.004},0.2);
// Bombshell spotlight
tl.to('#s8-l',{filter:'brightness(1.15)',duration:.25},0.78);tl.to('#s8-r',{filter:'brightness(.55)',duration:.25},0.78);
tl.to('#s8-bg',{scale:1.07,duration:.4,ease:'expo.out'},0.78);
tl.fromTo('#s8-or',{scale:0,rotation:-90},{scale:1,rotation:0,duration:.4,ease:'back.out(1.8)'},1.18);
// Midnight Fantasy spotlight
tl.to('#s8-r',{filter:'brightness(1.15)',duration:.25},1.56);tl.to('#s8-l',{filter:'brightness(.55)',duration:.25},1.56);
tl.to('#s8-bg',{scale:1,duration:.3},1.56);tl.to('#s8-bn',{scale:1.07,duration:.4,ease:'expo.out'},1.56);
tl.to(['#s8-l','#s8-r'],{filter:'brightness(1)',duration:.2},1.95);
""")

# ---------------------------------------------------------------- S9 URGENCY + END CARD 33.1 - 36.8
scene("s9", 4.3, """
#s9-bg{background:radial-gradient(900px 1000px at 50% 40%,#231a12,#0b0908 70%);}
#s9-a{top:520px;font-size:110px;font-weight:500;line-height:1}
#s9-b{top:650px;font-size:70px;font-weight:400;opacity:.8}
#s9-c{top:740px;font-size:168px;font-weight:800;letter-spacing:.04em;color:#d8b77a;line-height:1}
#s9-line{left:140px;top:960px;width:800px;height:3px;background:#d8b77a;transform-origin:left center}
#s9-end{position:absolute;inset:0}
#s9-glow{left:90px;top:120px;width:900px;height:900px;background:radial-gradient(closest-side,rgba(255,220,170,.28),transparent 70%)}
#s9-logo{left:240px;top:200px;width:600px;height:600px;mix-blend-mode:screen}
#s9-logo img{width:100%;height:100%}
#s9-pl{left:250px;top:1060px;width:580px;height:90px;border-radius:50%;background:radial-gradient(closest-side,#3c3026,#1d1612);box-shadow:0 0 0 3px #c9a86a inset,0 0 60px rgba(216,183,122,.3)}
.s9-bt{position:absolute;top:640px;height:450px;filter:drop-shadow(0 24px 30px rgba(0,0,0,.6))}
#s9-g{left:380px}#s9-n{left:560px}
#s9-cta{position:absolute;left:0;width:1080px;top:1190px;text-align:center}
#s9-cta span{display:inline-block;padding:24px 48px;border-radius:60px;background:#f2c94c;color:#0d0b0a;font-weight:700;font-size:34px;letter-spacing:.12em;text-transform:uppercase}
#s9-sub{top:1295px;font-size:30px;letter-spacing:.42em;text-transform:uppercase;color:#d8b77a}
""", """
<div id="s9-bg" class="full"></div>
<div id="s9-kin" class="full">
<div id="s9-a" class="abs center it">Jangan tunggu</div>
<div id="s9-b" class="abs center it">sampai</div>
<div id="s9-c" class="abs center">TERLEPAS.</div>
<div id="s9-line" class="abs"></div>
</div>
<div id="s9-end">
<div id="s9-glow" class="abs"></div>
<div id="s9-logo" class="abs"><img src="assets/img/logo.jpg"/></div>
<img id="s9-g" class="s9-bt" src="assets/img/bt_glory.png"/><img id="s9-n" class="s9-bt" src="assets/img/bt_noche.png"/>
<div id="s9-pl" class="abs"></div>
<div id="s9-cta"><span>Tekan beg kuning · Checkout</span></div>
<div id="s9-sub" class="abs center">Stok terhad</div>
</div>
""", """
tl.fromTo('#s9-a',{opacity:0,filter:'blur(10px)'},{opacity:1,filter:'blur(0px)',duration:.3,ease:'expo.out'},0.05);
tl.fromTo('#s9-b',{opacity:0},{opacity:.8,duration:.3},0.95);
tl.fromTo('#s9-c',{opacity:0,scale:1.6,filter:'blur(14px)'},{opacity:1,scale:1,filter:'blur(0px)',duration:.45,ease:'expo.out'},1.36);
shake(tl,'#s9-kin',1.4,18,5);
tl.fromTo('#s9-line',{scaleX:1},{scaleX:0,duration:1.85,ease:'none'},0.05);
tl.to('#s9-kin',{opacity:0,scale:.9,filter:'blur(12px)',duration:.25,ease:'power3.in'},1.95);
tl.set('#s9-end',{opacity:0},0);
tl.to('#s9-end',{opacity:1,duration:.3},2.05);
tl.fromTo('#s9-logo',{scale:1.2,filter:'blur(12px)'},{scale:1,filter:'blur(0px)',duration:.8,ease:'expo.out',immediateRender:false},2.05);
tl.fromTo(['#s9-g','#s9-n'],{y:120,opacity:0},{y:0,opacity:1,duration:.7,stagger:.1,ease:'expo.out',immediateRender:false},2.15);
tl.fromTo('#s9-cta span',{opacity:0,y:30},{opacity:1,y:0,duration:.5,ease:'expo.out',immediateRender:false},2.45);
tl.fromTo('#s9-sub',{opacity:0},{opacity:1,duration:.4,immediateRender:false},2.35);
""")

# ---------------------------------------------------------------- CHROME (brand mark, chapters, progress, grain)
chap = [(0,"01","Realiti"),(7.0,"02","Fakta"),(11.55,"03","Keperluan"),(15.85,"04","Peringatan"),(19.28,"05","Solusi"),(24.6,"06","Untuk kamu"),(27.9,"07","Checkout"),(30.95,"08","Pilihan"),(33.1,"09","Sekarang")]
chap_js = ""
for i,(t,n,l) in enumerate(chap):
    chap_js += f"tl.set('#big',{{textContent:'{n}'}},{t});tl.fromTo('#big',{{opacity:0,y:60}},{{opacity:1,y:0,duration:.8,ease:'expo.out',immediateRender:{'true' if i==0 else 'false'}}},{t});"
    chap_js += f"tl.set('#ch-n',{{textContent:'{n} /'}},{t});tl.set('#ch-l',{{textContent:'{l}'}},{t});tl.fromTo('#ch',{{opacity:0,y:-10}},{{opacity:1,y:0,duration:.35,ease:'expo.out',immediateRender:{'true' if i==0 else 'false'}}},{t});"
scene("chrome", TOTAL, """
#br{left:70px;top:184px;font-size:28px;letter-spacing:.5em;font-weight:500;color:rgba(244,238,230,.75)}
#ch{right:70px;top:180px;font-size:28px;letter-spacing:.32em;text-transform:uppercase;color:rgba(244,238,230,.75);text-align:right}
#ch-n{font-weight:600;color:#d8b77a;margin-right:14px}
#pg{left:70px;top:1360px;width:940px;height:2px;background:rgba(244,238,230,.12)}
#pgf{width:100%;height:100%;background:#d8b77a;transform-origin:left center}
#big{right:40px;top:1340px;font-size:520px;line-height:1;color:transparent;-webkit-text-stroke:2px rgba(216,183,122,.16);font-weight:500}
#gr{background:url('assets/img/grain.png');opacity:.07;mix-blend-mode:overlay}
#vg{background:radial-gradient(ellipse at 50% 45%,transparent 55%,rgba(0,0,0,.45) 100%)}
""", """
<div id="vg" class="full"></div>
<div id="gr" class="full"></div>
<div id="br" class="abs">FRESCURA BODY</div>
<div id="ch" class="abs"><span id="ch-n">01 /</span><span id="ch-l">Realiti</span></div>
<div id="pg" class="abs"><div id="pgf"></div></div>
<div id="big" class="abs it" data-layout-ignore>01</div>
""", chap_js + f"""
tl.fromTo('#pgf',{{scaleX:0}},{{scaleX:1,duration:{TOTAL},ease:'none'}},0);
tl.fromTo('#gr',{{backgroundPosition:'0px 0px'}},{{backgroundPosition:'512px 1536px',duration:{TOTAL},ease:'steps({int(TOTAL*15)})'}},0);
// dark chrome on the light editorial scene
tl.to(['#br','#ch'],{{color:'rgba(13,11,10,.8)',duration:.2}},24.6);tl.to('#ch-n',{{color:'#6e0f1d',duration:.2}},24.6);tl.to('#ch-n',{{color:'#d8b77a',duration:.2}},27.9);tl.to(['#br','#ch'],{{color:'rgba(244,238,230,.75)',duration:.2}},27.9);
tl.to('#vg',{{opacity:.35,duration:.2}},24.6);tl.to('#big',{{webkitTextStroke:'2px rgba(110,15,29,.18)',duration:.2}},24.6);tl.to('#big',{{webkitTextStroke:'2px rgba(216,183,122,.16)',duration:.2}},27.9);tl.to('#vg',{{opacity:1,duration:.2}},27.9);
tl.to(['#br','#ch','#pg','#big'],{{opacity:0,duration:.4}},35.1);
""")

# ---------------------------------------------------------------- CAPTIONS
# (text, voice_start, emphasis) ; groups split by '|'
WORDS = """Suami .00 0|dapat .44 0|perhatian, .66 1|/anak 1.52 0|dapat 1.66 0|perhatian, 1.94 1|/rumah 2.58 0|pun 3.02 0|dapat 3.30 0|perhatian. 3.46 1|/Habis 4.22 0|tu 4.56 0|diri 4.86 1|sendiri, 5.20 1|/siapa 5.46 0|nak 5.72 0|jaga? 5.86 1|
/Ramai 6.80 0|wanita 7.14 1|terlalu 7.66 0|sibuk 8.04 1|/menguruskan 8.44 0|keluarga 8.94 1|/sampai 9.64 0|tak 9.88 0|ada 10.08 0|masa 10.22 1|/untuk 10.56 0|diri 10.82 1|sendiri. 11.06 1|
/Padahal 11.34 0|kita 11.78 0|pun 12.00 0|perlukan 12.20 0|masa 12.46 1|/untuk 12.82 0|berehat 13.10 1|/dan 13.32 0|menjaga 13.54 0|kebersihan 13.82 1|/serta 14.28 0|penampilan 14.72 1|diri. 15.06 0|
/Jangan 15.62 0|asyik 16.14 0|dahulukan 16.48 1|/semua 16.94 0|orang 17.28 1|/sampai 17.52 0|lupa 17.82 1|/diri 18.36 1|sendiri. 18.74 1|
/Pastinya, 19.06 0|/Frescura 19.64 1|Body. 20.18 1|/Nikmati 20.48 0|buih 21.02 1|lembut 21.20 1|/terus 21.52 0|daripada 21.82 0|botol 22.18 1|/dengan 22.50 0|pilihan 22.74 0|wangian 23.10 1|/yang 23.48 0|feminin. 23.78 1|
/Girls, 24.38 1|/kali 25.04 0|ni 25.34 0|jangan 25.56 0|berkira 25.90 1|/sangat 26.24 0|untuk 26.60 0|diri 27.10 1|sendiri. 27.40 1|
/Tekan 27.68 0|beg 28.08 1|kuning 28.22 1|sekarang 28.40 0|/dan 28.78 0|checkout 29.06 1|/Frescura 29.46 1|Body, 29.90 1|/stok 30.16 0|tak 30.36 0|banyak. 30.50 1|
/Korang 30.72 0|pilih 30.98 0|nak 31.32 0|/Bombshell 31.48 1|ataupun 31.90 0|/Midnight 32.26 1|Fantasy. 32.44 1|
/Jangan 32.90 0|tunggu 33.38 1|/sampai 33.84 0|terlepas. 34.24 1"""
groups = []; cur = []
for tok in WORDS.replace("\n","").split("|"):
    tok = tok.strip()
    if not tok: continue
    new = tok.startswith("/"); tok = tok.lstrip("/")
    w, t, e = tok.split()
    if new and cur: groups.append(cur); cur = []
    cur.append((w, float(t)+OFF, e == "1"))
groups.append(cur)
cap_html = ""; cap_js = ""
for gi, g in enumerate(groups):
    start = g[0][1] - 0.06
    nxt = groups[gi+1][0][1] - 0.06 if gi+1 < len(groups) else 35.05
    end = min(nxt, g[-1][1] + 0.9)
    words = "".join(f'<span id="w{gi}_{wi}" class="w{" em" if e else ""}">{w}</span> ' for wi,(w,t,e) in enumerate(g))
    cap_html += f'<div id="cg{gi}" class="clip cg" data-start="{start:.3f}" data-duration="{end-start:.3f}"><div class="cin" id="ci{gi}"><span class="pill">{words.strip()}</span></div></div>\n'
    cap_js += f"tl.fromTo('#ci{gi}',{{opacity:0,y:18,scale:.96}},{{opacity:1,y:0,scale:1,duration:.16,ease:'expo.out'}},{start:.3f});"
    for wi,(w,t,e) in enumerate(g):
        cap_js += f"tl.fromTo('#w{gi}_{wi}',{{opacity:.38}},{{opacity:1,duration:.1,ease:'none'}},{t:.3f});"
        if e: cap_js += f"tl.fromTo('#w{gi}_{wi}',{{scale:1.1}},{{scale:1,duration:.3,ease:'expo.out',immediateRender:false}},{t:.3f});"
    cap_js += f"tl.to('#ci{gi}',{{opacity:0,duration:.1,ease:'power2.in'}},{end-0.1:.3f});"
scene("captions", TOTAL, """
.cg{position:absolute;left:0;top:1170px;width:1080px;height:150px;}
.cin{position:absolute;left:60px;width:960px;top:0;text-align:center;}
.pill{display:inline-block;padding:14px 34px 18px;border-radius:22px;background:rgba(13,11,10,.55);backdrop-filter:blur(10px);font-family:'Jost';font-weight:600;font-size:62px;line-height:1.15;color:#f4eee6;letter-spacing:.005em}
.w{display:inline-block}
.em{font-family:'Bodoni Moda';font-style:italic;font-weight:700;color:#e4c68a;font-size:70px;margin:0 .1em}
""", cap_html, cap_js)

# ---------------------------------------------------------------- ROOT
hosts = [("s1",0,7.0,10),("s2",7.0,4.55,11),("s3",11.55,4.3,12),("s4",15.85,3.43,13),("s5",19.28,5.32,14),("pump",21.15,2.15,15),("s6",24.6,3.3,16),("s7",27.9,3.05,17),("s8",30.95,2.15,18),("s9",33.1,4.3,19)]
host_html = "".join(f'<div id="{i}" data-composition-id="{i}" data-composition-src="compositions/{i}.html" data-start="{s}" data-duration="{d}" data-track-index="1" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:{z}"></div>\n' for i,s,d,z in hosts)
index = f"""<!doctype html>
<html lang="ms">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width={W}, height={H}"/>
<script src="gsap.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#0b0908}}
#bgfill{{position:absolute;inset:0;background:#0b0908}}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}" data-fps="30">
<div id="bgfill"></div>
{host_html}<div id="chrome" data-composition-id="chrome" data-composition-src="compositions/chrome.html" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:40"></div>
<div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-track-kind="captions" data-width="{W}" data-height="{H}" style="z-index:50"></div>
<audio id="mix" class="clip" src="assets/audio/mix.wav" data-start="0" data-duration="{TOTAL}" data-volume="1" data-track-index="4"></audio>
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
tl.set({{}}, {{}}, {TOTAL - 0.01});
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
open("index.html","w").write(index)
json.dump([[g[0][1], g[-1][1], " ".join(w for w,_,_ in g)] for g in groups], open("caption_groups.json","w"), ensure_ascii=False, indent=0)
print("groups", len(groups))
