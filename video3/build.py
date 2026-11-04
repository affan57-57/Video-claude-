"""Video 3 (modern motion graphics, minimalist luxury): build project/index.html from the voice's word timestamps.
Usage: python3 -I build.py PROJECT_DIR [--final]"""
import json, re, sys

proj = sys.argv[1]
FINAL = "--final" in sys.argv
DURATION = 37.6          # authored on the original voice timeline; remapped below

# The voice later got newly recorded phrases spliced in ("Woman Glory by Bombshell", "Noche by Midnight Fantasy").
# inserts.json = [[old_start, old_end, +seconds], ...]: the old span [a, b] now lasts (b - a + delta).
INSERTS = json.load(open(f"{proj}/assets/audio/inserts.json"))
def T(x):
    shift = 0.0
    for a, b, dl in INSERTS:
        if x >= b: shift += dl
        elif x > a: return round(a + shift + (x - a) * (b - a + dl) / (b - a), 3)
    return round(x + shift, 3)

words = [w for s in json.load(open(f"{proj}/assets/audio/words.json")) for w in s["words"]]
FIX = {"Flaskura": "Frescura", "Bodi": "Body", "parabens": "paraben", "didarang": "dilarang", "makmah": "makmal",
       "basenya": "best-nya", "basenya,": "best-nya,", "bui": "buih", "backbone": "beg kuning", "sepuluh": "cepat"}
# word fixes valid only inside a time window (word, from, to, replacement; "" drops the word)
WFIX = [("First", 3.8, 4.1, "Frescura"), ("Cooler", 4.0, 4.3, ""), ("No", 26.0, 26.2, "Noche"), ("Chair", 26.2, 26.4, ""),
        ("back", 35.0, 35.2, "beg"), ("on", 35.2, 35.4, "kuning"), ("it", 35.4, 35.5, ""), ("Tekan...", 39.7, 39.9, "Tekan")]
HIDE = [("di", 12.9, 13.7), ("kedai", 12.9, 13.7), ("bayu.", 12.9, 13.7)]   # unclear wording after "ujian makmal"
HL = {"bahan", "frescura", "body", "paraben", "berbahaya", "dilarang", "ujian", "makmal", "foaming", "buih", "lembut",
      "dua", "woman", "glory", "fresh", "floral", "noche", "sweet", "fruity", "perfume", "kegemaran", "beg", "kuning",
      "terhad", "cepat", "check", "out"}
clean = []
for w in words:
    txt = w["w"].strip()
    if any(txt == h and a <= w["s"] <= b for h, a, b in HIDE):
        continue
    core = txt.rstrip(".,?"); tail = txt[len(core):]
    wf = [rep for (k, a, b, rep) in WFIX if core == k and a <= w["s"] <= b]
    if wf:
        if wf[0] == "":
            continue
        txt = wf[0] + tail
    else:
        txt = FIX.get(core, core) + tail
    if txt.startswith("-") and clean:
        clean[-1]["t"] += txt; clean[-1]["e"] = w["e"]; continue
    clean.append({"t": txt, "s": w["s"], "e": w["e"]})
if clean and clean[-1]["t"].startswith("Tekan") and clean[-1]["s"] > 39:
    clean[-1]["t"] = "Tekan"
    clean.append({"t": "cepat!", "s": 40.29, "e": 40.6})   # whisper drops the last word on the room tone
chunks, cur = [], []
for i, w in enumerate(clean):
    cur.append(w)
    nxt = clean[i + 1] if i + 1 < len(clean) else None
    if (len(cur) >= 3 or re.search(r"[.,?!]$", w["t"]) or nxt is None or nxt["s"] - w["e"] > 0.3
            or len(" ".join(x["t"] for x in cur)) > 20):
        chunks.append(cur); cur = []

html, js = [], []
def A(l): js.append(l)
def clip(id_, s, d, inner="", cls="", style=""):
    html.append(f'<div id="{id_}" class="clip {cls}" data-start="{s:.3f}" data-duration="{d:.3f}" style="{style}">{inner}</div>')
