"""A luxury mall boutique set, drawn in SVG/CSS. Prefix keeps ids unique per scene."""


def mall_css(p):
    return f"""
#{p}-world{{position:absolute;inset:0;transform-origin:50% 62%;}}
#{p}-set{{position:absolute;inset:0;}}
#{p}-bok{{position:absolute;inset:0;}}
.{p}-b{{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(255,226,160,.55) 0%,rgba(255,226,160,0) 70%);}}
#{p}-sign{{position:absolute;left:0;right:0;top:470px;text-align:center;font-family:var(--serif);font-weight:700;
  font-size:58px;letter-spacing:.34em;padding-left:.34em;}}
#{p}-signsub{{position:absolute;left:0;right:0;top:546px;text-align:center;font-family:var(--sans);font-weight:600;
  font-size:28px;letter-spacing:.5em;padding-left:.6em;color:var(--gold);}}
.{p}-cone{{position:absolute;top:-60px;width:520px;height:1500px;transform-origin:50% 0;
  background:linear-gradient(180deg,rgba(255,236,190,.30),rgba(255,236,190,.06) 70%,rgba(255,236,190,0));
  clip-path:polygon(44% 0,56% 0,100% 100%,0 100%);filter:blur(6px);mix-blend-mode:screen;}}
.{p}-pod{{position:absolute;width:330px;height:240px;}}
.{p}-pod .top{{position:absolute;left:0;top:0;width:330px;height:70px;border-radius:50%;
  background:radial-gradient(ellipse at 50% 40%,#fbf6ee 0%,#e4dacb 55%,#b9ab97 100%);}}
.{p}-pod .side{{position:absolute;left:0;top:35px;width:330px;height:205px;border-radius:0 0 165px 165px / 0 0 35px 35px;
  background:linear-gradient(90deg,#8d8173 0%,#e9e0d2 32%,#fffaf2 46%,#d6cbbb 66%,#7c7166 100%);}}
.{p}-pod .band{{position:absolute;left:0;top:48px;width:330px;height:6px;background:linear-gradient(90deg,#8a6534,#fff0c9,#8a6534);}}
.{p}-btl{{position:absolute;width:236px;}}
.{p}-btl img{{display:block;width:100%;}}
.{p}-btl .refl{{position:absolute;left:0;top:100%;width:100%;transform:scaleY(-1);opacity:.22;
  -webkit-mask-image:linear-gradient(0deg,rgba(0,0,0,.9),rgba(0,0,0,0) 35%);mask-image:linear-gradient(0deg,rgba(0,0,0,.9),rgba(0,0,0,0) 35%);}}
.{p}-halo{{position:absolute;width:520px;height:520px;border-radius:50%;filter:blur(30px);}}
"""


