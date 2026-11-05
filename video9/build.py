"""Video 9 -- "3 sebab wajib tukar ke Frescura Body" in a new "Blush & Plum" fashion-editorial minimalist-luxury style.
Gloock (high-contrast serif) + Plus Jakarta Sans; SEBAB 01/02/03 tab bar, blob wipes, pump-press demo with bubble burst,
split comparison (gosok lama vs 1x tekan), crystal-lattice sea salt, "sea salt = garam laut" equation card, sunburst "paling best",
scent-profile meters on colour-washed scent scenes, phone shop mockup with yellow-bag tap + draining stock bar, checkout tick,
captions where words pop in as spoken and keywords switch to Gloock rose.
Usage: python3 -I build.py PROJECT_DIR [--final]"""
import json, math, re, sys

proj = sys.argv[1]
FINAL = "--final" in sys.argv
words = [w for s in json.load(open(f"{proj}/assets/audio/words.json")) for w in s["words"]]
REAL_END = round(words[-1]["e"], 2)
VOICE_END = round(REAL_END + 0.5, 2)
DURATION = round(VOICE_END + 1.6, 2)

FIX = {"bombshell": "Bombshell", "Minat": "Midnight", "minat": "Midnight", "fantasi": "Fantasy", "Forming": "Foaming"}
KEY = {"tiga", "frescura", "body", "tekan", "berbuih", "foaming", "pump", "buih", "lembut", "sea", "salt", "garam", "laut", "mineral",
       "best", "wangi", "perfume", "bombshell", "fresh", "feminine", "midnight", "fantasy", "manis", "fruity", "kuning", "terhad", "sendiri", "check", "out", "wajib"}
clean = []
for i, w in enumerate(words):
    txt = w["w"].strip(); core = txt.rstrip(".,?!"); tail = txt[len(core):]
    nxt = words[i + 1]["w"].strip().lower() if i + 1 < len(words) else ""
    if core.lower() == "fresh" and nxt.startswith("kura"): txt = "Frescura"
    elif core.lower().startswith("kurabodi"): txt = "Body" + tail
    else: txt = FIX.get(core, core) + tail
    if txt.startswith("-") and clean:
        clean[-1]["t"] += txt; clean[-1]["e"] = w["e"]; continue
    clean.append({"t": txt, "s": w["s"], "e": w["e"]})

def W(word, after=0.0):
    for w in clean:
        if w["s"] >= after - 0.01 and re.sub(r"[^a-z0-9]", "", w["t"].lower()) == word: return w["s"]
    raise KeyError(word)

FACE_END, H1, R1A, R1B, R1C, R2A, R2B, R3A, R3B, R3C, R3D, Q, SHOP, CO = 0.68, 0.68, 2.70, 4.83, 6.62, 8.57, 10.27, 14.07, 15.71, 18.76, 21.32, 24.14, 25.30, 28.74
CUTS = [H1, R1A, R1B, R1C, R2A, R2B, R3A, R3B, R3C, R3D, Q, SHOP, CO, VOICE_END]
DARK = [(R1C, R2A), (R3A, Q), (SHOP, CO)]

chunks, cur = [], []
for i, w in enumerate(clean):
    cur.append(w)
    nxt = clean[i + 1] if i + 1 < len(clean) else None
    if (len(cur) >= 3 or re.search(r"[.,?!]$", w["t"]) or nxt is None or nxt["s"] - w["e"] > 0.3
            or len(" ".join(x["t"] for x in cur)) > 16 or any(abs(nxt["s"] - c) < 0.12 for c in CUTS)):
        chunks.append(cur); cur = []

html, js, sfx = [], [], []
def S(t, s, g=0.6, auto=False): sfx.append({"t": round(t, 3), "sfx": s, "gain": g, "auto": auto})
def clip(id_, s, d, inner="", cls="", style=""):
    html.append(f'<div id="{id_}" class="clip {cls}" data-start="{s:.3f}" data-duration="{d:.3f}" style="{style}">{inner}</div>')
def back(id_, s, d, inner): clip(id_, s, d, inner, style="z-index:2")
def full(id_, src, s, d, z0=1.14):
    html.append(f'<video id="{id_}" class="clip bg" src="{src}" data-start="{s:.3f}" data-duration="{d:.3f}" data-media-start="0" muted playsinline></video>')
    js.append(f'tl.fromTo("#{id_}",{{scale:{z0}}},{{scale:1.0,duration:{d:.2f},ease:"power2.out"}},{s:.2f});')
def ivid(id_, src, s, d, box, extra=""):
    l, t_, w, h = box
    html.append(f'<video id="{id_}" class="clip" src="{src}" data-start="{s:.3f}" data-duration="{d:.3f}" data-media-start="0" muted playsinline '
                f'style="z-index:3;left:{l}px;top:{t_}px;width:{w}px;height:{h}px;object-fit:cover;{extra}"></video>')
SHADOW = "box-shadow:0 34px 80px rgba(59,29,46,.25);"
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
def CH(id_, txt): return f'<span id="{id_}">' + "".join(f'<span class="ch">{c}</span>' for c in txt) + "</span>"
def chars(sel, t, stagger=0.03):
    js.append(f'tl.fromTo("{sel} .ch",{{y:60,opacity:0,scale:1.3}},{{y:0,opacity:1,scale:1,duration:0.42,stagger:{stagger},ease:"expo.out"}},{t:.2f});')
    S(t, "top", 0.45, auto=True)
def kb(sel, s, d, z0=1.12, z1=1.0):
    js.append(f'tl.fromTo("{sel}",{{scale:{z0}}},{{scale:{z1},duration:{d:.2f},ease:"power1.out"}},{s:.2f});')
def img(id_, src, box, pos="50% 50%", radius=40, extra=""):
    l, t_, w, h = box
    return (f'<div id="{id_}" class="frame" style="left:{l}px;top:{t_}px;width:{w}px;height:{h}px;border-radius:{radius}px;{extra}">'
            f'<img src="{src}" alt="" style="object-position:{pos}"></div>')
