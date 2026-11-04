"""Build hf/project/index.html (HyperFrames composition) for the body-wash awareness edit.

Usage: python3 -I build_composition.py PROJECT_DIR [--final]
Reads PROJECT_DIR/assets/audio/words.json (word timestamps of the edited voice track).
Without --final a small PREVIEW tag is drawn on the frame.
"""
import json, random, re, sys

proj = sys.argv[1]
FINAL = "--final" in sys.argv

# ------------------------------------------------------------------ config
BRAND = "FRESCURA BODY"
IMG_HERO = "assets/product/hero_foam.jpg"      # bottle + pink foam on hand, dark backdrop
IMG_DUO_WOOD = "assets/product/duo_wood.jpg"
IMG_DUO_MARBLE = "assets/product/duo_marble.jpg"
IMG_DUO_DIAG = "assets/product/duo_diag.jpg"
IMG_GLORY = "assets/product/glory_card.jpg"
IMG_NOCHE = "assets/product/noche_card.jpg"
SCENT_A = "WOMAN GLORY"
SCENT_B = "NOCHE"

# Scene times below are authored on the voice timeline BEFORE pause-tightening;
# T() maps them onto the final voice (remap.json = removed intervals).
REMOVED = json.load(open(f"{proj}/assets/audio/remap.json"))
def T(x):
    out = x
    for a, b in REMOVED:
        if x >= b: out -= (b - a)
        elif x > a: out -= (x - a)
    return round(out, 3)
DURATION = T(62.4)

words = [w for s in json.load(open(f"{proj}/assets/audio/words.json")) for w in s["words"]]

# Caption text fixes (whisper mishearings) and words to hide until confirmed.
FIX = {"Atang": "Antara", "perfum": "perfume", "perfum.": "perfume.", "makmadi": "makmal",
       "makmah": "makmal", "favorite": "favourite", "favorite,": "favourite,", "noceh.": "Noche.",
       "noceh": "Noche", "noce": "Noche", "sendirilah.": "sendiri.", "tak?": "tau.",
       "fresh": "Frescura", "bodi.": "Body.", "korang?": "korang."}
HIDE = {"di", "keedah", "bayu.", "kurwa"}   # unclear lab-test wording; "kurwa" folded into brand
HIDE_AT = {(45.4, 46.9), (51.5, 52.4)}       # only hide inside these windows (final timeline)
FIX_AT = {"fresh": (51.4, 52.0)}             # "fresh" -> "Frescura" only at the brand mention
HL = {"perfume", "mewah", "foaming", "lembut", "gebu-gebu", "tekan", "buih", "dua", "woman",
      "glory", "noche", "fresh", "frescura", "body", "floral", "feminine", "sweet", "fruity", "paraben", "berbahaya",
      "ujian", "makmal", "istimewa", "try", "beg", "kuning", "check", "out", "terhad", "banyak",
      "favourite", "cepat", "gel", "buku", "wangian"}

def hidden(w):
    return w["w"].strip() in HIDE and any(a <= w["s"] <= b for a, b in HIDE_AT)

clean = []
for w in words:
    if hidden(w):
        continue
    txt = w["w"].strip()
    if txt in FIX_AT and not (FIX_AT[txt][0] <= w["s"] <= FIX_AT[txt][1]):
        pass
    else:
        txt = FIX.get(txt, txt)
    if txt.startswith("-") and clean:          # "gebu" + "-gebu" -> one word
        clean[-1]["t"] += txt; clean[-1]["e"] = w["e"]; continue
    clean.append({"t": txt, "s": w["s"], "e": w["e"]})

chunks, cur = [], []
for i, w in enumerate(clean):
    cur.append(w)
    nxt = clean[i + 1] if i + 1 < len(clean) else None
    brk = (len(cur) >= 3 or re.search(r"[.,?!]$", w["t"]) or nxt is None
           or nxt["s"] - w["e"] > 0.3 or len(" ".join(x["t"] for x in cur)) > 16)
    if brk:
        chunks.append(cur); cur = []

