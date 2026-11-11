# Generates the HyperFrames composition (index.html) + SFX cue list for the FRESCURA BODY awareness ad.
import json, sys, html
OUT = sys.argv[1]
VOICE_AT = 0.33          # voice clip placed at this film time
W_OFF = VOICE_AT + 0.22  # whisper word start -> film time
TOTAL = 37.2
def T(w): return round(w + W_OFF, 3)

# ---------------- captions (corrected spelling, whisper timings) ----------------
# '*' = luxury emphasis word (Bodoni italic, champagne)
PH = [
 [("Pagi",0.00),("dan",0.16),("*malam,",0.40)],
 [("mandi",0.88),("pagi",1.26),("untuk",1.62),("rasa",1.78),("*segar,",2.02)],
 [("mandi",2.54),("malam",2.90),("untuk",3.20),("rasa",3.38),("*tenang.",3.60)],
 [("*Frescura Body",4.18),("sesuai",4.88),("untuk",5.22),("kedua-duanya.",5.38)],
 [("Mengandungi",6.70),("*garam laut,",7.26)],
 [("bahan",7.78),("semula",8.16),("jadi",8.34),("yang",8.48),("kaya",8.70),("*mineral",9.06)],
 [("sudah",9.84),("lama",10.12),("digunakan",10.30),("dalam",10.68),("*penjagaan",11.00),("kulit.",11.36)],
 [("Kulit",11.74),("terasa",12.24),("lebih",12.54),("*lembut",12.68)],
 [("selepas",13.06),("mandi.",13.40)],
 [("Digabungkan",14.06),("dengan",14.74),("*parfum.",14.98)],
 [("Pagi,",15.40),("pilih",16.26)],
 [("*Woman Glory",16.70),("Bombshell",17.16),("yang",17.64),("*feminin",18.26)],
 [("dan",18.98),("*menyerlah",19.54)],
 [("untuk",20.00),("mulakan",20.26),("hari.",20.76)],
 [("Malam",21.32),("pula,",21.90)],
 [("*Noche",22.16),("Midnight Fantasy",22.40)],
 [("lebih",23.10),("*lembut",23.32),("dan",23.72),("manis",24.06)],
 [("serta",24.92),("*misteri.",25.36)],
 [("Stok",25.86),("pesanan",26.10),("ni",26.22),("sangat-sangat",26.34),("*terhad.",26.84)],
 [("Kalau",27.24),("nak",27.48),("*sepasang",27.62),("pagi",28.26),("dan",28.66),("malam,",28.70)],
 [("order",29.06),("*sekarang",29.38)],
 [("sebelum",29.60),("habis.",30.02)],
 [("Klik",30.46),("link",30.82),("di",30.94),("*bawah,",31.12)],
 [("tekan",31.46),("*beg kuning,",31.74),("check out",32.12),("*sekarang",32.52)],
 [("sebelum",32.72),("anda",33.10),("*terlambat.",33.20)],
]

css_extra = []; html_parts = []; js = []
def add(h): html_parts.append(h)
def tl(s): js.append(s)

# ---------------- scenes ----------------
S = dict(hook=(0,4.62), brand=(4.62,7.72), ocean=(7.72,12.25), soft=(12.25,14.35),
         scent=(14.35,16.75), glory=(16.75,21.80), noche=(21.80,26.38), urgent=(26.38,30.95),
         cta=(30.95,34.45), end=(34.45,TOTAL))
def scene(name, inner, cls=""):
    a,b = S[name]
    inner = inner.replace('<video class="bg-vid"', f'<video id="v-{name}" class="clip bg-vid" data-start="{a}" data-duration="{round(b-a,3)}" data-media-start="0"')
    add(f'<section id="sc-{name}" class="scene {cls}">{inner}</section>')
    tl(f'tl.set("#sc-{name}",{{visibility:"visible"}},{a}); tl.set("#sc-{name}",{{visibility:"hidden"}},{b});')

SFX = []   # (time, name, gain_db)
def sfx(t,n,g=0): SFX.append((round(t,3),n,g))

