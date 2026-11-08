# Generates the HyperFrames composition (index.html) for the FRESCURA BODY ad from timeline.py
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from timeline import *

OUTDIR = sys.argv[1]
caps = captions()
for g in caps:
    lim = FB_END + 0.05 if g["words"][0][1] < FB_END else END[0] + 0.05
    g["end"] = min(g["end"], lim)

PIP0 = round(f(7.60), 3); PIP1 = round(f(12.20), 3)
Q = lambda x: f"{x:.3f}"

def cap_html():
    h = []
    for i, g in enumerate(caps):
        spans = []
        for j, (w, a, b, k) in enumerate(g["words"]):
            cls = "w k" if k else "w"
            spans.append(f'<span class="{cls}" id="c{i}w{j}">{w}</span>')
        if g["kind"] == "q":
            h.append(f'<div class="cap q" id="c{i}"><span class="qmark">Q —</span>{" ".join(spans)}</div>')
        else:
            h.append(f'<div class="cap {g["kind"]}" id="c{i}">{" ".join(spans)}</div>')
    return "\n".join(h)

def vid(id_, src, start, dur, mstart=0.0, extra=""):
    return (f'<video id="{id_}" class="clip vid" src="assets/video/{src}" data-start="{Q(start)}" '
            f'data-duration="{Q(dur)}" data-media-start="{Q(mstart)}" muted playsinline {extra}></video>')

def scene(id_, start, dur, inner, cls=""):
    return f'<div id="{id_}" class="clip scene {cls}" data-start="{Q(start)}" data-duration="{Q(dur)}">{inner}</div>'

ICON_WAVE = '<svg viewBox="0 0 64 64"><path d="M6 26c6-6 12-6 18 0s12 6 18 0 12-6 16-2M6 38c6-6 12-6 18 0s12 6 18 0 12-6 16-2" /></svg>'
ICON_LEAF = '<svg viewBox="0 0 64 64"><path d="M14 50C14 26 30 12 54 10c0 24-14 40-38 40zM14 50l22-22" /></svg>'
ICON_BUBBLE = '<svg viewBox="0 0 64 64"><circle cx="24" cy="36" r="14"/><circle cx="44" cy="22" r="8"/><circle cx="46" cy="46" r="5"/></svg>'
BAG = '''<svg viewBox="0 0 200 220" class="bag"><path d="M28 70h144l-12 132a14 14 0 0 1-14 12H54a14 14 0 0 1-14-12z" fill="#FFC531"/>
<path d="M28 70h144l-3 30H31z" fill="#F2A900" opacity=".55"/><path d="M68 92V60a32 32 0 0 1 64 0v32" fill="none" stroke="#1a1408" stroke-width="12" stroke-linecap="round"/>
<circle cx="68" cy="96" r="8" fill="#1a1408"/><circle cx="132" cy="96" r="8" fill="#1a1408"/></svg>'''
STAMP = '''<svg viewBox="0 0 300 300" class="stampsvg"><defs><path id="sc" d="M150,150 m-112,0 a112,112 0 1,1 224,0 a112,112 0 1,1 -224,0"/></defs>
<circle cx="150" cy="150" r="140" fill="none" stroke="currentColor" stroke-width="5"/><circle cx="150" cy="150" r="88" fill="none" stroke="currentColor" stroke-width="2"/>
<text font-family="Outfit" font-weight="800" font-size="27" letter-spacing="7" fill="currentColor"><textPath href="#sc">REAL REVIEW ✦ TAK TIPU ✦ REAL REVIEW ✦</textPath></text>
<text x="150" y="168" text-anchor="middle" font-family="Bodoni Moda" font-style="italic" font-weight="700" font-size="64" fill="currentColor">100%</text></svg>'''

body = []
# ---------------- VIDEO / IMAGE BACKGROUNDS ----------------
body.append(vid("v_hook1", "pump_press.mp4", 0, 2.66, 0.0))
body.append(vid("v_hook2", "pump_close.mp4", 2.66, 2.84, 0.3))
body.append(vid("v_fb", "feedback_cut.mp4", FB_OUT, FB_END - FB_OUT, 0.0))
body.append(vid("v_pip", "pump_close.mp4", PIP0, PIP1 - PIP0, 0.2))
body.append(f'<img id="i_cta" class="clip bgimg" src="assets/img/products.jpg" data-start="{Q(CL)}" data-duration="{Q(S2-CL)}" />')
body.append(vid("v_stock", "pump_press.mp4", S2, S3 - S2, 0.6))
body.append(vid("v_voucher", "foam_lather.mp4", S3, S4 - S3, 1.2))

