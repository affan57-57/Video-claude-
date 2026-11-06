# Prepare real night-city backgrounds: 9:16 cover crop (1242x2208, room for Ken Burns) + luxury night grade.
# Usage: prep_real.py <real_dir> <out_dir>
import sys, numpy as np
from PIL import Image, ImageFilter
R, O = sys.argv[1], sys.argv[2]
OW, OH = 1242, 2208

def crop916(im, fx=.5, fy=.5, box=None):
    if box: im = im.crop(box)
    w, h = im.size; tw = min(w, h * 9 / 16); th = tw * 16 / 9
    x = min(max(0, fx * w - tw / 2), w - tw); y = min(max(0, fy * h - th / 2), h - th)
    return im.crop((int(x), int(y), int(x + tw), int(y + th))).resize((OW, OH), Image.LANCZOS)

def grade(im, expo=1.0, warm=.0, contrast=1.08, sat=1.0, night=False):
    a = np.asarray(im.convert('RGB')).astype(np.float32) / 255
    if night:  # day-for-night: crush sky/brights into navy, keep structure, add warm window glints
        L = a.mean(2, keepdims=True); S = a.max(2, keepdims=True) - a.min(2, keepdims=True)
        sky = np.clip((L - .55) * 3, 0, 1) * np.clip(1 - S * 2.2, 0, 1)
        sky = np.asarray(Image.fromarray((sky[..., 0] * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(18))).astype(np.float32)[..., None] / 255
        h = a.shape[0]; grad = np.linspace(0, 1, h)[:, None, None]
        navy = np.concatenate([.02 + .06 * grad, .03 + .07 * grad, .09 + .14 * grad], 2) * np.ones_like(a)
        body = (a ** 1.6) * np.array([.42, .48, .70])
        a = body * (1 - sky) + navy * sky
        a = np.clip(a * 1.25, 0, 1)
    a = np.clip((a - .5) * contrast + .5, 0, 1) * expo
    g = a.mean(2, keepdims=True); a = g + (a - g) * sat
    a[..., 0] *= 1 + warm; a[..., 2] *= 1 - warm * .6
    # vignette
    h, w = a.shape[:2]; yy, xx = np.mgrid[0:h, 0:w]
    v = 1 - .55 * np.clip(((xx / w - .5) ** 2 * 1.4 + (yy / h - .48) ** 2 * 1.1) * 2.2, 0, 1)
    a = a * v[..., None]
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))

jobs = {
 'klcc_hero':  (f'{R}/full/klcc_4e5909be.jpg', dict(fx=.5, fy=.45), dict(expo=.92, warm=.04)),
 'klcc_up':    (f'{R}/cm/klcc_night.jpg', dict(fx=.5, fy=.5), dict(expo=.95, warm=.02, contrast=1.12)),
 'ramlee':     (f'{R}/cm/ramlee.jpg', dict(fx=.62, fy=.5), dict(expo=.9, warm=.05)),
 'kl_skyline': (f'{R}/cm/kl_goodnight.jpg', dict(fx=.5, fy=.5, box=None), dict(expo=1.05, warm=.03)),
 'bb_street':  (f'{R}/full/bb_67a8ce7c.jpg', dict(fx=.5, fy=.5), dict(expo=.9, warm=.04)),
 'klcc_cloud': (f'{R}/full/klcc_0a9b7277.jpg', dict(fx=.5, fy=.5), dict(expo=.95, warm=.02)),
 'penang_lights': (f'{R}/full/komtar_6977c63c.jpg', dict(fx=.55, fy=.5), dict(expo=1.0, warm=.03)),
 'komtar_n':   (f'{R}/full/komtar_32506c22.jpg', dict(fx=.55, fy=.45), dict(night=True, contrast=1.1)),
 'alor_n':     (f'{R}/full/alor_6c427726.jpg', dict(fx=.5, fy=.4), dict(night=True, contrast=1.1)),
 'alor_hdr_n': (f'{R}/full/alor_d4c75544.jpg', dict(fx=.5, fy=.45), dict(night=True, contrast=1.1)),
}
for k, (src, c, g) in jobs.items():
    im = Image.open(src).convert('RGB')
    if k == 'kl_skyline':
        w, h = im.size; c['box'] = (int(w * .25), int(h * .28), int(w * .63), int(h * .93))
    out = grade(crop916(im, **c), **g)
    out.save(f'{O}/{k}.jpg', quality=90); print(k, im.size)
