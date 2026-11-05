"""Video 4 (modern motion graphics, minimalist luxury): "Perempuan ada dua jenis" -- Bombshell vs Midnight Fantasy.
Builds project/index.html (HyperFrames + GSAP) and project/assets/audio/sfx_cues.json from the cleaned voice's word times.
Usage: python3 -I build.py PROJECT_DIR [--final]"""
import json, re, sys

proj = sys.argv[1]
FINAL = "--final" in sys.argv
DURATION = 49.0          # voice is 47.6 s + end-card tail

words = [w for s in json.load(open(f"{proj}/assets/audio/words.json")) for w in s["words"]]
FIX = {"Pempuan": "Perempuan", "Hempur": "Hang pun", "bombshell": "Bombshell", "midnight": "Midnight", "fantasi": "Fantasy",
       "luangian": "wangian", "setersendiri": "tersendiri", "diorang": "diorang"}
HL = {"bombshell", "midnight", "fantasy", "fresh", "floral", "feminine", "elegant", "classy", "keyakinan", "manis", "fruity",
      "misteri", "menggoda", "suami", "aura", "tersendiri", "wangian", "personality", "komen", "share", "dua", "jenis"}
clean = []
for w in words:
    txt = w["w"].strip()
    core = txt.rstrip(".,?"); tail = txt[len(core):]
    if core == "minat":                       # whisper hears "Midnight" as "minat"
        txt = "Midnight"
    else:
        txt = FIX.get(core, core) + tail
    if txt.startswith("-") and clean:
        clean[-1]["t"] += txt; clean[-1]["e"] = w["e"]; continue
    clean.append({"t": txt, "s": w["s"], "e": w["e"]})
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
    clip(f"sect{n}", s, d, f'<div class="sect"{c}><b{b}>0{n}</b> &nbsp;/ 05 &nbsp;&nbsp;{label}</div>', style="z-index:8")
    fade(f"#sect{n} .sect", s + 0.1, 0.5, 10)
def bubble(id_, l, tp, name, txt, v=False):
    return (f'<div class="bubble{" v" if v else ""}" id="{id_}" style="left:{l}px;top:{tp}px"><div class="av"></div>'
            f'<div><small>{name}</small><span class="tx" id="{id_}t">{txt}</span></div></div>')
RINGS = ('<svg viewBox="0 0 220 140" style="width:440px;height:280px"><circle cx="80" cy="70" r="52" fill="none" stroke="#161412" stroke-width="7"/>'
         '<circle cx="140" cy="70" r="52" fill="none" stroke="#a5162f" stroke-width="7"/><path d="M128 14 l12 -12 l12 12 l-12 10z" fill="#a5162f"/></svg>')
SHARE = ('<svg viewBox="0 0 64 64"><path d="M38 10 L58 30 L38 50 V38 C24 38 14 42 6 54 C8 36 18 24 38 22 Z" fill="#161412"/></svg>')

# ---- S0 0.00-2.11: "Perempuan ada dua jenis" -- kinetic type + the two bottles (visual hook)
FACE0, FACE1 = 2.11, 2.97
clip("bg1", 0, FACE0, '<div class="ivory grid"></div>', style="z-index:2")
vid("p_duo", "assets/product/duo_white.jpg", 0.55, FACE0 - 0.55, (240, 560, 600, 1066), img=True)
clip("s1", 0, FACE0, f'<div class="t c" style="top:230px;font:200 132px/1 Montserrat;letter-spacing:-3px">{R("d0","PEREMPUAN")}</div>'
     f'<div class="t c serif-it" style="top:370px;font-size:96px;color:var(--rose)">{R("d1","ada 2 jenis")}</div>'
     '<div class="lbl v" id="d2" style="left:150px;top:1440px">MIDNIGHT FANTASY</div>'
     '<div class="lbl r" id="d3" style="left:640px;top:1440px">BOMBSHELL</div>')
rv("#d0", 0.02, 0.6); rv("#d1", 0.8, 0.6); pop("#d2", 1.45, 0.45); pop("#d3", 1.6, 0.45)
S(0.0, "boom", 0.5); S(0.02, "swoosh", 0.4); S(0.55, "swoosh", 0.4); S(0.8, "tick", 0.45); S(1.2, "pop", 0.45); S(1.45, "pop", 0.4); S(1.6, "pop", 0.4)

