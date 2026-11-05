"""Video 4 (minimalist luxury, Bombshell vs Midnight Fantasy): B-roll crops + the <1 s face.
Usage: python3 -I prep_broll.py MIXKIT_DIR OUT_DIR MAIN.mov"""
import os, subprocess, sys
M, out, main = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
G = "eq=saturation=0.95:contrast=1.04:gamma=1.02"
enc = ["-an", "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
C = {  # name: (mixkit id, ss, dur, focus_x, W, H)
    "rose":     (38386, 1.0, 4.2, 0.5, 900, 1000),
    "pinkrose": (40294, 1.0, 3.8, 0.5, 420, 420),
    "hijab":    (49306, 2.0, 3.6, 0.5, 900, 1150),
    "straw":    (16025, 2.0, 3.6, 0.5, 760, 760),
    "moon":     (4433, 6.0, 1.8, 0.45, 1080, 1920),
    "hearts":   (18802, 1.0, 3.0, 0.5, 700, 700),
    "lavender": (1244, 1.0, 2.3, 0.4, 1080, 1920),
    "perfume":  (21694, 1.0, 4.6, 0.5, 360, 360),
    "phone":    (49311, 2.0, 4.4, 0.55, 900, 1150),
    "typing":   (4915, 2.0, 4.8, 0.45, 900, 900),
    "stars":    (4124, 1.0, 4.8, 0.5, 1080, 1920),
    "bubbles":  (13787, 1.0, 1.6, 0.5, 1080, 1920),
}
for name, (i, ss, d, fx, W, H) in C.items():
    f = f"{M}/v/{i}.mp4"
    vf = (f"scale='if(gt(a,{W}/{H}),-2,{W})':'if(gt(a,{W}/{H}),{H},-2)':flags=lanczos,"
          f"crop={W}:{H}:(iw-{W})*{fx}:(ih-{H})/2,setsar=1,{G}")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-t", str(d), "-i", f, "-vf", vf, *enc, f"{out}/{name}.mp4"], check=True)
    print("ok", name)
# under 1 s of face: "Hang pun geng mana?" -- points at the viewer, then looks into the lens. Selfie recording is mirrored -> hflip.
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "3.06", "-t", "0.92", "-i", main, "-vf",
                f"hflip,scale=1080:1920:flags=lanczos,setsar=1,{G}", *enc, f"{out}/face.mp4"], check=True)
print("ok face")
