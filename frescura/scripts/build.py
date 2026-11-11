"""Generate the HyperFrames composition (project/index.html) from timeline.json.
All motion is keyed to word timestamps of the edited voice track, so every graphic lands on the spoken point.
Usage: python build.py PROJECT_DIR [--preview]
"""
import json, sys, html
P = sys.argv[1]; PREVIEW = "--preview" in sys.argv
tl = json.load(open(f"{P}/timeline.json")); W = tl["words"]
SEC = {s["name"]: s for s in tl["sections"]}
VOICE_END = tl["voice_dur"]; END_CARD = 2.9; TOTAL = round(VOICE_END + END_CARD, 3)
ws = lambda i: W[i]["s"]; we = lambda i: W[i]["e"]
T_TESTI, T_TESTI_END, T_CLOSE, T_END = SEC["testi"]["start"], SEC["testi"]["end"], SEC["closing"]["start"], SEC["closing"]["end"] + 0.08

# ---------- scene boundaries (output seconds) ----------
S2 = ws(8) - 0.04          # "Sebelum"
S3 = ws(12) - 0.06         # "tengok dulu apa kata pelanggan"
CUT1 = ws(54) - 0.02       # cutaway on "harum yang menyegarkan"
CUT2 = ws(57)              # second cutaway half
CUT_END = ws(60) - 0.03    # back to face on "Memang fresh"
C1 = T_CLOSE               # "Ha, dah yakin kan?"
C2 = ws(67) - 0.03         # "Jangan tangguh lagi"
C3 = ws(70) - 0.03         # "stok sangat-sangat terhad"
C4 = ws(74) - 0.03         # "tekan beg kuning sekarang dan checkout sekarang"
C6 = ws(82) - 0.03         # "tengok berapa harga TikTok"
E = T_END                  # end card

els = []; anim = []
def clip(start, end, inner, cls="", style="", z=1, id_=None):
    id_ = id_ or f"e{len(els)}"
    els.append(f'<div id="{id_}" class="clip {cls}" data-start="{start:.3f}" data-duration="{end-start:.3f}" style="z-index:{z};{style}">{inner}</div>')
    return id_
def video(src, start, end, z=1, cls="vid", media_start=0.0, id_=None):
    id_ = id_ or f"v{len(els)}"
    els.append(f'<div id="{id_}" class="vwrap {cls}" style="z-index:{z}">'
               f'<video id="{id_}_m" class="clip" src="assets/video/{src}" muted playsinline data-start="{start:.3f}" data-duration="{end-start:.3f}" data-media-start="{media_start:.3f}"></video></div>')
    return id_
def A(code): anim.append(code)

# ===================== VIDEO LAYERS =====================
v_hook = video("hook_pump.mp4", 0, S2, z=1)
A(f'tl.fromTo("#{v_hook}",{{scale:1.35,filter:"blur(18px) brightness(0.6)"}},{{scale:1.08,filter:"blur(0px) brightness(0.72)",duration:0.55,ease:"expo.out"}},0);')
A(f'tl.to("#{v_hook}",{{scale:1.0,duration:{S2-0.55:.3f},ease:"none"}},0.55);')
v_testi = video("testimonial.mp4", T_TESTI, T_TESTI_END + 0.1, z=2, id_="testi")
A(f'tl.fromTo("#testi",{{clipPath:"inset(31% 22% 31% 22% round 46px)",scale:1.04}},{{clipPath:"inset(0% 0% 0% 0% round 0px)",scale:1,duration:0.42,ease:"expo.inOut"}},{T_TESTI-0.02:.3f});')
v_c1 = video("foam_close.mp4", CUT1, CUT2, z=3)
v_c2 = video("beach_foam.mp4", CUT2, CUT_END, z=3)
for v, t0, t1 in ((v_c1, CUT1, CUT2), (v_c2, CUT2, CUT_END)):
    A(f'tl.fromTo("#{v}",{{scale:1.18,x:60}},{{scale:1.04,x:0,duration:{t1-t0:.3f},ease:"power2.out"}},{t0:.3f});')
v_yk = video("beach_hand.mp4", C1, C2, z=2)
A(f'tl.fromTo("#{v_yk}",{{scale:1.25,filter:"blur(10px) brightness(0.6)"}},{{scale:1.05,filter:"blur(0px) brightness(0.62)",duration:0.5,ease:"expo.out"}},{C1:.3f});')
v_pf = video("pump_fast.mp4", C2, C3, z=2)
A(f'tl.fromTo("#{v_pf}",{{scale:1.12,rotation:-2}},{{scale:1.0,rotation:0,duration:{C3-C2:.3f},ease:"power1.out"}},{C2:.3f});')
v_bag = video("foam_hand.mp4", C4, C6, z=2, cls="vid soft")
v_hero = video("bottle_hero.mp4", C6, E, z=2)
A(f'tl.fromTo("#{v_hero}",{{scale:1.2}},{{scale:1.04,duration:{E-C6:.3f},ease:"power2.out"}},{C6:.3f});')

