# Generates index.html + compositions/*.html for the Frescura Body awareness ad (1080x1920, 30fps)
import json, os
OFF = 0.25          # voice starts 0.25 s into the film
TOTAL = 37.4
W, H = 1080, 1920
os.makedirs("compositions", exist_ok=True)

FONTS = """
@font-face{font-family:'Bodoni Moda';font-style:normal;font-weight:400 900;src:url('assets/fonts/BodoniModa-normal.woff2') format('woff2');}
@font-face{font-family:'Bodoni Moda';font-style:italic;font-weight:400 900;src:url('assets/fonts/BodoniModa-italic.woff2') format('woff2');}
@font-face{font-family:'Jost';font-style:normal;font-weight:300 800;src:url('assets/fonts/Jost-normal.woff2') format('woff2');}
"""
BASE = FONTS + """
#root{position:absolute;inset:0;overflow:hidden;font-family:'Jost',sans-serif;color:#f4eee6;}
.abs{position:absolute;}
.full{position:absolute;inset:0;}
.serif{font-family:'Bodoni Moda',serif;}
.it{font-family:'Bodoni Moda',serif;font-style:italic;}
.eyebrow{font-family:'Jost';font-weight:500;font-size:30px;letter-spacing:.42em;text-transform:uppercase;color:#d8b77a;}
.center{left:0;width:1080px;text-align:center;}
.gold{color:#d8b77a;}
.rule{height:2px;background:linear-gradient(90deg,transparent,#d8b77a,transparent);}
svg .ln{fill:none;stroke:#d8b77a;stroke-width:3.2;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1;}
"""
HELP = """
function rng(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;}}
function inBlur(tl,sel,t,d,extra){tl.fromTo(sel,Object.assign({opacity:0,filter:'blur(10px)'},extra&&extra.from||{}),Object.assign({opacity:1,filter:'blur(0px)',duration:d||0.35,ease:'expo.out'},extra&&extra.to||{}),t);}
function outBlur(tl,sel,t,d){tl.to(sel,{opacity:0,filter:'blur(8px)',duration:d||0.18,ease:'power2.in'},t);}
function slam(tl,sel,t,s){tl.fromTo(sel,{opacity:0,scale:s||1.35,filter:'blur(12px)'},{opacity:1,scale:1,filter:'blur(0px)',duration:0.42,ease:'expo.out'},t);}
function draw(tl,sel,t,d){tl.fromTo(sel,{strokeDashoffset:1},{strokeDashoffset:0,duration:d||0.5,ease:'power2.out'},t);}
function shake(tl,sel,t,amp,seed){var r=rng(seed||7);for(var i=0;i<8;i++){tl.to(sel,{x:(r()-.5)*amp*(1-i/8),y:(r()-.5)*amp*(1-i/8),duration:0.03,ease:'none'},t+i*0.03);}tl.to(sel,{x:0,y:0,duration:0.04},t+0.24);}
"""

def scene(sid, dur, css, html, js):
    doc = f"""<template>
<style>{BASE}{css}</style>
<div id="root" data-composition-id="{sid}" data-width="{W}" data-height="{H}" data-start="0" data-duration="{dur}">
{html}
</div>
<script>
(function(){{
{HELP}
const tl = gsap.timeline({{ paused: true }});
{js}
tl.set({{}}, {{}}, {dur - 0.01});
window.__timelines["{sid}"] = tl;
}})();
</script>
</template>
"""
    open(f"compositions/{sid}.html", "w").write(doc)

ICON = {
 'suami':'<circle class="ln" pathLength="1" cx="48" cy="30" r="14"/><path class="ln" pathLength="1" d="M18 84 C18 62 32 54 48 54 C64 54 78 62 78 84"/><path class="ln" pathLength="1" d="M48 56 L43 66 L48 80 L53 66 Z"/>',
 'anak':'<circle class="ln" pathLength="1" cx="48" cy="38" r="12"/><path class="ln" pathLength="1" d="M30 84 C30 68 38 60 48 60 C58 60 66 68 66 84"/><path class="ln" pathLength="1" d="M38 28 Q48 16 58 28"/>',
 'rumah':'<path class="ln" pathLength="1" d="M14 46 L48 18 L82 46"/><path class="ln" pathLength="1" d="M24 40 V82 H72 V40"/><path class="ln" pathLength="1" d="M41 82 V60 H55 V82"/>',
 'moon':'<path class="ln" pathLength="1" d="M58 18 A32 32 0 1 0 80 62 A26 26 0 1 1 58 18 Z"/>',
 'drop':'<path class="ln" pathLength="1" d="M48 12 C48 12 22 44 22 60 A26 26 0 0 0 74 60 C74 44 48 12 48 12 Z"/><path class="ln" pathLength="1" d="M36 62 A12 12 0 0 0 48 74"/>',
 'spark':'<path class="ln" pathLength="1" d="M48 10 L54 42 L86 48 L54 54 L48 86 L42 54 L10 48 L42 42 Z"/>',
 'check':'<path class="ln" pathLength="1" d="M28 50 L43 65 L70 34"/>',
}
def icon(name, cls="", size=96):
    return f'<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 96 96">{ICON[name]}</svg>'

