"""Original ENSO explanations, real geographic outlines and an animated Pico."""
import hashlib,json,math
from functools import lru_cache
from pathlib import Path
from PIL import Image,ImageDraw
from base_art import W,H,NAVY,TEAL,GOLD,CORAL,WHITE,font,rect,label,arrow,wrap
import pico_animation
ROOT=Path(__file__).resolve().parent
ASSET_HASH=hashlib.sha256(b''.join(p.read_bytes() for p in sorted((ROOT/'assets').iterdir()) if p.suffix in ('.png','.geojson'))).hexdigest()
BLUE='#71bafa';WATER='#184c78';WARM='#ed9563';LAND='#316567'
TITLES={
 'hook_ocean':'O mar e o céu estão conectados','definition_pair':'El Niño • fase quente do sistema','warm_band':'Pacífico equatorial central e leste',
 'pacific_map':'Uma viagem pelo Pacífico','equator_pass':'A faixa da Linha do Equador',
 'trade_winds':'Alísios • de leste para oeste','warm_pool':'Uma reserva de calor no oeste','neutral_clouds':'Calor, umidade e nuvens',
 'upwelling':'A água fria que sobe','deep_dive':'Um corte ilustrado do oceano','nutrient_rise':'Água profunda e nutrientes',
 'fan_model':'Um modelo para acompanhar o empurrão','fan_push':'Ventilador representa os alísios',
 'fan_weak':'O ventilador diminui o empurrão','weak_winds':'O empurrão fica mais fraco','warm_spread':'O calor se redistribui',
 'coupled_system':'O oceano e a atmosfera respondem','ocean_air_loop':'Uma interação entre duas partes',
 'cloud_shift':'As nuvens mudam de posição','rain_belt':'A circulação e a chuva mudam',
 'teleconnection':'Uma conexão pela atmosfera','air_bridge':'Efeitos a longa distância',
 'brazil_north':'Partes do Norte e do Nordeste','region_caution':'As regiões têm diferenças internas',
 'brazil_south':'Possibilidade de mais chuva no Sul','rain_routes':'Sistemas de chuva e circulação',
 'not_switch':'O tempo depende de várias peças','weather_pieces':'El Niño modifica padrões e probabilidades',
 'three_states':'Quente • neutro • frio','nina_winds':'La Niña • águas mais frias',
 'irregular_clock':'O calendário não é um relógio','event_timeline':'Intervalos e durações variáveis',
 'name_story':'O nome e a época do Natal','coast_story':'Uma história ligada ao litoral peruano',
 'food_chain':'Nutrientes e vida marinha','marine_variation':'A resposta ecológica varia',
 'buoy_model':'Instrumentos acima e abaixo da superfície','monitor_lab':'Um conjunto de observações','sensor_link':'Oceano, vento, chuva e satélites',
 'anomaly_example':'Temperatura e diferença são coisas distintas','anomaly_difference':'Um exemplo de diferença positiva',
 'warming_compare':'Variação natural e tendência de longo prazo','trend_and_wave':'Os dois processos podem atuar juntos',
 'planning_field':'Informação para avaliar riscos','quiz_nino':'Qual pista explica melhor o fenômeno?',
 'quiz_answer':'Pacífico persistente + resposta da atmosfera','recap_ocean':'A resposta passa pelo mar e pelo céu','outro':'Cada pergunta abre outra viagem'}
LAB={'definition_pair','coupled_system','ocean_air_loop','not_switch','weather_pieces','three_states','irregular_clock','event_timeline','buoy_model','monitor_lab','sensor_link','anomaly_example','anomaly_difference','warming_compare','trend_and_wave','quiz_nino','quiz_answer'}

@lru_cache(None)
def scenery(kind):
 with Image.open(ROOT/'assets'/f'{kind}_Pixel_16x9.png') as im:return im.convert('RGBA').resize((1024,576),Image.Resampling.NEAREST)
def background(scene,t):
 kind='Field' if scene=='planning_field' else 'Lab' if scene in LAB else 'Pacific'
 src=scenery(kind);x=round(32+14*math.sin(t*.07));y=round(18+7*math.sin(t*.05));return src.crop((x,y,x+W,y+H))
