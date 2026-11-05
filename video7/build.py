"""Video 7 -- "Wanita lebih yakin: 5 perkara" in a new "Porcelain & Olive" airy minimalist-luxury style.
Instrument Serif + Outfit; per-character blur-rise type, frosted-glass cards, polaroid stacks, diagonal frames and clay swipe
transitions, odometer numerals, hand-drawn scribbles, split-scroll columns, story-segment progress, frosted captions.
Writes project/index.html (HyperFrames + GSAP) and project/assets/audio/sfx_cues.json from the voice's word times.
Usage: python3 -I build.py PROJECT_DIR [--final]"""
import json, re, sys

proj = sys.argv[1]
FINAL = "--final" in sys.argv
VOICE_END = 45.39
DURATION = 46.89

words = [w for s in json.load(open(f"{proj}/assets/audio/words.json")) for w in s["words"]]
import difflib
_old = [w for x in json.load(open(f"{proj}/assets/audio/words_scene_timeline.json")) for w in x["words"]]
_norm = lambda t: re.sub(r"[^a-z]", "", t.lower())
_m = difflib.SequenceMatcher(a=[_norm(w["w"]) for w in _old], b=[_norm(w["w"]) for w in words], autojunk=False)
_anc = [(0.0, 0.0)]
for blk in _m.get_matching_blocks():
    for k in range(blk.size):
        o, n = _old[blk.a + k], words[blk.b + k]
        _anc += [(o["s"], n["s"]), (o["e"], n["e"])]
_anc.sort(); _ao, _an = [], []
for o, n in _anc:
    if not _ao or (o > _ao[-1] and n > _an[-1]): _ao.append(o); _an.append(n)
def T(x):
    """first-cut time -> faster re-cut time (client asked for a faster, livelier read)"""
    if x >= _ao[-1]: return round(_an[-1] + (x - _ao[-1]), 3)
    i = max(k for k in range(len(_ao)) if _ao[k] <= x)
    return round(_an[i] + (x - _ao[i]) * (_an[i + 1] - _an[i]) / (_ao[i + 1] - _ao[i]), 3)
FIX = {"setiari": "setiap hari", "simiwa": "istimewa", "Gempak": "Keempat", "Fresh": "Frescura", "menggambungkan": "menggabungkan", "menginspirasi": "inspirasi",
       "bombshell": "Bombshell", "midnight": "Midnight", "fantasy": "Fantasy"}
DROP = {"Coral"}
HL = {"yakin", "5", "kebersihan", "pakaian", "selesa", "penampilan", "rumah", "masa", "mandi", "segar", "garam", "laut",
      "mineral", "frescura", "body", "sea", "salt", "perfume", "bombshell", "midnight", "fantasy", "istimewa", "keempat"}
clean = []
for w in words:
    txt = w["w"].strip(); core = txt.rstrip(".,?"); tail = txt[len(core):]
    if core in DROP: continue
    txt = FIX.get(core, core) + tail
    if txt.startswith("-") and clean:
        clean[-1]["t"] += txt; clean[-1]["e"] = w["e"]; continue
    clean.append({"t": txt, "s": w["s"], "e": w["e"]})
SECTIONS_OLD = [0.0, 5.98, 8.92, 12.28, 15.90, 18.56, 21.86, 26.56, 33.28, 39.38, VOICE_END]
SECTIONS = [T(x) for x in SECTIONS_OLD]
chunks, cur = [], []
for i, w in enumerate(clean):
    cur.append(w)
    nxt = clean[i + 1] if i + 1 < len(clean) else None
    if (len(cur) >= 3 or re.search(r"[.,?!]$", w["t"]) or nxt is None or nxt["s"] - w["e"] > 0.3
            or len(" ".join(x["t"] for x in cur)) > 18 or any(abs(nxt["s"] - c) < 0.12 for c in SECTIONS)):
        chunks.append(cur); cur = []

html, js, sfx = [], [], []
SPEED = 0.55
def _fast(l):
    return re.sub(r"duration:([\d.]+)", lambda m: f"duration:{float(m.group(1)) * SPEED:.2f}" if float(m.group(1)) <= 1.3 else m.group(0), l)
def A(l): js.append(_fast(l))
def S(t, s, g=0.6, auto=False): sfx.append({"t": round(t, 3), "sfx": s, "gain": g, "auto": auto})
def clip(id_, s, d, inner="", cls="", style=""):
    html.append(f'<div id="{id_}" class="clip {cls}" data-start="{s:.3f}" data-duration="{d:.3f}" style="{style}">{inner}</div>')
