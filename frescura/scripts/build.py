#!/usr/bin/env python3
"""Generate the HyperFrames composition (index.html) for the Frescura Body ad."""
import json, sys, html

S = sys.argv[1]
OUT = sys.argv[2]
TOTAL = float(sys.argv[3]) if len(sys.argv) > 3 else 37.8

W = json.load(open(f"{S}/words.json"))
for w in W:
    if w["w"] == "dalam troli,":
        w["w"] = "dalam"
# merge "tiba" + "-tiba"
m = []
for w in W:
    if m and w["w"].startswith("-"):
        m[-1]["w"] += w["w"]; m[-1]["e"] = w["e"]
    else:
        m.append(dict(w))
W = []
for w in m:
    if w["w"] == "Frescura Body":
        mid = round((w["s"] + w["e"]) / 2, 3)
        W.append(dict(w="Frescura", s=w["s"], e=mid)); W.append(dict(w="Body", s=mid, e=w["e"]))
    else:
        W.append(w)
T = {}  # first time a word appears (lookup helper)
def t(word, nth=1):
    c = 0
    for w in W:
        if w["w"].strip(",").lower() == word.lower():
            c += 1
            if c == nth:
                return w["s"]
    raise KeyError(word)

# ---------------- caption groups ----------------
GROUPS = [3, 3, 1, 2, 3, 3, 3, 3, 3, 3, 3]  # filled sequentially below by phrase list instead
PHRASES = [
    "Yang tahu tak apa perkara yang paling sekali memalukan",
    "bila korang tengah|bercakap dengan orang|tiba-tiba dia|macam nak menjauh|sebab bau badan",
    "Jangan ambil mudah|tentang kebersihan badan|terutamanya kalau korang|jenis mudah berpeluh",
    "pastikan mandi secara teratur, bersihkan kawasan lipatan badan dan gunakan deodoran jika diperlukan",
    "Semestinya untuk|rutin mandi|yang lebih menarik",
    "pastinya Frescura Body",
    "dengan buih yang lembut|kandungan garam laut|dan wanginya feminin|yang menyenangkan",
    "Jangan tunggu orang tegur baru nak ambil tindakan",
    "tekan beg kuning|sekarang dan masukkan|Frescura Body dalam|terutama jika kalian|pilih Bombshell|ataupun|Midnight Fantasy,|check out terus|sebab stok memang|sangat terhad",
]
HIDE = {0, 3, 5, 7}
HIDE_CHUNKS = {"sebab bau badan", "pilih Bombshell", "ataupun", "Midnight Fantasy,", "sangat terhad"}  # phrases replaced by big kinetic type / cards
ACCENT = {"memalukan", "bau", "badan", "kebersihan", "berpeluh", "deodoran", "menarik", "Frescura", "Body",
          "lembut", "garam", "laut", "feminin", "tindakan", "kuning", "Bombshell", "Midnight", "Fantasy,",
          "terhad", "rutin", "menjauh", "stok"}
groups = []
wi = 0
for pi, ph in enumerate(PHRASES):
    for chunk in ph.split("|"):
        n = len(chunk.split())
        ws = W[wi:wi + n]
        assert " ".join(x["w"] for x in ws) == chunk, (chunk, [x["w"] for x in ws])
        wi += n
        if pi not in HIDE and chunk not in HIDE_CHUNKS:
            groups.append(ws)
assert wi == len(W), (wi, len(W))

cap_html = []
cap_js = []
for gi, ws in enumerate(groups):
    s = ws[0]["s"] - 0.04
    nxt = groups[gi + 1][0]["s"] - 0.04 if gi + 1 < len(groups) else ws[-1]["e"] + 0.5
    e = min(ws[-1]["e"] + 0.35, nxt)
    spans = []
    for k, w in enumerate(ws):
        cls = "w acc" if w["w"] in ACCENT else "w"
        spans.append(f'<span class="{cls}" id="cw{gi}_{k}">{html.escape(w["w"])}</span>')
        cap_js.append(f'tl.fromTo("#cw{gi}_{k}",{{opacity:.42,y:10}},{{opacity:1,y:0,duration:.14,ease:"power3.out"}},{w["s"]:.3f});')
    cap_html.append(f'<div class="cap clip" id="cg{gi}" data-start="{s:.3f}" data-duration="{e - s:.3f}" data-track-index="9"><div class="capin">{" ".join(spans)}</div></div>')
    cap_js.append(f'tl.fromTo("#cg{gi} .capin",{{opacity:0,scale:.92,filter:"blur(10px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:.18,ease:"expo.out"}},{s:.3f});')

# ---------------- timing anchors ----------------
A = dict(
    hook=0.0, bila=t("bila"), tiba=t("tiba-tiba"), menjauh=t("menjauh"), bau=t("bau"),
    jangan=t("Jangan"), keb=t("kebersihan"), teru=t("terutamanya"), peluh=t("berpeluh"),
    past=t("pastikan"), bers=t("bersihkan"), guna=t("gunakan"), semes=t("Semestinya"), rutin=t("rutin"),
    menarik=t("menarik"), pastinya=t("pastinya"), fb=t("Frescura"), dengan=t("dengan", 2), buih=t("buih"),
    garam=t("kandungan"), wangi=t("dan", 2), feminin=t("feminin"), jangan2=t("Jangan", 2), tegur=t("tegur"),
    tindakan=t("ambil", 2), tekan=t("tekan"), kuning=t("kuning"), masuk=t("masukkan"), fb2=t("Frescura", 2),
    teruta=t("terutama"), bomb=t("Bombshell"), mid=t("Midnight"), check=t("check"), stok=t("stok"),
    terhad=t("terhad"), end=W[-1]["e"] + 0.3,
)
json.dump(A, open(f"{S}/anchors.json", "w"), indent=1)

# B-roll timeline: (file, start, end)
B = [
    ("b01", 0.0, A["tiba"]),
    ("b02", A["jangan"], A["past"]),
    ("b03", A["past"], A["bers"] + 0.2),
    ("b05", A["bers"] + 0.2, A["semes"]),
    ("foam_lather", A["semes"], A["rutin"] + 0.55),
    ("b17", A["rutin"] + 0.55, A["menarik"] - 0.5),
    ("b07", A["menarik"] - 0.5, A["pastinya"]),
    ("foam_pump", A["dengan"] - 0.12, A["garam"]),
    ("b09", A["garam"], A["wangi"]),
    ("b10", A["wangi"], A["feminin"] + 0.3),
    ("b11", A["feminin"] + 0.3, A["jangan2"]),
    ("b15", A["jangan2"], A["tekan"]),
    ("b16", A["tekan"], A["teruta"]),
    ("split", A["teruta"], A["check"]),
]

def clip(id_, f, s, e, z=1, extra=""):
    return (f'<video id="{id_}" class="clip bv" src="assets/broll/{f}.mp4" muted playsinline '
            f'data-start="{s:.3f}" data-duration="{e - s:.3f}" data-track-index="1" style="z-index:{z};{extra}"></video>')

