"""Video 6 -- "Balik kerja: 5 perkara" in a new "Editorial Espresso" minimalist-luxury style.
Bodoni Moda + Manrope, espresso/sand/brass/sage; text-as-window footage, outlined chapter numerals, arch frames,
bento grid, film-strip slides, marquee, blinds transitions, breathing guide, equalizer, phone OFF toggle, recap checklist.
Writes project/index.html (HyperFrames + GSAP) and project/assets/audio/sfx_cues.json from the voice's word times.
Usage: python3 -I build.py PROJECT_DIR [--final]"""
import json, re, sys

proj = sys.argv[1]
FINAL = "--final" in sys.argv
VOICE_END = 47.51
DURATION = 49.0

words = [w for s in json.load(open(f"{proj}/assets/audio/words.json")) for w in s["words"]]
FIX = {"nyakmati": "nikmati", "bersapur": "besar", "Fresura": "Frescura", "Bodi,": "Body,", "sisa": "sea salt",
       "bombshell": "Bombshell", "minat": "Midnight", "fantasi": "Fantasy", "Share": "share"}
HL = {"5", "pertama", "tarik", "nafas", "tenangkan", "kedua", "jauhkan", "telefon", "ketiga", "lagu", "keempat", "keluarga",
      "tersayang", "kelima", "mandi", "nikmati", "berehat", "ruang", "frescura", "body", "sea", "salt", "wangian", "perfume",
      "bombshell", "midnight", "fantasy", "share", "kerja"}
clean = []
for w in words:
    txt = w["w"].strip(); core = txt.rstrip(".,?"); tail = txt[len(core):]
    txt = FIX.get(txt, FIX.get(core, core) + tail)
    if txt.startswith("-") and clean:
        clean[-1]["t"] += txt; clean[-1]["e"] = w["e"]; continue
    clean.append({"t": txt, "s": w["s"], "e": w["e"]})
CHAPTERS = [3.78, 7.40, 11.88, 14.24, 18.18, 23.10, 29.04, 41.56]
chunks, cur = [], []
for i, w in enumerate(clean):
    cur.append(w)
    nxt = clean[i + 1] if i + 1 < len(clean) else None
    if (len(cur) >= 3 or re.search(r"[.,?!]$", w["t"]) or nxt is None or nxt["s"] - w["e"] > 0.3
            or len(" ".join(x["t"] for x in cur)) > 22 or any(abs(nxt["s"] - c) < 0.12 for c in CHAPTERS)):
        chunks.append(cur); cur = []

html, js, sfx = [], [], []
SPEED = 0.55
def _fast(l):
    return re.sub(r"duration:([\d.]+)", lambda m: f"duration:{float(m.group(1)) * SPEED:.2f}" if float(m.group(1)) <= 1.3 else m.group(0), l)
def A(l): js.append(_fast(l))
def S(t, s, g=0.6, auto=False): sfx.append({"t": round(t, 3), "sfx": s, "gain": g, "auto": auto})
def clip(id_, s, d, inner="", cls="", style=""):
    html.append(f'<div id="{id_}" class="clip {cls}" data-start="{s:.3f}" data-duration="{d:.3f}" style="{style}">{inner}</div>')
def vid(id_, src, s, d, box, cls="frame", media="0", img=False, z=4, punch=True):
    """Footage/photo in a mask (arch / frame / circle / tile); box = (left, top, w, h)."""
    l, tp, w, h = box
    rad = {"arch": "600px 600px 18px 18px", "circle": "50%", "tile": "14px"}.get(cls, "18px")
    st = f'z-index:{z};left:{l}px;top:{tp}px;width:{w}px;height:{h}px;object-fit:cover;border-radius:{rad}'
    if img:
        html.append(f'<img id="{id_}" class="clip" src="{src}" data-start="{s:.3f}" data-duration="{d:.3f}" alt="" style="{st}">')
    else:
        html.append(f'<video id="{id_}" class="clip" src="{src}" data-start="{s:.3f}" data-duration="{d:.3f}" data-media-start="{media}" muted playsinline style="{st}"></video>')
    if punch:
        js.append(f'tl.fromTo("#{id_}",{{scale:1.2}},{{scale:1.04,duration:0.42,ease:"expo.out"}},{s});')
        js.append(f'tl.to("#{id_}",{{scale:1.0,duration:{max(d - 0.42, 0.1):.2f},ease:"none"}},{s + 0.42:.3f});')
    if cls == "arch":
        js.append(f'tl.fromTo("#{id_}",{{clipPath:"inset(100% 0% 0% 0% round 600px 600px 18px 18px)"}},{{clipPath:"inset(0% 0% 0% 0% round 600px 600px 18px 18px)",duration:0.45,ease:"expo.out"}},{s});')
    elif cls == "circle":
        js.append(f'tl.fromTo("#{id_}",{{clipPath:"circle(0% at 50% 50%)"}},{{clipPath:"circle(50% at 50% 50%)",duration:0.4,ease:"expo.out"}},{s});')
    else:
        js.append(f'tl.fromTo("#{id_}",{{clipPath:"inset(0% 100% 0% 0% round 16px)"}},{{clipPath:"inset(0% 0% 0% 0% round 16px)",duration:0.38,ease:"expo.out"}},{s});')
    S(s, "whip", 0.42, auto=True); S(s + 0.1, "top", 0.38, auto=True)