# ------------------------------------------------------------------ helpers
html, js = [], []
def A(line): js.append(line)
def clip(id_, start, dur, inner="", cls="", style="", tag="div"):
    html.append(f'<{tag} id="{id_}" class="clip {cls}" data-start="{start:.3f}" '
                f'data-duration="{dur:.3f}" style="{style}">{inner}</{tag}>')
def video(id_, src, start, dur, cls="bg", push=True, enter="zoom"):
    html.append(f'<video id="{id_}" class="clip {cls}" src="{src}" data-start="{start:.3f}" '
                f'data-duration="{dur:.3f}" data-media-start="0" muted playsinline></video>')
    if enter == "zoom":
        A(f'tl.fromTo("#{id_}",{{scale:1.22}},{{scale:1.04,duration:0.45,ease:"power3.out"}},{start});')
    if push:
        A(f'tl.to("#{id_}",{{scale:1.12,duration:{max(dur-0.45,0.1):.2f},ease:"none"}},{start+0.45:.2f});')
    flash(start)

_seen = set()
def IR(sel):
    """immediateRender:false for every fromTo on a target except the first one."""
    if sel in _seen:
        return ",immediateRender:false"
    _seen.add(sel); return ""
def flash(t, strength=0.55):
    A(f'tl.fromTo("#flash",{{opacity:{strength}}},{{opacity:0,duration:0.22,ease:"power2.out"{IR("#flash")}}},{t:.2f});')

def pop(sel, t, from_scale=0.2, rot=0, dur=0.45, ease="back.out(2.2)"):
    A(f'tl.fromTo("{sel}",{{scale:{from_scale},opacity:0,rotation:{rot}}},'
      f'{{scale:1,opacity:1,rotation:0,duration:{dur},ease:"{ease}"}},{t:.2f});')
def slide(sel, t, x=0, y=80, dur=0.45):
    A(f'tl.fromTo("{sel}",{{x:{x},y:{y},opacity:0}},{{x:0,y:0,opacity:1,duration:{dur},ease:"power3.out"}},{t:.2f});')
def slam(sel, t):
    A(f'tl.fromTo("{sel}",{{scale:2.6,opacity:0}},{{scale:1,opacity:1,duration:0.32,ease:"power4.in"}},{t:.2f});')
    A(f'tl.fromTo("#root",{{x:-14,y:8}},{{x:0,y:0,duration:0.25,ease:"elastic.out(1,0.3)"{IR("#root")}}},{t+0.32:.2f});')

SVG_X = ('<svg viewBox="0 0 100 100" class="xmark"><path d="M18 18 L82 82 M82 18 L18 82" '
         'stroke="#ff2a3d" stroke-width="16" stroke-linecap="round" fill="none"/></svg>')
SVG_CHECK = ('<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" fill="#1fbf6a"/>'
             '<path d="M28 52 L44 68 L74 34" stroke="#fff" stroke-width="11" fill="none" '
             'stroke-linecap="round" stroke-linejoin="round"/></svg>')
SVG_STAR = ('<svg viewBox="0 0 100 100"><path d="M50 0 C55 38 62 45 100 50 C62 55 55 62 50 100 '
            'C45 62 38 55 0 50 C38 45 45 38 50 0Z" fill="#fff6c9"/></svg>')
SVG_BASKET = ('<svg viewBox="0 0 120 110"><path d="M38 40 L52 10 M82 40 L68 10" stroke="#3a2a00" '
              'stroke-width="8" stroke-linecap="round"/><path d="M8 40 H112 L100 100 H20 Z" '
              'fill="#3a2a00"/><path d="M42 56 V86 M60 56 V86 M78 56 V86" stroke="#ffd23f" '
              'stroke-width="7" stroke-linecap="round"/></svg>')

