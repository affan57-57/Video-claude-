"""Generate the HyperFrames composition (index.html) for the Frescura Body ad
from the retimed word transcript. Usage: python build.py words_edit.json OUT_index.html"""
import json, sys, html

WORDS, OUT = sys.argv[1], sys.argv[2]
O = 0.30            # voice-over starts 0.3s in (hook impact first)
END = 34.0          # total film length
W = json.load(open(WORDS))
for w in W: w["s"] += O; w["e"] += O

# -------- transcript clean-up (whisper mishearings -> real script) --------
FIX = {"mengenui": "mengandungi", "menyelar": "menyerlah", "mystery.": "misteri.", "noche": "Noche",
       "midnight": "Midnight", "fantasy": "Fantasy", "woman": "Woman", "glory": "Glory",
       "bombshell": "Bombshell", "Self": "Self-care", "checkout": "checkout"}
clean = []
for i, w in enumerate(W):
    t = w["t"]
    if t == "dari" and i > 0 and W[i - 1]["t"] == "glory": continue      # "Woman Glory Bombshell"
    if t == "care" and i > 0 and W[i - 1]["t"] == "Self": clean[-1]["e"] = w["e"]; continue
    clean.append(dict(t=FIX.get(t, t), s=w["s"], e=w["e"]))
# "Kamu" timing from whisper is clamped to the cut; trust the cut start
ACCENT = {"penat,", "mahal.", "selesa.", "Frescura", "Body", "garam", "laut,", "mineral", "kulit.", "perfume",
          "memanjakan", "Woman", "Glory", "Bombshell", "menyerlah", "Noche", "Midnight", "Fantasy", "misteri.",
          "giliran", "terhad.", "sekarang.", "Self-care", "diri", "sendiri."}
GOLD_ONLY = {"kuning"}

# -------- caption groups (skip hook, it has its own kinetic type) --------
HOOK_END = 3.25
groups, cur = [], []
for w in clean:
    if w["s"] < HOOK_END: continue
    if cur and (len(cur) >= 3 or w["s"] - cur[-1]["e"] > 0.28 or cur[-1]["t"][-1] in ",."):
        groups.append(cur); cur = []
    cur.append(w)
groups.append(cur)
TEKAN = [w["s"] for w in clean if w["t"] == "Tekan"][0]
groups = [g for g in groups if g[0]["s"] < TEKAN - 0.05]
CAP_END = TEKAN - 0.05


def esc(s): return html.escape(s, quote=True)


cap_html, cap_js = [], []
for gi, g in enumerate(groups):
    s = g[0]["s"] - 0.04
    e = groups[gi + 1][0]["s"] - 0.04 if gi + 1 < len(groups) else CAP_END
    spans = []
    for wi, w in enumerate(g):
        cls = "w acc" if w["t"] in ACCENT else ("w gold" if w["t"] in GOLD_ONLY else "w")
        spans.append(f'<span class="{cls}" id="cw{gi}_{wi}">{esc(w["t"])}</span>')
        cap_js.append(f'tl.fromTo("#cw{gi}_{wi}",{{opacity:.38,y:10,scale:.96}},{{opacity:1,y:0,scale:1,duration:.16,ease:"power3.out"}},{w["s"]:.3f});')
    cap_html.append(f'<div class="cap clip" id="cg{gi}" data-start="{s:.3f}" data-duration="{e - s:.3f}" data-track-index="9">{" ".join(spans)}</div>')
    cap_js.append(f'tl.fromTo("#cg{gi}",{{opacity:0,y:34,filter:"blur(10px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.22,ease:"expo.out"}},{s:.3f});')


def t(word, n=0):
    """start time of the n-th occurrence of a cleaned word"""
    hits = [w["s"] for w in clean if w["t"].strip(",.").lower() == word.lower()]
    return hits[n]


T = dict(
    hook_masa=t("masa"), self=t("Self-care"), mahal=t("mahal"), ianya=t("Ianya"), mandi=t("mandi"), selesa=t("selesa"),
    fres=t("Frescura"), garam=t("garam"), bahan=t("bahan"), kaya=t("kaya"), mineral=t("mineral"), sudah=t("sudah"),
    kulit=t("kulit"), gab=t("Digabungkan"), perfume=t("perfume"), setiap=t("setiap"), terasa=t("terasa"),
    manjakan=t("memanjakan"), pilih=t("Pilih"), bomb=t("Bombshell"), manis1=t("manis"), serlah=t("menyerlah"),
    ataupun=t("ataupun"), noche=t("Noche"), manis2=t("manis", 1), lembut=t("lembut"), misteri=t("misteri"),
    kamu=23.936 + O, orang=t("orang"), sekarang1=t("Sekarang"), giliran=t("giliran"), stok=t("Stok"), terhad=t("terhad"),
    klik=t("Klik"), tekan=t("Tekan"), kuning=t("kuning"), checkout=t("checkout"), sekarang2=t("sekarang", 1),
)
json.dump({k: round(v, 3) for k, v in T.items()}, open(OUT.replace(".html", "_cues.json"), "w"), indent=1)
S = {k: round(v - 0.06, 3) for k, v in T.items()}   # scene cuts land a hair before the word