def circle(d,x,y,r,fill,outline=None,width=2):d.ellipse(tuple(round(q) for q in (x-r,y-r,x+r,y+r)),fill=fill,outline=outline,width=width)
def panel(im,title):
 layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer)
 d.rounded_rectangle((38,77,748,487),radius=11,fill=(5,23,38,238),outline=(109,230,217,170),width=2)
 for x in range(61,733,33):
  for y in range(145,459,29):circle(d,x,y,.6,(141,216,215,30))
 rect(d,(56,91,60,118),GOLD);label(d,(74,105),title,18,GOLD,'lm');im.alpha_composite(layer);return ImageDraw.Draw(im)
def note(d,text='Modelo ilustrado • sem escala • não é uma observação atual'):
 label(d,(70,467),text,10,'#b7d4d6','lm')
def card(d,box,title,lines=(),color=TEAL,size=17):
 d.rounded_rectangle(tuple(round(q) for q in box),radius=10,fill='#1a3b50',outline=color,width=2)
 cx=(box[0]+box[2])/2;label(d,(cx,box[1]+29),title,size,color,'mm')
 for k,text in enumerate(lines):label(d,(cx,box[1]+71+k*29),text,size,WHITE,'mm')
def cloud(d,x,y,t,scale=1,rain=False):
 y+=2*math.sin(t*.6)
 for dx,dy,r in [(-33,0,21),(-10,-14,29),(24,-9,25),(48,3,18)]:circle(d,x+dx*scale,y+dy*scale,r*scale,'#bed7de')
 d.rounded_rectangle((x-45*scale,y-4*scale,x+62*scale,y+19*scale),radius=round(10*scale),fill='#bed7de')
 if rain:
  for k in range(8):
   xx=x-39*scale+k*13*scale;yy=y+26*scale+((t*50+k*11)%65)*scale
   d.line((xx,yy,xx-4*scale,yy+10*scale),fill=BLUE,width=2)
def moving_arrows(d,t,y,left=114,right=691,west=True,color=GOLD,weak=False,strong=False):
 count=3 if weak else 7 if strong else 5
 for k in range(count):
  x=left+((k*131+t*(15 if weak else 57 if strong else 39))%(right-left))
  length=44 if weak else 65;end=x-length if west else x+length
  if left<end<right:arrow(d,(x,y),(end,y),color,2 if weak else 3)
def ocean(d,t,warm=False,up=False,nutrients=False,clouds=False,cool=False):
 left,right,top,bottom=91,713,286,438
 d.rounded_rectangle((left,top,right,bottom),radius=8,fill=WATER,outline=BLUE,width=2)
 depth_w=38 if warm else 103 if cool else 84;depth_e=42 if warm else 12 if cool else 21
 d.polygon([(left+2,top+2),(right-2,top+2),(right-2,top+depth_e),(left+2,top+depth_w)],fill=WARM)
 if cool:d.polygon([(right-244,top+2),(right-2,top+2),(right-2,top+depth_e),(right-244,top+42)],fill=BLUE)
 d.line((left+4,top+depth_w,right-4,top+depth_e),fill=GOLD,width=2)
 for k in range(20):
  xx=left+((k*37+t*17)%(right-left-20));yy=top+11+(k%3)*12
  d.line((xx,yy,xx+15,yy),fill='#ffca8f',width=1)
 label(d,(183,405),'ÁGUA MAIS FRIA',14,'#a3d8ff','mm')
 label(d,(150,269),'SUPERFÍCIE',12,WHITE,'mm')
 label(d,(157,153),'OESTE',15,TEAL,'mm');label(d,(641,153),'LESTE',15,TEAL,'mm')
 label(d,(157,180),'Ásia / Oceania',13,WHITE,'mm');label(d,(641,180),'Américas',13,WHITE,'mm')
 if warm:moving_arrows(d,t,218,west=True,weak=True);moving_arrows(d,t,319,left=176,right=699,west=False,color='#b3413b')
 else:moving_arrows(d,t,218,west=True,strong=cool)
 if up:
  arrow(d,(645,418),(645,312 if not warm else 375),BLUE,4 if not warm else 2)
  for k in range(8 if not warm else 3):
   yy=425-((t*24+k*17)%(109 if not warm else 47));circle(d,646+7*math.sin(k),yy,2.5,TEAL if nutrients else BLUE)
 if nutrients:label(d,(563,449),'NUTRIENTES',13,TEAL,'mm')
 if clouds:cloud(d,476 if warm else 232,242,t,.67,True)
 note(d)

