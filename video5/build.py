"""Video 5 (modern motion graphics, minimalist luxury, upbeat): "Tidur wangi semerbak" -- story to product.
Builds project/index.html (HyperFrames + GSAP) and project/assets/audio/sfx_cues.json from the cleaned voice's word times.
Usage: python3 -I build.py PROJECT_DIR [--final]"""
import json, re, sys

proj = sys.argv[1]
FINAL = "--final" in sys.argv
DURATION = 52.2          # voice is 50.7 s + end-card tail

words = [w for s in json.load(open(f"{proj}/assets/audio/words.json")) for w in s["words"]]
FIX = {"lakseri": "luxury", "hati.": "hotel.", "hati": "hotel", "pajak": "panjat", "-kanti": "katil", "bantan": "bantal",
       "vex": "vibes", "usia": "tekan", "abek": "beg", "kuni": "kuning", "gang": "geng", "Terus": "Terus",
       "body": "buddy", "umat": "mak", "pocket": "poket", "kati": "katil", "semerba": "semerbak", "semerbah": "semerbak", "semerbah.": "semerbak.", "ku": "kuning", "kanti": "katil", "kanti,": "katil,",
       "Malam-lamam": "Lama-lama", "Malam-lamam,": "Lama-lama,"}   # client: "buddy", not "body"
DROP = {"Haa", "Haa,", "ke", "Dia,", "Apa"}          # fillers / mis-hearings left out of the captions
HL = {"wangi", "semerbak", "luxury", "hotel", "perangai", "mengada-ngada", "tidur", "standard", "spray", "perfume", "mahal",
      "mahal-mahal", "menangis", "membazir", "rahsia", "mandi", "malam", "melekat", "kulit", "fresh", "premium", "expensive",
      "vibes", "beg", "kuning", "habis", "katil", "bantal", "buddy"}
clean = []
for w in words:
    txt = w["w"].strip()
    core = txt.rstrip(".,?"); tail = txt[len(core):]
    if txt in DROP or core in DROP:
        continue
    if core == "-kanti":
        clean[-1]["t"] = "panjat katil"; clean[-1]["e"] = w["e"]; continue
    txt = FIX.get(txt, FIX.get(core, core) + tail)
    if txt.startswith("-") and clean:
        clean[-1]["t"] += txt; clean[-1]["e"] = w["e"]; continue
    if clean and clean[-1]["t"] == "kuning" and core == "ni" and w["s"] - clean[-1]["e"] < 0.15:   # "beg ku ni" = "beg kuning"
        clean[-1]["e"] = w["e"]; continue
    clean.append({"t": txt, "s": w["s"], "e": w["e"]})
for w in clean:
    w["t"] = {"Malam-lamam": "Lama-lama", "Malam-lamam,": "Lama-lama,"}.get(w["t"], w["t"])
chunks, cur = [], []
for i, w in enumerate(clean):
    cur.append(w)
    nxt = clean[i + 1] if i + 1 < len(clean) else None
    if (len(cur) >= 3 or re.search(r"[.,?!]$", w["t"]) or nxt is None or nxt["s"] - w["e"] > 0.3
            or len(" ".join(x["t"] for x in cur)) > 20):
        chunks.append(cur); cur = []

html, js, sfx = [], [], []
SPEED = 0.55             # client asked for snappier motion: every short tween runs ~45% faster
def _fast(l):
    return re.sub(r"duration:([\d.]+)", lambda m: f"duration:{float(m.group(1)) * SPEED:.2f}" if float(m.group(1)) <= 1.3 else m.group(0), l)
def A(l): js.append(_fast(l))
def S(t, s, g=0.6, auto=False):
    if s == "swoosh": s, g = "whip", g * 0.9      # short, punchy "sup" instead of the long soft swoosh
    if s == "tick": s = "top"
    sfx.append({"t": round(t, 3), "sfx": s, "gain": g, "auto": auto})
def clip(id_, s, d, inner="", cls="", style=""):
    html.append(f'<div id="{id_}" class="clip {cls}" data-start="{s:.3f}" data-duration="{d:.3f}" style="{style}">{inner}</div>')
def vid(id_, src, s, d, box, cls="frame", z0=1.15, z1=1.0, media="0", img=False):
    """Video/photo inside a masked frame; box = (left, top, w, h). The <video> is timed itself (required for playback)."""
    l, tp, w, h = box
    rad = "50%" if cls == "circle" else "44px"
    html.append(f'<div id="{id_}w" class="clip" data-start="{s:.3f}" data-duration="{d:.3f}" style="z-index:4">'
                f'<div id="{id_}m" class="{cls}" style="left:{l}px;top:{tp}px;width:{w}px;height:{h}px"></div></div>')
    st = f'z-index:4;left:{l}px;top:{tp}px;width:{w}px;height:{h}px;object-fit:cover;border-radius:{rad}'
    if img:
        html.append(f'<img id="{id_}" class="clip" src="{src}" data-start="{s:.3f}" data-duration="{d:.3f}" alt="" style="{st}">')
    else:
        html.append(f'<video id="{id_}" class="clip" src="{src}" data-start="{s:.3f}" data-duration="{d:.3f}" data-media-start="{media}" '
                    f'muted playsinline style="{st}"></video>')
    # zoom punch in, then a slow drift
    js.append(f'tl.fromTo("#{id_}",{{scale:{max(z0, 1.22)}}},{{scale:1.04,duration:0.42,ease:"expo.out"}},{s});')
    js.append(f'tl.to("#{id_}",{{scale:{z1},duration:{max(d - 0.42, 0.1):.2f},ease:"none"}},{s + 0.42:.3f});')
    js.append(f'tl.fromTo("#{id_},#{id_}m",{{clipPath:"inset(100% 0% 0% 0% round 44px)"}},{{clipPath:"inset(0% 0% 0% 0% round 44px)",duration:0.34,ease:"expo.out"}},{s});')
    S(s, "whip", 0.45, auto=True); S(s + 0.12, "top", 0.4, auto=True)