def R(id_, txt): return f'<span id="{id_}" class="rv"><span>{txt}</span></span>'
def rv(sel, t, d=0.7):
    js.append(f'tl.fromTo("{sel} > span",{{yPercent:118}},{{yPercent:0,duration:{max(d * SPEED, 0.22):.2f},ease:"expo.out"}},{t:.2f});')
    S(t, "top", 0.4, auto=True)
def fade(sel, t, d=0.6, y=24, x=0):
    js.append(f'tl.fromTo("{sel}",{{opacity:0,y:{y},x:{x}}},{{opacity:1,y:0,x:0,duration:{max(d * SPEED, 0.2):.2f},ease:"expo.out"}},{t:.2f});')
    S(t, "top", 0.32, auto=True)
def pop(sel, t, d=0.5, rot=0):
    js.append(f'tl.fromTo("{sel}",{{scale:0,rotation:{rot - 12}}},{{scale:1,rotation:{rot},duration:{max(d * 0.65, 0.22):.2f},ease:"back.out(3)"}},{t:.2f});')
    S(t, "top", 0.5, auto=True)
def CH(id_, txt):
    """Per-character spans (for the blur-rise type)."""
    return f'<span id="{id_}">' + "".join(f'<span class="ch">{c}</span>' for c in txt) + "</span>"
def chars(sel, t, stagger=0.035):
    js.append(f'tl.fromTo("{sel} .ch",{{yPercent:60,opacity:0,filter:"blur(14px)"}},{{yPercent:0,opacity:1,filter:"blur(0px)",duration:0.5,stagger:{stagger},ease:"expo.out"}},{t:.2f});')
    S(t, "top", 0.45, auto=True)
def full(id_, src, s, d, media="0", z0=1.16):
    html.append(f'<video id="{id_}" class="clip bg" src="{src}" data-start="{s:.3f}" data-duration="{d:.3f}" data-media-start="{media}" muted playsinline></video>')
    js.append(f'tl.fromTo("#{id_}",{{scale:{z0}}},{{scale:1.03,duration:0.45,ease:"expo.out"}},{s});')
    js.append(f'tl.to("#{id_}",{{scale:1.0,duration:{max(d - 0.45, 0.1):.2f},ease:"none"}},{s + 0.45:.3f});')
    S(s, "whip", 0.5, auto=True)
DIAG = "polygon(0% 0%, 100% 0%, 100% 86%, 0% 100%)"
def diag(id_, src, s, d, box, poly=DIAG, media="0"):
    """Footage framed by a diagonal edge, wiped in along the diagonal."""
    l, tp, w, h = box
    html.append(f'<video id="{id_}" class="clip" src="{src}" data-start="{s:.3f}" data-duration="{d:.3f}" data-media-start="{media}" muted playsinline '
                f'style="z-index:3;left:{l}px;top:{tp}px;width:{w}px;height:{h}px;object-fit:cover;clip-path:{poly}"></video>')
    js.append(f'tl.fromTo("#{id_}",{{clipPath:"polygon(0% 0%, 0% 0%, 0% 0%, 0% 0%)"}},{{clipPath:"{poly}",duration:0.5,ease:"expo.out"}},{s});')
    js.append(f'tl.fromTo("#{id_}",{{scale:1.15}},{{scale:1.0,duration:{d:.2f},ease:"power2.out"}},{s});')
    S(s, "whip", 0.45, auto=True)
def swipe(id_, t):
    """A clay parallelogram sweeps across the frame: the chapter transition."""
    clip(id_, t - 0.22, 0.5, '<div class="sw" style="position:absolute;top:-200px;left:0;width:1500px;height:2400px;background:var(--clay);transform:skewX(-18deg)"></div>', style="z-index:9")
    js.append(f'tl.fromTo("#{id_} .sw",{{x:-1900}},{{x:1300,duration:0.5,ease:"power3.inOut"}},{t - 0.22:.3f});')
    S(t - 0.2, "whip", 0.55)
def odo(id_, n, t, left, top, size=300, color="var(--olive)", start=0, italic=True):
    """Odometer numeral: a column of digits rolls up to n."""
    seq = [f"{k:02d}" if size < 400 else str(k) for k in range(start, n + 1)]
    lh = size * 1.12                               # tall rows: only one digit visible while rolling
    strip = "".join(f'<span style="height:{lh:.0f}px;line-height:{lh:.0f}px">{d}</span>' for d in seq)
    js.append(f'tl.fromTo("#{id_} .strip",{{y:0}},{{y:{-(len(seq) - 1) * lh:.0f},duration:0.6,ease:"expo.out"}},{t:.2f});')
    S(t, "click", 0.5); S(t + 0.3, "boom", 0.45)
    return (f'<div class="odo" id="{id_}" style="left:{left}px;top:{top}px;height:{lh:.0f}px;font:{"italic " if italic else ""}400 {size}px Instrument;color:{color}">'
            f'<div class="strip">{strip}</div></div>')