def full(id_, src, s, d, tag="video", media="0", z0=1.18):
    if tag == "video":
        html.append(f'<video id="{id_}" class="clip bg" src="{src}" data-start="{s:.3f}" data-duration="{d:.3f}" data-media-start="{media}" muted playsinline></video>')
    else:
        html.append(f'<img id="{id_}" class="clip bg" src="{src}" data-start="{s:.3f}" data-duration="{d:.3f}" alt="">')
    js.append(f'tl.fromTo("#{id_}",{{scale:{z0}}},{{scale:1.03,duration:0.45,ease:"expo.out"}},{s});')
    js.append(f'tl.to("#{id_}",{{scale:1.0,duration:{max(d - 0.45, 0.1):.2f},ease:"none"}},{s + 0.45:.3f});')
    S(s, "whip", 0.5, auto=True)
def rv(sel, t, d=0.7):
    js.append(f'tl.fromTo("{sel} > span",{{yPercent:118}},{{yPercent:0,duration:{max(d * SPEED, 0.22):.2f},ease:"expo.out"}},{t:.2f});')
    S(t, "top", 0.4, auto=True)
def fade(sel, t, d=0.6, y=24, x=0):
    js.append(f'tl.fromTo("{sel}",{{opacity:0,y:{y},x:{x}}},{{opacity:1,y:0,x:0,duration:{max(d * SPEED, 0.2):.2f},ease:"expo.out"}},{t:.2f});')
    S(t, "top", 0.32, auto=True)
def line(sel, t, d=0.8, axis="X"):
    js.append(f'tl.fromTo("{sel}",{{scale{axis}:0}},{{scale{axis}:1,duration:{max(d * SPEED, 0.22):.2f},ease:"expo.out"}},{t:.2f});')
def pop(sel, t, d=0.5):
    js.append(f'tl.fromTo("{sel}",{{scale:0}},{{scale:1,duration:{max(d * 0.65, 0.22):.2f},ease:"back.out(3)"}},{t:.2f});')
    S(t, "top", 0.5, auto=True)
def R(id_, txt): return f'<span id="{id_}" class="rv"><span>{txt}</span></span>'
def numeral(id_, n, t, left=70, top=150, size=300):
    """Giant outlined chapter numeral sliding in from the left."""
    clip_html = f'<div id="{id_}" class="giant outline" style="position:absolute;left:{left}px;top:{top}px;font-size:{size}px">{n}</div>'
    js.append(f'tl.fromTo("#{id_}",{{x:-260,opacity:0}},{{x:0,opacity:1,duration:0.5,ease:"expo.out"}},{t:.2f});')
    S(t, "boom", 0.45)
    return clip_html
def blinds(id_, t):
    """Five brass bars drop in and lift away: the chapter transition."""
    bars = "".join(f'<div class="blind" style="left:{i*216}px;width:217px"></div>' for i in range(5))
    clip(id_, t - 0.2, 0.55, bars, style="z-index:9")
    js.append(f'tl.fromTo("#{id_} .blind",{{scaleY:0,transformOrigin:"50% 0%"}},{{scaleY:1,duration:0.18,stagger:0.03,ease:"power3.in"}},{t - 0.2:.3f});')
    js.append(f'tl.to("#{id_} .blind",{{scaleY:0,transformOrigin:"50% 100%",duration:0.22,stagger:0.03,ease:"power3.out"}},{t + 0.04:.3f});')
    S(t - 0.2, "whip", 0.55)
def chap(id_, n, label, s, d):
    clip(id_, s, d, f'<div class="chap"><b>N&deg; 0{n}</b> &nbsp;/ 05 &nbsp;&middot;&nbsp; {label}</div>', style="z-index:8")
    js.append(f'tl.fromTo("#{id_} .chap",{{opacity:0,x:-20}},{{opacity:1,x:0,duration:0.3,ease:"expo.out"}},{s + 0.05:.3f});')
TICK = ('<svg viewBox="0 0 40 40"><path d="M8 21 L17 30 L33 11" stroke="#b8955a" stroke-width="4.5" fill="none" stroke-linecap="round" '
        'stroke-linejoin="round" stroke-dasharray="40" stroke-dashoffset="40"/></svg>')
