import cv2, numpy as np
s=0.68
bottles=[]
for name,glowc in [('noche',[0.10,0.02,0.16]),('bomb',[0.02,0.02,0.20])]:
    c=np.load(f'cut_{name}.npy').astype(np.float32)
    c=cv2.resize(c,None,fx=s,fy=s,interpolation=cv2.INTER_AREA)
    bottles.append((c[...,:3],c[...,3],np.array(glowc)))
W,H=1600,2000
X,Y=np.meshgrid(np.arange(W),np.arange(H))
navy=np.array([0.36,0.19,0.085]); deep=np.array([0.10,0.045,0.02])
horizon=1640
d=np.sqrt(((X-620)/1250)**2+((Y-900)/1350)**2)
g=np.clip(1-d,0,1)**1.3
img=(deep[None,None]+(navy-deep)[None,None]*g[...,None]).astype(np.float32)
floor=Y>horizon; fl=np.clip((Y-horizon)/300,0,1)
img[floor]*=((0.80+0.25*np.exp(-((Y[floor]-horizon)/90.)))*(1-0.45*fl[floor]))[...,None]
cx=W//2; ped_top=1480
U=(cx-390,cx+390,ped_top,ped_top+210); L=(cx-530,cx+530,ped_top+210,ped_top+350)
gap=56
bw0=bottles[0][1].shape[1]; bw1=bottles[1][1].shape[1]
xs=[cx-gap//2-bw0, cx+gap//2]
# shadows
sh=np.zeros((H,W),np.float32)
cv2.fillPoly(sh,[np.array([[U[1],U[2]],[U[1]+480,U[2]-250],[U[1]+480,L[3]],[U[1],L[3]]],np.int32)],1)
cv2.fillPoly(sh,[np.array([[L[1],L[2]],[L[1]+420,L[2]-190],[L[1]+420,L[3]],[L[1],L[3]]],np.int32)],1)
Ms=np.float32([[1.0,-0.95,ped_top*0.95],[0,0.92,ped_top*0.08]])
bm=np.zeros((H,W),np.float32)
for (B,A,_),ox in zip(bottles,xs):
    bh,bw=A.shape; bm[ped_top-bh:ped_top,ox:ox+bw]=np.maximum(bm[ped_top-bh:ped_top,ox:ox+bw],A)
sh=np.maximum(sh,cv2.warpAffine(bm,Ms,(W,H)))
sh=cv2.GaussianBlur(sh,(0,0),3.5)
img*=(1-0.70*sh)[...,None]
def face(x0,x1,y0,y1,top,bot):
    xx=np.linspace(0,1,x1-x0)[None,:]; yy=np.linspace(0,1,y1-y0)[:,None]
    v=(top+(bot-top)*yy)*(1.12-0.35*xx)
    img[y0:y1,x0:x1]=np.array([1.0,0.98,1.0])[None,None]*v[...,None]
face(L[0],L[1],L[2],L[3],0.075,0.035); face(L[0],L[1],L[2],L[2]+18,0.17,0.11)
face(U[0],U[1],U[2],U[3],0.085,0.040); face(U[0],U[1],U[2],U[2]+20,0.22,0.14)
img[U[2]:U[2]+2,U[0]:U[1]]*=1.9; img[L[2]:L[2]+2,L[0]:L[1]]*=1.6
img[U[2]:U[3],U[0]:U[0]+2]*=1.5; img[L[2]:L[3],L[0]:L[0]+2]*=1.4
# left bottle casts shadow onto right bottle's left part (light from upper-left)
for i,((B,A,glowc),ox) in enumerate(zip(bottles,xs)):
    bh,bw=A.shape; oy=ped_top-bh
    ref=np.flipud(B[-60:]); ra=np.flipud(A[-60:])*np.linspace(0.18,0,60)[:,None]
    sl=img[ped_top+1:ped_top+17,ox:ox+bw]; img[ped_top+1:ped_top+17,ox:ox+bw]=sl*(1-ra[:16,...,None])+ref[:16]*ra[:16,...,None]
    cs=np.zeros((H,W),np.float32); cv2.ellipse(cs,(ox+bw//2+8,ped_top+3),(bw//2+6,6),0,0,360,1,-1)
    cs=cv2.GaussianBlur(cs,(0,0),4); img*=(1-0.7*cs)[...,None]
    Bi=B.copy()
    if i==1:  # soft occlusion shadow from neighbour on lower-left of right bottle
        yy=np.linspace(0,1,bh)[:,None]; xx=np.linspace(0,1,bw)[None,:]
        occ=np.clip(1-xx/0.35,0,1)*np.clip((yy-0.45)/0.4,0,1)*0.35
        Bi=Bi*(1-occ[...,None])
    img[oy:ped_top,ox:ox+bw]=img[oy:ped_top,ox:ox+bw]*(1-A[...,None])+Bi*A[...,None]
    glow=np.zeros((H,W),np.float32); cv2.ellipse(glow,(ox+bw//2+30,ped_top+8),(bw//2+30,10),0,0,360,1,-1)
    glow=cv2.GaussianBlur(glow,(0,0),10)*(1-cs)
    img+=glow[...,None]*glowc*0.5
v=np.clip(1-0.35*(((X-W*0.45)/W)**2+((Y-H*0.45)/H)**2)*2.2,0,1)
img*=v[...,None]
img+=np.random.default_rng(1).normal(0,0.006,img.shape)
out=(np.clip(img,0,1)**(1/1.02)*255).astype(np.uint8)
cv2.imwrite('/home/user/Video-claude-/output/frescura_duo_studio_4x5.png',out)
cv2.imwrite('preview3.jpg',cv2.resize(out,(800,1000)))
