"""Video 11 -- "3 sebab sabun ni bau perfume mahal" in a new "Metro Noir" night-city minimalist-luxury style.
Syncopate (wide architectural caps) + Figtree; the product (cut out of the client's photos, never altered) floats over Kuala Lumpur
(KLCC Petronas towers, skyline, night traffic) and New York footage with a glass-floor reflection, location pills, amber neon
light-streak transitions, outlined numerals, the client's pump/foam demo in glass windows, scent-wave lines, CTA bag + stock bar +
checkout, captions in chrome with the spoken keyword lighting up in amber neon.
Usage: python3 -I build.py PROJECT_DIR [--final]"""
import json, math, re, sys

proj = sys.argv[1]
FINAL = "--final" in sys.argv
words = [w for s in json.load(open(f"{proj}/assets/audio/words.json")) for w in s["words"]]
REAL_END = round(words[-1]["e"], 2)
VOICE_END = round(REAL_END + 0.5, 2)
DURATION = round(VOICE_END + 1.6, 2)

FIX = {"minat": "Midnight", "fantasi": "Fantasy", "back": "beg"}
KEY = {"serius", "perfume", "mahal", "habis", "3", "frescura", "body", "inspirasi", "cium", "2", "premium", "bombshell", "fresh", "feminine",
       "harihari", "midnight", "fantasy", "manis", "fruity", "malam", "tekan", "buih", "lembut", "sea", "salt", "mineral", "mewah", "ratusratus",
       "lepaskan", "rugi", "gila", "kuning", "sekarang", "check", "out", "terhad", "sangatsangat"}
clean = []
skip = 0
for i, w in enumerate(words):
    if skip: skip -= 1; continue
    txt = w["w"].strip(); core = txt.rstrip(".,?!"); tail = txt[len(core):]
    nx = [x["w"].strip().lower() for x in words[i + 1:i + 3]]
    if core == "Fresh" and nx and nx[0].startswith("kurang"):
        clean.append({"t": "Frescura", "s": w["s"], "e": words[i + 1]["e"]})
        clean.append({"t": "Body.", "s": words[i + 2]["s"], "e": words[i + 2]["e"]}); skip = 2; continue
    if core.lower().startswith("silsat"):
        m = (w["s"] + w["e"]) / 2
        clean.append({"t": "sea", "s": w["s"], "e": m}); clean.append({"t": "salt", "s": m, "e": w["e"]}); continue
    if core == "perasaan":                                   # "mandi pun rasa mewah"
        m = (w["s"] + w["e"]) / 2
        clean.append({"t": "pun", "s": w["s"], "e": m}); clean.append({"t": "rasa", "s": m, "e": w["e"]}); continue
    if core == "lepas" and nx and nx[0].startswith("kan"):
        clean.append({"t": "lepaskan?", "s": w["s"], "e": words[i + 1]["e"]}); skip = 1; continue
    txt = FIX.get(core, core) + tail
    if txt.startswith("-") and clean:
        clean[-1]["t"] += txt; clean[-1]["e"] = w["e"]; continue
    clean.append({"t": txt, "s": w["s"], "e": w["e"]})

def W(word, after=0.0):
    for w in clean:
        if w["s"] >= after - 0.01 and re.sub(r"[^a-z0-9]", "", w["t"].lower()) == word: return w["s"]
    raise KeyError(word)

FACE_END = 0.80
A, B, C, R1A, R1B, R2A, R2B, R2C, R3A, R3B, P1, P2, P3, C1, C2, C3 = (
    0.80, 2.97, 4.99, 8.01, 11.72, 14.16, 16.37, 19.33, 22.57, 25.84, 29.24, 31.26, 35.14, 36.28, 38.11, 41.43)
CUTS = [A, B, C, R1A, R1B, R2A, R2B, R2C, R3A, R3B, P1, P2, P3, C1, C2, C3, VOICE_END]

chunks, cur = [], []
for i, w in enumerate(clean):
    cur.append(w)
    nxt = clean[i + 1] if i + 1 < len(clean) else None
    if (len(cur) >= 3 or re.search(r"[.,?!]$", w["t"]) or nxt is None or nxt["s"] - w["e"] > 0.3
            or len(" ".join(x["t"] for x in cur)) > 17 or any(abs(nxt["s"] - c) < 0.12 for c in CUTS)):
        chunks.append(cur); cur = []

html, js, sfx = [], [], []
def S(t, s, g=0.6, auto=False): sfx.append({"t": round(t, 3), "sfx": s, "gain": g, "auto": auto})
def clip(id_, s, d, inner="", cls="", style=""):
    html.append(f'<div id="{id_}" class="clip {cls}" data-start="{s:.3f}" data-duration="{d:.3f}" style="{style}">{inner}</div>')
def city(id_, src, s, d, media=0.0, z0=1.12, z1=1.0):
    html.append(f'<video id="{id_}" class="clip bg" src="assets/broll/{src}.mp4" data-start="{s:.3f}" data-duration="{d:.3f}" data-media-start="{media}" muted playsinline></video>')
    js.append(f'tl.fromTo("#{id_}",{{scale:{z0}}},{{scale:{z1},duration:{d:.2f},ease:"power1.out"}},{s:.2f});')