# ---- S2 2.11-2.97: the only face shot (0.86 s) -- "Hang pun geng mana?", pointing at the viewer, then into the lens
html.append(f'<video id="v_face" class="clip bg" src="assets/broll/face.mp4" data-start="{FACE0}" data-duration="{FACE1-FACE0:.2f}" data-media-start="0" muted playsinline style="z-index:6"></video>')
A(f'tl.fromTo("#v_face",{{scale:1.08}},{{scale:1.0,duration:{FACE1-FACE0:.2f},ease:"power2.out"}},{FACE0});')
A(f'tl.fromTo("#v_face",{{clipPath:"inset(0% 0% 0% 100%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:0.25,ease:"expo.out"}},{FACE0});')
clip("s2", FACE0, FACE1 - FACE0, '<div class="shade" style="background:linear-gradient(180deg,rgba(0,0,0,0) 55%,rgba(0,0,0,.6) 100%)"></div>'
     f'<div class="t c" style="top:1300px;font:200 150px/1 Montserrat;color:#fff;letter-spacing:-4px">{R("g1","GENG")}</div>'
     f'<div class="t c serif-it" style="top:1450px;color:#fff;font-size:110px">{R("g2","mana?")}</div>', style="z-index:7")
rv("#g1", 2.42, 0.45); rv("#g2", 2.62, 0.45)
S(2.11, "swoosh", 0.5); S(2.42, "tick", 0.5); S(2.62, "pop", 0.5)

# ---- S3 3.00-4.70: No. 01 Bombshell
clip("bg3", 3.0, 1.7, '<div class="ivory"></div>', style="z-index:2")
vid("p_g", "assets/product/glory_card.jpg", 3.0, 1.7, (560, 420, 430, 1100), img=True)
clip("s3", 3.0, 1.7, f'<div class="t kick" style="top:300px">{R("a0","Pertama · No. 01")}</div>'
     f'<div class="t kick" style="top:820px;right:auto;width:450px">{R("a1","Geng")}</div>'
     f'<div class="t" style="top:870px;right:auto;width:470px;font:300 92px/1 Montserrat;letter-spacing:-2px;color:var(--rose)">{R("a2","BOMB")}<br>{R("a3","SHELL")}</div>'
     f'<div class="t serif-it" style="top:1090px;right:auto;width:450px;font-size:54px;color:var(--mute)">{R("a4","Woman Glory")}</div>'
     '<div class="hair" id="a5" style="left:90px;width:380px;top:1180px"></div>')
rv("#a0", 3.05); rv("#a1", 3.72); rv("#a2", 4.0, 0.6); rv("#a3", 4.08, 0.6); rv("#a4", 4.3); line("#a5", 4.3)
sect(1, 3.0, 8.45, "BOMBSHELL")
S(3.0, "swoosh", 0.5); S(4.0, "boom", 0.55); S(4.3, "tick", 0.4)

# ---- S4 4.70-8.30: fresh, floral, feminine, elegant
clip("bg4", 4.7, 3.6, '<div class="ivory"></div>', style="z-index:2")
vid("v_rose", "assets/broll/rose.mp4", 4.7, 3.6, (90, 230, 900, 1000))
vid("v_prose", "assets/broll/pinkrose.mp4", 4.7, 3.6, (600, 960, 400, 400), cls="circle", z0=1.3)
clip("s4", 4.7, 3.6, f'<div class="t kick" style="top:150px">{R("r0","Suka bau")}</div>'
     '<div class="ring" id="r9" style="left:580px;top:940px;width:440px;height:440px"></div>'
     '<div class="t" style="top:1290px;right:auto;width:900px"><div class="chip" id="r1"><i></i>FRESH</div><div class="chip" id="r2"><i></i>FLORAL</div></div>'
     '<div class="t" style="top:1390px;right:auto;width:900px"><div class="chip" id="r3"><i></i>FEMININE</div><div class="chip" id="r4"><i></i>ELEGANT</div></div>')
