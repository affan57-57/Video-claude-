from common import scene

# local 0 = 11.75 s. terutamanya .05, bahagian .79, mudah 1.49, berpeluh 1.75,
# mandi 2.21, betul 2.89, bersihkan 3.41, ketiak 4.47, setiap 4.93, hari 5.23 ; ends 5.55
CSS = """
#z-kick{top:230px;}
#z-body{position:absolute;left:190px;top:330px;width:700px;height:760px;overflow:visible;}
#z-body path{fill:none;stroke:rgba(246,239,228,.85);stroke-width:5;stroke-linecap:round;stroke-linejoin:round;}
.hot{position:absolute;width:120px;height:120px;margin:-60px 0 0 -60px;border-radius:50%;
  background:radial-gradient(circle,rgba(255,107,122,.85) 0%,rgba(200,38,58,.35) 40%,rgba(200,38,58,0) 70%);}
.hring{position:absolute;width:120px;height:120px;margin:-60px 0 0 -60px;border-radius:50%;border:3px solid var(--rose-hi);}
.zl{position:absolute;font-family:var(--sans);font-weight:800;font-size:40px;letter-spacing:.14em;color:var(--ink);}
.zl i{display:block;width:150px;height:2px;background:var(--gold);margin-top:8px;transform-origin:0 50%;}
#z-big{position:absolute;left:0;right:0;top:1000px;text-align:center;font-family:var(--serif);font-style:italic;font-weight:900;font-size:104px;line-height:1;}
#z-vid{position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover;}
#z-shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(8,6,5,.78) 0%,rgba(8,6,5,.15) 34%,rgba(8,6,5,.1) 55%,rgba(8,6,5,.72) 100%);}
#z-dark{position:absolute;inset:0;background:radial-gradient(120% 70% at 50% 40%,#1d2a2c 0%,#0c1213 55%,#060808 100%);opacity:0;}
#z-rain{position:absolute;inset:0;}
.drop{position:absolute;width:4px;border-radius:3px;background:linear-gradient(180deg,rgba(200,240,255,0),rgba(220,245,255,.75));}
#z-list{position:absolute;left:110px;right:110px;top:250px;padding:40px 48px;}
.chk{display:flex;align-items:center;gap:30px;height:116px;}
.chk .box{width:76px;height:76px;flex:0 0 76px;border-radius:50%;border:3px solid var(--gold);display:flex;align-items:center;justify-content:center;}
.chk .box svg{width:44px;height:44px;}
.chk .box path{fill:none;stroke:#1a130d;stroke-width:8;stroke-linecap:round;stroke-linejoin:round;}
.chk .fill{position:absolute;width:76px;height:76px;border-radius:50%;background:linear-gradient(135deg,#fff0c9,#c99d5c);}
.chk .tx{font-family:var(--sans);font-weight:800;font-size:50px;letter-spacing:.02em;line-height:1.05;}
.chk .tx small{display:block;font-family:var(--serif);font-style:italic;font-weight:400;font-size:34px;color:var(--gold-hi);letter-spacing:0;margin-top:6px;}
"""

BODY = """
    <div class="bg-noir"></div>
    <div id="z-a" class="full">
      <div id="z-kick" class="kicker center-x">Zon mudah berpeluh</div>
      <svg id="z-body" viewBox="0 0 700 760">
        <path pathLength="1" d="M350 40 C300 40 270 80 270 130 C270 185 305 225 350 225 C395 225 430 185 430 130 C430 80 400 40 350 40 Z"/>
        <path pathLength="1" d="M310 225 L305 270 C230 285 180 300 150 340 C120 380 110 470 100 560 C95 610 90 680 92 740"/>
        <path pathLength="1" d="M390 225 L395 270 C470 285 520 300 550 340 C580 380 590 470 600 560 C605 610 610 680 608 740"/>
        <path pathLength="1" d="M205 420 C215 520 220 640 215 760"/>
        <path pathLength="1" d="M495 420 C485 520 480 640 485 760"/>
        <path pathLength="1" d="M305 270 C320 300 380 300 395 270"/>
      </svg>
      <div class="hot" id="z-h1" style="left:385px;top:790px"></div><div class="hring" id="z-r1" style="left:385px;top:790px"></div>
      <div class="hot" id="z-h2" style="left:695px;top:790px"></div><div class="hring" id="z-r2" style="left:695px;top:790px"></div>
      <div class="hot" id="z-h3" style="left:540px;top:600px"></div><div class="hring" id="z-r3" style="left:540px;top:600px"></div>
      <div class="zl" id="z-l1" style="left:90px;top:860px">KETIAK<i></i></div>
      <div class="zl" id="z-l2" style="left:770px;top:860px">KETIAK<i></i></div>
      <div class="zl" id="z-l3" style="left:600px;top:470px">LEHER<i></i></div>
      <div id="z-big" class="goldtxt">Mudah Berpeluh</div>
    </div>
    <video id="z-vid" class="clip" data-start="2.15" data-duration="2.3" data-track-index="2" muted playsinline src="assets/video/foam_lather.mp4"></video>
    <div id="z-dark"></div>
    <div id="z-rain" class="full"></div>
    <div id="z-shade"></div>
    <div id="z-list" class="glass">
      <div class="chk" id="z-c1"><span class="box"><span class="fill"></span><svg viewBox="0 0 44 44" style="position:relative"><path pathLength="1" d="M8 23 L18 33 L37 11"/></svg></span>
        <span class="tx">MANDI DENGAN BETUL<small>sabun seluruh badan, bilas bersih</small></span></div>
      <div class="chk" id="z-c2"><span class="box"><span class="fill"></span><svg viewBox="0 0 44 44" style="position:relative"><path pathLength="1" d="M8 23 L18 33 L37 11"/></svg></span>
        <span class="tx">BERSIHKAN KETIAK<small>setiap hari, tanpa skip</small></span></div>
    </div>
"""