def full(id_, src, s, d, z0=1.12, z1=1.0, tag="video", reveal="circle", media="0"):
    if tag == "video":
        html.append(f'<video id="{id_}" class="clip bg" src="{src}" data-start="{s:.3f}" data-duration="{d:.3f}" data-media-start="{media}" muted playsinline></video>')
    else:
        html.append(f'<img id="{id_}" class="clip bg" src="{src}" data-start="{s:.3f}" data-duration="{d:.3f}" alt="">')
    js.append(f'tl.fromTo("#{id_}",{{scale:{max(z0, 1.2)}}},{{scale:1.03,duration:0.45,ease:"expo.out"}},{s});')
    js.append(f'tl.to("#{id_}",{{scale:{z1},duration:{max(d - 0.45, 0.1):.2f},ease:"none"}},{s + 0.45:.3f});')
    if reveal == "circle":
        js.append(f'tl.fromTo("#{id_}",{{clipPath:"circle(0% at 50% 50%)"}},{{clipPath:"circle(75% at 50% 50%)",duration:0.4,ease:"expo.out"}},{s});')
    elif reveal == "up":
        js.append(f'tl.fromTo("#{id_}",{{clipPath:"inset(100% 0% 0% 0%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:0.36,ease:"expo.out"}},{s});')
    S(s, "whip", 0.5, auto=True)
def rv(sel, t, d=0.7):
    js.append(f'tl.fromTo("{sel} > span",{{yPercent:115}},{{yPercent:0,duration:{max(d * SPEED, 0.22):.2f},ease:"expo.out"}},{t:.2f});')
    S(t, "top", 0.38, auto=True)
def fade(sel, t, d=0.6, y=24, x=0):
    js.append(f'tl.fromTo("{sel}",{{opacity:0,y:{y},x:{x}}},{{opacity:1,y:0,x:0,duration:{max(d * SPEED, 0.2):.2f},ease:"expo.out"}},{t:.2f});')
    S(t, "top", 0.32, auto=True)
def line(sel, t, d=0.8):
    js.append(f'tl.fromTo("{sel}",{{scaleX:0}},{{scaleX:1,duration:{max(d * SPEED, 0.22):.2f},ease:"expo.out"}},{t:.2f});')
def pop(sel, t, d=0.5):
    js.append(f'tl.fromTo("{sel}",{{scale:0}},{{scale:1,duration:{max(d * 0.65, 0.22):.2f},ease:"back.out(3)"}},{t:.2f});')
    S(t, "top", 0.5, auto=True)
def typed(sel, t, d=0.6, n=12):
    js.append(f'tl.fromTo("{sel}",{{clipPath:"inset(0% 100% 0% 0%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:{d},ease:"steps({n})"}},{t:.2f});')
def R(id_, txt): return f'<span id="{id_}" class="rv"><span>{txt}</span></span>'
def sect(n, s, d, label, light=False):
    c = ' style="color:rgba(255,255,255,.75)"' if light else ""
    b = ' style="color:#fff"' if light else ""
    clip(f"sect{n}", s, d, f'<div class="sect"{c}><b{b}>0{n}</b> &nbsp;/ 04 &nbsp;&nbsp;{label}</div>', style="z-index:8")
    fade(f"#sect{n} .sect", s + 0.1, 0.5, 10)
def bubble(id_, l, tp, name, txt, v=False):
    return (f'<div class="bubble{" v" if v else ""}" id="{id_}" style="left:{l}px;top:{tp}px"><div class="av"></div>'
            f'<div><small>{name}</small><span class="tx" id="{id_}t">{txt}</span></div></div>')
RINGS = ('<svg viewBox="0 0 220 140" style="width:440px;height:280px"><circle cx="80" cy="70" r="52" fill="none" stroke="#161412" stroke-width="7"/>'
         '<circle cx="140" cy="70" r="52" fill="none" stroke="#a5162f" stroke-width="7"/><path d="M128 14 l12 -12 l12 12 l-12 10z" fill="#a5162f"/></svg>')
SHARE = ('<svg viewBox="0 0 64 64"><path d="M38 10 L58 30 L38 50 V38 C24 38 14 42 6 54 C8 36 18 24 38 22 Z" fill="#161412"/></svg>')

BASKET = ('<svg viewBox="0 0 120 110"><path d="M38 40 L52 10 M82 40 L68 10" stroke="#161412" stroke-width="8" stroke-linecap="round"/>'
          '<path d="M8 40 H112 L100 100 H20 Z" fill="#161412"/></svg>')
CHECK = ('<svg viewBox="0 0 100 100"><path id="ck" d="M22 52 L42 72 L78 32" stroke="#f3eee6" stroke-width="9" fill="none" '
         'stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="90" stroke-dashoffset="90"/></svg>')
SPARK = ('<svg viewBox="0 0 100 100"><path d="M50 4 L58 42 L96 50 L58 58 L50 96 L42 58 L4 50 L42 42 Z" fill="#c9a24a"/></svg>')
FACE0, FACE1 = 4.80, 5.70     # client: face under 1 s

