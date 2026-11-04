"""Video 2 (luxury / corporate): build project/index.html from the edited voice's word timestamps.
Usage: python3 -I build.py PROJECT_DIR [--final]"""
import json, re, sys

proj = sys.argv[1]
FINAL = "--final" in sys.argv
DURATION = 58.9
BRAND = "FRESCURA BODY"

words = [w for s in json.load(open(f"{proj}/assets/audio/words.json")) for w in s["words"]]
FIX = {"Lalu": "Selalu", "bahagia": "bahagia", "ke": "", "rework": "reward", "Fresh": "Frescura", "Kura": "",
       "Bodi": "Body", "dia": "dia", "gulit": "kulit", "noce": "Noche", "feminin": "feminine", "seduktif": "seductive",
       "make": "beg", "money": "kuning", "dapat": "dapatkan", "Kura@": ""}
CTX = {  # context-specific fixes: (word, start-window) -> replacement ("" = drop)
    ("bahagia", 0.0, 1.0): "bahagiakan", ("ke", 0.9, 1.2): "",
    ("dia", 23.0, 23.3): "", ("dia", 51.3, 51.6): "diri",
}
HL = {"bahagiakan", "sayang", "sibuk", "sendiri", "reward", "frescura", "body", "foaming", "pump", "buih", "lembut",
      "bersih", "segar", "wangian", "dua", "woman", "glory", "fresh", "floral", "feminine", "noche", "sweet", "fruity",
      "seductive", "komen", "layak", "bahagia", "dihargai", "hadiah", "manjakan", "kegemaran", "beg", "kuning", "terhad"}

clean = []
for w in words:
    if w["s"] > 58.45:           # whisper hallucination on the room tone after the last word
        continue
    txt = w["w"].strip()
    rep = None
    for (k, a, b), v in CTX.items():
        if txt.rstrip(".,") == k and a <= w["s"] <= b:
            rep = v
    if rep is None:
        core = txt.rstrip(".,?")
        tail = txt[len(core):]
        rep = (FIX.get(core, core) + tail) if FIX.get(core, core) != "" else ""
    if rep == "":
        continue
    if rep.startswith("-") and clean:
        clean[-1]["t"] += rep; clean[-1]["e"] = w["e"]; continue
    clean.append({"t": rep, "s": w["s"], "e": w["e"]})

chunks, cur = [], []
for i, w in enumerate(clean):
    cur.append(w)
    nxt = clean[i + 1] if i + 1 < len(clean) else None
    if (len(cur) >= 4 or re.search(r"[.,?!]$", w["t"]) or nxt is None or nxt["s"] - w["e"] > 0.3
            or len(" ".join(x["t"] for x in cur)) > 22):
        chunks.append(cur); cur = []

html, js = [], []
def A(l): js.append(l)
_seen = set()
def IR(sel):
    if sel in _seen: return ",immediateRender:false"
    _seen.add(sel); return ""
def clip(id_, s, d, inner="", cls="", style=""):
    html.append(f'<div id="{id_}" class="clip {cls}" data-start="{s:.3f}" data-duration="{d:.3f}" style="{style}">{inner}</div>')
def video(id_, src, s, d, z0=1.12, z1=1.0, cls="bg", fade=0.35, style=""):
    html.append(f'<video id="{id_}" class="clip {cls}" src="{src}" data-start="{s:.3f}" data-duration="{d:.3f}" '
                f'data-media-start="0" muted playsinline style="{style}"></video>')
    A(f'tl.fromTo("#{id_}",{{scale:{z0}}},{{scale:{z1},duration:{d:.2f},ease:"power1.out"}},{s});')
    if fade:
        A(f'tl.fromTo("#{id_}",{{opacity:0}},{{opacity:1,duration:{fade}}},{s});')
def photo(id_, src, s, d, z0=1.15, z1=1.02, pos="50% 50%"):
    html.append(f'<img id="{id_}" class="clip bg" src="{src}" data-start="{s:.3f}" data-duration="{d:.3f}" '
                f'style="object-position:{pos}" alt="">')
    A(f'tl.fromTo("#{id_}",{{scale:{z0}}},{{scale:{z1},duration:{d:.2f},ease:"power1.out"}},{s});')
    A(f'tl.fromTo("#{id_}",{{opacity:0}},{{opacity:1,duration:0.35}},{s});')
