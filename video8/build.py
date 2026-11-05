"""Video 8 -- "Stop! 5 kesilapan masa mandi" in a new "Mineral Mist" spa-mineral minimalist-luxury style.
Fraunces (soft, wonky optical serif) + Sora; educational infographics (thermometer, pressure dial, pump counter, rinse bar + magnifier,
moisture drop), teardrop/capsule/circle masks, ripple-ring chapter wipes, steam-glass wipe reveal, ingredient orbit, 3D card flips,
recap checklist, chat bubbles, droplet progress and marker-sweep captions.
Writes project/index.html (HyperFrames + GSAP) and project/assets/audio/sfx_cues.json from the voice's word times.
Usage: python3 -I build.py PROJECT_DIR [--final]"""
import json, re, sys

proj = sys.argv[1]
FINAL = "--final" in sys.argv
words = [w for s in json.load(open(f"{proj}/assets/audio/words.json")) for w in s["words"]]
REAL_END = round(words[-1]["e"], 2)
VOICE_END = round(REAL_END + 0.5, 2)
DURATION = round(VOICE_END + 1.6, 2)

FIX = {"sabut": "sabun", "Bodi": "Body", "sisa": "sisa", "bombshell": "Bombshell", "minat": "Midnight", "fantasi": "Fantasy", "Ditambah": "Ditambah"}
HL = {"stop", "5", "kesilapan", "panas", "kering", "kuat", "bersih", "sabun", "berlebihan", "membilas", "sempurna", "tertinggal", "pelembab",
      "frescura", "body", "salt", "mineral", "perfume", "bombshell", "midnight", "fantasy", "istimewa", "share", "komen", "baru", "tahu", "boleh"}
WARN = {"stop", "panas", "kuat", "berlebihan", "tertinggal", "kering", "boleh"}
clean = []
for i, w in enumerate(words):
    txt = w["w"].strip(); core = txt.rstrip(".,?!"); tail = txt[len(core):]
    nxt = words[i + 1]["w"].strip().lower() if i + 1 < len(words) else ""
    if core == "sisa" and nxt.startswith("yang"):          # "kandungan sea salt yang kaya..." (whisper hears "sisa")
        clean.append({"t": "sea", "s": w["s"], "e": (w["s"] + w["e"]) / 2}); clean.append({"t": "salt", "s": (w["s"] + w["e"]) / 2, "e": w["e"]}); continue
    txt = FIX.get(core, core) + tail
    if txt.startswith("-") and clean:
        clean[-1]["t"] += txt; clean[-1]["e"] = w["e"]; continue
    clean.append({"t": txt, "s": w["s"], "e": w["e"]})

def W(word, after=0.0):
    for w in clean:
        if w["s"] >= after - 0.01 and re.sub(r"[^a-z0-9]", "", w["t"].lower()) == word: return w["s"]
    raise KeyError(word)

# chapter cut points (all between words)
S1, C1, C2, C3, C4, C5, PR = 0.62, 2.92, 7.82, 12.46, 16.48, 21.46, 26.48
SALT, ORB, PERF, CARDS, RUT, RECAP, SHARE, KOM = 28.52, 30.14, 33.57, 36.48, 37.94, 40.30, 43.30, 46.54
SECTIONS = [S1, C1, C2, C3, C4, C5, PR, PERF, RECAP, SHARE, KOM, VOICE_END]

chunks, cur = [], []
for i, w in enumerate(clean):
    cur.append(w)
    nxt = clean[i + 1] if i + 1 < len(clean) else None
    if (len(cur) >= 3 or re.search(r"[.,?!]$", w["t"]) or nxt is None or nxt["s"] - w["e"] > 0.3
            or len(" ".join(x["t"] for x in cur)) > 17 or any(abs(nxt["s"] - c) < 0.12 for c in SECTIONS + [SALT, ORB, CARDS, RUT])):
        chunks.append(cur); cur = []

html, js, sfx = [], [], []
def S(t, s, g=0.6, auto=False): sfx.append({"t": round(t, 3), "sfx": s, "gain": g, "auto": auto})
def clip(id_, s, d, inner="", cls="", style=""):
    html.append(f'<div id="{id_}" class="clip {cls}" data-start="{s:.3f}" data-duration="{d:.3f}" style="{style}">{inner}</div>')
def vid(id_, src, s, d, cls="clip bg", style="", media="0"):
    return f'<video id="{id_}" class="{cls}" src="{src}" data-start="{s:.3f}" data-duration="{d:.3f}" data-media-start="{media}" muted playsinline style="{style}"></video>'
def R(id_, txt): return f'<span id="{id_}" class="rv"><span>{txt}</span></span>'
def rv(sel, t, d=0.45):
    js.append(f'tl.fromTo("{sel} > span",{{yPercent:118}},{{yPercent:0,duration:{d:.2f},ease:"expo.out"}},{t:.2f});')
    S(t, "top", 0.4, auto=True)
def fade(sel, t, d=0.4, y=30, x=0, s=1.0):
    js.append(f'tl.fromTo("{sel}",{{opacity:0,y:{y},x:{x},scale:{s}}},{{opacity:1,y:0,x:0,scale:1,duration:{d:.2f},ease:"expo.out"}},{t:.2f});')
    S(t, "top", 0.32, auto=True)
def pop(sel, t, d=0.35, rot=0, sfx_="pop"):
    js.append(f'tl.fromTo("{sel}",{{scale:0,rotation:{rot - 10}}},{{scale:1,rotation:{rot},duration:{d:.2f},ease:"back.out(2.6)"}},{t:.2f});')
    S(t, sfx_, 0.5, auto=True)
def CH(id_, txt):
    return f'<span id="{id_}">' + "".join(f'<span class="ch">{c}</span>' for c in txt) + "</span>"
def chars(sel, t, stagger=0.03):
    js.append(f'tl.fromTo("{sel} .ch",{{yPercent:70,opacity:0,rotation:6}},{{yPercent:0,opacity:1,rotation:0,duration:0.45,stagger:{stagger},ease:"expo.out"}},{t:.2f});')
    S(t, "top", 0.45, auto=True)
def kb(sel, s, d, z0=1.12, z1=1.0):
    """slow push on footage/photos"""
    js.append(f'tl.fromTo("{sel}",{{scale:{z0}}},{{scale:{z1},duration:{d:.2f},ease:"power1.out"}},{s:.2f});')
def full(id_, src, s, d, media="0", z0=1.14):
    html.append(vid(id_, src, s, d, media=media))
    js.append(f'tl.fromTo("#{id_}",{{scale:{z0}}},{{scale:1.0,duration:{d:.2f},ease:"power2.out"}},{s:.2f});')

def ivid(id_, src, s, d, box, extra=""):
    """inset footage: a top-level timed <video> (never nested in a timed div) sitting between a scene's backdrop (z2) and its graphics (z5)"""
    l, t_, w, h = box
    html.append(f'<video id="{id_}" class="clip" src="{src}" data-start="{s:.3f}" data-duration="{d:.3f}" data-media-start="0" muted playsinline '
                f'style="z-index:3;left:{l}px;top:{t_}px;width:{w}px;height:{h}px;object-fit:cover;{extra}"></video>')
def back(id_, s, d, inner):
    clip(id_, s, d, inner, style="z-index:2")