def wipe(id_, t, color="var(--plum)"):
    """section change: an organic blob blooms out of the bottom-left and drains away to the top-right"""
    clip(id_, t - 0.32, 0.72, f'<div class="blob bw" style="left:340px;top:760px;width:400px;height:400px;background:{color}"></div>', style="z-index:9")
    js.append(f'tl.fromTo("#{id_} .bw",{{scale:0,rotation:-40,transformOrigin:"0% 100%"}},{{scale:8,rotation:0,duration:0.32,ease:"power3.in"}},{t - 0.32:.3f});')
    js.append(f'tl.set("#{id_} .bw",{{transformOrigin:"100% 0%"}},{t:.3f});')
    js.append(f'tl.to("#{id_} .bw",{{scale:0,rotation:30,duration:0.36,ease:"power3.out"}},{t + 0.01:.3f});')
    S(t - 0.3, "whip", 0.55); S(t - 0.02, "boom", 0.35)
def header(n, label, light=False):
    col = "var(--champ)" if light else "var(--rose)"
    return (f'<div id="hn{n}" style="position:absolute;left:80px;top:150px;font:400 210px/1 Gloock;color:{col}">0{n}</div>'
            f'<div id="hl{n}" class="lab" style="position:absolute;left:340px;top:200px;{"color:var(--nude)" if light else ""}">Sebab {label}</div>'
            f'<div id="hr{n}" style="position:absolute;left:340px;top:255px;width:660px;height:2px;background:{col};transform-origin:0 50%"></div>')
def header_js(n, t):
    js.append(f'tl.fromTo("#hn{n}",{{y:80,opacity:0,scale:0.8}},{{y:0,opacity:1,scale:1,duration:0.45,ease:"back.out(1.8)"}},{t:.2f});')
    js.append(f'tl.fromTo("#hr{n}",{{scaleX:0}},{{scaleX:1,duration:0.5,ease:"expo.out"}},{t + 0.1:.2f});')
    fade(f"#hl{n}", t + 0.12, 0.35, y=0, x=-30)
    S(t, "chime", 0.45)

# ======================= H0: the only face shot (0.68 s) -- "Tiga" with three fingers up =======================
html.append(f'<video id="v_face" class="clip bg" src="assets/broll/face.mp4" data-start="0" data-duration="{FACE_END:.3f}" data-media-start="0" muted playsinline style="z-index:6"></video>')
clip("h0", 0, FACE_END,
     '<div class="veil" style="background:linear-gradient(180deg,rgba(59,29,46,.0) 60%,rgba(59,29,46,.5) 100%)"></div>'
     + "".join(f'<i class="fd" style="position:absolute;left:{420 + k * 90}px;top:1420px;width:56px;height:56px;border-radius:50%;background:var(--cream);'
               f'box-shadow:0 8px 20px rgba(0,0,0,.3)"></i>' for k in range(3)), style="z-index:7")
js.append(f'tl.fromTo("#v_face",{{scale:1.0}},{{scale:1.07,duration:{FACE_END},ease:"power1.out"}},0);')
js.append('tl.fromTo("#h0 .fd",{scale:0},{scale:1,duration:0.2,stagger:0.08,ease:"back.out(3)"},0.12);')
for k in range(3): S(0.12 + k * 0.08, "pop", 0.55)
S(0.0, "boom", 0.5)

# ======================= H1: 3 sebab wajib tukar ke Frescura Body =======================
back("h1b_", H1, R1A - H1, '<div class="blushbg"></div><div class="grain"></div>')
clip("h1", H1, R1A - H1,
     '<div class="t c" id="h3" style="top:150px;font:400 600px/1 Gloock;color:var(--rose)">3</div>'
     f'<div class="t c" style="top:770px;font:700 58px Jakarta;letter-spacing:-0.5px">{R("h1a","sebab wajib tukar ke")}</div>'
     f'<div class="t c big" style="top:850px;font-size:140px">{CH("h1c","Frescura Body")}</div>'
     + img("h1p", "assets/product/duo_marble.jpg", (230, 1050, 620, 430), "50% 42%", 215))
js.append(f'tl.fromTo("#h3",{{scale:0.3,opacity:0,rotation:-12}},{{scale:1,opacity:1,rotation:0,duration:0.4,ease:"back.out(1.7)"}},{H1:.2f});')
js.append(f'tl.to("#h3",{{scale:1.04,duration:{R1A - H1 - 0.4:.2f},ease:"none"}},{H1 + 0.4:.2f});')
S(H1, "whip", 0.5); S(H1 + 0.05, "boom", 0.5)
rv("#h1a", W("wajib")); chars("#h1c", W("frescura") - 0.05, 0.03)
js.append(f'tl.fromTo("#h1p",{{clipPath:"inset(100% 0% 0% 0% round 215px)",y:60}},{{clipPath:"inset(0% 0% 0% 0% round 215px)",y:0,duration:0.5,ease:"expo.out"}},{W("frescura"):.2f});')
S(W("frescura"), "shimmer", 0.5)

# tab bar SEBAB 01 / 02 / 03
tabs = "".join(f'<div class="tb" id="tb{k}"><i>0{k + 1}</i>{n}</div>' for k, n in enumerate(["BUIH", "SEA SALT", "WANGIAN"]))
clip("chrome", R1A, Q - R1A, f'<div id="tabs">{tabs}</div>', style="z-index:8")
js.append(f'tl.fromTo("#tabs .tb",{{y:-80,opacity:0}},{{y:0,opacity:1,duration:0.35,stagger:0.07,ease:"back.out(2)"}},{R1A:.2f});')
def tab_on(k, t):
    js.append(f'tl.to("#tb{k}",{{backgroundColor:"#3b1d2e",color:"#fbf6f2",borderColor:"#3b1d2e",duration:0.25}},{t:.2f});')
    if k: js.append(f'tl.to("#tb{k - 1}",{{backgroundColor:"rgba(251,246,242,.55)",color:"rgba(59,29,46,.45)",borderColor:"rgba(59,29,46,.15)",duration:0.25}},{t:.2f});')
    js.append(f'tl.fromTo("#tb{k}",{{scale:1.12}},{{scale:1,duration:0.35,ease:"back.out(3)"}},{t:.2f});')

# ======================= R1A: Yang pertama, tekan je terus berbuih (pump press + bubble burst) =======================
wipe("wp1", R1A)
back("r1b_", R1A, R1B - R1A, '<div class="blushbg"></div><div class="grain"></div>')
NOZ = (520, 712)
BUB0 = (540, 1080)                            # bubbles burst from the foam in the hand and spread around the bottle
bub = "".join(f'<i class="bb" style="position:absolute;left:{BUB0[0] - r // 2}px;top:{BUB0[1] - r // 2}px;width:{r}px;height:{r}px;border-radius:50%;'
              f'border:3px solid var(--cream);background:radial-gradient(circle at 30% 30%,rgba(255,255,255,.9),rgba(240,190,200,.35) 60%,rgba(255,255,255,.1))"></i>'
              for r in [70, 46, 90, 38, 60, 52, 80, 34, 64, 44, 74, 40])
