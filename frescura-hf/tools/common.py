"""Shared design tokens and snippets for the Frescura Body film (1080x1920, 30 fps)."""

FONTS = """
@font-face{font-family:'Bodoni Moda';font-style:normal;font-weight:400;src:url('assets/fonts/bodoni-moda-latin-400-normal.woff2') format('woff2');}
@font-face{font-family:'Bodoni Moda';font-style:italic;font-weight:400;src:url('assets/fonts/bodoni-moda-latin-400-italic.woff2') format('woff2');}
@font-face{font-family:'Bodoni Moda';font-style:normal;font-weight:700;src:url('assets/fonts/bodoni-moda-latin-700-normal.woff2') format('woff2');}
@font-face{font-family:'Bodoni Moda';font-style:italic;font-weight:700;src:url('assets/fonts/bodoni-moda-latin-700-italic.woff2') format('woff2');}
@font-face{font-family:'Bodoni Moda';font-style:normal;font-weight:900;src:url('assets/fonts/bodoni-moda-latin-900-normal.woff2') format('woff2');}
@font-face{font-family:'Bodoni Moda';font-style:italic;font-weight:900;src:url('assets/fonts/bodoni-moda-latin-900-italic.woff2') format('woff2');}
@font-face{font-family:'Manrope';font-style:normal;font-weight:400;src:url('assets/fonts/manrope-latin-400-normal.woff2') format('woff2');}
@font-face{font-family:'Manrope';font-style:normal;font-weight:600;src:url('assets/fonts/manrope-latin-600-normal.woff2') format('woff2');}
@font-face{font-family:'Manrope';font-style:normal;font-weight:800;src:url('assets/fonts/manrope-latin-800-normal.woff2') format('woff2');}
"""

TOKENS = """
:root{
  --noir:#0b0908; --espresso:#17110e; --ink:#f6efe4; --mute:#b9ab97;
  --gold:#d8b46e; --gold-hi:#fff0c9; --gold-lo:#8a6534;
  --rose:#c8263a; --rose-hi:#ff6b7a; --violet:#6c4fd1; --violet-hi:#b9a3ff;
  --serif:'Bodoni Moda', serif; --sans:'Manrope', sans-serif;
}
"""

BASE = """
*{margin:0;padding:0;box-sizing:border-box;}
#root{position:absolute;inset:0;overflow:hidden;font-family:var(--sans);color:var(--ink);}
.full{position:absolute;inset:0;}
.bg-noir{position:absolute;inset:0;background:
  radial-gradient(120% 70% at 50% 38%, #2a1f19 0%, #140f0c 48%, #070605 100%);}
.goldtxt{background:linear-gradient(100deg,#7d5a2c 0%,#e9cf98 22%,#fff3d2 34%,#c99d5c 52%,#f7e2b1 70%,#8f6834 100%);
  background-size:220% 100%; background-position:0% 50%;
  -webkit-background-clip:text; background-clip:text; color:transparent;}
.kicker{font-family:var(--sans);font-weight:600;font-size:30px;letter-spacing:.42em;text-transform:uppercase;color:var(--gold);}
.serif-i{font-family:var(--serif);font-style:italic;}
.center-x{position:absolute;left:0;right:0;text-align:center;}
.rule{height:2px;background:linear-gradient(90deg,transparent,var(--gold),transparent);transform-origin:50% 50%;}
.glass{background:linear-gradient(160deg,rgba(255,240,210,.09),rgba(255,240,210,.02));
  border:1.5px solid rgba(216,180,110,.55);border-radius:28px;
  box-shadow:0 30px 80px rgba(0,0,0,.45), inset 0 1px 0 rgba(255,255,255,.12);}
.dust{position:absolute;border-radius:50%;background:radial-gradient(circle,#ffe9b8 0%,rgba(255,220,150,.0) 70%);}
"""


def scene(cid, css, body, js, extra_head=""):
    """A sub-composition file: everything inside <template>."""
    return f"""<template>
  <style>
{FONTS}
{TOKENS}
{BASE}
{css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
{body}
  </div>
  <script>
  (function(){{
    const root = document.querySelector('[data-composition-id="{cid}"]');
    const $ = (s) => root.querySelector(s);
    const $$ = (s) => Array.from(root.querySelectorAll(s));
    // seeded PRNG: deterministic decoration
    let _s = {sum(map(ord, cid)) * 131 + 17};
    const rnd = () => (_s = (_s * 16807) % 2147483647) / 2147483647;
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines = window.__timelines || {{}};
    window.__timelines["{cid}"] = tl;
  }})();
  </script>
</template>
"""


def dust_js(container_sel, n, dur, area=(0, 0, 1080, 1920), size=(4, 14), alpha=(0.25, 0.8)):
    """Gold dust motes: generated once (seeded), drifting with the timeline."""
    x0, y0, w, h = area
    return f"""
    (function(){{
      const box = $('{container_sel}');
      for (let i=0;i<{n};i++){{
        const d=document.createElement('div'); d.className='dust';
        const sz={size[0]}+rnd()*({size[1]}-{size[0]});
        d.style.width=sz+'px'; d.style.height=sz+'px';
        d.style.left=({x0}+rnd()*{w})+'px'; d.style.top=({y0}+rnd()*{h})+'px';
        box.appendChild(d);
        const a={alpha[0]}+rnd()*({alpha[1]}-{alpha[0]});
        tl.fromTo(d,{{opacity:0,x:0,y:0}},{{opacity:a,duration:0.6,ease:'sine.out'}},rnd()*0.4);
        tl.fromTo(d,{{x:0,y:0}},{{x:(rnd()-0.5)*90,y:-40-rnd()*160,duration:{dur},ease:'none'}},0);
      }}
    }})();
"""
