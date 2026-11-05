// ---------- KL night skyline (original illustration) ----------
const NS='http://www.w3.org/2000/svg', svg=document.getElementById('sky');
let seed=7; const rnd=()=>{seed=(seed*16807)%2147483647;return (seed-1)/2147483646};
const el=(t,a,p=svg)=>{const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e};
const BASE=1480;

const defs=el('defs',{});
defs.innerHTML=`
<linearGradient id="skyg" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#05040c"/><stop offset=".35" stop-color="#140d2a"/>
  <stop offset=".62" stop-color="#3a1d3e"/><stop offset=".78" stop-color="#7a3f3a"/><stop offset=".86" stop-color="#c47a45"/><stop offset="1" stop-color="#2a1610"/>
</linearGradient>
<linearGradient id="petro" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#6f6250"/><stop offset=".35" stop-color="#fff3d2"/><stop offset=".55" stop-color="#e9d3a0"/><stop offset="1" stop-color="#4a3d2c"/>
</linearGradient>
<linearGradient id="tower" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#1b1a2b"/><stop offset=".5" stop-color="#2f2c44"/><stop offset="1" stop-color="#121120"/>
</linearGradient>
<linearGradient id="glass" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#3b5170"/><stop offset=".5" stop-color="#1c2638"/><stop offset="1" stop-color="#0d121c"/>
</linearGradient>
<linearGradient id="haze" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#c47a45" stop-opacity="0"/><stop offset=".7" stop-color="#e3a060" stop-opacity=".35"/><stop offset="1" stop-color="#f0b070" stop-opacity=".55"/>
</linearGradient>
<radialGradient id="moon"><stop offset="0" stop-color="#fff6dc"/><stop offset=".25" stop-color="#ffe9b5" stop-opacity=".55"/><stop offset="1" stop-color="#ffe0a0" stop-opacity="0"/></radialGradient>
<radialGradient id="bokeh"><stop offset="0" stop-color="#ffe2a8" stop-opacity=".9"/><stop offset=".6" stop-color="#ffcf80" stop-opacity=".35"/><stop offset="1" stop-color="#ffcf80" stop-opacity="0"/></radialGradient>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="soft"><feGaussianBlur stdDeviation="3"/></filter>
<linearGradient id="topshade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05040a" stop-opacity=".95"/><stop offset="1" stop-color="#05040a" stop-opacity="0"/></linearGradient>`;

el('rect',{x:0,y:0,width:1080,height:1920,fill:'url(#skyg)'});
// stars
for(let i=0;i<140;i++){el('circle',{cx:rnd()*1080,cy:rnd()*760,r:rnd()*1.4+.3,fill:'#fff',opacity:(rnd()*.6+.2).toFixed(2)})}
// moon glow
el('circle',{cx:1015,cy:575,r:110,fill:'url(#moon)',opacity:.45});
el('circle',{cx:1015,cy:575,r:18,fill:'#fff3d6',opacity:.8,filter:'url(#soft)'});

// generic buildings w/ windows
function building(x,w,h,fill,winC,winP,layerOp=1){
  const g=el('g',{opacity:layerOp});
  el('rect',{x,y:BASE-h,width:w,height:h,fill},g);
  const cw=6,ch=8,gx=5,gy=8;
  for(let yy=BASE-h+12;yy<BASE-10;yy+=ch+gy) for(let xx=x+5;xx<x+w-cw-3;xx+=cw+gx)
    if(rnd()<winP) el('rect',{x:xx,y:yy,width:cw,height:ch,fill:winC,opacity:(rnd()*.6+.4).toFixed(2)},g);
  return g;
}
// far layer
for(let x=-20;x<1100;){const w=40+rnd()*70,h=260+rnd()*330;building(x,w,h,'#1a1530','#f6c97a',.18,.75);x+=w+rnd()*6}

// ---- Merdeka-118-like faceted spire tower (centre, mostly behind bottles)
(function(){const cx=640,top=640,g=el('g',{});
  el('path',{d:`M${cx-70} ${BASE} L${cx-58} ${top+220} L${cx-30} ${top+60} L${cx} ${top} L${cx+30} ${top+60} L${cx+58} ${top+220} L${cx+70} ${BASE} Z`,fill:'url(#glass)'},g);
  for(let i=-3;i<=3;i++) el('path',{d:`M${cx+i*9} ${top+40+Math.abs(i)*12} L${cx+i*20} ${BASE}`,stroke:'#8fb3d9',"stroke-opacity":.25,"stroke-width":1.2},g);
  el('path',{d:`M${cx} ${top} L${cx} ${top-150}`,stroke:'#dfe9ff',"stroke-width":3,filter:'url(#glow)'},g);
  el('circle',{cx,cy:top-150,r:3.5,fill:'#ff5a5a',filter:'url(#glow)'},g);
})();