# ---- S0 0.00-2.85: HOOK (flash-forward) -- "Satu bilik tidur tu jadi wangi"
full("v_hotel", "assets/broll/hotel.mp4", 0.0, 2.85, 1.15, 1.0)
clip("s0", 0.0, 2.85, '<div class="shade" style="background:linear-gradient(180deg,rgba(0,0,0,.45) 0%,rgba(0,0,0,0) 45%,rgba(0,0,0,.35) 100%)"></div>'
     f'<div class="t c kick light" style="top:300px;letter-spacing:14px">{R("h0","Satu bilik tidur")}</div>'
     f'<div class="t c serif-it light" style="top:360px;font-size:110px">{R("h1","jadi")}</div>'
     f'<div class="t c light" style="top:500px;font:200 190px/1 Montserrat;letter-spacing:-4px" id="h2w">{R("h2","WANGI")}</div>'
     f'<div id="h3" style="position:absolute;left:800px;top:470px;width:90px;height:90px">{SPARK}</div>')
rv("#h0", 0.64); rv("#h1", 2.0, 0.5); rv("#h2", 2.28, 0.5); pop("#h3", 2.4, 0.4)
A('tl.to("#h3",{rotation:90,duration:0.6,ease:"power2.out"},2.5);')
S(0.0, "boom", 0.55); S(2.28, "boom", 0.4); S(2.4, "shimmer", 0.4)

# ---- S0b 2.85-4.80: "Terus auto macam LUXURY HOTEL"
full("v_corr", "assets/broll/corridor.mp4", 2.85, 1.95, 1.2, 1.0)
clip("s0b", 2.85, 1.95, '<div class="shade" style="background:rgba(10,8,6,.30)"></div>'
     f'<div class="t c kick light" style="top:640px;letter-spacing:14px">{R("l0","Terus auto macam")}</div>'
     f'<div class="t c light" style="top:720px;font:200 150px/1 Montserrat;letter-spacing:-3px">{R("l1","LUXURY")}</div>'
     f'<div class="t c serif-it" style="top:880px;font-size:130px;color:#f2d388">{R("l2","hotel")}</div>'
     '<div class="hair" id="l3" style="left:340px;width:400px;top:1060px;background:#f2d388"></div>')
rv("#l0", 2.95); rv("#l1", 3.64, 0.5); rv("#l2", 4.24, 0.5); line("#l3", 4.3)
S(3.64, "boom", 0.5)

# ---- S1 4.80-5.70: the only face shot (0.9 s) -- "Korang, aku..."
html.append(f'<video id="v_face" class="clip bg" src="assets/broll/face.mp4" data-start="{FACE0}" data-duration="{FACE1-FACE0:.2f}" data-media-start="0" muted playsinline style="z-index:6"></video>')
A(f'tl.fromTo("#v_face",{{scale:1.12}},{{scale:1.0,duration:0.45,ease:"expo.out"}},{FACE0});')
A(f'tl.fromTo("#v_face",{{clipPath:"inset(0% 0% 0% 100%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:0.3,ease:"expo.out"}},{FACE0});')
clip("s1", FACE0, FACE1 - FACE0, '<div class="shade" style="background:linear-gradient(180deg,rgba(0,0,0,0) 55%,rgba(0,0,0,.55) 100%)"></div>'
     f'<div class="t c light" style="top:1380px;font:200 130px/1 Montserrat;letter-spacing:-3px">{R("f0","KORANG,")}</div>', style="z-index:7")
rv("#f0", 4.85, 0.45)
S(4.8, "whip", 0.5)

# ---- S1b 5.70-6.80: "...ada satu PERANGAI tau" -- kinetic type
clip("s1b", FACE1, 6.80 - FACE1, '<div class="shade" style="background:var(--ink)"></div>'
     f'<div class="t c kick" style="top:700px;color:rgba(255,255,255,.7);letter-spacing:14px">{R("f1","Aku ada satu")}</div>'
     f'<div class="t c" style="top:770px;font:200 170px/1 Montserrat;letter-spacing:-4px;color:#fff">{R("f2","PERANGAI")}</div>'
     f'<div class="t c serif-it" style="top:960px;font-size:110px;color:#f2d388">{R("f3","tau!")}</div>')
A(f'tl.fromTo("#s1b",{{clipPath:"inset(100% 0% 0% 0%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:0.35,ease:"expo.out"}},{FACE1});')
rv("#f1", 5.72); rv("#f2", 5.78, 0.45); rv("#f3", 6.24, 0.4)
S(5.7, "whip", 0.5); S(5.78, "boom", 0.45)

# ---- S2 6.80-10.85: mak selalu bising -- "mengada-ngada"
clip("s2", 6.80, 4.05, '<div class="ivory grid"></div>'
     f'<div class="t c kick" style="top:420px">{R("m0","Lepas tu mak aku")}</div>'
     f'<div class="t c big" style="top:480px">{R("m1","SELALU BISING")}</div>'
     '<div class="bubble" id="m2" style="left:200px;top:760px;font-size:56px;padding:34px 50px 34px 30px"><div class="av" style="width:80px;height:80px"></div>'
     '<div><small>MAK</small><span class="tx" id="m2t">"Mengada-ngada!"</span></div></div>'
     '<div class="t c" style="top:1080px;font:200 260px/1 Montserrat;color:var(--rose)" id="m3">!!</div>')