# ===================== S1 HOOK =====================
hook = clip(0, S2, f'''
<div class="kicker gold" id="h_k">FRESCURA&nbsp;BODY</div>
<div class="hook">
  <div class="h1 mask"><span id="h_w1">Masih</span></div>
  <div class="h2 mask"><span id="h_w2" class="serif-i blush">ragu-ragu?</span></div>
  <div class="h3" id="h_w3">nak cuba <b class="brand">FRESCURA BODY</b><i class="uline" id="h_ul"></i></div>
</div>
<div class="flash" id="h_flash"></div>''', cls="layer", z=10)
A('tl.fromTo("#h_flash",{opacity:0.9},{opacity:0,duration:0.28,ease:"power2.out"},0);')
A('tl.fromTo("#h_k",{opacity:0,scale:1.25},{opacity:1,scale:1,duration:0.6,ease:"expo.out"},0.02);')
A(f'tl.fromTo("#h_w1",{{yPercent:110}},{{yPercent:0,duration:0.32,ease:"expo.out"}},{ws(0):.3f});')
A(f'tl.fromTo("#h_w2",{{yPercent:110,rotation:4}},{{yPercent:0,rotation:0,duration:0.34,ease:"expo.out"}},{ws(1):.3f});')
# hook "doubt" jitter on ragu-ragu
for k in range(6):
    A(f'tl.to("#h_w2",{{x:{[-9,8,-6,5,-3,0][k]},duration:0.035,ease:"none"}},{ws(1)+0.36+k*0.035:.3f});')
A(f'tl.fromTo("#h_w3",{{opacity:0,y:26}},{{opacity:1,y:0,duration:0.3,ease:"power3.out"}},{ws(3):.3f});')
A(f'tl.fromTo("#h_ul",{{scaleX:0}},{{scaleX:1,duration:0.4,ease:"expo.out"}},{ws(6):.3f});')
A(f'tl.to("#{hook} .hook",{{scale:0.92,opacity:0,filter:"blur(12px)",duration:0.16,ease:"power2.in"}},{S2-0.16:.3f});')

# ===================== S2 SEBELUM BUAT KEPUTUSAN (ivory editorial) =====================
s2 = clip(S2, S3 + 0.02, f'''
<div class="ivory-bg"><div class="grid"></div></div>
<div class="label-top ink" id="s2_l">01 &nbsp;—&nbsp; SEBELUM BUAT KEPUTUSAN</div>
<div class="card" id="s2_card"><div class="ticker"><div class="ticker-in" id="s2_tk">AROMATHERAPY &nbsp;·&nbsp; OCEAN SALT &nbsp;·&nbsp; GENTLE FOAMING &nbsp;·&nbsp; BODY SHOWER &nbsp;·&nbsp; 500ML &nbsp;·&nbsp; AROMATHERAPY &nbsp;·&nbsp; OCEAN SALT &nbsp;·&nbsp; GENTLE FOAMING &nbsp;·&nbsp;</div></div>
</div>
<div class="toggle" id="s2_tg"><span class="t-l">RAGU</span><div class="track"><i id="s2_knob"></i></div><span class="t-r">YAKIN</span></div>''', cls="layer", z=8)
els.append(f'<div id="s2_vw" class="cardvid" style="z-index:9"><video id="s2_vid" class="clip" src="assets/video/table_pump.mp4" muted playsinline data-start="{S2:.3f}" data-duration="{S3-S2+0.02:.3f}" data-media-start="0"></video></div>')
A(f'tl.fromTo("#{s2} .ivory-bg",{{clipPath:"circle(0% at 50% 50%)"}},{{clipPath:"circle(150% at 50% 50%)",duration:0.45,ease:"expo.out"}},{S2:.3f});')
A(f'tl.fromTo("#s2_card, #s2_vw",{{y:220,scale:0.86,rotation:3,opacity:0}},{{y:0,scale:1,rotation:0,opacity:1,duration:0.55,ease:"expo.out"}},{S2+0.05:.3f});')
A(f'tl.fromTo("#s2_l",{{opacity:0,x:-40}},{{opacity:1,x:0,duration:0.4,ease:"power3.out"}},{S2+0.1:.3f});')
A(f'tl.fromTo("#s2_tk",{{xPercent:0}},{{xPercent:-45,duration:{S3-S2:.3f},ease:"none"}},{S2:.3f});')
A(f'tl.fromTo("#s2_tg",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.35,ease:"back.out(2)"}},{ws(10):.3f});')
A(f'tl.fromTo("#s2_knob",{{x:0}},{{x:150,duration:0.5,ease:"expo.inOut"}},{ws(11):.3f});')
A(f'tl.to("#{s2}, #s2_vw",{{xPercent:-100,duration:0.2,ease:"power3.in"}},{S3-0.18:.3f});')

