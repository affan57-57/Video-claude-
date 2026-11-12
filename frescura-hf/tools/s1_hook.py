from common import scene, dust_js

CSS = """
#h-world{position:absolute;inset:0;}
#h-glow{position:absolute;left:140px;top:260px;width:800px;height:800px;border-radius:50%;
  background:radial-gradient(circle,rgba(216,180,110,.26) 0%,rgba(216,180,110,0) 65%);}
#h-title{position:absolute;left:0;right:0;top:250px;height:900px;}
#h-onion{position:absolute;left:390px;top:40px;width:300px;height:330px;overflow:visible;}
#h-onion path{fill:none;stroke:url(#h-gg);stroke-width:5;stroke-linecap:round;stroke-linejoin:round;}
#h-onion .wave{stroke:#e9cf98;stroke-width:4;opacity:.85;}
#h-k1{position:absolute;left:0;right:0;top:390px;text-align:center;font-family:var(--serif);font-style:italic;
  font-weight:900;font-size:236px;line-height:1;letter-spacing:-.01em;}
#h-k2{position:absolute;left:0;right:0;top:640px;text-align:center;font-family:var(--sans);font-weight:800;
  font-size:104px;letter-spacing:.04em;line-height:1;color:var(--ink);}
#h-k2 .em{position:relative;display:inline-block;}
#h-ul{position:absolute;left:0;right:0;bottom:-22px;height:8px;border-radius:4px;
  background:linear-gradient(90deg,#8a6534,#fff0c9,#c99d5c);transform-origin:0 50%;}
#h-kick{top:205px;}
.ring{position:absolute;left:390px;top:420px;width:300px;height:300px;border-radius:50%;
  border:3px solid rgba(233,207,152,.7);}
#h-nose{position:absolute;left:640px;top:740px;width:300px;height:300px;overflow:visible;}
#h-nose path{fill:none;stroke:var(--ink);stroke-width:7;stroke-linecap:round;stroke-linejoin:round;}
#h-trail{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:visible;}
#h-trail path{fill:none;stroke:#e9cf98;stroke-width:5;stroke-linecap:round;stroke-dasharray:2 18;}
#h-stamp{position:absolute;left:0;right:0;top:960px;text-align:center;}
#h-stamp span{display:inline-block;font-family:var(--sans);font-weight:800;font-size:92px;letter-spacing:.06em;
  color:var(--rose-hi);border:6px solid var(--rose-hi);border-radius:18px;padding:10px 34px 14px;
  background:rgba(200,38,58,.14);box-shadow:0 0 60px rgba(255,107,122,.35);}
#h-flash{position:absolute;inset:0;background:#fff3d6;opacity:0;}
"""

BODY = """
    <div id="h-bg" class="bg-noir"></div>
    <div id="h-world">
      <div id="h-glow"></div>
      <div id="h-dust" class="full"></div>
      <div class="ring" id="h-r1"></div><div class="ring" id="h-r2"></div><div class="ring" id="h-r3"></div>
      <div id="h-kick" class="kicker center-x">&#9888; Amaran</div>
      <div id="h-title">
        <svg id="h-onion" viewBox="0 0 300 330">
          <defs><linearGradient id="h-gg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stop-color="#fff0c9"/><stop offset=".5" stop-color="#d8b46e"/><stop offset="1" stop-color="#8a6534"/></linearGradient></defs>
          <path class="on" pathLength="1" d="M150 120 C150 120 160 150 205 178 C262 214 270 282 222 312 C192 330 108 330 78 312 C30 282 38 214 95 178 C140 150 150 120 150 120 Z"/>
          <path class="on" pathLength="1" d="M150 126 C128 170 112 230 122 318"/>
          <path class="on" pathLength="1" d="M150 126 C172 170 188 230 178 318"/>
          <path class="on" pathLength="1" d="M150 120 L150 92 M150 100 C140 88 132 84 124 84 M150 100 C160 88 168 84 176 84"/>
          <path class="wave" pathLength="1" d="M92 100 C76 80 108 66 92 46 S76 14 92 -6"/>
          <path class="wave" pathLength="1" d="M210 100 C194 80 226 66 210 46 S194 14 210 -6"/>
          <path class="wave" pathLength="1" d="M150 60 C134 40 166 26 150 6 S134 -26 150 -46"/>
        </svg>
        <div id="h-k1" class="goldtxt">Ketiak</div>
        <div id="h-k2">BAU <span class="em">BAWANG?<i id="h-ul"></i></span></div>
      </div>
      <svg id="h-trail" viewBox="0 0 1080 1920"><path id="h-tp" d="M540 520 C700 560 640 700 760 840"/></svg>
      <svg id="h-nose" viewBox="0 0 300 300">
        <path d="M200 20 C190 80 150 140 110 196 C96 216 112 236 140 232 L178 226"/>
        <path d="M150 210 C160 202 174 204 178 214"/>
        <path d="M210 262 C190 276 160 280 140 274"/>
      </svg>
      <div id="h-stamp"><span id="h-stamp-in">TERHIDU!</span></div>
    </div>
    <div id="h-flash"></div>
"""

