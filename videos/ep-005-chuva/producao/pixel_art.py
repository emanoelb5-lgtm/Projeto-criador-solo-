"""Detailed illustrated pixel environments plus accurate, animated scientific schematics."""
import hashlib,math,random
from functools import lru_cache
from pathlib import Path
from PIL import Image,ImageDraw
from base_art import W,H,NAVY,TEAL,GOLD,CORAL,WHITE,font,rect,label,arrow,pico,pose,paste_pico,wrap

ROOT=Path(__file__).resolve().parent
ASSET_HASH=hashlib.sha256(b''.join(p.read_bytes() for p in sorted((ROOT/'assets').glob('*.png')))).hexdigest()
SCENIC={
 'garden_before':'garden','garden_scent':'garden','garden_plants':'garden',
 'garden_wind':'garden','rain_elsewhere':'garden','porch_memory':'garden',
 'garden_first':'garden','aroma_memory':'garden',
 'forest_wind':'forest','forest_rain':'forest','forest_wet':'forest',
 'forest_glow':'forest','habitat':'forest',
 'soil_world':'soil','soil_network':'soil','story_network':'soil',
 'end_wave':'forest','end_question':'garden','end_card':'forest'
}
KINDS={
 'opening_map':'chain','pure_water':'water','compare_surfaces':'surfaces',
 'old_lab':'history','petrichor_word':'word','plant_oils':'plant',
 'soil_storage':'storage','bacteria_colony':'bacteria','molecule_hint':'geosmin',
 'geosmin':'geosmin','concentration':'concentration','clue_chain':'chain',
 'soil_zoom':'storage','drop_fall':'fall','camera_lab':'camera','drop_contact':'contact',
 'bubble_birth':'birth','bubble_rise':'rise','bubble_burst':'burst',
 'aerosols':'aerosols','wind_transfer':'wind','compare_rain':'raincompare',
 'surface_porosity':'porosity','soil_absorb':'absorb','surface_wet':'wet',
 'springtail':'springtail','scent_trail':'trail','spores_ride':'spores',
 'micro_lab':'evidence','y_tube':'tube','field_layers':'layers','rain_recap':'chain',
 'street_vs_forest':'surfaces','rain_cities':'surfaces','observation':'observe',
 'three_keys':'keys','recap_particles':'aerosols'
}
@lru_cache(None)
def scenery(kind):
    file={'garden':'Garden','forest':'Forest','soil':'Soil'}[kind]+'_Pixel_16x9.png'
    with Image.open(ROOT/'assets'/file) as im:return im.convert('RGBA').resize((1040,585),Image.Resampling.NEAREST)
def background(kind,t):
    src=scenery(kind)
    x=round(40+30*math.sin(t*.16));y=round(23+17*math.sin(t*.11+.4))
    return src.crop((x,y,x+W,y+H))
def circle(d,x,y,r,fill,outline=None,width=2):
    d.ellipse((round(x-r),round(y-r),round(x+r),round(y+r)),fill=fill,outline=outline,width=width)
def card(d,x,y,title,lines=(),width=188,color=TEAL):
    d.rounded_rectangle((x,y,x+width,y+92),radius=7,fill='#123143',outline=color,width=2)
    rect(d,(x+8,y+8,x+11,y+28),color)
    label(d,(x+20,y+21),title,17,color,'lm')
    for k,text in enumerate(lines):label(d,(x+12,y+48+k*21),text,13,WHITE,'lm')
def panel(im,title,subtitle=None):
    layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer)
    d.rounded_rectangle((36,68,722,419),radius=10,fill=(5,22,33,236),outline=(94,181,173,180),width=2)
    rect(d,(50,80,54,108),GOLD);label(d,(69,94),title,21,GOLD,'lm')
    if subtitle:label(d,(69,121),subtitle,13,TEAL,'lm')
    im.alpha_composite(layer)
    return ImageDraw.Draw(im)
def soil(d,y=315,x1=65,x2=693,deep=80,wet=False):
    d.polygon([(x1,y),(x1+90,y-6),(x1+172,y+2),(x1+268,y-3),(x1+390,y+2),(x2,y),(x2,y+deep),(x1,y+deep)],fill='#795236' if not wet else '#4d3a30')
    rng=random.Random(431)
    colors=['#b98653','#976842','#433633','#d5ad76']
    for k in range(150):
        x=rng.randrange(x1+2,x2-3);yy=rng.randrange(y+4,y+deep-3)
        rect(d,(x,yy,x+2+k%3,yy+1+k%2),colors[k%4])
    for x in range(x1+25,x2,80):
        d.line((x,y+3,x+8,y+20,x-6,y+37),fill='#d3aa73',width=2)
        circle(d,x+16,y+27,6,'#293031')
    if wet:rect(d,(x1,y-3,x2,y+2),'#539da5')
