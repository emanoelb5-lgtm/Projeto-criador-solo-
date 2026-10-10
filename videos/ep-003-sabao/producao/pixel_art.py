"""Original animated soap diagrams and the established Quase Infinito frame."""
import math
from PIL import Image,ImageDraw
from base_art import W,H,NAVY,TEAL,GOLD,CORAL,WHITE,font,rect,label,arrow,pico,wrap,starfield

def circle(d,x,y,r,color,outline=None):
    d.ellipse((int(x-r),int(y-r),int(x+r),int(y+r)),fill=color,outline=outline,width=2)
def water(d,x,y,r=11,t=0,marks=False):
    a=math.sin(t*.3)*.12
    for dx,dy in [(-r*.75,r*.65),(r*.75,r*.65)]:
        d.line((x,y,x+dx,y+dy),fill=WHITE,width=3)
        circle(d,x+dx,y+dy,r*.53,WHITE)
    circle(d,x,y,r,TEAL,'#285b68')
    if marks:
        label(d,(x,y-r-6),'δ−',10,TEAL,'mm')
        label(d,(x-r,y+r+13),'δ+',9,WHITE,'mm')
        label(d,(x+r,y+r+13),'δ+',9,WHITE,'mm')
def surfactant(d,x,y,angle,length=30,r=5,head=TEAL,tail=GOLD):
    points=[(x,y)]
    for k in range(1,7):
        amount=length*k/6;side=2.5 if k%2 else -2.5
        points.append((round(x+math.cos(angle)*amount-math.sin(angle)*side),round(y+math.sin(angle)*amount+math.cos(angle)*side)))
    d.line(points,fill=tail,width=3);circle(d,x,y,r,head,'#123c48')
def droplet(d,x,y,r=10,color=GOLD):
    d.polygon([(x,y-r*1.9),(x-r*.88,y-r*.05),(x+r*.88,y-r*.05)],fill=color)
    circle(d,x,y,r,color);circle(d,x-r*.3,y-r*.35,r*.22,'#fff0ba')
def plate(d,x=220,y=147,r=84,dirty=True,t=0):
    d.ellipse((x-r,y-r*.60,x+r,y+r*.60),fill='#d6e4df',outline=WHITE,width=4)
    d.ellipse((x-r*.72,y-r*.43,x+r*.72,y+r*.43),fill='#f1eee1',outline='#87a7ab',width=3)
    if dirty:
        for k in range(6):
            xx=x-48+k*17;yy=y+math.sin(k*1.8)*15
            d.ellipse((xx-16,yy-8,xx+16,yy+8),fill='#c59537')
            d.arc((x-53,y-31,x+55,y+32),20,330,fill=GOLD,width=3)
    else:
        for xx,yy in [(x-31,y-18),(x+39,y+8)]:
            d.line((xx-7,yy,xx+7,yy),fill=TEAL,width=2);d.line((xx,yy-7,xx,yy+7),fill=TEAL,width=2)
def faucet(d,x=350,y=60,t=0):
    rect(d,(x-5,y-20,x+8,y+35),'#adc0ca');rect(d,(x-42,y-23,x+9,y-10),'#d9e4e5')
    rect(d,(x-47,y-18,x-35,y+2),'#d9e4e5')
    for j in range(9):
        yy=y+15+(j*15+t*35)%135
        rect(d,(x-45+math.sin(t+j)*3,yy,x-39+math.sin(t+j)*3,yy+9),TEAL)
def bottle(d,x=90,y=142,color=TEAL,text='SABÃO'):
    d.rounded_rectangle((x-25,y-48,x+25,y+45),radius=9,fill=color,outline=WHITE,width=2)
    rect(d,(x-13,y-65,x+13,y-49),'#587a87');rect(d,(x-14,y-73,x+27,y-66),WHITE)
    rect(d,(x+21,y-69,x+29,y-57),WHITE)
    rect(d,(x-23,y-7,x+23,y+23),NAVY);label(d,(x,y+8),text,10,WHITE,'mm')
