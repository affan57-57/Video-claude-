# Generates the HyperFrames composition (index.html) for the FRESCURA BODY ad.
import json, random, html
W = json.load(open('/home/user/work/a/words_final.json'))
assert len(W) == 101
SPLIT, GAP = 23.46, 1.40
FIX = {7: 'bernyala?', 69: 'ikut', 70: 'mood', 73: 'varian', 76: 'warna'}
for i, w in enumerate(W):
    if i in FIX: w['w'] = FIX[i]
    if w['s'] >= SPLIT: w['s'] += GAP; w['e'] += GAP
# merge hyphen pairs
def word(i):
    if i in (12, 66): return dict(w=W[i]['w'] + W[i+1]['w'], s=W[i]['s'], e=W[i+1]['e'])
    return W[i]
PAGES = [[5,6,7],[8,9,10,11],[12,14,15],[16,17],[18,19,20],[21,22,23],[24,25,26],[27,28,29],[30,31,32,33],[34,35],
         [36,37,38],[39,40],[41,42],[43,44,45,46],[47,48],[49,50,51,52],[53,54,55],[56,57,58],[59,60,61],
         [62,63,64],[65,66],[68,69,70],[71,72,73,74],[75,76,77,78],[79],[80,81],[82,83,84],[85,86,87,88],
         [89,90,91],[92,93,94],[95,96,97],[98,99,100]]
KEY = {'bernyala','misteri','frescura','body','woman','glory','bombshell','yakin','noche','midnight','fantasy','istimewa',
       'perfume','garam','laut','mineral','lembut','kedua-duanya','mood','terhad','batch','beg','kuning','checkout','terlambat','habis','penjagaan'}
LIGHT = [(13.6, 16.4), (21.95, 23.5)]
END_SPEECH = 38.85
cap_html, cap_js = [], []
for pi, idx in enumerate(PAGES):
    ws = [word(i) for i in idx]
    start = ws[0]['s'] - 0.06
    nxt = word(PAGES[pi+1][0])['s'] - 0.06 if pi + 1 < len(PAGES) else END_SPEECH
    end = min(nxt, ws[-1]['e'] + 0.3)
    dark = any(a <= start + 0.05 < b for a, b in LIGHT)
    spans = []
    for k, w in enumerate(ws):
        txt = w['w'].strip(',.')
        bare = txt.strip('?').lower()
        cls = 'w key' if bare in KEY else 'w'
        shown = txt if bare in KEY else txt.upper()
        spans.append(f'<span class="{cls}" id="w{pi}_{k}">{html.escape(shown)}</span>')
        nx = ws[k+1]['s'] if k + 1 < len(ws) else end
        cap_js.append(f'cw("#w{pi}_{k}",{w["s"]:.3f},{nx:.3f},{str(bare in KEY).lower()},{str(dark).lower()});')
    cap_html.append(f'<div class="cap clip{" dark" if dark else ""}" id="cap{pi}" data-start="{start:.3f}" data-duration="{end-start:.3f}" data-track-index="20">{" ".join(spans)}</div>')
    cap_js.append(f'cp("#cap{pi}",{start:.3f});')

rnd = random.Random(7)
def particles(prefix, n, cls):
    out = []
    for i in range(n):
        out.append(f'<i class="{cls}" id="{prefix}{i}" style="left:{rnd.uniform(0,1040):.0f}px;top:{rnd.uniform(0,1900):.0f}px;'
                   f'--s:{rnd.uniform(0.5,1.25):.2f}"></i>')
    return ''.join(out)

TPL = open('/home/user/work/scripts/template.html').read()
out = (TPL.replace('%%CAPTIONS%%', '\n'.join(cap_html))
          .replace('%%CAPJS%%', '\n'.join(cap_js))
          .replace('%%PETALS%%', particles('pt', 22, 'petal'))
          .replace('%%STARS%%', particles('st', 80, 'star'))
          .replace('%%STARS2%%', particles('su', 60, 'star'))
          .replace('%%STARS3%%', particles('sv', 70, 'star'))
          .replace('%%DUST%%', particles('du', 46, 'dust'))
          .replace('%%BUBBLES%%', particles('bu', 18, 'bubble')))
open('/home/user/work/proj/index.html', 'w').write(out)
print('pages', len(PAGES), 'written', len(out))
for pi, idx in enumerate(PAGES):
    print(pi, f"{word(idx[0])['s']:.2f}", ' '.join(word(i)['w'] for i in idx))
