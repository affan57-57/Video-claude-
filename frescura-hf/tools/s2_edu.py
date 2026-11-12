from common import scene, dust_js

# local clock: 0 = 6.00 s in the film. Words: stres 1.54, berpeluh 1.90, sibuk 2.56,
# sebab 3.38, penting 4.04, jaga 4.68, kebersihan 5.04, badan 5.40 ; scene ends 5.75
CSS = """
#e-kick{top:250px;}
#e-rule{position:absolute;left:340px;width:400px;top:305px;}
#e-tiles{position:absolute;left:150px;right:150px;top:370px;height:620px;}
.tile{position:absolute;left:0;right:0;height:170px;display:flex;align-items:center;gap:40px;padding:0 46px;}
.tile svg{width:96px;height:96px;flex:0 0 96px;overflow:visible;}
.tile svg path,.tile svg circle,.tile svg line{fill:none;stroke:var(--gold);stroke-width:6;stroke-linecap:round;stroke-linejoin:round;}
.tile .lab{font-family:var(--sans);font-weight:800;font-size:66px;letter-spacing:.04em;}
.tile .num{margin-left:auto;font-family:var(--serif);font-style:italic;font-size:48px;color:var(--gold);}
#e-t1{top:0;} #e-t2{top:205px;} #e-t3{top:410px;}
#e-eq{position:absolute;left:0;right:0;top:660px;text-align:center;font-family:var(--serif);font-weight:900;
  font-style:italic;font-size:120px;}
#e-fact{position:absolute;left:120px;right:120px;top:380px;height:560px;padding:56px 60px;}
#e-fact .badge{display:inline-block;font-family:var(--sans);font-weight:800;font-size:30px;letter-spacing:.32em;
  color:#1a130d;background:linear-gradient(90deg,#e9cf98,#fff0c9,#c99d5c);padding:10px 22px 10px 28px;border-radius:40px;}
#e-fact .t{margin-top:34px;font-family:var(--serif);font-weight:700;font-size:64px;line-height:1.12;}
#e-fact .s{margin-top:26px;font-family:var(--sans);font-weight:600;font-size:38px;line-height:1.35;color:var(--mute);}
#e-fact .s b{color:var(--gold-hi);font-weight:800;}
#e-drop{position:absolute;right:56px;top:46px;width:120px;height:150px;overflow:visible;}
.bac{position:absolute;width:18px;height:18px;border-radius:50%;border:3px solid var(--rose-hi);}
#e-head{position:absolute;left:0;right:0;top:470px;text-align:center;}
#e-head .a{font-family:var(--sans);font-weight:800;font-size:58px;letter-spacing:.34em;color:var(--ink);}
#e-head .b{font-family:var(--serif);font-style:italic;font-weight:900;font-size:150px;line-height:1.02;margin-top:18px;}
#e-head .rule{width:520px;margin:30px auto 0;height:3px;}
"""

ICON_STRES = '<svg viewBox="0 0 96 96"><path pathLength="1" class="ic" d="M0 52 L22 52 L30 30 L42 74 L54 18 L64 60 L72 52 L96 52"/></svg>'
ICON_PELUH = '<svg viewBox="0 0 96 96"><path pathLength="1" class="ic" d="M48 6 C48 6 18 44 18 62 C18 80 32 92 48 92 C64 92 78 80 78 62 C78 44 48 6 48 6 Z"/><path pathLength="1" class="ic" d="M34 64 C34 72 40 78 48 78"/></svg>'
ICON_SIBUK = '<svg viewBox="0 0 96 96"><circle pathLength="1" class="ic" cx="48" cy="50" r="40"/><line class="hand" x1="48" y1="50" x2="48" y2="24"/><line x1="48" y1="50" x2="66" y2="50"/></svg>'

BODY = f"""
    <div class="bg-noir"></div>
    <div id="e-dust" class="full"></div>
    <div id="e-kick" class="kicker center-x">Kenapa badan berbau?</div>
    <div id="e-rule" class="rule"></div>
    <div id="e-tiles">
      <div id="e-t1" class="tile glass">{ICON_STRES}<span class="lab">STRES</span><span class="num">01</span></div>
      <div id="e-t2" class="tile glass">{ICON_PELUH}<span class="lab">BERPELUH</span><span class="num">02</span></div>
      <div id="e-t3" class="tile glass">{ICON_SIBUK}<span class="lab">SIBUK KERJA</span><span class="num">03</span></div>
    </div>
    <div id="e-fact" class="glass">
      <span class="badge">FAKTA</span>
      <svg id="e-drop" viewBox="0 0 96 120"><path d="M48 6 C48 6 14 52 14 74 C14 96 30 112 48 112 C66 112 82 96 82 74 C82 52 48 6 48 6 Z" fill="rgba(216,180,110,.18)" stroke="#d8b46e" stroke-width="5"/></svg>
      <div class="t">Peluh <span class="goldtxt">tak berbau.</span></div>
      <div class="s"><b>Bakteria</b> pada kulit yang hasilkan bau.</div>
      <div id="e-bacs"></div>
    </div>
    <div id="e-head">
      <div class="a">PENTING</div>
      <div class="b goldtxt">Jaga Kebersihan</div>
      <div class="b goldtxt" style="margin-top:0">Badan</div>
      <div class="rule" id="e-hr"></div>
    </div>
"""