def vid(id_, src, s, d, box, cls="frame", z0=1.15, z1=1.0, media="0"):
    """Video inside a masked frame; box = (left, top, w, h). The <video> is timed itself (required for playback)."""
    l, tp, w, h = box
    html.append(f'<div id="{id_}w" class="clip" data-start="{s:.3f}" data-duration="{d:.3f}" style="z-index:4">'
                f'<div id="{id_}m" class="{cls}" style="left:{l}px;top:{tp}px;width:{w}px;height:{h}px"></div></div>')
    html.append(f'<video id="{id_}" class="clip" src="{src}" data-start="{s:.3f}" data-duration="{d:.3f}" data-media-start="{media}" '
                f'muted playsinline style="z-index:4;left:{l}px;top:{tp}px;width:{w}px;height:{h}px;object-fit:cover;'
                f'border-radius:{"50%" if cls=="circle" else "44px"}"></video>')
    A(f'tl.fromTo("#{id_}",{{scale:{z0}}},{{scale:{z1},duration:{d:.2f},ease:"power2.out"}},{s});')
    A(f'tl.fromTo("#{id_},#{id_}m",{{clipPath:"inset(100% 0% 0% 0% round 44px)"}},{{clipPath:"inset(0% 0% 0% 0% round 44px)",duration:0.7,ease:"expo.out"}},{s});')
def full(id_, src, s, d, z0=1.12, z1=1.0, tag="video"):
    if tag == "video":
        html.append(f'<video id="{id_}" class="clip bg" src="{src}" data-start="{s:.3f}" data-duration="{d:.3f}" data-media-start="0" muted playsinline></video>')
    else:
        html.append(f'<img id="{id_}" class="clip bg" src="{src}" data-start="{s:.3f}" data-duration="{d:.3f}" alt="">')
    A(f'tl.fromTo("#{id_}",{{scale:{z0}}},{{scale:{z1},duration:{d:.2f},ease:"power2.out"}},{s});')
    A(f'tl.fromTo("#{id_}",{{clipPath:"circle(0% at 50% 50%)"}},{{clipPath:"circle(75% at 50% 50%)",duration:0.8,ease:"expo.inOut"}},{s});')
def rv(sel, t, d=0.7):
    A(f'tl.fromTo("{sel} > span",{{yPercent:110}},{{yPercent:0,duration:{d},ease:"expo.out"}},{t:.2f});')
def fade(sel, t, d=0.6, y=24, x=0):
    A(f'tl.fromTo("{sel}",{{opacity:0,y:{y},x:{x}}},{{opacity:1,y:0,x:0,duration:{d},ease:"expo.out"}},{t:.2f});')
def line(sel, t, d=0.8):
    A(f'tl.fromTo("{sel}",{{scaleX:0}},{{scaleX:1,duration:{d},ease:"expo.inOut"}},{t:.2f});')
def pop(sel, t, d=0.5):
    A(f'tl.fromTo("{sel}",{{scale:0}},{{scale:1,duration:{d},ease:"back.out(2.2)"}},{t:.2f});')
def R(id_, txt): return f'<span id="{id_}" class="rv"><span>{txt}</span></span>'
def sect(n, s, d, label):
    clip(f"sect{n}", s, d, f'<div class="sect"><b>0{n}</b> &nbsp;/ 06 &nbsp;&nbsp;{label}</div>', style="z-index:8")
    fade(f"#sect{n} .sect", s + 0.1, 0.5, 10)
CHECK = '<svg viewBox="0 0 100 100"><path id="ck" d="M22 52 L42 72 L78 32" stroke="#f3eee6" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="90" stroke-dashoffset="90"/></svg>'
BASKET = ('<svg viewBox="0 0 120 110"><path d="M38 40 L52 10 M82 40 L68 10" stroke="#161412" stroke-width="8" stroke-linecap="round"/>'
          '<path d="M8 40 H112 L100 100 H20 Z" fill="#161412"/></svg>')

