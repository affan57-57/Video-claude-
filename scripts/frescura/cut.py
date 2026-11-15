import sys
from PIL import Image, ImageDraw, ImageFilter
src,out=sys.argv[1],sys.argv[2]
im=Image.open(src).convert('RGB').crop((180,560,1000,1760))
def mk(body,collar,stem,head,box):
    m=Image.new('L',im.size,0); d=ImageDraw.Draw(m)
    d.rounded_rectangle(body,radius=22,fill=255); d.rounded_rectangle(collar,radius=12,fill=255)
    d.rectangle(stem,fill=255); d.polygon(head,fill=255)
    m=m.filter(ImageFilter.GaussianBlur(1.6))
    c=im.copy(); c.putalpha(m); return c.crop(box)
a=mk((30,338,345,1021),(106,243,290,340),(160,95,235,250),[(62,78),(68,108),(98,112),(110,100),(256,100),(264,70),(250,56),(100,60),(72,64)],(10,40,365,1040))
b=mk((403,370,711,1038),(463,262,652,372),(510,110,585,270),[(418,95),(424,124),(452,128),(462,118),(622,118),(630,90),(618,76),(460,78),(430,84)],(388,60,730,1055))
a.save(out+'/bottle_noche.png'); b.save(out+'/bottle_glory.png'); print(a.size,b.size)
