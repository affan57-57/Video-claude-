"""Video 3 SFX cue sheet (final voice timeline). Usage: python3 -I sfx_cues.py AUDIO_DIR"""
import json, sys
c = []
def a(t, s, g=0.6): c.append({"t": t, "sfx": s, "gain": g})
a(0.0, "pop", 0.35); a(0.1, "tick", 0.4); a(0.86, "swoosh", 0.5); a(1.02, "tick", 0.4); a(1.38, "pop", 0.4)
a(1.9, "swoosh", 0.55); a(2.24, "tick", 0.5); a(2.52, "boom", 0.6); a(2.62, "pop", 0.45); a(2.92, "tick", 0.45); a(3.34, "tick", 0.45)
a(3.88, "swoosh", 0.5); a(4.3, "chime", 0.4)
a(5.78, "swoosh", 0.45); a(6.32, "tick", 0.5); a(6.75, "click", 0.6); a(7.90, "tick", 0.45); a(8.7, "click", 0.6); a(8.85, "click", 0.5); a(9.16, "tick", 0.4)
a(10.45, "swoosh", 0.5); a(10.9, "riser", 0.3); a(12.34, "pop", 0.55); a(12.8, "chime", 0.45)
a(13.85, "swoosh", 0.5); a(14.0, "foam", 0.5); a(15.52, "boom", 0.5)
a(16.25, "swoosh", 0.45); a(16.5, "click", 0.7); a(16.7, "foam", 0.55); a(17.72, "pop", 0.45)
a(18.62, "swoosh", 0.55); a(18.78, "swoosh", 0.35); a(19.76, "boom", 0.5)
a(20.76, "swoosh", 0.45); a(23.14, "tick", 0.5); a(23.76, "tick", 0.5)
a(24.44, "swoosh", 0.45); a(26.56, "tick", 0.5); a(27.14, "tick", 0.5)
a(27.86, "swoosh", 0.5); a(29.6, "click", 0.6); a(30.45, "click", 0.6); a(30.5, "pop", 0.35)
a(31.66, "swoosh", 0.5); a(31.76, "boom", 0.5); a(32.94, "tick", 0.4); a(34.44, "tick", 0.45); a(36.7, "click", 0.7); a(37.16, "chime", 0.5)
json.dump(c, open(f"{sys.argv[1]}/sfx_cues.json", "w"), indent=0)
print(len(c), "cues")
