# Turn chrome fixtures in the bathroom photos into brushed gold (subtle, only inside hand-placed boxes).
import sys, numpy as np
from PIL import Image, ImageFilter
BD = sys.argv[1]
REG = {
 '3540719b': [(395, 325, 585, 378), (540, 370, 602, 655), (262, 48, 352, 110), (284, 222, 322, 268)],
 '1c929dca': [(146, 366, 230, 664), (329, 212, 347, 828), (570, 266, 664, 302), (610, 368, 664, 434), (580, 532, 682, 568)],
}
def gold(lum):
    # dark bronze -> warm gold -> pale highlight
    lo, mid, hi = np.array([.30, .20, .08]), np.array([.86, .66, .34]), np.array([1.0, .94, .76])
    l = lum[..., None]
    return np.where(l < .55, lo + (mid - lo) * (l / .55), mid + (hi - mid) * ((l - .55) / .45))
for name, boxes in REG.items():
    im = Image.open(f'{BD}/{name}.jpg').convert('RGB'); a = np.asarray(im).astype(np.float32) / 255
    lum = a.mean(2); sat = a.max(2) - a.min(2)
    L8 = Image.fromarray((lum * 255).astype(np.uint8))
    mu = np.asarray(L8.filter(ImageFilter.BoxBlur(3))).astype(np.float32) / 255
    mu2 = np.asarray(Image.fromarray((np.clip(lum ** 2, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.BoxBlur(3))).astype(np.float32) / 255
    std = np.sqrt(np.clip(mu2 - mu ** 2, 0, 1))
    e = ((std > .055) & (sat < .25)).astype(np.uint8) * 255
    e = Image.fromarray(e).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))   # close small gaps inside tubes
    metal = np.asarray(e) > 127
    box = np.zeros_like(metal)
    for (x0, y0, x1, y1) in boxes: box[y0:y1, x0:x1] = True
    m = (metal & box).astype(np.float32)
    if name == '3540719b':   # rain-shower head plate: fill as solid gold disc
        from PIL import ImageDraw
        e2 = Image.new('L', (a.shape[1], a.shape[0]), 0); ImageDraw.Draw(e2).ellipse((268, 54, 346, 98), fill=255)
        m = np.maximum(m, np.asarray(e2).astype(np.float32) / 255 * .85)
    m = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0))).astype(np.float32)[..., None] / 255
    m = m * box[..., None]
    out = a * (1 - m * .92) + gold(np.clip(lum * 1.05, 0, 1)) * m * .92
    Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)).save(f'{BD}/{name}_gold.jpg', quality=95)
    print(name, int(m.sum()))
