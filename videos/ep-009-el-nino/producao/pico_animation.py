"""Pico v2, animated with twelve authored body keyframes and narrative trajectories."""
import math
from functools import lru_cache
from pathlib import Path
import numpy as np
from PIL import Image,ImageOps
from scipy import ndimage

ROOT=Path(__file__).resolve().parent
ANIMATION_VERSION=3

@lru_cache(None)
def keyframes():
    with Image.open(ROOT/'assets/Pico_Animation_v3_16x9.png') as im:sheet=im.convert('RGBA')
    assert sheet.size==(1920,1080)
    frames={}
    for column in range(4):
        array=np.array(sheet.crop((column*480,0,(column+1)*480,1080)))
        components,count=ndimage.label(array[:,:,3]>20,structure=np.ones((3,3)))
        sizes=np.bincount(components.ravel())
        selected=sorted(range(1,count+1),key=lambda k:sizes[k],reverse=True)[:3]
        selected.sort(key=lambda k:float(np.where(components==k)[0].mean()))
        assert len(selected)==3 and all(sizes[k]>45000 for k in selected)
        for row,component in enumerate(selected):
            pixels=array.copy();pixels[:,:,3]*=(components==component)
            sprite=Image.fromarray(pixels);bounds=sprite.getchannel('A').getbbox();sprite=sprite.crop(bounds)
            a=np.array(sprite);r,g,b=a[:,:,0],a[:,:,1],a[:,:,2]
            gold=(r>180)&(g>100)&(g<220)&(b<110)&(g.astype(float)>r.astype(float)/1.9)&(a[:,:,3]>128)
            gold[int(sprite.height*.59):,:]=False
            yy,xx=np.where(gold);assert len(xx)>1000
            hx=float(xx.mean());hy=float(yy.mean())
            canvas=Image.new('RGBA',(620,500))
            position=(round(330-hx),round(140-hy))
            assert position[0]>=0 and position[1]>=0 and position[0]+sprite.width<=620 and position[1]+sprite.height<=500
            canvas.alpha_composite(sprite,position);frames[row*4+column]=canvas
    boxes=[im.getchannel('A').getbbox() for im in frames.values()]
    common=(min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes))
    return tuple(frames[k].crop(common) for k in range(12))

def phase_frame(cycle,t):
    if cycle=='flying':return [0,1,2,3,2,1][int(t*9)%6]
    if cycle=='wave':
        if 2.9<t%4.2<3.12:return 7
        return 4+[0,1,2,1][int(t*6)%4]
    # Extend, indicate the target for a moment, and relax the elbow.
    u=t%2.8
    return 8+(0 if u<.30 else 1 if u<.60 else 2 if u<2.18 else 3)

@lru_cache(maxsize=384)
def transformed(index,height,flip,bank):
    im=keyframes()[index]
    im=im.resize((round(im.width*height/im.height),height),Image.Resampling.NEAREST)
    if flip:im=ImageOps.mirror(im)
    if bank:im=im.rotate(bank,resample=Image.Resampling.NEAREST,expand=True)
    return im

def sprite(cycle,t,height=175,flip=False,bank=0):
    return transformed(phase_frame(cycle,t),round(height),bool(flip),round(bank/2)*2)

def ease(u):return .5-.5*math.cos(math.pi*max(0,min(1,u)))

def motion(item,scene,local):
    duration=item['duration'];u=max(0,min(1,local/duration));kind=item.get('motion','target')
    x=837+20*math.sin(local*.48);y=313+12*math.sin(local*.82);height=172
    cycle='point' if item['action']!='wave' else 'wave';flip=False;bank=0;opacity=1
    if kind in ('west','east','cross'):
        cycle='flying';height=116
        west=kind=='west';x=(821-698*ease(u)) if west else 122+698*ease(u)
        y=219+11*math.sin(math.pi*u);flip=west;bank=(-7 if west else 7)*math.sin(math.pi*u)
    elif kind=='entrance':
        cycle='flying';height=148;x=845-64*ease(min(1,local/4.2));y=283-36*math.sin(min(1,local/4.2)*math.pi)
        flip=True;bank=12*math.sin(local*.8);opacity=min(1,local/.65)
    elif kind=='dive':
        cycle='flying';height=105;x=640-190*math.sin(math.pi*u);y=208+190*math.sin(math.pi*u)
        flip=u<.5;bank=26*math.cos(math.pi*u)
    elif kind=='cloud':
        cycle='flying';height=108;x=237+494*ease(u);y=228-12*math.sin(math.pi*u);bank=8*math.sin(local*.7)
    elif kind=='arc':
        cycle='flying';height=116;x=151+600*ease(u);y=296-143*math.sin(math.pi*u);bank=15*math.cos(math.pi*u)
    elif kind=='fish':
        cycle='flying';height=112;x=158+587*(.5-.5*math.cos(local*.42));y=325+42*math.sin(local*.64)
        flip=math.sin(local*.42)<0;bank=10*math.cos(local*.64)
    elif kind=='pair':y=266+45*math.sin(local*.76)
    elif kind=='north':y=230+16*math.sin(local*.75)
    elif kind=='south':y=359+13*math.sin(local*.70)
    elif kind=='fan':x=820+18*math.sin(local*.52);y=286+15*math.sin(local*.84)
    elif kind=='timeline':cycle='wave';y=309+23*math.sin(local*.80)
    elif kind in ('boat','field'):cycle='wave';y=343+18*math.sin(local*.72)
    elif kind=='quiz':y=321+31*math.sin(local*.45)
    elif kind=='farewell':
        cycle='wave';x=815+15*math.sin(local*.6);y=327+17*math.sin(local*.8);height=187
        if scene=='outro' and local>duration-2.2:
            q=(local-duration+2.2)/2.2;cycle='flying';flip=True;x=815-409*ease(q);y=327-143*ease(q);height=149
            opacity=max(0,min(1,(duration-local)/.7))
    return {'x':x,'y':y,'height':height,'cycle':cycle,'flip':flip,'bank':bank,'opacity':opacity}

def place(canvas,item,scene,local):
    plan=motion(item,scene,local);image=sprite(plan['cycle'],local,plan['height'],plan['flip'],plan['bank'])
    # Keep each complete drawing within the persistent frame and source footer.
    bounds=image.getchannel('A').getbbox();assert bounds
    x=max(25,min(935-image.width,round(plan['x']-(bounds[0]+bounds[2])/2)))
    y=max(76,min(486-image.height,round(plan['y']-(bounds[1]+bounds[3])/2)))
    if plan['opacity']<1:
        image=image.copy();image.putalpha(image.getchannel('A').point(lambda a:round(a*plan['opacity'])))
    canvas.alpha_composite(image,(x,y))
    return plan,(x,y,image.width,image.height)
