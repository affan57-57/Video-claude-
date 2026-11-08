import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as ndi
def fix(src,cut,dst,dx,dy):
    rgb=np.asarray(Image.open(src).convert('RGB')).astype(np.float32)/255
    a=np.asarray(Image.open(cut))[...,3].astype(np.float32)/255
    H,W=a.shape; mx=rgb.max(2); mn=rgb.min(2); sat=(mx-mn)/(mx+1e-6)
    white=(mx>0.62)&(sat<0.22)
    reg=np.zeros((H,W),bool)
    # old-grid rects (x0,y0,x1,y1) -> shift
    for x0,y0,x1,y1 in [(44,368,305,445),(146,400,272,606),(96,596,330,735)]:
        reg[max(0,y0+dy):y1+dy, max(0,x0+dx):x1+dx]=True
    m=white&reg
    m=ndi.binary_closing(m,iterations=3); m=ndi.binary_fill_holes(m); m=ndi.binary_opening(m,iterations=2)
    lab,n=ndi.label(m); 
    if n: sizes=ndi.sum(m,lab,range(1,n+1)); m=np.isin(lab,1+np.where(sizes>sizes.max()*0.05)[0])
    pm=np.asarray(Image.fromarray((m*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))).astype(np.float32)/255
    alpha=np.maximum(a,pm)
    out=np.dstack([rgb*255,alpha*255]).astype(np.uint8); im=Image.fromarray(out,'RGBA'); im=im.crop(im.getbbox()); im.save(dst); print(dst,im.size)
fix('crop_noche.png','noche_cut.png','noche_full.png',15,-190)
fix('crop_wg.png','wg_cut.png','wg_full.png',-5,-190)
