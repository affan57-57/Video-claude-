# Build a HyperFrames project for V1 (a1 voice-only) or V2 (a2 talking head).
# Usage: build.py v1|v2 <scratch_dir>
import sys, os, json, shutil, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
from comp import *

V, S = sys.argv[1], sys.argv[2]
W = f'{S}/work'; P = f'{S}/proj_{V}'
src = {'v1': 'a1', 'v2': 'a2'}[V]
edl = json.load(open(f'{W}/{src}.edl.json')); words = edl['words']; VD = edl['duration']
T, E, PREV = anchors(words)
TAIL = 1.0; TOTAL = round(VD + TAIL, 3)

# ---------------- assets ----------------
for d in ['assets/fonts', 'assets/city', 'assets/sfx', 'compositions']: os.makedirs(f'{P}/{d}', exist_ok=True)
for f in os.listdir(f'{S}/fonts'):
    if f.endswith('.woff2'): shutil.copy(f'{S}/fonts/{f}', f'{P}/assets/fonts/{f}')
shutil.rmtree(f'{P}/assets/city', ignore_errors=True); os.makedirs(f'{P}/assets/city')
for n in ['klcc_hero', 'klcc_up', 'klcc_cloud', 'komtar_n', 'penang_lights', 'alor_hdr_n', 'ramlee', 'kl_skyline']: shutil.copy(f'{S}/realbg/{n}.jpg', f'{P}/assets/city/{n}.jpg')
shutil.copy(f'{S}/realbg/bb_monorail.mp4', f'{P}/assets/city/bb_monorail.mp4')
SFXD = '/root/.claude/skills/media-use/audio/assets/sfx'
for f in os.listdir(SFXD):
    if f.endswith('.mp3') or f == 'CREDITS.md': shutil.copy(f'{SFXD}/{f}', f'{P}/assets/sfx/{f}')
for f in ['bottle.png', 'music.m4a', 'broll_pump.mp4', 'broll_close.mp4', 'broll_foam.mp4', 'broll_lather.mp4']:
    shutil.copy(f'{S}/assets/{f}', f'{P}/assets/{f}')
shutil.copy(f'{W}/{src}.voice_cut.wav', f'{P}/assets/voice.wav')
if V == 'v2': shutil.copy(f'{W}/a2_aroll.mp4', f'{P}/assets/aroll.mp4')

scenes = []; cues = []
def sfx(t, n, v=.5): cues.append((t, n, v))