rv("#r0", 4.75); A('tl.fromTo("#r9",{scale:0.6,opacity:0},{scale:1,opacity:1,duration:0.8,ease:"expo.out"},5.0);')
for k, tt in (("r1", 5.36), ("r2", 6.08), ("r3", 6.86), ("r4", 7.62)):
    fade(f"#{k}", tt, 0.5, 0, -30); S(tt, "pop", 0.45)
S(4.7, "swoosh", 0.5); S(7.62, "chime", 0.35)

# ---- S5 8.30-11.45: classy & penuh keyakinan
clip("bg5", 8.3, 3.15, '<div class="ivory"></div>', style="z-index:2")
vid("v_hj", "assets/broll/hijab.mp4", 8.3, 3.15, (90, 230, 900, 1150))
clip("s5", 8.3, 3.15, '<div class="shade" style="inset:auto;left:90px;top:900px;width:900px;height:480px;border-radius:0 0 44px 44px;'
     'background:linear-gradient(180deg,rgba(0,0,0,0),rgba(0,0,0,.55))"></div>'
     f'<div class="t kick" style="top:150px">{R("c0","Jenis yang suka nampak")}</div>'
     f'<div class="t" style="top:1060px;left:150px;font:200 150px/1 Montserrat;letter-spacing:-4px;color:#fff">{R("c1","CLASSY")}</div>'
     f'<div class="t serif-it" style="top:1225px;left:150px;font-size:66px;color:#fff">{R("c2","&amp; penuh keyakinan")}</div>')
rv("#c0", 8.35); rv("#c1", 9.36, 0.6); rv("#c2", 10.46, 0.7)
S(8.3, "swoosh", 0.5); S(9.36, "boom", 0.45); S(10.46, "chime", 0.4)

# ---- S6 11.45-13.70: No. 02 Midnight Fantasy (night palette)
clip("bg6", 11.45, 2.25, '<div class="shade" style="background:radial-gradient(ellipse at 30% 30%,#3a2d78 0%,#1c1638 60%,#0e0b1d 100%)"></div>', style="z-index:2")
A('tl.fromTo("#bg6",{clipPath:"inset(0% 0% 100% 0%)"},{clipPath:"inset(0% 0% 0% 0%)",duration:0.6,ease:"expo.inOut"},11.45);')
vid("p_n", "assets/product/noche_card.jpg", 11.45, 2.25, (560, 420, 420, 1107), img=True)
clip("s6", 11.45, 2.25, f'<div class="t kick" style="top:300px;color:rgba(255,255,255,.7)">{R("n0","Team kedua · No. 02")}</div>'
     f'<div class="t kick" style="top:820px;right:auto;width:450px;color:rgba(255,255,255,.7)">{R("n1","Geng")}</div>'
     f'<div class="t" style="top:870px;right:auto;width:470px;font:300 80px/1.02 Montserrat;letter-spacing:-1px;color:#fff">{R("n2","MIDNIGHT")}<br>{R("n3","FANTASY")}</div>'
     f'<div class="t serif-it" style="top:1070px;right:auto;width:450px;font-size:54px;color:#b9a8ff">{R("n4","Noche")}</div>'
     '<div class="hair" id="n5" style="left:90px;width:380px;top:1160px;background:#fff"></div>')
rv("#n0", 11.55); rv("#n1", 12.28); rv("#n2", 12.8, 0.6); rv("#n3", 12.9, 0.6); rv("#n4", 13.15); line("#n5", 13.15)
sect(2, 11.45, 12.0, "MIDNIGHT FANTASY", light=True)
S(11.45, "swoosh", 0.55); S(12.8, "boom", 0.55); S(13.15, "shimmer", 0.4)

# ---- S7a 13.70-17.55: manis, fruity
clip("bg7", 13.7, 3.85, '<div class="ivory"></div>', style="z-index:2")
vid("v_st", "assets/broll/straw.mp4", 13.7, 3.85, (160, 330, 760, 760), cls="circle")
clip("s7", 13.7, 3.85, f'<div class="t c kick" style="top:180px">{R("m0","Diorang suka bau yang")}</div>'
     '<div class="ring" id="m9" style="left:120px;top:290px;width:840px;height:840px"></div>'
     '<div class="t c" style="top:1210px"><div class="chip v" id="m1"><i></i>MANIS</div><div class="chip v" id="m2"><i></i>FRUITY</div></div>')