def scrib(id_, kind, left, top, w, h, t):
    paths = {"under": f"M6 {h*0.6:.0f} C {w*0.25:.0f} {h*0.25:.0f}, {w*0.55:.0f} {h*0.95:.0f}, {w-6} {h*0.4:.0f}",
             "circle": f"M{w*0.5:.0f} 8 C {w*0.95:.0f} 4, {w-4} {h*0.85:.0f}, {w*0.5:.0f} {h-6} C {w*0.08:.0f} {h-8}, 4 {h*0.3:.0f}, {w*0.55:.0f} 14"}
    js.append(f'tl.fromTo("#{id_} path",{{strokeDashoffset:1600}},{{strokeDashoffset:0,duration:0.5,ease:"power2.out"}},{t:.2f});')
    S(t, "swoosh", 0.35)
    return (f'<svg class="scrib" id="{id_}" style="left:{left}px;top:{top}px;width:{w}px;height:{h}px" viewBox="0 0 {w} {h}">'
            f'<path d="{paths[kind]}" stroke-dasharray="1600" stroke-dashoffset="1600"/></svg>')
def pola(id_, src, left, top, w, h, rot, cap=""):
    c = f'<div class="cap2">{cap}</div>' if cap else ""
    return f'<div class="pola" id="{id_}" style="left:{left}px;top:{top}px;width:{w}px;height:{h}px;transform:rotate({rot}deg)"><img src="{src}" alt="">{c}</div>'

# ======================= HOOK =======================
# S0 0.00-0.64: the only face shot (0.64 s, from the client's own recording), eyes into the lens -- "Wanita,"
html.append(f'<video id="v_face" class="clip bg" src="assets/broll/face.mp4" data-start="0" data-duration="0.640" data-media-start="0" muted playsinline style="z-index:6"></video>')
A('tl.fromTo("#v_face",{scale:1.12},{scale:1.0,duration:0.64,ease:"power2.out"},0);')
clip("s0", 0, 0.64, '<div class="shade" style="background:linear-gradient(180deg,rgba(43,42,39,0) 50%,rgba(43,42,39,.55) 100%)"></div>'
     f'<div class="t c boneclr" style="top:1230px;font:italic 400 210px/1 Instrument">{CH("h0","Wanita,")}</div>', style="z-index:7")
chars("#h0", 0.02, 0.03)
S(0.0, "boom", 0.55)

# S1 0.64-3.48: kalau nak rasa lebih YAKIN dengan diri sendiri -- confident woman, frosted card, scribble
full("v_wom", "assets/broll/woman.mp4", 0.64, 2.84)
clip("s1", 0.64, 2.84, '<div class="glass" id="g1" style="left:80px;top:1010px;width:920px;height:470px"></div>'
     f'<div class="t c eyebrow" style="top:1060px">{R("y0","Kalau nak rasa lebih")}</div>'
     f'<div class="t c serif" style="top:1120px;font-size:190px">{CH("y1","yakin")}</div>'
     + scrib("y2", "under", 300, 1300, 480, 60, 2.10) +
     f'<div class="t c body" style="top:1380px">{R("y3","dengan diri sendiri")}</div>')
A('tl.fromTo("#g1",{opacity:0,y:60},{opacity:1,y:0,duration:0.5,ease:"expo.out"},0.70);')
rv("#y0", 0.72); chars("#y1", 1.84, 0.05); rv("#y3", 2.56)
S(1.84, "boom", 0.45)

# S2 3.48-5.98: cuba buat 5 perkara ni -- odometer 1->5, polaroid fan
POL = [("still_hands.jpg", -14), ("still_closet.jpg", -7), ("still_look.jpg", 0), ("still_drops.jpg", 7), ("still_salt.jpg", 14)]
pols = "".join(pola(f"pl{i}", f"assets/broll/{f}", 420, 1060, 240, 270, r) for i, (f, r) in enumerate(POL))
clip("s2", 3.48, 2.50, '<div class="bonebg"></div><div class="paper"></div>'
     f'<div class="t c eyebrow" style="top:250px">{R("c0","Cuba buat")}</div>'
     + odo("c1", 5, 4.78, 400, 330, size=560, color="var(--char)", start=1)
     + f'<div class="t c serif-it clay" style="top:840px;font-size:130px">{R("c2","perkara ni")}</div>' + pols)
