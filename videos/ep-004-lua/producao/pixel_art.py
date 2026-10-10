"""Original Moon, parallax and perception diagrams; established Pico and frame."""
import math
from PIL import Image,ImageDraw
from base_art import W,H,NAVY,TEAL,GOLD,CORAL,WHITE,font,rect,label,arrow,pico,wrap,earth,sun

def circle(d,x,y,r,color,outline=None):
    d.ellipse((round(x-r),round(y-r),round(x+r),round(y+r)),fill=color,outline=outline,width=2)
def foot(d,text):label(d,(235,239),text,10,TEAL,'mm')
def stars(d,t):
    for k in range(48):
        x=18+(k*79)%443;y=37+(k*47)%153
        rect(d,(x,y,x+1,y+1),WHITE if (k+int(t))%11==0 else '#28465f')
def moon(d,x,y,r=28,phase='full'):
    circle(d,x,y,r,'#e7e6ce','#b2d2d2')
    for dx,dy,rr in [(-.25,-.34,.17),(.38,.12,.2),(-.11,.38,.12),(.21,-.29,.1),(-.46,.12,.09)]:
        circle(d,x+dx*r,y+dy*r,r*rr,'#b2bfae')
    if phase=='crescent':circle(d,x+r*.46,y-r*.12,r*.87,NAVY)
    rect(d,(x-r*.5,y-r*.55,x-r*.35,y-r*.45),'#f5f3dd')
def tree(d,x,y,size=1):
    rect(d,(x-3*size,y-27*size,x+3*size,y),'#865f42')
    d.polygon([(x,y-77*size),(x-27*size,y-26*size),(x+27*size,y-26*size)],fill='#276b64')
    d.polygon([(x,y-67*size),(x-21*size,y-35*size),(x+21*size,y-35*size)],fill='#418b7a')
def house(d,x,y,size=1):
    rect(d,(x-20*size,y-33*size,x+20*size,y),'#446278')
    d.polygon([(x-26*size,y-33*size),(x,y-53*size),(x+26*size,y-33*size)],fill='#bd6d5a')
    rect(d,(x-9*size,y-21*size,x+2*size,y-9*size),GOLD)
def car(d,x,y,t=0,color=CORAL,size=1):
    rect(d,(x-33*size,y-16*size,x+36*size,y+4*size),color)
    d.polygon([(x-23*size,y-16*size),(x-13*size,y-32*size),(x+12*size,y-32*size),(x+27*size,y-16*size)],fill=color)
    rect(d,(x-11*size,y-28*size,x+8*size,y-17*size),'#193a52')
    rect(d,(x+12*size,y-26*size,x+19*size,y-17*size),TEAL)
    for dx in [-20,22]:
        circle(d,x+dx*size,y+4*size,8*size,'#07111e',WHITE)
        a=t*4
        d.line((x+dx*size-4*math.cos(a)*size,y+4*size-4*math.sin(a)*size,x+dx*size+4*math.cos(a)*size,y+4*size+4*math.sin(a)*size),fill=TEAL,width=2)
    rect(d,(x+33*size,y-11*size,x+37*size,y-6*size),GOLD)
def road(d,y=213):
    rect(d,(0,y,480,270),'#23364a')
    for x in range(5,480,50):rect(d,(x,y+15,x+25,y+17),GOLD)
def mountains(d,y=165,t=0):
    for k in range(6):
        x=-60+k*103-(t*3)%103
        d.polygon([(x-68,y),(x+8,y-60-k%2*22),(x+85,y)],fill='#23465b')
        d.polygon([(x-30,y-37),(x+8,y-60-k%2*22),(x+32,y-34)],fill='#44718a')
def window(d,t=0,close=False):
    stars(d,t);mountains(d,163,t);moon(d,342,88,32)
    rect(d,(0,181,480,217),'#16414c')
    for k in range(6):tree(d,((k*120-t*(52 if close else 35))%660)-80,209,.78)
    road(d,212)
    rect(d,(0,29,480,42),'#294857');rect(d,(0,40,18,228),'#294857');rect(d,(459,40,480,228),'#294857')
    rect(d,(0,221,480,239),'#345262')