# ---------------- SCENES ----------------
body.append(scene("s_hook", 0, 2.66, f'''
  <div class="tint" style="background:linear-gradient(180deg,rgba(8,6,8,.72),rgba(8,6,8,.45) 45%,rgba(8,6,8,.85))"></div>
  <div id="hk" class="center-stack" style="top:560px">
    <div id="hk_eyebrow" class="eyebrow">FRESCURA BODY &nbsp;·&nbsp; REAL REVIEW</div>
    <div id="hk1" class="mega" style="font-size:168px">{"".join(f'<span class="ch">{c}</span>' for c in "APA KATA")}</div>
    <div id="hk2" class="serif-xl">pelanggan<span class="gold">?</span></div>
    <div id="hk_line" class="hairline"></div>
  </div>
  <div id="pc_wrap"><div id="pc_word" class="wordmark">FRESCURA BODY</div>
    <div id="pcard" class="card"><img src="assets/img/products.jpg"/><div id="pc_sheen" class="sheen"></div></div>
</div>
'''))
body.append(scene("s_hook2", 2.66, 2.94, f'''
  <div class="tint" style="background:linear-gradient(180deg,rgba(8,6,8,.75),rgba(8,6,8,.25) 50%,rgba(8,6,8,.8))"></div>
  <div class="center-stack" style="top:300px">
    <div id="tg1" class="mega" style="font-size:180px">TENGOK</div>
    <div id="tg2" class="serif-xl" style="margin-top:-30px">sendiri<span class="gold">.</span></div>
    <div id="tg_line" class="hairline"></div>
  </div>
  <div id="rec" class="pill glass" style="top:820px"><span class="dot"></span>REAL FEEDBACK</div>
'''))
body.append(scene("s_fb", FB_OUT, FB_END - FB_OUT, f'''
  <div class="tint" style="background:linear-gradient(180deg,rgba(8,6,8,.55),rgba(8,6,8,0) 30%,rgba(8,6,8,0) 62%,rgba(8,6,8,.7))"></div>
  <div id="fb_tag" class="pill glass" style="top:150px;left:72px"><span class="dot"></span>PELANGGAN SEBENAR</div>
  <div id="b_lembut" class="badge glass" style="top:560px;right:70px">
    <div class="b-ico">✦</div><div class="b-serif">lembut</div><div class="b-sans">SANGAT</div></div>
  <div id="glory" class="minicard"><img src="assets/img/glory.jpg"/><div class="mc-cap"><b>WOMAN GLORY</b><i>Bombshell</i></div></div>
  <svg id="scent" viewBox="0 0 300 400"><path id="sc1" d="M60 390 C 20 300, 110 260, 70 170 S 120 40, 90 0"/><path id="sc2" d="M150 390 C 110 300, 200 260, 160 170 S 210 40, 180 0"/><path id="sc3" d="M240 390 C 200 300, 290 260, 250 170 S 300 40, 270 0"/></svg>
  <div id="b_wangi" class="badge glass" style="top:430px;left:70px"><div class="b-ico">✓</div><div class="b-serif">wangi</div><div class="b-sans">MEMANG WANGI</div></div>
  <div id="stamp">{STAMP}</div>
  <div id="pip_frame"><div id="pip_res" class="pip-res">makin <i>lembut</i> ✦</div></div>
  <div id="thanks" class="thanks"><i>terima kasih</i><span>atas review jujur ♡</span></div>
'''))
body.append(scene("s_cta1", CL, S2 - CL, f'''
  <div class="tint" style="background:linear-gradient(180deg,rgba(8,6,8,.7),rgba(8,6,8,.1) 40%,rgba(8,6,8,.75))"></div>
  <div class="center-stack" style="top:230px">
    <div id="nk1" class="mega" style="font-size:170px">NAK</div>
    <div id="nk2" class="serif-xl" style="margin-top:-36px">cuba<span class="gold">?</span></div>
  </div>
  <div id="co_btn" class="cta-btn" style="top:1090px">CHECK OUT <span>⟶</span><div id="co_ring" class="ring"></div></div>
'''))
body.append(scene("s_stock", S2, S3 - S2, f'''
  <div class="tint" style="background:radial-gradient(ellipse at 50% 40%,rgba(60,6,16,.55),rgba(8,4,6,.92) 75%)"></div>
  <div class="center-stack" style="top:300px">
    <div id="st1" class="outline">STOK</div>
    <div id="st2" class="serif-xl rose" style="margin-top:-40px">terhad<span>!</span></div>
  </div>
  <div id="stockbox" class="glass panel" style="top:820px">
    <div class="sb-top"><span class="eyebrow">BAKI STOK · TIKTOK SHOP</span><span id="sb_hot" class="hot">HAMPIR HABIS</span></div>
    <div class="track big"><div id="s_fill" class="fill rosefill"></div></div>
    <div class="ticks">{"".join("<i></i>" for _ in range(20))}</div>
  </div>
  <div id="glitchR" class="glitch-layer r">terhad!</div><div id="glitchC" class="glitch-layer c">terhad!</div>
'''))
body.append(scene("s_voucher", S3, S4 - S3, f'''
  <div class="tint" style="background:linear-gradient(180deg,rgba(8,6,8,.8),rgba(8,6,8,.45) 50%,rgba(8,6,8,.85))"></div>
  <div class="center-stack" style="top:250px">
    <div id="vc1" class="eyebrow" style="font-size:30px">CUBA TENGOK</div>
    <div id="vc2" class="serif-xl" style="font-size:150px">berapa<span class="gold">?</span></div>
  </div>
  <div id="ticket"><div class="t-left"><div class="eyebrow ink" style="font-size:22px">VOUCHER</div><div class="t-serif">TikTok Shop</div><div class="t-small">untuk korang</div></div>
    <div class="t-div"></div><div class="t-right"><div class="t-rm">RM</div><div class="t-q"><span id="q1">?</span><span id="q2">?</span><span id="q3">?</span></div></div>
    <div id="t_sheen" class="sheen"></div></div>
'''))
body.append(scene("s_bag", S4, END[0] - S4, f'''
  <div class="tint" style="background:radial-gradient(circle at 50% 42%,#2a2210 0%,#0c0a08 60%)"></div>
  <div class="center-stack" style="top:190px">
    <div id="tk1" class="mega" style="font-size:160px">TEKAN</div>
    <div id="tk2" class="serif-xl yellow" style="margin-top:-30px;font-size:150px">beg kuning</div>
  </div>
  <div id="bagwrap">{BAG}<div id="ripple1" class="ripple"></div><div id="ripple2" class="ripple"></div>
    <div id="finger" class="finger"></div></div>
  <div id="arrow" class="arrow-dl">↙</div>
  <div id="co2" class="cta-btn yellowbtn" style="top:1170px">CHECK OUT SEKARANG</div>
'''))
body.append(scene("s_end", END[0], END[1] - END[0], f'''
  <div style="position:absolute;inset:0;background:#000"></div>
  <div id="logo_glow"></div>
  <img id="logo" src="assets/img/logo.jpg"/>
  <div id="end_t1" class="eyebrow" style="position:absolute;top:1340px;width:100%;text-align:center;font-size:28px">DAPATKAN DI TIKTOK SHOP</div>
  <div id="end_t2" class="e-title" style="top:1400px;color:#f4eee6;font-size:78px"><i>Noche</i> <span class="sans" style="font-size:50px">&amp;</span> <i>Woman Glory</i></div>
  <div id="fadeout" style="position:absolute;inset:0;background:#000;opacity:0"></div>
'''))

