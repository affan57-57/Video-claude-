"""Video 12 (Metro Noir sequel: KLCC, Menara KL, TRX + mall): city/mall B-roll crops, the client's pump/foam demo and the under-1 s face.
Usage: python3 -I prep_broll.py MIXKIT_DIR OUT_DIR MAIN.mp4 PART2.mp4 [names...]"""
import os, subprocess, sys
M, out, main, part2 = sys.argv[1:5]
os.makedirs(out, exist_ok=True)
G = "eq=saturation=1.08:contrast=1.06:brightness=-0.03,colorbalance=rs=.03:bs=.04:rh=.04:bh=-.03"
enc = ["-an", "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
C = {  # name: (mixkit id, ss, dur, focus_x)
    "mall_atrium": (31086, 0.5, 7.4, 0.50),   # luxury mall atrium, escalators
    "mall_esc":    (25516, 0.5, 5.0, 0.50),   # multi-level escalators
    "mall_glass":  (22137, 2.0, 2.9, 0.40),   # glass lift, white mall
    "mall_wide":   (36273, 0.5, 2.4, 0.50),   # mall interior from above
    "mall_tokyo":  (30954, 0.5, 2.8, 0.45),   # luxury atrium (time lapse)
    "boutique":    (34213, 6.0, 3.0, 0.40),   # boutique display (jewellery)
    "escalator":   (14529, 2.0, 2.9, 0.50),   # escalator from above
    "kl_klcc_kl":  (20130, 2.0, 0.9, 0.62),   # KLCC + Menara KL by day
    "klcc_day":    (30180, 1.0, 3.9, 0.55),   # KLCC skyline by day
    "kl_tower":    (39442, 1.0, 1.9, 0.22),   # Menara KL
    "klcc_night":  (20122, 4.5, 4.1, 0.60),   # Petronas towers at night
    "kl_dusk":     (27749, 4.0, 3.5, 0.55),   # dusk silhouettes: KLCC + Menara KL
    "kl_night":    (20120, 0.5, 2.0, 0.55),   # KL night with the twin towers
    "kl_aerial":   (20119, 0.5, 3.1, 0.50),   # KL night aerial
    "klcc_up":     (20137, 4.0, 1.7, 0.50),   # Petronas from below
}
only = set(sys.argv[5:])
for name, (i, ss, d, fx) in C.items():
    if only and name not in only: continue
    vf = f"scale=-2:1920:flags=lanczos,crop=1080:1920:(iw-1080)*{fx}:0,setsar=1,{G}"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-t", str(d), "-i", f"{M}/v/{i}.mp4", "-vf", vf, *enc, f"{out}/{name}.mp4"], check=True)
    print("ok", name)
P = {"lather1": (24.0, 2.7), "pump": (10.1, 2.8), "palm": (11.0, 4.3), "lather2": (27.0, 2.4)}   # client's own demo: no flip, no grade
for name, (ss, d) in P.items():
    if only and name not in only: continue
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-t", str(d), "-i", part2, "-vf", "scale=720:1280:flags=lanczos,setsar=1", *enc, f"{out}/{name}.mp4"], check=True)
    print("ok", name)
if not only or "face" in only:
    # 0.75 s of face (client: under 1 s): "Serius lah," eyes into the lens (src 0.59-1.43, played 1.12x). Selfie -> hflip.
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "0.59", "-t", "0.85", "-i", main, "-vf",
                    "hflip,setpts=PTS/1.12,scale=1080:1920:flags=lanczos,setsar=1,eq=saturation=0.95:gamma=1.05:contrast=1.03",
                    *enc, f"{out}/face.mp4"], check=True)
    print("ok face")