clip("r1a", R1A, R1B - R1A,
     header(1, "Pertama")
     + f'<div class="t big" style="top:360px;left:80px;font-size:112px;line-height:1.04">{R("r1t1","Tekan je,")}<br>{R("r1t2","<span class=rose>terus berbuih.</span>")}</div>'
     + img("r1p", "assets/product/hero_foam.jpg", (290, 640, 500, 800), "50% 30%", 40)
     + f'<div id="tapr" style="position:absolute;left:{NOZ[0] - 70}px;top:{NOZ[1] - 70}px;width:140px;height:140px;border-radius:50%;border:6px solid var(--bag)"></div>'
     + f'<svg id="fing" style="position:absolute;left:{NOZ[0] - 10}px;top:{NOZ[1] - 150}px;width:120px;height:150px" viewBox="0 0 80 100">'
       '<path d="M30 8 a8 8 0 0 1 16 0 V44 l18 6 a8 8 0 0 1 6 9 L64 92 H26 L8 62 a7 7 0 0 1 11 -8 L30 64 Z" fill="var(--cream)" stroke="var(--plum)" stroke-width="3.5" stroke-linejoin="round"/></svg>'
     + bub)
header_js(1, R1A); tab_on(0, W("pertama"))
js.append(f'tl.fromTo("#r1p",{{clipPath:"inset(0% 50% 0% 50% round 40px)"}},{{clipPath:"inset(0% 0% 0% 0% round 40px)",duration:0.5,ease:"expo.out"}},{R1A + 0.15:.2f});')
kb("#r1p img", R1A, R1B - R1A, 1.15, 1.0)
rv("#r1t1", W("tekan") - 0.05)
tt = W("tekan")
js.append(f'tl.fromTo("#fing",{{y:-60,opacity:0}},{{y:0,opacity:1,duration:0.25,ease:"power2.out"}},{tt - 0.25:.2f});')
js.append(f'tl.to("#fing",{{y:26,duration:0.1,yoyo:true,repeat:1,ease:"power2.inOut"}},{tt:.2f});')
js.append(f'tl.fromTo("#tapr",{{scale:0.2,opacity:1}},{{scale:1.8,opacity:0,duration:0.5,ease:"power2.out"}},{tt + 0.08:.2f});')
js.append(f'tl.fromTo("#r1p",{{scale:1}},{{scale:0.97,duration:0.1,yoyo:true,repeat:1}},{tt + 0.05:.2f});')
S(tt + 0.05, "click", 0.7); S(tt + 0.08, "ripple", 0.4)
rv("#r1t2", W("terus") - 0.05)
tb_ = W("berbuih")
js.append(f'tl.to("#fing",{{opacity:0,duration:0.15}},{tb_ - 0.25:.2f});')
for k in range(12):
    ang = -math.pi * (k + 0.5) / 12
    dist = 260 + (k * 53) % 160
    js.append(f'tl.fromTo("#r1a .bb:nth-of-type({k + 1})",{{x:0,y:0,scale:0,opacity:1}},'
              f'{{x:{math.cos(ang) * dist * 1.6:.0f},y:{math.sin(ang) * dist * 0.75:.0f},scale:1,opacity:0.95,duration:0.7,ease:"power3.out"}},{tb_ - 0.2 + k * 0.03:.2f});')
S(tb_ - 0.2, "foam", 0.6)
for k in range(5): S(tb_ - 0.15 + k * 0.07, "pop", 0.32)

# ======================= R1B: Foaming pump, tak payah gosok lama (split comparison) =======================
back("r1bb_", R1B, R1C - R1B, '<div class="blushbg"></div><div class="grain"></div>')
ivid("v_gsk", "assets/broll/gosok.mp4", R1B, R1C - R1B, (40, 560, 490, 880), "border-radius:36px;" + SHADOW)
clip("r1b", R1B, R1C - R1B,
     f'<div class="t lab c" style="top:190px">{R("r1ba","Foaming pump")}</div>'
     f'<div class="t c big" style="top:250px;font-size:108px;line-height:1.05">{R("r1bb","Tak payah")}<br>{R("r1bc","<span class=rose>gosok lama</span>")}</div>'
     + img("r1bp", "assets/product/hero_foam.jpg", (550, 560, 490, 880), "50% 35%", 36)
     + '<svg id="sw" style="position:absolute;left:80px;top:600px;width:150px;height:150px" viewBox="0 0 100 100">'
       '<circle cx="50" cy="54" r="38" fill="rgba(251,246,242,.92)" stroke="var(--plum)" stroke-width="5"/><rect x="44" y="6" width="12" height="10" rx="3" fill="var(--plum)"/>'
       '<line id="swh" x1="50" y1="54" x2="50" y2="26" stroke="var(--rose)" stroke-width="5" stroke-linecap="round"/></svg>'
     '<div class="pill" id="r1bl" style="left:100px;top:1320px;font-size:30px;padding:14px 28px">GOSOK LAMA</div>'
     '<div class="pill r" id="r1br" style="left:640px;top:1320px;font-size:30px;padding:14px 28px">1&times; TEKAN</div>'
     '<svg id="r1bx" style="position:absolute;left:40px;top:560px;width:490px;height:880px;overflow:visible" viewBox="0 0 490 880">'
     '<path d="M60 160 L430 720 M430 160 L60 720" stroke="var(--rose)" stroke-width="22" stroke-linecap="round" fill="none" stroke-dasharray="680" stroke-dashoffset="680"/></svg>'
     '<div id="r1bk" style="position:absolute;left:880px;top:600px;width:130px;height:130px;border-radius:50%;background:var(--rose);display:flex;align-items:center;justify-content:center;box-shadow:0 14px 34px rgba(59,29,46,.3)">'
     '<svg viewBox="0 0 100 100" style="width:76px;height:76px"><path d="M24 52 L43 70 L78 32" stroke="var(--cream)" stroke-width="11" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></div>')