def ivid(id_, src, s, d, box, media=0.0, extra=""):
    l, t_, w, h = box
    html.append(f'<video id="{id_}" class="clip window" src="assets/broll/{src}.mp4" data-start="{s:.3f}" data-duration="{d:.3f}" data-media-start="{media}" muted playsinline '
                f'style="z-index:3;left:{l}px;top:{t_}px;width:{w}px;height:{h}px;object-fit:cover;{extra}"></video>')
def R(id_, txt): return f'<span id="{id_}" class="rv"><span>{txt}</span></span>'
def rv(sel, t, d=0.45):
    js.append(f'tl.fromTo("{sel} > span",{{yPercent:118}},{{yPercent:0,duration:{d:.2f},ease:"expo.out"}},{t:.2f});')
    S(t, "top", 0.4, auto=True)
def fade(sel, t, d=0.4, y=30, x=0, s=1.0):
    js.append(f'tl.fromTo("{sel}",{{opacity:0,y:{y},x:{x},scale:{s}}},{{opacity:1,y:0,x:0,scale:1,duration:{d:.2f},ease:"expo.out"}},{t:.2f});')
    S(t, "top", 0.32, auto=True)
def pop(sel, t, d=0.35, rot=0, sfx_="pop"):
    js.append(f'tl.fromTo("{sel}",{{scale:0,rotation:{rot - 8}}},{{scale:1,rotation:{rot},duration:{d:.2f},ease:"back.out(2.4)"}},{t:.2f});')
    S(t, sfx_, 0.5, auto=True)
def CH(id_, txt): return f'<span id="{id_}">' + "".join(f'<span class="ch">{c}</span>' for c in txt) + "</span>"
def chars(sel, t, stagger=0.03):
    js.append(f'tl.fromTo("{sel} .ch",{{opacity:0,y:-40,filter:"blur(8px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.4,stagger:{stagger},ease:"expo.out"}},{t:.2f});')
    S(t, "top", 0.45, auto=True)
def loc(id_, txt, small=""):
    sm = f"<small>{small}</small>" if small else ""
    return f'<div class="loc" id="{id_}"><i></i>{txt}{sm}</div>'
def loc_js(id_, t):
    js.append(f'tl.fromTo("#{id_}",{{x:-60,opacity:0}},{{x:0,opacity:1,duration:0.4,ease:"expo.out"}},{t + 0.1:.2f});')
def bottle(id_, src, x, y, h):
    return (f'<div class="glow" id="{id_}g" style="left:{x - h * 0.45:.0f}px;top:{y + h * 0.55:.0f}px;width:{h * 0.9 + 200:.0f}px;height:{h * 0.5:.0f}px"></div>'
            f'<img class="bottle" id="{id_}" src="assets/product/{src}" alt="" style="left:{x}px;top:{y}px;height:{h}px">')
def bottle_js(id_, t, d_hold):
    js.append(f'tl.fromTo("#{id_}",{{y:260,opacity:0,rotation:-6}},{{y:0,opacity:1,rotation:0,duration:0.6,ease:"expo.out"}},{t:.2f});')
    js.append(f'tl.to("#{id_}",{{y:-18,duration:{max(d_hold, 0.5):.2f},ease:"sine.inOut"}},{t + 0.6:.2f});')
    js.append(f'tl.fromTo("#{id_}g",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.6,ease:"power2.out"}},{t:.2f});')
    S(t, "whip", 0.5)
def streak(id_, t):
    """transition: an amber light trail races across the frame (car-light streak) with a soft flash"""
    clip(id_, t - 0.25, 0.5, '<div class="sk" style="position:absolute;left:0;top:930px;width:1400px;height:60px;border-radius:30px;'
         'background:linear-gradient(90deg,rgba(255,181,71,0),#ffd28a 40%,#fff 55%,rgba(255,181,71,0));filter:blur(6px)"></div>'
         '<div class="sk2" style="position:absolute;left:0;top:990px;width:1100px;height:14px;border-radius:7px;'
         'background:linear-gradient(90deg,rgba(224,71,95,0),#ff8fa3 50%,rgba(224,71,95,0));filter:blur(3px)"></div>', style="z-index:9")
    js.append(f'tl.fromTo("#{id_} .sk",{{x:-1500,scaleY:0.6}},{{x:1300,scaleY:1.4,duration:0.45,ease:"power3.inOut"}},{t - 0.25:.3f});')
    js.append(f'tl.fromTo("#{id_} .sk2",{{x:1200}},{{x:-1200,duration:0.45,ease:"power3.inOut"}},{t - 0.22:.3f});')
    js.append(f'tl.fromTo("#flash",{{opacity:0.35}},{{opacity:0,duration:0.25}},{t:.3f});')
    S(t - 0.25, "whip", 0.55)
