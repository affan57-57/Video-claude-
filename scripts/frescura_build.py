"""Build the Frescura Body HyperFrames project: index.html (scenes + audio) and captions.html.
Scene bodies live in scenes/*.html fragments (markup + <script> body); this script wraps them
with the shared brand tokens/fonts and writes compositions/*.html.
Usage: python frescura_build.py PROJECT_DIR
"""
import json, sys, os, re, html

P = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920

FONTS = """
@font-face{font-family:'Bodoni Moda';src:url('assets/fonts/BodoniModa-500.woff2') format('woff2');font-weight:500;font-style:normal}
@font-face{font-family:'Bodoni Moda';src:url('assets/fonts/BodoniModa-500i.woff2') format('woff2');font-weight:500;font-style:italic}
@font-face{font-family:'Bodoni Moda';src:url('assets/fonts/BodoniModa-800.woff2') format('woff2');font-weight:800;font-style:normal}
@font-face{font-family:'Jost';src:url('assets/fonts/Jost-300.woff2') format('woff2');font-weight:300}
@font-face{font-family:'Jost';src:url('assets/fonts/Jost-500.woff2') format('woff2');font-weight:500}
@font-face{font-family:'Jost';src:url('assets/fonts/Jost-700.woff2') format('woff2');font-weight:700}
"""
TOKENS = """
#root{position:absolute;inset:0;overflow:hidden;--noir:#0b0908;--esp:#18110d;--ink:#f4ede3;--mute:#b9ad9f;--gold:#d9b98c;--gold2:#f3dcb0;--rose:#b3182f;--violet:#6d4bd6;
 font-family:'Jost',sans-serif;color:var(--ink);background:var(--noir)}
#root .abs{position:absolute}
#root .full{position:absolute;left:0;top:0;width:1080px;height:1920px}
#root .serif{font-family:'Bodoni Moda',serif;font-weight:500}
#root .ital{font-family:'Bodoni Moda',serif;font-style:italic;font-weight:500}
#root .kick{font-family:'Jost',sans-serif;font-weight:500;letter-spacing:.42em;text-transform:uppercase;color:var(--gold);font-size:34px}
#root .center{left:0;width:1080px;text-align:center}
#root .glow{position:absolute;border-radius:50%;pointer-events:none}
#root .hair{position:absolute;height:2px;background:linear-gradient(90deg,transparent,var(--gold),transparent)}
#root .card{position:absolute;border:1.5px solid rgba(217,185,140,.55);background:linear-gradient(160deg,rgba(40,30,24,.82),rgba(12,10,9,.86));border-radius:28px}
"""


def scene(name, dur, body):
    """body: fragment with markup, <style> extras and a <script> section using `tl`."""
    m = re.search(r"<script>(.*)</script>", body, re.S)
    js = m.group(1) if m else ""
    rest = body[: m.start()] + body[m.end():] if m else body
    sm = re.search(r"<style>(.*)</style>", rest, re.S)
    css = sm.group(1) if sm else ""
    markup = rest[: sm.start()] + rest[sm.end():] if sm else rest
    out = f"""<template>
<style>{FONTS}{TOKENS}{css}</style>
<div id="root" data-composition-id="{name}" data-width="{W}" data-height="{H}" data-duration="{dur}">
{markup.strip()}
</div>
<script>
(function(){{
const tl = gsap.timeline({{ paused: true }});
const S = "[data-composition-id='{name}'] ";
{js.strip()}
window.__timelines["{name}"] = tl;
}})();
</script>
</template>
"""
    open(f"{P}/compositions/{name}.html", "w").write(out)


# ---------------------------------------------------------------- scenes
SCENES = [  # id, start, duration
    ("hook", 0.00, 2.28), ("clock", 2.28, 3.02), ("human", 5.30, 5.42), ("busy", 10.72, 5.64),
    ("gift", 16.36, 3.26), ("boutique", 19.62, 1.48), ("foam", 21.10, 1.68), ("ingred", 22.78, 1.80),
    ("scents", 24.58, 2.80), ("nowait", 27.38, 3.72), ("cta", 31.10, 4.22), ("love", 35.32, 4.68),
]
TOTAL = 40.0
for sid, st, du in SCENES:
    frag = open(f"{HERE}/frescura_scenes/{sid}.html").read()
    scene(sid, du, frag)