SHADOW = "box-shadow:0 30px 70px rgba(16,50,58,.22);"
DROP_D = "M50 3 C50 3 10 50 10 74 a40 40 0 0 0 80 0 C90 50 50 3 50 3 Z"
def ripple(id_, t, color="var(--foam)", x=540, y=960):
    """chapter wipe: a water-ring bloom from the centre that clears to the next scene"""
    rings = "".join(f'<div class="rg" style="position:absolute;left:{x - 60}px;top:{y - 60}px;width:120px;height:120px;border-radius:50%;'
                    f'border:{6 - k * 2}px solid {color}"></div>' for k in range(3))
    clip(id_, t - 0.3, 0.75, f'<div class="disc" style="position:absolute;left:{x - 60}px;top:{y - 60}px;width:120px;height:120px;border-radius:50%;background:{color}"></div>{rings}',
         style="z-index:9")
    js.append(f'tl.fromTo("#{id_} .disc",{{scale:0,opacity:1}},{{scale:40,duration:0.32,ease:"power2.in"}},{t - 0.3:.3f});')
    js.append(f'tl.to("#{id_} .disc",{{opacity:0,duration:0.25,ease:"power1.out"}},{t + 0.02:.3f});')
    js.append(f'tl.fromTo("#{id_} .rg",{{scale:0.2,opacity:0.9}},{{scale:22,opacity:0,duration:0.7,stagger:0.08,ease:"power2.out"}},{t - 0.25:.3f});')
    S(t - 0.3, "whip", 0.5); S(t - 0.05, "ripple", 0.45)

def chapter(n, t, title_html, n_id, lite=False):
    col = "var(--foam)" if lite else "var(--sea)"
    tc = "pearl" if lite else "ink"
    return (f'<div class="num" id="{n_id}n" style="position:absolute;left:70px;top:150px;color:{col}">0{n}</div>'
            f'<div class="lab" id="{n_id}l" style="position:absolute;left:400px;top:200px;color:{"var(--foam)" if lite else "var(--alert)"}">Kesilapan</div>'
            f'<div class="hair" id="{n_id}r" style="left:400px;top:258px;width:600px;{"background:var(--foam)" if lite else ""}"></div>'
            f'<div class="t h1 {tc}" style="top:370px;left:70px;text-align:left;font-size:116px">{title_html}</div>')
def chapter_js(n_id, t):
    js.append(f'tl.fromTo("#{n_id}n",{{yPercent:90,opacity:0,filter:"blur(12px)"}},{{yPercent:0,opacity:1,filter:"blur(0px)",duration:0.5,ease:"expo.out"}},{t:.2f});')
    js.append(f'tl.fromTo("#{n_id}r",{{scaleX:0}},{{scaleX:1,duration:0.5,ease:"expo.out"}},{t + 0.1:.2f});')
    fade(f"#{n_id}l", t + 0.12, 0.35, y=0, x=-30)
    S(t, "drip", 0.6)

def dropfill(k, t):
    js.append(f'tl.to("#dp{k}",{{fillOpacity:1,duration:0.25}},{t:.2f});')
    js.append(f'tl.fromTo("#dps{k}",{{scale:1.6}},{{scale:1,duration:0.4,ease:"back.out(3)"}},{t:.2f});')

# ======================= S0 HOOK: the only face shot (0.62 s) -- "Stop!" with the raised palm =======================
html.append(vid("v_face", "assets/broll/face.mp4", 0, S1, style="z-index:6"))
clip("s0", 0, S1,
     '<div class="veil" style="background:linear-gradient(180deg,rgba(16,50,58,0) 55%,rgba(16,50,58,.55) 100%)"></div>'
     '<svg id="oct" style="position:absolute;left:290px;top:1150px;width:500px;height:500px" viewBox="0 0 100 100">'
     '<path d="M30 3 H70 L97 30 V70 L70 97 H30 L3 70 V30 Z" fill="var(--alert)" fill-opacity=".92" stroke="var(--pearl)" stroke-width="2.5"/></svg>'
     '<div class="t c" id="stopt" style="top:1300px;font:800 150px/1 Sora;letter-spacing:6px;color:var(--pearl)">STOP</div>', style="z-index:7")
js.append('tl.fromTo("#oct",{scale:2.6,opacity:0,rotation:-25},{scale:1,opacity:1,rotation:0,duration:0.22,ease:"back.out(2)"},0.02);')
js.append('tl.fromTo("#stopt",{scale:2.2,opacity:0},{scale:1,opacity:1,duration:0.2,ease:"expo.out"},0.06);')
js.append('tl.to("#oct, #stopt",{x:-8,duration:0.04,yoyo:true,repeat:3},0.26);')
js.append('tl.fromTo("#v_face",{scale:1.0},{scale:1.08,duration:0.62,ease:"power1.out"},0);')
S(0.02, "stamp", 0.9); S(0.03, "boom", 0.6)

# ======================= S1 "Jangan buat 5 kesilapan ini masa mandi" =======================
full("v_shw", "assets/broll/shower.mp4", S1, C1 - S1)
clip("s1", S1, C1 - S1,
     '<div class="veil" style="background:linear-gradient(180deg,rgba(228,235,233,.92) 0%,rgba(228,235,233,.55) 45%,rgba(228,235,233,.9) 100%)"></div>'
     f'<div class="t c lab" style="top:300px;font-size:40px">{R("s1a","Jangan buat")}</div>'
     '<div class="t c" id="s1n" style="top:360px;font:italic 300 560px/1 Fraunces;font-variation-settings:\'SOFT\' 100,\'WONK\' 1,\'opsz\' 144;color:var(--sea)">5</div>'
     f'<div class="t c h1" style="top:930px;font-size:150px">{CH("s1k","kesilapan")}</div>'
     '<div class="chip s" id="s1m" style="left:310px;top:1150px"><b></b>MASA MANDI</div>')
js.append(f'tl.fromTo("#v_shw",{{opacity:0}},{{opacity:1,duration:0.15}},{S1});')
rv("#s1a", W("jangan"))
t5 = W("5")
js.append(f'tl.fromTo("#s1n",{{scale:0.2,opacity:0,filter:"blur(20px)"}},{{scale:1,opacity:1,filter:"blur(0px)",duration:0.4,ease:"back.out(1.8)"}},{t5:.2f});')
S(t5, "boom", 0.6); S(t5, "drip", 0.55)
chars("#s1k", W("kesilapan"), 0.025)
pop("#s1m", W("masa"), 0.35, rot=-2)
S(S1 + 0.02, "whip", 0.5)

# droplet progress bar (5 mistakes), visible through the chapters
dsv = "".join(f'<svg id="dps{k}" viewBox="0 0 100 120"><path id="dp{k}" d="{DROP_D}"/></svg>' for k in range(5))
clip("chrome", W("masa"), PR - W("masa"), f'<div id="drops">{dsv}</div>', style="z-index:8")
js.append(f'tl.fromTo("#drops svg",{{y:-60,opacity:0}},{{y:0,opacity:1,duration:0.35,stagger:0.06,ease:"back.out(2)"}},{W("masa"):.2f});')

