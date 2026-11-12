"""Generates index.html + compositions/*.html for the Frescura Body film."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import FONTS, TOKENS, BASE, scene
import s1_hook, s2_edu, s3_zones, s4_mall, s5_foam, s8_cta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOTAL = 38.0

SCENES = [  # id, start, duration
    ('hook', 0.00, 6.00), ('edu', 6.00, 5.75), ('zones', 11.75, 5.55), ('mall', 17.30, 4.00),
    ('foam', 21.30, 1.90), ('salt', 23.20, 1.05), ('scents', 24.25, 2.37), ('wait', 26.62, 3.72),
    ('cta', 30.34, 7.66),
]

# ---------- captions ----------
words = [w for s in json.load(open(os.path.join(ROOT, 'assets/transcript_words.json'))) for w in s['w']]
BRAND = {74: 'Bombshell'}
MERGE = {(1, 2): 'BUAT-BUAT', (21, 22): 'LAGI-LAGI', (60, 62): '@Frescura Body', (95, 97): '@Frescura Body',
         (76, 77): '@Midnight Fantasy', (89, 89): 'BEG KUNING', (74, 74): '@Bombshell'}
tokens = []  # (text, start, end, brand)
i = 0
while i < len(words):
    hit = next(((a, b) for (a, b) in MERGE if a == i), None)
    if hit:
        a, b = hit; t = MERGE[hit]
        tokens.append((t.lstrip('@'), words[a][0], words[b][1], t.startswith('@'))); i = b + 1; continue
    t = re.sub(r'[.,]', '', words[i][2].strip()).upper()
    tokens.append((t, words[i][0], words[i][1], False)); i += 1

GROUPS = ["JANGAN BUAT-BUAT", "TAK TAHU", "KETIAK BAU BAWANG NI", "BUKAN SETAKAT KORANG", "SENDIRI YANG PERASAN",
          "ORANG SENDIRI PUN", "BOLEH TERHIDU TAU", "LAGI-LAGI BILA KORANG", "TENGAH STRES BERPELUH",
          "DAN SIBUK BEKERJA", "SEBAB TU PENTING", "UNTUK JAGA", "KEBERSIHAN BADAN", "TERUTAMANYA BAHAGIAN",
          "YANG MUDAH BERPELUH", "MANDI DENGAN BETUL", "DAN BERSIHKAN", "BAHAGIAN KETIAK", "SETIAP HARI",
          "KALAU NAK PENGALAMAN", "MANDI YANG LEBIH", "MENYENANGKAN", "PASTINYA", "Frescura Body",
          "BUIH LEMBUT", "TERUS DARIPADA BOTOL", "DENGAN GARAM LAUT", "DAN PILIHAN WANGIAN", "Bombshell SERTA",
          "Midnight Fantasy", "JANGAN TUNGGU", "SAMPAI ORANG SEBELAH", "TUTUP HIDUNG", "BARU NAK BERTINDAK",
          "TEKAN BEG KUNING NI", "SEKARANG DAN", "CHECK OUT", "Frescura Body", "SEBAB STOK MEMANG",
          "SANGAT TAK BANYAK", "SIAPA CEPAT", "DIA DAPAT"]
KEY = {'BAWANG', 'TERHIDU', 'STRES', 'BERPELUH', 'PENTING', 'KEBERSIHAN', 'KETIAK', 'BETUL', 'LEMBUT',
       'GARAM', 'LAUT', 'TUNGGU', 'HIDUNG', 'BERTINDAK', 'BEG KUNING', 'SEKARANG', 'STOK', 'CEPAT', 'DAPAT',
       'MENYENANGKAN', 'BOTOL', 'SETIAP'}
groups = []; k = 0
for g in GROUPS:
    n = 0; txt = ''
    toks = []
    while txt != g:
        toks.append(tokens[k]); k += 1
        txt = ' '.join(t[0] for t in toks)
        assert len(toks) < 8 and g.startswith(txt), (g, txt)
    groups.append(toks)
assert k == len(tokens), (k, len(tokens))

cap_html = []; cap_js = []
for gi, toks in enumerate(groups):
    st = max(0.12, toks[0][1] - 0.06)
    nxt = groups[gi + 1][0][1] - 0.06 if gi + 1 < len(groups) else toks[-1][2] + 0.5
    en = min(nxt, toks[-1][2] + 0.9)
    spans = []
    for wi, (t, a, b, br) in enumerate(toks):
        cls = 'w br' if br else ('w key' if t in KEY else 'w')
        spans.append(f'<span class="{cls}" id="cw{gi}_{wi}"><span class="in" id="ci{gi}_{wi}">{t}</span></span>')
        cap_js.append(f"tl.fromTo('#cw{gi}_{wi}',{{opacity:.55}},{{opacity:1,duration:0.08}},{max(st, a-0.03):.2f});")
        if cls != 'w':
            cap_js.append(f"tl.fromTo('#ci{gi}_{wi}',{{scale:1}},{{scale:1.1,duration:0.1,yoyo:true,repeat:1,ease:'sine.out'}},{a+0.02:.2f});")
    cap_html.append(f'      <div class="cg" id="cg{gi}"><span class="pill" id="cp{gi}">{" ".join(spans)}</span></div>')
    cap_js.append(f"tl.fromTo('#cg{gi}',{{opacity:0}},{{opacity:1,duration:0.01}},{st:.2f});")
    cap_js.append(f"tl.fromTo('#cp{gi}',{{y:22,scale:.94}},{{y:0,scale:1,duration:0.18,ease:'back.out(2.2)'}},{st:.2f});")
    cap_js.append(f"tl.to('#cg{gi}',{{opacity:0,duration:0.08,ease:'power2.in'}},{en-0.08:.2f}); tl.set('#cg{gi}',{{opacity:0,visibility:'hidden'}},{en:.2f});")

CAP_CSS = """
.cg{position:absolute;left:50px;right:50px;top:1160px;text-align:center;opacity:0;line-height:1.1;}
.pill{display:inline-block;padding:14px 30px 18px;border-radius:26px;background:rgba(12,9,7,.52);
  border:1.5px solid rgba(216,180,110,.42);box-shadow:0 14px 40px rgba(0,0,0,.35);}