# ===================== S3 APA KATA PELANGGAN =====================
pol = "".join(f'<div class="pol" id="pol{i}"><img src="assets/img/fb_{t}.jpg"/></div>' for i, t in enumerate(("1.5", "7.5", "13.5")))
stars = "".join(f'<svg class="star" id="st{i}" viewBox="0 0 24 24"><path d="M12 2.5l2.9 6.1 6.6.8-4.9 4.6 1.3 6.6L12 17.3l-5.9 3.3 1.3-6.6-4.9-4.6 6.6-.8z"/></svg>' for i in range(5))
s3 = clip(S3, T_TESTI + 0.42, f'''
<div class="ink-bg"><div class="glow"></div></div>
<div class="bigquote serif-i gold" id="s3_q">&ldquo;</div>
<div class="pols">{pol}</div>
<div class="s3-head"><div class="label-top gold2" id="s3_l">02 &nbsp;—&nbsp; TESTIMONI SEBENAR</div>
<div class="s3-pre" id="s3_p">Tengok dulu…</div><div class="s3-t" id="s3_t">Apa kata <span class="serif-i blush">pelanggan</span> kami</div>
<div class="stars">{stars}</div></div>''', cls="layer", z=7)
A(f'tl.fromTo("#{s3} .ink-bg",{{xPercent:100}},{{xPercent:0,duration:0.22,ease:"power3.out"}},{S3-0.02:.3f});')
A(f'tl.fromTo("#s3_q",{{opacity:0,scale:2.2,rotation:-12}},{{opacity:0.9,scale:1,rotation:0,duration:0.5,ease:"expo.out"}},{S3+0.1:.3f});')
for i, (r, x) in enumerate(((-9, -250), (0, 0), (8, 250))):
    A(f'tl.fromTo("#pol{i}",{{y:900,rotation:{r*3},opacity:0}},{{y:0,x:{x},rotation:{r},opacity:1,duration:0.6,ease:"expo.out"}},{S3+0.15+i*0.12:.3f});')
A(f'tl.fromTo("#s3_l",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.35}},{ws(12)+0.1:.3f});')
A(f'tl.fromTo("#s3_p",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.35,ease:"expo.out"}},{ws(12):.3f});')
A(f'tl.fromTo("#s3_t",{{opacity:0,y:40,filter:"blur(10px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.45,ease:"expo.out"}},{ws(14):.3f});')
for i in range(5):
    A(f'tl.fromTo("#st{i}",{{scale:0,rotation:-90}},{{scale:1,rotation:0,duration:0.3,ease:"back.out(3)"}},{ws(15)+i*0.08:.3f});')
A(f'tl.to(".pols, .s3-head, #s3_q",{{opacity:0,scale:1.12,filter:"blur(14px)",duration:0.3,ease:"power2.in"}},{T_TESTI-0.32:.3f});')
A(f'tl.to("#{s3} .ink-bg",{{opacity:0,duration:0.3}},{T_TESTI+0.1:.3f});')