rv("#r1ba", R1B + 0.02); rv("#r1bb", W("tak", R1B)); rv("#r1bc", W("gosok") - 0.05)
js.append(f'tl.fromTo("#v_gsk",{{xPercent:-110}},{{xPercent:0,duration:0.45,ease:"expo.out"}},{R1B:.2f});')
js.append(f'tl.fromTo("#r1bp",{{xPercent:110}},{{xPercent:0,duration:0.45,ease:"expo.out"}},{R1B + 0.05:.2f});')
S(R1B, "whip", 0.55)
fade("#sw", W("gosok") - 0.2, 0.3, y=0, s=0.5)
js.append(f'tl.fromTo("#swh",{{rotation:0,svgOrigin:"50 54"}},{{rotation:720,svgOrigin:"50 54",duration:1.2,ease:"none"}},{W("gosok") - 0.1:.2f});')
for k in range(6): S(W("gosok") - 0.1 + k * 0.2, "tick", 0.45)
pop("#r1bl", W("gosok"), 0.3, rot=-3)
js.append(f'tl.to("#r1bx path",{{strokeDashoffset:0,duration:0.3,ease:"power2.out"}},{W("lama") + 0.05:.2f});')
js.append(f'tl.to("#v_gsk",{{filter:"grayscale(1) brightness(.85)",duration:0.3}},{W("lama") + 0.05:.2f});')
S(W("lama") + 0.05, "buzz", 0.45)
pop("#r1br", W("lama") + 0.2, 0.3, rot=2); pop("#r1bk", W("lama") + 0.28, 0.35); S(W("lama") + 0.3, "chime", 0.45)

# ======================= R1C: buih lembut terus keluar dari botol =======================
full("v_bub", "assets/broll/bubbles.mp4", R1C, R2A - R1C, z0=1.2)
float_b = "".join(f'<i class="fb" style="position:absolute;left:{x}px;top:{y}px;width:{r}px;height:{r}px;border-radius:50%;border:2.5px solid rgba(251,246,242,.85);'
                  f'background:radial-gradient(circle at 30% 30%,rgba(255,255,255,.7),rgba(255,255,255,.05) 65%)"></i>'
                  for x, y, r in [(120, 1300, 90), (300, 1500, 50), (860, 1380, 110), (700, 1600, 60), (480, 1450, 36), (940, 1100, 44), (60, 1000, 56), (620, 1250, 30)])
clip("r1c", R1C, R2A - R1C,
     '<div class="veil" style="background:linear-gradient(180deg,rgba(59,29,46,.55) 0%,rgba(59,29,46,.15) 55%,rgba(59,29,46,.6) 100%)"></div>'
     + float_b +
     f'<div class="t c cream" style="top:430px;font:400 300px/0.9 Gloock">{CH("r1cb","Buih")}</div>'
     f'<div class="t c" style="top:720px;font:italic 300 120px/1 Jakarta;color:#ffd0d8">{R("r1cl","lembut")}</div>'
     f'<div class="t c" style="top:930px;font:600 46px Jakarta;color:var(--cream);letter-spacing:1px">{R("r1ck","terus keluar dari botol")}</div>')
S(R1C, "swoosh", 0.5)
chars("#r1cb", W("buih") - 0.05, 0.05); rv("#r1cl", W("lembut")); rv("#r1ck", W("terus", R1C))
js.append(f'tl.fromTo("#r1c .fb",{{y:0,opacity:0}},{{y:-900,opacity:1,duration:{R2A - R1C:.2f},stagger:0.1,ease:"none"}},{R1C:.2f});')
S(W("buih") - 0.05, "foam", 0.5)

# ======================= R2A: Yang kedua, ada sea salt (crystal lattice) =======================
wipe("wp2", R2A, color="var(--rose)")
full("v_slt", "assets/broll/salt.mp4", R2A, R2B - R2A, z0=1.15)
HX = [(540 + 230 * math.cos(math.pi / 3 * k + math.pi / 6), 1160 + 230 * math.sin(math.pi / 3 * k + math.pi / 6)) for k in range(6)]
lat = "".join(f'<line x1="{HX[k][0]:.0f}" y1="{HX[k][1]:.0f}" x2="{HX[(k + 1) % 6][0]:.0f}" y2="{HX[(k + 1) % 6][1]:.0f}"/>' for k in range(6))
lat += "".join(f'<line x1="540" y1="1160" x2="{x:.0f}" y2="{y:.0f}"/>' for x, y in HX)
nodes = "".join(f'<circle class="nd" cx="{x:.0f}" cy="{y:.0f}" r="16"/>' for x, y in HX + [(540, 1160)])
clip("r2a", R2A, R2B - R2A,
     '<div class="veil" style="background:linear-gradient(180deg,rgba(244,232,227,.92) 0%,rgba(244,232,227,.5) 40%,rgba(244,232,227,.2) 100%)"></div>'
     + header(2, "Kedua")
     + f'<div class="t c big" style="top:420px;font-size:230px">{CH("r2s","Sea Salt")}</div>'
     f'<svg id="lat" style="position:absolute;left:0;top:0;width:1080px;height:1920px" viewBox="0 0 1080 1920">'
     f'<g fill="none" stroke="var(--cream)" stroke-width="4" stroke-dasharray="460" stroke-dashoffset="460">{lat}</g>'
     f'<g fill="var(--rose)" stroke="var(--cream)" stroke-width="5">{nodes}</g></svg>')
header_js(2, R2A); tab_on(1, W("kedua"))
chars("#r2s", W("sea") - 0.1, 0.04); S(W("sea"), "shimmer", 0.5)
js.append(f'tl.to("#lat line",{{strokeDashoffset:0,duration:0.6,stagger:0.04,ease:"power2.out"}},{W("ada") - 0.1:.2f});')
js.append(f'tl.fromTo("#lat .nd",{{scale:0,transformOrigin:"50% 50%"}},{{scale:1,duration:0.25,stagger:0.06,ease:"back.out(3)"}},{W("ada") + 0.1:.2f});')
for k in range(7): S(W("ada") + 0.1 + k * 0.06, "click", 0.35)

# ======================= R2B: formulasi dengan sea salt ataupun garam laut, kaya mineral semula jadi =======================
full("v_sea", "assets/broll/sea.mp4", R2B, R3A - R2B, z0=1.12)
clip("r2b", R2B, R3A - R2B,
     '<div class="veil" style="background:rgba(244,232,227,.25)"></div>'
     f'<div class="t c lab" style="top:250px;color:var(--plum)">{R("r2bf","Formulasi dengan")}</div>'
     '<div id="eqc" style="position:absolute;left:110px;top:320px;width:860px;height:560px;border-radius:44px;background:rgba(251,246,242,.6);'
     'backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,.7);box-shadow:0 30px 70px rgba(59,29,46,.2)"></div>'
     f'<div class="t c big" style="top:370px;font-size:140px">{R("eq1","Sea Salt")}</div>'
     f'<div class="t c" style="top:530px;font:400 130px/1 Gloock;color:var(--plum)">{R("eq2","=")}</div>'
     f'<div class="t c big rose" style="top:680px;font-size:140px">{R("eq3","Garam Laut")}</div>'
     '<div class="pill p" id="r2m" style="left:200px;top:960px"><b>&#10022;</b>KAYA MINERAL</div>'
     '<div class="pill r" id="r2j" style="left:330px;top:1080px"><b>&#10047;</b>SEMULA JADI</div>'
     + img("r2p", "assets/product/duo_marble.jpg", (390, 1200, 300, 300), "50% 45%", 150))