rv("#m0", 14.5); A('tl.fromTo("#m9",{scale:0.7,opacity:0},{scale:1,opacity:1,duration:0.9,ease:"expo.out"},13.8);')
fade("#m1", 15.44, 0.5, 30); fade("#m2", 16.38, 0.5, 30)
S(13.7, "swoosh", 0.5); S(15.44, "pop", 0.5); S(16.38, "pop", 0.5)

# ---- S7b 17.55-18.95: agak misteri
full("v_moon", "assets/broll/moon.mp4", 17.55, 1.4, 1.15, 1.0)
clip("s7b", 17.55, 1.4, '<div class="shade" style="background:rgba(8,6,20,.35)"></div>'
     f'<div class="t c kick" style="top:700px;color:rgba(255,255,255,.75);letter-spacing:14px">{R("y0","Agak")}</div>'
     f'<div class="t c" style="top:760px;font:200 170px/1 Montserrat;letter-spacing:-4px;color:#fff" id="y1">MISTERI</div>')
rv("#y0", 17.45 + 0.15)
A('tl.fromTo("#y1",{opacity:0,filter:"blur(24px)",scale:1.25},{opacity:1,filter:"blur(0px)",scale:1,duration:0.9,ease:"expo.out"},17.8);')
S(17.55, "swoosh", 0.4); S(17.8, "boom", 0.5); S(17.9, "shimmer", 0.35)

# ---- S8 18.95-21.50: paling penting... menggoda
clip("bg8", 18.95, 2.55, '<div class="ivory"></div>', style="z-index:2")
vid("v_ht", "assets/broll/hearts.mp4", 18.95, 2.55, (190, 420, 700, 700), cls="circle")
clip("s8", 18.95, 2.55, f'<div class="t c kick" style="top:230px">{R("h1","Dan yang paling penting")}</div>'
     '<div class="ring" id="h2" style="left:150px;top:380px;width:780px;height:780px"></div>'
     f'<div class="t c serif-it" style="top:1190px;font-size:150px;color:var(--rose)">{R("h3","Menggoda")}</div>')
rv("#h1", 19.05); A('tl.fromTo("#h2",{scale:0.6,opacity:0},{scale:1,opacity:1,duration:0.9,ease:"expo.out"},19.0);'); rv("#h3", 20.68, 0.7)
S(18.95, "swoosh", 0.5); S(19.3, "riser", 0.3); S(20.68, "boom", 0.55)

# ---- S9 21.50-23.40: "tapi goda suami je lah"
clip("s9", 21.5, 1.9, '<div class="ivory"></div>'
     f'<div class="t c kick" style="top:420px">{R("j0","Tapi...")}</div>'
     '<div id="j1" style="position:absolute;left:320px;top:560px">' + RINGS + '</div>'
     f'<div class="t c" style="top:930px;font:300 128px/1 Montserrat;letter-spacing:-3px">{R("j2","SUAMI JE")}</div>'
     f'<div class="t c serif-it" style="top:1080px;font-size:80px;color:var(--rose)">{R("j3","tau!")}</div>')
A('tl.fromTo("#s9",{clipPath:"inset(0% 0% 0% 100%)"},{clipPath:"inset(0% 0% 0% 0%)",duration:0.45,ease:"expo.inOut"},21.5);')
rv("#j0", 21.6); pop("#j1", 22.32, 0.6); rv("#j2", 22.48, 0.6); rv("#j3", 23.0)
A('tl.to("#j1",{rotation:-6,duration:0.12,yoyo:true,repeat:3,ease:"sine.inOut"},22.95);')
S(21.5, "swoosh", 0.5); S(22.32, "pop", 0.55); S(22.48, "chime", 0.45); S(23.0, "tick", 0.5)

# ---- S10 23.40-25.25: aura tersendiri
full("v_lav", "assets/broll/lavender.mp4", 23.4, 1.85, 1.12, 1.0)
clip("s10", 23.4, 1.85, '<div class="shade" style="background:rgba(30,22,60,.30)"></div>'
     '<div class="glow" id="u0" style="left:240px;top:560px;width:600px;height:600px"></div>'
     '<div class="glow" id="u1" style="left:140px;top:460px;width:800px;height:800px;opacity:.5"></div>'
     f'<div class="t c" style="top:740px;font:200 190px/1 Montserrat;letter-spacing:-4px;color:#fff">{R("u2","AURA")}</div>'
     f'<div class="t c serif-it" style="top:950px;font-size:76px;color:#fff">{R("u3","tersendiri")}</div>')
