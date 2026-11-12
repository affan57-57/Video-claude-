#!/usr/bin/env python3
"""Generate the Frescura Body HyperFrames composition (index.html) from the word-timed transcript."""
import json, sys, html

S = sys.argv[1]
OUT = f"{S}/hf/frescura/index.html"
VO = 0.2            # voice offset in film time
DUR = 33.9

raw = [w for s in json.load(open(f"{S}/work/tx_final.json")) for w in s["words"]]
FIX = {19: "berpeluh,", 74: "beg"}
W = []
for i, w in enumerate(raw):
    W.append(dict(t=round(w["s"] + VO, 3), e=round(w["e"] + VO, 3), w=FIX.get(i, w["w"].strip())))

# caption chunks: (first word idx, last word idx, emphasised idxs, override text per idx)
BRAND = {41: "Frescura", 42: None, 43: "Body", 80: "Frescura", 81: None, 82: "Body"}
CHUNKS = [
    (5, 8, [], {}), (9, 10, [10], {}), (11, 14, [13, 14], {}),
    (15, 18, [18], {}), (19, 21, [19, 21], {}), (22, 27, [27], {}),
    (28, 32, [32], {}), (33, 35, [], {}), (36, 37, [37], {}), (38, 39, [], {}),
    (44, 47, [47], {}), (48, 50, [50], {}),
    (51, 54, [53, 54], {}), (55, 57, [], {}),
    (62, 64, [64], {}), (65, 67, [67], {}),
    (68, 72, [70, 71], {}), (73, 76, [74, 75], {}), (77, 82, [80, 82], {}),
    (83, 84, [84], {}), (85, 86, [85], {}), (87, 90, [88], {}),
]

def esc(s): return html.escape(s, quote=True)

# ---------------------------------------------------------------- shots (film time)
SHOTS = [  # id, src, start, end, kenburns(from,to), extra-class
    ("v_hook",   "hook",     0.00, 1.95, (1.18, 1.04), ""),
    ("v_coupbg", "couple",   1.95, 5.50, (1.25, 1.15), "blurbg"),
    ("v_city",   "city",     5.50, 6.92, (1.10, 1.22), ""),
    ("v_heat",   "heat",     6.92, 9.98, (1.04, 1.14), ""),
    ("v_sh1",    "shower1",  9.98, 12.62, (1.14, 1.04), ""),
    ("v_sh2",    "shower2", 12.62, 15.02, (1.02, 1.12), ""),
    ("v_pump",   "pumpc",   16.42, 18.54, (1.08, 1.0), ""),
    ("v_ripple", "ripple",  18.54, 20.00, (1.2, 1.05), ""),
    ("v_petals", "petals",  20.00, 21.32, (1.1, 1.0), ""),
    ("v_violet", "violet",  21.32, 22.90, (1.15, 1.05), ""),
    ("v_lather", "lather",  22.90, 24.60, (1.12, 1.02), ""),
    ("v_phone",  "phone",   24.60, 28.18, (1.04, 1.12), ""),
]
CUTS = [1.95, 5.50, 6.92, 9.98, 12.62, 15.02, 16.42, 18.54, 20.0, 21.32, 22.9, 24.6, 28.18, 31.45]

CHAPTERS = [(0, 5.5, "01", "Masalah"), (5.5, 9.98, "02", "Punca"), (9.98, 15.02, "03", "Solusi"),
            (15.02, 24.6, "04", "Frescura Body"), (24.6, 31.45, "05", "Dapatkan")]

parts = []
A = parts.append

def clip(id_, start, end, cls="", inner="", style="", tag="div"):
    A(f'<{tag} id="{id_}" class="clip {cls}" data-start="{start:.3f}" data-duration="{end-start:.3f}" style="{style}">{inner}</{tag}>')