# ======================= C1 #1 Air terlalu panas -> kulit kering (thermometer) =======================
ripple("rp1", C1)
full("v_stm", "assets/broll/steam.mp4", C1, C2 - C1, z0=1.06)
TH_X, TH_Y, TH_H = 760, 640, 700
therm = (f'<svg id="th" style="position:absolute;left:{TH_X}px;top:{TH_Y}px;width:220px;height:{TH_H + 60}px;overflow:visible" viewBox="0 0 220 {TH_H + 60}">'
         f'<rect x="80" y="0" width="60" height="{TH_H - 90}" rx="30" fill="rgba(246,245,241,.85)" stroke="var(--ink)" stroke-width="4"/>'
         f'<circle cx="110" cy="{TH_H - 40}" r="62" fill="rgba(246,245,241,.85)" stroke="var(--ink)" stroke-width="4"/>'
         f'<rect id="merc" x="96" y="30" width="28" height="{TH_H - 100}" rx="14" fill="var(--sea)" style="transform-origin:110px {TH_H - 70}px"/>'
         f'<circle id="bulb" cx="110" cy="{TH_H - 40}" r="46" fill="var(--sea)"/>'
         + "".join(f'<line x1="150" x2="{172 if k % 2 == 0 else 162}" y1="{60 + k * 60}" y2="{60 + k * 60}" stroke="var(--ink)" stroke-width="3"/>' for k in range(9))
         + '</svg>'
         f'<div id="thhot" class="chip a" style="left:{TH_X - 215}px;top:{TH_Y + 30}px;font-size:28px;padding:12px 24px">PANAS &#10005;</div>'
         f'<div id="thok" class="chip" style="left:{TH_X - 205}px;top:{TH_Y + 330}px;font-size:28px;padding:12px 24px">SUAM &#10003;</div>')
back("c1b_", C1, C2 - C1, '<div class="veil" style="background:rgba(228,235,233,.55)"></div>')
ivid("v_hot", "assets/broll/hotbath.mp4", C1, C2 - C1, (90, 620, 560, 780), "clip-path:url(#tdrop)")
clip("c1", C1, C2 - C1,
     chapter(1, C1, f'{R("c1a","Air terlalu")}<br>{R("c1b","<i class=alert>panas</i>")}', "c1")
     + therm +
     '<div class="chip a" id="c1k" style="left:470px;top:1420px"><b></b>KULIT KERING</div>')
chapter_js("c1", C1); dropfill(0, W("pertama"))
js.append(f'tl.fromTo("#v_hot",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:0.5,ease:"back.out(1.6)"}},{W("mandi", C1):.2f});')
S(W("mandi", C1), "drip", 0.55)
js.append(f'tl.to("#v_hot",{{scale:1.05,duration:{C2 - W("mandi", C1) - 0.5:.2f},ease:"none"}},{W("mandi", C1) + 0.5:.2f});')
rv("#c1a", W("air", C1)); rv("#c1b", W("panas", C1) - 0.1)
fade("#th", W("menggunakan", C1), 0.4, y=40)
js.append(f'tl.fromTo("#merc",{{scaleY:0.18,svgOrigin:"110 {TH_H - 70}"}},{{scaleY:0.45,svgOrigin:"110 {TH_H - 70}",duration:0.5,ease:"power2.out"}},{W("menggunakan", C1) + 0.2:.2f});')
fade("#thok", W("terlalu", C1), 0.35, y=0, x=20)
tp = W("panas", C1)
js.append(f'tl.to("#merc",{{scaleY:1,svgOrigin:"110 {TH_H - 70}",duration:0.7,ease:"power3.inOut"}},{tp - 0.1:.2f});')
js.append(f'tl.to("#merc, #bulb",{{attr:{{fill:"#c4553f"}},duration:0.5}},{tp:.2f});')
js.append(f'tl.to("#th",{{x:5,duration:0.05,yoyo:true,repeat:5}},{tp + 0.55:.2f});')
fade("#thhot", tp + 0.3, 0.3, y=0, x=20); S(tp + 0.1, "riser", 0.35); S(tp + 0.55, "buzz", 0.45)
pop("#c1k", W("kering", C1) - 0.15, 0.35, rot=-3)

# ======================= C2 #2 Gosok terlalu kuat (pressure dial) -> MITOS =======================
ripple("rp2", C2)
back("c2b_", C2, C3 - C2, '<div class="mistbg"></div><div class="grain"></div>')
ivid("v_scr", "assets/broll/scrub.mp4", C2, C3 - C2, (60, 650, 960, 560), "border-radius:48px;" + SHADOW)
clip("c2", C2, C3 - C2,
     chapter(2, C2, f'{R("c2a","Gosok terlalu")}<br>{R("c2b","<i class=alert>kuat</i>")}', "c2")
     + '<svg id="dial" style="position:absolute;left:290px;top:1180px;width:500px;height:300px;overflow:visible" viewBox="0 0 500 300">'
     '<path d="M40 260 A210 210 0 0 1 110 103" fill="none" stroke="var(--foam)" stroke-width="34"/>'
     '<path d="M118 96 A210 210 0 0 1 382 96" fill="none" stroke="var(--sand)" stroke-width="34"/>'
     '<path d="M390 103 A210 210 0 0 1 460 260" fill="none" stroke="var(--alert)" stroke-width="34"/>'
     '<g id="needle" style="transform-origin:250px 260px"><line x1="250" y1="260" x2="250" y2="80" stroke="var(--ink)" stroke-width="10" stroke-linecap="round"/></g>'
     '<circle cx="250" cy="260" r="22" fill="var(--ink)"/></svg>'
     '<div class="lab" id="dl1" style="position:absolute;left:130px;top:1430px;font-size:26px">Lembut</div>'
     '<div class="lab" id="dl2" style="position:absolute;left:800px;top:1430px;font-size:26px;color:var(--alert)">Kuat</div>'
     '<div class="glass" id="myth" style="left:110px;top:760px;width:860px;height:340px"></div>'
     '<div class="t c" id="myt" style="top:800px;font:400 92px/1.05 Fraunces;font-variation-settings:\'SOFT\' 100,\'WONK\' 1,\'opsz\' 144">lebih kuat<br><span style="color:var(--alert);font-style:italic">&#8800;</span> lebih bersih</div>'
     '<div class="stamp" id="mys" style="left:620px;top:700px;font-size:56px;transform:rotate(8deg)">MITOS</div>')
chapter_js("c2", C2); dropfill(1, W("kedua"))
js.append(f'tl.fromTo("#v_scr",{{clipPath:"inset(50% 50% 50% 50% round 48px)"}},{{clipPath:"inset(0% 0% 0% 0% round 48px)",duration:0.5,ease:"expo.out"}},{W("menggosok"):.2f});')
S(W("menggosok"), "whip", 0.45)
rv("#c2a", W("menggosok")); rv("#c2b", W("kuat") - 0.15)
fade("#dial", W("badan", C2), 0.4, y=40); fade("#dl1", W("badan", C2) + 0.1, 0.3, y=10); fade("#dl2", W("badan", C2) + 0.15, 0.3, y=10)
js.append(f'tl.fromTo("#needle",{{rotation:-75,svgOrigin:"250 260"}},{{rotation:-40,svgOrigin:"250 260",duration:0.4,ease:"power2.out"}},{W("badan", C2) + 0.1:.2f});')
tk = W("kuat", C2)
js.append(f'tl.to("#needle",{{rotation:68,svgOrigin:"250 260",duration:0.45,ease:"back.out(2.5)"}},{tk - 0.25:.2f});')
js.append(f'tl.to("#needle",{{rotation:60,svgOrigin:"250 260",duration:0.06,yoyo:true,repeat:5}},{tk + 0.2:.2f});')
S(tk - 0.2, "riser", 0.3); S(tk + 0.1, "buzz", 0.45)
ti = W("ingat", C2)
js.append(f'tl.fromTo("#myth",{{opacity:0,scale:0.9}},{{opacity:1,scale:1,duration:0.35,ease:"expo.out"}},{ti:.2f});')
fade("#myt", ti + 0.05, 0.35, y=30)
js.append(f'tl.fromTo("#mys",{{scale:2.4,opacity:0,rotation:-10}},{{scale:1,opacity:1,rotation:8,duration:0.2,ease:"power4.in"}},{W("bersih", C2) - 0.05:.2f});')
S(W("bersih", C2) + 0.13, "stamp", 0.8)