def sparkles(prefix, t, n, area, seed):
    r = random.Random(seed)
    x0, y0, x1, y1 = area
    for i in range(n):
        x, y, s = r.uniform(x0, x1), r.uniform(y0, y1), r.uniform(40, 110)
        html.append(f'<div id="{prefix}{i}" class="spark" style="left:{x:.0f}px;top:{y:.0f}px;'
                    f'width:{s:.0f}px;height:{s:.0f}px">{SVG_STAR}</div>')
        d = t + i * 0.06
        A(f'tl.fromTo("#{prefix}{i}",{{scale:0,opacity:1,rotation:0}},{{scale:1,rotation:90,'
          f'duration:0.35,ease:"back.out(3)"}},{d:.2f});')
        A(f'tl.to("#{prefix}{i}",{{scale:0,opacity:0,duration:0.3}},{d+0.45:.2f});')

def rising_bubbles(prefix, start, dur, n, seed, color="rgba(255,255,255,0.55)"):
    r = random.Random(seed)
    out = []
    for i in range(n):
        x, s = r.uniform(-40, 1080), r.uniform(30, 150)
        delay = r.uniform(0, dur * 0.6); speed = r.uniform(1.6, 3.2)
        out.append(f'<div id="{prefix}{i}" class="bub" style="left:{x:.0f}px;width:{s:.0f}px;'
                   f'height:{s:.0f}px;border-color:{color}"></div>')
        A(f'tl.fromTo("#{prefix}{i}",{{y:2050,x:0}},{{y:-200,x:{r.uniform(-120,120):.0f},'
          f'duration:{speed:.2f},ease:"none"}},{start+delay:.2f});')
    return "".join(out)

def product_card(id_, w, src=IMG_HERO, ratio=16/9):
    return (f'<div id="{id_}" class="prod" style="width:{w}px;height:{w*ratio:.0f}px">'
            f'<img src="{src}" alt=""></div>')
def photo(id_, src, start, dur, z0=1.18, z1=1.04, pos="50% 50%"):
    """Full-frame product photo with a slow Ken Burns push."""
    html.append(f'<img id="{id_}" class="clip bg" src="{src}" data-start="{start:.3f}" '
                f'data-duration="{dur:.3f}" style="object-position:{pos}" alt="">')
    A(f'tl.fromTo("#{id_}",{{scale:{z0}}},{{scale:{z1},duration:{dur:.2f},ease:"power1.out"}},{start});')
    flash(start)

# ------------------------------------------------------------------ scenes
# S0  0.00-2.51  hook on the hero product shot (no face)
photo("ph_hero", IMG_HERO, 0.0, 2.51, 1.3, 1.05, "50% 40%")
clip("s0", 0.0, 2.51, '<div class="shade"></div><div class="hook"><div id="h0a" class="hk1">SABUN MANDI</div>'
     '<div id="h0b" class="hk2">BAU MACAM</div><div id="h0c" class="hk3">PERFUME MEWAH?!</div></div>')
slam("#h0a", 0.05); slam("#h0b", 0.55); slam("#h0c", 1.05)
sparkles("sp0_", 1.75, 6, (120, 260, 960, 760), 1)

# S1  2.51-4.46  the only 2 s of face: talking to camera with the bottle
video("v_face", "assets/broll/face.mp4", 2.51, 1.95, enter="none", push=False)
A('tl.fromTo("#v_face",{scale:1.12},{scale:1.0,duration:1.95,ease:"power2.out"},2.51);')
clip("s1", 2.51, 1.95, f'<div id="t1" class="tag" style="top:250px">{BRAND}</div>')
pop("#t1", 2.7)

# S2  4.46-6.45  "keluar gel ataupun sabun buku"
video("v_gel", "assets/broll/gel.mp4", 4.46, 1.0)
clip("s2a", 4.46, 1.0, '<div id="c2a" class="chip" style="top:620px">SABUN GEL</div>'
     f'<div id="x2a" class="xwrap" style="top:430px">{SVG_X}</div>')
pop("#c2a", 4.5); pop("#x2a", 5.0, 3, 30, 0.25, "power4.in")
clip("s2b", 5.46, 0.99, '<div class="creambg"></div>'
     '<div id="soap" class="soapbar"><div class="soapshine"></div><span>SOAP</span></div>'
     '<div id="c2b" class="chip" style="top:1080px">SABUN BUKU</div>'
     f'<div id="x2b" class="xwrap" style="top:520px">{SVG_X}</div>')