A('tl.fromTo("#u0,#u1",{scale:0.5,opacity:0},{scale:1,opacity:1,duration:1.2,stagger:0.15,ease:"expo.out"},23.45);')
A('tl.to("#u0",{scale:1.06,duration:0.6,yoyo:true,repeat:2,ease:"sine.inOut"},24.6);')
rv("#u2", 24.18, 0.6); rv("#u3", 24.5, 0.7)
S(23.4, "swoosh", 0.45); S(23.5, "shimmer", 0.45); S(24.18, "boom", 0.45)

# ---- S11a 25.25-27.30: "Tapi aku nak tahu" -- real foaming pump on an ivory studio backdrop
full("v_pump", "assets/broll/pump_ivory.mp4", 25.25, 2.05, 1.06, 1.0, reveal="up", media="3.4")
clip("s11a", 25.25, 2.05, '<div class="shade" style="background:linear-gradient(180deg,rgba(243,238,230,.92) 0%,rgba(243,238,230,0) 22%)"></div>'
     f'<div class="t c kick" style="top:150px">{R("q0","Tapi aku nak tahu")}</div>'
     f'<div class="t c serif-it" style="top:205px;font-size:84px">{R("q1","betulkah...")}</div>')
rv("#q0", 25.35); rv("#q1", 26.36, 0.6)
S(25.25, "swoosh", 0.5); S(25.6, "foam", 0.5); S(26.36, "tick", 0.45)
sect(3, 25.25, 6.35, "PERSONALITI")

# ---- S11b 27.30-31.60: wangian = personality? (educational card)
clip("bg11", 27.3, 4.3, '<div class="ivory grid"></div>', style="z-index:2")
vid("v_pf", "assets/broll/perfume.mp4", 27.3, 4.3, (620, 1150, 360, 360), cls="circle")
clip("s11b", 27.3, 4.3, f'<div class="t kick" style="top:260px">{R("e0","Pilihan")}</div>'
     f'<div class="t big" style="top:310px">{R("e1","WANGIAN")}</div>'
     f'<div class="t" style="top:440px;font:200 120px/1 Montserrat">{R("e2","=")}</div>'
     f'<div class="t big accent" style="top:580px">{R("e3","PERSONALITI")}<span style="font-family:Playfair;font-style:italic">{R("e3b","?")}</span></div>'
     '<div class="hair" id="e4" style="left:90px;width:900px;top:790px"></div>'
     '<div class="row2" id="e5" style="top:880px"><div class="nm" style="color:var(--rose)">BOMBSHELL</div><div class="ar"></div><div class="tr">classy · yakin</div></div>'
     '<div class="row2" id="e6" style="top:990px"><div class="nm" style="color:var(--violet)">MIDNIGHT FANTASY</div><div class="ar"></div><div class="tr">misteri · aura</div></div>'
     '<div class="hair" id="e7" style="left:90px;width:900px;top:1100px;opacity:.4"></div>')
rv("#e0", 27.34); rv("#e1", 27.84, 0.6); rv("#e2", 28.6); rv("#e3", 30.04, 0.6); rv("#e3b", 30.5, 0.4); line("#e4", 29.3, 1.0)
fade("#e5", 30.85, 0.6, 0, -30); fade("#e6", 31.1, 0.6, 0, -30); line("#e5 .ar", 30.95, 0.4); line("#e6 .ar", 31.2, 0.4); line("#e7", 31.2)
S(27.3, "swoosh", 0.5); S(27.84, "tick", 0.5); S(28.6, "tick", 0.45); S(30.04, "boom", 0.5); S(30.5, "pop", 0.45); S(30.85, "click", 0.5); S(31.1, "click", 0.5)

