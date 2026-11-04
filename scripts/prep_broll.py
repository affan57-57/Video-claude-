"""Trim + crop every B-roll clip to 1080x1920 / 30fps, silent, lightly graded.
Usage: python3 -I prep_broll.py SOURCE.mp4 MIXKIT_DIR OUT_DIR"""
import os, subprocess, sys

src, mk, out = sys.argv[1:4]
os.makedirs(out, exist_ok=True)

def pick(n):
    p = f"{mk}/v1080/{n}.mp4"
    if os.path.exists(p) and os.path.getsize(p) > 10000:
        return p
    return f"{mk}/v/{n}.mp4"

# name: (file, media_start, duration, horizontal focus 0..1, extra filter)
CLIPS = {
    "gel":        (pick(21769), 0.5, 2.6, 0.55, ""),
    "bubbles":    (pick(44812), 1.0, 3.2, 0.50, ""),
    "pinkbubble": (pick(13787), 2.0, 2.2, 0.50, ""),
    "lather":     (pick(33705), 3.0, 3.1, 0.32, ""),
    "irid":       (pick(44834), 1.0, 3.3, 0.50, ""),
    "perfume":    (pick(20766), 0.3, 2.7, 0.78, ""),
    "stream":     (pick(34517), 1.0, 3.2, 0.40, ""),
    "rose":       (pick(171),   1.0, 5.6, 0.50, ""),
    "flowers":    (pick(1168),  2.0, 4.7, 0.50, ""),
    "berries":    (pick(15973), 0.5, 3.2, 0.50, ""),
    "lab":        (pick(17556), 0.5, 6.4, 0.38, ""),
    "scientist":  (pick(4719),  1.0, 3.7, 0.50, ""),
    "shower":     (pick(21766), 2.0, 3.9, 0.30, ""),
    "phone":      (pick(42136), 0.5, 6.3, 0.50, ""),
}

def run(cmd):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *cmd], check=True)

grade = "eq=saturation=1.12:contrast=1.04"
enc = ["-an", "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
       "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
for name, (f, ss, d, fx, extra) in CLIPS.items():
    vf = (f"scale=-2:1920:flags=lanczos,crop=1080:1920:(iw-1080)*{fx}:0,"
          f"scale=1080:1920,setsar=1,{grade}{extra}")
    run(["-ss", str(ss), "-t", str(d), "-i", f, "-vf", vf, *enc, f"{out}/{name}.mp4"])
    print("ok", name)

# Talking-head hook: the only 2 s of face. Source is mirrored, so flip it.
run(["-ss", "16.29", "-t", "2.15", "-i", src, "-vf",
     f"hflip,scale=1080:1920:flags=lanczos,setsar=1,{grade}", *enc, f"{out}/face.mp4"])
# Product placeholder (until real product photos arrive): bottle crop, flipped so label reads right.
run(["-ss", "0.6", "-t", "3.0", "-i", src, "-vf",
     f"hflip,crop=340:604:0:372,scale=720:1280:flags=lanczos,setsar=1,{grade}", *enc,
     f"{out}/product.mp4"])
run(["-ss", "1.0", "-i", src, "-frames:v", "1", "-vf",
     "hflip,crop=340:604:0:372,scale=720:1280:flags=lanczos", f"{out}/product.jpg"])
print("ok face/product")