SHARE = '<svg viewBox="0 0 64 64"><path d="M38 10 L58 30 L38 50 V38 C24 38 14 42 6 54 C8 36 18 24 38 22 Z" fill="#1b1613"/></svg>'
HEART = ('<svg viewBox="0 0 120 110" style="width:120px;height:110px"><path id="hp" d="M60 100 C20 70 6 50 6 32 C6 16 18 6 32 6 C44 6 54 14 60 24 '
         'C66 14 76 6 88 6 C102 6 114 16 114 32 C114 50 100 70 60 100 Z" fill="none" stroke="#b8955a" stroke-width="4" stroke-dasharray="330" stroke-dashoffset="330"/></svg>')

# ======================= HOOK =======================
# S0 0.00-0.30: "BALIK" -- one-word typographic punch
clip("s0", 0.0, 0.38, '<div class="esp"></div><div class="t c" style="top:760px;font:italic 400 260px/1 Bodoni;color:var(--cream)" id="b0">Balik</div>')
A('tl.fromTo("#b0",{scale:1.35,opacity:0},{scale:1,opacity:1,duration:0.25,ease:"expo.out"},0);')
S(0.0, "boom", 0.6)

# S1 0.38-1.16: the only face shot (0.78 s), into the lens -- "kerja, jangan"
html.append('<video id="v_face" class="clip bg" src="assets/broll/face.mp4" data-start="0.380" data-duration="0.780" data-media-start="0" muted playsinline style="z-index:6"></video>')
A('tl.fromTo("#v_face",{clipPath:"inset(0% 0% 100% 0%)"},{clipPath:"inset(0% 0% 0% 0%)",duration:0.25,ease:"expo.out"},0.38);')
A('tl.fromTo("#v_face",{scale:1.1},{scale:1.0,duration:0.78,ease:"power2.out"},0.38);')
clip("s1", 0.38, 0.78, '<div class="shade" style="background:linear-gradient(180deg,rgba(27,22,19,0) 55%,rgba(27,22,19,.75) 100%)"></div>'
     f'<div class="t c" style="top:1360px;font:italic 400 150px/1 Bodoni;color:var(--cream)">{R("f0","kerja,")}</div>', style="z-index:7")
rv("#f0", 0.40, 0.45)
S(0.38, "whip", 0.5)

# S2 1.16-2.26: "jangan terus fikir pasal KERJA" -- the word is a window onto the office at night, then struck out
clip("s2", 1.16, 1.10, '<div class="esp" style="background:#0e0b09"></div><div class="t c" id="k1" style="top:770px;left:0;right:0;font:900 250px/1 Bodoni;letter-spacing:-6px;-webkit-text-stroke:1.5px rgba(245,239,230,.55);color:transparent;background:url(assets/broll/office.jpg) center 45%/1400px auto;-webkit-background-clip:text;background-clip:text">KERJA</div>'
     f'<div class="t c label" style="top:640px;color:var(--brass)">{R("k0","Jangan terus fikir pasal")}</div>'
     '<div style="position:absolute;left:110px;width:860px;top:955px;height:12px;background:var(--brass);transform-origin:0 50%" id="k2"></div>')
A('tl.fromTo("#k1",{scale:1.25,backgroundPosition:"30% 45%"},{scale:1,backgroundPosition:"60% 45%",duration:1.1,ease:"expo.out"},1.16);')
S(1.16, "whip", 0.5)
rv("#k0", 1.18); line("#k2", 1.90, 0.4)
S(1.90, "whip", 0.45); S(1.98, "boom", 0.4)

# S3 2.26-3.78: "Cuba buat 5 perkara ini" -- giant outlined 5 + marquee of the five tips
clip("s3", 2.26, 1.52, '<div class="esp"></div><div class="grain"></div>'
     '<div class="giant outline" id="big5" style="position:absolute;left:300px;top:380px;font-size:900px;line-height:.8">5</div>'
     f'<div class="t c label" style="top:300px">{R("p0","Cuba buat")}</div>'
     f'<div class="t c disp-it" style="top:1180px;color:var(--cream)">{R("p1","perkara ini")}</div>'
     '<div class="marq" id="mq" style="top:1430px"><span>Tarik nafas</span><span class="d">&middot;</span><span>Jauhkan telefon</span><span class="d">&middot;</span>'
     '<span>Dengar lagu</span><span class="d">&middot;</span><span>Masa keluarga</span><span class="d">&middot;</span><span>Mandi &amp; me-time</span><span class="d">&middot;</span>'
     '<span>Tarik nafas</span><span class="d">&middot;</span><span>Jauhkan telefon</span></div>')
