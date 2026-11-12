#!/usr/bin/env python3
"""Generate the HyperFrames composition (index.html) for the Frescura Body ad."""
import json, html

caps = json.load(open('/home/user/work/caps.json'))
VO_END = 37.67
TOTAL = 39.6

# ---------------- scenes: (id, start, end) ----------------
S = dict(
    hook=(0.0, 6.25), edu=(6.25, 11.21), ring=(11.21, 15.85), self=(15.85, 17.47),
    br1=(17.47, 19.9), br2=(19.9, 22.25), mall=(22.25, 24.32), f1=(24.32, 25.26),
    f2=(25.26, 25.99), f3=(25.99, 26.81), threein=(26.81, 28.24), bomb=(28.24, 29.10),
    noche=(29.10, 30.47), rugi=(30.47, 32.69), tangguh=(32.69, 34.10), cta=(34.10, 37.67),
    end=(37.67, TOTAL),
)
# scenes where the big kinetic type replaces bottom captions
NO_CAPS = {'hook', 'self', 'mall', 'bomb', 'noche'}

def clip(sid, inner, extra_cls='', z=1):
    s, e = S[sid]
    pre = VIDS.get(sid, '')
    return pre + (f'<section id="{sid}" class="clip scene {extra_cls}" data-start="{s:.3f}" '
            f'data-duration="{e - s:.3f}" style="z-index:{z}">{inner}</section>')

def emph(txt):
    out = []
    for t in txt.split(' '):
        if t.startswith('*'):
            out.append(f'<em>{html.escape(t.strip("*"))}</em>')
        else:
            out.append(html.escape(t))
    return ' '.join(out)

# ---------------- captions ----------------
def in_nocaps(t):
    return any(S[k][0] - 0.01 <= t < S[k][1] for k in NO_CAPS)

cap_html, cap_js = [], []
for i, c in enumerate(caps):
    if in_nocaps((c['s'] + c['e']) / 2):
        continue
    s = c['s']; e = caps[i + 1]['s'] if i + 1 < len(caps) else c['e'] + 0.3
    e = min(e, c['e'] + 0.35)
    words = []
    joined = ' '.join(c['toks'])
    # group *a b* emphasis spans
    toks, buf, inem = [], [], False
    for t in c['toks']:
        if t.startswith('*'): inem = True
        closing = t.rstrip('.,!?').endswith('*')
        buf.append(t.replace('*', ''))
        if not inem or closing:
            toks.append((' '.join(buf), inem)); buf = []; inem = False
    ti = 0
    for j, (w, em) in enumerate(toks):
        n = len(w.split(' '))
        wt = c['tt'][min(ti, len(c['tt']) - 1)]; ti += n
        cls = 'w em' if em else 'w'
        words.append(f'<span class="{cls}" id="c{i}w{j}">{html.escape(w)}</span>')
        cap_js.append(f'tl.fromTo("#c{i}w{j}",{{opacity:0,y:28,filter:"blur(10px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.22,ease:"power3.out"}},{max(s, wt - 0.04):.3f});')
        if em:
            cap_js.append(f'tl.fromTo("#c{i}w{j}",{{scale:1.18}},{{scale:1,duration:.35,ease:"back.out(3)"}},{max(s, wt - 0.04):.3f});')
    lc=' lightcap' if any(S[k][0]<=(c['s']+c['e'])/2<S[k][1] for k in ('edu','threein')) else ''
    cap_html.append(f'<div class="clip cap{lc}" data-start="{s:.3f}" data-duration="{e - s:.3f}" id="cap{i}"><div class="capline">{" ".join(words)}</div></div>')
    cap_js.append(f'tl.to("#cap{i} .capline",{{opacity:0,y:-14,duration:.12}},{e - 0.12:.3f});')

# ---------------- scene markup ----------------
J = []  # timeline js
VIDS = {}
def at(t): return f'{t:.3f}'