.w{display:inline-block;font-family:var(--sans);font-weight:800;font-size:70px;letter-spacing:.015em;color:#fbf6ee;
  text-shadow:0 3px 0 rgba(0,0,0,.35),0 8px 34px rgba(0,0,0,.75);margin:0 .1em;}
.w .in{display:inline-block;}
.w.key{color:#ffe2a6;text-shadow:0 3px 0 rgba(60,40,10,.45),0 0 30px rgba(216,180,110,.45),0 8px 34px rgba(0,0,0,.75);}
.w.br{font-family:var(--serif);font-style:italic;font-weight:900;font-size:84px;letter-spacing:0;
  color:#ffe9bd;text-shadow:0 0 34px rgba(216,180,110,.55),0 8px 34px rgba(0,0,0,.8);}
"""
captions = scene('captions', CAP_CSS, '\n'.join(cap_html), '    ' + '\n    '.join(cap_js))

# ---------- sfx (start, file, volume) ----------
SFX = [
    (0.00, 'impact-bass-1', 0.55), (0.00, 'sparkle', 0.25), (0.92, 'whoosh', 0.6), (1.98, 'whoosh-short', 0.45),
    (3.93, 'glitch-3', 0.9), (5.24, 'pop', 1.0), (5.26, 'impact-bass-2', 0.22), (5.80, 'whoosh', 0.6),
    (7.44, 'pop', 0.9), (7.80, 'pop', 0.9), (8.46, 'pop', 0.9), (9.32, 'whoosh-short', 0.5), (9.30, 'ping', 1.0),
    (10.70, 'sparkle', 0.35), (11.62, 'whoosh', 0.6), (12.40, 'ping', 0.8), (13.84, 'whoosh-short', 0.55),
    (14.50, 'click', 1.0), (15.10, 'click', 1.0), (16.16, 'whoosh', 0.35),
    (16.49, 'riser', 0.30), (17.10, 'whoosh-cinematic', 0.32), (20.22, 'impact-bass-1', 0.6), (20.24, 'sparkle', 0.4),
    (21.22, 'whoosh', 0.6), (21.30, 'pop', 0.9), (22.30, 'click', 0.9), (23.14, 'whoosh-short', 0.5),
    (23.24, 'sparkle', 0.45), (24.18, 'whoosh', 0.55), (25.12, 'whoosh-short', 0.55), (25.95, 'whoosh', 0.5),
    (25.98, 'sparkle', 0.3), (26.58, 'impact-bass-2', 0.28), (28.70, 'glitch-3', 0.9), (29.10, 'pop', 0.8),
    (29.80, 'pop', 1.0), (30.28, 'whoosh', 0.6), (30.78, 'click', 1.0), (31.96, 'click', 1.0),
    (33.22, 'ping', 0.9), (34.70, 'glitch-3', 0.5), (34.96, 'impact-bass-1', 0.6), (34.98, 'sparkle', 0.4),
    (36.42, 'whoosh-cinematic', 0.22), (36.44, 'impact-bass-1', 0.35), (36.48, 'sparkle', 0.4),
]
DUR = {'impact-bass-1': 2.1, 'impact-bass-2': 2.5, 'sparkle': 1.8, 'whoosh': 0.57, 'whoosh-short': 0.57, 'glitch-3': 1.0,
       'pop': 0.7, 'ping': 1.3, 'click': 0.36, 'riser': 3.9, 'whoosh-cinematic': 3.2}

def build_index():
    hosts = []
    for z, (cid, st, du) in enumerate(SCENES, start=1):
        hosts.append(f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" '
                     f'data-start="{st}" data-duration="{du}" data-track-index="1" data-track-kind="graphics" '
                     f'data-width="1080" data-height="1920" style="z-index:{z}"></div>')
    sfx = []
    for n, (st, f, v) in enumerate(SFX):
        d = min(DUR[f], TOTAL - st)
        sfx.append(f'      <audio id="sfx{n:02d}" class="clip" data-start="{st}" data-duration="{d:.2f}" data-track-index="{4 + n % 8}" '
                   f'data-volume="{v}" src="assets/sfx/{f}.mp3"></audio>')
    return f"""<!doctype html>
<html lang="ms">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
{FONTS}
{TOKENS}
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ margin:0; width:1080px; height:1920px; overflow:hidden; background:#070605; }}
      #root {{ position:relative; width:100%; height:100%; overflow:hidden; }}
      #frame {{ position:absolute; inset:0; pointer-events:none; z-index:40; }}
      #frame .b {{ position:absolute; left:44px; right:44px; top:44px; bottom:44px; border:1.5px solid rgba(216,180,110,.38); border-radius:6px; }}
      #frame .c {{ position:absolute; width:46px; height:46px; border-color:#e6c98f; border-style:solid; border-width:0; }}
      #brandtag {{ position:absolute; left:0; right:0; top:1748px; opacity:.7; text-align:center; z-index:41; font-family:'Manrope'; font-weight:600;
        font-size:28px; letter-spacing:.5em; padding-left:.55em; color:rgba(230,201,143,.85); }}
      #grain {{ position:absolute; inset:0; z-index:42; opacity:.07; mix-blend-mode:overlay; pointer-events:none; }}
      #vig {{ position:absolute; inset:0; z-index:39; background:radial-gradient(130% 80% at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,.55) 100%); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{chr(10).join(hosts)}
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}"
        data-track-index="3" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:30"></div>
      <div id="vig"></div>
      <div id="frame"><div class="b"></div>
        <div class="c" style="left:30px;top:30px;border-left-width:3px;border-top-width:3px"></div>
        <div class="c" style="right:30px;top:30px;border-right-width:3px;border-top-width:3px"></div>
        <div class="c" style="left:30px;bottom:30px;border-left-width:3px;border-bottom-width:3px"></div>
        <div class="c" style="right:30px;bottom:30px;border-right-width:3px;border-bottom-width:3px"></div>
      </div>
      <div id="brandtag" data-layout-ignore>FRESCURA BODY</div>
      <svg id="grain" viewBox="0 0 1080 1920"><filter id="gn"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="4"/></filter><rect width="1080" height="1920" filter="url(#gn)"/></svg>
      <audio id="voice" class="clip" data-start="0" data-duration="36.53" data-track-index="2" data-volume="1" src="assets/audio/voice.wav"></audio>
{chr(10).join(sfx)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      tl.fromTo('#brandtag', {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6 }}, 0.2);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""

def main():
    os.makedirs(os.path.join(ROOT, 'compositions'), exist_ok=True)
    out = {'hook': s1_hook.build(), 'edu': s2_edu.build(), 'zones': s3_zones.build(), 'mall': s4_mall.build(),
           **s5_foam.build(), **s8_cta.build(), 'captions': captions}
    for k, v in out.items():
        open(os.path.join(ROOT, 'compositions', k + '.html'), 'w').write(v)
    open(os.path.join(ROOT, 'index.html'), 'w').write(build_index())
    print('ok', len(groups), 'caption groups')

main()