def num(id_, n, label):
    return (f'<div id="{id_}n" class="sy out" style="position:absolute;left:70px;top:150px;font-size:210px;line-height:1">{n}</div>'
            f'<div id="{id_}l" class="lab" style="position:absolute;left:{110 + 200 * len(n)}px;top:225px;color:var(--amber)">{label}</div>'
            f'<div id="{id_}r" class="hair" style="left:{110 + 200 * len(n)}px;top:275px;width:{900 - 200 * len(n)}px"></div>')
def num_js(id_, t):
    js.append(f'tl.fromTo("#{id_}n",{{opacity:0,x:-80}},{{opacity:1,x:0,duration:0.45,ease:"expo.out"}},{t:.2f});')
    js.append(f'tl.fromTo("#{id_}r",{{scaleX:0}},{{scaleX:1,duration:0.5,ease:"expo.out"}},{t + 0.1:.2f});')
    fade(f"#{id_}l", t + 0.12, 0.35, y=0, x=-30); S(t, "boom", 0.4)
BAG = ('<svg viewBox="0 0 100 100" style="width:{s}px;height:{s}px"><path d="M18 34 H82 L76 90 H24 Z" fill="var(--bag)" stroke="var(--night)" stroke-width="4" stroke-linejoin="round"/>'
       '<path d="M36 40 V28 a14 14 0 0 1 28 0 V40" fill="none" stroke="var(--night)" stroke-width="5" stroke-linecap="round"/></svg>')

# ======================= FACE (0.80 s): "Serius," =======================
html.append(f'<video id="v_face" class="clip bg" src="assets/broll/face.mp4" data-start="0" data-duration="{FACE_END:.3f}" data-media-start="0" muted playsinline style="z-index:6"></video>')
js.append(f'tl.fromTo("#v_face",{{scale:1.0}},{{scale:1.08,duration:{FACE_END},ease:"power1.out"}},0);')
S(0.0, "boom", 0.45)

# ======================= A: sabun ni bau perfume mahal (KLCC) =======================
streak("sk0", A)
city("v_a", "klcc_up", A, B - A)
clip("a", A, B - A, '<div class="shade"></div>' + loc("la", "KLCC", "KUALA LUMPUR")
     + f'<div class="t c" style="top:250px;font:800 56px Figtree;letter-spacing:6px">{R("aa","SABUN NI BAU")}</div>'
     f'<div class="t c sy" style="top:340px;font-size:118px;line-height:1">{CH("ab","PERFUME")}</div>'
     f'<div class="t c sy amber" style="top:480px;font-size:118px;line-height:1">{CH("ac","MAHAL")}</div>'
     + bottle("ag", "glory_single.png", 395, 700, 760))
loc_js("la", A); rv("#aa", W("sabun") - 0.05); chars("#ab", W("perfume") - 0.1, 0.03); chars("#ac", W("mahal") - 0.05, 0.04)
bottle_js("ag", A + 0.1, B - A - 0.7); S(W("mahal"), "boom", 0.4)

# ======================= B: kalau tak percaya, tengok sampai habis (New York bokeh) =======================
streak("sk1", B)
city("v_b", "ny_bokeh", B, C - B, media=0.0)
clip("b", B, C - B, '<div class="shade"></div>' + loc("lb", "NEW YORK")
     + f'<div class="t c" style="top:600px;font:800 64px Figtree;letter-spacing:4px">{R("ba","Kalau tak percaya,")}</div>'
     f'<div class="t c" style="top:720px;font:800 56px Figtree;color:var(--steel);letter-spacing:8px">{R("bb","TENGOK")}</div>'
     f'<div class="t c sy" style="top:800px;font-size:100px;line-height:1.05">{R("bc","SAMPAI")}<br>{R("bd","<span class=amber>HABIS</span>")}</div>'
     '<div id="bbar" style="position:absolute;left:170px;top:1080px;width:740px;height:6px;border-radius:3px;background:rgba(238,241,246,.2);overflow:hidden">'
     '<i id="bf" style="position:absolute;inset:0;background:linear-gradient(90deg,#ffb547,#fff);transform-origin:0 50%"></i></div>')
loc_js("lb", B); rv("#ba", W("kalau")); rv("#bb", W("tengok") - 0.05); rv("#bc", W("sampai") - 0.05); rv("#bd", W("habis") - 0.05)
js.append(f'tl.fromTo("#bf",{{scaleX:0}},{{scaleX:1,duration:{W("habis") + 0.3 - W("tengok"):.2f},ease:"power1.inOut"}},{W("tengok"):.2f});')
S(W("tengok"), "riser", 0.35)

# ======================= C: 3 sebab ... Frescura Body (KL day -> night) =======================
streak("sk2", C)
city("v_c", "kl_dusk", C, R1A - C, z0=1.05)
clip("c", C, R1A - C, '<div class="shade"></div>' + loc("lc", "KUALA LUMPUR")
     + '<div id="cbig" class="sy out" style="position:absolute;left:0;right:0;top:170px;text-align:center;font-size:420px;line-height:1">3</div>'
     f'<div class="t c syl" style="top:610px;font-size:46px">{R("ca","SEBAB")}</div>'
     f'<div class="t c" style="top:690px;font:800 56px Figtree">{R("cb","sabun ni bau")} {R("cc","<span class=amber>perfume mahal</span>")}</div>'
     + bottle("cd", "duo_white_cut.png", 300, 830, 640)
     + f'<div class="t c sy" style="top:1440px;font-size:64px">{CH("ce","FRESCURA BODY")}</div>')
