from common import scene
from mall import mall_css, mall_svg, bokeh_js

# local 0 = 17.30. kalau .04, pengalaman .56, mandi .96, menyenangkan 1.78,
# pastinya 2.42, fresh 2.96, body 3.60 ; ends 4.00
P = 'm'
CSS = mall_css(P) + """
#m-k1{position:absolute;left:0;right:0;top:930px;text-align:center;}
#m-k1 .a{font-family:var(--sans);font-weight:600;font-size:34px;letter-spacing:.4em;padding-left:.4em;color:var(--gold);}
#m-k1 .b{font-family:var(--serif);font-style:italic;font-weight:400;font-size:68px;line-height:1.05;margin-top:16px;color:var(--ink);}
#m-logo{position:absolute;left:290px;top:300px;width:500px;height:500px;mix-blend-mode:screen;}
#m-logo img{width:100%;height:100%;}
#m-podL{left:110px;top:1210px;} #m-podR{left:640px;top:1210px;}
#m-bL{left:157px;top:620px;} #m-bR{left:687px;top:620px;}
#m-hL{left:15px;top:640px;background:radial-gradient(circle,rgba(200,38,58,.55),rgba(200,38,58,0) 70%);}
#m-hR{left:545px;top:640px;background:radial-gradient(circle,rgba(108,79,209,.6),rgba(108,79,209,0) 70%);}
#m-cL{left:15px;} #m-cR{left:545px;}
#m-flash{position:absolute;inset:0;background:radial-gradient(circle at 50% 45%,#fff6dc 0%,rgba(255,240,200,0) 60%);opacity:0;}
#m-sweep{position:absolute;top:0;left:-400px;width:300px;height:1920px;background:linear-gradient(90deg,rgba(255,240,200,0),rgba(255,240,200,.22),rgba(255,240,200,0));clip-path:polygon(30% 0,100% 0,70% 100%,0 100%);}
"""

BODY = f"""
    <div id="m-world">
      {mall_svg(P)}
      <div id="m-sign" class="goldtxt">FRESCURA</div>
      <div id="m-signsub">BODY &nbsp;·&nbsp; BOUTIQUE</div>
      <div id="m-hL" class="m-halo"></div><div id="m-hR" class="m-halo"></div>
      <div id="m-cL" class="m-cone"></div><div id="m-cR" class="m-cone"></div>
      <div id="m-podL" class="m-pod"><div class="side"></div><div class="top"></div><div class="band"></div></div>
      <div id="m-podR" class="m-pod"><div class="side"></div><div class="top"></div><div class="band"></div></div>
      <div id="m-bL" class="m-btl"><img src="assets/img/bomb_cut.png"><img class="refl" src="assets/img/bomb_cut.png"></div>
      <div id="m-bR" class="m-btl"><img src="assets/img/noche_cut.png"><img class="refl" src="assets/img/noche_cut.png"></div>
    </div>
    <div id="m-k1"><div class="a">PENGALAMAN MANDI</div><div class="b">yang lebih <span class="goldtxt">menyenangkan</span></div></div>
    <div id="m-logo"><img src="assets/img/logo.jpg"></div>
    <div id="m-sweep"></div>
    <div id="m-flash"></div>
"""

JS = bokeh_js(P, 22, 4.0) + """
    // dolly in down the mall
    tl.fromTo('#m-world',{scale:1.55,y:-120,opacity:0},{scale:1.0,y:0,opacity:1,duration:2.6,ease:'expo.out'},0);
    tl.fromTo('#m-world',{rotation:-1.5},{rotation:0,duration:2.6,ease:'power2.out'},0);
    tl.fromTo('#m-k1 .a',{opacity:0},{opacity:1,duration:0.6,ease:'power3.out'},0.5);
    tl.fromTo('#m-k1 .b',{opacity:0,y:30,filter:'blur(10px)'},{opacity:1,y:0,filter:'blur(0px)',duration:0.5,ease:'expo.out'},1.0);
    tl.to('#m-k1',{opacity:0,y:-30,duration:0.25,ease:'power2.in'},2.55);
    tl.fromTo('#m-sign',{opacity:.35},{opacity:1,duration:0.2},2.9);
    tl.fromTo('#m-sign',{backgroundPosition:'0% 50%'},{backgroundPosition:'100% 50%',duration:1.2,ease:'sine.inOut'},2.9);
    // podiums + bottles rise at "Frescura"
    tl.fromTo(['#m-podL','#m-podR'],{y:260,opacity:0},{y:0,opacity:1,duration:0.5,ease:'expo.out',stagger:0.06},2.45);
    tl.fromTo('#m-bL',{y:340,opacity:0,scale:.9},{y:0,opacity:1,scale:1,duration:0.55,ease:'back.out(1.3)'},2.92);
    tl.fromTo('#m-bR',{y:340,opacity:0,scale:.9},{y:0,opacity:1,scale:1,duration:0.55,ease:'back.out(1.3)'},3.02);
    tl.fromTo(['#m-hL','#m-hR'],{opacity:0,scale:.6},{opacity:1,scale:1,duration:0.6,ease:'power2.out'},2.95);
    tl.fromTo(['#m-cL','#m-cR'],{opacity:0,scaleX:.4},{opacity:1,scaleX:1,duration:0.35,ease:'power2.out'},2.92);
    tl.fromTo('#m-cL',{rotation:-6},{rotation:4,duration:1.1,ease:'sine.inOut'},2.92);
    tl.fromTo('#m-cR',{rotation:6},{rotation:-4,duration:1.1,ease:'sine.inOut'},2.92);
    tl.fromTo('#m-flash',{opacity:0},{opacity:.85,duration:0.06},2.94);
    tl.to('#m-flash',{opacity:0,duration:0.5,ease:'power2.out'},3.0);
    // neon logo pops over the storefront
    tl.fromTo('#m-logo',{opacity:0,scale:.3},{opacity:1,scale:.62,y:-110,duration:0.4,ease:'back.out(1.8)'},2.96);
    tl.fromTo('#m-logo',{filter:'brightness(1)'},{keyframes:{filter:['brightness(1.8)','brightness(.7)','brightness(1.5)','brightness(1)']},duration:0.35,ease:'none'},3.0);
    tl.fromTo('#m-sweep',{x:0},{x:1900,duration:0.8,ease:'power2.inOut'},3.2);
    tl.fromTo('#m-world',{scale:1.0},{scale:1.04,duration:1.0,ease:'sine.out'},3.0);
"""

def build():
    return scene('mall', CSS, BODY, JS)