A('tl.fromTo("#s2",{clipPath:"inset(0% 0% 0% 100%)"},{clipPath:"inset(0% 0% 0% 0%)",duration:0.45,ease:"expo.inOut"},6.80);')
rv("#m0", 6.9); rv("#m1", 7.86, 0.5); fade("#m2", 8.6, 0.4, 30); typed("#m2t", 9.9, 0.55, 14); pop("#m3", 10.18, 0.4)
A('tl.to("#m2",{x:-12,duration:0.05,yoyo:true,repeat:5,ease:"none"},10.2);')
sect(1, 6.80, 9.0, "PERANGAI")
S(8.1, "boom", 0.4); S(9.95, "click", 0.4); S(10.15, "click", 0.4)

# ---- S3 10.85-15.60: sebab apa? nak tidur -> badan mesti wangi semerbak
clip("bg3", 10.85, 4.75, '<div class="ivory"></div>', style="z-index:2")
vid("v_bed", "assets/broll/bedroom.mp4", 10.85, 4.75, (90, 380, 900, 1150))
vid("v_cdl", "assets/broll/candle.mp4", 13.2, 2.4, (640, 1200, 380, 380), cls="circle")
clip("s3", 10.85, 4.75, f'<div class="t c" style="top:150px;font:300 96px/1 Montserrat;letter-spacing:-2px">{R("q0","SEBAB APA?")}</div>'
     '<div class="shade" style="inset:auto;left:90px;top:1030px;width:900px;height:500px;border-radius:0 0 44px 44px;background:linear-gradient(180deg,rgba(0,0,0,0),rgba(0,0,0,.55))"></div>'
     f'<div class="t" style="top:1000px;left:150px;font:200 120px/1 Montserrat;color:#fff;letter-spacing:-2px">{R("q1","TIDUR")}</div>'
     f'<div class="t serif-it" style="top:1140px;left:150px;font-size:76px;color:#fff">{R("q2","wangi semerbak")}</div>')
rv("#q0", 10.9, 0.5); rv("#q1", 12.38, 0.5); rv("#q2", 14.18, 0.6)
S(10.9, "boom", 0.4); S(14.2, "shimmer", 0.5)

# ---- S4 15.60-18.85: body yang ada standard
clip("s4", 15.6, 3.25, '<div class="ivory grid"></div>'
     f'<div class="t c kick" style="top:520px">{R("b0","Barulah rasa macam")}</div>'
     f'<div class="t c" style="top:600px;font:200 220px/1 Montserrat;letter-spacing:-6px">{R("b1","BUDDY")}</div>'
     f'<div class="t c serif-it" style="top:850px;font-size:90px;color:var(--mute)">{R("b2","yang ada")}</div>'
     f'<div class="badge" id="b3" style="left:390px;top:1000px">{CHECK}STAN<br>DARD</div>')
A('tl.fromTo("#s4",{clipPath:"circle(0% at 50% 50%)"},{clipPath:"circle(80% at 50% 50%)",duration:0.45,ease:"expo.out"},15.6);')
rv("#b0", 15.7); rv("#b1", 17.18, 0.5); rv("#b2", 17.72); pop("#b3", 18.12, 0.45)
A('tl.to("#ck",{strokeDashoffset:0,duration:0.3,ease:"power2.out"},18.3);')
S(15.6, "whip", 0.5); S(17.18, "boom", 0.45); S(18.3, "chime", 0.4)

# ---- S5 18.85-22.90: dulu... sebelum panjat katil, jenuh aku spray
clip("bg5", 18.85, 4.05, '<div class="ivory"></div>', style="z-index:2")
vid("v_bd", "assets/broll/bed.mp4", 18.85, 4.05, (90, 380, 900, 1000))
clip("s5", 18.85, 4.05, f'<div class="t kick" style="top:180px">{R("p0","Dulu, korang faham-faham je lah")}</div>'
     f'<div class="t" style="top:240px;font:300 92px/1 Montserrat;letter-spacing:-2px">{R("p1","PANJAT KATIL")}</div>'
     f'<div class="t c" style="top:1150px;font:300 170px/1 Montserrat;letter-spacing:-4px;color:var(--rose);text-shadow:0 4px 30px rgba(255,255,255,.8)">{R("p2","SPRAY!")}</div>'
     + "".join(f'<div class="dot sp" style="left:{540 + dx}px;top:{1130 + dy}px"></div>' for dx, dy in
               ((-260, -40), (-180, -120), (-90, -170), (0, -190), (90, -170), (180, -120), (260, -40), (-220, 60), (220, 60))))
rv("#p0", 18.95); rv("#p1", 20.98, 0.5); rv("#p2", 22.26, 0.45)
A('tl.fromTo("#s5 .sp",{scale:0,opacity:1,y:60},{scale:1.4,opacity:0,y:0,duration:0.7,stagger:0.03,ease:"expo.out"},22.3);')
S(22.3, "foam", 0.55)

# ---- S6 22.90-26.60: perfume mahal-mahal kat badan, kat baju, kat bantal
clip("bg6", 22.9, 3.7, '<div class="ivory"></div>', style="z-index:2")
vid("v_sh", "assets/broll/shelf.mp4", 22.9, 3.7, (90, 330, 900, 1000))
clip("s6", 22.9, 3.7, f'<div class="t kick" style="top:180px">{R("r0","Perfume")}</div>'
     f'<div class="t" style="top:230px;font:300 92px/1 Montserrat;letter-spacing:-2px">{R("r1","MAHAL-MAHAL")}</div>'
     '<div class="t c" style="top:1380px"><div class="chip" id="r2"><i></i>BADAN</div><div class="chip" id="r3"><i></i>BAJU</div>'
     '<div class="chip" id="r4"><i></i>BANTAL</div></div>'
     '<div class="lbl r" id="r5" style="left:640px;top:400px;font-size:34px">RM RM RM</div>')