loc_js("lc", C)
js.append(f'tl.fromTo("#cbig",{{scale:2.2,opacity:0}},{{scale:1,opacity:1,duration:0.45,ease:"expo.out"}},{C:.2f});')
S(C, "boom", 0.55)
rv("#ca", W("sebab") - 0.05); rv("#cb", W("sabun", C) - 0.05); rv("#cc", W("perfume", C) - 0.05)
bottle_js("cd", W("frescura") - 0.15, R1A - W("frescura") - 0.5); chars("#ce", W("frescura"), 0.025)

# ======================= R1A: sebab pertama -- inspirasi perfume (KL sunset) =======================
streak("sk3", R1A)
city("v_r1a", "kl_sunset", R1A, R1B - R1A)
clip("r1a", R1A, R1B - R1A, '<div class="shade"></div>' + loc("l1", "KLCC", "KUALA LUMPUR") + num("h1", "01", "Sebab pertama")
     + f'<div class="t" style="top:420px;font:800 54px Figtree">{R("r1a1","wangian dia memang")}</div>'
     f'<div class="t sy" style="top:500px;font-size:96px;line-height:1.05">{R("r1a2","INSPIRASI")}<br>{R("r1a3","<span class=amber>PERFUME</span>")}</div>'
     + bottle("r1g", "glory_single.png", 560, 760, 720))
loc_js("l1", R1A); num_js("h1", R1A)
rv("#r1a1", W("wangian") - 0.05); rv("#r1a2", W("inspirasi") - 0.05); rv("#r1a3", W("perfume", R1A) - 0.05)
bottle_js("r1g", W("wangian") - 0.1, R1B - W("wangian") - 0.6)

# ======================= R1B: sekali cium, terus bau perfume mahal (NY purple) =======================
city("v_r1b", "ny_purple", R1B, R2A - R1B)
waves = "".join(f'<svg class="wv" style="position:absolute;left:0;top:{860 + k * 70}px;width:1080px;height:80px" viewBox="0 0 1080 80">'
                f'<path d="M-20 40 C 120 {5 + k * 6}, 240 {75 - k * 6}, 380 40 S 640 {5 + k * 8}, 780 40 S 1000 {70 - k * 5}, 1100 40" fill="none" '
                f'stroke="{["#ffb547", "#ffd3da", "#e2d8ff"][k]}" stroke-width="{5 - k}" stroke-linecap="round" stroke-dasharray="1400" stroke-dashoffset="1400"/></svg>'
                for k in range(3))
clip("r1b", R1B, R2A - R1B, '<div class="shade"></div>' + loc("l1b", "NEW YORK")
     + f'<div class="t c" style="top:430px;font:800 66px Figtree;letter-spacing:3px">{R("r1b1","Sekali cium,")}</div>'
     f'<div class="t c syl" style="top:540px;font-size:44px">{R("r1b2","terus bau")}</div>'
     f'<div class="t c sy" style="top:620px;font-size:104px;line-height:1.05">{R("r1b3","PERFUME")}<br>{R("r1b4","<span class=amber>MAHAL</span>")}</div>'
     + waves)
loc_js("l1b", R1B); S(R1B, "swoosh", 0.5)
rv("#r1b1", W("sekali") - 0.05); rv("#r1b2", W("terus", R1B) - 0.05); rv("#r1b3", W("perfume", R1B) - 0.05); rv("#r1b4", W("mahal", R1B) - 0.05)
js.append(f'tl.to("#r1b .wv path",{{strokeDashoffset:0,duration:1.0,stagger:0.12,ease:"power2.out"}},{W("cium"):.2f});')
js.append(f'tl.fromTo("#r1b .wv",{{x:-40}},{{x:40,duration:{R2A - W("cium"):.2f},ease:"sine.inOut"}},{W("cium"):.2f});')
S(W("cium"), "shimmer", 0.5)

# ======================= R2A: sebab kedua -- 2 bau premium (KL night traffic) =======================
streak("sk4", R2A)
city("v_r2a", "kl_traffic", R2A, R2B - R2A, media=0.0)
clip("r2a", R2A, R2B - R2A, '<div class="shade"></div>' + loc("l2", "KUALA LUMPUR") + num("h2", "02", "Sebab kedua")
     + f'<div class="t c sy" style="top:420px;font-size:92px;line-height:1.08">{R("r2t1","2 BAU")}<br>{R("r2t2","<span class=amber>PREMIUM</span>")}</div>'
     + bottle("r2g", "glory_single.png", 190, 760, 680) + bottle("r2n", "noche_single.png", 570, 760, 680))
loc_js("l2", R2A); num_js("h2", R2A)
rv("#r2t1", W("2") - 0.1); rv("#r2t2", W("premium") - 0.05)
bottle_js("r2g", W("ada", R2A) - 0.1, R2B - W("ada", R2A) - 0.6); bottle_js("r2n", W("ada", R2A) + 0.1, R2B - W("ada", R2A) - 0.8)

