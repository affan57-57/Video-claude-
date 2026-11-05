"""Video 5 (tidur wangi semerbak): B-roll crops + the 2 s face.  Usage: python3 -I prep_broll.py MIXKIT_DIR OUT_DIR MAIN.mp4"""
import os, subprocess, sys
M, out, main = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
G = "eq=saturation=0.95:contrast=1.04:gamma=1.02"
enc = ["-an", "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
C = {  # name: (mixkit id, ss, dur, focus_x, W, H)
    "hotel":    (4196, 2.0, 3.2, 0.35, 1080, 1920),
    "corridor": (34613, 0.5, 2.2, 0.5, 1080, 1920),
    "bedroom":  (3111, 2.0, 5.0, 0.45, 900, 1150),
    "candle":   (6925, 3.0, 3.8, 0.5, 380, 380),
    "bed":      (4198, 1.0, 4.4, 0.35, 900, 1000),
    "shelf":    (21694, 1.0, 4.0, 0.5, 900, 1000),
    "money":    (18304, 1.0, 4.4, 0.5, 900, 900),
    "wallet":   (18299, 3.0, 4.4, 0.5, 400, 400),
    "shower":   (21766, 3.0, 3.0, 0.5, 1080, 1920),
    "moon":     (4433, 6.0, 3.0, 0.45, 420, 420),
    "candles":  (48498, 2.0, 4.6, 0.5, 1080, 1920),
}
for name, (i, ss, d, fx, W, H) in C.items():
    f = f"{M}/v/{i}.mp4"
    vf = (f"scale='if(gt(a,{W}/{H}),-2,{W})':'if(gt(a,{W}/{H}),{H},-2)':flags=lanczos,"
          f"crop={W}:{H}:(iw-{W})*{fx}:(ih-{H})/2,setsar=1,{G}")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-t", str(d), "-i", f, "-vf", vf, *enc, f"{out}/{name}.mp4"], check=True)
    print("ok", name)
# 2.0 s of face, front camera, looking into the lens: "Korang, aku ada satu perangai tau". Selfie -> hflip.
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "0.49", "-t", "2.02", "-i", main, "-vf",
                f"hflip,scale=1080:1920:flags=lanczos,setsar=1,{G}", *enc, f"{out}/face.mp4"], check=True)
print("ok face")
