from common import scene

# ---- foam: local 0 = 21.30, buih .08, lembut .44, terus .80, botol 1.38 ; ends 1.90
FOAM_CSS = """
#f-vid{position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover;}
#f-shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(8,6,5,.7) 0%,rgba(8,6,5,0) 30%,rgba(8,6,5,0) 58%,rgba(8,6,5,.72) 100%);}
#f-t{position:absolute;left:0;right:0;top:230px;text-align:center;}
#f-t .a{font-family:var(--serif);font-style:italic;font-weight:900;font-size:150px;line-height:1;color:#fff;text-shadow:0 10px 50px rgba(0,0,0,.45);}
#f-t .b{margin-top:14px;font-family:var(--sans);font-weight:800;font-size:44px;letter-spacing:.34em;padding-left:.34em;color:var(--gold-hi);}
#f-call{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:visible;}
#f-call path{fill:none;stroke:#fff0c9;stroke-width:3;}
#f-call circle{fill:#fff0c9;}
#f-tag{position:absolute;left:600px;top:640px;padding:14px 26px;border-radius:40px;background:rgba(12,9,7,.55);
  border:1.5px solid rgba(255,240,201,.7);font-family:var(--sans);font-weight:800;font-size:34px;letter-spacing:.12em;color:#fff6e4;}
"""
FOAM_BODY = """
    <video id="f-vid" class="clip" data-start="0" data-duration="1.9" data-track-index="2" muted playsinline src="assets/video/foam_pump.mp4" data-media-start="0.35"></video>
    <div id="f-shade"></div>
    <svg id="f-call" viewBox="0 0 1080 1920"><path id="f-line" pathLength="1" d="M470 930 L560 700 L600 700"/><circle id="f-dot" cx="470" cy="930" r="10"/></svg>
    <div id="f-tag">TERUS DARI BOTOL</div>
    <div id="f-t"><div class="a">Buih Lembut</div><div class="b">SOFT FOAM</div></div>
"""
FOAM_JS = """
    tl.fromTo('#f-vid',{scale:1.0},{scale:1.14,duration:1.9,ease:'none'},0);
    tl.fromTo('#f-t .a',{opacity:0,y:50,filter:'blur(12px)'},{opacity:1,y:0,filter:'blur(0px)',duration:0.4,ease:'expo.out'},0.05);
    tl.fromTo('#f-t .b',{opacity:0},{opacity:1,duration:0.5,ease:'power3.out'},0.4);
    tl.fromTo('#f-dot',{scale:0,transformOrigin:'50% 50%'},{scale:1,duration:0.2,ease:'back.out(3)'},0.76);
    tl.fromTo('#f-line',{strokeDasharray:1,strokeDashoffset:1},{strokeDashoffset:0,duration:0.3,ease:'power2.out'},0.8);
    tl.fromTo('#f-tag',{opacity:0,x:-30},{opacity:1,x:0,duration:0.3,ease:'expo.out'},1.0);
    tl.to('#f-root-fade',{},1.9);
"""