# ===================== S4 TESTIMONIAL OVERLAYS =====================
lt = clip(T_TESTI + 0.35, ws(33) + 0.4, '''<div class="lt" id="lt"><i class="dot"></i><div><div class="lt-a">TESTIMONI PELANGGAN</div><div class="lt-b serif-i">Real customer · real review</div></div></div>''', z=20)
A(f'tl.fromTo("#lt",{{x:-420,opacity:0}},{{x:0,opacity:1,duration:0.5,ease:"expo.out"}},{T_TESTI+0.35:.3f});')
A(f'tl.to("#lt",{{x:-420,opacity:0,duration:0.3,ease:"power2.in"}},{ws(33)+0.1:.3f});')
feather = '<svg viewBox="0 0 64 64" class="ico"><path class="draw" d="M52 8C30 10 16 26 14 50M52 8c-2 14-10 26-26 30M44 12c-4 10-10 16-20 18M14 50l-6 6"/></svg>'
scent = '<svg viewBox="0 0 64 64" class="ico"><path class="draw" d="M20 54c-6-8 6-14 0-22s6-14 0-22M32 54c-6-8 6-14 0-22s6-14 0-22M44 54c-6-8 6-14 0-22s6-14 0-22"/></svg>'
co = clip(ws(34) - 0.05, ws(36) + 0.35, f'''
<div class="callout" id="co1">{feather}<div><div class="co-t serif-i">Lembut</div><div class="co-s">Buih mousse halus · gentle foaming</div></div></div>
<div class="callout" id="co2">{scent}<div><div class="co-t serif-i">Wangi</div><div class="co-s">Aromatherapy · rose fragrance</div></div></div>''', cls="layer", z=20)
A(f'tl.fromTo("#co1",{{x:520,opacity:0}},{{x:0,opacity:1,duration:0.45,ease:"expo.out"}},{ws(34)-0.05:.3f});')
A(f'tl.fromTo("#co1 .draw",{{strokeDashoffset:200}},{{strokeDashoffset:0,duration:0.7,ease:"power2.out"}},{ws(34):.3f});')
A(f'tl.fromTo("#co2",{{x:520,opacity:0}},{{x:0,opacity:1,duration:0.45,ease:"expo.out"}},{ws(35)-0.05:.3f});')
A(f'tl.fromTo("#co2 .draw",{{strokeDashoffset:200}},{{strokeDashoffset:0,duration:0.7,ease:"power2.out"}},{ws(35):.3f});')
A(f'tl.to("#co1, #co2",{{x:520,opacity:0,duration:0.3,stagger:0.06,ease:"power2.in"}},{ws(36):.3f});')
ring_txt = "TAK TIPU • 100% JUJUR • REAL REVIEW • "
stamp = clip(ws(42) - 0.04, ws(47), f'''<div class="stamp" id="stp"><svg viewBox="0 0 200 200"><defs><path id="cpath" d="M100,100 m-78,0 a78,78 0 1,1 156,0 a78,78 0 1,1 -156,0"/></defs>
<text><textPath href="#cpath" startOffset="0">{ring_txt}</textPath></text></svg><div class="stamp-c serif-i">100%<small>jujur</small></div></div>''', z=21)
A(f'tl.fromTo("#stp",{{scale:2.6,opacity:0,rotation:-30}},{{scale:1,opacity:1,rotation:-8,duration:0.28,ease:"power4.in"}},{ws(42)-0.04:.3f});')
A(f'tl.to("#stp svg",{{rotation:120,duration:{ws(47)-ws(42):.3f},ease:"none"}},{ws(42):.3f});')
A(f'tl.to("#stp",{{scale:0.4,opacity:0,duration:0.22,ease:"power2.in"}},{ws(47)-0.22:.3f});')
chk = '<svg viewBox="0 0 24 24" class="ck"><path d="M5 12.5l4.2 4.2L19 7"/></svg>'
cl = clip(ws(49) - 0.1, CUT1 + 0.02, f'''<div class="checklist" id="ckl"><div class="ck-h">KENAPA ORANG SUKA</div>
<div class="ck-i" id="ci0">{chk}<span>Lembut di kulit</span></div><div class="ck-i" id="ci1">{chk}<span>Wangi tahan lama</span></div><div class="ck-i" id="ci2">{chk}<span class="serif-i">Menyegarkan</span></div></div>''', z=20)
A(f'tl.fromTo("#ckl",{{y:-60,opacity:0}},{{y:0,opacity:1,duration:0.4,ease:"expo.out"}},{ws(49)-0.1:.3f});')
for i, wi in enumerate((51, 52, 54)):
    A(f'tl.fromTo("#ci{i}",{{x:-40,opacity:0.0}},{{x:0,opacity:1,duration:0.3,ease:"power3.out"}},{ws(wi)-0.05:.3f});')
    A(f'tl.fromTo("#ci{i} .ck path",{{strokeDashoffset:30}},{{strokeDashoffset:0,duration:0.3}},{ws(wi):.3f});')
edu = clip(CUT1, CUT_END, f'''<div class="edu"><div class="label-top gold2" id="ed_l">03 &nbsp;—&nbsp; RAHSIA FORMULA</div>
<div class="edu-t" id="ed_t">Rahsia di sebalik<br/><span class="serif-i blush">keharuman</span></div>
<div class="chips"><span class="chip" id="ch0">Aromatherapy</span><span class="chip" id="ch1">Ocean Salt</span><span class="chip" id="ch2">Gentle Foaming</span></div></div>''', cls="layer", z=19)
A(f'tl.fromTo("#ed_l",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.3}},{CUT1:.3f});')
A(f'tl.fromTo("#ed_t",{{opacity:0,y:50,filter:"blur(12px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.45,ease:"expo.out"}},{CUT1+0.05:.3f});')
for i in range(3):
    A(f'tl.fromTo("#ch{i}",{{opacity:0,y:30,scale:0.8}},{{opacity:1,y:0,scale:1,duration:0.35,ease:"back.out(2.4)"}},{CUT2-0.25+i*0.18:.3f});')