# ---- S0 0.00-0.90: the only face shot (under 1 s), to camera, holding the bottle
FACE_END = 0.90
html.append(f'<video id="v_face" class="clip bg" src="assets/broll/face.mp4" data-start="0" data-duration="{FACE_END}" data-media-start="0" muted playsinline></video>')
A(f'tl.fromTo("#v_face",{{scale:1.0}},{{scale:1.05,duration:{FACE_END},ease:"none"}},0);')
clip("s0", 0, FACE_END, '<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 55%,rgba(0,0,0,.55) 100%)"></div>'
     f'<div class="t c kick" style="top:1330px;color:#fff;letter-spacing:10px">{R("k0","Kalau beli sabun mandi")}</div>'
     '<div class="hair" id="h0" style="left:390px;width:300px;top:1395px;background:#fff"></div>')
rv("#k0", 0.1); line("#h0", 0.4)
# ---- S0b 0.90-1.94: "mesti korang nak tahu kan" -- voice continues over motion graphics
clip("bg0b", FACE_END, 1.94 - FACE_END, '<div class="ivory"></div>', style="z-index:2")
vid("v_bub0", "assets/broll/pump_foam.mp4", FACE_END, 1.94 - FACE_END, (240, 700, 600, 600), cls="circle", media="1.2")
clip("s0b", FACE_END, 1.94 - FACE_END, f'<div class="t c kick" style="top:420px">{R("m0","Mesti korang")}</div>'
     f'<div class="t c big" style="top:480px">{R("m1","nak tahu...")}</div>'
     '<div class="ring" id="m2" style="left:200px;top:660px;width:680px;height:680px"></div>')
A(f'tl.fromTo("#bg0b",{{clipPath:"circle(0% at 50% 50%)"}},{{clipPath:"circle(80% at 50% 50%)",duration:0.45,ease:"expo.inOut"}},{FACE_END});')
rv("#m0", 1.02); rv("#m1", 1.38)
A('tl.fromTo("#m2",{scale:0.7,opacity:0},{scale:1,opacity:1,duration:0.6,ease:"expo.out"},1.0);')

# ---- S1 1.94-3.92: HOOK question, kinetic type
clip("s1", 1.94, 1.98, '<div class="ivory"></div>'
     f'<div class="t kick" style="top:420px">{R("q0","Soalan penting")}</div>'
     f'<div class="t big" style="top:520px">{R("q1","Ada bahan")}</div>'
     f'<div class="t huge accent" style="top:650px">{R("q2","APA?")}</div>'
     f'<div class="t big" style="top:850px">{R("q3","dalam sabun")}</div>'
     f'<div class="t big" style="top:970px">{R("q4","mandi anda")}</div>'
     '<div class="ring" id="rq" style="left:55px;top:640px;width:440px;height:210px"></div>'
     '<div class="hair" id="hq" style="left:90px;width:900px;top:1130px"></div>')
A('tl.fromTo("#s1",{clipPath:"inset(0% 0% 0% 100%)"},{clipPath:"inset(0% 0% 0% 0%)",duration:0.5,ease:"expo.inOut"},1.94);')
rv("#q0", 2.0); rv("#q1", 2.24); rv("#q2", 2.52, 0.5); rv("#q3", 2.92); rv("#q4", 3.34); line("#hq", 3.0, 1.0)
A('tl.fromTo("#rq",{scale:0,rotation:-90},{scale:1,rotation:0,duration:0.6,ease:"back.out(1.8)"},2.62);')

# ---- S2 3.92-5.82: product reveal
clip("bg2", 3.92, 1.9, '<div class="ivory grid"></div>', style="z-index:2")
vid("v_prod", "assets/product/duo_marble.jpg", 3.92, 1.9, (190, 360, 700, 900))
html[-1] = html[-1].replace('<video id="v_prod"', '<img id="v_prod"').replace('data-media-start="0" muted playsinline', 'alt=""').replace('></video>', '>')
clip("s2", 3.92, 1.9, f'<div class="t c kick" style="top:250px">{R("p0","Introducing")}</div>'
     f'<div class="t c" style="top:1320px;font:600 46px Montserrat;letter-spacing:14px">{R("p1","FRESCURA BODY")}</div>'
     f'<div class="t c serif-it" style="top:1385px;font-size:52px;color:var(--mute)">{R("p2","gentle foaming body shower")}</div>')
