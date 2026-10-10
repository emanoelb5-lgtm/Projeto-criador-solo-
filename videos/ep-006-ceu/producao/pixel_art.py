"""Original animated optics schematics and detailed pixel environments. No captions."""
import hashlib, math, random
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw
from base_art import W,H,NAVY,TEAL,GOLD,CORAL,WHITE,font,rect,label,arrow,pico,wrap

ROOT=Path(__file__).resolve().parent
ASSET_HASH=hashlib.sha256(b''.join(p.read_bytes() for p in sorted((ROOT/'assets').glob('*.png')))).hexdigest()
BLUE='#70adff';RED='#ff806e';VIOLET='#bb9eff'
COLORS=[RED,'#ffaf68',GOLD,'#83dfb1',TEAL,BLUE,VIOLET]
TITLES={
 'light_route':'Siga o caminho da luz','prism':'Uma mistura de cores','wavelengths':'Comprimentos de onda',
 'spectrum':'Luz visível','air_zoom':'O ar também participa','molecules':'Moléculas do ar',
 'rayleigh':'Espalhamento de Rayleigh','scatter_compare':'O azul se espalha mais',
 'side_observer':'Luz que chega de outra direção','blue_routes':'Muitos caminhos até os olhos',
 'atmosphere_toggle':'Com ar / sem ar','space_routes':'Iluminação e céu luminoso',
 'horizon_gradient':'O horizonte muda o percurso','route_question':'E a luz que segue adiante?',
 'earth_high':'Sol alto','earth_low':'Sol perto do horizonte','path_compare':'Compare as travessias',
 'beam_short':'Caminho curto','beam_long':'Caminho longo','red_arrival':'A mistura que chega',
 'two_observers':'Luz espalhada / luz transmitida','tank_setup':'Laboratório imaginado',
 'tank_side':'Observador lateral','tank_end':'Na saída do feixe','tank_compare':'Dois pontos de vista',
 'analogy_limits':'A analogia tem limites','cloud_droplets':'Gotículas de água',
 'cloud_paths':'Uma mistura ampla de cores','sunset_variations':'Um ambiente, muitas variações',
 'mars_dust':'Poeira fina na atmosfera de Marte','planet_compare':'O que está no caminho?',
 'recap_routes':'Dois percursos, uma explicação','recap_three':'Três perguntas para investigar'
}

@lru_cache(None)
def scenery(kind):
    with Image.open(ROOT/'assets'/f'{kind}_Pixel_16x9.png') as im:
        return im.convert('RGBA').resize((1024,576),Image.Resampling.NEAREST)

def background(kind,t):
    src=scenery(kind);x=round(32+19*math.sin(t*.09));y=round(18+10*math.sin(t*.07))
    return src.crop((x,y,x+W,y+H))

def circle(d,x,y,r,fill,outline=None,width=2):
    d.ellipse(tuple(round(q) for q in (x-r,y-r,x+r,y+r)),fill=fill,outline=outline,width=width)

def panel(im,title):
    layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer)
    d.rounded_rectangle((38,76,748,489),radius=12,fill=(5,22,33,241),outline=(110,240,211,135),width=2)
    for x in range(58,740,24):
        for y in range(134,481,24):circle(d,x,y,.7,(106,177,184,34))
    rect(d,(55,91,59,119),GOLD);label(d,(75,106),title,22,GOLD,'lm')
    im.alpha_composite(layer);return ImageDraw.Draw(im)

def note(d,text='Esquema sem escala'):
    label(d,(72,466),text,11,'#91b7bf','lm')

def moving_ray(d,a,b,t,color=BLUE,width=3,density=5):
    arrow(d,a,b,color,width)
    for k in range(density):
        q=(t*.24+k/density)%1
        circle(d,a[0]+(b[0]-a[0])*q,a[1]+(b[1]-a[1])*q,3 if width>2 else 2,WHITE)

