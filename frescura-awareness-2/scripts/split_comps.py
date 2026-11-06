# Restructure the single-file v2 composition into HyperFrames sub-compositions.
import re, sys, os, shutil, zlib
SRC, DST = sys.argv[1], sys.argv[2]
html = open(os.path.join(SRC, "index.html")).read()
if os.path.exists(DST): shutil.rmtree(DST)
shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns(".hyperframes", "node_modules"))
os.makedirs(os.path.join(DST, "compositions"), exist_ok=True)

head = html[: html.index("<body>")]
body = html[html.index("<body>"):]
script = body[body.index("<script>") + 8 : body.rindex("</script>")]

def block(marker):  # scene block from its comment to the next comment
    i = body.index(marker); i = body.index("\n", i) + 1
    j = body.index("<!--", i)
    return body[i:j].rstrip()
def media(mid):
    m = re.search(r'\s*<(img|video) id="%s"[^>]*?(/>|></video>)' % mid, body)
    return m.group(0).strip()
def js(a, b):
    i = script.index(a); j = script.index(b)
    return script[i:j]

def shift_starts(frag, T0):
    def f(m):
        return 'data-start="%s"' % (round(float(m.group(1)) - T0, 3) if round(float(m.group(1)) - T0, 3) != int(round(float(m.group(1)) - T0, 3)) else int(round(float(m.group(1)) - T0, 3)))
    return re.sub(r'data-start="([0-9.]+)"', f, frag)

kb_lines = {m.group(1): m.group(0) for m in re.finditer(r'kb\("#(m\w+)",[^\n]*\);', script)}

COMPS = [
  ("hook", 0, 4.62, ["m1"], ["<!-- S1 HOOK"], [("// ---------- S1 hook", "// ---------- S2 process")]),
  ("process", 4.62, 5.38, [], ["<!-- S2 PROCESS"], [("// ---------- S2 process", "// ---------- S3 minerals")]),
  ("minerals", 10.0, 4.42, [], ["<!-- S3 MINERALS"], [("// ---------- S3 minerals", "// ---------- S4 Mg")]),
  ("hydrate", 14.42, 2.1, [], ["<!-- S4 Mg"], [("// ---------- S4 Mg", "// ---------- S5 pilih")]),
  ("choose", 16.52, 1.94, [], ["<!-- S5 PILIH"], [("// ---------- S5 pilih", "// ---------- S6 product")]),
  ("product", 18.46, 5.46, ["m6a", "m6b"], ["<!-- S6a PRODUCT", "<!-- S6b SPA"], [("// ---------- S6 product", "// ---------- S7 / S8 foam")]),
  ("foam", 23.92, 6.58, ["m7a", "m7b", "m8a", "m8b"], ["<!-- S7 FOAM", "<!-- S8a CLEAN", "<!-- S8b FEATURES"], [("// ---------- S7 / S8 foam", "// ---------- S9 two")]),
  ("duo", 30.5, 1.74, [], ["<!-- S9 TWO"], [("// ---------- S9 two", "// ---------- S10 / S11 variants")]),
  ("variants", 32.24, 8.26, [], ["<!-- S10 WOMAN GLORY", "<!-- S11 NOCHE"], [("// ---------- S10 / S11 variants", "// ---------- S12 stock")]),
  ("stock", 40.5, 1.86, [], ["<!-- S12 STOCK"], [("// ---------- S12 stock", "// ---------- S13 CTA")]),
  ("cta", 42.36, 2.64, ["m13"], ["<!-- S13 CTA"], [("// ---------- S13 CTA", "// ---------- captions")]),
]

def write_comp(cid, T0, inner_html, code):
    seed = zlib.crc32(cid.encode())
    tpl = f'''<!-- HyperFrames sub-composition: {cid} (root time {T0}s). Timing inside is local to this composition. -->
<template id="{cid}-template">
  <div data-composition-id="{cid}" data-width="1080" data-height="1920" class="comp-root">
{inner_html}
    <script>
      (function () {{
        const base = gsap.timeline({{ paused: true }});
        const tl = HF.shift(base, {T0});
        const rnd = HF.rng({seed});
        const kb = (sel, t, d, a, b, x = 0) => tl.fromTo(sel, {{ scale: a, xPercent: x }}, {{ scale: b, xPercent: -x, duration: d, ease: "power1.out" }}, t);
{code}
        window.__timelines = window.__timelines || {{}};
        window.__timelines["{cid}"] = base;
      }})();
    </script>
  </div>
</template>
'''
    open(os.path.join(DST, "compositions", cid + ".html"), "w").write(tpl)

