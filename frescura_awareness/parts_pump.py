 ARCH overlay 21.15 - 23.3
rb = __import__('random').Random(9)
bubbles = "".join(f'<div class="s6-b" id="s6-b{i}" style="left:{rb.randint(200,880)}px;top:{rb.randint(820,1080)}px;width:{(s:=rb.randint(14,46))}px;height:{s}px"></div>' for i in range(16))
scene("pump", 2.15, """
#pp-dim{background:rgba(8,7,6,.86)}
#pp-arch{left:100px;top:230px;width:880px;height:920px;overflow:hidden;border-radius:440px 440px 28px 28px;}
#pp-v{position:absolute;left:-100px;top:-230px;width:1080px;height:1920px;object-fit:cover;}
#pp-rim{left:100px;top:230px;width:880px;height:920px;border-radius:440px 440px 28px 28px;box-shadow:0 0 0 2px #d8b77a inset;}
#pp-tag{left:150px;top:560px;padding:16px 26px;background:rgba(11,9,8,.72);border:1.5px solid #d8b77a;border-radius:40px;font-size:28px;letter-spacing:.3em;text-transform:uppercase;color:#d8b77a}
#pp-h{top:1000px;font-size:96px;font-weight:600;text-shadow:0 6px 30px rgba(0,0,0,.6)}
.s6-b{position:absolute;border-radius:50%;background:radial-gradient(circle at 32% 30%,rgba(255,255,255,.95),rgba(255,255,255,.25) 35%,rgba(255,220,230,.08) 70%);box-shadow:0 0 0 1.5px rgba(255,255,255,.55) inset}
""", f"""
<div id="pp-dim" class="full"></div>
<div id="pp-arch" class="abs"><video id="pp-v" class="clip" src="assets/vid/pump_close.mp4" data-start="0" data-duration="2.15" muted playsinline></video></div>
<div id="pp-rim" class="abs"></div>
<div id="pp-tag" class="abs">1 pam · terus jadi buih</div>
<div id="pp-h" class="abs center it">buih lembut.</div>
<div id="pp-bub" class="full">{bubbles}</div>
""", """
tl.fromTo('#pp-dim',{opacity:0},{opacity:1,duration:.3,ease:'power2.out'},0);
tl.fromTo(['#pp-arch','#pp-rim'],{clipPath:'inset(48% 34% 6% 34% round 200px)',opacity:0},{clipPath:'inset(0% 0% 0% 0% round 0px)',opacity:1,duration:.55,ease:'expo.out'},0);
tl.fromTo('#pp-v',{scale:1.2},{scale:1.0,duration:2.15,ease:'power1.out'},0);
tl.fromTo('#pp-tag',{opacity:0,x:-30},{opacity:1,x:0,duration:.4,ease:'expo.out'},0.42);
tl.fromTo('#pp-h',{opacity:0,filter:'blur(10px)',scale:1.15},{opacity:1,filter:'blur(0px)',scale:1,duration:.4,ease:'expo.out'},0.3);
var r=rng(21);for(var i=0;i<16;i++){var t=0.25+r()*0.9,d=0.6+r()*.3;tl.fromTo('#s6-b'+i,{opacity:0,y:40,scale:.4},{opacity:1,y:-160-r()*260,scale:1,duration:d,ease:'power2.out'},t);tl.to('#s6-b'+i,{opacity:0,scale:1.3,duration:.12},t+d);}
tl.to(['#pp-arch','#pp-rim'],{clipPath:'inset(48% 34% 6% 34% round 200px)',opacity:0,duration:.3,ease:'power3.in'},1.82);
tl.to(['#pp-dim','#pp-tag','#pp-h'],{opacity:0,duration:.25,ease:'power2.in'},1.85);
""")