# HOOK ---------------------------------------------------------------
hs, he = S['hook']
hook = '''
<div class="bg-ink"></div><div class="aurora a1"></div><div class="aurora a2"></div>
<div class="hk-index"><span>FRESCURA BODY</span><span>— 01 / PERHATIAN</span></div>
<div class="hk-wrap">
  <div class="hk-l1" id="hk1">Korang tak</div>
  <div class="hk-l2" id="hk2"><span class="hk-big">TAKUT</span><span class="hk-q">ke?</span></div>
  <div class="hk-rule" id="hkr"></div>
  <div class="hk-l3" id="hk3">perkara <span class="hk-kecil" id="hkk">kecil</span></div>
  <div class="hk-l4" id="hk4">yang selalu <s id="hks">diabaikan</s></div>
</div>
<div class="couple" id="couple">
  <div class="dot d1" id="d1"></div><div class="dot d2" id="d2"></div>
  <div class="gap-line" id="gapl"><span id="gapt">JARAK</span></div>
  <div class="hk-l5" id="hk5"><em>tak selesa</em> nak dekat?</div>
</div>
'''
J += [
    f'tl.fromTo("#hook .a1",{{x:-200,y:-100,scale:1}},{{x:140,y:160,scale:1.3,duration:{he - hs},ease:"none"}},0);',
    f'tl.fromTo("#hook .a2",{{x:150,y:200}},{{x:-160,y:-80,duration:{he - hs},ease:"none"}},0);',
    'tl.fromTo(".hk-index",{opacity:0,y:-20},{opacity:1,y:0,duration:.5,ease:"power2.out"},0.05);',
    'tl.fromTo("#hk1",{opacity:0,y:60,filter:"blur(16px)"},{opacity:1,y:0,filter:"blur(0px)",duration:.35,ease:"power3.out"},0.0);',
    'tl.fromTo("#hk2 .hk-big",{opacity:0,scale:2.4,filter:"blur(30px)"},{opacity:1,scale:1,filter:"blur(0px)",duration:.42,ease:"expo.out"},0.22);',
    'tl.fromTo("#hk2 .hk-q",{opacity:0,x:40},{opacity:1,x:0,duration:.3,ease:"power3.out"},0.48);',
    'tl.fromTo("#hook .hk-wrap",{x:0},{x:-10,duration:.05,yoyo:true,repeat:5,ease:"none"},0.26);',
    'tl.fromTo("#hkr",{scaleX:0},{scaleX:1,duration:.5,ease:"expo.out"},0.7);',
    'tl.fromTo("#hk3",{opacity:0,y:40},{opacity:1,y:0,duration:.3,ease:"power3.out"},0.75);',
    'tl.fromTo("#hkk",{scale:1.8},{scale:.55,duration:.6,ease:"power2.inOut"},1.25);',
    'tl.fromTo("#hk4",{opacity:0,y:40},{opacity:1,y:0,duration:.3,ease:"power3.out"},1.8);',
    'tl.fromTo("#hks",{"--strike":"0%"},{"--strike":"100%",duration:.45,ease:"power2.inOut"},2.75);',
    'tl.to("#hook .hk-wrap",{opacity:0,y:-120,filter:"blur(14px)",duration:.4,ease:"power2.in"},3.0);',
    'tl.fromTo("#couple",{opacity:0},{opacity:1,duration:.3},3.2);',
    'tl.fromTo("#d1",{x:-60,scale:0},{x:0,scale:1,duration:.5,ease:"back.out(2)"},3.25);',
    'tl.fromTo("#d2",{x:60,scale:0},{x:0,scale:1,duration:.5,ease:"back.out(2)"},3.35);',
    'tl.to("#d1",{x:-250,duration:1.6,ease:"power2.inOut"},4.15);',
    'tl.to("#d2",{x:250,duration:1.6,ease:"power2.inOut"},4.15);',
    'tl.fromTo("#gapl",{scaleX:0,opacity:0},{scaleX:1,opacity:1,duration:1.6,ease:"power2.inOut"},4.15);',
    'tl.fromTo("#hk5",{opacity:0,y:50,filter:"blur(12px)"},{opacity:1,y:0,filter:"blur(0px)",duration:.4,ease:"power3.out"},5.35);',
    f'tl.to("#hook",{{opacity:0,duration:.18}},{he - 0.18:.3f});',
]

# EDU checklist ------------------------------------------------------
es, ee = S['edu']
ICON = {
 'body': '<svg viewBox="0 0 100 100"><path class="st" d="M50 14c8 0 13 6 13 13s-5 13-13 13-13-6-13-13 5-13 13-13zM24 88c0-16 11-30 26-30s26 14 26 30"/><path class="st" d="M76 20l4-8 4 8 8 4-8 4-4 8-4-8-8-4z"/></svg>',
 'smell': '<svg viewBox="0 0 100 100"><path class="st" d="M30 80c-10-12 10-18 0-30s10-18 0-30M50 80c-10-12 10-18 0-30s10-18 0-30M70 80c-10-12 10-18 0-30s10-18 0-30"/></svg>',
 'cloth': '<svg viewBox="0 0 100 100"><path class="st" d="M36 14l14 10 14-10 24 14-8 18-10-5v45H30V41l-10 5-8-18z"/></svg>',
}
cards = [('01', 'Kebersihan', 'Badan', 'body', 8.45), ('02', 'Bau', 'Badan', 'smell', 9.65), ('03', 'Pakaian', '& Penampilan', 'cloth', 10.56)]
edu = '<div class="bg-ivory"></div><div class="grid-lines"></div>'
edu += '<div class="edu-kicker" id="ek"><span class="pill">EDUKASI</span> Perkara yang kita kena</div><div class="edu-title" id="et"><em>ambil berat</em></div>'
edu += '<div class="cards">'
for k, (n, a, b, ic, t) in enumerate(cards):
    edu += f'<div class="card" id="card{k}"><div class="cnum">{n}</div><div class="cicon">{ICON[ic]}</div><div class="ctext"><b>{a}</b><span>{b}</span></div><div class="ctick" id="tick{k}">✓</div></div>'
    J += [f'tl.fromTo("#card{k}",{{opacity:0,x:-160,rotationY:-35}},{{opacity:1,x:0,rotationY:0,duration:.45,ease:"expo.out"}},{at(t - 0.1)});',
          f'tl.fromTo("#card{k} .st",{{strokeDashoffset:300}},{{strokeDashoffset:0,duration:.7,ease:"power2.out"}},{at(t)});',
          f'tl.fromTo("#tick{k}",{{scale:0,rotation:-90}},{{scale:1,rotation:0,duration:.35,ease:"back.out(3)"}},{at(t + 0.35)});']
