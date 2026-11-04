"""Composite background-removed pump footage (RGBA PNG sequence) onto a luxury studio backdrop.
Usage: python3 -I compose_pump.py FRAMES_DIR OUT.mp4 [FOCUS_X FOCUS_Y]   (spotlight centre, 0..1)
The subject's own pixels are untouched; only the beach background is replaced."""
import subprocess, sys
import numpy as np
from PIL import Image, ImageFilter
fr, out = sys.argv[1:3]
fx, fy = (float(sys.argv[3]), float(sys.argv[4])) if len(sys.argv) > 4 else (0.5, 0.45)
W, H = 1080, 1920
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
base = np.array([11, 9, 7], np.float32)
d = np.sqrt(((xx - fx * W) / (W * 0.62)) ** 2 + ((yy - fy * H) / (H * 0.42)) ** 2)
spot = np.clip(1 - d, 0, 1) ** 1.8
img = base + spot[..., None] * np.array([92, 64, 38], np.float32)          # warm champagne glow
beam = np.clip(1 - np.abs((xx - 0.78 * W) + (yy - 0.0) * 0.45) / 260, 0, 1) * np.clip(1 - yy / (H * 0.9), 0, 1)
img += beam[..., None] * np.array([30, 24, 16], np.float32)                 # soft diagonal light beam
floor = np.clip((yy - H * 0.80) / (H * 0.2), 0, 1)
img *= (1 - 0.45 * floor)[..., None]
noise = np.random.default_rng(1).normal(0, 2.0, (H, W, 1))                   # anti-banding dither
bg = Image.fromarray(np.clip(img + noise, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1))
bgp = out.rsplit(".", 1)[0] + "_bg.png"
bg.save(bgp)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", bgp, "-framerate", "30", "-i", f"{fr}/%04d.png",
                "-filter_complex", "[1]scale=1080:-2:flags=lanczos,format=rgba[fg];[0][fg]overlay=0:(H-h)/2:shortest=1,"
                "format=yuv420p", "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-an",
                "-movflags", "+faststart", out], check=True)
print("ok", out)