# ------------------------------------------------------------------ media
A(f'<audio id="mix" src="assets/audio/mix.wav" data-start="0" data-duration="{DUR}" data-volume="1"></audio>')
for vid, src, a, b, kb, cls in SHOTS:
    A(f'<video id="{vid}" class="clip media {cls}" src="assets/video/{src}.mp4" muted playsinline '
      f'data-start="{a:.3f}" data-duration="{b-a:.3f}"></video>')
# sharp couple card (same clip, framed)
A('<video id="v_coup" class="clip media card-video" src="assets/video/couple.mp4" muted playsinline data-start="1.950" data-duration="3.550"></video>')

# ------------------------------------------------------------------ scenes
# S1 hook
clip("s_hook", 0, 1.95, "scene", """
<div class="shade-bottom"></div>
<svg class="odor" viewBox="0 0 600 420" aria-hidden="true">
  <path class="ow ow1" d="M120 400 C 60 320, 180 260, 120 180 S 160 60, 120 10"/>
  <path class="ow ow2" d="M300 400 C 240 320, 360 260, 300 180 S 340 60, 300 10"/>
  <path class="ow ow3" d="M480 400 C 420 320, 540 260, 480 180 S 520 60, 480 10"/>
</svg>
<div class="hook">
  <div class="hook-k">BALIK KERJA,</div>
  <div class="hook-l1"><span>Badan</span> <span>dah</span></div>
  <div class="hook-l2"><span>berbau?</span></div>
  <div class="hook-rule"></div>
</div>""")

# S2 couple framed card
clip("s_couple", 1.95, 5.5, "scene", """
<div class="card-frame" id="coupframe"></div>
<div class="pill" id="pill-alert"><i class="dot"></i>AMARAN BAU BADAN</div>
<div class="measure" id="measure"><span class="mline"></span><span class="mlabel">jarak "selamat"</span></div>
""")

# S3/S4 education grid
ICON = {
 "move": '<svg viewBox="0 0 48 48"><path d="M8 34h22M14 26h22M20 18h20"/><path d="M34 12l8 6-8 6"/></svg>',
 "drop": '<svg viewBox="0 0 48 48"><path d="M24 6C18 16 12 22 12 30a12 12 0 0 0 24 0c0-8-6-14-12-24z"/><path d="M19 31a5 5 0 0 0 5 5"/></svg>',
 "dust": '<svg viewBox="0 0 48 48"><circle cx="12" cy="14" r="2.5"/><circle cx="30" cy="10" r="2"/><circle cx="22" cy="24" r="3"/><circle cx="38" cy="26" r="2.5"/><circle cx="14" cy="36" r="2"/><circle cx="32" cy="38" r="3"/></svg>',
 "sun":  '<svg viewBox="0 0 48 48"><circle cx="24" cy="24" r="8"/><path d="M24 4v6M24 38v6M4 24h6M38 24h6M10 10l4 4M34 34l4 4M38 10l-4 4M14 34l-4 4"/></svg>',
}
grid = "".join(f'<div class="chip" id="chip{k}"><div class="ic">{ICON[ic]}</div><div class="ct"><b>{t}</b><small>{s}</small></div></div>'
               for k, (ic, t, s) in enumerate([("move", "Bergerak", "aktiviti harian"), ("drop", "Berpeluh", "kelembapan kulit"),
                                                ("dust", "Habuk", "kotoran melekat"), ("sun", "Cuaca panas", "peluh berganda")]))
clip("s_edu", 5.5, 9.98, "scene", f"""
<div class="shade-top"></div>
<div class="edu-head"><span class="eyebrow">SEPANJANG HARI</span><span class="eh-title">Apa yang <em>badan</em> lalui</span></div>
<div class="grid">{grid}</div>
<div class="temp" id="temp"><span class="tnum" id="tnum">28</span><span class="tdeg">°C</span><span class="tlab">SUHU TENGAH HARI</span></div>
""")

