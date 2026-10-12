"""Episode-specific buoyancy illustrations, animated models and the approved Pico v2."""
import hashlib,math,random
from functools import lru_cache
from pathlib import Path
from PIL import Image,ImageDraw
from base_art import W,H,NAVY,TEAL,GOLD,CORAL,WHITE,font,rect,label,arrow,pico,wrap
ROOT=Path(__file__).resolve().parent
ASSET_HASH=hashlib.sha256(b''.join(p.read_bytes() for p in sorted((ROOT/'assets').glob('*.png')))).hexdigest()
BLUE='#6aaafa';STEEL='#618598';WOOD='#bd925f'
TITLES={
'hook_contrast':'Um gigante e um prego','harbor_ship':'O que mantém o casco flutuando?',
'hull_reveal':'Um corte pelo casco','density_cubes':'Mesmo volume, massas diferentes','mass_volume':'Densidade = massa / volume',
'hull_air':'Espaços protegidos da água','underwater_hull':'A água pressiona o casco','pressure_zoom':'Mais fundo, maior pressão',
'pressure_cube':'Uma caixa completamente submersa','buoyant_arrows':'A resultante aponta para cima',
'displacement':'O espaço que a água deixou','water_equivalent':'O peso da água deslocada','number_example':'Uma comparação com números',
'ship_balance':'Peso e empuxo em equilíbrio','solid_vs_hollow':'Mesmo material, outra forma','shape_transform':'O volume externo importa',
'clay_ball':'Bola de massa de modelar','clay_boat':'A mesma porção vira uma tigela','clay_compare':'A massa não mudou',
'cargo_loading':'Mais carga, maior volume submerso','freeboard':'Calado e parte fora da água','engine_off':'Um cargueiro também flutua parado',
'flood_start':'A água começa a entrar','flood_progress':'O espaço interno deixa de estar protegido','flood_balance':'A condição de flutuação muda',
 'tilt_boat':'Flutuação e estabilidade','tilt_cargo':'A posição da carga importa',
'salt_compare':'O líquido também participa','egg_compare':'Uma comparação de densidades',
'fresh_salt_boat':'Mesma carga, outro líquido','water_density':'A densidade da água pode variar',
'submarine_overview':'Uma descida controlada','ballast_fill':'Água entrando nos tanques de lastro','sub_neutral':'Flutuação neutra',
'ballast_empty':'Ar comprimido expulsando água','sub_surface':'O modelo volta à superfície','ice_density':'Gelo e água líquida',
'hidden_volume':'A fotografia mostra só parte da história','challenge_boats':'Qual dos dois fica mais fundo?',
'challenge_answer':'O carregado desloca mais água','recap_contrast':'O prego e o navio','recap_three':'Massa, volume e líquido',
'harbor_end':'Olhe para a linha da água','outro':'Cada pergunta abre outra viagem'}

@lru_cache(None)
def scenery(kind):
 with Image.open(ROOT/'assets'/f'{kind}_Pixel_16x9.png') as im:return im.convert('RGBA').resize((1024,576),Image.Resampling.NEAREST)
def background(kind,t):
 src=scenery(kind);x=round(32+17*math.sin(t*.08));y=round(18+9*math.sin(t*.06))
 return src.crop((x,y,x+W,y+H))
def circle(d,x,y,r,c,outline=None,width=2):d.ellipse(tuple(round(a) for a in (x-r,y-r,x+r,y+r)),fill=c,outline=outline,width=width)
def panel(im,title):
 layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer)
 d.rounded_rectangle((38,76,748,488),radius=11,fill=(5,24,38,236),outline=(106,225,218,160),width=2)
 for x in range(60,730,24):
  for y in range(138,458,24):circle(d,x,y,.6,(130,210,210,25))
 rect(d,(55,91,59,119),GOLD);label(d,(73,105),title,19,GOLD,'lm');im.alpha_composite(layer)
 return ImageDraw.Draw(im)
def note(d,text='Modelo ilustrado • sem escala'):
 label(d,(69,468),text,10,'#a2c3cd','lm')
def water(d,t,level=315,left=77,right=713,bottom=440):
 rect(d,(left,level,right,bottom),'#153e57')
 for k in range(19):
  x=left+9+(k*31)%max(1,right-left-40);y=level+15+(k*23)%max(1,bottom-level-24)
  x+=math.sin(t*.5+k)*5;d.line((x,y,x+15,y),fill='#2b5971',width=1)
 points=[(x,level+2*math.sin(x*.037-t*1.1)) for x in range(left,right+1,4)]
 d.line(points,fill=BLUE,width=3)