edu += '</div>'
J += [f'tl.fromTo("#ek",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.35,ease:"power3.out"}},{at(es + 0.05)});',
      f'tl.fromTo("#et",{{opacity:0,y:60,filter:"blur(14px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.45,ease:"expo.out"}},{at(7.7)});',
      f'tl.fromTo("#edu .grid-lines",{{opacity:0,scale:1.15}},{{opacity:1,scale:1,duration:1.2,ease:"power2.out"}},{at(es)});',
      f'tl.to("#edu .cards",{{y:-30,duration:{ee - es},ease:"none"}},{at(es)});']

# RING / routine -------------------------------------------------------
rs, re_ = S['ring']
ring = '''<div class="bg-ink2"></div>
<div class="ring-wrap"><svg viewBox="0 0 400 260" class="rings"><circle class="rg" id="rg1" cx="150" cy="130" r="88"/><circle class="rg" id="rg2" cx="250" cy="130" r="88"/></svg></div>
<div class="ring-k" id="rk">JANGAN PANDANG RINGAN</div>
<div class="ring-t" id="rt"><em>Rutin</em> penjagaan diri</div>
<div class="years"><div class="ylab">walaupun dah</div><div class="ynum" id="ynum">01</div><div class="ylab">tahun berkahwin</div></div>
<div class="routine" id="rout"><span>MANDI</span><i></i><span>WANGI</span><i></i><span>KEMAS</span><i></i><span>YAKIN</span></div>'''
J += [f'tl.fromTo("#rg1",{{strokeDashoffset:560}},{{strokeDashoffset:0,duration:1.1,ease:"power2.inOut"}},{at(rs + 0.05)});',
      f'tl.fromTo("#rg2",{{strokeDashoffset:560}},{{strokeDashoffset:0,duration:1.1,ease:"power2.inOut"}},{at(rs + 0.25)});',
      f'tl.fromTo(".rings",{{rotation:-8,scale:.9}},{{rotation:4,scale:1.05,duration:{re_ - rs},ease:"none"}},{at(rs)});',
      f'tl.fromTo("#rk",{{opacity:0,}},{{opacity:1,duration:.6,ease:"expo.out"}},{at(rs + 0.1)});',
      f'tl.fromTo("#rt",{{opacity:0,y:50,filter:"blur(12px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.45,ease:"expo.out"}},{at(12.87)});',
      f'tl.fromTo("#rout span, #rout i",{{opacity:0,y:20}},{{opacity:1,y:0,stagger:.08,duration:.3,ease:"power2.out"}},{at(13.2)});',
      f'tl.fromTo(".years",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.35,ease:"power3.out"}},{at(14.05)});']
for k in range(1, 11):
    J.append(f'tl.set("#ynum",{{textContent:"{k:02d}{"+" if k == 10 else ""}"}},{at(14.15 + (k - 1) * 0.12)});')
J.append(f'tl.to("#ring",{{opacity:0,duration:.15}},{at(re_ - 0.15)});')

# SELF --------------------------------------------------------------
ss, se = S['self']
selfh = '''<div class="bg-ink"></div><div class="mirror" id="mir"><div class="sweep" id="swp"></div></div>
<div class="self-t"><div class="out" id="so1">DIRI SENDIRI</div><div class="self-i" id="so2">pun <em>kena jaga.</em></div></div>'''
J += [f'tl.fromTo("#mir",{{scaleY:0,opacity:0}},{{scaleY:1,opacity:1,duration:.5,ease:"expo.out"}},{at(ss)});',
      f'tl.fromTo("#swp",{{x:-500}},{{x:500,duration:1.0,ease:"power2.inOut"}},{at(ss + 0.3)});',
      f'tl.fromTo("#so1",{{opacity:0,scale:1.4,}},{{opacity:1,scale:1,duration:.45,ease:"expo.out"}},{at(ss + 0.02)});',
      f'tl.fromTo("#so2",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.35,ease:"power3.out"}},{at(16.6)});']

