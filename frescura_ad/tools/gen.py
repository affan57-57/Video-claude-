# Generates the HyperFrames composition (index.html) for the Frescura Body ad.
import json, sys, random
P = sys.argv[1]
D = 39.6  # total film length (voice ends ~38.7)

# ---------------- words (final timeline, seconds) ----------------
W = [(0.00,"Kau"),(0.18,"perasan"),(0.36,"tak,"),(0.62,"bila"),(0.96,"stres,"),(1.68,"satu"),(1.80,"badan"),(2.10,"rasa"),
(2.44,"melekit,"),(3.26,"berpeluh"),(3.64,"dan"),(3.88,"langsung"),(4.38,"tak"),(4.58,"segar."),(5.54,"Balik"),(5.82,"kerja"),
(6.18,"pula,"),(6.62,"terus"),(6.76,"sambung"),(7.08,"urus"),(7.38,"rumah,"),(8.12,"masak"),(8.40,"dan"),(8.58,"jaga"),(8.90,"anak."),
(9.44,"Memang"),(9.86,"penat."),(10.58,"Sebab"),(10.80,"tu,"),(11.05,"jangan"),(11.42,"abaikan"),(11.82,"rutin"),(12.16,"mandi,"),
(12.80,"bersihkan"),(13.22,"badan"),(13.82,"selepas"),(14.26,"berpeluh"),(14.70,"dan"),(14.90,"tukar"),(15.30,"pakaian"),(15.74,"kepada"),
(16.08,"yang"),(16.32,"bersih."),(17.00,"Pastinya"),(17.75,"Frescura"),(18.20,"Body"),(18.42,"untuk"),(18.76,"melengkapkan"),(19.54,"rutin"),
(20.00,"mandi"),(20.50,"korang."),(21.35,"Nikmati"),(21.82,"buih"),(22.14,"lembut"),(22.64,"terus"),(22.94,"daripada"),(23.30,"botol"),
(23.62,"dengan"),(23.88,"pilihan"),(24.30,"wangian"),(24.66,"feminin."),(25.55,"Bombshell,"),(26.00,"Midnight"),(26.25,"Fantasy,"),
(26.76,"itulah"),(27.14,"pilihan"),(27.50,"yang"),(27.66,"terbaik,"),(28.30,"yang"),(28.56,"menyenangkan."),(29.45,"Girls,"),
(30.20,"jangan"),(30.52,"biarkan"),(30.88,"diri"),(31.26,"sendiri"),(31.64,"terus"),(32.06,"terabai."),(32.72,"Tukar"),(33.34,"sekarang,"),
(34.10,"pilih"),(34.24,"Bombshell"),(34.74,"ataupun"),(35.18,"Midnight"),(35.40,"Fantasy,"),(36.15,"check"),(36.38,"out"),(36.50,"terus,"),
(36.80,"stok"),(37.15,"sangat"),(37.45,"sangat"),(37.75,"terhad.")]
KEY = {"stres,","melekit,","berpeluh","segar.","penat.","mandi,","bersih.","Frescura","Body","buih","lembut","feminin.","Bombshell,",
       "Midnight","Fantasy,","terbaik,","Girls,","terabai.","sekarang,","Bombshell","check","out","terhad."}
ends = [W[i+1][0] for i in range(len(W)-1)] + [38.65]
chunks, cur = [], []
for i,(t,w) in enumerate(W):
    cur.append((t, min(ends[i], t+0.9), w))
    if w[-1] in ",." or len(cur) == 3:
        chunks.append(cur); cur = []
if cur: chunks.append(cur)

# ---------------- scenes ----------------
# (id, video, start, end, mode)
SC = [("a","s01_stress",0.00,1.65,"full"),("b","s02_sweat",1.65,3.25,"full"),("c","s03_tired",3.25,5.45,"arch"),
("d1","s04_work",5.45,6.65,"arch"),("d2","s05_laundry",6.65,8.05,"arch"),("d3","s06_cook",8.05,8.55,"full"),("d4","s07_baby",8.55,9.40,"full"),
("e","s08_penat",9.40,10.55,"arch"),("f1","s09_shower",10.55,12.75,"arch"),("f2","s10_wash",12.75,14.85,"full"),("f3","s11_clothes",14.85,16.95,"arch"),
("g","s12_mallbg",16.95,21.35,"bg"),("h","s13_pump",21.35,24.25,"full"),("i","s14_foam",24.25,25.50,"full"),
("k","s16_bath",29.40,31.40,"full"),("l","s17_mall",31.40,32.70,"arch"),("m","s18_phone",32.70,34.10,"full"),("o","s20_endbg",36.0,D,"bg")]

def vid(sid, src, s, e, mode):
    d = round(e - s, 3)
    if mode == "arch":
        return (f'<video id="v-{sid}" class="clip archvid" src="assets/v/{src}.mp4" data-start="{s}" data-duration="{d}" '
                f'data-media-start="0" muted playsinline></video>')
    return (f'<video id="v-{sid}" class="clip scene fullvid" src="assets/v/{src}.mp4" data-start="{s}" data-duration="{d}" '
            f'data-media-start="0" muted playsinline></video>')

videos = "\n".join(vid(*x) for x in SC)