hosts = []
for cid, T0, dur, mids, blocks, jsr in COMPS:
    parts = [media(m) for m in mids] + [block(b) for b in blocks]
    inner = "\n".join("    " + shift_starts(p, T0).strip().replace("\n", "\n    ") for p in parts)
    code = "".join(kb_lines[m] + "\n" for m in mids) + "".join(js(a, b) for a, b in jsr)
    code = "\n".join("        " + l for l in code.splitlines())
    write_comp(cid, T0, inner, code)
    hosts.append((cid, T0, dur))

# captions + HUD compositions
caps_code = js("// ---------- captions", "window.__timelines")
light_code = js("// ---------- light scenes", "// ---------- transitions")
light_caps = "\n".join(l for l in light_code.splitlines() if "#frame" not in l).replace('.set("#shade", { opacity: 0 }, a)', "").replace('.set("#shade", { opacity: 1 }, b)', "")
write_comp("captions", 0, '    <div id="caps" class="clip" data-start="0" data-duration="45"></div>',
           "\n".join("        " + l for l in (light_caps + caps_code).splitlines()))
hud_html = '''    <div id="frame" class="clip" data-start="0" data-duration="45"><div class="bd"></div><div class="segs"></div><div class="brand">FRESCURA BODY</div></div>
    <div id="blinds" class="clip" data-start="0" data-duration="45"><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>'''
seg_code = js("// ---------- scene list", "for (let t = 0; t < 45; t += 0.1)")
frame_code = "\n".join(l for l in light_code.splitlines() if "#frame" in l)
trans = js("// ---------- transitions", "// ---------- media camera moves")
blinds_code = trans[: trans.index("[10.0, 14.42")]
write_comp("hud", 0, hud_html, "\n".join("        " + l for l in (seg_code + frame_code + "\n" + blinds_code).splitlines()))

# root index.html
root_code = js("for (let t = 0; t < 45; t += 0.1)", "// ---------- light scenes") + \
  "      [[4.62, 10.0], [14.42, 18.46], [40.5, 42.36]].forEach(([a, b]) => { tl.set(\"#shade\", { opacity: 0 }, a); tl.set(\"#shade\", { opacity: 1 }, b); });\n" + \
  trans[trans.index("[10.0, 14.42"):]
host_html = "\n".join(
  f'      <div id="host-{cid}" class="clip" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{T0}" data-duration="{d}" data-track-index="{i}"></div>'
  for i, (cid, T0, d) in enumerate(hosts))
new_body = f'''<body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="45" data-width="1080" data-height="1920" data-fps="30">
      <!-- Scene sub-compositions (compositions/*.html), mounted in root time -->
{host_html}
      <!-- Global layers -->
      <div id="shade" class="clip" data-start="0" data-duration="45" data-track-index="20"></div>
      <div id="host-captions" class="clip" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="45" data-track-index="21"></div>
      <div id="host-hud" class="clip" data-composition-id="hud" data-composition-src="compositions/hud.html" data-start="0" data-duration="45" data-track-index="22"></div>
      <div id="flash" class="clip" data-start="0" data-duration="45" data-track-index="23"></div>
      <div id="grain" class="clip" data-start="0" data-duration="45" data-track-index="24"></div>
      <audio id="mix" data-start="0" data-duration="45" data-media-start="0" data-volume="1" data-track-index="30" src="assets/audio/mix.wav"></audio>
    </div>
    <script>
      let seed = 4520261106;
      const rnd = () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
      const tl = gsap.timeline({{ paused: true }});
{root_code}
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
'''
head = head.replace('<script src="assets/captions.js"></script>', '<script src="assets/captions.js"></script>\n    <script src="assets/hf-helpers.js"></script>')
head = head.replace("#frame { pointer-events: none; }", "#frame { pointer-events: none; }\n      .comp-root { position: absolute; inset: 0; }")
head = head.replace("#frame .bd { position: absolute; inset: 30px;", "#frame .bd { position: absolute; inset: 30px;")
open(os.path.join(DST, "index.html"), "w").write(head + new_body)
open(os.path.join(DST, "assets", "hf-helpers.js"), "w").write('''// Shared helpers for Frescura sub-compositions.
// HF.shift lets a scene keep root-time positions while its own timeline stays local (t - T0).
window.HF = {
  shift(base, T0) {
    const w = {
      fromTo(a, b, c, t) { base.fromTo(a, b, c, t - T0); return w; },
      to(a, b, t) { base.to(a, b, t - T0); return w; },
      set(a, b, t) { base.set(a, b, t - T0); return w; },
    };
    return w;
  },
  rng(seed) { let s = seed >>> 0; return () => ((s = (s * 1664525 + 1013904223) % 4294967296) / 4294967296); },
};
var $ = (s) => document.querySelector(s);
var $$ = (s) => Array.from(document.querySelectorAll(s));
var E = "expo.out", P = "power3.out", B = "back.out(1.7)";
''')
print("ok", len(hosts), "scene comps")
