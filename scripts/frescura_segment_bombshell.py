import cv2, numpy as np
im=cv2.imread('/root/.claude/uploads/c4c5ab1f-3904-5231-9785-20e7ddb4f867/3e5ce6a6-image.jpg')
x0,y0,x1,y1=560,470,965,1650
sub=im[y0:y1,x0:x1].copy()
mask=np.zeros(sub.shape[:2],np.uint8)
rect=(25,25,sub.shape[1]-55,sub.shape[0]-35)
bg=np.zeros((1,65),np.float64); fg=np.zeros((1,65),np.float64)
cv2.grabCut(sub,mask,rect,bg,fg,8,cv2.GC_INIT_WITH_RECT)
# label area definitely fg
mask[470:1090, 55:355]=cv2.GC_FGD; mask[70:105,80:280]=cv2.GC_FGD; mask[120:400,170:240]=cv2.GC_FGD
cv2.grabCut(sub,mask,None,bg,fg,5,cv2.GC_INIT_WITH_MASK)
m=np.where((mask==1)|(mask==3),255,0).astype(np.uint8)
n,lab,st,_=cv2.connectedComponentsWithStats(m)
k=1+np.argmax(st[1:,4]); m=np.where(lab==k,255,0).astype(np.uint8)
m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))
cv2.imwrite('mask2.png',m)
viz=sub.copy(); viz[m==0]=(0,255,0); cv2.imwrite('viz2.png',viz)