@lru_cache(None)
def countries():return json.loads((ROOT/'assets/world_110m.geojson').read_text())['features']
def polygons(feature):
 g=feature['geometry'];return g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
def pacific_map(d,t,warm=False):
 layer=Image.new('RGBA',(658,287),'#12304b');dd=ImageDraw.Draw(layer)
 def project(lon,lat):return ((lon%360-40)/300*658,(60-lat)/120*287)
 for f in countries():
  if f['properties'].get('CONTINENT') not in ('Asia','Oceania','North America','South America') and f['properties']['ADMIN']!='Russia':continue
  for poly in polygons(f):
   pts=[project(lon,lat) for lon,lat in poly[0]]
   dd.polygon(pts,fill=LAND,outline='#67a591')
 yy=project(180,0)[1];dd.line((0,yy,658,yy),fill='#b4ddd1',width=1)
 if warm:
  x0=project(169,0)[0];x1=project(278,0)[0]
  dd.rounded_rectangle((x0,yy-15,x1,yy+15),radius=13,fill=(255,147,93,224))
  for k in range(9):circle(dd,x0+((t*14+k*37)%(x1-x0)),yy,2,GOLD)
 layer_rgb=layer.convert('RGB')
 # Paste the exact geographic outlines onto the drawing's owning image.
 d._image.paste(layer_rgb,(75,146))
 label(d,(393,158),'PACÍFICO',20,GOLD,'mm');label(d,(159,300),'Equador',11,WHITE,'mm')
 label(d,(232,420),'ÁSIA / OCEANIA',13,TEAL,'mm');label(d,(645,420),'AMÉRICAS',13,TEAL,'mm')
 if warm:label(d,(429,339),'CENTRO E LESTE EQUATORIAL',13,CORAL,'mm')
 note(d,'Limites: Natural Earth • faixa e cores explicativas, sem dados atuais')
def brazil(d,t,south=False,caution=False):
 feature=next(f for f in countries() if f['properties']['ADMIN']=='Brazil')
 def xy(lon,lat):return 72+(lon+75)*8.6,186+(6-lat)*6.15
 for poly in polygons(feature):d.polygon([xy(*p) for p in poly[0]],fill=LAND,outline=TEAL,width=2)
 label(d,(262,163),'BRASIL',20,GOLD,'mm')
 centers=[(-52,-28)] if south else [(-53,-2),(-40,-5)]
 for lon,lat in centers:
  x,y=xy(lon,lat);circle(d,x,y,25+3*math.sin(t),'#995c3f' if not south else '#285e88',GOLD if not south else BLUE,2)
 if caution:card(d,(443,197,719,420),'VARIAÇÕES',['Região','Época do ano','Cada episódio'],GOLD)
 elif south:
  card(d,(443,197,719,420),'POSSIBILIDADE',['Chuvas acima','da média','em certas estações'],BLUE)
  cloud(d,582,381,t,.58,True)
 else:
  card(d,(443,197,719,420),'POSSIBILIDADE',['Menos chuva','em partes do','Norte e Nordeste'],CORAL)
 note(d,'Áreas indicadas são esquemáticas • tendências variam por lugar e estação')

def fan(d,t,weak=False):
 cx,cy=630,283;circle(d,cx,cy,57,'#244453',TEAL,3)
 for k in range(3):
  a=t*(.8 if weak else 3.4)+k*math.tau/3
  pts=[(cx,cy),(cx+44*math.cos(a-.3),cy+44*math.sin(a-.3)),(cx+49*math.cos(a+.28),cy+49*math.sin(a+.28))]
  d.polygon(pts,fill=TEAL)
 circle(d,cx,cy,12,GOLD);rect(d,(624,344,637,402),TEAL);rect(d,(585,400,678,407),GOLD)
 label(d,(630,194),'ALÍSIOS',17,GOLD,'mm')
 d.rounded_rectangle((91,271,501,421),radius=8,fill=WATER,outline=BLUE,width=3)
 slope=25 if weak else 75;d.polygon([(95,275),(497,275),(497,299),(95,299+slope)],fill=WARM)
 moving_arrows(d,t,235,left=97,right=534,west=True,weak=weak)
 label(d,(291,377),'ÁGUA MAIS FRIA',16,BLUE,'mm');note(d,'Analogia visual • não é um experimento medido')
