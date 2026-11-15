from rembg import remove, new_session
from PIL import Image
im=Image.open("img/duo_flat.jpg").convert("RGB")
for mdl in ["isnet-general-use","u2net"]:
  s=new_session(mdl)
  for name,box in [("noche",(170,590,560,1640)),("wg",(560,590,960,1700))]:
    c=im.crop(box); o=remove(c,session=s,post_process_mask=True)
    o.save(f"img/{name}_{mdl}.png")
c=Image.new('RGB',(1600,1110),(60,140,60)); x=0
for mdl in ["isnet-general-use","u2net"]:
  for n in ["noche","wg"]:
    a=Image.open(f"img/{n}_{mdl}.png"); c.paste(a,(x,0),a); x+=400
c.save("peek/cuts.jpg")
