# Scene components + city background + project assembly.
import json, random, os
from lib import *

LOC = {'klcc': ('KLCC · KUALA LUMPUR', '3.1579° N  ·  101.7116° E'),
       'bb': ('BUKIT BINTANG · KL', '3.1466° N  ·  101.7101° E'),
       'komtar': ('KOMTAR · PULAU PINANG', '5.4146° N  ·  100.3296° E'),
       'alorsetar': ('MENARA ALOR SETAR · KEDAH', '6.1219° N  ·  100.3695° E')}

def city_scene(segs, total, citydir):
    """segs: [(t0, t1, name)] covering [0,total]."""
    els, js = [], []
    for i, (t0, t1, nm) in enumerate(segs):
        data = json.load(open(f'{citydir}/{nm}.json'))
        tw = ''.join(f'<rect id="city-s{i}-t{k}" x="{x:.1f}" y="{y:.1f}" width="6" height="9" fill="#FFF0D0"/>' for k, (x, y) in enumerate(data['twinkle']))
        bc = ''.join(f'<circle id="city-s{i}-b{k}" cx="{x}" cy="{y}" r="5" fill="#FF3B3B"/><circle id="city-s{i}-bh{k}" cx="{x}" cy="{y}" r="16" fill="#FF3B3B" opacity=".25"/>' for k, (x, y) in enumerate(data['beacons']))
        train = ''
        if nm == 'bb':
            win = ''.join(f'<rect x="{12+j*36}" y="9" width="24" height="12" rx="2" fill="#FFE6BF"/>' for j in range(9))
            train = f'<svg id="city-s{i}-train" class="abs" style="left:0;top:1118px" width="340" height="34" viewBox="0 0 340 34"><rect width="340" height="32" rx="12" fill="#1c2448" stroke="#37E3FF" stroke-opacity=".6"/>{win}</svg>'
        els.append(f'<div id="city-s{i}" class="abs sky" style="left:-60px;top:0;width:1200px;height:1920px;z-index:{i+1}">'
                   f'<img src="assets/city/{nm}.png" style="position:absolute;left:0;top:0;width:1200px;height:1920px">'
                   f'<svg class="abs" style="left:0;top:0" width="1200" height="1920" viewBox="0 0 1200 1920">{tw}{bc}</svg>{train}</div>')
        d = t1 - t0
        if i == 0: js.append(f'tl.set("#city-s{i}",{{opacity:1}},0);')
        else:
            js.append(f'tl.fromTo("#city-s{i}",{{opacity:0}},{{opacity:1,duration:.9,ease:"power2.inOut"}},{t0-.2:.3f});')
        js.append(f'tl.set("#city-s{i}",{{opacity:0}},{t1+.75:.3f});' if i + 1 < len(segs) else '')
        js.append(f'tl.fromTo("#city-s{i}",{{scale:1.0,x:-26,y:0}},{{scale:1.075,x:26,y:-18,duration:{d+1:.2f},ease:"none"}},{max(0,t0-.2):.3f});')
        r = random.Random(i * 7 + 3)
        for k in range(len(data['twinkle'])):
            per = r.uniform(.5, 1.4); n = int((d + 1) / per)
            js.append(f'tl.fromTo("#city-s{i}-t{k}",{{opacity:0}},{{opacity:{r.uniform(.6,1):.2f},duration:{per:.2f},repeat:{n},yoyo:true,ease:"sine.inOut"}},{t0+r.uniform(0,.6):.2f});')
        for k in range(len(data['beacons'])):
            n = int((d + 1) / 0.6)
            js.append(f'tl.fromTo(["#city-s{i}-b{k}","#city-s{i}-bh{k}"],{{opacity:.15}},{{opacity:1,duration:.3,repeat:{n},yoyo:true,ease:"steps(1)"}},{t0+k*.17:.2f});')
        if train:
            n = int(d / 5.5) + 1
            js.append(f'tl.fromTo("#city-s{i}-train",{{x:-420}},{{x:1320,duration:5.5,repeat:{n},ease:"none"}},{t0:.2f});')
        # location tag
        a, b = LOC[nm]
        els.append(f'<div id="city-tag{i}" class="abs h" style="left:72px;top:190px;z-index:50"><div class="syn" id="city-tag{i}a">◆ {a}</div>'
                   f'<div style="font-family:Syne;font-size:17px;letter-spacing:.18em;color:rgba(246,241,231,.6);margin-top:10px">{b}</div></div>')
        js.append(IN(f'#city-tag{i}', t0 + .25, 'fade') + IN(f'#city-tag{i}a', t0 + .25, 'track'))
        js.append(f'tl.to("#city-tag{i}",{{opacity:0,duration:.3}},{min(t0+3.6,t1-.3):.2f});')
        # flare sweep at transitions
        if i:
            els.append(f'<div id="city-flare{i}" class="abs" style="left:0;top:0;width:700px;height:1920px;z-index:60;opacity:0;background:linear-gradient(100deg,transparent 0%,rgba(255,226,180,.0) 30%,rgba(255,226,180,.38) 50%,rgba(255,180,200,.0) 70%,transparent 100%)"></div>')
            js.append(f'tl.fromTo("#city-flare{i}",{{x:-800,opacity:1}},{{x:1200,opacity:1,duration:.75,ease:"power2.inOut"}},{t0-.3:.3f});tl.set("#city-flare{i}",{{opacity:0}},{t0+.5:.3f});')
    # bokeh + light trails + vignette (shared)
    r = random.Random(99); bok = []
    for k in range(16):
        s = r.randint(40, 170); c = r.choice(['255,214,160', '255,120,170', '120,220,255', '255,240,220'])
        x, y = r.randint(-60, 1080), r.randint(300, 1700)
        bok.append(f'<div id="city-bk{k}" class="abs" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;border-radius:50%;background:radial-gradient(circle,rgba({c},.55) 0%,rgba({c},.18) 45%,rgba({c},0) 70%);opacity:{r.uniform(.25,.7):.2f}"></div>')
        js.append(f'tl.fromTo("#city-bk{k}",{{x:0,y:0}},{{x:{r.randint(-120,120)},y:{r.randint(-260,-60)},duration:{total:.2f},ease:"none"}},0);')
    trails = []
    for k in range(9):
        y = 1385 + k * 26 + r.randint(-6, 6); w = r.randint(260, 620); red = k % 3 != 0
        col = 'rgba(255,70,70,.95)' if red else 'rgba(255,244,214,.95)'
        trails.append(f'<div id="city-tr{k}" class="abs" style="left:0;top:{y}px;width:{w}px;height:{r.choice([3,4,5])}px;border-radius:4px;background:linear-gradient(90deg,transparent,{col});box-shadow:0 0 18px {col}"></div>')
        dur = r.uniform(1.6, 3.2); n = int(total / dur) + 1; ltr = k % 2 == 0
        js.append(f'tl.fromTo("#city-tr{k}",{{x:{-w-50 if ltr else 1180}}},{{x:{1180 if ltr else -w-50},duration:{dur:.2f},repeat:{n},ease:"none"}},{r.uniform(0,1.5):.2f});')
    els.append(f'<div id="city-bokeh" class="abs" style="inset:0;z-index:30;mix-blend-mode:screen">{"".join(bok)}</div>')
    els.append(f'<div id="city-trails" class="abs" style="inset:0;z-index:31;mix-blend-mode:screen">{"".join(trails)}</div>')
    els.append('<div id="city-vig" class="abs" style="inset:0;z-index:40;background:radial-gradient(120% 70% at 50% 45%,rgba(0,0,0,0) 45%,rgba(0,0,0,.55) 100%),linear-gradient(180deg,rgba(2,3,8,.55) 0%,rgba(2,3,8,0) 22%,rgba(2,3,8,0) 70%,rgba(2,3,8,.6) 100%)"></div>')
    css = BASE_CSS + '#root{background:#03050C;overflow:hidden}.sky{opacity:0;transform-origin:50% 62%}'
    return scene_file('city', ''.join(els), '\n'.join(js), css)

