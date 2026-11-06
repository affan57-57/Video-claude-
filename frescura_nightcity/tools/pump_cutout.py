# Export the pump B-roll with NO background, original colours (no grade):
#  - <out>_transparent.webm  (VP9 + alpha)
#  - <out>_putih.mp4         (clean white background)
#  - <out>_bluescreen.mp4    (solid blue for chroma key; blue because the sleeve is sage green)
import sys, subprocess, numpy as np
from PIL import Image, ImageFilter
import warnings; warnings.filterwarnings('ignore')
from scipy import ndimage as nd
SRC, OUT = sys.argv[1], sys.argv[2]
SW, SH, W, H, FPS = 720, 1280, 1080, 1920, 30
rd = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', SRC, '-f', 'rawvideo', '-pix_fmt', 'rgba', '-'], stdout=subprocess.PIPE)
def enc(args, pix_in):
    return subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', pix_in, '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-'] + args, stdin=subprocess.PIPE)
w_alpha = enc(['-c:v', 'libvpx-vp9', '-pix_fmt', 'yuva420p', '-b:v', '0', '-crf', '28', '-row-mt', '1', '-deadline', 'good', '-cpu-used', '4', '-auto-alt-ref', '0', OUT + '_transparent.webm'], 'rgba')
w_white = enc(['-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-pix_fmt', 'yuv420p', OUT + '_putih.mp4'], 'rgb24')
w_blue = enc(['-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-pix_fmt', 'yuv420p', OUT + '_bluescreen.mp4'], 'rgb24')
WHITE = np.array([248, 246, 243], np.float32) / 255; BLUE = np.array([0, 71, 187], np.float32) / 255
n = 0
while True:
    buf = rd.stdout.read(SW * SH * 4)
    if len(buf) < SW * SH * 4: break
    t = n / FPS
    f = np.asarray(Image.frombuffer('RGBA', (SW, SH), buf, 'raw', 'RGBA', 0, 1)).astype(np.float32) / 255
    rgb, al = f[..., :3].copy(), f[..., 3]
    if t >= 22.3:  # leftover teal table in the lathering shot: key out + despill
        g = rgb[..., 1] - rgb[..., 0]; lum = rgb.mean(2)
        m = np.clip((g - .025) * 12, 0, 1) * np.clip((.72 - lum) * 5, 0, 1)
        m = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(2))).astype(np.float32) / 255
        al = al * (1 - m)
        rgb[..., 1] = np.minimum(rgb[..., 1], (rgb[..., 0] + rgb[..., 2]) / 2 + .02)
    # bottle label/plastic made solid: red-dominant pixels (closed to cover the black label + text) inside the subject's area
    red = ((rgb[..., 0] - np.maximum(rgb[..., 1], rgb[..., 2]) > .15) & (rgb[..., 0] > .25)).astype(np.uint8) * 255
    red = np.asarray(Image.fromarray(red).resize((SW // 2, SH // 2)).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5)).resize((SW, SH))).astype(np.float32) / 255
    near = np.asarray(Image.fromarray((al * 255).astype(np.uint8)).resize((SW // 2, SH // 2)).filter(ImageFilter.MaxFilter(5)).resize((SW, SH))).astype(np.float32) / 255
    al = np.maximum(al, red * (near > .1))
    if t < 9.83: al[1237:, :] = 0                       # table strip under the bottle in the first shot
    al = np.asarray(Image.fromarray((al * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.6))).astype(np.float32) / 255
    al = np.clip((al - .30) / .40, 0, 1)                # firm subject: faint haze removed, partial areas made solid
    # drop small floating fragments: keep connected parts larger than 1.2% of the frame
    lab, nlab = nd.label(al > .5)
    if nlab > 1:
        sizes = nd.sum(np.ones_like(al), lab, range(1, nlab + 1))
        keep = np.isin(lab, np.where(sizes > .012 * al.size)[0] + 1)
        keep = nd.binary_dilation(keep, iterations=3)
        al = al * keep
    big = Image.fromarray((np.dstack([rgb, al]) * 255 + .5).clip(0, 255).astype(np.uint8), 'RGBA').resize((W, H), Image.LANCZOS)
    f2 = np.asarray(big).astype(np.float32) / 255; rgb, al = f2[..., :3], f2[..., 3]
    A = al[..., None]
    w_alpha.stdin.write((np.dstack([rgb, al]) * 255 + .5).clip(0, 255).astype(np.uint8).tobytes())
    w_white.stdin.write(((rgb * A + WHITE * (1 - A)) * 255 + .5).clip(0, 255).astype(np.uint8).tobytes())
    w_blue.stdin.write(((rgb * A + BLUE * (1 - A)) * 255 + .5).clip(0, 255).astype(np.uint8).tobytes())
    n += 1
    if n % 120 == 0: print('frame', n, flush=True)
for w in (w_alpha, w_white, w_blue): w.stdin.close(); w.wait()
rd.wait(); print('done', n)
