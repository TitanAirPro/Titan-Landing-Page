import sys, numpy as np
from PIL import Image
DX,DY,PAD=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
from PIL import ImageFilter
dil0=lambda m,k: np.array(Image.fromarray(m.astype(np.uint8)*255).filter(ImageFilter.MaxFilter(k)))>0
im=Image.open('elephant_source.webp').convert('RGB').crop((0,0,1024,650))
a=np.array(im).astype(float)
grey=(np.abs(a[:,:,0]-a[:,:,2])<18)&(a.min(2)>140)&(a.min(2)<246)
reg=np.zeros(grey.shape,bool); reg[0:236,740:]=True
sm=grey&reg
sm=sm&dil0(grey&(a.min(2)<232)&reg,7)
H=650+PAD
c=np.full((H,1024,3),255.0); c[PAD:]=a
smoke=a.copy()
c[PAD:][sm]=255
ys,xs=np.where(sm)
for y,x in zip(ys,xs):
    ny,nx=y+PAD+DY,x+DX
    if 0<=ny<H and 0<=nx<1024: c[ny,nx]=np.minimum(c[ny,nx],smoke[y,x])
# keep the real colours; alpha only from how far a pixel is from white (soft edges, webp noise dropped)
alpha=np.clip((244-c.min(2))/28.0,0,1)
rgb=c
# wipe the faint outline left where the smoke used to be
from PIL import ImageFilter
dil=lambda m,k: np.array(Image.fromarray(m.astype(np.uint8)*255).filter(ImageFilter.MaxFilter(k)))>0
old=np.zeros(alpha.shape,bool); old[PAD:][sm]=True
new=np.zeros(alpha.shape,bool)
for y,x in zip(ys,xs):
    if 0<=y+PAD+DY<H and 0<=x+DX<1024: new[y+PAD+DY,x+DX]=True
box=np.zeros(alpha.shape,bool); box[:PAD+232,730:]=True
solid=(c[:,:,1]-c[:,:,0]>60)|(c.min(2)<200)   # teal, sun, dark parts
alpha[(dil(old,9)|box)&~dil(new,3)&~dil(solid,5)]=0
base=np.dstack([np.clip(rgb,0,255),alpha*255]).astype(np.uint8)
Image.fromarray(base,'RGBA').save('base.png')
teal=(c[:,:,1]-c[:,:,0]>40); keep=np.zeros_like(teal); keep[PAD+200:PAD+300,900:1000]=True
b=base.copy(); b[~(teal&keep)]=0
Image.fromarray(b,'RGBA').save('trunk.png')
print(H)