if V == 'v1':
    b_three, b_p1 = T('Tiga'), T('Pertama')
    b_p2 = PREV('kedua'); b_p3 = PREV('ketiga'); b_q = T('Kau', T('wangi', b_p3 + 1)); b_cta = T('Tapi', b_q)
    # HOOK
    s = Scene('hook', 0, b_three)
    s.text('tag', '<span class="syn">◆ Sebelum kau beli sabun baru</span>', 300, 0, T('tengok'), 'fade')
    s.text('l1', '<span class="syne x8 shadow" style="font-size:160px">Jangan</span>', 370, 0, T('tengok'), 'settle')
    s.text('l2', '<span class="syne shadow" style="font-size:120px">beli sabun</span>', 535, 0, T('tengok'), 'settle')
    s.text('l3', '<span class="bod gt" style="font-size:160px">dulu…</span>', 650, 0.05, T('tengok'), 'settle')
    s.text('m1', '<span class="syne x8 shadow" style="font-size:190px">Tengok</span>', 400, T('tengok'), T('Jangan'), 'slam')
    s.text('m2', '<span class="bod gt" style="font-size:170px">ni dulu.</span>', 590, T('ni'), T('Jangan'), 'slam')
    s.text('n1', '<span class="syne shadow" style="font-size:100px">Jangan sampai</span>', 330, T('Jangan'), None, 'rise')
    s.text('n2', '<span class="syne x8 gt" style="font-size:240px;line-height:.9">DUIT</span>', 450, T('duit'), None, 'slam')
    s.text('n3', '<span class="bod" style="font-size:160px;color:#FF5A6E">terbazir.</span>', 690, T('terbazir'), None, 'slam')
    s.coins(T('duit') + .1)
    scenes.append(s)
    sfx(0.0, 'impact-bass-1', .55); sfx(T('tengok'), 'whoosh', .5); sfx(T('ni') + .1, 'pop', .35); sfx(T('duit'), 'impact-bass-2', .45); sfx(T('terbazir'), 'glitch-3', .9)
    # THREE + REVEAL
    s = Scene('three', b_three, b_p1)
    s.text('n', '<span class="bod gt" style="font-size:520px;font-style:normal;font-weight:400;line-height:.8">3</span>', 250, b_three, T('Frescura') if False else T('fresh', b_three), 'zoom')
    s.text('t', '<span class="syne x8 shadow" style="font-size:110px">Benda</span>', 700, b_three + .15, T('fresh', b_three), 'rise')
    s.text('s', '<span class="bod" style="font-size:70px;color:rgba(246,241,231,.85)">sabun biasa <span style="color:#FF5A6E">tak boleh bagi</span></span>', 830, T('tak', b_three), T('fresh', b_three), 'rise')
    s.bottle('btl', T('fresh', b_three) - .1, None, top=300, h=720)
    s.text('brand', '<span class="syn" style="font-size:26px">Frescura Body</span>', 1110, T('fresh', b_three) + .4, None, 'track')
    s.particles('sp', T('body', b_three), 540, 640, 20, 380)
    scenes.append(s)
    sfx(b_three, 'whoosh-cinematic', .45); sfx(T('tak', b_three), 'pop', .35); sfx(T('fresh', b_three), 'impact-bass-1', .6); sfx(T('body', b_three) + .1, 'sparkle', .55)
    # POINT 1 — BUIH SIAP-SIAP
    s = Scene('p1', b_p1, b_p2)
    tb = T('tekan', b_p1)
    s.header('01', 'Buih', 'siap-siap.', b_p1, T('Tak', b_p1) + .05)
    s.chip('c1', icon('sponge', 84), 'Tak perlu span', 120, 430, T('span', b_p1) - .1, tb, 'left', w=840)
    s.add(f'<div id="p1-x1" class="abs h" style="left:850px;top:450px">{icon("x",80)}</div>'); s.a(IN('#p1-x1', s.t(T('span', b_p1)) + .2, 'pop')); s.a(OUT('#p1-x1', s.t(tb), 'fade'))
    s.chip('c2', icon('scrub', 84), 'Tak perlu gosok', 120, 640, T('gosok', b_p1) - .1, tb, 'left', w=840)
    s.add(f'<div id="p1-x2" class="abs h" style="left:850px;top:660px">{icon("x",80)}</div>'); s.a(IN('#p1-x2', s.t(T('gosok', b_p1)) + .2, 'pop')); s.a(OUT('#p1-x2', s.t(tb), 'fade'))
    s.text('only', '<span class="bod gt" style="font-size:84px">cuma tekan pam.</span>', 860, T('gosok', b_p1) + .35, tb, 'rise')
    tbu = T('bui', tb)
    s.broll('br1', 'broll_pump.mp4', tb, tbu, 0.6, 'Tekan pam', label_icon='pump')
    s.broll('br2', 'broll_foam.mp4', tbu, b_p2, 0.4, 'Buih lembut')
    scenes.append(s)
    sfx(b_p1, 'whoosh', .5); sfx(b_p1 + .05, 'ping', .9); sfx(T('span', b_p1) + .2, 'pop', .4); sfx(T('gosok', b_p1) + .2, 'pop', .4); sfx(tb, 'whoosh-cinematic', .4); sfx(tb + .5, 'click', .5); sfx(tbu, 'sparkle', .5)
    # POINT 2 — OCEAN SALT
    s = Scene('p2', b_p2, b_p3)
    tk = T('kaya', b_p2); tku = T('kulit', b_p2)
    s.header('02', 'Ocean salt', 'garam laut.', b_p2, tk)
    s.add(f'<div id="p2-cr" class="abs h" style="left:290px;top:330px">{crystals_svg("p2",500)}</div>')
    s.a(IN('#p2-cr', s.t(tk) - .1, 'zoom')); s.a(OUT('#p2-cr', s.t(tku), 'shrink'))
    s.a(f'tl.fromTo("#p2-cr",{{y:0}},{{y:-20,duration:.8,repeat:5,yoyo:true,ease:"sine.inOut",immediateRender:false}},{s.t(tk):.3f});')
    s.text('mt', '<span class="syn" style="font-size:22px">Mineral semula jadi</span>', 870, tk, tku, 'track')
    for k, (sym, nm_) in enumerate([('Mg', 'Magnesium'), ('Ca', 'Kalsium'), ('K', 'Kalium')]):
        x = 95 + k * 305
        s.add(f'<div id="p2-m{k}" class="abs h glass" style="left:{x}px;top:930px;width:280px;height:200px;display:flex;flex-direction:column;align-items:center;justify-content:center;border-radius:28px">'
              f'<span class="bod gt" style="font-size:96px;font-style:normal;font-weight:700">{sym}</span><span style="font-family:Syne;font-weight:700;font-size:26px;color:#F6F1E7;letter-spacing:.1em;text-transform:uppercase">{nm_}</span></div>')
        s.a(IN(f'#p2-m{k}', s.t(T('mineral', b_p2)) + k * .22, 'pop')); s.a(OUT(f'#p2-m{k}', s.t(tku), 'fade'))
        sfx(T('mineral', b_p2) + k * .22, 'pop', .35)
    s.broll('br', 'broll_lather.mp4', tku, b_p3, 0.0, 'Segar macam mandi laut', label_icon='wave')
    scenes.append(s)
    sfx(b_p2, 'whoosh', .5); sfx(b_p2 + .05, 'ping', .9); sfx(tk - .1, 'sparkle', .45); sfx(tku, 'whoosh-cinematic', .4)
    # POINT 3 — WANGI PERFUME
    s = Scene('p3', b_p3, b_q)
    tpi = T('Pilih', b_p3); tat = T('atau', tpi); tke = T('Keluar', b_p3)
    s.header('03', 'Wangi', 'perfume.', b_p3, tpi)
    s.add(f'<div id="p3-pf" class="abs h" style="left:330px;top:640px">{perfume_svg("p3",420)}</div>')
    s.a(IN('#p3-pf', s.t(T('wangi', b_p3)) - .2, 'fade')); s.a(OUT('#p3-pf', s.t(tpi), 'fade'))
    s.a(f'tl.to("#p3-pf-b",{{strokeDashoffset:0,duration:.9,ease:"power2.inOut"}},{s.t(T("wangi", b_p3))-.2:.3f});tl.to("#p3-pf-n",{{strokeDashoffset:0,duration:.6,ease:"power2.inOut"}},{s.t(T("wangi", b_p3))+.3:.3f});')
    s.particles('mist', T('perfume', b_p3), 470, 690, 20, 300)
    s.scent_card('bs', 'Bombshell', 300, tpi, ['Fresh', 'Feminine'], 'sun', 'Siang · hari-hari')
    s.scent_card('mf', 'Midnight Fantasy', 690, tat, ['Manis', 'Fruity'], 'moon', 'Malam')
    s.a(OUT('#p3-bs', s.t(tke), 'left')); s.a(OUT('#p3-mf', s.t(tke), 'left'))
    s.text('k1', '<span class="syne shadow" style="font-size:100px">Keluar bilik air</span>', 430, tke, None, 'rise')
    s.text('k2', '<span class="bod gt" style="font-size:190px">terus wangi.</span>', 560, T('terus', tke), None, 'slam')
    s.particles('aura', T('terus', tke), 540, 760, 26, 460)
    scenes.append(s)
    sfx(b_p3, 'whoosh', .5); sfx(b_p3 + .05, 'ping', .9); sfx(T('perfume', b_p3), 'sparkle', .55); sfx(tpi, 'whoosh', .45); sfx(tat, 'whoosh', .45); sfx(tke, 'whoosh-cinematic', .35); sfx(T('terus', tke), 'sparkle', .6)
    # QUESTION — sabun biasa vs Frescura
    s = Scene('q', b_q, b_cta)
    tns = T('nak', T('atau', b_q)); tor = T('orang', b_q); tpl = T('Pilihan', b_q)
    s.add(f'<div id="q-a" class="abs h glass" style="left:70px;top:300px;width:450px;height:640px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:28px;filter:grayscale(1)">'
          f'<div style="width:220px;height:140px;border-radius:40px;background:linear-gradient(160deg,#d7d7d7,#8d8d8d);box-shadow:inset 0 -10px 20px rgba(0,0,0,.25)"></div>'
          f'<span class="syne" style="font-size:58px;color:#bdbdbd">Sabun<br>biasa</span><span style="font-family:Syne;font-size:28px;color:#9a9a9a;letter-spacing:.12em">BAU BIASA JE</span></div>')
    s.add(f'<div id="q-b" class="abs h glass" style="left:560px;top:300px;width:450px;height:640px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:20px;border-color:rgba(232,198,144,.9);box-shadow:0 0 80px rgba(226,194,138,.35)">'
          f'<img src="assets/bottle.png" style="width:118px;height:352px"><span class="bod gt" style="font-size:72px;font-weight:700">Frescura</span><span style="font-family:Syne;font-size:28px;color:#F6F1E7;letter-spacing:.12em">BAU PERFUME</span></div>')
    s.add('<div id="q-vs" class="abs h" style="left:490px;top:570px;width:100px;height:100px;border-radius:50%;z-index:5;background:#0b0e1c;border:1.5px solid rgba(232,198,144,.8);display:flex;align-items:center;justify-content:center"><span style="font-family:Syne;font-weight:800;font-size:34px;color:#E2C28A">VS</span></div>')
    s.a(IN('#q-a', 0, 'left')); s.a(IN('#q-vs', .3, 'pop')); s.a(IN('#q-b', s.t(tns), 'right'))
    s.a(f'tl.to("#q-a",{{opacity:.35,scale:.94,duration:.4}},{s.t(tns):.3f});tl.fromTo("#q-b",{{scale:1}},{{scale:1.04,duration:.4,ease:"back.out(2)",immediateRender:false}},{s.t(tns)+.4:.3f});')
    s.add(f'<div id="q-bub" class="abs h" style="left:150px;top:980px;padding:24px 38px;border-radius:36px 36px 36px 8px;background:rgba(246,241,231,.95);font-family:Syne;font-weight:700;font-size:42px;color:#141018">“Pakai perfume apa ni?”</div>')
    s.a(IN('#q-bub', s.t(tor), 'pop'))
    for n_ in ['q-a', 'q-b', 'q-vs', 'q-bub']: s.a(OUT('#' + n_, s.t(tpl), 'fade'))
    s.text('pl1', '<span class="syne shadow" style="font-size:110px">Pilihan</span>', 470, tpl, None, 'rise')
    s.text('pl2', '<span class="bod gt" style="font-size:150px">di tangan kau.</span>', 600, T('tangan', tpl), None, 'slam')
    scenes.append(s)
    sfx(b_q, 'whoosh', .5); sfx(b_q + .3, 'pop', .35); sfx(tns, 'whoosh', .4); sfx(tor, 'pop', .5); sfx(tpl, 'whoosh-cinematic', .35); sfx(T('tangan', tpl), 'impact-bass-1', .4)
    # CTA
    s = Scene('cta', b_cta, TOTAL)
    tkb = T('Tekan', b_cta); tco = T('cek', b_cta)
    s.stock_bar(b_cta, tkb - .1)
    s.bag_cta(tkb, tco, TOTAL)
    scenes.append(s)
    sfx(b_cta, 'whoosh', .5); sfx(tkb, 'riser', .35); sfx(tkb, 'impact-bass-2', .55); sfx(tkb + .5, 'click', .6); sfx(tco, 'click', .6); sfx(T('klik', b_cta), 'pop', .5)
    city = [(0, b_three, 'klcc_hero'), (b_three, b_p1, 'klcc_up'), (b_p1, b_p2, 'bb_monorail'), (b_p2, tk, 'komtar_n'), (tk, b_p3, 'penang_lights'),
            (b_p3, tpi, 'alor_hdr_n'), (tpi, b_q, 'klcc_cloud'), (b_q, b_cta, 'ramlee'), (b_cta, TOTAL, 'kl_skyline')]
    states = []; punches = []

