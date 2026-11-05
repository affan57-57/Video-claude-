"""Video 9 ("3 sebab tukar ke Frescura Body"): B-roll crops + the under-1 s face.  Usage: python3 -I prep_broll.py MIXKIT_DIR OUT_DIR MAIN.mp4 [names...]"""
import os, subprocess, sys
M, out, main = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
G = "eq=saturation=0.9:contrast=1.03:gamma=1.03,colorbalance=rs=.03:gs=-.01:bs=-.01:rh=.02"   # warm blush grade
enc = ["-an", "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
C = {  # name: (mixkit id, ss, dur, focus_x, W, H, extra filter)
    "gosok":   (5321, 3.0, 2.2, 0.50, 540, 1160, ""),
    "bubbles": (44812, 1.0, 2.2, 0.50, 1080, 1920, ""),
    "salt":    (22402, 8.0, 2.0, 0.55, 1080, 1920, ""),
    "sea":     (50236, 4.0, 4.0, 0.40, 1080, 1920, ""),
    "perfume": (21694, 1.2, 3.2, 0.45, 1080, 1920, ""),
    "rose":    (38386, 4.0, 2.9, 0.55, 1080, 1920, ""),
    "sky":     (46203, 0.3, 3.0, 0.50, 1080, 1920, ""),
    "berries": (10423, 3.0, 3.0, 0.70, 620, 620, ""),
    "unbox":   (31274, 2.0, 1.4, 0.45, 960, 700, ""),
    "shop":    (42136, 5.5, 3.6, 0.50, 1080, 1920, ",gblur=sigma=22"),
}
only = set(sys.argv[4:])
for name, (i, ss, d, fx, W, H, ex) in C.items():
    if only and name not in only: continue
    vf = (f"scale='if(gt(a,{W}/{H}),-2,{W})':'if(gt(a,{W}/{H}),{H},-2)':flags=lanczos,"
          f"crop={W}:{H}:(iw-{W})*{fx}:(ih-{H})/2,setsar=1,{G}{ex}")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-t", str(d), "-i", f"{M}/v/{i}.mp4", "-vf", vf, *enc, f"{out}/{name}.mp4"], check=True)
    print("ok", name)
if not only or "face" in only:
    # 0.68 s of face (client: under 1 s): "Tiga" with three fingers raised, eyes into the lens (src 1.12-1.88, played 1.12x to
    # match the sped-up voice). Selfie -> hflip.
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "1.12", "-t", "0.78", "-i", main, "-vf",
                    "hflip,setpts=PTS/1.12,scale=1080:1920:flags=lanczos,setsar=1,eq=saturation=0.95:gamma=1.05:contrast=1.03",
                    *enc, f"{out}/face.mp4"], check=True)
    print("ok face")