# ======================= R2B: Bombshell -- fresh & feminine, sesuai hari-hari (KL by day) =======================
city("v_r2b", "kl_day", R2B, R2C - R2B)
clip("r2b", R2B, R2C - R2B, '<div class="shade"></div>' + loc("l2b", "KUALA LUMPUR", "SIANG")
     + bottle("r2bg", "glory_single.png", 90, 520, 900)
     + f'<div style="position:absolute;left:560px;top:560px;width:480px"><div class="sy" style="font-size:62px;line-height:1.1">{R("r2b1","WOMAN")}<br>{R("r2b2","GLORY")}</div>'
     f'<div class="lab" style="margin-top:14px;color:#ffd3da">{R("r2b3","by Bombshell")}</div></div>'
     '<div class="chip r" id="r2bf" style="left:560px;top:860px">FRESH</div>'
     '<div class="chip r" id="r2bm" style="left:560px;top:960px">FEMININE</div>'
     '<div class="chip a" id="r2bh" style="left:560px;top:1100px">&#9728; HARI-HARI</div>')
loc_js("l2b", R2B); bottle_js("r2bg", R2B, R2C - R2B - 0.7)
rv("#r2b1", R2B + 0.05); rv("#r2b2", R2B + 0.15); rv("#r2b3", R2B + 0.3)
pop("#r2bf", W("fresh", R2B) - 0.05, 0.3, rot=-2); pop("#r2bm", W("feminine") - 0.05, 0.3, rot=2); pop("#r2bh", W("harihari") - 0.1, 0.35, rot=-3)

# ======================= R2C: Midnight Fantasy -- manis & fruity, sesuai untuk malam (KLCC at night) =======================
streak("sk5", R2C)
city("v_r2c", "klcc_night", R2C, R3A - R2C, media=0.0)
clip("r2c", R2C, R3A - R2C, '<div class="shade"></div>' + loc("l2c", "KLCC", "MALAM")
     + bottle("r2cn", "noche_single.png", 620, 520, 900)
     + f'<div style="position:absolute;left:60px;top:560px;width:540px"><div class="sy" style="font-size:72px;line-height:1.1">{R("r2c1","NOCHE")}</div>'
     f'<div class="lab" style="margin-top:14px;color:#e2d8ff;line-height:1.5">{R("r2c2","by Midnight")}<br>{R("r2c3","Fantasy")}</div></div>'
     '<div class="chip v" id="r2cm" style="left:60px;top:860px">MANIS</div>'
     '<div class="chip v" id="r2cf" style="left:60px;top:960px">FRUITY</div>'
     '<div class="chip a" id="r2cu" style="left:60px;top:1100px">&#9790; UNTUK MALAM</div>')
loc_js("l2c", R2C); bottle_js("r2cn", R2C, R3A - R2C - 0.7)
rv("#r2c1", R2C + 0.05); rv("#r2c2", W("fantasy") - 0.1); rv("#r2c3", W("fantasy"))
pop("#r2cm", W("manis") - 0.05, 0.3, rot=-2); pop("#r2cf", W("fruity") - 0.05, 0.3, rot=2); pop("#r2cu", W("malam") - 0.15, 0.35, rot=-3)

# ======================= R3A: sebab ketiga -- tekan je terus keluar buih lembut (pump demo in a glass window) =======================
streak("sk6", R3A)
city("v_r3a", "city_air", R3A, R3B - R3A)
ivid("v_pmp", "pump", R3A, R3B - R3A, (250, 480, 580, 1030))
clip("r3a", R3A, R3B - R3A, '<div class="veil" style="position:absolute;inset:0;background:rgba(10,14,26,.45)"></div>', style="z-index:2")
clip("r3at", R3A, R3B - R3A, loc("l3", "KUALA LUMPUR") + num("h3", "03", "Sebab ketiga")
     + f'<div class="t" style="top:370px;left:330px;font:800 50px Figtree">{R("r3a1","tekan je,")} {R("r3a2","<span class=amber>buih lembut</span>")}</div>'
     '<div id="r3ar" style="position:absolute;left:540px;top:820px;width:150px;height:150px;border-radius:50%;border:6px solid var(--bag)"></div>')
loc_js("l3", R3A); num_js("h3", R3A)
js.append(f'tl.fromTo("#v_pmp",{{clipPath:"inset(50% 0% 50% 0% round 30px)"}},{{clipPath:"inset(0% 0% 0% 0% round 30px)",duration:0.5,ease:"expo.out"}},{R3A + 0.1:.2f});')
rv("#r3a1", W("tekan", R3A) - 0.05); rv("#r3a2", W("buih") - 0.05)
js.append(f'tl.fromTo("#r3ar",{{scale:0.2,opacity:1}},{{scale:1.9,opacity:0,duration:0.5,ease:"power2.out"}},{W("tekan", R3A) + 0.1:.2f});')
S(W("tekan", R3A) + 0.1, "click", 0.7); S(W("buih") - 0.1, "foam", 0.6)

