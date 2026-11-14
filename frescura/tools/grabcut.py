import cv2,numpy as np,sys
for src,dst in zip(sys.argv[1::2],sys.argv[2::2]):
    im=cv2.imread(src); h,w=im.shape[:2]
    mask=np.zeros((h,w),np.uint8); rect=(18,10,w-36,h-20)
    bg=np.zeros((1,65),np.float64); fg=np.zeros((1,65),np.float64)
    cv2.grabCut(im,mask,rect,bg,fg,8,cv2.GC_INIT_WITH_RECT)
    m=np.where((mask==1)|(mask==3),255,0).astype(np.uint8)
    # keep largest component, fill holes
    n,lab,st,_=cv2.connectedComponentsWithStats(m); k=1+np.argmax(st[1:,4]); m=np.where(lab==k,255,0).astype(np.uint8)
    cnts,_=cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE); m2=np.zeros_like(m); cv2.drawContours(m2,cnts,-1,255,-1)
    m2=cv2.erode(m2,np.ones((3,3),np.uint8),1); m2=cv2.GaussianBlur(m2,(5,5),0)
    out=np.dstack([im,m2]); cv2.imwrite(dst,out); print(dst)