def drop(d,x,y,r=30):
    d.polygon([(x,y-r*1.4),(x-r*.78,y),(x+r*.78,y)],fill='#368bba')
    circle(d,x,y,r*.8,'#368bba','#9be8ee',2)
    d.arc((round(x-r*.55),round(y-r*.6),round(x+r*.55),round(y+r*.5)),170,263,fill='#d4f7f2',width=3)
def rain(im,t,density=64,wind=0):
    layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer)
    for k in range(density):
        x=(k*139+int(t*wind*20))%1040-40;y=(k*61+t*(105+k%4*22))%485-20
        length=9+k%11
        d.line((round(x),round(y),round(x-3-wind),round(y+length)),fill=(176,220,239,90+k%3*30),width=1+k%2)
    for k in range(10):
        age=(t*.8+k*.17)%1;xx=55+(k*89)%850;yy=343+(k*23)%73
        if age<.75:d.ellipse((xx-age*15,yy-age*3,xx+age*15,yy+age*3),outline=(179,220,220,round(120*(1-age))),width=1)
    im.alpha_composite(layer)
def atmosphere(im,kind,t,wet=False):
    layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer)
    if wet:rect(d,(0,45,W,442),(7,27,46,26))
    if kind!='soil':
        for k in range(16):
            x=15+(k*131+t*(6+k%3))%950;y=123+(k*49)%180
            d.rectangle((x,y,x+60+k%3*28,y+2),fill=(143,209,207,16))
        # Foreground fern and leafy silhouettes provide a separate, swaying depth layer.
        for bx in [6,944]:
            sway=5*math.sin(t*1.3+(bx%7));base=(bx,424);tip=(bx+sway+(40 if bx<100 else -40),350)
            d.line((base,tip),fill=(30,100,92,170),width=3)
            for k in range(7):
                yy=414-k*9;xx=bx+(tip[0]-bx)*(424-yy)/74
                span=(30-k*2)*(1 if bx<100 else -1)
                d.polygon([(xx,yy),(xx+span,yy-9),(xx+span*.74,yy+1),(xx,yy+3)],fill=(31,109+k*3,93,180))
    else:
        for k in range(20):
            x=(90+k*41+t*(3+k%4))%740;y=108+(k*31)%286+math.sin(t+k)*2
            circle(d,x,y,1.4,(226,171,94,80))
    im.alpha_composite(layer)
def motes(d,t,x1=70,y1=265,x2=670,y2=166,count=20,color=TEAL):
    for k in range(count):
        q=(t*.14+k/count)%1
        x=x1+(x2-x1)*q;y=y1+(y2-y1)*q+math.sin(q*9+k)*10
        circle(d,x,y,2+k%2,color)
def bacteria(d,t,x=240,y=267):
    for j in range(7):
        xx=x+(j-3)*25;yy=y+math.sin(j*2.1+t*.4)*10
        points=[(xx-21,yy+12),(xx-11,yy-4),(xx+4,yy+2),(xx+16,yy-17)]
        d.line(points,fill='#71cfb3',width=5)
        d.line((xx-11,yy-4,xx-17,yy-15),fill='#a9e7ba',width=3)
        d.line((xx+4,yy+2,xx+21,yy+10),fill='#4b9d87',width=3)
        for px,py in points:circle(d,px,py,2,'#d6e9b3')
def springtail(d,x,y,t=0,size=1,spores=False):
    # Symbolic dorsal view: six legs, two antennae, segmented body.
    ink='#102633'
    for side in [-1,1]:
        for k in range(3):
            xx=x+(-20+k*23)*size;yy=y+side*14*size
            a=(xx+side*6*size,yy+side*(17+math.sin(t*5+k)*3)*size)
            b=(xx-9*size,a[1]+side*10*size)
            d.line([(xx,yy),a,b],fill=ink,width=max(2,round(5*size)))
            d.line([(xx,yy),a,b],fill='#f1cd8b',width=max(1,round(2*size)))
    for k in range(4):
        circle(d,x+(k-1.5)*18*size,y,(15 if k<3 else 13)*size,['#bd8750','#d3a061','#e4b97b','#f4d393'][k],ink,3)
    for side in [-1,1]:d.line([(x+41*size,y+side*7*size),(x+58*size,y+side*22*size),(x+66*size,y+side*26*size)],fill='#f2d397',width=max(1,round(2*size)))
    circle(d,x+38*size,y-6*size,2*size,ink)
    if spores:
        for k in range(10):circle(d,x+((k*17)%70-35)*size,y+((k*11)%24-12)*size,2.4*size,TEAL)