class Scene:
    def __init__(s, sid, start, end):
        s.sid, s.start, s.end = sid, start, end; s.dur = end - start; s.els = []; s.js = []; s.css = ''; s.n = 0
    def t(s, abs_t): return abs_t - s.start
    def id(s, name): return f'{s.sid}-{name}'
    def add(s, html): s.els.append(html)
    def a(s, js): s.js.append(js)
    def file(s): return scene_file(s.sid, '\n'.join(s.els), '\n'.join(s.js), BASE_CSS + s.css)

    # ---- components (times are ABSOLUTE film time) ----
    def text(s, name, html, y, t_in, t_out=None, kind='rise', cls='', style='', out='up'):
        i = s.id(name)
        s.add(f'<div id="{i}" class="full h {cls}" style="top:{y}px;{style}">{fit_html(html)}</div>')
        s.a(IN('#' + i, s.t(t_in), kind))
        if t_out is not None and t_out < s.end - .05: s.a(OUT('#' + i, s.t(t_out), out, s.t(t_in), kind))
        return i

    def header(s, num, title, sub, t_in, t_out=None, y=290):
        n = s.text('num', f'<span class="bod gt" style="font-size:210px;font-style:normal;font-weight:400">{num}</span>', y - 20, t_in, t_out, 'zoom')
        s.add(f'<div id="{s.id("rule")}" class="abs h" style="left:440px;top:{y+205}px;width:200px;height:2px;background:linear-gradient(90deg,transparent,#E2C28A,transparent)"></div>')
        s.a(IN('#' + s.id('rule'), s.t(t_in) + .15, 'wipe'))
        if t_out: s.a(OUT('#' + s.id('rule'), s.t(t_out), 'fade'))
        s.text('ttl', f'<span class="syne shadow" style="font-size:92px">{title}</span>', y + 238, t_in + .12, t_out, 'rise')
        if sub: s.text('sub', f'<span class="bod gt" style="font-size:96px">{sub}</span>', y + 345, t_in + .3, t_out, 'rise')

    def chip(s, name, icon_html, label, x, y, t_in, t_out=None, kind='left', w=None, color='var(--ink)'):
        i = s.id(name); ws = f'width:{w}px;' if w else ''; fsz = min(44, int(700 / (len(label) * .70)))
        s.add(f'<div id="{i}" class="abs h glass" style="left:{x}px;top:{y}px;{ws}padding:22px 34px;display:flex;align-items:center;gap:26px">{icon_html}'
              f'<span style="font-family:Syne;font-weight:700;font-size:{fsz}px;color:{color};text-transform:uppercase;line-height:1.05;white-space:nowrap">{label}</span></div>')
        s.a(IN('#' + i, s.t(t_in), kind))
        if t_out is not None and t_out < s.end - .05: s.a(OUT('#' + i, s.t(t_out), 'fade', s.t(t_in), kind))
        return i

    def broll(s, name, src, t_in, t_out, media_start, label=None, x=170, y=200, w=740, h=890, kind='zoom', label_icon='spark'):
        i = s.id(name); vs = s.t(t_in) - .05; vd = (t_out - t_in) + .45
        s.add(f'<div id="{i}" class="abs h" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:44px;overflow:hidden;'
              f'box-shadow:0 50px 120px rgba(0,0,0,.65),0 0 0 1.5px rgba(232,198,144,.55);background:#000">'
              f'<div id="{i}-kb" style="position:absolute;inset:0"><video id="{i}-v" class="clip" data-start="{max(0,vs):.3f}" data-duration="{vd:.3f}" data-media-start="{media_start:.3f}" '
              f'muted playsinline src="assets/{src}" style="position:absolute;left:0;top:0;width:{w}px;height:{h}px;object-fit:cover"></video></div>'
              f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.0) 60%,rgba(0,0,0,.45) 100%)"></div></div>')
        s.a(IN('#' + i, s.t(t_in), kind))
        s.a(f'tl.fromTo("#{i}-kb",{{scale:1.12}},{{scale:1.0,duration:{t_out-t_in+.4:.2f},ease:"none"}},{s.t(t_in):.3f});')
        if t_out < s.end - .05: s.a(OUT('#' + i, s.t(t_out), 'shrink', s.t(t_in), kind))
        if label:
            s.chip(name + 'lb', icon(label_icon, 46), label, 0, y + h - 56, t_in + .35, t_out, 'fade', color='var(--ink)')
            s.a(f'tl.set("#{s.id(name+"lb")}",{{left:"50%",xPercent:-50}},0);')
        return i

    def bottle(s, name, t_in, t_out=None, cx=540, top=360, h=760, podium=True, halo=True):
        i = s.id(name); w = round(h * 319 / 963)
        halo_html = ''
        if halo:
            halo_html = (f'<div id="{i}-glow" class="abs" style="left:{cx-380}px;top:{top+h*.5-380:.0f}px;width:760px;height:760px;border-radius:50%;'
                         f'background:radial-gradient(circle,rgba(255,200,150,.42) 0%,rgba(195,18,59,.22) 38%,rgba(0,0,0,0) 68%)"></div>'
                         f'<svg id="{i}-ring" class="abs" style="left:{cx-310}px;top:{top+h*.5-310:.0f}px" width="620" height="620" viewBox="0 0 620 620">'
                         f'<circle cx="310" cy="310" r="300" fill="none" stroke="#E2C28A" stroke-width="1.5" stroke-dasharray="2 12" opacity=".8"/>'
                         f'<circle cx="310" cy="310" r="262" fill="none" stroke="#E2C28A" stroke-width="1" opacity=".45"/></svg>')
        pod = (f'<div class="abs" style="left:{cx-260}px;top:{top+h-34}px;width:520px;height:70px;border-radius:50%;background:radial-gradient(ellipse at 50% 40%,#2a2f4d 0%,#0b0e1c 70%);'
               f'box-shadow:0 0 0 1.5px rgba(232,198,144,.55),0 30px 60px rgba(0,0,0,.7)"></div>') if podium else ''
        s.add(f'<div id="{i}" class="abs h" style="left:0;top:0;width:1080px;height:1920px">{halo_html}{pod}'
              f'<div id="{i}-b" class="abs" style="left:{cx-w/2:.0f}px;top:{top}px;width:{w}px;height:{h}px">'
              f'<img src="assets/bombshell.png" style="position:absolute;left:0;top:0;width:{w}px;height:{h}px;filter:drop-shadow(0 30px 40px rgba(0,0,0,.6))">'
              f'<div id="{i}-sh" style="position:absolute;inset:0;-webkit-mask-image:url(assets/bombshell.png);mask-image:url(assets/bombshell.png);-webkit-mask-size:100% 100%;mask-size:100% 100%;'
              f'background:linear-gradient(105deg,transparent 35%,rgba(255,255,255,.65) 50%,transparent 65%);background-size:300% 100%;background-position:100% 0;mix-blend-mode:screen"></div></div></div>')
        s.a(IN('#' + i, s.t(t_in), 'fade'))
        s.a(f'tl.fromTo("#{i}-b",{{y:260,opacity:0,scale:.9}},{{y:0,opacity:1,scale:1,duration:1.0,ease:"expo.out"}},{s.t(t_in):.3f});')
        s.a(f'tl.fromTo("#{i}-sh",{{backgroundPosition:"100% 0"}},{{backgroundPosition:"-50% 0",duration:1.1,ease:"power2.inOut"}},{s.t(t_in)+.55:.3f});')
        if halo:
            s.a(f'tl.fromTo("#{i}-ring",{{rotation:0,scale:.6,opacity:0}},{{rotation:40,scale:1,opacity:1,duration:{max(1.5,s.dur-s.t(t_in)):.2f},ease:"power1.out"}},{s.t(t_in):.3f});')
            s.a(f'tl.fromTo("#{i}-glow",{{scale:.5,opacity:0}},{{scale:1,opacity:1,duration:1.2,ease:"power2.out"}},{s.t(t_in):.3f});')
        if t_out is not None and t_out < s.end - .05: s.a(OUT('#' + i, s.t(t_out), 'fade'))
        return i

    def coins(s, t_in, n=6):
        r = random.Random(4)
        for k in range(n):
            i = s.id(f'coin{k}'); x = 140 + k * 140 + r.randint(-30, 30)
            s.add(f'<div id="{i}" class="abs h" style="left:{x}px;top:180px;width:120px;height:120px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#FFF1C8,#E2C28A 45%,#9C6B2E 100%);'
                  f'box-shadow:0 10px 30px rgba(0,0,0,.6),inset 0 0 0 6px rgba(255,255,255,.25);display:flex;align-items:center;justify-content:center;font-family:Bodoni Moda;font-weight:800;font-size:44px;color:#5a3a10">RM</div>')
            s.a(f'tl.fromTo("#{i}",{{opacity:1,y:-300,rotation:{r.randint(-90,90)}}},{{opacity:0,y:{r.randint(1150,1400)},rotation:{r.randint(-360,360)},duration:{r.uniform(1.4,2.0):.2f},ease:"power2.in"}},{s.t(t_in)+k*.08:.3f});')

    def particles(s, name, t_in, cx, cy, n=22, spread=420, up=True, color='255,226,180'):
        r = random.Random(len(name) * 13)
        for k in range(n):
            i = s.id(f'{name}{k}'); sz = r.randint(6, 20)
            s.add(f'<div id="{i}" class="abs h" style="left:{cx}px;top:{cy}px;width:{sz}px;height:{sz}px;border-radius:50%;background:rgba({color},.95);box-shadow:0 0 {sz}px {sz//2}px rgba({color},.45)"></div>')
            dx = r.uniform(-spread, spread); dy = -r.uniform(150, 600) if up else r.uniform(-200, 200)
            s.a(f'tl.fromTo("#{i}",{{opacity:0,x:0,y:0,scale:.3}},{{keyframes:[{{opacity:1,scale:1,duration:.25}},{{opacity:0,x:{dx:.0f},y:{dy:.0f},scale:{r.uniform(.4,1.6):.2f},duration:{r.uniform(1.2,2.2):.2f},ease:"power2.out"}}]}},{s.t(t_in)+r.uniform(0,.5):.3f});')

    def scent_card(s, name, kind, y, t_in, tags, mood_icon, mood):
        i = s.id(name)
        img = 'bombshell' if kind == 'Bombshell' else 'noche'
        vis = (f'<div style="width:190px;height:300px;position:relative;flex:none;border-radius:26px;background:radial-gradient(circle at 50% 45%,rgba(255,255,255,.14),rgba(0,0,0,0) 70%)">'
               f'<img src="assets/{img}.png" style="position:absolute;left:46px;top:2px;width:98px;height:296px;filter:drop-shadow(0 16px 24px rgba(0,0,0,.6))"></div>')
        tg = ''.join(f'<span style="padding:10px 22px;border-radius:999px;border:1.5px solid rgba(232,198,144,.6);font-family:Syne;font-weight:700;font-size:28px;color:#F6F1E7;text-transform:uppercase">{t}</span>' for t in tags)
        bg = 'linear-gradient(150deg,rgba(80,14,34,.82),rgba(14,8,18,.86))' if kind == 'Bombshell' else 'linear-gradient(150deg,rgba(52,22,86,.84),rgba(10,8,24,.88))'
        s.add(f'<div id="{i}" class="abs h glass" style="left:70px;top:{y}px;width:940px;height:360px;background:{bg};display:flex;align-items:center;gap:34px;padding:30px 40px">{vis}'
              f'<div style="display:flex;flex-direction:column;gap:18px"><div class="syn" style="font-size:18px">{"Woman Glory" if kind == "Bombshell" else "Noche"}</div>'
              f'<div class="bod gt" style="font-size:{86 if kind=="Bombshell" else 70}px;font-weight:600">{kind}</div><div style="display:flex;gap:12px;flex-wrap:wrap">{tg}</div>'
              f'<div style="display:flex;align-items:center;gap:12px;font-family:Syne;font-size:28px;color:rgba(246,241,231,.75);text-transform:uppercase;letter-spacing:.08em">{icon(mood_icon,44)}{mood}</div></div></div>')
        s.a(IN('#' + i, s.t(t_in), 'right' if kind != 'Bombshell' else 'left'))
        return i

    def stock_bar(s, t_in, t_drain_end):
        i = s.id('stock')
        s.add(f'<div id="{i}" class="abs h glass" style="left:110px;top:280px;width:860px;padding:30px 40px">'
              f'<div style="display:flex;justify-content:space-between;align-items:baseline"><span class="syne" style="font-size:52px">Stok</span><span class="bod gt" style="font-size:60px">terhad</span></div>'
              f'<div style="margin-top:22px;height:22px;border-radius:12px;background:rgba(255,255,255,.08);overflow:hidden"><div id="{i}-f" style="height:100%;width:100%;border-radius:12px;background:linear-gradient(90deg,#FF3B5C,#FFB347,#E2C28A);transform-origin:0 50%"></div></div>'
              f'<div style="margin-top:14px;font-family:Syne;font-size:26px;color:rgba(246,241,231,.7);letter-spacing:.14em;text-transform:uppercase">Hampir habis</div></div>')
        s.a(IN('#' + i, s.t(t_in), 'down'))
        s.a(f'tl.fromTo("#{i}-f",{{scaleX:1}},{{scaleX:.12,duration:{t_drain_end-t_in:.2f},ease:"power2.inOut"}},{s.t(t_in)+.3:.3f});')
        return i

    def bag_cta(s, t_bag, t_btn, t_end):
        i = s.id('bag')
        s.add(f'<div id="{i}-rip" class="abs h" style="left:340px;top:470px;width:400px;height:400px;border-radius:50%;border:3px solid #FFD43B"></div>')
        s.add(f'<div id="{i}" class="abs h" style="left:390px;top:500px;width:300px;height:300px;filter:drop-shadow(0 0 60px rgba(255,200,0,.55))">{bag_svg(300)}</div>')
        s.a(IN('#' + i, s.t(t_bag), 'pop'))
        n = int((t_end - t_bag) / .5)
        s.a(f'tl.fromTo("#{i}",{{scale:1}},{{scale:1.08,duration:.25,repeat:{n},yoyo:true,ease:"sine.inOut",immediateRender:false}},{s.t(t_bag)+.5:.3f});')
        s.a(f'tl.fromTo("#{i}-rip",{{opacity:.9,scale:.6}},{{opacity:0,scale:1.6,duration:1,repeat:{int((t_end-t_bag)/1)},ease:"power2.out"}},{s.t(t_bag)+.2:.3f});')
        s.text('tk', '<span class="syne x8 shadow" style="font-size:150px">Tekan</span>', 820, t_bag + .1, None, 'slam')
        s.text('bk', '<span class="bod gt" style="font-size:124px;font-weight:700">beg kuning</span>', 950, t_bag + .25, None, 'slam')
        # arrow toward bottom-left (shop basket)
        s.add(f'<svg id="{s.id("arr")}" class="abs h" style="left:90px;top:1080px" width="170" height="170" viewBox="0 0 100 100"><path d="M80 20 L26 74 M26 74 L26 36 M26 74 L64 74" fill="none" stroke="#FFD43B" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>')
        s.a(IN('#' + s.id('arr'), s.t(t_bag) + .4, 'pop'))
        s.a(f'tl.fromTo("#{s.id("arr")}",{{x:0,y:0}},{{x:-18,y:18,duration:.35,repeat:{int((t_end-t_bag)/.35)},yoyo:true,ease:"sine.inOut",immediateRender:false}},{s.t(t_bag)+.9:.3f});')
        b = s.id('btn')
        s.add(f'<div id="{b}" class="full h" style="top:1092px"><span style="display:inline-block;padding:20px 46px;white-space:nowrap;border-radius:999px;background:linear-gradient(180deg,#FFF1D0,#E2C28A);'
              f'font-family:Syne;font-weight:700;font-size:44px;color:#1a1208;letter-spacing:.04em;box-shadow:0 20px 60px rgba(226,194,138,.45)">CHECKOUT SEKARANG →</span></div>')
        s.a(IN('#' + b, s.t(t_btn), 'pop'))
        s.a(f'tl.fromTo("#{b}",{{scale:1}},{{scale:1.06,duration:.3,repeat:{int((t_end-t_btn)/.3)},yoyo:true,ease:"sine.inOut",immediateRender:false}},{s.t(t_btn)+.5:.3f});')