else:  # ---------------- V2: talking head ----------------
    b_three = T('Tiga'); b_p1 = T('Sebab', b_three + 1); b_p2 = PREV('kedua'); b_p3 = PREV('ketiga')
    b_pr = T('Kau', b_p3); b_cta = T('Tekan', b_pr)
    # HOOK (A-roll low window)
    s = Scene('hook', 0, b_three)
    tk = T('Kalau')
    s.text('l1', '<span class="syne shadow" style="font-size:96px">Sabun ni bau</span>', 270, 0, tk, 'settle')
    s.text('l2', '<span class="bod gt" style="font-size:150px;font-weight:600">perfume mahal?</span>', 375, 0.05, tk, 'settle')
    s.text('m1', '<span class="syne shadow" style="font-size:80px">Tak percaya?</span>', 280, tk, None, 'slam')
    s.text('m2', '<span class="bod gt" style="font-size:118px">tengok sampai habis.</span>', 385, T('tengok'), None, 'rise')
    scenes.append(s)
    sfx(0.0, 'impact-bass-1', .55); sfx(T('mahal'), 'sparkle', .5); sfx(tk, 'whoosh', .5); sfx(T('habis'), 'pop', .4)
    # THREE + reveal (A-roll off)
    s = Scene('three', b_three, b_p1)
    tf = T('Fresh', b_three)
    s.text('n', '<span class="bod gt" style="font-size:520px;font-style:normal;font-weight:400;line-height:.8">3</span>', 250, b_three, tf, 'zoom')
    s.text('t', '<span class="syne x8 shadow" style="font-size:110px">Sebab</span>', 700, b_three + .15, tf, 'rise')
    s.text('s', '<span class="bod gt" style="font-size:84px">bau perfume mahal</span>', 820, T('bau', b_three), tf, 'rise')
    s.bottle('btl', tf - .1, None, top=300, h=720)
    s.text('brand', '<span class="syn" style="font-size:26px">Frescura Body</span>', 1110, tf + .3, None, 'track')
    s.particles('sp', tf + .3, 540, 640, 20, 380)
    scenes.append(s)
    sfx(b_three, 'whoosh-cinematic', .45); sfx(tf, 'impact-bass-1', .6); sfx(tf + .4, 'sparkle', .55)
    # P1 — INSPIRASI PERFUME (A-roll full, then perfume graphic)
    s = Scene('p1', b_p1, b_p2)
    ts = T('Sekali', b_p1)
    s.add('<div id="p1-chip" class="abs h glass" style="left:70px;top:250px;padding:18px 30px;border-radius:999px;display:flex;align-items:center;gap:18px">'
          '<span class="bod gt" style="font-size:54px;font-style:normal">01</span><span style="width:2px;height:40px;background:rgba(232,198,144,.6)"></span>'
          '<span style="font-family:Syne;font-weight:800;font-size:40px;color:#F6F1E7;text-transform:uppercase">Inspirasi perfume</span></div>')
    s.a(IN('#p1-chip', 0, 'left')); s.a(OUT('#p1-chip', s.t(ts), 'fade'))
    s.add(f'<div id="p1-pf" class="abs h" style="left:330px;top:520px">{perfume_svg("p1",420)}</div>')
    s.a(IN('#p1-pf', s.t(ts), 'fade'))
    s.a(f'tl.to("#p1-pf-b",{{strokeDashoffset:0,duration:.9,ease:"power2.inOut"}},{s.t(ts):.3f});tl.to("#p1-pf-n",{{strokeDashoffset:0,duration:.6,ease:"power2.inOut"}},{s.t(ts)+.4:.3f});')
    s.text('sc1', '<span class="syne shadow" style="font-size:100px">Sekali cium</span>', 260, ts, None, 'rise')
    s.text('sc2', '<span class="bod gt" style="font-size:130px">terus mahal.</span>', 380, T('terus', ts), None, 'slam')
    s.particles('mist', T('cium', ts), 470, 570, 24, 320)
    scenes.append(s)
    sfx(b_p1, 'whoosh', .5); sfx(b_p1 + .05, 'ping', .9); sfx(ts, 'whoosh-cinematic', .4); sfx(T('cium', ts), 'sparkle', .6); sfx(T('mahal', ts), 'pop', .4)
    # P2 — DUA BAU PREMIUM
    s = Scene('p2', b_p2, b_p3)
    tb = T('Bombshell', b_p2); tm = T('Midnight', b_p2) if False else T('minat', b_p2)
    s.text('n', '<span class="bod gt" style="font-size:116px;font-style:normal">02</span>', 262, b_p2, tb, 'zoom')
    s.text('t', '<span class="syne shadow" style="font-size:72px">Dua bau</span>', 380, b_p2 + .12, tb, 'rise')
    s.text('s', '<span class="bod gt" style="font-size:84px">premium.</span>', 448, T('premium', b_p2), tb, 'slam')
    s.scent_card('bs', 'Bombshell', 300, tb, ['Fresh', 'Feminine'], 'sun', 'Pakai hari-hari')
    s.scent_card('mf', 'Midnight Fantasy', 690, tm, ['Manis', 'Fruity'], 'moon', 'Untuk malam')
    scenes.append(s)
    sfx(b_p2, 'whoosh', .5); sfx(b_p2 + .05, 'ping', .9); sfx(T('premium', b_p2), 'pop', .4); sfx(tb, 'whoosh-cinematic', .4); sfx(tm, 'whoosh', .45); sfx(T('malam', b_p2), 'sparkle', .45)
    # P3 — BUIH + SEA SALT
    s = Scene('p3', b_p3, b_pr)
    tt = T('tekan', b_p3); tbu = T('buih', tt); tad = T('Ada', b_p3); tma = T('mandi', tad)
    s.text('n', '<span class="bod gt" style="font-size:116px;font-style:normal">03</span>', 262, b_p3, tt, 'zoom')
    s.text('t', '<span class="syne shadow" style="font-size:80px">Tekan je</span>', 390, b_p3 + .12, tt, 'rise')
    s.broll('br1', 'broll_close.mp4', tt, tbu, 0.0, 'Tekan je', label_icon='pump')
    s.broll('br2', 'broll_foam.mp4', tbu, tad, 0.4, 'Buih lembut')
    s.add(f'<div id="p3-cr" class="abs h" style="left:290px;top:300px">{crystals_svg("p3",500)}</div>')
    s.a(IN('#p3-cr', s.t(tad), 'zoom')); s.a(OUT('#p3-cr', s.t(tma), 'shrink'))
    s.text('ss', '<span class="syne shadow" style="font-size:96px">Sea salt</span>', 800, tad, tma, 'rise')
    s.text('ss2', '<span class="syn" style="font-size:22px">Kaya mineral semula jadi</span>', 925, T('kaya', tad), tma, 'track')
    for k, sym in enumerate(['Mg', 'Ca', 'K']):
        s.add(f'<div id="p3-m{k}" class="abs h glass" style="left:{180+k*270}px;top:990px;width:180px;height:120px;display:flex;align-items:center;justify-content:center;border-radius:26px">'
              f'<span class="bod gt" style="font-size:76px;font-style:normal;font-weight:700">{sym}</span></div>')
        s.a(IN(f'#p3-m{k}', s.t(T('mineral', tad)) + k * .18, 'pop')); s.a(OUT(f'#p3-m{k}', s.t(tma), 'fade'))
        sfx(T('mineral', tad) + k * .18, 'pop', .35)
    s.broll('br3', 'broll_lather.mp4', tma, b_pr, 2.0, 'Mandi pun rasa mewah', label_icon='spark')
    scenes.append(s)
    sfx(b_p3, 'whoosh', .5); sfx(b_p3 + .05, 'ping', .9); sfx(tt, 'whoosh-cinematic', .4); sfx(tt + .4, 'click', .5); sfx(tbu, 'sparkle', .5); sfx(tad, 'whoosh', .45); sfx(tma, 'whoosh', .45)
    # PRICE — perfume ratus-ratus vs sabun
    s = Scene('price', b_pr, b_cta)
    tta = T('Tapi', b_pr); tru = T('Rugi', b_pr)
    s.add(f'<div id="pr-pf" class="abs h" style="left:330px;top:300px">{perfume_svg("pr",420)}</div>')
    s.a(IN('#pr-pf', 0, 'fade')); s.a('tl.set(["#pr-pf-b","#pr-pf-n"],{strokeDashoffset:0},0);'); s.a(OUT('#pr-pf', s.t(tta), 'fade'))
    s.add('<div id="pr-tag" class="abs h" style="left:560px;top:420px;transform-origin:0 0"><div style="padding:22px 34px;border-radius:18px;background:linear-gradient(180deg,#FFF1D0,#E2C28A);'
          'font-family:Syne;font-weight:700;font-size:52px;white-space:nowrap;color:#1a1208;box-shadow:0 20px 50px rgba(0,0,0,.5)">RM ratus-ratus</div></div>')
    s.a(IN('#pr-tag', s.t(T('ratus', b_pr)), 'pop'))
    s.a(f'tl.fromTo("#pr-tag",{{rotation:-8}},{{rotation:6,duration:.5,repeat:3,yoyo:true,ease:"sine.inOut",immediateRender:false}},{s.t(T("ratus", b_pr)):.3f});'); s.a(OUT('#pr-tag', s.t(tta), 'fade'))
    s.text('sp', '<span class="syne shadow" style="font-size:96px">Sanggup?</span>', 1010, T('sanggup', b_pr), tta, 'slam')
    s.text('q1', '<span class="syne shadow" style="font-size:72px">Sabun bau perfume</span>', 270, tta, tru, 'rise')
    s.text('q2', '<span class="bod gt" style="font-size:118px">kau nak lepas?</span>', 360, T('kau', tta), tru, 'rise')
    s.text('r1', '<span class="syne x8" style="font-size:210px;color:#FF5A6E;text-shadow:0 10px 50px rgba(255,60,90,.45)">RUGI</span>', 250, tru, None, 'slam')
    s.text('r2', '<span class="bod gt" style="font-size:100px">gila weh.</span>', 440, T('gila', tru), None, 'slam')
    scenes.append(s)
    sfx(b_pr, 'whoosh', .5); sfx(T('ratus', b_pr), 'pop', .45); sfx(T('sanggup', b_pr), 'impact-bass-1', .35); sfx(tta, 'whoosh-cinematic', .4); sfx(tru, 'impact-bass-2', .6); sfx(tru + .05, 'glitch-3', .8)
    # CTA
    s = Scene('cta', b_cta, TOTAL)
    tco = T('cek', b_cta)
    s.stock_bar(T('stok', b_cta) - .2, T('stok', b_cta) + 1.6)
    s.bag_cta(b_cta + .05, tco, TOTAL)
    scenes.append(s)
    sfx(b_cta, 'riser', .35); sfx(b_cta + .05, 'impact-bass-2', .55); sfx(b_cta + .5, 'click', .6); sfx(T('stok', b_cta), 'whoosh', .4); sfx(tco, 'click', .6)
    sfx(T('Tekan', T('terahat', b_cta)), 'click', .6)
    city = [(0, b_p1, 'klcc'), (b_p1, b_p2, 'bb'), (b_p2, b_p3, 'alorsetar'), (b_p3, b_pr, 'komtar'), (b_pr, b_cta, 'bb'), (b_cta, TOTAL, 'klcc')]
    ts = T('Sekali', b_p1); tt = T('tekan', b_p3); tta = T('Tapi', b_pr)
    states = [(0, 'low'), (b_three, 'off'), (b_p1, 'full'), (ts, 'off'), (b_p2, 'low'), (T('Bombshell', b_p2), 'off'), (b_p3, 'low'), (tt, 'off'),
              (tta, 'low'), (b_cta, 'off')]
    punches = [(T('Serius'), 1.06, .6), (T('mahal'), 1.08, .5), (T('memang', b_p1), 1.1, .7), (T('Rugi', b_pr), 1.14, .9)]

