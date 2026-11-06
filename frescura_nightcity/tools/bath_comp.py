# Composite the matted pump B-roll over a luxury minimalist bathroom with animated shower water + soft steam.
# Usage: bath_comp.py <alpha.mov> <bath_dir> <out.mp4> [preview_seconds]
import sys, subprocess, numpy as np, random
from PIL import Image, ImageFilter, ImageDraw
SRC, BD, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
LIMIT = float(sys.argv[4]) if len(sys.argv) > 4 else None
W, H, FPS = 1080, 1920, 30
SW, SH = 720, 1280
CUT1, XF = 9.833, 23.0  # hard cut (new shot) / crossfade into the shower view

def bg(name, box, blur, zoom=1.10):
    im = Image.open(f'{BD}/{name}.jpg').convert('RGB').crop(box)
    im = im.resize((int(W * zoom), int(H * zoom)), Image.LANCZOS).filter(ImageFilter.GaussianBlur(blur))
    a = np.asarray(im).astype(np.float32) / 255
    a = np.clip((a - .5) * 1.06 + .5, 0, 1) * np.array([1.03, 1.0, .95]) * .92   # warm, slightly dim
    return a
BGA = bg('3540719b', (250, 0, 610, 640), 3.5)            # counter, rain shower head, faucet, candle
BGB = bg('3540719b', (170, 230, 530, 870), 9)             # sink/faucet close, strong depth of field
BGC = bg('1c929dca', (322, 150, 682, 790), 7)             # glass shower + rain head
# shower heads in output coords (for animated water): (x, y, cone width, fall length)
HEADS = {'A': (180, 235, 120, 900), 'C': (876, 400, 150, 1150)}

def kenburns(a, t, t0, t1):
    p = min(1, max(0, (t - t0) / max(1e-3, t1 - t0)))
    z = 1.10 - .06 * p; h, w = a.shape[:2]
    cw, ch = int(W * 1.10 / z), int(H * 1.10 / z)
    cw, ch = min(cw, w), min(ch, h)
    x0, y0 = (w - cw) // 2, (h - ch) // 2
    crop = Image.fromarray((a[y0:y0 + ch, x0:x0 + cw] * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)
    return np.asarray(crop).astype(np.float32) / 255

rng = random.Random(3)
DROPS = [(rng.uniform(-1, 1), rng.uniform(0, 1), rng.uniform(.6, 1.0), rng.uniform(40, 110), rng.uniform(.10, .30)) for _ in range(90)]
STEAM = [(rng.uniform(0, W), rng.uniform(H * .3, H), rng.uniform(260, 520), rng.uniform(.035, .07), rng.uniform(20, 45)) for _ in range(7)]

def water_layer(t, head):
    hx, hy, cone, L = head
    img = Image.new('L', (W // 2, H // 2), 0); d = ImageDraw.Draw(img)
    for (u, ph, sp, ln, al) in DROPS:
        f = (ph + t * 2.4 * sp) % 1.0                  # progress down the fall
        y = hy + f * L; x = hx + u * cone * (0.35 + f)  # widening cone
        d.line([(x / 2, (y - ln) / 2), (x / 2, y / 2)], fill=int(255 * al * (1 - f * .6)), width=1)
    img = img.filter(ImageFilter.GaussianBlur(.8)).resize((W, H), Image.BILINEAR)
    return np.asarray(img).astype(np.float32)[..., None] / 255

def steam_layer(t):
    img = Image.new('L', (W // 4, H // 4), 0); d = ImageDraw.Draw(img)
    for (x, y, r, al, sp) in STEAM:
        yy = (y - t * sp) % (H * 1.2) - H * .1
        d.ellipse([(x - r) / 4, (yy - r * .6) / 4, (x + r) / 4, (yy + r * .6) / 4], fill=int(255 * al))
    img = img.filter(ImageFilter.GaussianBlur(14)).resize((W, H), Image.BILINEAR)
    return np.asarray(img).astype(np.float32)[..., None] / 255

shadow = Image.new('L', (W, H), 0); ImageDraw.Draw(shadow).ellipse([270, 1800, 720, 1868], fill=150)
SHADOW = np.asarray(shadow.filter(ImageFilter.GaussianBlur(22))).astype(np.float32)[..., None] / 255

dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', SRC], capture_output=True, text=True).stdout)
if LIMIT: dur = min(dur, LIMIT)
rd = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', SRC, '-t', f'{dur}', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-'], stdout=subprocess.PIPE)
wr = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-g', '15', OUT], stdin=subprocess.PIPE)
n = 0
while True:
    buf = rd.stdout.read(SW * SH * 4)
    if len(buf) < SW * SH * 4: break
    t = n / FPS
    fr = Image.frombuffer('RGBA', (SW, SH), buf, 'raw', 'RGBA', 0, 1).resize((W, H), Image.LANCZOS)
    f = np.asarray(fr).astype(np.float32) / 255
    rgb, al = f[..., :3], f[..., 3:4]
    al = np.asarray(Image.fromarray((al[..., 0] * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0))).astype(np.float32)[..., None] / 255
    if t >= 22.3:  # key out leftover teal-green table the matte kept in the lathering shot
        g = rgb[..., 1] - rgb[..., 0]; lum = rgb.mean(2)
        m = np.clip((g - .025) * 12, 0, 1) * np.clip((.72 - lum) * 5, 0, 1)
        m = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(3))).astype(np.float32) / 255
        al = al * (1 - m[..., None])
        lim = (rgb[..., 0] + rgb[..., 2]) / 2 + .02; rgb = rgb.copy(); rgb[..., 1] = np.minimum(rgb[..., 1], lim)   # despill
    rgb = np.clip((rgb - .5) * 1.05 + .5, 0, 1) * np.array([1.03, 1.0, .95]) * .95   # match warm bathroom light
    if t < CUT1:
        b = kenburns(BGA, t, 0, CUT1); b = b * (1 - SHADOW * .8)
        w = water_layer(t, HEADS['A']); b = b + (1 - b) * w * .9
    else:
        bB = kenburns(BGB, t, CUT1, XF + .6)
        if t < XF: b = bB
        else:
            bC = kenburns(BGC, t, XF, dur); wC = water_layer(t, HEADS['C']); bC = bC + (1 - bC) * wC * .9
            k = min(1, (t - XF) / .6); b = bB * (1 - k) + bC * k
    s = steam_layer(t); b = b + (1 - b) * s
    out = rgb * al + b * (1 - al)
    wr.stdin.write((np.clip(out, 0, 1) * 255).astype(np.uint8).tobytes()); n += 1
    if n % 60 == 0: print('frame', n, flush=True)
wr.stdin.close(); wr.wait(); rd.wait(); print('done', n)