fresh = clip(ws(61) - 0.06, T_TESTI_END + 0.1, '''<div class="fresh serif-i" id="fr">fresh.</div><div class="ripples"><i id="rp0"></i><i id="rp1"></i><i id="rp2"></i></div>''', cls="layer", z=19)
A(f'tl.fromTo("#fr",{{scale:0.4,opacity:0}},{{scale:1,opacity:1,duration:0.4,ease:"expo.out"}},{ws(61)-0.06:.3f});')
for i in range(3):
    A(f'tl.fromTo("#rp{i}",{{scale:0.2,opacity:0.9}},{{scale:3.2,opacity:0,duration:0.9,ease:"power2.out"}},{ws(61)+i*0.12:.3f});')
# whip transition to closing
A(f'tl.to("#testi",{{x:-300,filter:"blur(24px)",duration:0.16,ease:"power3.in"}},{T_TESTI_END-0.06:.3f});')

# ===================== CLOSING =====================
yk = clip(C1, C2, f'''<div class="yk"><svg viewBox="0 0 120 120" class="ckc"><circle cx="60" cy="60" r="52"/><path d="M36 62l16 16 32-34"/></svg>
<div class="yk-a" id="yk_a"><span id="yk0">Ha,</span> <span id="yk1">dah</span> <span id="yk2">yakin,</span></div><div class="yk-b serif-i gold2" id="yk3">kan?</div></div>''', cls="layer", z=12)
A(f'tl.fromTo("#yk0",{{opacity:0,scale:1.6}},{{opacity:1,scale:1,duration:0.25,ease:"back.out(3)"}},{ws(63):.3f});')
A(f'tl.fromTo("#yk1, #yk2",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.3,stagger:0.25,ease:"expo.out"}},{ws(64):.3f});')
A(f'tl.fromTo("#yk3",{{opacity:0,scale:0.6,rotation:-6}},{{opacity:1,scale:1,rotation:0,duration:0.35,ease:"back.out(2.6)"}},{ws(66)-0.05:.3f});')
A(f'tl.fromTo(".ckc circle",{{strokeDashoffset:330}},{{strokeDashoffset:0,duration:0.5,ease:"power2.out"}},{ws(65)-0.1:.3f});')
A(f'tl.fromTo(".ckc path",{{strokeDashoffset:90}},{{strokeDashoffset:0,duration:0.3,ease:"power2.out"}},{ws(65)+0.2:.3f});')
A(f'tl.to("#{yk} .yk",{{scale:1.4,opacity:0,filter:"blur(10px)",duration:0.18,ease:"power2.in"}},{C2-0.16:.3f});')
ticks = "".join(f'<i style="transform:rotate({i*30}deg) translateY(-118px)"></i>' for i in range(12))
ck = clip(C2, C3, f'''<div class="clock" id="clk"><div class="ticks">{ticks}</div><div class="hand" id="hnd"></div><div class="hub"></div></div>
''', cls="layer", z=12)
A(f'tl.fromTo("#clk",{{scale:0,rotation:-90}},{{scale:1,rotation:0,duration:0.35,ease:"back.out(2)"}},{C2:.3f});')
A(f'tl.fromTo("#hnd",{{rotation:0}},{{rotation:720,duration:{C3-C2:.3f},ease:"power1.inOut"}},{C2:.3f});')
st_ = clip(C3, C4, f'''<div class="ivory-bg warm"></div><img class="bottle" id="bt" src="assets/img/bottle_cutout@2x.png"/><div class="shadow" id="bts"></div>
<div class="stock" id="stk"><div class="stk-h">STOK SEMASA</div><div class="bar"><i id="bar"></i></div><div class="stk-r"><span>Hampir habis</span><b id="stk_p">TERHAD</b></div></div>
<div class="pill-red" id="pr">Sangat-sangat terhad</div>''', cls="layer", z=12)
A(f'tl.fromTo("#{st_} .ivory-bg",{{clipPath:"inset(100% 0 0 0)"}},{{clipPath:"inset(0% 0 0 0)",duration:0.32,ease:"expo.out"}},{C3:.3f});')
A(f'tl.fromTo("#bt",{{y:500,rotation:12,opacity:0}},{{y:0,rotation:-4,opacity:1,duration:0.6,ease:"expo.out"}},{C3+0.05:.3f});')
A(f'tl.to("#bt",{{y:-18,rotation:-2,duration:{C4-C3-0.6:.3f},ease:"sine.inOut"}},{C3+0.65:.3f});')
A(f'tl.fromTo("#stk",{{x:400,opacity:0}},{{x:0,opacity:1,duration:0.45,ease:"expo.out"}},{C3+0.15:.3f});')
A(f'tl.fromTo("#bar",{{scaleX:1}},{{scaleX:0.12,duration:{ws(73)-C3:.3f},ease:"power2.inOut"}},{C3+0.3:.3f});')
A(f'tl.fromTo("#pr",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:0.3,ease:"back.out(3)"}},{ws(73)-0.05:.3f});')
A(f'tl.to("#pr",{{scale:1.08,duration:0.12,yoyo:true,repeat:3,ease:"sine.inOut"}},{ws(73)+0.25:.3f});')
bag_svg = '''<svg viewBox="0 0 200 220" class="bagsvg"><path d="M70 70V56a30 30 0 0 1 60 0v14" fill="none" stroke="#1a1410" stroke-width="12" stroke-linecap="round"/>
<path d="M30 70h140l-10 128a14 14 0 0 1-14 12H54a14 14 0 0 1-14-12z" fill="#FFC72C"/><path d="M30 70h140l-2 22H32z" fill="#F2B200"/>
<circle cx="72" cy="104" r="7" fill="#1a1410"/><circle cx="128" cy="104" r="7" fill="#1a1410"/></svg>'''
bag = clip(C4, C6, f'''<div class="ink-veil"></div><div class="bagwrap" id="bg">{bag_svg}<div class="badge" id="bdg">1</div></div>
<div class="tap" id="tp"><i id="tr0"></i><i id="tr1"></i></div><svg class="finger" id="fg" viewBox="0 0 64 64"><path d="M26 6a5 5 0 0 1 10 0v22l12 3c4 1 6 4 5 8l-3 15c-1 4-4 6-8 6H28c-3 0-5-1-7-4L10 40c-2-3 1-7 5-5l11 7z" fill="#fff" stroke="#1a1410" stroke-width="3"/></svg>
<div class="bag-t" id="bgt">Tekan <span class="serif-i yellow">beg kuning</span></div>
<div class="cta-btn" id="cob"><span>Checkout sekarang</span><svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></div>''', cls="layer", z=12)
A(f'tl.fromTo("#bg",{{scale:0,rotation:-20}},{{scale:1,rotation:0,duration:0.45,ease:"back.out(2.2)"}},{C4:.3f});')
A(f'tl.fromTo("#bgt",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.3}},{C4+0.05:.3f});')
A(f'tl.fromTo("#fg",{{x:260,y:300,opacity:0}},{{x:0,y:0,opacity:1,duration:0.35,ease:"power3.out"}},{ws(74)-0.25:.3f});')
A(f'tl.to("#fg",{{scale:0.86,duration:0.08,yoyo:true,repeat:1}},{ws(75):.3f});')
for i in range(2):
    A(f'tl.fromTo("#tr{i}",{{scale:0.2,opacity:0.95}},{{scale:2.6,opacity:0,duration:0.6,ease:"power2.out"}},{ws(75)+i*0.12:.3f});')