# S5 fact card
clip("s_fact", 9.98, 12.62, "scene", """
<div class="shade-top"></div>
<div class="fact" id="fact">
  <div class="fact-k"><span>FAKTA</span><i></i><span>KENAPA BADAN BERBAU</span></div>
  <div class="fact-t">Peluh itu sendiri <em>tak berbau</em>. Bau terhasil apabila <em>bakteria</em> di kulit memecahkan peluh.</div>
</div>""")

# S6 checklist
items = "".join(f'<div class="ck" id="ck{k}"><span class="box"><svg viewBox="0 0 24 24"><path d="M5 12.5l4.2 4.2L19 7"/></svg></span>{t}</div>'
                for k, t in enumerate(["Mandi selepas kerja", "Bersihkan dengan sempurna", "Baru berehat"]))
clip("s_check", 12.62, 15.02, "scene", f"""
<div class="shade-top"></div>
<div class="checklist"><div class="eyebrow">RUTIN WAJIB</div>{items}</div>
<div class="whiteout" id="whiteout"></div>""")

# S7 boutique reveal (mall display)
bokeh = "".join(f'<i style="left:{(k*137)%1080}px;top:{(k*263)%1300+80}px;width:{30+(k*37)%90}px;height:{30+(k*37)%90}px;opacity:{0.10+((k*13)%10)/45:.2f}"></i>'
                for k in range(22))
def boutique(id_, a, b, extra=""):
    clip(id_, a, b, "scene boutique", f"""
<div class="wall"></div><div class="bokeh">{bokeh}</div>
<div class="strip s1"></div><div class="strip s2"></div><div class="strip s3"></div>
<div class="sign"><img src="assets/img/logo.jpg" alt=""/></div>
<div class="spot sp1"></div><div class="spot sp2"></div>
<div class="lbox lb1"><img src="assets/img/noche.jpg" alt=""/><span class="sel"></span><span class="lb-tag">NOCHE · MIDNIGHT FANTASY</span></div>
<div class="lbox lb2"><img src="assets/img/glory.jpg" alt=""/><span class="sel"></span><span class="lb-tag">WOMAN GLORY · BOMBSHELL</span></div>
<div class="floor"></div>
<div class="plinth"></div>
{extra}""")

boutique("s_reveal", 15.02, 16.42, """
<div class="reveal-t"><span class="rk">PASTINYA,</span><span class="rt">Frescura <em>Body</em></span><span class="rs">SOFT &nbsp;|&nbsp; FRAGRANT</span></div>
<div class="flash" id="flash1"></div>""")

# S8 pump callouts
clip("s_pump", 16.42, 18.54, "scene", """
<div class="shade-top"></div>
<svg class="ring" id="ring" viewBox="0 0 200 200"><defs><path id="circ" d="M100 100 m-74 0 a74 74 0 1 1 148 0 a74 74 0 1 1 -148 0"/></defs>
 <text><textPath href="#circ">GENTLE FOAMING · BODY SHOWER · </textPath></text></svg>
<div class="callout" id="call1"><span class="cl-line"></span><span class="cl-dot"></span><div class="cl-t"><b>Buih lembut</b><small>terus dari pam · tak perlu digosok lama</small></div></div>
""")

# S9 ocean salt
salt = "".join(f'<i style="left:{(k*97)%1040+20}px;top:{1100+(k*151)%700}px;width:{8+(k*7)%14}px;height:{8+(k*7)%14}px"></i>' for k in range(26))
clip("s_salt", 18.54, 20.0, "scene", f"""
<div class="salt">{salt}</div>
<div class="big-t salt-t"><span class="bk">OCEAN SALT</span><span class="bt">Garam <em>Laut</em></span><span class="bs">diperkaya dengan aromaterapi</span></div>""")

# S10 Bombshell
clip("s_bomb", 20.0, 21.32, "scene", """
<div class="pcard pc-r" id="pc_glory"><img src="assets/img/glory.jpg" alt=""/></div>
<div class="big-t bomb-t"><span class="bk">WOMAN GLORY</span><span class="bt"><em>Bombshell</em></span><span class="bs">mawar merah · berani &amp; menggoda</span></div>""")

