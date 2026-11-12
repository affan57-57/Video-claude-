from common import scene, dust_js
from mall import mall_css, mall_svg, bokeh_js

# ---- dont wait: local 0 = 26.62. tunggu .72, orang 1.22, sebelah 1.70, tutup 2.16,
# hidung 2.50, baru 2.76, bertindak 3.24 ; ends 3.72
W_CSS = """
#w-t{position:absolute;left:0;right:0;top:250px;text-align:center;}
#w-t .a{font-family:var(--serif);font-style:italic;font-weight:900;font-size:170px;line-height:.95;}
#w-t .b{font-family:var(--sans);font-weight:800;font-size:56px;letter-spacing:.3em;padding-left:.3em;margin-top:22px;color:var(--ink);}
#w-scene{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:visible;}
#w-scene .ln{fill:none;stroke:var(--ink);stroke-width:7;stroke-linecap:round;stroke-linejoin:round;}
#w-scene .wv{fill:none;stroke:#b6d36a;stroke-width:6;stroke-linecap:round;stroke-dasharray:4 16;opacity:.9;}
#w-hand{fill:#17110e;stroke:var(--gold);stroke-width:6;stroke-linejoin:round;}
#w-ex{position:absolute;left:840px;top:610px;width:90px;height:90px;border-radius:50%;background:var(--rose);
  color:#fff;font-family:var(--sans);font-weight:800;font-size:64px;line-height:90px;text-align:center;box-shadow:0 0 40px rgba(255,107,122,.7);}
#w-act{position:absolute;left:0;right:0;top:1060px;text-align:center;}
#w-act span{display:inline-block;font-family:var(--sans);font-weight:800;font-size:64px;letter-spacing:.12em;color:#1a130d;
  padding:18px 46px 20px;border-radius:60px;background:linear-gradient(90deg,#c99d5c,#fff0c9,#d8b46e);box-shadow:0 20px 60px rgba(216,180,110,.35);}
#w-flash{position:absolute;inset:0;background:var(--rose);opacity:0;mix-blend-mode:screen;}
"""
W_BODY = """
    <div class="bg-noir"></div>
    <div id="w-dust" class="full"></div>
    <div id="w-t"><div class="a goldtxt">Jangan Tunggu</div><div class="b">SAMPAI&hellip;</div></div>
    <svg id="w-scene" viewBox="0 0 1080 1920">
      <g id="w-L">
        <path class="ln" pathLength="1" d="M300 640 C200 640 150 720 150 800 C150 880 190 930 240 950 L240 1010"/>
        <path class="ln" pathLength="1" d="M300 640 C380 640 420 690 430 750 L470 800 L432 812 C436 850 430 880 400 900 L360 905 L360 1010"/>
        <path class="ln" d="M380 735 L392 735"/>
      </g>
      <g id="w-R">
        <path class="ln" pathLength="1" d="M780 640 C880 640 930 720 930 800 C930 880 890 930 840 950 L840 1010"/>
        <path class="ln" pathLength="1" d="M780 640 C700 640 660 690 650 750 L610 800 L648 812 C644 850 650 880 680 900 L720 905 L720 1010"/>
        <path class="ln" id="w-eye" d="M690 735 C696 742 704 742 710 735"/>
      </g>
      <path class="wv" d="M470 780 C500 760 520 800 550 780 S600 760 620 790"/>
      <path class="wv" d="M460 820 C490 800 510 840 540 820 S590 800 612 828"/>
      <path class="wv" d="M470 860 C500 840 520 880 550 860 S600 840 620 866"/>
      <path id="w-hand" d="M560 760 C560 740 590 736 600 752 L640 760 C660 762 670 790 655 800 L640 845 C632 868 600 872 580 860 L560 840 Z"/>
    </svg>
    <div id="w-ex">!</div>
    <div id="w-act"><span>BERTINDAK SEKARANG</span></div>
    <div id="w-flash"></div>
"""
W_JS = dust_js('#w-dust', 20, 3.72, area=(40, 200, 1000, 1100)) + """
    tl.fromTo('#w-t .a',{scale:1.6,opacity:0,filter:'blur(16px)'},{scale:1,opacity:1,filter:'blur(0px)',duration:0.3,ease:'expo.out'},0.0);
    tl.fromTo('#w-t .a',{backgroundPosition:'0% 50%'},{backgroundPosition:'100% 50%',duration:3.7,ease:'none'},0);
    tl.fromTo('#w-t .b',{opacity:0,y:20},{opacity:1,y:0,duration:0.3,ease:'power3.out'},1.06);
    tl.fromTo('#w-L .ln',{strokeDasharray:1,strokeDashoffset:1},{strokeDashoffset:0,duration:0.5,ease:'power2.out'},1.18);
    tl.fromTo('#w-R .ln',{strokeDasharray:1,strokeDashoffset:1},{strokeDashoffset:0,duration:0.5,ease:'power2.out'},1.62);
    tl.fromTo('#w-scene .wv',{opacity:0,strokeDashoffset:80},{opacity:.9,strokeDashoffset:0,duration:1.6,ease:'none',stagger:0.08},1.75);
    tl.fromTo('#w-hand',{y:260,x:40,opacity:0},{y:0,x:0,opacity:1,duration:0.3,ease:'back.out(1.6)'},2.14);
    tl.fromTo('#w-R',{x:0},{keyframes:{x:[0,10,-8,6,0]},duration:0.3,ease:'none'},2.44);
    tl.fromTo('#w-ex',{scale:0,opacity:0},{scale:1,opacity:1,duration:0.25,ease:'back.out(3)'},2.48);
    tl.fromTo('#w-flash',{opacity:0},{keyframes:{opacity:[0,.22,0]},duration:0.3,ease:'none'},2.48);
    tl.to(['#w-scene','#w-ex'],{opacity:.25,duration:0.25},3.15);
    tl.fromTo('#w-act span',{scale:.6,opacity:0},{scale:1,opacity:1,duration:0.3,ease:'back.out(2)'},3.20);
    tl.to('#w-act span',{scale:.94,duration:0.08,yoyo:true,repeat:1},3.5);
"""