def leak(s, d=1.6, peak=0.75):
    i = len(html)
    html.append(f'<video id="lk{i}" class="clip leak" src="assets/broll/leak.mp4" data-start="{s:.3f}" '
                f'data-duration="{d:.3f}" data-media-start="0" muted playsinline></video>')
    A(f'tl.fromTo("#lk{i}",{{opacity:0}},{{opacity:{peak},duration:{d/2:.2f},yoyo:true,repeat:1,ease:"sine.inOut"}},{s});')
def flash(t, k=0.35):
    A(f'tl.fromTo("#flash",{{opacity:{k}}},{{opacity:0,duration:0.5,ease:"power2.out",immediateRender:false}},{t:.2f});')
def reveal(sel, t, d=0.8):  # text rises out of a mask
    A(f'tl.fromTo("{sel} > span",{{yPercent:110}},{{yPercent:0,duration:{d},ease:"expo.out"}},{t:.2f});')
def fade(sel, t, d=0.7, y=30):
    A(f'tl.fromTo("{sel}",{{opacity:0,y:{y}}},{{opacity:1,y:0,duration:{d},ease:"power3.out"}},{t:.2f});')
def out_(sel, t, d=0.4):
    A(f'tl.to("{sel}",{{opacity:0,duration:{d},ease:"power2.in"}},{t:.2f});')
def rule(id_, top, t):
    html_ = f'<div id="{id_}" class="rule" style="top:{top}px"></div>'
    A(f'tl.fromTo("#{id_}",{{scaleX:0}},{{scaleX:1,duration:0.9,ease:"expo.out"}},{t:.2f});')
    return html_
def R(id_, text, cls=""):
    return f'<span id="{id_}" class="rv {cls}"><span>{text}</span></span>'
STAR = ('<svg viewBox="0 0 100 100"><path d="M50 0C54 40 60 46 100 50C60 54 54 60 50 100C46 60 40 54 0 50C40 46 46 40 50 0Z" '
        'fill="#fff3d6"/></svg>')
def sparkle(prefix, t, pts):
    for i, (x, y, s) in enumerate(pts):
        html.append(f'<div id="{prefix}{i}" class="spk" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px">{STAR}</div>')
        A(f'tl.fromTo("#{prefix}{i}",{{scale:0,rotation:0,opacity:1}},{{scale:1,rotation:45,duration:0.5,ease:"back.out(2)"}},{t+i*0.12:.2f});')
        A(f'tl.to("#{prefix}{i}",{{scale:0,opacity:0,duration:0.5}},{t+0.7+i*0.12:.2f});')
BASKET = ('<svg viewBox="0 0 120 110"><path d="M38 40 L52 10 M82 40 L68 10" stroke="#1a1209" stroke-width="7" '
          'stroke-linecap="round"/><path d="M8 40 H112 L100 100 H20 Z" fill="#1a1209"/><path d="M42 56 V86 M60 56 V86 M78 56 V86" '
          'stroke="#d6b57a" stroke-width="6" stroke-linecap="round"/></svg>')
HEART = '<svg class="hrt" viewBox="0 0 100 90"><path d="M50 88 C10 60 0 40 0 25 C0 10 12 0 26 0 C38 0 46 8 50 16 C54 8 62 0 74 0 C88 0 100 10 100 25 C100 40 90 60 50 88Z" fill="#d6b57a"/></svg>'

# ============================== scenes (voice timeline) ==============================
# S0 0.00-3.96 HOOK on the hero product shot
photo("ph_hero", "assets/product/hero_foam.jpg", 0.0, 1.84, 1.28, 1.08, "50% 38%")
leak(0.0, 2.0, 0.8)
clip("s0", 0.0, 1.84, '<div class="shade"></div>'
     f'<div class="line it" style="top:300px;font-size:64px;color:#efe6d6">{R("h0a","Selalu sangat kita")}</div>'
     f'<div class="line serif" style="top:380px;font-size:104px;letter-spacing:4px">{R("h0b","BAHAGIAKAN")}</div>'
     f'<div class="line serif" style="top:500px;font-size:104px;letter-spacing:4px">{R("h0c","ORANG LAIN")}</div>'
     + rule("r0", 650, 1.2))