# Scene boundaries
B = dict(s1a=0.0, s1b=1.55, s2=S["self"], s2b=S["ianya"], s3=S["fres"], s3b=S["garam"], s3c=S["sudah"],
         s4=S["gab"], s4b=S["setiap"], s5=S["pilih"], s6=S["ataupun"], s7=S["kamu"], s7b=S["sekarang1"],
         s8=S["stok"], s9=S["klik"], s10=32.30)
def dur(a, b): return round(B[b] - B[a], 3)

# salt crystals (deterministic positions)
crystals = []
import math
for k in range(26):
    x = (k * 397) % 1000 / 1000 * 1000 + 40; y = (k * 653) % 1000 / 1000 * 1500 + 180
    sz = 10 + (k * 31) % 26; r = (k * 47) % 90
    crystals.append(f'<i class="xtal" style="left:{x:.0f}px;top:{y:.0f}px;width:{sz}px;height:{sz}px;transform:rotate({r}deg)"></i>')
sparks = "".join(f'<i class="spk" style="left:{(k*271)%1000+40}px;top:{(k*557)%1600+150}px;--d:{(k%5)*.12:.2f}s"></i>' for k in range(18))

CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..900;1,6..96,400..900&family=DM+Serif+Display:ital@0;1&family=Jost:wght@300;400;500;600;700&display=swap');
:root{--ground:#07070a;--ink:#f6f1e7;--muted:#b9b2a6;--gold:#e7cf9f;--gold2:#c9a96a;--cyan:#5fe3ff;--red:#e0313c;--violet:#9b6bff;--yellow:#ffd23f;
--display:'Bodoni Moda',serif;--cap:'DM Serif Display',serif;--label:'Jost',sans-serif;}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:var(--ground)}
#root{position:relative;width:1080px;height:1920px;overflow:hidden;background:var(--ground);font-family:var(--label);color:var(--ink)}
.clip{position:absolute;inset:0}
.full{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.scrim{position:absolute;inset:0;background:linear-gradient(180deg,rgba(7,7,10,.72) 0%,rgba(7,7,10,.08) 30%,rgba(7,7,10,.10) 58%,rgba(7,7,10,.86) 100%)}
.scrim.heavy{background:radial-gradient(120% 80% at 50% 45%,rgba(7,7,10,.25),rgba(7,7,10,.92))}
.kicker{font-family:var(--label);font-weight:500;letter-spacing:.42em;text-transform:uppercase;font-size:30px;color:var(--gold)}
.disp{font-family:var(--display);font-weight:500;line-height:.92;letter-spacing:-.01em}
.it{font-style:italic}
.center{position:absolute;left:0;right:0;text-align:center}
.rule{display:block;height:2px;background:linear-gradient(90deg,transparent,var(--gold),transparent);margin:0 auto}
/* captions */
.cap{inset:auto 60px 300px 60px;top:auto;height:auto;text-align:center;font-family:var(--cap);font-size:96px;line-height:1.04;color:var(--ink);
 text-shadow:0 4px 30px rgba(0,0,0,.75),0 2px 6px rgba(0,0,0,.6);letter-spacing:.005em}
.cap .w{display:inline-block;margin:0 .1em}
.cap .acc{color:var(--gold);font-style:italic}
.cap .gold{color:var(--yellow);font-style:italic}
/* glass chip */
.chip{display:inline-flex;align-items:center;gap:16px;padding:20px 38px;border-radius:999px;border:1.5px solid rgba(231,207,159,.55);
 background:rgba(12,12,16,.55);backdrop-filter:blur(14px);font-family:var(--label);font-weight:500;font-size:34px;letter-spacing:.24em;text-transform:uppercase;color:var(--ink)}
.chip b{width:12px;height:12px;border-radius:50%;background:var(--gold);box-shadow:0 0 18px var(--gold)}
.xtal{position:absolute;background:linear-gradient(135deg,rgba(255,255,255,.95),rgba(190,230,255,.35));border:1px solid rgba(255,255,255,.7);box-shadow:0 0 22px rgba(160,220,255,.55)}
.spk{position:absolute;width:6px;height:6px;border-radius:50%;background:#fff;box-shadow:0 0 14px 4px rgba(255,240,210,.8)}
.grain{position:absolute;inset:-60px;pointer-events:none;opacity:.075;mix-blend-mode:overlay;
 background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")}
.vig{position:absolute;inset:0;pointer-events:none;background:radial-gradient(110% 75% at 50% 50%,transparent 55%,rgba(0,0,0,.55))}
.flash{position:absolute;inset:0;pointer-events:none;background:radial-gradient(60% 40% at 50% 50%,rgba(255,244,225,.9),rgba(255,244,225,0) 70%);opacity:0;mix-blend-mode:screen}
.bar{position:absolute;left:0;top:0;height:6px;width:1080px;transform-origin:0 50%;background:linear-gradient(90deg,var(--gold2),var(--gold),#fff6e0)}
.frame{position:absolute;inset:34px;border:1.5px solid rgba(231,207,159,.28);border-radius:28px;pointer-events:none}
.idx{position:absolute;top:70px;left:70px;font-family:var(--label);font-size:24px;letter-spacing:.35em;color:rgba(246,241,231,.7)}
.brand{position:absolute;top:70px;right:70px;font-family:var(--label);font-size:24px;letter-spacing:.35em;color:rgba(246,241,231,.7)}
.ring{position:absolute;border-radius:50%;border:2px solid rgba(231,207,159,.6)}
.card{position:absolute;inset:0;background:radial-gradient(90% 60% at 50% 38%,#1a1714 0%,#0a0a0d 62%,#050507 100%)}
.wave path{fill:none;stroke-width:3}
.meter{position:absolute;left:140px;right:140px;height:26px;border-radius:20px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);overflow:hidden}
.meter i{position:absolute;left:0;top:0;bottom:0;width:100%;transform-origin:0 50%;background:linear-gradient(90deg,#ff5a5f,#e0313c)}
.btn{position:absolute;left:170px;right:170px;height:150px;border-radius:999px;background:linear-gradient(180deg,#ffe07a,#ffc81f);color:#141008;
 display:flex;align-items:center;justify-content:center;font-family:var(--label);font-weight:700;font-size:46px;letter-spacing:.2em;box-shadow:0 20px 60px rgba(255,200,31,.35)}
.tapr{position:absolute;width:120px;height:120px;border-radius:50%;border:4px solid #fff;opacity:0}
"""

# ------------------------------------------------------------------ HTML
H = f"""<!doctype html>
<html lang="ms" data-resolution="portrait">
<head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>{CSS}</style></head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1080" data-height="1920">

<!-- ===== S1 HOOK: foam pump B-roll + kinetic type ===== -->
<video id="v1" class="full clip" src="assets/p1.mp4" muted data-track-index="0" data-start="0" data-duration="{B['s1b']+0.2:.3f}" data-media-start="0.2"></video>
<div id="s1a" class="clip" data-start="0" data-duration="{B['s1b']+0.2:.3f}" data-track-index="1">
  <div class="scrim heavy"></div>
  <div class="center" style="top:560px"><div class="kicker" id="h_k">Hari yang</div></div>
  <div class="center disp it" id="h_penat" style="top:640px;font-size:270px;color:var(--ink)">Penat?</div>
  <span class="rule" id="h_rule" style="position:absolute;top:960px;left:290px;width:500px"></span>
</div>
<div id="s1b" class="clip" data-start="{B['s1b']}" data-duration="{B['s2']-B['s1b']+0.1:.3f}" data-track-index="1">
  <img id="i1b" class="full" src="assets/duo_wet.jpg" alt=""/>
  <div class="scrim"></div>
  <div class="center kicker" id="h2_k" style="top:1250px">kamu layak dapat</div>
  <div class="center disp" id="h2_a" style="top:1320px;font-size:140px">Masa untuk</div>
  <div class="center disp it" id="h2_b" style="top:1460px;font-size:160px;color:var(--gold)">diri sendiri.</div>
</div>

<!-- ===== S2 MYTH: self-care tak semestinya mahal ===== -->
<div id="s2" class="clip" data-start="{B['s2']}" data-duration="{dur('s2','s2b')+0.1:.3f}" data-track-index="1">
  <div class="card"></div>
  <div class="center kicker" id="m_k" style="top:330px">Mitos vs Fakta</div>
  <div class="center disp" id="m_a" style="top:420px;font-size:150px">Self-care</div>
  <div class="center disp it" id="m_b" style="top:580px;font-size:190px;color:var(--muted)">= mahal</div>
  <div id="m_strike" style="position:absolute;top:700px;left:300px;width:540px;height:10px;background:var(--red);transform-origin:0 50%;border-radius:6px;box-shadow:0 0 30px rgba(224,49,60,.7)"></div>
  <div class="center" id="m_fakta" style="top:860px"><span class="chip"><b></b>Fakta · tak semestinya</span></div>
  <svg id="m_tag" style="position:absolute;left:400px;top:1000px" width="280" height="200" viewBox="0 0 280 200">
    <path d="M30 40 H190 L250 100 L190 160 H30 Z" fill="none" stroke="#e7cf9f" stroke-width="5" stroke-linejoin="round"/>
    <circle cx="190" cy="100" r="12" fill="none" stroke="#e7cf9f" stroke-width="5"/>
    <text x="100" y="118" text-anchor="middle" font-family="Jost" font-size="54" font-weight="600" fill="#f6f1e7">RM</text>
    <line id="m_tagx" x1="20" y1="180" x2="260" y2="20" stroke="#e0313c" stroke-width="10" stroke-linecap="round"/>
  </svg>
</div>
<video id="v2b" class="full clip" src="assets/p3.mp4" muted data-track-index="0" data-start="{B['s2b']}" data-duration="{dur('s2b','s3')+0.1:.3f}" data-media-start="0"></video>
<div id="s2b" class="clip" data-start="{B['s2b']}" data-duration="{dur('s2b','s3')+0.1:.3f}" data-track-index="1">
  <div class="scrim"></div>
  <div class="center" id="mb_chip" style="top:260px"><span class="chip"><b></b>Bermula di bilik mandi</span></div>
  <div class="center disp it" id="mb_t" style="top:380px;font-size:150px;color:var(--ink)">yang selesa.</div>
</div>

<!-- ===== S3 EDU: Frescura Body + garam laut ===== -->
<div id="s3" class="clip" data-start="{B['s3']}" data-duration="{dur('s3','s3b')+0.1:.3f}" data-track-index="1">
  <div class="card" style="background:#000"></div>
  <img id="logo" src="assets/logo.jpg" alt="" style="position:absolute;left:90px;top:520px;width:900px;height:900px;mix-blend-mode:screen"/>
  <div class="ring" id="lg_ring" style="left:140px;top:570px;width:800px;height:800px;border-color:rgba(95,227,255,.5)"></div>
  <div class="center kicker" id="lg_k" style="top:380px;color:var(--cyan)">Memperkenalkan</div>
</div>
<div id="s3b" class="clip" data-start="{B['s3b']}" data-duration="{dur('s3b','s3c')+0.1:.3f}" data-track-index="1">
  <div class="card" style="background:radial-gradient(90% 60% at 50% 40%,#0c1c24 0%,#071017 55%,#040608 100%)"></div>
  <div id="xtals">{''.join(crystals)}</div>
  <svg class="wave" style="position:absolute;left:0;top:1080px" width="1080" height="260" viewBox="0 0 1080 260">
    <path id="wv1" d="M-20 130 C 120 60, 240 200, 380 130 S 640 60, 780 130 S 1000 200, 1100 130" stroke="rgba(95,227,255,.75)"/>
    <path id="wv2" d="M-20 170 C 140 110, 260 230, 400 170 S 660 110, 800 170 S 1020 230, 1100 170" stroke="rgba(231,207,159,.6)"/>
  </svg>
  <div class="center kicker" id="g_k" style="top:300px;color:var(--cyan)">Bahan utama</div>
  <div class="center disp" id="g_a" style="top:370px;font-size:170px">Garam Laut</div>
  <div class="center disp it" id="g_b" style="top:560px;font-size:70px;color:var(--gold)">bahan semula jadi</div>
  <div id="minerals" style="position:absolute;top:760px;left:0;right:0;display:flex;justify-content:center;gap:26px">
    <div class="mn" id="mn0" style="width:190px;height:190px;border-radius:50%;border:2px solid rgba(95,227,255,.7);display:flex;flex-direction:column;align-items:center;justify-content:center;background:rgba(10,30,40,.6)"><span class="disp" style="font-size:78px">Mg</span><span style="font-size:20px;letter-spacing:.2em">MAGNESIUM</span></div>
    <div class="mn" id="mn1" style="width:190px;height:190px;border-radius:50%;border:2px solid rgba(95,227,255,.7);display:flex;flex-direction:column;align-items:center;justify-content:center;background:rgba(10,30,40,.6)"><span class="disp" style="font-size:78px">Ca</span><span style="font-size:20px;letter-spacing:.2em">KALSIUM</span></div>
    <div class="mn" id="mn2" style="width:190px;height:190px;border-radius:50%;border:2px solid rgba(95,227,255,.7);display:flex;flex-direction:column;align-items:center;justify-content:center;background:rgba(10,30,40,.6)"><span class="disp" style="font-size:78px">K</span><span style="font-size:20px;letter-spacing:.2em">KALIUM</span></div>
  </div>
  <div class="center kicker" id="mn_lbl" style="top:990px;color:var(--ink)">Kaya mineral</div>
</div>
<video id="v3c" class="full clip" src="assets/p2.mp4" muted data-track-index="0" data-start="{B['s3c']}" data-duration="{dur('s3c','s4')+0.1:.3f}" data-media-start="0"></video>
<div id="s3c" class="clip" data-start="{B['s3c']}" data-duration="{dur('s3c','s4')+0.1:.3f}" data-track-index="1">
  <div class="scrim"></div>
  <div class="center kicker" id="sk_k" style="top:250px">Sudah lama digunakan</div>
  <div class="center disp it" id="sk_t" style="top:320px;font-size:96px">dalam penjagaan kulit</div>
  <div class="center" id="sk_chip" style="top:470px"><span class="chip"><b></b>Gentle Foaming</span></div>
</div>

<!-- ===== S4 perfume formula + lather ===== -->
<div id="s4" class="clip" data-start="{B['s4']}" data-duration="{dur('s4','s4b')+0.1:.3f}" data-track-index="1">
  <div class="card"></div>
  <div class="ring" id="rg1" style="left:340px;top:640px;width:400px;height:400px"></div>
  <div class="ring" id="rg2" style="left:340px;top:640px;width:400px;height:400px"></div>
  <div class="ring" id="rg3" style="left:340px;top:640px;width:400px;height:400px"></div>
  <div id="f_a" style="position:absolute;left:90px;top:700px;width:280px;height:280px;border-radius:50%;border:2px solid var(--cyan);display:flex;align-items:center;justify-content:center;text-align:center;font-family:var(--display);font-size:52px;line-height:1">Garam<br/>Laut</div>
  <div id="f_plus" class="disp" style="position:absolute;left:470px;top:740px;width:140px;text-align:center;font-size:150px;color:var(--gold)">+</div>
  <div id="f_b" style="position:absolute;left:710px;top:700px;width:280px;height:280px;border-radius:50%;border:2px solid var(--gold);display:flex;align-items:center;justify-content:center;text-align:center;font-family:var(--display);font-style:italic;font-size:58px;line-height:1">Perfume</div>
  <div class="center kicker" id="f_k" style="top:440px">Formula Frescura</div>
  <div class="center disp it" id="f_eq" style="top:1080px;font-size:110px;color:var(--gold)">= mandi wangi</div>
</div>
<video id="v4b" class="full clip" src="assets/p4.mp4" muted data-track-index="0" data-start="{B['s4b']}" data-duration="{dur('s4b','s5')+0.1:.3f}" data-media-start="0.3"></video>
<div id="s4b" class="clip" data-start="{B['s4b']}" data-duration="{dur('s4b','s5')+0.1:.3f}" data-track-index="1">
  <div class="scrim"></div>
  <div id="spk4">{sparks}</div>
  <div class="center kicker" id="pm_k" style="top:270px">Setiap kali mandi</div>
  <div class="center disp it" id="pm_t" style="top:340px;font-size:150px;color:var(--gold)">memanjakan diri</div>
</div>

<!-- ===== S5 Woman Glory Bombshell ===== -->
<div id="s5" class="clip" data-start="{B['s5']}" data-duration="{dur('s5','s6')+0.1:.3f}" data-track-index="1">
  <div class="card" style="background:radial-gradient(70% 50% at 35% 55%,#3a0a0e 0%,#12070a 60%,#060406 100%)"></div>
  <img id="wg" src="assets/duo_wet.jpg" alt="" style="position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover;transform-origin:30% 55%"/>
  <div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(6,4,6,0) 0%,rgba(6,4,6,0) 50%,rgba(6,4,6,.94) 64%)"></div>
  <div class="scrim" style="opacity:.8"></div>
  <div class="idx" id="wg_idx">PILIHAN 01</div>
  <div id="wg_name" style="position:absolute;left:600px;top:560px;width:440px">
    <div class="disp it" style="font-size:96px;color:#ff6a70">Woman<br/>Glory</div>
    <div class="kicker" style="margin-top:22px;color:var(--ink);font-size:32px">Bombshell</div>
  </div>
  <div id="wg_c1" style="position:absolute;left:600px;top:900px"><span class="chip" style="border-color:rgba(255,106,112,.7)"><b style="background:#ff6a70;box-shadow:0 0 18px #ff6a70"></b>Manis</span></div>
  <div id="wg_c2" style="position:absolute;left:600px;top:1010px"><span class="chip" style="border-color:rgba(255,106,112,.7)"><b style="background:#ff6a70;box-shadow:0 0 18px #ff6a70"></b>Menyerlah</span></div>
</div>

<!-- ===== S6 Noche Midnight Fantasy ===== -->
<div id="s6" class="clip" data-start="{B['s6']}" data-duration="{dur('s6','s7')+0.1:.3f}" data-track-index="1">
  <div class="card" style="background:radial-gradient(70% 50% at 65% 55%,#1d0f3d 0%,#0b0718 60%,#050409 100%)"></div>
  <img id="nc" src="assets/duo_wet.jpg" alt="" style="position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover;transform-origin:70% 55%"/>
  <div style="position:absolute;inset:0;background:linear-gradient(270deg,rgba(5,4,9,0) 0%,rgba(5,4,9,0) 50%,rgba(5,4,9,.94) 64%)"></div>
  <div class="scrim" style="opacity:.8"></div>
  <div class="brand" id="nc_idx">PILIHAN 02</div>
  <div id="nc_name" style="position:absolute;left:60px;top:560px;width:460px">
    <div class="disp" style="font-size:120px;letter-spacing:.06em;color:#c9b2ff">Noche</div>
    <div class="kicker" style="margin-top:22px;color:var(--ink);font-size:30px">Midnight Fantasy</div>
  </div>
  <div id="nc_c1" style="position:absolute;left:60px;top:860px"><span class="chip" style="border-color:rgba(155,107,255,.7)"><b style="background:var(--violet);box-shadow:0 0 18px var(--violet)"></b>Manis</span></div>
  <div id="nc_c2" style="position:absolute;left:60px;top:970px"><span class="chip" style="border-color:rgba(155,107,255,.7)"><b style="background:var(--violet);box-shadow:0 0 18px var(--violet)"></b>Lembut</span></div>
  <div id="nc_c3" style="position:absolute;left:60px;top:1080px"><span class="chip" style="border-color:rgba(155,107,255,.7)"><b style="background:var(--violet);box-shadow:0 0 18px var(--violet)"></b>Misteri</span></div>
</div>

<!-- ===== S7 emotional: giliran kamu ===== -->
<div id="s7" class="clip" data-start="{B['s7']}" data-duration="{dur('s7','s7b')+0.1:.3f}" data-track-index="1">
  <img id="i7" class="full" src="assets/duo_table.jpg" alt="" style="top:170px"/>
  <div class="scrim"></div>
  <div class="center kicker" id="k7" style="top:150px">Setiap hari</div>
  <div class="center disp it" id="t7" style="top:210px;font-size:92px">kamu jaga orang lain</div>
</div>
<video id="v7b" class="full clip" src="assets/p5.mp4" muted data-track-index="0" data-start="{B['s7b']}" data-duration="{dur('s7b','s8')+0.1:.3f}" data-media-start="0"></video>
<div id="s7b" class="clip" data-start="{B['s7b']}" data-duration="{dur('s7b','s8')+0.1:.3f}" data-track-index="1">
  <div class="scrim heavy"></div>
  <div class="center kicker" id="k7b" style="top:520px">Sekarang</div>
  <div class="center disp" id="t7b" style="top:600px;font-size:200px">Giliran</div>
  <div class="center disp it" id="t7c" style="top:790px;font-size:200px;color:var(--gold)">kamu.</div>
</div>

<!-- ===== S8 urgency ===== -->
<div id="s8" class="clip" data-start="{B['s8']}" data-duration="{dur('s8','s9')+0.1:.3f}" data-track-index="1">
  <div class="card" style="background:radial-gradient(80% 50% at 50% 45%,#2a0b0e 0%,#0c0607 65%,#050304 100%)"></div>
  <div class="center kicker" id="u_k" style="top:520px">Stok batch ini</div>
  <div class="center disp it" id="u_t" style="top:600px;font-size:220px;color:#ff5a5f">Terhad</div>
  <div class="meter" style="top:900px"><i id="u_bar"></i></div>
  <div class="center" style="top:950px;font-size:26px;letter-spacing:.35em;color:var(--muted)" id="u_lbl">STOK SEMAKIN BERKURANG</div>
</div>

<!-- ===== S9 CTA ===== -->
<div id="s9" class="clip" data-start="{B['s9']}" data-duration="{dur('s9','s10')+0.1:.3f}" data-track-index="1">
  <img id="i9" class="full" src="assets/duo_curve.jpg" alt=""/>
  <div class="scrim" style="background:linear-gradient(180deg,rgba(7,7,10,.55),rgba(7,7,10,.35) 40%,rgba(7,7,10,.92) 75%)"></div>
  <div class="center kicker" id="c_k" style="top:250px">Klik link di bawah</div>
  <div class="center kicker" id="c_k2" style="top:1290px;color:var(--yellow)">Tekan beg kuning</div>
  <svg id="c_bag" style="position:absolute;left:420px;top:1040px" width="240" height="240" viewBox="0 0 240 240">
    <path d="M40 80 H200 L188 220 H52 Z" fill="#ffd23f" stroke="#141008" stroke-width="6" stroke-linejoin="round"/>
    <path d="M82 96 V64 a38 38 0 0 1 76 0 V96" fill="none" stroke="#141008" stroke-width="10" stroke-linecap="round"/>
  </svg>
  <div class="btn" id="c_btn" style="top:1370px">CHECKOUT SEKARANG</div>
  <div class="tapr" id="c_tap" style="left:620px;top:1385px"></div>
  <div id="c_arrows" style="position:absolute;left:0;right:0;top:1560px;text-align:center;font-family:var(--label);font-size:70px;color:var(--yellow);line-height:.6">
    <div id="ar1">&#8964;</div><div id="ar2">&#8964;</div><div id="ar3">&#8964;</div></div>
</div>

<!-- ===== S10 end card ===== -->
<div id="s10" class="clip" data-start="{B['s10']}" data-duration="{END-B['s10']:.3f}" data-track-index="1">
  <div class="card" style="background:#000"></div>
  <img id="logo2" src="assets/logo.jpg" alt="" style="position:absolute;left:90px;top:420px;width:900px;height:900px;mix-blend-mode:screen"/>
  <div class="center kicker" id="e_k" style="top:1380px;color:var(--ink);letter-spacing:.6em">Soft · Fragrant</div>
  <div class="center" id="e_cta" style="top:1470px"><span class="chip" style="border-color:rgba(255,210,63,.7)"><b style="background:var(--yellow);box-shadow:0 0 18px var(--yellow)"></b>Tekan beg kuning</span></div>
</div>

<!-- ===== captions ===== -->
{chr(10).join(cap_html)}

<!-- ===== global finish ===== -->
<div id="flash" class="flash clip" data-start="0" data-duration="{END}" data-track-index="20"></div>
<div class="vig clip" data-start="0" data-duration="{END}" data-track-index="21"></div>
<div id="grain" class="grain clip" data-start="0" data-duration="{END}" data-track-index="22"></div>
<div class="frame clip" id="frm" data-start="0" data-duration="{END}" data-track-index="23"></div>
<div class="bar clip" id="pbar" data-start="0" data-duration="{END}" data-track-index="24" style="inset:auto;top:0;left:0;height:6px"></div>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
const B = {json.dumps(B)}; const T = {json.dumps(S)};
const ex="expo.out", p4="power4.out";
// progress bar + grain jitter
tl.fromTo("#pbar",{{scaleX:0}},{{scaleX:1,duration:{END},ease:"none"}},0);
tl.to("#grain",{{x:40,y:-30,duration:{END},ease:"steps({int(END*12)})"}},0);
function flash(at,o=.55){{tl.fromTo("#flash",{{opacity:o}},{{opacity:0,duration:.35,ease:"power2.out"}},at);}}
function kb(sel,at,d,s0=1.12,s1=1.0,x0=0,x1=0){{tl.fromTo(sel,{{scale:s0,x:x0}},{{scale:s1,x:x1,duration:d,ease:"none"}},at);}}
function rise(sel,at,d=.5,yy=60){{tl.fromTo(sel,{{opacity:0,y:yy,filter:"blur(14px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:d,ease:ex}},at);}}
function pop(sel,at){{tl.fromTo(sel,{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.45,ease:"back.out(2.2)"}},at);}}

// S1 hook
kb("#v1",0,{B['s1b']+0.2:.3f},1.25,1.05);
tl.fromTo("#h_k",{{opacity:0,scaleX:1.6,filter:"blur(8px)"}},{{opacity:1,scaleX:1,filter:"blur(0px)",duration:.6,ease:ex}},0.12);
tl.fromTo("#h_penat",{{opacity:0,scale:1.6,filter:"blur(30px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:.5,ease:p4}},0.25);
tl.fromTo("#h_rule",{{scaleX:0}},{{scaleX:1,duration:.6,ease:ex}},0.55);
tl.to("#h_penat",{{scale:1.06,duration:.8,ease:"none"}},0.75);
flash(B.s1b,.7);
kb("#i1b",B.s1b,{B['s2']-B['s1b']:.3f},1.22,1.04,0,0);
rise("#h2_k",B.s1b+.02,.4,30);
tl.fromTo("#h2_a",{{opacity:0,y:-80,filter:"blur(16px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.45,ease:ex}},T.hook_masa);
tl.fromTo("#h2_b",{{opacity:0,y:80,filter:"blur(16px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.5,ease:ex}},T.hook_masa+.4);

// S2 myth
flash(B.s2,.35);
rise("#m_k",B.s2,.45,30); rise("#m_a",B.s2+.05);
rise("#m_b",T.mahal-.15,.4);
tl.fromTo("#m_strike",{{scaleX:0}},{{scaleX:1,duration:.32,ease:"power3.inOut"}},T.mahal+.25);
pop("#m_fakta",T.mahal+.45);
tl.fromTo("#m_tag",{{opacity:0,y:40,rotation:-8}},{{opacity:1,y:0,rotation:0,duration:.5,ease:ex}},B.s2+.35);
tl.fromTo("#m_tagx",{{strokeDasharray:300,strokeDashoffset:300}},{{strokeDashoffset:0,duration:.3,ease:"power2.out"}},T.mahal+.3);
kb("#v2b",B.s2b,{dur('s2b','s3')+0.1:.3f},1.18,1.02);
pop("#mb_chip",B.s2b+.1); rise("#mb_t",T.selesa-.1,.45);

// S3 logo + education
flash(B.s3,.6);
tl.fromTo("#logo",{{opacity:0,scale:.82,filter:"blur(18px) brightness(2)"}},{{opacity:1,scale:1,filter:"blur(0px) brightness(1)",duration:.8,ease:ex}},B.s3+.02);
tl.fromTo("#lg_ring",{{opacity:.9,scale:.7}},{{opacity:0,scale:1.35,duration:1.1,ease:"power2.out"}},B.s3+.1);
rise("#lg_k",B.s3+.1,.5,20);
tl.to("#logo",{{scale:1.06,duration:{dur('s3','s3b'):.3f},ease:"none"}},B.s3+.8);
tl.fromTo("#xtals .xtal",{{opacity:0,y:120}},{{opacity:1,y:-60,duration:{dur('s3b','s3c'):.3f},ease:"none",stagger:.02}},B.s3b);
tl.fromTo("#wv1",{{x:-120}},{{x:60,duration:{dur('s3b','s3c'):.3f},ease:"sine.inOut"}},B.s3b);
tl.fromTo("#wv2",{{x:80}},{{x:-100,duration:{dur('s3b','s3c'):.3f},ease:"sine.inOut"}},B.s3b);
rise("#g_k",B.s3b,.4,20); rise("#g_a",B.s3b+.04,.5); rise("#g_b",T.bahan,.45,30);
pop("#mn0",T.kaya); pop("#mn1",T.kaya+.14); pop("#mn2",T.kaya+.28); rise("#mn_lbl",T.mineral,.4,20);
kb("#v3c",B.s3c,{dur('s3c','s4')+0.1:.3f},1.2,1.04);
rise("#sk_k",B.s3c+.02,.4,20); rise("#sk_t",B.s3c+.12,.5); pop("#sk_chip",T.kulit);

// S4 formula
flash(B.s4,.4);
rise("#f_k",B.s4,.4,20);
tl.fromTo("#f_a",{{opacity:0,x:-200}},{{opacity:1,x:0,duration:.5,ease:ex}},B.s4+.05);
tl.fromTo("#f_b",{{opacity:0,x:200}},{{opacity:1,x:0,duration:.5,ease:ex}},T.perfume-.1);
pop("#f_plus",T.perfume-.2);
tl.to("#f_a",{{x:120,duration:.35,ease:"power3.in"}},T.perfume+.45);
tl.to("#f_b",{{x:-120,duration:.35,ease:"power3.in"}},T.perfume+.45);
["#rg1","#rg2","#rg3"].forEach((r,i)=>tl.fromTo(r,{{opacity:.9,scale:.5}},{{opacity:0,scale:1.9,duration:1.0,ease:"power2.out"}},T.perfume+.75+i*.16));
rise("#f_eq",T.perfume+.8,.45);
kb("#v4b",B.s4b,{dur('s4b','s5')+0.1:.3f},1.15,1.0);
tl.fromTo("#spk4 .spk",{{opacity:0,scale:0}},{{opacity:1,scale:1.4,duration:.25,yoyo:true,repeat:1,stagger:.11,ease:"power2.out"}},T.manjakan-.3);
rise("#pm_k",B.s4b+.02,.4,20); rise("#pm_t",T.manjakan-.05,.5);

// S5 Woman Glory (push into left bottle)
flash(B.s5,.45);
tl.fromTo("#wg",{{scale:1.22,x:-40,y:0}},{{scale:1.34,x:-50,y:-20,duration:{dur('s5','s6')+0.1:.3f},ease:"none"}},B.s5);
tl.fromTo("#wg_idx",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:.4,ease:ex}},B.s5+.05);
tl.fromTo("#wg_name",{{opacity:0,x:80,filter:"blur(12px)"}},{{opacity:1,x:0,filter:"blur(0px)",duration:.55,ease:ex}},B.s5+.1);
pop("#wg_c1",T.manis1); pop("#wg_c2",T.serlah);

// S6 Noche (push into right bottle) with wipe
tl.fromTo("#s6",{{clipPath:"inset(0 0 0 100%)"}},{{clipPath:"inset(0 0 0 0%)",duration:.38,ease:"power4.inOut"}},B.s6);
tl.fromTo("#nc",{{scale:1.22,x:40,y:0}},{{scale:1.34,x:50,y:-20,duration:{dur('s6','s7')+0.1:.3f},ease:"none"}},B.s6);
tl.fromTo("#nc_idx",{{opacity:0,x:30}},{{opacity:1,x:0,duration:.4,ease:ex}},B.s6+.15);
tl.fromTo("#nc_name",{{opacity:0,x:-80,filter:"blur(12px)"}},{{opacity:1,x:0,filter:"blur(0px)",duration:.55,ease:ex}},T.noche-.05);
pop("#nc_c1",T.manis2); pop("#nc_c2",T.lembut); pop("#nc_c3",T.misteri);

// S7
flash(B.s7,.4);
kb("#i7",B.s7,{dur('s7','s7b')+0.1:.3f},1.05,1.22);
rise("#k7",B.s7+.05,.4,20); rise("#t7",T.orang-.2,.5);
flash(B.s7b,.6);
kb("#v7b",B.s7b,{dur('s7b','s8')+0.1:.3f},1.25,1.05);
rise("#k7b",B.s7b,.35,20);
tl.fromTo("#t7b",{{opacity:0,scaleX:1.5,filter:"blur(18px)"}},{{opacity:1,scaleX:1,filter:"blur(0px)",duration:.6,ease:ex}},T.giliran-.05);
tl.fromTo("#t7c",{{opacity:0,scale:1.4,filter:"blur(20px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:.5,ease:p4}},T.giliran+.6);

// S8 urgency
tl.fromTo("#s8",{{scale:1.12}},{{scale:1,duration:.4,ease:ex}},B.s8);
rise("#u_k",B.s8,.35,20);
tl.fromTo("#u_t",{{opacity:0,scale:1.8}},{{opacity:1,scale:1,duration:.35,ease:"back.out(1.6)"}},T.terhad-.12);
tl.fromTo("#u_bar",{{scaleX:1}},{{scaleX:.14,duration:.9,ease:"power3.inOut"}},B.s8+.1);
tl.fromTo("#u_t",{{x:-6}},{{x:6,duration:.05,repeat:7,yoyo:true,ease:"none"}},T.terhad+.25);
rise("#u_lbl",B.s8+.3,.4,10);

// S9 CTA
flash(B.s9,.5);
kb("#i9",B.s9,{dur('s9','s10')+0.1:.3f},1.15,1.0);
rise("#c_k",B.s9,.4,20);
["#ar1","#ar2","#ar3"].forEach((a,i)=>tl.fromTo(a,{{opacity:0,y:-20}},{{opacity:1,y:10,duration:.4,repeat:7,yoyo:true,ease:"sine.inOut"}},B.s9+.1+i*.12));
rise("#c_k2",T.tekan,.4,20);
tl.fromTo("#c_bag",{{opacity:0,y:-200,rotation:-15}},{{opacity:1,y:0,rotation:0,duration:.6,ease:"bounce.out"}},T.tekan);
tl.to("#c_bag",{{scale:1.15,duration:.18,yoyo:true,repeat:1,ease:"power2.out"}},T.kuning);
tl.fromTo("#c_btn",{{opacity:0,y:60,scale:.9}},{{opacity:1,y:0,scale:1,duration:.45,ease:"back.out(2)"}},T.checkout-.15);
tl.to("#c_btn",{{scale:.94,duration:.1,yoyo:true,repeat:1,ease:"power2.inOut"}},T.sekarang2);
tl.fromTo("#c_tap",{{opacity:1,scale:.3}},{{opacity:0,scale:2.2,duration:.5,ease:"power2.out"}},T.sekarang2);

// S10 end card
flash(B.s10,.8);
tl.fromTo("#logo2",{{opacity:0,scale:1.25,filter:"blur(24px) brightness(2.5)"}},{{opacity:1,scale:1,filter:"blur(0px) brightness(1)",duration:.9,ease:ex}},B.s10);
rise("#e_k",B.s10+.35,.5,20); pop("#e_cta",B.s10+.55);

// captions
{chr(10).join(cap_js)}

window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body></html>
"""
open(OUT, "w").write(H)
print("scenes", json.dumps(B))
print("caption groups", len(groups))