rv("#p0", 4.0); rv("#p1", 4.3); rv("#p2", 4.7)
sect(1, 3.92, 1.9, "PRODUK")

# ---- S3 5.82-10.50: formula, educational
clip("bg3", 5.82, 4.68, '<div class="ivory"></div>', style="z-index:2")
clip("s3", 5.82, 4.68, f'<div class="t kick" style="top:300px">{R("f0","Formula")}</div>'
     f'<div class="t mid" style="top:380px;color:var(--mute)">{R("f1","Tanpa")}</div>'
     '<div class="t" style="top:450px"><span style="position:relative;display:inline-block" class="big">'
     f'{R("f2","Paraben")}<i class="strike" id="sk1"></i></span></div>'
     f'<div class="t" style="top:575px;font:italic 500 34px Playfair;color:var(--mute)">{R("f3","*Paraben: sejenis bahan pengawet")}</div>'
     f'<div class="t mid" style="top:700px;color:var(--mute)">{R("f4","Tanpa")}</div>'
     '<div class="t" style="top:770px"><span style="position:relative;display:inline-block" class="big">'
     f'{R("f5","Bahan")}<i class="strike" id="sk2"></i></span></div>'
     '<div class="t" style="top:890px"><span style="position:relative;display:inline-block" class="big">'
     f'{R("f6","Berbahaya")}<i class="strike" id="sk3"></i></span></div>'
     f'<div class="t" style="top:1020px;font:500 40px Montserrat;letter-spacing:4px">{R("f7","yang dilarang dalam kosmetik")}</div>')
rv("#f0", 5.85); rv("#f1", 5.82); rv("#f2", 6.32); line("#sk1", 6.75, 0.5); rv("#f3", 7.0)
rv("#f4", 7.48); rv("#f5", 7.90); rv("#f6", 8.20); line("#sk2", 8.7, 0.4); line("#sk3", 8.85, 0.5); rv("#f7", 9.16)
vid("v_lab", "assets/broll/lab.mp4", 5.82, 4.68, (600, 1120, 380, 380), cls="circle")
sect(2, 5.82, 4.68, "FORMULA")

# ---- S4 10.50-13.88: lab tested
clip("bg4", 10.5, 3.38, '<div class="ivory"></div>', style="z-index:2")
vid("v_sci", "assets/broll/scientist.mp4", 10.5, 3.38, (90, 330, 900, 1125))
clip("s4", 10.5, 3.38, f'<div class="t kick" style="top:230px">{R("l0","Telah menjalani")}</div>'
     '<div class="hair" id="scan" style="left:90px;width:900px;top:330px;height:3px;background:#fff;box-shadow:0 0 30px #fff"></div>'
     f'<div class="badge" id="bd" style="left:660px;top:1240px">{CHECK}UJIAN<br>MAKMAL</div>')
rv("#l0", 10.56)
A('tl.fromTo("#scan",{y:0,opacity:1},{y:1100,opacity:0.2,duration:1.6,ease:"power1.inOut"},10.9);')
pop("#bd", 12.34, 0.6)
A('tl.to("#ck",{strokeDashoffset:0,duration:0.5,ease:"power2.out"},12.8);')
sect(3, 10.5, 3.38, "KESELAMATAN")