rv("#r2bf", W("formulasi"))
js.append(f'tl.fromTo("#eqc",{{scale:0.85,opacity:0}},{{scale:1,opacity:1,duration:0.4,ease:"expo.out"}},{R2B:.2f});')
S(R2B, "whip", 0.45)
rv("#eq1", W("sea", R2B)); rv("#eq2", W("ataupun")); rv("#eq3", W("garam"))
pop("#r2m", W("mineral") - 0.1, 0.35, rot=-3); pop("#r2j", W("semula"), 0.35, rot=2)
js.append(f'tl.fromTo("#r2p",{{scale:0,rotation:-20}},{{scale:1,rotation:0,duration:0.45,ease:"back.out(1.8)"}},{W("kaya"):.2f});')
S(W("kaya"), "drip", 0.5)

# ======================= R3A: Yang ketiga, yang ni yang paling best (sunburst) =======================
wipe("wp3", R3A, color="var(--champ)")
back("r3ab_", R3A, R3B - R3A, '<div class="plumbg"></div>'
     '<div id="sun" style="position:absolute;left:-460px;top:-60px;width:2000px;height:2000px;border-radius:50%;'
     'background:repeating-conic-gradient(rgba(194,154,116,.16) 0deg 6deg, transparent 6deg 18deg)"></div>')
stars = "".join(f'<svg class="st" style="position:absolute;left:{x}px;top:{y}px;width:{r}px;height:{r}px" viewBox="0 0 100 100"><path d="M50 0 L58 42 L100 50 L58 58 L50 100 L42 58 L0 50 L42 42 Z" fill="var(--bag)"/></svg>'
                for x, y, r in [(170, 760, 70), (850, 700, 90), (780, 1180, 56), (220, 1220, 48), (520, 560, 40)])
clip("r3a", R3A, R3B - R3A,
     header(3, "Ketiga", light=True)
     + f'<div class="t c" style="top:640px;font:700 56px Jakarta;color:var(--nude)">{R("r3ay","yang ni yang")}</div>'
     f'<div class="t c cream" style="top:730px;font:400 260px/1 Gloock">{CH("r3ab","paling")}</div>'
     f'<div class="t c" style="top:980px;font:italic 300 190px/1 Jakarta;color:var(--bag)">{R("r3ac","best!")}</div>' + stars)
header_js(3, R3A); tab_on(2, W("ketiga"))
js.append(f'tl.fromTo("#sun",{{rotation:0,scale:0.6,opacity:0}},{{rotation:40,scale:1,opacity:1,duration:{R3B - R3A:.2f},ease:"power1.out"}},{R3A:.2f});')
rv("#r3ay", W("yang", R3A + 0.6)); chars("#r3ab", W("paling") - 0.05, 0.03)
tbest = W("best")
rv("#r3ac", tbest - 0.05); S(tbest, "boom", 0.5)
js.append(f'tl.fromTo("#r3a .st",{{scale:0,rotation:-90}},{{scale:1,rotation:0,duration:0.4,stagger:0.05,ease:"back.out(3)"}},{tbest:.2f});')
S(tbest + 0.05, "shimmer", 0.55)

# ======================= R3B: wangi dia adalah wangi perfume =======================
full("v_prf", "assets/broll/perfume.mp4", R3B, R3C - R3B, z0=1.15)
mist = "".join(f'<i class="ms" style="position:absolute;left:{x}px;top:{y}px;width:{r}px;height:{r}px;border-radius:50%;background:rgba(251,246,242,.9);filter:blur(1px)"></i>'
               for x, y, r in [(380, 980, 12), (460, 900, 8), (540, 1040, 14), (640, 940, 9), (720, 1060, 7), (420, 1100, 10), (600, 860, 7), (500, 980, 6)])
clip("r3b", R3B, R3C - R3B,
     '<div class="veil" style="background:linear-gradient(180deg,rgba(59,29,46,.85) 0%,rgba(59,29,46,.35) 50%,rgba(59,29,46,.75) 100%)"></div>'
     f'<div class="t c lab" style="top:250px;color:var(--nude)">{R("r3bd","Wangi dia")}</div>'
     f'<div class="t c cream" style="top:310px;font:400 230px/1 Gloock">{CH("r3bw","wangi")}</div>'
     f'<div class="t c" style="top:550px;font:italic 300 150px/1 Jakarta;color:#ffd0d8">{R("r3bp","perfume")}</div>' + mist)
S(R3B, "swoosh", 0.5)
rv("#r3bd", W("wangi", R3B) - 0.05); chars("#r3bw", W("wangi", R3B + 0.5) - 0.1, 0.04); rv("#r3bp", W("perfume") - 0.05)
js.append(f'tl.fromTo("#r3b .ms",{{opacity:0,y:60,scale:0.3}},{{opacity:0.9,y:-200,scale:1,duration:1.4,stagger:0.08,ease:"power1.out"}},{W("perfume") - 0.2:.2f});')
S(W("perfume") - 0.2, "spray", 0.6)

# ======================= R3C: Bombshell -- fresh & feminine (rose wash + scent meters) =======================
full("v_rse", "assets/broll/rose.mp4", R3C, R3D - R3C, z0=1.12)
def meter(id_, name, left, top):
    return f'<div class="meter" id="{id_}" style="left:{left}px;top:{top}px"><div class="nm">{name}</div><div class="tr"><div class="fl"></div></div></div>'