# S11 Midnight fantasy
stars = "".join(f'<i style="left:{(k*71)%1080}px;top:{(k*193)%1100}px;opacity:{0.3+((k*7)%10)/14:.2f};width:{2+(k%3)}px;height:{2+(k%3)}px"></i>' for k in range(70))
clip("s_noche", 21.32, 22.9, "scene", f"""
<div class="stars">{stars}</div>
<div class="pcard pc-l" id="pc_noche"><img src="assets/img/noche.jpg" alt=""/></div>
<div class="big-t noche-t"><span class="bk">NOCHE</span><span class="bt">Midnight <em>Fantasy</em></span><span class="bs">violet malam · lembut &amp; misteri</span></div>""")

# S12 lather badge
clip("s_lather", 22.9, 24.6, "scene", """
<div class="shade-top"></div>
<div class="badge3" id="badge3"><span>AROMATHERAPY</span><i></i><span>OCEAN SALT</span><i></i><span>500 ML</span></div>""")

# S13 phone CTA
clip("s_cta", 24.6, 28.18, "scene", """
<div class="shade-top"></div>
<div class="cta-k" id="ctak"><span class="eyebrow">JANGAN TANGGUH</span></div>
<div class="bagbtn" id="bagbtn">
  <svg viewBox="0 0 64 64"><path d="M14 22h36l-3 32H17z"/><path d="M24 24v-6a8 8 0 0 1 16 0v6"/></svg>
  <span class="tap" id="tap"></span>
</div>
<div class="toast" id="toast"><span class="tk"><svg viewBox="0 0 24 24"><path d="M5 12.5l4.2 4.2L19 7"/></svg></span><div><b>Frescura Body</b><small>sedia untuk check out</small></div></div>""")

# S14 choose + stock (boutique again)
boutique("s_choose", 28.18, 31.45, """

<div class="choose-t"><span class="eyebrow">PILIH WANGIAN KEGEMARAN</span></div>
<div class="stock" id="stock"><div class="st-row"><span>STOK TERHAD</span><b id="stp">100%</b></div><div class="st-bar"><i id="stbar"></i></div></div>""")

# S15 end card
clip("s_end", 31.45, DUR, "scene endcard", """
<div class="end-glow"></div>
<img class="end-logo" id="endlogo" src="assets/img/logo.jpg" alt=""/>
<div class="end-line" id="endline"></div>
<div class="end-cta" id="endcta"><svg viewBox="0 0 64 64"><path d="M14 22h36l-3 32H17z"/><path d="M24 24v-6a8 8 0 0 1 16 0v6"/></svg>Tekan beg kuning sekarang</div>
<div class="end-sub">Woman Glory · Noche &nbsp;—&nbsp; 500 ml</div>""")

# ------------------------------------------------------------------ captions
for ci, (a, b, emph, _) in enumerate(CHUNKS):
    st = W[a]["t"] - 0.06
    en = (W[b + 1]["t"] - 0.04) if b + 1 < len(W) else W[b]["e"] + 0.3
    if ci + 1 < len(CHUNKS): en = min(en, W[CHUNKS[ci + 1][0]]["t"] - 0.06)
    spans = []
    for i in range(a, b + 1):
        txt = BRAND.get(i, W[i]["w"])
        if txt is None: continue
        cls = "w em" if i in emph else "w"
        spans.append(f'<span class="{cls}" data-t="{W[i]["t"]:.3f}">{esc(txt)}</span>')
    pos = " low" if ci >= 19 else (" high" if ci == 14 else "")
    clip(f"cap{ci}", st, en, "cap" + pos, " ".join(spans))

# ------------------------------------------------------------------ persistent UI
for k, (a, b, n, t) in enumerate(CHAPTERS):
    clip(f"chap{k}", a, b, "chap", f'<span class="cn">{n}</span><span class="cbar"></span><span class="ct">{t}</span>')