# deterministic star field + bokeh
rnd = random.Random(5)
stars = ",".join(f"radial-gradient({rnd.choice([1,1.5,2,2.5])}px {rnd.choice([1,1.5,2])}px at {rnd.uniform(0,100):.1f}% {rnd.uniform(0,70):.1f}%, rgba(255,255,255,{rnd.uniform(.4,1):.2f}), transparent)" for _ in range(90))
bokeh = "".join(f'<i class="bk" style="left:{rnd.uniform(0,100):.1f}%;top:{rnd.uniform(5,95):.1f}%;width:{(s:=rnd.uniform(18,90)):.0f}px;height:{s:.0f}px;opacity:{rnd.uniform(.15,.5):.2f}"></i>' for _ in range(12))
sparks = "".join(f'<i class="sp" style="left:{rnd.uniform(5,95):.1f}%;top:{rnd.uniform(10,90):.1f}%;transform:scale({rnd.uniform(.4,1.2):.2f})"></i>' for _ in range(8))

caps = []
for ci, ch in enumerate(chunks):
    s = ch[0][0]; e = (chunks[ci+1][0][0] if ci+1 < len(chunks) else 38.9)
    e = min(e, ch[-1][1] + 0.35) if ci+1 < len(chunks) else e
    spans = "".join(f'<span class="w{" k" if w in KEY else ""}" data-t="{t}">{w}</span> ' for t,_,w in ch)
    caps.append(f'<div class="cap" data-s="{s}" data-e="{round(e,3)}">{spans.strip()}</div>')
caps = "\n".join(caps)

