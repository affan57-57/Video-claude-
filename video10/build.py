"""Video 10 -- "3 rahsia wangi tanpa perfume" in a new "Lilac Silk" perfume-advert minimalist-luxury style.
Italiana (high-fashion display) + Urbanist; chat-bubble cascade hook, "watch to the end" progress bar, line-art perfume bottle crossed out
and swapped for the client's own product footage, roman-numeral rail (I / II / III), aroma-swirl line drawings, scent selector cards
with a cursor, the client's pump/foam demo, silk-ribbon transitions, stock icons that run out, checkout tick,
captions on a pearl label card where each word fills with ink as it is spoken.
Usage: python3 -I build.py PROJECT_DIR [--final]"""
import json, math, re, sys

proj = sys.argv[1]
FINAL = "--final" in sys.argv
words = [w for s in json.load(open(f"{proj}/assets/audio/words.json")) for w in s["words"]]
REAL_END = round(words[-1]["e"], 2)
VOICE_END = round(REAL_END + 0.5, 2)
DURATION = round(VOICE_END + 1.6, 2)

FIX = {"bombshell": "Bombshell", "minat": "Midnight", "fantasi": "Fantasy", "up": "out"}
KEY = {"perfume", "wajib", "habis", "3", "rahsia", "wangi", "frescura", "body", "inspirasi", "spray", "pilih", "fresh", "feminine",
       "bombshell", "tekan", "berbuih", "sea", "salt", "mineral", "segar", "melekat", "kuning", "terhad", "check", "out", "sekarang", "sama"}
VIO = {"manis", "fruity", "midnight", "fantasy"}
clean = []
for i, w in enumerate(words):
    txt = w["w"].strip(); core = txt.rstrip(".,?!"); tail = txt[len(core):]
    nxt = words[i + 1]["w"].strip().lower() if i + 1 < len(words) else ""
    if core == "Fresh" and nxt.startswith("fura"):
        clean.append({"t": "Frescura", "s": w["s"], "e": words[i + 1]["e"]}); continue
    if core == "Fura": continue
    if core.lower().startswith("sisap"):                     # "Ada sea salt, yang kaya mineral"
        m = (w["s"] + w["e"]) / 2
        clean.append({"t": "sea", "s": w["s"], "e": m}); clean.append({"t": "salt" + tail, "s": m, "e": w["e"]}); continue
    txt = FIX.get(core, core) + tail
    if txt.startswith("-") and clean:
        clean[-1]["t"] += txt; clean[-1]["e"] = w["e"]; continue
    clean.append({"t": txt, "s": w["s"], "e": w["e"]})

def W(word, after=0.0):
    for w in clean:
        if w["s"] >= after - 0.01 and re.sub(r"[^a-z0-9]", "", w["t"].lower()) == word: return w["s"]
    raise KeyError(word)

FACE_END, S1, S2, S3, R1A, R1B, R2A, R2B, R2C, R3A, R3B, R3C, R3D, C1, C2, C3, C4 = (
    0.76, 0.76, 2.20, 3.97, 6.84, 10.07, 12.73, 14.53, 16.82, 18.87, 21.11, 22.67, 23.80, 24.82, 26.25, 28.02, 29.50)
CUTS = [S1, S2, S3, R1A, R1B, R2A, R2B, R2C, R3A, R3B, R3C, R3D, C1, C2, C3, C4, VOICE_END]

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
def full(id_, src, s, d, z0=1.12):
    html.append(f'<video id="{id_}" class="clip bg" src="{src}" data-start="{s:.3f}" data-duration="{d:.3f}" data-media-start="0" muted playsinline></video>')
    js.append(f'tl.fromTo("#{id_}",{{scale:{z0}}},{{scale:1.0,duration:{d:.2f},ease:"power2.out"}},{s:.2f});')
def ivid(id_, src, s, d, box, extra=""):
    l, t_, w, h = box
    html.append(f'<video id="{id_}" class="clip" src="{src}" data-start="{s:.3f}" data-duration="{d:.3f}" data-media-start="0" muted playsinline '
                f'style="z-index:3;left:{l}px;top:{t_}px;width:{w}px;height:{h}px;object-fit:cover;{extra}"></video>')
SHADOW = "box-shadow:0 34px 80px rgba(29,26,44,.25);"
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
def chars(sel, t, stagger=0.035):
    js.append(f'tl.fromTo("{sel} .ch",{{opacity:0,y:20,filter:"blur(10px)",x:(i,el,a)=>(i-(a.length-1)/2)*22}},{{opacity:1,y:0,filter:"blur(0px)",x:0,duration:0.5,stagger:{stagger},ease:"expo.out"}},{t:.2f});')
    S(t, "shimmer", 0.35, auto=True)
def img(id_, src, box, pos="50% 50%", radius="36px", extra=""):
    l, t_, w, h = box
    return (f'<div id="{id_}" class="frame" style="left:{l}px;top:{t_}px;width:{w}px;height:{h}px;border-radius:{radius};{extra}">'
            f'<img src="{src}" alt="" style="object-position:{pos}"></div>')
def ribbon(id_, t):
    """chapter change: a wide silk band (lilac -> pearl -> lilac) sweeps diagonally across the frame"""
    clip(id_, t - 0.3, 0.62, '<div class="rb" style="position:absolute;top:-400px;left:0;width:2200px;height:2800px;transform:skewX(-22deg);'
         'background:linear-gradient(90deg,rgba(143,128,191,0) 0%,#c9c0dc 18%,#faf8fb 50%,#c9c0dc 82%,rgba(143,128,191,0) 100%)"></div>', style="z-index:9")
    js.append(f'tl.fromTo("#{id_} .rb",{{x:-2600}},{{x:1500,duration:0.6,ease:"power2.inOut"}},{t - 0.3:.3f});')
    S(t - 0.28, "swoosh", 0.55); S(t - 0.05, "whip", 0.4)