def eye(d,x,y,color=WHITE):
    d.ellipse((x-17,y-9,x+17,y+9),outline=color,width=2)
    circle(d,x,y,6,color);circle(d,x,y,3,NAVY)

def sun(d,x,y,t,r=22):
    for k in range(12):
        a=k*math.pi/6+t*.035
        d.line((x+(r+6)*math.cos(a),y+(r+6)*math.sin(a),x+(r+13)*math.cos(a),y+(r+13)*math.sin(a)),fill=GOLD,width=2)
    circle(d,x,y,r,GOLD);circle(d,x-5,y-6,r*.55,'#ffdf93')

def molecules(d,t,area=(190,168,690,418),count=35):
    x1,y1,x2,y2=area
    for k in range(count):
        x=x1+(k*67)%(x2-x1)+math.sin(t*.7+k)*3
        y=y1+(k*53)%(y2-y1)+math.cos(t*.6+k)*3
        circle(d,x-3,y,5,'#366176',TEAL,1);circle(d,x+4,y+2,5,'#416b7d','#a7d9e2',1)

def spectrum(d,t,x=119,y=192,width=560,height=91):
    for j in range(width):
        c=COLORS[min(6,int(j/width*7))]
        d.line((x+j,y,x+j,y+height),fill=c,width=1)
    d.rectangle((x-2,y-2,x+width+2,y+height+2),outline=WHITE,width=2)
    pos=x+(t*.09%1)*width;d.line((pos,y-10,pos,y+height+10),fill=WHITE,width=2)

def waves(d,t):
    for y,period,c,text in [(211,41,BLUE,'AZUL'),(340,79,RED,'VERMELHO')]:
        points=[(x,y+26*math.sin((x-110-t*39)*2*math.pi/period)) for x in range(111,680)]
        d.line(points,fill=c,width=4);label(d,(110,y-55),text,17,c,'lm')
        x=270+(110+t*39+period*.75-270)%period;d.line((x,y-30,x+period,y-30),fill=WHITE,width=2)
        for xx in (x,x+period):d.line((xx,y-35,xx,y-25),fill=WHITE,width=2)
    label(d,(389,419),'Intervalo entre cristas',16,TEAL,'mm')

def scattering(d,t,kind):
    molecules(d,t,count=24)
    cx,cy=358,271
    if kind=='scatter_compare':
        for y,c,many in [(218,BLUE,7),(351,RED,3)]:
            moving_ray(d,(84,y),(326,y),t,c,4)
            circle(d,336,y,8,TEAL)
            for k in range(many):
                a=(-1.2+k*2.4/max(1,many-1));end=(336+260*math.cos(a),y+74*math.sin(a))
                moving_ray(d,(347,y),end,t+k*.16,c,3 if many==7 else 2,3)
        label(d,(88,172),'AZUL',16,BLUE,'lm');label(d,(88,311),'VERMELHO',16,RED,'lm')
        note(d,'Raios simbólicos; não são contagens medidas');return
    moving_ray(d,(82,cy),(cx,cy),t,WHITE,5)
    circle(d,cx,cy,10,TEAL,WHITE,2)
    moving_ray(d,(cx+11,cy),(687,cy),t,RED,3)
    for k,end in enumerate([(531,152),(634,178),(426,404),(555,396),(208,398)]):
        moving_ray(d,(cx,cy),end,t+k*.22,BLUE,3,4)
    moving_ray(d,(cx,cy),(229,160),t,RED,1,2)
    label(d,(87,235),'LUZ INCIDENTE',13,WHITE,'lm')
    if kind in ['side_observer','light_route']:
        eye(d,558,416,BLUE);label(d,(535,436),'OBSERVADOR',12,BLUE,'mm')
    else:label(d,(525,435),'Direções diferentes',16,TEAL,'mm')
    note(d)