clip("r3c", R3C, R3D - R3C,
     '<div class="veil" style="background:linear-gradient(160deg,rgba(176,42,69,.82) 0%,rgba(120,20,40,.7) 100%)"></div>'
     '<div class="blob" id="r3cbl" style="left:20px;top:250px;width:560px;height:1150px;background:rgba(251,246,242,.12)"></div>'
     + img("r3cg", "assets/product/glory_card.jpg", (90, 300, 400, 1020), "50% 50%", 28)
     + f'<div style="position:absolute;left:540px;top:380px;width:480px;font:400 104px/1 Gloock;color:var(--cream)">{R("r3cn","Woman")}<br>{R("r3cn2","Glory")}</div>'
     f'<div class="lab" style="position:absolute;left:545px;top:620px;color:#ffd0d8">{R("r3cb","by Bombshell")}</div>'
     + meter("m1", "FRESH", 545, 760) + meter("m2", "FEMININE", 545, 900)
     + '<div class="pill" id="r3cr" style="left:545px;top:1080px;font-size:30px;padding:14px 28px;color:var(--rose)"><b>&#10047;</b>ROSE &middot; FLORAL</div>')
js.append(f'tl.fromTo("#r3cg",{{rotationY:-90,opacity:0,transformPerspective:1400}},{{rotationY:0,opacity:1,duration:0.5,ease:"back.out(1.4)"}},{R3C:.2f});')
js.append(f'tl.fromTo("#r3cbl",{{scale:0.5,rotation:-20,opacity:0}},{{scale:1,rotation:10,opacity:1,duration:{R3D - R3C:.2f},ease:"power1.out"}},{R3C:.2f});')
S(R3C, "whip", 0.55); S(R3C + 0.15, "chime", 0.45)
rv("#r3cn", R3C + 0.1); rv("#r3cn2", R3C + 0.2); rv("#r3cb", R3C + 0.35)
for sel, w_ in (("#m1", W("fresh", R3C)), ("#m2", W("feminine"))):
    fade(sel, w_ - 0.25, 0.3, y=20)
    js.append(f'tl.fromTo("{sel} .fl",{{scaleX:0}},{{scaleX:0.92,duration:0.6,ease:"power3.out"}},{w_:.2f});')
    S(w_, "riser", 0.25)
pop("#r3cr", W("feminine") + 0.2, 0.3, rot=-2)

# ======================= R3D: Midnight Fantasy -- manis & fruity (violet night + berries) =======================
full("v_sky", "assets/broll/sky.mp4", R3D, Q - R3D, z0=1.12)
ivid("v_ber", "assets/broll/berries.mp4", R3D, Q - R3D, (110, 690, 380, 380), "border-radius:50%;border:6px solid var(--cream);" + SHADOW)
clip("r3d", R3D, Q - R3D,
     '<div class="veil" style="background:linear-gradient(160deg,rgba(90,63,158,.55) 0%,rgba(40,24,80,.7) 100%)"></div>'
     '<div class="blob" id="r3dbl" style="left:520px;top:240px;width:540px;height:1160px;background:rgba(251,246,242,.12)"></div>'
     + img("r3dn", "assets/product/noche_card.jpg", (600, 300, 400, 1020), "50% 50%", 28)
     + f'<div style="position:absolute;left:80px;top:330px;width:480px;font:400 120px/1 Gloock;color:var(--cream)">{R("r3dt","Noche")}</div>'
     f'<div class="lab" style="position:absolute;left:84px;top:470px;line-height:1.5;color:#d9ccff">{R("r3db","by Midnight")}<br>{R("r3db2","Fantasy")}</div>'
     + meter("m3", "MANIS", 80, 1120) + meter("m4", "FRUITY", 80, 1250))
js.append(f'tl.fromTo("#r3dn",{{rotationY:90,opacity:0,transformPerspective:1400}},{{rotationY:0,opacity:1,duration:0.5,ease:"back.out(1.4)"}},{R3D:.2f});')
js.append(f'tl.fromTo("#r3dbl",{{scale:0.5,rotation:20,opacity:0}},{{scale:1,rotation:-10,opacity:1,duration:{Q - R3D:.2f},ease:"power1.out"}},{R3D:.2f});')
S(R3D, "whip", 0.55); S(R3D + 0.15, "chime", 0.45)
rv("#r3dt", R3D + 0.1); rv("#r3db", W("fantasy") - 0.1); rv("#r3db2", W("fantasy"))
js.append(f'tl.fromTo("#v_ber",{{scale:0}},{{scale:1,duration:0.45,ease:"back.out(1.7)"}},{W("suka") - 0.2:.2f});')
S(W("suka") - 0.2, "drip", 0.5)
for sel, w_ in (("#m3", W("manis")), ("#m4", W("fruity"))):
    fade(sel, w_ - 0.25, 0.3, y=20)
    js.append(f'tl.fromTo("{sel} .fl",{{scaleX:0}},{{scaleX:0.9,duration:0.6,ease:"power3.out"}},{w_:.2f});')
    S(w_, "riser", 0.25)
js.append(f'tl.to("#tabs",{{opacity:0,duration:0.25}},{Q - 0.3:.2f});')

# ======================= Q: Korang nak rasa sendiri tak? =======================
wipe("wp4", Q)
back("qb_", Q, SHOP - Q, '<div class="blushbg"></div><div class="grain"></div>')
ivid("v_unb", "assets/broll/unbox.mp4", Q, SHOP - Q, (60, 900, 960, 600), "border-radius:40px;" + SHADOW)
clip("q", Q, SHOP - Q,
     '<div id="qm" style="position:absolute;left:640px;top:120px;font:400 700px/1 Gloock;color:var(--rose);opacity:.9">?</div>'
     f'<div style="position:absolute;left:80px;top:330px;font:700 64px Jakarta">{R("qa","Korang nak")}</div>'
     f'<div style="position:absolute;left:80px;top:420px;font:400 170px/1 Gloock">{R("qb","rasa")}</div>'
     f'<div style="position:absolute;left:80px;top:600px;font:italic 300 150px/1 Jakarta;color:var(--rose)">{R("qc","sendiri?")}</div>')
js.append(f'tl.fromTo("#qm",{{scale:0.2,rotation:-30,opacity:0}},{{scale:1,rotation:8,opacity:0.9,duration:0.45,ease:"back.out(1.8)"}},{Q + 0.02:.2f});')
rv("#qa", W("korang", Q) - 0.05); rv("#qb", W("rasa", Q) - 0.05); rv("#qc", W("sendiri", Q) - 0.05)
js.append(f'tl.fromTo("#v_unb",{{clipPath:"inset(100% 0% 0% 0% round 40px)"}},{{clipPath:"inset(0% 0% 0% 0% round 40px)",duration:0.45,ease:"expo.out"}},{Q + 0.1:.2f});')

