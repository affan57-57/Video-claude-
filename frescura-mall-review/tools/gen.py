# Generates the FRESCURA BODY mall-review HyperFrames project (index.html + compositions/*.html)
import json, os, sys
PROJ = sys.argv[1]
FONTS = open(os.path.join(PROJ, "assets/fonts/fonts.css")).read()
W, H = 1080, 1920
D = 0.68  # extra time kept so the customer's 'dia wangi' is heard in full
def S(t): return round(t + D, 3) if t >= 11.46 else t
TOTAL = round(35.2 + D, 2)

TOKENS = """
  --ivory:#F4EEE6; --ivory2:#EAE1D4; --ink:#141113; --ink2:#2B2528;
  --gold:#D9B77A; --gold2:#B8925A; --rose:#7C1830; --noche:#2B1F5E; --bag:#F6C433;
  --serif:'Cormorant Garamond', 'EB Garamond', serif; --sans:'Plus Jakarta Sans', 'Inter', sans-serif;
"""

def scene(cid, body, css, js):
    return f"""<template>
  <style>
    {FONTS}
    #root {{ position:absolute; inset:0; {TOKENS} font-family:var(--sans); }}
    #root * {{ box-sizing:border-box; }}
    {css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="{W}" data-height="{H}">
{body}
  </div>
  <script>
    window.__timelines = window.__timelines || {{}};
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""

files = {}

# ---------------------------------------------------------------- HOOK (0 - 3.6)
files["hook"] = scene("hook", """
    <div id="hk-scrim"></div>
    <div id="hk-top">
      <div id="hk-eyebrow"><span class="hk-rule"></span>FRESCURA BODY &middot; MALL EDITION<span class="hk-rule"></span></div>
      <div id="hk-l1">REAKSI</div>
      <div id="hk-l2">sebenar</div>
      <div id="hk-l3">pelanggan bila <b>cuba sendiri</b></div>
    </div>
    <div id="hk-pin">
      <svg viewBox="0 0 24 24" width="40" height="40"><path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 9.6A2.6 2.6 0 1 1 12 6.4a2.6 2.6 0 0 1 0 5.2z" fill="#D9B77A"/></svg>
      <span>Live tester &middot; di mall</span>
    </div>
    <div id="hk-brand"><span>FRESCURA</span><span>BODY</span></div>
""", """
    #hk-scrim { position:absolute; inset:0; background:linear-gradient(180deg, rgba(10,8,9,.82) 0%, rgba(10,8,9,.35) 38%, rgba(10,8,9,0) 55%, rgba(10,8,9,.25) 100%); }
    #hk-top { position:absolute; left:0; right:0; top:250px; text-align:center; color:var(--ivory); }
    #hk-eyebrow { font:700 30px/1 var(--sans); letter-spacing:.3em; color:var(--gold); display:flex; align-items:center; justify-content:center; gap:22px; }
    .hk-rule { display:inline-block; width:70px; height:2px; background:var(--gold); }
    #hk-l1 { font:800 178px/0.9 var(--sans); letter-spacing:-.02em; margin-top:34px; }
    #hk-l2 { font:italic 600 200px/0.8 var(--serif); color:var(--gold); margin-top:-6px; }
    #hk-l3 { font:500 50px/1.1 var(--sans); margin-top:26px; color:var(--ivory); }
    #hk-l3 b { font-weight:800; }
    #hk-pin { position:absolute; left:0; right:0; margin:0 auto; top:300px; width:560px; height:86px; border-radius:43px;
      background:rgba(20,17,19,.78); border:1.5px solid rgba(217,183,122,.7); color:var(--ivory); display:flex; align-items:center; justify-content:center; gap:16px;
      font:700 36px/1 var(--sans); opacity:0; }
    #hk-brand { position:absolute; left:0; right:0; top:430px; text-align:center; color:var(--ivory); opacity:0; }
    #hk-brand span { display:block; font:600 150px/0.95 var(--serif); letter-spacing:.12em; text-shadow:0 6px 40px rgba(0,0,0,.45); }
    #hk-brand span + span { font:800 60px/1 var(--sans); letter-spacing:.62em; color:var(--gold); margin-top:14px; }
""", """
    tl.fromTo("#hk-l1", {scale:1.06}, {scale:1, duration:1.6, ease:"power3.out"}, 0);
    tl.fromTo("#hk-l2", {y:30, opacity:0.0}, {y:0, opacity:1, duration:0.45, ease:"power3.out"}, 0.05);
    tl.fromTo("#hk-l3", {y:24, opacity:0}, {y:0, opacity:1, duration:0.4, ease:"power2.out"}, 0.35);
    tl.fromTo(".hk-rule", {scaleX:0}, {scaleX:1, duration:0.6, ease:"power3.out"}, 0.1);
    tl.to("#hk-top", {y:-60, opacity:0, duration:0.3, ease:"power2.in"}, 1.62);
    tl.fromTo("#hk-pin", {y:30, opacity:0, scale:0.9}, {y:0, opacity:1, scale:1, duration:0.4, ease:"back.out(2)"}, 1.95);
    tl.fromTo("#hk-brand", {opacity:0, y:30}, {opacity:1, y:0, duration:0.5, ease:"power2.out"}, 2.12);
    tl.fromTo("#hk-brand span:first-child", {scale:1.25}, {scale:1, duration:1.2, ease:"expo.out"}, 2.12);
    tl.to(["#hk-pin","#hk-brand"], {opacity:0, duration:0.2, ease:"power2.in"}, 3.38);