JS = dust_js('#e-dust', 26, 5.75, area=(40, 200, 1000, 1200)) + """
    tl.fromTo('#e-kick',{opacity:0,y:-20},{opacity:1,y:0,duration:0.4,ease:'power3.out'},0.05);
    tl.fromTo('#e-rule',{scaleX:0},{scaleX:1,duration:0.6,ease:'power3.inOut'},0.1);
    [['#e-t1',1.50],['#e-t2',1.86],['#e-t3',2.52]].forEach(([t,at],i)=>{
      tl.fromTo(t,{x:i%2? 620:-620,opacity:0},{x:0,opacity:.32,duration:0.42,ease:'expo.out'},0.25+i*0.15);
      tl.to(t,{opacity:1,scale:1.04,duration:0.14,ease:'power2.out'},at);
      tl.to(t,{scale:1,duration:0.3,ease:'power2.out'},at+0.14);
      tl.fromTo(t+' .ic',{strokeDasharray:1,strokeDashoffset:1},{strokeDashoffset:0,duration:0.6,ease:'power2.out'},at+0.1);
    });
    tl.fromTo('#e-t3 .hand',{rotation:0,transformOrigin:'48px 50px'},{rotation:720,duration:2.4,ease:'none',svgOrigin:'48 50'},2.6);
    tl.fromTo('#e-t2 svg',{y:0},{keyframes:{y:[0,6,0,6,0]},duration:1.6,ease:'sine.inOut'},2.0);
    // collapse into "= BAU"
    tl.to('#e-tiles',{scale:.82,y:-60,opacity:0,duration:0.3,ease:'power3.in'},3.30);
    tl.to(['#e-kick','#e-rule'],{opacity:0,duration:0.25},3.30);
    // FAKTA card
    tl.fromTo('#e-fact',{y:140,opacity:0,scale:.92},{y:0,opacity:1,scale:1,duration:0.45,ease:'expo.out'},3.40);
    tl.fromTo('#e-fact .t',{opacity:0,y:20},{opacity:1,y:0,duration:0.35,ease:'power2.out'},3.55);
    tl.fromTo('#e-fact .s',{opacity:0,y:20},{opacity:1,y:0,duration:0.35,ease:'power2.out'},3.75);
    (function(){
      const box=$('#e-bacs');
      for(let i=0;i<9;i++){ const b=document.createElement('div'); b.className='bac';
        b.style.left=(600+rnd()*180)+'px'; b.style.top=(70+rnd()*150)+'px'; box.appendChild(b);
        tl.fromTo(b,{scale:0,opacity:0},{scale:1,opacity:.9,duration:0.25,ease:'back.out(3)'},3.9+i*0.05);
        tl.fromTo(b,{x:0,y:0},{x:(rnd()-.5)*60,y:(rnd()-.5)*60,duration:1.0,ease:'sine.inOut'},3.9);
      }})();
    tl.to('#e-fact',{y:-80,scale:.9,opacity:0,duration:0.3,ease:'power3.in'},4.62);
    // JAGA KEBERSIHAN BADAN
    tl.fromTo('#e-head .a',{opacity:0},{opacity:1,duration:0.5,ease:'power3.out'},4.66);
    tl.fromTo('#e-head .b',{opacity:0,y:60,filter:'blur(14px)'},{opacity:1,y:0,filter:'blur(0px)',duration:0.4,ease:'expo.out',stagger:0.2},4.74);
    tl.fromTo('#e-head .b',{backgroundPosition:'0% 50%'},{backgroundPosition:'100% 50%',duration:1.2,ease:'sine.inOut'},4.74);
    tl.fromTo('#e-hr',{scaleX:0},{scaleX:1,duration:0.5,ease:'power3.inOut'},5.2);
    tl.to('#e-head',{opacity:0,scale:1.06,duration:0.18,ease:'power2.in'},5.56);
"""

def build():
    return scene('edu', CSS, BODY, JS)
