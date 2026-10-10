"""Original, deterministic pixel scenes and reusable flying explorer Pico."""
import math
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont

W,H=960,540
NAVY='#071621';TEAL='#6ef0d3';GOLD='#ffcb72';CORAL='#ff8b71';WHITE='#f2f3ed'

@lru_cache(None)
def font(size,bold=False):
    path='/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if bold else '')+'.ttf'
    return ImageFont.truetype(path,size)
def rect(d,box,color):d.rectangle(tuple(round(x) for x in box),fill=color)
def label(d,pos,value,size=12,color=WHITE,anchor=None):
    d.text(tuple(round(x) for x in pos),value,font=font(size,True),fill=color,anchor=anchor)
def arrow(d,a,b,color=TEAL,width=3):
    d.line((a,b),fill=color,width=width)
    dx,dy=b[0]-a[0],b[1]-a[1];angle=math.atan2(dy,dx)
    p=[b,(b[0]-9*math.cos(angle-.55),b[1]-9*math.sin(angle-.55)),(b[0]-9*math.cos(angle+.55),b[1]-9*math.sin(angle+.55))]
    d.polygon(p,fill=color)
def clock(d,c,r,t,color=GOLD):
    x,y=c;d.ellipse((x-r,y-r,x+r,y+r),fill='#183446',outline=color,width=4)
    for k in range(12):
        a=k*math.pi/6;d.line((x+math.sin(a)*r*.8,y-math.cos(a)*r*.8,x+math.sin(a)*r*.9,y-math.cos(a)*r*.9),fill=color,width=2)
    a=t*.25;d.line((x,y,x+math.sin(a)*r*.76,y-math.cos(a)*r*.76),fill=WHITE,width=3)
    a=t*.03;d.line((x,y,x+math.sin(a)*r*.52,y-math.cos(a)*r*.52),fill=TEAL,width=4)
    d.ellipse((x-4,y-4,x+4,y+4),fill=CORAL)
def sun(d,x,y,r=22):
    for k in range(12):
        a=k*math.pi/6;d.line((x+math.cos(a)*(r+5),y+math.sin(a)*(r+5),x+math.cos(a)*(r+11),y+math.sin(a)*(r+11)),fill=GOLD,width=2)
    d.ellipse((x-r,y-r,x+r,y+r),fill=GOLD)

def clock_at(d,c,r,hour,minute,t):
    x,y=c;clock(d,c,r,0)
    d.ellipse((x-r*.77,y-r*.77,x+r*.77,y+r*.77),fill='#183446')
    for value,length,color,width in [(minute/60,r*.68,WHITE,3),((hour%12+minute/60)/12,r*.47,TEAL,4),(t/60,r*.70,CORAL,1)]:
        a=value*math.pi*2;d.line((x,y,x+math.sin(a)*length,y-math.cos(a)*length),fill=color,width=width)
    d.ellipse((x-3,y-3,x+3,y+3),fill=CORAL)

def earth(d,x,y,r=37,t=0):
    d.ellipse((x-r,y-r,x+r,y+r),fill='#287794',outline=TEAL,width=2)
    d.polygon([(x-r*.7,y-r*.4),(x-r*.2,y-r*.75),(x+r*.25,y-r*.45),(x,y),(x+r*.2,y+r*.35),(x-r*.25,y+r*.75),(x-r*.55,y+r*.2)],fill='#78be89')
    for k in range(3):
        a=t*.15+k*1.8;yy=y-r*.5+k*r*.5
        d.line((x-r*.7,yy,x+r*.7,yy),fill='#85bbca',width=1)

def gear(d,x,y,r,t,color=GOLD):
    for k in range(12):
        a=k*math.pi/6+t*.45;xx=x+math.cos(a)*r;yy=y+math.sin(a)*r
        rect(d,(xx-5,yy-5,xx+5,yy+5),color)
    d.ellipse((x-r+3,y-r+3,x+r-3,y+r-3),fill=color)
    d.ellipse((x-r*.53,y-r*.53,x+r*.53,y+r*.53),fill='#153547',outline=TEAL,width=2)
    for k in range(4):
        a=k*math.pi/2+t*.45;d.line((x,y,x+math.cos(a)*r*.65,y+math.sin(a)*r*.65),fill=color,width=4)
    d.ellipse((x-4,y-4,x+4,y+4),fill=CORAL)

def starfield(d,t):
    for k in range(42):
        x=25+(k*83)%430;y=42+(k*47)%173
        col=WHITE if (k+int(t*2))%7==0 else '#386178';rect(d,(x,y,x+1,y+1),col)

def footer(d,text,color=TEAL):label(d,(233,238),text,11,color,'mm')

def pico(action,t,scene):
    spr=Image.new('RGBA',(32,40));d=ImageDraw.Draw(spr)
    dark='#123342';skin='#e7b580';suit='#5cddc8';outline='#031722'
    flap=int((math.sin(t*8)+1)*2)
    rect(d,(2,23-flap,8,30),outline);rect(d,(3,24-flap,8,28),'#b9f5e7')
    rect(d,(25,23-flap,31,30),outline);rect(d,(25,24-flap,30,28),'#b9f5e7')
    rect(d,(8,18,25,34),outline);rect(d,(10,20,23,32),suit)
    rect(d,(8,5,25,19),outline);rect(d,(9,4,24,8),GOLD);rect(d,(8,8,25,17),GOLD)
    rect(d,(10,10,23,18),skin);rect(d,(10,9,23,13),dark)
    rect(d,(11,10,14,12),TEAL);rect(d,(18,10,21,12),TEAL)
    rect(d,(14,16,18,17),'#a26348');rect(d,(11,18,24,21),CORAL)
    scarf=3+int(math.sin(t*6)*2);rect(d,(23,19,30,21),CORAL);rect(d,(29,20,31,22+scarf),CORAL)
    rect(d,(12,24,21,27),dark);rect(d,(15,23,18,28),GOLD)
    rect(d,(10,32,14,36),dark);rect(d,(20,32,24,36),dark)
    if action in ('point','follow','wave','question'):
        rect(d,(4,17 if action=='wave' else 23,10,26),outline);rect(d,(5,17 if action=='wave' else 24,9,25),skin)
    if action=='carry':clock(d,(4,26),5,t,GOLD)
    if action=='inspect':d.ellipse((0,14,9,23),outline=TEAL,width=2);d.line((7,21,12,27),fill=GOLD,width=2)
    if action=='clock':clock(d,(3,23),5,t,GOLD)
    if action in ('question','surprise'):label(d,(30,0),'?' if action=='question' else '!',9,GOLD,'rm')
    return spr.resize((96,120),Image.Resampling.NEAREST)

def wrap(text,width=57):
    out=[];line=[]
    for word in text.split():
        if line and len(' '.join(line+[word]))>width:out.append(' '.join(line));line=[]
        line.append(word)
    if line:out.append(' '.join(line))
    return out