rv("#r0", 23.0); rv("#r1", 23.8, 0.5); pop("#r5", 24.1, 0.4)
fade("#r2", 24.62, 0.4, 30); fade("#r3", 25.3, 0.4, 30); fade("#r4", 26.04, 0.4, 30)
S(24.1, "click", 0.5)

# ---- S7 26.60-30.70: poket menangis, membazir gila
clip("bg7", 26.6, 4.1, '<div class="ivory"></div>', style="z-index:2")
vid("v_mn", "assets/broll/money.mp4", 26.6, 4.1, (90, 380, 900, 900))
vid("v_wl", "assets/broll/wallet.mp4", 26.6, 4.1, (620, 1060, 400, 400), cls="circle")
clip("s7", 26.6, 4.1, f'<div class="t kick" style="top:180px">{R("w0","Lama-lama poket aku")}</div>'
     f'<div class="t" style="top:240px;font:300 100px/1 Montserrat;letter-spacing:-2px">{R("w1","MENANGIS")}</div>'
     '<div class="t" style="top:1330px;right:auto;width:500px;font:600 24px Montserrat;letter-spacing:8px;color:var(--mute)" id="w2">BAKI POKET</div>'
     '<div class="bar" style="left:90px;width:480px;top:1380px;height:14px"><i id="w3" style="width:100%;background:var(--ink)"></i></div>'
     f'<div class="t" style="top:1430px;right:auto;width:560px;font:italic 500 76px/1.1 Playfair;color:var(--rose)">{R("w4","membazir gila!")}</div>')
rv("#w0", 26.7); rv("#w1", 28.46, 0.5); fade("#w2", 27.6, 0.3, 10)
A('tl.fromTo("#w3",{scaleX:1},{scaleX:0.04,duration:2.2,ease:"power2.in"},27.8);')
A('tl.to("#w3",{backgroundColor:"#a5162f",duration:0.4},29.0);')
rv("#w4", 29.44, 0.5)
sect(2, 15.6, 15.1, "DULU")
S(28.46, "boom", 0.45); S(29.44, "boom", 0.4)

# ---- S8 30.70-34.05: satu hari... aku terjumpa satu RAHSIA (product reveal)
clip("s8", 30.7, 3.35, '<div class="shade" style="background:radial-gradient(ellipse at 50% 45%,#2a2430 0%,#0d0b10 70%)"></div>'
     f'<div class="t c kick" style="top:330px;color:rgba(255,255,255,.7)">{R("x0","Sampailah satu hari tu")}</div>'
     f'<div class="t c serif-it" style="top:390px;font-size:84px;color:#fff">{R("x1","aku terjumpa satu")}</div>'
     f'<div class="t c" style="top:500px;font:200 170px/1 Montserrat;letter-spacing:6px;color:#f2d388" id="x2">RAHSIA</div>'
     '<div class="glow" id="x4" style="left:240px;top:760px;width:600px;height:600px;opacity:.5"></div>')
A('tl.fromTo("#s8",{opacity:0},{opacity:1,duration:0.3},30.7);')
rv("#x0", 30.78); rv("#x1", 32.18, 0.5)
A('tl.fromTo("#x2",{opacity:0,filter:"blur(24px)",scale:1.3},{opacity:1,filter:"blur(0px)",scale:1,duration:0.6,ease:"expo.out"},33.22);')
A('tl.fromTo("#x4",{scale:0.5,opacity:0},{scale:1,opacity:.5,duration:0.8,ease:"expo.out"},33.3);')
vid("p_rev", "assets/product/duo_white.jpg", 33.4, 0.65, (330, 780, 420, 746), img=True)
html[-2] = html[-2].replace('style="z-index:4"', 'style="z-index:6"'); html[-1] = html[-1].replace("z-index:4;", "z-index:6;")
S(30.7, "riser", 0.35); S(33.22, "boom", 0.6); S(33.3, "shimmer", 0.5)

# ---- S9 34.05-36.75: mandi malam sebelum tidur
full("v_shower", "assets/broll/shower.mp4", 34.05, 2.7, 1.15, 1.0)
vid("v_mo", "assets/broll/moon.mp4", 34.05, 2.7, (600, 260, 400, 400), cls="circle")
clip("s9", 34.05, 2.7, '<div class="shade" style="background:rgba(15,20,35,.30)"></div>'
     f'<div class="t kick light" style="top:820px;letter-spacing:12px">{R("y0","Sekali aku")}</div>'
     f'<div class="t light" style="top:880px;font:200 160px/1 Montserrat;letter-spacing:-4px">{R("y1","MANDI")}<br>{R("y2","MALAM")}</div>'
     f'<div class="t serif-it light" style="top:1230px;font-size:76px">{R("y3","sebelum tidur")}</div>')
rv("#y0", 34.14); rv("#y1", 34.96, 0.5); rv("#y2", 35.28, 0.5); rv("#y3", 35.68, 0.5)
sect(3, 34.05, 11.05, "RAHSIA")
S(34.96, "boom", 0.4)