JS = """
    tl.fromTo('#z-kick',{opacity:0,y:-16},{opacity:1,y:0,duration:0.4,ease:'power3.out'},0.0);
    tl.fromTo('#z-body path',{strokeDasharray:1,strokeDashoffset:1},{strokeDashoffset:0,duration:0.8,ease:'power2.inOut',stagger:0.05},0.0);
    [['#z-h1','#z-r1',0.75],['#z-h2','#z-r2',0.85],['#z-h3','#z-r3',1.45]].forEach(([h,r,at])=>{
      tl.fromTo(h,{scale:0,opacity:0},{scale:1,opacity:1,duration:0.35,ease:'back.out(2)'},at);
      tl.fromTo(h,{scale:1},{scale:1.25,duration:0.35,yoyo:true,repeat:3,ease:'sine.inOut'},at+0.35);
      tl.fromTo(r,{scale:.6,opacity:0},{scale:2.4,keyframes:{opacity:[0,.9,0]},duration:0.9,ease:'sine.out'},at);
    });
    [['#z-l1',0.8],['#z-l2',0.9],['#z-l3',1.5]].forEach(([l,at])=>{
      tl.fromTo(l,{opacity:0,y:14},{opacity:1,y:0,duration:0.3,ease:'power3.out'},at);
      tl.fromTo(l+' i',{scaleX:0},{scaleX:1,duration:0.4,ease:'power3.out'},at+0.05);
    });
    tl.fromTo('#z-big',{opacity:0,scale:.9},{opacity:1,scale:1,duration:0.4,ease:'expo.out'},1.72);
    tl.to('#z-a',{opacity:0,scale:1.08,duration:0.16,ease:'power2.in'},2.0);
    // lather b-roll (2.15-4.45): slow push-in
    tl.fromTo('#z-vid',{scale:1.12},{scale:1.0,duration:2.3,ease:'power1.out'},2.15);
    tl.fromTo('#z-shade',{opacity:0},{opacity:1,duration:0.15},2.15);
    tl.fromTo('#z-list',{y:-60,opacity:0},{y:0,opacity:1,duration:0.4,ease:'expo.out'},2.16);
    tl.fromTo('#z-c1',{opacity:.35},{opacity:1,duration:0.2},2.2);
    tl.fromTo('#z-c2',{opacity:.35},{opacity:.35,duration:0.01},2.2);
    [['#z-c1',2.80],['#z-c2',3.40]].forEach(([c,at])=>{
      tl.fromTo(c+' .fill',{scale:0},{scale:1,duration:0.25,ease:'back.out(2.5)'},at);
      tl.fromTo(c+' path',{strokeDasharray:1,strokeDashoffset:1},{strokeDashoffset:0,duration:0.25,ease:'power2.out'},at+0.08);
    });
    tl.to('#z-c2',{opacity:1,duration:0.2},3.38);
    // after the footage: dark shower glow + rain
    tl.fromTo('#z-dark',{opacity:0},{opacity:1,duration:0.12},4.42);
    (function(){ const box=$('#z-rain');
      for(let i=0;i<70;i++){ const d=document.createElement('div'); d.className='drop';
        const h=40+rnd()*90; d.style.height=h+'px'; d.style.left=(rnd()*1080)+'px'; d.style.top=(-200-rnd()*400)+'px'; box.appendChild(d);
        tl.fromTo(d,{y:0,opacity:0},{y:2400,opacity:.8,duration:0.9+rnd()*0.5,ease:'none'},4.42+rnd()*0.4);
      }})();
    tl.fromTo('#z-list',{scale:1},{scale:1.04,duration:1.0,ease:'sine.out'},4.45);
    tl.to('#z-list',{opacity:0,y:-40,duration:0.18,ease:'power2.in'},5.36);
"""

def build():
    return scene('zones', CSS, BODY, JS)