""")

# ---------------------------------------------------------------- EDU (3.6 - 7.3) ; card video lives in root
files["edu"] = scene("edu", """
    <div id="ed-head">
      <div id="ed-eyebrow">DALAM SETIAP PAM</div>
      <div id="ed-title">3 rahsia <i>wangi &amp; lembut</i></div>
    </div>
    <div class="ed-chip" id="ed-c1"><span class="n">01</span><span class="t"><b>Aromatherapy</b><em>haruman yang menenangkan</em></span></div>
    <div class="ed-chip" id="ed-c2"><span class="n">02</span><span class="t"><b>Ocean Salt</b><em>rasa bersih &amp; segar</em></span></div>
    <div class="ed-chip" id="ed-c3"><span class="n">03</span><span class="t"><b>Gentle Foaming</b><em>busa terus dari pam</em></span></div>
    <div id="ed-bar"><span class="dot"></span>FEEDBACK PELANGGAN<span class="play"></span></div>
    <div id="ed-wipe"></div>
""", """
    #ed-head { position:absolute; left:0; right:0; top:180px; text-align:center; color:var(--ink); }
    #ed-eyebrow { font:700 30px/1 var(--sans); letter-spacing:.4em; color:var(--gold2); }
    #ed-title { font:600 84px/1 var(--serif); margin-top:14px; }
    #ed-title i { color:var(--rose); }
    .ed-chip { position:absolute; left:120px; width:600px; height:104px; border-radius:26px; background:rgba(244,238,230,.92);
      display:flex; align-items:center; gap:24px; padding:0 30px; box-shadow:0 18px 50px rgba(20,17,19,.22); opacity:0; }
    #ed-c1 { top:370px; } #ed-c2 { top:488px; } #ed-c3 { top:606px; }
    .ed-chip .n { font:italic 600 60px/1 var(--serif); color:var(--gold2); width:70px; }
    .ed-chip .t b { display:block; font:800 40px/1.05 var(--sans); color:var(--ink); }
    .ed-chip .t em { display:block; font:italic 500 34px/1.1 var(--serif); color:var(--ink2); margin-top:4px; }
    #ed-bar { position:absolute; left:0; right:0; margin:0 auto; top:1000px; width:640px; height:92px; border-radius:46px; background:var(--ink);
      color:var(--ivory); display:flex; align-items:center; justify-content:center; gap:20px; font:800 34px/1 var(--sans); letter-spacing:.16em; opacity:0; }
    #ed-bar .dot { width:18px; height:18px; border-radius:50%; background:#E0475B; }
    #ed-bar .play { width:0; height:0; border-left:22px solid var(--gold); border-top:14px solid transparent; border-bottom:14px solid transparent; }
    #ed-wipe { position:absolute; left:0; right:0; top:0; height:1920px; background:var(--ink); transform-origin:50% 100%; transform:scaleY(0); }
""", """
    tl.fromTo("#ed-head", {y:-30, opacity:0}, {y:0, opacity:1, duration:0.45, ease:"power3.out"}, 0.05);
    [["#ed-c1",0.30],["#ed-c2",0.98],["#ed-c3",1.68]].forEach(([s,t]) => {
      tl.fromTo(s, {x:-80, opacity:0}, {x:0, opacity:1, duration:0.45, ease:"power3.out"}, t);
    });
    tl.fromTo("#ed-bar", {y:40, opacity:0, scale:0.9}, {y:0, opacity:1, scale:1, duration:0.4, ease:"back.out(1.8)"}, 2.52);
    tl.fromTo("#ed-bar .dot", {opacity:1}, {opacity:0.2, duration:0.25, yoyo:true, repeat:5, ease:"none"}, 2.6);
    tl.fromTo("#ed-wipe", {scaleY:0}, {scaleY:1, duration:0.32, ease:"power3.in"}, 3.38);