clip("brandbar", 0, 31.45, "brandbar", '<span>FRESCURA BODY</span>')
clip("frame", 0, DUR, "frame", "")
clip("lightleak", 0, DUR, "leak", "")
clip("grain", 0, DUR, "grain", "")
clip("vignette", 0, DUR, "vig", "")

BODY = "\n".join(parts)

# ------------------------------------------------------------------ timeline script
js = []
J = js.append
J("const tl = gsap.timeline({ paused: true });")
for vid, src, a, b, kb, cls in SHOTS:
    J(f'tl.fromTo("#{vid}", {{scale:{kb[0]}}}, {{scale:{kb[1]}, duration:{b-a:.3f}, ease:"none"}}, {a});')
J('tl.fromTo("#v_coup", {scale:1.12}, {scale:1.0, duration:3.55, ease:"none"}, 1.95);')
# cut punches + leak flashes
for c in CUTS:
    J(f'tl.fromTo("#lightleak", {{opacity:0.55}}, {{opacity:0, duration:0.35, ease:"power2.out", immediateRender:false}}, {c});')
# hook
J('tl.fromTo(".hook-l1 span", {yPercent:0, opacity:1}, {yPercent:0, opacity:1, duration:0.01}, 0);')
J('tl.fromTo(".hook", {scale:1.08}, {scale:1, duration:0.5, ease:"expo.out"}, 0);')
J('tl.fromTo(".hook-l2 span", {scale:1.22}, {scale:1, duration:0.4, ease:"back.out(2.5)", immediateRender:false}, 0.8);')
J('tl.fromTo(".hook-rule", {scaleX:0}, {scaleX:1, duration:0.5, ease:"expo.out"}, 0.9);')
J('tl.fromTo(".ow", {strokeDashoffset:600, opacity:0.0}, {strokeDashoffset:0, opacity:0.85, duration:0.9, stagger:0.12, ease:"power2.out"}, 0.8);')
J('tl.fromTo("#v_hook", {x:0}, {x:-14, duration:0.06, yoyo:true, repeat:5, ease:"none"}, 1.40);')
# couple
J('tl.fromTo(["#v_coup","#coupframe"], {clipPath:"inset(50% 0% 50% 0% round 34px)"}, {clipPath:"inset(0% 0% 0% 0% round 34px)", duration:0.55, ease:"expo.out"}, 1.95);')
J('tl.fromTo("#pill-alert", {y:30, opacity:0}, {y:0, opacity:1, duration:0.4, ease:"back.out(2)"}, 3.6);')
J('tl.fromTo("#pill-alert .dot", {scale:1}, {scale:1.6, duration:0.25, yoyo:true, repeat:5, ease:"sine.inOut"}, 3.7);')
J('tl.fromTo("#measure .mline", {scaleX:0}, {scaleX:1, duration:0.6, ease:"expo.out"}, 4.0);')
J('tl.fromTo("#measure .mlabel", {opacity:0, y:12}, {opacity:1, y:0, duration:0.35}, 4.35);')
# edu
J('tl.fromTo(".edu-head", {opacity:0, y:-24}, {opacity:1, y:0, duration:0.45, ease:"expo.out"}, 5.52);')
for k, t in enumerate([W[18]["t"], W[19]["t"], W[21]["t"], W[25]["t"]]):
    J(f'tl.fromTo("#chip{k}", {{opacity:0, y:50, scale:0.9}}, {{opacity:1, y:0, scale:1, duration:0.45, ease:"back.out(1.8)"}}, {t-0.12:.3f});')
    J(f'tl.fromTo("#chip{k} .ic", {{rotate:-25}}, {{rotate:0, duration:0.6, ease:"elastic.out(1,0.5)"}}, {t-0.12:.3f});')