# ---- S12 31.60-35.55: komen Bombshell
clip("bg12", 31.6, 3.95, '<div class="ivory"></div>', style="z-index:2")
vid("v_ph", "assets/broll/phone.mp4", 31.6, 3.95, (90, 260, 900, 1150))
clip("s12", 31.6, 3.95, f'<div class="t kick" style="top:160px">{R("o0","Korang jangan malu-malu")}</div>'
     + bubble("o1", 150, 1000, "GENG MANA?", "Bombshell!") +
     '<div class="lbl r" id="o2" style="left:150px;top:880px">KOMEN SEKARANG</div>')
rv("#o0", 31.7); pop("#o2", 32.8, 0.45); fade("#o1", 34.4, 0.45, 30); typed("#o1t", 34.7, 0.5, 10)
sect(4, 31.6, 9.5, "KOMEN")
S(31.6, "swoosh", 0.5); S(32.8, "pop", 0.45); S(34.4, "pop", 0.5); S(34.75, "click", 0.4); S(34.95, "click", 0.35); S(35.2, "chime", 0.35)

# ---- S13 35.55-39.90: komen Midnight Fantasy (night)
full("v_sky", "assets/broll/stars.mp4", 35.55, 4.35, 1.1, 1.0, reveal="up")
vid("v_ty", "assets/broll/typing.mp4", 35.55, 4.35, (140, 330, 800, 800), cls="circle")
clip("s13", 35.55, 4.35, f'<div class="t c kick" style="top:200px;color:rgba(255,255,255,.75)">{R("i0","Yang mana geng")}</div>'
     '<div class="glow" id="i9" style="left:110px;top:300px;width:860px;height:860px;opacity:.6"></div>'
     + bubble("i1", 170, 1180, "GENG MANA?", "Midnight Fantasy!", v=True) +
     f'<div class="t c" style="top:1340px;font:300 64px/1.1 Montserrat;letter-spacing:2px;color:#fff">{R("i2","MIDNIGHT FANTASY?")}</div>')
rv("#i0", 35.65); A('tl.fromTo("#i9",{scale:0.7,opacity:0},{scale:1,opacity:.6,duration:0.9,ease:"expo.out"},35.7);'); rv("#i2", 36.58, 0.6)
fade("#i1", 38.16, 0.45, 30); typed("#i1t", 38.5, 0.7, 16)
S(35.55, "swoosh", 0.5); S(36.58, "boom", 0.45); S(38.16, "pop", 0.5); S(38.55, "click", 0.35); S(38.8, "click", 0.35); S(39.05, "click", 0.35); S(39.3, "chime", 0.35)

# ---- S14 39.90-41.10: tolong share
full("v_bub", "assets/broll/bubbles.mp4", 39.9, 1.2, 1.1, 1.0)
clip("s14", 39.9, 1.2, f'<div class="t c kick light" style="top:640px;letter-spacing:12px">{R("x0","Tolong")}</div>'
     f'<div class="sharebtn" id="x1" style="top:760px">{SHARE}SHARE</div>'
     '<div class="tap" id="x2" style="left:740px;top:850px"></div>'
     f'<div class="t c serif-it light" style="top:990px;font-size:72px">{R("x3","video ni")}</div>')
rv("#x0", 39.95); pop("#x1", 40.3, 0.45); rv("#x3", 40.48)
A('tl.fromTo("#x2",{opacity:0,scale:1.5},{opacity:1,scale:1,duration:0.25},40.6);')
A('tl.to("#x1",{scale:0.94,duration:0.1,yoyo:true,repeat:1,ease:"sine.inOut"},40.78);')
S(39.9, "swoosh", 0.5); S(40.3, "pop", 0.55); S(40.78, "click", 0.7); S(40.85, "chime", 0.4)

# ---- S15 41.10-47.40: tanya kawan-kawan -- poll on the real product photo
full("ph_poll", "assets/product/duo_wood_rl.jpg", 41.1, DURATION - 41.1, 1.08, 1.0, tag="img")
clip("s15", 41.1, 6.3, '<div class="shade" style="background:linear-gradient(180deg,rgba(243,238,230,.95) 0%,rgba(243,238,230,0) 20%)"></div>'
     f'<div class="t c kick" style="top:140px">{R("z0","Cuba tanya kawan-kawan")}</div>'
     f'<div class="t c serif-it" style="top:195px;font-size:80px">{R("z1","geng mana?")}</div>'
     '<div class="sel" id="zA" style="left:150px;top:380px;width:400px;height:1100px"></div>'
     '<div class="sel" id="zB" style="left:550px;top:380px;width:400px;height:1100px"></div>'
     '<div class="lbl r" id="zA2" style="left:205px;top:1400px">BOMBSHELL</div>'
     '<div class="lbl v" id="zB2" style="left:570px;top:1400px">MIDNIGHT FANTASY</div>'
     '<div class="tap" id="ztap" style="left:330px;top:1300px"></div>')