def droplet_scene(d,t,kind):
    soil(d,y=339,deep=59)
    cx=358
    if kind=='fall':
        phase=(t*.55)%1;drop(d,cx,174+phase*106,31)
        arrow(d,(438,193),(438,294),GOLD)
        label(d,(cx,377),'Água encontra uma superfície porosa',16,WHITE,'mm')
        return
    if kind=='contact':
        phase=min(1,(t%5)/1.2)
        if phase<.5:drop(d,cx,174+phase*265,28)
        else:d.ellipse((cx-112,279,cx+112,338),fill='#317ba0',outline='#9cdae0',width=3)
    else:
        d.ellipse((cx-153,239,cx+153,342),fill='#286b90',outline='#9cdae0',width=3)
        rect(d,(cx-151,289,cx+151,339),'#286b90')
    if kind in ['birth','rise','burst'] or (kind=='contact' and phase>=.5):
        for k in range(7):
            xx=cx-110+k*36
            if kind=='birth':yy=320-5*math.sin(t+k)
            elif kind=='rise':yy=325-((t*.28+k*.09)%1)*70
            elif kind=='burst':yy=265+5*math.sin(t+k)
            else:yy=322-10*math.sin(t*.8+k)
            circle(d,xx,yy,5+k%3,'#326889','#c2f2e8',2)
        if kind=='burst':
            for k in range(24):
                q=(t*.55+k/24)%1
                xx=cx+(k%2*2-1)*q*(45+k%8*11);yy=252-q*100+q*q*25
                circle(d,xx,yy,1+k%3,TEAL)
    label(d,(cx,377),{'contact':'A gota se espalha no contato','birth':'Pequenas bolhas ficam aprisionadas','rise':'As bolhas sobem dentro da água','burst':'Ao romper, lançam gotículas menores'}[kind],16,WHITE,'mm')
