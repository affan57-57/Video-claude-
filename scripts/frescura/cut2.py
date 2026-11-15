import sys, numpy as np
from rembg import remove, new_session
from PIL import Image
from scipy import ndimage
src,dst,model=sys.argv[1:4]
im=Image.open(src).convert("RGB")
m=np.array(remove(im, session=new_session(model), only_mask=True)).astype(float)/255
b=m>0.5
b=ndimage.binary_closing(b, iterations=6); b=ndimage.binary_fill_holes(b)
lab,n=ndimage.label(b); sizes=ndimage.sum(b,lab,range(1,n+1)); b=lab==(np.argmax(sizes)+1)
a=ndimage.gaussian_filter(b.astype(float),1.2)
out=np.dstack([np.array(im),(a*255).astype(np.uint8)])
Image.fromarray(out,"RGBA").save(dst); print(dst, b.mean())