A(f'tl.to("#bg",{{scale:1.12,duration:0.1,yoyo:true,repeat:1,ease:"power2.out"}},{ws(76):.3f});')
A(f'tl.fromTo("#bdg",{{scale:0}},{{scale:1,duration:0.25,ease:"back.out(4)"}},{ws(76)+0.05:.3f});')
A(f'tl.to("#bg",{{y:-160,scale:0.78,duration:0.35,ease:"expo.inOut"}},{ws(78)-0.1:.3f});')
A(f'tl.to("#bgt",{{opacity:0,y:-30,duration:0.2}},{ws(78)-0.1:.3f});')
A(f'tl.to("#fg",{{x:30,y:330,duration:0.35,ease:"expo.inOut"}},{ws(78)-0.1:.3f});')
A(f'tl.fromTo("#cob",{{opacity:0,y:60,scale:0.9}},{{opacity:1,y:0,scale:1,duration:0.35,ease:"back.out(2)"}},{ws(78)-0.05:.3f});')
A(f'tl.to("#cob",{{scale:0.93,duration:0.08,yoyo:true,repeat:1}},{ws(80):.3f});')
A(f'tl.to("#fg",{{scale:0.86,duration:0.08,yoyo:true,repeat:1}},{ws(80):.3f});')
digits = "".join(f"<b>{d}</b>" for d in "?✦?✦?✦?✦?✦?✦??")  # no real-looking numbers: price is revealed on TikTok Shop
pr = clip(C6, E + 0.02, f'''<div class="price" id="pc"><div class="pc-h">HARGA DI TIKTOK SHOP</div><div class="pc-v"><span class="rm">RM</span>
<div class="slot"><div class="reel" id="rl0">{digits}</div></div><div class="slot"><div class="reel" id="rl1">{digits}</div></div></div>
<div class="pc-s serif-i">Tengok sendiri — harga istimewa untuk kamu</div><i class="shine" id="shn"></i></div>''', cls="layer", z=12)
A(f'tl.fromTo("#pc",{{rotationY:-90,opacity:0}},{{rotationY:0,opacity:1,duration:0.5,ease:"expo.out"}},{C6:.3f});')
A(f'tl.fromTo("#rl0",{{yPercent:0}},{{yPercent:-92.857,duration:{ws(85)-C6:.3f},ease:"power3.inOut"}},{C6+0.1:.3f});')
A(f'tl.fromTo("#rl1",{{yPercent:0}},{{yPercent:-92.857,duration:{ws(85)-C6+0.25:.3f},ease:"power3.inOut"}},{C6+0.1:.3f});')
A(f'tl.fromTo("#shn",{{xPercent:-150}},{{xPercent:350,duration:0.7,ease:"power2.inOut"}},{ws(85):.3f});')
A(f'tl.to("#pc",{{y:-14,duration:0.25,yoyo:true,repeat:1,ease:"sine.inOut"}},{ws(85):.3f});')