# ---- salt: local 0 = 23.20, garam .08, laut .52 ; ends 1.05
SALT_CSS = """
#s-bg{position:absolute;inset:0;background:radial-gradient(110% 70% at 50% 42%,#20323a 0%,#0d1519 55%,#050708 100%);}
.xtal{position:absolute;background:linear-gradient(135deg,rgba(255,255,255,.95),rgba(200,230,240,.55) 50%,rgba(255,255,255,.25));
  box-shadow:0 0 18px rgba(220,245,255,.6);border-radius:3px;}
#s-ring{position:absolute;left:240px;top:420px;width:600px;height:600px;border-radius:50%;border:2px solid rgba(220,245,255,.55);}
#s-ring2{position:absolute;left:290px;top:470px;width:500px;height:500px;border-radius:50%;border:1px dashed rgba(220,245,255,.4);}
#s-t{position:absolute;left:0;right:0;top:590px;text-align:center;}
#s-t .a{font-family:var(--sans);font-weight:800;font-size:40px;letter-spacing:.5em;padding-left:.5em;color:#cfeef7;}
#s-t .b{font-family:var(--serif);font-style:italic;font-weight:900;font-size:150px;line-height:1.05;margin-top:6px;
  background:linear-gradient(100deg,#9fc7d3,#ffffff 40%,#bfe3ee 60%,#ffffff 80%);background-size:200% 100%;-webkit-background-clip:text;background-clip:text;color:transparent;}
#s-t .c{font-family:var(--sans);font-weight:600;font-size:34px;letter-spacing:.12em;color:var(--mute);margin-top:10px;}
"""
SALT_BODY = """
    <div id="s-bg"></div>
    <div id="s-ring"></div><div id="s-ring2"></div>
    <div id="s-x" class="full"></div>
    <div id="s-t"><div class="a">OCEAN</div><div class="b">Garam Laut</div></div>
"""
SALT_JS = """
    (function(){ const box=$('#s-x');
      for(let i=0;i<46;i++){ const d=document.createElement('div'); d.className='xtal';
        const s=8+rnd()*30; d.style.width=s+'px'; d.style.height=s+'px';
        d.style.left=(rnd()*1080)+'px'; d.style.top=(-100-rnd()*700)+'px'; box.appendChild(d);
        tl.fromTo(d,{y:0,rotation:rnd()*90,opacity:.95},{y:1500+rnd()*500,rotation:200+rnd()*300,duration:1.05,ease:'power1.in'},0);
      }})();
    tl.fromTo('#s-ring',{scale:.5,opacity:0},{scale:1,opacity:1,duration:0.5,ease:'expo.out'},0);
    tl.fromTo('#s-ring2',{rotation:0},{rotation:90,duration:1.05,ease:'none'},0);
    tl.fromTo('#s-t .a',{opacity:0},{opacity:1,duration:0.45,ease:'power3.out'},0.02);
    tl.fromTo('#s-t .b',{opacity:0,scale:1.2,filter:'blur(14px)'},{opacity:1,scale:1,filter:'blur(0px)',duration:0.35,ease:'expo.out'},0.08);
    tl.fromTo('#s-t .b',{backgroundPosition:'0% 50%'},{backgroundPosition:'100% 50%',duration:1.0,ease:'none'},0.08);
    tl.fromTo('#s-t .c',{opacity:0},{opacity:1,duration:0.3},0.4);
"""