A('tl.fromTo("#s2",{clipPath:"polygon(0% 0%, 0% 0%, 0% 100%, 0% 100%)"},{clipPath:"polygon(0% 0%, 100% 0%, 100% 100%, 0% 100%)",duration:0.45,ease:"expo.out"},3.48);')
rv("#c0", 3.50); rv("#c2", 5.18, 0.5)
for i, (f, r) in enumerate(POL):
    js.append(f'tl.fromTo("#pl{i}",{{x:0,y:300,rotation:0,opacity:0}},{{x:{(i - 2) * 158},y:{abs(i - 2) * 22},rotation:{r},opacity:1,duration:0.5,ease:"back.out(1.6)"}},{4.80 + i * 0.07:.2f});')
    S(4.80 + i * 0.07, "top", 0.35)
S(3.48, "whip", 0.5)

# ======================= TIPS =======================
def tip_text(n, t0, eyebrow, l1, l2, sub, t1, t2, tsub, sub_cls="clay"):
    return (odo(f"d{n}", n, t0 + 0.05, 70, 1000, size=280, start=0)
            + f'<div class="t eyebrow" style="top:1130px;left:340px">{R(f"e{n}", eyebrow)}</div>'
            + f'<div class="t serif" style="top:1180px;left:340px;font-size:118px">{R(f"l{n}a", l1)}</div>'
            + (f'<div class="t serif-it {sub_cls}" style="top:1310px;left:340px;font-size:96px">{R(f"l{n}b", l2)}</div>' if l2 else ""))

# T1 5.98-8.92: jaga kebersihan diri setiap hari
swipe("sw1", 5.98)
clip("bg1", 5.98, 2.94, '<div class="bonebg"></div>', style="z-index:2")
diag("v_hand", "assets/broll/hands.mp4", 5.98, 2.94, (0, 0, 1080, 1100))
clip("t1", 5.98, 2.94, tip_text(1, 5.98, "Jaga", "kebersihan", "setiap hari", "", 0, 0, 0)
     + pola("t1p", "assets/broll/still_soap.jpg", 690, 640, 300, 360, 6, "natural")
     + scrib("t1s", "circle", 320, 1290, 560, 150, 8.48))
rv("#e1", 6.80); rv("#l1a", 7.16, 0.5); rv("#l1b", 8.26, 0.5)
A('tl.fromTo("#t1p",{y:-400,rotation:-20,opacity:0},{y:0,rotation:6,opacity:1,duration:0.5,ease:"back.out(1.5)"},7.20);')
S(7.2, "top", 0.45)

# T2 8.92-12.28: pilih pakaian buat korang rasa selesa -- split-scroll columns + glass card
swipe("sw2", 8.92)
html.append('<video id="v_fab" class="clip" src="assets/broll/fabric.mp4" data-start="8.920" data-duration="3.360" data-media-start="0" muted playsinline style="z-index:3;left:0;top:0;width:530px;height:1920px;object-fit:cover"></video>')
html.append('<video id="v_clo" class="clip" src="assets/broll/closet.mp4" data-start="8.920" data-duration="3.360" data-media-start="0" muted playsinline style="z-index:3;left:550px;top:0;width:530px;height:1920px;object-fit:cover"></video>')
clip("bg2", 8.92, 3.36, '<div class="bonebg"></div>', style="z-index:2")
A('tl.fromTo("#v_fab",{y:-260},{y:120,duration:3.36,ease:"none"},8.92);')
A('tl.fromTo("#v_clo",{y:260},{y:-120,duration:3.36,ease:"none"},8.92);')
A('tl.fromTo("#v_fab,#v_clo",{clipPath:"inset(100% 0% 0% 0%)"},{clipPath:"inset(0% 0% 0% 0%)",duration:0.45,stagger:0.08,ease:"expo.out"},8.92);')
S(8.92, "whip", 0.45)
clip("t2", 8.92, 3.36, odo("d2", 2, 8.97, 70, 150, size=280, color="var(--bone)")
     + '<div class="glass" id="g2" style="left:90px;top:980px;width:900px;height:470px"></div>'
     + f'<div class="t c eyebrow" style="top:1030px;color:var(--char)">{R("e2","Pilih pakaian")}</div>'
     + f'<div class="t c serif" style="top:1095px;font-size:130px">{R("l2a","yang buat")}</div>'
     + f'<div class="t c serif-it clay" style="top:1240px;font-size:130px">{CH("l2b","selesa")}</div>')
