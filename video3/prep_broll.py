"""Video 3 (minimalist luxury): B-roll + the 2 s face.  Usage: python3 -I prep_broll.py SCRATCH OUT_DIR MAIN.mp4"""
import os, subprocess, sys
S, out, main = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
def pick(*cands):
    for p in cands:
        if os.path.exists(p) and os.path.getsize(p) > 10000: return p
G = "eq=saturation=0.95:contrast=1.04:gamma=1.02"
enc = ["-an", "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
C = {  # name: (file, ss, dur, focus, W, H)
    "lab":       (pick(f"{S}/mixkit/v/17556.mp4"), 0.5, 4.4, 0.40, 1080, 1080),
    "scientist": (pick(f"{S}/mixkit/v1080/4719.mp4", f"{S}/mixkit/v/4719.mp4"), 1.0, 3.4, 0.5, 1080, 1350),
    "bubbles":   (pick(f"{S}/mixkit/v1080/44812.mp4"), 1.0, 2.4, 0.5, 1080, 1080),
    "rose":      (pick(f"{S}/mixkit/v1080/171.mp4"), 1.0, 3.8, 0.5, 1080, 1080),
    "stars":     (pick(f"{S}/v2/mk/v/46101.mp4"), 0.5, 3.4, 0.5, 1080, 1080),
}
for name, (f, ss, d, fx, W, H) in C.items():
    vf = (f"scale='if(gt(a,{W}/{H}),-2,{W})':'if(gt(a,{W}/{H}),{H},-2)':flags=lanczos,"
          f"crop={W}:{H}:(iw-{W})*{fx}:(ih-{H})/2,setsar=1,{G}")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-t", str(d), "-i", f, "-vf", vf, *enc, f"{out}/{name}.mp4"], check=True)
    print("ok", name)
# 2 s of face, to camera, holding the bottle. The selfie recording is mirrored -> flip so the label reads.
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "0", "-t", "1.98", "-i", main, "-vf",
                f"hflip,scale=1080:1920:flags=lanczos,setsar=1,{G}", *enc, f"{out}/face.mp4"], check=True)
print("ok face")