flash(5.46)
A('tl.fromTo("#soap",{y:-900,rotation:-30},{y:0,rotation:-8,duration:0.4,ease:"bounce.out"},5.46);')
pop("#c2b", 5.56); pop("#x2b", 6.1, 3, 30, 0.25, "power4.in")

# S3  6.40-9.30  "tapi yang ni ... keluar foaming"
video("v_bub", "assets/broll/bubbles.mp4", 6.40, 2.90)
clip("s3", 6.40, 2.90, '<div class="shade"></div><div class="kicker" id="k3">TAPI YANG NI...</div>'
     + product_card("p3", 400) + '<div id="t3" class="mega glow" style="top:300px">FOAMING!</div>'
     + rising_bubbles("b3_", 6.4, 2.9, 14, 3))
slam("#k3", 6.46)
A('tl.fromTo("#p3",{y:900,rotation:10},{y:0,rotation:-4,duration:0.6,ease:"back.out(1.6)"},7.0);')
A('tl.to("#k3",{opacity:0,duration:0.2},8.45);')
slam("#t3", 8.6)
sparkles("sp3_", 8.66, 5, (100, 200, 980, 600), 3)

# S4  9.30-11.20  "bukan sahaja berbuih yang lembut"
video("v_pink", "assets/broll/pinkbubble.mp4", 9.30, 1.90)
clip("s4", 9.30, 1.90, '<div id="t4a" class="soft" style="top:430px">BUIH</div>'
     '<div id="t4b" class="soft pinkt" style="top:640px">LEMBUT</div>'
     + rising_bubbles("b4_", 9.3, 1.9, 10, 4))
pop("#t4a", 10.2, 0.3); pop("#t4b", 10.7, 0.3)
A('tl.to("#t4a,#t4b",{y:-25,duration:0.5,yoyo:true,repeat:1,ease:"sine.inOut"},10.95);')

# S5  11.20-14.00  "kalau korang pegang, gebu-gebu"
video("v_lather", "assets/broll/lather.mp4", 11.20, 2.80)
clip("s5", 11.20, 2.80, '<div class="kicker" id="k5">KALAU PEGANG...</div>'
     '<div id="cloud" class="cloud"><span>GEBU-GEBU</span></div>')
slide("#k5", 11.5, 0, -60)
A('tl.fromTo("#cloud",{scale:0,opacity:0},{scale:1,opacity:1,duration:0.5,ease:"elastic.out(1,0.45)"},12.95);')
A('tl.to("#cloud",{scaleX:1.12,scaleY:0.88,duration:0.12,yoyo:true,repeat:3,ease:"sine.inOut"},13.24);')

# S6  14.00-19.40  educational list: keistimewaan
video("v_irid", "assets/broll/irid.mp4", 14.00, 3.00)
video("v_perf", "assets/broll/perfume.mp4", 17.00, 2.40)
clip("s6", 14.00, 5.40, '<div class="shade"></div><div class="panel" id="pn6">'
     '<div class="ptitle" id="pt6">KEISTIMEWAAN KAMI</div>'
     '<div class="row" id="r6a"><b>01</b><span>BODY WASH &amp; SHOWER</span></div>'
     '<div class="row" id="r6b"><b>02</b><span>JENIS FOAMING</span></div>'
     '<div class="row" id="r6c"><b>03</b><span>WANGIAN ALA <em>PERFUME</em></span></div></div>')
pop("#pn6", 14.05, 0.6, 0, 0.4, "power3.out"); slide("#pt6", 14.25, -60, 0)
slide("#r6a", 15.38, -120, 0); slide("#r6b", 16.98, -120, 0); slide("#r6c", 17.92, -120, 0)
sparkles("sp6_", 18.76, 5, (120, 260, 960, 700), 6)

# S7  19.40-22.20  infographic: one press = instant foam
clip("s7", 19.40, 2.80, '<div class="redbg"></div>'
     '<div id="t7a" class="mega" style="top:230px">1x TEKAN</div>'
     '<div class="pumpwrap"><div id="pumphead" class="pumphead"></div><div class="pumpneck"></div>'
     '<div class="pumpbody"><span>FOAM</span></div>'
     '<div id="foam" class="foam"><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div></div>'
     '<div id="t7b" class="tag big" style="top:1170px">TERUS JADI BUIH!</div>')