A('tl.fromTo("#g2",{opacity:0,y:60},{opacity:1,y:0,duration:0.5,ease:"expo.out"},9.40);')
rv("#e2", 9.50); rv("#l2a", 10.52, 0.5); chars("#l2b", 11.48, 0.05)

# T3 12.28-15.90: jaga penampilan walau hanya duduk dekat rumah
swipe("sw3", 12.28)
clip("bg3", 12.28, 3.62, '<div class="bonebg"></div>', style="z-index:2")
diag("v_look", "assets/broll/look.mp4", 12.28, 3.62, (0, 0, 1080, 1100))
clip("t3", 12.28, 3.62, tip_text(3, 12.28, "Jaga", "penampilan", "", "", 0, 0, 0)
     + '<div class="sticker" id="t3s" style="left:430px;top:1330px">walau di rumah</div>')
rv("#e3", 13.04); rv("#l3a", 13.38, 0.5); pop("#t3s", 15.16, 0.45, rot=-4)

# T4 15.90-18.56: luangkan masa untuk diri sendiri -- flowers + glass medallion
swipe("sw4", 15.90)
full("v_flw", "assets/broll/flowers.mp4", 15.90, 2.66)
clip("t4", 15.90, 2.66, odo("d4", 4, 15.95, 70, 150, size=280, color="var(--bone)")
     + '<div class="glass" id="g4" style="left:170px;top:560px;width:740px;height:740px;border-radius:50%"></div>'
     + f'<div class="t c eyebrow" style="top:720px;color:var(--char)">{R("e4","Luangkan")}</div>'
     + f'<div class="t c serif" style="top:790px;font-size:150px">{R("l4a","masa")}</div>'
     + f'<div class="t c serif-it clay" style="top:950px;font-size:104px">{R("l4b","untuk diri")}<br>{R("l4c","sendiri")}</div>')
A('tl.fromTo("#g4",{scale:0.6,opacity:0},{scale:1,opacity:1,duration:0.6,ease:"expo.out"},16.0);')
rv("#e4", 16.76); rv("#l4a", 17.06, 0.5); rv("#l4b", 17.44, 0.5); rv("#l4c", 18.10, 0.5)

# T5 18.56-21.86: jangan pernah abaikan rutin mandi
swipe("sw5", 18.56)
clip("bg5", 18.56, 3.30, '<div class="bonebg"></div>', style="z-index:2")
diag("v_drop", "assets/broll/drops.mp4", 18.56, 3.30, (0, 0, 1080, 1100))
clip("t5", 18.56, 3.30, tip_text(5, 18.56, "Jangan abaikan", "rutin", "mandi", "", 0, 0, 0)
     + scrib("t5s", "under", 340, 1400, 420, 60, 21.40))
rv("#e5", 19.36); rv("#l5a", 20.60, 0.5); rv("#l5b", 21.22, 0.5)

# ======================= WHY BATHING =======================
# M1 21.86-25.02: mandi membantu membersihkan badan
full("v_bub", "assets/broll/bubbles.mp4", 21.86, 3.16)
clip("m1", 21.86, 3.16, f'<div class="t c eyebrow" style="top:620px;color:var(--char)">{R("m0","Mandi membantu")}</div>'
     '<div class="glass" id="gm1" style="left:240px;top:700px;width:600px;height:240px;border-radius:120px"></div>'
     f'<div class="t c serif" style="top:745px;font-size:140px">{CH("m1t","bersih")}</div>')
A('tl.fromTo("#gm1",{scaleX:0.2,opacity:0},{scaleX:1,opacity:1,duration:0.5,ease:"expo.out"},23.10);')
rv("#m0", 22.0); chars("#m1t", 23.18, 0.05)
S(22.0, "foam", 0.45)
# M2 25.02-26.56: dan membuat korang lebih segar
full("v_spl", "assets/broll/splash.mp4", 25.02, 1.54, z0=1.3)
clip("m2", 25.02, 1.54, '<div class="shade" style="background:rgba(43,42,39,.18)"></div>'
     f'<div class="t c eyebrow boneclr" style="top:700px">{R("m2a","& buat korang lebih")}</div>'
     f'<div class="t c boneclr" style="top:780px;font:italic 400 250px/1 Instrument">{CH("m2b","segar.")}</div>')
rv("#m2a", 25.04); chars("#m2b", 26.0, 0.05)
S(26.0, "boom", 0.5)