# 1 HOOK — split sky: PAGI (sunrise) / MALAM (night)
scene("hook", '''
<div class="half top"><div class="sky-day"></div><div class="sun"></div><img class="hk-img" src="assets/img/marble.jpg">
  <div class="hk-word hk-pagi">Pagi</div><div class="hk-tag hk-t1"><span class="dot"></span>SEGAR</div></div>
<div class="half bot"><div class="sky-night"></div><canvas id="cv-stars1" width="1080" height="960"></canvas><div class="moon"></div>
  <div class="hk-word hk-malam">Malam</div><div class="hk-tag hk-t2"><span class="dot"></span>TENANG</div></div>
<div class="hk-line"></div><div class="hk-amp">&amp;</div>
<div class="kicker hk-kick">1 RITUAL · 2 MOOD</div>''')
tl('''
tl.fromTo(".hk-pagi",{yPercent:110,opacity:0},{yPercent:0,opacity:1,duration:.55,ease:"expo.out"},0.02);
tl.fromTo(".hk-malam",{yPercent:-110,opacity:0},{yPercent:0,opacity:1,duration:.55,ease:"expo.out"},0.38);
tl.fromTo(".hk-line",{scaleX:0},{scaleX:1,duration:.7,ease:"expo.inOut"},0.05);
tl.fromTo(".hk-amp",{scale:0,rotation:-30,opacity:0},{scale:1,rotation:0,opacity:1,duration:.5,ease:"back.out(2)"},0.5);
tl.fromTo(".hk-kick",{opacity:0,y:-30,scaleX:1.5},{opacity:1,y:0,scaleX:1,duration:.8,ease:"power3.out"},0.2);
tl.fromTo(".sun",{y:260},{y:0,duration:4.4,ease:"power2.out"},0);
tl.fromTo(".moon",{y:-120,opacity:0},{y:0,opacity:1,duration:3.6,ease:"power2.out"},0.4);
tl.fromTo(".hk-img",{scale:1.25,opacity:0},{scale:1.08,opacity:.38,duration:4.6,ease:"none"},0);
tl.fromTo(".hk-t1",{opacity:0,x:-60},{opacity:1,x:0,duration:.45,ease:"expo.out"},%s);
tl.fromTo(".hk-t2",{opacity:0,x:60},{opacity:1,x:0,duration:.45,ease:"expo.out"},%s);
tl.to(".top",{yPercent:-100,duration:.45,ease:"expo.in"},4.17);
tl.to(".bot",{yPercent:100,duration:.45,ease:"expo.in"},4.17);
tl.to(".hk-line,.hk-amp,.hk-kick",{opacity:0,duration:.25},4.17);
''' % (T(2.02), T(3.60)))
sfx(0.0,"impact",0); sfx(0.02,"whoosh",-4); sfx(0.38,"whoosh2",-6); sfx(0.5,"tink",-6)
sfx(T(2.02),"pop",-5); sfx(T(3.60),"pop",-5); sfx(4.12,"whoosh",-4)

# 2 BRAND — both bottles, circle mask reveal + logo tracking
scene("brand", '''
<div class="mask-wrap"><img class="br-img" src="assets/img/marble.jpg"></div>
<div class="br-vign"></div>
<div class="logo br-logo"><div class="lg-1">FRESCURA</div><div class="lg-rule"></div><div class="lg-2">B O D Y</div></div>
<div class="stamp br-stamp"><div>2 IN 1</div><small>RITUAL MANDI</small></div>''')
a=S["brand"][0]
tl(f'''
tl.fromTo("#sc-brand .mask-wrap",{{clipPath:"circle(0% at 50% 48%)"}},{{clipPath:"circle(80% at 50% 48%)",duration:.9,ease:"expo.out"}},{a});
tl.fromTo(".br-img",{{scale:1.35}},{{scale:1.05,duration:3.2,ease:"power2.out"}},{a});
tl.fromTo(".lg-1",{{scaleX:1.5,opacity:0,filter:"blur(14px)"}},{{scaleX:1,opacity:1,filter:"blur(0px)",duration:1.1,ease:"expo.out"}},{a+0.15});
tl.fromTo(".lg-rule",{{scaleX:0}},{{scaleX:1,duration:.8,ease:"expo.inOut"}},{a+0.45});
tl.fromTo(".lg-2",{{opacity:0,y:16}},{{opacity:1,y:0,duration:.6,ease:"power3.out"}},{a+0.6});
tl.fromTo(".br-stamp",{{scale:2.2,opacity:0,rotation:-14}},{{scale:1,opacity:1,rotation:-8,duration:.45,ease:"back.out(1.7)"}},{T(5.38)});
tl.to("#sc-brand .mask-wrap",{{clipPath:"inset(0% 0% 100% 0%)",duration:.45,ease:"expo.in"}},{S["brand"][1]-0.45});
tl.to(".br-logo,.br-stamp",{{opacity:0,y:-60,duration:.35,ease:"power2.in"}},{S["brand"][1]-0.42});
''')
sfx(a,"shimmer",-6); sfx(a+0.15,"riser_short",-8); sfx(T(5.38),"stamp",-3); sfx(S["brand"][1]-0.45,"whoosh2",-5)