flash(19.4)
pop("#t7a", 19.45, 0.3)
for tt in (19.45, 20.1):
    A(f'tl.to("#pumphead",{{y:46,duration:0.1,yoyo:true,repeat:1,ease:"power2.in"}},{tt});')
A('tl.fromTo("#foam i",{scale:0,opacity:0},{scale:1,opacity:1,duration:0.4,stagger:0.08,ease:"back.out(2.5)"},20.5);')
pop("#t7b", 21.12)

# S8  22.20-25.10  "tak perlu nak berbuih-buihkan sendiri"
video("v_stream", "assets/broll/stream.mp4", 22.20, 2.90)
clip("s8", 22.20, 2.90, '<div class="shade"></div>'
     f'<div id="x8" class="xwrap small" style="top:360px">{SVG_X}</div>'
     '<div id="t8a" class="mega" style="top:600px">TAK PERLU</div>'
     '<div id="t8b" class="tag" style="top:800px">BERBUIH-BUIHKAN SENDIRI</div>')
pop("#x8", 22.3, 3, 40, 0.25, "power4.in"); slam("#t8a", 22.45); slide("#t8b", 23.0)

# S9  25.10-30.40  two scents, on the real product photo (Noche left, Woman Glory right)
photo("ph_duo", IMG_DUO_MARBLE, 25.10, 5.30, 1.12, 1.0, "50% 50%")
clip("s9", 25.10, 5.30, '<div class="shade top"></div>'
     '<div id="t9" class="mega" style="top:120px"><span class="num" id="n9">2</span> PILIHAN WANGIAN</div>'
     f'<div id="lA" class="plabel pa" style="left:575px">{SCENT_A}</div>'
     f'<div id="lB" class="plabel pb" style="left:150px">{SCENT_B}</div>'
     '<div id="vs" class="vs">VS</div>')
pop("#t9", 25.25, 0.5, 0, 0.4); pop("#n9", 26.12, 3, 0, 0.35, "power4.in")
A('tl.fromTo("#lA",{y:-120,opacity:0},{y:0,opacity:1,duration:0.45,ease:"back.out(2)"},27.52);')
pop("#vs", 28.66, 3, 90, 0.3, "power4.in")
A('tl.fromTo("#lB",{y:-120,opacity:0},{y:0,opacity:1,duration:0.45,ease:"back.out(2)"},29.16);')

# S10 30.40-34.85  Woman Glory notes + bottle card
video("v_flow", "assets/broll/flowers.mp4", 30.40, 4.45)
clip("s10", 30.40, 4.45, '<div class="shade"></div>'
     f'<div id="t10" class="ribbon" style="top:240px">{SCENT_A}</div>'
     + product_card("pg", 330, IMG_GLORY, 1200/470) +
     '<div class="notes left"><div id="n10a" class="note">FRESH</div><div id="n10b" class="note">FLORAL</div>'
     '<div id="n10c" class="note">FEMININE</div></div>')
slide("#t10", 30.48, -400, 0)
A('tl.fromTo("#pg",{x:500,rotation:12},{x:0,rotation:4,duration:0.55,ease:"back.out(1.6)"},30.6);')
pop("#n10a", 32.48); pop("#n10b", 33.08); pop("#n10c", 33.78)

# S11 34.85-37.80  Noche notes + bottle card
video("v_berry", "assets/broll/berries.mp4", 34.85, 2.95)
clip("s11", 34.85, 2.95, '<div class="shade"></div>'
     f'<div id="t11" class="ribbon pk" style="top:240px">{SCENT_B}</div>'
     + product_card("pn", 320, IMG_NOCHE, 1200/455) +
     '<div class="notes left"><div id="n11a" class="note">SWEET</div><div id="n11b" class="note">FRUITY</div></div>')
