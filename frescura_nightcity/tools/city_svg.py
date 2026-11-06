# Night-city skyline generator: KLCC, Bukit Bintang, Komtar (Penang), Menara Alor Setar (Kedah).
# Writes <out>/<name>.svg (static, rendered to PNG later) and <out>/<name>.json (twinkle/beacon overlay data).
import random, json, sys, math
W, H, BASE = 1200, 1920, 1360

def grad_defs():
    return f'''<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
 <stop offset="0" stop-color="#03050C"/><stop offset=".38" stop-color="#070C1E"/>
 <stop offset=".60" stop-color="#121633"/><stop offset=".69" stop-color="#2A1838"/>
 <stop offset=".71" stop-color="#3A1E33"/><stop offset=".72" stop-color="#0A0E1E"/><stop offset="1" stop-color="#03040A"/></linearGradient>
<radialGradient id="haze" cx=".5" cy=".7" r=".55"><stop offset="0" stop-color="#FFB27A" stop-opacity=".30"/>
 <stop offset=".45" stop-color="#C2477A" stop-opacity=".12"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
<linearGradient id="bld" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#121a36"/><stop offset="1" stop-color="#070a17"/></linearGradient>
<linearGradient id="bldFar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a2246"/><stop offset="1" stop-color="#0d1330"/></linearGradient>
<linearGradient id="pet" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F4F1EA"/><stop offset=".5" stop-color="#C9CCD8"/><stop offset="1" stop-color="#7C819C"/></linearGradient>
<linearGradient id="cyl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0a0f22"/><stop offset=".45" stop-color="#2a3358"/><stop offset=".6" stop-color="#3a4570"/><stop offset="1" stop-color="#0a0f22"/></linearGradient>
<linearGradient id="gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE7B8"/><stop offset="1" stop-color="#C99A55"/></linearGradient>
<linearGradient id="refl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset=".55" stop-color="#fff" stop-opacity="0"/></linearGradient>
<mask id="reflMask"><rect x="0" y="{BASE}" width="{W}" height="{H-BASE}" fill="url(#refl)"/></mask>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>
<filter id="glowS" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5"/></filter>
<filter id="blurR"><feGaussianBlur stdDeviation="3 9"/></filter>
</defs>'''

