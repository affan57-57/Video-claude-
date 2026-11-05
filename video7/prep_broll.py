"""Video 7 ("Wanita lebih yakin: 5 perkara"): B-roll crops + the under-1 s face.  Usage: python3 -I prep_broll.py MIXKIT_DIR OUT_DIR MAIN.mov"""
import os, subprocess, sys
M, out, main = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
G = "eq=saturation=0.85:contrast=1.03:gamma=1.04:brightness=0.02,colorbalance=rs=.02:gs=.02:bs=-.02"   # soft, airy, slightly warm
enc = ["-an", "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
C = {  # name: (mixkit id, ss, dur, focus_x, W, H)
    "woman":   (45655, 1.0, 2.8, 0.62, 1080, 1920),
    "hands":   (33096, 2.0, 3.2, 0.45, 1080, 1100),
    "soap":    (2804, 1.0, 3.2, 0.5, 420, 520),
    "fabric":  (40229, 2.0, 3.6, 0.5, 530, 1920),
    "closet":  (35798, 1.0, 3.6, 0.5, 530, 1920),
    "look":    (45756, 2.0, 3.8, 0.62, 1080, 1100),
    "flowers": (1187, 3.0, 2.9, 0.5, 1080, 1920),
    "drops":   (106, 2.0, 3.5, 0.5, 1080, 1100),
    "bubbles": (44766, 2.0, 3.0, 0.5, 1080, 1920),
    "splash":  (9294, 1.0, 2.2, 0.5, 1080, 1920),
    "salt":    (22402, 3.0, 6.9, 0.5, 1080, 1100),
    "ocean":   (2091, 2.0, 1.6, 0.5, 1080, 1920),
}
for name, (i, ss, d, fx, W, H) in C.items():
    f = f"{M}/v/{i}.mp4"
    vf = (f"scale='if(gt(a,{W}/{H}),-2,{W})':'if(gt(a,{W}/{H}),{H},-2)':flags=lanczos,"
          f"crop={W}:{H}:(iw-{W})*{fx}:(ih-{H})/2,setsar=1,{G}")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-t", str(d), "-i", f, "-vf", vf, *enc, f"{out}/{name}.mp4"], check=True)
    print("ok", name)
# 0.64 s of face (client: under 1 s, from her own recording), eyes into the lens (src 1.40-2.04; niqab, so no lip-sync needed). Selfie -> hflip.
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "1.40", "-t", "0.64", "-i", main, "-vf",
                f"hflip,scale=1080:1920:flags=lanczos,setsar=1,{G}", *enc, f"{out}/face.mp4"], check=True)
print("ok face")
