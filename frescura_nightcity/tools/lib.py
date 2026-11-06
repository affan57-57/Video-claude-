# Shared building blocks for the FRESCURA night-city HyperFrames projects.
import json, random, re, html as H

FONTS = """
@font-face{font-family:'Bodoni Moda';font-style:normal;font-weight:400 900;src:url('assets/fonts/BodoniModa-normal.woff2') format('woff2')}
@font-face{font-family:'Bodoni Moda';font-style:italic;font-weight:400 900;src:url('assets/fonts/BodoniModa-italic.woff2') format('woff2')}
@font-face{font-family:'Syne';font-style:normal;font-weight:400 800;src:url('assets/fonts/Syne-normal.woff2') format('woff2')}
@font-face{font-family:'Syncopate';font-style:normal;font-weight:700;src:url('assets/fonts/Syncopate-700.woff2') format('woff2')}
"""
BASE_CSS = FONTS + """
#root{position:absolute;inset:0;--ink:#F6F1E7;--gold:#E2C28A;--gold2:#FFF1D0;--rose:#C3123B;--plum:#2A1240}
.abs{position:absolute}
.h{opacity:0}
.full{position:absolute;left:0;width:1080px;text-align:center;white-space:nowrap}
.x8{font-weight:800 !important}
.syne{font-family:'Syne';font-weight:700;text-transform:uppercase;letter-spacing:-.015em;color:var(--ink);line-height:.95}
.bod{font-family:'Bodoni Moda';font-style:italic;font-weight:500;line-height:1}
.gt{background:linear-gradient(180deg,#FFF4DA 0%,#E9CB92 45%,#B8884A 100%);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 4px 16px rgba(0,0,0,.75))}
.syn{font-family:'Syncopate';font-weight:700;letter-spacing:.34em;text-transform:uppercase;font-size:20px;color:var(--gold)}
.glass{background:linear-gradient(160deg,rgba(28,32,60,.72),rgba(8,10,22,.78));border:1.5px solid rgba(232,198,144,.42);border-radius:34px;box-shadow:0 40px 90px rgba(0,0,0,.55),inset 0 1px 0 rgba(255,255,255,.10)}
.shadow{text-shadow:0 6px 40px rgba(0,0,0,.65)}
.pill{display:inline-flex;align-items:center;gap:14px;white-space:nowrap;padding:16px 30px;border-radius:999px;font-family:'Syne';font-weight:700;font-size:34px;color:var(--ink);text-transform:uppercase;letter-spacing:.02em}
"""

def anchors(words):
    def norm(t): return re.sub(r'[^a-z]', '', t.lower())
    def T(w, after=0.0, nth=0):
        k = 0
        for x in words:
            if x['start'] >= after - 1e-6 and norm(x['text']).startswith(norm(w)):
                if k == nth: return x['start']
                k += 1
        raise KeyError(w)
    def E(w, after=0.0):
        for x in words:
            if x['start'] >= after - 1e-6 and norm(x['text']).startswith(norm(w)): return x['end']
        raise KeyError(w)
    def prev(w, after=0.0):
        t = T(w, after); ps = [x['start'] for x in words if x['start'] < t - 1e-6]
        return ps[-1]
    return T, E, prev

# ---------- caption word clean-up ----------
FIX = {'bui': 'buih', 'sisap': 'sea salt', 'silsat': 'sea salt', 'bombsher': 'Bombshell', 'kuni': 'kuning', 'perfum': 'perfume',
       'terahat': 'terhad', 'mainan': 'Midnight', 'minat': 'Midnight', 'fantasi': 'Fantasy', 'span': 'span'}
EMPH = {'perfume', 'mahal', 'frescura', 'buih', 'sea', 'mineral', 'bombshell', 'midnight', 'wangi', 'premium', 'mewah', 'rugi',
        'kuning', 'terhad', 'tiga', 'pertama', 'kedua', 'ketiga', 'lembut', 'segar', 'terbazir', 'dulu', 'habis', 'inspirasi',
        'fruity', 'feminine', 'checkout', 'pilihan', 'laut', 'serius'}

def clean_words(words):
    out = []
    for w in words:
        t = w['text']
        if t.startswith('-') and out:
            out[-1]['text'] += t; out[-1]['end'] = w['end']; continue
        core = re.sub(r'[^\w]', '', t).lower(); tail = re.sub(r'^[\w-]+', '', t)
        if core == 'kura' and out and out[-1]['text'].lower().startswith('fresh'):
            out[-1]['text'] = 'Frescura'; out[-1]['end'] = w['end']; continue
        if core in ('body', 'bodhi') and out and out[-1]['text'] == 'Frescura':
            t = 'Body' + tail
        elif core == 'out' and out and out[-1]['text'].lower() == 'cek':
            out[-1]['text'] = 'checkout' + tail; out[-1]['end'] = w['end']; continue
        elif core in FIX:
            t = FIX[core] + tail
        out.append(dict(w, text=t))
    return out

