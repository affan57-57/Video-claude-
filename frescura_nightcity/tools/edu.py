# Animated educational infographics for the FRESCURA edit (times are absolute film time).
from lib import IN, OUT, icon, G

def steps_compare(s, t_steps, t_right, t_out):
    """Sabun biasa: 3 langkah  vs  Frescura: 1 langkah."""
    steps = [('sponge', 'Basahkan span'), ('scrub', 'Gosok lama'), ('drop', 'Baru berbuih')]
    rows = ''.join(
        f'<div id="{s.id(f"st{k}")}" class="h" style="display:flex;align-items:center;gap:16px;margin-top:26px">'
        f'<div style="width:58px;height:58px;flex:none;border-radius:50%;border:2px solid rgba(255,255,255,.35);display:flex;align-items:center;justify-content:center;font-family:Syne;font-weight:800;font-size:28px;color:#cfcfcf">{k+1}</div>'
        f'{icon(ic, 54, "#bdbdbd", 5)}<span style="font-family:Syne;font-weight:700;font-size:30px;color:#d6d6d6;text-transform:uppercase;line-height:1.05">{tx}</span></div>'
        for k, (ic, tx) in enumerate(steps))
    s.add(f'<div id="{s.id("cl")}" class="abs h glass" style="left:60px;top:400px;width:470px;height:700px;padding:34px 30px;background:linear-gradient(160deg,rgba(40,40,48,.78),rgba(12,12,16,.85));border-color:rgba(255,255,255,.18)">'
          f'<div class="syne" style="font-size:40px;color:#bdbdbd">Sabun biasa</div><div class="bod" style="font-size:54px;color:#FF5A6E;margin-top:6px">3 langkah</div>{rows}'
          f'<div id="{s.id("stx")}" class="h" style="margin-top:34px;display:flex;align-items:center;gap:14px">{icon("x", 60)}<span style="font-family:Syne;font-weight:800;font-size:34px;color:#FF5A6E">LECEH</span></div></div>')
    bub = ''.join(f'<div id="{s.id(f"bb{k}")}" class="abs h" style="left:{x}px;top:{y}px;width:{r}px;height:{r}px;border-radius:50%;'
                  f'background:radial-gradient(circle at 35% 30%,#fff,rgba(255,200,220,.85) 40%,rgba(255,150,190,.55) 75%);box-shadow:0 0 18px rgba(255,180,210,.6)"></div>'
                  for k, (x, y, r) in enumerate([(120, 420, 90), (200, 390, 70), (90, 350, 56), (250, 450, 60), (170, 470, 76), (60, 440, 50), (290, 400, 44)]))
    s.add(f'<div id="{s.id("cr")}" class="abs h glass" style="left:550px;top:400px;width:470px;height:700px;padding:34px 30px;border-color:rgba(232,198,144,.95);box-shadow:0 0 90px rgba(226,194,138,.35)">'
          f'<div class="syne gt" style="font-size:40px">Frescura</div><div class="bod" style="font-size:54px;color:#F1DDB0;margin-top:6px">1 langkah</div>'
          f'<div style="display:flex;align-items:center;gap:16px;margin-top:26px"><div style="width:58px;height:58px;border-radius:50%;background:linear-gradient(180deg,#FFF1D0,#E2C28A);display:flex;align-items:center;justify-content:center;font-family:Syne;font-weight:800;font-size:28px;color:#1a1208">1</div>'
          f'{icon("pump", 58)}<span style="font-family:Syne;font-weight:800;font-size:34px;color:#F6F1E7">TEKAN PAM</span></div>'
          f'<div id="{s.id("crc")}" class="h" style="position:absolute;left:30px;bottom:34px;display:flex;align-items:center;gap:14px">{icon("check", 60)}<span style="font-family:Syne;font-weight:800;font-size:34px;color:#E2C28A">TERUS BUIH</span></div>{bub}</div>')
    s.a(IN('#' + s.id('cl'), s.t(t_steps[0]) - .1, 'left'))
    for k, t in enumerate(t_steps):
        s.a(IN('#' + s.id(f'st{k}'), s.t(t), 'left'))
    s.a(IN('#' + s.id('stx'), s.t(t_steps[-1]) + .3, 'pop'))
    s.a(IN('#' + s.id('cr'), s.t(t_right), 'right'))
    for k in range(7):
        s.a(f'tl.fromTo("#{s.id(f"bb{k}")}",{{opacity:0,scale:0,y:40}},{{opacity:1,scale:1,y:0,duration:.45,ease:"back.out(2.5)"}},{s.t(t_right)+.3+k*.07:.3f});')
    s.a(IN('#' + s.id('crc'), s.t(t_right) + .55, 'pop'))
    for n in ['cl', 'cr']: s.a(OUT('#' + s.id(n), s.t(t_out), 'fade'))