# ---- S10 36.75-38.90: bau dia melekat kat kulit (real foam on ivory)
full("v_pump", "assets/broll/pump_ivory.mp4", 36.75, 2.15, 1.06, 1.0, reveal="up", media="3.2")
clip("s10", 36.75, 2.15, '<div class="shade" style="background:linear-gradient(180deg,rgba(243,238,230,.92) 0%,rgba(243,238,230,0) 24%)"></div>'
     f'<div class="t c kick" style="top:150px">{R("k0","Bau dia memang")}</div>'
     f'<div class="t c" style="top:200px;font:300 96px/1 Montserrat;letter-spacing:-2px">{R("k1","MELEKAT")}</div>'
     f'<div class="t c serif-it" style="top:310px;font-size:72px;color:var(--rose)">{R("k2","kat kulit")}</div>')
rv("#k0", 36.85); rv("#k1", 37.78, 0.5); rv("#k2", 38.3, 0.5)
S(37.0, "foam", 0.5); S(37.78, "boom", 0.4)

# ---- S11 38.90-40.95: fresh, premium, expensive
clip("bg11", 38.9, 2.05, '<div class="ivory"></div>', style="z-index:2")
vid("p_diag", "assets/product/diag_b.jpg", 38.9, 2.05, (560, 330, 430, 760), img=True)
clip("s11", 38.9, 2.05, f'<div class="t kick" style="top:330px">{R("e0","Rasa dia")}</div>'
     '<div class="t" style="top:420px;right:auto;width:470px"><div class="chip" id="e1"><i></i>FRESH</div></div>'
     '<div class="t" style="top:540px;right:auto;width:470px"><div class="chip" id="e2"><i></i>PREMIUM</div></div>'
     '<div class="t" style="top:660px;right:auto;width:470px"><div class="chip" id="e3" style="background:var(--ink);color:#f2d388"><i style="background:#f2d388"></i>EXPENSIVE</div></div>')
rv("#e0", 38.94); pop("#e1", 39.2, 0.35); pop("#e2", 39.76, 0.35); pop("#e3", 40.4, 0.4)
S(40.4, "chime", 0.45)

# ---- S12 40.95-45.10: tak payah membazir perfume mahal; tidur pun ada vibes mahal
clip("s12a", 40.95, 1.95, '<div class="ivory grid"></div>'
     f'<div class="t c kick" style="top:640px">{R("z0","Tak payah dah membazir")}</div>'
     '<div class="t c" style="top:720px"><span style="position:relative;display:inline-block;font:300 92px/1 Montserrat;letter-spacing:-2px;white-space:nowrap">'
     f'{R("z1","PERFUME MAHAL")}<i class="strike" id="z2"></i></span></div>'
     '<div class="t c" style="top:860px;font:200 200px/1 Montserrat;color:var(--rose)" id="z3">&#10005;</div>')
A('tl.fromTo("#s12a",{clipPath:"inset(0% 0% 0% 100%)"},{clipPath:"inset(0% 0% 0% 0%)",duration:0.4,ease:"expo.inOut"},40.95);')
rv("#z0", 41.32); rv("#z1", 42.38, 0.45); line("#z2", 42.6, 0.3); pop("#z3", 42.72, 0.35)
S(40.95, "whip", 0.5); S(42.6, "whip", 0.4); S(42.72, "boom", 0.4)
full("v_cdls", "assets/broll/candles.mp4", 42.9, 2.2, 1.15, 1.0)
clip("s12b", 42.9, 2.2, '<div class="shade" style="background:rgba(0,0,0,.25)"></div>'
     f'<div class="t c kick light" style="top:700px;letter-spacing:12px">{R("v0","Lepas ni tidur pun ada")}</div>'
     f'<div class="t c light" style="top:770px;font:200 170px/1 Montserrat;letter-spacing:-4px">{R("v1","VIBES")}</div>'
     f'<div class="t c serif-it" style="top:950px;font-size:130px;color:#f2d388">{R("v2","mahal")}</div>')
A('tl.fromTo("#s12b .shade",{opacity:0},{opacity:1,duration:0.3},43.15);')
rv("#v0", 43.22); rv("#v1", 44.32, 0.45); rv("#v2", 44.62, 0.45)
S(44.32, "boom", 0.45); S(44.62, "shimmer", 0.4)

# ---- S13 45.10-50.70: CTA -- tekan beg kuning sekarang, sebelum habis
clip("bg13", 45.1, 5.6, '<div class="ivory"></div>', style="z-index:2")
vid("p_cta", "assets/product/duo_wood2.jpg", 45.1, 5.6, (190, 330, 700, 800), img=True)
clip("s13", 45.1, 5.6, f'<div class="t c kick" style="top:160px">{R("c0","Geng buddy yang nak tidur")}</div>'
     f'<div class="t c serif-it" style="top:210px;font-size:64px;color:var(--rose);white-space:nowrap">{R("c1","wangi semerbak malam ni")}</div>'
     f'<div class="btn" id="btn" style="top:1190px"><div class="bk">{BASKET}</div>TEKAN BEG KUNING</div>'
     f'<div class="t c kick" style="top:1375px;color:var(--ink)">{R("c2","Sekarang")}</div>'
     '<div class="bar" style="top:1440px"><i id="cb"></i></div>'
     f'<div class="t c" style="top:1465px;font:600 24px Montserrat;letter-spacing:8px;color:var(--rose)">{R("c3","SEBELUM HABIS")}</div>')