def card(d,x,y,text,color=TEAL,width=128):
    d.rounded_rectangle((x-width/2,y-23,x+width/2,y+23),radius=5,fill='#19394d',outline=color,width=2)
    label(d,(x,y),text,12,color,'mm')
def observers(d,y=214):
    for x,c,text in [(125,TEAL,'A'),(335,CORAL,'B')]:
        circle(d,x,y,7,c);label(d,(x,y+17),text,11,c,'mm')
    d.line((125,y+8,335,y+8),fill=GOLD,width=2)
def geometry(d,t,far=False,compare=False):
    observers(d)
    if compare:
        targets=[(230,146,TEAL),(230,61,GOLD)]
    else:targets=[(230,65 if far else 146,TEAL)]
    for x,y,c in targets:
        circle(d,x,y,8,c)
        for xx in [125,335]:d.line((xx,214,x,y),fill=c,width=2)
        d.arc((x-22,y-22,x+22,y+22),25,155,fill=c,width=2)
    label(d,(230,38),'MESMO DESLOCAMENTO',13,WHITE,'mm')
    foot(d,'Esquema sem escala • muda a direção da visão')
def pencil(d,x,y,size=1):
    rect(d,(x-5*size,y-43*size,x+5*size,y+42*size),GOLD)
    rect(d,(x-5*size,y-43*size,x+5*size,y-32*size),CORAL)
    d.polygon([(x-5*size,y+42*size),(x+5*size,y+42*size),(x,y+53*size)],fill='#d9b97e')
def pencil_view(d,t,mode):
    rect(d,(35,53,417,221),'#23485d')
    for x in [86,188,289,386]:rect(d,(x,67,x+8,216),'#517183')
    shift=(-1 if mode=='left_eye' else 1) if mode in ('left_eye','right_eye') else math.sin(t*1.6)
    amount=47 if mode=='pencil_near' else 17 if mode=='pencil_far' else 31
    pencil(d,225+shift*amount,140,1.03)
    if mode in ('left_eye','right_eye'):label(d,(232,34),'OLHO ESQUERDO' if mode=='left_eye' else 'OLHO DIREITO',13,GOLD,'mm')
    else:label(d,(232,34),'UM LÁPIS. DOIS PONTOS DE VISTA.',12,GOLD,'mm')
    foot(d,'O lápis fica parado • a observação muda')
def camera(d,x,y):
    rect(d,(x-28,y-17,x+28,y+21),'#507183');rect(d,(x-18,y-25,x,y-16),TEAL)
    circle(d,x+5,y+3,13,'#18374d',TEAL);circle(d,x+5,y+3,6,'#72baba')
def orbital(d,t,stellar=False):
    sun(d,155,140,22)
    d.ellipse((63,48,247,232),outline='#416a81',width=2)
    a=t*.16
    if not stellar:earth(d,155+92*math.cos(a),140+92*math.sin(a),14,t)
    if stellar:
        rect(d,(379,107,381,129),GOLD);rect(d,(370,117,390,119),GOLD)
        for x,y in [(438,66),(437,113),(428,172)]:rect(d,(x,y,x+2,y+2),WHITE)
        for xx,yy in [(63,140),(247,140)]:
            d.line((xx,yy,380,118),fill=TEAL,width=2);earth(d,xx,yy,11,t)
            label(d,(xx,yy+23),'A' if xx==63 else 'B',10,TEAL,'mm')
        label(d,(155,35),'ÓRBITA DA TERRA',12,GOLD,'mm')
        foot(d,'Paralaxe estelar • deslocamentos ampliados')
    else:foot(d,'Esquema • posições e tempos sem escala')