def foam_formula(s, t_in, t_out, y=985):
    """Cecair + Udara = Buih (sits on the B-roll card's lower edge)."""
    parts = [('drop', 'Cecair'), ('+', None), ('wave', 'Udara'), ('=', None), ('bubbles', 'Buih lembut')]
    html = []
    for k, (ic, lb) in enumerate(parts):
        if lb is None:
            html.append(f'<span id="{s.id(f"ff{k}")}" class="h bod gt" style="font-size:70px;font-weight:700;margin:0 6px">{ic}</span>')
        else:
            vis = (icon(ic, 64) if ic != 'bubbles' else
                   '<svg width="64" height="64" viewBox="0 0 100 100"><circle cx="34" cy="60" r="22" fill="none" stroke="#E2C28A" stroke-width="5"/><circle cx="66" cy="40" r="16" fill="none" stroke="#E2C28A" stroke-width="5"/><circle cx="70" cy="76" r="10" fill="none" stroke="#E2C28A" stroke-width="5"/></svg>')
            html.append(f'<div id="{s.id(f"ff{k}")}" class="h" style="display:flex;flex-direction:column;align-items:center;gap:6px">{vis}<span style="font-family:Syne;font-weight:700;font-size:24px;color:#F6F1E7;text-transform:uppercase;white-space:nowrap">{lb}</span></div>')
    s.add(f'<div id="{s.id("ff")}" class="abs h glass" style="left:110px;top:{y}px;width:860px;height:150px;display:flex;align-items:center;justify-content:center;gap:22px;border-radius:30px">{"".join(html)}</div>')
    s.a(IN('#' + s.id('ff'), s.t(t_in), 'up'))
    for k in range(5): s.a(IN('#' + s.id(f'ff{k}'), s.t(t_in) + .25 + k * .16, 'pop'))
    if t_out < s.end - .05: s.a(OUT('#' + s.id('ff'), s.t(t_out), 'fade'))

def salt_process(s, t_nodes, t_out, y=770):
    """Air laut -> disejat matahari -> kristal garam."""
    cx = [200, 540, 880]; labels = ['Air laut', 'Disejat matahari', 'Kristal garam']
    cube = ('<svg width="96" height="96" viewBox="0 0 100 100"><polygon points="50,14 86,34 50,54 14,34" fill="#fff" fill-opacity=".95"/>'
            '<polygon points="14,34 50,54 50,92 14,72" fill="#C9D6F2"/><polygon points="86,34 50,54 50,92 86,72" fill="#8EA2D2"/></svg>')
    vis = [icon('wave', 96), icon('sun', 96), cube]
    for k in range(3):
        s.add(f'<div id="{s.id(f"sn{k}")}" class="abs h" style="left:{cx[k]-95}px;top:{y}px;width:190px;display:flex;flex-direction:column;align-items:center;gap:16px">'
              f'<div style="width:170px;height:170px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:radial-gradient(circle at 50% 35%,rgba(60,70,120,.85),rgba(10,12,26,.9));'
              f'border:2px solid rgba(232,198,144,.75);box-shadow:0 0 50px rgba(226,194,138,.25)">{vis[k]}</div>'
              f'<span style="font-family:Syne;font-weight:700;font-size:26px;color:#F6F1E7;text-transform:uppercase;text-align:center;line-height:1.1;white-space:nowrap">{labels[k]}</span></div>')
        s.a(IN('#' + s.id(f'sn{k}'), s.t(t_nodes[k]), 'pop'))
        if k:
            s.add(f'<svg id="{s.id(f"sa{k}")}" class="abs" style="left:{cx[k-1]+90}px;top:{y+70}px" width="{cx[k]-cx[k-1]-180}" height="30" viewBox="0 0 {cx[k]-cx[k-1]-180} 30">'
                  f'<path id="{s.id(f"sap{k}")}" d="M4 15 L{cx[k]-cx[k-1]-196} 15 M{cx[k]-cx[k-1]-206} 5 L{cx[k]-cx[k-1]-194} 15 L{cx[k]-cx[k-1]-206} 25" stroke="{G}" stroke-width="4" fill="none" stroke-linecap="round" stroke-dasharray="200" stroke-dashoffset="200"/></svg>')
            s.a(f'tl.fromTo("#{s.id(f"sap{k}")}",{{strokeDashoffset:200}},{{strokeDashoffset:0,duration:.45,ease:"power2.out"}},{s.t(t_nodes[k])-.35:.3f});')
            if t_out < s.end - .05: s.a(OUT('#' + s.id(f'sa{k}'), s.t(t_out), 'fade'))
        if t_out < s.end - .05: s.a(OUT('#' + s.id(f'sn{k}'), s.t(t_out), 'fade'))
    # vapour rising from the sea node
    for k in range(6):
        i = s.id(f'vp{k}')
        s.add(f'<div id="{i}" class="abs h" style="left:{170+k*12}px;top:{y+40}px;width:14px;height:14px;border-radius:50%;background:rgba(200,220,255,.9);box-shadow:0 0 12px rgba(200,220,255,.7)"></div>')
        s.a(f'tl.fromTo("#{i}",{{opacity:0,x:0,y:0}},{{keyframes:[{{opacity:1,duration:.15}},{{opacity:0,x:{150+k*30},y:{-60-k*12},duration:.9,ease:"power1.out"}}]}},{s.t(t_nodes[1])-.4+k*.08:.3f});')