A('tl.fromTo("#s3",{clipPath:"inset(0% 0% 100% 0%)"},{clipPath:"inset(0% 0% 0% 0%)",duration:0.4,ease:"expo.out"},2.26);')
rv("#p0", 2.28)
A('tl.fromTo("#big5",{scale:0.4,opacity:0,rotation:-12},{scale:1,opacity:1,rotation:0,duration:0.55,ease:"back.out(2)"},2.96);')
rv("#p1", 3.20, 0.5)
A('tl.fromTo("#mq",{x:0},{x:-1500,duration:1.5,ease:"none"},2.28);')
S(2.26, "whip", 0.5); S(2.96, "boom", 0.6)

# ======================= TIPS (chapters) =======================
# T1 3.78-7.40: tarik nafas pelan-pelan, tenangkan fikiran -- arch sea + breathing guide
blinds("bl1", 3.78)
clip("bg1", 3.78, 3.62, '<div class="esp"></div>', style="z-index:2")
vid("v_sea", "assets/broll/sea.mp4", 3.78, 3.62, (500, 500, 490, 820), cls="arch")
clip("t1", 3.78, 3.62, numeral("n1", "01", 3.80)
     + f'<div class="t disp" style="top:620px;left:90px;width:420px;font-size:112px">{R("a0","Tarik")}<br>{R("a1","nafas")}</div>'
     + f'<div class="t disp-it brass" style="top:880px;left:90px;width:420px;font-size:66px">{R("a2","pelan-pelan")}</div>'
     + '<div class="breath-dot" id="bd" style="left:150px;top:1040px;width:260px;height:260px"></div>'
     + '<div class="breath" id="br" style="left:150px;top:1040px;width:260px;height:260px"></div>'
     + '<div class="t label" id="bt" style="top:1158px;left:150px;width:260px;text-align:center;letter-spacing:6px">TARIK</div>'
     + '<div class="t label" id="bh" style="top:1158px;left:150px;width:260px;text-align:center;letter-spacing:6px;opacity:0">HEMBUS</div>'
     + f'<div class="t mid" style="top:1390px;left:500px;width:500px;color:var(--sand);font-size:44px">{R("a3","&amp; tenangkan fikiran")}</div>')
chap("c1", 1, "NAFAS", 3.78, 3.62)
rv("#a0", 4.80, 0.5); rv("#a1", 5.04, 0.5); rv("#a2", 5.36)
A('tl.fromTo("#br,#bd",{scale:0.45},{scale:1.15,duration:1.25,ease:"sine.inOut"},4.80);')
A('tl.to("#br,#bd",{scale:0.55,duration:1.3,ease:"sine.inOut"},6.06);')
A('tl.to("#bt",{opacity:0,duration:0.2},6.0);'); A('tl.fromTo("#bh",{opacity:0},{opacity:1,duration:0.2},6.06);')
rv("#a3", 6.50)
S(4.80, "riser", 0.3); S(6.06, "shimmer", 0.4)

# T2 7.40-11.88: jauhkan diri sekejap daripada telefon & media sosial -- phone card pushed away, notifications fall, OFF toggle
blinds("bl2", 7.40)
clip("bg2", 7.40, 4.48, '<div class="esp"></div>', style="z-index:2")
vid("v_ph", "assets/broll/phone.mp4", 7.40, 4.48, (250, 560, 580, 820), cls="frame")
clip("t2", 7.40, 4.48, numeral("n2", "02", 7.42)
     + f'<div class="t disp" style="top:240px;left:480px;width:520px;font-size:104px">{R("j0","Jauhkan")}</div>'
     + f'<div class="t disp-it brass" style="top:360px;left:480px;width:520px;font-size:66px">{R("j1","diri sekejap")}</div>'
     + '<div class="notif" id="j2" style="left:120px;top:640px"><i></i>12 notifikasi baru</div>'
     + '<div class="notif" id="j3" style="left:520px;top:820px"><i style="background:var(--rose)"></i>48 likes</div>'
     + '<div class="notif" id="j4" style="left:160px;top:1000px"><i style="background:var(--sage)"></i>3 mesej</div>'
     + '<div class="toggle" id="j5" style="left:440px;top:1430px"><i></i></div>'
     + '<div class="toggle-l" id="j6" style="left:270px;top:1462px;color:var(--mute)">ON</div>'
     + '<div class="toggle-l" id="j7" style="left:670px;top:1462px;color:var(--brass);opacity:0">OFF</div>')