def pixel_scene(name,t):
    im=Image.new('RGB',(480,270),NAVY);d=ImageDraw.Draw(im)
    stars(d,t)
    if name in ('car_window','return_window'):
        window(d,t);foot(d,'A paisagem passa. A Lua continua lá longe.')
    elif name in ('moon_mystery','moon_question'):
        moon(d,276,115,69);label(d,(128,130),'?',65,GOLD,'mm')
        foot(d,'Por que ela parece acompanhar você?')
    elif name=='two_cars':
        moon(d,236,76,30);road(d,219);car(d,116,202,t,CORAL);car(d,349,202,-t,TEAL)
        label(d,(117,163),'UMA PESSOA',10,WHITE,'mm');label(d,(348,163),'OUTRA PESSOA',10,WHITE,'mm');foot(d,'Duas viagens • a mesma Lua')
    elif name=='roadside_posts':
        moon(d,341,74);mountains(d,154,t);road(d,215)
        for k in range(7):
            x=(k*95-t*75)%650-80
            rect(d,(x,102,x+8,221),'#67818c');rect(d,(x-6,99,x+20,108),GOLD)
        foot(d,'O que está perto cruza a janela depressa')
    elif name=='landscape_layers':
        moon(d,344,66,22);mountains(d,151,t)
        for k in range(5):tree(d,(k*118-t*17)%620-80,196,.6)
        road(d,217)
        for k in range(5):
            x=(k*112-t*63)%610-70;rect(d,(x,161,x+5,223),GOLD)
        label(d,(94,56),'LUA',10,WHITE);label(d,(48,121),'SERRA',10,GOLD);label(d,(40,178),'POSTES',10,TEAL)
        foot(d,'Distâncias diferentes • mudanças aparentes diferentes')
    elif name in ('tree_observer','view_a_b','angle_tree'):
        tree(d,243,154,1.1);road(d,215)
        x=108+(math.sin(t*.6)+1)*113 if name=='tree_observer' else (110 if name=='view_a_b' and int(t*.65)%2==0 else 339)
        car(d,x,217,t,size=.7);arrow(d,(x,192),(243,91),TEAL)
        if name=='angle_tree':
            d.line((110,192,243,91,339,192),fill=GOLD,width=2);label(d,(238,54),'A DIREÇÃO MUDA',15,GOLD,'mm')
        foot(d,'A árvore fica • o observador se desloca')
    elif name=='earth_moon_distance':
        earth(d,75,133,44,t);moon(d,392,132,12)
        d.line((121,133,375,133),fill=TEAL,width=2)
        label(d,(252,104),'384.400 km',26,GOLD,'mm');label(d,(252,156),'DISTÂNCIA MÉDIA',12,WHITE,'mm')
        foot(d,'Terra e Lua • esquema sem escala')
    elif name=='thirty_earths':
        for k in range(30):earth(d,42+k*12.1,148,5,t)
        earth(d,36,148,12,t);moon(d,423,148,5)
        label(d,(236,88),'CERCA DE 30 TERRAS',23,GOLD,'mm');foot(d,'Comparação de distância • ilustração simplificada')
    elif name in ('pencil_test','left_eye','right_eye','pencil_near','pencil_far'):pencil_view(d,t,name)
    elif name=='parallax_word':
        label(d,(235,100),'PARALAXE',35,GOLD,'mm');arrow(d,(115,164),(172,164));arrow(d,(352,164),(296,164),CORAL)
        pencil(d,235+math.sin(t)*19,159,.48);foot(d,'O ponto de observação muda • a direção aparente também')
    elif name in ('sightlines_near','sightlines_far','rays_comparison'):
        geometry(d,t,far=name=='sightlines_far',compare=name=='rays_comparison')
    elif name=='street_scale':
        road(d,207)
        for k in range(5):house(d,70+k*80,197,.6)
        car(d,80+(t*27)%275,211,t,size=.75)
        label(d,(236,71),'UM TRECHO DE RUA',24,GOLD,'mm');foot(d,'Pequeno deslocamento do observador')
    elif name=='moon_scale':
        earth(d,60,152,23,t);moon(d,404,80,17)
        for x in [112,216]:d.line((x,210,404,80),fill=TEAL,width=2);circle(d,x,210,5,CORAL)
        label(d,(215,85),'MUITO LONGE',22,GOLD,'mm');foot(d,'Linhas e distâncias ampliadas • sem escala')
    elif name=='tiny_angle':
        observers(d);moon(d,234,71,21)
        for x in [125,335]:d.line((x,214,234,71),fill=TEAL,width=2)
        card(d,235,132,'MUDANÇA MINÚSCULA',GOLD,196);foot(d,'O ângulo do desenho foi ampliado para explicar')
    elif name in ('nearby_moon','close_moon_pass'):
        road(d,218);tree(d,270,191,.9);moon(d,272,92,18)
        x=85+(t*44)%285
        car(d,x,220,t,size=.8);arrow(d,(x,191),(272,92))
        label(d,(118,66),'LUA DE BRINQUEDO',11,GOLD,'mm');foot(d,'Experimento imaginário • objeto perto da estrada')
    elif name=='far_moon_return':
        window(d,t,True);foot(d,'Com a Lua verdadeira, a direção mal muda')
    elif name=='two_routes':
        moon(d,245,64,22)
        d.line((60,224,218,224,270,159,393,159),fill='#32576c',width=17)
        d.line((60,177,165,177,211,132,394,132),fill='#32576c',width=17)
        car(d,120+(t*24)%220,214,t,CORAL,.55);car(d,141+(t*17)%185,133,-t,TEAL,.55)
        foot(d,'Trajetos diferentes • observadores diferentes')
    elif name=='two_windows':
        for x in [25,248]:
            rect(d,(x,61,x+193,208),'#26495c');moon(d,x+138,102,19)
            for k in range(3):tree(d,x+(k*73-t*33)%193,201,.38)
            rect(d,(x,205,x+193,220),'#547481')
        label(d,(115,39),'JANELA A',13,CORAL,'mm');label(d,(343,39),'JANELA B',13,TEAL,'mm');foot(d,'Para cada passageiro, a Lua parece conservar a direção')
    elif name=='shared_moon':
        moon(d,238,83,40)
        for x in [88,386]:car(d,x,207,t,TEAL if x==386 else CORAL,.7);arrow(d,(x,174),(238,125))
        foot(d,'Um objeto distante • várias observações')
    elif name=='mountain_layers':
        mountains(d,161,t);road(d,219)
        for k in range(6):tree(d,(k*98-t*44)%640-85,211,.68)
        label(d,(233,58),'A SERRA PARECE ACOMPANHAR',16,GOLD,'mm');foot(d,'A distância também muda a leitura da paisagem')
    elif name=='cloud_reference':
        for k in range(4):
            x=30+(k*107+t*10)%415;y=75+k%2*31
            for dx,dy,rr in [(-17,5,13),(0,-4,18),(20,5,13)]:circle(d,x+dx,y+dy,rr,'#7d96a6')
        arrow(d,(160,145),(283,145),CORAL);label(d,(223,165),'MOVIMENTO COM O VENTO',11,CORAL,'mm')
        car(d,235+math.sin(t)*70,217,t,size=.7);foot(d,'Distância e movimento próprio são pistas diferentes')
    elif name=='earth_rotation':
        earth(d,212,145,70,t)
        a=t*.33;circle(d,212+64*math.cos(a),145+64*math.sin(a),5,CORAL)
        d.arc((118,51,306,239),20,310,fill=GOLD,width=3);label(d,(357,134),'ROTAÇÃO',15,GOLD,'mm')
        foot(d,'A Terra gira • o céu muda ao longo das horas')
    elif name=='moon_orbit':
        earth(d,205,139,39,t);d.ellipse((87,21,323,257),outline='#45718b',width=2)
        a=t*.18;moon(d,205+118*math.cos(a),139+118*math.sin(a),17)
        label(d,(362,128),'ÓRBITA',16,GOLD,'mm');foot(d,'O movimento orbital existe • esquema sem escala')
    elif name=='night_timelapse':
        mountains(d,216,0);moon(d,77+((t*20)%315),160-82*math.sin((t*.13)%math.pi),23)
        label(d,(235,44),'CÉU OBSERVADO DURANTE HORAS',14,GOLD,'mm');foot(d,'Passagem do tempo acelerada • ilustração')
    elif name=='hours_clock':
        for k in range(3):
            x=105+k*130
            d.ellipse((x-45,93,x+45,183),outline=TEAL,width=3)
            a=(t*.5+k*1.8);d.line((x,138,x+32*math.sin(a),138-32*math.cos(a)),fill=GOLD,width=3)
            label(d,(x,207),['INÍCIO','DEPOIS','MAIS TARDE'][k],10,WHITE,'mm')
        foot(d,'O mesmo lugar • momentos diferentes')
    elif name=='motion_timescales':
        card(d,128,114,'SEGUNDOS',TEAL,169);card(d,342,114,'HORAS',GOLD,169)
        car(d,128,182,t,size=.75);moon(d,342,167,24)
        foot(d,'Viagem curta e passagem de uma noite não são o mesmo teste')
    elif name in ('horizon_moon','high_moon'):
        mountains(d,217,0);moon(d,237,182 if name=='horizon_moon' else 83,31)
        for k in range(5):house(d,36+k*93,232,.52)
        label(d,(235,38),'A IMPRESSÃO DE TAMANHO',14,GOLD,'mm');foot(d,'Ilusão da Lua • outra pergunta sobre percepção')
    elif name=='camera_same_zoom':
        camera(d,118,162);moon(d,337,104,29);arrow(d,(154,149),(290,117))
        card(d,267,190,'MESMO ZOOM',GOLD,152);foot(d,'Comparar a largura em duas fotos da mesma noite')
    elif name in ('photo_comparison','equal_diameters'):
        for x,y in [(30,68),(250,68)]:
            rect(d,(x,y,x+193,y+134),'#18354c');moon(d,x+96,y+(94 if x==30 else 47),28)
            if x==30:
                for k in range(4):house(d,x+24+k*45,y+129,.25)
            label(d,(x+97,221),'HORIZONTE' if x==30 else 'MAIS ALTA',11,WHITE,'mm')
        if name=='equal_diameters':
            for x,y in [(126,162),(346,115)]:d.line((x-28,y,x+28,y),fill=CORAL,width=2);label(d,(x,y-36),'MESMA LARGURA',10,CORAL,'mm')
        foot(d,'Modelo ilustrativo • largura praticamente igual')
    elif name=='brain_context':
        for k in range(7):
            x=181+(k%4)*29;y=80+(k//4)*38;circle(d,x,y,23,'#658b9c',TEAL)
        moon(d,355,115,24);arrow(d,(320,115),(276,115),GOLD)
        label(d,(223,185),'PERCEPÇÃO + CONTEXTO',17,GOLD,'mm');foot(d,'A explicação completa da ilusão ainda é discutida')
    elif name=='illusion_questions':
        moon(d,219,115,48)
        for k in range(3):label(d,(116+k*116,192),'?',32,GOLD,'mm')
        foot(d,'Reconhecer uma pergunta aberta faz parte da ciência')
    elif name=='separate_mysteries':
        card(d,125,98,'DIREÇÃO',TEAL,170);card(d,347,98,'TAMANHO',GOLD,170)
        arrow(d,(86,174),(164,155));moon(d,347,170,29)
        foot(d,'Parecer acompanhar e parecer maior são efeitos diferentes')
    elif name=='parallax_bridge':
        pencil(d,104,139,.65);arrow(d,(143,139),(239,139));orbital(d,t,True)
        foot(d,'A mesma ideia • da sala para a astronomia')
    elif name=='stars_background':
        for x,y in [(93,74),(157,166),(262,97),(365,176)]:
            rect(d,(x-7,y,x+7,y+2),WHITE);rect(d,(x,y-7,x+2,y+7),WHITE)
        x=235+math.sin(t*.75)*18
        circle(d,x,143,8,GOLD);label(d,(230,219),'ESTRELA EM PRIMEIRO PLANO',12,GOLD,'mm')
        foot(d,'Deslocamento aparente ampliado contra o fundo distante')
    elif name in ('earth_orbit','stellar_sightlines'):orbital(d,t,True)
    elif name=='star_shift':
        for x in range(75,420,70):circle(d,x,95,2,WHITE);circle(d,x,181,2,WHITE)
        circle(d,193,95,7,GOLD);circle(d,256,181,7,GOLD)
        label(d,(59,94),'A',15,TEAL,'mm');label(d,(59,181),'B',15,CORAL,'mm');arrow(d,(193,123),(256,154),GOLD)
        foot(d,'Vistos de A e B • deslocamento estelar exagerado')
    elif name=='cosmic_ruler':
        rect(d,(59,118,415,173),'#183e55')
        for x in range(70,410,15):rect(d,(x,121,x+1,133+(x%3)*4),TEAL)
        label(d,(237,153),'DISTÂNCIA',21,GOLD,'mm');moon(d,390,68,15)
        foot(d,'A geometria permite medir distâncias no espaço')
    elif name in ('walking_test','near_far_frames','notice_layers'):
        mountains(d,170,t);tree(d,160-(t*15)%120,218,.9);house(d,363-(t*2)%40,179,.47)
        if name=='near_far_frames':card(d,129,68,'PERTO',CORAL,110);card(d,350,68,'LONGE',TEAL,110)
        if name=='notice_layers':label(d,(232,44),'OBSERVE A PAISAGEM',19,GOLD,'mm')
        foot(d,'Mudar de posição revela pistas de distância')
    elif name=='answer_card':
        moon(d,236,83,31);label(d,(236,154),'MUITO DISTANTE',24,GOLD,'mm')
        label(d,(236,192),'A DIREÇÃO QUASE NÃO MUDA',15,TEAL,'mm')
        foot(d,'Durante um pequeno trajeto na Terra')
    elif name=='three_clues':
        for x,text in [(84,'OBSERVADOR'),(238,'TRAJETO'),(388,'DISTÂNCIA')]:card(d,x,108,text,TEAL,139)
        circle(d,84,180,13,CORAL);arrow(d,(180,180),(286,180),GOLD);moon(d,389,180,18)
        foot(d,'Três pistas para interpretar o que vemos')
    elif name=='journey_out':
        earth(d,97,159,29,t);moon(d,277,93,23)
        for k in range(4):arrow(d,(140+k*25,139-k*6),(153+k*25,134-k*6),TEAL,2)
        label(d,(233,212),'DA JANELA AO UNIVERSO',18,GOLD,'mm');foot(d,'Uma pergunta simples pode levar muito longe')
    elif name=='pico_night':
        window(d,t);moon(d,344,87,32);foot(d,'Qual foi sua primeira pergunta olhando para o céu?')
    elif name=='question_board':
        for x,y,txt in [(128,83,'O CÉU'),(346,83,'A TERRA'),(237,178,'SUA PRÓXIMA PERGUNTA')]:
            card(d,x,y,txt,GOLD,180 if y==178 else 143)
        foot(d,'Conte nos comentários • explore com o Pico')
    elif name=='end':
        for k in range(170):
            a=k*math.pi*2/170;x=240+94*math.cos(a)/(1+math.sin(a)**2);y=104+94*math.sin(a)*math.cos(a)/(1+math.sin(a)**2)
            rect(d,(x-2,y-2,x+2,y+2),GOLD if k%7==0 else TEAL)
        label(d,(240,187),'QUASE INFINITO',28,WHITE,'mm');label(d,(240,222),'Cada pergunta abre outra viagem.',12,GOLD,'mm')
    else:raise ValueError('Unknown Moon scene: '+name)
    stage=Image.new('RGB',(W,H),NAVY)
    stage.paste(im.resize((768,432),Image.Resampling.NEAREST),(96,16))
    return stage

def overlay(item,scene,t,global_time,cue,source='',pixel=False):
    layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer)
    rect(d,(0,0,W,42),(5,18,29,230));rect(d,(0,443,W,H),(5,18,29,235))
    d.rectangle((12,12,W-13,H-13),outline=(110,240,211,240),width=2)
    for x,y,sx,sy in [(12,12,1,1),(948,12,-1,1),(12,528,1,-1),(948,528,-1,-1)]:
        d.line((x+sx*31,y,x,y,x,y+sy*23),fill=GOLD,width=4)
    label(d,(32,12),'QUASE INFINITO',16,WHITE);label(d,(927,14),'04 / LUA',12,TEAL,'ra')
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