def sfx_tags(cues):
    """cues: [(t_abs, name, vol)] -> audio tags. Impact/whoosh-cinematic trimmed so the hit lands on t."""
    PEAK = {'whoosh': .164, 'whoosh-short': .164, 'pop': .12, 'ping': .05, 'sparkle': .03, 'click': .075, 'click-soft': .075, 'glitch-3': .29, 'key-press': .08}
    TRIM = {'impact-bass-1': (1.80, .156), 'impact-bass-2': (1.70, .366), 'whoosh-cinematic': (1.9, .65), 'riser': (0.0, 3.03)}
    FD = {'whoosh': .57, 'whoosh-short': .57, 'whoosh-cinematic': 5.54, 'impact-bass-1': 2.12, 'impact-bass-2': 2.59, 'pop': .72, 'ping': 1.32, 'sparkle': 1.8,
          'click': .37, 'click-soft': .37, 'riser': 10.03, 'glitch-3': 3.1, 'key-press': .4}
    out = []
    for k, (t, nm, vol) in enumerate(sorted(cues)):
        if nm in TRIM:
            ms, pk = TRIM[nm]; st = t - pk; dur = {'impact-bass-1': .32, 'impact-bass-2': .89, 'whoosh-cinematic': 1.6, 'riser': 3.1}[nm]
        else:
            ms, st, dur = 0, t - PEAK.get(nm, 0) + 1 / 30, None
        if st < 0: ms += -st; st = 0
        if not dur: dur = FD[nm] - ms
        out.append(f'<audio id="sfx{k}" class="clip" data-start="{st:.3f}" data-duration="{dur:.3f}" data-media-start="{ms:.3f}" data-volume="{vol}" data-track-index="{10+k%8}" src="assets/sfx/{nm}.mp3"></audio>')
    return out