vids = []
kb = []
for i, (f, s, e) in enumerate(B):
    vid = f"v{i}"
    vids.append(clip(vid, f, s, e))
    kb.append(f'tl.fromTo("#{vid}",{{scale:1.16}},{{scale:1.02,duration:{e - s:.3f},ease:"none"}},{s:.3f});')
    if i: kb.append(f'tl.fromTo("#{vid}",{{filter:"brightness(1.9) blur(14px)"}},{{filter:"brightness(1) blur(0px)",duration:.28,ease:"expo.out"}},{s:.3f});')

def boutique(pid, s, e, logo=True, bottles=True):
    """Luxury mall boutique display built from CSS."""
    bok = []
    seed = 7
    for k in range(8):
        seed = (seed * 1103515245 + 12345) % 2**31
        x = seed % 1080; seed = (seed * 1103515245 + 12345) % 2**31
        y = 140 + seed % 700; seed = (seed * 1103515245 + 12345) % 2**31
        r = 30 + seed % 90
        col = ["rgba(255,214,160,.55)", "rgba(255,236,210,.45)", "rgba(210,170,255,.35)", "rgba(255,190,150,.4)"][k % 4]
        bok.append(f'<i class="bok {pid}bok" style="left:{x}px;top:{y}px;width:{r}px;height:{r}px;background:{col}"></i>')
    b = f'''
<div class="scene clip boutique" id="{pid}" data-start="{s:.3f}" data-duration="{e - s:.3f}" data-track-index="2">
  <div class="bq-cam" id="{pid}cam">
    <div class="bq-wall"></div>
    {''.join(bok)}
    <div class="arch a1"></div><div class="arch a2"></div><div class="arch a3"></div>
    <div class="strip s1"></div><div class="strip s2"></div>
    <div class="floor"></div>
    <div class="cone c1" id="{pid}c1"></div><div class="cone c2" id="{pid}c2"></div>
    <div class="ped p1"><div class="ptop"></div><div class="pbody"></div></div>
    <div class="ped p2"><div class="ptop"></div><div class="pbody"></div></div>
    {'<img class="btl bred" id="%sbr" src="assets/img/red_cut.png"><img class="btl bred refl" src="assets/img/red_cut.png"><img class="btl bpur" id="%sbp" src="assets/img/purple_cut.png"><img class="btl bpur refl" src="assets/img/purple_cut.png">' % (pid, pid) if bottles else ''}
    <div class="sheen" id="{pid}sh"></div>
  </div>
  {f"""<div class="logo" id="{pid}logo"><svg class="ring" viewBox="0 0 600 600"><circle id="{pid}ring" cx="300" cy="300" r="280" /></svg>
    <div class="lg1">FRESCURA BODY</div><div class="lg2">SOFT &nbsp;|&nbsp; FRAGRANT</div></div>""" if logo else ''}
</div>'''
    js = f'''
tl.fromTo("#{pid}cam",{{scale:1.12,y:40}},{{scale:1,y:0,duration:{e - s:.3f},ease:"power2.out"}},{s:.3f});
tl.fromTo(".{pid}bok",{{x:-30}},{{x:40,duration:{e - s:.3f},ease:"none",stagger:0}},{s:.3f});
tl.fromTo(["#{pid}c1","#{pid}c2"],{{opacity:0}},{{opacity:1,duration:.5,stagger:.12,ease:"power2.out"}},{s + 0.05:.3f});
tl.fromTo("#{pid}sh",{{xPercent:-120}},{{xPercent:120,duration:1.1,ease:"power2.inOut"}},{s + 0.25:.3f});
'''
    if bottles:
        js += f'''tl.fromTo("#{pid}br",{{y:120,opacity:0}},{{y:0,opacity:1,duration:.55,ease:"expo.out"}},{s + 0.05:.3f});
tl.fromTo("#{pid}bp",{{y:120,opacity:0}},{{y:0,opacity:1,duration:.55,ease:"expo.out"}},{s + 0.15:.3f});
'''
    return b, js

bq1, bq1js = boutique("bq1", A["pastinya"], A["dengan"] - 0.12)
bq2, bq2js = boutique("bq2", A["check"], TOTAL, logo=False)