# ---- scents: local 0 = 24.25, pilihan .07, wangian .49, bombshell .93, serta 1.43, midnight 1.77 ; ends 2.37
SC_CSS = """
#c-bgL{position:absolute;left:0;top:0;width:540px;height:1920px;background:radial-gradient(90% 50% at 60% 45%,#5a1019 0%,#25080c 60%,#0b0405 100%);}
#c-bgR{position:absolute;left:540px;top:0;width:540px;height:1920px;background:radial-gradient(90% 50% at 40% 45%,#2c1f66 0%,#120c2c 60%,#05040c 100%);}
#c-split{position:absolute;left:539px;top:0;width:2px;height:1920px;background:linear-gradient(180deg,transparent,var(--gold),transparent);transform-origin:50% 0;}
#c-k{top:240px;}
#c-k2{position:absolute;left:0;right:0;top:290px;text-align:center;font-family:var(--serif);font-style:italic;font-size:76px;color:var(--ink);}
.c-b{position:absolute;top:400px;width:200px;}
.c-b img{width:100%;display:block;filter:drop-shadow(0 40px 50px rgba(0,0,0,.6));}
#c-bL{left:170px;} #c-bR{left:710px;}
.c-lab{position:absolute;top:1035px;width:540px;text-align:center;}
.c-lab .n{font-family:var(--serif);font-style:italic;font-weight:900;font-size:52px;line-height:1;white-space:nowrap;}
.c-lab .d{margin-top:10px;font-family:var(--sans);font-weight:600;font-size:28px;letter-spacing:.24em;color:var(--mute);}
#c-lL{left:0;} #c-lR{left:540px;}
.pet{position:absolute;width:34px;height:22px;border-radius:60% 0 60% 0;background:linear-gradient(135deg,#ff5b6e,#9e1020);}
.star{position:absolute;width:6px;height:6px;border-radius:50%;background:#fff;box-shadow:0 0 12px 3px rgba(185,163,255,.9);}
"""
SC_BODY = """
    <div id="c-bgL"></div><div id="c-bgR"></div><div id="c-split"></div>
    <div id="c-fx" class="full"></div>
    <div id="c-k" class="kicker center-x">Pilihan Wangian</div>
    <div id="c-k2">dua mood, satu mewah</div>
    <div id="c-bL" class="c-b"><img src="assets/img/bomb_cut.png"></div>
    <div id="c-bR" class="c-b"><img src="assets/img/noche_cut.png"></div>
    <div id="c-lL" class="c-lab"><div class="n" style="color:#ff8a97">Bombshell</div><div class="d">ROSE &middot; BERANI</div></div>
    <div id="c-lR" class="c-lab"><div class="n" style="color:#c9b8ff">Midnight Fantasy</div><div class="d">NOCHE &middot; MISTERI</div></div>
"""
SC_JS = """
    tl.fromTo('#c-split',{scaleY:0},{scaleY:1,duration:0.4,ease:'power3.out'},0);
    tl.fromTo('#c-bgL',{x:-540},{x:0,duration:0.45,ease:'expo.out'},0);
    tl.fromTo('#c-bgR',{x:540},{x:0,duration:0.45,ease:'expo.out'},0);
    tl.fromTo('#c-k',{opacity:0,y:-14},{opacity:1,y:0,duration:0.35,ease:'power3.out'},0.07);
    tl.fromTo('#c-k2',{opacity:0,y:20},{opacity:1,y:0,duration:0.35,ease:'power3.out'},0.45);
    tl.fromTo('#c-bL',{x:-420,opacity:0,rotation:-10},{x:0,opacity:1,rotation:0,duration:0.5,ease:'expo.out'},0.88);
    tl.fromTo('#c-lL',{opacity:0,y:30},{opacity:1,y:0,duration:0.35,ease:'power3.out'},0.95);
    tl.fromTo('#c-bR',{x:420,opacity:0,rotation:10},{x:0,opacity:1,rotation:0,duration:0.5,ease:'expo.out'},1.72);
    tl.fromTo('#c-lR',{opacity:0,y:30},{opacity:1,y:0,duration:0.35,ease:'power3.out'},1.79);
    tl.fromTo(['#c-bL','#c-bR'],{y:0},{y:-18,duration:1.4,ease:'sine.inOut'},0.95);
    (function(){ const box=$('#c-fx');
      for(let i=0;i<22;i++){ const p=document.createElement('div'); p.className='pet';
        p.style.left=(rnd()*500)+'px'; p.style.top=(-60-rnd()*300)+'px'; box.appendChild(p);
        tl.fromTo(p,{y:0,x:0,rotation:rnd()*180,opacity:0},{y:1300+rnd()*700,x:(rnd()-.5)*160,rotation:360+rnd()*360,opacity:1,duration:1.5,ease:'none'},0.9+rnd()*0.2);
      }
      for(let i=0;i<40;i++){ const s=document.createElement('div'); s.className='star';
        s.style.left=(560+rnd()*500)+'px'; s.style.top=(160+rnd()*1150)+'px'; box.appendChild(s);
        tl.fromTo(s,{scale:0,opacity:0},{scale:1+rnd(),opacity:1,duration:0.2,ease:'power2.out'},1.74+rnd()*0.4);
        tl.to(s,{opacity:.3,duration:0.2,ease:'sine.inOut'},2.05+rnd()*0.2);
      }})();
"""

def build():
    return {
        'foam': scene('foam', FOAM_CSS, FOAM_BODY, FOAM_JS.replace("    tl.to('#f-root-fade',{},1.9);\n", "")),
        'salt': scene('salt', SALT_CSS, SALT_BODY, SALT_JS),
        'scents': scene('scents', SC_CSS, SC_BODY, SC_JS),
    }