# ======================= FACT =======================
# F 26.56-33.28: tahukah korang? garam laut -- mineral semula jadi -- produk penjagaan diri
swipe("swf", 26.56)
clip("bgf", 26.56, 6.72, '<div class="bonebg"></div><div class="paper"></div>', style="z-index:2")
diag("v_salt", "assets/broll/salt.mp4", 26.56, 6.72, (0, 330, 1080, 760), poly="polygon(0% 10%, 100% 0%, 100% 90%, 0% 100%)")
clip("fct", 26.56, 6.72, '<div class="sticker o" id="f0" style="left:330px;top:200px;font-size:36px">Tahukah korang?</div>'
     f'<div class="t eyebrow" style="top:1140px">{R("f1","Garam laut mengandungi")}</div>'
     f'<div class="t serif" style="top:1195px;font-size:132px">{R("f2","mineral")}</div>'
     f'<div class="t serif-it clay" style="top:1200px;left:600px;font-size:110px">{R("f3","semula jadi")}</div>'
     '<div class="t" style="top:1360px"><div class="chipx" id="f4"><i></i>PRODUK PENJAGAAN DIRI</div></div>')
pop("#f0", 26.60, 0.45, rot=-3); rv("#f1", 27.76); rv("#f2", 29.0, 0.5); rv("#f3", 29.42, 0.5); fade("#f4", 31.8, 0.4, 0, -30)
S(26.60, "boom", 0.5)

# ======================= PRODUCT =======================
# P0 33.28-34.10: "Sebab tu," -- zoom through the sea
html.append('<video id="v_oce" class="clip bg" src="assets/broll/ocean.mp4" data-start="33.280" data-duration="0.820" data-media-start="0" muted playsinline></video>')
A('tl.fromTo("#v_oce",{scale:1.0,filter:"blur(0px)"},{scale:2.6,filter:"blur(10px)",duration:0.82,ease:"power2.in"},33.28);')
S(33.28, "riser", 0.4)
# P1 34.10-39.38: Frescura Body menggabungkan sea salt + wangian inspirasi perfume
clip("prd", 34.10, 5.28, '<div class="bonebg"></div><div class="paper"></div>'
     + pola("pp", "assets/product/duo_marble2.jpg", 240, 230, 600, 900, -2)
     + f'<div class="t c serif" style="top:1240px;font-size:128px">{CH("p1","Frescura Body")}</div>'
     '<div class="t c" style="top:1400px;left:40px;right:40px;white-space:nowrap"><div class="chipx" id="p2" style="margin:0;font-size:34px;padding:16px 28px"><i></i>SEA SALT</div>'
     '<span class="plus" id="p3" style="position:relative;top:20px;margin:0 12px;font-size:80px">+</span>'
     '<div class="chipx" id="p4" style="margin:0;font-size:34px;padding:16px 28px"><i style="background:var(--olive)"></i>WANGIAN ALA PERFUME</div></div>')
A('tl.fromTo("#prd",{opacity:0,scale:1.25},{opacity:1,scale:1,duration:0.45,ease:"expo.out"},34.10);')
A('tl.fromTo("#pp",{y:-500,rotation:-14},{y:0,rotation:-2,duration:0.6,ease:"back.out(1.4)"},34.12);')
chars("#p1", 34.10, 0.03); fade("#p2", 36.12, 0.4, 0, -30); pop("#p3", 36.9, 0.3); fade("#p4", 37.24, 0.4, 0, 30)
S(34.10, "boom", 0.6); S(34.2, "shimmer", 0.45)

# ======================= SCENTS =======================
# S 39.38-45.39: kita ada pilihan Bombshell & Midnight Fantasy -> rutin mandi lebih istimewa
clip("bgs", 39.38, 6.01, '<div class="stonebg"></div><div class="paper"></div>', style="z-index:2")
clip("sc", 39.38, 6.01, f'<div class="t c eyebrow" style="top:200px">{R("k0","Kita ada pilihan")}</div>'
     + pola("k1", "assets/product/glory_card.jpg", 130, 300, 380, 820, -5, "Bombshell")
     + pola("k2", "assets/product/noche_card.jpg", 570, 320, 380, 820, 5, "Midnight Fantasy")
     + f'<div class="t c serif-it" style="top:1290px;font-size:104px">{R("k3","rutin mandi lebih")}</div>'
     + f'<div class="t c serif clay" style="top:1395px;font-size:118px">{CH("k4","istimewa")}</div>'
     + scrib("k5", "under", 330, 1515, 420, 50, 44.95))