# 3 OCEAN SALT — educational: procedural ocean + 3D salt crystals + mineral tiles
cubes="".join(f'<div class="cube c{i}"><i></i><i></i><i></i><i></i><i></i><i></i></div>' for i in range(5))
scene("ocean", f'''
<canvas id="cv-ocean" width="1080" height="1920"></canvas>
<div class="cubes">{cubes}</div>
<div class="edu-head"><div class="kicker">BAHAN UTAMA</div><div class="edu-title">Garam <em>Laut</em></div><div class="edu-sub">OCEAN SALT · SEMULA JADI</div></div>
<div class="tiles">
 <div class="tile t1"><b>Mg</b><span>Magnesium</span></div>
 <div class="tile t2"><b>Ca</b><span>Kalsium</span></div>
 <div class="tile t3"><b>K</b><span>Kalium</span></div>
</div>
<div class="edu-fact"><span class="fact-line"></span>Rahsia spa &amp; penjagaan kulit sejak dahulu</div>''')
a,b=S["ocean"]
tl(f'''
tl.fromTo("#sc-ocean",{{clipPath:"inset(100% 0% 0% 0%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:.55,ease:"expo.out"}},{a});
tl.fromTo(".edu-head .kicker",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.5}},{a+0.15});
tl.fromTo(".edu-title",{{opacity:0,y:80,filter:"blur(12px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.7,ease:"expo.out"}},{T(7.26)-0.1});
tl.fromTo(".edu-sub",{{opacity:0,scaleX:1.5}},{{opacity:1,scaleX:1,duration:.8,ease:"power3.out"}},{T(7.78)});
tl.fromTo(".cube",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:.6,stagger:.12,ease:"back.out(1.6)"}},{a+0.3});
tl.fromTo(".cube",{{rotationX:-20,rotationY:0}},{{rotationX:340,rotationY:400,duration:{b-a},ease:"none"}},{a});
tl.fromTo(".cubes",{{y:60}},{{y:-80,duration:{b-a},ease:"none"}},{a});
tl.fromTo(".tile",{{opacity:0,y:90,rotationX:-70}},{{opacity:1,y:0,rotationX:0,duration:.6,stagger:.16,ease:"expo.out"}},{T(9.06)-0.15});
tl.fromTo(".edu-fact",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.5,ease:"power3.out"}},{T(10.30)});
tl.fromTo(".fact-line",{{scaleX:0}},{{scaleX:1,duration:.6,ease:"expo.out"}},{T(10.30)});
tl.to("#sc-ocean",{{opacity:0,scale:1.08,filter:"blur(18px)",duration:.4,ease:"power2.in"}},{b-0.4});
''')
sfx(a,"whoosh",-4); sfx(a+0.05,"wave",-5); sfx(T(7.26)-0.1,"impact_soft",-4)
for i in range(3): sfx(T(9.06)-0.15+i*0.16,"tick",-4)
sfx(T(10.30),"shimmer",-9); sfx(b-0.4,"whoosh2",-6)

# 4 SOFT — foam in palm b-roll + softness meter + bubbles
scene("soft", '''
<video class="bg-vid" src="assets/video/foam_palm.mp4" muted playsinline></video>
<canvas id="cv-bub" width="1080" height="1920"></canvas>
<div class="meter"><div class="m-lbl">KELEMBUTAN KULIT</div><div class="m-bar"><div class="m-fill"></div></div><div class="m-val"><span id="m-num">0</span>%</div></div>
<div class="big-out so-big">lembut</div>''')
a,b=S["soft"]
tl(f'''
tl.fromTo("#sc-soft",{{opacity:0,scale:1.12}},{{opacity:1,scale:1,duration:.45,ease:"power3.out"}},{a});
tl.fromTo("#sc-soft .bg-vid",{{scale:1.05}},{{scale:1.18,duration:{b-a},ease:"none"}},{a});
tl.fromTo(".so-big",{{opacity:0,y:120,scale:.8}},{{opacity:1,y:0,scale:1,duration:.7,ease:"expo.out"}},{T(12.68)-0.1});
tl.fromTo(".meter",{{opacity:0,x:-80}},{{opacity:1,x:0,duration:.5,ease:"expo.out"}},{a+0.15});
tl.fromTo(".m-fill",{{scaleX:0}},{{scaleX:.96,duration:1.4,ease:"power3.out"}},{T(12.54)});
tl.fromTo("#m-num",{{innerText:0}},{{innerText:96,duration:1.4,ease:"power3.out",snap:{{innerText:1}}}},{T(12.54)});
tl.to("#sc-soft",{{xPercent:-100,duration:.4,ease:"expo.in"}},{b-0.4});
''')
sfx(a,"bubbles",-4); sfx(T(12.54),"riser_short",-9); sfx(T(12.68)-0.1,"impact_soft",-5); sfx(T(13.95),"ding",-8); sfx(b-0.4,"whoosh",-5)