rv("#c0", 45.2); rv("#c1", 46.7, 0.5)
A('tl.fromTo("#btn",{opacity:0,y:60},{opacity:1,y:0,duration:0.5,ease:"expo.out"},48.18);')
A('tl.to("#btn",{scale:1.06,duration:0.14,yoyo:true,repeat:5,ease:"sine.inOut"},48.9);')
rv("#c2", 49.46); rv("#c3", 49.96)
A('tl.fromTo("#cb",{scaleX:1},{scaleX:0.12,duration:1.4,ease:"power2.in"},49.96);')
sect(4, 45.1, 5.6, "TEKAN BEG KUNING")
S(48.18, "whip", 0.5); S(48.3, "pop", 0.6); S(48.9, "click", 0.6); S(49.2, "click", 0.5); S(49.96, "boom", 0.45)

# ---- S14 50.70-52.20: end card
clip("s14", 50.7, DURATION - 50.7, '<div class="ivory"></div>'
     f'<div class="t c" style="top:700px;font:600 46px Montserrat;letter-spacing:16px">{R("n0","FRESCURA BODY")}</div>'
     '<div class="hair" id="n1" style="left:390px;width:300px;top:780px"></div>'
     f'<div class="t c serif-it" style="top:830px;font-size:72px;color:var(--rose)">{R("n2","tidur wangi semerbak")}</div>'
     f'<div class="btn" id="n3" style="top:1000px;transform-origin:50% 50%"><div class="bk">{BASKET}</div>TEKAN BEG KUNING</div>')
A('tl.fromTo("#s14",{clipPath:"inset(100% 0% 0% 0%)"},{clipPath:"inset(0% 0% 0% 0%)",duration:0.45,ease:"expo.inOut"},50.7);')
rv("#n0", 50.85); line("#n1", 51.0); rv("#n2", 51.1); pop("#n3", 51.3, 0.4)
S(50.7, "whip", 0.5); S(50.85, "chime", 0.5)

# ---- scenes above are authored on the first voice cut (words_scene_timeline.json). The voice was re-cut so
# "hotel" and "expensive" are no longer clipped; map every scene/SFX time onto the new voice by matching words.
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
    if x >= _ao[-1]: return round(_an[-1] + (x - _ao[-1]), 3)
    i = max(k for k in range(len(_ao)) if _ao[k] <= x)
    return round(_an[i] + (x - _ao[i]) * (_an[i + 1] - _an[i]) / (_ao[i + 1] - _ao[i]), 3)
def _ra(m):
    st, d = float(m.group(1)), float(m.group(2))
    return f'data-start="{T(st):.3f}" data-duration="{T(st + d) - T(st):.3f}"'
html = [re.sub(r'data-start="([\d.]+)" data-duration="([\d.]+)"', _ra, h) for h in html]
js = [re.sub(r",([\d.]+)\);$", lambda m: f",{T(float(m.group(1))):.3f});", l) for l in js]
_punch = {}                                       # keep each zoom punch -> slow drift pair back-to-back after the remap
for i, l in enumerate(js):
    m = re.match(r'tl\.fromTo\("(#[\w-]+)",\{scale:[\d.]+\},\{scale:[\d.]+,duration:([\d.]+),ease:"expo\.out"\},([\d.]+)\);$', l)
    if m: _punch[m.group(1)] = float(m.group(3)) + float(m.group(2)); continue
    m = re.match(r'(tl\.to\("(#[\w-]+)",\{scale:[\d.]+,duration:)([\d.]+)(,ease:"none"\},)([\d.]+)\);$', l)
    if m and m.group(2) in _punch:
        st0 = _punch.pop(m.group(2)); end = float(m.group(5)) + float(m.group(3))
        js[i] = f"{m.group(1)}{max(end - st0, 0.1):.2f}{m.group(4)}{st0:.3f});"
for c in sfx: c["t"] = T(c["t"])
DURATION = round(T(DURATION), 2)
# ---- scene changes must fall between words, never mid-word: snap every top-level scene boundary
_SCN = re.compile(r'^(s\d+[ab]?|v_hotel|v_corr|v_shower|v_pump|v_cdls|bg\d+|v_\w+w|p_\w+w|v_bed|v_bd|v_sh|v_mn|v_wl|v_cdl|v_mo|p_\w+)$')
def _bounds():
    out = set()
    for h in html:
        m = re.search(r'id="([^"]+)"[^>]*data-start="([\d.]+)" data-duration="([\d.]+)"', h)
        if m and re.match(r'^(s\d+[ab]?|bg\d+|v_hotel|v_corr|v_shower|v_pump|v_cdls)$', m.group(1)):
            out.add(round(float(m.group(2)) + float(m.group(3)), 3))
    return out
_moves = {}
for b in sorted(_bounds()):
    mid = [w for w in words if w["s"] + 0.04 < b < w["e"] - 0.04]
    if mid and b < DURATION - 0.05:
        w = mid[0]; i = words.index(w)
        starts_sentence = i == 0 or re.search(r"[.,?!]$", words[i - 1]["w"].strip()) or w["s"] - words[i - 1]["e"] > 0.15
        if starts_sentence and b - w["s"] < 0.45:
            nb = w["s"]                                  # the new sentence begins with this word: cut just before it
        else:                                            # mid-phrase: finish the phrase, cut before the next one ("…mahal dah | Lepas ni…")
            nxt = [x for x in words[i + 1:] if re.match(r"(?i)^(lepas|so|sampailah|sekali|dulu|tak|dia|sebab|korang)\b", x["w"].strip()) and x["s"] - b < 0.4]
            nb = nxt[0]["s"] if nxt else w["e"]
        _moves[b] = round(nb, 3)
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
print("scene boundaries moved off mid-word:", _moves)
_punch = {}                                       # keep each zoom punch -> slow drift pair back-to-back after the remap
for i, l in enumerate(js):
    m = re.match(r'tl\.fromTo\("(#[\w-]+)",\{scale:[\d.]+\},\{scale:[\d.]+,duration:([\d.]+),ease:"expo\.out"\},([\d.]+)\);$', l)
    if m: _punch[m.group(1)] = float(m.group(3)) + float(m.group(2)); continue
    m = re.match(r'(tl\.to\("(#[\w-]+)",\{scale:[\d.]+,duration:)([\d.]+)(,ease:"none"\},)([\d.]+)\);$', l)
    if m and m.group(2) in _punch:
        st0 = _punch.pop(m.group(2)); end = float(m.group(5)) + float(m.group(3))
        js[i] = f"{m.group(1)}{max(end - st0, 0.1):.2f}{m.group(4)}{st0:.3f});"