reveal("#h0a", 0.05); reveal("#h0b", 0.5); reveal("#h0c", 1.0)
# 1.84-3.89 the only 2 s of face: straight to camera, the hook's punchline
video("v_face", "assets/broll/face.mp4", 1.84, 2.05, 1.08, 1.0, fade=0.15)
clip("s0b", 1.84, 2.05, '<div class="shade" style="background:linear-gradient(180deg,rgba(8,6,4,0) 50%,rgba(8,6,4,.85) 100%)"></div>'
     f'<div class="line it" style="top:1250px;font-size:64px;color:#efe6d6">{R("h0d","tapi diri sendiri...")}</div>'
     f'<div class="line serif gold" style="top:1330px;font-size:92px;font-style:italic">{R("h0e","tak pernah disayang?")}</div>')
reveal("#h0d", 2.06); reveal("#h0e", 2.94, 0.9)

# persistent corporate frame + brand mark from 3.96 on
clip("chrome", 3.89, DURATION - 3.89, f'<div class="frame"><i></i><i></i><i></i><i></i></div>'
     f'<div class="mark">{BRAND}</div>', style="z-index:8")
A('tl.fromTo("#chrome",{opacity:0},{opacity:1,duration:0.8},3.89);')

# S1 3.98-7.46 busy triptych (desaturated)
for i, (n, t0, lab, tl_) in enumerate([("busy_type", 4.0, "KERJA", 5.06), ("busy_kitchen", 4.35, "RUMAH", 6.32),
                                         ("busy_family", 4.7, "KELUARGA", 6.96)]):
    top = i * 640
    html.append(f'<video id="v_{n}" class="clip panel-v" src="assets/broll/{n}.mp4" data-start="{t0:.3f}" '
                f'data-duration="{7.46-t0:.3f}" data-media-start="0" muted playsinline style="top:{top}px"></video>')
    A(f'tl.fromTo("#v_{n}",{{clipPath:"inset(0% 100% 0% 0%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:0.8,ease:"expo.inOut"}},{t0});')
    clip(f"pl{i}", tl_, 7.46 - tl_, f'<div class="plabel" style="top:{top+500}px">{lab}</div>')
    fade(f"#pl{i} .plabel", tl_, 0.6, 20)
html.append('<div id="pls" class="clip" data-start="4.000" data-duration="3.460" style="z-index:3">'
            '<div class="pline" style="top:639px"></div><div class="pline" style="top:1279px"></div></div>')

# S2 7.48-10.72 hourglass
video("v_hour", "assets/broll/hourglass.mp4", 7.46, 3.28)
clip("s2", 7.46, 3.28, '<div class="shade"></div>'
     f'<div class="line it" style="top:330px;font-size:60px;color:#efe6d6">{R("t2a","Sampai terlupa...")}</div>'
     f'<div class="line serif" style="top:1150px;font-size:76px;letter-spacing:6px">{R("t2b","MASA UNTUK")}</div>'
     f'<div class="line serif gold" style="top:1245px;font-size:96px;font-style:italic">{R("t2c","diri sendiri")}</div>')
reveal("#t2a", 8.0); reveal("#t2b", 9.26); reveal("#t2c", 9.88)

# S3 10.74-12.06 candles: the turn
video("v_cand", "assets/broll/candles.mp4", 10.72, 2.84)
leak(10.6, 1.4, 0.6)
clip("s3", 10.72, 2.84, '<div class="shade"></div>'
     f'<div class="line it" style="top:700px;font-size:68px;color:#fff">{R("t3a","Apa kata sekali-sekala...")}</div>'
     f'<div class="line kick" style="top:860px">{R("t3b","REWARD YOURSELF")}</div>'
     f'<div class="line serif gold" style="top:920px;font-size:110px;font-style:italic">{R("t3c","hadiahkan diri")}</div>')
reveal("#t3a", 10.8); reveal("#t3b", 12.2, 0.6); reveal("#t3c", 12.48, 1.0)
sparkle("sp3_", 12.9, [(180, 900, 46), (860, 1040, 40)])

# S5 14.06-15.00 product reveal: light sweep + lockup
photo("ph_diag", "assets/product/duo_diag.jpg", 13.56, 1.44, 1.12, 1.03)
clip("s5", 13.56, 1.44, '<div class="shade full" style="background:rgba(8,6,4,.62)"></div><div id="sw5" class="sweep"></div>'
     f'<div class="lockup" style="top:820px"><div class="brand gold">{R("l5a","FRESCURA")}</div>'
     f'<div class="sub">{R("l5b","GENTLE FOAMING BODY SHOWER")}</div></div>')