J('tl.fromTo("#temp", {opacity:0, scale:0.85}, {opacity:1, scale:1, duration:0.4, ease:"back.out(2)"}, 8.9);')
J('const T={v:28}; tl.to(T, {v:36, duration:0.9, ease:"power2.out", onUpdate:()=>{document.getElementById("tnum").textContent=Math.round(T.v);}}, 9.0);')
J('tl.fromTo("#temp .tnum", {color:"#f4efe7"}, {color:"#ff8a5c", duration:0.9}, 9.0);')
# fact
J('tl.fromTo("#fact", {opacity:0, y:-40, clipPath:"inset(0 0 100% 0)"}, {opacity:1, y:0, clipPath:"inset(0 0 0% 0)", duration:0.6, ease:"expo.out"}, 10.6);')
J('tl.fromTo("#fact .fact-k i", {scaleX:0}, {scaleX:1, duration:0.6, ease:"expo.out"}, 10.75);')
# checklist
J('tl.fromTo(".checklist .eyebrow", {opacity:0}, {opacity:1, duration:0.3}, 12.7);')
for k, t in enumerate([13.0, 13.62, 14.26]):
    J(f'tl.fromTo("#ck{k}", {{opacity:0, x:-40}}, {{opacity:1, x:0, duration:0.4, ease:"expo.out"}}, {t});')
    J(f'tl.fromTo("#ck{k} path", {{strokeDashoffset:30}}, {{strokeDashoffset:0, duration:0.3, ease:"power2.out"}}, {t+0.12:.2f});')
J('tl.fromTo("#whiteout", {opacity:0}, {opacity:1, duration:0.32, ease:"power2.in"}, 14.7);')
# reveal (mall boutique)
def boutique_js(sel, a, dur):
    J(f'tl.fromTo("{sel} .wall, {sel} .bokeh", {{scale:1.22}}, {{scale:1.04, duration:{dur}, ease:"power2.out"}}, {a});')
    J(f'tl.fromTo("{sel} .bokeh i", {{y:0}}, {{y:-60, duration:{dur}, ease:"none", stagger:0}}, {a});')
    J(f'tl.fromTo("{sel} .lbox", {{y:120, opacity:0, rotateY:18}}, {{y:0, opacity:1, rotateY:0, duration:0.7, ease:"expo.out", stagger:0.12}}, {a+0.05});')
    J(f'tl.fromTo("{sel} .spot", {{opacity:0}}, {{opacity:1, duration:0.12, stagger:0.14, ease:"steps(2)"}}, {a});')
    J(f'tl.fromTo("{sel} .strip", {{scaleY:0}}, {{scaleY:1, duration:0.6, stagger:0.07, ease:"expo.out"}}, {a});')
    J(f'tl.fromTo("{sel} .sign img", {{opacity:0, filter:"brightness(0.2)"}}, {{opacity:1, filter:"brightness(1.15)", duration:0.25, ease:"steps(3)"}}, {a+0.2});')
boutique_js("#s_reveal", 15.02, 1.4)
J('tl.fromTo("#flash1", {opacity:1}, {opacity:0, duration:0.5, ease:"power2.out"}, 15.02);')
J('tl.fromTo(".reveal-t .rk", {opacity:0, scale:1.3}, {opacity:1, scale:1, duration:0.6, ease:"expo.out"}, 15.05);')
J('tl.fromTo(".reveal-t .rt", {opacity:0, y:40, filter:"blur(12px)"}, {opacity:1, y:0, filter:"blur(0px)", duration:0.55, ease:"expo.out"}, 15.4);')
J('tl.fromTo(".reveal-t .rs", {opacity:0}, {opacity:1, duration:0.4}, 15.8);')
# pump
J('tl.fromTo("#ring", {rotate:0, opacity:0}, {rotate:140, opacity:1, duration:2.1, ease:"none"}, 16.42);')
J('tl.fromTo("#call1 .cl-line", {scaleX:0}, {scaleX:1, duration:0.45, ease:"expo.out"}, 16.6);')
J('tl.fromTo("#call1 .cl-dot", {scale:0}, {scale:1, duration:0.3, ease:"back.out(3)"}, 16.55);')
J('tl.fromTo("#call1 .cl-t", {opacity:0, x:30}, {opacity:1, x:0, duration:0.45, ease:"expo.out"}, 16.85);')
# salt
J('tl.fromTo(".salt i", {y:0, rotate:0, opacity:0}, {y:-520, rotate:180, opacity:0.9, duration:1.46, ease:"power1.out", stagger:0.02}, 18.54);')
for sel, a in (("salt-t", 18.6), ("bomb-t", 20.55), ("noche-t", 21.5)):
    J(f'tl.fromTo(".{sel} .bk", {{opacity:0, scale:1.3}}, {{opacity:1, scale:1, duration:0.6, ease:"expo.out"}}, {a});')
    J(f'tl.fromTo(".{sel} .bt", {{opacity:0, yPercent:40, clipPath:"inset(0 0 100% 0)"}}, {{opacity:1, yPercent:0, clipPath:"inset(0 0 0% 0)", duration:0.5, ease:"expo.out"}}, {a+0.12:.2f});')
    J(f'tl.fromTo(".{sel} .bs", {{opacity:0}}, {{opacity:1, duration:0.4}}, {a+0.4:.2f});')