def world(d,t,low=False,x=385,y=707,r=399,mini=False):
    d.ellipse((x-r-72,y-r-72,x+r+72,y+r+72),fill='#173d5b',outline=BLUE,width=2)
    d.ellipse((x-r,y-r,x+r,y+r),fill='#235444',outline=TEAL,width=2)
    rng=random.Random(77)
    for k in range(48):
        xx=x-r+rng.randint(60,2*r-60);yy=y-r+rng.randint(12,155)
        if (xx-x)**2+(yy-y)**2<r*r:
            rect(d,(xx,yy,xx+14+k%6,yy+3),'#3e7452')
    target=(x,y-r);eye(d,target[0],target[1]-3)
    origin=(92,target[1]-39) if low else (x,189)
    moving_ray(d,origin,(target[0],target[1]-17),t,GOLD if low else WHITE,4)
    sun(d,origin[0],origin[1]-24 if not low else origin[1],t,17)
    label(d,(116,339),'ATMOSFERA',11,BLUE,'lm')
    note(d,'Atmosfera exagerada; esquema sem escala')

def beams(d,t,long=False):
    x1=109;x2=681;yc=266
    rect(d,(x1,186,x2,365),'#16323f')
    count=44 if long else 12
    molecules(d,t,(x1+8,192,x2-12,355),count)
    sun(d,83,yc,t,16)
    for j,c in enumerate([BLUE,TEAL,RED]):
        yy=yc-19+j*19
        cut=x2 if j!=0 or not long else 445
        moving_ray(d,(x1,yy),(cut,yy),t+j*.21,c,3,6)
        if cut<x2:d.line((cut,yy,x2,yy),fill='#36516e',width=1)
        for k in range((6 if long else 2) if j==0 else (2 if long else 1)):
            xx=185+k*(65 if long else 180);end=(xx+32,156 if k%2==0 else 396)
            moving_ray(d,(xx,yy),end,t+k*.13,c,2,2)
    eye(d,708,yc,RED if long else WHITE)
    label(d,(392,426),'MAIS ATMOSFERA' if long else 'MENOS ATMOSFERA',18,TEAL,'mm')
    note(d,'Redistribuição ilustrada; não é uma medida espectral')

def tank(d,t,kind):
    label(d,(82,145),'MODELO ILUSTRADO',12,TEAL,'lm')
    rect(d,(103,260,166,295),'#6d8090');circle(d,169,277,20,GOLD,WHITE)
    d.rounded_rectangle((226,213,610,358),radius=12,fill='#153b50',outline='#b6e8e7',width=3)
    rect(d,(226,352,610,366),'#547e87')
    molecules(d,t,(242,230,593,339),count=28)
    for j,c in enumerate([BLUE,TEAL,RED]):
        yy=269+j*9
        moving_ray(d,(191,yy),(410 if j==0 else 606,yy),t,c,3)
    for k in range(6):
        xx=262+k*57
        moving_ray(d,(xx,275),(xx+21,383),t+k*.13,BLUE,2,2)
    if kind in ['tank_side','tank_compare','tank_setup']:
        eye(d,430,400,BLUE);label(d,(430,431),'DE LADO',16,BLUE,'mm')
    if kind in ['tank_end','tank_compare','tank_setup']:
        moving_ray(d,(611,284),(671,284),t,RED,4,3)
        eye(d,696,284,RED);label(d,(692,337),'SAÍDA',15,RED,'mm')
    note(d,'Analogia de percursos; cores e tamanhos simplificados')

def clouds(d,t,kind):
    for k in range(24):
        x=211+(k*61)%325;y=230+(k*41)%97
        circle(d,x,y,22+(k%3)*4,'#d9edee','#f3fcf5',2)
    if kind=='cloud_droplets':
        for k in range(7):circle(d,153+k*78,380,8,'#66bed2',WHITE,2)
        label(d,(378,419),'GOTÍCULAS  >  MOLÉCULAS',18,TEAL,'mm')
    else:
        moving_ray(d,(78,272),(245,272),t,WHITE,5)
        for j,c in enumerate(COLORS):moving_ray(d,(443,260+j*4),(675,167+j*38),t+j*.17,c,3,3)
        label(d,(381,412),'Muitas cores chegam juntas',17,WHITE,'mm')
    note(d)