# persistent overlays
overlays = f'''
<div id="caps" class="clip" data-start="0" data-duration="{Q(TOTAL)}">{cap_html()}</div>
<div id="frame" class="clip" data-start="0" data-duration="{Q(END[0])}">
  <div class="fr-border"></div>
  <div class="fr-tl">FRESCURA BODY</div><div class="fr-tr">Nº 01 — REVIEW</div>
  <div class="fr-bl">SOFT | FRAGRANT</div><div id="fr_time" class="fr-br">500 ML</div>
</div>
<div id="fx" class="clip" data-start="0" data-duration="{Q(TOTAL)}">
  <div id="flash"></div><div id="iris"></div>
  <div id="grain"></div><div id="vignette"></div>
</div>
<audio id="mix" src="assets/audio/mix.wav" data-start="0" data-duration="{Q(TOTAL)}" data-volume="1"></audio>
'''

CSS = open(os.path.join(os.path.dirname(__file__), "style.css")).read()
JS = open(os.path.join(os.path.dirname(__file__), "anim.js")).read()
consts = dict(FB_OUT=FB_OUT, FB_END=FB_END, CL=CL, S2=S2, S3=S3, S4=S4, PIP0=PIP0, PIP1=PIP1, TERIMA=f(18.24), END0=END[0], END1=END[1], TOTAL=TOTAL,
              LEMBUT=f(5.16), LAMA=f(7.66), LEMBUT2=f(8.64), WANGI_Q=f(12.86), WANGI=f(14.28), TIPU=f(15.96),
              CUBA=m(8.84), CEPAT=m(9.38), CHECK=m(10.06), TIKTOK=m(11.80), SANGAT=m(12.84), TERHAD=m(13.76),
              BERAPA=m(15.18), TIKTOK2=m(15.96), TEKAN=m(17.14), BEG=m(17.50), CHECK2=m(18.20))
html = f'''<!doctype html>
<html lang="ms" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
{open(os.path.join(OUTDIR, "assets/fonts/fonts.css")).read()}
{CSS}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{Q(TOTAL)}" data-width="1080" data-height="1920" data-fps="30">
<div id="stage">
{chr(10).join(body)}
</div>
{overlays}
</div>
<script>
const C = {json.dumps(consts)};
const CAPS = {json.dumps([dict(kind=g["kind"], start=g["start"], end=g["end"], words=[[w, a, b, k] for w, a, b, k in g["words"]]) for g in caps], ensure_ascii=False)};
{JS}
</script>
</body>
</html>
'''
open(os.path.join(OUTDIR, "index.html"), "w").write(html)
print("wrote index.html", len(html))