# ---------------- write files ----------------
hosts = [{'id': 'city', 'start': 0, 'dur': TOTAL, 'track': 0, 'z': 1}]
for k, s in enumerate(scenes):
    open(f'{P}/compositions/{s.sid}.html', 'w').write(s.file())
    hosts.append({'id': s.sid, 'start': s.start, 'dur': s.dur, 'track': 3 + k % 2, 'z': 10})
open(f'{P}/compositions/city.html', 'w').write(city_scene_real(city, TOTAL) if V == 'v1' else city_scene(city, TOTAL, f'{S}/city'))
cap, groups = captions_html(words, TOTAL)
open(f'{P}/compositions/captions.html', 'w').write(cap)
hosts.append({'id': 'captions', 'start': 0, 'dur': TOTAL, 'track': 6, 'z': 20, 'kind': 'captions'})
audio = [f'<audio id="voice" class="clip" data-start="0" data-duration="{VD:.3f}" data-volume="1" data-track-index="7" src="assets/voice.wav"></audio>',
         f'<audio id="music" class="clip" data-start="0" data-duration="{TOTAL:.3f}" data-volume="0.16" data-fade-in="0.3" data-fade-out="1.2" data-track-index="8" src="assets/music.m4a"></audio>']
audio += sfx_tags(cues)
open(f'{P}/index.html', 'w').write(index_html(TOTAL, hosts, audio, 'aroll.mp4' if V == 'v2' else None, aroll_js(states, punches) if V == 'v2' else ''))
for f in ['meta.json', 'hyperframes.json', 'package.json']:
    if not os.path.exists(f'{P}/{f}'): shutil.copy(f'{S}/hf/demo/{f}', f'{P}/{f}')
json.dump({'id': f'frescura-{V}', 'name': f'Frescura night city {V}'}, open(f'{P}/meta.json', 'w'))
print(V, 'total', TOTAL, 'scenes', [(s.sid, round(s.start, 2), round(s.end, 2)) for s in scenes], 'sfx', len(cues), 'caption groups', len(groups))