// ---- Exchange-106-like tower (right)
(function(){const x=870,w=100,top=620,g=el('g',{});
  el('path',{d:`M${x} ${BASE} L${x} ${top+40} L${x+w*0.5} ${top} L${x+w} ${top+28} L${x+w} ${BASE} Z`,fill:'url(#glass)'},g);
  for(let yy=top+50;yy<BASE;yy+=14) el('line',{x1:x+4,y1:yy,x2:x+w-4,y2:yy,stroke:'#f3c983',"stroke-opacity":(.18+rnd()*.25).toFixed(2),"stroke-width":2},g);
  el('path',{d:`M${x} ${top+40} L${x+w*0.5} ${top} L${x+w} ${top+28}`,stroke:'#fff0c8',"stroke-width":3,fill:'none',filter:'url(#glow)'},g);
  el('line',{x1:x+w*0.5,y1:top,x2:x+w*0.5,y2:BASE,stroke:'#fff0c8',"stroke-opacity":.35,"stroke-width":2},g);
})();

// ---- Menara-KL-like telecom tower
(function(){const cx=392,g=el('g',{});
  el('path',{d:`M${cx-16} ${BASE} L${cx-9} 860 L${cx+9} 860 L${cx+16} ${BASE} Z`,fill:'url(#tower)'},g);
  el('path',{d:`M${cx-22} 860 L${cx+22} 860 L${cx+40} 830 L${cx+44} 800 L${cx+36} 778 L${cx-36} 778 L${cx-44} 800 L${cx-40} 830 Z`,fill:'#2a2640'},g);
  el('rect',{x:cx-42,y:800,width:84,height:6,fill:'#ffd38a',filter:'url(#glow)'},g);
  el('rect',{x:cx-36,y:818,width:72,height:4,fill:'#ffe6b5',opacity:.8},g);
  el('path',{d:`M${cx-26} 778 L${cx-14} 752 L${cx+14} 752 L${cx+26} 778 Z`,fill:'#2f2b48'},g);
  el('rect',{x:cx-5,y:690,width:10,height:62,fill:'#3a3654'},g);
  el('line',{x1:cx,y1:690,x2:cx,y2:610,stroke:'#e6e1ff',"stroke-width":3,filter:'url(#glow)'},g);
  el('circle',{cx,cy:610,r:4,fill:'#ff5a5a',filter:'url(#glow)'},g);
})();

// ---- Twin-tower landmark (left), glowing champagne-silver
function twin(cx,w,top){
  const g=el('g',{filter:'url(#glow)'}),H=BASE-top;
  const tiers=[[0,1],[.55,.9],[.66,.8],[.75,.68],[.82,.56],[.87,.42],[.91,.3]];
  let d='';
  for(let i=0;i<tiers.length;i++){
    const [f,s]=tiers[i],nf=i+1<tiers.length?tiers[i+1][0]:.95;
    const y0=BASE-H*f,y1=BASE-H*nf,hw=w*s/2;
    d+=`M${cx-hw} ${y0} L${cx-hw} ${y1} L${cx+hw} ${y1} L${cx+hw} ${y0} Z `;
  }
  d+=`M${cx-w*.12} ${BASE-H*.95} L${cx} ${BASE-H*.985} L${cx+w*.12} ${BASE-H*.95} Z`;
  el('path',{d,fill:'url(#petro)'},g);
  // vertical ribs
  for(let i=-3;i<=3;i++){const xx=cx+i*w*.13;el('line',{x1:xx,y1:BASE-H*.86*(1-Math.abs(i)*.06),x2:xx,y2:BASE,stroke:'#7d6a4c',"stroke-opacity":.55,"stroke-width":1.6},g)}
  // ring lines
  for(let f=.05;f<.86;f+=.035){const s=f<.55?1:f<.66?.9:f<.75?.8:.68;el('line',{x1:cx-w*s/2,x2:cx+w*s/2,y1:BASE-H*f,y2:BASE-H*f,stroke:'#fff8e6',"stroke-opacity":.35,"stroke-width":1.2},g)}
  el('line',{x1:cx,y1:BASE-H*.985,x2:cx,y2:top-40,stroke:'#fffaf0',"stroke-width":3},g);
  el('circle',{cx,cy:top-40,r:2.5,fill:'#fff'},g);
  return H;
}
const pTop=560; twin(98,84,pTop); const H=twin(262,84,pTop);
// sky bridge
(function(){const g=el('g',{filter:'url(#glow)'});const y=BASE-H*.48;
  el('rect',{x:140,y:y-10,width:80,height:12,fill:'#f4e3bb'},g);
  el('path',{d:`M180 ${y+2} L148 ${y+90} M180 ${y+2} L212 ${y+90}`,stroke:'#e9d3a0',"stroke-width":4},g);
})();

// near layer
for(let x=-30;x<1110;){const w=50+rnd()*90,h=120+rnd()*230;building(x,w,h,'#0c0a14','#ffcf85',.28,1);x+=w+rnd()*4}
// city haze
el('rect',{x:0,y:1150,width:1080,height:340,fill:'url(#haze)'});
// bokeh
for(let i=0;i<34;i++){const r=6+rnd()*26;el('circle',{cx:rnd()*1080,cy:1150+rnd()*330,r,fill:'url(#bokeh)',opacity:(.25+rnd()*.5).toFixed(2)})}
// top shade for text legibility
el('rect',{x:0,y:0,width:1080,height:640,fill:'url(#topshade)'});
document.fonts.ready.then(()=>document.body.dataset.ready=1);