# ======================= R3B: sea salt, kaya mineral, mandi pun rasa mewah (lather window over NY bokeh) =======================
city("v_r3b", "ny_bokeh", R3B, P1 - R3B, media=2.0)
ivid("v_lth", "lather", R3B, P1 - R3B, (90, 330, 520, 925))
clip("r3b", R3B, P1 - R3B, '<div class="veil" style="position:absolute;inset:0;background:rgba(10,14,26,.4)"></div>', style="z-index:2")
clip("r3bt", R3B, P1 - R3B, loc("l3b", "NEW YORK")
     + '<div class="chip a" id="r3bs" style="left:620px;top:470px">SEA SALT</div>'
     '<div class="chip" id="r3bm" style="left:620px;top:580px">KAYA MINERAL</div>'
     f'<div style="position:absolute;left:640px;top:760px;width:400px;font:800 46px Figtree;line-height:1.2">{R("r3b1","mandi pun")}<br>{R("r3b2","rasa")}</div>'
     f'<div class="sy amber" style="position:absolute;left:630px;top:880px;font-size:76px">{CH("r3b3","MEWAH")}</div>')
loc_js("l3b", R3B)
js.append(f'tl.fromTo("#v_lth",{{x:-600,rotation:-4}},{{x:0,rotation:0,duration:0.55,ease:"expo.out"}},{R3B:.2f});')
S(R3B, "whip", 0.5)
pop("#r3bs", W("sea", R3B) - 0.05, 0.3, rot=-2); pop("#r3bm", W("mineral") - 0.05, 0.3, rot=2)
rv("#r3b1", W("mandi") - 0.05); rv("#r3b2", W("pun", R3B)); chars("#r3b3", W("mewah") - 0.1, 0.04)

# ======================= P1: kau sanggup beli perfume ratus-ratus (Times Square) =======================
streak("sk7", P1)
city("v_p1", "ny_times", P1, P2 - P1)
clip("p1", P1, P2 - P1, '<div class="shade"></div>' + loc("lp1", "TIMES SQUARE", "NEW YORK")
     + '<div id="prm" class="sy out" style="position:absolute;left:0;right:0;top:300px;text-align:center;font-size:300px;line-height:1;opacity:.35">RM</div>'
     f'<div class="t c" style="top:560px;font:800 60px Figtree">{R("p1a","Kau sanggup beli perfume")}</div>'
     f'<div class="t c sy amber" style="top:680px;font-size:78px;left:20px;right:20px">{CH("p1b","RATUS-RATUS")}</div>')
loc_js("lp1", P1)
js.append(f'tl.fromTo("#prm",{{scale:1.6,opacity:0}},{{scale:1,opacity:0.35,duration:0.6,ease:"expo.out"}},{P1:.2f});')
rv("#p1a", W("sanggup") - 0.1); chars("#p1b", W("ratusratus") - 0.05, 0.03); S(W("ratusratus"), "riser", 0.35)

# ======================= P2: sabun yang bau perfume mahal ni, kau nak lepaskan? (duo over NY bokeh) =======================
city("v_p2", "ny_bokeh", P2, P3 - P2, media=5.4)
clip("p2", P2, P3 - P2, '<div class="shade"></div>' + loc("lp2", "NEW YORK")
     + f'<div class="t c" style="top:230px;font:800 60px Figtree">{R("p2a","Tapi sabun yang bau")}</div>'
     f'<div class="t c sy" style="top:320px;font-size:84px">{R("p2b","PERFUME")} {R("p2c","<span class=amber>MAHAL</span>")}</div>'
     + bottle("p2d", "duo_white_cut.png", 290, 560, 700)
)
loc_js("lp2", P2); S(P2, "swoosh", 0.5)
rv("#p2a", W("sabun", P2) - 0.05); rv("#p2b", W("perfume", P2) - 0.05); rv("#p2c", W("mahal", P2) - 0.05)
bottle_js("p2d", W("sabun", P2), P3 - W("sabun", P2) - 0.7)
js.append(f'tl.to("#p2d",{{scale:1.06,duration:0.25,yoyo:true,repeat:1}},{W("lepaskan"):.2f});'); S(W("lepaskan"), "pop", 0.5)

# ======================= P3: rugi gila weh =======================
clip("p3", P3, C1 - P3, '<div class="nightbg"></div>'
     f'<div class="t c sy" id="p3r" style="top:640px;font-size:200px;line-height:1;color:var(--rose);text-shadow:0 0 40px rgba(224,71,95,.6)">RUGI</div>'
     f'<div class="t c sy amber" id="p3g" style="top:860px;font-size:110px;line-height:1">GILA WEH</div>')
js.append(f'tl.fromTo("#p3r",{{scale:2.4,opacity:0}},{{scale:1,opacity:1,duration:0.25,ease:"power4.out"}},{P3 + 0.02:.2f});')
js.append(f'tl.to("#p3r",{{x:-12,duration:0.04,yoyo:true,repeat:5}},{P3 + 0.3:.2f});')
js.append(f'tl.fromTo("#p3g",{{y:80,opacity:0}},{{y:0,opacity:1,duration:0.3,ease:"back.out(2)"}},{W("gila"):.2f});')
S(P3, "boom", 0.6); S(P3 + 0.3, "buzz", 0.45)