flash(13.56, 0.5)
A('tl.fromTo("#sw5",{x:-900},{x:900,duration:1.2,ease:"power2.inOut"},13.6);')
reveal("#l5a", 13.65, 0.8); reveal("#l5b", 14.0, 0.7)

# S6 15.00-20.30 real pump press, background replaced
video("v_press", "assets/broll/pump_press.mp4", 15.0, 5.3, 1.08, 1.0)
clip("s6", 15.0, 5.3, '<div class="shade" style="opacity:.6"></div>'
     '<div id="c6a" class="callout" style="left:610px;top:858px"><div class="dot"></div><div class="ln"></div>'
     '<div class="tx">FOAMING<small>pump</small></div></div>'
     '<div id="c6b" class="callout" style="left:770px;top:1180px"><div class="tx">BUIH<br>LEMBUT<small>terus dari botol</small></div></div>')
A('tl.fromTo("#c6a .dot",{scale:0},{scale:1,duration:0.4,ease:"back.out(3)"},16.66);')
A('tl.fromTo("#c6a .ln",{scaleX:0},{scaleX:1,duration:0.6,ease:"expo.out"},16.76);')
fade("#c6a .tx", 16.96, 0.6, 0)
fade("#c6b .tx", 18.22, 0.8, 20)

# S7 20.32-25.62 foam close-up -> water; benefit list
video("v_foam", "assets/broll/pump_foam.mp4", 20.30, 2.4, 1.1, 1.0)
video("v_show", "assets/broll/shower.mp4", 22.70, 2.94)
clip("s7", 20.30, 5.34, '<div class="shade full"></div><div class="blist">'
     '<div class="kick" id="k7" style="margin-bottom:20px">LEPAS MANDI</div>'
     '<div class="bi" id="b7a"><b>01</b><span>BERSIH</span><em>badan segar</em></div>'
     '<div class="bi" id="b7b"><b>02</b><span>LEMBUT</span><em>kulit terasa halus</em></div>'
     '<div class="bi" id="b7c"><b>03</b><span>SEGAR</span><em>sepanjang hari</em></div></div>')
fade("#k7", 20.4, 0.6, 0)
for sel, t0 in (("#b7a", 22.12), ("#b7b", 24.12), ("#b7c", 25.04)):
    A(f'tl.fromTo("{sel}",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.7,ease:"expo.out"}},{t0});')

# S8 25.66-28.40 fragrance: smoke
video("v_smoke", "assets/broll/smoke.mp4", 25.64, 2.78)
clip("s8", 25.64, 2.78, f'<div class="line kick" style="top:700px">{R("t8a","DITAMBAH PULA")}</div>'
     f'<div class="line serif gold" style="top:780px;font-size:150px;font-style:italic">{R("t8b","Wangian")}</div>'
     f'<div class="line it" style="top:970px;font-size:64px;color:#efe6d6">{R("t8c","yang menyenangkan")}</div>')
reveal("#t8a", 25.7); reveal("#t8b", 26.5, 1.0); reveal("#t8c", 27.38)
sparkle("sp8_", 26.9, [(230, 760, 50), (820, 900, 40), (700, 720, 60)])

# S9 28.42-29.54 two signature scents
photo("ph_wood", "assets/product/duo_wood.jpg", 28.42, 1.12, 1.12, 1.04)
clip("s9", 28.42, 1.12, '<div class="shade"></div>'
     f'<div class="line kick" style="top:250px">{R("t9a","2 SIGNATURE SCENTS")}</div>'
     f'<div class="line serif" style="top:310px;font-size:84px">{R("t9b","Dua Pilihan")}</div>')
reveal("#t9a", 28.45, 0.5); reveal("#t9b", 28.72, 0.6)

# S10 29.54-35.48 Woman Glory
video("v_rose", "assets/broll/rose.mp4", 29.54, 5.94)
clip("s10", 29.54, 5.94, '<div class="shade full"></div>'
     '<div class="stitle"><div class="n">I · SIGNATURE</div>'
     f'<div class="t">{R("t10a","Woman")}<br>{R("t10b","Glory")}</div><div class="s">{R("t10c","Bombshell")}</div></div>'
     '<div id="cg" class="card" style="left:640px;top:520px;width:360px;height:919px"><img src="assets/product/glory_card.jpg" alt=""></div>'
     '<div class="notes"><div class="note" id="n10a">FRESH</div><div class="note" id="n10b">FLORAL</div>'
     '<div class="note" id="n10c">FEMININE</div></div>')