def scheme(im,scene,t):
    kind=KINDS[scene]
    titles={
      'chain':'A viagem do aroma','water':'A água encontra o ambiente',
      'surfaces':'Cada lugar oferece ingredientes','history':'Uma pergunta antiga, um novo nome',
      'word':'PETRICOR','plant':'Compostos aromáticos das plantas','storage':'O chão guarda substâncias',
      'bacteria':'Uma fábrica viva no solo','geosmin':'GEOSMINA','concentration':'Pequenas concentrações',
      'fall':'Aproxime a câmera','camera':'Uma câmera mais rápida que o olhar',
      'contact':'1 · Contato','birth':'2 · Formação de bolhas','rise':'3 · As bolhas sobem','burst':'4 · Gotículas no ar',
      'aerosols':'Do solo para o ar','wind':'O vento continua a viagem',
      'raincompare':'Mais água não é sempre mais aerossol','porosity':'As propriedades da superfície importam',
      'absorb':'A água pode entrar depressa','wet':'Um chão seco ou já molhado?',
      'springtail':'Um pequeno habitante do solo','trail':'Moléculas podem funcionar como sinais',
      'spores':'Alimento e transporte','evidence':'Uma pista testada em experimentos',
      'tube':'A atração por diferentes cheiros','layers':'Duas histórias se encontram',
      'observe':'Observe de um lugar protegido','keys':'Três etapas do mistério'
    }
    d=panel(im,titles[kind],'Ilustração ampliada • movimentos e tamanhos sem escala')
    if kind in ['fall','contact','birth','rise','burst']:droplet_scene(d,t,kind)
    elif kind in ['chain','keys','layers']:
        if kind=='keys':names=['PRODUÇÃO','LIBERAÇÃO','TRANSPORTE'];lines=[['Solo e seres vivos'],['Umidade e gotas'],['Movimento do ar']]
        elif kind=='layers':names=['BIOLOGIA','FÍSICA','PERCEPÇÃO'];lines=[['Organismos e sinais'],['Gotas e superfícies'],['Uma pista sensorial']]
        else:names=['CHÃO','GOTA','AR'];lines=[['Guarda ingredientes'],['Ajuda a liberá-los'],['Continua a viagem']]
        for j,name in enumerate(names):card(d,65+j*220,203,name,lines[j],width=195,color=[GOLD,TEAL,CORAL][j])
        for j in [0,1]:arrow(d,(263+j*220,247),(283+j*220,247),TEAL,3)
        motes(d,t,88,351,661,327,18)
        label(d,(376,376),'Um processo que passa pelo ambiente inteiro',15,WHITE,'mm')
    elif kind=='word':
        label(d,(370,214),'PETRA  +  ICHOR',29,WHITE,'mm')
        label(d,(370,258),'pedra  +  fluido dos deuses',19,TEAL,'mm')
        label(d,(370,326),'Bear e Thomas · 1964',20,GOLD,'mm')
        label(d,(370,365),'Um nome para um aroma familiar',16,WHITE,'mm')
    elif kind=='history':
        for x,name in [(149,'MATERIAL SECO'),(401,'UMIDADE')]:
            card(d,x-75,203,name,['Investigação do aroma'],180,GOLD if x==149 else TEAL)
        drop(d,500,319,24);soil(d,335,70,656,59)
        label(d,(365,167),'Isabel Bear + Richard Thomas',20,WHITE,'mm')
        label(d,(365,377),'Mistura oleosa liberada por umidade',16,WHITE,'mm')
    elif kind in ['storage','porosity','absorb','wet']:
        soil(d,273,70,690,121,kind=='wet')
        for k in range(7):
            x=104+k*86
            if kind in ['storage','porosity']:
                circle(d,x,320,13,'#172b33','#bd8b53',3)
                circle(d,x+21,350,7,TEAL)
            elif kind=='absorb':
                phase=(t*.4+k*.13)%1;circle(d,x,204+phase*155,3,TEAL)
            else:drop(d,x,204+(t*45+k*37)%58,8)
        label(d,(366,177),{'storage':'Grãos, poros e frestas','porosity':'O encontro depende do solo','absorb':'Absorção rápida muda o impacto','wet':'A película de água muda o encontro'}[kind],20,WHITE,'mm')
    elif kind=='plant':
        soil(d,340,69,687,50)
        d.line((257,339,257,192),fill='#73c79b',width=5)
        for k in range(6):
            yy=216+k*17;side=-1 if k%2 else 1
            d.polygon([(257,yy),(257+side*68,yy-26),(257+side*46,yy+2)],fill=['#4b997a','#79c299'][k%2])
            d.line((257,yy,257+side*53,yy-16),fill='#b6d4a0',width=2)
        motes(d,t,275,237,590,321,14,GOLD)
        label(d,(516,214),'COMPOSTOS',19,GOLD,'mm');label(d,(516,247),'AROMÁTICOS',19,GOLD,'mm')
        label(d,(376,374),'Podem se acumular na terra e nas pedras',15,WHITE,'mm')
    elif kind=='water':
        drop(d,184,249,54)
        arrow(d,(264,247),(347,247),GOLD)
        card(d,380,199,'O ENCONTRO',['Água + ambiente','Ingredientes diferentes'],258,TEAL)
        label(d,(368,359),'O aroma terroso envolve materiais do lugar',16,WHITE,'mm')
    elif kind=='surfaces':
        for x,green in [(70,True),(399,False)]:
            if green:soil(d,289,x,x+286,81)
            else:
                rect(d,(x,289,x+286,370),'#5d6e77')
                for j in range(5):d.line((x+j*62,290,x+j*62,370),fill='#273c4d',width=3)
                d.line((x,329,x+285,329),fill='#273c4d',width=3)
            label(d,(x+143,187),'VEGETAÇÃO' if green else 'PISO E PAREDES',17,TEAL if green else GOLD,'mm')
            for k in range(4):drop(d,x+42+k*66,231+math.sin(t+k)*12,9)
        label(d,(375,395),'Uma mistura depende do ambiente',15,WHITE,'mm')
    elif kind in ['bacteria','geosmin','concentration']:
        if kind=='bacteria':
            bacteria(d,t,244,254)
            card(d,432,193,'STREPTOMYCES',['Bactérias do solo','Produzem geosmina'],241,TEAL)
        else:
            for k in range(24 if kind=='concentration' else 13):
                x=128+(k*101)%513;y=188+(k*67)%113+math.sin(t+k)*8
                circle(d,x,y,2 if kind=='concentration' else 5,TEAL if k%3 else GOLD)
            label(d,(373,335),'UMA SUBSTÂNCIA · AROMA TERROSO',18,GOLD,'mm')
        label(d,(376,380),'Partículas são símbolos; não é uma estrutura molecular',13,WHITE,'mm')
    elif kind in ['aerosols','wind']:
        soil(d,334,69,691,57)
        motes(d,t,235,324,663,158,29)
        if kind=='wind':
            for k in range(3):arrow(d,(80,205+k*38),(555+math.sin(t)*20,192+k*38),GOLD,2)
        drop(d,235,301,18)
        label(d,(493,296),'GOTÍCULAS',20,WHITE,'mm');label(d,(493,327),'SUSPENSAS NO AR',18,TEAL,'mm')
        label(d,(374,380),'Aerossóis podem carregar materiais da superfície',14,WHITE,'mm')
    elif kind in ['camera','evidence']:
        rect(d,(106,205,283,304),'#426779');rect(d,(119,180,213,209),'#365468')
        circle(d,219,252,39,'#102736',TEAL,5);circle(d,219,252,20,'#2f7894',WHITE,2)
        d.line((188,305,145,367),fill=GOLD,width=4);d.line((188,305,235,367),fill=GOLD,width=4)
        card(d,357,181,'OBSERVAR E TESTAR',['Comparar condições','Registrar movimentos','Investigar mecanismos'],301,TEAL)
        label(d,(379,382),'Uma explicação pode ser colocada à prova',15,WHITE,'mm')
    elif kind=='raincompare':
        for x,title,fast in [(70,'LEVE / MODERADA',False),(395,'IMPACTO RÁPIDO',True)]:
            label(d,(x+141,175),title,17,TEAL if not fast else GOLD,'mm');soil(d,320,x,x+284,59)
            for k in range(7):drop(d,x+24+k*37,211+(t*(160 if fast else 55)+k*26)%66,7)
            for k in range(15 if not fast else 4):
                q=(t*.5+k*.071)%1;circle(d,x+23+(k*31)%231,311-q*63,2,TEAL)
        label(d,(377,399),'Comparação qualitativa nas condições do estudo',13,WHITE,'mm')
    elif kind in ['springtail','trail','spores']:
        soil(d,361,70,690,29)
        x=280+math.sin(t*.5)*28 if kind!='spores' else 185+(t*30)%342
        springtail(d,x,276,t,1.4,kind=='spores')
        if kind=='trail':motes(d,t,525,233,x+56,271,18,TEAL)
        if kind=='spores':
            for k in range(11):circle(d,140+k*38,341+math.sin(k)*7,3,TEAL)
        card(d,473,197,'COLÊMBOLO',['Artrópode do solo','Alimento e transporte'],207,GOLD)
        label(d,(376,393),'Ilustração de um colêmbolo e sinais químicos',13,WHITE,'mm')
    elif kind=='tube':
        junction=(292,261)
        for end in [(136,350),(538,183),(538,335)]:
            d.line((junction,end),fill='#4c7384',width=37);d.line((junction,end),fill='#193344',width=29)
        q=(t*.14)%1;x=136+(538-136)*q;y=350+(183-350)*q
        springtail(d,x,y,t,.5)
        label(d,(571,164),'COMPOSTOS',14,TEAL,'mm');label(d,(571,186),'DO SOLO',14,TEAL,'mm')
        label(d,(582,347),'COMPARAÇÃO',13,GOLD,'mm')
        label(d,(377,395),'Esquema de escolha entre diferentes cheiros',13,WHITE,'mm')
    elif kind=='observe':
        for j,(name,lines) in enumerate([('QUANDO?',['Antes ou depois?']),('VENTO?',['Mudou a direção?']),('AMBIENTE?',['Vegetação ou piso?'])]):
            card(d,64+j*220,208,name,lines,195,[GOLD,TEAL,CORAL][j])
        label(d,(376,362),'Anote, compare e faça novas perguntas',17,WHITE,'mm')
        label(d,(376,392),'Uma observação sozinha não prova a causa',13,TEAL,'mm')
    else:raise RuntimeError('Undrawn science kind '+kind)