# ---- S5 13.88-16.30: foaming
clip("bg5", 13.88, 2.42, '<div class="ivory"></div>', style="z-index:2")
vid("v_foam", "assets/broll/pump_foam.mp4", 13.88, 2.42, (190, 560, 700, 700), cls="circle", media="0.6")
clip("s5", 13.88, 2.42, f'<div class="t c kick" style="top:330px">{R("o0","Yang best-nya")}</div>'
     f'<div class="t c big" style="top:390px">{R("o1","jenis")}</div>'
     f'<div class="t c huge" style="top:1320px">{R("o2","FOAMING")}</div>'
     '<div class="ring" id="o3" style="left:150px;top:520px;width:780px;height:780px"></div>'
     '<div class="ring" id="o4" style="left:110px;top:480px;width:860px;height:860px;opacity:.4"></div>')
rv("#o0", 13.92); rv("#o1", 15.2); rv("#o2", 15.52, 0.6)
A('tl.fromTo("#o3,#o4",{scale:0.6,opacity:0},{scale:1,opacity:1,duration:0.9,stagger:0.12,ease:"expo.out"},13.95);')
sect(4, 13.88, 2.42, "FOAMING PUMP")

# ---- S6 16.30-18.66: real pump press on ivory backdrop
full("v_press", "assets/broll/pump_press.mp4", 16.30, 2.36, 1.08, 1.0)
clip("s6", 16.30, 2.36, '<div id="c1" class="callout" style="left:610px;top:858px"><div class="d"></div><div class="l"></div>'
     '<div class="x">1× TEKAN<small>terus keluar</small></div></div>'
     '<div id="c2" class="callout" style="left:770px;top:1180px"><div class="x">BUIH<br>LEMBUT</div></div>')
pop("#c1 .d", 16.5, 0.4); line("#c1 .l", 16.6, 0.6); fade("#c1 .x", 16.8, 0.5, 0, -10); fade("#c2 .x", 17.72, 0.6, 20)

# ---- S7 18.66-20.80: two scents split
clip("s7", 18.66, 2.14, '<div class="ivory"></div>'
     '<div class="block" id="b1" style="left:0;top:0;width:540px;height:1920px;background:var(--rose)"></div>'
     '<div class="block" id="b2" style="left:540px;top:0;width:540px;height:1920px;background:var(--violet)"></div>'
     f'<div class="t c" style="top:640px;font:200 340px/1 Montserrat;color:#fff;letter-spacing:-10px">{R("w0","02")}</div>'
     f'<div class="t c kick" style="top:1010px;color:#fff;letter-spacing:12px">{R("w1","Pilihan wangian")}</div>')
A('tl.fromTo("#b1",{yPercent:-100},{yPercent:0,duration:0.7,ease:"expo.inOut"},18.7);')
A('tl.fromTo("#b2",{yPercent:100},{yPercent:0,duration:0.7,ease:"expo.inOut"},18.78);')
rv("#w0", 19.76, 0.6); rv("#w1", 19.94)
sect(5, 18.66, 9.24, "WANGIAN")

# ---- S8 20.80-24.48: Woman Glory
clip("bg8", 20.80, 3.68, '<div class="ivory"></div>', style="z-index:2")
vid("v_g", "assets/product/glory_card.jpg", 20.80, 3.68, (560, 420, 430, 1100))
html[-1] = html[-1].replace('<video id="v_g"', '<img id="v_g"').replace('data-media-start="0" muted playsinline', 'alt=""').replace('></video>', '>')
vid("v_rose", "assets/broll/rose.mp4", 20.80, 3.68, (90, 420, 380, 380), cls="circle")
clip("s8", 20.80, 3.68, f'<div class="t kick" style="top:300px">{R("g0","No. 01")}</div>'
     f'<div class="t" style="top:880px;font:300 96px/1 Montserrat;letter-spacing:-1px">{R("g1","WOMAN")}<br>{R("g2","GLORY")}</div>'
     f'<div class="t serif-it accent" style="top:1090px;font-size:60px">{R("g3","by Bombshell")}</div>'
     '<div class="t" style="top:1220px;right:auto;width:480px"><div class="chip" id="g4"><i></i>FRESH</div><div class="chip" id="g5"><i></i>FLORAL</div></div>')
