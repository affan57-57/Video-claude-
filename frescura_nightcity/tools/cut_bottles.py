import sys, numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage as nd
P = sys.argv[1]
im = Image.open(P + 'duo.jpg').convert('RGB'); a = np.asarray(im).astype(np.float32); H, W = a.shape[:2]
R, G, B = a[..., 0], a[..., 1], a[..., 2]; mx = a.max(2); mn = a.min(2)
white = ((mx - mn) < 38) & (mx > 175)          # white pump plastic
spec = {  # body (x0,y0,x1,y1,r), pump rects (x0,y0,x1,y1)
 'noche': ((205, 896, 531, 1602, 26), [(236, 612, 436, 690), (330, 670, 420, 810), (280, 795, 475, 905)]),
 'bombshell': ((579, 924, 897, 1598, 24), [(594, 632, 810, 700), (690, 680, 785, 830), (640, 818, 835, 930)]),
}
for name, (body, pumps) in spec.items():
    m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m)
    x0, y0, x1, y1, r = body; d.rounded_rectangle((x0, y0, x1, y1), r, fill=255)
    mb = np.asarray(m) > 0
    mp = np.zeros_like(mb)
    for (px0, py0, px1, py1) in pumps: mp[py0:py1, px0:px1] = True
    mp = mp & white
    mp = nd.binary_opening(mp, iterations=1); mp = nd.binary_closing(mp, iterations=4); mp = nd.binary_fill_holes(mp)
    lab, n = nd.label(mp); 
    if n: sizes = nd.sum(mp, lab, range(1, n + 1)); mp = lab == (np.argmax(sizes) + 1)
    mask = mb | mp
    alpha = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0))
    rgba = im.copy(); rgba.putalpha(alpha)
    ys, xs = np.where(mask); box = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
    c = rgba.crop(box); c.save(P + f'{name}.png'); print(name, box, c.size)
    bg = Image.new('RGBA', c.size, (15, 20, 45, 255)); bg.alpha_composite(c); bg.convert('RGB').save(P + f'{name}_chk.jpg')