# ---- CTA: local 0 = 30.34. bekon .30, sekarang .72, check 1.32, frescura 1.82, stok 2.94,
# banyak 4.38, siapa 4.64, cepat 5.04, dapat 5.62 ; end card to 7.66
P = 'k'
K_CSS = mall_css(P) + """
#k-dim{position:absolute;inset:0;background:rgba(8,6,5,.55);}
#k-bL{left:180px;top:780px;width:200px;} #k-bR{left:700px;top:780px;width:200px;}
#k-podL{left:115px;top:1240px;} #k-podR{left:635px;top:1240px;}
#k-cart{position:absolute;left:0;right:0;top:300px;height:640px;}
#k-basket{position:absolute;left:390px;top:30px;width:300px;height:300px;overflow:visible;}
#k-tapR{position:absolute;left:470px;top:110px;width:140px;height:140px;border-radius:50%;border:5px solid #ffd21f;}
#k-finger{position:absolute;left:600px;top:200px;width:150px;height:190px;overflow:visible;}
#k-l1{position:absolute;left:0;right:0;top:360px;text-align:center;font-family:var(--sans);font-weight:800;font-size:70px;letter-spacing:.04em;}
#k-l1 .y{color:#1a1200;background:#ffd21f;padding:2px 22px 6px;border-radius:14px;}
#k-btn{position:absolute;left:0;right:0;top:480px;text-align:center;}
#k-btn span{display:inline-block;font-family:var(--sans);font-weight:800;font-size:46px;letter-spacing:.2em;padding:24px 56px 26px 66px;
  border-radius:70px;color:#1a130d;background:linear-gradient(90deg,#c99d5c,#fff0c9,#d8b46e);box-shadow:0 18px 50px rgba(216,180,110,.4);}
#k-stock{position:absolute;left:150px;right:150px;top:300px;padding:44px 50px;}
#k-stock .h{display:flex;justify-content:space-between;align-items:baseline;}
#k-stock .h b{font-family:var(--sans);font-weight:800;font-size:54px;letter-spacing:.14em;}
#k-stock .h i{font-family:var(--serif);font-style:italic;font-weight:900;font-size:78px;color:var(--rose-hi);font-variant-numeric:tabular-nums;}
#k-bar{margin-top:26px;height:26px;border-radius:13px;background:rgba(255,255,255,.08);border:1px solid rgba(216,180,110,.4);overflow:hidden;}
#k-fill{height:100%;width:100%;border-radius:13px;background:linear-gradient(90deg,#c8263a,#ff6b7a);transform-origin:0 50%;}
#k-stock .s{margin-top:22px;font-family:var(--sans);font-weight:600;font-size:32px;letter-spacing:.1em;color:var(--mute);}
#k-fast{position:absolute;left:0;right:0;top:330px;text-align:center;}
#k-fast .a{font-family:var(--serif);font-style:italic;font-weight:900;font-size:150px;line-height:.98;}
#k-end{position:absolute;left:0;right:0;top:250px;text-align:center;}
#k-logo{width:560px;height:560px;margin:0 auto;mix-blend-mode:screen;}
#k-logo img{width:100%;height:100%;}
#k-flash{position:absolute;inset:0;background:radial-gradient(circle at 50% 40%,#fff6dc,rgba(255,240,200,0) 60%);opacity:0;}
"""
K_BODY = f"""
    <div id="k-world">
      {mall_svg(P)}
      <div id="k-sign" class="goldtxt" style="position:absolute;left:0;right:0;top:470px;text-align:center;font-family:var(--serif);font-weight:700;font-size:58px;letter-spacing:.34em;padding-left:.34em;">FRESCURA</div>
      <div id="k-cL" class="k-cone" style="left:20px"></div><div id="k-cR" class="k-cone" style="left:540px"></div>
      <div id="k-podL" class="k-pod"><div class="side"></div><div class="top"></div><div class="band"></div></div>
      <div id="k-podR" class="k-pod"><div class="side"></div><div class="top"></div><div class="band"></div></div>
      <div id="k-bL" class="k-btl"><img src="assets/img/bomb_cut.png"><img class="refl" src="assets/img/bomb_cut.png"></div>
      <div id="k-bR" class="k-btl"><img src="assets/img/noche_cut.png"><img class="refl" src="assets/img/noche_cut.png"></div>
    </div>
    <div id="k-dim"></div>
    <div id="k-cart">
      <div id="k-tapR"></div>
      <svg id="k-basket" viewBox="0 0 300 300">
        <path d="M60 120 L240 120 L216 250 C214 262 206 268 194 268 L106 268 C94 268 86 262 84 250 Z" fill="#ffd21f"/>
        <path d="M100 120 C100 60 200 60 200 120" fill="none" stroke="#ffd21f" stroke-width="18" stroke-linecap="round"/>
        <path d="M110 160 L110 230 M150 160 L150 230 M190 160 L190 230" stroke="#1a1200" stroke-width="12" stroke-linecap="round"/>
      </svg>
      <svg id="k-finger" viewBox="0 0 150 190"><path d="M40 10 C52 10 58 18 58 30 L58 92 L70 86 C80 82 92 86 96 96 L108 92 C118 90 128 96 130 106 L138 104 C148 104 150 116 150 124 L146 160 C142 178 128 190 108 190 L70 190 C52 190 40 180 32 164 L6 110 C0 98 8 88 18 90 L24 92 L24 28 C24 18 30 10 40 10 Z" fill="#f6efe4" stroke="#1a130d" stroke-width="5"/></svg>
      <div id="k-l1">TEKAN <span class="y">BEG KUNING</span></div>
      <div id="k-btn"><span>CHECK OUT</span></div>
    </div>
    <div id="k-stock" class="glass">
      <div class="h"><b>STOK TERHAD</b><i id="k-pct">100%</i></div>
      <div id="k-bar"><div id="k-fill"></div></div>
      <div class="s">Siapa cepat, dia dapat.</div>
    </div>
    <div id="k-fast"><div class="a goldtxt">Siapa Cepat,</div><div class="a goldtxt">Dia Dapat.</div></div>
    <div id="k-end"><div id="k-logo"><img src="assets/img/logo.jpg"></div></div>
    <div id="k-flash"></div>
"""
K_JS = bokeh_js(P, 20, 7.66) + """
    tl.fromTo('#k-world',{scale:1.08},{scale:1.0,duration:7.6,ease:'sine.out'},0);
    tl.fromTo(['#k-cL','#k-cR'],{opacity:.6},{opacity:1,duration:0.4},0);
    // basket + tap
    tl.fromTo('#k-basket',{scale:0,rotation:-20,opacity:0},{scale:1,rotation:0,opacity:1,duration:0.35,ease:'back.out(2.2)'},0.0);
    tl.fromTo('#k-l1',{opacity:0,y:30},{opacity:1,y:0,duration:0.3,ease:'power3.out'},0.1);
    tl.fromTo('#k-finger',{x:160,y:160,opacity:0},{x:0,y:0,opacity:1,duration:0.3,ease:'power3.out'},0.08);
    tl.to('#k-finger',{x:-50,y:-50,scale:.9,duration:0.12,ease:'power2.in'},0.36);
    tl.to('#k-finger',{x:0,y:0,scale:1,duration:0.2,ease:'power2.out'},0.5);
    tl.fromTo('#k-basket',{scale:1},{keyframes:{scale:[1,.88,1.08,1]},duration:0.4,ease:'none'},0.46);
    tl.fromTo('#k-tapR',{scale:.5,opacity:0},{scale:2.6,keyframes:{opacity:[0,1,0]},duration:0.6,ease:'power2.out'},0.48);
    tl.to('#k-finger',{x:-50,y:-50,scale:.9,duration:0.1,ease:'power2.in'},1.2);
    tl.to('#k-finger',{x:0,y:0,scale:1,duration:0.2,ease:'power2.out'},1.3);
    tl.fromTo('#k-btn span',{scale:.6,opacity:0},{scale:1,opacity:1,duration:0.3,ease:'back.out(2)'},1.28);
    tl.fromTo('#k-btn span',{scale:1},{keyframes:{scale:[1,.9,1.05,1]},duration:0.35,ease:'none'},1.66);
    tl.fromTo('#k-btn span',{backgroundPosition:'0% 50%'},{backgroundPosition:'100% 50%',duration:1,ease:'none'},1.3);
    tl.to('#k-cart',{opacity:0,y:-40,duration:0.25,ease:'power2.in'},2.80);
    tl.fromTo('#k-sign',{opacity:1},{opacity:0,duration:0.3},0.0);
    // stock draining
    tl.fromTo('#k-stock',{opacity:0,y:60},{opacity:1,y:0,duration:0.35,ease:'expo.out'},2.90);
    const pct={v:100};
    tl.fromTo(pct,{v:100},{v:7,duration:1.6,ease:'power2.inOut',onUpdate:()=>{$('#k-pct').textContent=Math.round(pct.v)+'%';}},3.0);
    tl.fromTo('#k-fill',{scaleX:1},{scaleX:.07,duration:1.6,ease:'power2.inOut'},3.0);
    tl.fromTo('#k-stock',{x:0},{keyframes:{x:[0,-8,8,-5,0]},duration:0.25,ease:'none'},4.4);
    tl.to('#k-stock',{opacity:0,scale:.92,duration:0.2,ease:'power2.in'},4.58);
    // siapa cepat dia dapat
    tl.fromTo('#k-fast .a',{opacity:0,y:60,filter:'blur(14px)'},{opacity:1,y:0,filter:'blur(0px)',duration:0.35,ease:'expo.out',stagger:0.38},4.64);
    tl.fromTo('#k-fast .a',{backgroundPosition:'0% 50%'},{backgroundPosition:'100% 50%',duration:1.4,ease:'sine.inOut'},4.64);
    tl.fromTo('#k-flash',{opacity:0},{keyframes:{opacity:[0,.7,0]},duration:0.45,ease:'none'},4.62);
    tl.to('#k-dim',{opacity:.25,duration:0.6},4.7);
    tl.to('#k-fast',{opacity:0,y:-30,duration:0.25,ease:'power2.in'},6.0);
    // end card
    tl.fromTo('#k-logo',{opacity:0,scale:.6},{opacity:1,scale:1,duration:0.5,ease:'back.out(1.6)'},6.12);
    tl.fromTo('#k-logo',{filter:'brightness(1)'},{keyframes:{filter:['brightness(2)','brightness(.6)','brightness(1.6)','brightness(1)']},duration:0.4,ease:'none'},6.15);
    tl.fromTo(['#k-bL','#k-bR'],{y:0},{y:-14,duration:2.0,ease:'sine.inOut'},5.6);
"""

def build():
    return {'wait': scene('wait', W_CSS, W_BODY, W_JS), 'cta': scene('cta', K_CSS, K_BODY, K_JS)}