""")

# ---------------------------------------------------------------- REVIEW overlays (7.3 - 21.5)  local t = out - 7.3
R0 = 7.3
def r(t): return round(S(t) - R0, 3)
files["review"] = scene("review", f"""
    <div id="rv-open"></div>
    <div id="rv-scrim"></div>
    <div id="rv-frame"></div>
    <div id="rv-rec"><span class="dot"></span>REAL REVIEW</div>
    <div id="rv-loc">LIVE TESTER &middot; MALL</div>
    <div id="rv-wangi"><i>wangi</i><span>&#10022; haruman aromatherapy</span></div>
    <div class="rv-card" id="rv-foam"><span class="k">GENTLE FOAMING</span><span class="v">Busa lembut &mdash; tangan rasa halus</span></div>
    <div id="rv-stamp"><svg viewBox="0 0 300 300" width="300" height="300">
      <circle cx="150" cy="150" r="138" fill="none" stroke="#D9B77A" stroke-width="5"/>
      <circle cx="150" cy="150" r="120" fill="none" stroke="#D9B77A" stroke-width="2"/>
      <text x="150" y="140" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="56" fill="#F4EEE6">100%</text>
      <text x="150" y="196" text-anchor="middle" font-family="Cormorant Garamond" font-style="italic" font-weight="600" font-size="54" fill="#D9B77A">tak tipu</text>
    </svg></div>
    <div id="rv-stars"><div class="row">{''.join(f'<span class="st" id="rv-s{i}">&#9733;</span>' for i in range(5))}</div><div class="lbl">5.0 &middot; pelanggan puas hati</div></div>
    <div class="rv-card" id="rv-aroma"><span class="k">AROMATHERAPY</span><span class="v">Wangi lembut yang menenangkan</span></div>
""", """
    #rv-open { position:absolute; inset:0; background:var(--ink); transform-origin:50% 0%; }
    #rv-scrim { position:absolute; inset:0; background:linear-gradient(180deg, rgba(10,8,9,.62) 0%, rgba(10,8,9,0) 22%, rgba(10,8,9,0) 52%, rgba(10,8,9,.45) 100%); }
    #rv-frame { position:absolute; left:36px; top:36px; right:36px; bottom:36px; border:2px solid rgba(244,238,230,.55); border-radius:34px; }
    #rv-rec { position:absolute; left:84px; top:190px; height:66px; padding:0 28px; border-radius:33px; background:rgba(20,17,19,.72); color:var(--ivory);
      display:flex; align-items:center; gap:14px; font:800 28px/1 var(--sans); letter-spacing:.2em; }
    #rv-rec .dot { width:16px; height:16px; border-radius:50%; background:#E0475B; }
    #rv-loc { position:absolute; right:84px; top:206px; color:var(--ivory); font:700 28px/1 var(--sans); letter-spacing:.22em; opacity:.9; }
    #rv-wangi { position:absolute; left:0; right:0; top:330px; text-align:center; color:var(--ivory); opacity:0; }
    #rv-wangi i { display:block; font:italic 600 190px/0.9 var(--serif); color:var(--gold); text-shadow:0 0 30px rgba(0,0,0,.85), 0 8px 50px rgba(0,0,0,.7); }
    #rv-wangi span { display:inline-block; margin-top:10px; font:700 30px/1 var(--sans); letter-spacing:.14em; background:rgba(20,17,19,.7); padding:16px 26px; border-radius:30px; }
    .rv-card { position:absolute; left:84px; top:300px; width:720px; padding:30px 36px; border-radius:30px; background:rgba(244,238,230,.94);
      box-shadow:0 20px 60px rgba(0,0,0,.3); opacity:0; }
    .rv-card .k { display:block; font:800 28px/1 var(--sans); letter-spacing:.32em; color:var(--gold2); }
    .rv-card .v { display:block; font:italic 600 58px/1.05 var(--serif); color:var(--ink); margin-top:12px; }
    #rv-stamp { position:absolute; right:96px; top:330px; width:300px; height:300px; opacity:0; }
    #rv-stamp svg { filter:drop-shadow(0 10px 30px rgba(0,0,0,.45)); }
    #rv-stars { position:absolute; left:0; right:0; top:330px; text-align:center; }
    #rv-stars .row { display:flex; justify-content:center; gap:14px; }
    #rv-stars .st { font-size:96px; line-height:1; color:var(--gold); opacity:0; text-shadow:0 6px 30px rgba(0,0,0,.45); display:inline-block; }
    #rv-stars .lbl { display:inline-block; margin-top:18px; font:800 30px/1 var(--sans); letter-spacing:.12em; color:var(--ivory); background:rgba(20,17,19,.7); padding:16px 28px; border-radius:30px; opacity:0; }