def perfume_pyramid(s, t_in, t_out, cx=330, top=760, h=380, w=470):
    """Top / Heart / Base notes, built bottom-up."""
    bands = [('Base note', 'tahan lama', .62), ('Heart note', 'jiwa wangian', .80), ('Top note', 'bau pertama', 1.0)]
    bh = h / 3
    for k, (nm, desc, op) in enumerate(bands):
        y0 = top + h - (k + 1) * bh; y1 = y0 + bh
        hw0 = w / 2 * ((y0 - top) / h); hw1 = w / 2 * ((y1 - top) / h)
        pts = f'{cx-hw1:.0f},{y1-top:.0f} {cx+hw1:.0f},{y1-top:.0f} {cx+hw0:.0f},{y0-top+4:.0f} {cx-hw0:.0f},{y0-top+4:.0f}'
        s.add(f'<svg id="{s.id(f"py{k}")}" class="abs h" style="left:0;top:{top}px" width="1080" height="{h}" viewBox="0 0 1080 {h}">'
              f'<polygon points="{pts}" fill="url(#{s.id("pyg")})" fill-opacity="{op}" stroke="#FFF1D0" stroke-opacity=".6" stroke-width="2"/></svg>')
        ly = y0 + bh / 2 - 36
        s.add(f'<div id="{s.id(f"pl{k}")}" class="abs h" style="left:{cx+hw1+28:.0f}px;top:{ly:.0f}px;white-space:nowrap">'
              f'<div class="syne" style="font-size:34px">{nm}</div><div class="bod gt" style="font-size:40px">{desc}</div></div>')
        t = s.t(t_in) + k * .28
        s.a(f'tl.fromTo("#{s.id(f"py{k}")}",{{opacity:0,y:40,scaleX:.6,transformOrigin:"{cx}px 50%"}},{{opacity:1,y:0,scaleX:1,duration:.45,ease:"back.out(1.8)"}},{t:.3f});')
        s.a(IN('#' + s.id(f'pl{k}'), t + .1, 'right'))
        if t_out < s.end - .05:
            s.a(OUT('#' + s.id(f'py{k}'), s.t(t_out), 'fade', t, 'rise')); s.a(OUT('#' + s.id(f'pl{k}'), s.t(t_out), 'fade', t + .1, 'right'))
    s.add(f'<svg width="0" height="0" style="position:absolute"><defs><linearGradient id="{s.id("pyg")}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF1D0"/><stop offset="1" stop-color="#B8884A"/></linearGradient></defs></svg>')

def scent_rings(s, t_in, cx=540, cy=900, n=5):
    for k in range(n):
        i = s.id(f'ring{k}')
        s.add(f'<div id="{i}" class="abs h" style="left:{cx-150}px;top:{cy-150}px;width:300px;height:300px;border-radius:50%;border:3px solid rgba(232,198,144,.9);box-shadow:0 0 30px rgba(226,194,138,.5)"></div>')
        s.a(f'tl.fromTo("#{i}",{{opacity:.95,scale:.2}},{{opacity:0,scale:3.2,duration:1.5,ease:"power2.out",immediateRender:false}},{s.t(t_in)+k*.28:.3f});')