fade("#s10 .n", 29.6, 0.6, 0); reveal("#t10a", 30.48); reveal("#t10b", 30.7); reveal("#t10c", 31.1)
A('tl.fromTo("#cg",{opacity:0,y:120},{opacity:1,y:0,duration:1.2,ease:"expo.out"},29.8);')
for sel, t0 in (("#n10a", 32.98), ("#n10b", 33.70), ("#n10c", 34.42)):
    A(f'tl.fromTo("{sel}",{{opacity:0,x:-40}},{{opacity:1,x:0,duration:0.6,ease:"expo.out"}},{t0});')

# S11 35.52-41.42 Noche
video("v_stars", "assets/broll/stars.mp4", 35.48, 5.96)
clip("s11", 35.48, 5.96, '<div class="shade full"></div>'
     '<div class="stitle"><div class="n">II · SIGNATURE</div>'
     f'<div class="t">{R("t11a","Noche")}</div><div class="s">{R("t11b","Midnight Fantasy")}</div></div>'
     '<div id="cn" class="card" style="left:640px;top:520px;width:350px;height:923px"><img src="assets/product/noche_card.jpg" alt=""></div>'
     '<div class="notes" style="top:760px"><div class="note" id="n11a">SWEET</div><div class="note" id="n11b">FRUITY</div>'
     '<div class="note" id="n11c">SEDUCTIVE</div></div>')
fade("#s11 .n", 35.55, 0.6, 0); reveal("#t11a", 36.26); reveal("#t11b", 36.7)
A('tl.fromTo("#cn",{opacity:0,y:120},{opacity:1,y:0,duration:1.2,ease:"expo.out"},35.7);')
for sel, t0 in (("#n11a", 39.28), ("#n11b", 39.80), ("#n11c", 40.32)):
    A(f'tl.fromTo("{sel}",{{opacity:0,x:-40}},{{opacity:1,x:0,duration:0.6,ease:"expo.out"}},{t0});')

# S12 41.46-43.56 comment prompt
video("v_bok", "assets/broll/bokeh.mp4", 41.44, 2.14)
clip("s12", 41.44, 2.14, '<div class="shade full"></div>'
     f'<div class="line kick" style="top:420px">{R("t12a","KOMEN PILIHAN ANDA")}</div>'
     f'<div class="cm" id="cm1" style="top:640px"><div class="av r"></div><div><div class="who">PILIHAN 1</div>'
     f'<div class="msg">Woman Glory</div></div>{HEART}</div>'
     f'<div class="cm" id="cm2" style="top:840px"><div class="av v"></div><div><div class="who">PILIHAN 2</div>'
     f'<div class="msg">Noche</div></div>{HEART}</div>')
reveal("#t12a", 41.5, 0.6)
A('tl.fromTo("#cm1",{opacity:0,y:60},{opacity:1,y:0,duration:0.6,ease:"expo.out"},42.0);')
A('tl.fromTo("#cm2",{opacity:0,y:60},{opacity:1,y:0,duration:0.6,ease:"expo.out"},42.46);')
A('tl.fromTo("#cm1 .hrt,#cm2 .hrt",{scale:0},{scale:1,duration:0.4,stagger:0.25,ease:"back.out(3)"},42.9);')

# S13 43.58-47.78 you deserve it
video("v_candle", "assets/broll/candle.mp4", 43.56, 2.5)
video("v_cand2", "assets/broll/candles.mp4", 46.06, 1.72)
clip("s13", 43.56, 4.22, '<div class="shade"></div>'
     f'<div class="line it" style="top:520px;font-size:64px;color:#efe6d6">{R("t13a","Ingat,")}</div>'
     f'<div class="line serif" style="top:620px;font-size:110px">{R("t13b","Anda Layak")}</div>'
     + rule("r13", 780, 45.4) +
     f'<div class="line serif gold" style="top:820px;font-size:100px;font-style:italic">{R("t13c","dihargai.")}</div>')