# ======================= C3 #3 Sabun berlebihan (pump counter) -> TAK BOLEH =======================
ripple("rp3", C3)
full("v_bub", "assets/broll/bubbles.mp4", C3, C4 - C3, z0=1.1)
cnt = "".join(f'<span style="display:block;height:200px;line-height:200px">&times;{k}</span>' for k in range(1, 6))
back("c3b_", C3, C4 - C3, '<div class="veil" style="background:rgba(228,235,233,.72)"></div>')
ivid("v_sop", "assets/broll/soap.mp4", W("menggunakan", C3), C4 - W("menggunakan", C3), (90, 680, 560, 560), "border-radius:50%;" + SHADOW)
clip("c3", C3, C4 - C3,
     chapter(3, C3, f'{R("c3a","Sabun")}<br>{R("c3b","<i class=alert>berlebihan</i>")}', "c3")
     + '<div class="lab" id="c3p" style="position:absolute;left:700px;top:760px">Pam</div>'
     f'<div id="c3c" style="position:absolute;left:690px;top:810px;height:200px;overflow:hidden;font:italic 300 190px Fraunces;color:var(--sea)">'
     f'<div class="strip">{cnt}</div></div>'
     '<div class="hair" id="c3h" style="left:700px;top:1030px;width:300px"></div>'
     '<div class="stamp" id="c3s" style="left:210px;top:1080px;transform:rotate(-6deg)">TAK BOLEH!</div>')
chapter_js("c3", C3); dropfill(2, W("ketiga"))
tm = W("menggunakan", C3)
js.append(f'tl.fromTo("#v_sop",{{scale:0,rotation:-30}},{{scale:1,rotation:0,duration:0.5,ease:"back.out(1.6)"}},{tm:.2f});')
S(tm, "drip", 0.5)
rv("#c3a", W("sabun", C3) - 0.1); fade("#c3p", W("sabun", C3), 0.3, y=10, x=20); fade("#c3c", W("sabun", C3), 0.3, y=20)
js.append(f'tl.fromTo("#c3h",{{scaleX:0}},{{scaleX:1,duration:0.4,ease:"expo.out"}},{W("sabun", C3):.2f});')
tsec, tber = W("secara", C3), W("berlebihan", C3)
for k, tt in enumerate([tsec, tsec + 0.33, tber, tber + 0.3]):
    js.append(f'tl.to("#c3c .strip",{{y:{-(k + 1) * 200},duration:0.18,ease:"back.out(2)"}},{tt:.2f});')
    js.append(f'tl.fromTo("#v_sop",{{scale:0.94}},{{scale:1,duration:0.18,ease:"power2.out"}},{tt:.2f});')
    S(tt, "click", 0.6); S(tt + 0.03, "foam", 0.3)
rv("#c3b", tber - 0.05)
js.append(f'tl.to("#c3c",{{color:"#c4553f",duration:0.2}},{tber + 0.3:.2f});')
tb = W("tak", C3)
js.append(f'tl.fromTo("#c3s",{{scale:2.6,opacity:0,rotation:-20}},{{scale:1,opacity:1,rotation:-6,duration:0.16,ease:"power4.in"}},{tb - 0.16:.2f});')
js.append(f'tl.to("#c3s",{{x:-10,duration:0.04,yoyo:true,repeat:5}},{tb:.2f});')
S(tb, "stamp", 0.9); S(tb + 0.02, "buzz", 0.5)

# ======================= C4 #4 Tak bilas sempurna (rinse bar stalls + magnifier on the soap residue) =======================
ripple("rp4", C4, color="var(--ink)")
full("v_rns", "assets/broll/rinse.mp4", C4, C5 - C4, z0=1.08)
dots = "".join(f'<i class="rd" style="position:absolute;left:{x}px;top:{y}px;width:{r}px;height:{r}px;border-radius:50%;border:4px solid var(--alert);'
               f'background:rgba(196,85,63,.25)"></i>' for x, y, r in [(90, 120, 46), (230, 80, 34), (300, 220, 54), (150, 260, 30), (330, 110, 28)])
back("c4b_", C4, C5 - C4, '<div class="veil" style="background:linear-gradient(180deg,rgba(16,50,58,.82) 0%,rgba(16,50,58,.45) 50%,rgba(16,50,58,.85) 100%)"></div>')
ivid("v_fom", "assets/broll/foam.mp4", C4, C5 - C4, (250, 640, 440, 440), "border-radius:50%;border:8px solid var(--pearl);" + SHADOW)
clip("c4", C4, C5 - C4,
     chapter(4, C4, f'{R("c4a","Bilas tak")}<br>{R("c4b","<i style=color:var(--foam)>sempurna</i>")}', "c4", lite=True)
     + '<div id="lens" style="position:absolute;left:250px;top:640px;width:440px;height:440px;overflow:visible">' + dots +
     '<div style="position:absolute;left:350px;top:390px;width:44px;height:170px;border-radius:22px;background:var(--pearl);transform:rotate(-45deg);transform-origin:50% 0"></div></div>'
     '<div class="lab" id="c4w" style="position:absolute;left:110px;top:1240px;color:var(--foam)">Bilas</div>'
     '<div id="c4bar" style="position:absolute;left:110px;top:1300px;width:860px;height:30px;border-radius:15px;background:rgba(246,245,241,.2);overflow:hidden">'
     '<i id="c4f" style="position:absolute;left:0;top:0;bottom:0;width:100%;border-radius:15px;background:var(--foam);transform-origin:0 50%"></i></div>'
     '<div class="chip a" id="c4k" style="left:450px;top:1370px"><b></b>SISA SABUN</div>')
chapter_js("c4", C4); dropfill(3, W("keempat"))
js.append('tl.set("#drops",{attr:{class:"lite"}},%.2f);' % (C4 - 0.05))
js.append('tl.set("#drops",{attr:{class:""}},%.2f);' % (C5 - 0.05))
rv("#c4a", W("tidak", C4)); rv("#c4b", W("sempurna", C4) - 0.1)
tmb = W("membilas", C4)
fade("#c4w", tmb, 0.3, y=10); fade("#c4bar", tmb, 0.3, y=10)
js.append(f'tl.fromTo("#c4f",{{scaleX:0}},{{scaleX:0.72,duration:1.6,ease:"power2.out"}},{tmb:.2f});')
js.append(f'tl.to("#c4f",{{scaleX:0.7,duration:0.08,yoyo:true,repeat:5}},{tmb + 1.7:.2f});')
S(tmb, "swoosh", 0.4)
tsh = W("sehingga", C4)
js.append(f'tl.fromTo("#lens, #v_fom",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:0.4,ease:"back.out(1.6)"}},{tsh - 0.3:.2f});')
js.append(f'tl.fromTo("#lens, #v_fom",{{x:-120}},{{x:90,duration:{C5 - tsh:.2f},ease:"sine.inOut"}},{tsh - 0.3:.2f});')
S(tsh - 0.3, "whip", 0.4)
ts = W("sisa", C4)
js.append(f'tl.fromTo("#lens .rd",{{scale:0}},{{scale:1,duration:0.25,stagger:0.08,ease:"back.out(3)"}},{ts:.2f});')
for k in range(5): S(ts + k * 0.08, "pop", 0.35)
pop("#c4k", W("tertinggal", C4) - 0.1, 0.35, rot=-3)