J('tl.fromTo("#pc_glory", {x:700, rotate:8}, {x:0, rotate:-3, duration:0.6, ease:"expo.out"}, 20.02);')
J('tl.fromTo("#pc_glory", {scale:1}, {scale:1.06, duration:1.3, ease:"none"}, 20.02);')
J('tl.fromTo("#pc_noche", {x:-700, rotate:-8}, {x:0, rotate:3, duration:0.6, ease:"expo.out"}, 21.34);')
J('tl.fromTo("#pc_noche", {scale:1}, {scale:1.06, duration:1.5, ease:"none"}, 21.34);')
J('tl.fromTo(".stars i", {opacity:0.1}, {opacity:1, duration:0.4, yoyo:true, repeat:3, stagger:{each:0.015, from:"random"}, ease:"sine.inOut"}, 21.32);')
# lather
J('tl.fromTo("#badge3", {opacity:0, y:-30}, {opacity:1, y:0, duration:0.5, ease:"expo.out"}, 23.0);')
# CTA
J('tl.fromTo("#ctak", {opacity:0, y:-20}, {opacity:1, y:0, duration:0.4}, 24.7);')
J('tl.fromTo("#bagbtn", {scale:0, rotate:-20}, {scale:1, rotate:0, duration:0.55, ease:"back.out(2.2)"}, 25.3);')
J('tl.to("#bagbtn", {scale:0.86, duration:0.08, ease:"power2.in"}, 26.05);')
J('tl.to("#bagbtn", {scale:1.08, duration:0.3, ease:"back.out(3)"}, 26.13);')
J('tl.fromTo("#tap", {scale:0.2, opacity:0.9}, {scale:2.6, opacity:0, duration:0.6, ease:"power2.out"}, 26.08);')
J('tl.fromTo("#bagbtn", {y:0}, {y:-10, duration:0.5, yoyo:true, repeat:3, ease:"sine.inOut"}, 26.45);')
J('tl.fromTo("#toast", {y:-160, opacity:0}, {y:0, opacity:1, duration:0.5, ease:"expo.out"}, 26.92);')
# choose
boutique_js("#s_choose", 28.18, 3.27)
J('tl.fromTo(".choose-t", {opacity:0, y:-20}, {opacity:1, y:0, duration:0.4}, 28.3);')
J('tl.fromTo("#s_choose .lb1 .sel", {opacity:0, scale:1.12}, {opacity:1, scale:1, duration:0.3, ease:"back.out(2)"}, 28.95);')
J('tl.to("#s_choose .lb1 .sel", {opacity:0, duration:0.2}, 29.68);')
J('tl.to("#s_choose .lb1", {scale:1.05, duration:0.3, ease:"back.out(2)"}, 28.95);')
J('tl.to("#s_choose .lb1", {scale:1, duration:0.3}, 29.68);')
J('tl.fromTo("#s_choose .lb2 .sel", {opacity:0, scale:1.12}, {opacity:1, scale:1, duration:0.3, ease:"back.out(2)"}, 29.7);')
J('tl.to("#s_choose .lb2", {scale:1.05, duration:0.3, ease:"back.out(2)"}, 29.7);')
J('tl.fromTo("#stock", {opacity:0, y:40}, {opacity:1, y:0, duration:0.4, ease:"expo.out"}, 30.3);')
J('tl.fromTo("#stbar", {scaleX:1}, {scaleX:0.16, duration:1.0, ease:"power3.out"}, 30.5);')
J('const P={v:100}; tl.to(P, {v:16, duration:1.0, ease:"power3.out", onUpdate:()=>{document.getElementById("stp").textContent=Math.round(P.v)+"%";}}, 30.5);')
J('tl.fromTo("#stock", {x:0}, {x:6, duration:0.05, yoyo:true, repeat:5}, 31.0);')
# end
J('tl.fromTo("#endlogo", {scale:1.25, opacity:0, filter:"blur(14px)"}, {scale:1, opacity:1, filter:"blur(0px)", duration:0.9, ease:"expo.out"}, 31.45);')
J('tl.fromTo("#endlogo", {y:0}, {y:-12, duration:2.4, ease:"none"}, 31.5);')
J('tl.fromTo("#endline", {scaleX:0}, {scaleX:1, duration:0.7, ease:"expo.out"}, 31.9);')
J('tl.fromTo("#endcta", {opacity:0, y:30}, {opacity:1, y:0, duration:0.5, ease:"back.out(2)"}, 32.1);')
J('tl.fromTo(".end-sub", {opacity:0}, {opacity:1, duration:0.5}, 32.4);')
J('tl.fromTo(".end-glow", {opacity:0.2, scale:0.8}, {opacity:1, scale:1.1, duration:2.4, ease:"sine.out"}, 31.45);')
# captions: chunk pop + karaoke
for ci, (a, b, emph, _) in enumerate(CHUNKS):
    st = W[a]["t"] - 0.06
    J(f'tl.fromTo("#cap{ci}", {{y:26, opacity:0, scale:0.96}}, {{y:0, opacity:1, scale:1, duration:0.22, ease:"back.out(2)"}}, {st:.3f});')
