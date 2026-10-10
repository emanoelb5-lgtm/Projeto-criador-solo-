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

def pixel_scene(name,t):
    im=Image.new('RGB',(480,270),NAVY);d=ImageDraw.Draw(im);starfield(d,t)
    if name in ('question24','twentyfour'):
        clock(d,(301,138),70,t)
        label(d,(114,118),'24',57,GOLD,'mm');label(d,(114,171),'HORAS',19,TEAL,'mm')
        if name=='question24':label(d,(388,75),'?',43,CORAL,'mm')
        footer(d,'Uma escolha com milhares de anos')
    elif name=='daynight':
        sun(d,90,132,25);earth(d,235,139,63,t)
        d.pieslice((172,76,298,202),-90,90,fill='#102c43',outline=TEAL,width=2)
        arrow(d,(130,110),(157,110),GOLD,2);arrow(d,(130,163),(157,163),GOLD,2)
        label(d,(332,136),'DIA',16,GOLD,'mm');label(d,(332,171),'NOITE',16,TEAL,'mm')
        footer(d,'A natureza oferece o ciclo; nós criamos a régua')
    elif name=='timeline_history':
        label(d,(232,53),'UMA LONGA VIAGEM',19,GOLD,'mm')
        d.line((62,146,386,146),fill=TEAL,width=3)
        for i,(lab,when) in enumerate([('Sombras','Antiguidade'),('Máquinas','Engrenagens'),('Cristais','Eletrônica'),('Átomos','Precisão')]):
            x=64+i*106;d.ellipse((x-6,140,x+6,152),fill=GOLD);label(d,(x,116),lab,11,WHITE,'mm');label(d,(x,176),when,8,TEAL,'mm')
        footer(d,'Várias ideias construíram o relógio que conhecemos')
    elif name=='ancient_day':
        rect(d,(0,176,480,270),'#6f5438');rect(d,(0,210,480,251),'#2f7d96')
        for x,w in [(115,84),(239,63),(321,43)]:d.polygon([(x-w,177),(x,91),(x+w,177)],fill='#be965b');d.polygon([(x,91),(x+w,177),(x+12,177)],fill='#8f6d47')
        sun(d,75,76,22);label(d,(232,51),'OBSERVAR O CÉU',17,WHITE,'mm')
        for k in range(7):rect(d,(k*76+(t*10)%76,223,k*76+36+(t*10)%76,225),'#68b7c2')
        footer(d,'Reconstrução ilustrativa em pixel art',WHITE)
    elif name in ('shadow','cloud_shadow'):
        d.ellipse((101,119,369,214),fill='#364b4c',outline=GOLD,width=2)
        for k in range(12):
            a=k*math.pi/6;d.line((236+math.cos(a)*89,167+math.sin(a)*28,236+math.cos(a)*112,167+math.sin(a)*39),fill=GOLD,width=2)
        a=-1.3+math.sin(t*.24)*.9;d.polygon([(233,164),(233+95*math.cos(a),168+39*math.sin(a)),(240,169)],fill='#081c27')
        rect(d,(231,106,239,168),TEAL);sun(d,86+math.sin(t*.14)*24,76,20)
        if name=='cloud_shadow':
            for j in range(4):d.ellipse((37+j*23,46,82+j*23,88),fill='#9bacba')
        footer(d,'A sombra muda de posição com o Sol' if name=='shadow' else 'Sem luz direta, a leitura fica difícil')
    elif name in ('twelve_day','twelve_night'):
        night=name=='twelve_night';cx,cy=226,151;r=77
        for k in range(12):
            a=k*30-90;d.pieslice((cx-r,cy-r,cx+r,cy+r),a,a+29,fill=('#163954' if night else '#ab7b3a'),outline=NAVY,width=2)
            ang=(a+15)*math.pi/180;label(d,(cx+math.cos(ang)*r*.77,cy+math.sin(ang)*r*.77),str(k+1),10,WHITE,'mm')
        d.ellipse((cx-33,cy-33,cx+33,cy+33),fill=NAVY)
        if night:d.ellipse((cx-15,cy-15,cx+15,cy+15),fill=WHITE);d.ellipse((cx-6,cy-19,cx+20,cy+7),fill=NAVY)
        else:sun(d,cx,cy,15)
        label(d,(226,53),'12 PARTES DA '+('NOITE' if night else 'LUZ'),18,TEAL if night else GOLD,'mm')
    elif name=='season_hours':
        label(d,(231,52),'12 PARTES • TAMANHOS DIFERENTES',14,GOLD,'mm')
        for j,(width,lab) in enumerate([(320,'Mais tempo de luz'),(210,'Menos tempo de luz')]):
            y=101+j*75;label(d,(58,y-19),lab,12,WHITE)
            for k in range(12):rect(d,(58+k*width/12,y,56+(k+1)*width/12,y+24),(GOLD if k%2==0 else '#bb8a49') if j==0 else (TEAL if k%2==0 else '#359986'))
        footer(d,'Exemplo esquemático: horas sazonais')
    elif name=='pizza_hours':
        label(d,(229,52),'AS MESMAS 12 FATIAS',18,GOLD,'mm')
        for x,r in [(139,71),(330,47)]:
            d.ellipse((x-r,142-r,x+r,142+r),fill='#c18c47',outline=GOLD,width=3)
            for k in range(12):
                a=k*math.pi/6;d.line((x,142,x+math.cos(a)*r,142+math.sin(a)*r),fill=NAVY,width=2)
            for k in range(7):
                a=k*2.4;xx=x+math.cos(a)*r*.65;yy=142+math.sin(a)*r*.65;d.ellipse((xx-4,yy-4,xx+4,yy+4),fill=CORAL)
        footer(d,'A quantidade de partes não fixa a duração de cada uma')
    elif name in ('waterclock','water_compare'):
        label(d,(230,53),'CONTAR A MUDANÇA DO NÍVEL',17,GOLD,'mm')
        for j,x in enumerate([145,305] if name=='water_compare' else [224]):
            level=111+((t*(2+j))%53);d.polygon([(x-44,87),(x+44,87),(x+24,192),(x-24,192)],fill='#243a46',outline=GOLD,width=3)
            d.polygon([(x-37+(level-87)*.16,level),(x+37-(level-87)*.16,level),(x+20,188),(x-20,188)],fill='#3c9caf')
            for k in range(5):d.line((x+27,103+k*17,x+43,103+k*17),fill=WHITE,width=1)
            yy=199+(t*27)%21;rect(d,(x-2,yy,x+2,yy+6),TEAL)
            d.ellipse((x-35,224,x+35,230),fill='#276a80')
        footer(d,'O fluxo precisa ser controlado' if name=='water_compare' else 'Água em movimento como referência')
    elif name in ('regular_pulse','frequency'):
        label(d,(230,54),'UM RITMO PARA CONTAR',18,GOLD,'mm')
        for j in range(3):
            pts=[(x,99+j*35+12*math.sin(x*.11-t*3)) for x in range(57,402)]
            d.line(pts,fill=[TEAL,GOLD,CORAL][j],width=2)
        label(d,(228,216),'REPETIR  →  COMPARAR  →  CONTAR',13,WHITE,'mm')
    elif name in ('base60','divide60'):
        label(d,(231,52),'60',34,GOLD,'mm')
        if name=='base60':
            selected=int(t*.6)%6
            for row in range(6):
                for col in range(10):rect(d,(93+col*28,90+row*19,107+col*28,101+row*19),GOLD if row==selected else TEAL)
            footer(d,'60 unidades • contagem ilustrativa')
        else:
            for j,parts in enumerate([2,3,4]):
                y=103+j*41
                for k in range(parts):rect(d,(114+k*270/parts,y,111+(k+1)*270/parts,y+24),TEAL if k%2 else GOLD);label(d,(114+(k+.5)*270/parts,y+12),str(60//parts),12,NAVY,'mm')
                label(d,(81,y+12),'÷ '+str(parts),13,WHITE,'mm')
            footer(d,'Divisões sem sobras: uma vantagem matemática')
    elif name=='units':
        for j,(number,unit) in enumerate([('24','horas'),('60','minutos/h'),('60','segundos/min')]):
            x=103+j*126;rect(d,(x-49,84,x+49,190),'#163a4d');label(d,(x,116),number,30,GOLD,'mm');label(d,(x,163),unit,10,WHITE,'mm')
            if j<2:label(d,(x+62,137),'×',21,TEAL,'mm')
        footer(d,'As unidades constroem uma conta compartilhada')
    elif name=='seconds_day':
        label(d,(229,107),'86.400',49,GOLD,'mm');label(d,(229,161),'SEGUNDOS',21,TEAL,'mm')
        footer(d,'24 × 60 × 60 = 86.400')
    elif name=='gears':
        gear(d,161,141,65,t);gear(d,270,115,44,-t);gear(d,326,188,36,t)
        label(d,(226,55),'CONTROLAR O MOVIMENTO',18,GOLD,'mm');footer(d,'Pesos, engrenagens e mecanismos de controle')
    elif name=='pendulum':
        rect(d,(173,68,281,221),'#6b4c37');rect(d,(184,80,270,207),'#132b38');clock(d,(227,109),23,t)
        angle=math.sin(t*2.3)*.33;x=227+math.sin(angle)*62;y=143+math.cos(angle)*62
        d.line((227,143,x,y),fill=GOLD,width=3);d.ellipse((x-14,y-14,x+14,y+14),fill=GOLD)
        label(d,(99,106),'TIC',17,TEAL,'mm');label(d,(346,181),'TAC',17,CORAL,'mm');footer(d,'Um movimento regular para marcar intervalos')
    elif name in ('local_clocks','synchronized'):
        synchronized=name=='synchronized'
        for j,x in enumerate([131,327]):
            minute=0 if synchronized or j==0 else 12
            clock_at(d,(x,125),53,8,minute,t);label(d,(x,192),'08:00' if minute==0 else '08:12',22,GOLD,'mm');label(d,(x,65),'CIDADE '+('A' if j==0 else 'B'),12,WHITE,'mm')
        arrow(d,(204,125),(253,125),TEAL,2)
        footer(d,'Uma referência compartilhada' if synchronized else 'Exemplo: referências locais diferentes')
    elif name=='train_map':
        label(d,(229,51),'UMA REDE PRECISA COMBINAR HORAS',15,GOLD,'mm')
        pts=[(85,158),(203,109),(329,149),(213,206)]
        for a,b in [(pts[0],pts[1]),(pts[1],pts[2]),(pts[1],pts[3])]:d.line((a,b),fill=TEAL,width=4)
        for j,(x,y) in enumerate(pts):d.ellipse((x-9,y-9,x+9,y+9),fill=GOLD);label(d,(x,y-24),['Londres','Greenwich','Estações','Telégrafo'][j],11,WHITE,'mm')
        phase=(t*.22)%1;x=85+118*phase;y=158-49*phase;rect(d,(x-12,y-8,x+12,y+8),CORAL)
        footer(d,'Mapa esquemático • referências históricas britânicas')
    elif name=='timezones':
        earth(d,229,137,70,t)
        for j,(x,txt) in enumerate([(79,'07:00'),(232,'10:00'),(378,'14:00')]):
            rect(d,(x-43,188,x+43,213),'#173a4d');label(d,(x,200),txt,17,GOLD,'mm')
        label(d,(228,52),'O MESMO INSTANTE',20,WHITE,'mm');footer(d,'Horários ilustrativos em diferentes regiões')
    elif name=='two_days':
        for j,(x,a,b,c) in enumerate([(130,'ESTRELAS','23 h 56 min',TEAL),(324,'SOL MÉDIO','24 horas',GOLD)]):
            rect(d,(x-88,82,x+88,204),'#143345');label(d,(x,110),a,17,c,'mm');label(d,(x,167),b,18,WHITE,'mm')
        label(d,(229,54),'DUAS REFERÊNCIAS',20,GOLD,'mm');footer(d,'Valores aproximados • o dia solar real varia')
    elif name in ('orbit','extra_turn','sun_alignment'):
        sun(d,103,152,26)
        # One orbit advance is exaggerated so the solar alignment is visible.
        phase=(t*.16)%1;theta=.04+.30*phase;x=103+205*math.cos(theta);y=152-205*math.sin(theta)
        d.arc((-102,-53,308,357),-35,18,fill='#345264',width=2);earth(d,x,y,29,t)
        arrow(d,(x,y),(x-71,y),TEAL,2)
        if name!='orbit':arrow(d,(x,y),(x-72*math.cos(theta),y+72*math.sin(theta)),GOLD,2)
        d.arc((x-38,y-38,x+38,y+38),30,305,fill=WHITE,width=2)
        label(d,(367,96),'estrelas',10,TEAL,'mm')
        label(d,(230,52),{'orbit':'GIRAR E AVANÇAR','extra_turn':'UM PEQUENO GIRO EXTRA','sun_alignment':'VOLTAR A APONTAR PARA O SOL'}[name],16,GOLD,'mm')
        label(d,(119,86),'SOL',12,GOLD,'mm');label(d,(352,173),'TERRA',12,TEAL,'mm')
        label(d,(218,201),'≈ 4 MINUTOS A MAIS',15,CORAL,'mm')
        footer(d,'Esquema • movimento e ângulos ampliados',WHITE)
    elif name=='mean_day':
        label(d,(229,56),'DIA SOLAR MÉDIO',22,GOLD,'mm')
        for j in range(7):
            x=96+j*38;h=56+math.sin(j*.9)*15;rect(d,(x,195-h,x+23,195),'#31768b')
        d.line((77,135,379,135),fill=GOLD,width=3);label(d,(227,111),'24 HORAS',24,WHITE,'mm')
        footer(d,'Variação ilustrativa dos dias solares ao longo do ano')
    elif name=='quartz':
        label(d,(230,55),'QUARTZO',24,GOLD,'mm')
        x=191+math.sin(t*8)*3;d.polygon([(x,87),(x+59,94),(x+72,171),(x+28,196),(x-25,167),(x-20,108)],fill='#8cbccc',outline=TEAL,width=3)
        d.line((x+18,100,x+35,176),fill=WHITE,width=3);d.line((x-8,117,x+49,152),fill='#b7e2e7',width=2)
        for xx in [110,315]:d.line([(xx,120+k*3) for k in range(20)],fill=GOLD,width=2)
        footer(d,'Vibrações contadas por um circuito eletrônico')
    elif name=='circuit':
        rect(d,(113,76,335,211),'#194c46')
        for k in range(6):
            yy=96+k*18;d.line((129,yy,182,yy,182,139+k*3,224,139+k*3),fill=TEAL,width=2)
            d.line((270,109+k*13,317,109+k*13),fill=GOLD,width=2)
        rect(d,(208,108,271,177),'#112b35');label(d,(239,140),'RITMO',12,WHITE,'mm')
        pulse=129+(t*49)%180;d.ellipse((pulse-3,193,pulse+3,199),fill=CORAL)
        footer(d,'Eletrônica transforma repetição em marcação')
    elif name=='atom':
        label(d,(230,54),'UMA REFERÊNCIA ATÔMICA',18,GOLD,'mm')
        for y,col,txt in [(113,TEAL,'nível 2'),(186,GOLD,'nível 1')]:d.line((114,y,343,y),fill=col,width=3);label(d,(91,y),txt,9,WHITE,'rm')
        arrow(d,(229,176),(229,123),CORAL,3)
        for k in range(70):
            x=272+k;yy=152+6*math.sin(k*.27-t*4)
            if k>0:d.line((x-1,previous,x,yy),fill=WHITE,width=1)
            previous=yy
        label(d,(241,210),'SINAL ↔ REFERÊNCIA',12,TEAL,'mm');footer(d,'Diagrama conceitual de níveis de energia',WHITE)
    elif name=='cesium':
        rect(d,(78,77,199,204),'#174453');label(d,(91,88),'55',12,TEAL);label(d,(138,141),'Cs',45,GOLD,'mm');label(d,(138,184),'CÉSIO-133',11,WHITE,'mm')
        label(d,(295,112),'9.192.631.770',18,GOLD,'mm');label(d,(295,151),'períodos',16,WHITE,'mm');label(d,(295,179),'em 1 segundo',13,TEAL,'mm')
        footer(d,'A definição atômica do segundo foi adotada em 1967')
    elif name in ('satellites','signal_time'):
        earth(d,225,160,52,t)
        for j,(x,y) in enumerate([(103,81),(334,84),(354,201),(94,210)]):
            rect(d,(x-9,y-7,x+9,y+7),GOLD);rect(d,(x-30,y-5,x-13,y+5),TEAL);rect(d,(x+13,y-5,x+30,y+5),TEAL)
            if name=='signal_time':
                phase=(t*.5+j*.23)%1;xx=x+(226-x)*phase;yy=y+(156-y)*phase;d.line((x,y,226,156),fill='#376e82',width=1);d.ellipse((xx-3,yy-3,xx+3,yy+3),fill=CORAL)
        label(d,(229,48),'MEDIR TEMPO PARA ACHAR POSIÇÃO',14,GOLD,'mm');footer(d,'Sinais de vários satélites • esquema sem escala')
    elif name=='recap':
        label(d,(229,52),'MILHARES DE ANOS NO SEU RELÓGIO',15,GOLD,'mm')
        clock(d,(229,145),49,t)
        for j,(txt,x,y) in enumerate([('Sombras',97,99),('Água',99,170),('Trens',219,213),('Quartzo',350,174),('Átomos',351,103)]):
            d.line((229,145,x,y),fill='#396779',width=2);rect(d,(x-41,y-12,x+41,y+12),'#16394c');label(d,(x,y),txt,12,TEAL,'mm')
    elif name=='end':
        for k in range(170):
            a=k*math.pi*2/170;xx=240+94*math.cos(a)/(1+math.sin(a)**2);yy=104+94*math.sin(a)*math.cos(a)/(1+math.sin(a)**2);rect(d,(xx-2,yy-2,xx+2,yy+2),GOLD if k%7==0 else TEAL)
        label(d,(240,187),'QUASE INFINITO',28,WHITE,'mm');label(d,(240,222),'Cada pergunta abre outra viagem.',12,GOLD,'mm')
    else:raise ValueError('Unknown original scene: '+name)
    stage=Image.new('RGB',(W,H),NAVY);stage.paste(im.resize((768,432),Image.Resampling.NEAREST),(96,16));return stage

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

def overlay(item,scene,t,global_time,cue,source='',pixel=False):
    layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer)
    rect(d,(0,0,W,42),(5,18,29,230));rect(d,(0,443,W,H),(5,18,29,235))
    d.rectangle((12,12,W-13,H-13),outline=(110,240,211,240),width=2)
    for x,y,sx,sy in [(12,12,1,1),(948,12,-1,1),(12,528,1,-1),(948,528,-1,-1)]:
        d.line((x+sx*31,y,x,y,x,y+sy*23),fill=GOLD,width=4)
    label(d,(32,12),'QUASE INFINITO',16,WHITE)
    label(d,(927,14),'02 / 24 HORAS',12,TEAL,'ra')
    if t<3.2:
        alpha=int(235*min(1,max(0,(3.2-t)/.4)))
        width=min(650,int(d.textlength(item['title'],font=font(20,True)))+34)
        rect(d,(30,51,30+width,86),(5,18,29,alpha));label(d,(45,57),item['title'],20,GOLD)
    if source and not pixel:
        credit=source[:100];width=int(d.textlength(credit,font=font(11,True)))+15
        rect(d,(25,416,min(790,25+width),440),(5,18,29,215));label(d,(31,421),credit,11,'#e5eeeb')
    if cue:
        lines=wrap(cue)
        if len(lines)>2:lines=wrap(cue,65)
        for j,line in enumerate(lines[:2]):
            label(d,(480,453+j*28),line,24,WHITE,'ma')
    rect(d,(28,521,932,524),'#28434f');rect(d,(28,521,28+904*min(1,global_time/504),524),TEAL)
    action=item['action'];x=805+int(14*math.sin(t*.7));y=303+int(8*math.sin(t*2.3))
    if action=='fly':
        x=782+int(28*math.sin(t*.8));y=280+int(18*math.sin(t*.6))
    elif action=='follow':
        x=805+int(14*math.sin(t*.7));y=274+int(22*math.sin(t*.7))
    elif action=='carry':x=765+int(22*math.sin(t*.9));y=287+int(6*math.sin(t*2))
    if scene=='end':x=433+int(math.sin(t)*18);y=104+int(8*math.sin(t*2))
    layer.alpha_composite(pico(action,t,scene),(x,y))
    return layer