# B-ROLL -----------------------------------------------------------
def broll(sid, src, mstart, label_k, label_t, push=1.08):
    s, e = S[sid]
    VIDS[sid] = f'<video class="clip vid" id="v_{sid}" src="assets/{src}" muted playsinline data-start="{s:.3f}" data-duration="{e - s:.3f}" data-media-start="{mstart}"></video>'
    inner = (f'<div class="vgrad"></div><div class="lb-top"></div>'
             f'<div class="tag" id="tag_{sid}"><span class="tk">{label_k}</span><span class="tt">{label_t}</span></div>')
    J.extend([f'tl.fromTo("#v_{sid}",{{scale:1.0}},{{scale:{push},duration:{e - s:.3f},ease:"none"}},{at(s)});',
              f'tl.fromTo("#v_{sid}",{{clipPath:"inset(0% 0% 100% 0%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:.4,ease:"expo.inOut"}},{at(s)});',
              f'tl.fromTo("#tag_{sid}",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:.4,ease:"expo.out"}},{at(s + 0.2)});'])
    return inner

br1 = broll('br1', 'pump1.mp4', 0.3, 'RUTIN HARIAN', 'Sentiasa bersih &amp; segar')
br2 = broll('br2', 'pump4.mp4', 0.0, 'PENGALAMAN MANDI', 'Lembut · Menenangkan')

# MALL boutique ---------------------------------------------------------
def boutique(prefix, bottles='pair'):
    bok = ''
    import math
    pts = [(80, 260, 90, '#f6d7a0'), (240, 180, 60, '#ffe7c2'), (430, 290, 120, '#f2c67d'), (640, 200, 70, '#fff1d6'), (820, 270, 100, '#e9b86c'),
           (990, 190, 80, '#ffe2b0'), (160, 470, 50, '#fff'), (520, 430, 45, '#ffd9a0'), (900, 460, 60, '#ffe9c9'), (330, 90, 40, '#fff4e0'), (760, 80, 55, '#f8d9a8')]
    for k, (x, y, r, c) in enumerate(pts):
        bok += f'<i class="bk" style="left:{x}px;top:{y}px;width:{r * 2}px;height:{r * 2}px;background:radial-gradient(circle,{c} 0%,{c}55 45%,transparent 70%)"></i>'
    return f'''<div class="mall-bg"></div><div class="bokeh" id="{prefix}bok">{bok}</div>
<div class="arch"><i></i><i></i><i></i><i></i></div>
<div class="beam b1"></div><div class="beam b2"></div><div class="beam b3"></div>
<div class="floor"></div>
<div class="podium" id="{prefix}pod"><div class="ptop"></div><div class="pside"></div></div>
<div class="prod" id="{prefix}prod"><img src="assets/img/{bottles}.png" class="pimg"><img src="assets/img/{bottles}.png" class="prefl"><div class="glint" id="{prefix}gl"></div></div>'''

ms, me = S['mall']
mall = boutique('m') + '''<div class="brand"><div class="b-k" id="bk">pastinya</div><div class="b-n" id="bn">FRESCURA&nbsp;BODY</div><div class="b-s" id="bs">menjadi <em>pilihan</em></div></div>'''
J += [f'tl.fromTo("#mall",{{opacity:0}},{{opacity:1,duration:.25}},{at(ms)});',
      f'tl.fromTo("#mprod",{{y:220,opacity:0,scale:.9}},{{y:0,opacity:1,scale:1,duration:.7,ease:"expo.out"}},{at(ms + 0.05)});',
      f'tl.fromTo("#mpod",{{y:160,opacity:0}},{{y:0,opacity:1,duration:.6,ease:"expo.out"}},{at(ms)});',
      f'tl.fromTo("#mall .scene-cam",{{scale:1}},{{scale:1.06,duration:{me - ms},ease:"none"}},{at(ms)});',
      f'tl.fromTo("#mbok",{{x:40}},{{x:-60,duration:{me - ms},ease:"none"}},{at(ms)});',
      f'tl.fromTo("#mgl",{{x:-600}},{{x:700,duration:.9,ease:"power2.inOut"}},{at(22.85)});',
      f'tl.fromTo("#bk",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.3}},{at(ms + 0.02)});',
      f'tl.fromTo("#bn",{{opacity:0,filter:"blur(18px)"}},{{opacity:1,filter:"blur(0px)",duration:.55,ease:"expo.out"}},{at(22.8)});',
      f'tl.fromTo("#bs",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.3}},{at(23.5)});',
      f'tl.fromTo("#mall .beam",{{opacity:0}},{{opacity:1,stagger:.12,duration:.4}},{at(ms + 0.1)});']