def sphere(d,x,y,r=46,t=0,oil=False,heads=True):
    circle(d,x,y,r,'#253c49' if not oil else '#a4792a',GOLD if oil else '#365a6c')
    if oil:
        for k in range(5):circle(d,x+math.sin(k*2.1)*r*.55,y+math.cos(k*1.4)*r*.45,r*.16,GOLD)
    for k in range(14):
        angle=k*2*math.pi/14+t*.08
        surfactant(d,x+r*math.cos(angle),y+r*math.sin(angle),angle+math.pi,length=r*.40,r=4)
def card(d,x,y,title,color=TEAL):
    d.rounded_rectangle((x-65,y-26,x+65,y+26),radius=6,fill='#173545',outline=color,width=2)
    label(d,(x,y),title,12,color,'mm')
def water_background(d,t):
    for k in range(18):
        x=31+(k*67)%414+math.sin(t*.5+k)*8;y=71+(k*53)%148+math.cos(t*.6+k)*5
        circle(d,x,y,2,'#254f64')
def foot(d,text):label(d,(235,239),text,10,TEAL,'mm')
def bubble(d,x,y,r,t=0):
    d.ellipse((x-r,y-r,x+r,y+r),outline=TEAL,width=2)
    d.arc((x-r+3,y-r+3,x+r-3,y+r-3),190,275,fill=WHITE,width=2)
    d.arc((x-r+1,y-r+1,x+r-1,y+r-1),20,95,fill=CORAL,width=2)