def index_html(total, hosts, audio, aroll=None, aroll_js=''):
    ar = ''
    if aroll:
        ar = (f'<div id="aroll-wrap" style="position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:5;opacity:0;transform-origin:50% 50%;'
              f'clip-path:inset(150px 50px 150px 50px round 64px)"><div id="aroll-zoom" style="position:absolute;inset:0;transform-origin:50% 40%">'
              f'<video id="aroll" class="clip" data-start="0" data-duration="{total-0.05:.3f}" data-track-index="2" muted playsinline src="assets/{aroll}" '
              f'style="position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover"></video></div>'
              f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.35) 0%,rgba(0,0,0,0) 18%,rgba(0,0,0,0) 62%,rgba(0,0,0,.55) 100%)"></div></div>'
              f'<div id="aroll-frame" style="position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:6;opacity:0;pointer-events:none;transform-origin:50% 50%">'
              f'<div style="position:absolute;left:50px;top:150px;right:50px;bottom:150px;border-radius:64px;border:3px solid rgba(232,198,144,.75);box-shadow:0 0 60px rgba(226,194,138,.35)"></div></div>')
    host = ''.join(f'<div id="{h["id"]}" data-composition-id="{h["id"]}" data-composition-src="compositions/{h["id"]}.html" data-start="{h["start"]:.3f}" '
                   f'data-duration="{h["dur"]:.3f}" data-track-index="{h["track"]}" data-track-kind="{h.get("kind","graphics")}" data-width="1080" data-height="1920" '
                   f'style="z-index:{h["z"]}"></div>\n' for h in hosts)
    return f'''<!doctype html>
<html lang="ms">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:#03050C}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden}}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{total:.3f}" data-width="1080" data-height="1920" data-fps="30">
<div id="bgfill" style="position:absolute;inset:0;background:#03050C;z-index:0"></div>
{ar}
{host}
{chr(10).join(audio)}
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
{aroll_js}
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''

# A-roll states for the wrapper (pre-scale coordinates inside 1080x1920)
AR = {
 'low':  {'w': '{opacity:1,scale:.58,x:0,y:40,clipPath:"inset(150px 50px 150px 50px round 64px)"}', 'f': '{opacity:1,scale:.58,x:0,y:40}'},
 'full': {'w': '{opacity:1,scale:1,x:0,y:-110,clipPath:"inset(0px 0px 0px 0px round 0px)"}', 'f': '{opacity:0,scale:1,x:0,y:-110}'},
 'off':  {'w': '{opacity:0,scale:.55,x:0,y:160,clipPath:"inset(150px 50px 150px 50px round 64px)"}', 'f': '{opacity:0,scale:.55,x:0,y:160}'},
}
def aroll_js(states, punches=()):
    js = []
    for k, (t, st) in enumerate(states):
        d = 0 if k == 0 else .55
        if d == 0:
            js.append(f'tl.set("#aroll-wrap",{AR[st]["w"]},0);tl.set("#aroll-frame",{AR[st]["f"]},0);')
        else:
            js.append(f'tl.to("#aroll-wrap",Object.assign({AR[st]["w"]},{{duration:{d},ease:"expo.inOut"}}),{t-.25:.3f});')
            js.append(f'tl.to("#aroll-frame",Object.assign({AR[st]["f"]},{{duration:{d},ease:"expo.inOut"}}),{t-.25:.3f});')
    for t, sc, dur in punches:
        js.append(f'tl.fromTo("#aroll-zoom",{{scale:1}},{{scale:{sc},duration:.18,ease:"power3.out"}},{t:.3f});tl.to("#aroll-zoom",{{scale:1,duration:.5,ease:"power2.inOut"}},{t+dur:.3f});')
    return '\n'.join(js)

# ---------------- real-photo / real-video night city background ----------------
RLOC = {'klcc_hero': ('KLCC · KUALA LUMPUR', '3.1579° N  ·  101.7116° E'),
        'klcc_up': ('PETRONAS TWIN TOWERS · KLCC', '3.1579° N  ·  101.7116° E'),
        'klcc_cloud': ('KLCC · KUALA LUMPUR', '3.1579° N  ·  101.7116° E'),
        'bb_monorail': ('BUKIT BINTANG · KL', '3.1466° N  ·  101.7101° E'),
        'bb_street': ('BUKIT BINTANG · KL', '3.1466° N  ·  101.7101° E'),
        'komtar_n': ('KOMTAR · PULAU PINANG', '5.4146° N  ·  100.3296° E'),
        'penang_lights': ('PULAU PINANG · BUKIT BENDERA', '5.4240° N  ·  100.2690° E'),
        'alor_hdr_n': ('MENARA ALOR SETAR · KEDAH', '6.1219° N  ·  100.3695° E'),
        'ramlee': ('JALAN P. RAMLEE · KL', '3.1554° N  ·  101.7068° E'),
        'kl_skyline': ('KUALA LUMPUR · MALAM', '3.1390° N  ·  101.6869° E')}

def city_scene_real(segs, total):
    """segs: [(t0, t1, name)]; name 'bb_monorail' is a video, the rest are graded stills (1242x2208)."""
    els, js = [], []
    for i, (t0, t1, nm) in enumerate(segs):
        d = t1 - t0
        if nm.endswith('monorail'):
            media = (f'<video id="city-s{i}-v" class="clip" data-start="{max(0,t0-.25):.3f}" data-duration="{d+1.0:.3f}" data-media-start="0" muted playsinline '
                     f'src="assets/city/{nm}.mp4" style="position:absolute;left:81px;top:144px;width:1080px;height:1920px;object-fit:cover"></video>')
        else:
            media = f'<img src="assets/city/{nm}.jpg" style="position:absolute;left:0;top:0;width:1242px;height:2208px">'
        els.append(f'<div id="city-s{i}" class="abs sky" style="left:-81px;top:-144px;width:1242px;height:2208px;z-index:{i+1}">{media}</div>')
        if i == 0: js.append(f'tl.set("#city-s{i}",{{opacity:1}},0);')
        else: js.append(f'tl.fromTo("#city-s{i}",{{opacity:0}},{{opacity:1,duration:.7,ease:"power2.inOut"}},{t0-.2:.3f});')
        if i + 1 < len(segs): js.append(f'tl.set("#city-s{i}",{{opacity:0}},{t1+.6:.3f});')
        r = random.Random(i * 11 + 5); dx = r.choice([-1, 1]) * 30
        js.append(f'tl.fromTo("#city-s{i}",{{scale:1.0,x:{-dx},y:0}},{{scale:1.09,x:{dx},y:-24,duration:{d+1:.2f},ease:"none"}},{max(0,t0-.2):.3f});')
        a, b = RLOC[nm]
        els.append(f'<div id="city-tag{i}" class="abs h" style="left:72px;top:190px;z-index:50"><div class="syn" id="city-tag{i}a">◆ {a}</div>'
                   f'<div style="font-family:Syne;font-size:17px;letter-spacing:.18em;color:rgba(246,241,231,.7);margin-top:10px">{b}</div></div>')
        js.append(IN(f'#city-tag{i}', t0 + .25, 'fade') + IN(f'#city-tag{i}a', t0 + .25, 'track'))
        js.append(f'tl.to("#city-tag{i}",{{opacity:0,duration:.3}},{min(t0+3.2,t1-.3):.2f});')
        if i:
            els.append(f'<div id="city-flare{i}" class="abs" style="left:0;top:0;width:700px;height:1920px;z-index:60;opacity:0;background:linear-gradient(100deg,transparent 0%,rgba(255,226,180,0) 30%,rgba(255,226,180,.42) 50%,rgba(255,180,200,0) 70%,transparent 100%)"></div>')
            js.append(f'tl.fromTo("#city-flare{i}",{{x:-800,opacity:1}},{{x:1200,opacity:1,duration:.7,ease:"power2.inOut"}},{t0-.3:.3f});tl.set("#city-flare{i}",{{opacity:0}},{t0+.45:.3f});')
    # soft bokeh (light leaks) + legibility shading
    r = random.Random(99); bok = []
    for k in range(9):
        s = r.randint(80, 220); c = r.choice(['255,214,160', '255,140,180', '255,240,220'])
        x, y = r.randint(-60, 1080), r.randint(250, 1600)
        bok.append(f'<div id="city-bk{k}" class="abs" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;border-radius:50%;background:radial-gradient(circle,rgba({c},.40) 0%,rgba({c},.12) 45%,rgba({c},0) 70%);opacity:{r.uniform(.25,.55):.2f}"></div>')
        js.append(f'tl.fromTo("#city-bk{k}",{{x:0,y:0}},{{x:{r.randint(-120,120)},y:{r.randint(-260,-60)},duration:{total:.2f},ease:"none"}},0);')
    els.append(f'<div id="city-bokeh" class="abs" style="inset:0;z-index:30;mix-blend-mode:screen">{"".join(bok)}</div>')
    els.append('<div id="city-shade" class="abs" style="inset:0;z-index:40;background:linear-gradient(180deg,rgba(3,4,10,.62) 0%,rgba(3,4,10,.30) 16%,rgba(3,4,10,.22) 40%,rgba(3,4,10,.40) 58%,rgba(3,4,10,.72) 70%,rgba(3,4,10,.55) 85%,rgba(3,4,10,.75) 100%)"></div>')
    els.append('<div id="city-vig" class="abs" style="inset:0;z-index:41;background:radial-gradient(120% 75% at 50% 45%,rgba(0,0,0,0) 50%,rgba(0,0,0,.55) 100%)"></div>')
    css = BASE_CSS + '#root{background:#03050C;overflow:hidden}.sky{opacity:0;transform-origin:50% 55%}'
    return scene_file('city', ''.join(els), '\n'.join(js), css)

def duo(s, name, t_in, top=330, h=680):
    """NOCHE + Bombshell rising together on one podium."""
    i = s.id(name); w = round(h * 319 / 963)
    s.add(f'<div id="{i}" class="abs h" style="left:0;top:0;width:1080px;height:1920px">'
          f'<div id="{i}-glow" class="abs" style="left:110px;top:{top+h*.5-430:.0f}px;width:860px;height:860px;border-radius:50%;background:radial-gradient(circle,rgba(255,200,150,.40) 0%,rgba(150,60,200,.22) 38%,rgba(0,0,0,0) 68%)"></div>'
          f'<svg id="{i}-ring" class="abs" style="left:200px;top:{top+h*.5-340:.0f}px" width="680" height="680" viewBox="0 0 680 680"><circle cx="340" cy="340" r="330" fill="none" stroke="#E2C28A" stroke-width="1.5" stroke-dasharray="2 12" opacity=".8"/><circle cx="340" cy="340" r="290" fill="none" stroke="#E2C28A" stroke-width="1" opacity=".45"/></svg>'
          f'<div class="abs" style="left:200px;top:{top+h-36}px;width:680px;height:80px;border-radius:50%;background:radial-gradient(ellipse at 50% 40%,#2a2f4d 0%,#0b0e1c 70%);box-shadow:0 0 0 1.5px rgba(232,198,144,.55),0 30px 60px rgba(0,0,0,.7)"></div>'
          + ''.join(f'<div id="{i}-{k}" class="abs" style="left:{cx-w/2:.0f}px;top:{top}px;width:{w}px;height:{h}px">'
                    f'<img src="assets/{img}.png" style="position:absolute;left:0;top:0;width:{w}px;height:{h}px;filter:drop-shadow(0 30px 40px rgba(0,0,0,.6))">'
                    f'<div id="{i}-sh{k}" style="position:absolute;inset:0;-webkit-mask-image:url(assets/{img}.png);mask-image:url(assets/{img}.png);-webkit-mask-size:100% 100%;mask-size:100% 100%;'
                    f'background:linear-gradient(105deg,transparent 35%,rgba(255,255,255,.6) 50%,transparent 65%);background-size:300% 100%;background-position:100% 0;mix-blend-mode:screen"></div></div>'
                    for k, (img, cx) in enumerate([('noche', 395), ('bombshell', 685)])) + '</div>')
    s.a(IN('#' + i, s.t(t_in), 'fade'))
    for k in range(2):
        s.a(f'tl.fromTo("#{i}-{k}",{{y:280,opacity:0,rotation:{-6 if k == 0 else 6}}},{{y:0,opacity:1,rotation:{-3 if k == 0 else 3},duration:1.0,ease:"expo.out"}},{s.t(t_in)+k*.15:.3f});')
        s.a(f'tl.fromTo("#{i}-sh{k}",{{backgroundPosition:"100% 0"}},{{backgroundPosition:"-50% 0",duration:1.1,ease:"power2.inOut"}},{s.t(t_in)+.6+k*.15:.3f});')
    s.a(f'tl.fromTo("#{i}-ring",{{rotation:0,scale:.6,opacity:0}},{{rotation:40,scale:1,opacity:1,duration:{max(1.5,s.dur-s.t(t_in)):.2f},ease:"power1.out"}},{s.t(t_in):.3f});')
    s.a(f'tl.fromTo("#{i}-glow",{{scale:.5,opacity:0}},{{scale:1,opacity:1,duration:1.2,ease:"power2.out"}},{s.t(t_in):.3f});')
    return i

Scene.duo = duo
