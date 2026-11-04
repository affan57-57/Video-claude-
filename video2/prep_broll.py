"""Video 2 (luxury): trim/crop/grade B-roll to 1080x1920 (or panel sizes). 
Usage: python3 -I prep_broll.py MIXKIT_V2_DIR MIXKIT_V1_DIR MAIN.mp4 OUT_DIR  (MAIN = the talking-head source)"""
import os, subprocess, sys
mk2, mk1, main, out = sys.argv[1:5]
os.makedirs(out, exist_ok=True)
def pick(n):
    for d in (f"{mk2}/v", f"{mk1}/v1080", f"{mk1}/v"):
        p = f"{d}/{n}.mp4"
        if os.path.exists(p) and os.path.getsize(p) > 10000:
            return p
WARM = "eq=saturation=0.92:contrast=1.08:gamma=0.96,colorbalance=rs=0.03:gs=0.0:bs=-0.03:rh=0.02:bh=-0.02"
COOL = "eq=saturation=0.35:contrast=1.05:brightness=-0.03,colorbalance=bs=0.04:rs=-0.02"
# name: (id, ss, dur, focus, W, H, grade)
C = {
    "busy_type":   (1781,  1.0, 3.6, 0.5, 1080, 640, COOL),
    "busy_kitchen":(40522, 1.0, 3.6, 0.5, 1080, 640, COOL),
    "busy_family": (6213,  2.0, 3.6, 0.5, 1080, 640, COOL),
    "hourglass":   (28901, 1.0, 3.3, 0.5, 1080, 1920, WARM),
    "candles":     (41744, 1.0, 2.9, 0.5, 1080, 1920, WARM),
    "shower":      (34517, 1.0, 3.3, 0.40, 1080, 1920, WARM),
    "smoke":       (50956, 1.0, 3.0, 0.5, 1080, 1920, WARM),
    "rose":        (171,   1.0, 6.2, 0.5, 1080, 1920, WARM),
    "stars":       (46101, 0.5, 6.2, 0.5, 1080, 1920, "eq=saturation=1.05:contrast=1.06"),
    "bokeh":       (45355, 0.5, 2.4, 0.5, 1080, 1920, WARM),
    "candle":      (48919, 0.5, 2.5, 0.72, 1080, 1920, WARM),
    "gift":        (14839, 0.5, 2.6, 0.5, 1080, 1920, WARM),
    "tealights":   (3438,  0.5, 2.3, 0.5, 1080, 1920, WARM),
    "leak":        (48495, 0.0, 6.0, 0.5, 1080, 1920, "eq=saturation=0.8"),
}
enc = ["-an", "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
for name, (n, ss, d, fx, W, H, g) in C.items():
    f = pick(n)
    vf = (f"scale='if(gt(a,{W}/{H}),-2,{W})':'if(gt(a,{W}/{H}),{H},-2)':flags=lanczos,"
          f"crop={W}:{H}:(iw-{W})*{fx}:(ih-{H})/2,setsar=1,{g}")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-t", str(d), "-i", f, "-vf", vf, *enc,
                    f"{out}/{name}.mp4"], check=True)
    print("ok", name, f)
# the 2 s of face: the only stretch where he looks straight into the lens -- the hook's punchline,
# "tapi diri kita tak pernah kita sayang" (source 1.84-3.89, no pause cut inside it)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "1.84", "-t", "2.05", "-i", main, "-vf",
                f"scale=1080:1920:flags=lanczos,setsar=1,{WARM}", *enc, f"{out}/face.mp4"], check=True)
print("ok face")
