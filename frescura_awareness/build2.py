# v2: "3 perkara" script. Generates index.html + compositions/*.html (1080x1920, 30fps)
import json, os, glob
exec(open('parts_head.py').read())          # OFF, W, H, BASE, HELP, scene(), ICON, icon()
TOTAL = 33.6
for f in glob.glob('compositions/*.html'): os.remove(f)
ICON.update({
 'shirt':'<path class="ln" pathLength="1" d="M32 16 L14 28 L22 42 L32 37 V84 H64 V37 L74 42 L82 28 L64 16 Q48 30 32 16 Z"/>',
 'eye':'<path class="ln" pathLength="1" d="M6 48 Q48 10 90 48 Q48 86 6 48 Z"/><circle class="ln" pathLength="1" cx="48" cy="48" r="13"/>',
 'heart':'<path class="ln" pathLength="1" d="M48 80 C20 60 12 44 22 30 C32 18 44 24 48 32 C52 24 64 18 74 30 C84 44 76 60 48 80 Z"/>',
 'cart':'<path class="ln" pathLength="1" d="M8 18 H20 L30 62 H76 L84 30 H24"/><circle class="ln" pathLength="1" cx="36" cy="76" r="6"/><circle class="ln" pathLength="1" cx="70" cy="76" r="6"/>',
})
TIPCSS = """
#{p}-k{{top:236px;left:470px;text-align:left;}}
#{p}-num{{left:70px;top:200px;font-size:250px;line-height:1;color:#d8b77a;font-weight:500}}
#{p}-t1{{left:470px;top:280px;font-size:66px;font-weight:500;}}
#{p}-t2{{left:470px;top:365px;width:560px;font-size:56px;font-weight:700;line-height:1.12;letter-spacing:.01em}}
#{p}-arch{{left:150px;top:540px;width:780px;height:600px;overflow:hidden;border-radius:390px 390px 26px 26px;}}
#{p}-rim{{left:150px;top:540px;width:780px;height:600px;border-radius:390px 390px 26px 26px;box-shadow:0 0 0 2px #d8b77a inset;}}
"""
def tip_head(p, num, eyebrow, t1, t2):
    return f'''<div id="{p}-bg" class="full" style="background:radial-gradient(900px 900px at 50% 45%,#211912,#0b0908 70%)"></div>
<div id="{p}-num" class="abs it">{num}</div>
<div id="{p}-k" class="abs eyebrow">{eyebrow}</div>
<div id="{p}-t1" class="abs it">{t1}</div>
<div id="{p}-t2" class="abs serif">{t2}</div>'''
def tip_in(p, tk, tt1, tt2):
    return f"""tl.fromTo('#{p}-num',{{opacity:0,y:120,filter:'blur(14px)'}},{{opacity:1,y:0,filter:'blur(0px)',duration:.5,ease:'expo.out'}},0);
inBlur(tl,'#{p}-k',{tk},.35);inBlur(tl,'#{p}-t1',{tt1},.3);
tl.fromTo('#{p}-t2',{{opacity:0,x:40,filter:'blur(10px)'}},{{opacity:1,x:0,filter:'blur(0px)',duration:.4,ease:'expo.out'}},{tt2});
tl.fromTo(['#{p}-arch','#{p}-rim'],{{clipPath:'inset(100% 0% 0% 0% round 0px)'}},{{clipPath:'inset(0% 0% 0% 0% round 0px)',duration:.6,ease:'expo.out'}},0.05);"""
def tip_out(p, t):
    return f"tl.to('#{p}-wrap',{{x:-300,opacity:0,filter:'blur(14px)',duration:.22,ease:'power3.in'}},{t});"