SWIRL = ["M0 300 C 40 250, -40 200, 0 150 S 40 50, 0 0", "M0 300 C -50 240, 50 190, 0 140 S -45 60, 10 0", "M0 300 C 35 230, -35 170, 5 110 S 30 40, -5 0"]
def swirls(id_, x0, y0, scale=1.0, color="var(--lilac)", w=6):
    return "".join(f'<svg class="sw" id="{id_}{k}" style="position:absolute;left:{x0 + k * 70 - 60}px;top:{y0 - 300 * scale:.0f}px;width:120px;height:{300 * scale + 10:.0f}px;overflow:visible" '
                   f'viewBox="-60 0 120 310"><path d="{p}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-dasharray="420" stroke-dashoffset="420"/></svg>'
                   for k, p in enumerate(SWIRL))
def swirls_js(id_, t):
    for k in range(3):
        js.append(f'tl.to("#{id_}{k} path",{{strokeDashoffset:0,duration:0.9,ease:"power2.out"}},{t + k * 0.12:.2f});')
        js.append(f'tl.fromTo("#{id_}{k}",{{y:40,opacity:0}},{{y:-30,opacity:1,duration:1.4,ease:"sine.out"}},{t + k * 0.12:.2f});')
    S(t, "shimmer", 0.4)
BAG = ('<svg viewBox="0 0 100 100" style="width:{s}px;height:{s}px"><path d="M18 34 H82 L76 90 H24 Z" fill="var(--bag)" stroke="var(--ink)" stroke-width="4" stroke-linejoin="round"/>'
       '<path d="M36 40 V28 a14 14 0 0 1 28 0 V40" fill="none" stroke="var(--ink)" stroke-width="5" stroke-linecap="round"/></svg>')
HAND = ('<svg viewBox="0 0 80 100" style="width:{s}px;height:{s}px"><path d="M30 8 a8 8 0 0 1 16 0 V44 l18 6 a8 8 0 0 1 6 9 L64 92 H26 L8 62 a7 7 0 0 1 11 -8 L30 64 Z" '
        'fill="var(--pearl)" stroke="var(--ink)" stroke-width="3.5" stroke-linejoin="round"/></svg>')
def bubbles(prefix, items):
    out = ""
    for k, (txt, x, y, right, col) in enumerate(items):
        cls = "bub rt" if right else "bub"
        pos = f"right:{x}px" if right else f"left:{x}px"
        av = (f'<div class="av" style="{pos.replace(str(x), str(x - 90)) if not right else "right:" + str(x - 90) + "px"};top:{y + 30}px;background:{col}"></div>')
        out += f'<div id="{prefix}{k}" style="position:absolute;inset:0">{av}<div class="{cls}" style="{pos};top:{y}px">{txt}</div></div>'
    return out

# ======================= S0: the only face shot (0.76 s) -- "Kalau kau nak orang..." =======================
html.append(f'<video id="v_face" class="clip bg" src="assets/broll/face.mp4" data-start="0" data-duration="{FACE_END:.3f}" data-media-start="0" muted playsinline style="z-index:6"></video>')
js.append(f'tl.fromTo("#v_face",{{scale:1.0}},{{scale:1.08,duration:{FACE_END},ease:"power1.out"}},0);')
S(0.0, "boom", 0.45)

# ======================= S1: orang tanya kau pakai perfume apa ni (chat bubbles) =======================
back("s1b_", S1, S2 - S1, '<div class="silkbg"></div>')
B1 = [("Pakai perfume apa ni?", 180, 300, False, "var(--rose)"), ("Wanginya! Perfume apa?", 180, 520, True, "var(--violet)"),
      ("Bau apa ni? Sedapnya", 180, 740, False, "var(--lilac)")]
clip("s1", S1, S2 - S1, bubbles("s1q", B1)
     + f'<div class="t c it" style="top:960px;font-size:230px;line-height:1">{CH("s1p","perfume")}</div>'
     f'<div class="t c" style="top:1210px;font:800 90px Urbanist;color:var(--lilac)">{R("s1a","apa ni?")}</div>')
for k, t_ in enumerate([S1 + 0.02, S1 + 0.22, S1 + 0.42]):
    js.append(f'tl.fromTo("#s1q{k}",{{scale:0.4,opacity:0,y:40,transformOrigin:"{"100%" if B1[k][3] else "0%"} 100%"}},{{scale:1,opacity:1,y:0,duration:0.3,ease:"back.out(2.2)"}},{t_:.2f});')
    S(t_, "pop", 0.55)
chars("#s1p", W("perfume") - 0.1, 0.03); rv("#s1a", W("apa"))

# ======================= S2: kau wajib tengok video ni sampai habis (progress bar) =======================
back("s2b_", S2, S3 - S2, '<div class="inkbg"></div>')
clip("s2", S2, S3 - S2,
     '<div id="s2pl" style="position:absolute;left:440px;top:330px;width:200px;height:200px;border-radius:50%;border:4px solid var(--pearl);display:flex;align-items:center;justify-content:center">'
     '<svg viewBox="0 0 100 100" style="width:90px;height:90px;margin-left:12px"><path d="M20 10 L88 50 L20 90 Z" fill="var(--pearl)"/></svg></div>'
     f'<div class="t c" style="top:620px;font:800 72px Urbanist;color:var(--haze)">{R("s2a","Wajib tengok")}</div>'
     f'<div class="t c it pearl" style="top:720px;font-size:150px;line-height:1">{R("s2b","sampai habis")}</div>'
     '<div id="s2bar" style="position:absolute;left:140px;top:1000px;width:800px;height:16px;border-radius:8px;background:rgba(250,248,251,.2);overflow:hidden">'
     '<i id="s2f" style="position:absolute;inset:0;border-radius:8px;background:linear-gradient(90deg,var(--lilac),var(--pearl));transform-origin:0 50%"></i></div>'
     '<div id="s2n" style="position:absolute;left:140px;top:1040px;width:800px;text-align:right;font:800 54px Urbanist;color:var(--pearl)"><span id="s2v">0</span>%</div>')
