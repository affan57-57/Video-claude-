 BOUTIQUE 19.28 - 24.6
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