# ---- the face (0.92 s, client: under 1 s) ends on a word boundary near the end of "Korang, aku ada..."
_FACE_LEN = 0.92
_fw = [w for w in words if 4.0 < w["s"] < 6.0]
_fend = min((w["s"] for w in _fw), key=lambda t: abs(t - 5.45))
for i, h in enumerate(html):
    m = re.search(r'id="(v_face|s1)"[^>]*data-start="([\d.]+)" data-duration="([\d.]+)"', h)
    if m:
        html[i] = h.replace(f'data-start="{m.group(2)}" data-duration="{m.group(3)}"', f'data-start="{_fend - _FACE_LEN:.3f}" data-duration="{_FACE_LEN:.3f}"')
    m = re.search(r'id="(v_corr|s0b)"[^>]*data-start="([\d.]+)" data-duration="([\d.]+)"', h)
    if m:
        st = float(m.group(2)); html[i] = h.replace(f'data-duration="{m.group(3)}"', f'data-duration="{_fend - _FACE_LEN - st:.3f}"')
js = [re.sub(r'^(tl\.fromTo\("#v_face",.*\},)([\d.]+)\);$', lambda q: f"{q.group(1)}{_fend - _FACE_LEN:.3f});", l) for l in js]
for c in sfx:
    if c["sfx"] == "whip" and abs(c["t"] - 4.565) < 0.2: c["t"] = round(_fend - _FACE_LEN, 3)
for i, h in enumerate(html):
    m = re.search(r'id="(s1b)"[^>]*data-start="([\d.]+)" data-duration="([\d.]+)"', h)
    if not m: continue
    st, d = float(m.group(2)), float(m.group(3)); _face_start = _fend - _FACE_LEN
    if True:                                         # kinetic PERANGAI beat takes over right when the face ends
        end = st + d; ns = _face_start + _FACE_LEN
        html[i] = h.replace(f'data-start="{m.group(2)}" data-duration="{m.group(3)}"', f'data-start="{ns:.3f}" data-duration="{end - ns:.3f}"')
        js = [re.sub(r'(tl\.fromTo\("#s1b",.*\},)([\d.]+)\);$', lambda q: f"{q.group(1)}{ns:.3f});", l) for l in js]

# ---- persistent: progress bar (hidden on the face shot)
clip("chrome", 0, DURATION, '<div id="prog"></div>', style="z-index:5")
A(f'tl.fromTo("#prog",{{scaleX:0}},{{scaleX:1,duration:{DURATION:.2f},ease:"none"}},0);')

# ---- captions (pill), after the hook and the face shot (they carry their own type) until the end card
for ci, ch in enumerate(chunks):
    st = ch[0]["s"]
    if st < 6.8 or st >= DURATION - 1.5:
        continue
    nxt = chunks[ci + 1][0]["s"] if ci + 1 < len(chunks) else DURATION - 1.5
    en = min(nxt, ch[-1]["e"] + 0.45) if nxt - ch[-1]["e"] > 0.6 else nxt
    en = min(en, DURATION - 1.5)
    sp = []
    for wi, w in enumerate(ch):
        key = re.sub(r"[^a-z\-]", "", w["t"].lower())
        sp.append(f'<span id="w{ci}_{wi}" class="w{" hl" if key in HL else ""}">{w["t"].rstrip(".,?")}</span>')
        A(f'tl.fromTo("#w{ci}_{wi}",{{opacity:0.35}},{{opacity:1,duration:0.15}},{w["s"]:.2f});')
    clip(f"cap{ci}", st, max(en - st, 0.2), '<span class="pill">' + " ".join(sp) + "</span>", cls="cap")
    A(f'tl.fromTo("#cap{ci} .pill",{{y:20,opacity:0}},{{y:0,opacity:1,duration:0.25,ease:"power3.out"}},{st:.2f});')

sfx.sort(key=lambda c: c["t"])
manual = [c for c in sfx if not c["auto"]]
kept = list(manual)
for c in (c for c in sfx if c["auto"]):           # auto cues yield to hand-placed ones and to each other
    if any(abs(c["t"] - k["t"]) < 0.07 for k in kept):
        continue
    kept.append(c)
kept.sort(key=lambda c: c["t"])
for c in kept: c.pop("auto", None)
sfx = kept
for c in sfx:                                      # quick white flash on every impact for extra energy
    if c["sfx"] == "boom":
        js.append(f'tl.fromTo("#flash",{{opacity:0.45}},{{opacity:0,duration:0.22,ease:"power2.out"}},{c["t"]:.3f});')
json.dump(sfx, open(f"{proj}/assets/audio/sfx_cues.json", "w"), indent=0)
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
print(len(chunks), "caption chunks,", len(js), "tweens,", len(sfx), "sfx cues")