def pair(d,t):
 card(d,(96,189,346,401),'OCEANO',[],GOLD);card(d,(451,189,701,401),'ATMOSFERA',[],TEAL)
 for k in range(6):
  y=278+k*12;d.line((119,y,322,y),fill=WARM if k<3 else BLUE,width=5)
 cloud(d,573,300,t,.86,True)
 arrow(d,(354,264),(443,264),GOLD,3);arrow(d,(443,339),(354,339),TEAL,3)
 note(d,'A interação combina aquecimento persistente e resposta atmosférica')
def hook(d,t):
 card(d,(81,190,349,422),'MENOS CHUVA',[],CORAL);card(d,(442,190,710,422),'MAIS CHUVA',[],BLUE)
 circle(d,215,305,43,GOLD)
 for k in range(8):
  a=k*math.tau/8;d.line((215+52*math.cos(a),305+52*math.sin(a),215+63*math.cos(a),305+63*math.sin(a)),fill=GOLD,width=3)
 cloud(d,569,303,t,1.05,True);note(d,'Efeitos variam conforme a região, a estação e o episódio')
def teleconnection(d,t):
 for x,name,color in [(210,'PACÍFICO',CORAL),(589,'BRASIL',TEAL)]:
  circle(d,x,327,80,'#184669',color,3)
  for yy in [300,327,354]:d.arc((x-77,yy-36,x+77,yy+36),0,180,fill='#6897ad',width=1)
  label(d,(x,430),name,18,color,'mm')
 d.arc((209,171,590,394),180,358,fill=GOLD,width=4)
 q=(t*.11)%1;x=210+379*q;y=282-108*math.sin(math.pi*q);circle(d,x,y,5,WHITE)
 note(d,'Ligação esquemática • não representa água do Pacífico chegando ao Brasil')

def weather_pieces(d,t):
 for k,(box,title,lines,c) in enumerate([
  ((83,177,362,296),'PACÍFICO',['El Niño / La Niña'],CORAL),((427,177,706,296),'ATLÂNTICO',['Outro oceano'],BLUE),
  ((83,321,362,440),'SISTEMAS',['Frentes e massas de ar'],TEAL),((427,321,706,440),'LOCAL',['Condições da região'],GOLD)]):
  card(d,box,title,lines,c,15)
  if int(t*.5)%4==k:d.rounded_rectangle((box[0]-4,box[1]-4,box[2]+4,box[3]+4),radius=13,outline=WHITE,width=2)
 note(d,'Padrões e probabilidades • nenhum fenômeno explica sozinho cada chuva')
def states(d,t):
 for k,(x,word,line,c) in enumerate([(188,'EL NIÑO','Mais quente',CORAL),(397,'NEUTRO','Próximo da referência',TEAL),(606,'LA NIÑA','Mais frio',BLUE)]):
  card(d,(x-92,185,x+92,407),word,[],c,18)
  for j in range(5):d.line((x-61,280+j*13,x+61,280+j*13),fill=c if j<3 else WATER,width=5)
  label(d,(x,368),line,12,WHITE,'mm')
  if int(t/2.4)%3==k:d.rounded_rectangle((x-97,180,x+97,412),radius=12,outline=GOLD,width=2)
 note(d,'Fases do sistema • neutralidade não impede eventos extremos')
def intervals(d,t):
 card(d,(81,192,350,384),'INTERVALOS',['2 a 7 anos','em geral'],GOLD,20)
 card(d,(441,192,710,384),'DURAÇÃO',['9 a 12 meses','em geral'],TEAL,20)
 d.line((116,422,676,422),fill='#64939b',width=2)
 for x in [119,280,340,546,676]:circle(d,x,422,4+(2 if int(t*.6)%5==[119,280,340,546,676].index(x) else 0),GOLD)
 note(d,'Intervalos irregulares • durações variam • marcadores não são anos reais')