# ------------------------------------------------ A HOOK 0 - 5.3
scene("a", 5.3, """
#a-bg{background:radial-gradient(900px 900px at 50% 40%,#2a1f17 0%,#120e0b 55%,#0b0908 100%);}
#a-k{top:240px;}
#a-t1{top:290px;font-size:92px;font-weight:500;}
#a-t2{top:410px;font-size:118px;font-weight:800;line-height:1;letter-spacing:-.01em}
#a-t3{top:515px;font-size:64px;font-weight:500;color:#d8b77a}
.a-p{position:absolute;top:720px;width:230px;height:230px;border-radius:50%;border:2px solid rgba(216,183,122,.7);display:flex;align-items:center;justify-content:center;background:radial-gradient(circle,rgba(216,183,122,.12),transparent 70%)}
.a-p span{font-family:'Jost';font-size:30px;letter-spacing:.32em;text-transform:uppercase}
#a-l{left:150px}#a-r{left:700px}
#a-h{left:460px;top:745px;width:160px;height:160px}
#a-x{top:290px;font-size:80px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;line-height:1}
#a-3{top:400px;font-size:560px;line-height:1;color:#d8b77a;font-weight:600}
#a-3b{top:1010px;font-size:84px;font-weight:500}
""", f"""
<div id="a-bg" class="full"></div>
<div id="a-wrap" class="full">
<div id="a-k" class="abs center eyebrow">Tip untuk isteri</div>
<div id="a-t1" class="abs center it">Nak suami sentiasa</div>
<div id="a-t2" class="abs center serif">selesa &amp; dekat?</div>
<div id="a-l" class="a-p"><span>Dia</span></div>
<div id="a-r" class="a-p"><span>Kamu</span></div>
<svg id="a-h" class="abs" viewBox="0 0 96 96">{ICON['heart'].replace('class="ln"','class="ln a-hl"')}</svg>
<div id="a-x" class="abs center gold">Jangan abaikan</div>
<div id="a-3" class="abs center serif">3</div>
<div id="a-3b" class="abs center it">perkara ini.</div>
</div>
""", """
tl.fromTo('#a-k',{opacity:0,scaleX:1.3},{opacity:1,scaleX:1,duration:.8,ease:'expo.out'},0);
tl.fromTo('#a-t2',{scale:1.08},{scale:1,duration:1.2,ease:'expo.out'},0);
tl.fromTo('#a-l',{opacity:0,x:-200},{opacity:1,x:0,duration:.6,ease:'expo.out'},0.7);
tl.fromTo('#a-r',{opacity:0,x:200},{opacity:1,x:0,duration:.6,ease:'expo.out'},0.85);
// "dekat dengan korang": they move closer, heart draws
tl.to('#a-l',{x:110,duration:.6,ease:'power3.inOut'},2.2);tl.to('#a-r',{x:-110,duration:.6,ease:'power3.inOut'},2.2);
draw(tl,'.a-hl',2.65,.5);tl.fromTo('#a-h',{scale:.6},{scale:1,duration:.5,ease:'back.out(2)'},2.65);
// "jangan abaikan"
tl.to(['#a-t1','#a-t2','#a-k','#a-l','#a-r','#a-h'],{opacity:0,filter:'blur(10px)',duration:.2,ease:'power2.in'},3.15);
tl.set(['#a-x','#a-3','#a-3b'],{opacity:0},0);
slam(tl,'#a-x',3.3,1.4);shake(tl,'#a-wrap',3.35,18,2);
tl.fromTo('#a-3',{opacity:0,scale:2.2,filter:'blur(20px)'},{opacity:1,scale:1,filter:'blur(0px)',duration:.5,ease:'expo.out',immediateRender:false},4.2);
inBlur(tl,'#a-3b',4.5,.35);
tl.to('#a-3',{x:-600,opacity:0,filter:'blur(16px)',duration:.25,ease:'power3.in'},5.05);
tl.to(['#a-x','#a-3b'],{opacity:0,duration:.2},5.05);
""")

# ------------------------------------------------ B TIP 1 kebersihan badan 5.3 - 7.25
scene("b", 1.95, TIPCSS.format(p='b') + """
#b-v{position:absolute;left:-150px;top:-540px;width:1080px;height:1920px;object-fit:cover}
#b-ic{left:840px;top:1050px;width:120px;height:120px;border-radius:50%;background:#0d0b0a;border:2px solid #d8b77a;display:flex;align-items:center;justify-content:center}
""", f"""<div id="b-wrap" class="full">{tip_head('b','01','Pertama','Jaga','kebersihan badan')}
<div id="b-arch" class="abs"><video id="b-v" class="clip" src="assets/vid/lather.mp4" data-start="0" data-duration="1.95" muted playsinline></video></div>
<div id="b-rim" class="abs"></div>
<div id="b-ic" class="abs">{icon('drop','b-svg',72)}</div></div>
""", tip_in('b', .1, .8, 1.1) + """
tl.fromTo('#b-v',{scale:1.15},{scale:1,duration:1.95,ease:'power1.out'},0);
tl.fromTo('#b-ic',{scale:0},{scale:1,duration:.4,ease:'back.out(2)'},1.2);draw(tl,'.b-svg .ln',1.25,.45);
""" + tip_out('b', 1.73))

