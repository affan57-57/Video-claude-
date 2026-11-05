"""Video 11 ("3 sebab sabun ni bau perfume mahal", city concept): city B-roll crops, the client's pump/foam demo and the under-1 s face.
Usage: python3 -I prep_broll.py MIXKIT_DIR OUT_DIR MAIN.mp4 PART2.mp4 [names...]"""
import os, subprocess, sys
M, out, main, part2 = sys.argv[1:5]
os.makedirs(out, exist_ok=True)
G = "eq=saturation=1.08:contrast=1.06:brightness=-0.03,colorbalance=rs=.03:bs=.04:rh=.04:bh=-.03"   # night-city grade: cool shadows, warm lights
enc = ["-an", "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
C = {  # name: (mixkit id, ss, dur, focus_x)  -> full-frame 1080x1920
    "klcc_up":   (20137, 2.0, 5.6, 0.50),   # Petronas Twin Towers from below (KLCC)
    "ny_bokeh":  (4330, 3.0, 9.4, 0.50),    # New York skyline bokeh
    "kl_dusk":   (30988, 6.0, 3.2, 0.62),   # KL day -> night
    "kl_sunset": (20121, 2.0, 3.9, 0.60),   # KL skyline with the twin towers at sunset
    "ny_purple": (4087, 2.0, 2.6, 0.50),    # New York at night
    "kl_traffic":(20128, 0.5, 6.0, 0.50),   # KL night traffic
    "kl_day":    (39442, 1.0, 3.1, 0.22),   # KL skyline by day (KL Tower)
    "klcc_night":(20122, 4.5, 5.0, 0.60),   # Petronas towers at night
    "ny_times":  (24516, 8.0, 2.2, 0.50),   # Times Square at night
    "city_air":  (49873, 2.0, 3.5, 0.60),   # aerial city at night
}
only = set(sys.argv[5:])
for name, (i, ss, d, fx) in C.items():
    if only and name not in only: continue
    vf = f"scale=-2:1920:flags=lanczos,crop=1080:1920:(iw-1080)*{fx}:0,setsar=1,{G}"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-t", str(d), "-i", f"{M}/v/{i}.mp4", "-vf", vf, *enc, f"{out}/{name}.mp4"], check=True)
    print("ok", name)
# client's own product demo (rear camera: label reads correctly; no flip, no grade)
P = {"pump": (10.1, 3.4), "lather": (24.0, 3.5)}
for name, (ss, d) in P.items():
    if only and name not in only: continue
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-t", str(d), "-i", part2, "-vf", "scale=720:1280:flags=lanczos,setsar=1", *enc, f"{out}/{name}.mp4"], check=True)
    print("ok", name)
if not only or "face" in only:
    # 0.80 s of face (client: under 1 s): "Serius," eyes into the lens (src 0.00-0.90, played 1.12x to match the voice). Selfie -> hflip.
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "0.0", "-t", "0.90", "-i", main, "-vf",
                    "hflip,setpts=PTS/1.12,scale=1080:1920:flags=lanczos,setsar=1,eq=saturation=0.95:gamma=1.05:contrast=1.03",
                    *enc, f"{out}/face.mp4"], check=True)
    print("ok face")