def caption_groups(words, maxw=3, maxch=17):
    groups = []; cur = []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        chars = sum(len(x['text']) + 1 for x in cur)
        brk = (nxt is None or re.search(r'[.,!?]$', w['text']) or (nxt['start'] - w['end']) >= .15 or len(cur) >= maxw
               or chars + len(nxt['text']) > maxch)
        if brk: groups.append(cur); cur = []
    return groups

def captions_html(words, total, cid='captions'):
    words = clean_words(words); groups = caption_groups(words)
    els, js = [], []
    for gi, g in enumerate(groups):
        gs = max(0.05, g[0]['start'] - .06) if gi else 0.12
        nxt = groups[gi + 1][0]['start'] - .06 if gi + 1 < len(groups) else total
        ge = min(nxt, g[-1]['end'] + .45)
        em_done = False; spans = []; chars = 0
        for wi, w in enumerate(g):
            core = re.sub(r'[^a-z]', '', w['text'].lower())
            em = (not em_done) and core in EMPH
            em_done |= em
            chars += len(w['text']) * (.64 if em else .70) + .3
            cls = 'cw em' if em else 'cw'
            inner = f'<span class="gt">{H.escape(w["text"])}</span>' if em else H.escape(w['text'])
            spans.append(f'<span id="cap-w{gi}-{wi}" class="{cls}">{inner}</span>')
        fs = max(54, min(92, int(940 / chars)))
        els.append(f'<div id="cap-g{gi}" class="cg" style="font-size:{fs}px">{"".join(spans)}</div>')
        js.append(f'tl.set("#cap-g{gi}",{{opacity:1,visibility:"visible"}},{gs:.3f});')
        for wi, w in enumerate(g):
            t = max(gs, w['start'] - .05)
            js.append(f'tl.fromTo("#cap-w{gi}-{wi}",{{opacity:0,y:34,scale:.92}},{{opacity:1,y:0,scale:1,duration:.24,ease:"power3.out"}},{t:.3f});')
        js.append(f'tl.to("#cap-g{gi}",{{opacity:0,duration:.12,ease:"power2.in"}},{ge-.12:.3f});tl.set("#cap-g{gi}",{{opacity:0,visibility:"hidden"}},{ge:.3f});')
    css = BASE_CSS + """
.cg{position:absolute;left:0;top:1196px;width:1080px;text-align:center;opacity:0;visibility:hidden;white-space:nowrap}
.cw{display:inline-block;margin:0 .13em;font-family:'Syne';font-weight:700;text-transform:uppercase;color:#FBF7EF;letter-spacing:-.01em;
 text-shadow:0 3px 0 rgba(0,0,0,.35),0 8px 34px rgba(0,0,0,.85)}
.cw.em{font-family:'Bodoni Moda';font-style:italic;font-weight:700;text-transform:none;font-size:1.28em;letter-spacing:0;text-shadow:none;filter:drop-shadow(0 6px 22px rgba(0,0,0,.8))}
"""
    return scene_file(cid, ''.join(els), '\n'.join(js), css), groups

def scene_file(sid, body, js, css):
    return f'''<template>
<style>{css}</style>
<div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
{body}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{js}
window.__timelines["{sid}"] = tl;
</script>
</template>
'''

# ---------- animation helpers ----------
INS = {
 'rise': ('{opacity:0,y:60,filter:"blur(14px)"}', '{opacity:1,y:0,filter:"blur(0px)",duration:.62,ease:"power3.out"}'),
 'slam': ('{opacity:0,scale:1.45}', '{opacity:1,scale:1,duration:.4,ease:"expo.out"}'),
 'settle': ('{opacity:1,scale:1.16}', '{opacity:1,scale:1,duration:.8,ease:"power3.out"}'),
 'pop': ('{opacity:0,scale:.4}', '{opacity:1,scale:1,duration:.5,ease:"back.out(2.4)"}'),
 'left': ('{opacity:0,x:-160}', '{opacity:1,x:0,duration:.6,ease:"expo.out"}'),
 'right': ('{opacity:0,x:160}', '{opacity:1,x:0,duration:.6,ease:"expo.out"}'),
 'up': ('{opacity:0,y:260}', '{opacity:1,y:0,duration:.9,ease:"expo.out"}'),
 'down': ('{opacity:0,y:-120}', '{opacity:1,y:0,duration:.6,ease:"expo.out"}'),
 'fade': ('{opacity:0}', '{opacity:1,duration:.45,ease:"power1.out"}'),
 'zoom': ('{opacity:0,scale:.82}', '{opacity:1,scale:1,duration:.7,ease:"expo.out"}'),
 'wipe': ('{opacity:1,clipPath:"inset(0% 100% 0% 0%)"}', '{opacity:1,clipPath:"inset(0% 0% 0% 0%)",duration:.7,ease:"power3.inOut"}'),
 'track': ('{opacity:0,scaleX:1.5,transformOrigin:"0% 50%"}', '{opacity:1,scaleX:1,duration:.9,ease:"power3.out"}'),
}
def IN(sel, t, kind='rise', delay=0):
    a, b = INS[kind]; return f'tl.fromTo("{sel}",{a},{b},{t+delay:.3f});'