# ======================= C5 #5 Lupa pelembab (moisture drop drains) =======================
ripple("rp5", C5)
back("c5b_", C5, PR - C5, '<div class="mistbg"></div><div class="grain"></div>')
ivid("v_lot", "assets/broll/lotion.mp4", C5, PR - C5, (80, 660, 450, 800), "border-radius:999px;" + SHADOW)
clip("c5", C5, PR - C5,
     chapter(5, C5, f'{R("c5a","Lupa")}<br>{R("c5b","<i class=alert>pelembab</i>")}', "c5")
     + '<svg id="mdrop" style="position:absolute;left:600px;top:720px;width:400px;height:480px;overflow:visible" viewBox="0 0 100 120">'
     '<defs><clipPath id="mclip"><path d="' + DROP_D + '"/></clipPath></defs>'
     '<g clip-path="url(#mclip)"><rect id="mlev" x="0" y="0" width="100" height="120" fill="var(--sea)" style="transform-origin:50px 117px"/>'
     '<path id="mwav" d="M-20 0 Q 0 -5 20 0 T 60 0 T 100 0 T 140 0 V 8 H -20 Z" fill="var(--foam)"/></g>'
     '<path d="' + DROP_D + '" fill="none" stroke="var(--ink)" stroke-width="2.4"/></svg>'
     '<div class="lab" id="c5m" style="position:absolute;left:560px;top:1230px;width:480px;text-align:center">Kelembapan kulit</div>'
     '<div class="chip s" id="c5t" style="left:600px;top:1300px;font-size:34px"><b></b>SELEPAS MANDI</div>'
     '<div class="chip a" id="c5k" style="left:560px;top:1400px;font-size:34px"><b></b>MUDAH KERING</div>')
chapter_js("c5", C5); dropfill(4, W("kelima"))
js.append(f'tl.fromTo("#v_lot",{{clipPath:"inset(100% 0% 0% 0% round 999px)"}},{{clipPath:"inset(0% 0% 0% 0% round 999px)",duration:0.55,ease:"expo.out"}},{W("terlupa"):.2f});')
S(W("terlupa"), "whip", 0.45)
rv("#c5a", W("terlupa")); rv("#c5b", W("pelembab") - 0.1)
fade("#mdrop", W("menggunakan", C5), 0.4, y=40); fade("#c5m", W("menggunakan", C5) + 0.1, 0.3, y=10)
js.append(f'tl.fromTo("#mlev, #mwav",{{y:0}},{{y:0,duration:0.01}},{C5:.2f});')
js.append(f'tl.fromTo("#mwav",{{x:0}},{{x:-40,duration:{PR - C5:.2f},ease:"none"}},{C5:.2f});')
tpl = W("pelembab")
js.append(f'tl.fromTo("#mlev",{{y:12}},{{y:86,duration:2.4,ease:"power1.inOut"}},{tpl:.2f});')
js.append(f'tl.fromTo("#mwav",{{y:12}},{{y:86,duration:2.4,ease:"power1.inOut"}},{tpl:.2f});')
js.append(f'tl.to("#mlev",{{attr:{{fill:"#c4553f"}},duration:1.2}},{tpl + 1.4:.2f});')
S(tpl, "swoosh", 0.4)
pop("#c5t", W("selepas"), 0.35, rot=-2)
pop("#c5k", W("mudah", C5) - 0.1, 0.35, rot=2)
js.append(f'tl.to("#drops",{{opacity:0,duration:0.3}},{PR - 0.35:.2f});')

# ======================= PRODUCT: steam-glass wipe reveal =======================
clip("pr", PR, SALT - PR,
     '<img id="prh" class="bg" src="assets/product/hero_foam.jpg" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover" alt="">'
     '<div class="veil" style="background:linear-gradient(180deg,rgba(16,50,58,0) 55%,rgba(16,50,58,.8) 100%)"></div>'
     '<div id="steam" style="position:absolute;inset:0;backdrop-filter:blur(26px) saturate(.8);-webkit-backdrop-filter:blur(26px) saturate(.8);'
     'background:rgba(228,235,233,.45);-webkit-mask-image:linear-gradient(115deg,transparent calc(var(--m) - 12%),#000 calc(var(--m) + 4%));'
     'mask-image:linear-gradient(115deg,transparent calc(var(--m) - 12%),#000 calc(var(--m) + 4%));--m:-20%"></div>'
     f'<div class="t c lab" style="top:1250px;color:var(--foam)">{R("pra","Hadir dengan")}</div>'
     f'<div class="t c pearl" style="top:1300px;font:400 150px/1 Fraunces;font-variation-settings:\'SOFT\' 100,\'WONK\' 1,\'opsz\' 144">{CH("prb","Frescura Body")}</div>')
kb("#prh", PR, SALT - PR, 1.1, 1.0)
js.append(f'tl.fromTo("#steam",{{"--m":"-20%"}},{{"--m":"125%",duration:0.9,ease:"power2.inOut"}},{PR + 0.05:.2f});')
S(PR, "swoosh", 0.6); S(PR + 0.1, "shimmer", 0.5)
chars("#prb", W("frescura"), 0.03); rv("#pra", W("hadir"))

# ======================= SEA SALT -> mineral semula jadi =======================
full("v_wav", "assets/broll/waves.mp4", SALT, ORB - SALT, z0=1.2)
back("slb_", SALT, ORB - SALT, '<div class="veil" style="background:rgba(16,50,58,.35)"></div>')
ivid("v_slt", "assets/broll/salt.mp4", SALT, ORB - SALT, (220, 260, 640, 640), "border-radius:50%;border:6px solid var(--pearl);" + SHADOW)
clip("sl", SALT, ORB - SALT,
     f'<div class="t c pearl" style="top:960px;font:italic 300 190px/1 Fraunces;font-variation-settings:\'SOFT\' 100,\'WONK\' 1,\'opsz\' 144">{CH("slt","Sea Salt")}</div>'
     '<div class="chip" id="slm" style="left:150px;top:1220px"><b></b>MINERAL</div>'
     '<div class="chip s" id="sls" style="left:520px;top:1220px"><b></b>SEMULA JADI</div>')
js.append(f'tl.fromTo("#v_slt",{{scale:0}},{{scale:1,duration:0.45,ease:"back.out(1.5)"}},{SALT:.2f});')
S(SALT, "ripple", 0.5); S(SALT, "whip", 0.4)
chars("#slt", W("sea") - 0.05, 0.03)
pop("#slm", W("mineral"), 0.3, rot=-3); pop("#sls", W("semula"), 0.3, rot=2)

# ======================= ORBIT: formulasi penjagaan badan =======================
orb_chips = [("SEA SALT", 40), ("MINERAL", 140), ("GENTLE FOAMING", 220), ("500 ML", 320)]
OD = 25                                     # orbit drift (deg) while the chips settle
oc = "".join(f'<div class="och" id="oc{k}" style="position:absolute;left:540px;top:830px;width:0;height:0">'
             f'<div class="cr" style="position:absolute;left:0;top:-400px;width:0;height:0">'
             f'<div style="position:absolute;left:-300px;top:-45px;width:600px;height:90px;display:flex;align-items:center;justify-content:center">'
             f'<div class="chip{" s" if k % 2 else ""}" style="position:relative;font-size:32px;padding:16px 30px"><b></b>{n}</div></div></div></div>'
             for k, (n, a) in enumerate(orb_chips))