# FEATURES ---------------------------------------------------------------
def feature(sid, src, mstart, num, title, sub, extra=''):
    s, e = S[sid]
    VIDS[sid] = f'<video class="clip vid" id="v_{sid}" src="assets/{src}" muted playsinline data-start="{s:.3f}" data-duration="{e - s:.3f}" data-media-start="{mstart}"></video>'
    inner = (f'<div class="vgrad"></div>{extra}'
             f'<div class="feat" id="ft_{sid}"><div class="fnum">{num}<small>/03</small></div><div class="fline"></div><div class="ftitle">{title}</div><div class="fsub">{sub}</div></div>')
    J.extend([f'tl.fromTo("#v_{sid}",{{scale:1.12}},{{scale:1.0,duration:{e - s:.3f},ease:"power1.out"}},{at(s)});',
              f'tl.fromTo("#v_{sid}",{{clipPath:"circle(0% at 50% 50%)"}},{{clipPath:"circle(80% at 50% 50%)",duration:.35,ease:"power3.out"}},{at(s)});',
              f'tl.fromTo("#ft_{sid} .fnum",{{opacity:0,y:-40}},{{opacity:1,y:0,duration:.3,ease:"power3.out"}},{at(s + 0.05)});',
              f'tl.fromTo("#ft_{sid} .fline",{{scaleX:0}},{{scaleX:1,duration:.4,ease:"expo.out"}},{at(s + 0.1)});',
              f'tl.fromTo("#ft_{sid} .ftitle",{{opacity:0,x:-50}},{{opacity:1,x:0,duration:.3,ease:"power3.out"}},{at(s + 0.12)});',
              f'tl.fromTo("#ft_{sid} .fsub",{{opacity:0}},{{opacity:1,duration:.3}},{at(s + 0.25)});'])
    return inner

salt = '<div class="salt">' + ''.join(f'<i style="left:{(k * 137) % 1000 + 30}px;top:{(k * 211) % 1500 + 100}px;width:{8 + (k * 7) % 16}px;height:{8 + (k * 7) % 16}px"></i>' for k in range(28)) + '</div>'
f1 = feature('f1', 'pump3.mp4', 0.2, '01', 'Buih Lembut', 'Gentle foaming · tak kesat di kulit')
f2 = feature('f2', 'pump2.mp4', 1.0, '02', 'Garam Laut', 'Ocean salt · rasa segar &amp; bersih', salt)
J.append(f'tl.fromTo("#f2 .salt i",{{y:-200,opacity:0,rotation:0}},{{y:300,opacity:1,rotation:180,stagger:.01,duration:.7,ease:"power1.in"}},{at(S["f2"][0])});')
# f3: photo with ken burns
f3s, f3e = S['f3']
f3 = ('<div class="photo" id="ph_f3" style="background-image:url(assets/img/flat_wood.jpg)"></div><div class="vgrad"></div>'
      '<div class="feat" id="ft_f3"><div class="fnum">03<small>/03</small></div><div class="fline"></div><div class="ftitle">Wangian Feminine</div><div class="fsub">Aromatherapy · tahan lama</div></div>')
J += [f'tl.fromTo("#ph_f3",{{scale:1.25,y:60}},{{scale:1.1,y:-40,duration:{f3e - f3s:.3f},ease:"none"}},{at(f3s)});',
      f'tl.fromTo("#f3",{{clipPath:"inset(0% 100% 0% 0%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:.3,ease:"expo.out"}},{at(f3s)});',
      f'tl.fromTo("#ft_f3 .fnum",{{opacity:0,y:-40}},{{opacity:1,y:0,duration:.3}},{at(f3s + .05)});',
      f'tl.fromTo("#ft_f3 .fline",{{scaleX:0}},{{scaleX:1,duration:.4,ease:"expo.out"}},{at(f3s + .1)});',
      f'tl.fromTo("#ft_f3 .ftitle",{{opacity:0,x:-50}},{{opacity:1,x:0,duration:.3}},{at(f3s + .12)});',
      f'tl.fromTo("#ft_f3 .fsub",{{opacity:0}},{{opacity:1,duration:.3}},{at(f3s + .25)});']