slide("#t11", 34.92, 400, 0)
A('tl.fromTo("#pn",{x:500,rotation:12},{x:0,rotation:4,duration:0.55,ease:"back.out(1.6)"},35.0);')
pop("#n11a", 36.76); pop("#n11b", 37.28)

# S12 37.80-43.95  formulation checklist (educational)
video("v_lab", "assets/broll/lab.mp4", 37.80, 6.15)
clip("s12", 37.80, 6.15, '<div class="shade blue"></div><div class="panel light" id="pn12">'
     '<div class="ptitle" id="pt12">FORMULASI KAMI</div>'
     f'<div class="crow" id="r12a"><i>{SVG_CHECK}</i><span>TANPA PARABEN</span></div>'
     '<div class="fnote" id="f12">*Paraben = sejenis bahan pengawet</div>'
     f'<div class="crow" id="r12b"><i>{SVG_CHECK}</i><span>TANPA BAHAN BERBAHAYA</span></div>'
     '<div class="fnote" id="f12b">yang dilarang dalam kosmetik</div></div>')
pop("#pn12", 37.9, 0.6, 0, 0.4, "power3.out"); slide("#pt12", 38.74, -60, 0)
pop("#r12a", 40.42, 1.8, 0, 0.25, "power4.in"); slide("#f12", 40.9, 0, 30)
pop("#r12b", 41.82, 1.8, 0, 0.25, "power4.in"); slide("#f12b", 42.6, 0, 30)

# S13 43.95-47.40  lab tested stamp
video("v_sci", "assets/broll/scientist.mp4", 43.95, 3.45)
clip("s13", 43.95, 3.45, '<div class="shade"></div>'
     '<div id="t13" class="kicker" style="top:300px">PRODUK TELAH MENJALANI</div>'
     '<div id="stamp" class="stamp"><div>UJIAN</div><div class="big">MAKMAL</div><div>✓ DIUJI</div></div>')
slide("#t13", 44.02, 0, -60)
A('tl.fromTo("#stamp",{scale:3.2,opacity:0,rotation:-30},{scale:1,opacity:1,rotation:-12,duration:0.28,ease:"power4.in"},45.48);')
A('tl.fromTo("#root",{x:-16,y:10},{x:0,y:0,duration:0.3,ease:"elastic.out(1,0.3)"' + IR("#root") + '},45.76);')

# S14 47.40-51.00  experience
video("v_show", "assets/broll/shower.mp4", 47.40, 3.60)
clip("s14", 47.40, 3.60, '<div class="shade"></div>'
     '<div id="t14a" class="kicker" style="top:420px">PENGALAMAN MANDIAN</div>'
     '<div id="t14b" class="mega glow" style="top:540px">LEBIH ISTIMEWA</div>')
slide("#t14a", 48.82, 0, 60); slam("#t14b", 49.88)
sparkles("sp14_", 50.1, 6, (100, 380, 980, 820), 14)

# S15 51.00-52.95  product hero: "korang kena try Frescura Body"
photo("ph_diag", IMG_DUO_DIAG, 51.00, 1.95, 1.0, 1.14, "50% 50%")
clip("s15", 51.00, 1.95, '<div class="shade top"></div>'
     '<div id="t15" class="mega" style="top:150px">WAJIB TRY!</div>'
     f'<div id="t15b" class="tag big" style="top:340px">{BRAND}</div>')
slam("#t15", 51.15); pop("#t15b", 51.8)

# S16 52.95-58.95  CTA: yellow basket + limited stock
video("v_phone", "assets/broll/phone.mp4", 52.95, 6.00)
clip("s16", 52.95, 6.00, '<div class="shade"></div>'
     '<div id="t16a" class="kicker" style="top:230px">TEKAN BEG KUNING</div>'
     f'<div id="basket" class="basket">{SVG_BASKET}</div><div id="ripple" class="ripple"></div>'
     '<div id="t16b" class="tag big" style="top:330px">CHECK OUT SEKARANG</div>'
     '<div id="stock" class="stock"><div class="slabel">STOK SANGAT TERHAD!</div>'
     '<div class="sbar"><div id="sfill" class="sfill"></div></div></div>')