# 5 SCENT — parfum: pump close-up + scent waves + sparkles
scene("scent", '''
<video class="bg-vid" src="assets/video/pump_close.mp4" muted playsinline></video>
<div class="tint rose"></div>
<canvas id="cv-spark" width="1080" height="1920"></canvas>
<svg class="waves" viewBox="0 0 1080 600"><path class="wv w1" d="M-40 300 C 180 160, 360 440, 560 300 S 940 160, 1120 300"/><path class="wv w2" d="M-40 360 C 200 220, 380 500, 580 360 S 960 220, 1120 360"/><path class="wv w3" d="M-40 240 C 160 100, 340 380, 540 240 S 920 100, 1120 240"/></svg>
<div class="pill-row"><div class="pill p1">AROMATERAPI</div><div class="plus">+</div><div class="pill p2">PARFUM</div></div>''')
a,b=S["scent"]
tl(f'''
tl.fromTo("#sc-scent",{{xPercent:100}},{{xPercent:0,duration:.45,ease:"expo.out"}},{a});
tl.fromTo("#sc-scent .bg-vid",{{scale:1.15}},{{scale:1.02,duration:{b-a},ease:"none"}},{a});
tl.fromTo(".wv",{{strokeDashoffset:1400}},{{strokeDashoffset:0,duration:1.6,stagger:.18,ease:"power2.out"}},{a+0.2});
tl.fromTo(".waves",{{x:-40}},{{x:40,duration:{b-a},ease:"sine.inOut"}},{a});
tl.fromTo(".p1",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.5,ease:"expo.out"}},{a+0.25});
tl.fromTo(".plus",{{opacity:0,scale:0,rotation:-90}},{{opacity:1,scale:1,rotation:0,duration:.45,ease:"back.out(2)"}},{T(14.74)});
tl.fromTo(".p2",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.5,ease:"expo.out"}},{T(14.98)});
tl.to("#sc-scent",{{clipPath:"circle(0% at 50% 50%)",duration:.4,ease:"expo.in"}},{b-0.4});
''')
sfx(a,"whoosh2",-4); sfx(a+0.2,"shimmer",-7); sfx(T(14.74),"tick",-4); sfx(T(14.98),"sparkle",-4); sfx(b-0.4,"whoosh",-5)

# 6 GLORY — PAGI: Woman Glory bombshell
scene("glory", '''
<video class="bg-vid" src="assets/video/pump_table.mp4" muted playsinline></video>
<div class="tint warm"></div>
<div class="time-chip tc-day"><span class="ico sun-ico"></span>PAGI · 07:00</div>
<div class="pcard gl-card"><div class="pc-img"><img src="assets/img/flatlay.jpg" style="left:0px;top:-230px"></div>
  <div class="pc-txt"><div class="pc-k">AROMA PAGI</div><div class="pc-n">Woman <em>Glory</em></div><div class="pc-s">BOMBSHELL</div></div></div>
<div class="notes gl-notes"><div class="note n1">Feminin</div><div class="note n2">Menyerlah</div><div class="note n3">Bertenaga</div></div>''')
a,b=S["glory"]
tl(f'''
tl.fromTo("#sc-glory",{{clipPath:"circle(0% at 50% 50%)"}},{{clipPath:"circle(85% at 50% 50%)",duration:.6,ease:"expo.out"}},{a});
tl.fromTo("#sc-glory .bg-vid",{{scale:1.0}},{{scale:1.12,duration:{b-a},ease:"none"}},{a});
tl.fromTo(".tc-day",{{opacity:0,y:-40}},{{opacity:1,y:0,duration:.5,ease:"expo.out"}},{T(15.40)});
tl.fromTo(".gl-card",{{opacity:0,x:520,rotation:6}},{{opacity:1,x:0,rotation:-2,duration:.75,ease:"expo.out"}},{T(16.70)-0.12});
tl.fromTo(".gl-card .pc-img img",{{scale:1.4}},{{scale:1.15,duration:4,ease:"power2.out"}},{T(16.70)-0.12});
tl.fromTo(".gl-notes .n1",{{opacity:0,scale:.6,y:30}},{{opacity:1,scale:1,y:0,duration:.45,ease:"back.out(2)"}},{T(18.26)});
tl.fromTo(".gl-notes .n2",{{opacity:0,scale:.6,y:30}},{{opacity:1,scale:1,y:0,duration:.45,ease:"back.out(2)"}},{T(19.54)});
tl.fromTo(".gl-notes .n3",{{opacity:0,scale:.6,y:30}},{{opacity:1,scale:1,y:0,duration:.45,ease:"back.out(2)"}},{T(20.26)});
tl.to("#sc-glory",{{yPercent:-100,duration:.45,ease:"expo.in"}},{b-0.45});
''')
sfx(a,"whoosh",-4); sfx(T(15.40),"tink",-5); sfx(T(16.70)-0.12,"swoosh_card",-3)
for t in (18.26,19.54,20.26): sfx(T(t),"pop",-4)
sfx(b-0.45,"whoosh2",-4)