clip("ob", ORB, PERF - ORB,
     '<div class="mistbg"></div><div class="grain"></div>'
     '<svg id="obr" style="position:absolute;left:110px;top:400px;width:860px;height:860px" viewBox="0 0 100 100">'
     '<circle cx="50" cy="50" r="49" fill="none" stroke="var(--sea)" stroke-width=".3" stroke-dasharray="1 1.4"/></svg>'
     '<div id="obp" class="rounded" style="left:330px;top:460px;width:420px;height:740px;border-radius:210px">'
     '<img id="obi" src="assets/product/duo_marble.jpg" alt="" style="width:100%;height:100%;object-fit:cover"></div>'
     + f'<div id="obw" style="position:absolute;inset:0">{oc}</div>'
     f'<div class="t c h1" style="top:1300px;font-size:92px">{R("oba","Formulasi")} {R("obb","<i class=sea>penjagaan badan</i>")}</div>')
js.append(f'tl.fromTo("#obp",{{clipPath:"inset(100% 0% 0% 0% round 210px)"}},{{clipPath:"inset(0% 0% 0% 0% round 210px)",duration:0.55,ease:"expo.out"}},{ORB:.2f});')
kb("#obi", ORB, PERF - ORB, 1.15, 1.0); S(ORB, "whip", 0.5)
js.append(f'tl.fromTo("#obr",{{rotation:0,scale:0.6,opacity:0}},{{rotation:90,scale:1,opacity:1,duration:{PERF - ORB:.2f},ease:"power1.out"}},{ORB:.2f});')
for k in range(len(orb_chips)):
    js.append(f'tl.fromTo("#oc{k} .chip",{{scale:0}},{{scale:1,duration:0.3,ease:"back.out(2.5)"}},{ORB + 0.25 + k * 0.22:.2f});')
    S(ORB + 0.25 + k * 0.22, "pop", 0.4)
for k, (n, a) in enumerate(orb_chips):
    js.append(f'tl.fromTo("#oc{k}",{{rotation:{a - OD}}},{{rotation:{a},duration:{PERF - ORB:.2f},ease:"power1.out"}},{ORB:.2f});')
    js.append(f'tl.fromTo("#oc{k} .cr",{{rotation:{OD - a}}},{{rotation:{-a},duration:{PERF - ORB:.2f},ease:"power1.out"}},{ORB:.2f});')
rv("#oba", W("formulasi")); rv("#obb", W("penjagaan"))

# ======================= PERFUME: wangian berinspirasikan perfume =======================
full("v_prf", "assets/broll/perfume.mp4", PERF, CARDS - PERF, z0=1.15)
spark = "".join(f'<i class="sp" style="position:absolute;left:{x}px;top:{y}px;width:{r}px;height:{r}px;border-radius:50%;background:var(--pearl);opacity:.0"></i>'
                for x, y, r in [(300, 900, 10), (420, 820, 7), (520, 960, 12), (640, 860, 8), (700, 980, 6), (380, 1020, 9), (580, 760, 6)])
clip("pf", PERF, CARDS - PERF,
     '<div class="veil" style="background:linear-gradient(180deg,rgba(16,50,58,.82) 0%,rgba(16,50,58,.25) 50%,rgba(16,50,58,.6) 100%)"></div>'
     f'<div class="t c lab" style="top:260px;color:var(--foam)">{R("pfa","Ditambah pula dengan")}</div>'
     f'<div class="t c pearl" style="top:330px;font:400 160px/1 Fraunces;font-variation-settings:\'SOFT\' 100,\'WONK\' 1,\'opsz\' 144">{CH("pfb","wangian")}</div>'
     f'<div class="t c" style="top:520px;font:italic 300 84px/1.1 Fraunces;color:var(--pearl)">{R("pfc","berinspirasikan")}<br>{R("pfd","<span class=pearl>perfume</span>")}</div>'
     + spark)
rv("#pfa", PERF + 0.03); chars("#pfb", W("wangian"), 0.03); rv("#pfc", W("berinspirasikan")); rv("#pfd", W("perfume") - 0.05)
js.append(f'tl.fromTo("#pf .sp",{{opacity:0,y:40,scale:0.4}},{{opacity:0.9,y:-120,scale:1,duration:1.6,stagger:0.08,ease:"power1.out"}},{W("perfume") - 0.3:.2f});')
S(W("perfume") - 0.3, "spray", 0.55); S(W("perfume"), "shimmer", 0.4)

# ======================= CARDS: Woman Glory by Bombshell / Noche by Midnight Fantasy (3D flip) =======================
clip("cd", CARDS, RUT - CARDS,
     '<div class="mistbg"></div><div class="grain"></div>'
     '<div style="position:absolute;inset:0;perspective:1600px">'
     '<div id="cdg" style="position:absolute;left:110px;top:240px;width:400px;height:1020px;border-radius:30px;overflow:hidden;box-shadow:0 30px 70px rgba(16,50,58,.25)">'
     '<img src="assets/product/glory_card.jpg" alt="" style="width:100%;height:100%;object-fit:cover"></div>'
     '<div id="cdn" style="position:absolute;left:570px;top:240px;width:400px;height:1020px;border-radius:30px;overflow:hidden;box-shadow:0 30px 70px rgba(16,50,58,.25)">'
     '<img src="assets/product/noche_card.jpg" alt="" style="width:100%;height:100%;object-fit:cover"></div></div>'
     '<div id="cdgl" style="position:absolute;left:70px;top:1290px;width:480px;text-align:center;font:italic 400 52px/1.1 Fraunces;color:var(--rose)">Woman Glory<br><span style="font:600 26px Sora;letter-spacing:6px">BY BOMBSHELL</span></div>'
     '<div id="cdnl" style="position:absolute;left:530px;top:1290px;width:480px;text-align:center;font:italic 400 52px/1.1 Fraunces;color:var(--violet)">Noche<br><span style="font:600 26px Sora;letter-spacing:6px">BY MIDNIGHT FANTASY</span></div>')
for sel, lab, w_ in (("#cdg", "#cdgl", "bombshell"), ("#cdn", "#cdnl", "midnight")):
    t_ = W(w_) - 0.1
    js.append(f'tl.fromTo("{sel}",{{rotationY:-95,opacity:0}},{{rotationY:0,opacity:1,duration:0.5,ease:"back.out(1.4)"}},{t_:.2f});')
    fade(lab, t_ + 0.15, 0.35, y=20); S(t_, "whip", 0.5); S(t_ + 0.2, "chime", 0.4)

# ======================= RUTIN: untuk menjadikan rutin mandi lebih istimewa =======================
clip("rt", RUT, RECAP - RUT,
     '<img id="rti" src="assets/product/duo_wood.jpg" alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">'
     '<div class="glass" id="rtg" style="left:90px;top:170px;width:900px;height:330px"></div>'
     f'<div class="t c lab" style="top:215px">{R("rta","Rutin mandi")}</div>'
     f'<div class="t c" style="top:270px;font:400 108px/1.05 Fraunces;font-variation-settings:\'SOFT\' 100,\'WONK\' 1,\'opsz\' 144">'
     f'{R("rtb","lebih")} {R("rtc","<i class=sea>istimewa</i>")}</div>'
     + "".join(f'<div class="rr" style="position:absolute;left:480px;top:1200px;width:120px;height:120px;border-radius:50%;border:3px solid var(--pearl)"></div>' for _ in range(3)))
js.append(f'tl.fromTo("#rti",{{scale:1.15,filter:"blur(10px)"}},{{scale:1.0,filter:"blur(0px)",duration:0.7,ease:"expo.out"}},{RUT:.2f});')
js.append(f'tl.to("#rti",{{scale:1.06,duration:{RECAP - RUT - 0.7:.2f},ease:"none"}},{RUT + 0.7:.2f});')
S(RUT, "swoosh", 0.5)
js.append(f'tl.fromTo("#rtg",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:0.4,ease:"expo.out"}},{W("rutin") - 0.1:.2f});')
rv("#rta", W("rutin")); rv("#rtb", W("lebih", RUT)); rv("#rtc", W("istimewa") - 0.05)
js.append(f'tl.fromTo("#rt .rr",{{scale:0.2,opacity:0.9}},{{scale:9,opacity:0,duration:1.4,stagger:0.25,ease:"power2.out"}},{W("istimewa"):.2f});')
S(W("istimewa"), "ripple", 0.5); S(W("istimewa") + 0.1, "chime", 0.45)

