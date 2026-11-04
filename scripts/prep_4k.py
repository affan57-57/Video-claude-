"""Build 2160x3840 versions of every clip the composition uses (for the 4K master).
AI-upscales (Real-ESRGAN) the low-res sources; native 4K/1080 sources are lanczos-resized.
Usage: python3 -I prep_4k.py SOURCE.mp4 MIXKIT_DIR MODEL.pth OUT_DIR"""
import os, subprocess, sys
src, mk, model, out = sys.argv[1:5]
here = os.path.dirname(os.path.abspath(__file__))
os.makedirs(out, exist_ok=True)
W, H = 2160, 3840
def best(n):
    for r in ("v2160", "v1080", "v"):
        p = f"{mk}/{r}/{n}.mp4"
        if os.path.exists(p) and os.path.getsize(p) > 10000:
            return p
# name: (mixkit id or None for the talking-head source, media start, used duration, h-focus, mode)
CLIPS = {
    "face":       (None,  0.18, 2.1, 0.5,  "ai"),
    "gel":        (21769, 0.5,  1.2, 0.55, "ai"),
    "lather":     (33705, 3.0,  3.0, 0.32, "ai"),
    "perfume":    (20766, 0.3,  2.6, 0.78, "ai"),
    "stream":     (34517, 1.0,  3.1, 0.40, "ai"),
    "berries":    (15973, 0.5,  3.1, 0.50, "ai"),
    "shower":     (21766, 2.0,  3.8, 0.30, "ai"),
    "lab":        (17556, 0.5,  6.4, 0.38, "lanczos"),   # soft bokeh, sits under the panel
    "bubbles":    (44812, 1.0,  3.2, 0.50, "lanczos"),   # native 4K
    "irid":       (44834, 1.0,  3.3, 0.50, "lanczos"),   # native 4K
    "scientist":  (4719,  1.0,  3.7, 0.50, "lanczos"),   # native 4K
    "pinkbubble": (13787, 2.0,  2.2, 0.50, "lanczos"),   # 1080x1920
    "flowers":    (1168,  2.0,  4.7, 0.50, "lanczos"),   # 1080x1920
    "phone":      (42136, 0.5,  6.3, 0.50, "lanczos"),   # 1080x1920, blurred in comp
}
only = sys.argv[5:] or list(CLIPS)
for name in only:
    n, ss, d, fx, mode = CLIPS[name]
    f = src if n is None else best(n)
    dst = f"{out}/{name}.mp4"
    if n is None:
        pre = "hflip"
    else:  # vertical 9:16 crop at source resolution
        iw, ih = map(int, subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries",
                     "stream=width,height", "-of", "csv=p=0", f], capture_output=True, text=True).stdout.split(","))
        cw = min(iw, ih * 9 // 16) // 2 * 2
        pre = f"crop={cw}:{ih}:{int((iw - cw) * fx)}:0"
    if mode == "ai":
        subprocess.run([sys.executable, "-I", f"{here}/ai_upscale.py", model, "video", f, dst,
                        str(ss), str(d), pre, str(W), str(H)], check=True)
    else:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-t", str(d), "-i", f, "-vf",
                        f"{pre},scale={W}:{H}:flags=lanczos,unsharp=5:5:0.4,setsar=1,fps=30,"
                        "eq=saturation=1.12:contrast=1.04", "-an", "-c:v", "libx264", "-preset", "slow",
                        "-crf", "15", "-pix_fmt", "yuv420p", "-movflags", "+faststart", dst], check=True)
    print("done", name, f, flush=True)
