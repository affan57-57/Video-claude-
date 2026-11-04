"""Write the SFX cue sheet (times authored on the pre-tightening voice timeline, remapped).
Usage: python3 -I sfx_cues.py AUDIO_DIR   (reads AUDIO_DIR/remap.json, writes AUDIO_DIR/sfx_cues.json)"""
import json, sys
d = sys.argv[1]
REMOVED = json.load(open(f"{d}/remap.json"))
def T(x):
    out = x
    for a, b in REMOVED:
        if x >= b: out -= (b - a)
        elif x > a: out -= (x - a)
    return round(out, 3)
c = []
def a(t, s, g=0.6, pan=0): c.append({"t": T(t), "sfx": s, "gain": g, "pan": pan})
# hook on product photo
a(0.0, "impact", 0.9); a(0.08, "pop", 0.5); a(0.58, "pop", 0.45); a(1.08, "pop", 0.5); a(1.75, "sparkle", 0.5)
# face (to camera) + gel / bar soap
a(2.4, "whoosh", 0.55); a(2.7, "pop", 0.45)
a(4.4, "whoosh", 0.5); a(4.5, "pop", 0.5, -0.3); a(5.0, "error", 0.45)
a(5.4, "whoosh", 0.45); a(5.62, "boing", 0.35); a(5.6, "pop", 0.5, 0.3); a(6.1, "error", 0.45)
a(6.32, "impact", 0.7); a(6.4, "whoosh_rev", 0.5); a(8.6, "bubbles", 0.6); a(8.66, "sparkle", 0.45)
a(9.2, "whoosh", 0.5); a(10.74, "pop", 0.5)
a(11.1, "whoosh", 0.5); a(12.98, "boing", 0.55); a(13.24, "boing", 0.45)
a(13.9, "whoosh", 0.55); a(14.3, "click", 0.6); a(15.4, "pop", 0.45); a(16.98, "pop", 0.45)
a(16.9, "whoosh", 0.5); a(17.92, "sparkle", 0.5); a(18.76, "ding", 0.5)
a(19.3, "whoosh", 0.5); a(19.45, "click", 0.7); a(20.1, "click", 0.7); a(20.75, "bubbles", 0.6); a(21.6, "bubbles", 0.5)
a(22.1, "whoosh", 0.5); a(22.45, "error", 0.45)
a(25.0, "whoosh", 0.55); a(26.12, "pop", 0.5); a(27.52, "impact", 0.45); a(28.66, "pop", 0.4); a(29.16, "impact", 0.45); a(29.7, "ding", 0.35)
a(30.3, "whoosh", 0.5); a(30.6, "whoosh", 0.35); a(32.48, "pop", 0.5, -0.3); a(33.08, "pop", 0.5); a(33.78, "pop", 0.5, 0.3)
a(34.75, "whoosh", 0.5); a(35.0, "whoosh", 0.35); a(36.76, "pop", 0.5, -0.3); a(37.28, "pop", 0.5, 0.3)
a(37.7, "whoosh", 0.5); a(40.42, "stamp", 0.7); a(41.82, "stamp", 0.7)
a(43.85, "whoosh", 0.5); a(45.76, "stamp", 0.85)
a(47.3, "whoosh", 0.5); a(48.82, "sparkle", 0.45); a(50.1, "ding", 0.4)
a(49.4, "riser", 0.45); a(51.0, "impact", 0.75); a(51.1, "sparkle", 0.5); a(51.8, "pop", 0.5)
a(52.85, "whoosh", 0.55); a(53.56, "click", 0.7); a(53.75, "cash", 0.5); a(55.68, "tick", 0.5); a(56.42, "tick", 0.5); a(56.96, "tick", 0.5); a(57.7, "impact", 0.55); a(58.22, "tick", 0.5); a(58.52, "tick", 0.5)
a(58.85, "whoosh", 0.55); a(59.82, "pop", 0.5, -0.3); a(60.68, "pop", 0.5, 0.3); a(61.4, "click", 0.7); a(61.92, "cash", 0.55); a(62.05, "ding", 0.45)
json.dump(c, open(f"{d}/sfx_cues.json", "w"), indent=0)
print(len(c), "cues")