js.append(f'tl.fromTo("#s2pl",{{scale:0,rotation:-90}},{{scale:1,rotation:0,duration:0.4,ease:"back.out(2)"}},{S2:.2f});')
S(S2, "whip", 0.5)
rv("#s2a", W("wajib") - 0.05); rv("#s2b", W("sampai") - 0.05)
js.append(f'tl.fromTo("#s2f",{{scaleX:0}},{{scaleX:1,duration:{W("habis") + 0.3 - W("tengok"):.2f},ease:"power1.inOut"}},{W("tengok"):.2f});')
js.append(f'tl.fromTo("#s2v",{{textContent:0}},{{textContent:100,duration:{W("habis") + 0.3 - W("tengok"):.2f},ease:"power1.inOut",snap:{{textContent:1}}}},{W("tengok"):.2f});')
S(W("tengok"), "riser", 0.35); S(W("habis") + 0.3, "ding", 0.5)

# ======================= S3: 3 rahsia wangi tanpa perfume -- Frescura Body =======================
ribbon("rb1", S3)
back("s3b_", S3, R1A - S3, '<div class="silkbg"></div>')
ivid("v_her", "assets/broll/hero.mp4", W("frescura"), R1A - W("frescura"), (290, 640, 500, 760), "border-radius:250px 250px 36px 36px;" + SHADOW)
clip("s3", S3, R1A - S3,
     f'<div style="position:absolute;left:80px;top:120px;font:400 360px/1 Italiana;color:var(--lilac)">{R("s3n","3")}</div>'
     f'<div style="position:absolute;left:330px;top:190px;font:400 130px/1 Italiana">{R("s3r","Rahsia")}</div>'
     f'<div style="position:absolute;left:330px;top:330px;font:800 64px Urbanist">{R("s3w","wangi")} {R("s3t","<span class=rose>tanpa perfume</span>")}</div>'
     '<svg id="s3bt" style="position:absolute;left:340px;top:640px;width:400px;height:760px" viewBox="0 0 200 380">'
     '<g fill="none" stroke="var(--ink)" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="900" stroke-dashoffset="900">'
     '<path d="M80 20 H120 V70 H80 Z"/><path d="M70 70 H130 V110 H70 Z"/><path d="M40 110 H160 Q180 110 180 140 V340 Q180 370 150 370 H50 Q20 370 20 340 V140 Q20 110 40 110 Z"/>'
     '<path d="M45 180 H155"/><path d="M60 260 Q100 240 140 260"/></g>'
     '<path id="s3x" d="M0 380 L200 60" stroke="var(--rose)" stroke-width="12" stroke-linecap="round" stroke-dasharray="400" stroke-dashoffset="400"/></svg>'
     '<div class="tag k" id="s3fb" style="left:300px;top:1340px;font:400 64px Italiana;letter-spacing:2px;padding:14px 46px">Frescura Body</div>')
js.append(f'tl.fromTo("#s3n > span",{{yPercent:118}},{{yPercent:0,duration:0.5,ease:"expo.out"}},{S3:.2f});')
S(S3, "boom", 0.45)
rv("#s3r", W("rahsia") - 0.05); rv("#s3w", W("wangi") - 0.05); rv("#s3t", W("tanpa") - 0.05)
js.append(f'tl.to("#s3bt g",{{strokeDashoffset:0,duration:0.7,ease:"power2.out"}},{W("wangi") - 0.1:.2f});')
S(W("wangi") - 0.1, "swoosh", 0.35)
js.append(f'tl.to("#s3x",{{strokeDashoffset:0,duration:0.25,ease:"power3.out"}},{W("perfume", S3) + 0.05:.2f});')
S(W("perfume", S3) + 0.05, "buzz", 0.4)
tf = W("frescura")
js.append(f'tl.to("#s3bt",{{opacity:0,scale:0.9,duration:0.25}},{tf - 0.05:.2f});')
js.append(f'tl.fromTo("#v_her",{{clipPath:"inset(100% 0% 0% 0% round 250px 250px 36px 36px)"}},{{clipPath:"inset(0% 0% 0% 0% round 250px 250px 36px 36px)",duration:0.5,ease:"expo.out"}},{tf:.2f});')
pop("#s3fb", tf + 0.25, 0.35); S(tf, "chime", 0.5)

# roman-numeral rail
rail = "".join(f'<div class="rn" id="rn{k}">{n}</div>' for k, n in enumerate(["I", "II", "III"]))
clip("chrome", R1A, C1 - R1A, f'<div id="rail">{rail}</div>', style="z-index:8")
js.append(f'tl.fromTo("#rail .rn",{{x:-80,opacity:0}},{{x:0,opacity:1,duration:0.35,stagger:0.07,ease:"back.out(2)"}},{R1A:.2f});')
def rail_on(k, t, lite):
    js.append(f'tl.set("#rail",{{attr:{{class:"{"lite" if lite else ""}"}}}},{t:.2f});')
    js.append(f'tl.to("#rn{k}",{{color:"#b02a45",scale:1.35,duration:0.3,ease:"back.out(3)"}},{t:.2f});')
    if k: js.append(f'tl.to("#rn{k - 1}",{{color:"rgba(143,128,191,.55)",scale:1,duration:0.3}},{t:.2f});')
