"""Video 10 ("3 rahsia wangi tanpa perfume"): B-roll crops, the client's own pump/foam demo (part2) and the under-1 s face.
Usage: python3 -I prep_broll.py MIXKIT_DIR OUT_DIR MAIN.mp4 PART2.mp4 [names...]"""
import os, subprocess, sys
M, out, main, part2 = sys.argv[1:5]
os.makedirs(out, exist_ok=True)
G = "eq=saturation=0.9:contrast=1.03:gamma=1.03,colorbalance=rs=.01:gs=-.01:bs=.03"   # cool lilac grade (stock footage only)
enc = ["-an", "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
C = {  # name: (mixkit id, ss, dur, focus_x, W, H)
    "rose":    (40294, 2.0, 2.4, 0.50, 460, 600),
    "berries": (50537, 2.5, 2.2, 0.50, 460, 600),
    "sea":     (31745, 6.0, 1.7, 0.50, 1080, 1920),
}
only = set(sys.argv[5:])
for name, (i, ss, d, fx, W, H) in C.items():
    if only and name not in only: continue
    vf = (f"scale='if(gt(a,{W}/{H}),-2,{W})':'if(gt(a,{W}/{H}),{H},-2)':flags=lanczos,"
          f"crop={W}:{H}:(iw-{W})*{fx}:(ih-{H})/2,setsar=1,{G}")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-t", str(d), "-i", f"{M}/v/{i}.mp4", "-vf", vf, *enc, f"{out}/{name}.mp4"], check=True)
    print("ok", name)
# client's own product demo (part2.mp4, rear camera: label reads correctly, no flip, no colour grade so the bottle is untouched)
P = {"hero": (0.0, 2.0), "side": (3.6, 2.8), "pump": (10.1, 2.4), "palm": (15.0, 1.4), "lather": (25.0, 1.4)}
for name, (ss, d) in P.items():
    if only and name not in only: continue
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-t", str(d), "-i", part2, "-vf",
                    "scale=1080:1920:flags=lanczos,setsar=1", *enc, f"{out}/{name}.mp4"], check=True)
    print("ok", name)
if not only or "face" in only:
    # 0.76 s of face (client: under 1 s): "Kalau kau nak orang…", eyes into the lens (src 0.80-1.66, played 1.12x to match the voice). Selfie -> hflip.
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "0.80", "-t", "0.86", "-i", main, "-vf",
                    "hflip,setpts=PTS/1.12,scale=1080:1920:flags=lanczos,setsar=1,eq=saturation=0.95:gamma=1.05:contrast=1.03",
                    *enc, f"{out}/face.mp4"], check=True)
    print("ok face")