""", f"""
    tl.fromTo("#rv-open", {{scaleY:1}}, {{scaleY:0, duration:0.4, ease:"power3.out"}}, 0.0);
    tl.fromTo("#rv-frame", {{scale:1.04, opacity:0}}, {{scale:1, opacity:1, duration:0.6, ease:"power3.out"}}, 0.15);
    tl.fromTo("#rv-rec", {{x:-40, opacity:0}}, {{x:0, opacity:1, duration:0.4, ease:"power3.out"}}, 0.3);
    tl.fromTo("#rv-loc", {{x:40, opacity:0}}, {{x:0, opacity:0.9, duration:0.4, ease:"power3.out"}}, 0.4);
    tl.fromTo("#rv-rec .dot", {{opacity:1}}, {{opacity:0.15, duration:0.5, yoyo:true, repeat:27, ease:"sine.inOut"}}, 0.4);
    // wangi (9.50)
    tl.fromTo("#rv-wangi", {{opacity:0, y:30, scale:0.92}}, {{opacity:1, y:0, scale:1, duration:0.45, ease:"back.out(1.6)"}}, {r(9.48)});
    tl.to("#rv-wangi", {{opacity:0, y:-20, duration:0.3, ease:"power2.in"}}, {r(11.55)});
    // foam cutaway 11.70-12.85
    tl.fromTo("#rv-foam", {{x:-60, opacity:0}}, {{x:0, opacity:1, duration:0.4, ease:"power3.out"}}, {r(11.78)});
    tl.to("#rv-foam", {{opacity:0, x:-30, duration:0.25, ease:"power2.in"}}, {r(13.9)});
    // stamp tak tipu (15.14)
    tl.fromTo("#rv-stamp", {{opacity:0, scale:2.2, rotation:-35}}, {{opacity:1, scale:1, rotation:-12, duration:0.32, ease:"power4.in"}}, {r(14.82)});
    tl.to("#rv-stamp", {{opacity:0, duration:0.3}}, {r(17.3)});
    // stars 17.8 ...
    {''.join(f'tl.fromTo("#rv-s{i}", {{opacity:0, scale:0.2, rotation:-40}}, {{opacity:1, scale:1, rotation:0, duration:0.3, ease:"back.out(2.5)"}}, {r(17.80 + i*0.2)});' for i in range(5))}
    tl.fromTo("#rv-stars .lbl", {{opacity:0, y:16}}, {{opacity:1, y:0, duration:0.35, ease:"power2.out"}}, {r(18.30)});
    tl.to("#rv-stars", {{opacity:0, duration:0.25}}, {r(19.25)});
    // aroma cutaway 19.30-20.10
    tl.fromTo("#rv-aroma", {{x:-60, opacity:0}}, {{x:0, opacity:1, duration:0.35, ease:"power3.out"}}, {r(19.36)});
    tl.to("#rv-aroma", {{opacity:0, duration:0.25}}, {r(20.9)});
""")

# ---------------------------------------------------------------- CTA (21.5 - 32.6) local = out - 21.5
C0 = 21.5
def c(t): return round(t - C0, 3)
files["cta"] = scene("cta", f"""
    <div id="ct-p1">
      <div id="ct-eyebrow">DUA WANGIAN SIGNATURE</div>
      <div class="ct-tag" id="ct-tag1"><b>WOMAN GLORY</b><i>Bombshell</i></div>
      <div class="ct-tag" id="ct-tag2"><b>NOCHE</b><i>Midnight Fantasy</i></div>
      <div id="ct-shop"><svg viewBox="0 0 24 24" width="46" height="46"><path d="M6 7h12l-1 13H7L6 7zm3 0a3 3 0 0 1 6 0" fill="none" stroke="#141113" stroke-width="2.2" stroke-linejoin="round"/></svg>TikTok Shop</div>
    </div>
    <div id="ct-p2">
      <div id="ct-stock">
        <div class="k">STOK TERHAD</div>
        <div class="num"><span id="ct-pct">100</span><small>%</small></div>
        <div class="bar"><div id="ct-fill"></div></div>
        <div class="v">tinggal sikit sahaja</div>
      </div>
    </div>
    <div id="ct-p3">
      <div id="ct-bagwrap">
        <svg id="ct-bag" viewBox="0 0 200 220" width="440" height="484">
          <path d="M60 70 a40 40 0 0 1 80 0" fill="none" stroke="#141113" stroke-width="10" stroke-linecap="round"/>
          <path d="M28 70 h144 l-10 136 a8 8 0 0 1-8 8 H46 a8 8 0 0 1-8-8z" fill="#F6C433"/>
          <path d="M28 70 h144 l-2 26 H30z" fill="#E2AE1E"/>
          <circle cx="70" cy="104" r="7" fill="#141113"/><circle cx="130" cy="104" r="7" fill="#141113"/>
        </svg>
        <div id="ct-badge">+1</div>
        <div id="ct-ripple"></div>
        <div id="ct-ripple2"></div>
      </div>
      <div id="ct-p3t"><b>CHECKOUT</b><i>tekan beg kuning sekarang</i></div>
    </div>
    <div id="ct-p4">
      <div id="ct-gift">
        <div class="k">TIKTOK SHOP</div>
        <div id="ct-disc">
          <svg viewBox="0 0 400 240" width="640" height="384"><path d="M60 20 H380 a20 20 0 0 1 20 20 V200 a20 20 0 0 1-20 20 H60 L0 120z" fill="#D9B77A"/><circle cx="62" cy="120" r="16" fill="#1A1230"/></svg>
          <div id="ct-disctxt"><span id="ct-dnum">?</span><small>% OFF</small></div>
        </div>
        <div class="v">Lihat berapa <i>diskaun</i> menanti korang</div>
      </div>
    </div>