def rail_lite(t, lite): js.append(f'tl.set("#rail",{{attr:{{class:"{"lite" if lite else ""}"}}}},{t:.2f});')
def head(id_, num, label, light=False):
    return (f'<div id="{id_}n" style="position:absolute;left:130px;top:120px;font:400 300px/1 Italiana;color:{"var(--haze)" if light else "var(--lilac)"}">{num}</div>'
            f'<div id="{id_}l" class="lab" style="position:absolute;left:{170 + 90 * len(num)}px;top:230px;{"color:var(--haze)" if light else ""}">Rahsia {label}</div>')
def head_js(id_, t):
    js.append(f'tl.fromTo("#{id_}n",{{opacity:0,filter:"blur(16px)",scale:1.3}},{{opacity:1,filter:"blur(0px)",scale:1,duration:0.5,ease:"expo.out"}},{t:.2f});')
    fade(f"#{id_}l", t + 0.12, 0.35, y=0, x=-30); S(t, "chime", 0.45)

# ======================= R1A: Rahsia pertama -- bau dia memang inspirasi perfume =======================
ribbon("rb2", R1A)
back("r1b_", R1A, R1B - R1A, '<div class="silkbg"></div>')
clip("r1a", R1A, R1B - R1A,
     head("h1", "I", "Pertama")
     + f'<div style="position:absolute;left:130px;top:430px;font:800 60px Urbanist">{R("r1b","bau dia memang")}</div>'
     f'<div style="position:absolute;left:130px;top:510px;font:400 150px/1 Italiana">{R("r1c","inspirasi")}</div>'
     f'<div style="position:absolute;left:130px;top:650px;font:400 150px/1 Italiana;color:var(--rose)">{R("r1d","perfume")}</div>'
     + img("r1g", "assets/product/glory_card.jpg", (560, 840, 300, 680), "50% 50%", "28px")
     + swirls("r1s", 520, 840, 1.0) + swirls("r1t", 860, 900, 0.8, "var(--rose)", 5))
head_js("h1", R1A); rail_on(0, W("pertama"), False)
rv("#r1b", W("bau") - 0.05); rv("#r1c", W("inspirasi") - 0.05); rv("#r1d", W("perfume", R1A) - 0.05)
js.append(f'tl.fromTo("#r1g",{{y:300,rotation:8,opacity:0}},{{y:0,rotation:-3,opacity:1,duration:0.6,ease:"expo.out"}},{W("bau") - 0.1:.2f});')
S(W("bau") - 0.1, "whip", 0.45)
swirls_js("r1s", W("inspirasi")); swirls_js("r1t", W("perfume", R1A))

# ======================= R1B: lepas mandi pun orang ingat kau baru spray perfume =======================
full("v_sid", "assets/broll/side.mp4", R1B, R2A - R1B, z0=1.15)
mist = "".join(f'<i class="ms" style="position:absolute;left:{x}px;top:{y}px;width:{r}px;height:{r}px;border-radius:50%;background:rgba(250,248,251,.95)"></i>'
               for x, y, r in [(500, 1000, 12), (560, 940, 8), (620, 1060, 14), (700, 980, 9), (760, 1080, 7), (520, 1120, 10), (660, 900, 7), (600, 1010, 6), (720, 920, 11)])
clip("r1s_", R1B, R2A - R1B,
     '<div class="veil" style="background:linear-gradient(180deg,rgba(29,26,44,.85) 0%,rgba(29,26,44,.25) 55%,rgba(29,26,44,.6) 100%)"></div>'
     f'<div class="t lab" style="top:170px;left:130px;color:var(--haze)">{R("r1sa","Lepas mandi pun")}</div>'
     '<div class="bub rt" id="r1sq" style="right:90px;top:260px;font-size:50px">Eh, baru spray perfume ke?</div>'
     f'<div class="t c it pearl" style="top:480px;font-size:180px;line-height:1">{R("r1sb","baru spray")}</div>' + mist)
rail_lite(R1B, True)
rv("#r1sa", R1B + 0.05)
js.append(f'tl.fromTo("#r1sq",{{scale:0.4,opacity:0,transformOrigin:"100% 100%"}},{{scale:1,opacity:1,duration:0.35,ease:"back.out(2.2)"}},{W("ingat") - 0.1:.2f});')
S(W("ingat") - 0.1, "pop", 0.55)
rv("#r1sb", W("baru", R1B) - 0.05)
js.append(f'tl.fromTo("#r1s_ .ms",{{opacity:0,y:80,scale:0.3}},{{opacity:0.95,y:-260,scale:1,duration:1.2,stagger:0.06,ease:"power1.out"}},{W("spray") - 0.15:.2f});')
S(W("spray") - 0.15, "spray", 0.6)

# ======================= R2: Rahsia kedua -- pilih bau kau (selector cards + cursor) =======================
ribbon("rb3", R2A)
back("r2b_", R2A, R3A - R2A, '<div class="silkbg"></div>')
CA, CB = (70, 640, 455, 820), (555, 640, 455, 820)
ivid("v_rse", "assets/broll/rose.mp4", R2B, R3A - R2B, (CA[0], CA[1], CA[2], 560), "border-radius:36px 36px 0 0;")
ivid("v_ber", "assets/broll/berries.mp4", R2C, R3A - R2C, (CB[0], CB[1], CB[2], 560), "border-radius:36px 36px 0 0;")
def card(id_, box, letter):
    l, t_, w, h = box
    return (f'<div id="{id_}" style="position:absolute;left:{l}px;top:{t_}px;width:{w}px;height:{h}px;border-radius:36px;background:var(--pearl);'
            f'box-shadow:0 30px 70px rgba(29,26,44,.18);border:3px solid rgba(143,128,191,.35);z-index:-1">'
            f'<div style="position:absolute;inset:0 0 260px 0;border-radius:36px 36px 0 0;background:linear-gradient(160deg,#e3ddee,#cfc6e2);display:flex;align-items:center;justify-content:center;'
            f'font:400 260px Italiana;color:rgba(29,26,44,.25)">{letter}</div></div>')
