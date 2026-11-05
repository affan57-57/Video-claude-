"""Video 6 ("5 perkara lepas balik kerja"): B-roll crops + the under-1 s face.  Usage: python3 -I prep_broll.py MIXKIT_DIR OUT_DIR MAIN.mov"""
import os, subprocess, sys
M, out, main = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
G = "eq=saturation=0.88:contrast=1.05:gamma=1.0,colorbalance=rs=.03:gs=.01:bs=-.03"   # warm, slightly muted editorial grade
enc = ["-an", "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
C = {  # name: (mixkit id, ss, dur, focus_x, W, H)
    "office":  (24344, 3.0, 1.6, 0.5, 1080, 1920),
    "sea":     (34363, 2.0, 4.0, 0.5, 560, 900),
    "phone":   (14669, 1.0, 4.8, 0.6, 640, 900),
    "vinyl":   (48459, 2.0, 2.8, 0.5, 600, 600),
    "family":  (6213, 4.0, 4.3, 0.5, 1080, 452),
    "bath":    (47057, 1.0, 5.2, 0.5, 900, 700),
    "candle":  (3438, 1.0, 5.2, 0.5, 440, 620),
    "tea":     (9267, 2.0, 3.2, 0.5, 1080, 1920),
    "book":    (1724, 2.0, 3.4, 0.5, 1080, 1920),
    "city":    (3134, 4.0, 2.0, 0.5, 1080, 1920),
}
for name, (i, ss, d, fx, W, H) in C.items():
    f = f"{M}/v/{i}.mp4"
    vf = (f"scale='if(gt(a,{W}/{H}),-2,{W})':'if(gt(a,{W}/{H}),{H},-2)':flags=lanczos,"
          f"crop={W}:{H}:(iw-{W})*{fx}:(ih-{H})/2,setsar=1,{G}")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-t", str(d), "-i", f, "-vf", vf, *enc, f"{out}/{name}.mp4"], check=True)
    print("ok", name)
# 0.78 s of face (client: under 1 s): "kerja, jangan", eyes in the lens (src 0.87-1.65). Selfie -> hflip (poster text reads right).
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "0.87", "-t", "0.78", "-i", main, "-vf",
                f"hflip,scale=1080:1920:flags=lanczos,setsar=1,{G}", *enc, f"{out}/face.mp4"], check=True)
print("ok face")
