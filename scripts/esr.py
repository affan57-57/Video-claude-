import sys, glob, os, torch, torch.nn as nn, torch.nn.functional as F, numpy as np
from PIL import Image
from safetensors.torch import load_file
class SRVGG(nn.Module):
    def __init__(s, nf=64, nc=32, up=4):
        super().__init__(); s.up=up; b=[nn.Conv2d(3,nf,3,1,1), nn.PReLU(nf)]
        for _ in range(nc): b+= [nn.Conv2d(nf,nf,3,1,1), nn.PReLU(nf)]
        b+=[nn.Conv2d(nf,3*up*up,3,1,1)]; s.body=nn.ModuleList(b); s.ps=nn.PixelShuffle(up)
    def forward(s,x):
        o=x
        for m in s.body: o=m(o)
        return s.ps(o)+F.interpolate(x,scale_factor=s.up,mode='nearest')
net=SRVGG(); net.load_state_dict(load_file(sys.argv[1])); net.eval(); torch.set_num_threads(int(os.environ.get("NT","4")))
src,dst=sys.argv[2],sys.argv[3]; os.makedirs(dst,exist_ok=True)
files=sorted(glob.glob(src+'/*.png'))[int(os.environ.get("A","0")):int(os.environ.get("B","999999"))]
with torch.inference_mode():
    for i,f in enumerate(files):
        o=os.path.join(dst,os.path.basename(f))
        if os.path.exists(o): continue
        im=np.asarray(Image.open(f).convert('RGB'),dtype=np.float32)/255.
        x=torch.from_numpy(im).permute(2,0,1)[None]; H,W=x.shape[2:]; T=int(os.environ.get("TILE","192")); P=8
        y=torch.zeros(1,3,H*4,W*4)
        for t0 in range(0,H,T):
            for l0 in range(0,W,T):
                a,b=max(t0-P,0),min(t0+T+P,H); c,d=max(l0-P,0),min(l0+T+P,W)
                o_=net(x[:,:,a:b,c:d]); tt,ll=(t0-a)*4,(l0-c)*4; hh,ww=(min(t0+T,H)-t0)*4,(min(l0+T,W)-l0)*4
                y[:,:,t0*4:t0*4+hh,l0*4:l0*4+ww]=o_[:,:,tt:tt+hh,ll:ll+ww]
        y=y.clamp(0,1)[0].permute(1,2,0).numpy()
        Image.fromarray((y*255+0.5).astype(np.uint8)).resize((1080,1976),Image.LANCZOS).save(o, compress_level=1)
        if i%20==0: print(i,len(files),flush=True)