slam("#t16a", 52.98); pop("#basket", 53.2)
A('tl.fromTo("#ripple",{scale:0.2,opacity:0.9},{scale:2.2,opacity:0,duration:0.5,ease:"power2.out"},53.56);')
A('tl.to("#basket",{scale:0.86,duration:0.08,yoyo:true,repeat:1},53.68);')
pop("#t16b", 54.24)
pop("#stock", 55.68, 0.5)
A('tl.fromTo("#sfill",{width:"42%"},{width:"7%",duration:2.8,ease:"power1.in"},55.8);')
A('tl.to("#stock .slabel",{opacity:0.25,duration:0.15,yoyo:true,repeat:7},56.4);')

# S17 58.95-62.40  final CTA on the duo photo
photo("ph_wood", IMG_DUO_WOOD, 58.95, 62.4 - 58.95, 1.15, 1.02, "50% 50%")
clip("s17", 58.95, 62.4 - 58.95, '<div class="shade top"></div>'
     '<div id="t17" class="mega" style="top:120px">PILIH WANGIAN<br>FAVOURITE KORANG</div>'
     f'<div id="fB" class="plabel pb" style="left:150px;top:1020px">{SCENT_B}</div>'
     f'<div id="fA" class="plabel pa" style="left:570px;top:1020px">{SCENT_A}</div>'
     f'<div id="btn" class="btn" style="top:1170px"><i>{SVG_BASKET}</i>CHECK OUT SEKARANG</div>')
pop("#t17", 59.1, 0.4); pop("#fB", 59.82, 0.2, -15); pop("#fA", 60.68, 0.2, 15)
pop("#btn", 61.4, 0.2)
A('tl.to("#btn",{scale:1.08,duration:0.2,yoyo:true,repeat:3,ease:"sine.inOut"},61.9);')

# ---- remap every scene time onto the tightened voice timeline (captions are already final)
def _remap_attr(m):
    s, d = float(m.group(1)), float(m.group(2))
    return f'data-start="{T(s):.3f}" data-duration="{T(s + d) - T(s):.3f}"'
html = [re.sub(r'data-start="([\d.]+)" data-duration="([\d.]+)"', _remap_attr, h) for h in html]
js = [re.sub(r',([\d.]+)\);$', lambda m: f",{T(float(m.group(1))):.3f});", l) for l in js]

# ------------------------------------------------------------------ captions
for ci, ch in enumerate(chunks):
    start = ch[0]["s"]
    if start < 2.4:          # hook headline already says it on screen
        continue
    nxt = chunks[ci + 1][0]["s"] if ci + 1 < len(chunks) else DURATION
    end = min(nxt, ch[-1]["e"] + 0.5) if nxt - ch[-1]["e"] > 0.6 else nxt
    spans = []
    for wi, w in enumerate(ch):
        key = re.sub(r"[^a-z\-]", "", w["t"].lower())
        cls = "w hl" if key in HL else "w"
        spans.append(f'<span id="w{ci}_{wi}" class="{cls}">{w["t"].rstrip(".,")}</span>')
        A(f'tl.fromTo("#w{ci}_{wi}",{{scale:0.6,opacity:0.0}},{{scale:1,opacity:1,duration:0.12,'
          f'ease:"back.out(3)"}},{w["s"]:.2f});')
    clip(f"cap{ci}", start, max(end - start, 0.2), " ".join(spans), cls="cap")

# ------------------------------------------------------------------ page
CSS = open(f"{proj}/style.css").read()
body = "\n".join(html)
preview_tag = "" if FINAL else '<div class="pv">PREVIEW</div>'
page = f"""<!doctype html>
<html lang="ms" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
{CSS}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DURATION}" data-width="1080" data-height="1920">
<audio id="mix" class="clip" src="assets/audio/mix.wav" data-start="0" data-duration="{DURATION}" data-volume="1"></audio>
{body}
<div id="flash"></div>
<div class="vign"></div>
{preview_tag}
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body>
</html>
"""
open(f"{proj}/index.html", "w").write(page)
print(f"scenes ok, {len(chunks)} caption chunks, {len(js)} tweens")