JS = dust_js('#h-dust', 34, 6.0, area=(60, 200, 960, 1200)) + """
    // frame 0 is the hook: title already on screen, settling in
    tl.fromTo('#h-k1',{scale:1.12,opacity:1,y:0},{scale:1,duration:0.9,ease:'expo.out'},0);
    tl.fromTo('#h-k2',{y:24,opacity:1},{y:0,opacity:1,duration:0.6,ease:'power3.out'},0.0);
    tl.fromTo('#h-k1',{backgroundPosition:'0% 50%'},{backgroundPosition:'100% 50%',duration:6,ease:'none'},0);
    tl.fromTo('#h-ul',{scaleX:0},{scaleX:1,duration:0.5,ease:'power3.inOut'},0.35);
    tl.fromTo('#h-onion .on',{strokeDashoffset:1,strokeDasharray:1},{strokeDashoffset:0,duration:0.9,ease:'power2.out',stagger:0.08},0);
    tl.fromTo('#h-onion .wave',{strokeDashoffset:1,strokeDasharray:1,opacity:0},{strokeDashoffset:0,opacity:.85,duration:0.7,ease:'sine.out',stagger:0.12},0.5);
    tl.fromTo('#h-onion .wave',{y:0},{y:-26,duration:5,ease:'sine.inOut'},0.5);
    tl.fromTo('#h-glow',{scale:.8,opacity:.6},{scale:1.15,opacity:1,duration:6,ease:'sine.inOut'},0);
    tl.fromTo('#h-kick',{opacity:0,y:-16},{opacity:1,y:0,duration:0.6,ease:'power2.out'},0.15);
    // "ketiak" punch (0.98)
    tl.fromTo('#h-flash',{opacity:0},{opacity:.28,duration:0.05},0.96);
    tl.to('#h-flash',{opacity:0,duration:0.3,ease:'power2.out'},1.01);
    tl.fromTo('#h-title',{scale:1},{scale:1.07,duration:0.08,ease:'power2.out'},0.96);
    tl.to('#h-title',{scale:1,duration:0.5,ease:'elastic.out(1,0.45)'},1.04);
    // spreading smell: rings
    ['#h-r1','#h-r2','#h-r3'].forEach((r,i)=>{
      tl.fromTo(r,{scale:0.4,opacity:0},{scale:3.2,opacity:0,keyframes:{opacity:[0,.7,0]},duration:1.6,ease:'sine.out'},1.9+i*0.45);
    });
    // title moves up to make room (2.0)
    tl.to('#h-title',{y:-120,scale:.78,duration:0.7,ease:'expo.inOut'},2.0);
    tl.to('#h-kick',{opacity:0,duration:0.3},2.0);
    // nose arrives + scent trail (4.0)
    tl.fromTo('#h-nose',{x:420,opacity:0,rotation:8},{x:0,opacity:1,rotation:0,duration:0.6,ease:'expo.out'},3.95);
    tl.fromTo('#h-tp',{strokeDashoffset:400},{strokeDashoffset:0,duration:2.0,ease:'none'},4.0);
    tl.fromTo('#h-trail',{opacity:0},{opacity:1,duration:0.3},4.0);
    tl.fromTo('#h-nose',{scale:1},{scale:1.08,duration:0.12,yoyo:true,repeat:3,ease:'sine.inOut'},4.9);
    // TERHIDU stamp (5.32)
    tl.fromTo('#h-stamp-in',{scale:2.6,opacity:0,rotation:-14},{scale:1,opacity:1,rotation:-6,duration:0.22,ease:'back.out(2.2)'},5.28);
    tl.fromTo('#h-world',{x:0},{keyframes:{x:[0,-14,12,-8,6,0]},duration:0.32,ease:'none'},5.3);
    // exit
    tl.to('#h-world',{scale:1.12,opacity:0,duration:0.22,ease:'power2.in'},5.78);
"""

def build():
    return scene('hook', CSS, BODY, JS)