# ------------------------------------------------ C TIP 2 pakaian bersih 7.25 - 9.7
r = __import__('random').Random(12)
sp = "".join(f'<svg class="abs c-sp" id="c-sp{i}" style="left:{x}px;top:{y}px" width="{z}" height="{z}" viewBox="0 0 96 96"><path d="M48 10 L54 42 L86 48 L54 54 L48 86 L42 54 L10 48 L42 42 Z" fill="#fff5dc"/></svg>' for i,(x,y,z) in enumerate([(300,640,60),(700,700,44),(250,960,40),(760,980,56),(520,600,34)]))
scene("c", 2.45, TIPCSS.format(p='c') + """
#c-img{position:absolute;left:-760px;top:-60px;width:2000px;height:auto;filter:blur(3px) brightness(.55) sepia(.2)}
#c-sh{left:390px;top:680px;width:300px;height:300px}
#c-sh .ln{stroke:#f4eee6;stroke-width:2.6}
""", f"""<div id="c-wrap" class="full">{tip_head('c','02','Kedua','Pastikan','pakaian sentiasa bersih')}
<div id="c-arch" class="abs"><img id="c-img" src="assets/img/linen_pair.jpg"/></div>
<div id="c-rim" class="abs"></div>
<svg id="c-sh" class="abs" viewBox="0 0 96 96">{ICON['shirt'].replace('class="ln"','class="ln c-shl"')}</svg>
{sp}</div>
""", tip_in('c', .05, .6, 1.0) + """
tl.fromTo('#c-img',{x:0,y:0},{x:-120,y:-40,duration:2.45,ease:'power1.inOut'},0);
draw(tl,'.c-shl',0.9,.8);
tl.fromTo('.c-sp',{opacity:0,scale:0,rotation:-60},{opacity:1,scale:1,rotation:0,duration:.35,stagger:.06,ease:'back.out(2)'},1.95);
""" + tip_out('c', 2.23))

# ------------------------------------------------ D TIP 3 rutin konsisten 9.7 - 13.3
days = ["Isn","Sel","Rab","Kha","Jum","Sab","Ahd"]
dhtml = "".join(f'<div class="d-day" id="d-d{i}"><div class="d-c"><svg width="54" height="54" viewBox="0 0 96 96"><path class="ln d-ck{i}" pathLength="1" d="M28 50 L43 65 L70 34" style="stroke:#0d0b0a;stroke-width:9"/></svg><div class="d-f" id="d-f{i}"></div></div><span>{d}</span></div>' for i,d in enumerate(days))
scene("d", 3.6, TIPCSS.format(p='d') + """
#d-card{left:110px;top:600px;width:860px;height:470px;border-radius:30px;background:rgba(244,238,230,.05);border:1.5px solid rgba(216,183,122,.4);}
#d-ct{left:150px;top:640px;font-size:30px;letter-spacing:.32em;text-transform:uppercase;color:#d8b77a}
#d-st{right:150px;top:625px;font-size:56px;font-weight:700}
#d-row{left:150px;top:760px;width:780px;display:flex;justify-content:space-between}
.d-day{display:flex;flex-direction:column;align-items:center;gap:16px;font-size:28px;letter-spacing:.08em}
.d-c{position:relative;width:88px;height:88px;border-radius:50%;border:2px solid rgba(216,183,122,.5);display:flex;align-items:center;justify-content:center;overflow:hidden}
.d-c svg{position:relative;z-index:2}
.d-f{position:absolute;inset:0;background:#d8b77a;border-radius:50%}
#d-note{left:150px;top:940px;width:780px;font-size:34px;line-height:1.3;opacity:.85}
#d-note b{font-family:'Bodoni Moda';font-style:italic;color:#d8b77a}
""", f"""<div id="d-wrap" class="full">{tip_head('d','03','Ketiga','Amalkan','rutin penjagaan diri')}
<div id="d-card" class="abs"></div>
<div id="d-ct" class="abs">Rutin mingguan</div>
<div id="d-st" class="abs serif"><span id="d-n">0</span>/7</div>
<div id="d-row" class="abs">{dhtml}</div>
<div id="d-note" class="abs">Kuncinya: <b>konsisten</b>, setiap hari.</div></div>
""", tip_in('d', .1, .8, 1.2).replace("tl.fromTo(['#d-arch','#d-rim'],{clipPath:'inset(100% 0% 0% 0% round 0px)'},{clipPath:'inset(0% 0% 0% 0% round 0px)',duration:.6,ease:'expo.out'},0.05);","") + """
tl.fromTo('#d-card',{opacity:0,y:60},{opacity:1,y:0,duration:.5,ease:'expo.out'},0.3);
tl.fromTo(['#d-ct','#d-st'],{opacity:0},{opacity:1,duration:.3},0.45);
tl.fromTo('.d-day',{opacity:0,y:30},{opacity:1,y:0,duration:.35,stagger:.05,ease:'expo.out'},0.5);
var dn=document.getElementById('d-n');
for(var i=0;i<7;i++){var t=1.4+i*0.21;tl.fromTo('#d-f'+i,{scale:0},{scale:1,duration:.22,ease:'back.out(2)'},t);draw(tl,'.d-ck'+i,t+.08,.2);(function(k){tl.call(function(){dn.textContent=String(k)},null,t+.01);tl.call(function(){dn.textContent=String(k-1)},null,t-.01);})(i+1);}
inBlur(tl,'#d-note',2.3,.4);
""" + tip_out('d', 3.38))