""", """
    #ct-p1, #ct-p2, #ct-p3, #ct-p4 { position:absolute; inset:0; opacity:0; }
    #ct-p1 { opacity:1; }
    #ct-eyebrow { position:absolute; left:0; right:0; top:200px; text-align:center; font:800 28px/1 var(--sans); letter-spacing:.4em; color:var(--ink);
      opacity:0; }
    .ct-tag { position:absolute; padding:22px 30px; border-radius:24px; background:rgba(20,17,19,.86); color:var(--ivory); opacity:0; box-shadow:0 18px 50px rgba(0,0,0,.25); }
    .ct-tag b { display:block; font:800 32px/1 var(--sans); letter-spacing:.18em; }
    .ct-tag i { display:block; font:italic 600 48px/1.05 var(--serif); color:var(--gold); margin-top:8px; }
    #ct-tag1 { left:60px; top:290px; }
    #ct-tag2 { right:60px; top:460px; text-align:right; }
    #ct-shop { position:absolute; left:0; right:0; margin:0 auto; top:1000px; width:460px; height:100px; border-radius:50px; background:var(--gold);
      color:var(--ink); display:flex; align-items:center; justify-content:center; gap:16px; font:800 44px/1 var(--sans); opacity:0; box-shadow:0 18px 50px rgba(0,0,0,.3); }
    #ct-p2 { background:linear-gradient(180deg, rgba(14,11,13,.55), rgba(14,11,13,.2) 60%, rgba(14,11,13,.5)); }
    #ct-stock { position:absolute; left:110px; right:110px; top:330px; padding:46px 50px; border-radius:36px; background:rgba(20,17,19,.82); color:var(--ivory); text-align:center;
      border:1.5px solid rgba(217,183,122,.6); }
    #ct-stock .k { font:800 34px/1 var(--sans); letter-spacing:.38em; color:var(--gold); }
    #ct-stock .num { font:600 200px/1 var(--serif); margin-top:10px; }
    #ct-stock .num small { font-size:90px; color:var(--gold); }
    #ct-stock .bar { height:22px; border-radius:11px; background:rgba(244,238,230,.15); margin-top:14px; overflow:hidden; }
    #ct-fill { height:100%; width:100%; border-radius:11px; background:linear-gradient(90deg,#E0475B,var(--gold)); transform-origin:0 50%; }
    #ct-stock .v { font:italic 600 52px/1 var(--serif); margin-top:26px; }
    #ct-p3 { background:radial-gradient(circle at 50% 38%, #FFF8EC 0%, var(--ivory) 45%, var(--ivory2) 100%); }
    #ct-bagwrap { position:absolute; left:320px; top:280px; width:440px; height:484px; }
    #ct-badge { position:absolute; right:-20px; top:30px; width:120px; height:120px; border-radius:60px; background:var(--rose); color:#fff; font:800 50px/120px var(--sans); text-align:center; opacity:0; }
    #ct-ripple, #ct-ripple2 { position:absolute; left:170px; top:250px; width:100px; height:100px; border-radius:50%; border:6px solid var(--ink); opacity:0; }
    #ct-p3t { position:absolute; left:0; right:0; top:820px; text-align:center; color:var(--ink); }
    #ct-p3t b { display:block; font:800 96px/1 var(--sans); letter-spacing:.08em; }
    #ct-p3t i { display:block; font:italic 600 62px/1.1 var(--serif); color:var(--rose); margin-top:10px; }
    #ct-p4 { background:radial-gradient(circle at 50% 35%, #3A2C78 0%, #221846 45%, #120C24 100%); }
    #ct-gift { position:absolute; left:0; right:0; top:260px; text-align:center; color:var(--ivory); }
    #ct-gift .k { font:800 30px/1 var(--sans); letter-spacing:.42em; color:var(--gold); }
    #ct-disc { position:relative; width:640px; height:384px; margin:40px auto 0; }
    #ct-disctxt { position:absolute; left:90px; right:0; top:0; bottom:0; display:flex; align-items:center; justify-content:center; gap:10px; color:#1A1230; }
    #ct-dnum { font:600 220px/1 var(--serif); min-width:150px; display:inline-block; }
    #ct-disctxt small { font:800 54px/1 var(--sans); }
    #ct-gift .v { font:600 64px/1.1 var(--serif); margin-top:40px; padding:0 80px; }
    #ct-gift .v i { color:var(--gold); }