A('tl.fromTo("#sc",{clipPath:"polygon(100% 0%, 100% 0%, 100% 100%, 100% 100%)"},{clipPath:"polygon(0% 0%, 100% 0%, 100% 100%, 0% 100%)",duration:0.45,ease:"expo.out"},39.38);')
rv("#k0", 39.40)
A('tl.fromTo("#k1",{y:-900,rotation:-25},{y:0,rotation:-5,duration:0.6,ease:"back.out(1.4)"},40.28);')
A('tl.fromTo("#k2",{y:-900,rotation:25},{y:0,rotation:5,duration:0.6,ease:"back.out(1.4)"},41.36);')
A('tl.to("#k1,#k2",{scale:0.86,y:-60,duration:0.5,ease:"power2.inOut"},42.9);')
rv("#k3", 43.56, 0.5); chars("#k4", 44.34, 0.04)
S(40.28, "whip", 0.5); S(40.6, "top", 0.5); S(41.36, "whip", 0.5); S(41.7, "top", 0.5); S(44.34, "chime", 0.5)

# END 45.39-46.89
clip("end", VOICE_END, DURATION - VOICE_END, '<div class="olivebg"></div>'
     f'<div class="t c boneclr" style="top:760px;font:400 150px/1 Instrument">{CH("n0","Frescura Body")}</div>'
     f'<div class="t c eyebrow" style="top:950px;color:var(--stone)">{R("n1","Woman Glory &middot; Noche")}</div>')
A(f'tl.fromTo("#end",{{clipPath:"polygon(0% 0%, 0% 0%, 0% 100%, 0% 100%)"}},{{clipPath:"polygon(0% 0%, 100% 0%, 100% 100%, 0% 100%)",duration:0.5,ease:"expo.inOut"}},{VOICE_END});')
chars("#n0", VOICE_END + 0.15, 0.03); rv("#n1", VOICE_END + 0.6)
S(VOICE_END, "whip", 0.55); S(VOICE_END + 0.2, "chime", 0.5)

# ---- remap the scenes (authored on the first cut) onto the faster voice
def _ra(m):
    st, d = float(m.group(1)), float(m.group(2))
    return f'data-start="{T(st):.3f}" data-duration="{T(st + d) - T(st):.3f}"'
html = [re.sub(r'data-start="([\d.]+)" data-duration="([\d.]+)"', _ra, h) for h in html]
js = [re.sub(r",([\d.]+)\);$", lambda m: f",{T(float(m.group(1))):.3f});", l) for l in js]
for c in sfx: c["t"] = T(c["t"])
_punch = {}                                       # keep zoom punch -> drift pairs back-to-back
for i, l in enumerate(js):
    m = re.match(r'tl\.fromTo\("(#[\w-]+)",\{scale:[\d.]+\},\{scale:[\d.]+,duration:([\d.]+),ease:"expo\.out"\},([\d.]+)\);$', l)
    if m: _punch[m.group(1)] = float(m.group(3)) + float(m.group(2)); continue
    m = re.match(r'(tl\.to\("(#[\w-]+)",\{scale:[\d.]+,duration:)([\d.]+)(,ease:"none"\},)([\d.]+)\);$', l)
    if m and m.group(2) in _punch:
        st0 = _punch.pop(m.group(2)); end = float(m.group(5)) + float(m.group(3))
        js[i] = f"{m.group(1)}{max(end - st0, 0.1):.2f}{m.group(4)}{st0:.3f});"
VOICE_END = T(VOICE_END); DURATION = round(VOICE_END + 1.5, 2)
# snap any scene boundary that the remap put inside a word: before a new sentence, otherwise after the word
def _bounds():
    out = set()
    for h in html:
        m = re.search(r'id="([^"]+)"[^>]*data-start="([\d.]+)" data-duration="([\d.]+)"', h)
        if m and re.match(r'^(s\d|bg\w*|t\d|m\d|fct|prd|sc|v_\w+)$', m.group(1)):
            out.add(round(float(m.group(2)) + float(m.group(3)), 3))
    return out
_moves = {}
for b in sorted(_bounds()):
    mid = [w for w in words if w["s"] + 0.04 < b < w["e"] - 0.04]
    if mid and b < VOICE_END - 0.05:
        w = mid[0]; i = words.index(w)
        new_sentence = i == 0 or re.search(r"[.,?!]$", words[i - 1]["w"].strip())
        _moves[b] = round(w["s"] if new_sentence and b - w["s"] < 0.45 else w["e"], 3)
def _mv(x):
    for o, n in _moves.items():
        if abs(x - o) < 0.003: return n
    return x