# ======================= SHOP: Tekan beg kuning sekarang -- stok sangat-sangat terhad (phone mockup) =======================
full("v_shp", "assets/broll/shop.mp4", SHOP, CO - SHOP, z0=1.1)
BAG = ('<svg viewBox="0 0 100 100" style="width:{s}px;height:{s}px"><path d="M18 34 H82 L76 90 H24 Z" fill="var(--bag)" stroke="var(--plum)" stroke-width="4" stroke-linejoin="round"/>'
       '<path d="M36 40 V28 a14 14 0 0 1 28 0 V40" fill="none" stroke="var(--plum)" stroke-width="5" stroke-linecap="round"/></svg>')
clip("sh", SHOP, CO - SHOP,
     '<div class="veil" style="background:rgba(59,29,46,.45)"></div>'
     '<div id="ph" style="position:absolute;left:250px;top:180px;width:580px;height:1110px;border-radius:78px;background:var(--cream);border:16px solid #1f0f18;'
     'box-shadow:0 40px 90px rgba(0,0,0,.45);overflow:hidden">'
     '<div style="position:absolute;left:180px;top:14px;width:190px;height:34px;border-radius:17px;background:#1f0f18"></div>'
     '<img src="assets/product/duo_marble.jpg" alt="" style="position:absolute;left:0;top:70px;width:100%;height:600px;object-fit:cover;object-position:50% 40%">'
     '<div style="position:absolute;left:36px;top:700px;font:400 60px/1 Gloock;color:var(--plum)">Frescura Body</div>'
     '<div style="position:absolute;left:36px;top:780px;font:600 26px Jakarta;color:var(--champ);letter-spacing:2px">WOMAN GLORY &middot; NOCHE &middot; 500 ML</div>'
     '<div style="position:absolute;left:36px;top:830px;font:700 26px Jakarta;color:var(--rose);letter-spacing:2px">&#9679; STOK TERHAD</div>'
     f'<div id="bagb" style="position:absolute;left:36px;right:36px;top:900px;height:130px;border-radius:65px;background:var(--bag);display:flex;align-items:center;justify-content:center;gap:18px;'
     f'font:800 34px Jakarta;color:var(--plum);white-space:nowrap">{BAG.format(s=60)}TEKAN BEG KUNING</div></div>'
     '<div id="shr" style="position:absolute;left:470px;top:1040px;width:140px;height:140px;border-radius:50%;border:7px solid var(--cream)"></div>'
     '<div class="lab" id="stl" style="position:absolute;left:150px;top:1350px;color:var(--cream)">Stok</div>'
     '<div id="stb" style="position:absolute;left:150px;top:1400px;width:780px;height:26px;border-radius:13px;background:rgba(251,246,242,.25);overflow:hidden">'
     '<i id="stf" style="position:absolute;left:0;top:0;bottom:0;width:100%;border-radius:13px;background:var(--bag);transform-origin:0 50%"></i></div>'
     '<div class="pill r" id="stp" style="left:640px;top:1300px;font-size:30px;padding:14px 28px">TERHAD!</div>')
js.append(f'tl.fromTo("#ph",{{y:500,rotation:8,opacity:0}},{{y:0,rotation:0,opacity:1,duration:0.5,ease:"expo.out"}},{SHOP:.2f});')
S(SHOP, "whip", 0.55)
tk = W("tekan", SHOP)
js.append(f'tl.fromTo("#shr",{{scale:0.2,opacity:1}},{{scale:1.8,opacity:0,duration:0.5,ease:"power2.out"}},{tk + 0.2:.2f});')
js.append(f'tl.fromTo("#bagb",{{scale:1}},{{scale:0.93,duration:0.1,yoyo:true,repeat:1}},{tk + 0.2:.2f});')
S(tk + 0.2, "click", 0.75); S(tk + 0.25, "ding", 0.55)
js.append(f'tl.to("#bagb",{{scale:1.04,duration:0.35,yoyo:true,repeat:3,ease:"sine.inOut"}},{tk + 0.6:.2f});')
tst = W("stok", SHOP)
fade("#stl", tst - 0.2, 0.3, y=10); fade("#stb", tst - 0.2, 0.3, y=10)
js.append(f'tl.fromTo("#stf",{{scaleX:0.55}},{{scaleX:0.1,duration:1.6,ease:"power2.inOut"}},{tst:.2f});')
js.append(f'tl.to("#stf",{{backgroundColor:"#b02a45",duration:0.6}},{tst + 0.8:.2f});')
S(tst, "riser", 0.35)
pop("#stp", W("terhad") - 0.1, 0.35, rot=-4)
js.append(f'tl.to("#stp",{{scale:1.1,duration:0.12,yoyo:true,repeat:1}},{W("terhad") + 0.3:.2f});')
S(W("terhad"), "buzz", 0.35)

# ======================= CO: Tekan beg kuning dan check out =======================
back("cob_", CO, VOICE_END + 0.6 - CO, '<div class="blushbg"></div><div class="grain"></div>')
conf = "".join(f'<i class="cf" style="position:absolute;left:530px;top:1110px;width:{r}px;height:{r}px;border-radius:{"50%" if k % 2 else "4px"};background:{c}"></i>'
               for k, (r, c) in enumerate([(18, "var(--rose)"), (14, "var(--bag)"), (20, "var(--violet)"), (12, "var(--champ)"), (16, "var(--rose)"),
                                           (14, "var(--bag)"), (18, "var(--violet)"), (12, "var(--rose)"), (16, "var(--champ)"), (14, "var(--bag)")]))
clip("co", CO, VOICE_END + 0.6 - CO,
     f'<div id="cobag" style="position:absolute;left:330px;top:230px;width:420px;height:420px;display:flex;align-items:center;justify-content:center;'
     f'border-radius:50%;background:var(--cream);box-shadow:0 30px 70px rgba(59,29,46,.2)">{BAG.format(s=300)}</div>'
     '<div id="cor" style="position:absolute;left:470px;top:370px;width:140px;height:140px;border-radius:50%;border:7px solid var(--rose)"></div>'
     f'<div class="t c" style="top:710px;font:700 60px Jakarta">{R("coa","Tekan")}</div>'
     f'<div class="t c big" style="top:790px;font-size:160px">{R("cob","beg kuning")}</div>'
     '<div id="cobtn" style="position:absolute;left:250px;top:1050px;width:580px;height:130px;border-radius:65px;background:var(--plum);color:var(--cream);'
     'display:flex;align-items:center;justify-content:center;gap:20px;font:800 46px Jakarta;letter-spacing:4px;box-shadow:0 20px 50px rgba(59,29,46,.35)">'
     '<span id="cotx">CHECK OUT</span><svg id="cotk" viewBox="0 0 100 100" style="width:70px;height:70px"><path d="M20 52 L42 72 L80 30" stroke="var(--bag)" stroke-width="12" fill="none" '
     'stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="100" stroke-dashoffset="100"/></svg></div>' + conf)