def pixel_scene(scene,t):
    if scene not in SCENIC and scene not in KINDS:raise RuntimeError('Unknown scene '+scene)
    kind=SCENIC.get(scene,'soil' if KINDS.get(scene) in ['storage','bacteria','geosmin','concentration','springtail','trail','spores','porosity','absorb','wet'] else 'forest')
    im=background(kind,t)
    wet=scene in ['garden_scent','garden_first','forest_rain','forest_wet','rain_elsewhere']
    atmosphere(im,kind,t,wet)
    if wet:rain(im,t,70 if scene=='forest_rain' else 43,1.3)
    if scene in KINDS:scheme(im,scene,t)
    elif scene in ['garden_scent','garden_wind','forest_wind','story_network','soil_network']:
        d=ImageDraw.Draw(im);motes(d,t,150,338,650,222,20,TEAL)
    elif scene=='rain_elsewhere':
        layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer)
        d.rounded_rectangle((65,91,662,162),radius=8,fill=(4,23,37,213),outline=TEAL,width=2)
        label(d,(364,127),'O ar pode vir de onde já choveu',20,WHITE,'mm')
        for k in range(3):arrow(d,(90,206+k*35),(635,195+k*35),TEAL,2)
        im.alpha_composite(layer)
    elif scene in ['forest_glow','end_wave','end_question','end_card']:
        layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer)
        if scene.startswith('end_'):
            d.rounded_rectangle((55,112,654,339),radius=8,fill=(4,22,35,220),outline=TEAL,width=2)
            label(d,(353,164),'QUASE INFINITO',36,GOLD,'mm')
            lines=['Qual lugar tem o melhor','cheiro de chuva para você?'] if scene=='end_question' else ['Cada pergunta','abre outra viagem.']
            for k,line in enumerate(lines):label(d,(353,227+k*36),line,24,WHITE,'mm')
            label(d,(354,310),'COMENTE  ·  ACOMPANHE A PRÓXIMA PISTA',12,TEAL,'mm')
        else:
            for k in range(23):
                x=(50+k*49+t*7)%900;y=129+(k*43)%275+math.sin(t+k)*5
                circle(d,x,y,1.8,(242,209,121,140))
        im.alpha_composite(layer)
    return im.convert('RGB')