rv("#g0", 20.85); rv("#g1", 20.82); rv("#g2", 20.89); rv("#g3", 21.0); fade("#g4", 23.14, 0.5, 0, -30); fade("#g5", 23.76, 0.5, 0, -30)

# ---- S9 24.48-27.90: Noche
clip("bg9", 24.48, 3.42, '<div class="ivory"></div>', style="z-index:2")
vid("v_n", "assets/product/noche_card.jpg", 24.48, 3.42, (560, 420, 420, 1107))
html[-1] = html[-1].replace('<video id="v_n"', '<img id="v_n"').replace('data-media-start="0" muted playsinline', 'alt=""').replace('></video>', '>')
vid("v_star", "assets/broll/stars.mp4", 24.48, 3.42, (90, 420, 380, 380), cls="circle")
clip("s9", 24.48, 3.42, f'<div class="t kick" style="top:300px">{R("n0","No. 02")}</div>'
     f'<div class="t" style="top:880px;font:300 96px/1 Montserrat;letter-spacing:-1px">{R("n1","NOCHE")}</div>'
     f'<div class="t serif-it" style="top:990px;right:auto;width:450px;font-size:48px;line-height:1.15;color:var(--violet)">{R("n2","by Midnight")}<br>{R("n2b","Fantasy")}</div>'
     '<div class="t" style="top:1220px;right:auto;width:480px"><div class="chip v" id="n3"><i></i>SWEET</div><div class="chip v" id="n4"><i></i>FRUITY</div></div>')
rv("#n0", 24.49); rv("#n1", 24.50); rv("#n2", 24.622); rv("#n2b", 24.795); fade("#n3", 26.56, 0.5, 0, -30); fade("#n4", 27.14, 0.5, 0, -30)

# ---- S10 27.90-31.70: choose your favourite (selection UI on the real photo)
full("ph_sel", "assets/product/duo_marble.jpg", 27.90, 3.8, 1.06, 1.0, tag="img")
clip("s10", 27.90, 3.8, '<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(243,238,230,.95) 0%,rgba(243,238,230,0) 24%)"></div>'
     f'<div class="t c kick" style="top:150px">{R("s0","Pilih je")}</div>'
     f'<div class="t c serif-it" style="top:205px">{R("s1","kegemaran anda")}</div>'
     '<div class="sel" id="selA" style="left:120px;top:400px;width:440px;height:1180px"></div>'
     '<div class="sel" id="selB" style="left:530px;top:400px;width:440px;height:1180px"></div>'
     '<div class="tap" id="tap" style="left:300px;top:1380px"></div>')
rv("#s0", 28.0); rv("#s1", 30.3, 0.8)
A('tl.fromTo("#tap",{opacity:0,scale:1.4},{opacity:1,scale:1,duration:0.3},29.4);')
A('tl.fromTo("#selA",{opacity:0,scale:1.06},{opacity:1,scale:1,duration:0.35,ease:"back.out(2)"},29.6);')
A('tl.to("#tap",{x:440,duration:0.45,ease:"power2.inOut"},30.0);')
A('tl.to("#selA",{opacity:0,duration:0.2},30.3);')
A('tl.fromTo("#selB",{opacity:0,scale:1.06},{opacity:1,scale:1,duration:0.35,ease:"back.out(2)"},30.45);')
sect(6, 27.90, 3.8, "PILIHAN")

# ---- S11 31.70-37.60: CTA
clip("bg11", 31.70, DURATION - 31.70, '<div class="ivory"></div>', style="z-index:2")
vid("v_cta", "assets/product/duo_wood.jpg", 31.70, DURATION - 31.70, (190, 300, 700, 820))
html[-1] = html[-1].replace('<video id="v_cta"', '<img id="v_cta"').replace('data-media-start="0" muted playsinline', 'alt=""').replace('></video>', '>')
clip("s11", 31.70, DURATION - 31.70, f'<div class="t c" style="top:180px;font:600 40px Montserrat;letter-spacing:16px">{R("e0","FRESCURA BODY")}</div>'
     f'<div class="btn" id="btn" style="top:1190px"><div class="bk">{BASKET}</div>TEKAN BEG KUNING</div>'
     f'<div class="t c kick" style="top:1375px;color:var(--ink)">{R("e1","Check out sekarang")}</div>'
     '<div class="bar" style="top:1450px"><i id="sb"></i></div>'
     f'<div class="t c" style="top:1475px;font:600 24px Montserrat;letter-spacing:8px;color:var(--rose)">{R("e2","STOK SANGAT TERHAD")}</div>')