def pixel_scene(name,t):
    im=Image.new('RGB',(480,270),NAVY);d=ImageDraw.Draw(im)
    water_background(d,t)
    if name in ('oily_plate','mystery','question_return'):
        plate(d,t=t);faucet(d,t=t)
        if name!='oily_plate':label(d,(100,110),'?',64,GOLD,'mm')
        foot(d,'Para onde vai a gordura depois da lavagem?')
    elif name in ('sink_journey','zoom'):
        plate(d,x=130,y=152,r=69,t=t)
        d.ellipse((267,66,395,194),fill='#183c50',outline=TEAL,width=4)
        d.line((371,171,410,210),fill=GOLD,width=9)
        for k in range(8):surfactant(d,300+(k*17)%78,94+(k*29)%73,t*.2+k,length=15,r=3)
        arrow(d,(207,153),(254,130));foot(d,'Uma viagem para dentro de uma gota')
    elif name in ('glass_layers','shaking','separate'):
        d.rounded_rectangle((132,57,329,207),radius=10,outline=WHITE,width=3)
        rect(d,(137,118,324,203),'#266f87')
        if name=='shaking':
            for k in range(19):circle(d,147+(k*31)%161+math.sin(t*3+k)*4,83+(k*41)%112,4+(k%3),GOLD)
        else:
            rect(d,(137,76,324,117),'#a77d2d')
            label(d,(232,97),'ÓLEO',15,GOLD,'mm');label(d,(232,163),'ÁGUA',15,WHITE,'mm')
        foot(d,'Agitar dispersa por um tempo; as gotinhas podem se reunir')
    elif name in ('water_molecules','polarity','water_network'):
        for k,(x,y) in enumerate([(108,124),(232,94),(335,141),(220,185)]):
            water(d,x+math.sin(t+k)*3,y,23,t,marks=name=='polarity')
        if name=='water_network':
            for a,b in [((121,130),(206,109)),((252,110),(307,137)),((244,178),(319,150))]:
                for j in range(5):
                    x=a[0]+(b[0]-a[0])*j/5;y=a[1]+(b[1]-a[1])*j/5
                    circle(d,x,y,1,GOLD)
        foot(d,'Regiões com cargas parciais diferentes • modelo ampliado')
    elif name in ('oil_chains','water_oil','partners'):
        if name=='oil_chains':
            for j in range(3):
                pts=[(80+k*38,102+j*41+(12 if k%2 else 0)) for k in range(8)]
                d.line(pts,fill=GOLD,width=4)
                for x,y in pts:circle(d,x,y,5,'#b27f27')
            foot(d,'Grandes regiões pouco compatíveis com a água')
        else:
            rect(d,(25,64,213,209),'#143b50');rect(d,(249,64,437,209),'#4d4024')
            for k in range(5):water(d,61+(k*43)%120,88+(k*53)%98,12,t)
            for k in range(5):droplet(d,281+(k*29)%119,101+(k*43)%88,12)
            label(d,(123,220),'ÁGUA',13,TEAL,'mm');label(d,(344,220),'GORDURA',13,GOLD,'mm')
    elif name in ('soap_molecule','head_tail','head_inwater','tail_inoil'):
        surfactant(d,136,139,0,length=220,r=22)
        if name=='head_inwater':
            for k in range(4):water(d,105+math.cos(k*1.55+t*.15)*67,139+math.sin(k*1.55+t*.15)*58,12,t)
        elif name=='tail_inoil':
            rect(d,(224,81,385,198),'#62502a')
            surfactant(d,136,139,0,length=220,r=22);droplet(d,317,116,17)
        label(d,(130,89),'CABEÇA',13,TEAL,'mm');label(d,(307,187),'CAUDA',13,GOLD,'mm')
        foot(d,'A cabeça interage com água; a cauda com gordura')
    elif name in ('interface','bridge','soap_many'):
        rect(d,(24,51,441,136),'#185369');rect(d,(24,138,441,209),'#826325')
        for k in range(4 if name=='soap_many' else 3):
            surfactant(d,100+k*85,121,math.pi/2,length=52,r=9)
        label(d,(385,76),'ÁGUA',13,WHITE,'mm');label(d,(366,187),'GORDURA',13,GOLD,'mm')
        foot(d,'Moléculas posicionadas na interface entre os materiais')
    elif name in ('surround','release','oil_drop','droplets','emulsion'):
        if name in ('droplets','emulsion'):
            for k in range(5):sphere(d,70+k*83,130+math.sin(t*.8+k)*35,23,t,oil=True)
            foot(d,'Gotículas dispersas com moléculas na superfície')
        else:
            sphere(d,231+math.sin(t*.45)*7,139,67,t,oil=True)
            for k in range(9):water(d,47+(k*73)%390,65+(k*49)%153,7,t)
            foot(d,'Gota de gordura revestida • desenho sem escala')
    elif name in ('micelle','micelle_inside','micelle_escape'):
        sphere(d,229+math.sin(t*.4)*5,140,64,t)
        for k in range(4):circle(d,221+math.sin(k*2.1)*21,139+math.cos(k*1.7)*18,7,GOLD)
        label(d,(231,55),'MICELA',19,GOLD,'mm')
        if name=='micelle_inside':arrow(d,(363,150),(261,142),CORAL,2)
        foot(d,'Caudas para dentro; cabeças em contato com a água')
    elif name in ('sponge','detach'):
        plate(d,x=200,t=t)
        x=183+math.sin(t*2)*35
        d.rounded_rectangle((x-34,76,x+34,117),radius=6,fill=GOLD,outline=WHITE,width=2)
        rect(d,(x-33,109,x+33,122),'#5ea37f')
        for k in range(5):circle(d,x-22+k*11,88+(k%2)*8,2,'#b48233')
        if name=='detach':
            for k in range(6):droplet(d,279+(k*17+t*15)%105,108+(k*29)%86,5)
        foot(d,'O movimento ajuda a desprender e dispersar o material')
    elif name in ('stream','rinse','final_journey'):
        plate(d,x=132,r=70,dirty=False,t=t);faucet(d,x=199,t=t)
        for k in range(4):
            x=215+(t*28+k*46)%220;y=130+math.sin(t*.6+k)*35
            sphere(d,x,y,15,t,oil=True)
        arrow(d,(228,212),(419,212))
        foot(d,'O material desprendido segue com a água do enxágue')
    elif name in ('whole_process','recap'):
        for x,text,color in [(78,'SOLTAR',GOLD),(230,'DISPERSAR',TEAL),(382,'LEVAR',WHITE)]:
            card(d,x,148,text,color)
        arrow(d,(149,147),(155,147),GOLD,2);arrow(d,(301,147),(306,147),TEAL,2)
        label(d,(231,80),'A VIAGEM DA GORDURA',18,GOLD,'mm')
        foot(d,'Moléculas + movimento + enxágue')
    elif name=='plate_clean':
        plate(d,x=232,r=112,dirty=False,t=t);foot(d,'Uma superfície limpa: o material mudou de lugar')
    elif name in ('foam','bubbles_float'):
        for k in range(17):
            x=35+(k*61)%408;y=83+(k*47-t*14)%118
            bubble(d,x,y,12+(k%3)*5,t)
        foot(d,'A espuma contém bolhas com ar')
    elif name=='bubble_cut':
        bubble(d,190,138,68,t);label(d,(190,138),'AR',23,WHITE,'mm')
        d.line((259,133,319,98),fill=GOLD,width=2)
        rect(d,(333,91,340,197),GOLD);rect(d,(340,91,361,197),TEAL);rect(d,(361,91,368,197),GOLD)
        label(d,(351,64),'PELÍCULA',11,GOLD,'mm')
        label(d,(351,217),'ÁGUA + SABÃO',10,TEAL,'mm')
        foot(d,'Corte esquemático ampliado: camada líquida entre interfaces')
    elif name in ('bubble_vs_micelle','architecture'):
        sphere(d,123,146,43,t);bubble(d,332,146,63,t)
        label(d,(123,63),'MICELA',16,GOLD,'mm');label(d,(332,63),'BOLHA',16,TEAL,'mm')
        label(d,(332,146),'AR',18,WHITE,'mm');foot(d,'Círculos parecidos; estruturas diferentes • sem escala')
    elif name in ('hardwater','minerals','soap_scum','mineral_react','residue','waters_compare','water_conditions'):
        if name in ('minerals','hardwater','mineral_react','water_conditions'):
            for k in range(7):water(d,67+(k*61)%348,95+(k*43)%108,12,t)
            for k,(x,y) in enumerate([(137,93),(260,167),(342,110)]):
                circle(d,x+math.sin(t+k)*4,y,23,CORAL);label(d,(x+math.sin(t+k)*4,y),'Ca' if k%2==0 else 'Mg',13,NAVY,'mm')
            foot(d,'Cálcio e magnésio dissolvidos: a composição faz diferença')
        elif name=='waters_compare':
            card(d,121,135,'ÁGUA A',TEAL);card(d,347,135,'ÁGUA B',CORAL)
            for k in range(2):circle(d,100+k*40,189,8,CORAL)
            for k in range(6):circle(d,295+k*20,189,8,CORAL)
            foot(d,'Diferentes concentrações de minerais • comparação ilustrativa')
        else:
            d.rectangle((110,76,352,202),outline=WHITE,width=3)
            for k in range(24):circle(d,119+(k*31)%225,169+(k*13)%27,3+(k%3),'#c7d2ce')
            foot(d,'Alguns minerais reagem com sabão e formam resíduos')
    elif name in ('soap_factory','saponification'):
        droplet(d,90,126,30)
        label(d,(90,193),'ÓLEOS / GORDURAS',9,GOLD,'mm')
        card(d,233,128,'REAÇÃO',TEAL);arrow(d,(132,125),(160,125));arrow(d,(306,125),(330,125))
        d.rounded_rectangle((348,100,415,150),radius=8,fill=TEAL,outline=WHITE,width=2)
        label(d,(382,124),'SABÃO',11,NAVY,'mm');label(d,(380,193),'NOVO MATERIAL',9,TEAL,'mm')
        foot(d,'Transformação química dos materiais de partida')
    elif name in ('soap_detergent','molecule_compare','shelves','formulation'):
        if name=='shelves':
            rect(d,(33,176,443,184),'#38606a')
            for k in range(5):bottle(d,77+k*77,122,TEAL if k%2 else CORAL,'LIMPEZA')
            foot(d,'Produtos diferentes podem compartilhar o mesmo princípio')
        elif name=='formulation':
            bottle(d,x=225,y=151)
            for k,(txt,x,y) in enumerate([('Moléculas',85,93),('Ingredientes',350,104),('Água',114,193),('Movimento',355,201)]):
                card(d,x,y,txt,GOLD if k%2 else TEAL);d.line((x,y,225,140),fill='#467688',width=1)
            foot(d,'O produto é uma formulação: vários fatores atuam juntos')
        else:
            surfactant(d,94,106,0,length=97,r=16);surfactant(d,280,171,0,length=97,r=16,head=CORAL)
            label(d,(121,72),'SABÃO',15,TEAL,'mm');label(d,(327,212),'DETERGENTE',15,CORAL,'mm')
            foot(d,'Composições diferentes; regiões com afinidades distintas')
    elif name in ('see_everyday','hidden_world','next_question'):
        for k,(x,y,r) in enumerate([(92,139,48),(229,119,64),(365,148,44)]):
            bubble(d,x,y,r,t);label(d,(x,y),'?' if name=='next_question' else ('ÁGUA' if k==0 else 'IDEIAS' if k==1 else 'PICO'),18,GOLD if k%2 else WHITE,'mm')
        foot(d,'Qual detalhe da sua rotina merece outra investigação?')
    elif name=='end':
        for k in range(170):
            a=k*math.pi*2/170;x=240+94*math.cos(a)/(1+math.sin(a)**2);y=104+94*math.sin(a)*math.cos(a)/(1+math.sin(a)**2)
            rect(d,(x-2,y-2,x+2,y+2),GOLD if k%7==0 else TEAL)
        label(d,(240,187),'QUASE INFINITO',28,WHITE,'mm')
        label(d,(240,222),'Cada pergunta abre outra viagem.',12,GOLD,'mm')
    else:raise ValueError('Unknown soap scene: '+name)
    stage=Image.new('RGB',(W,H),NAVY)
    stage.paste(im.resize((768,432),Image.Resampling.NEAREST),(96,16))
    return stage