# 7 NOCHE — MALAM: Noche midnight fantasy
scene("noche", '''
<div class="sky-night full"></div><canvas id="cv-stars2" width="1080" height="1920"></canvas>
<img class="nc-bg" src="assets/img/flatlay.jpg">
<div class="time-chip tc-night"><span class="ico moon-ico"></span>MALAM · 22:00</div>
<div class="pcard nc-card"><div class="pc-img"><img src="assets/img/flatlay.jpg" style="left:-526px;top:-1150px"></div>
  <div class="pc-txt"><div class="pc-k">AROMA MALAM</div><div class="pc-n"><em>Noche</em></div><div class="pc-s">MIDNIGHT FANTASY</div></div></div>
<div class="notes nc-notes"><div class="note n1">Lembut</div><div class="note n2">Manis</div><div class="note n3">Misteri</div></div>''')
a,b=S["noche"]
tl(f'''
tl.fromTo("#sc-noche",{{yPercent:100}},{{yPercent:0,duration:.5,ease:"expo.out"}},{a});
tl.fromTo(".nc-bg",{{scale:1.3,opacity:0}},{{scale:1.1,opacity:.22,duration:{b-a},ease:"none"}},{a});
tl.fromTo(".tc-night",{{opacity:0,y:-40}},{{opacity:1,y:0,duration:.5,ease:"expo.out"}},{T(21.32)});
tl.fromTo(".nc-card",{{opacity:0,x:-520,rotation:-6}},{{opacity:1,x:0,rotation:2,duration:.75,ease:"expo.out"}},{T(22.16)-0.12});
tl.fromTo(".nc-card .pc-img img",{{scale:1.4}},{{scale:1.15,duration:4,ease:"power2.out"}},{T(22.16)-0.12});
tl.fromTo(".nc-notes .n1",{{opacity:0,scale:.6,y:30}},{{opacity:1,scale:1,y:0,duration:.45,ease:"back.out(2)"}},{T(23.32)});
tl.fromTo(".nc-notes .n2",{{opacity:0,scale:.6,y:30}},{{opacity:1,scale:1,y:0,duration:.45,ease:"back.out(2)"}},{T(24.06)});
tl.fromTo(".nc-notes .n3",{{opacity:0,scale:.6,y:30}},{{opacity:1,scale:1,y:0,duration:.45,ease:"back.out(2)"}},{T(25.36)});
tl.to("#sc-noche",{{opacity:0,filter:"blur(20px)",scale:1.1,duration:.4,ease:"power2.in"}},{b-0.4});
''')
sfx(a,"whoosh",-4); sfx(a+0.1,"night",-6); sfx(T(21.32),"tink",-5); sfx(T(22.16)-0.12,"swoosh_card",-3)
for t in (23.32,24.06,25.36): sfx(T(t),"pop",-4)
sfx(b-0.4,"whoosh2",-5)

# 8 URGENT — stok terhad + set pagi & malam
scene("urgent", '''
<img class="ur-bg" src="assets/img/flatlay.jpg"><div class="ur-shade"></div>
<div class="ur-badge"><span class="live"></span>STOK TERHAD</div>
<div class="stock"><div class="st-top"><span>BAKI STOK</span><span><b id="st-num">100</b>%</span></div><div class="st-bar"><div class="st-fill"></div></div></div>
<div class="duo"><div class="orb o-day"><span class="ico sun-ico"></span><small>PAGI</small></div><div class="duo-plus">+</div><div class="orb o-night"><span class="ico moon-ico"></span><small>MALAM</small></div></div>
<div class="duo-lbl">SET <em>Sepasang</em></div>
<div class="order-btn">ORDER SEKARANG</div>''')
a,b=S["urgent"]
tl(f'''
tl.fromTo("#sc-urgent",{{opacity:0,scale:.9}},{{opacity:1,scale:1,duration:.45,ease:"expo.out"}},{a});
tl.fromTo(".ur-bg",{{scale:1.2,rotation:-3}},{{scale:1.05,rotation:0,duration:{b-a},ease:"none"}},{a});
tl.fromTo(".ur-badge",{{opacity:0,scale:1.8}},{{opacity:1,scale:1,duration:.4,ease:"back.out(2)"}},{T(25.86)});
tl.fromTo(".stock",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.45,ease:"expo.out"}},{T(26.10)});
tl.fromTo(".st-fill",{{scaleX:1}},{{scaleX:.12,duration:1.3,ease:"power3.inOut"}},{T(26.34)});
tl.fromTo("#st-num",{{innerText:100}},{{innerText:12,duration:1.3,ease:"power3.inOut",snap:{{innerText:1}}}},{T(26.34)});
tl.fromTo(".live",{{scale:1}},{{scale:1.6,opacity:.4,duration:.5,repeat:8,yoyo:true,ease:"sine.inOut"}},{T(25.86)});
tl.fromTo(".o-day",{{opacity:0,x:-200}},{{opacity:1,x:0,duration:.55,ease:"expo.out"}},{T(27.62)});
tl.fromTo(".o-night",{{opacity:0,x:200}},{{opacity:1,x:0,duration:.55,ease:"expo.out"}},{T(27.62)+0.1});
tl.fromTo(".duo-plus",{{opacity:0,scale:0}},{{opacity:1,scale:1,duration:.4,ease:"back.out(2)"}},{T(28.66)});
tl.fromTo(".duo-lbl",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.5,ease:"expo.out"}},{T(28.26)});
tl.fromTo(".order-btn",{{opacity:0,y:60,scale:.9}},{{opacity:1,y:0,scale:1,duration:.5,ease:"back.out(1.8)"}},{T(29.06)});
tl.to(".order-btn",{{scale:1.06,duration:.25,repeat:3,yoyo:true,ease:"sine.inOut"}},{T(29.6)});
tl.to("#sc-urgent",{{clipPath:"inset(0% 0% 0% 100%)",duration:.4,ease:"expo.in"}},{b-0.4});
''')
sfx(a,"impact",-5); sfx(T(25.86),"alarm",-8); sfx(T(26.34),"drain",-6); sfx(T(27.62),"whoosh2",-7)
sfx(T(28.66),"tink",-5); sfx(T(29.06),"stamp",-4); sfx(b-0.4,"whoosh",-5)