clip("r2", R2A, R3A - R2A,
     head("h2", "II", "Kedua")
     + f'<div style="position:absolute;left:130px;top:430px;font:400 140px/1 Italiana">{R("r2t","Pilih bau")} {R("r2u","<span class=lilac>kau</span>")}</div>'
     + '<div id="r2cards" style="position:absolute;inset:0;z-index:0">' + card("r2ca", CA, "A") + card("r2cb", CB, "B") + '</div>'
     f'<div id="r2na" style="position:absolute;left:{CA[0] + 30}px;top:{CA[1] + 580}px;width:{CA[2] - 60}px"><div style="font:400 62px/1 Italiana;color:var(--rose)">Woman Glory</div>'
     '<div class="lab" style="font-size:22px;letter-spacing:5px;margin-top:10px;color:var(--rose)">by Bombshell</div>'
     '<div style="display:flex;gap:10px;margin-top:18px"><span class="tag r" id="r2f1" style="position:relative;font-size:22px;padding:10px 18px">FRESH</span>'
     '<span class="tag r" id="r2f2" style="position:relative;font-size:22px;padding:10px 18px">FEMININE</span></div></div>'
     f'<div id="r2nb" style="position:absolute;left:{CB[0] + 30}px;top:{CB[1] + 580}px;width:{CB[2] - 60}px"><div style="font:400 62px/1 Italiana;color:var(--violet)">Noche</div>'
     '<div class="lab" style="font-size:22px;letter-spacing:5px;margin-top:10px;color:var(--violet)">by Midnight Fantasy</div>'
     '<div style="display:flex;gap:10px;margin-top:18px"><span class="tag v" id="r2m1" style="position:relative;font-size:22px;padding:10px 18px">MANIS</span>'
     '<span class="tag v" id="r2m2" style="position:relative;font-size:22px;padding:10px 18px">FRUITY</span></div></div>'
     + "".join(f'<div id="{i}" style="position:absolute;left:{b[0] + b[2] - 110}px;top:{b[1] + 20}px;width:90px;height:90px;border-radius:50%;background:{c};'
               f'display:flex;align-items:center;justify-content:center;box-shadow:0 10px 24px rgba(0,0,0,.25)"><svg viewBox="0 0 100 100" style="width:56px;height:56px">'
               f'<path d="M22 52 L42 72 L80 30" stroke="var(--pearl)" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></div>'
               for i, b, c in (("r2ka", CA, "var(--rose)"), ("r2kb", CB, "var(--violet)")))
     + f'<div id="cur" style="position:absolute;left:520px;top:1100px">{HAND.format(s=130)}</div>')
head_js("h2", R2A); rail_on(1, W("kedua"), False)
rv("#r2t", W("pilih") - 0.05); rv("#r2u", W("kau", W("pilih")) - 0.05)
js.append(f'tl.fromTo("#r2ca, #r2cb",{{y:300,opacity:0}},{{y:0,opacity:1,duration:0.5,stagger:0.1,ease:"expo.out"}},{W("boleh") - 0.1:.2f});')
S(W("boleh") - 0.1, "whip", 0.45)
js.append(f'tl.fromTo("#cur",{{opacity:0,x:200,y:300}},{{opacity:1,x:0,y:0,duration:0.5,ease:"power2.out"}},{W("pilih"):.2f});')
js.append(f'tl.to("#cur",{{x:-260,y:-200,duration:0.5,ease:"power2.inOut"}},{R2B:.2f});')
js.append(f'tl.fromTo("#v_rse",{{clipPath:"inset(100% 0% 0% 0% round 36px 36px 0 0)"}},{{clipPath:"inset(0% 0% 0% 0% round 36px 36px 0 0)",duration:0.45,ease:"expo.out"}},{R2B:.2f});')
S(R2B, "swoosh", 0.4)
fade("#r2na", R2B + 0.15, 0.35, y=20)
pop("#r2f1", W("fresh", R2B), 0.3); pop("#r2f2", W("feminine"), 0.3)
ta = W("ambil")
js.append(f'tl.to("#cur",{{scale:0.85,duration:0.08,yoyo:true,repeat:1}},{ta + 0.2:.2f});')
js.append(f'tl.to("#r2ca",{{borderColor:"#b02a45",borderWidth:6,duration:0.2}},{ta + 0.2:.2f});')
pop("#r2ka", ta + 0.25, 0.3); S(ta + 0.2, "click", 0.7); S(ta + 0.3, "ding", 0.45)
js.append(f'tl.to("#cur",{{x:230,y:-200,duration:0.45,ease:"power2.inOut"}},{R2C:.2f});')
js.append(f'tl.fromTo("#v_ber",{{clipPath:"inset(100% 0% 0% 0% round 36px 36px 0 0)"}},{{clipPath:"inset(0% 0% 0% 0% round 36px 36px 0 0)",duration:0.45,ease:"expo.out"}},{R2C:.2f});')
S(R2C, "swoosh", 0.4)
fade("#r2nb", R2C + 0.15, 0.35, y=20)
pop("#r2m1", W("manis"), 0.3); pop("#r2m2", W("fruity"), 0.3)
tm = W("midnight")
js.append(f'tl.to("#cur",{{scale:0.85,duration:0.08,yoyo:true,repeat:1}},{tm + 0.1:.2f});')
js.append(f'tl.to("#r2cb",{{borderColor:"#5a3f9e",borderWidth:6,duration:0.2}},{tm + 0.1:.2f});')
pop("#r2kb", tm + 0.15, 0.3); S(tm + 0.1, "click", 0.7); S(tm + 0.2, "ding", 0.45)