def mall_svg(p):
    # one-point perspective: vanishing point (540, 860)
    pil = []
    for i, (x0, x1) in enumerate([(0, 150), (150, 250), (250, 318), (318, 362)]):
        pass
    strips = ""
    # left wall gold light strips (trapezoids toward VP)
    for xa, w in [(40, 26), (190, 18), (292, 12), (352, 8), (392, 6)]:
        # top/bottom y shrink toward VP
        k = (540 - xa) / 540.0
        top = 860 - 860 * k
        bot = 860 + 1060 * k
        strips += f'<polygon points="{xa},{top:.0f} {xa+w},{top + 860*(w/540):.0f} {xa+w},{bot - 1060*(w/540):.0f} {xa},{bot:.0f}" fill="url(#{p}-gs)"/>'
        xb = 1080 - xa - w
        strips += f'<polygon points="{xb+w},{top:.0f} {xb},{top + 860*(w/540):.0f} {xb},{bot - 1060*(w/540):.0f} {xb+w},{bot:.0f}" fill="url(#{p}-gs)"/>'
    lights = ""
    for r, (y, n) in enumerate([(60, 5), (200, 5), (300, 5), (370, 5)]):
        span = 1080 - 2 * (540 * (y / 860))
        x0 = 540 - span / 2
        for j in range(n):
            x = x0 + span * (j + 0.5) / n
            s = 1 - y / 860
            lights += f'<ellipse cx="{x:.0f}" cy="{y}" rx="{34*s:.0f}" ry="{9*s:.0f}" fill="#fff4d6" opacity=".9"/>'
            lights += f'<ellipse cx="{x:.0f}" cy="{y}" rx="{90*s:.0f}" ry="{40*s:.0f}" fill="url(#{p}-lg)" opacity=".5"/>'
    floor_refl = ""
    for xa in [53, 199, 298, 356, 395]:
        floor_refl += f'<rect x="{xa-8}" y="1180" width="22" height="740" fill="url(#{p}-fr)" opacity=".5"/>'
        floor_refl += f'<rect x="{1080-xa-14}" y="1180" width="22" height="740" fill="url(#{p}-fr)" opacity=".5"/>'
    veins = ""
    for d in ["M0 1500 C200 1460 380 1560 620 1480 S980 1520 1080 1450",
              "M0 1760 C260 1700 420 1820 700 1730 S960 1800 1080 1740",
              "M120 1920 C260 1700 420 1560 560 1380", "M900 1920 C820 1720 700 1560 610 1400"]:
        veins += f'<path d="{d}" fill="none" stroke="rgba(216,180,110,.16)" stroke-width="3"/>'
    return f"""
      <svg id="{p}-set" viewBox="0 0 1080 1920" preserveAspectRatio="none">
        <defs>
          <linearGradient id="{p}-gs" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff0c9" stop-opacity=".2"/><stop offset=".45" stop-color="#ffe3a3"/><stop offset="1" stop-color="#c99d5c" stop-opacity=".3"/></linearGradient>
          <radialGradient id="{p}-lg"><stop offset="0" stop-color="#ffe7b3" stop-opacity=".8"/><stop offset="1" stop-color="#ffe7b3" stop-opacity="0"/></radialGradient>
          <linearGradient id="{p}-fr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe3a3" stop-opacity=".6"/><stop offset="1" stop-color="#ffe3a3" stop-opacity="0"/></linearGradient>
          <linearGradient id="{p}-fl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a221d"/><stop offset=".35" stop-color="#1a1411"/><stop offset="1" stop-color="#0b0807"/></linearGradient>
          <linearGradient id="{p}-wl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0d0a08"/><stop offset="1" stop-color="#231a15"/></linearGradient>
          <linearGradient id="{p}-wr" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#0d0a08"/><stop offset="1" stop-color="#231a15"/></linearGradient>
          <linearGradient id="{p}-gl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2d231d"/><stop offset="1" stop-color="#120e0c"/></linearGradient>
          <radialGradient id="{p}-shop" cx=".5" cy=".55" r=".6"><stop offset="0" stop-color="#5a4430"/><stop offset=".6" stop-color="#241b15"/><stop offset="1" stop-color="#120d0a"/></radialGradient>
        </defs>
        <rect width="1080" height="1920" fill="#0e0b09"/>
        <polygon points="0,0 1080,0 700,420 380,420" fill="#120e0c"/>
        <polygon points="0,0 380,420 380,1180 0,1920" fill="url(#{p}-wl)"/>
        <polygon points="1080,0 700,420 700,1180 1080,1920" fill="url(#{p}-wr)"/>
        <polygon points="0,1920 380,1180 700,1180 1080,1920" fill="url(#{p}-fl)"/>
        {veins}
        {floor_refl}
        {strips}
        {lights}
        <rect x="380" y="420" width="320" height="760" fill="url(#{p}-shop)"/>
        <rect x="300" y="430" width="480" height="150" fill="#0d0a08"/>
        <rect x="300" y="430" width="480" height="150" fill="none" stroke="#c99d5c" stroke-width="2.5"/>
        <rect x="312" y="442" width="456" height="126" fill="none" stroke="rgba(216,180,110,.35)" stroke-width="1"/>
        <rect x="350" y="580" width="380" height="600" fill="url(#{p}-gl)" opacity=".9"/>
        <rect x="350" y="580" width="380" height="600" fill="none" stroke="#c99d5c" stroke-width="3"/>
        <line x1="540" y1="580" x2="540" y2="1180" stroke="rgba(216,180,110,.5)" stroke-width="2"/>
        <polygon points="360,590 460,590 380,1170 360,1170" fill="rgba(255,240,210,.06)"/>
        <polygon points="560,590 600,590 560,880" fill="rgba(255,240,210,.05)"/>
        <rect x="380" y="1176" width="320" height="6" fill="#c99d5c" opacity=".8"/>
      </svg>
      <div id="{p}-bok" class="full"></div>
"""


def bokeh_js(p, n, dur):
    return f"""
    (function(){{ const box=$('#{p}-bok');
      for(let i=0;i<{n};i++){{ const b=document.createElement('div'); b.className='{p}-b';
        const s=30+rnd()*120; b.style.width=s+'px'; b.style.height=s+'px';
        b.style.left=(rnd()*1080-s/2)+'px'; b.style.top=(rnd()*1300-s/2)+'px'; box.appendChild(b);
        tl.fromTo(b,{{opacity:0,x:0}},{{opacity:.2+rnd()*.5,x:(rnd()-.5)*120,duration:{dur},ease:'sine.inOut'}},0);
      }} }})();
"""