# ------------------------------------------------ E overlooked 13.3 - 15.4
scene("e", 2.1, """
#e-bg{background:radial-gradient(800px 800px at 50% 45%,#1d1611,#0b0908 70%)}
#e-t{top:300px;font-size:120px;font-weight:500}
#e-eye{left:340px;top:520px;width:400px;height:400px;transform-origin:50% 50%}
#e-eye .ln{stroke-width:2.4}
#e-lid{opacity:0;left:340px;top:712px;width:400px;height:4px;background:#d8b77a;border-radius:2px}
#e-x{top:960px;font-size:92px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;line-height:1.05}
""", f"""<div id="e-bg" class="full"></div><div id="e-wrap" class="full">
<div id="e-t" class="abs center it">Nampak mudah…</div>
<svg id="e-eye" class="abs" viewBox="0 0 96 96">{ICON['eye'].replace('class="ln"','class="ln e-l"')}</svg>
<div id="e-lid" class="abs"></div>
<div id="e-x" class="abs center gold">Terlepas<br/>pandang.</div></div>
""", """
inBlur(tl,'#e-t',0.03,.4);
draw(tl,'.e-l',0.4,.6);
tl.to('#e-eye',{scaleY:.04,duration:.18,ease:'power3.in'},1.25);tl.to('#e-lid',{opacity:1,duration:.05},1.4);
slam(tl,'#e-x',1.31,1.4);shake(tl,'#e-wrap',1.33,16,4);
tl.to('#e-wrap',{opacity:0,scale:1.15,filter:'blur(14px)',duration:.22,ease:'power3.in'},1.88);
""")

# ------------------------------------------------ F MALL 15.4 - 22.45 (reuses v1 mall scene)
mall = open('parts_mall.py').read().split('\n',1)[1]
for a,b in [('scene("s5", 5.32,','scene("s5", 7.05,'),("duration:5.32","duration:7.05"),("duration:3.75,","duration:5.5,"),
            ('<div id="s5-pre" class="abs center it">Pastinya,</div>','<div id="s5-pre" class="abs center it">Untuk rutin mandi<br/>harian korang,</div>'),
            ("#s5-pre{top:860px;font-size:76px;","#s5-pre{top:270px;font-size:72px;line-height:1.1;"),
            ("{opacity:1,filter:'blur(0px)',duration:.3,ease:'expo.out'},0.03);","{opacity:1,filter:'blur(0px)',duration:.4,ease:'expo.out'},0.45);"),
            ("tl.to('#s5-pre',{opacity:0,filter:'blur(8px)',duration:.2},0.85);","tl.to('#s5-pre',{opacity:0,filter:'blur(8px)',duration:.2},2.15);"),
            ("0.58+d);","2.42+d);"),("tl.to('#s5-sign',{opacity:1,duration:.05},0.9);","tl.to('#s5-sign',{opacity:1,duration:.05},2.74);"),
            ("ease:'expo.out'},3.6);","ease:'expo.out'},5.8);"),("ease:'expo.out'},3.75);","ease:'expo.out'},6.32);"),
            ("},5.08);","},6.8);")]:
    assert a in mall, a; mall = mall.replace(a,b)
exec(mall)
pump = open('parts_pump.py').read().split('\n',1)[1]
for a,b in [('scene("pump", 2.15,','scene("pump", 1.9,'),('data-duration="2.15"','data-duration="1.9"'),("duration:2.15,","duration:1.9,"),
            ("},1.82);","},1.58);"),("},1.85);","},1.6);"),("var t=0.25+r()*0.9,","var t=0.2+r()*0.6,"),("ease:'expo.out'},0.3);","ease:'expo.out'},0.22);")]:
    assert a in pump, a; pump = pump.replace(a,b)
exec(pump)