""", f"""
    // P1 bottles (21.5 - 26.6)
    tl.fromTo("#ct-eyebrow", {{opacity:0, y:-20}}, {{opacity:1, y:0, duration:0.4, ease:"power2.out"}}, {c(21.75)});
    tl.fromTo("#ct-tag1", {{opacity:0, x:-60}}, {{opacity:1, x:0, duration:0.45, ease:"power3.out"}}, {c(22.6)});
    tl.fromTo("#ct-tag2", {{opacity:0, x:60}}, {{opacity:1, x:0, duration:0.45, ease:"power3.out"}}, {c(23.4)});
    tl.fromTo("#ct-shop", {{opacity:0, scale:0.6, y:30}}, {{opacity:1, scale:1, y:0, duration:0.45, ease:"back.out(2)"}}, {c(25.72)});
    tl.to("#ct-p1", {{opacity:0, duration:0.2}}, {c(26.45)});
    // P2 stock (26.6 - 28.15)
    tl.fromTo("#ct-p2", {{opacity:0}}, {{opacity:1, duration:0.15}}, {c(26.6)});
    tl.fromTo("#ct-stock", {{scale:0.85, y:40}}, {{scale:1, y:0, duration:0.4, ease:"back.out(1.7)"}}, {c(26.6)});
    tl.fromTo("#ct-fill", {{scaleX:1}}, {{scaleX:0.12, duration:1.1, ease:"power2.inOut"}}, {c(26.85)});
    const pct = {{v:100}};
    tl.fromTo(pct, {{v:100}}, {{v:12, duration:1.1, ease:"power2.inOut", onUpdate:() => {{ document.querySelector("#ct-pct").textContent = Math.round(pct.v); }} }}, {c(26.85)});
    tl.to("#ct-p2", {{opacity:0, duration:0.15}}, {c(28.05)});
    // P3 bag (28.15 - 30.15)
    tl.fromTo("#ct-p3", {{opacity:0}}, {{opacity:1, duration:0.12}}, {c(28.12)});
    tl.fromTo("#ct-bagwrap", {{y:-500, rotation:-10}}, {{y:0, rotation:0, duration:0.55, ease:"bounce.out"}}, {c(28.15)});
    tl.fromTo("#ct-p3t", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.4, ease:"power3.out"}}, {c(28.55)});
    tl.fromTo("#ct-bag", {{scale:1}}, {{scale:0.9, duration:0.08, yoyo:true, repeat:1, ease:"power2.out", transformOrigin:"50% 60%"}}, {c(29.56)});
    tl.fromTo("#ct-ripple", {{opacity:0.9, scale:0.3}}, {{opacity:0, scale:2.6, duration:0.6, ease:"power2.out"}}, {c(29.56)});
    tl.fromTo("#ct-ripple2", {{opacity:0.6, scale:0.3}}, {{opacity:0, scale:3.6, duration:0.8, ease:"power2.out"}}, {c(29.66)});
    tl.fromTo("#ct-badge", {{opacity:0, scale:0}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(3)"}}, {c(29.62)});
    tl.to("#ct-p3", {{opacity:0, duration:0.12}}, {c(30.08)});
    // P4 discount (30.15 - 32.6)
    tl.fromTo("#ct-p4", {{opacity:0}}, {{opacity:1, duration:0.15}}, {c(30.15)});
    tl.fromTo("#ct-disc", {{scale:0.5, rotation:-18, opacity:0}}, {{scale:1, rotation:-6, opacity:1, duration:0.5, ease:"back.out(1.8)"}}, {c(30.2)});
    const dn = {{v:0}}; const seq = ["5","10","15","20","25","?"];
    tl.fromTo(dn, {{v:0}}, {{v:5.99, duration:1.4, ease:"power1.in", onUpdate:() => {{ document.querySelector("#ct-dnum").textContent = seq[Math.min(5, Math.floor(dn.v))]; }} }}, {c(30.45)});
    tl.fromTo("#ct-gift .v", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.4, ease:"power2.out"}}, {c(30.4)});
    tl.to("#ct-disc", {{rotation:4, duration:0.12, yoyo:true, repeat:3, ease:"sine.inOut"}}, {c(31.9)});
""")

# ---------------------------------------------------------------- END CARD (32.6 - 35.2)
files["endcard"] = scene("endcard", """
    <div id="ec-bg"></div>
    <img id="ec-logo" src="assets/img/logo.jpg" alt="Frescura Body"/>
    <div id="ec-cta"><span>Dapatkan di</span><b>TikTok Shop</b></div>
    <div id="ec-line">tekan beg kuning &middot; stok terhad</div>
""", """
    #ec-bg { position:absolute; inset:0; background:#000; }
    #ec-logo { position:absolute; left:90px; top:330px; width:900px; height:900px; object-fit:contain; }
    #ec-cta { position:absolute; left:0; right:0; top:1160px; text-align:center; color:var(--ivory); }
    #ec-cta span { display:block; font:italic 600 60px/1 var(--serif); color:var(--gold); }
    #ec-cta b { display:inline-block; margin-top:18px; font:800 56px/1 var(--sans); letter-spacing:.08em; padding:24px 44px; border-radius:50px; border:2px solid var(--gold); }
    #ec-line { position:absolute; left:0; right:0; top:1390px; text-align:center; color:rgba(244,238,230,.7); font:700 30px/1 var(--sans); letter-spacing:.3em; text-transform:uppercase; }
""", """
    tl.fromTo("#ec-logo", {scale:1.25, opacity:0}, {scale:1, opacity:1, duration:0.9, ease:"expo.out"}, 0.0);
    tl.fromTo("#ec-cta", {y:40, opacity:0}, {y:0, opacity:1, duration:0.5, ease:"power3.out"}, 0.55);
    tl.fromTo("#ec-line", {opacity:0}, {opacity:1, duration:0.4}, 0.55);
    tl.to("#ec-logo", {scale:1.04, duration:1.6, ease:"none"}, 0.95);