# ======================= R3A: Rahsia ketiga -- tekan je terus berbuih (client pump demo) =======================
ribbon("rb4", R3A)
full("v_pmp", "assets/broll/pump.mp4", R3A, R3B - R3A, z0=1.1)
TAP = (690, 720)
clip("r3a", R3A, R3B - R3A,
     '<div class="veil" style="background:linear-gradient(180deg,rgba(29,26,44,.8) 0%,rgba(29,26,44,.1) 40%,rgba(29,26,44,0) 70%,rgba(29,26,44,.45) 100%)"></div>'
     + head("h3", "III", "Ketiga", light=True)
     + f'<div style="position:absolute;left:130px;top:420px;font:400 120px/1 Italiana;color:var(--pearl)">{R("r3t","Tekan je,")}</div>'
     f'<div style="position:absolute;left:130px;top:540px;font:800 64px Urbanist;color:var(--bag)">{R("r3u","terus berbuih")}</div>'
     f'<div id="r3r" style="position:absolute;left:{TAP[0] - 80}px;top:{TAP[1] - 80}px;width:160px;height:160px;border-radius:50%;border:7px solid var(--bag)"></div>')
head_js("h3", R3A); rail_on(2, W("ketiga"), True)
rv("#r3t", W("tekan", R3A) - 0.05); rv("#r3u", W("terus", R3A) - 0.05)
tt = W("tekan", R3A)
js.append(f'tl.fromTo("#r3r",{{scale:0.2,opacity:1}},{{scale:1.9,opacity:0,duration:0.55,ease:"power2.out"}},{tt + 0.1:.2f});')
S(tt + 0.1, "click", 0.7); S(W("berbuih") - 0.1, "foam", 0.6)

# ======================= R3B: ada sea salt yang kaya mineral =======================
full("v_sea", "assets/broll/sea.mp4", R3B, R3C - R3B, z0=1.15)
clip("r3b", R3B, R3C - R3B,
     '<div class="veil" style="background:rgba(29,26,44,.35)"></div>'
     f'<div class="t c lab" style="top:500px;color:var(--pearl)">{R("r3ba","ada")}</div>'
     f'<div class="t c it pearl" style="top:560px;font-size:230px;line-height:1">{CH("r3bs","Sea Salt")}</div>'
     '<div class="tag" id="r3bm" style="left:330px;top:860px"><b style="font:400 44px Italiana">&#10022;</b>KAYA MINERAL</div>')
rv("#r3ba", R3B + 0.02); chars("#r3bs", W("sea") - 0.05, 0.04); pop("#r3bm", W("mineral") - 0.1, 0.35, rot=-2)
S(R3B, "whip", 0.45)

# ======================= R3C: kulit rasa segar (lather) =======================
full("v_lth", "assets/broll/lather.mp4", R3C, R3D - R3C, z0=1.1)
clip("r3c", R3C, R3D - R3C,
     '<div class="veil" style="background:linear-gradient(180deg,rgba(29,26,44,.65) 0%,rgba(29,26,44,.1) 50%,rgba(29,26,44,.4) 100%)"></div>'
     f'<div class="t c" style="top:330px;font:800 66px Urbanist;color:var(--pearl)">{R("r3ca","kulit rasa")}</div>'
     f'<div class="t c it pearl" style="top:420px;font-size:260px;line-height:1">{CH("r3cs","segar")}</div>')
rv("#r3ca", W("kulit") - 0.05); chars("#r3cs", W("segar") - 0.1, 0.04); S(R3C, "whip", 0.45); S(W("segar"), "ripple", 0.4)

# ======================= R3D: bau pun melekat (aroma swirls) =======================
full("v_plm", "assets/broll/palm.mp4", R3D, C1 - R3D, z0=1.1)
clip("r3d", R3D, C1 - R3D,
     '<div class="veil" style="background:linear-gradient(180deg,rgba(29,26,44,.7) 0%,rgba(29,26,44,.1) 50%,rgba(29,26,44,.4) 100%)"></div>'
     f'<div class="t c" style="top:300px;font:800 66px Urbanist;color:var(--pearl)">{R("r3da","bau pun")}</div>'
     f'<div class="t c it" style="top:390px;font-size:220px;line-height:1;color:#ffd0dc">{CH("r3dm","melekat")}</div>'
     + swirls("r3dw", 400, 1250, 1.3, "var(--pearl)", 7) + swirls("r3dv", 640, 1300, 1.1, "#ffd0dc", 6))
rv("#r3da", W("bau", R3D) - 0.05); chars("#r3dm", W("melekat") - 0.1, 0.035)
swirls_js("r3dw", R3D + 0.05); swirls_js("r3dv", R3D + 0.25)
js.append(f'tl.to("#rail",{{opacity:0,duration:0.25}},{C1 - 0.3:.2f});')

# ======================= C1: nak orang tanya kau soalan yang sama? (bubble callback) =======================
ribbon("rb5", C1)
back("c1b_", C1, C2 - C1, '<div class="silkbg"></div>')
B2 = [("Pakai perfume apa ni?", 120, 260, False, "var(--rose)"), ("Wanginya! Perfume apa?", 120, 450, True, "var(--violet)"),
      ("Bau apa ni? Sedapnya", 120, 640, False, "var(--lilac)")]
clip("c1", C1, C2 - C1, bubbles("c1q", B2)
     + f'<div class="t c" style="top:900px;font:800 70px Urbanist">{R("c1a","soalan yang")}</div>'
     f'<div class="t c it" style="top:990px;font-size:230px;line-height:1;color:var(--rose)">{CH("c1s","sama?")}</div>')
for k in range(3):
    js.append(f'tl.fromTo("#c1q{k}",{{scale:0.4,opacity:0,y:40,transformOrigin:"{"100%" if B2[k][3] else "0%"} 100%"}},{{scale:1,opacity:1,y:0,duration:0.3,ease:"back.out(2.2)"}},{C1 + 0.05 + k * 0.18:.2f});')
    S(C1 + 0.05 + k * 0.18, "pop", 0.5)
