"""Brighten + even the visible skin of the face shot (client: "cerah yang cantik dan flawless"), frame by frame.
Identity untouched: only exposure, gentle skin smoothing (edge-preserving), skin lift and a soft glow.
Usage: python3 face_glow.py IN.mp4 OUT.mp4"""
import sys, subprocess, os, glob, cv2, numpy as np
src, dst = sys.argv[1:3]
tmp = dst + ".frames"; os.makedirs(tmp, exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, f"{tmp}/%04d.png"], check=True)
for f in sorted(glob.glob(f"{tmp}/*.png")):
    bgr = cv2.imread(f); img = bgr.astype(np.float32) / 255
    ycc = cv2.cvtColor(bgr, cv2.COLOR_BGR2YCrCb)
    skin = cv2.inRange(ycc, (50, 135, 80), (255, 178, 135)).astype(np.float32) / 255
    skin = cv2.GaussianBlur(cv2.morphologyEx(skin, cv2.MORPH_OPEN, np.ones((7, 7))), (0, 0), 12)
    # 1) flawless: edge-preserving smoothing on skin, keep a little fine texture
    sm = cv2.bilateralFilter(bgr, 0, 28, 9).astype(np.float32) / 255
    det = img - cv2.GaussianBlur(img, (0, 0), 1.6)
    img = img * (1 - 0.6 * skin[..., None]) + (sm + det * 0.5) * (0.6 * skin[..., None])
    # 2) overall exposure lift (soft shoulder) + extra lift on skin, a touch less red
    img = 1 - (1 - img) ** 1.25
    lab = cv2.cvtColor(np.clip(img, 0, 1), cv2.COLOR_BGR2LAB)
    L = lab[..., 0] / 100
    lab[..., 0] = np.clip(L + 0.20 * skin * (1 - L) ** 1.1, 0, 1) * 100
    lab[..., 1] += 1.5 * skin          # fresh, slightly rosy
    lab[..., 2] += 2.0 * skin          # warm peach
    img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    # 3) soft luminous glow
    hi = np.clip((img - 0.5) / 0.5, 0, 1); bl = cv2.GaussianBlur(hi, (0, 0), 16)
    img = 1 - (1 - img) * (1 - bl * 0.16)
    # 4) restore crispness: gentle S-curve + clarity on luminance (eyes stay sharp)
    img = np.clip(img, 0, 1); img = img + 0.10 * (img - 0.5) * (1 - np.abs(img - 0.5) * 2)
    blur = cv2.GaussianBlur(img, (0, 0), 3); img = img + 0.35 * (img - blur) * (1 - skin[..., None] * 0.5)
    cv2.imwrite(f, (np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "30", "-i", f"{tmp}/%04d.png", "-c:v", "libx264", "-preset", "medium",
                "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", dst], check=True)
for f in glob.glob(f"{tmp}/*.png"): os.remove(f)
os.rmdir(tmp); print("ok", dst)
