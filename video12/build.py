"""Video 12 -- "3 sebab kau kena tukar ke Frescura Body" (Metro Noir sequel: KLCC, Menara KL, TRX line-art and inside the mall).
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

FIX = {"minat": "Midnight", "fantasi": "Fantasy", "lengah": "lenguh", "femenil": "feminine", "Melepas": "Lepas", "bombshell": "Bombshell"}
KEY = {"serius", "gosok", "lenguh", "tangan", "tekan", "sekali", "buih", "3", "frescura", "body", "span", "lama", "lembut", "penuh", "sea", "salt",
       "mineral", "bersih", "segar", "kering", "perfume", "bombshell", "fresh", "feminine", "midnight", "fantasy", "manis", "fruity", "wangi",
       "biasa", "sekarang", "stok", "habis", "menyesal", "rugi", "besar", "kuning", "check", "out"}
clean = []
skip = 0
for i, w in enumerate(words):
    if skip: skip -= 1; continue
    txt = w["w"].strip(); core = txt.rstrip(".,?!"); tail_ = txt[len(core):]
    nx = [x["w"].strip().lower() for x in words[i + 1:i + 3]]
    if core == "fresh" and nx and nx[0].startswith("kurang"):
        clean.append({"t": "Frescura", "s": w["s"], "e": words[i + 1]["e"]})
        clean.append({"t": "Body.", "s": words[i + 2]["s"], "e": words[i + 2]["e"]}); skip = 2; continue
    if core == "sisa" and nx and nx[0].startswith("yang"):        # "ada sea salt yang kaya mineral"
        m = (w["s"] + w["e"]) / 2
        clean.append({"t": "sea", "s": w["s"], "e": m}); clean.append({"t": "salt", "s": m, "e": w["e"]}); continue
    if core == "kewangi":                                         # "dah buat kau wangi"
        m = (w["s"] + w["e"]) / 2
        clean.append({"t": "kau", "s": w["s"], "e": m}); clean.append({"t": "wangi" + tail_, "s": m, "e": w["e"]}); continue
    if core == "tangan" and w["s"] < 4: tail_ = "?"
    txt = FIX.get(core, core) + tail_
    if txt.startswith("-") and clean:
        clean[-1]["t"] += txt; clean[-1]["e"] = w["e"]; continue
    clean.append({"t": txt, "s": w["s"], "e": w["e"]})

def W(word, after=0.0):
    for w in clean:
        if w["s"] >= after - 0.01 and re.sub(r"[^a-z0-9]", "", w["t"].lower()) == word: return w["s"]
    raise KeyError(word)

FACE_END = 0.75
H1, H2, S3A, S3B, R1A, R1B, R2A, R2B, R3A, R3B, R3C, R3D, P1, P2, P3, P4, P5, C1, C2 = (
    0.75, 3.36, 6.07, 7.80, 8.59, 11.40, 15.61, 19.39, 21.70, 24.62, 26.43, 28.88, 32.32, 35.07, 37.94, 40.67, 42.62, 45.84, 46.74)
CUTS = [H1, H2, S3A, S3B, R1A, R1B, R2A, R2B, R3A, R3B, R3C, R3D, P1, P2, P3, P4, P5, C1, C2, VOICE_END]

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

# ======================= FACE (0.75 s): "Serius lah," =======================
html.append(f'<video id="v_face" class="clip bg" src="assets/broll/face.mp4" data-start="0" data-duration="{FACE_END:.3f}" data-media-start="0" muted playsinline style="z-index:6"></video>')
js.append(f'tl.fromTo("#v_face",{{scale:1.0}},{{scale:1.08,duration:{FACE_END},ease:"power1.out"}},0);')
S(0.0, "boom", 0.45)

def veil(id_, s, d, a=0.45):
    clip(id_, s, d, f'<div style="position:absolute;inset:0;background:rgba(10,14,26,{a})"></div>', style="z-index:2")

# ======================= H1: kau masih gosok sabun ni sampai lenguh tangan? (mall atrium + lather window) =======================
streak("sk0", H1)
city("v_h1", "mall_atrium", H1, H2 - H1, media=0.0)
ivid("v_lt1", "lather1", H1, H2 - H1, (260, 470, 560, 995))
veil("h1v", H1, H2 - H1)
clip("h1", H1, H2 - H1, loc("lh1", "DALAM MALL", "KUALA LUMPUR")
     + f'<div class="t c" style="top:200px;font:800 58px Figtree">{R("h1a","Kau masih")} {R("h1b","<span class=amber>gosok</span>")}</div>'
     f'<div class="t c sy" style="top:290px;font-size:76px">{CH("h1c","SAMPAI LENGUH")}</div>'
     '<svg id="h1x" style="position:absolute;left:260px;top:470px;width:560px;height:995px;overflow:visible" viewBox="0 0 560 995">'
     '<path d="M70 230 L490 770 M490 230 L70 770" stroke="#e0475f" stroke-width="20" stroke-linecap="round" fill="none" stroke-dasharray="700" stroke-dashoffset="700"/></svg>'
     '<div class="chip r" id="h1t" style="left:340px;top:1380px;font-size:36px">LENGUH TANGAN?</div>')
loc_js("lh1", H1)
js.append(f'tl.fromTo("#v_lt1",{{clipPath:"inset(50% 0% 50% 0% round 30px)"}},{{clipPath:"inset(0% 0% 0% 0% round 30px)",duration:0.5,ease:"expo.out"}},{H1:.2f});')
rv("#h1a", W("kau") - 0.05); rv("#h1b", W("gosok") - 0.05); chars("#h1c", W("sampai") - 0.05, 0.025)
js.append(f'tl.to("#h1x path",{{strokeDashoffset:0,duration:0.3,ease:"power2.out"}},{W("tangan") - 0.1:.2f});')
js.append(f'tl.to("#v_lt1",{{filter:"grayscale(1) brightness(.8)",duration:0.3}},{W("tangan") - 0.1:.2f});')
pop("#h1t", W("tangan"), 0.3, rot=-3); S(W("tangan") - 0.1, "buzz", 0.45)

# ======================= H2: tengok ni, tekan sekali je, buih terus keluar (pump in a window over mall escalators) =======================
city("v_h2", "mall_esc", H2, S3A - H2, media=0.0)
ivid("v_pmp", "pump", H2, S3A - H2, (250, 430, 580, 1030))
veil("h2v", H2, S3A - H2)
clip("h2", H2, S3A - H2, loc("lh2", "DALAM MALL")
     + f'<div class="t c" style="top:190px;font:800 58px Figtree">{R("h2a","Tengok ni,")}</div>'
     f'<div class="t c sy amber" style="top:280px;font-size:80px">{CH("h2b","1× TEKAN")}</div>'
     '<div id="h2ring" style="position:absolute;left:540px;top:770px;width:150px;height:150px;border-radius:50%;border:6px solid var(--bag)"></div>'
     '<div class="chip a" id="h2c" style="left:290px;top:1380px;font-size:36px">BUIH TERUS KELUAR</div>')
loc_js("lh2", H2); S(H2, "whip", 0.5)
js.append(f'tl.fromTo("#v_pmp",{{x:700,rotation:5}},{{x:0,rotation:0,duration:0.5,ease:"expo.out"}},{H2:.2f});')
rv("#h2a", W("tengok") - 0.05); chars("#h2b", W("tekan") - 0.1, 0.03)
js.append(f'tl.fromTo("#h2ring",{{scale:0.2,opacity:1}},{{scale:1.9,opacity:0,duration:0.5,ease:"power2.out"}},{W("tekan") + 0.1:.2f});')
S(W("tekan") + 0.1, "click", 0.7); pop("#h2c", W("buih") - 0.05, 0.3, rot=2); S(W("buih"), "foam", 0.6)

# ======================= S3A: 3 sebab kau kena tukar ke -- line-art skyline KLCC / Menara KL / TRX =======================
streak("sk1", S3A)
def tower(cx):
    pts = [(-40, 680), (-40, 320), (-32, 300), (-32, 250), (-24, 232), (-24, 190), (-14, 172), (-14, 130), (-6, 118), (-2, 40), (0, 8)]
    pts = pts + [(-x, y) for x, y in reversed(pts[:-1])]
    return "M" + " L".join(f"{cx + x} {y}" for x, y in pts)
sky = (f'<path d="{tower(220)}"/><path d="{tower(360)}"/><path d="M260 430 H320 M268 430 L290 520 L312 430"/>'
       '<path d="M560 680 Q578 560 582 340 M620 680 Q602 560 598 340"/><ellipse cx="590" cy="312" rx="48" ry="28"/><path d="M584 284 V230 H596 V284 M590 230 V110"/>'
       '<path d="M800 680 V150 L818 118 L840 52 L862 118 L880 150 V680"/><path d="M820 170 V680 M840 120 V680 M860 170 V680"/>'
       '<path d="M60 680 V560 H130 V680 M440 680 V500 H520 V680 M660 680 V590 H740 V680 M930 680 V540 H1010 V680"/><path d="M30 680 H1050"/>')
clip("s3a", S3A, S3B - S3A, '<div class="nightbg"></div>'
     + '<div id="s3n" class="sy out" style="position:absolute;left:0;right:0;top:140px;text-align:center;font-size:300px;line-height:1">3</div>'
     f'<div class="t c syl" style="top:470px;font-size:44px">{R("s3t1","SEBAB")}</div>'
     f'<div class="t c" style="top:540px;font:800 54px Figtree">{R("s3t2","kau kena")} {R("s3t3","<span class=amber>tukar ke</span>")}</div>'
     f'<svg id="sky" style="position:absolute;left:0;top:700px;width:1080px;height:700px" viewBox="0 0 1080 700">'
     f'<g fill="none" stroke="#eef1f6" stroke-width="3.5" stroke-linejoin="round" stroke-linecap="round" stroke-dasharray="1800" stroke-dashoffset="1800">{sky}</g></svg>'
     '<div class="lab" id="sk_a" style="position:absolute;left:160px;top:1405px;color:var(--amber)">KLCC</div>'
     '<div class="lab" id="sk_b" style="position:absolute;left:470px;top:1405px;color:var(--amber)">MENARA KL</div>'
     '<div class="lab" id="sk_c" style="position:absolute;left:800px;top:1405px;color:var(--amber)">TRX</div>')
js.append(f'tl.fromTo("#s3n",{{scale:2.2,opacity:0}},{{scale:1,opacity:1,duration:0.45,ease:"expo.out"}},{S3A:.2f});')
S(S3A, "boom", 0.55)
rv("#s3t1", W("sebab") - 0.05); rv("#s3t2", W("kau", S3A) - 0.05); rv("#s3t3", W("tukar") - 0.05)
js.append(f'tl.to("#sky path, #sky ellipse",{{strokeDashoffset:0,duration:1.2,stagger:0.05,ease:"power2.out"}},{S3A + 0.1:.2f});')
S(S3A + 0.1, "swoosh", 0.45)
for k, sel in enumerate(["#sk_a", "#sk_b", "#sk_c"]):
    fade(sel, S3A + 0.6 + k * 0.25, 0.3, y=15)

# ======================= S3B: Frescura Body (KLCC + Menara KL by day) =======================
city("v_s3b", "kl_klcc_kl", S3B, R1A - S3B, z0=1.15)
clip("s3b", S3B, R1A - S3B, '<div class="shade"></div>' + loc("ls3", "KLCC &middot; MENARA KL")
     + bottle("s3d", "duo_white_cut.png", 300, 760, 640) + f'<div class="t c sy" style="top:1440px;font-size:64px">{CH("s3e","FRESCURA BODY")}</div>')
loc_js("ls3", S3B); bottle_js("s3d", S3B, R1A - S3B - 0.6); chars("#s3e", S3B + 0.05, 0.02); S(S3B, "chime", 0.5)

# ======================= R1A: sebab pertama -- tak payah span, tak payah gosok lama (white mall, glass lift) =======================
streak("sk2", R1A)
city("v_r1a", "mall_glass", R1A, R1B - R1A)
clip("r1a", R1A, R1B - R1A, '<div class="shade" style="background:linear-gradient(180deg,rgba(10,14,26,.85) 0%,rgba(10,14,26,.45) 45%,rgba(10,14,26,.7) 100%)"></div>'
     + loc("l1", "DALAM MALL") + num("h1", "01", "Sebab pertama")
     + f'<div class="t sy" style="top:430px;font-size:68px;line-height:1.25">{R("r1a1","TAK PAYAH")}<br>{R("r1a2","<span class=amber>SPAN</span>")}</div>'
     f'<div class="t sy" style="top:720px;font-size:68px;line-height:1.25">{R("r1a3","TAK PAYAH")}<br>{R("r1a4","<span class=amber>GOSOK LAMA</span>")}</div>'
     '<div class="chip r" id="r1x1" style="left:620px;top:470px;font-size:40px">&#10005;</div>'
     '<div class="chip r" id="r1x2" style="left:620px;top:760px;font-size:40px">&#10005;</div>')
loc_js("l1", R1A); num_js("h1", R1A)
rv("#r1a1", W("tak", R1A) - 0.05); rv("#r1a2", W("span") - 0.05); pop("#r1x1", W("span") + 0.15, 0.3, sfx_="buzz")
rv("#r1a3", W("tak", W("span")) - 0.05); rv("#r1a4", W("gosok", R1A) - 0.05); pop("#r1x2", W("lama", R1A) + 0.1, 0.3, sfx_="buzz")

# ======================= R1B: tekan je, buih lembut terus keluar dari botol dan penuh tapak tangan (palm window over atrium) =======================
city("v_r1b", "mall_atrium", R1B, R2A - R1B, media=2.7)
ivid("v_plm", "palm", R1B, R2A - R1B, (90, 330, 560, 995))
veil("r1bv", R1B, R2A - R1B)
clip("r1b", R1B, R2A - R1B, loc("l1b", "DALAM MALL")
     + '<div class="chip a" id="r1b1" style="left:610px;top:430px">TEKAN JE</div>'
     f'<div style="position:absolute;left:680px;top:560px;width:380px;font:800 50px Figtree;line-height:1.2">{R("r1b2","buih")}</div>'
     f'<div class="sy amber" style="position:absolute;left:670px;top:630px;font-size:60px;line-height:1.1">{CH("r1b3","LEMBUT")}</div>'
     '<div class="chip" id="r1b4" style="left:620px;top:1060px;font-size:28px">PENUH TAPAK TANGAN</div>')
loc_js("l1b", R1B)
js.append(f'tl.fromTo("#v_plm",{{x:-650,rotation:-4}},{{x:0,rotation:0,duration:0.5,ease:"expo.out"}},{R1B:.2f});')
S(R1B, "whip", 0.5)
pop("#r1b1", W("tekan", R1B) - 0.05, 0.3, rot=-2); rv("#r1b2", W("buih", R1B) - 0.05); chars("#r1b3", W("lembut") - 0.05, 0.04)
S(W("buih", R1B), "foam", 0.6); pop("#r1b4", W("penuh") - 0.05, 0.3, rot=2)

# ======================= R2A: sebab kedua -- sea salt, kaya mineral (KLCC skyline by day) =======================
streak("sk3", R2A)
city("v_r2a", "klcc_day", R2A, R2B - R2A)
clip("r2a", R2A, R2B - R2A, '<div class="shade"></div>' + loc("l2", "KLCC", "KUALA LUMPUR") + num("h2", "02", "Sebab kedua")
     + f'<div class="t sy" style="top:420px;font-size:96px;line-height:1.05">{R("r2a1","SEA")}<br>{R("r2a2","<span class=amber>SALT</span>")}</div>'
     '<div class="chip" id="r2a3" style="left:70px;top:700px">KAYA MINERAL</div>'
     + bottle("r2g", "glory_single.png", 600, 650, 820))
loc_js("l2", R2A); num_js("h2", R2A)
rv("#r2a1", W("sea") - 0.05); rv("#r2a2", W("salt") - 0.05); pop("#r2a3", W("mineral") - 0.1, 0.3, rot=-2)
bottle_js("r2g", W("buih", R2A) - 0.1, R2B - W("buih", R2A) - 0.6)

# ======================= R2B: kulit rasa bersih, segar, tak kering (lather window over the mall) =======================
city("v_r2b", "mall_wide", R2B, R3A - R2B)
ivid("v_lt2", "lather2", R2B, R3A - R2B, (470, 330, 540, 960))
veil("r2bv", R2B, R3A - R2B)
clip("r2b", R2B, R3A - R2B, loc("l2b", "DALAM MALL")
     + f'<div style="position:absolute;left:70px;top:380px;font:800 52px Figtree">{R("r2b0","kulit rasa")}</div>'
     + "".join(f'<div class="chip a" id="r2b{k}" style="left:70px;top:{490 + k * 120}px">&#10003; {t}</div>' for k, t in enumerate(["BERSIH", "SEGAR", "TAK KERING"], 1)))
loc_js("l2b", R2B)
js.append(f'tl.fromTo("#v_lt2",{{x:600,rotation:4}},{{x:0,rotation:0,duration:0.5,ease:"expo.out"}},{R2B:.2f});')
S(R2B, "whip", 0.5); rv("#r2b0", W("kulit") - 0.05)
for k, w_ in enumerate(["bersih", "segar", "kering"], 1): pop(f"#r2b{k}", W(w_) - 0.05, 0.3, rot=-2 if k % 2 else 2)

# ======================= R3A: sebab ketiga -- bau dia memang bau perfume (mall boutique) =======================
streak("sk4", R3A)
city("v_r3a", "boutique", R3A, R3B - R3A)
clip("r3a", R3A, R3B - R3A, '<div class="shade"></div>' + loc("l3", "BUTIK MALL") + num("h3", "03", "Sebab ketiga")
     + f'<div class="t c" style="top:520px;font:800 56px Figtree">{R("r3a1","bau dia memang")}</div>'
     f'<div class="t c sy" style="top:610px;font-size:96px;line-height:1.05">{R("r3a2","BAU")}<br>{R("r3a3","<span class=amber>PERFUME</span>")}</div>')
loc_js("l3", R3A); num_js("h3", R3A)
rv("#r3a1", W("bau", R3A) - 0.05); rv("#r3a2", W("bau", W("memang")) - 0.05); rv("#r3a3", W("perfume", R3A) - 0.05); S(W("perfume", R3A), "shimmer", 0.5)

# ======================= R3B: Bombshell -- fresh & feminine (Menara KL) =======================
city("v_r3b", "kl_tower", R3B, R3C - R3B)
clip("r3b", R3B, R3C - R3B, '<div class="shade"></div>' + loc("l3b", "MENARA KL", "KUALA LUMPUR")
     + bottle("r3bg", "glory_single.png", 560, 520, 900)
     + f'<div style="position:absolute;left:60px;top:560px;width:500px"><div class="sy" style="font-size:62px;line-height:1.1">{R("r3b1","WOMAN")}<br>{R("r3b2","GLORY")}</div>'
     f'<div class="lab" style="margin-top:14px;color:#ffd3da">{R("r3b3","by Bombshell")}</div></div>'
     '<div class="chip r" id="r3bf" style="left:60px;top:860px">FRESH</div><div class="chip r" id="r3bm" style="left:60px;top:960px">FEMININE</div>')
loc_js("l3b", R3B); bottle_js("r3bg", R3B, R3C - R3B - 0.7); S(R3B, "whip", 0.5)
rv("#r3b1", R3B + 0.05); rv("#r3b2", R3B + 0.15); rv("#r3b3", R3B + 0.3)
pop("#r3bf", W("fresh", R3B) - 0.05, 0.3, rot=-2); pop("#r3bm", W("feminine") - 0.05, 0.3, rot=2)

# ======================= R3C: Midnight Fantasy -- manis & fruity (KLCC at night) =======================
streak("sk5", R3C)
city("v_r3c", "klcc_night", R3C, R3D - R3C)
clip("r3c", R3C, R3D - R3C, '<div class="shade"></div>' + loc("l3c", "KLCC", "MALAM")
     + bottle("r3cn", "noche_single.png", 600, 520, 900)
     + f'<div style="position:absolute;left:60px;top:560px;width:540px"><div class="sy" style="font-size:72px;line-height:1.1">{R("r3c1","NOCHE")}</div>'
     f'<div class="lab" style="margin-top:14px;color:#e2d8ff;line-height:1.5">{R("r3c2","by Midnight")}<br>{R("r3c3","Fantasy")}</div></div>'
     '<div class="chip v" id="r3cm" style="left:60px;top:860px">MANIS</div><div class="chip v" id="r3cf" style="left:60px;top:960px">FRUITY</div>')
loc_js("l3c", R3C); bottle_js("r3cn", R3C, R3D - R3C - 0.7)
rv("#r3c1", R3C + 0.05); rv("#r3c2", W("midnight") - 0.05); rv("#r3c3", W("fantasy") - 0.05)
pop("#r3cm", W("manis") - 0.05, 0.3, rot=-2); pop("#r3cf", W("fruity") - 0.05, 0.3, rot=2)

# ======================= R3D: lepas mandi, badan wangi yang lama (dusk: KLCC + Menara KL silhouettes) =======================
city("v_r3d", "kl_dusk", R3D, P1 - R3D, z0=1.08)
waves = "".join(f'<svg class="wv" style="position:absolute;left:0;top:{980 + k * 70}px;width:1080px;height:80px" viewBox="0 0 1080 80">'
                f'<path d="M-20 40 C 120 {5 + k * 6}, 240 {75 - k * 6}, 380 40 S 640 {5 + k * 8}, 780 40 S 1000 {70 - k * 5}, 1100 40" fill="none" '
                f'stroke="{["#ffb547", "#ffd3da", "#e2d8ff"][k]}" stroke-width="{5 - k}" stroke-linecap="round" stroke-dasharray="1400" stroke-dashoffset="1400"/></svg>'
                for k in range(3))
clip("r3d", R3D, P1 - R3D, '<div class="shade"></div>' + loc("l3d", "KLCC &middot; MENARA KL")
     + f'<div class="t c" style="top:520px;font:800 58px Figtree">{R("r3d1","Lepas mandi,")}</div>'
     f'<div class="t c sy" style="top:620px;font-size:100px;line-height:1.05">{R("r3d2","WANGI")}<br>{R("r3d3","<span class=amber>LAMA</span>")}</div>' + waves)
loc_js("l3d", R3D); S(R3D, "swoosh", 0.5)
rv("#r3d1", R3D + 0.05); rv("#r3d2", W("wangi", R3D) - 0.05); rv("#r3d3", W("lama", R3D) - 0.05)
js.append(f'tl.to("#r3d .wv path",{{strokeDashoffset:0,duration:1.0,stagger:0.12,ease:"power2.out"}},{W("badan"):.2f});')
S(W("badan"), "shimmer", 0.5)

# ======================= P1: orang lain dah mandi wangi macam pakai perfume (busy mall atrium) =======================
streak("sk6", P1)
city("v_p1", "mall_tokyo", P1, P2 - P1)
clip("p1", P1, P2 - P1, '<div class="shade" style="background:rgba(10,14,26,.62)"></div>' + loc("lp1", "DALAM MALL")
     + f'<div class="t c" style="top:480px;font:800 60px Figtree">{R("p1a","Orang lain dah")}</div>'
     f'<div class="t c" style="top:570px;font:800 60px Figtree">{R("p1b","mandi")} {R("p1c","<span class=amber>wangi</span>")}</div>'
     f'<div class="t c syl" style="top:690px;font-size:42px">{R("p1d","MACAM PAKAI")}</div>'
     f'<div class="t c sy" style="top:760px;font-size:100px">{CH("p1e","PERFUME")}</div>')
loc_js("lp1", P1)
rv("#p1a", W("orang") - 0.05); rv("#p1b", W("mandi", P1) - 0.05); rv("#p1c", W("wangi", P1) - 0.05); rv("#p1d", W("macam") - 0.05); chars("#p1e", W("perfume", P1) - 0.1, 0.03)

# ======================= P2: kau masih setia dengan sabun biasa, tak payah beli perfume (escalator) =======================
city("v_p2", "escalator", P2, P3 - P2)
clip("p2", P2, P3 - P2, '<div class="shade"></div>' + loc("lp2", "DALAM MALL")
     + f'<div class="t c" style="top:470px;font:800 58px Figtree">{R("p2a","Kau masih setia dengan")}</div>'
     f'<div class="t c sy" id="p2b" style="top:570px;font-size:84px;color:var(--steel)">SABUN BIASA?</div>'
     '<div id="p2s" style="position:absolute;left:180px;top:620px;width:720px;height:8px;border-radius:4px;background:#e0475f;transform-origin:0 50%"></div>'
     f'<div class="t c" style="top:760px;font:800 56px Figtree">{R("p2c","tak payah beli")} {R("p2d","<span class=amber>perfume</span>")}</div>')
loc_js("lp2", P2); S(P2, "swoosh", 0.5)
rv("#p2a", W("kau", P2) - 0.05); fade("#p2b", W("sabun", P2) - 0.05, 0.3, y=20)
js.append(f'tl.fromTo("#p2s",{{scaleX:0}},{{scaleX:1,duration:0.3,ease:"power2.out"}},{W("biasa") + 0.25:.2f});')
S(W("biasa") + 0.25, "buzz", 0.4)
rv("#p2c", W("tak", P2) - 0.05); rv("#p2d", W("perfume", P2) - 0.05)

# ======================= P3: sekarang ni, sabun ni dah buat kau wangi (duo over the white atrium) =======================
streak("sk7", P3)
city("v_p3", "mall_atrium", P3, P4 - P3, media=4.4, z0=1.18)
clip("p3", P3, P4 - P3, '<div class="shade"></div>' + loc("lp3", "DALAM MALL", "KUALA LUMPUR")
     + f'<div class="t c syl" style="top:250px;font-size:44px">{R("p3a","SEKARANG NI")}</div>'
     f'<div class="t c" style="top:330px;font:800 60px Figtree">{R("p3b","sabun ni dah buat kau")}</div>'
     f'<div class="t c sy amber" style="top:420px;font-size:110px">{CH("p3c","WANGI")}</div>'
     + bottle("p3d", "duo_white_cut.png", 290, 640, 700))
loc_js("lp3", P3)
rv("#p3a", W("sekarang", P3) - 0.05); rv("#p3b", W("sabun", P3) - 0.05); chars("#p3c", W("wangi", P3) - 0.1, 0.04)
bottle_js("p3d", W("sabun", P3) - 0.1, P4 - W("sabun", P3) - 0.6)

# ======================= P4: stok kami tinggal sikit je (KL night) =======================
city("v_p4", "kl_night", P4, P5 - P4)
clip("p4", P4, P5 - P4, '<div class="shade"></div>' + loc("lp4", "KUALA LUMPUR")
     + f'<div class="t c syl" style="top:600px;font-size:54px">{R("p4a","STOK KAMI")}</div>'
     f'<div class="t c" style="top:690px;font:800 70px Figtree">{R("p4b","tinggal")} {R("p4c","<span class=amber>sikit je</span>")}</div>'
     '<div style="position:absolute;left:140px;top:880px;width:800px;height:24px;border-radius:12px;background:rgba(238,241,246,.2);overflow:hidden">'
     '<i id="p4f" style="position:absolute;inset:0;border-radius:12px;background:linear-gradient(90deg,#e0475f,#ffb547);transform-origin:0 50%"></i></div>')
loc_js("lp4", P4); S(P4, "whip", 0.5)
rv("#p4a", W("stok") - 0.05); rv("#p4b", W("tinggal") - 0.05); rv("#p4c", W("sikit") - 0.05)
js.append(f'tl.fromTo("#p4f",{{scaleX:0.55}},{{scaleX:0.08,duration:1.6,ease:"power2.inOut"}},{W("stok"):.2f});'); S(W("stok"), "riser", 0.35)

# ======================= P5: nanti habis, jangan menyesal. tak beli, rugi besar =======================
clip("p5", P5, C1 - P5, '<div class="nightbg"></div>'
     f'<div class="t c" style="top:520px;font:800 60px Figtree">{R("p5a","Nanti habis,")}</div>'
     f'<div class="t c sy" id="p5b" style="top:620px;font-size:84px;line-height:1.1">JANGAN<br>MENYESAL</div>'
     f'<div class="t c sy" id="p5c" style="top:900px;font-size:130px;color:var(--rose);text-shadow:0 0 40px rgba(224,71,95,.6)">RUGI</div>'
     f'<div class="t c sy amber" id="p5d" style="top:1060px;font-size:96px">BESAR</div>')
rv("#p5a", P5 + 0.02)
js.append(f'tl.fromTo("#p5b",{{scale:1.6,opacity:0}},{{scale:1,opacity:1,duration:0.3,ease:"power4.out"}},{W("jangan") - 0.05:.2f});'); S(W("jangan"), "stamp", 0.6)
js.append(f'tl.fromTo("#p5c",{{scale:2.4,opacity:0}},{{scale:1,opacity:1,duration:0.25,ease:"power4.out"}},{W("rugi") - 0.05:.2f});')
js.append(f'tl.to("#p5c",{{x:-12,duration:0.04,yoyo:true,repeat:5}},{W("rugi") + 0.2:.2f});')
js.append(f'tl.fromTo("#p5d",{{y:80,opacity:0}},{{y:0,opacity:1,duration:0.3,ease:"back.out(2)"}},{W("besar") - 0.05:.2f});')
S(W("rugi") - 0.05, "boom", 0.6); S(W("rugi") + 0.2, "buzz", 0.45)

# ======================= C1: tekan beg kuning sekarang (mall escalators) =======================
streak("sk8", C1)
city("v_c1", "mall_esc", C1, C2 - C1, media=2.8)
clip("c1", C1, C2 - C1, '<div class="shade"></div>' + loc("lc1", "DALAM MALL")
     + f'<div id="c1b" style="position:absolute;left:120px;top:780px;width:840px;height:190px;border-radius:95px;background:var(--bag);display:flex;align-items:center;justify-content:center;'
     f'gap:22px;font:900 58px Figtree;color:var(--night);box-shadow:0 0 60px rgba(246,196,69,.45),0 26px 60px rgba(0,0,0,.5)">{BAG.format(s=96)}TEKAN BEG KUNING</div>'
     '<div id="c1r" style="position:absolute;left:470px;top:800px;width:150px;height:150px;border-radius:50%;border:7px solid #fff"></div>'
     '<div class="chip a" id="c1s" style="left:390px;top:1040px;font-size:40px">SEKARANG</div>')
loc_js("lc1", C1)
js.append(f'tl.fromTo("#c1b",{{y:300,scale:0.8,opacity:0}},{{y:0,scale:1,opacity:1,duration:0.4,ease:"back.out(1.8)"}},{C1:.2f});')
tk = W("kuning", C1)
js.append(f'tl.to("#c1b",{{scale:0.93,duration:0.09,yoyo:true,repeat:1}},{tk:.2f});')
js.append(f'tl.fromTo("#c1r",{{scale:0.2,opacity:1}},{{scale:1.9,opacity:0,duration:0.5,ease:"power2.out"}},{tk + 0.05:.2f});')
S(tk, "click", 0.75); S(tk + 0.05, "ding", 0.55); pop("#c1s", W("sekarang", C1) - 0.05, 0.3, rot=-2)

# ======================= C2: dan check out sekarang sebelum stok kami habis (KL night aerial) =======================
city("v_c2", "kl_aerial", C2, VOICE_END + 0.6 - C2, z0=1.2)
conf = "".join(f'<i class="cf" style="position:absolute;left:530px;top:1000px;width:{r}px;height:{r}px;border-radius:{"50%" if k % 2 else "3px"};background:{c}"></i>'
               for k, (r, c) in enumerate([(18, "#ffb547"), (14, "#f6c445"), (20, "#e0475f"), (12, "#9b7bff"), (16, "#fff"),
                                           (14, "#ffb547"), (18, "#e0475f"), (12, "#9b7bff"), (16, "#f6c445"), (14, "#fff")]))
clip("c2", C2, VOICE_END + 0.6 - C2, '<div class="shade"></div>' + loc("lc2", "KUALA LUMPUR")
     + '<div id="c2btn" style="position:absolute;left:190px;top:700px;width:700px;height:160px;border-radius:80px;background:var(--chrome);color:var(--night);'
     'display:flex;align-items:center;justify-content:center;gap:22px;font:900 52px Figtree;letter-spacing:6px;box-shadow:0 0 50px rgba(238,241,246,.3)">'
     'CHECK OUT<svg viewBox="0 0 100 100" style="width:72px;height:72px"><path id="c2tk" d="M20 52 L42 72 L80 30" stroke="#e0475f" stroke-width="12" fill="none" '
     'stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="100" stroke-dashoffset="100"/></svg></div>'
     f'<div class="t c syl" style="top:960px;font-size:40px">{R("c2a","SEBELUM STOK")}</div>'
     f'<div class="t c sy" id="c2h" style="top:1030px;font-size:110px;color:var(--rose);text-shadow:0 0 40px rgba(224,71,95,.6)">HABIS</div>' + conf)
loc_js("lc2", C2)
js.append(f'tl.fromTo("#c2btn",{{y:200,opacity:0}},{{y:0,opacity:1,duration:0.35,ease:"back.out(1.8)"}},{C2 + 0.02:.2f});')
tch = W("check", C2)
js.append(f'tl.to("#c2btn",{{scale:0.93,duration:0.1,yoyo:true,repeat:1}},{tch:.2f});')
js.append(f'tl.to("#c2btn",{{backgroundColor:"#ffb547",duration:0.3}},{tch + 0.15:.2f});')
js.append(f'tl.to("#c2tk",{{strokeDashoffset:0,duration:0.3,ease:"power2.out"}},{tch + 0.2:.2f});')
S(tch, "click", 0.7); S(tch + 0.2, "ding", 0.65)
for k in range(10):
    a = -math.pi / 2 + (k - 4.5) * 0.33
    js.append(f'tl.fromTo("#c2 .cf:nth-of-type({k + 1})",{{x:0,y:0,opacity:1,rotation:0}},{{x:{math.cos(a) * 400:.0f},y:{math.sin(a) * 320 - 200:.0f},rotation:{180 + k * 40},opacity:0,duration:1.0,ease:"power2.out"}},{tch + 0.25:.2f});')
rv("#c2a", W("sebelum") - 0.05)
js.append(f'tl.fromTo("#c2h",{{scale:2,opacity:0}},{{scale:1,opacity:1,duration:0.25,ease:"power4.out"}},{W("habis", C2) - 0.1:.2f});'); S(W("habis", C2), "stamp", 0.6)

# ======================= END CARD (Petronas from below) =======================
html.append(f'<video id="v_end" class="clip bg" src="assets/broll/klcc_up.mp4" data-start="{VOICE_END:.3f}" data-duration="{DURATION - VOICE_END:.3f}" data-media-start="0" muted playsinline style="z-index:6"></video>')
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
    if m and not m.group(1).startswith(("cap", "sk", "v_face", "c2", "v_c2")):
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