# ======================= RECAP: jangan biarkan kawan-kawan buat kesilapan yang sama =======================
items = ["Air terlalu panas", "Gosok terlalu kuat", "Sabun berlebihan", "Bilas tak sempurna", "Lupa pelembab"]
rows = "".join(
    f'<div class="rw" id="rw{k}" style="position:absolute;left:110px;top:{560 + k * 150}px;width:860px;height:120px">'
    f'<svg style="position:absolute;left:0;top:14px;width:92px;height:92px" viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="none" stroke="var(--alert)" stroke-width="6"/>'
    f'<path class="xx" d="M32 32 L68 68 M68 32 L32 68" stroke="var(--alert)" stroke-width="8" stroke-linecap="round" fill="none" stroke-dasharray="110" stroke-dashoffset="110"/></svg>'
    f'<div style="position:absolute;left:130px;top:26px;font:600 56px Sora;color:var(--ink);white-space:nowrap">{txt}</div>'
    f'<i class="st" style="position:absolute;left:122px;top:62px;width:{len(txt) * 33 + 10}px;height:5px;background:var(--alert);transform-origin:0 50%"></i>'
    f'<i style="position:absolute;left:0;right:0;bottom:0;height:1px;background:rgba(16,50,58,.18)"></i></div>' for k, txt in enumerate(items))
clip("rc", RECAP, SHARE - RECAP,
     '<div class="mistbg"></div><div class="grain"></div>'
     f'<div class="t lab" style="top:210px;left:110px">{R("rca","Jangan biarkan kawan-kawan")}</div>'
     f'<div class="t h1" style="top:270px;left:110px;font-size:110px">{R("rcb","buat yang")} {R("rcc","<i class=alert>sama</i>")}</div>'
     + rows)
rv("#rca", RECAP + 0.04); rv("#rcb", W("buat", RECAP)); rv("#rcc", W("sama", RECAP) - 0.05)
for k in range(5):
    t_ = RECAP + 0.55 + k * 0.4
    js.append(f'tl.fromTo("#rw{k}",{{opacity:0,x:-40}},{{opacity:1,x:0,duration:0.3,ease:"expo.out"}},{t_:.2f});')
    js.append(f'tl.to("#rw{k} .xx",{{strokeDashoffset:0,duration:0.25,ease:"power2.out"}},{t_ + 0.15:.2f});')
    js.append(f'tl.fromTo("#rw{k} .st",{{scaleX:0}},{{scaleX:1,duration:0.3,ease:"power2.inOut"}},{t_ + 0.2:.2f});')
    S(t_, "top", 0.4); S(t_ + 0.18, "click", 0.55)

# ======================= SHARE =======================
full("v_phn", "assets/broll/phone.mp4", SHARE, KOM - SHARE, z0=1.12)
av = "".join(f'<div class="av" style="position:absolute;left:{x}px;top:{y}px;width:120px;height:120px;border-radius:50%;background:var(--pearl);'
             f'box-shadow:0 12px 30px rgba(0,0,0,.25)"><svg viewBox="0 0 100 100" style="width:100%;height:100%"><circle cx="50" cy="40" r="17" fill="var(--sea)"/>'
             f'<path d="M20 86 C24 62 76 62 80 86 Z" fill="var(--sea)"/></svg>'
             f'<b style="position:absolute;right:-14px;top:-10px;padding:4px 12px;border-radius:999px;background:var(--alert);color:var(--pearl);font:700 26px Sora">+1</b></div>'
             for x, y in [(160, 1080), (480, 1180), (800, 1060)])
clip("sh", SHARE, KOM - SHARE,
     '<div class="veil" style="background:linear-gradient(180deg,rgba(16,50,58,.85) 0%,rgba(16,50,58,.45) 60%,rgba(16,50,58,.8) 100%)"></div>'
     f'<div class="t c pearl" style="top:250px;font:italic 300 230px/1 Fraunces;font-variation-settings:\'SOFT\' 100,\'WONK\' 1,\'opsz\' 144">{CH("sht","Share")}</div>'
     f'<div class="t c" style="top:520px;font:600 50px/1.3 Sora;color:var(--foam)">{R("sha","supaya lebih ramai tahu")}<br>{R("shb","<span class=pearl>cara jaga kulit masa mandi</span>")}</div>'
     '<svg id="shp" style="position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:visible" viewBox="0 0 1080 1920">'
     '<path id="shl" d="M540 760 C 300 860, 200 960, 220 1100 M540 760 C 540 900, 540 1000, 540 1200 M540 760 C 780 860, 880 940, 860 1080" '
     'fill="none" stroke="var(--pearl)" stroke-width="4" stroke-dasharray="12 14" opacity=".8"/></svg>'
     '<div id="plane" style="position:absolute;left:490px;top:710px;width:100px;height:100px"><svg viewBox="0 0 100 100"><path d="M8 48 L92 10 L66 90 L48 58 Z" fill="var(--pearl)"/>'
     '<path d="M48 58 L92 10" stroke="var(--sea)" stroke-width="4"/></svg></div>' + av)
chars("#sht", W("share"), 0.04); S(W("share"), "boom", 0.45)
rv("#sha", W("supaya")); rv("#shb", W("cara", SHARE))
js.append(f'tl.fromTo("#shl",{{opacity:0}},{{opacity:0.8,duration:0.4}},{W("video", SHARE):.2f});')
js.append(f'tl.fromTo("#plane",{{scale:0,rotation:-30}},{{scale:1,rotation:0,duration:0.35,ease:"back.out(2)"}},{W("video", SHARE):.2f});')
js.append(f'tl.to("#plane",{{y:-30,duration:0.4,yoyo:true,repeat:1,ease:"sine.inOut"}},{W("video", SHARE) + 0.35:.2f});')
S(W("video", SHARE), "swoosh", 0.5)
js.append(f'tl.fromTo("#sh .av",{{scale:0}},{{scale:1,duration:0.35,stagger:0.25,ease:"back.out(2.5)"}},{W("ramai"):.2f});')
for k in range(3): S(W("ramai") + k * 0.25, "pop", 0.5)

# ======================= KOMEN "baru tahu" (chat bubbles) =======================
full("v_typ", "assets/broll/typing.mp4", KOM, VOICE_END + 0.6 - KOM, z0=1.1)
clip("km", KOM, VOICE_END + 0.6 - KOM,
     '<div class="veil" style="background:rgba(228,235,233,.8)"></div>'
     '<div class="lab" id="kml" style="position:absolute;left:110px;top:300px">Komen di bawah</div>'
     '<div id="kb1" style="position:absolute;left:90px;top:380px;max-width:760px;padding:34px 44px;border-radius:44px 44px 44px 10px;background:var(--pearl);'
     'font:500 50px/1.25 Sora;color:var(--ink);box-shadow:0 16px 40px rgba(16,50,58,.15)">Kalau korang tahu tips ni&hellip;</div>'
     '<div id="kdots" style="position:absolute;right:110px;top:640px;padding:30px 40px;border-radius:44px 44px 10px 44px;background:var(--sea);display:flex;gap:14px">'
     + "".join('<i style="width:20px;height:20px;border-radius:50%;background:var(--pearl);display:block"></i>' for _ in range(3)) + '</div>'
     '<div id="kb2" style="position:absolute;right:90px;top:640px;padding:40px 60px;border-radius:56px 56px 12px 56px;background:var(--sea);'
     'font:italic 400 120px/1 Fraunces;font-variation-settings:\'SOFT\' 100,\'WONK\' 1,\'opsz\' 144;color:var(--pearl);box-shadow:0 20px 50px rgba(16,50,58,.25)">baru tahu!</div>'
     '<div id="kh" style="position:absolute;right:120px;top:860px;width:110px;height:110px;border-radius:50%;background:var(--alert);display:flex;align-items:center;justify-content:center">'
     '<svg viewBox="0 0 100 100" style="width:60px;height:60px"><path d="M50 84 C20 62 10 46 18 32 C26 18 44 20 50 34 C56 20 74 18 82 32 C90 46 80 62 50 84 Z" fill="var(--pearl)"/></svg></div>')