class Sky:
    def __init__(s, seed):
        s.r = random.Random(seed); s.parts = []; s.glow = []; s.twinkle = []; s.beacons = []
    def add(s, x): s.parts.append(x)
    def windows(s, x, y, w, h, p=.35, cw=13, ch=19, warm=True, tw=3):
        r = s.r; out = []; cands = []
        cols = max(1, int((w - 8) // cw)); rows = max(1, int((h - 10) // ch))
        ox = x + (w - cols * cw) / 2 + 3
        for i in range(rows):
            for j in range(cols):
                if r.random() < p:
                    wx, wy = ox + j * cw, y + 10 + i * ch
                    c = r.choice(['#FFD9A0', '#FFE6BF', '#FFC27A'] if warm else ['#CFE3FF', '#E6F0FF'])
                    a = r.uniform(.35, .95)
                    out.append(f'<rect x="{wx:.1f}" y="{wy:.1f}" width="6" height="9" fill="{c}" opacity="{a:.2f}"/>')
                    cands.append((wx, wy))
        r.shuffle(cands); s.twinkle += [c for c in cands[:tw]]
        s.add(''.join(out))
    def building(s, x, w, h, far=False, p=.32, rim=True, warm=True, tw=2):
        y = BASE - h
        s.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{"bldFar" if far else "bld"})"/>')
        if rim: s.add(f'<line x1="{x}" y1="{y}" x2="{x+w}" y2="{y}" stroke="#FFB98A" stroke-opacity=".22" stroke-width="2"/>')
        if not far: s.windows(x, y, w, h - 6, p, warm=warm, tw=tw)
        else: s.windows(x, y, w, h - 6, p * .5, warm=warm, tw=0)
    def filler(s, x0, x1, hmin, hmax, far=False, p=.3):
        x = x0
        while x < x1:
            w = s.r.randint(60, 130); h = s.r.randint(hmin, hmax)
            s.building(x, w, h, far=far, p=p); x += w + s.r.randint(-6, 10)
    def svg(s, extra_bg=''):
        body = ''.join(s.parts); glow = ''.join(s.glow)
        stars = ''.join(f'<circle cx="{s.r.uniform(0,W):.0f}" cy="{s.r.uniform(40,760):.0f}" r="{s.r.uniform(.6,1.8):.1f}" fill="#fff" opacity="{s.r.uniform(.15,.7):.2f}"/>' for _ in range(70))
        city = f'<g id="city">{glow and f"<g filter=\"url(#glow)\" opacity=\".75\">{glow}</g>"}{body}</g>'
        return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{grad_defs()}
<rect width="{W}" height="{H}" fill="url(#sky)"/>{stars}
<rect width="{W}" height="{H}" fill="url(#haze)"/>{extra_bg}
{city}
<g mask="url(#reflMask)" opacity=".38"><g transform="translate(0,{2*BASE}) scale(1,-1)" filter="url(#blurR)"><use xlink:href="#city"/></g></g>
<rect x="0" y="{BASE}" width="{W}" height="2" fill="#FFCFA0" opacity=".25"/>
</svg>'''

def moon(x, y, r=46):
    return (f'<mask id="mm{x}"><rect width="1200" height="1920" fill="#fff"/><circle cx="{x+r*.42}" cy="{y-r*.22}" r="{r*.92}" fill="#000"/></mask>'
            f'<g opacity=".95" mask="url(#mm{x})"><circle cx="{x}" cy="{y}" r="{r*1.6}" fill="#F3E3C0" opacity=".05"/><circle cx="{x}" cy="{y}" r="{r}" fill="#F5E9CF"/></g>')

def petronas(s, cx):
    tiers = [(BASE, 790, 78), (790, 680, 68), (680, 605, 58), (605, 548, 48), (548, 506, 38), (506, 474, 28)]
    pts_l, pts_r = [], []
    for (y0, y1, hw) in tiers:
        pts_l += [(cx - hw, y0), (cx - hw, y1)]; pts_r += [(cx + hw, y0), (cx + hw, y1)]
    pts = pts_l + [(cx - 10, 474), (cx - 6, 400), (cx - 3, 330), (cx, 250), (cx + 3, 330), (cx + 6, 400), (cx + 10, 474)] + pts_r[::-1]
    poly = ' '.join(f'{x:.0f},{y:.0f}' for x, y in pts)
    s.glow.append(f'<polygon points="{poly}" fill="#E9E2FF" opacity=".55"/>')
    s.add(f'<polygon points="{poly}" fill="url(#pet)" opacity=".93"/>')
    lines = []
    for (y0, y1, hw) in tiers:
        for k in range(-hw + 8, hw - 4, 9):
            lines.append(f'<line x1="{cx+k}" y1="{y0}" x2="{cx+k}" y2="{y1+3}" stroke="#5A607C" stroke-width="1.6" opacity=".55"/>')
        lines.append(f'<line x1="{cx-hw}" y1="{y1}" x2="{cx+hw}" y2="{y1}" stroke="#FFFFFF" stroke-width="2.4" opacity=".9"/>')
    for y in range(820, BASE, 34):
        lines.append(f'<line x1="{cx-78}" y1="{y}" x2="{cx+78}" y2="{y}" stroke="#fff" stroke-width="1" opacity=".22"/>')
    s.add(''.join(lines)); s.beacons.append((cx, 252))

def menara_kl(s, cx):
    s.add(f'<polygon points="{cx-16},{BASE} {cx-10},{720} {cx+10},{720} {cx+16},{BASE}" fill="url(#bld)"/>')
    s.add(f'<path d="M{cx-52},{722} Q{cx},{650} {cx+52},{722} L{cx+40},{748} Q{cx},{765} {cx-40},{748} Z" fill="#1b2346"/>')
    s.add(f'<rect x="{cx-46}" y="{712}" width="92" height="8" fill="#FFD9A0" opacity=".8"/>')
    s.glow.append(f'<rect x="{cx-50}" y="{700}" width="100" height="30" fill="#FFC27A"/>')
    s.add(f'<rect x="{cx-6}" y="{600}" width="12" height="70" fill="#1b2346"/><line x1="{cx}" y1="{600}" x2="{cx}" y2="{470}" stroke="#8a90b0" stroke-width="3"/>')
    s.beacons.append((cx, 470))

def merdeka(s, cx):
    pts = [(cx - 70, BASE), (cx - 58, 700), (cx - 40, 470), (cx - 14, 330), (cx, 160), (cx + 14, 330), (cx + 40, 470), (cx + 58, 700), (cx + 70, BASE)]
    poly = ' '.join(f'{x},{y}' for x, y in pts)
    s.add(f'<polygon points="{poly}" fill="#151c3c"/>')
    s.add(f'<polyline points="{cx-58},700 {cx-40},470 {cx-14},330 {cx},160" fill="none" stroke="#E8C690" stroke-width="2" opacity=".75"/>')
    s.add(f'<polyline points="{cx+58},700 {cx+40},470 {cx+14},330 {cx},160" fill="none" stroke="#E8C690" stroke-width="1.4" opacity=".45"/>')
    s.windows(cx - 50, 720, 100, 600, .25, tw=2); s.beacons.append((cx, 162))

def build_klcc():
    s = Sky(11)
    s.filler(-20, 1220, 260, 520, far=True)
    merdeka(s, 1010); menara_kl(s, 150)
    s.filler(-20, 300, 140, 380, p=.3); s.filler(820, 1220, 160, 420, p=.3)
    petronas(s, 470); petronas(s, 730)
    # skybridge
    s.add(f'<rect x="{470+78}" y="862" width="{730-470-156}" height="16" fill="#D9DCE8"/><rect x="{470+78}" y="866" width="{730-470-156}" height="6" fill="#FFF3D6" opacity=".9"/>')
    s.add(f'<polyline points="{470+78},990 {600},878 {730-78},990" fill="none" stroke="#C9CCD8" stroke-width="5"/>')
    s.filler(-20, 1220, 70, 200, p=.38)
    return s, moon(880, 360, 40)

def build_bb():
    s = Sky(23)
    s.filler(-20, 1220, 380, 760, far=True)
    x = -10; neon = ['#FF3D7F', '#37E3FF', '#FFB347', '#C08BFF', '#FF6A3D']; k = 0
    while x < 1220:
        w = s.r.randint(120, 200); h = s.r.randint(380, 860); y = BASE - h
        s.building(x, w, h, p=.28, tw=2)
        c = neon[k % len(neon)]; k += 1
        if k % 2 == 0:  # vertical neon sign strip
            sx = x + s.r.randint(14, w - 40); sy = y + s.r.randint(60, 200); sh = s.r.randint(160, 300)
            s.add(f'<rect x="{sx}" y="{sy}" width="26" height="{sh}" rx="4" fill="{c}" opacity=".9"/>')
            s.add(''.join(f'<rect x="{sx+6}" y="{sy+12+i*30}" width="14" height="18" rx="2" fill="#fff" opacity=".55"/>' for i in range(int(sh // 30) - 1)))
            s.glow.append(f'<rect x="{sx-6}" y="{sy}" width="38" height="{sh}" fill="{c}"/>')
        else:  # LED facade screen
            sx = x + 14; sw = w - 28; sy = y + 70; sh = min(240, h - 220)
            if sh > 80:
                s.add(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="6" fill="{c}" opacity=".55"/>')
                s.add(f'<rect x="{sx+10}" y="{sy+sh*.35:.0f}" width="{sw-20}" height="10" fill="#fff" opacity=".6"/><rect x="{sx+10}" y="{sy+sh*.55:.0f}" width="{(sw-20)*.6:.0f}" height="8" fill="#fff" opacity=".45"/>')
                s.glow.append(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" fill="{c}"/>')
        x += w + s.r.randint(4, 14)
    # monorail track
    s.add(f'<rect x="-20" y="1150" width="1240" height="18" fill="#0b0f22"/><rect x="-20" y="1150" width="1240" height="3" fill="#FFD9A0" opacity=".35"/>')
    s.add(''.join(f'<rect x="{px}" y="1168" width="22" height="{BASE-1168}" fill="#090c1c"/>' for px in range(40, 1200, 210)))
    s.filler(-20, 1220, 60, 150, p=.4)
    return s, ''

def build_komtar():
    s = Sky(37)
    hill = f'<path d="M-20,{BASE} C120,980 300,930 470,1010 C620,1080 760,900 980,960 C1100,990 1180,1050 1220,1080 L1220,{BASE} Z" fill="#0b1128"/>'
    hill += ''.join(f'<circle cx="{120+i*37}" cy="{1000+ (i%5)*14}" r="2" fill="#FFD9A0" opacity=".6"/>' for i in range(26))
    s.add(hill)
    s.filler(-20, 1220, 200, 420, far=True)
    cx, top, R = 620, 340, 105
    s.glow.append(f'<rect x="{cx-R}" y="{top}" width="{2*R}" height="{BASE-top}" rx="{R}" fill="#8FA4FF" opacity=".35"/>')
    s.add(f'<rect x="{cx-R}" y="{top}" width="{2*R}" height="{BASE-top}" fill="url(#cyl)"/>')
    s.add(f'<ellipse cx="{cx}" cy="{top}" rx="{R}" ry="18" fill="#2c3660"/>')
    bands = []
    for i, y in enumerate(range(top + 30, BASE - 10, 15)):
        a = .25 + .6 * ((i * 7) % 5) / 5
        bands.append(f'<path d="M{cx-R+6},{y} Q{cx},{y+10} {cx+R-6},{y}" stroke="#FFE2B0" stroke-width="2.2" fill="none" opacity="{a:.2f}"/>')
    s.add(''.join(bands))
    s.add(f'<rect x="{cx-40}" y="{top-70}" width="80" height="70" fill="#1d2548"/><rect x="{cx-40}" y="{top-40}" width="80" height="6" fill="#37E3FF" opacity=".8"/>')
    s.glow.append(f'<rect x="{cx-46}" y="{top-46}" width="92" height="16" fill="#37E3FF"/>')
    s.add(f'<line x1="{cx}" y1="{top-70}" x2="{cx}" y2="{top-210}" stroke="#8a90b0" stroke-width="4"/>')
    s.beacons.append((cx, top - 210))
    # The Top
    s.building(820, 120, 560, p=.25); s.add(f'<rect x="820" y="{BASE-560}" width="120" height="8" fill="#C08BFF" opacity=".8"/>')
    s.glow.append(f'<rect x="815" y="{BASE-566}" width="130" height="18" fill="#C08BFF"/>')
    s.filler(-20, 470, 140, 380, p=.32); s.filler(960, 1220, 160, 340, p=.32)
    s.filler(-20, 1220, 60, 170, p=.4)
    return s, moon(170, 330, 40)

def build_alorsetar():
    s = Sky(53)
    s.filler(-20, 1220, 160, 360, far=True)
    cx = 640
    s.add(f'<polygon points="{cx-34},{BASE} {cx-17},{640} {cx+17},{640} {cx+34},{BASE}" fill="url(#bld)"/>')
    s.add(f'<line x1="{cx}" y1="{BASE}" x2="{cx}" y2="660" stroke="#FFD9A0" stroke-width="2" opacity=".35"/>')
    # pod
    s.add(f'<path d="M{cx-78},612 Q{cx},540 {cx+78},612 Q{cx+60},668 {cx},676 Q{cx-60},668 {cx-78},612 Z" fill="#1e2750"/>')
    s.add(f'<path d="M{cx-74},612 Q{cx},628 {cx+74},612" stroke="url(#gold)" stroke-width="7" fill="none"/>')
    s.add(''.join(f'<circle cx="{cx-60+i*12}" cy="{596+ (abs(5-i))*1.5:.0f}" r="2.6" fill="#FFE6BF"/>' for i in range(11)))
    s.glow.append(f'<ellipse cx="{cx}" cy="610" rx="90" ry="40" fill="#FFC27A" opacity=".8"/>')
    s.add(f'<rect x="{cx-22}" y="540" width="44" height="40" rx="8" fill="#2a3360"/><rect x="{cx-22}" y="556" width="44" height="5" fill="#37E3FF" opacity=".85"/>')
    s.add(f'<polygon points="{cx-8},540 {cx},330 {cx+8},540" fill="#8a90b0"/>')
    s.beacons.append((cx, 332))
    # Masjid Zahir style domes (silhouette with gold rims)
    for (dx, r) in [(170, 48), (260, 34), (90, 30)]:
        s.add(f'<rect x="{dx-r}" y="{1210}" width="{2*r}" height="{BASE-1210}" fill="#0b1024"/>'
              f'<path d="M{dx-r},1212 A{r},{r*1.1} 0 0 1 {dx+r},1212 Z" fill="#0b1024" stroke="#E8C690" stroke-width="2.4"/>'
              f'<line x1="{dx}" y1="{1212-r*1.1}" x2="{dx}" y2="{1212-r*1.1-26}" stroke="#E8C690" stroke-width="2"/>')
    s.add(f'<rect x="330" y="1020" width="18" height="{BASE-1020}" fill="#0b1024" stroke="#E8C690" stroke-width="1.5"/><path d="M324,1020 L339,990 L354,1020 Z" fill="#E8C690"/>')
    s.filler(400, 560, 160, 420, p=.3); s.filler(720, 1220, 180, 460, p=.3)
    s.filler(-20, 1220, 50, 140, p=.4)
    return s, moon(980, 360, 42)

if __name__ == '__main__':
    out = sys.argv[1]
    for name, fn in [('klcc', build_klcc), ('bb', build_bb), ('komtar', build_komtar), ('alorsetar', build_alorsetar)]:
        s, extra = fn()
        open(f'{out}/{name}.svg', 'w').write(s.svg(extra))
        json.dump({'twinkle': s.twinkle, 'beacons': s.beacons}, open(f'{out}/{name}.json', 'w'))
        print(name, len(s.twinkle), 'twinkles', len(s.beacons), 'beacons')
