"""Build compositions/captions.html from the word-level transcript of the processed voice.
Usage: python build_captions.py <transcript.json> <out.html>
Whisper spells brand words by sound; FIXES maps word index -> the correct spelling. A list value
splits one recognised word into several caption words (time shared by character count); a None
value merges the word into the previous one.
"""
import json, sys, html

VO_OFFSET = 0.10
words = [dict(t=w["w"].strip(), s=w["s"], e=w["e"]) for seg in json.load(open(sys.argv[1])) for w in seg["words"]]
idx = {i: w["t"] for i, w in enumerate(words)}

def find(t, start=0):
    for i in range(start, len(words)):
        if words[i]["t"].lower().strip(",.?") == t: return i
    raise SystemExit(f"word {t} not found")

FIXES = {0: "Korang"}
FIXES[find("asal")] = "asas"
i = find("fresh"); FIXES[i] = "Frescura"; FIXES[i + 1] = None; FIXES[i + 2] = "Body"
for k in range(2):
    i = find("minat", (i + 1)); FIXES[i] = "Midnight"; FIXES[i + 1] = "Fantasy" + words[i + 1]["t"][-1:].replace("i", "")
i = find("bekunis"); FIXES[i] = ["beg", "kuning"]
i = find("check"); FIXES[i] = "checkout"; FIXES[i + 1] = None
for j, w in enumerate(words):
    if w["t"].lower().startswith("bombshell"): FIXES[j] = "Bombshell" + w["t"][9:]

out = []
for j, w in enumerate(words):
    f = FIXES.get(j, w["t"])
    if f is None:
        out[-1]["e"] = w["e"]; continue
    if isinstance(f, list):
        tot = sum(len(x) for x in f); t0 = w["s"]
        for x in f:
            d = (w["e"] - w["s"]) * len(x) / tot; out.append(dict(t=x, s=t0, e=t0 + d)); t0 += d
        continue
    out.append(dict(t=f, s=w["s"], e=w["e"]))
for w in out: w["s"] += VO_OFFSET; w["e"] += VO_OFFSET

# key words get the gold accent
KEY = {"suami", "kemas,", "bersih", "wangi?", "bersolek", "asas", "kebersihan", "pakaian", "rutin", "mandi",
       "penting.", "istimewa,", "frescura", "body", "feminine", "bombshell", "midnight", "fantasy.", "fantasy,",
       "stok", "habis.", "beg", "kuning", "kegemaran", "checkout", "dua"}

# groups: 2-4 words, break on punctuation or a pause >= 0.15 s
phrases, cur = [], []
for k, w in enumerate(out):
    cur.append(w)
    nxt = out[k + 1] if k + 1 < len(out) else None
    if nxt is None or w["t"][-1] in ",.?" or nxt["s"] - w["e"] >= 0.15:
        phrases.append(cur); cur = []
groups = []
for p in phrases:
    n = -(-len(p) // 4); base, extra = divmod(len(p), n); i = 0
    for g in range(n):
        size = base + (1 if g < extra else 0)
        if p[i + size - 1]["t"] == "Midnight" and i + size < len(p): size += 1  # never split the name
        groups.append(p[i:i + size]); i += size
        if i >= len(p): break
    if i < len(p): groups[-1] += p[i:]

html_groups, js = [], []
for g_i, g in enumerate(groups):
    gs = max(0.12, g[0]["s"] - 0.06)
    ge = (groups[g_i + 1][0]["s"] - 0.06) if g_i + 1 < len(groups) else g[-1]["e"] + 0.35
    spans = []
    for w_i, w in enumerate(g):
        cls = "cw key" if w["t"].lower() in KEY else "cw"
        spans.append(f'<span class="{cls}" id="cw-{g_i}-{w_i}">{html.escape(w["t"])}</span>')
        js.append(f'  word("#cw-{g_i}-{w_i}", {w["s"]:.3f});')
    html_groups.append(f'    <div class="cg" id="cg-{g_i}"><div class="cg-in">{" ".join(spans)}</div></div>')
    js.append(f'  group("#cg-{g_i}", {gs:.3f}, {ge:.3f});')

page = f"""<template>
  <style>
    @font-face {{ font-family: "Jost"; src: url("assets/fonts/Jost-normal.woff2") format("woff2"); font-weight: 300 700; font-style: normal; }}
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    .cg {{ position: absolute; left: 0; width: 1080px; top: 1186px; text-align: center; opacity: 0; visibility: hidden; overflow: visible; }}
    .cg-in {{ display: inline-block; max-width: 920px; padding: 16px 34px 20px; border-radius: 22px; background: rgba(12,10,9,.52); font-family: "Jost"; font-weight: 600; font-size: 66px; line-height: 1.12; letter-spacing: .005em; color: #f5efe6; text-shadow: 0 3px 14px rgba(0,0,0,.55); }}
    .cw {{ display: inline-block; opacity: .55; }}
    .cw.key {{ color: #e8c98a; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
{chr(10).join(html_groups)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    function group(sel, s, e) {{
      tl.set(sel, {{ visibility: "visible" }}, s);
      tl.fromTo(sel, {{ opacity: 0, y: 14, filter: "blur(6px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.14, ease: "power3.out" }}, s);
      tl.to(sel, {{ opacity: 0, duration: 0.08, ease: "power2.in" }}, e - 0.08);
      tl.set(sel, {{ opacity: 0, visibility: "hidden" }}, e);
    }}
    function word(sel, t) {{
      tl.fromTo(sel, {{ opacity: 0.55, scale: 1 }}, {{ opacity: 1, scale: 1.07, duration: 0.1, ease: "power2.out" }}, t - 0.02);
      tl.to(sel, {{ scale: 1, duration: 0.18, ease: "power2.inOut" }}, t + 0.08);
    }}
{chr(10).join(js)}
    window.__timelines["captions"] = tl;
  </script>
</template>
"""
open(sys.argv[2], "w").write(page)
print(len(groups), "groups")
for g in groups: print(f'{g[0]["s"]:6.2f}', " ".join(w["t"] for w in g))