def boat(d,t):
 for k in range(8):
  yy=338+k*12;d.line((106,yy,689,yy),fill='#396f8c',width=2)
 y=322+5*math.sin(t*.8)
 d.polygon([(235,y),(566,y),(520,y+55),(292,y+55)],fill='#9c663f',outline=GOLD)
 rect(d,(394,y-126,401,y),GOLD);d.polygon([(405,y-116),(482,y-21),(405,y-21)],fill='#e9daba',outline=WHITE)
 label(d,(398,183),'NOME LIGADO À ÉPOCA DO NATAL',17,GOLD,'mm')
 label(d,(398,421),'LITORAL PERUANO',18,TEAL,'mm');note(d,'Cena e barco ilustrados • não é registro histórico')
def fish(d,x,y,t,color=GOLD):
 y+=6*math.sin(t)
 d.ellipse((x-25,y-13,x+25,y+13),fill=color,outline=WHITE,width=1)
 d.polygon([(x-22,y),(x-41,y-17),(x-41,y+17)],fill=color);circle(d,x+14,y-3,2,NAVY)
def food_chain(d,t,variation=False):
 for x,title,c in [(169,'NUTRIENTES',TEAL),(393,'ORGANISMOS',GOLD),(617,'PEIXES',BLUE)]:
  card(d,(x-95,186,x+95,390),title,[],c,15)
 for k in range(17):circle(d,124+(k*17)%94,264+(k*23)%87,2+(k%2),TEAL)
 for k in range(9):
  x=346+(k*27)%99;y=272+(k*15)%59;circle(d,x,y,5,GOLD)
  d.line((x-7,y,x+7,y),fill=CORAL,width=1)
 fish(d,616,292,t,BLUE);fish(d,616,341,t+1,TEAL)
 arrow(d,(269,303),(290,303),GOLD,3);arrow(d,(493,303),(516,303),GOLD,3)
 label(d,(395,427),'RELAÇÕES QUE PODEM MUDAR',17,TEAL,'mm')
 note(d,'Modelo de relações • espécies e intensidades variam entre ambientes')
def sensors(d,t,kind):
 if kind=='monitor_lab':
  for k,(x,title,lines,c) in enumerate([(188,'OCEANO',['Temperatura','Superfície / fundo'],GOLD),(397,'ATMOSFERA',['Vento e chuva','Resposta ao oceano'],TEAL),(606,'SATÉLITES',['Observações','Visão de grandes áreas'],BLUE)]):
   card(d,(x-92,192,x+92,408),title,lines,c,13)
   circle(d,x,360,10+4*math.sin(t+k),c)
  note(d,'Laboratório ilustrado • os instrumentos não mostram dados de um boletim');return
 d.rounded_rectangle((108,279,688,435),radius=8,fill=WATER,outline=BLUE,width=2)
 cy=279+3*math.sin(t*.75)
 d.ellipse((221,cy-15,340,cy+15),fill=GOLD,outline=WHITE,width=2)
 rect(d,(273,193,285,cy-5),TEAL);d.line((279,193,339,193),fill=GOLD,width=3)
 for yy in [334,376,416]:
  d.line((279,cy+16,279,yy),fill='#bac3cb',width=2);rect(d,(271,yy-5,287,yy+5),TEAL)
 label(d,(279,161),'BOIA ILUSTRADA',15,GOLD,'mm')
 rect(d,(521,191,547,227),'#accbd8');rect(d,(479,197,515,222),BLUE);rect(d,(553,197,589,222),BLUE)
 d.line((534,229,280,271),fill='#6d9fa8',width=1)
 for k in range(4):circle(d,291+((t*36+k*56)%244),268-((t*36+k*56)%244)*.16,2,GOLD)
 label(d,(536,160),'SATÉLITE',15,BLUE,'mm');note(d,'Modelo ilustrado de observação • sem medições atuais')
def anomaly(d,t):
 examples=[(182,'REFERÊNCIA','26 °C',TEAL),(397,'OBSERVADO','27 °C',GOLD),(612,'DIFERENÇA','+1 °C',CORAL)]
 for k,(x,word,value,c) in enumerate(examples):
  card(d,(x-96,210,x+96,384),word,[],c,15)
  label(d,(x,305),value,33,c,'mm')
  if int(t/2)%3==k:d.line((x-61,355,x+61,355),fill=WHITE,width=3)
 label(d,(396,167),'EXEMPLO INVENTADO',19,GOLD,'mm')
 label(d,(398,427),'27 − 26 = +1',22,WHITE,'mm')
 note(d,'Exemplo aritmético • não diagnostica El Niño nem representa dados atuais')