# 9 CTA — lather b-roll, yellow basket, arrow, checkout tap
scene("cta", '''
<video class="bg-vid" src="assets/video/lather.mp4" muted playsinline></video>
<div class="cta-shade"></div>
<div class="cta-arrow"><i></i><i></i><i></i></div>
<div class="cta-lbl">LINK DI BAWAH</div>
<div class="basket"><svg viewBox="0 0 120 120"><path d="M20 44 H100 L90 98 Q88 106 80 106 H40 Q32 106 30 98 Z" fill="#F7C531"/><path d="M40 44 Q40 16 60 16 Q80 16 80 44" fill="none" stroke="#F7C531" stroke-width="9" stroke-linecap="round"/><path d="M48 62 V88 M60 62 V88 M72 62 V88" stroke="#1b1414" stroke-width="6" stroke-linecap="round" opacity=".55"/></svg><span class="bk-badge">1</span></div>
<div class="checkout"><span>CHECK OUT</span><span class="arr">→</span></div>
<div class="tap"></div>''')
a,b=S["cta"]
tl(f'''
tl.fromTo("#sc-cta",{{xPercent:-100}},{{xPercent:0,duration:.45,ease:"expo.out"}},{a});
tl.fromTo("#sc-cta .bg-vid",{{scale:1.1}},{{scale:1.25,duration:{b-a},ease:"none"}},{a});
tl.fromTo(".cta-lbl",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:.45,ease:"expo.out"}},{T(30.82)});
tl.fromTo(".cta-arrow i",{{opacity:0,y:-40}},{{opacity:1,y:0,duration:.35,stagger:.1,ease:"power3.out"}},{T(30.82)});
tl.to(".cta-arrow",{{y:30,duration:.35,repeat:7,yoyo:true,ease:"sine.inOut"}},{T(31.2)});
tl.fromTo(".basket",{{opacity:0,scale:0,rotation:-25}},{{opacity:1,scale:1,rotation:0,duration:.55,ease:"back.out(2.2)"}},{T(31.74)-0.08});
tl.fromTo(".bk-badge",{{scale:0}},{{scale:1,duration:.35,ease:"back.out(3)"}},{T(31.74)+0.3});
tl.fromTo(".checkout",{{opacity:0,y:60}},{{opacity:1,y:0,duration:.45,ease:"expo.out"}},{T(32.12)-0.1});
tl.fromTo(".tap",{{opacity:0,scale:.3}},{{opacity:.9,scale:1,duration:.18,ease:"power2.out"}},{T(32.52)});
tl.to(".tap",{{opacity:0,scale:2.2,duration:.45,ease:"power2.out"}},{T(32.52)+0.18});
tl.to(".checkout",{{scale:.92,duration:.1,yoyo:true,repeat:1}},{T(32.52)});
tl.to("#sc-cta",{{opacity:0,duration:.35}},{b-0.35});
''')
sfx(a,"whoosh2",-4); sfx(T(30.82),"tick",-5); sfx(T(31.74)-0.08,"bounce",-3); sfx(T(31.74)+0.3,"ding",-6)
sfx(T(32.52),"click",-2); sfx(T(32.6),"cash",-6)