chap("c2", 2, "TELEFON", 7.40, 4.48)
fade("#j2", 7.70, 0.35, 30); fade("#j3", 7.86, 0.35, 30); fade("#j4", 8.02, 0.35, 30)
rv("#j0", 8.18, 0.5); rv("#j1", 8.78)
A('tl.to("#v_ph",{x:340,rotation:8,opacity:0.18,duration:0.7,ease:"expo.inOut"},8.30);')
A('tl.to("#j2,#j3,#j4",{y:520,opacity:0,rotation:12,duration:0.6,stagger:0.08,ease:"power2.in"},9.64);')
fade("#j5", 9.70, 0.35, 20); fade("#j6", 9.70, 0.35, 20)
A('tl.to("#j5 i",{x:-96,duration:0.3,ease:"expo.inOut"},10.16);')
A('tl.to("#j5",{backgroundColor:"#2a221d",boxShadow:"inset 0 0 0 2px #b8955a",duration:0.3},10.16);')
A('tl.to("#j6",{opacity:0.25,duration:0.2},10.16);'); A('tl.to("#j7",{opacity:1,duration:0.2},10.2);')
S(9.64, "whip", 0.5); S(10.16, "click", 0.8); S(10.3, "pop", 0.5)

# T3 11.88-14.24: dengar lagu yang korang suka -- spinning record + live equalizer
blinds("bl3", 11.88)
clip("bg3", 11.88, 2.36, '<div class="esp"></div>', style="z-index:2")
vid("v_vin", "assets/broll/vinyl.mp4", 11.88, 2.36, (240, 520, 600, 600), cls="circle")
A('tl.fromTo("#v_vin",{rotation:0},{rotation:200,duration:2.36,ease:"none"},11.88);')
EQ = "".join(f'<i id="eq{i}"></i>' for i in range(14))
clip("t3", 11.88, 2.36, numeral("n3", "03", 11.90)
     + f'<div class="t disp" style="top:240px;left:480px;width:520px;font-size:104px">{R("m0","Dengar")}</div>'
     + f'<div class="t disp-it brass" style="top:360px;left:480px;width:520px;font-size:66px">{R("m1","lagu kegemaran")}</div>'
     + '<div class="breath" style="left:216px;top:496px;width:648px;height:648px;border-color:rgba(184,149,90,.5)" id="m2"></div>'
     + f'<div class="eq" style="left:306px;top:1200px">{EQ}</div>')
chap("c3", 3, "MUZIK", 11.88, 2.36)
rv("#m0", 12.88, 0.5); rv("#m1", 13.08)
A('tl.fromTo("#m2",{scale:0.8,opacity:0},{scale:1,opacity:1,duration:0.6,ease:"expo.out"},11.95);')
import random
random.seed(6)
for i in range(14):
    t0 = 12.0
    while t0 < 14.2:
        h = random.uniform(0.15, 1.0); d = round(random.uniform(0.12, 0.22), 2)
        js.append(f'tl.to("#eq{i}",{{scaleY:{h:.2f},duration:{d:.2f},ease:"sine.inOut"}},{t0:.2f});'); t0 = round(t0 + d, 2)
S(12.88, "boom", 0.4)

# T4 14.24-18.18: luangkan masa dengan keluarga / orang yang tersayang -- cinematic letterbox band
blinds("bl4", 14.24)
clip("bg4", 14.24, 3.94, '<div class="esp"></div>', style="z-index:2")
html.append('<video id="v_fam" class="clip" src="assets/broll/family.mp4" data-start="14.240" data-duration="3.940" data-media-start="0" muted playsinline '
            'style="z-index:4;left:0;top:640px;width:1080px;height:452px;object-fit:cover"></video>')
A('tl.fromTo("#v_fam",{clipPath:"inset(50% 0% 50% 0%)"},{clipPath:"inset(0% 0% 0% 0%)",duration:0.5,ease:"expo.out"},14.24);')
A('tl.fromTo("#v_fam",{scale:1.12},{scale:1.0,duration:3.94,ease:"none"},14.24);')
S(14.24, "whip", 0.45)
clip("t4", 14.24, 3.94, numeral("n4", "04", 14.26)
     + f'<div class="t disp" style="top:240px;left:480px;width:540px;font-size:96px">{R("q0","Luangkan")}<br>{R("q0b","masa")}</div>'
     + f'<div class="t label" style="top:1130px">{R("q1","dengan keluarga atau")}</div>'
     + f'<div class="t c disp-it" style="top:1200px;font-size:104px;color:var(--cream)">{R("q2","orang yang")}<br>{R("q3","tersayang")}</div>'
     + f'<div id="q4" style="position:absolute;left:480px;top:1460px">{HEART}</div>'
     + '<div class="rule" id="q5" style="left:0;width:1080px;top:639px"></div><div class="rule" id="q6" style="left:0;width:1080px;top:1092px"></div>')
chap("c4", 4, "KELUARGA", 14.24, 3.94)
rv("#q0", 15.20, 0.5); rv("#q0b", 15.68, 0.5); rv("#q1", 15.98); rv("#q2", 17.30, 0.5); rv("#q3", 17.74, 0.5); line("#q5", 14.3); line("#q6", 14.3)
A('tl.to("#hp",{strokeDashoffset:0,duration:0.5,ease:"power2.out"},17.74);')
S(17.74, "chime", 0.45)

