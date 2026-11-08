import sys,glob,os,time
from rembg import new_session, remove
from PIL import Image
model,src,dst=sys.argv[1:4]; step=int(os.environ.get("STEP","1")); os.makedirs(dst,exist_ok=True)
s=new_session(model); fs=sorted(glob.glob(src+'/*.png'))[::step]
lim=int(os.environ.get("LIM","0")) or len(fs); t=time.time()
for k,f in enumerate(fs[:lim]):
    o=os.path.join(dst,os.path.basename(f))
    if os.path.exists(o): continue
    remove(Image.open(f), session=s, post_process_mask=True).save(o)
    if k%25==0: print(k,lim,round(time.time()-t,1),flush=True)
print("done",round(time.time()-t,1))
