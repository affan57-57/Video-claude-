import os, sys
from PIL import Image
from rembg import remove, new_session
s = new_session("birefnet-general-lite")
for f in sys.argv[1:]:
    im = Image.open(f).convert("RGB")
    out = remove(im, session=s)
    bb = out.getbbox(); out = out.crop(bb)
    out.save(os.path.splitext(f)[0] + "_cut.png"); print("ok", f, out.size, flush=True)