rv("#c1a", W("soalan") - 0.05); chars("#c1s", W("sama") - 0.05, 0.04)

# ======================= C2: tekan beg kuning sekarang dan check out =======================
full("v_hr2", "assets/broll/hero.mp4", C2, C3 - C2, z0=1.2)
clip("c2", C2, C3 - C2,
     '<div class="veil" style="background:linear-gradient(180deg,rgba(235,231,239,.15) 0%,rgba(235,231,239,.25) 50%,rgba(29,26,44,.55) 100%)"></div>'
     f'<div id="c2btn" style="position:absolute;left:120px;top:1180px;width:840px;height:190px;border-radius:95px;background:var(--bag);display:flex;align-items:center;'
     f'justify-content:center;gap:24px;font:900 60px Urbanist;color:var(--ink);letter-spacing:1px;box-shadow:0 26px 60px rgba(0,0,0,.35)">{BAG.format(s=100)}TEKAN BEG KUNING</div>'
     '<div id="c2r" style="position:absolute;left:460px;top:1195px;width:160px;height:160px;border-radius:50%;border:7px solid var(--pearl)"></div>'
     f'<div id="c2h" style="position:absolute;left:560px;top:1260px">{HAND.format(s=150)}</div>'
     '<div class="tag k" id="c2s" style="left:400px;top:1060px;font-size:34px">SEKARANG</div>')
js.append(f'tl.fromTo("#c2btn",{{y:300,scale:0.8,opacity:0}},{{y:0,scale:1,opacity:1,duration:0.4,ease:"back.out(1.8)"}},{C2:.2f});')
S(C2, "whip", 0.5)
tk = W("tekan", C2)
js.append(f'tl.fromTo("#c2h",{{x:120,y:160,opacity:0}},{{x:0,y:0,opacity:1,duration:0.3,ease:"power2.out"}},{tk - 0.15:.2f});')
js.append(f'tl.to("#c2h",{{y:24,duration:0.09,yoyo:true,repeat:1}},{W("kuning", C2):.2f});')
js.append(f'tl.to("#c2btn",{{scale:0.94,duration:0.09,yoyo:true,repeat:1}},{W("kuning", C2):.2f});')
js.append(f'tl.fromTo("#c2r",{{scale:0.2,opacity:1}},{{scale:1.9,opacity:0,duration:0.5,ease:"power2.out"}},{W("kuning", C2) + 0.05:.2f});')
S(W("kuning", C2), "click", 0.75); S(W("kuning", C2) + 0.05, "ding", 0.55)
pop("#c2s", W("sekarang", C2), 0.3, rot=-3)
js.append(f'tl.to("#c2btn",{{scale:1.05,duration:0.3,yoyo:true,repeat:1,ease:"sine.inOut"}},{W("check", C2):.2f});')

# ======================= C3: stok sangat-sangat terhad (bottles run out) =======================
back("c3b_", C3, C4 - C3, '<div class="inkbg"></div>')
BOT = ('<svg viewBox="0 0 40 70" style="width:100%;height:100%"><rect x="14" y="2" width="12" height="10" rx="2" fill="currentColor"/><rect x="11" y="12" width="18" height="8" rx="2" fill="currentColor"/>'
       '<rect x="4" y="20" width="32" height="48" rx="7" fill="currentColor"/></svg>')
bots = "".join(f'<div class="bt" style="position:absolute;left:{150 + (k % 6) * 135}px;top:{760 + (k // 6) * 220}px;width:100px;height:175px;color:{"var(--rose)" if k % 2 == 0 else "var(--violet)"}">{BOT}</div>'
               for k in range(12))
clip("c3", C3, C4 - C3,
     f'<div class="t c it pearl" style="top:300px;font-size:240px;line-height:1">{CH("c3s","Stok")}</div>'
     f'<div class="t c" style="top:560px;font:800 64px Urbanist;color:var(--haze)">{R("c3a","sangat-sangat")}</div>' + bots
     + '<div class="tag r" id="c3t" style="left:340px;top:1230px;font-size:48px;padding:20px 50px">TERHAD!</div>')
chars("#c3s", C3 + 0.02, 0.05); rv("#c3a", W("sangatsangat") - 0.05)
js.append(f'tl.fromTo("#c3 .bt",{{y:60,opacity:0}},{{y:0,opacity:1,duration:0.3,stagger:0.025,ease:"back.out(2)"}},{C3 + 0.05:.2f});')
gone = [11, 4, 9, 2, 7, 10, 5, 0, 8, 3]
for j, k in enumerate(gone):
    t_ = W("sangatsangat") + 0.05 + j * 0.07
    js.append(f'tl.to("#c3 .bt:nth-of-type({k + 1})",{{opacity:0.12,scale:0.8,duration:0.15}},{t_:.2f});')
    S(t_, "tick", 0.35)
pop("#c3t", W("terhad") - 0.1, 0.35, rot=-4); S(W("terhad"), "buzz", 0.4)

# ======================= C4: tekan dan check out sekarang =======================
back("c4b_", C4, VOICE_END + 0.6 - C4, '<div class="silkbg"></div>')
conf = "".join(f'<i class="cf" style="position:absolute;left:530px;top:1000px;width:{r}px;height:{r}px;border-radius:{"50%" if k % 2 else "4px"};background:{c}"></i>'
               for k, (r, c) in enumerate([(18, "var(--rose)"), (14, "var(--bag)"), (20, "var(--violet)"), (12, "var(--lilac)"), (16, "var(--rose)"),
                                           (14, "var(--bag)"), (18, "var(--violet)"), (12, "var(--rose)"), (16, "var(--lilac)"), (14, "var(--bag)")]))