# T5 18.18-23.10: mandi & nikmati masa untuk diri sendiri -- bento grid
blinds("bl5", 18.18)
clip("bg5", 18.18, 4.92, '<div class="esp"></div>', style="z-index:2")
vid("v_bath", "assets/broll/bath.mp4", 18.18, 4.92, (90, 520, 900, 560), cls="tile")
vid("v_cdl", "assets/broll/candle.mp4", 19.82, 3.28, (90, 1100, 440, 420), cls="tile")
vid("v_pmp", "assets/broll/pump_ivory.mp4", 20.66, 2.44, (550, 1100, 440, 420), cls="tile", media="3.3")
clip("t5", 18.18, 4.92, numeral("n5", "05", 18.20)
     + f'<div class="t disp" style="top:240px;left:480px;width:520px;font-size:104px">{R("u0","Mandi")}</div>'
     + f'<div class="t disp-it brass" style="top:360px;left:480px;width:520px;font-size:62px">{R("u1","&amp; nikmati masa")}</div>'
     + f'<div class="t label" style="top:455px;left:480px;width:520px">{R("u2","untuk diri sendiri")}</div>')
chap("c5", 5, "MANDI &amp; ME-TIME", 18.18, 4.92)
rv("#u0", 19.82, 0.5); rv("#u1", 20.66); rv("#u2", 21.60)
S(19.9, "foam", 0.5); S(22.74, "chime", 0.4)

# ======================= REFLECTION =======================
# R1 23.10-26.00: kadang-kadang kita tak perlukan sesuatu yang besar untuk berehat -- tea, editorial pull-quote
blinds("blr", 23.10)
full("v_tea", "assets/broll/tea.mp4", 23.10, 2.90)
clip("refl1", 23.10, 2.90, '<div class="shade" style="background:linear-gradient(180deg,rgba(27,22,19,.75) 0%,rgba(27,22,19,.2) 45%,rgba(27,22,19,.1) 100%)"></div>'
     f'<div class="t label" style="top:260px">{R("r0","Kadang-kadang")}</div>'
     f'<div class="t disp-it" style="top:330px;font-size:84px;line-height:1.08">{R("r1","kita tak perlukan")}<br>{R("r2","sesuatu yang besar")}<br>{R("r3","untuk berehat.")}</div>')
rv("#r0", 23.12); rv("#r1", 24.28, 0.5); rv("#r2", 24.88, 0.5); rv("#r3", 25.96, 0.5)
# R2 26.00-29.04: cukup dengan beri ruang kepada diri sendiri -- film-strip slide to the book, centred quote
html.append('<video id="v_book" class="clip bg" src="assets/broll/book.mp4" data-start="26.000" data-duration="3.040" data-media-start="0" muted playsinline style="z-index:2"></video>')
A('tl.fromTo("#v_book",{x:1080},{x:0,duration:0.45,ease:"expo.inOut"},26.00);')
A('tl.fromTo("#v_book",{scale:1.08},{scale:1.0,duration:3.04,ease:"none"},26.00);')
S(26.0, "whip", 0.5)
clip("refl2", 26.00, 3.04, '<div class="shade" style="background:rgba(27,22,19,.55)"></div>'
     '<div class="t c brass" style="top:470px;font:400 260px/1 Bodoni" id="r4">&ldquo;</div>'
     f'<div class="t c disp-it" style="top:760px;font-size:92px;line-height:1.1">{R("r5","Cukup beri ruang")}<br>{R("r6","kepada diri sendiri.")}</div>'
     '<div class="rule" id="r7" style="left:440px;width:200px;top:1060px"></div>')
A('tl.fromTo("#refl2",{opacity:0},{opacity:1,duration:0.3},26.15);')
pop("#r4", 26.30, 0.4); rv("#r5", 26.76, 0.6); rv("#r6", 27.92, 0.6); line("#r7", 28.66)
S(28.66, "chime", 0.45)

# ======================= PRODUCT =======================
# P1 29.04-39.46: rutin mandi lebih istimewa -> FRESCURA BODY -> sea salt, wangian ala perfume (spec sheet)
blinds("blp", 29.04)
clip("bgp", 29.04, 10.42, '<div class="esp"></div><div class="grain"></div>', style="z-index:2")
vid("p_duo", "assets/product/duo_white.jpg", 29.04, 10.42, (470, 560, 520, 924), cls="arch", img=True)
clip("prod1", 29.04, 4.64, f'<div class="t label" style="top:250px">{R("w0","Nak jadikan rutin mandi")}</div>'
     f'<div class="t disp-it" style="top:310px;font-size:96px">{R("w1","lebih istimewa?")}</div>'
     f'<div class="t mid" style="top:760px;left:90px;width:360px;color:var(--sand);font-size:46px">{R("w2","Korang")}<br>{R("w3","kena cuba")}</div>'
     '<div class="vrule" id="w4" style="left:90px;top:900px;height:420px"></div>')
