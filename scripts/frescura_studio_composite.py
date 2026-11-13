import cv2, numpy as np
src=cv2.imread('/root/.claude/uploads/c4c5ab1f-3904-5231-9785-20e7ddb4f867/3e5ce6a6-image.jpg').astype(np.float32)/255
H0,W0=src.shape[:2]
# ---- mask: grabcut for pump/cap + geometric body
gc=np.zeros((H0,W0),np.uint8)
m=cv2.imread('mask.png',0); gc[500:1620,170:580]=m
gc[900:,:]=0
body=np.zeros_like(gc)
x0,y0,x1,y1,r=191,887,550,1636,22
cv2.rectangle(body,(x0+r,y0),(x1-r,y1),255,-1); cv2.rectangle(body,(x0,y0+r),(x1,y1-r),255,-1)
for cx,cy in [(x0+r,y0+r),(x1-r,y0+r),(x0+r,y1-r),(x1-r,y1-r)]: cv2.circle(body,(cx,cy),r,255,-1)
mask=np.maximum(gc,body)
mask=cv2.erode(mask,np.ones((3,3),np.uint8))
alpha=cv2.GaussianBlur(mask.astype(np.float32)/255,(0,0),1.2)
bx0,by0,bx1,by1=180,500,565,1645
B=src[by0:by1,bx0:bx1].copy(); A=alpha[by0:by1,bx0:bx1]
# ---- relight bottle: cool, directional falloff
h,w=A.shape
xx=np.linspace(0,1,w)[None,:]; yy=np.linspace(0,1,h)[:,None]
light=1.18-0.36*xx-0.08*yy           # key from upper left
Bl=B*light[...,None]
# neutralise warm wood tint on plastic edges & cap
Bl=Bl*np.array([1.04,0.98,0.95])     # BGR slight cool
# rim light on right edge
edge=cv2.GaussianBlur((A>0.5).astype(np.float32),(0,0),6)
rim=np.clip((A-edge)*3,0,1)*(xx>0.6)
Bl=Bl+rim[...,None]*np.array([0.55,0.35,0.25])*0.6
Bl=np.clip(Bl,0,1).astype(np.float32)
np.save('cut_noche.npy',np.dstack([Bl,A]))
s=0.80
Bs=cv2.resize(Bl,None,fx=s,fy=s,interpolation=cv2.INTER_AREA); As=cv2.resize(A,None,fx=s,fy=s,interpolation=cv2.INTER_AREA)
bh,bw=As.shape
# ---- scene 1600x2000
W,H=1600,2000
X,Y=np.meshgrid(np.arange(W),np.arange(H))
navy=np.array([0.36,0.19,0.085])     # BGR midnight navy
deep=np.array([0.10,0.045,0.02])
horizon=1640
d=np.sqrt(((X-620)/1250)**2+((Y-900)/1350)**2)
g=np.clip(1-d,0,1)**1.3
bg=deep[None,None]+ (navy-deep)[None,None]*g[...,None]
floor=(Y>horizon); 
fl=np.clip((Y-horizon)/300,0,1)
bg[floor]*= (0.80+0.25*np.exp(-((Y[floor]-horizon)/90.)))[...,None]*(1-0.45*fl[floor])[...,None]
img=bg.astype(np.float32)
cx=W//2
ped_top=1500
def shade(region,col): img[region]=col
# pedestal geometry: upper block and lower step, with small top faces
U=(cx-290,cx+290,ped_top,ped_top+200); L=(cx-430,cx+430,ped_top+200,ped_top+330)
# ---- long shadows (light from upper-left -> to right)
sh=np.zeros((H,W),np.float32)
# pedestal shadow on floor/wall
pts=np.array([[U[1],U[2]],[U[1]+520,U[2]-260],[U[1]+520,L[3]],[U[1],L[3]]],np.int32)
cv2.fillPoly(sh,[pts],1)
pts2=np.array([[L[1],L[2]],[L[1]+460,L[2]-200],[L[1]+460,L[3]],[L[1],L[3]]],np.int32)
cv2.fillPoly(sh,[pts2],1)
# bottle shadow: shear mask onto wall, up-right
bm=np.zeros((H,W),np.float32)
ox=cx-bw//2; oy=ped_top-bh
bm[oy:oy+bh,ox:ox+bw]=As
M=np.float32([[1,0.0,0],[0,1,0]])
# long shadow: stretch horizontally & shift right
Ms=np.float32([[1.0,-0.95,ped_top*0.95],[0,0.92,ped_top*0.08]])
bsh=cv2.warpAffine(bm,Ms,(W,H))
sh=np.maximum(sh,bsh)
sh=cv2.GaussianBlur(sh,(0,0),3.5)
img*= (1-0.70*sh)[...,None]
# draw pedestal (matte black, faces)
def face(x0,x1,y0,y1,top,bot,grad_x=True):
    xs=np.linspace(0,1,x1-x0)[None,:]; ys=np.linspace(0,1,y1-y0)[:,None]
    v=top+(bot-top)*ys
    v=v*(1.12-0.35*xs)
    img[y0:y1,x0:x1]=np.array([1.0,0.98,1.0])[None,None]*v[...,None]
face(L[0],L[1],L[2],L[3],0.075,0.035)
face(L[0],L[1],L[2],L[2]+18,0.17,0.11)   # lower top face
face(U[0],U[1],U[2],U[3],0.085,0.040)
face(U[0],U[1],U[2],U[2]+20,0.22,0.14)   # upper top face
# crisp highlight edges
img[U[2]:U[2]+2,U[0]:U[1]]*=1.9; img[L[2]:L[2]+2,L[0]:L[1]]*=1.6
img[U[2]:U[3],U[0]:U[0]+2]*=1.5; img[L[2]:L[3],L[0]:L[0]+2]*=1.4
# reflection of bottle on pedestal top (subtle)
ref=np.flipud(Bs[-60:]); refa=np.flipud(As[-60:])*np.linspace(0.18,0,60)[:,None]
ry=U[2]+1; rx=ox
img[ry:ry+16,rx:rx+bw]=img[ry:ry+16,rx:rx+bw]*(1-refa[:16,...,None])+ref[:16]*refa[:16,...,None]
# contact shadow
cs=np.zeros((H,W),np.float32); cv2.ellipse(cs,(cx+10,ped_top+3),(bw//2+6,6),0,0,360,1,-1)
cs=cv2.GaussianBlur(cs,(0,0),4); img*=(1-0.7*cs)[...,None]
# bottle
img[oy:oy+bh,ox:ox+bw]=img[oy:oy+bh,ox:ox+bw]*(1-As[...,None])+Bs*As[...,None]
# light spill: faint pink glow through liquid onto top face
glow=np.zeros((H,W),np.float32); cv2.ellipse(glow,(cx+40,ped_top+8),(bw//2+40,10),0,0,360,1,-1)
glow=cv2.GaussianBlur(glow,(0,0),10)*(1-cs)
img+=glow[...,None]*np.array([0.10,0.02,0.16])*0.5
# grade: vignette + grain
v=np.clip(1-0.35*(((X-W*0.45)/W)**2+((Y-H*0.45)/H)**2)*2.2,0,1)
img*=v[...,None]
img+=np.random.default_rng(1).normal(0,0.006,img.shape)
out=(np.clip(img,0,1)**(1/1.02)*255).astype(np.uint8)
cv2.imwrite('/home/user/Video-claude-/output/frescura_noche_studio_4x5.png',out)
cv2.imwrite('preview.jpg',cv2.resize(out,(800,1000)))