INDUR = {'rise': .62, 'slam': .4, 'settle': .8, 'pop': .5, 'left': .6, 'right': .6, 'up': .9, 'down': .6, 'fade': .45, 'zoom': .7, 'wipe': .7, 'track': .9}
def OUT(sel, t, kind='up', t_in=None, kin=None):
    if t_in is not None: t = max(t, t_in + INDUR.get(kin, .6) + .32)
    v = {'up': '{opacity:0,y:-50,filter:"blur(10px)",duration:.32,ease:"power2.in"}',
         'fade': '{opacity:0,duration:.3,ease:"power1.in"}',
         'shrink': '{opacity:0,scale:.85,duration:.35,ease:"power2.in"}',
         'left': '{opacity:0,x:-200,duration:.35,ease:"power2.in"}'}[kind]
    return f'tl.to("{sel}",{v},{max(0,t-.32):.3f});'

# ---------- icons (gold line art) ----------
G = '#E2C28A'
def icon(name, size=90, color=G, sw=4):
    p = {
     'sponge': f'<rect x="12" y="26" width="76" height="52" rx="14" fill="none" stroke="{color}" stroke-width="{sw}"/><circle cx="32" cy="44" r="5" fill="{color}"/><circle cx="56" cy="58" r="6" fill="{color}"/><circle cx="70" cy="40" r="4" fill="{color}"/><circle cx="40" cy="64" r="3.5" fill="{color}"/>',
     'scrub': f'<path d="M14 30 Q30 18 46 30 T78 30" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/><path d="M14 50 Q30 38 46 50 T78 50" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/><path d="M14 70 Q30 58 46 70 T78 70" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>',
     'x': f'<circle cx="50" cy="50" r="40" fill="none" stroke="#FF5A6E" stroke-width="{sw}"/><path d="M34 34 L66 66 M66 34 L34 66" stroke="#FF5A6E" stroke-width="{sw+1}" stroke-linecap="round"/>',
     'check': f'<circle cx="50" cy="50" r="40" fill="none" stroke="{color}" stroke-width="{sw}"/><path d="M32 52 L45 64 L70 37" fill="none" stroke="{color}" stroke-width="{sw+1}" stroke-linecap="round" stroke-linejoin="round"/>',
     'pump': f'<rect x="30" y="44" width="40" height="48" rx="8" fill="none" stroke="{color}" stroke-width="{sw}"/><rect x="42" y="28" width="16" height="16" fill="none" stroke="{color}" stroke-width="{sw}"/><path d="M42 28 L42 18 L74 18" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/><path d="M50 4 L50 12" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>',
     'moon': f'<path d="M64 14 A38 38 0 1 0 86 64 A30 30 0 1 1 64 14 Z" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linejoin="round"/><circle cx="76" cy="26" r="3" fill="{color}"/>',
     'sun': f'<circle cx="50" cy="50" r="18" fill="none" stroke="{color}" stroke-width="{sw}"/>' + ''.join(f'<line x1="{50+28*__import__("math").cos(a):.1f}" y1="{50+28*__import__("math").sin(a):.1f}" x2="{50+40*__import__("math").cos(a):.1f}" y2="{50+40*__import__("math").sin(a):.1f}" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>' for a in [i*0.785 for i in range(8)]),
     'drop': f'<path d="M50 10 C50 10 20 46 20 64 A30 30 0 0 0 80 64 C80 46 50 10 50 10 Z" fill="none" stroke="{color}" stroke-width="{sw}"/>',
     'wave': f'<path d="M6 50 Q20 36 34 50 T62 50 T90 50" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/><path d="M6 70 Q20 56 34 70 T62 70 T90 70" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" opacity=".6"/>',
     'leaf': f'<path d="M20 80 C20 40 50 18 84 16 C82 52 60 80 20 80 Z M20 80 L60 40" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linejoin="round"/>',
     'heart': f'<path d="M50 84 C20 62 10 46 10 32 A20 20 0 0 1 50 26 A20 20 0 0 1 90 32 C90 46 80 62 50 84 Z" fill="none" stroke="{color}" stroke-width="{sw}"/>',
     'berry': f'<circle cx="38" cy="58" r="20" fill="none" stroke="{color}" stroke-width="{sw}"/><circle cx="64" cy="62" r="18" fill="none" stroke="{color}" stroke-width="{sw}"/><path d="M48 38 C50 24 60 16 72 14" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>',
     'spark': f'<path d="M50 6 L58 42 L94 50 L58 58 L50 94 L42 58 L6 50 L42 42 Z" fill="{color}"/>',
     'nose': f'<path d="M20 40 Q50 10 80 40" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/><path d="M28 60 Q50 44 72 60" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" opacity=".7"/><path d="M36 80 Q50 70 64 80" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" opacity=".45"/>',
    }[name]
    return f'<svg width="{size}" height="{size}" viewBox="0 0 100 100">{p}</svg>'