# 10 END CARD
scene("end", '''
<div class="end-bg"></div>
<div class="arch"><img src="assets/img/plinth.jpg"></div>
<div class="logo end-logo"><div class="lg-1">FRESCURA</div><div class="lg-rule"></div><div class="lg-2">B O D Y</div></div>
<div class="end-tag">Segar di pagi hari · <em>Tenang</em> di malam hari</div>''', "light")
a,b=S["end"]
tl(f'''
tl.fromTo("#sc-end",{{opacity:0}},{{opacity:1,duration:.4}},{a});
tl.fromTo(".arch",{{clipPath:"inset(100% 0% 0% 0% round 300px 300px 0 0)"}},{{clipPath:"inset(0% 0% 0% 0% round 300px 300px 0 0)",duration:.9,ease:"expo.out"}},{a+0.05});
tl.fromTo(".arch img",{{scale:1.3}},{{scale:1.08,duration:2,ease:"power2.out"}},{a});
tl.fromTo(".end-logo .lg-1",{{scaleX:1.5,opacity:0}},{{scaleX:1,opacity:1,duration:1,ease:"expo.out"}},{a+0.3});
tl.fromTo(".end-logo .lg-rule",{{scaleX:0}},{{scaleX:1,duration:.8,ease:"expo.inOut"}},{a+0.5});
tl.fromTo(".end-logo .lg-2",{{opacity:0}},{{opacity:1,duration:.5}},{a+0.7});
tl.fromTo(".end-tag",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.6}},{a+0.8});
''')
sfx(a,"impact_soft",-4); sfx(a+0.3,"shimmer",-5); sfx(a+0.05,"riser_short",-12)

# ---------------- captions ----------------
cap_html=[]
for i,ph in enumerate(PH):
    st=T(ph[0][1])-0.06
    en=T(PH[i+1][0][1])-0.06 if i+1<len(PH) else T(33.20)+1.0
    en=min(en, st+3.2, S['end'][0])
    words=[]
    for j,(w,t) in enumerate(ph):
        em=w.startswith("*"); w=w.lstrip("*")
        words.append(f'<span class="w{" em" if em else ""}" id="w{i}_{j}">{html.escape(w)}</span>')
        tl(f'tl.fromTo("#w{i}_{j}",{{opacity:0,y:34,filter:"blur(10px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.28,ease:"power3.out"}},{T(t)-0.04});')
        if em: tl(f'tl.fromTo("#w{i}_{j}",{{scale:1.25}},{{scale:1,duration:.45,ease:"back.out(2)"}},{T(t)-0.04});')
    cap_html.append(f'<div id="cap{i}" class="clip cap" data-start="{round(st,3)}" data-duration="{round(en-st,3)}" data-track-index="5">{" ".join(words)}</div>')
    tl(f'tl.to("#cap{i}",{{}},0);')
add("\n".join(cap_html))

# progress line + grain + frame corners (persistent)
add(f'<div id="ovl" class="clip overlay" data-start="0" data-duration="{TOTAL}" data-track-index="9"><div class="corner c-tl"></div><div class="corner c-tr"></div><div class="corner c-bl"></div><div class="corner c-br"></div><div class="prog"><div class="prog-fill"></div></div><div class="grain"></div></div>')
tl(f'tl.fromTo(".prog-fill",{{scaleX:0}},{{scaleX:1,duration:{TOTAL},ease:"none"}},0);')
tl(f'tl.fromTo(".grain",{{backgroundPosition:"0px 0px"}},{{backgroundPosition:"0px 2400px",duration:{TOTAL},ease:"steps(500)"}},0);')

# audio (pre-mixed voice + music + sfx)
add(f'<audio class="clip" id="mix" src="assets/audio/mix.wav" data-start="0" data-duration="{TOTAL}" data-volume="1" data-track-index="10"></audio>')