rv("#e0", 31.8)
A('tl.fromTo("#btn",{opacity:0,y:60},{opacity:1,y:0,duration:0.6,ease:"expo.out"},31.76);')
rv("#e1", 32.94); rv("#e2", 34.44)
A('tl.fromTo("#sb",{scaleX:1},{scaleX:0.15,duration:2.2,ease:"power2.in"},34.44);')
A('tl.to("#btn",{scale:1.05,duration:0.18,yoyo:true,repeat:5,ease:"sine.inOut"},36.7);')

# ---- remap every scene time onto the spliced voice (captions below already use the new word times)
def _ra(m):
    s, d = float(m.group(1)), float(m.group(2))
    return f'data-start="{T(s):.3f}" data-duration="{T(s + d) - T(s):.3f}"'
html = [re.sub(r'data-start="([\d.]+)" data-duration="([\d.]+)"', _ra, h) for h in html]
js = [re.sub(r',([\d.]+)\);$', lambda m: f",{T(float(m.group(1))):.3f});", l) for l in js]
DURATION = T(DURATION)

# ---- persistent: progress bar + wordmark (hidden on the face shot)
clip("chrome", FACE_END, DURATION - FACE_END, '<div id="prog"></div>', style="z-index:8")
A(f'tl.fromTo("#prog",{{scaleX:0}},{{scaleX:1,duration:{DURATION-FACE_END:.2f},ease:"none"}},{FACE_END});')

# ---- captions (pill)
for ci, ch in enumerate(chunks):
    st = ch[0]["s"]
    if st < 1.9 or 1.9 <= st < 3.9:     # face shot + hook question carry their own on-screen type
        continue
    nxt = chunks[ci + 1][0]["s"] if ci + 1 < len(chunks) else DURATION
    en = min(nxt, ch[-1]["e"] + 0.45) if nxt - ch[-1]["e"] > 0.6 else nxt
    sp = []
    for wi, w in enumerate(ch):
        key = re.sub(r"[^a-z\-]", "", w["t"].lower())
        sp.append(f'<span id="w{ci}_{wi}" class="w{" hl" if any(k in HL for k in key.split()) or key in HL else ""}">{w["t"].rstrip(".,?")}</span>')
        A(f'tl.fromTo("#w{ci}_{wi}",{{opacity:0.35}},{{opacity:1,duration:0.15}},{w["s"]:.2f});')
    clip(f"cap{ci}", st, max(en - st, 0.2), '<span class="pill">' + " ".join(sp) + "</span>", cls="cap")
    A(f'tl.fromTo("#cap{ci} .pill",{{y:20,opacity:0}},{{y:0,opacity:1,duration:0.25,ease:"power3.out"}},{st:.2f});')

CSS = open(f"{proj}/style.css").read()
pv = "" if FINAL else '<div class="pv">PREVIEW</div>'
page = f"""<!doctype html>
<html lang="ms" data-resolution="portrait"><head><meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
{CSS}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DURATION}" data-width="1080" data-height="1920">
<audio id="mix" class="clip" src="assets/audio/mix.wav" data-start="0" data-duration="{DURATION}" data-volume="1"></audio>
{chr(10).join(html)}
<div id="flash"></div>{pv}
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines["main"] = tl;
tl.seek(0);
</script></body></html>
"""
open(f"{proj}/index.html", "w").write(page)
print(len(chunks), "caption chunks,", len(js), "tweens")