# THREE-IN-ONE -------------------------------------------------------------
ts, te = S['threein']
three = '''<div class="bg-ivory"></div><div class="grid-lines"></div>
<div class="t-k" id="t3k">DALAM SATU BOTOL</div>
<div class="t-bottle" id="t3b"><img src="assets/img/pair.png"></div>
<div class="orb o1" id="o1"><b>Buih</b><span>Lembut</span></div><div class="orb o2" id="o2"><b>Garam</b><span>Laut</span></div><div class="orb o3" id="o3"><b>Wangian</b><span>Feminine</span></div>
<div class="t-big" id="t3n">3<span>in</span>1</div>'''
J += [f'tl.fromTo("#t3k",{{opacity:0,}},{{opacity:1,duration:.5,ease:"expo.out"}},{at(ts)});',
      f'tl.fromTo("#t3b",{{opacity:0,scale:.7,y:80}},{{opacity:1,scale:1,y:0,duration:.6,ease:"expo.out"}},{at(ts + 0.05)});',
      f'tl.fromTo("#o1",{{x:-420,y:-260,opacity:0}},{{x:0,y:0,opacity:1,duration:.5,ease:"back.out(1.6)"}},{at(ts + 0.15)});',
      f'tl.fromTo("#o2",{{x:420,y:-160,opacity:0}},{{x:0,y:0,opacity:1,duration:.5,ease:"back.out(1.6)"}},{at(ts + 0.3)});',
      f'tl.fromTo("#o3",{{x:-300,y:300,opacity:0}},{{x:0,y:0,opacity:1,duration:.5,ease:"back.out(1.6)"}},{at(ts + 0.45)});',
      f'tl.to("#o1",{{x:355,y:405,scale:.2,opacity:0,duration:.4,ease:"power3.in"}},{at(te - 0.55)});',
      f'tl.to("#o2",{{x:-355,y:95,scale:.2,opacity:0,duration:.4,ease:"power3.in"}},{at(te - 0.55)});',
      f'tl.to("#o3",{{x:345,y:-275,scale:.2,opacity:0,duration:.4,ease:"power3.in"}},{at(te - 0.55)});',
      f'tl.fromTo("#t3n",{{opacity:0,scale:2}},{{opacity:1,scale:1,duration:.4,ease:"expo.out"}},{at(ts + 0.6)});',
      f'tl.fromTo("#t3b",{{filter:"brightness(1)"}},{{filter:"brightness(1.5)",duration:.15,yoyo:true,repeat:1}},{at(te - 0.18)});']

# BOMBSHELL / NOCHE hero -----------------------------------------------------
def hero(sid, img, cls, k, name, sub):
    s, e = S[sid]
    inner = (f'<div class="hero-bg {cls}"></div><div class="hero-ring" id="hr_{sid}"></div>'
             f'<div class="hero-name" id="hn_{sid}"><span class="hk">{k}</span><span class="hn">{name}</span><span class="hs">{sub}</span></div>'
             f'<img class="hero-img" id="hi_{sid}" src="assets/img/{img}.png"><div class="hero-floor"></div>')
    J.extend([f'tl.fromTo("#hi_{sid}",{{y:260,rotation:-6,opacity:0}},{{y:0,rotation:0,opacity:1,duration:.5,ease:"expo.out"}},{at(s)});',
              f'tl.fromTo("#hi_{sid}",{{scale:1}},{{scale:1.06,duration:{e - s:.3f},ease:"none"}},{at(s)});',
              f'tl.fromTo("#hr_{sid}",{{scale:.3,opacity:0,rotation:0}},{{scale:1,opacity:1,rotation:90,duration:{e - s:.3f},ease:"power2.out"}},{at(s)});',
              f'tl.fromTo("#hn_{sid} .hn",{{opacity:0,y:80,filter:"blur(16px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.45,ease:"expo.out"}},{at(s + 0.05)});',
              f'tl.fromTo("#hn_{sid} .hk, #hn_{sid} .hs",{{opacity:0}},{{opacity:1,duration:.3,stagger:.1}},{at(s + 0.15)});',
              f'tl.fromTo("#{sid}",{{clipPath:"inset(50% 0% 50% 0%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:.3,ease:"expo.out"}},{at(s)});'])
    return inner
stars = '<div class="stars">' + ''.join(f'<i style="left:{(k * 97) % 1080}px;top:{(k * 173) % 1100}px;opacity:{0.3 + (k % 7) / 10}"></i>' for k in range(60)) + '</div>'
bomb = hero('bomb', 'red', 'rose', 'NO. 01 · WOMAN GLORY', 'Bombshell', 'Rose · Berani · Memikat')
noche = hero('noche', 'noche', 'violet', 'NO. 02 · NOCHE', 'Midnight<br>Fantasy', 'Violet · Lembut · Misteri')
noche = stars + noche

# RUGI recap ----------------------------------------------------------------
gs, ge = S['rugi']
rugi = ('<div class="photo" id="ph_r1" style="background-image:url(assets/img/sun_diag.jpg)"></div>'
        '<div class="photo" id="ph_r2" style="background-image:url(assets/img/marble.jpg)"></div><div class="vgrad strong"></div>'
        '<div class="recap" id="recap"><div class="rk">KELEBIHANNYA</div>'
        '<div class="ri" id="ri0"><i>✓</i>Buih lembut</div><div class="ri" id="ri1"><i>✓</i>Garam laut</div><div class="ri" id="ri2"><i>✓</i>Wangian feminine</div><div class="ri" id="ri3"><i>✓</i>500 ml · tahan lama</div></div>')