# ===================== END CARD =====================
endc = clip(E, TOTAL, f'''<div class="ivory-bg"><div class="glow rose"></div></div>
<div class="ec-top" id="ec_k">WOMAN GLORY &nbsp;·&nbsp; BOMBSHELL</div>
<img class="ec-bottle" id="ec_b" src="assets/img/bottle_cutout@2x.png"/><div class="ec-sh" id="ec_s"></div>
<div class="wordmark" id="ec_w"><div class="wm-a">FRESCURA</div><div class="wm-b">BODY</div></div>
<div class="ec-chips" id="ec_c"><span>Aromatherapy</span><span>Ocean Salt</span><span>Gentle Foaming</span><span>500ml</span></div>
<div class="ec-cta" id="ec_cta">{bag_svg}<span>Tekan beg kuning sekarang</span></div>''', cls="layer", z=14)
A(f'tl.fromTo("#{endc} .ivory-bg",{{clipPath:"circle(0% at 50% 60%)"}},{{clipPath:"circle(150% at 50% 60%)",duration:0.55,ease:"expo.inOut"}},{E-0.05:.3f});')
A(f'tl.fromTo("#ec_b",{{y:420,scale:0.7,opacity:0}},{{y:0,scale:1,opacity:1,duration:0.8,ease:"expo.out"}},{E+0.15:.3f});')
A(f'tl.to("#ec_b",{{y:-16,duration:1.6,ease:"sine.inOut"}},{E+0.95:.3f});')
A(f'tl.fromTo("#ec_s",{{scaleX:0.3,opacity:0}},{{scaleX:1,opacity:1,duration:0.8}},{E+0.2:.3f});')
A(f'tl.fromTo("#ec_k",{{opacity:0,scale:1.3}},{{opacity:1,scale:1,duration:0.8,ease:"expo.out"}},{E+0.25:.3f});')
A(f'tl.fromTo("#ec_w .wm-a",{{opacity:0,y:60,filter:"blur(14px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.7,ease:"expo.out"}},{E+0.35:.3f});')
A(f'tl.fromTo("#ec_w .wm-b",{{opacity:0,scale:1.4}},{{opacity:1,scale:1,duration:0.8,ease:"expo.out"}},{E+0.5:.3f});')
A(f'tl.fromTo("#ec_c span",{{opacity:0,y:24}},{{opacity:1,y:0,duration:0.35,stagger:0.08,ease:"power3.out"}},{E+0.75:.3f});')
A(f'tl.fromTo("#ec_cta",{{opacity:0,y:60,scale:0.9}},{{opacity:1,y:0,scale:1,duration:0.45,ease:"back.out(2)"}},{E+1.05:.3f});')
A(f'tl.to("#ec_cta",{{scale:1.05,duration:0.3,yoyo:true,repeat:3,ease:"sine.inOut"}},{E+1.6:.3f});')