def warming(d,t,combined=False):
 if not combined:
  card(d,(84,188,361,406),'EL NIÑO',['Variação natural','Oceano + atmosfera','Meses a poucos anos'],CORAL,16)
  card(d,(427,188,704,406),'AQUECIMENTO GLOBAL',['Tendência de longo prazo','Influência humana','Acúmulo de calor'],GOLD,16)
 else:
  x0,y0,x1,y1=104,409,695,188
  d.line((x0,y1,x0,y0,x1,y0),fill='#94bac6',width=2)
  trend=[];wave=[];both=[]
  for k in range(240):
   x=x0+k/239*(x1-x0);base=371-k*.52;var=27*math.sin(k*.078)
   trend.append((x,base));wave.append((x,312+var));both.append((x,base+var))
  d.line(trend,fill=GOLD,width=3);d.line(wave,fill=BLUE,width=2);d.line(both,fill=CORAL,width=3)
  index=int(t*15)%240;circle(d,*both[index],4,WHITE)
  label(d,(399,435),'TEMPO →',14,WHITE,'mm')
  label(d,(227,163),'TENDÊNCIA',13,GOLD,'mm');label(d,(397,163),'VARIABILIDADE',13,BLUE,'mm');label(d,(607,163),'COMBINAÇÃO',13,CORAL,'mm')
 note(d,'Esquema conceitual sem dados reais • os processos podem atuar juntos')
def planning(d,t):
 for x,word,c in [(177,'ÁGUA',BLUE),(397,'LAVOURAS',TEAL),(617,'PLANEJAMENTO',GOLD)]:
  card(d,(x-94,208,x+94,383),word,[],c,14)
  if word=='ÁGUA':
   d.polygon([(x,265),(x-21,309),(x-12,332),(x+12,332),(x+21,309)],fill=c)
  elif word=='LAVOURAS':
   d.line((x,334,x,273),fill=c,width=4)
   for k in range(3):
    y=280+k*17;d.ellipse((x-30,y-8,x,y+7),fill=c);d.ellipse((x,y-6,x+30,y+9),fill=c)
  else:
   d.rounded_rectangle((x-30,268,x+30,333),radius=4,outline=c,width=2)
   for y in [282,297,312]:d.line((x-18,y,x+19,y),fill=c,width=3)
 label(d,(397,427),'BOLETINS + OBSERVAÇÃO LOCAL',16,GOLD,'mm');note(d,'Propriedade ilustrada • tendência regional precisa de informação local')
def quiz(d,t,answer=False):
 choices=[('A','Um dia quente em uma praia'),('B','Pacífico persistente + resposta da atmosfera'),('C','O mesmo tempo em todo o Brasil')]
 for k,(letter,line) in enumerate(choices):
  y=180+k*86;c=TEAL if answer and letter=='B' else '#7c9ca8'
  d.rounded_rectangle((72,y,718,y+69),radius=10,fill='#1c3a4d',outline=c,width=3)
  circle(d,108,y+35,20,c);label(d,(108,y+35),letter,18,NAVY,'mm');label(d,(148,y+35),line,16,WHITE,'lm')
 note(d,'A pista reúne o oceano e a atmosfera • efeitos não são iguais em todo lugar')
def recap(d,t):
 for k,(x,title,lines,c) in enumerate([(180,'OCEANO',['Calor se redistribui'],CORAL),(397,'VENTOS',['Circulação responde'],TEAL),(614,'CHUVA',['Padrões mudam'],BLUE)]):
  card(d,(x-95,208,x+95,394),title,lines,c,14)
  if k==0:
   for j in range(4):d.line((x-57,309+j*11,x+57,309+j*11),fill=c,width=5)
  elif k==1:moving_arrows(d,t,331,left=x-68,right=x+68,west=True,color=c,weak=True)
  else:cloud(d,x-8,326,t,.55,True)
 arrow(d,(282,296),(293,296),GOLD,2);arrow(d,(499,296),(512,296),GOLD,2)
 note(d,'Um sistema conectado • cada episódio e cada região têm suas diferenças')