rv("#z0", 41.2); rv("#z1", 42.18, 0.7)
A('tl.fromTo("#ztap",{opacity:0,scale:1.4},{opacity:1,scale:1,duration:0.3},43.6);')
A('tl.fromTo("#zA",{opacity:0,scale:1.06},{opacity:1,scale:1,duration:0.35,ease:"back.out(2)"},44.1);'); pop("#zA2", 44.15, 0.45)
A('tl.to("#ztap",{x:400,duration:0.5,ease:"power2.inOut"},45.6);')
A('tl.to("#zA",{opacity:0.25,duration:0.3},46.3);')
A('tl.fromTo("#zB",{opacity:0,scale:1.06},{opacity:1,scale:1,duration:0.35,ease:"back.out(2)"},46.42);'); pop("#zB2", 46.47, 0.45)
sect(5, 41.1, 6.3, "TANYA KAWAN")
S(41.1, "swoosh", 0.5); S(43.6, "tick", 0.4); S(44.1, "click", 0.7); S(44.15, "pop", 0.45); S(45.6, "swoosh", 0.3); S(46.42, "click", 0.7); S(46.47, "pop", 0.45)

# ---- S16 47.40-49.00: end card
clip("s16", 47.4, DURATION - 47.4, '<div class="ivory"></div>'
     f'<div class="t c" style="top:560px;font:600 46px Montserrat;letter-spacing:16px">{R("f0","FRESCURA BODY")}</div>'
     '<div class="hair" id="f1" style="left:390px;width:300px;top:640px"></div>'
     f'<div class="t c kick" style="top:740px">{R("f2","Komen di bawah")}</div>'
     '<div class="t c" style="top:820px"><div class="chip" id="f3"><i></i>BOMBSHELL</div></div>'
     f'<div class="t c serif-it" style="top:930px;font-size:60px;color:var(--mute)">{R("f4","atau")}</div>'
     '<div class="t c" style="top:1030px"><div class="chip v" id="f5"><i></i>MIDNIGHT FANTASY</div></div>'
     f'<div class="t c" style="top:1200px;font:italic 500 40px Playfair;color:var(--mute)">{R("f6","Woman Glory · Noche")}</div>')
A('tl.fromTo("#s16",{clipPath:"inset(100% 0% 0% 0%)"},{clipPath:"inset(0% 0% 0% 0%)",duration:0.6,ease:"expo.inOut"},47.4);')
rv("#f0", 47.6); line("#f1", 47.8); rv("#f2", 47.9); pop("#f3", 48.05, 0.45); rv("#f4", 48.2); pop("#f5", 48.3, 0.45); rv("#f6", 48.45)
S(47.4, "swoosh", 0.55); S(47.6, "chime", 0.5); S(48.05, "pop", 0.45); S(48.3, "pop", 0.45)

# ---- persistent: progress bar (hidden on the face shot)
clip("chrome", 0, DURATION, '<div id="prog"></div>', style="z-index:5")
A(f'tl.fromTo("#prog",{{scaleX:0}},{{scaleX:1,duration:{DURATION:.2f},ease:"none"}},0);')

# ---- captions (pill), from 3.0 s (face, hook and question carry their own type) until the end card
for ci, ch in enumerate(chunks):
    st = ch[0]["s"]
    if st < 2.95 or st >= 47.4 or 25.25 <= st < 27.3:
        continue
    nxt = chunks[ci + 1][0]["s"] if ci + 1 < len(chunks) else 47.4
    en = min(nxt, ch[-1]["e"] + 0.45) if nxt - ch[-1]["e"] > 0.6 else nxt
    en = min(en, 47.4)
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
open(f"{proj}/index.html", "w").write(page)
print(len(chunks), "caption chunks,", len(js), "tweens,", len(sfx), "sfx cues")