# ------------------------------------------------ G RECAP (light) 22.45 - 25.6
items = [("01","Badan bersih"),("02","Pakaian bersih"),("03","Rutin konsisten")]
grows = "".join(f'<div id="g-r{i}" class="abs g-row" style="top:{520+i*130}px"><span class="it g-n">{n}</span><span>{t}</span><svg class="g-ck" width="60" height="60" viewBox="0 0 96 96"><path class="ln g-l{i}" pathLength="1" d="M28 50 L43 65 L70 34" style="stroke:#6e0f1d;stroke-width:7"/></svg></div>' for i,(n,t) in enumerate(items))
scene("g", 3.15, """
#g-bg{background:radial-gradient(900px 1100px at 50% 40%,#f6f0e8,#e8ddcf 70%,#d9ccbb);}
#g-k{top:240px;color:#6e0f1d}
#g-t{top:290px;font-size:104px;font-weight:600;color:#0d0b0a;line-height:1}
.g-row{left:130px;width:820px;height:110px;border-bottom:1.5px solid rgba(13,11,10,.18);display:flex;align-items:center;gap:30px;font-size:52px;font-weight:600;color:#0d0b0a}
.g-n{font-size:54px;color:#6e0f1d;width:80px}
.g-ck{margin-left:auto}
#g-x{top:960px;font-size:82px;font-weight:800;color:#0d0b0a;letter-spacing:.02em;line-height:1.05}
#g-x b{font-family:'Bodoni Moda';font-style:italic;color:#6e0f1d;font-weight:700}
""", f"""<div id="g-bg" class="full"></div><div id="g-wrap" class="full">
<div id="g-k" class="abs center eyebrow">Ringkasan</div>
<div id="g-t" class="abs center it">3 perkara ini</div>
{grows}
<div id="g-x" class="abs center">Jangan sekadar <b>dengar.</b></div></div>
""", """
tl.fromTo('#g-bg',{clipPath:'circle(0% at 50% 50%)'},{clipPath:'circle(80% at 50% 50%)',duration:.4,ease:'power3.out'},0);
inBlur(tl,'#g-k',.1,.35);inBlur(tl,'#g-t',.2,.4);
for(var i=0;i<3;i++){var t=.72+i*.2;tl.fromTo('#g-r'+i,{opacity:0,x:-60},{opacity:1,x:0,duration:.4,ease:'expo.out'},t);draw(tl,'.g-l'+i,t+.2,.3);}
tl.to('.g-row',{opacity:.35,duration:.3},1.95);
slam(tl,'#g-x',1.98,1.3);
tl.to('#g-wrap',{opacity:0,yPercent:-6,filter:'blur(8px)',duration:.2,ease:'power3.in'},2.93);
""")