# ---------------- canvas procedural b-roll ----------------
CANVAS_JS = r'''
function rng(seed){return function(){seed|=0;seed=seed+0x6D2B79F5|0;let t=Math.imul(seed^seed>>>15,1|seed);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;}}
function makeStars(n,seed,w,h){const r=rng(seed);return Array.from({length:n},()=>({x:r()*w,y:r()*h,s:r()*2.2+.4,p:r()*6.28,f:r()*2+.5}));}
const ST1=makeStars(160,7,1080,960), ST2=makeStars(260,11,1080,1920);
function drawStars(id,stars,t,shoot){const c=document.getElementById(id);if(!c)return;const g=c.getContext('2d');g.clearRect(0,0,c.width,c.height);
 for(const s of stars){const a=.35+.65*Math.abs(Math.sin(s.p+t*s.f));g.globalAlpha=a;g.fillStyle='#fff';g.beginPath();g.arc(s.x,s.y-t*4,s.s,0,6.283);g.fill();}
 if(shoot){const k=(t%2.2)/2.2;if(k<.35){const x=200+k*1400,y=200+k*500;const gr=g.createLinearGradient(x,y,x-220,y-80);gr.addColorStop(0,'rgba(255,255,255,.95)');gr.addColorStop(1,'rgba(255,255,255,0)');g.globalAlpha=1-k/.35;g.strokeStyle=gr;g.lineWidth=3;g.beginPath();g.moveTo(x,y);g.lineTo(x-220,y-80);g.stroke();}}
 g.globalAlpha=1;}
function drawOcean(t){const c=document.getElementById('cv-ocean');if(!c)return;const g=c.getContext('2d');
 const bg=g.createLinearGradient(0,0,0,1920);bg.addColorStop(0,'#0c2a33');bg.addColorStop(.55,'#123e48');bg.addColorStop(1,'#071a20');g.fillStyle=bg;g.fillRect(0,0,1080,1920);
 // caustic light
 for(let i=0;i<7;i++){const x=540+Math.sin(t*.6+i*1.7)*420;const gr=g.createRadialGradient(x,300+i*30,0,x,300+i*30,520);gr.addColorStop(0,'rgba(201,164,106,.10)');gr.addColorStop(1,'rgba(201,164,106,0)');g.fillStyle=gr;g.fillRect(0,0,1080,1920);}
 // layered wave lines
 for(let L=0;L<26;L++){const y0=980+L*36;g.beginPath();for(let x=-20;x<=1100;x+=12){const y=y0+Math.sin(x*.006+t*1.3+L*.5)*(18+L*1.2)+Math.sin(x*.017-t*2+L)*6;x<0?g.moveTo(x,y):g.lineTo(x,y);}
  g.strokeStyle=`rgba(244,238,230,${.05+L*.012})`;g.lineWidth=1.4;g.stroke();}
 // salt sparkles
 const r=rng(3);for(let i=0;i<120;i++){const x=r()*1080,y0=r()*1920,sp=20+r()*60;const y=(y0-t*sp+1920*4)%1920;const a=.25+.75*Math.abs(Math.sin(t*3+i));g.globalAlpha=a*.8;g.fillStyle='#fff';const s=1+r()*3;g.fillRect(x,y,s,s);}g.globalAlpha=1;}
function drawBubbles(t){const c=document.getElementById('cv-bub');if(!c)return;const g=c.getContext('2d');g.clearRect(0,0,1080,1920);const r=rng(21);
 for(let i=0;i<46;i++){const x=r()*1080+Math.sin(t*2+i)*18,sp=120+r()*220,rad=6+r()*26;const y=1980-((t*sp+r()*1920)%2100);
  g.beginPath();g.arc(x,y,rad,0,6.283);g.strokeStyle='rgba(255,255,255,.55)';g.lineWidth=2;g.stroke();g.beginPath();g.arc(x-rad*.35,y-rad*.35,rad*.22,0,6.283);g.fillStyle='rgba(255,255,255,.7)';g.fill();}}
function drawSpark(t){const c=document.getElementById('cv-spark');if(!c)return;const g=c.getContext('2d');g.clearRect(0,0,1080,1920);const r=rng(5);
 for(let i=0;i<70;i++){const bx=r()*1080,by=r()*1400+200,ph=r()*6.28,sz=4+r()*12;const a=Math.max(0,Math.sin(t*2.4+ph));const x=bx+Math.sin(t+ph)*30,y=by-t*30;
  g.globalAlpha=a;g.fillStyle='#F3DDB0';g.beginPath();g.moveTo(x,y-sz);g.lineTo(x+sz*.22,y-sz*.22);g.lineTo(x+sz,y);g.lineTo(x+sz*.22,y+sz*.22);g.lineTo(x,y+sz);g.lineTo(x-sz*.22,y+sz*.22);g.lineTo(x-sz,y);g.lineTo(x-sz*.22,y-sz*.22);g.closePath();g.fill();}g.globalAlpha=1;}
function canvasLane(fn,start,dur){const p={t:0};tl.fromTo(p,{t:0},{t:dur,duration:dur,ease:"none",onUpdate:()=>fn(p.t),onStart:()=>fn(p.t)},start);}
'''
lanes = f'''
canvasLane(t=>drawStars('cv-stars1',ST1,t,false),{S["hook"][0]},{S["hook"][1]-S["hook"][0]});
canvasLane(t=>drawOcean(t),{S["ocean"][0]},{S["ocean"][1]-S["ocean"][0]});
canvasLane(t=>drawBubbles(t),{S["soft"][0]},{S["soft"][1]-S["soft"][0]});
canvasLane(t=>drawSpark(t),{S["scent"][0]},{S["scent"][1]-S["scent"][0]});
canvasLane(t=>drawStars('cv-stars2',ST2,t,true),{S["noche"][0]},{S["noche"][1]-S["noche"][0]});
'''

CSS = open(sys.argv[2]).read()
doc = f'''<!doctype html>
<html lang="ms" data-resolution="portrait">
<head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<script src="assets/gsap.min.js"></script>
<style>{CSS}</style></head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{chr(10).join(html_parts)}
</div>
<script>
const tl = gsap.timeline({{paused:true}});
{CANVAS_JS}
{lanes}
{chr(10).join(j for j in js if 'tl.to("#cap' not in j)}
window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body></html>'''
open(OUT,"w").write(doc)
json.dump(dict(voice_at=VOICE_AT,total=TOTAL,sfx=SFX),open(OUT.replace("index.html","sfx_cues.json"),"w"),indent=1)
print("ok", len(SFX), "sfx cues")