def overlay(item,scene,local,global_time,cue,source,pixel):
    im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im)
    # Persistent frame, distinct caption band: the only subtitle-rendering layer.
    rect(d,(0,0,959,49),(7,22,33,248));rect(d,(0,446,959,539),(7,22,33,255))
    d.rectangle((9,9,950,531),outline=TEAL,width=2)
    rect(d,(9,49,951,51),GOLD);rect(d,(9,445,951,447),GOLD)
    label(d,(27,27),'QUASE INFINITO',16,GOLD,'lm')
    label(d,(219,27),item['title'],16,WHITE,'lm')
    label(d,(930,27),'05',17,TEAL,'rm')
    progress=min(1,global_time/504);rect(d,(25,526,935,528),'#234454')
    rect(d,(25,526,25+910*progress,528),TEAL)
    # Keep credits readable without painting any second copy of the subtitles.
    rect(d,(18,425,942,445),(7,22,33,225))
    credit='Pixel art e animação original • cenários ilustrativos' if pixel else source
    label(d,(30,435),credit[:92],10,'#c2d9d3','lm')
    act=item['action'];height=208 if pixel else 154
    if scene in ['bubble_birth','bubble_rise','bubble_burst','drop_contact','camera_lab','micro_lab','y_tube']:act='point'
    if scene in ['geosmin','concentration','springtail','compare_rain']:act='surprise'
    if scene in ['plant_oils','soil_storage','bacteria_colony','spores_ride']:act='inspect'
    if scene in ['end_wave','end_card']:act='wave';height=253
    if scene=='end_question':act='question';height=248
    spr=pico(act,global_time,scene,height)
    x=936-spr.width;y=420-spr.height
    if act=='flying':
        x-=round(30+20*math.sin(local*.6));y-=round(22+17*math.sin(local*.8))
        for k in range(7):circle(d,x-5-k*9,y+spr.height*.6+math.sin(local*5+k)*3,2,GOLD if k%2 else TEAL)
    im.alpha_composite(spr,(int(x),int(y+math.sin(global_time*2.1)*3)))
    if cue:
        lines=wrap(cue)
        if len(lines)>2:raise RuntimeError('More than two subtitle lines')
        ys=[488] if len(lines)==1 else [474,505]
        for line,yc in zip(lines,ys):
            d.text((480,yc),line,font=font(23,True),fill=WHITE,anchor='mm',stroke_width=1,stroke_fill=NAVY)
    return im