# ------------------------------------------------ H CTA bag -> trolley -> checkout 25.6 - 29.2
scene("h", 3.6, """
#h-bg{background:radial-gradient(800px 800px at 50% 35%,#2a2010,#0b0908 70%);}
#h-t1{top:230px;font-size:92px;font-weight:500}
#h-t2{top:330px;font-size:120px;font-weight:800;letter-spacing:.08em;color:#f2c94c;line-height:1}
#h-btn{left:410px;top:500px;width:260px;height:260px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#ffe28a,#f2c94c 45%,#c99a1e);box-shadow:0 30px 80px rgba(242,201,76,.35);display:flex;align-items:center;justify-content:center}
#h-btn svg path{fill:none;stroke:#0d0b0a;stroke-width:5;stroke-linecap:round;stroke-linejoin:round}
#h-rip{left:410px;top:500px;width:260px;height:260px;border-radius:50%;border:3px solid #f2c94c}
#h-badge{left:630px;top:500px;width:74px;height:74px;border-radius:50%;background:#e0566e;color:#fff;font-weight:700;font-size:38px;display:flex;align-items:center;justify-content:center;box-shadow:0 8px 20px rgba(0,0,0,.4)}
#h-tip{left:0;top:0;width:70px;height:70px;border-radius:50%;background:rgba(244,238,230,.92);box-shadow:0 10px 30px rgba(0,0,0,.5)}
#h-card{left:110px;top:840px;width:860px;height:200px;border-radius:28px;background:rgba(244,238,230,.06);border:1.5px solid rgba(216,183,122,.4);display:flex;align-items:center;padding:0 28px;box-sizing:border-box;gap:22px}
#h-card .th{display:flex;gap:4px;height:150px}#h-card .th img{height:150px}
#h-card .tx{flex:1}#h-card .tx .a{font-family:'Bodoni Moda';font-style:italic;font-size:42px}#h-card .tx .b{font-size:28px;letter-spacing:.24em;color:#d8b77a;text-transform:uppercase;margin-top:6px}
#h-co{position:relative;width:250px;height:76px;border-radius:40px;background:#f2c94c;color:#0d0b0a;font-weight:700;font-size:30px;letter-spacing:.06em;text-transform:uppercase}
#h-co div{position:absolute;inset:0;border-radius:40px;display:flex;align-items:center;justify-content:center;gap:8px}
#h-co2{background:#f4eee6}#h-co3{background:#2e7d4f;color:#fff}
#h-co svg .ln{stroke:#0d0b0a;stroke-dashoffset:0;stroke-width:6}
""", f"""<div id="h-bg" class="full"></div><div id="h-wrap" class="full">
<div id="h-t1" class="abs center it">Tekan</div>
<div id="h-t2" class="abs center">BEG KUNING</div>
<div id="h-rip" class="abs"></div>
<div id="h-btn" class="abs"><svg width="130" height="130" viewBox="0 0 96 96"><path d="M22 36 H74 L78 84 H18 Z"/><path d="M36 36 V28 A12 12 0 0 1 60 28 V36"/></svg></div>
<div id="h-badge" class="abs">1</div>
<div id="h-card" class="abs"><div class="th"><img src="assets/img/bt_glory.png"/><img src="assets/img/bt_noche.png"/></div><div class="tx"><div class="a">Frescura Body</div><div class="b">500 ml</div></div>
<div id="h-co" data-layout-allow-overlap><div id="h-co1" data-layout-allow-overlap><svg width="40" height="40" viewBox="0 0 96 96">{ICON['cart']}</svg>+ Troli</div><div id="h-co2" data-layout-allow-overlap>Checkout</div><div id="h-co3" data-layout-allow-overlap>✓ Berjaya</div></div></div>
<div id="h-tip" class="abs"></div></div>
""", """
inBlur(tl,'#h-t1',0.05,.3);
tl.fromTo('#h-t2',{opacity:0,scaleX:1.5,filter:'blur(10px)'},{opacity:1,scaleX:1,filter:'blur(0px)',duration:.45,ease:'expo.out'},0.25);
tl.fromTo('#h-btn',{scale:0,rotation:-30},{scale:1,rotation:0,duration:.4,ease:'back.out(1.6)'},0.0);
tl.fromTo('#h-tip',{x:820,y:980,opacity:0},{x:600,y:690,opacity:1,duration:.35,ease:'power3.out'},0.1);
tl.to('#h-btn',{scale:.9,duration:.07},0.47);tl.to('#h-btn',{scale:1,duration:.28,ease:'back.out(2)'},0.54);
tl.fromTo('#h-rip',{scale:1,opacity:.9},{scale:1.7,opacity:0,duration:.6,ease:'power2.out'},0.5);
tl.fromTo('#h-card',{opacity:0,y:80},{opacity:1,y:0,duration:.5,ease:'expo.out'},0.8);
tl.set(['#h-co2','#h-co3','#h-badge'],{opacity:0},0);
tl.to('#h-tip',{x:790,y:930,duration:.45,ease:'power3.inOut'},1.75);
tl.to('#h-co',{scale:.92,duration:.07},2.27);tl.to('#h-co',{scale:1,duration:.25,ease:'back.out(2)'},2.34);
tl.fromTo('#h-badge',{scale:0,opacity:1},{scale:1,opacity:1,duration:.35,ease:'back.out(2.5)',immediateRender:false},2.32);
tl.to('#h-co2',{opacity:1,duration:.15},2.6);
tl.to('#h-tip',{x:800,y:940,duration:.3,ease:'power2.inOut'},2.7);
tl.to('#h-co',{scale:.92,duration:.07},3.13);tl.to('#h-co',{scale:1,duration:.22,ease:'back.out(2)'},3.2);
tl.to('#h-co3',{opacity:1,duration:.15},3.18);
tl.to('#h-tip',{opacity:0,duration:.15},3.3);
tl.to('#h-wrap',{opacity:0,filter:'blur(10px)',duration:.18,ease:'power2.in'},3.42);
""")