""")

# ---------------------------------------------------------------- CAPTIONS (0 - 32.6)
CAP = [ # start, end, text  ; *word* = highlighted
 (0.10,1.20,"Ini antara pengalaman kami"),
 (1.20,2.14,"ketika bawa"),
 (2.14,3.45,"*Frescura Body* ke mall"),
 (3.70,4.90,"Jom tengok apa"),
 (4.90,6.22,"*reaksi* & feedback pelanggan"),
 (6.22,7.20,"yang datang *mencuba*"),
 (7.38,9.24,"So, apa pengalaman?"),
 (9.26,10.55,"Rasa *wangi* tak sabun ni?"),
 (10.68,12.25,"Dia *wangi!*"),
 (11.70,12.70,"Tangan jadi *lembut*"),
 (12.84,14.50,"Memang tangan *lembut* lah"),
 (14.54,15.60,"Tapi wangi ni *tak tipu!*"),
 (15.70,16.34,"Wangi, tak tipu."),
 (16.34,17.45,"Betul ke? Kau tak tipu?"),
 (17.64,19.30,"Memang *tak tipu* lah"),
 (19.30,20.05,"memang *wangi* lah!"),
 (20.10,21.40,"Terima kasih *banyak!*"),
 (22.06,23.62,"So, sekarang korang pula"),
 (23.62,24.48,"untuk dapatkan"),
 (24.48,25.24,"*Frescura Body*"),
 (25.24,26.45,"melalui *TikTok Shop*"),
 (26.68,28.10,"Stok sangat *tak banyak!*"),
 (28.10,29.00,"Cepat *checkout*"),
 (29.00,29.54,"dan tengok"),
 (29.54,30.10,"*beg kuning* sekarang!"),
 (30.30,31.32,"Lihat berapa"),
 (31.32,32.50,"*TikTok* bagi dekat korang"),
]
import re
body, js = [], []
for i,(s,e,t) in enumerate(CAP):
    s, e = S(s), (e if e == 12.25 else S(e))
    parts = re.split(r"(\*[^*]+\*)", t)
    words = []
    for p in parts:
        if not p: continue
        if p.startswith("*"):
            words.append(f'<span class="w hl">{p[1:-1]}</span>')
        else:
            words += [f'<span class="w">{w}</span>' for w in p.split()]
    body.append(f'    <div class="cg" id="cg{i}"><div class="pill">{" ".join(words)}</div></div>')
    n = len(words); step = min(0.09, max(0.04, (e - s) * 0.35 / max(1, n)))
    js.append(f'tl.fromTo("#cg{i}", {{opacity:0}}, {{opacity:1, duration:0.01}}, {s:.2f});')
    js.append(f'tl.fromTo("#cg{i} .pill", {{y:18, scale:0.96}}, {{y:0, scale:1, duration:0.22, ease:"power3.out"}}, {s:.2f});')
    js.append(f'tl.fromTo("#cg{i} .w", {{opacity:0, y:14}}, {{opacity:1, y:0, duration:0.16, stagger:{step:.3f}, ease:"power2.out"}}, {s:.2f});')
    if '*' in t: js.append(f'tl.fromTo("#cg{i} .hl", {{scale:0.8}}, {{scale:1, duration:0.3, ease:"back.out(3)"}}, {s+0.05:.2f});')
    js.append(f'tl.to("#cg{i}", {{opacity:0, duration:0.08, ease:"power2.in"}}, {e-0.08:.2f});')
    js.append(f'tl.set("#cg{i}", {{opacity:0, visibility:"hidden"}}, {e:.2f});')
files["captions"] = scene("captions", "\n".join(body), """
    .cg { position:absolute; left:0; right:0; top:1150px; text-align:center; opacity:0; }
    .cg .pill { display:inline-block; max-width:1000px; padding:20px 34px 24px; border-radius:30px; background:rgba(18,15,17,.74);
      box-shadow:0 14px 40px rgba(0,0,0,.25); }
    .cg .w { display:inline-block; margin:0 .13em; font:800 66px/1.12 var(--sans); color:#FFFDF8; letter-spacing:-.01em; }
    .cg .hl { font:italic 600 88px/1 var(--serif); color:var(--gold); letter-spacing:0; padding:0 4px; }
""", "\n".join("    "+x for x in js))

for k,v in files.items():
    open(os.path.join(PROJ, f"compositions/{k}.html"), "w").write(v)

# ---------------------------------------------------------------- ROOT
def vid(id_, src, start, dur, mstart, rate=1.0, z=2, style=""):
    return (f'      <video id="{id_}" class="clip media" src="assets/video/{src}" muted playsinline data-start="{start}" data-duration="{dur}" '
            f'data-media-start="{mstart}" data-playback-rate="{rate}" data-track-index="1" style="z-index:{z};{style}"></video>')
def host(id_, start, dur, z, kind="graphics", track=3):
    return (f'      <div id="{id_}" data-composition-id="{id_}" data-composition-src="compositions/{id_}.html" data-start="{start}" '
            f'data-duration="{dur}" data-track-index="{track}" data-track-kind="{kind}" data-width="{W}" data-height="{H}" style="z-index:{z}"></div>')
SFX = [ # file, start, volume
 ("impact-bass-1",0.00,0.55),("sparkle",0.15,0.55),
 ("whoosh",1.69,0.85),("pop",1.83,1.3),("sparkle",2.10,0.5),
 ("whoosh-short",3.44,0.85),("pop",3.78,1.3),("click",4.50,1.8),("pop",5.18,1.3),
 ("ping",5.80,0.9),("whoosh-cinematic",4.70,0.55),
 ("sparkle",9.42,0.4),
 ("whoosh",11.54,0.8),("whoosh-short",12.69,0.7),
 ("impact-bass-1",15.07,0.5),
 ("pop",17.68,1.1),("click",17.93,1.6),("pop",18.08,1.1),("click",18.33,1.6),("pop",18.48,1.2),("ping",18.55,0.6),
 ("whoosh",19.14,0.8),("whoosh-short",19.94,0.7),
 ("whoosh",21.34,0.85),("sparkle",21.55,0.5),("pop",22.48,1.2),("click",23.33,1.6),("ping",25.40,0.9),
 ("impact-bass-1",26.55,0.45),("key-press",26.90,2.5),("key-press",27.12,2.5),("key-press",27.34,2.5),("key-press",27.56,2.5),("key-press",27.78,2.5),
 ("whoosh",28.00,0.85),("click",29.49,2.2),("pop",29.60,1.3),
 ("whoosh-short",30.00,0.8),("sparkle",30.40,0.6),("riser",29.15,0.32),
 ("impact-bass-1",32.56,0.6),("sparkle",32.75,0.55),
]
DUR={"whoosh":0.57,"whoosh-short":0.57,"whoosh-cinematic":5.5,"pop":0.72,"impact-bass-1":2.1,"impact-bass-2":2.59,"riser":3.45,"sparkle":1.8,"click":0.36,"ping":1.32,"key-press":0.43}
sfx_html = "\n".join(f'      <audio id="sfx{i}" class="clip" src="assets/audio/{f}.mp3" data-start="{s}" data-duration="{DUR[f]}" data-volume="{v}" data-track-index="{10+i}"></audio>' for i,(f,s,v) in enumerate((f,S(s),v) for f,s,v in SFX))

FULL = "position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover;"
CARD = "position:absolute;left:90px;top:340px;width:900px;height:640px;object-fit:cover;border-radius:40px;box-shadow:0 30px 80px rgba(20,17,19,.28);"
index = f"""<!doctype html>
<html lang="ms" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ margin:0; width:1080px; height:1920px; overflow:hidden; background:#141113; }}
      #root {{ position:relative; width:1080px; height:1920px; overflow:hidden; }}
      .bgfill {{ position:absolute; left:0; top:0; width:1080px; height:1920px; }}
      #kb {{ position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:cover; }}
      #kbwrap {{ position:absolute; left:0; top:0; width:1080px; height:1920px; overflow:hidden; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}">
      <div id="edu-bg" class="clip bgfill" data-start="3.6" data-duration="3.7" data-track-index="0" style="z-index:1;background:radial-gradient(circle at 50% 30%, #FBF6EE 0%, #F4EEE6 50%, #E7DCCD 100%);"></div>
{vid("v-hook", "pump.mp4", 0, 1.85, 15.6, 0.85, 2, FULL)}
{vid("v-booth", "review.mp4", 1.85, 1.75, 0.0, 1.0, 2, FULL)}
{vid("v-press", "pump.mp4", 3.6, 3.7, 10.0, 1.3, 2, CARD)}
{vid("v-r1", "review.mp4", 7.3, 4.93, 1.015, 1.06, 2, FULL)}
{vid("v-r2", "review.mp4", 12.23, 3.98, 6.241, 1.06, 2, FULL)}
{vid("v-r3", "review.mp4", 16.21, 1.94, 10.419, 1.06, 2, FULL)}
{vid("v-r4", "review.mp4", 18.15, 4.03, 13.415, 1.06, 2, FULL)}
{vid("v-foam", "pump.mp4", 12.38, 1.15, 17.0, 1.0, 3, FULL)}
{vid("v-lather", "pump.mp4", 19.98, 0.8, 26.0, 1.2, 3, FULL)}
      <div id="kb-clip" class="clip" data-start="22.18" data-duration="5.1" data-track-index="2" style="z-index:2;position:absolute;left:0;top:0;width:1080px;height:1920px;">
        <div id="kbwrap"><img id="kb" src="assets/img/bottles.jpg" alt="Frescura Body Woman Glory dan Noche"/></div>
      </div>
{vid("v-stand", "pump.mp4", 27.28, 1.55, 0.2, 1.0, 2, FULL)}
{host("hook", 0, 3.6, 10)}
{host("edu", 3.6, 3.7, 10)}
{host("review", 7.3, 14.88, 10)}
{host("cta", 22.18, 11.1, 10)}
{host("endcard", 33.28, 2.6, 10)}
{host("captions", 0, 33.28, 50, "captions", 4)}
      <audio id="voice" class="clip" src="assets/audio/voice.wav" data-start="0" data-volume="1" data-track-index="9"></audio>
{sfx_html}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      tl.fromTo("#kb", {{scale:1.18, x:30, y:20}}, {{scale:1.02, x:0, y:0, duration:5.1, ease:"power1.out"}}, 22.18);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(os.path.join(PROJ, "index.html"), "w").write(index)
print("ok", list(files))