def nail(d,x,y,t=0,size=65):
 layer=Image.new('RGBA',(90,110));q=ImageDraw.Draw(layer)
 q.polygon([(35,29),(49,29),(48,84),(42,101),(36,84)],fill='#9daebe',outline='#e5f3f8')
 q.rectangle((24,17,60,30),fill='#c8d7dd',outline=WHITE,width=2)
 for yy in range(40,79,7):q.line((36,yy,48,yy),fill='#5c778d',width=2)
 layer=layer.resize((round(size*.82),size),Image.Resampling.NEAREST).rotate(17+3*math.sin(t),resample=Image.Resampling.NEAREST,expand=True)
 return layer,(round(x-layer.width/2),round(y-layer.height/2))
def draw_nail(im,x,y,t=0,size=65):
 sprite,pos=nail(None,x,y,t,size);im.alpha_composite(sprite,pos)
def ship_layer(w=420,cut=False,cargo=2,flood=0,cargo_shift=0):
 im=Image.new('RGBA',(440,240));d=ImageDraw.Draw(im)
 y=111;poly=[(8,y),(427,y),(363,y+111),(78,y+111)]
 d.polygon(poly,fill='#30586b',outline=WHITE,width=2)
 d.polygon([(14,y+8),(417,y+8),(363,y+102),(79,y+102)],fill='#ad694f' if not cut else '#102936',outline=STEEL)
 if cut:
  for x in range(101,379,70):
   d.rectangle((x,y+14,x+54,y+91),fill='#213e50',outline=GOLD,width=1)
   if flood:d.rectangle((x,y+91-round(flood*73),x+54,y+91),fill=BLUE)
  label(d,(239,y+53),'ESPAÇO INTERNO',12,TEAL,'mm')
 else:
  for yy in range(y+15,y+100,15):d.line((48+(yy-y)*.29,yy,414-(yy-y)*.49,yy),fill='#4e7a8b',width=1)
  for xx in range(103,381,36):
   for yy in [y+21,y+69]:circle(d,xx,yy,1,WHITE)
 for k in range(max(0,cargo)):
  x=91+(k%4)*65+cargo_shift;yy=y-30-(k//4)*29;c=[CORAL,GOLD,TEAL,BLUE][k%4]
  d.rectangle((x,yy,x+60,yy+27),fill=c,outline=NAVY,width=2)
  for j in range(x+5,x+58,8):d.line((j,yy+3,j,yy+24),fill='#334e61',width=1)
 d.rectangle((354,64,393,y-1),fill='#dbe9e5',outline=STEEL,width=2)
 for yy in [70,83,96]:
  for xx in range(358,388,9):rect(d,(xx,yy,xx+5,yy+5),NAVY)
 d.line((379,64,379,45),fill=GOLD,width=2)
 return im.resize((w,round(240*w/440)),Image.Resampling.NEAREST)
def ship(im,x=165,y=179,w=480,cut=False,cargo=4,flood=0,tilt=0,cargo_shift=0):
 sprite=ship_layer(w,cut,cargo,flood,cargo_shift)
 if tilt:sprite=sprite.rotate(tilt,resample=Image.Resampling.NEAREST,expand=True)
 im.alpha_composite(sprite,(round(x),round(y)))
 return ImageDraw.Draw(im)
def forces(d,x,y,up=90,down=90):
 arrow(d,(x-75,y+65),(x-75,y+65-up),TEAL,5)
 arrow(d,(x+80,y-72),(x+80,y-72+down),CORAL,5)
 label(d,(x-75,y+86),'EMPUXO',12,TEAL,'mm');label(d,(x+80,y-90),'PESO',12,CORAL,'mm')

def comparison(im,d,t):
 water(d,t,level=317);ship(im,102,156,390,cargo=6)
 draw_nail(im,610,354+24*math.sin(t*.5),t,92);d=ImageDraw.Draw(im)
 label(d,(289,405),'NAVIO',17,TEAL,'mm');label(d,(612,421),'PREGO',17,CORAL,'mm')
 arrow(d,(668,333),(668,389),CORAL,3);note(d,'Comparação ilustrada • tamanhos diferentes de propósito')
def densities(d,t,kind):
 for x,c,title in [(153,WOOD,'MADEIRA'),(449,STEEL,'AÇO')]:
  d.polygon([(x,213),(x+119,213),(x+151,189),(x+32,189)],fill=c,outline=WHITE)
  d.polygon([(x+119,213),(x+151,189),(x+151,308),(x+119,330)],fill='#386075',outline=WHITE)
  d.rectangle((x,213,x+119,330),fill=c,outline=WHITE,width=2)
  count=12 if title=='MADEIRA' else 36
  for k in range(count):
   xx=x+12+(k*29)%94;yy=225+(k*23)%91;circle(d,xx,yy,2,'#f2e7c4')
  label(d,(x+63,367),title,17,c,'mm')
 label(d,(399,148),'MESMO VOLUME',14,TEAL,'mm')
 if kind=='mass_volume':label(d,(398,415),'Massa ÷ volume',23,GOLD,'mm')
 else:label(d,(398,415),'Massa diferente no mesmo espaço',17,WHITE,'mm')
 note(d,'Símbolos de massa; não representam contagem de átomos')
def hull(im,d,t,kind):
 water(d,t,level=314)
 ship(im,127,156,510,cut=kind!='harbor_ship',cargo=3)
 d=ImageDraw.Draw(im)
 if kind=='hull_reveal':
  scan=183+((t*.16)%1)*409
  d.line((scan,265,scan,390),fill=TEAL,width=2)
  label(d,(392,425),'INVESTIGANDO O INTERIOR',14,TEAL,'mm')
 elif kind=='hull_air':
  arrow(d,(390,177),(381,329),GOLD,3);label(d,(390,151),'PROTEGIDO DA ÁGUA',14,GOLD,'mm')
 elif kind in ['underwater_hull','hidden_volume']:
  for x in [220,310,405,500,578]:arrow(d,(x,423),(x,384),TEAL,3)
  label(d,(397,446),'A parte submersa também conta',14,TEAL,'mm')
 else:label(d,(394,426),'Casco + carga + espaços internos',15,WHITE,'mm')
 note(d)
def pressure(d,t,kind):
 water(d,t,level=161,bottom=438)
 d.rectangle((305,239,498,352),fill='#395b70',outline=WHITE,width=3)
 for x in [330,386,467]:
  arrow(d,(x,207),(x,233),CORAL,3)
  arrow(d,(x,419),(x,358),TEAL,4)
 for y in [258,301,338]:
  length=(y-230)*.35+24
  arrow(d,(305-length,y),(299,y),BLUE,2)
  arrow(d,(498+length,y),(504,y),BLUE,2)
 if kind=='buoyant_arrows':
  arrow(d,(616,407),(616,245),TEAL,6);label(d,(615,216),'EMPUXO',16,TEAL,'mm')
 else:
  label(d,(398,190),'MENOR PRESSÃO',14,CORAL,'mm');label(d,(398,437),'MAIOR PRESSÃO',14,TEAL,'mm')
 note(d,'Caixa submersa em líquido em repouso; setas sem escala')
def displacement(im,d,t,kind):
 water(d,t,level=300,left=78,right=419)
 ship(im,94,182,296,cut=True,cargo=1)
 d=ImageDraw.Draw(im)
 d.rounded_rectangle((486,251,683,401),radius=11,fill='#245e79',outline=BLUE,width=3)
 for x in range(496,675,22):d.line((x,270,x,383),fill='#498dad',width=1)
 arrow(d,(421,348),(476,348),GOLD,3)
 label(d,(584,427),'ÁGUA EQUIVALENTE',14,BLUE,'mm')
 label(d,(247,427),'PARTE SUBMERSA',14,TEAL,'mm')
 if kind=='number_example':
  label(d,(248,155),'10 toneladas',23,WHITE,'mm');label(d,(584,155),'10 m³',29,BLUE,'mm')
  label(d,(397,197),'Água doce: aproximação de 1.000 kg/m³',13,GOLD,'mm')
  note(d,'Exemplo inventado, com valores arredondados')
 else:
  label(d,(582,180),'PESO DA ÁGUA',16,BLUE,'mm');label(d,(245,180),'EMPUXO',18,TEAL,'mm')
  note(d,'O recipiente representa um volume; não é água sendo bombeada')
def balance(im,d,t,kind):
 water(d,t,level=311);ship(im,147,164,480,cargo=5)
 d=ImageDraw.Draw(im);forces(d,394,329)
 label(d,(400,158),'EMPUXO = PESO',23,GOLD,'mm');note(d,'Equilíbrio em água tranquila; setas representam forças')
def bowls(im,d,t,kind):
 water(d,t,level=306)
 is_clay=kind.startswith('clay');color='#bb8363' if is_clay else STEEL
 if kind in ['clay_ball','solid_vs_hollow','shape_transform','clay_compare']:
  yy=353+14*math.sin(t*.45);circle(d,205,yy,37,color,WHITE,2)
  label(d,(205,420),'BOLA' if is_clay else 'MACIÇO',15,CORAL,'mm')
 if kind in ['clay_boat','solid_vs_hollow','shape_transform','clay_compare']:
  xx=315 if kind=='clay_boat' else 442;yy=275
  d.polygon([(xx,yy),(xx+236,yy),(xx+197,yy+83),(xx+42,yy+83)],fill=color,outline=WHITE)
  d.polygon([(xx+18,yy+7),(xx+216,yy+7),(xx+188,yy+62),(xx+50,yy+62)],fill=NAVY,outline=GOLD)
  label(d,(xx+115,420),'TIGELA' if is_clay else 'RECIPIENTE',15,TEAL,'mm')
 label(d,(397,171),'MESMA MASSA',19,GOLD,'mm');note(d,'Simulação ilustrada • borda acima da água, interior protegido')
def loading(im,d,t,kind):
 q=(math.sin(t*.27)+1)/2;depth=round(23*q);cargo=2+int(q*7)
 water(d,t,level=320);ship(im,140,163+depth,493,cargo=cargo)
 d=ImageDraw.Draw(im)
 if kind=='freeboard':
  x=689;d.line((x,320,x,415+depth),fill=GOLD,width=3)
  for yy in [320,415+depth]:d.line((x-9,yy,x+9,yy),fill=GOLD,width=2)
  label(d,(664,369),'CALADO',11,GOLD,'rm')
 else:label(d,(393,152),'CARGA → MAIS ÁGUA DESLOCADA',16,GOLD,'mm')
 note(d,'Movimento exagerado para mostrar a mudança de calado')
def flooding(im,d,t,kind):
 q=.12 if kind=='flood_start' else (.45 if kind=='flood_progress' else .85)
 q=min(.95,q+.08*math.sin(t*.35));water(d,t,level=303)
 ship(im,139,163+q*42,493,cut=True,cargo=4,flood=q)
 d=ImageDraw.Draw(im)
 for k in range(5):
  x=641-k*18;yy=300+8*math.sin(t*2+k);circle(d,x,yy,3,BLUE)
 arrow(d,(664,306),(603,321),BLUE,4)
 label(d,(396,167),'ENTRADA DE ÁGUA',17,BLUE,'mm')
 note(d,'Modelo de inundação; não representa um acidente real')
def tilt(im,d,t,kind):
 water(d,t,level=325)
 angle=8*math.sin(t*.4) if kind=='tilt_boat' else 10+3*math.sin(t*.4)
 ship(im,119,139,470,cut=True,cargo=5,tilt=angle,cargo_shift=round(-40*(.5+.5*math.sin(t*.4))) if kind=='tilt_cargo' else 0)
 d=ImageDraw.Draw(im)
 label(d,(393,428),'FLUTUAR ≠ ESTAR ESTÁVEL',17,GOLD,'mm')
 note(d,'Inclinação ilustrativa; não é cálculo de estabilidade naval')
def salt(im,d,t,kind):
 for x,title,level,c in [(93,'ÁGUA DOCE',300,BLUE),(421,'ÁGUA SALGADA',300,TEAL)]:
  water(d,t,level=level,left=x,right=x+273,bottom=421)
  label(d,(x+135,171),title,16,c,'mm')
  if kind in ['egg_compare','water_density']:
   yy=351 if title=='ÁGUA DOCE' else 290
   d.ellipse((x+106,yy-32,x+164,yy+40),fill='#eee1b6',outline=WHITE,width=2)
   if title=='ÁGUA SALGADA':
    for k in range(16):circle(d,x+15+(k*43)%242,322+(k*23)%89,1.5,GOLD)
  else:ship(im,x+11,208 if title=='ÁGUA DOCE' else 186,245,cargo=3)
  d=ImageDraw.Draw(im)
 label(d,(397,449),'MESMO OBJETO • LÍQUIDOS DIFERENTES',12,GOLD,'mm')
 note(d,'Diferenças de altura ampliadas; concentração de sal ilustrativa')
def submarine(im,d,t,kind):
 rect(d,(78,145,715,441),'#15394e')
 level=kind=='sub_surface';y=251-43*(.5+.5*math.sin(t*.4)) if level else 261
 body=(115,y,674,y+104)
 d.rounded_rectangle(tuple(round(a) for a in body),radius=44,fill='#58788b',outline=WHITE,width=2)
 d.rounded_rectangle((154,y+18,637,y+85),radius=25,fill='#102834',outline=GOLD,width=2)
 d.rectangle((339,y-43,412,y),fill='#496a80',outline=WHITE,width=2)
 d.line((381,y-43,381,y-69,405,y-69),fill=STEEL,width=5)
 if kind=='ballast_fill':fraction=.2+.65*(t*.16%1)
 elif kind=='ballast_empty':fraction=.85-.7*(t*.16%1)
 else:fraction=.52 if kind=='sub_neutral' else .16
 for x in [177,480]:
  d.rounded_rectangle((x,y+31,x+121,y+73),radius=8,fill='#a2c9c2',outline=TEAL,width=2)
  rect(d,(x+4,y+71-round(fraction*37),x+117,y+71),BLUE)
 label(d,(395,y+51),'INTERIOR',12,WHITE,'mm')
 if kind in ['ballast_fill','ballast_empty']:
  start=(231,y+127) if kind=='ballast_fill' else (231,y+49)
  end=(231,y+70) if kind=='ballast_fill' else (231,y+129)
  arrow(d,start,end,BLUE,4);label(d,(395,412),'ÁGUA ENTRA' if kind=='ballast_fill' else 'ÁGUA SAI',17,BLUE,'mm')
  if kind=='ballast_empty':arrow(d,(570,y-32),(570,y+22),GOLD,3);label(d,(570,y-49),'AR COMPRIMIDO',11,GOLD,'mm')
 elif kind=='sub_neutral':
  forces(d,398,324,75,75);label(d,(395,180),'EMPUXO ≈ PESO',20,GOLD,'mm')
 elif level:
  d.line((81,y+49,711,y+49),fill=BLUE,width=3);arrow(d,(699,y+103),(699,y-22),TEAL,4)
 else:label(d,(395,406),'TANQUES DE LASTRO',17,TEAL,'mm')
 for k in range(9):circle(d,100+(k*79)%599,166+(k*41)%233,1,'#79a9bf')
 note(d,'Modelo simplificado; casco externo aproximadamente constante')
def iceberg(d,t):
 water(d,t,level=264)
 d.polygon([(195,264),(232,247),(297,234),(338,214),(385,248),(427,246),(477,264),(440,331),(382,406),(307,427),(227,339)],fill='#accfde',outline=WHITE)
 d.polygon([(232,247),(297,234),(338,214),(329,287),(292,329)],fill='#eef7ef')
 d.line((80,264,711,264),fill=BLUE,width=3)
 label(d,(558,222),'GELO',21,WHITE,'mm');label(d,(558,304),'ÁGUA LÍQUIDA',15,BLUE,'mm')
 label(d,(558,364),'Menor densidade',15,TEAL,'mm');note(d,'Proporções ilustradas; não é medição de um iceberg')
def challenge(im,d,t,kind):
 water(d,t,level=310)
 ship(im,87,204,288,cargo=0);ship(im,423,225 if kind=='challenge_answer' else 204,288,cargo=8)
 d=ImageDraw.Draw(im)
 label(d,(229,159),'SEM CARGA',16,TEAL,'mm');label(d,(564,159),'COM CARGA',16,CORAL,'mm')
 if kind=='challenge_answer':arrow(d,(654,386),(654,428),GOLD,3);label(d,(397,442),'MAIS VOLUME SUBMERSO',16,GOLD,'mm')
 else:
  q='?' if t<5 else 'Pense na água deslocada'
  label(d,(397,431),q,29 if q=='?' else 17,GOLD,'mm')
 note(d,'Barcos idênticos, em água tranquila; posição final ilustrada')
def recap(d,t):
 for x,title,c in [(97,'MASSA',CORAL),(300,'VOLUME',TEAL),(509,'LÍQUIDO',BLUE)]:
  d.rounded_rectangle((x,209,x+162,354),radius=12,fill='#19384a',outline=c,width=3)
  label(d,(x+81,382),title,15,c,'mm')
  if title=='MASSA':
   for k in range(4):rect(d,(x+22+k*29,261,x+45+k*29,314),c)
  elif title=='VOLUME':d.rectangle((x+43,247,x+123,323),outline=c,width=4)
  else:
   for y in range(252,328,16):d.line([(x+25+j,y+4*math.sin(j*.12-t)) for j in range(110)],fill=c,width=2)
 label(d,(395,156),'TRÊS PARTES DA COMPARAÇÃO',17,GOLD,'mm');note(d)

def pixel_scene(kind,t):
 env='Underwater' if kind.startswith(('sub_','submarine','ballast','pressure','buoyant','flood','ice_')) or kind=='underwater_hull' else ('Harbor' if kind in ['harbor_ship','harbor_end','hook_contrast','engine_off','hidden_volume','outro'] else 'Workshop')
 im=background(env,t)
 if kind in ['harbor_end','outro']:
  layer=Image.new('RGBA',(W,H));dd=ImageDraw.Draw(layer)
  dd.rounded_rectangle((55,106,723,309),radius=13,fill=(5,22,36,220),outline=TEAL,width=2)
  label(dd,(389,172),'QUASE INFINITO',34,GOLD,'mm')
  label(dd,(389,237),'Cada pergunta abre outra viagem.',19,WHITE,'mm')
  im.alpha_composite(layer)
  if kind=='harbor_end':
   d=ImageDraw.Draw(im)
   for k in range(12):
    xx=98+k*47;yy=392+6*math.sin(t*.8+k);d.line((xx,yy,xx+19,yy),fill=TEAL,width=2)
  return im.convert('RGB')
 d=panel(im,TITLES[kind])
 if kind in ['hook_contrast','recap_contrast']:comparison(im,d,t)
 elif kind in ['density_cubes','mass_volume']:densities(d,t,kind)
 elif kind in ['harbor_ship','hull_reveal','hull_air','underwater_hull','hidden_volume']:hull(im,d,t,kind)
 elif kind in ['pressure_zoom','pressure_cube','buoyant_arrows']:pressure(d,t,kind)
 elif kind in ['displacement','water_equivalent','number_example']:displacement(im,d,t,kind)
 elif kind=='ship_balance':balance(im,d,t,kind)
 elif kind in ['solid_vs_hollow','shape_transform','clay_ball','clay_boat','clay_compare']:bowls(im,d,t,kind)
 elif kind in ['cargo_loading','freeboard']:loading(im,d,t,kind)
 elif kind=='engine_off':
  hull(im,d,t,kind);d=ImageDraw.Draw(im);label(d,(395,158),'ATRACADO • SEM PROPULSÃO',17,GOLD,'mm')
 elif kind.startswith('flood'):flooding(im,d,t,kind)
 elif kind.startswith('tilt'):tilt(im,d,t,kind)
 elif kind in ['salt_compare','egg_compare','fresh_salt_boat','water_density']:salt(im,d,t,kind)
 elif kind.startswith(('sub','ballast')):submarine(im,d,t,kind)
 elif kind=='ice_density':iceberg(d,t)
 elif kind.startswith('challenge'):challenge(im,d,t,kind)
 elif kind=='recap_three':recap(d,t)
 else:raise ValueError('Unknown original scene '+kind)
 return im.convert('RGB')

def overlay(item,scene,local,global_time,source,pixel):
 im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im)
 d.rounded_rectangle((9,9,W-10,H-10),radius=14,outline=TEAL,width=4)
 d.rounded_rectangle((16,16,W-17,H-17),radius=11,outline=(255,203,114,168),width=1)
 d.rounded_rectangle((26,25,933,64),radius=7,fill=(5,20,33,221))
 label(d,(43,44),'QUASE INFINITO',13,GOLD,'lm')
 label(d,(262,44),item['title'],14,WHITE,'lm')
 rect(d,(27,493,933,521),(5,20,33,218));label(d,(39,507),source[:94],10,'#bbd9df','lm')
 if not pixel:label(d,(917,88),'REGISTRO REAL',11,WHITE,'rm')
 action=item['action'];height=202 if scene=='outro' else 186
 sprite=pico(action,local,height=height)
 if sprite.width>174:
  height=round(height*174/sprite.width);sprite=pico(action,local,height=height)
 x=min(W-25-sprite.width,758+4*math.sin(local*.4+item['index']*.7));y=284+9*math.sin(local*.7)
 if action=='flying':y-=24*math.sin(local*.4)
 im.alpha_composite(sprite,(round(x),round(y)))
 # A short gold trace follows Pico; no spoken words or caption cues are drawn.
 d=ImageDraw.Draw(im)
 for k in range(5):circle(d,x+57-k*7,y+sprite.height+11+k*.5,1,GOLD)
 progress=global_time/486
 d.line((30,529,30+898*max(0,min(1,progress)),529),fill=GOLD,width=2)
 return im
