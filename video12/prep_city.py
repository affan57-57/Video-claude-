"""Video 12 v2: night-city photos/videos from Wikimedia Commons (CC licences, see EDIT_PLAN) -> project/assets/city.
Portrait photos are cover-cropped to 1188x2112 (10% margin for a slow push); panoramas are scaled to 1920 px high for a sideways pan.
Usage: python3 -I prep_city.py COMMONS_DIR OUT_DIR"""
import os, subprocess, sys
from PIL import Image, ImageEnhance
src, out = sys.argv[1:3]
os.makedirs(out, exist_ok=True)
def cover(name, fx=0.5, fy=0.5, W=1188, H=2112):
    im = Image.open(f"{src}/hi/{name}.jpg").convert("RGB")
    s = max(W / im.width, H / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = round((im.width - W) * fx); y = round((im.height - H) * fy)
    im = im.crop((x, y, x + W, y + H)); im = ImageEnhance.Contrast(im).enhance(1.06)
    im.save(f"{out}/{name}.jpg", quality=90); print("ok", name, im.size)
def pano(name, H=1920):
    im = Image.open(f"{src}/hi/{name}.jpg").convert("RGB")
    s = H / im.height; im = im.resize((round(im.width * s), H), Image.LANCZOS); im = ImageEnhance.Contrast(im).enhance(1.06)
    im.save(f"{out}/{name}.jpg", quality=88); print("ok", name, im.size)
pf = Image.open(f"{src}/hi/pav_front.jpg").convert("RGB")   # crop to the PAVILION sign + LED facade (no shop adverts)
h = 1480; w = round(h * 1188 / 2112); x = (pf.width - w) // 2
pf.crop((x, 0, x + w, h)).resize((1188, 2112), Image.LANCZOS).save(f"{out}/pav_front.jpg", quality=90); print("ok pav_front (sign crop)")
cover("pav_in1", 0.45); cover("pav_in2", 0.55)
cover("klcc_bridge", 0.5, 0.5); cover("trx_crown", 0.5, 0.3)
tc = Image.open(f"{out}/trx_crown.jpg")                      # dusk sky -> night: darker, deeper blue, LED crown kept bright
tc = ImageEnhance.Brightness(tc).enhance(0.62); tc = ImageEnhance.Contrast(tc).enhance(1.2); tc = ImageEnhance.Color(tc).enhance(1.15)
tc.save(f"{out}/trx_crown.jpg", quality=90); print("ok trx_crown (night grade)")
cover("trx_tower", 0.45, 0.3); cover("kltower_merdeka", 0.5, 0.35)
pano("sky2022"); pano("sky2024")
enc = ["-an", "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
# Kuala Lumpur Tower light show (portrait): zoom in on the tower through the window
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "0.3", "-t", "6.8", "-i", f"{src}/kltower.webm", "-vf",
                "crop=640:1138:(iw-640)*0.46:40,scale=1080:1920:flags=lanczos,setsar=1,eq=contrast=1.05:saturation=1.1", *enc, f"{out}/kltower_led.mp4"], check=True)
print("ok kltower_led")