def pixel_scene(scene,t):
 im=background(scene,t)
 if scene=='outro':
  layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer)
  d.rounded_rectangle((134,143,734,336),radius=14,fill=(5,22,36,232),outline=GOLD,width=2)
  label(d,(435,216),'QUASE INFINITO',31,GOLD,'mm');label(d,(435,281),'Cada pergunta abre outra viagem.',19,WHITE,'mm')
  im.alpha_composite(layer);return im.convert('RGB')
 d=panel(im,TITLES[scene])
 if scene=='hook_ocean':hook(d,t)
 elif scene in ('definition_pair','coupled_system','ocean_air_loop'):pair(d,t)
 elif scene in ('warm_band','pacific_map','equator_pass'):pacific_map(d,t,scene=='warm_band')
 elif scene in ('trade_winds','warm_pool','neutral_clouds'):ocean(d,t,clouds=scene=='neutral_clouds')
 elif scene in ('upwelling','deep_dive','nutrient_rise'):ocean(d,t,up=True,nutrients=True)
 elif scene in ('fan_model','fan_push','fan_weak'):fan(d,t,scene=='fan_weak')
 elif scene in ('weak_winds','warm_spread'):ocean(d,t,warm=True,up=True)
 elif scene in ('cloud_shift','rain_belt'):ocean(d,t,warm=True,clouds=True)
 elif scene in ('teleconnection','air_bridge'):teleconnection(d,t)
 elif scene in ('brazil_north','region_caution','brazil_south','rain_routes'):brazil(d,t,scene in ('brazil_south','rain_routes'),scene=='region_caution')
 elif scene in ('not_switch','weather_pieces'):weather_pieces(d,t)
 elif scene=='three_states':states(d,t)
 elif scene=='nina_winds':ocean(d,t,up=True,nutrients=True,cool=True)
 elif scene in ('irregular_clock','event_timeline'):intervals(d,t)
 elif scene in ('name_story','coast_story'):boat(d,t)
 elif scene in ('food_chain','marine_variation'):food_chain(d,t,scene=='marine_variation')
 elif scene in ('buoy_model','monitor_lab','sensor_link'):sensors(d,t,scene)
 elif scene in ('anomaly_example','anomaly_difference'):anomaly(d,t)
 elif scene in ('warming_compare','trend_and_wave'):warming(d,t,scene=='trend_and_wave')
 elif scene=='planning_field':planning(d,t)
 elif scene in ('quiz_nino','quiz_answer'):quiz(d,t,scene=='quiz_answer')
 elif scene=='recap_ocean':recap(d,t)
 else:raise ValueError('Unknown ENSO scene: '+scene)
 return im.convert('RGB')

def overlay(item,scene,local,global_time,source,pixel):
 im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im)
 d.rounded_rectangle((9,9,W-10,H-10),radius=14,outline=TEAL,width=4)
 d.rounded_rectangle((16,16,W-17,H-17),radius=11,outline=(255,203,114,163),width=1)
 d.rounded_rectangle((26,25,933,64),radius=7,fill=(5,20,33,228))
 label(d,(43,44),'QUASE INFINITO',13,GOLD,'lm');label(d,(261,44),item['title'],14,WHITE,'lm')
 if pixel:source='Cenário e modelo ilustrados • Quase Infinito'
 else:
  d.rounded_rectangle((746,75,926,101),radius=5,fill=(5,20,33,222));label(d,(916,88),'IMAGEM ATUAL ILUSTRATIVA',10,WHITE,'rm')
 rect(d,(27,493,933,521),(5,20,33,226));label(d,(39,507),source[:94],10,'#c0d9dc','lm')
 plan,box=pico_animation.place(im,item,scene,local)
 if plan['cycle']=='flying':
  d=ImageDraw.Draw(im);direction=1 if plan['flip'] else -1
  anchor=box[0]+box[2]*(.83 if plan['flip'] else .17);yy=box[1]+box[3]*.72
  for k in range(6):
   xx=anchor+direction*k*8
   if 27<xx<931 and 78<yy<486:circle(d,xx,yy+2*math.sin(local*3+k),1+(k==0),GOLD)
 d.line((30,529,30+898*max(0,min(1,global_time/498)),529),fill=GOLD,width=2)
 # Source credits and explanatory labels remain; narration captions are absent.
 return im