# ---------------------------------------------------------------- captions
words = json.load(open(sys.argv[2]))  # list of {w,s,e} from whisper (final voice timeline)
fix = {2: "korang ingat", 54: "Sesekali", 55: None, 57: "isteri", 67: "Buih", 74: "laut", 91: "isteri",
       98: "link", 102: "checkout", 103: None, 110: "pelancaran", 114: "isteri", 10: "uruskan", 84: "misteri", 86: "seksi."}
W2 = []
for i, w in enumerate(words):
    t = w["w"].strip()
    if i in fix:
        if fix[i] is None:
            W2[-1]["e"] = w["e"]; W2[-1]["idx"].append(i); continue
        t = fix[i]
    W2.append(dict(t=t, s=w["s"], e=w["e"], idx=[i]))
    if i == 77:  # spoken "feminin" between wangian and Bombshell
        W2.append(dict(t="feminin", s=24.20, e=24.56, idx=[77.5]))
# fix punctuation/case tokens
for w in W2:
    w["t"] = w["t"].replace("-suami,", "suami,").replace("-kadang", "kadang")
GROUPS = [[0, 1], [2, 4], [5, 6], [7, 9], [10, 11], [12, 15], [16, 19], [20, 23], [24, 26], [27, 30], [31, 34], [35, 36],
          [37, 40], [41, 43], [44, 47], [48, 50], [51, 53], [54, 56], [57, 59], [60, 63], [64, 66], [67, 69], [70, 72],
          [73, 75], [76, 77.5], [78, 79], [80, 81], [82, 84], [85, 86], [87, 88], [89, 92], [93, 96], [97, 100],
          [101, 103], [104, 105], [106, 109], [110, 112], [113, 115], [116, 119]]
EMPH = {"robot", "malam", "manusia", "penat", "perhatian", "dihargai", "sibuk", "bahagiakan", "istimewa", "frescura", "body",
        "lembut", "laut", "feminin", "bombshell", "midnight", "fantasy", "misteri", "seksi", "hadiah", "link", "checkout",
        "pelancaran", "tiktok", "cinta", "sayangkan", "wanita", "botol"}


def key(w):
    return re.sub(r"[^a-z]", "", w["t"].lower())


groups = []
for a, b in GROUPS:
    ws = [w for w in W2 if a <= w["idx"][0] <= b]
    # merge "Suami" + "suami," into one token
    merged = []
    for w in ws:
        if merged and w["t"].startswith("suami") and merged[-1]["t"].lower() == "suami":
            merged[-1] = dict(merged[-1], t="Suami-suami,", e=w["e"])
        elif merged and w["t"].startswith("kadang") and merged[-1]["t"].lower() == "kadang":
            merged[-1] = dict(merged[-1], t="Kadang-kadang", e=w["e"])
        else:
            merged.append(w)
    groups.append(merged)

cap_html, cap_js = [], []
for gi, g in enumerate(groups):
    gs = max(0.12, g[0]["s"] - 0.06)
    nxt = groups[gi + 1][0]["s"] - 0.06 if gi + 1 < len(groups) else g[-1]["e"] + 0.35
    ge = min(nxt, g[-1]["e"] + 0.45)
    spans = []
    for wi, w in enumerate(g):
        k = key(w); em = k in EMPH
        txt = html.escape(w["t"])
        cls = "w em" if em else "w"
        spans.append(f'<span class="{cls}" id="c{gi}w{wi}">{txt}</span>')
        cap_js.append(f'tl.fromTo("#c{gi}w{wi}",{{opacity:0,y:26,filter:"blur(8px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.16,ease:"power3.out"}},{max(gs, w["s"] - 0.05):.3f});')
        if em:
            cap_js.append(f'tl.fromTo("#c{gi}w{wi}",{{scale:1.18}},{{scale:1,duration:.35,ease:"expo.out"}},{w["s"]:.3f});')
    cap_html.append(f'<div class="grp" id="cg{gi}"><div class="line">{" ".join(spans)}</div></div>')
    cap_js.append(f'tl.set("#cg{gi}",{{opacity:1,visibility:"visible"}},{gs:.3f});')
    cap_js.append(f'tl.to("#cg{gi}",{{opacity:0,duration:.1,ease:"power2.in"}},{ge - 0.1:.3f});')
    cap_js.append(f'tl.set("#cg{gi}",{{visibility:"hidden"}},{ge:.3f});')