# ------------------------------------------------ I STOCK + END CARD 29.2 - 33.6
scene("i", 4.4, """
#i-bg{background:radial-gradient(900px 1000px at 50% 40%,#231a12,#0b0908 70%);}
#i-k{top:420px;font-size:40px;letter-spacing:.5em;text-transform:uppercase}
#i-bar{left:140px;top:520px;width:800px;height:26px;border-radius:13px;background:rgba(244,238,230,.12);overflow:hidden}
#i-fill{width:100%;height:100%;background:linear-gradient(90deg,#e0566e,#f2c94c);border-radius:13px;transform-origin:left center}
#i-pc{top:580px;font-size:150px;font-weight:700;color:#e0566e;line-height:1}
#i-x{top:800px;font-size:118px;font-weight:800;letter-spacing:.04em;color:#d8b77a;line-height:1.02;text-transform:uppercase}
#i-end{position:absolute;inset:0}
#i-glow{left:90px;top:120px;width:900px;height:900px;background:radial-gradient(closest-side,rgba(255,220,170,.28),transparent 70%)}
#i-logo{left:240px;top:200px;width:600px;height:600px;mix-blend-mode:screen}
#i-logo img{width:100%;height:100%}
#i-pl{left:250px;top:1060px;width:580px;height:90px;border-radius:50%;background:radial-gradient(closest-side,#3c3026,#1d1612);box-shadow:0 0 0 3px #c9a86a inset,0 0 60px rgba(216,183,122,.3)}
.i-bt{position:absolute;top:640px;height:450px;filter:drop-shadow(0 24px 30px rgba(0,0,0,.6))}
#i-g{left:380px}#i-n{left:560px}
#i-cta{position:absolute;left:0;width:1080px;top:1190px;text-align:center}
#i-cta span{display:inline-block;padding:24px 48px;border-radius:60px;background:#f2c94c;color:#0d0b0a;font-weight:700;font-size:34px;letter-spacing:.12em;text-transform:uppercase}
#i-sub{top:1295px;font-size:30px;letter-spacing:.42em;text-transform:uppercase;color:#d8b77a}
""", """<div id="i-bg" class="full"></div>
<div id="i-kin" class="full">
<div id="i-k" class="abs center">Stok</div>
<div id="i-bar" class="abs"><div id="i-fill"></div></div>
<div id="i-pc" class="abs center serif"><span id="i-n0">100</span>%</div>
<div id="i-x" class="abs center">Sangat<br/>terhad.</div>
</div>
<div id="i-end">
<div id="i-glow" class="abs"></div>
<div id="i-logo" class="abs"><img src="assets/img/logo.jpg"/></div>
<img id="i-g" class="i-bt" src="assets/img/bt_glory.png"/><img id="i-n" class="i-bt" src="assets/img/bt_noche.png"/>
<div id="i-pl" class="abs"></div>
<div id="i-cta"><span>Tekan beg kuning · Checkout</span></div>
<div id="i-sub" class="abs center">Stok sangat terhad</div>
</div>
""", """
inBlur(tl,'#i-k',0.1,.35);tl.fromTo('#i-bar',{opacity:0,scaleX:.6},{opacity:1,scaleX:1,duration:.4,ease:'expo.out'},0.1);
var c={v:100},n0=document.getElementById('i-n0');
tl.fromTo(c,{v:100},{v:7,duration:.85,ease:'power3.out',onUpdate:function(){n0.textContent=Math.round(c.v)}},0.6);
tl.fromTo('#i-fill',{scaleX:1},{scaleX:.07,duration:.85,ease:'power3.out'},0.6);
tl.fromTo('#i-pc',{opacity:0},{opacity:1,duration:.2},0.55);
tl.set('#i-x',{opacity:0},0);
slam(tl,'#i-x',1.5,1.5);shake(tl,'#i-kin',1.52,20,6);
tl.to('#i-kin',{opacity:0,scale:.9,filter:'blur(12px)',duration:.25,ease:'power3.in'},2.0);
tl.set('#i-end',{opacity:0},0);
tl.to('#i-end',{opacity:1,duration:.3},2.1);
tl.fromTo('#i-logo',{scale:1.2,filter:'blur(12px)'},{scale:1,filter:'blur(0px)',duration:.8,ease:'expo.out',immediateRender:false},2.1);
tl.fromTo(['#i-g','#i-n'],{y:120,opacity:0},{y:0,opacity:1,duration:.7,stagger:.1,ease:'expo.out',immediateRender:false},2.2);
tl.fromTo('#i-cta span',{opacity:0,y:30},{opacity:1,y:0,duration:.5,ease:'expo.out',immediateRender:false},2.3);
tl.fromTo('#i-sub',{opacity:0},{opacity:1,duration:.4,immediateRender:false},2.35);
""")

# ------------------------------------------------ CHROME
chap = [(0,"","Tip isteri"),(5.3,"01","Badan"),(7.25,"02","Pakaian"),(9.7,"03","Rutin"),(13.3,"","Ingat"),(15.4,"","Solusi"),(22.45,"","Ringkasan"),(25.6,"","Checkout"),(29.2,"","Sekarang")]
chap_js = ""
for i,(t,n,l) in enumerate(chap):
    lab = f"{n} / {l}" if n else l
    chap_js += f"tl.set('#ch',{{textContent:'{lab}'}},{t});tl.fromTo('#ch',{{opacity:0,y:-10}},{{opacity:1,y:0,duration:.35,ease:'expo.out',immediateRender:{'true' if i==0 else 'false'}}},{t});"