reveal("#t13a", 43.6); reveal("#t13b", 44.72); reveal("#t13c", 47.08, 1.0)
leak(46.9, 1.4, 0.55)

# S14 47.80-50.24 gift
video("v_gift", "assets/broll/gift.mp4", 47.78, 2.48)
clip("s14", 47.78, 2.48, '<div class="shade"></div>'
     f'<div class="line it" style="top:330px;font-size:62px;color:#efe6d6">{R("t14a","Jangan tunggu orang lain")}</div>'
     f'<div class="line serif" style="top:410px;font-size:96px">{R("t14b","belikan hadiah")}</div>')
reveal("#t14a", 47.85); reveal("#t14b", 49.16)

# S15 50.28-52.32 pamper yourself
video("v_tea", "assets/broll/tealights.mp4", 50.26, 2.08)
clip("s15", 50.26, 2.08, '<div class="shade"></div>'
     f'<div class="line kick" style="top:760px">{R("t15a","SESEKALI")}</div>'
     f'<div class="line serif gold" style="top:830px;font-size:120px;font-style:italic">{R("t15b","Manjakan Diri")}</div>')
reveal("#t15a", 50.3); reveal("#t15b", 51.04, 1.0)
sparkle("sp15_", 51.5, [(160, 820, 50), (880, 960, 44)])

# S16 52.34-54.92 choose your favourite
photo("ph_marble", "assets/product/duo_marble.jpg", 52.34, 2.6, 1.12, 1.0)
clip("s16", 52.34, 2.6, '<div class="shade"></div>'
     f'<div class="line kick" style="top:200px">{R("t16a","PILIH KEGEMARAN ANDA")}</div>'
     f'<div class="line serif gold" style="top:250px;font-size:84px">{R("t16b","Frescura Body")}</div>')
reveal("#t16a", 52.4, 0.6); reveal("#t16b", 53.26, 0.9)

# S17 54.94-58.90 CTA + end lockup
photo("ph_cta", "assets/product/hero_foam.jpg", 54.92, DURATION - 54.92, 1.0, 1.1, "50% 40%")
clip("s17", 54.92, DURATION - 54.92, '<div class="shade full" style="background:rgba(8,6,4,.74)"></div>'
     f'<div class="lockup" style="top:420px"><div class="brand gold" style="font-size:84px">{R("l17a","FRESCURA")}</div>'
     f'<div class="sub">{R("l17b","BODY · GENTLE FOAMING")}</div></div>'
     f'<div id="btn" class="btn" style="top:900px">{BASKET}TEKAN BEG KUNING</div>'
     '<div class="stock" id="stk" style="top:1100px"><i></i>STOK TERHAD · DAPATKAN SEKARANG</div>')
leak(54.9, 1.8, 0.7)
reveal("#l17a", 55.0, 0.9); reveal("#l17b", 55.3, 0.7)
A('tl.fromTo("#btn",{opacity:0,scale:0.85},{opacity:1,scale:1,duration:0.8,ease:"expo.out"},55.26);')
A('tl.to("#btn",{scale:1.04,duration:0.5,yoyo:true,repeat:3,ease:"sine.inOut"},56.2);')
fade("#stk", 57.02, 0.6, 10)
A('tl.to("#stk i",{opacity:0.2,duration:0.3,yoyo:true,repeat:5},57.5);')

# ============================== captions ==============================
for ci, ch in enumerate(chunks):
    st = ch[0]["s"]
    if st < 3.9:            # the hook headlines carry the opening line
        continue
    nxt = chunks[ci + 1][0]["s"] if ci + 1 < len(chunks) else DURATION
    en = min(nxt, ch[-1]["e"] + 0.5) if nxt - ch[-1]["e"] > 0.6 else nxt
    sp = []
    for wi, w in enumerate(ch):
        key = re.sub(r"[^a-z\-]", "", w["t"].lower())
        sp.append(f'<span id="w{ci}_{wi}" class="w{" hl" if key in HL else ""}">{w["t"].rstrip(".,?")}</span>')
        A(f'tl.fromTo("#w{ci}_{wi}",{{opacity:0,y:14}},{{opacity:1,y:0,duration:0.25,ease:"power2.out"}},{w["s"]:.2f});')
    clip(f"cap{ci}", st, max(en - st, 0.2), " ".join(sp), cls="cap")

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
<div class="vign"></div><div id="flash"></div>{pv}
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