CAP_CSS = """
#root{background:transparent}
#root .grp{position:absolute;left:0;top:1120px;width:1080px;text-align:center;opacity:0;visibility:hidden}
#root .line{display:inline-block;max-width:960px;padding:10px 20px;
  text-shadow:0 3px 14px rgba(0,0,0,.9),0 0 3px rgba(0,0,0,.95),0 0 40px rgba(0,0,0,.55);
  font-family:'Jost',sans-serif;font-weight:700;font-size:58px;line-height:1.12;letter-spacing:.02em;text-transform:uppercase;color:#f4ede3}
#root .w{display:inline-block;transform-origin:50% 70%}
#root .w.em{font-family:'Bodoni Moda',serif;font-style:italic;font-weight:500;text-transform:none;font-size:70px;letter-spacing:0;
  color:#f3dcb0;text-shadow:0 0 22px rgba(217,185,140,.45)}
"""
scene("captions", TOTAL, f"<style>{CAP_CSS}</style>\n" + "\n".join(cap_html) + "\n<script>\n" + "\n".join(cap_js) + "\n</script>")

# ---------------------------------------------------------------- audio + index
SFX = [  # (file, t, vol)
    ("impact", 0.00, .75), ("glitch", 0.02, .45), ("glitch", 1.60, .5), ("whoosh", 2.16, .55),
    ("tick", 3.38, .7), ("tick", 4.02, .7), ("tick", 4.32, .7), ("whoosh_s", 5.22, .5),
    ("pop", 5.50, .5), ("whoosh_s", 7.55, .5), ("glitch", 7.75, .3), ("whoosh_s", 8.42, .5), ("whoosh_s", 10.12, .5), ("sparkle", 10.2, .35),
    ("whoosh", 10.64, .55), ("ping", 10.95, .5), ("ping", 11.40, .5), ("ping", 11.85, .5), ("ping", 12.30, .5), ("ping", 12.80, .55),
    ("whoosh", 13.80, .6), ("sparkle", 13.95, .45),
    ("whoosh", 16.30, .5), ("riser", 17.62, .5), ("sparkle", 18.96, .6), ("glass", 19.00, .55),
    ("impact", 19.62, .8), ("shutter", 19.72, .45), ("shutter", 19.88, .45), ("shutter", 20.04, .45), ("sparkle", 20.35, .35),
    ("whoosh_s", 21.04, .55), ("squish", 21.18, .9), ("squish", 21.95, .7),
    ("pop", 22.84, .55), ("sparkle", 22.9, .3), ("pop", 23.42, .55),
    ("impact", 24.58, .6), ("whoosh", 25.36, .6), ("pop", 26.42, .55), ("pop", 26.96, .6), ("heartbeat", 26.5, .45),
    ("whoosh", 27.34, .55), ("tick", 28.60, .6), ("whoosh_s", 29.28, .5), ("glass", 30.58, .5),
    ("whoosh", 31.06, .55), ("pop", 31.38, .8), ("shutter", 32.42, .45), ("riser", 33.0, .35), ("kaching", 34.18, .75),
    ("whoosh", 35.28, .5), ("heartbeat", 36.36, .75), ("sparkle", 37.0, .45), ("impact", 37.92, .6), ("tada", 38.0, .55), ("glass", 38.12, .5),
]
hosts = []
for i, (sid, st, du) in enumerate(SCENES):
    hosts.append(f'      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{st}" data-duration="{du}" data-track-index="1" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:{i + 1}"></div>')
hosts.append(f'      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-track-kind="captions" data-width="{W}" data-height="{H}" style="z-index:50"></div>')
aud = [f'      <audio id="voice" class="clip" src="assets/audio/voice.wav" data-start="0" data-duration="37.99" data-track-index="3" data-volume="1.12"></audio>',
       f'      <audio id="music" class="clip" src="assets/audio/music.wav" data-start="0" data-duration="{TOTAL}" data-track-index="4" data-volume="0.2" data-fade-out="1.6"></audio>']
for j, (f, t, v) in enumerate(SFX):
    import soundfile as _sf
    dur = round(_sf.info(f"{P}/assets/audio/{f}.wav").duration, 3)
    dur = min(dur, TOTAL - t)
    aud.append(f'      <audio id="sfx{j:02d}-{f}" class="clip" src="assets/audio/{f}.wav" data-start="{t}" data-duration="{dur}" data-track-index="{5 + j % 6}" data-volume="{v}"></audio>')
index = f"""<!doctype html>
<html lang="ms">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: #0b0908; }}
      #root {{ position: relative; width: 100%; height: 100%; }}
      #bg {{ position: absolute; inset: 0; background: #0b0908; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}">
      <div id="bg"></div>
{chr(10).join(hosts)}
{chr(10).join(aud)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(f"{P}/index.html", "w").write(index)
print("built", len(SCENES), "scenes,", len(groups), "caption groups,", len(SFX), "sfx")