J('document.querySelectorAll(".cap .w").forEach(s=>{const t=+s.dataset.t; tl.fromTo(s,{opacity:0.38},{opacity:1,duration:0.08},t); if(s.classList.contains("em")) tl.fromTo(s,{scale:0.86},{scale:1,duration:0.3,ease:"back.out(3)"},t);});')
# chapters
for k, (a, b, n, t) in enumerate(CHAPTERS):
    J(f'tl.fromTo("#chap{k} .cbar", {{scaleX:0}}, {{scaleX:1, duration:0.5, ease:"expo.out"}}, {a+0.05});')
    J(f'tl.fromTo("#chap{k} .ct", {{opacity:0, x:-10}}, {{opacity:1, x:0, duration:0.4}}, {a+0.1});')
J(f'tl.fromTo("#grain", {{backgroundPosition:"0px 0px"}}, {{backgroundPosition:"640px 410px", duration:{DUR}, ease:"steps({int(DUR*12)})"}}, 0);')
J("window.__timelines = window.__timelines || {};")
J('window.__timelines["main"] = tl;')
J("tl.seek(0);")
SCRIPT = "\n".join(js)

CSS = open(f"{S}/tools/style.css").read()
doc = f"""<!doctype html>
<html lang="ms" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fonts.css" />
<script src="assets/gsap.min.js"></script>
<style>
{CSS}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
{BODY}
</div>
<script>
{SCRIPT}
</script>
</body>
</html>
"""
open(OUT, "w").write(doc)
print("wrote", OUT, len(doc))