# ===================== CAPTIONS =====================
# (display word, source word index, accent)   — wording corrected from the transcript
CAPS = [
  ("dark",  [("Sebelum",8), ("korang",9), ("buat",10), ("keputusan,",11,1)]),
  ("light", [("Apa",18), ("pengalaman",19,1), ("yang",20), ("kau",21), ("rasa",22)]),
  ("light", [("daripada",24), ("tester",25), ("yang",26), ("kami",27), ("bagi",28), ("tu,",29)]),
  ("light", [("rasa",30), ("apa",31), ("tu?",32)]),
  ("light", [("Rasa",33), ("lembut,",34,1), ("wangi.",35,1)]),
  ("light", [("Memang",36), ("lembut",37), ("dan",38), ("wangi",39), ("lah,",40)]),
  ("light", [("tak",41), ("tipu.",42,1), ("Betul",43), ("ke",44), ("kau",45), ("ni?",46)]),
  ("light", [("Ya,",47), ("betul.",48), ("Sangat-sangat",49), ("lembut,",51,1), ("wangi",52,1)]),
  ("light", [("dan",53), ("harum",54,1), ("yang",55), ("menyegarkan",56,1)], 59),
  ("light", [("Memang",60), ("fresh",61,1), ("lah.",62)]),
  ("light", [("Jangan",67), ("tangguh",68,1), ("lagi,",69)]),
  ("dark",  [("stok",70), ("sangat-sangat",71), ("terhad!",73,1)]),
  ("light", [("tekan",74), ("beg",75), ("kuning",76,1), ("sekarang",77)]),
  ("light", [("dan",78), ("checkout",79,1), ("sekarang",81)]),
  ("light", [("tengok",82), ("berapa",83), ("harga",84), ("TikTok",85,1)]),
  ("light", [("bagi",86), ("dekat",87), ("kamu.",88)]),
]
for ci, cap in enumerate(CAPS):
    theme, words = cap[0], cap[1]; last = cap[2] if len(cap) > 2 else words[-1][1]
    t0 = ws(words[0][1]) - 0.06
    nxt = ws(CAPS[ci+1][1][0][1]) - 0.06 if ci+1 < len(CAPS) else we(last) + 0.3
    t1 = min(we(last) + 0.25, nxt) if nxt - we(last) < 0.8 else we(last) + 0.25
    spans = "".join(f'<span class="w{" acc serif-i" if len(w) > 2 else ""}" id="c{ci}w{k}">{html.escape(w[0])}</span> ' for k, w in enumerate(words))
    cid = clip(t0, t1, f'<div class="cap {theme}" id="cap{ci}">{spans}</div>', z=30)
    A(f'tl.fromTo("#cap{ci}",{{opacity:0,y:24,scale:0.96}},{{opacity:1,y:0,scale:1,duration:0.18,ease:"power3.out"}},{t0:.3f});')
    for k, w in enumerate(words):
        A(f'tl.fromTo("#c{ci}w{k}",{{opacity:0.38}},{{opacity:1,duration:0.08}},{ws(w[1])-0.02:.3f});')
        if len(w) > 2:
            A(f'tl.fromTo("#c{ci}w{k}",{{scale:0.7}},{{scale:1,duration:0.3,ease:"back.out(3)"}},{ws(w[1])-0.02:.3f});')

# scrim behind light captions over footage
for t0, t1 in ((T_TESTI + 0.3, T_TESTI_END + 0.1), (C2, C3), (C4, E)):
    clip(t0, t1, '<div class="scrim"></div>', cls="layer", z=29)
# ===================== GLOBAL: grain, vignette, audio =====================
clip(0, TOTAL, '<div class="grain" id="grain"></div><div class="vign"></div>' + ('<div class="wm">PREVIEW · FRESCURA BODY</div>' if PREVIEW else ''), cls="layer nopoint", z=50)
nsteps = int(TOTAL*12)
A(f'tl.to("#grain",{{backgroundPosition:"{nsteps*137 % 512}px {nsteps*251 % 512}px",duration:{TOTAL:.3f},ease:"steps({nsteps})"}},0);')
els.append(f'<audio id="mixaudio" class="clip" src="assets/audio/mix.wav" data-start="0" data-duration="{TOTAL:.3f}" data-volume="1"></audio>')

CSS = open(f"{P}/style.css").read()
out = f'''<!doctype html>
<html lang="ms" data-resolution="portrait">
<head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<title>Frescura Body — Testimoni</title>
<script src="assets/gsap.min.js"></script>
<link rel="stylesheet" href="assets/fonts/fonts.css"/>
<style>{CSS}</style></head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL:.3f}" data-width="1080" data-height="1920" data-fps="30">
{chr(10).join(els)}
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(anim)}
tl.set({{}}, {{}}, {TOTAL:.3f});
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body></html>'''
open(f"{P}/index.html", "w").write(out)
print("wrote index.html", "duration", TOTAL, "elements", len(els), "tweens", len(anim))