js.append(f'tl.fromTo("#cobag",{{scale:0,rotation:-25}},{{scale:1,rotation:0,duration:0.45,ease:"back.out(1.8)"}},{CO:.2f});')
S(CO, "whip", 0.5); S(CO + 0.05, "pop", 0.6)
js.append(f'tl.fromTo("#cor",{{scale:0.3,opacity:1}},{{scale:2.2,opacity:0,duration:0.5,ease:"power2.out"}},{W("kuning", CO):.2f});')
js.append(f'tl.fromTo("#cobag",{{scale:1}},{{scale:0.9,duration:0.1,yoyo:true,repeat:1}},{W("kuning", CO):.2f});')
S(W("kuning", CO), "click", 0.7)
rv("#coa", CO + 0.05); rv("#cob", W("beg", CO) - 0.05)
tch = W("check", CO)
js.append(f'tl.fromTo("#cobtn",{{y:120,opacity:0}},{{y:0,opacity:1,duration:0.35,ease:"back.out(1.8)"}},{W("dan", CO) - 0.1:.2f});')
js.append(f'tl.to("#cobtn",{{scale:0.93,duration:0.1,yoyo:true,repeat:1}},{tch:.2f});')
js.append(f'tl.to("#cobtn",{{backgroundColor:"#b02a45",duration:0.3}},{tch + 0.15:.2f});')
js.append(f'tl.to("#cotk path",{{strokeDashoffset:0,duration:0.3,ease:"power2.out"}},{tch + 0.2:.2f});')
S(tch, "click", 0.7); S(tch + 0.2, "ding", 0.65)
for k in range(10):
    a = -math.pi / 2 + (k - 4.5) * 0.33
    js.append(f'tl.fromTo("#co .cf:nth-of-type({k + 1})",{{x:0,y:0,opacity:1,rotation:0}},{{x:{math.cos(a) * 380:.0f},y:{math.sin(a) * 300 + 120:.0f},rotation:{180 + k * 40},opacity:0,duration:1.0,ease:"power2.out"}},{tch + 0.25:.2f});')
S(tch + 0.25, "shimmer", 0.5)

# ======================= END CARD =======================
clip("end", VOICE_END, DURATION - VOICE_END,
     '<div class="plumbg"></div>'
     + img("enp", "assets/product/duo_diag.jpg", (340, 240, 400, 700), "50% 50%", 200)
     + f'<div class="t c cream" style="top:1030px;font:400 116px/1 Gloock;left:40px;right:40px">{CH("en0","Frescura Body")}</div>'
     f'<div class="t c lab" style="top:1190px;color:var(--nude)">{R("en1","Woman Glory &middot; Noche")}</div>'
     f'<div class="pill" id="enb" style="left:290px;top:1290px;background:var(--bag);font-size:34px">{BAG.format(s=48)}TEKAN BEG KUNING</div>')
js.append(f'tl.fromTo("#end",{{clipPath:"circle(0% at 50% 40%)"}},{{clipPath:"circle(130% at 50% 40%)",duration:0.55,ease:"expo.inOut"}},{VOICE_END:.2f});')
js.append(f'tl.fromTo("#enp",{{clipPath:"inset(100% 0% 0% 0% round 200px)"}},{{clipPath:"inset(0% 0% 0% 0% round 200px)",duration:0.6,ease:"expo.out"}},{VOICE_END + 0.2:.2f});')
chars("#en0", VOICE_END + 0.35, 0.03); rv("#en1", VOICE_END + 0.75); pop("#enb", VOICE_END + 0.9, 0.35)
S(VOICE_END, "whip", 0.5); S(VOICE_END + 0.35, "chime", 0.5)

# ---- scene changes must fall between words
_tops = []
for h in html:
    m = re.search(r'id="([^"]+)"[^>]*data-start="([\d.]+)" data-duration="([\d.]+)"', h)
    if m and not m.group(1).startswith(("cap", "wp", "chrome", "cob", "co")):
        _tops.append((m.group(1), round(float(m.group(2)) + float(m.group(3)), 3)))
_bad = [(i, e, w["w"]) for i, e in _tops for w in words if w["s"] + 0.04 < e < w["e"] - 0.04 and e < VOICE_END - 0.05]
if _bad: print("WARNING scene ends mid-word:", _bad)

# ---- captions: words pop in as spoken; keywords switch to Gloock rose
for ci, ch in enumerate(chunks):
    st = ch[0]["s"]
    if st < FACE_END - 0.05 or st >= VOICE_END:
        continue
    nxt = chunks[ci + 1][0]["s"] if ci + 1 < len(chunks) else VOICE_END
    en = min(nxt, ch[-1]["e"] + 0.45) if nxt - ch[-1]["e"] > 0.6 else nxt
    en = min(en, VOICE_END)
    sp = []
    for wi, w in enumerate(ch):
        key = re.sub(r"[^a-z0-9]", "", w["t"].lower())
        sp.append(f'<span id="w{ci}_{wi}" class="w{" k" if key in KEY else ""}">{w["t"].rstrip(".,!")}</span>')
        if wi:
            js.append(f'tl.fromTo("#w{ci}_{wi}",{{opacity:0,y:24,scale:0.85}},{{opacity:1,y:0,scale:1,duration:0.14,ease:"back.out(2.5)"}},{w["s"]:.2f});')
    dk = any(a - 0.05 <= st < b for a, b in DARK)
    clip(f"cap{ci}", st, max(en - st, 0.2), f'<span class="ln{" dk" if dk else ""}">' + " ".join(sp) + "</span>", cls="cap")
    js.append(f'tl.fromTo("#cap{ci} .ln",{{y:26,opacity:0}},{{y:0,opacity:1,duration:0.14,ease:"power3.out"}},{st:.2f});')

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
        js.append(f'tl.fromTo("#flash",{{opacity:0.22}},{{opacity:0,duration:0.2,ease:"power2.out"}},{c["t"]:.3f});')
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
print(len(chunks), "caption chunks,", len(js), "tweens,", len(kept), "sfx cues, duration", DURATION)