# ======================= C1: tekan beg kuning sekarang, check out sekarang (KL traffic) =======================
city("v_c1", "kl_traffic", C1, C2 - C1, media=2.2)
clip("c1", C1, C2 - C1, '<div class="shade"></div>' + loc("lc1", "KUALA LUMPUR")
     + f'<div id="c1b" style="position:absolute;left:120px;top:780px;width:840px;height:190px;border-radius:95px;background:var(--bag);display:flex;align-items:center;justify-content:center;'
     f'gap:22px;font:900 58px Figtree;color:var(--night);box-shadow:0 0 60px rgba(246,196,69,.45),0 26px 60px rgba(0,0,0,.5)">{BAG.format(s=96)}TEKAN BEG KUNING</div>'
     '<div id="c1r" style="position:absolute;left:470px;top:800px;width:150px;height:150px;border-radius:50%;border:7px solid #fff"></div>'
     '<div class="chip a" id="c1s" style="left:330px;top:1040px;font-size:40px">CHECK OUT SEKARANG</div>')
loc_js("lc1", C1)
js.append(f'tl.fromTo("#c1b",{{y:300,scale:0.8,opacity:0}},{{y:0,scale:1,opacity:1,duration:0.4,ease:"back.out(1.8)"}},{C1:.2f});')
S(C1, "whip", 0.5)
tk = W("kuning", C1)
js.append(f'tl.to("#c1b",{{scale:0.93,duration:0.09,yoyo:true,repeat:1}},{tk:.2f});')
js.append(f'tl.fromTo("#c1r",{{scale:0.2,opacity:1}},{{scale:1.9,opacity:0,duration:0.5,ease:"power2.out"}},{tk + 0.05:.2f});')
S(tk, "click", 0.75); S(tk + 0.05, "ding", 0.55)
pop("#c1s", W("check", C1) - 0.05, 0.3, rot=-2)

# ======================= C2: stok memang dah tak banyak, sangat-sangat terhad (KLCC from below) =======================
city("v_c2", "klcc_up", C2, C3 - C2, media=2.2)
clip("c2", C2, C3 - C2, '<div class="shade"></div>' + loc("lc2", "KLCC", "KUALA LUMPUR")
     + f'<div class="t c syl" style="top:520px;font-size:54px">{R("c2a","STOK KAMI")}</div>'
     f'<div class="t c" style="top:610px;font:800 70px Figtree">{R("c2b","memang dah tak banyak")}</div>'
     '<div id="c2bar" style="position:absolute;left:140px;top:820px;width:800px;height:24px;border-radius:12px;background:rgba(238,241,246,.2);overflow:hidden">'
     '<i id="c2f" style="position:absolute;inset:0;border-radius:12px;background:linear-gradient(90deg,#e0475f,#ffb547);transform-origin:0 50%"></i></div>'
     f'<div class="t c sy" id="c2t" style="top:930px;font-size:120px;color:var(--rose);text-shadow:0 0 40px rgba(224,71,95,.6)">TERHAD</div>')
loc_js("lc2", C2); S(C2, "swoosh", 0.5)
rv("#c2a", W("stok") - 0.05); rv("#c2b", W("memang", C2) - 0.05)
js.append(f'tl.fromTo("#c2f",{{scaleX:0.6}},{{scaleX:0.08,duration:2.2,ease:"power2.inOut"}},{W("stok"):.2f});')
S(W("stok"), "riser", 0.35)
js.append(f'tl.fromTo("#c2t",{{scale:2,opacity:0}},{{scale:1,opacity:1,duration:0.25,ease:"power4.out"}},{W("terhad") - 0.1:.2f});')
S(W("terhad"), "stamp", 0.7)

# ======================= C3: tekan beg kuning dan check out sekarang =======================
streak("sk8", C3)
city("v_c3", "kl_traffic", C3, VOICE_END + 0.6 - C3, media=4.1, z0=1.2)
conf = "".join(f'<i class="cf" style="position:absolute;left:530px;top:1000px;width:{r}px;height:{r}px;border-radius:{"50%" if k % 2 else "3px"};background:{c}"></i>'
               for k, (r, c) in enumerate([(18, "#ffb547"), (14, "#f6c445"), (20, "#e0475f"), (12, "#9b7bff"), (16, "#fff"),
                                           (14, "#ffb547"), (18, "#e0475f"), (12, "#9b7bff"), (16, "#f6c445"), (14, "#fff")]))
clip("c3", C3, VOICE_END + 0.6 - C3, '<div class="shade"></div>'
     f'<div class="t c" style="top:420px;font:800 64px Figtree">{R("c3a","Tekan")} {R("c3b","<span style=color:var(--bag)>beg kuning</span>")}</div>'
     '<div id="c3btn" style="position:absolute;left:190px;top:930px;width:700px;height:160px;border-radius:80px;background:var(--chrome);color:var(--night);'
     'display:flex;align-items:center;justify-content:center;gap:22px;font:900 52px Figtree;letter-spacing:6px;box-shadow:0 0 50px rgba(238,241,246,.3)">'
     'CHECK OUT<svg viewBox="0 0 100 100" style="width:72px;height:72px"><path id="c3tk" d="M20 52 L42 72 L80 30" stroke="#e0475f" stroke-width="12" fill="none" '
     'stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="100" stroke-dashoffset="100"/></svg></div>' + conf)