clip("c4", C4, VOICE_END + 0.6 - C4,
     f'<div class="t c" style="top:340px;font:800 70px Urbanist">{R("c4a","Tekan dan")}</div>'
     f'<div class="t c it" style="top:460px;font-size:170px;line-height:1;left:20px;right:20px">{CH("c4c","check out")}</div>'
     '<div id="c4btn" style="position:absolute;left:190px;top:930px;width:700px;height:160px;border-radius:80px;background:var(--ink);color:var(--pearl);'
     'display:flex;align-items:center;justify-content:center;gap:22px;font:900 56px Urbanist;letter-spacing:5px;box-shadow:0 22px 54px rgba(29,26,44,.35)">'
     'CHECK OUT<svg viewBox="0 0 100 100" style="width:76px;height:76px"><path id="c4tk" d="M20 52 L42 72 L80 30" stroke="var(--bag)" stroke-width="12" fill="none" '
     'stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="100" stroke-dashoffset="100"/></svg></div>'
     '<div class="tag" id="c4s" style="left:380px;top:1150px;font-size:36px;background:var(--bag)">SEKARANG</div>' + conf)
rv("#c4a", C4 + 0.05); chars("#c4c", W("check", C4) - 0.25, 0.03)
js.append(f'tl.fromTo("#c4btn",{{y:200,opacity:0}},{{y:0,opacity:1,duration:0.35,ease:"back.out(1.8)"}},{C4 + 0.1:.2f});')
S(C4, "whip", 0.5)
tch = W("check", C4)
js.append(f'tl.to("#c4btn",{{scale:0.93,duration:0.1,yoyo:true,repeat:1}},{tch:.2f});')
js.append(f'tl.to("#c4btn",{{backgroundColor:"#b02a45",duration:0.3}},{tch + 0.15:.2f});')
js.append(f'tl.to("#c4tk",{{strokeDashoffset:0,duration:0.3,ease:"power2.out"}},{tch + 0.2:.2f});')
S(tch, "click", 0.7); S(tch + 0.2, "ding", 0.65)
pop("#c4s", W("sekarang", C4) - 0.05, 0.3, rot=3)
for k in range(10):
    a = -math.pi / 2 + (k - 4.5) * 0.33
    js.append(f'tl.fromTo("#c4 .cf:nth-of-type({k + 1})",{{x:0,y:0,opacity:1,rotation:0}},{{x:{math.cos(a) * 400:.0f},y:{math.sin(a) * 320 + 120:.0f},rotation:{180 + k * 40},opacity:0,duration:1.0,ease:"power2.out"}},{tch + 0.25:.2f});')
S(tch + 0.25, "shimmer", 0.5)

# ======================= END CARD =======================
clip("end", VOICE_END, DURATION - VOICE_END,
     '<div class="inkbg"></div>'
     + img("enp", "assets/product/duo_wood.jpg", (340, 220, 400, 720), "50% 50%", "200px 200px 36px 36px")
     + f'<div class="t c pearl it" style="top:1010px;font-size:150px;line-height:1;left:30px;right:30px">{CH("en0","Frescura Body")}</div>'
     f'<div class="t c lab" style="top:1190px;color:var(--haze)">{R("en1","Woman Glory &middot; Noche")}</div>'
     f'<div class="tag" id="enb" style="left:300px;top:1290px;background:var(--bag);font-size:32px">{BAG.format(s=48)}TEKAN BEG KUNING</div>')
js.append(f'tl.fromTo("#end",{{clipPath:"inset(0% 0% 100% 0%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:0.55,ease:"expo.inOut"}},{VOICE_END:.2f});')
js.append(f'tl.fromTo("#enp",{{clipPath:"inset(100% 0% 0% 0% round 200px 200px 36px 36px)"}},{{clipPath:"inset(0% 0% 0% 0% round 200px 200px 36px 36px)",duration:0.6,ease:"expo.out"}},{VOICE_END + 0.2:.2f});')
chars("#en0", VOICE_END + 0.35, 0.03); rv("#en1", VOICE_END + 0.8); pop("#enb", VOICE_END + 0.95, 0.35)
S(VOICE_END, "whip", 0.5); S(VOICE_END + 0.35, "chime", 0.5)

# ---- scene changes must fall between words
_tops = []
for h in html:
    m = re.search(r'id="([^"]+)"[^>]*data-start="([\d.]+)" data-duration="([\d.]+)"', h)
    if m and not m.group(1).startswith(("cap", "rb", "chrome", "c4")):
        _tops.append((m.group(1), round(float(m.group(2)) + float(m.group(3)), 3)))
_bad = [(i, e, w["w"]) for i, e in _tops for w in words if w["s"] + 0.04 < e < w["e"] - 0.04 and e < VOICE_END - 0.05]
if _bad: print("WARNING scene ends mid-word:", _bad)

# ---- captions: pearl label card; each word fills with ink left-to-right while spoken
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
        cls = "w l" if key in VIO else ("w k" if key in KEY else "w")
        sp.append(f'<span id="w{ci}_{wi}" class="{cls}">{w["t"].rstrip(".,!")}</span>')
        js.append(f'tl.fromTo("#w{ci}_{wi}",{{backgroundPosition:"100% 0%"}},{{backgroundPosition:"0% 0%",duration:{max(w["e"] - w["s"], 0.12):.2f},ease:"none"}},{w["s"]:.2f});')
    clip(f"cap{ci}", st, max(en - st, 0.2), '<span class="ln">' + " ".join(sp) + "</span>", cls="cap")
    js.append(f'tl.fromTo("#cap{ci} .ln",{{y:26,opacity:0,scale:0.96}},{{y:0,opacity:1,scale:1,duration:0.16,ease:"power3.out"}},{st:.2f});')

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