html = f"""<!doctype html>
<html lang="ms" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fonts.css" />
<script src="assets/gsap.min.js"></script>
<style>
:root {{ --ink:#0b0a0c; --ivory:#f6f1ea; --gold:#e3c48e; --gold2:#b8924f; --rose:#9e1027; --plum:#3a1f7a; --serif:'Bodoni Moda',serif; --sans:'Jost',sans-serif; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:1080px; height:1920px; overflow:hidden; background:var(--ink); }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; background:radial-gradient(120% 70% at 50% 30%, #2a2420 0%, #141113 55%, #0b0a0c 100%); font-family:var(--sans); color:var(--ivory); }}
.clip {{ position:absolute; }}
.scene {{ left:0; top:0; width:1080px; height:1920px; }}
.fullvid {{ object-fit:cover; z-index:1; }}
.archscene {{ z-index:1; }}
.archbg {{ position:absolute; inset:0; background:radial-gradient(120% 70% at 50% 30%, #2a2420 0%, #141113 55%, #0b0a0c 100%); }}
.arch {{ position:absolute; left:100px; top:330px; width:880px; height:1100px; border-radius:440px 440px 26px 26px; overflow:hidden;
        box-shadow:0 40px 120px rgba(0,0,0,.6), 0 0 0 1.5px rgba(227,196,142,.55); }}
.archvid {{ left:100px; top:330px; width:880px; height:1100px; object-fit:cover; z-index:1; border-radius:440px 440px 26px 26px; box-shadow:0 40px 120px rgba(0,0,0,.6), 0 0 0 1.5px rgba(227,196,142,.55); }}
.layer {{ position:absolute; inset:0; pointer-events:none; }}
.gfx {{ position:absolute; opacity:0; }}
/* typography */
.eyebrow {{ font-family:var(--sans); font-weight:500; font-size:30px; letter-spacing:.42em; text-transform:uppercase; color:var(--gold); }}
.display {{ font-family:var(--serif); font-style:italic; font-weight:500; line-height:.92; letter-spacing:-.01em; color:var(--ivory); text-shadow:0 6px 40px rgba(0,0,0,.55); }}
.caps {{ font-family:var(--sans); font-weight:600; letter-spacing:.06em; text-transform:uppercase; }}
.center {{ left:0; width:1080px; text-align:center; }}
/* overlays */
#shade {{ z-index:3; background:linear-gradient(180deg, rgba(11,10,12,.62) 0%, rgba(11,10,12,0) 26%, rgba(11,10,12,0) 58%, rgba(11,10,12,.78) 100%); }}
#vignette {{ z-index:20; background:radial-gradient(130% 90% at 50% 50%, transparent 55%, rgba(0,0,0,.55) 100%); }}
#grain {{ z-index:21; background:url(assets/img/grain.png); opacity:.07; mix-blend-mode:overlay; }}
#frame {{ z-index:19; position:absolute; inset:34px; border:1px solid rgba(227,196,142,.32); border-radius:4px; }}
#brandbar {{ z-index:19; top:74px; }}
#brandbar span {{ font-size:22px; letter-spacing:.6em; color:rgba(246,241,234,.8); font-weight:500; }}
#prog {{ z-index:19; position:absolute; left:60px; bottom:64px; height:3px; width:960px; background:rgba(255,255,255,.14); border-radius:2px; overflow:hidden; }}
#progfill {{ height:100%; width:100%; background:linear-gradient(90deg,var(--gold2),var(--gold)); transform-origin:0 50%; transform:scaleX(0); }}
#flash {{ z-index:18; background:#fff7ea; opacity:0; }}
/* captions */
#caps {{ z-index:16; }}
.cap {{ position:absolute; left:60px; width:960px; top:1520px; text-align:center; opacity:0; font-family:var(--sans); font-weight:600; font-size:74px;
        line-height:1.08; letter-spacing:-.005em; color:#fff; text-shadow:0 4px 24px rgba(0,0,0,.75), 0 1px 3px rgba(0,0,0,.6); }}
.cap .w {{ display:inline-block; opacity:.55; transform:translateY(10px); }}
.cap .w.k {{ font-family:var(--serif); font-style:italic; font-weight:600; font-size:86px; color:var(--gold); }}
/* chips, cards */
.chip {{ display:inline-flex; align-items:center; gap:16px; padding:18px 30px; border-radius:60px; background:rgba(20,17,19,.55); backdrop-filter:blur(14px);
        border:1px solid rgba(227,196,142,.45); font-family:var(--sans); font-weight:500; font-size:34px; letter-spacing:.16em; text-transform:uppercase; color:var(--ivory); }}
.chip b {{ width:12px; height:12px; border-radius:50%; background:var(--gold); box-shadow:0 0 14px var(--gold); }}
.glass {{ background:rgba(18,15,17,.55); backdrop-filter:blur(18px); border:1px solid rgba(227,196,142,.38); border-radius:28px; }}
.meter {{ width:520px; height:10px; border-radius:6px; background:rgba(255,255,255,.18); overflow:hidden; }}
.meter i {{ display:block; height:100%; width:100%; background:linear-gradient(90deg,#e3c48e,#f4e2bd); transform-origin:0 50%; }}
.todo {{ display:flex; align-items:center; gap:22px; font-size:40px; font-weight:500; letter-spacing:.02em; margin:14px 0; opacity:.35; }}
.todo .bx {{ width:40px; height:40px; border:2px solid var(--gold); border-radius:10px; position:relative; }}
.todo .bx::after {{ content:''; position:absolute; left:11px; top:3px; width:11px; height:22px; border:solid var(--gold); border-width:0 4px 4px 0; transform:rotate(45deg) scale(var(--ck,0)); }}
.todo .tx {{ position:relative; }}
.todo .tx::after {{ content:''; position:absolute; left:-4px; right:-4px; top:54%; height:3px; background:var(--gold); transform:scaleX(var(--st,0)); transform-origin:0 50%; }}
.stepnum {{ font-family:var(--serif); font-weight:400; font-size:250px; line-height:1; color:transparent; -webkit-text-stroke:2px var(--gold); }}
.bk {{ position:absolute; border-radius:50%; background:radial-gradient(circle, rgba(255,226,170,.9), rgba(255,226,170,0) 70%); }}
.sp {{ position:absolute; width:26px; height:26px; background:radial-gradient(circle, #fff 0 8%, transparent 9%), linear-gradient(90deg, transparent 46%, rgba(255,240,210,.9) 50%, transparent 54%), linear-gradient(0deg, transparent 46%, rgba(255,240,210,.9) 50%, transparent 54%); }}
/* luxury display / podium */
.podium {{ position:absolute; left:140px; width:800px; height:212px; filter:drop-shadow(0 40px 60px rgba(0,0,0,.7)); }}
.podium::before {{ content:''; position:absolute; left:0; right:0; top:75px; height:137px; border-radius:0 0 400px 400px / 0 0 75px 75px; background:linear-gradient(90deg,#6f655b,#cdbfae 45%,#e8ddd0 55%,#7c7166); }}
.podium::after {{ content:''; position:absolute; left:0; right:0; top:0; height:150px; border-radius:50%; background:radial-gradient(60% 60% at 50% 40%, #faf6f0 0%, #ddd3c6 55%, #a89c8e 100%); box-shadow:inset 0 0 0 1.5px rgba(227,196,142,.7); }}
.spot {{ position:absolute; left:140px; top:-200px; width:800px; height:1700px; background:radial-gradient(50% 60% at 50% 0%, rgba(255,236,200,.38), rgba(255,236,200,0) 70%);
        clip-path:polygon(38% 0,62% 0,100% 100%,0 100%); filter:blur(8px); }}
.bottle {{ position:absolute; filter:drop-shadow(0 30px 40px rgba(0,0,0,.55)); }}
.refl {{ position:absolute; transform:scaleY(-1); opacity:.22; -webkit-mask-image:linear-gradient(0deg, rgba(0,0,0,.9), transparent 40%); filter:blur(1px); }}
.sweep {{ position:absolute; top:0; width:220px; height:100%; background:linear-gradient(100deg, transparent, rgba(255,250,235,.55), transparent); mix-blend-mode:soft-light; }}
.btn {{ display:inline-flex; align-items:center; gap:20px; padding:30px 62px; border-radius:80px; background:linear-gradient(135deg,#f1dcb3,#c79f5c); color:#1a1410;
       font-family:var(--sans); font-weight:700; font-size:44px; letter-spacing:.2em; text-transform:uppercase; box-shadow:0 18px 60px rgba(227,196,142,.35); }}
.half {{ position:absolute; top:0; width:540px; height:1920px; overflow:hidden; }}
.logo {{ position:absolute; filter:drop-shadow(0 0 18px rgba(60,200,255,.35)); }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">

{videos}

<!-- J: variant split (motion design) -->
<div id="sc-j" class="clip scene" data-start="25.5" data-duration="3.9" style="z-index:2">
  <div class="half" id="j-left" style="left:0;background:radial-gradient(90% 60% at 50% 45%, #c0182f 0%, #6e0a18 55%, #2a050a 100%)">
    <img src="assets/img/photo1.jpg" style="position:absolute;left:-560px;top:-60px;width:1150px;opacity:.12;filter:blur(6px)" />
  </div>
  <div class="half" id="j-right" style="left:540px;background:{stars}, radial-gradient(90% 60% at 50% 45%, #5332a8 0%, #24135a 55%, #0b0620 100%)"></div>
  <div style="position:absolute;left:539px;top:0;width:2px;height:1920px;background:linear-gradient(180deg,transparent,var(--gold),transparent)" id="j-div"></div>
  <img id="j-glory" class="bottle" src="assets/img/glory.png" style="left:130px;top:330px;width:280px" />
  <img id="j-noche" class="bottle" src="assets/img/noche.png" style="left:670px;top:316px;width:286px" />
  <div id="j-n1" class="gfx" style="left:0;width:540px;top:1215px;text-align:center"><div class="eyebrow" style="font-size:24px">Woman Glory</div><div class="display" style="font-size:84px;margin-top:10px">Bombshell</div></div>
  <div id="j-n2" class="gfx" style="left:540px;width:540px;top:1215px;text-align:center"><div class="eyebrow" style="font-size:24px">Noche</div><div class="display" style="font-size:84px;margin-top:10px">Midnight<br/>Fantasy</div></div>
  <div id="j-badge" class="gfx glass" style="left:300px;top:150px;width:480px;padding:26px 0;text-align:center"><div class="eyebrow" style="font-size:24px;letter-spacing:.5em">✦ Pilihan ✦</div><div class="display" style="font-size:76px;font-style:normal;font-weight:600;letter-spacing:.06em">TERBAIK</div></div>
</div>

<!-- N: pick one -->
<div id="sc-n" class="clip scene" data-start="34.1" data-duration="1.9" style="z-index:2;background:#0b0a0c">
  <div id="n-a" class="layer" style="background:radial-gradient(80% 55% at 50% 42%, #c0182f 0%, #5c0814 60%, #1a0306 100%)">
    <img src="assets/img/glory.png" class="bottle" style="left:375px;top:250px;width:330px" id="n-ga" />
    <div class="display center" style="position:absolute;top:1270px;font-size:120px">Bombshell</div>
  </div>
  <div id="n-b" class="layer" style="opacity:0;background:{stars}, radial-gradient(80% 55% at 50% 42%, #5332a8 0%, #1f1050 60%, #08041a 100%)">
    <img src="assets/img/noche.png" class="bottle" style="left:372px;top:240px;width:336px" id="n-nb" />
    <div class="display center" style="position:absolute;top:1270px;font-size:104px">Midnight Fantasy</div>
  </div>
  <div id="n-atau" class="gfx center eyebrow" style="top:150px;font-size:34px">Pilih kegemaran anda</div>
</div>

<!-- G & O luxury mall display layers -->
<div id="g-stage" class="clip scene" data-start="16.95" data-duration="4.4" style="z-index:4">
  <div class="layer" style="background:radial-gradient(70% 45% at 50% 55%, rgba(0,0,0,0), rgba(0,0,0,.55))"></div>
  <div class="layer" id="g-bokeh">{bokeh}</div>
  <div class="spot" id="g-spot"></div>
  <div class="podium" id="g-pod" style="top:1255px"></div>
  <div id="g-bottles" style="position:absolute;left:0;top:0;width:1080px;height:1920px">
    <img class="refl" src="assets/img/noche.png" style="left:205px;top:1395px;width:300px" />
    <img class="refl" src="assets/img/glory.png" style="left:560px;top:1395px;width:296px" />
    <img class="bottle" id="g-noche" src="assets/img/noche.png" style="left:205px;top:520px;width:300px" />
    <img class="bottle" id="g-glory" src="assets/img/glory.png" style="left:560px;top:548px;width:296px" />
    <div class="sweep" id="g-sweep" style="left:-260px;height:900px;top:520px"></div>
  </div>
  <img class="logo gfx" id="g-logo" src="assets/img/logo.png" style="left:240px;top:60px;width:600px" />
  <div class="gfx center eyebrow" id="g-tag" style="top:1450px;font-size:28px">The Luxury Foam Collection</div>
  <div class="layer" id="g-sparks">{sparks}</div>
</div>

<div id="o-stage" class="clip scene" data-start="36.0" data-duration="{round(D-36.0,2)}" style="z-index:4">
  <div class="layer" style="background:radial-gradient(70% 45% at 50% 50%, rgba(0,0,0,.1), rgba(0,0,0,.6))"></div>
  <div class="spot" style="opacity:.8"></div>
  <div class="podium" style="top:1000px;transform:scale(.82)"></div>
  <img class="bottle" id="o-noche" src="assets/img/noche.png" style="left:268px;top:370px;width:260px" />
  <img class="bottle" id="o-glory" src="assets/img/glory.png" style="left:560px;top:395px;width:256px" />
  <img class="logo gfx" id="o-logo" src="assets/img/logo.png" style="left:300px;top:20px;width:480px" />
  <div class="gfx center" id="o-btn" style="top:1190px"><span class="btn">Check Out ➝</span></div>
  <div class="gfx" id="o-stock" style="left:230px;top:1360px;width:620px;text-align:center">
     <div class="caps" style="font-size:30px;letter-spacing:.38em;color:var(--gold)">Stok sangat terhad</div>
     <div class="meter" style="width:620px;margin-top:22px;height:12px"><i id="o-bar" style="background:linear-gradient(90deg,#e05a4f,#e3c48e)"></i></div>
     <div class="caps" id="o-pct" style="font-size:24px;letter-spacing:.3em;margin-top:16px;color:rgba(246,241,234,.75)">Tinggal sedikit sahaja</div>
  </div>
</div>

<div id="shade" class="layer"></div>

<!-- ======= motion graphics ======= -->
<div class="layer" style="z-index:10">
  <!-- A hook -->
  <div id="a-eye" class="gfx center eyebrow" style="top:250px">Kau perasan tak?</div>
  <div id="a-h1" class="gfx center display" style="top:330px;font-size:200px">Stres?</div>
  <div id="a-h2" class="gfx center caps" style="top:560px;font-size:58px;letter-spacing:.2em">Badan jadi <span style="font-family:var(--serif);font-style:italic;text-transform:none;letter-spacing:0;color:var(--gold);font-size:80px">melekit</span></div>
  <!-- B/C symptoms + meter -->
  <div id="b-meter" class="gfx glass" style="left:120px;top:150px;width:840px;padding:30px 40px">
     <div style="display:flex;justify-content:space-between;align-items:baseline"><span class="eyebrow" style="font-size:24px">Tahap kesegaran</span><span id="b-pct" class="caps" style="font-size:44px;color:var(--gold)">100%</span></div>
     <div class="meter" style="width:760px;margin-top:18px"><i id="b-bar"></i></div>
  </div>
  <div id="b-c1" class="gfx" style="left:110px;top:1120px"><span class="chip"><b></b>Melekit</span></div>
  <div id="b-c2" class="gfx" style="left:370px;top:1230px"><span class="chip"><b></b>Berpeluh</span></div>
  <div id="b-c3" class="gfx" style="left:250px;top:1340px"><span class="chip"><b></b>Tak segar</span></div>
  <!-- D checklist + clock -->
  <div id="d-card" class="gfx glass" style="left:110px;top:120px;width:860px;padding:34px 46px">
     <div style="display:flex;justify-content:space-between;align-items:center"><span class="eyebrow" style="font-size:24px">Lepas kerja</span>
     <span class="caps" style="font-size:46px;font-family:var(--serif);font-style:italic;text-transform:none;color:var(--gold)" id="d-clock">17:30</span></div>
     <div style="display:flex;gap:34px;margin-top:10px">
     <div class="todo" id="d-t1"><span class="bx"></span><span class="tx">Rumah</span></div>
     <div class="todo" id="d-t2"><span class="bx"></span><span class="tx">Masak</span></div>
     <div class="todo" id="d-t3"><span class="bx"></span><span class="tx">Anak</span></div></div>
  </div>
  <!-- E penat -->
  <div id="e-h" class="gfx center display" style="top:150px;font-size:118px">Memang <span style="color:var(--gold)">penat.</span></div>
  <div id="e-bat" class="gfx" style="left:440px;top:1440px;width:200px;height:84px;border:3px solid var(--ivory);border-radius:16px;padding:8px">
     <div id="e-batfill" style="height:100%;width:100%;background:var(--gold);border-radius:8px;transform-origin:0 50%"></div>
     <div style="position:absolute;right:-16px;top:24px;width:10px;height:30px;background:var(--ivory);border-radius:0 4px 4px 0"></div></div>
  <!-- F routine steps -->
  <div id="f-head" class="gfx center" style="top:120px"><div class="eyebrow" style="font-size:26px">Sebab tu — jangan abaikan</div><div class="display" style="font-size:96px;margin-top:14px">Rutin Mandi</div></div>
  <div id="f-dots" class="gfx center" style="top:1450px"></div>
  <div id="f-s1" class="gfx" style="left:90px;top:1080px"><div class="stepnum">01</div></div>
  <div id="f-s1t" class="gfx" style="left:110px;top:1340px" ><span class="chip"><b></b>Mandi setiap hari</span></div>
  <div id="f-s2" class="gfx" style="left:90px;top:300px"><div class="stepnum">02</div></div>
  <div id="f-s2t" class="gfx glass" style="left:90px;top:570px;padding:26px 36px"><div class="eyebrow" style="font-size:22px">Langkah 02</div><div class="display" style="font-size:66px;margin-top:8px">Bersihkan badan<br/>selepas berpeluh</div></div>
  <div id="f-s3" class="gfx" style="left:90px;top:1080px"><div class="stepnum">03</div></div>
  <div id="f-s3t" class="gfx" style="left:110px;top:1340px"><span class="chip"><b></b>Tukar pakaian bersih</span></div>
  <!-- G brand words -->
  <div id="g-h" class="gfx center" style="top:1530px"></div>
  <!-- H pump callouts -->
  <div id="h-h" class="gfx center" style="top:150px"><div class="eyebrow" style="font-size:26px">Terus daripada botol</div><div class="display" style="font-size:150px;margin-top:6px">Buih <span style="color:var(--gold)">Lembut</span></div></div>
  <div id="h-c1" class="gfx" style="left:600px;top:560px"><span class="chip"><b></b>Foam pump</span></div>
  <div id="h-c2" class="gfx glass" style="left:96px;top:1080px;padding:22px 30px;width:420px">
     <div class="eyebrow" style="font-size:20px">Formula</div>
     <div class="caps" style="font-size:30px;margin-top:10px;line-height:1.5;letter-spacing:.12em">Ocean Salt<br/>Aromatherapy<br/>Gentle Foaming</div></div>
  <!-- I -->
  <div id="i-h" class="gfx center" style="top:220px"><div class="eyebrow" style="font-size:26px">Pilihan wangian</div><div class="display" style="font-size:150px;margin-top:6px">Feminin</div></div>
  <!-- K / L -->
  <div id="k-h" class="gfx center display" style="top:210px;font-size:230px">Girls,</div>
  <div id="k-s" class="gfx center caps" style="top:470px;font-size:46px;letter-spacing:.28em">jangan biarkan diri</div>
  <div id="l-h" class="gfx center" style="top:130px"><div class="eyebrow" style="font-size:26px">Self-care itu wajib</div><div class="display" style="font-size:110px;margin-top:10px">Jangan <span style="color:var(--gold)">terabai.</span></div></div>
  <!-- M -->
  <div id="m-h" class="gfx center" style="top:190px"><div class="eyebrow" style="font-size:28px">Jom upgrade rutin mandi</div><div class="display" style="font-size:170px;margin-top:6px">Tukar<br/><span style="color:var(--gold)">Sekarang</span></div></div>
</div>

<div id="caps" class="layer">
{caps}
</div>

<div id="flash" class="layer"></div>
<div id="vignette" class="layer"></div>
<div id="grain" class="layer"></div>
<div id="frame"></div>
<div id="brandbar" class="gfx center" style="opacity:1"><span>FRESCURA · BODY</span></div>
<div id="prog"><div id="progfill"></div></div>

</div>
<script>
const tl = gsap.timeline({{ paused: true }});
const q = s => document.querySelector(s);
const E = "expo.out", P4 = "power4.out";
const IN = (sel, t, v={{}}) => tl.fromTo(sel, Object.assign({{opacity:0, y:60, filter:"blur(14px)"}}, v.from||{{}}), Object.assign({{opacity:1, y:0, x:0, filter:"blur(0px)", duration:.55, ease:E}}, v.to||{{}}), t);
const OUT = (sel, t, d=.25) => tl.to(sel, {{opacity:0, filter:"blur(10px)", duration:d, ease:"power2.in"}}, t);
const FLASH = (t, o=.55) => tl.fromTo("#flash", {{opacity:o}}, {{opacity:0, duration:.35, ease:"power2.out"}}, t);
const SPLIT = (sel) => {{ const el=q(sel); const txt=el.textContent; el.innerHTML = [...txt].map(c=>`<span style="display:inline-block">${{c===' '?'&nbsp;':c}}</span>`).join(''); return el.children; }};

// progress bar
tl.fromTo("#progfill", {{scaleX:0}}, {{scaleX:1, duration:{D}, ease:"none"}}, 0);

// ---- scene punch-in transitions on every video/scene
const cuts = {json.dumps([[x[0], x[2], x[3], x[4]] for x in SC])};
cuts.forEach(([id,s,e,mode]) => {{
  const el = q("#v-"+id);
  if (mode==="arch") {{
    tl.fromTo(el, {{scale:1.08, y:80, opacity:0}}, {{scale:1, y:0, opacity:1, duration:.5, ease:E}}, s);
    tl.to(el, {{scale:1.03, duration:Math.max(.1,e-s-.5), ease:"none"}}, s+.5);
  }} else {{
    tl.fromTo(el, {{scale:1.16, filter:"blur(10px)"}}, {{scale:1.02, filter:"blur(0px)", duration:.45, ease:E}}, s);
    tl.to(el, {{scale:1.0, duration:Math.max(.1,e-s-.45), ease:"none"}}, s+.45);
  }}
}});

// ---- A hook
FLASH(0, .9);
SPLIT("#a-h1");
tl.set("#a-h1", {{opacity:1}}, 0.9);
IN("#a-eye", 0.02, {{to:{{duration:.4}}}});
tl.fromTo("#a-h1 span", {{opacity:0, y:120, rotateX:-70, filter:"blur(18px)"}}, {{opacity:1, y:0, rotateX:0, filter:"blur(0px)", duration:.6, ease:E, stagger:.05}}, 0.9);
tl.fromTo("#a-h1", {{scale:1.25}}, {{scale:1, duration:1.2, ease:P4}}, 0.9);
IN("#a-h2", 2.05);
OUT(["#a-eye","#a-h1","#a-h2"], 2.9);
// ---- B meter & chips
IN("#b-meter", 3.0);
const pct = {{v:100}};
tl.to(pct, {{v:18, duration:2.6, ease:"power2.inOut", onUpdate:()=>{{ q("#b-pct").textContent = Math.round(pct.v)+"%"; }}}}, 2.5);
tl.fromTo("#b-bar", {{scaleX:1}}, {{scaleX:.18, duration:2.6, ease:"power2.inOut"}}, 2.5);
tl.to("#b-bar", {{background:"linear-gradient(90deg,#d9534f,#e3a07a)", duration:1.2}}, 3.6);
IN("#b-c1", 2.44, {{from:{{x:-80,y:0}}}}); IN("#b-c2", 3.26, {{from:{{x:80,y:0}}}}); IN("#b-c3", 4.40, {{from:{{x:-80,y:0}}}});
OUT(["#b-meter","#b-c1","#b-c2","#b-c3"], 5.3);
// ---- D checklist
IN("#d-card", 5.5);
const clk = {{m:17*60+30}};
tl.to(clk, {{m:23*60, duration:3.8, ease:"power1.in", onUpdate:()=>{{ const m=Math.round(clk.m); q("#d-clock").textContent = String(Math.floor(m/60)).padStart(2,"0")+":"+String(m%60).padStart(2,"0"); }}}}, 5.55);
[["#d-t1",7.15],["#d-t2",8.12],["#d-t3",8.70]].forEach(([s,t])=>{{
  tl.to(s, {{opacity:1, duration:.15}}, t);
  tl.fromTo(s+" .bx", {{"--ck":0}}, {{"--ck":1, duration:.3, ease:"back.out(3)"}}, t);
  tl.fromTo(s+" .tx", {{"--st":0}}, {{"--st":1, duration:.35, ease:P4}}, t+.08);
}});
OUT("#d-card", 9.3);
// ---- E penat
IN("#e-h", 9.42, {{from:{{scale:1.25, y:0}}, to:{{scale:1}}}});
IN("#e-bat", 9.6, {{from:{{y:30}}}});
tl.fromTo("#e-batfill", {{scaleX:.9}}, {{scaleX:.06, duration:.8, ease:"power3.in"}}, 9.7);
tl.to("#e-batfill", {{background:"#e0524a", duration:.2}}, 10.2);
tl.to("#e-bat", {{opacity:.25, duration:.08, yoyo:true, repeat:3}}, 10.25);
OUT(["#e-h","#e-bat"], 10.48, .12);
// ---- F routine
FLASH(10.55, .35);
IN("#f-head", 10.6);
IN("#f-s1", 11.8, {{from:{{x:-60,y:0}}}}); IN("#f-s1t", 12.1, {{from:{{y:30}}}});
OUT(["#f-s1","#f-s1t"], 12.65, .15);
OUT("#f-head", 12.65, .15);
IN("#f-s2", 12.85, {{from:{{x:-60,y:0}}}}); IN("#f-s2t", 13.1);
OUT(["#f-s2","#f-s2t"], 14.75, .15);
IN("#f-s3", 14.95, {{from:{{x:-60,y:0}}}}); IN("#f-s3t", 15.3, {{from:{{y:30}}}});
OUT(["#f-s3","#f-s3t"], 16.8, .15);
// ---- G luxury mall reveal
FLASH(16.95, .6);
tl.fromTo("#g-stage", {{scale:1.12}}, {{scale:1, duration:4.4, ease:"power2.out"}}, 16.95);
tl.fromTo("#g-spot", {{opacity:0}}, {{opacity:1, duration:.8}}, 17.0);
tl.fromTo("#g-pod", {{opacity:0, y:120, scale:.8}}, {{opacity:1, y:0, scale:1, duration:.8, ease:E}}, 17.05);
tl.fromTo("#g-bottles", {{y:700, opacity:0}}, {{y:0, opacity:1, duration:1.0, ease:"expo.out"}}, 17.4);
tl.fromTo("#g-noche", {{rotation:-6}}, {{rotation:0, duration:1.2, ease:E}}, 17.4);
tl.fromTo("#g-glory", {{rotation:6}}, {{rotation:0, duration:1.2, ease:E}}, 17.4);
tl.fromTo("#g-sweep", {{x:0}}, {{x:1500, duration:1.3, ease:"power2.inOut"}}, 18.4);
tl.fromTo("#g-sweep", {{x:0}}, {{x:1500, duration:1.3, ease:"power2.inOut", immediateRender:false}}, 20.0);
tl.fromTo("#g-logo", {{opacity:0, scale:.6, filter:"blur(20px)"}}, {{opacity:1, scale:1, filter:"blur(0px)", duration:.8, ease:E}}, 17.75);
IN("#g-tag", 18.8, {{from:{{y:20}}}});
tl.fromTo("#g-bokeh .bk", {{y:0}}, {{y:-120, duration:4.4, ease:"none", stagger:{{each:.02}}}}, 16.95);
tl.fromTo("#g-sparks .sp", {{opacity:0, scale:0}}, {{opacity:1, scale:1, duration:.3, stagger:{{each:.09, yoyo:true, repeat:1}}, ease:"power2.out"}}, 17.9);
tl.to("#g-stage", {{opacity:0, duration:.2}}, 21.2);
// ---- H pump
IN("#h-h", 21.45);
IN("#h-c1", 22.0, {{from:{{x:60,y:0}}}});
IN("#h-c2", 22.6, {{from:{{x:-60,y:0}}}});
OUT(["#h-h","#h-c1","#h-c2"], 24.15, .15);
// ---- I feminin
IN("#i-h", 24.3);
OUT("#i-h", 25.4, .12);
// ---- J variants
FLASH(25.5, .4);
tl.fromTo("#j-left", {{xPercent:-100}}, {{xPercent:0, duration:.5, ease:E}}, 25.5);
tl.fromTo("#j-right", {{xPercent:100}}, {{xPercent:0, duration:.5, ease:E}}, 25.95);
tl.fromTo("#j-glory", {{x:-500, rotation:-12, opacity:0}}, {{x:0, rotation:0, opacity:1, duration:.7, ease:E}}, 25.55);
tl.fromTo("#j-noche", {{x:500, rotation:12, opacity:0}}, {{x:0, rotation:0, opacity:1, duration:.7, ease:E}}, 26.0);
IN("#j-n1", 25.75); IN("#j-n2", 26.2);
tl.fromTo("#j-div", {{scaleY:0}}, {{scaleY:1, duration:.8, ease:E}}, 25.9);
tl.fromTo("#j-badge", {{opacity:0, scale:1.6, filter:"blur(16px)"}}, {{opacity:1, scale:1, filter:"blur(0px)", duration:.5, ease:"back.out(1.6)"}}, 27.1);
tl.to(["#j-glory","#j-noche"], {{y:-24, duration:1.4, ease:"sine.inOut", yoyo:true, repeat:1}}, 26.6);
// ---- K/L
IN("#k-h", 29.45, {{from:{{y:0, scale:1.3}}, to:{{scale:1}}}});
IN("#k-s", 30.2);
OUT(["#k-h","#k-s"], 31.3, .12);
IN("#l-h", 31.45);
OUT("#l-h", 32.6, .12);
// ---- M
FLASH(32.7, .4);
IN("#m-h", 32.72, {{from:{{scale:1.2, y:0}}, to:{{scale:1}}}});
OUT("#m-h", 34.0, .12);
// ---- N pick
IN("#n-atau", 34.15, {{from:{{y:20}}}});
tl.fromTo("#n-ga", {{scale:.7, y:200, opacity:0}}, {{scale:1, y:0, opacity:1, duration:.6, ease:E}}, 34.15);
tl.fromTo("#n-b", {{clipPath:"circle(0% at 50% 45%)", opacity:1}}, {{clipPath:"circle(80% at 50% 45%)", opacity:1, duration:.55, ease:"power3.inOut"}}, 35.05);
tl.fromTo("#n-nb", {{scale:.8, rotation:8}}, {{scale:1, rotation:0, duration:.7, ease:E}}, 35.1);
// ---- O end card
FLASH(36.0, .5);
tl.fromTo("#o-stage", {{scale:1.1}}, {{scale:1, duration:3.6, ease:"power2.out"}}, 36.0);
tl.fromTo(["#o-noche","#o-glory"], {{y:500, opacity:0}}, {{y:0, opacity:1, duration:.8, ease:E, stagger:.08}}, 36.0);
tl.fromTo("#o-logo", {{opacity:0, scale:.7}}, {{opacity:1, scale:1, duration:.7, ease:E}}, 36.1);
tl.fromTo("#o-btn", {{opacity:0, y:40, scale:.8}}, {{opacity:1, y:0, scale:1, duration:.5, ease:"back.out(2)"}}, 36.15);
tl.to("#o-btn", {{scale:1.07, duration:.35, ease:"sine.inOut", yoyo:true, repeat:5}}, 36.7);
IN("#o-stock", 36.8, {{from:{{y:30}}}});
tl.fromTo("#o-bar", {{scaleX:1}}, {{scaleX:.12, duration:1.9, ease:"power3.inOut"}}, 36.9);
// ---- captions (word pop)
document.querySelectorAll(".cap").forEach(c => {{
  const s = +c.dataset.s, e = +c.dataset.e;
  tl.fromTo(c, {{opacity:0, y:24}}, {{opacity:1, y:0, duration:.14, ease:P4}}, s);
  c.querySelectorAll(".w").forEach(w => {{
    tl.to(w, {{opacity:1, y:0, duration:.14, ease:"back.out(2.5)"}}, +w.dataset.t);
  }});
  tl.to(c, {{opacity:0, duration:.08}}, e - .08);
}});
// hide captions on end-card bottom zone (button/stock live there)
tl.set("#caps", {{y:0}}, 0);
tl.to("#caps", {{y:110, duration:.3, ease:P4}}, 36.0);
tl.to("#brandbar", {{opacity:0, duration:.3}}, 16.95); tl.to("#brandbar", {{opacity:1, duration:.3}}, 21.35);
tl.to("#brandbar", {{opacity:0, duration:.3}}, 35.9);
window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body>
</html>
"""
open(f"{P}/index.html", "w").write(html)
json.dump(dict(chunks=chunks), open(f"{P}/captions.json", "w"), ensure_ascii=False)
print("chunks", len(chunks))
