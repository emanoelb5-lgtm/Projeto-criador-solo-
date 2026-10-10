"""Shared palette, type and the improved, six-pose Pico character."""
import math
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W,H=960,540
NAVY='#071621';TEAL='#6ef0d3';GOLD='#ffcb72';CORAL='#ff8b71';WHITE='#f2f3ed'
ROOT=Path(__file__).resolve().parent

@lru_cache(None)
def font(size,bold=False):
    return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if bold else '')+'.ttf',size)
def rect(d,box,color):d.rectangle(tuple(round(x) for x in box),fill=color)
def label(d,pos,value,size=18,color=WHITE,anchor=None):
    d.text(tuple(round(x) for x in pos),value,font=font(size,True),fill=color,anchor=anchor)
def arrow(d,a,b,color=TEAL,width=4):
    d.line((a,b),fill=color,width=width)
    angle=math.atan2(b[1]-a[1],b[0]-a[0])
    d.polygon([b,(b[0]-12*math.cos(angle-.5),b[1]-12*math.sin(angle-.5)),(b[0]-12*math.cos(angle+.5),b[1]-12*math.sin(angle+.5))],fill=color)
def wrap(text,width=57):
    out=[];line=[]
    for word in text.split():
        if line and len(' '.join(line+[word]))>width:out.append(' '.join(line));line=[]
        line.append(word)
    if line:out.append(' '.join(line))
    return out
@lru_cache(None)
def pose(action):
    positions={'wave':(0,0),'point':(1,0),'question':(2,0),'inspect':(0,1),'surprise':(1,1),'flying':(2,1)}
    x,y=positions.get(action,(1,0))
    with Image.open(ROOT/'assets/Pico_Design_v2_16x9.png') as sheet:
        cell=sheet.crop((x*640,y*540,(x+1)*640,(y+1)*540)).convert('RGBA')
    bounds=cell.getchannel('A').getbbox()
    if not bounds:raise RuntimeError('Missing transparent Pico pose '+action)
    return cell.crop(bounds)
@lru_cache(maxsize=120)
def sized_pose(action,height):
    im=pose(action)
    return im.resize((round(im.width*height/im.height),height),Image.Resampling.NEAREST)
def pico(action,t=0,scene='',height=198):
    sprite=sized_pose(action,height)
    angle=2*math.sin(t*1.4) if action=='flying' else .7*math.sin(t*.8)
    return sprite.rotate(angle,resample=Image.Resampling.NEAREST,expand=True)
def paste_pico(im,action,t,x,y,height=198):
    sprite=pico(action,t,height=height)
    im.alpha_composite(sprite,(round(x),round(y+math.sin(t*2.1)*4)))