rv("#c3a", C3 + 0.05); rv("#c3b", W("beg", C3) - 0.05)
js.append(f'tl.fromTo("#c3btn",{{y:200,opacity:0}},{{y:0,opacity:1,duration:0.35,ease:"back.out(1.8)"}},{C3 + 0.1:.2f});')
tch = W("check", C3)
js.append(f'tl.to("#c3btn",{{scale:0.93,duration:0.1,yoyo:true,repeat:1}},{tch:.2f});')
js.append(f'tl.to("#c3btn",{{backgroundColor:"#ffb547",duration:0.3}},{tch + 0.15:.2f});')
js.append(f'tl.to("#c3tk",{{strokeDashoffset:0,duration:0.3,ease:"power2.out"}},{tch + 0.2:.2f});')
S(tch, "click", 0.7); S(tch + 0.2, "ding", 0.65)
for k in range(10):
    a = -math.pi / 2 + (k - 4.5) * 0.33
    js.append(f'tl.fromTo("#c3 .cf:nth-of-type({k + 1})",{{x:0,y:0,opacity:1,rotation:0}},{{x:{math.cos(a) * 400:.0f},y:{math.sin(a) * 320 + 120:.0f},rotation:{180 + k * 40},opacity:0,duration:1.0,ease:"power2.out"}},{tch + 0.25:.2f});')
S(tch + 0.25, "shimmer", 0.5)

# ======================= END CARD (KLCC at night) =======================
html.append(f'<video id="v_end" class="clip bg" src="assets/broll/klcc_night.mp4" data-start="{VOICE_END:.3f}" data-duration="{DURATION - VOICE_END:.3f}" data-media-start="3.3" muted playsinline style="z-index:6"></video>')
clip("end", VOICE_END, DURATION - VOICE_END, '<div class="shade"></div>'
     + bottle("enb", "duo_white_cut.png", 330, 380, 600)
     + f'<div class="t c sy" style="top:1180px;font-size:76px">{CH("en0","FRESCURA BODY")}</div>'
     f'<div class="t c lab" style="top:1290px;color:var(--chrome)">{R("en1","Woman Glory &middot; Noche")}</div>'
     f'<div class="chip" id="eny" style="left:300px;top:1380px;background:var(--bag);color:var(--night);border-color:var(--bag)">{BAG.format(s=44)}TEKAN BEG KUNING</div>',
     style="z-index:7")
js.append(f'tl.fromTo("#v_end, #end",{{opacity:0}},{{opacity:1,duration:0.35}},{VOICE_END:.2f});')
bottle_js("enb", VOICE_END + 0.1, 1.0); chars("#en0", VOICE_END + 0.35, 0.025); rv("#en1", VOICE_END + 0.8); pop("#eny", VOICE_END + 0.95, 0.35)
S(VOICE_END + 0.35, "chime", 0.5)

# ---- scene changes must fall between words
_tops = []
for h in html:
    m = re.search(r'id="([^"]+)"[^>]*data-start="([\d.]+)" data-duration="([\d.]+)"', h)
    if m and not m.group(1).startswith(("cap", "sk", "v_face", "c3", "v_c3")):
        _tops.append((m.group(1), round(float(m.group(2)) + float(m.group(3)), 3)))
_bad = [(i, e, w["w"]) for i, e in _tops for w in words if w["s"] + 0.04 < e < w["e"] - 0.04 and e < VOICE_END - 0.05]
if _bad: print("WARNING scene ends mid-word:", _bad)

# ---- captions: chrome Figtree; keyword lights up amber neon as it is spoken
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
        sp.append(f'<span id="w{ci}_{wi}" class="w">{w["t"].rstrip(".,!")}</span>')
        if key in KEY:
            js.append(f'tl.to("#w{ci}_{wi}",{{color:"#ffb547",textShadow:"0 0 26px rgba(255,181,71,.9), 0 4px 24px rgba(0,0,0,.85)",duration:0.12}},{w["s"]:.2f});')
    clip(f"cap{ci}", st, max(en - st, 0.2), '<span class="ln">' + " ".join(sp) + "</span>", cls="cap")
    js.append(f'tl.fromTo("#cap{ci} .ln",{{y:24,opacity:0}},{{y:0,opacity:1,duration:0.14,ease:"power3.out"}},{st:.2f});')

# ---- SFX
sfx.sort(key=lambda c: c["t"])
kept = [c for c in sfx if not c["auto"]]
for c in (c for c in sfx if c["auto"]):
    if any(abs(c["t"] - k["t"]) < 0.07 for k in kept): continue
    kept.append(c)
kept.sort(key=lambda c: c["t"])
for c in kept: c.pop("auto", None)
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