rv("#w0", 29.06); rv("#w1", 31.56, 0.5); rv("#w2", 32.70); rv("#w3", 32.92); line("#w4", 33.0, 0.6, axis="Y")
clip("prod2", 33.68, 5.78, f'<div class="t c" style="top:200px;font:400 104px/1 Bodoni;letter-spacing:22px">{R("x0","FRESCURA")}</div>'
     f'<div class="t c label" style="top:330px;letter-spacing:30px">{R("x1","BODY")}</div>'
     '<div class="spec" id="x2" style="left:90px;top:760px"><div><div class="x">SEA SALT<small>ocean salt</small></div></div><div class="l"></div><div class="d"></div></div>'
     '<div class="spec" id="x3" style="left:90px;top:960px"><div><div class="x">PILIHAN WANGIAN<small>dua pilihan</small></div></div><div class="l"></div><div class="d"></div></div>'
     '<div class="spec" id="x4" style="left:90px;top:1160px"><div><div class="x">ALA PERFUME<small>berinspirasikan</small></div></div><div class="l"></div><div class="d"></div></div>')
A('tl.fromTo("#prod2",{opacity:0},{opacity:1,duration:0.2},33.68);')
rv("#x0", 33.68, 0.6); rv("#x1", 34.28, 0.5)
for k, tt in (("x2", 35.54), ("x3", 36.54), ("x4", 37.78)):
    fade(f"#{k} .x", tt, 0.4, 0, -20); line(f"#{k} .l", tt + 0.08, 0.4); pop(f"#{k} .d", tt + 0.25, 0.3)
S(33.68, "boom", 0.55); S(34.3, "shimmer", 0.4)

# P2 39.46-41.56: seperti Bombshell dan Midnight Fantasy -- film-strip of the two scent cards
clip("bgs", 39.46, 2.10, '<div class="esp"></div>', style="z-index:2")
vid("p_gl", "assets/product/glory_card.jpg", 39.46, 2.10, (110, 470, 420, 1060), cls="frame", img=True, punch=False)
vid("p_no", "assets/product/noche_card.jpg", 40.90, 0.66, (550, 470, 420, 1060), cls="frame", img=True, punch=False)
A('tl.fromTo("#p_gl",{x:700,rotation:4},{x:0,rotation:-2,duration:0.45,ease:"expo.out"},39.46);')
A('tl.fromTo("#p_no",{x:700,rotation:6},{x:0,rotation:2,duration:0.45,ease:"expo.out"},40.90);')
clip("s5x", 39.46, 2.10, f'<div class="t c label" style="top:300px">{R("y0","Seperti")}</div>'
     '<div class="lbl r" id="y1" style="left:185px;top:1460px">BOMBSHELL</div>'
     '<div class="lbl v" id="y2" style="left:560px;top:1460px">MIDNIGHT FANTASY</div>')
rv("#y0", 39.48); pop("#y1", 39.98, 0.4); pop("#y2", 41.0, 0.4)

# ======================= RECAP + SHARE =======================
# C 41.56-47.51: kalau tips ni bermanfaat, share video ni supaya lebih ramai tahu cara menjaga diri
blinds("blc", 41.56)
TIPS = ["Tarik nafas", "Jauhkan telefon", "Dengar lagu", "Masa keluarga", "Mandi &amp; me-time"]
rows = "".join(f'<div class="check" id="ck{i}" style="top:{470 + i * 118}px"><span class="n">0{i+1}</span><div class="bx">{TICK}</div>{t}</div>' for i, t in enumerate(TIPS))
clip("cta", 41.56, VOICE_END - 41.56, '<div class="esp"></div><div class="grain"></div>'
     f'<div class="t label" style="top:250px">{R("z0","Kalau tips ni bermanfaat")}</div>'
     f'<div class="t disp-it" style="top:310px;font-size:84px">{R("z1","5 perkara tadi")}</div>'
     + rows +
     f'<div class="sharebtn" id="z2" style="top:1110px">{SHARE}SHARE</div>'
     '<div class="tap" id="z3" style="left:720px;top:1150px"></div>'
     f'<div class="t c disp-it" style="top:1310px;font-size:66px;color:var(--sand)">{R("z4","supaya lebih ramai tahu")}<br>{R("z5","cara menjaga diri")}</div>')
rv("#z0", 41.58); rv("#z1", 41.96, 0.5)
for i in range(5):
    tt = 42.2 + i * 0.28
    fade(f"#ck{i}", tt, 0.35, 0, -30)
    js.append(f'tl.to("#ck{i} path",{{strokeDashoffset:0,duration:0.22,ease:"power2.out"}},{tt + 0.12:.2f});')
    S(tt + 0.12, "click", 0.5)