J += [f'tl.fromTo("#ph_r1",{{scale:1.3,x:0}},{{scale:1.15,x:-40,duration:1.0,ease:"none"}},{at(gs)});',
      f'tl.set("#ph_r2",{{opacity:0}},{at(gs)});', f'tl.set("#ph_r2",{{opacity:1}},{at(31.33)});',
      f'tl.fromTo("#ph_r2",{{scale:1.1}},{{scale:1.25,duration:{ge - 31.33:.3f},ease:"none"}},{at(31.33)});',
      f'tl.fromTo("#recap",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.3}},{at(31.3)});']
for k in range(4):
    J.append(f'tl.fromTo("#ri{k}",{{opacity:0,x:-80}},{{opacity:1,x:0,duration:.3,ease:"expo.out"}},{at(31.45 + k * 0.22)});')
    J.append(f'tl.fromTo("#ri{k} i",{{scale:0}},{{scale:1,duration:.3,ease:"back.out(3)"}},{at(31.55 + k * 0.22)});')

# TANGGUH -------------------------------------------------------------------
gs2, ge2 = S['tangguh']
tang = ('<div class="photo" id="ph_t" style="background-image:url(assets/img/dark_studio.jpg)"></div><div class="vgrad strong"></div>'
        '<div class="clock" id="clk"><svg viewBox="0 0 200 200"><circle cx="100" cy="100" r="88" class="cf"/><line x1="100" y1="100" x2="100" y2="38" class="ch" id="chm"/><line x1="100" y1="100" x2="146" y2="100" class="ch2" id="chh"/></svg></div>'
        '<div class="tg" id="tg">JANGAN<br><em>tangguh</em></div>')
J += [f'tl.fromTo("#ph_t",{{scale:1.05}},{{scale:1.2,duration:{ge2 - gs2:.3f},ease:"none"}},{at(gs2)});',
      f'tl.fromTo("#clk",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:.4,ease:"back.out(2)"}},{at(gs2)});',
      f'tl.fromTo("#chm",{{rotation:0,svgOrigin:"100 100"}},{{rotation:1080,svgOrigin:"100 100",duration:{ge2 - gs2:.3f},ease:"power1.in"}},{at(gs2)});',
      f'tl.fromTo("#chh",{{rotation:0,svgOrigin:"100 100"}},{{rotation:90,svgOrigin:"100 100",duration:{ge2 - gs2:.3f},ease:"power1.in"}},{at(gs2)});',
      f'tl.fromTo("#tg",{{opacity:0,y:60,filter:"blur(12px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.4,ease:"expo.out"}},{at(33.0)});']

# CTA -----------------------------------------------------------------------
cs, ce = S['cta']
cta = '''<div class="bg-ink"></div><div class="aurora a3"></div>
<div class="cta-k" id="ck">LANGKAH SETERUSNYA</div>
<div class="bag" id="bag"><svg viewBox="0 0 200 200"><path d="M40 70h120l-10 100H50z" class="bagb"/><path d="M70 72V58a30 30 0 0 1 60 0v14" class="bagh"/></svg>
<div class="ripple" id="rp1"></div><div class="ripple" id="rp2"></div><div class="finger" id="fing"></div></div>
<div class="cta-t" id="ct1">Tekan <b>beg kuning</b></div>
<div class="cta-btn" id="cbtn">CHECK OUT SEKARANG <span>→</span></div>
<div class="stock" id="stk"><div class="sl"><span>STOK FRESCURA BODY</span><span id="spc">100%</span></div><div class="sbar"><i id="sfill"></i></div><div class="sw">⚠ Stok memang tak banyak</div></div>'''
J += [f'tl.fromTo("#ck",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:.3}},{at(cs)});',
      f'tl.fromTo("#bag",{{scale:0,rotation:-20}},{{scale:1,rotation:0,duration:.5,ease:"back.out(2.2)"}},{at(cs)});',
      f'tl.fromTo("#fing",{{x:220,y:240,opacity:0}},{{x:0,y:0,opacity:1,duration:.4,ease:"power3.out"}},{at(cs + 0.25)});',
      f'tl.to("#bag svg",{{scale:.86,duration:.08,yoyo:true,repeat:1}},{at(cs + 0.65)});',
      f'tl.fromTo("#rp1",{{scale:.3,opacity:.9}},{{scale:2.4,opacity:0,duration:.7,ease:"power2.out"}},{at(cs + 0.65)});',
      f'tl.fromTo("#rp2",{{scale:.3,opacity:.9}},{{scale:2.4,opacity:0,duration:.7,ease:"power2.out"}},{at(cs + 0.85)});',
      f'tl.fromTo("#ct1",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.3,ease:"power3.out"}},{at(cs + 0.05)});',
      f'tl.fromTo("#cbtn",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.4,ease:"back.out(2)"}},{at(34.83)});',
      f'tl.to("#cbtn",{{scale:1.06,duration:.25,yoyo:true,repeat:5,ease:"sine.inOut"}},{at(35.3)});',
      f'tl.fromTo("#stk",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.3}},{at(35.42)});',
      f'tl.fromTo("#sfill",{{scaleX:1}},{{scaleX:.12,duration:1.6,ease:"power2.inOut"}},{at(35.7)});',
      ]