def bag_svg(size=300):
    return f'''<svg width="{size}" height="{size}" viewBox="0 0 200 200">
<defs><linearGradient id="bagG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE15A"/><stop offset="1" stop-color="#F5A800"/></linearGradient></defs>
<path d="M66 70 C66 30 134 30 134 70" fill="none" stroke="#FFE7A0" stroke-width="12" stroke-linecap="round"/>
<path d="M36 66 L164 66 L154 176 Q152 186 142 186 L58 186 Q48 186 46 176 Z" fill="url(#bagG)"/>
<path d="M36 66 L164 66 L162 84 L38 84 Z" fill="#fff" opacity=".25"/>
<circle cx="74" cy="92" r="7" fill="#7A4A00" opacity=".6"/><circle cx="126" cy="92" r="7" fill="#7A4A00" opacity=".6"/></svg>'''

def perfume_svg(sid, size=420):
    # line-art perfume bottle with atomiser
    return f'''<svg width="{size}" height="{size*1.25:.0f}" viewBox="0 0 200 250" fill="none" stroke="{G}" stroke-width="3">
<path id="{sid}-pf-b" d="M48 104 Q48 92 60 92 L140 92 Q152 92 152 104 L152 226 Q152 238 140 238 L60 238 Q48 238 48 226 Z" stroke-dasharray="560" stroke-dashoffset="560"/>
<path id="{sid}-pf-n" d="M84 92 L84 70 L116 70 L116 92 M78 70 L122 70 L122 56 L78 56 Z M100 56 L100 40 M100 40 L72 40" stroke-dasharray="240" stroke-dashoffset="240"/>
<path d="M62 120 L62 214" stroke-width="5" stroke-linecap="round" opacity=".35"/>
<text x="100" y="172" fill="{G}" stroke="none" font-family="Bodoni Moda" font-style="italic" font-size="26" text-anchor="middle">Parfum</text>
</svg>'''

def crystals_svg(sid, size=520):
    r = random.Random(5); cubes = []
    for i, (cx, cy, s) in enumerate([(100, 120, 46), (60, 150, 30), (140, 152, 34), (104, 170, 26), (36, 176, 18), (166, 180, 20), (128, 92, 22)]):
        top = f'{cx},{cy-s*.5} {cx+s*.87},{cy} {cx},{cy+s*.5} {cx-s*.87},{cy}'
        left = f'{cx-s*.87},{cy} {cx},{cy+s*.5} {cx},{cy+s*1.5} {cx-s*.87},{cy+s}'
        right = f'{cx+s*.87},{cy} {cx},{cy+s*.5} {cx},{cy+s*1.5} {cx+s*.87},{cy+s}'
        cubes.append(f'<g id="{sid}-cr{i}"><polygon points="{top}" fill="#FFFFFF" fill-opacity=".92"/><polygon points="{left}" fill="#C9D6F2" fill-opacity=".85"/><polygon points="{right}" fill="#8EA2D2" fill-opacity=".85"/><polyline points="{top}" fill="none" stroke="#fff" stroke-width="1.5"/></g>')
    return f'<svg width="{size}" height="{size}" viewBox="0 0 200 220">{"".join(cubes)}</svg>'

def fit_html(h):
    """Shrink font-size of syne/bod spans so each line fits 950px."""
    def f(m):
        cls, size, rest, txt = m.group(1), int(m.group(2)), m.group(3), m.group(4)
        plain = re.sub(r'<[^>]+>', '', txt); plain = H.unescape(plain)
        k = 1.32 if 'x8' in cls else (.70 if 'syne' in cls else (.58 if 'bod' in cls else None))
        if k is None or not plain: return m.group(0)
        n = len(plain) - plain.count(' ') * .6
        fs = min(size, int(950 / (n * k)))
        return f'<span class="{cls}" style="font-size:{fs}px{rest}">{txt}</span>'
    return re.sub(r'<span class="([^"]*)" style="font-size:(\d+)px([^"]*)">(.*?)</span>', f, h)