pop("#z2", 43.86, 0.45)
A('tl.fromTo("#z3",{opacity:0,scale:1.5},{opacity:1,scale:1,duration:0.25},44.30);')
A('tl.to("#z2",{scale:0.94,duration:0.1,yoyo:true,repeat:1,ease:"sine.inOut"},44.44);')
rv("#z4", 45.06, 0.5); rv("#z5", 46.16, 0.5)
S(44.44, "click", 0.8); S(44.5, "chime", 0.5)

# END 47.51-49.00
clip("end", VOICE_END, DURATION - VOICE_END, '<div class="sandbg"></div>'
     f'<div class="t c ink" style="top:740px;font:400 110px/1 Bodoni;letter-spacing:20px">{R("e0","FRESCURA")}</div>'
     f'<div class="t c label" style="top:870px;letter-spacing:30px;color:var(--esp)">{R("e1","BODY")}</div>'
     '<div class="rule" id="e2" style="left:440px;width:200px;top:950px;background:var(--esp)"></div>'
     f'<div class="t c" style="top:990px;font:italic 400 52px Bodoni;color:#6d6358">{R("e3","Woman Glory &middot; Noche")}</div>')
A(f'tl.fromTo("#end",{{clipPath:"inset(100% 0% 0% 0%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:0.5,ease:"expo.inOut"}},{VOICE_END});')
rv("#e0", VOICE_END + 0.15, 0.6); rv("#e1", VOICE_END + 0.35); line("#e2", VOICE_END + 0.45); rv("#e3", VOICE_END + 0.55)
S(VOICE_END, "whip", 0.55); S(VOICE_END + 0.2, "chime", 0.5)

# ---- chrome: vertical brass progress line (from the first tip), caption band
clip("chrome", 3.78, DURATION - 3.78, '<div id="vprog"><i></i></div>', style="z-index:8")
A(f'tl.fromTo("#vprog i",{{scaleY:0}},{{scaleY:1,duration:{DURATION - 3.78:.2f},ease:"none"}},3.78);')
clip("band", 3.78, VOICE_END - 3.78, '<div id="capband"></div>', style="z-index:8")

# ---- scene changes must fall between words: audit top-level boundaries
_tops = []
for h in html:
    m = re.search(r'id="([^"]+)"[^>]*data-start="([\d.]+)" data-duration="([\d.]+)"', h)
    if m and re.match(r'^(s\d|bg\w*|t\d|refl\d|prod\d|cta|end|v_face|s5x)$', m.group(1)):
        _tops.append((m.group(1), round(float(m.group(2)) + float(m.group(3)), 3)))
_bad = [(i, e, w["w"]) for i, e in _tops for w in words if w["s"] + 0.04 < e < w["e"] - 0.04 and e < VOICE_END - 0.05]
if _bad: print("WARNING scene ends mid-word:", _bad)

# ---- captions: lower band, spoken word lights up (none over the hook/face/"5 perkara" or the end card)
for ci, ch in enumerate(chunks):
    st = ch[0]["s"]
    if st < 3.7 or st >= VOICE_END:
        continue
    nxt = chunks[ci + 1][0]["s"] if ci + 1 < len(chunks) else VOICE_END
    en = min(nxt, ch[-1]["e"] + 0.45) if nxt - ch[-1]["e"] > 0.6 else nxt
    en = min(en, VOICE_END)
    sp = []
    for wi, w in enumerate(ch):
        key = re.sub(r"[^a-z0-9\-]", "", w["t"].lower())
        hl = key in HL
        sp.append(f'<span id="w{ci}_{wi}" class="w">{w["t"].rstrip(".,?")}</span>')
        js.append(f'tl.fromTo("#w{ci}_{wi}",{{color:"rgba(245,239,230,.45)"}},{{color:"{"#b8955a" if hl else "#f5efe6"}",duration:0.08}},{w["s"]:.2f});')
    clip(f"cap{ci}", st, max(en - st, 0.2), '<span class="line">' + " ".join(sp) + "</span>", cls="cap")
    js.append(f'tl.fromTo("#cap{ci} .line",{{y:16,opacity:0}},{{y:0,opacity:1,duration:0.14,ease:"power3.out"}},{st:.2f});')

# ---- SFX: auto cues yield to hand-placed ones; flash on every impact
sfx.sort(key=lambda c: c["t"])
kept = [c for c in sfx if not c["auto"]]
for c in (c for c in sfx if c["auto"]):
    if any(abs(c["t"] - k["t"]) < 0.07 for k in kept): continue
    kept.append(c)
kept.sort(key=lambda c: c["t"])
for c in kept:
    c.pop("auto", None)
    if c["sfx"] == "boom":
        js.append(f'tl.fromTo("#flash",{{opacity:0.35}},{{opacity:0,duration:0.2,ease:"power2.out"}},{c["t"]:.3f});')
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