scene("chrome", TOTAL, """
#br{left:70px;top:184px;font-size:28px;letter-spacing:.5em;font-weight:500;color:rgba(244,238,230,.75)}
#ch{right:70px;top:180px;font-size:28px;letter-spacing:.32em;text-transform:uppercase;color:rgba(244,238,230,.75);text-align:right}
#pg{left:70px;top:1360px;width:940px;height:2px;background:rgba(244,238,230,.12)}
#pgf{width:100%;height:100%;background:#d8b77a;transform-origin:left center}
#big{right:40px;top:1340px;font-size:520px;line-height:1;color:transparent;-webkit-text-stroke:2px rgba(216,183,122,.16);font-weight:500}
#gr{background:url('assets/img/grain.png');opacity:.07;mix-blend-mode:overlay}
#vg{background:radial-gradient(ellipse at 50% 45%,transparent 55%,rgba(0,0,0,.45) 100%)}
""", """
<div id="vg" class="full"></div>
<div id="gr" class="full"></div>
<div id="br" class="abs">FRESCURA BODY</div>
<div id="ch" class="abs">Tip isteri</div>
<div id="pg" class="abs"><div id="pgf"></div></div>
<div id="big" class="abs it" data-layout-ignore>3</div>
""", chap_js + f"""
tl.set('#big',{{textContent:'3'}},0);tl.set('#big',{{textContent:'1'}},5.3);tl.set('#big',{{textContent:'2'}},7.25);tl.set('#big',{{textContent:'3'}},9.7);
tl.fromTo('#big',{{opacity:1}},{{opacity:0,duration:.3}},13.3);
tl.fromTo('#pgf',{{scaleX:0}},{{scaleX:1,duration:{TOTAL},ease:'none'}},0);
tl.fromTo('#gr',{{backgroundPosition:'0px 0px'}},{{backgroundPosition:'512px 1536px',duration:{TOTAL},ease:'steps({int(TOTAL*15)})'}},0);
tl.to(['#br','#ch'],{{color:'rgba(13,11,10,.8)',duration:.2}},22.45);tl.to(['#br','#ch'],{{color:'rgba(244,238,230,.75)',duration:.2}},25.6);
tl.to('#vg',{{opacity:.35,duration:.2}},22.45);tl.to('#vg',{{opacity:1,duration:.2}},25.6);
tl.to(['#br','#ch','#pg'],{{opacity:0,duration:.4}},31.2);
""")

# ------------------------------------------------ CAPTIONS (voice times; corrected spelling)
WORDS = """Korang .00 0|nak .30 0|suami .48 1|/sentiasa .80 0|selesa, 1.32 1|/dekat 1.96 1|dengan 2.34 0|korang? 2.56 0|/Jangan 3.00 0|abaikan 3.44 1|/3 3.98 1|perkara 4.24 0|ini. 4.54 0|
/Yang 5.10 0|pertama, 5.20 1|/jaga 5.88 0|kebersihan 6.18 1|badan. 6.58 0|/Yang 7.04 0|kedua, 7.12 1|/pastikan 7.64 0|pakaian 8.04 1|/sentiasa 8.50 0|bersih. 8.98 1|
/Dan 9.50 0|yang 9.62 0|ketiga, 9.80 1|/amalkan 10.30 0|rutin 10.82 1|/penjagaan 11.32 0|diri 11.80 1|/yang 12.00 0|konsisten. 12.22 1|
/Nampak 13.08 0|mudah, 13.32 1|/tapi 13.74 0|ramai 13.92 0|yang 14.26 0|/terlepas 14.36 1|pandang. 14.66 1|
/So, 15.18 0|untuk 15.66 0|rutin 15.84 0|/mandi 16.10 1|harian 16.36 0|korang, 16.66 0|/pastinya 17.24 0|/Frescura 17.62 1|Body 18.14 1|/dengan 18.36 0|buih 18.62 1|yang 18.78 0|lembut 18.90 1|/terus 19.32 0|daripada 19.44 0|botol, 19.82 1|/dan 20.16 0|pilihan 20.30 0|wangian 20.56 1|/Bombshell 21.00 1|serta 21.24 0|/Midnight 21.52 1|Fantasy. 21.82 1|
/Kalau 22.28 0|dah 22.46 0|tahu 22.72 0|/3 22.92 1|perkara 23.24 0|ini, 23.58 0|/jangan 24.18 0|sekadar 24.38 0|/dengar 24.80 1|sahaja. 25.04 0|
/Tekan 25.46 0|beg 25.60 1|kuning 25.82 1|/dan 26.00 0|masukkan 26.16 0|/Frescura 26.78 1|Body 27.18 1|/dalam 27.36 0|troli, 27.62 1|/dan 28.08 0|checkout 28.48 1|sekarang 28.82 0|/sebab 29.18 0|stok 29.59 1|/sangat 29.93 0|terhad. 30.46 1"""
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
    nxt = groups[gi+1][0][1] - 0.06 if gi+1 < len(groups) else 31.25
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

# ------------------------------------------------ ROOT
hosts = [("a",0,5.3,10),("b",5.3,1.95,11),("c",7.25,2.45,12),("d",9.7,3.6,13),("e",13.3,2.1,14),("s5",15.4,7.05,15),("pump",18.6,1.9,16),("g",22.45,3.15,17),("h",25.6,3.6,18),("i",29.2,4.4,19)]
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
print("groups", len(groups))