def _rb(m):
    st, d = float(m.group(1)), float(m.group(2)); ns, ne = _mv(st), _mv(round(st + d, 3))
    return f'data-start="{ns:.3f}" data-duration="{ne - ns:.3f}"'
html = [re.sub(r'data-start="([\d.]+)" data-duration="([\d.]+)"', _rb, h) for h in html]
js = [re.sub(r",([\d.]+)\);$", lambda m: f",{_mv(float(m.group(1))):.3f});", l) for l in js]
for c in sfx: c["t"] = _mv(c["t"])
if _moves: print("scene boundaries moved off mid-word:", _moves)

# ---- story-style segment bar (after the face)
segs = "".join(f'<div class="sg"><i id="sg{i}"></i></div>' for i in range(len(SECTIONS) - 1))
clip("chrome", T(0.64), DURATION - T(0.64), f'<div id="story">{segs}</div>', style="z-index:8")
for i in range(len(SECTIONS) - 1):
    a, b = max(SECTIONS[i], T(0.64)), SECTIONS[i + 1]
    js.append(f'tl.fromTo("#sg{i}",{{scaleX:0}},{{scaleX:1,duration:{b - a:.2f},ease:"none"}},{a:.2f});')

# ---- scene changes must fall between words
_tops = []
for h in html:
    m = re.search(r'id="([^"]+)"[^>]*data-start="([\d.]+)" data-duration="([\d.]+)"', h)
    if m and re.match(r'^(s\d|bg\w*|t\d|m\d|fct|prd|sc|end|v_face|v_oce|v_wom|v_flw|v_bub|v_spl)$', m.group(1)):
        _tops.append((m.group(1), round(float(m.group(2)) + float(m.group(3)), 3)))
_bad = [(i, e, w["w"]) for i, e in _tops for w in words if w["s"] + 0.04 < e < w["e"] - 0.04 and e < VOICE_END - 0.05]
if _bad: print("WARNING scene ends mid-word:", _bad)

# ---- captions: frosted strip, keyword underline sweeps in with the word
for ci, ch in enumerate(chunks):
    st = ch[0]["s"]
    if st < 0.6 or st >= VOICE_END:
        continue
    nxt = chunks[ci + 1][0]["s"] if ci + 1 < len(chunks) else VOICE_END
    en = min(nxt, ch[-1]["e"] + 0.45) if nxt - ch[-1]["e"] > 0.6 else nxt
    en = min(en, VOICE_END)
    sp = []
    for wi, w in enumerate(ch):
        key = re.sub(r"[^a-z0-9\-]", "", w["t"].lower())
        hl = key in HL
        sp.append(f'<span id="w{ci}_{wi}" class="w{" hl" if hl else ""}">{w["t"].rstrip(".,?")}</span>')
        js.append(f'tl.fromTo("#w{ci}_{wi}",{{opacity:0.4}},{{opacity:1,duration:0.08}},{w["s"]:.2f});')
        if hl:
            js.append(f'tl.fromTo("#w{ci}_{wi}",{{"--u":0}},{{"--u":1,duration:0.25,ease:"power2.out"}},{w["s"]:.2f});')
    clip(f"cap{ci}", st, max(en - st, 0.2), '<span class="strip">' + " ".join(sp) + "</span>", cls="cap")
    js.append(f'tl.fromTo("#cap{ci} .strip",{{y:18,opacity:0}},{{y:0,opacity:1,duration:0.14,ease:"power3.out"}},{st:.2f});')

# ---- SFX: auto cues yield to hand-placed ones; soft flash on impacts
sfx.sort(key=lambda c: c["t"])
kept = [c for c in sfx if not c["auto"]]
for c in (c for c in sfx if c["auto"]):
    if any(abs(c["t"] - k["t"]) < 0.07 for k in kept): continue
    kept.append(c)
kept.sort(key=lambda c: c["t"])
for c in kept:
    c.pop("auto", None)
    if c["sfx"] == "boom":
        js.append(f'tl.fromTo("#flash",{{opacity:0.3}},{{opacity:0,duration:0.2,ease:"power2.out"}},{c["t"]:.3f});')
json.dump(kept, open(f"{proj}/assets/audio/sfx_cues.json", "w"), indent=0)

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
_ids = re.findall(r'\bid="([^"]+)"', page)
_dup = sorted({i for i in _ids if _ids.count(i) > 1})
assert not _dup, f"duplicate element ids break rendering: {_dup}"
open(f"{proj}/index.html", "w").write(page)
print(len(chunks), "caption chunks,", len(js), "tweens,", len(kept), "sfx cues")