a = A
FACT_T = a["teru"]
html_out = f'''<!doctype html>
<html lang="ms" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
@font-face{{font-family:'Bodoni Moda';font-style:normal;font-weight:400 900;font-display:block;src:url(assets/fonts/BodoniModa-normal-400_700.woff2) format('woff2');}}
@font-face{{font-family:'Bodoni Moda';font-style:italic;font-weight:400 900;font-display:block;src:url(assets/fonts/BodoniModa-italic-400_700.woff2) format('woff2');}}
@font-face{{font-family:'Manrope';font-style:normal;font-weight:200 800;font-display:block;src:url(assets/fonts/Manrope-normal-800.woff2) format('woff2');}}
@font-face{{font-family:'Unbounded';font-style:normal;font-weight:200 900;font-display:block;src:url(assets/fonts/Unbounded-normal-800.woff2) format('woff2');}}
:root{{
  --ground:#09070a; --ink:#f6efe4; --gold:#d9b878; --gold2:#f3dcaa; --rose:#a3122e; --plum:#231429; --violet:#6f4fd1; --yellow:#ffc82e;
  --serif:'Bodoni Moda',serif; --sans:'Manrope',sans-serif; --disp:'Unbounded',sans-serif;
}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:var(--ground)}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:var(--ground);font-family:var(--sans);color:var(--ink)}}
.clip{{position:absolute;inset:0}}
.bv{{width:1080px;height:1920px;object-fit:cover;transform-origin:50% 50%}}
.scene{{overflow:hidden}}
.dim{{position:absolute;inset:0;pointer-events:none}}
/* global look */
#vig{{position:absolute;inset:0;z-index:40;pointer-events:none;background:radial-gradient(ellipse 80% 65% at 50% 46%,rgba(0,0,0,0) 52%,rgba(0,0,0,.55) 100%)}}
#shade{{position:absolute;inset:0;z-index:5;pointer-events:none;background:linear-gradient(180deg,rgba(6,4,6,.55) 0%,rgba(6,4,6,0) 22%,rgba(6,4,6,0) 58%,rgba(6,4,6,.78) 100%)}}
#grain{{position:absolute;inset:-200px;z-index:41;pointer-events:none;opacity:.075;mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='240' height='240' filter='url(%23n)'/></svg>")}}
#bug{{position:absolute;top:92px;left:0;right:0;z-index:50;display:flex;align-items:center;justify-content:center;gap:22px;
  font:700 22px/1 var(--sans);letter-spacing:.55em;color:rgba(246,239,228,.82);text-indent:.55em}}
#bug i{{display:block;width:70px;height:1px;background:linear-gradient(90deg,transparent,var(--gold))}}
#bug i:last-child{{transform:scaleX(-1)}}
#prog{{position:absolute;top:0;left:0;height:6px;width:1080px;z-index:51;transform-origin:0 50%;background:linear-gradient(90deg,var(--gold),var(--gold2))}}
.leak{{position:absolute;top:-10%;left:0;width:1080px;height:120%;z-index:45;pointer-events:none;mix-blend-mode:screen;opacity:0;
  background:linear-gradient(100deg,rgba(0,0,0,0) 30%,rgba(255,206,150,.65) 48%,rgba(255,244,220,.9) 52%,rgba(255,180,140,.5) 58%,rgba(0,0,0,0) 72%)}}
#flash{{position:absolute;inset:0;z-index:46;background:#fff7ea;opacity:0;pointer-events:none}}
/* captions */
.cap{{z-index:30;display:flex;align-items:flex-end;justify-content:center;padding:0 70px 250px}}
.capin{{text-align:center;font:800 76px/1.12 var(--sans);letter-spacing:-.015em;color:var(--ink);
  text-shadow:0 4px 24px rgba(0,0,0,.65),0 1px 2px rgba(0,0,0,.6);max-width:940px}}
.capin .w{{display:inline-block}}
.capin .acc{{font-family:var(--serif);font-style:italic;font-weight:700;font-size:92px;letter-spacing:0;
  color:#f0d59c;text-shadow:0 4px 22px rgba(0,0,0,.75),0 0 2px rgba(0,0,0,.5)}}
/* hook */
#hook{{z-index:20;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding-top:40px}}
.k-small{{font:600 40px/1 var(--sans);letter-spacing:.32em;text-transform:uppercase;color:var(--gold2);text-indent:.32em}}
.k-serif{{font:italic 600 128px/1 var(--serif);margin-top:34px}}
.k-out{{font:800 200px/0.95 var(--disp);letter-spacing:-.03em;color:transparent;-webkit-text-stroke:3px var(--gold);margin-top:26px}}
.k-big{{font:800 118px/1 var(--disp);letter-spacing:-.03em;margin-top:10px;
  background:linear-gradient(180deg,#ffffff 0%,#f3dcaa 60%,#c99b55 100%);-webkit-background-clip:text;background-clip:text;color:transparent}}
.k-line{{width:0;height:2px;background:var(--gold);margin-top:40px}}
/* conversation graphic */
#conv{{z-index:12;background:radial-gradient(ellipse 90% 70% at 50% 40%,#2b1730 0%,#120a14 55%,#070508 100%)}}
#conv svg{{position:absolute;left:0;top:420px}}
.fig{{fill:none;stroke:var(--ink);stroke-width:7;stroke-linecap:round}}
.figr{{stroke:var(--gold)}}
.odor path{{fill:none;stroke:#9fb27a;stroke-width:6;stroke-linecap:round;opacity:.9}}
#dist{{stroke:var(--gold2);stroke-width:3;stroke-dasharray:10 12;fill:none}}
.bb{{position:absolute;left:0;right:0;top:1160px;text-align:center}}
.bb .t1{{font:600 38px/1 var(--sans);letter-spacing:.3em;color:rgba(246,239,228,.7);text-indent:.3em}}
.bb .t2{{white-space:nowrap;font:800 132px/1 var(--disp);letter-spacing:-.03em;margin-top:22px;color:#ffe9e4;text-shadow:0 0 60px rgba(196,30,58,.65)}}
.chip{{display:inline-flex;align-items:center;gap:14px;padding:14px 26px;border:1.5px solid rgba(217,184,120,.7);border-radius:100px;
  font:700 26px/1 var(--sans);letter-spacing:.3em;color:var(--gold2);text-indent:.3em;background:rgba(10,8,10,.45);backdrop-filter:blur(10px)}}
.chip b{{width:10px;height:10px;border-radius:50%;background:var(--gold)}}
/* sweat headline + fact card */
#sweat{{z-index:12}}
.hl{{position:absolute;left:0;right:0;top:220px;text-align:center}}
.hl .a{{font:800 92px/1 var(--disp);letter-spacing:-.03em}}
.hl .b{{font:italic 600 118px/1.05 var(--serif);color:var(--gold2);margin-top:14px}}
.glass{{position:absolute;left:80px;right:80px;border-radius:44px;padding:52px 56px;background:linear-gradient(160deg,rgba(32,24,30,.72),rgba(12,9,12,.6));
  border:1px solid rgba(243,220,170,.28);backdrop-filter:blur(22px) saturate(1.2);box-shadow:0 30px 80px rgba(0,0,0,.5)}}
#fact{{top:640px}}
#fact .f1{{font:800 58px/1.12 var(--sans);margin-top:28px}}
#fact .f2{{font:500 40px/1.35 var(--sans);color:rgba(246,239,228,.78);margin-top:18px}}
#fact .f2 em{{font-family:var(--serif);font-style:italic;font-weight:700;color:var(--gold2)}}
.drop{{position:absolute;width:44px;height:62px;opacity:0}}
/* steps */
#steps{{z-index:12}}
#steps .hl{{top:250px}}
.step{{position:absolute;left:80px;right:80px;height:250px;border-radius:40px;display:flex;align-items:center;gap:40px;padding:0 50px;
  background:linear-gradient(120deg,rgba(28,20,26,.78),rgba(10,8,10,.58));border:1px solid rgba(243,220,170,.25);backdrop-filter:blur(20px);opacity:0}}
.step .n{{font:italic 700 118px/1 var(--serif);color:var(--gold);width:150px}}
.step .tt{{font:800 54px/1.08 var(--sans)}}
.step .ss{{font:500 34px/1.3 var(--sans);color:rgba(246,239,228,.7);margin-top:10px}}
.step svg{{margin-left:auto;flex:none}}
.tick circle{{fill:none;stroke:rgba(243,220,170,.35);stroke-width:4}}
.tick path{{fill:none;stroke:var(--gold2);stroke-width:7;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:80;stroke-dashoffset:80}}
/* mall headline */
#mall{{z-index:12}}
#mall .hl{{top:300px}}
#mall .hl .a{{font:600 44px/1 var(--sans);letter-spacing:.34em;color:var(--gold2);text-indent:.34em}}
#mall .hl .b{{font-size:150px;color:var(--ink)}}
#mall .hl{{text-shadow:0 6px 40px rgba(0,0,0,.85),0 0 4px rgba(0,0,0,.6)}}
#mall{{background:linear-gradient(180deg,rgba(6,4,6,.7) 0%,rgba(6,4,6,0) 45%)}}
/* boutique */
.boutique{{z-index:14;background:#070506}}
.bq-cam{{position:absolute;inset:0;transform-origin:50% 60%}}
.bq-wall{{position:absolute;inset:0;background:radial-gradient(ellipse 70% 45% at 50% 34%,#3a2a24 0%,#1a1213 45%,#080607 80%)}}
.bok{{position:absolute;border-radius:50%;filter:blur(18px);mix-blend-mode:screen}}
.arch{{position:absolute;top:330px;width:300px;height:900px;border-radius:150px 150px 0 0;
  background:linear-gradient(180deg,rgba(255,226,180,.16),rgba(255,226,180,.03) 70%,rgba(0,0,0,0));border:2px solid rgba(217,184,120,.35);
  box-shadow:inset 0 0 80px rgba(255,214,160,.12),0 0 40px rgba(217,184,120,.12)}}
.a1{{left:-80px;opacity:.6}} .a2{{left:390px;width:300px}} .a3{{left:860px;opacity:.6}}
.strip{{position:absolute;top:240px;width:6px;height:1100px;border-radius:6px;background:linear-gradient(180deg,rgba(255,230,190,0),#ffe6be 30%,#ffd598 70%,rgba(255,230,190,0));
  box-shadow:0 0 30px 8px rgba(255,205,140,.45)}}
.s1{{left:250px}} .s2{{left:824px}}
.floor{{position:absolute;left:0;right:0;top:1240px;bottom:0;background:linear-gradient(180deg,#1c1415 0%,#0b0809 40%,#050404 100%);
  border-top:1px solid rgba(243,220,170,.25)}}
.cone{{position:absolute;top:-60px;width:620px;height:1400px;opacity:0;mix-blend-mode:screen;filter:blur(30px);
  background:linear-gradient(180deg,rgba(255,236,205,.42),rgba(255,226,190,.08) 85%,rgba(0,0,0,0));clip-path:polygon(42% 0,58% 0,100% 100%,0 100%)}}
.c1{{left:-20px}} .c2{{left:480px}}
.ped{{position:absolute;top:1130px;width:380px;height:300px}}
.p1{{left:110px}} .p2{{left:590px}}
.ptop{{position:absolute;left:0;top:0;width:380px;height:90px;border-radius:50%;z-index:2;
  background:radial-gradient(ellipse at 45% 40%,#fbf6ef 0%,#e1d8cc 50%,#b9ab9b 100%);box-shadow:0 0 50px rgba(255,230,200,.25)}}
.pbody{{position:absolute;left:0;top:45px;width:380px;height:255px;
  background:linear-gradient(90deg,#8d8174 0%,#efe7dc 30%,#fffaf3 45%,#d8cdbf 70%,#6f645a 100%);border-radius:0 0 190px 190px/0 0 45px 45px}}
.btl{{position:absolute;height:600px;bottom:calc(1920px - 1172px);filter:drop-shadow(0 30px 40px rgba(0,0,0,.6))}}
.bred{{left:206px}} .bpur{{left:678px}}
.refl{{transform:scaleY(-1);transform-origin:50% 100%;bottom:auto;top:1172px;opacity:.16;filter:blur(2px);
  -webkit-mask-image:linear-gradient(0deg,rgba(0,0,0,0) 55%,#000 100%);mask-image:linear-gradient(0deg,rgba(0,0,0,0) 55%,#000 100%);display:none}}
.sheen{{position:absolute;inset:0;mix-blend-mode:screen;background:linear-gradient(105deg,rgba(0,0,0,0) 40%,rgba(255,240,215,.22) 50%,rgba(0,0,0,0) 60%)}}
.logo{{position:absolute;left:0;right:0;top:120px;height:420px;display:flex;flex-direction:column;align-items:center;justify-content:center}}
.logo .ring{{position:absolute;width:420px;height:420px;left:330px;top:0}}
.logo .ring circle{{fill:none;stroke:#5fe3ff;stroke-width:5;stroke-dasharray:1760;stroke-dashoffset:1760;filter:drop-shadow(0 0 12px #2fb8ff)}}
.lg1{{font:600 104px/1 var(--serif);letter-spacing:.06em;color:#e8fbff;text-shadow:0 0 22px rgba(80,220,255,.85),0 0 60px rgba(40,160,255,.55)}}
.lg2{{font:700 26px/1 var(--sans);letter-spacing:.7em;color:rgba(246,239,228,.85);margin-top:28px;text-indent:.7em}}
/* feature tags */
.feat{{position:absolute;left:80px;top:1080px;z-index:25;opacity:0}}
.feat .ix{{font:700 26px/1 var(--sans);letter-spacing:.4em;color:var(--gold2)}}
.feat .nm{{font:800 112px/1 var(--disp);letter-spacing:-.03em;margin-top:18px;text-shadow:0 6px 30px rgba(0,0,0,.5)}}
.feat .en{{font:italic 600 58px/1 var(--serif);color:var(--gold2);margin-top:14px}}
.feat .bar{{width:120px;height:3px;background:var(--gold);margin-top:26px;transform-origin:0 50%}}
.bub{{position:absolute;border-radius:50%;border:2px solid rgba(255,255,255,.75);background:radial-gradient(circle at 35% 30%,rgba(255,255,255,.7),rgba(255,255,255,.05) 45%,rgba(255,200,230,.12));opacity:0;z-index:24}}
/* kinetic */
#kin{{z-index:16;background:radial-gradient(ellipse 90% 60% at 50% 45%,rgba(8,5,8,.78),rgba(8,5,8,.55));display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding-bottom:120px}}
#kin .k1{{font:800 120px/1 var(--disp);letter-spacing:-.03em}}
#kin .k2{{font:italic 600 150px/1.05 var(--serif);color:var(--gold2);margin-top:10px}}
#kin .k3{{font:600 42px/1 var(--sans);letter-spacing:.34em;color:rgba(246,239,228,.75);margin-top:50px;text-indent:.34em}}
#kin .k4{{display:inline-block;white-space:nowrap;font:800 84px/1 var(--disp);letter-spacing:-.03em;margin-top:24px;padding:18px 34px;border:3px solid var(--gold);border-radius:24px}}
/* shop UI */
#shop{{z-index:16}}
#shop .hl{{top:220px}}
#shop .hl .a{{font-size:74px}}
.ylw{{color:var(--yellow);text-shadow:0 0 40px rgba(255,200,46,.45)}}
#card{{position:absolute;left:110px;top:520px;width:860px;height:960px;border-radius:56px;overflow:hidden;
  background:linear-gradient(170deg,rgba(40,28,34,.86),rgba(14,10,13,.88));border:1px solid rgba(243,220,170,.3);backdrop-filter:blur(26px);box-shadow:0 40px 120px rgba(0,0,0,.6)}}
#card .img{{position:absolute;left:30px;right:30px;top:30px;height:600px;border-radius:36px;background:radial-gradient(ellipse at 50% 40%,#5b1220 0%,#2a0a12 60%,#12060a 100%)}}
#card .img img{{position:absolute;height:540px;left:50%;top:40px;transform:translateX(-50%)}}
#card .t{{position:absolute;left:56px;top:670px;font:800 50px/1.1 var(--sans)}}
#card .s{{position:absolute;left:56px;top:740px;font:500 32px/1.3 var(--sans);color:rgba(246,239,228,.7)}}
#card .st{{position:absolute;left:56px;top:810px;font:700 34px/1 var(--sans);color:var(--gold2);letter-spacing:.12em}}
#ybtn{{position:absolute;right:46px;top:810px;width:170px;height:120px;border-radius:30px;background:var(--yellow);display:flex;align-items:center;justify-content:center;
  box-shadow:0 14px 40px rgba(255,200,46,.45)}}
#ybadge{{position:absolute;right:30px;top:792px;width:58px;height:58px;border-radius:50%;background:#e8203c;color:#fff;font:800 32px/58px var(--sans);text-align:center;opacity:0;z-index:3}}
#tap{{position:absolute;left:810px;top:1390px;width:120px;height:120px;border-radius:50%;border:5px solid #fff;opacity:0;z-index:20}}
#finger{{position:absolute;left:840px;top:1440px;width:130px;opacity:0;z-index:21}}
#fly{{position:absolute;left:400px;top:700px;height:300px;opacity:0;z-index:22}}
#cartlbl{{position:absolute;left:0;right:0;top:1498px;text-align:center;opacity:0}}
/* split */
#split{{z-index:16}} .half{{background:transparent}}
.half{{position:absolute;top:0;width:540px;height:1920px;overflow:hidden}}
.half video{{position:absolute;left:-270px;top:0;width:1080px;height:1920px;object-fit:cover}}
.hL{{left:0}} .hR{{left:540px}}
.half .tint{{position:absolute;inset:0}}
.hL .tint{{background:linear-gradient(180deg,rgba(60,0,12,.25),rgba(40,0,10,.7))}}
.hR .tint{{background:linear-gradient(180deg,rgba(20,10,60,.2),rgba(16,6,40,.7))}}
.half img{{position:absolute;height:820px;left:50%;top:460px;transform:translateX(-50%);filter:drop-shadow(0 40px 50px rgba(0,0,0,.7))}}
.half .nm{{position:absolute;left:0;right:0;top:1330px;text-align:center}}
.half .nm .x{{font:700 22px/1 var(--sans);letter-spacing:.45em;color:rgba(246,239,228,.7);text-indent:.45em}}
.half .nm .y{{font:italic 700 74px/1.04 var(--serif);margin-top:16px}}
.half .shade{{position:absolute;inset:0;background:rgba(0,0,0,.6);opacity:0}}
#divider{{position:absolute;left:539px;top:0;width:2px;height:1920px;background:linear-gradient(180deg,transparent,var(--gold),transparent);z-index:3}}
/* stock */
#stock{{position:absolute;inset:0;z-index:18}}
#stock .glass{{top:300px;text-align:center;padding:50px 56px 56px}}
#stock .c1{{font:800 82px/1 var(--disp);letter-spacing:-.03em}}
#stock .c2{{font:500 34px/1 var(--sans);color:rgba(246,239,228,.72);margin-top:22px;letter-spacing:.08em}}
.track{{height:22px;border-radius:22px;background:rgba(255,255,255,.12);margin-top:40px;overflow:hidden}}
#fill{{height:100%;width:100%;border-radius:22px;background:linear-gradient(90deg,#e33a4f,#f3a35d);transform-origin:0 50%}}
.lv{{display:flex;justify-content:space-between;margin-top:18px;font:700 28px/1 var(--sans);color:var(--gold2);letter-spacing:.1em}}
#dot{{display:inline-block;width:16px;height:16px;border-radius:50%;background:#ff3b52;margin-right:12px;box-shadow:0 0 18px #ff3b52}}
#stamp{{position:absolute;left:0;right:0;top:1330px;margin:auto;width:760px;text-align:center;font:800 104px/1 var(--disp);letter-spacing:-.02em;color:#ffe7ea;
  border:6px solid #e8203c;border-radius:28px;padding:22px 0;transform:rotate(-7deg);opacity:0;background:rgba(120,8,24,.35);text-shadow:0 0 30px rgba(232,32,60,.6);z-index:19}}
/* end card */
#endc{{position:absolute;left:0;right:0;top:1480px;text-align:center;z-index:20;opacity:0}}
#endc .pill{{display:inline-flex;align-items:center;gap:22px;padding:26px 46px;border-radius:120px;background:var(--yellow);color:#1a1205;font:800 46px/1 var(--sans);box-shadow:0 20px 60px rgba(255,200,46,.4)}}
#endc .sm{{font:600 30px/1 var(--sans);letter-spacing:.4em;color:rgba(246,239,228,.75);margin-top:34px;text-indent:.4em}}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL:.3f}" data-width="1080" data-height="1920">

{''.join(vids)}

<div class="clip" id="hookdim" data-start="0" data-duration="{a['tiba']:.3f}" data-track-index="2" style="z-index:3;background:rgba(5,3,6,.6)"></div>
<!-- hook -->
<div class="scene clip" id="hook" data-start="0" data-duration="{a['bila']:.3f}" data-track-index="3">
  <div class="k-small" id="h1">Korang tahu tak</div>
  <div class="k-serif" id="h2">apa perkara</div>
  <div class="k-out" id="h3">PALING</div>
  <div class="k-big" id="h4">MEMALUKAN?</div>
  <div class="k-line" id="h5"></div>
</div>

<!-- conversation motion graphic -->
<div class="scene clip" id="conv" data-start="{a['tiba']:.3f}" data-duration="{a['jangan'] - a['tiba']:.3f}" data-track-index="3">
  <div style="position:absolute;top:300px;left:0;right:0;text-align:center"><span class="chip" id="cchip"><b></b>SITUASI BIASA</span></div>
  <svg width="1080" height="700" viewBox="0 0 1080 700">
    <g id="figL"><circle class="fig" cx="360" cy="170" r="70"/><path class="fig" d="M230 470 Q230 300 360 300 Q490 300 490 470"/></g>
    <g id="figR"><circle class="fig figr" cx="720" cy="170" r="70"/><path class="fig figr" d="M590 470 Q590 300 720 300 Q850 300 850 470"/></g>
    <g id="dots"><circle cx="500" cy="120" r="10" fill="#f3dcaa"/><circle cx="540" cy="120" r="10" fill="#f3dcaa"/><circle cx="580" cy="120" r="10" fill="#f3dcaa"/></g>
    <path id="dist" d="M440 580 L920 580"/>
    <g class="odor" id="odor">
      <path d="M300 300 C270 250 330 220 300 170 C270 120 330 90 300 40"/>
      <path d="M380 290 C350 240 410 210 380 160 C350 110 410 80 380 30"/>
      <path d="M460 300 C430 250 490 220 460 170 C430 120 490 90 460 40"/>
    </g>
  </svg>
  <div class="bb"><div class="t1" id="bb1">SEBAB</div><div class="t2" id="bb2">BAU BADAN</div></div>
</div>

<!-- sweat -->
<div class="scene clip" id="sweat" data-start="{a['jangan']:.3f}" data-duration="{a['past'] - a['jangan']:.3f}" data-track-index="3">
  <div class="hl"><div class="a" id="sw1">JANGAN AMBIL MUDAH</div><div class="b" id="sw2">kebersihan badan</div></div>
  <div class="glass" id="fact"><span class="chip"><b></b>FAKTA RINGKAS</span>
    <div class="f1">Peluh sebenarnya tak berbau.</div>
    <div class="f2">Bau terhasil bila <em>bakteria</em> di kulit memecahkan peluh, terutama di kawasan lembap.</div></div>
  {''.join(f'<svg class="drop" id="dr{k}" style="left:{140 + k * 150}px;top:{820 + (k % 2) * 40}px" viewBox="0 0 44 62"><path d="M22 2 C22 2 4 26 4 40 a18 18 0 0 0 36 0 C40 26 22 2 22 2Z" fill="rgba(200,230,255,.55)" stroke="#e8f6ff" stroke-width="2"/></svg>' for k in range(6))}
</div>

<!-- 3 steps -->
<div class="scene clip" id="steps" data-start="{a['past']:.3f}" data-duration="{a['semes'] - a['past']:.3f}" data-track-index="3">
  <div class="hl"><span class="chip" id="stc"><b></b>3 LANGKAH ASAS</span><div class="b" id="stt" style="margin-top:26px;font-size:112px">Kebersihan Badan</div></div>
  {''.join(f"""<div class="step" id="st{k}" style="top:{720 + k * 290}px"><div class="n">0{k + 1}</div><div><div class="tt">{tt}</div><div class="ss">{ss}</div></div>
    <svg class="tick" width="96" height="96" viewBox="0 0 96 96"><circle cx="48" cy="48" r="42"/><path id="tk{k}" d="M28 50 L43 64 L70 34"/></svg></div>""" for k, (tt, ss) in enumerate([
      ("Mandi secara teratur", "Sekurang-kurangnya 2× sehari"),
      ("Bersih lipatan badan", "Ketiak, leher &amp; celah kulit"),
      ("Guna deodoran", "Jika diperlukan, selepas mandi")]))}
</div>

<!-- mall / rutin -->
<div class="scene clip" id="mall" data-start="{a['semes']:.3f}" data-duration="{a['pastinya'] - a['semes']:.3f}" data-track-index="3">
  <div class="hl"><div class="a" id="ml1">RUTIN MANDI</div><div class="b" id="ml2">lebih mewah</div></div>
</div>

{bq1}

<!-- feature tags -->
<div class="scene clip" id="feats" data-start="{a['dengan'] - 0.12:.3f}" data-duration="{a['jangan2'] - a['dengan'] + 0.12:.3f}" data-track-index="4" style="z-index:24">
  <div class="feat" id="f1"><div class="ix">01 / 03</div><div class="nm">Buih Lembut</div><div class="en">Gentle Foaming</div><div class="bar"></div></div>
  <div class="feat" id="f2"><div class="ix">02 / 03</div><div class="nm">Garam Laut</div><div class="en">Ocean Salt</div><div class="bar"></div></div>
  <div class="feat" id="f3"><div class="ix">03 / 03</div><div class="nm">Wangian<br>Feminin</div><div class="en">Aromatherapy</div><div class="bar"></div></div>
  {''.join(f'<i class="bub" id="bu{k}" style="left:{90 + (k * 137) % 900}px;top:{1300 + (k * 53) % 300}px;width:{36 + (k * 23) % 60}px;height:{36 + (k * 23) % 60}px"></i>' for k in range(10))}
</div>

<!-- kinetic: jangan tunggu -->
<div class="scene clip" id="kin" data-start="{a['jangan2']:.3f}" data-duration="{a['tekan'] - a['jangan2']:.3f}" data-track-index="3">
  <div class="k1" id="kn1">JANGAN TUNGGU</div>
  <div class="k2" id="kn2">orang tegur</div>
  <div class="k3" id="kn3">BARU NAK</div>
  <div class="k4" id="kn4">AMBIL TINDAKAN</div>
</div>

<!-- shop UI -->
<div class="scene clip" id="shop" data-start="{a['tekan']:.3f}" data-duration="{a['teruta'] - a['tekan']:.3f}" data-track-index="3">
  <div class="dim" style="background:rgba(8,6,8,.55)"></div>
  <div class="hl"><div class="a" id="sh1">TEKAN <span class="ylw">BEG KUNING</span></div><div class="b" id="sh2" style="font-size:84px">sekarang juga</div></div>
  <div id="card">
    <div class="img"><img src="assets/img/red_cut.png"></div>
    <div class="t">Frescura Body</div>
    <div class="s">Gentle Foaming Body Shower · 500ml</div>
    <div class="st">★★★★★</div>
    <div id="ybtn"><svg width="66" height="66" viewBox="0 0 64 64"><path d="M14 22 h36 l-3 34 h-30 z" fill="#1a1205"/><path d="M23 24 v-6 a9 9 0 0 1 18 0 v6" fill="none" stroke="#1a1205" stroke-width="5" stroke-linecap="round"/></svg></div>
    <div id="ybadge">1</div>
  </div>
  <div id="tap"></div>
  <svg id="finger" viewBox="0 0 100 130"><path d="M38 8 a10 10 0 0 1 20 0 v46 l18 4 a12 12 0 0 1 10 14 l-6 34 a14 14 0 0 1 -14 12 h-26 a14 14 0 0 1 -12 -7 l-16 -30 a8 8 0 0 1 12 -9 l14 14 z" fill="#fff" stroke="#1a1205" stroke-width="3"/></svg>
  <img id="fly" src="assets/img/red_cut.png">
  <div id="cartlbl"><span class="chip"><b></b>DITAMBAH KE TROLI</span></div>
</div>

<!-- split variants -->
<div class="scene clip" id="split" data-start="{a['teruta']:.3f}" data-duration="{a['check'] - a['teruta']:.3f}" data-track-index="3">
  <div class="half hL" id="hL"><div class="tint"></div>
    <img id="spr" src="assets/img/red_cut.png"><div class="nm"><div class="x">WOMAN GLORY</div><div class="y" id="nmL">Bombshell</div></div><div class="shade" id="shL"></div></div>
  <div class="half hR" id="hR"><div class="tint"></div>
    <img id="spp" src="assets/img/purple_cut.png"><div class="nm"><div class="x">NOCHE</div><div class="y" id="nmR">Midnight<br>Fantasy</div></div><div class="shade" id="shR"></div></div>
  <div id="divider"></div>
  <div style="position:absolute;top:250px;left:0;right:0;text-align:center;z-index:4"><span class="chip" id="spchip"><b></b>PILIH WANGIAN ANDA</span></div>
</div>

{bq2}

<!-- stock urgency -->
<div class="scene clip" id="stock" data-start="{a['check']:.3f}" data-duration="{a['end'] - a['check']:.3f}" data-track-index="5">
  <div class="glass" id="stg"><div class="c1">CHECK OUT</div><div class="c2">sekarang sebelum kehabisan</div>
    <div class="track"><div id="fill"></div></div>
    <div class="lv"><span><i id="dot"></i>STOK TINGGAL SEDIKIT</span><span id="pct">12%</span></div></div>
  <div id="stamp">STOK TERHAD</div>
</div>

<!-- end card -->
<div id="endc"><div class="pill"><svg width="54" height="54" viewBox="0 0 64 64"><path d="M14 22 h36 l-3 34 h-30 z" fill="#1a1205"/><path d="M23 24 v-6 a9 9 0 0 1 18 0 v6" fill="none" stroke="#1a1205" stroke-width="5" stroke-linecap="round"/></svg>Tekan beg kuning sekarang</div>
  <div class="sm">BOMBSHELL &nbsp;·&nbsp; MIDNIGHT FANTASY</div></div>
<div class="logo" id="endlogo" style="z-index:20;opacity:0"><svg class="ring" viewBox="0 0 600 600"><circle id="endring" cx="300" cy="300" r="280"/></svg>
  <div class="lg1">FRESCURA BODY</div><div class="lg2">SOFT &nbsp;|&nbsp; FRAGRANT</div></div>

{''.join(cap_html)}

<div id="shade"></div>
<div id="vig"></div>
<div id="grain"></div>
<div class="leak" id="lk"></div>
<div id="flash"></div>
<div id="bug"><i></i>FRESCURA BODY<i></i></div>
<div id="prog"></div>
<audio id="mix" src="assets/audio/mix.wav" data-start="0" data-duration="{TOTAL:.3f}" data-track-index="0" data-volume="1"></audio>
</div>

<script>
const tl = gsap.timeline({{ paused: true }});
const E = "expo.out";
function leak(at, d){{ d = d || .42; tl.set("#lk",{{x:-1300,opacity:1}},at); tl.to("#lk",{{x:1300,duration:d,ease:"power2.inOut"}},at); tl.set("#lk",{{opacity:0}},at+d+0.001); }}
function flash(at, o){{ tl.set("#flash",{{opacity:o||.55}},at); tl.to("#flash",{{opacity:0,duration:.35,ease:"power2.out"}},at); }}
tl.set("#lk",{{x:-1300,opacity:0}},0); tl.set("#flash",{{opacity:0}},0);
function punch(sel, at){{ tl.fromTo(sel,{{scale:1.18}},{{scale:1,duration:.45,ease:E}},at); }}
function shake(sel, at){{ tl.fromTo(sel,{{x:-14}},{{x:0,duration:.35,ease:"elastic.out(1.2,0.3)"}},at); }}

// global
tl.fromTo("#prog",{{scaleX:0}},{{scaleX:1,duration:{TOTAL:.3f},ease:"none"}},0);
tl.fromTo("#grain",{{x:0,y:0}},{{x:-160,y:120,duration:{TOTAL:.3f},ease:"steps(260)"}},0);
tl.fromTo("#bug",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:.6,ease:E}},.1);
tl.to("#bug",{{opacity:0,duration:.3}},{a['end'] - 0.2:.3f});

// b-roll ken burns + cut glow
{chr(10).join(kb)}
tl.fromTo("#hookdim",{{opacity:1}},{{opacity:.25,duration:.4}},{a['bila'] - 0.2:.3f});

// HOOK
tl.fromTo("#h1",{{opacity:0,y:30,scaleX:1.35}},{{opacity:1,y:0,scaleX:1,duration:.5,ease:E}},0.02);
tl.fromTo("#h2",{{opacity:0,y:50,filter:"blur(12px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.45,ease:E}},{t("apa"):.3f});
tl.fromTo("#h3",{{opacity:0,scale:1.6}},{{opacity:1,scale:1,duration:.4,ease:E}},{t("paling"):.3f});
tl.fromTo("#h4",{{opacity:0,scale:2.2,filter:"blur(20px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:.38,ease:E}},{t("memalukan"):.3f});
tl.to("#h5",{{width:520,duration:.6,ease:E}},{t("memalukan") + 0.1:.3f});
shake("#hook",{t("memalukan"):.3f}); flash({t("memalukan"):.3f},.45);
tl.to("#hook",{{opacity:0,scale:.9,filter:"blur(12px)",duration:.22}},{a['bila'] - 0.18:.3f});

// CONVERSATION
leak({a['tiba'] - 0.18:.3f});
tl.fromTo("#cchip",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:.4,ease:E}},{a['tiba']:.3f});
tl.fromTo(["#figL","#figR"],{{opacity:0,y:80}},{{opacity:1,y:0,duration:.45,stagger:.08,ease:E}},{a['tiba']:.3f});
tl.fromTo("#dots circle",{{opacity:0,scale:0,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:.2,stagger:.08,ease:"back.out(3)"}},{a['tiba'] + 0.3:.3f});
tl.to("#dots",{{opacity:0,duration:.15}},{a['menjauh']:.3f});
tl.to("#figR",{{x:200,rotation:8,transformOrigin:"50% 100%",duration:.5,ease:"power3.out"}},{a['menjauh']:.3f});
tl.fromTo("#dist",{{strokeDashoffset:500,opacity:0}},{{strokeDashoffset:0,opacity:1,duration:.5,ease:"power2.out"}},{a['menjauh'] + 0.1:.3f});
tl.fromTo("#odor path",{{opacity:0,y:60}},{{opacity:.9,y:-10,duration:.7,stagger:.1,ease:"sine.out"}},{a['bau'] - 0.1:.3f});
tl.to("#odor path",{{y:-60,opacity:0,duration:.5,stagger:.08,ease:"sine.in"}},{a['bau'] + 0.62:.3f});
tl.fromTo("#bb1",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.3,ease:E}},{t("sebab"):.3f});
tl.fromTo("#bb2",{{opacity:0,scale:1.8,filter:"blur(16px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:.35,ease:E}},{a['bau']:.3f});
shake("#bb2",{a['bau'] + 0.05:.3f});

// SWEAT
leak({a['jangan'] - 0.2:.3f});
tl.fromTo("#sw1",{{opacity:0,y:-40}},{{opacity:1,y:0,duration:.4,ease:E}},{a['jangan']:.3f});
tl.fromTo("#sw2",{{opacity:0,y:30,filter:"blur(10px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.45,ease:E}},{a['keb']:.3f});
tl.fromTo("#fact",{{opacity:0,y:160}},{{opacity:1,y:0,duration:.55,ease:E}},{FACT_T:.3f});
tl.fromTo(".drop",{{opacity:0,y:-120}},{{opacity:1,y:60,duration:.6,stagger:.06,ease:"power2.in"}},{a['peluh'] - 0.2:.3f});
tl.to(".drop",{{opacity:0,y:140,duration:.3,stagger:.06}},{a['peluh'] + 0.4:.3f});

// STEPS
flash({a['past']:.3f},.35);
tl.fromTo("#stc",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:.4,ease:E}},{a['past']:.3f});
tl.fromTo("#stt",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.45,ease:E}},{a['past'] + 0.08:.3f});
{chr(10).join(f'tl.fromTo("#st{k}",{{opacity:0,x:-200,filter:"blur(10px)"}},{{opacity:1,x:0,filter:"blur(0px)",duration:.45,ease:E}},{tk:.3f}); tl.to("#tk{k}",{{strokeDashoffset:0,duration:.35,ease:"power2.out"}},{tk + 0.25:.3f});' for k, tk in enumerate([t("mandi"), a['bers'], a['guna']]))}
tl.to("#steps .step",{{opacity:0,x:120,duration:.2,stagger:.04}},{a['semes'] - 0.22:.3f});

// MALL
leak({a['semes'] - 0.2:.3f});
tl.fromTo("#ml1",{{opacity:0,scaleX:1.4}},{{opacity:1,scaleX:1,duration:.6,ease:E}},{a['rutin']:.3f});
tl.fromTo("#ml2",{{opacity:0,y:40,filter:"blur(12px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.5,ease:E}},{a['menarik'] - 0.1:.3f});

// BOUTIQUE REVEAL
{bq1js}
flash({a['pastinya']:.3f},.6);
tl.fromTo("#bq1logo",{{opacity:0,scale:.85}},{{opacity:1,scale:1,duration:.6,ease:E}},{a['fb'] - 0.05:.3f});
tl.to("#bq1ring",{{strokeDashoffset:0,duration:.9,ease:"power2.inOut"}},{a['fb'] - 0.05:.3f});
flash({a['fb']:.3f},.5);

// FEATURES
leak({a['dengan'] - 0.3:.3f},.36);
{chr(10).join(f'tl.fromTo("#f{k + 1}",{{opacity:0,x:-120}},{{opacity:1,x:0,duration:.4,ease:E}},{s0:.3f}); tl.fromTo("#f{k + 1} .bar",{{scaleX:0}},{{scaleX:1,duration:.5,ease:E}},{s0 + 0.1:.3f}); tl.to("#f{k + 1}",{{opacity:0,x:80,duration:.18}},{s1 - 0.12:.3f});' for k, (s0, s1) in enumerate([(a['dengan'] - 0.05, a['garam']), (a['garam'], a['wangi']), (a['wangi'], a['jangan2'])]))}
tl.fromTo(".bub",{{opacity:0,y:120,scale:.4}},{{opacity:1,y:-260,scale:1,duration:1.1,stagger:.05,ease:"sine.out"}},{a['buih'] - 0.25:.3f});
tl.to(".bub",{{opacity:0,duration:.2,stagger:.02}},{a['buih'] + 0.95:.3f});

// KINETIC
flash({a['jangan2']:.3f},.4);
tl.fromTo("#kn1",{{opacity:0,y:60,scale:1.3}},{{opacity:1,y:0,scale:1,duration:.35,ease:E}},{a['jangan2']:.3f});
tl.fromTo("#kn2",{{opacity:0,filter:"blur(14px)",y:30}},{{opacity:1,filter:"blur(0px)",y:0,duration:.4,ease:E}},{t("orang", 2):.3f});
tl.fromTo("#kn3",{{opacity:0}},{{opacity:1,duration:.3}},{t("baru"):.3f});
tl.fromTo("#kn4",{{opacity:0,scale:1.9}},{{opacity:1,scale:1,duration:.35,ease:E}},{a['tindakan']:.3f});
shake("#kn4",{a['tindakan'] + 0.05:.3f});

// SHOP
leak({a['tekan'] - 0.2:.3f});
tl.fromTo("#sh1",{{opacity:0,y:-40}},{{opacity:1,y:0,duration:.4,ease:E}},{a['tekan']:.3f});
tl.fromTo("#sh2",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.4,ease:E}},{t("sekarang"):.3f});
tl.fromTo("#card",{{opacity:0,y:200,rotationX:18}},{{opacity:1,y:0,rotationX:0,duration:.6,ease:E}},{a['tekan']:.3f});
tl.fromTo("#finger",{{opacity:0,x:120,y:160}},{{opacity:1,x:0,y:0,duration:.35,ease:"power3.out"}},{a['kuning'] - 0.35:.3f});
tl.to("#finger",{{scale:.9,duration:.08,yoyo:true,repeat:1}},{a['kuning']:.3f});
tl.to("#ybtn",{{scale:.86,duration:.08,yoyo:true,repeat:1}},{a['kuning']:.3f});
tl.fromTo("#tap",{{opacity:.9,scale:.3}},{{opacity:0,scale:1.8,duration:.5,ease:"power2.out"}},{a['kuning']:.3f});
tl.to("#finger",{{opacity:0,y:120,duration:.3}},{a['kuning'] + 0.35:.3f});
tl.fromTo("#fly",{{opacity:0,x:0,y:0,scale:1}},{{opacity:1,duration:.1}},{a['masuk']:.3f});
tl.to("#fly",{{x:430,y:600,scale:.18,rotation:25,duration:.6,ease:"power2.in"}},{a['masuk'] + 0.05:.3f});
tl.set("#fly",{{opacity:0}},{a['masuk'] + 0.66:.3f});
tl.fromTo("#ybadge",{{opacity:0,scale:0}},{{opacity:1,scale:1,duration:.4,ease:"back.out(3)"}},{a['masuk'] + 0.66:.3f});
tl.fromTo("#cartlbl",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.35,ease:E}},{a['masuk'] + 0.7:.3f});

// SPLIT
flash({a['teruta']:.3f},.4);
tl.fromTo("#spchip",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:.4,ease:E}},{a['teruta'] + 0.2:.3f});
tl.fromTo(["#spr","#spp"],{{y:160,opacity:0}},{{y:0,opacity:1,duration:.55,stagger:.1,ease:E}},{a['teruta'] + 0.1:.3f});
tl.to("#shR",{{opacity:1,duration:.25}},{a['bomb'] - 0.05:.3f});
tl.to("#spr",{{scale:1.08,duration:.5,ease:E}},{a['bomb'] - 0.05:.3f});
tl.fromTo("#nmL",{{scale:1.4,color:"#ffffff"}},{{scale:1,color:"#f3dcaa",duration:.4,ease:E}},{a['bomb']:.3f});
tl.to("#shR",{{opacity:0,duration:.25}},{a['mid'] - 0.1:.3f});
tl.to("#shL",{{opacity:1,duration:.25}},{a['mid'] - 0.1:.3f});
tl.to("#spr",{{scale:1,duration:.4}},{a['mid'] - 0.1:.3f});
tl.to("#spp",{{scale:1.08,duration:.5,ease:E}},{a['mid'] - 0.1:.3f});
tl.fromTo("#nmR",{{scale:1.4,color:"#ffffff"}},{{scale:1,color:"#d9c8ff",duration:.4,ease:E}},{a['mid']:.3f});

// STOCK + END
{bq2js}
flash({a['check']:.3f},.5);
tl.fromTo("#stg",{{opacity:0,y:-120}},{{opacity:1,y:0,duration:.5,ease:E}},{a['check']:.3f});
tl.fromTo("#fill",{{scaleX:.62}},{{scaleX:.12,duration:1.4,ease:"power2.inOut"}},{a['check'] + 0.2:.3f});
tl.fromTo("#dot",{{opacity:1}},{{opacity:.2,duration:.25,repeat:7,yoyo:true}},{a['check']:.3f});
tl.fromTo("#stamp",{{opacity:0,scale:2.4}},{{opacity:1,scale:1,duration:.28,ease:"power4.in"}},{a['terhad'] - 0.2:.3f});
shake("#stamp",{a['terhad'] + 0.08:.3f}); flash({a['terhad'] + 0.08:.3f},.3);
tl.to(["#stg","#stamp"],{{opacity:0,y:-60,duration:.3}},{a['end'] - 0.1:.3f});
tl.fromTo("#endlogo",{{opacity:0,scale:.85}},{{opacity:1,scale:1,duration:.6,ease:E}},{a['end']:.3f});
tl.fromTo("#endring",{{strokeDashoffset:1760}},{{strokeDashoffset:0,duration:1,ease:"power2.inOut"}},{a['end']:.3f});
tl.fromTo("#endc",{{opacity:0,y:60}},{{opacity:1,y:0,duration:.5,ease:E}},{a['end'] + 0.25:.3f});
tl.to("#endc .pill",{{scale:1.06,duration:.35,yoyo:true,repeat:3,ease:"sine.inOut"}},{a['end'] + 0.8:.3f});
leak({a['end'] + 0.1:.3f},.6);

// captions
{chr(10).join(cap_js)}

window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body>
</html>
'''
open(OUT, "w").write(html_out)
print("wrote", OUT, "groups", len(groups))
print(json.dumps(A))