fade("#kml", KOM + 0.02, 0.3, y=10)
js.append(f'tl.fromTo("#kb1",{{scale:0.6,opacity:0,transformOrigin:"0% 100%"}},{{scale:1,opacity:1,duration:0.35,ease:"back.out(2)"}},{W("kalau", KOM):.2f});')
S(W("kalau", KOM), "pop", 0.5)
tdots = W("tips", KOM)
js.append(f'tl.fromTo("#kdots",{{scale:0,opacity:0,transformOrigin:"100% 100%"}},{{scale:1,opacity:1,duration:0.25,ease:"back.out(2)"}},{tdots:.2f});')
js.append(f'tl.fromTo("#kdots i",{{y:0}},{{y:-12,duration:0.18,stagger:0.08,yoyo:true,repeat:3,ease:"sine.inOut"}},{tdots + 0.1:.2f});')
tkm = W("komen", KOM)
js.append(f'tl.to("#kdots",{{opacity:0,duration:0.08}},{tkm:.2f});')
js.append(f'tl.fromTo("#kb2",{{scale:0.4,opacity:0,transformOrigin:"100% 100%"}},{{scale:1,opacity:1,duration:0.35,ease:"back.out(2.2)"}},{tkm:.2f});')
S(tkm, "drip", 0.6)
pop("#kh", W("tahu", tkm) + 0.1, 0.35, rot=0)
js.append(f'tl.to("#kh",{{scale:1.18,duration:0.12,yoyo:true,repeat:1}},{W("tahu", tkm) + 0.5:.2f});')
S(W("tahu", tkm) + 0.15, "chime", 0.5)

# ======================= END CARD =======================
clip("end", VOICE_END, DURATION - VOICE_END,
     '<div class="inkbg"></div>'
     '<img id="enp" src="assets/product/duo_diag.jpg" alt="" style="position:absolute;left:340px;top:260px;width:400px;height:700px;object-fit:cover;border-radius:200px">'
     f'<div class="t c pearl" style="top:1060px;font:400 140px/1 Fraunces;font-variation-settings:\'SOFT\' 100,\'WONK\' 1,\'opsz\' 144">{CH("en0","Frescura Body")}</div>'
     f'<div class="t c lab" style="top:1230px;color:var(--foam)">{R("en1","Woman Glory &middot; Noche")}</div>')
js.append(f'tl.fromTo("#end",{{clipPath:"circle(0% at 50% 50%)"}},{{clipPath:"circle(75% at 50% 50%)",duration:0.55,ease:"expo.inOut"}},{VOICE_END:.2f});')
js.append(f'tl.fromTo("#enp",{{clipPath:"inset(100% 0% 0% 0% round 200px)"}},{{clipPath:"inset(0% 0% 0% 0% round 200px)",duration:0.6,ease:"expo.out"}},{VOICE_END + 0.2:.2f});')
chars("#en0", VOICE_END + 0.35, 0.03); rv("#en1", VOICE_END + 0.8)
S(VOICE_END, "ripple", 0.5); S(VOICE_END + 0.35, "chime", 0.5)

# ---- scene changes must fall between words
_tops = []
for h in html:
    m = re.search(r'id="([^"]+)"[^>]*data-start="([\d.]+)" data-duration="([\d.]+)"', h)
    if m and not m.group(1).startswith(("cap", "rp", "chrome")):
        _tops.append((m.group(1), round(float(m.group(2)) + float(m.group(3)), 3)))
_bad = [(i, e, w["w"]) for i, e in _tops for w in words if w["s"] + 0.04 < e < w["e"] - 0.04 and e < VOICE_END - 0.05]
if _bad: print("WARNING scene ends mid-word:", _bad)

DARK = [(C4, C5), (PR, ORB), (PERF, CARDS), (SHARE, KOM)]
# ---- captions: Sora with a pearl halo; each word gets a marker sweep while spoken
for ci, ch in enumerate(chunks):
    st = ch[0]["s"]
    if st < S1 - 0.05 or st >= VOICE_END:
        continue
    nxt = chunks[ci + 1][0]["s"] if ci + 1 < len(chunks) else VOICE_END
    en = min(nxt, ch[-1]["e"] + 0.45) if nxt - ch[-1]["e"] > 0.6 else nxt
    en = min(en, VOICE_END)
    sp = []
    for wi, w in enumerate(ch):
        key = re.sub(r"[^a-z0-9]", "", w["t"].lower())
        cls = "w hl" if key in WARN else "w"
        sp.append(f'<span id="w{ci}_{wi}" class="{cls}"><i></i>{w["t"].rstrip(".,?!")}</span>')
        nx = ch[wi + 1]["s"] if wi + 1 < len(ch) else en
        if key in HL or key in WARN:
            js.append(f'tl.fromTo("#w{ci}_{wi} i",{{scaleX:0}},{{scaleX:1,duration:0.12,ease:"power2.out"}},{w["s"]:.2f});')
            js.append(f'tl.set("#w{ci}_{wi}",{{attr:{{class:"{cls} on"}}}},{w["s"] + 0.12:.2f});')
    dk = any(a - 0.05 <= st < b for a, b in DARK)
    clip(f"cap{ci}", st, max(en - st, 0.2), f'<span class="ln{" dk" if dk else ""}">' + " ".join(sp) + "</span>", cls="cap")
    js.append(f'tl.fromTo("#cap{ci} .ln",{{y:22,opacity:0,filter:"blur(6px)"}},{{y:0,opacity:1,filter:"blur(0px)",duration:0.16,ease:"power3.out"}},{st:.2f});')

# ---- SFX: auto cues yield to hand-placed ones; soft flash on impacts
sfx.sort(key=lambda c: c["t"])
kept = [c for c in sfx if not c["auto"]]
for c in (c for c in sfx if c["auto"]):
    if any(abs(c["t"] - k["t"]) < 0.07 for k in kept): continue
    kept.append(c)
kept.sort(key=lambda c: c["t"])
for c in kept:
    c.pop("auto", None)
    if c["sfx"] in ("boom", "stamp"):
        js.append(f'tl.fromTo("#flash",{{opacity:0.25}},{{opacity:0,duration:0.2,ease:"power2.out"}},{c["t"]:.3f});')
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
<svg width="0" height="0" style="position:absolute"><clipPath id="tdrop" clipPathUnits="objectBoundingBox"><path d="M.5 0 C.5 0 .02 .42 .02 .64 a.48 .36 0 0 0 .96 0 C.98 .42 .5 0 .5 0 Z"/></clipPath></svg>
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
print(len(chunks), "caption chunks,", len(js), "tweens,", len(kept), "sfx cues, duration", DURATION)