for k, p in enumerate([100, 86, 71, 55, 40, 28, 19, 12]):
    J.append(f'tl.set("#spc",{{textContent:"{p}%"}},{at(35.7 + k * 0.2)});')
J.append(f'tl.fromTo(".sw",{{opacity:0}},{{opacity:1,duration:.12,yoyo:true,repeat:5}},{at(36.69)});')

# END card ------------------------------------------------------------------
ns, ne = S['end']
endc = boutique('e') + '''<div class="brand end"><div class="b-n" id="en">FRESCURA&nbsp;BODY</div><div class="b-sf" id="es2">SOFT &nbsp;|&nbsp; FRAGRANT</div><div class="b-v" id="ev">Bombshell &nbsp;·&nbsp; Midnight Fantasy</div></div>'''
J += [f'tl.fromTo("#end",{{opacity:0}},{{opacity:1,duration:.3}},{at(ns)});',
      f'tl.fromTo("#eprod",{{y:180,opacity:0}},{{y:0,opacity:1,duration:.7,ease:"expo.out"}},{at(ns)});',
      f'tl.fromTo("#epod",{{y:120,opacity:0}},{{y:0,opacity:1,duration:.6,ease:"expo.out"}},{at(ns)});',
      f'tl.fromTo("#end .scene-cam",{{scale:1.08}},{{scale:1,duration:{ne - ns},ease:"power1.out"}},{at(ns)});',
      f'tl.fromTo("#egl",{{x:-600}},{{x:700,duration:1.0,ease:"power2.inOut"}},{at(ns + 0.4)});',
      f'tl.fromTo("#en",{{opacity:0,filter:"blur(18px)"}},{{opacity:1,filter:"blur(0px)",duration:.6,ease:"expo.out"}},{at(ns + 0.1)});',
      f'tl.fromTo("#es2",{{opacity:0}},{{opacity:1,duration:.4}},{at(ns + 0.5)});',
      f'tl.fromTo("#ev",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.4}},{at(ns + 0.7)});',
      f'tl.fromTo("#ebok",{{x:-40}},{{x:40,duration:{ne - ns},ease:"none"}},{at(ns)});',
      f'tl.to("#end",{{opacity:0,duration:.4}},{at(ne - 0.4)});']

def cam(inner):
    return f'<div class="scene-cam">{inner}</div>'

scenes = [clip('hook', hook), clip('edu', edu), clip('ring', ring), clip('self', selfh), clip('br1', br1), clip('br2', br2),
          clip('mall', cam(mall)), clip('f1', f1), clip('f2', f2), clip('f3', f3), clip('threein', three), clip('bomb', bomb),
          clip('noche', noche), clip('rugi', rugi), clip('tangguh', tang), clip('cta', cta), clip('end', cam(endc))]

# progress bar + grain (global)
J.append(f'tl.fromTo("#prog",{{scaleX:0}},{{scaleX:1,duration:{TOTAL},ease:"none"}},0);')
for k in range(int(TOTAL * 12)):
    J.append(f'tl.set("#grain",{{x:{(k * 173) % 300 - 150},y:{(k * 97) % 300 - 150}}},{k / 12:.3f});')

css = open('/home/user/work/style.css').read()
fonts = open('/home/user/work/hf/proj/assets/fonts/local.css').read()
PREVIEW = __import__('os').environ.get('PREVIEW', '1') == '1'
wm = '<div class="wm">PREVIEW</div>' if PREVIEW else ''
doc = f'''<!doctype html>
<html lang="ms" data-resolution="portrait">
<head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<script src="assets/gsap.min.js"></script>
<style>{fonts}
{css}</style></head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{''.join(scenes)}
<div id="caps">{''.join(cap_html)}</div>
<div class="grain-wrap"><div id="grain"></div></div>
<div id="progw"><div id="prog"></div></div>
{wm}
<audio id="mix" class="clip" src="assets/mix.wav" data-start="0" data-duration="{TOTAL}" data-volume="1"></audio>
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(J)}
{chr(10).join(cap_js)}
tl.set({{}},{{}},{TOTAL});
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body></html>'''
open('/home/user/work/hf/proj/index.html', 'w').write(doc)
json.dump(S, open('/home/user/work/scenes.json', 'w'))
print('ok', len(J), 'tweens', len(cap_html), 'captions')
