"""Video 8 ("Stop! 5 kesilapan masa mandi"): B-roll crops + the under-1 s face.  Usage: python3 -I prep_broll.py MIXKIT_DIR OUT_DIR MAIN.mp4"""
import os, subprocess, sys
M, out, main = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
G = "eq=saturation=0.82:contrast=1.04:gamma=1.03,colorbalance=rs=-.03:gs=.0:bs=.04:rh=-.02:bh=.03"   # cool mineral-mist grade
enc = ["-an", "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
C = {  # name: (mixkit id, ss, dur, focus_x, W, H)
    "shower":  (21766, 4.0, 2.5, 0.30, 1080, 1920),
    "steam":   (10334, 3.5, 5.1, 0.50, 1080, 1920),
    "hotbath": (21764, 1.5, 5.0, 0.55, 820, 1100),
    "scrub":   (5321, 2.5, 4.8, 0.50, 1080, 1250),
    "soap":    (21768, 2.8, 2.6, 0.41, 1080, 1300),
    "bubbles": (44812, 1.0, 4.2, 0.50, 1080, 1920),
    "rinse":   (34517, 2.0, 5.1, 0.50, 1080, 1920),
    "foam":    (44834, 3.0, 5.1, 0.50, 640, 640),
    "lotion":  (45118, 0.2, 5.2, 0.55, 1080, 1250),
    "waves":   (31745, 3.0, 2.0, 0.50, 1080, 1920),
    "salt":    (22402, 8.0, 3.6, 0.55, 760, 760),
    "perfume": (21694, 1.2, 3.0, 0.45, 1080, 1920),
    "phone":   (4915, 2.0, 3.4, 0.50, 1080, 1920),
    "typing":  (39774, 1.0, 2.9, 0.40, 1080, 1920),
}
only = set(sys.argv[4:])
for name, (i, ss, d, fx, W, H) in C.items():
    if only and name not in only: continue
    f = f"{M}/v/{i}.mp4"
    vf = (f"scale='if(gt(a,{W}/{H}),-2,{W})':'if(gt(a,{W}/{H}),{H},-2)':flags=lanczos,"
          f"crop={W}:{H}:(iw-{W})*{fx}:(ih-{H})/2,setsar=1,{G}")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-t", str(d), "-i", f, "-vf", vf, *enc, f"{out}/{name}.mp4"], check=True)
    print("ok", name)
if not only or "face" in only:
    # 0.60 s of face (client: under 1 s): face clear, then "Stop!" with the raised palm, eyes into the lens (src 0.50-1.20, played 1.12x to match the
    # sped-up voice). Selfie -> hflip.
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "0.50", "-t", "0.70", "-i", main, "-vf",
                    f"hflip,setpts=PTS/1.12,scale=1080:1920:flags=lanczos,setsar=1,eq=saturation=0.95:gamma=1.04:contrast=1.03",
                    *enc, f"{out}/face.mp4"], check=True)
    print("ok face")