def horizon(im,t):
    d=panel(im,TITLES['horizon_gradient'])
    for y in range(163,412):
        q=(y-163)/249
        c=tuple(round(a+(b-a)*q) for a,b in zip((39,114,199),(184,218,225)))
        d.line((80,y,700,y),fill=c,width=1)
    d.polygon([(80,412),(160,368),(229,402),(300,355),(418,399),(523,359),(700,410)],fill='#24484f')
    moving_ray(d,(136,264),(500,350),t,WHITE,2,6)
    eye(d,541,363);label(d,(390,446),'Perto do horizonte',17,TEAL,'mm')
    note(d)

def scheme(im,scene,t):
    if scene=='horizon_gradient':horizon(im,t);return
    d=panel(im,TITLES[scene])
    if scene=='prism':
        d.polygon([(329,181),(310,365),(446,301)],fill='#27556b',outline=TEAL)
        d.line((329,181,355,281,446,301),fill='#89d8df',width=3)
        moving_ray(d,(89,260),(321,260),t,WHITE,5)
        moving_ray(d,(321,260),(409,285),t,WHITE,4)
        for k,c in enumerate(COLORS):moving_ray(d,(409,285),(684,300+k*19),t+k*.07,c,3,5)
        label(d,(90,220),'MISTURA',17,WHITE,'lm');note(d,'Separação ilustrada por refração; sem escala')
    elif scene=='wavelengths':waves(d,t);note(d)
    elif scene=='spectrum':
        spectrum(d,t);label(d,(120,326),'MAIS LONGAS',17,RED,'lm');label(d,(679,326),'MAIS CURTAS',17,VIOLET,'rm')
        label(d,(400,395),'Comprimento de onda',19,WHITE,'mm');note(d)
    elif scene in ['air_zoom','molecules']:
        molecules(d,t,(150,171,684,412),38)
        if scene=='air_zoom':
            d.ellipse((209,180,500,419),outline=GOLD,width=4);d.line((459,391,548,440),fill=GOLD,width=9)
        else:
            label(d,(195,440),'NITROGÊNIO',17,TEAL,'mm');label(d,(566,440),'OXIGÊNIO',17,BLUE,'mm')
        note(d,'Moléculas ampliadas e representadas por símbolos')
    elif scene in ['rayleigh','scatter_compare','side_observer','light_route']:
        scattering(d,t,scene)
    elif scene in ['blue_routes','recap_routes','two_observers']:
        sun(d,106,176,t)
        d.line((98,414,695,414),fill=TEAL,width=3)
        for k in range(9):
            x=181+(k*89)%462;y=188+(k*71)%174
            circle(d,x,y,4,TEAL)
            moving_ray(d,(106,197),(x,y),t+k*.1,WHITE,1,2)
            moving_ray(d,(x,y),(399,391),t+k*.17,BLUE,2,3)
        eye(d,399,400,BLUE);label(d,(394,439),'LUZ ESPALHADA',16,BLUE,'mm')
        if scene!='blue_routes':
            moving_ray(d,(107,183),(668,290),t,RED,3,6);eye(d,687,294,RED)
            label(d,(629,348),'TRANSMITIDA',13,RED,'mm')
        note(d)
    elif scene in ['earth_high','earth_low']:
        body=Image.new('RGBA',(W,H));world(ImageDraw.Draw(body),t,scene=='earth_low')
        im.alpha_composite(body.crop((65,130,732,481)),(65,130))
    elif scene=='path_compare':
        for x,y,low in [(244,338,False),(540,338,True)]:
            circle(d,x,y,70,'#235444',TEAL,2);d.arc((x-97,y-97,x+97,y+97),180,355,fill=BLUE,width=18)
            a=(x-116,y-74) if low else (x,y-147)
            moving_ray(d,a,(x,y-72),t,GOLD if low else WHITE,3,4)
            label(d,(x,420),'LONGO' if low else 'CURTO',18,GOLD if low else WHITE,'mm')
        note(d,'Atmosfera exagerada; trajetos simbólicos')
    elif scene in ['beam_short','beam_long','red_arrival']:beams(d,t,scene!='beam_short')
    elif scene in ['route_question','atmosphere_toggle','space_routes']:
        q=(t%9)/9;has_air=scene=='route_question' or (scene=='atmosphere_toggle' and q<.55)
        rect(d,(79,153,706,422),'#1c4e7b' if has_air else '#050c16')
        sun(d,137,213,t,24)
        d.polygon([(79,421),(261,366),(456,391),(589,346),(706,421)],fill='#316458')
        moving_ray(d,(161,221),(552,358),t,GOLD,3)
        if has_air:
            for k in range(7):moving_ray(d,(246+k*51,252+k*12),(355,375),t+k*.12,BLUE,2,2)
        label(d,(381,441),'COM ATMOSFERA' if has_air else 'SEM ATMOSFERA',17,BLUE if has_air else WHITE,'mm');note(d)
    elif scene.startswith('tank_'):tank(d,t,scene)
    elif scene=='analogy_limits':
        for x,title,r,color in [(225,'MOLÉCULAS',7,TEAL),(548,'PARTÍCULAS',21,GOLD)]:
            d.rounded_rectangle((x-129,172,x+129,400),radius=9,fill='#173442',outline=color,width=2)
            for k in range(6):circle(d,x-70+k%3*70,236+k//3*83+math.sin(t+k)*3,r,color)
            label(d,(x,429),title,18,color,'mm')
        note(d,'Tamanho, quantidade e material importam; sem escala')
    elif scene in ['cloud_droplets','cloud_paths']:clouds(d,t,scene)
    elif scene=='sunset_variations':
        for j in range(3):
            x=83+j*211
            rect(d,(x,188,x+185,366),['#84465b','#a76742','#536077'][j])
            sun(d,x+49,293,t,14);d.polygon([(x,366),(x+63,330),(x+117,353),(x+185,318),(x+185,366)],fill='#253b44')
            for k in range(j*7):circle(d,x+11+k*31%160,219+k*17%91+math.sin(t+k)*2,2,GOLD)
            label(d,(x+92,414),['NUVENS','POEIRA','PERCURSOS'][j],16,WHITE,'mm')
        note(d,'Cores ilustrativas; não classificam a qualidade do ar')
    elif scene in ['mars_dust','planet_compare']:
        if scene=='mars_dust':
            rect(d,(77,151,708,419),'#5c443e');sun(d,133,285,t,22)
            for k in range(42):circle(d,180+k*79%475,178+k*59%202+math.sin(t+k)*2,2,GOLD)
            moving_ray(d,(163,283),(665,283),t,BLUE,4,8)
            for k in range(6):moving_ray(d,(270+k*53,283),(306+k*49,167 if k%2 else 398),t+k*.2,RED,2,3)
            label(d,(403,440),'MARTE · POEIRA FINA',17,TEAL,'mm')
        else:
            for x,name,c,r in [(228,'TERRA',TEAL,7),(549,'MARTE',GOLD,13)]:
                circle(d,x,282,109,'#15313e',c,3)
                for k in range(12):circle(d,x-68+k*31%130,217+k*37%135+math.sin(t+k)*2,r if k%3==0 else r*.5,c)
                label(d,(x,433),name,20,c,'mm')
        note(d,'Distribuição esquemática; não representa dados medidos')
    elif scene=='recap_three':
        for k,(text,color) in enumerate([('CORES',GOLD),('INTERAÇÕES',TEAL),('PERCURSOS',BLUE)]):
            x=190+k*206;circle(d,x,278,65,'#163442',color,3)
            label(d,(x,270),str(k+1),38,color,'mm');label(d,(x,378),text,16,color,'mm')
            if k<2:arrow(d,(x+77,278),(x+126,278),WHITE,2)
        note(d,'Uma maneira de organizar a investigação')
    else:raise ValueError('Unknown scheme '+scene)

def pixel_scene(scene,t):
    kind='Sunset' if scene in ['sunset_lookout','closing_split','end_card','route_question','earth_low','beam_long','red_arrival','two_observers','sunset_variations'] else 'Lab' if scene in ['lab_intro','prism','wavelengths','spectrum','tank_setup','tank_side','tank_end','tank_compare','analogy_limits'] else 'Day'
    im=background(kind,t)
    if scene in ['opening_split','closing_split']:
        other=background('Sunset',t);im.alpha_composite(other.crop((W//2,0,W,H)),(W//2,0))
        d=ImageDraw.Draw(im);d.line((480,24,480,516),fill=GOLD,width=3)
        for x,text,color in [(235,'AZUL',BLUE),(718,'VERMELHO',GOLD)]:
            d.rounded_rectangle((x-96,146,x+96,190),radius=8,fill=NAVY)
            label(d,(x,168),text,23,color,'mm')
    elif scene in TITLES:scheme(im,scene,t)
    elif scene=='end_card':
        layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer)
        d.rounded_rectangle((67,135,734,374),radius=12,fill=(7,22,33,222),outline=TEAL,width=2)
        label(d,(398,206),'QUASE INFINITO',40,GOLD,'mm')
        label(d,(398,278),'Cada pergunta abre outra viagem.',24,WHITE,'mm')
        im.alpha_composite(layer)
    elif scene not in ['day_lookout','sunset_lookout','day_flight','lab_intro']:raise ValueError(scene)
    # Separate parallax-like foreground glints; the scene has its own explanatory animation.
    if kind!='Lab':
        layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer)
        for k in range(12):
            x=(48+k*83+t*(3+k%4))%955;y=395+(k*23)%93+math.sin(t*.7+k)*5
            rect(d,(x,y,x+2,y+1),(255,219,140,50+k%4*15))
        im.alpha_composite(layer)
    return im

def overlay(item,scene,local,global_time,source,pixel):
    """Only brand, chapter label, source credit, frame and Pico. Never narration text."""
    im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im)
    rect(d,(0,0,W,28),(5,19,29,245));label(d,(21,14),'QUASE INFINITO',13,GOLD,'lm')
    label(d,(934,14),f"{item['index']+1:02d} · {item['title']}",12,WHITE,'rm')
    d.rectangle((7,34,952,512),outline=(110,240,211,195),width=2)
    for x,y,sx,sy in [(7,34,1,1),(952,34,-1,1),(7,512,1,-1),(952,512,-1,-1)]:
        d.line((x,y,x+sx*23,y),fill=GOLD,width=4);d.line((x,y,x,y+sy*18),fill=GOLD,width=4)
    rect(d,(0,518,W,H),(5,19,29,248))
    label(d,(19,531),source,9,'#b6c7c7','lm')
    rect(d,(650,528,936,532),'#29414f');rect(d,(650,528,650+286*global_time/492,532),TEAL)
    if scene.startswith('mars_photo'):
        d.rounded_rectangle((29,57,410,104),radius=6,fill=(5,19,29,224))
        label(d,(44,80),'Curiosity · Marte · 15 abr 2015',17,WHITE,'lm')
    action=item['action'];height=197 if pixel else 147
    if scene in ['end_card','closing_split']:height=249;action='wave'
    if scene=='day_flight':action='flying';height=204
    spr=pico(action,global_time,height=height);x=940-spr.width;y=501-spr.height
    if action=='flying':
        x-=round(28+13*math.sin(local*.9));y-=round(25+14*math.sin(local*.7))
        for k in range(6):circle(d,x-4-k*8,y+spr.height*.55,2,GOLD if k%2 else TEAL)
    im.alpha_composite(spr,(round(x),round(y+3*math.sin(global_time*1.6))))
    return im
