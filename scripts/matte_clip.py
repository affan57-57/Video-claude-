"""Cut the subject out of every frame of a clip (BiRefNet via rembg) -> RGBA PNG sequence.
Usage: python3 matte_clip.py IN.mp4 SS DUR OUT_DIR"""
import os, subprocess, sys, glob
from PIL import Image
from rembg import remove, new_session
src, ss, dur, out = sys.argv[1:5]
os.makedirs(out + "/src", exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", ss, "-t", dur, "-i", src, "-vf", "fps=30",
                f"{out}/src/%04d.png"], check=True)
s = new_session("birefnet-general-lite")
fs = sorted(glob.glob(f"{out}/src/*.png"))
for i, f in enumerate(fs):
    dst = f"{out}/{os.path.basename(f)}"
    if os.path.exists(dst):
        continue
    remove(Image.open(f).convert("RGB"), session=s).save(dst)
    print(f"{i+1}/{len(fs)}", flush=True)
print("DONE", flush=True)