def overlay(item,scene,t,global_time,cue,source='',pixel=False):
    layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer)
    rect(d,(0,0,W,42),(5,18,29,230));rect(d,(0,443,W,H),(5,18,29,235))
    d.rectangle((12,12,W-13,H-13),outline=(110,240,211,240),width=2)
    for x,y,sx,sy in [(12,12,1,1),(948,12,-1,1),(12,528,1,-1),(948,528,-1,-1)]:
        d.line((x+sx*31,y,x,y,x,y+sy*23),fill=GOLD,width=4)
    label(d,(32,12),'QUASE INFINITO',16,WHITE)
    label(d,(927,14),'03 / SABÃO',12,TEAL,'ra')
    if t<3.2:
        width=min(740,int(d.textlength(item['title'],font=font(20,True)))+34)
        rect(d,(30,51,30+width,86),(5,18,29,230));label(d,(45,57),item['title'],20,GOLD)
    if source and not pixel:
        credit=source[:95];width=int(d.textlength(credit,font=font(11,True)))+15
        rect(d,(25,416,min(790,25+width),440),(5,18,29,215));label(d,(31,421),credit,11,'#e5eeeb')
    if cue:
        lines=wrap(cue)
        if len(lines)>2:lines=wrap(cue,65)
        for j,line in enumerate(lines[:2]):label(d,(480,453+j*28),line,24,WHITE,'ma')
    rect(d,(28,521,932,524),'#28434f');rect(d,(28,521,28+904*min(1,global_time/504),524),TEAL)
    action=item['action'];x=805+int(14*math.sin(t*.7));y=303+int(8*math.sin(t*2.3))
    if action=='fly':x=782+int(28*math.sin(t*.8));y=280+int(18*math.sin(t*.6))
    elif action=='follow':x=805+int(14*math.sin(t*.7));y=274+int(22*math.sin(t*.7))
    if scene=='end':x=433+int(math.sin(t)*18);y=104+int(8*math.sin(t*2))
    layer.alpha_composite(pico(action,t,scene),(x,y))
    return layer

