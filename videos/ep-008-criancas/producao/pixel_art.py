"""Original timeline, document and calendar graphics for an investigation of Children's Day."""
import hashlib,math
from functools import lru_cache
from pathlib import Path
from PIL import Image,ImageDraw
from base_art import W,H,NAVY,TEAL,GOLD,CORAL,WHITE,font,rect,label,arrow,pico,wrap
ROOT=Path(__file__).resolve().parent
ASSET_HASH=hashlib.sha256(b''.join(p.read_bytes() for p in sorted((ROOT/'assets').glob('*.png')))).hexdigest()
BLUE='#79b7f6';PAPER='#ecdbb0'
TITLES={
'gift_question':'O que existe por trás da comemoração?','three_layers':'Três pistas para investigar','calendar_layers':'Um dia, diferentes histórias',
'archive_arrival':'A viagem começa nos documentos','year_1924':'Brasil • 1924','decree_seal':'Uma festa dedicada à criança',
'proposal_path':'Da proposta à oficialização','decree_card':'Decreto nº 4.867 • 1924',
 'two_dates':'Assinatura e comemoração','october_calendar':'12 de outubro','date_insight':'Cada data tem uma função',
'decree_excerpt':'O que o texto institui','gift_not_required':'Uma data e um costume','paper_to_people':'O documento começa a circular','tradition_cycle':'Uma tradição ganha diferentes sentidos',
 'toyshop_arrival':'O mundo dos brinquedos','company_timeline':'A data já existia antes da empresa','materials_reveal':'Objetos que atravessam gerações',
'campaign_board':'A comemoração também chega às vitrines','commercial_flow':'Como uma associação se reforça','gift_chain':'Presentes e memória',
'play_options':'Mais de uma forma de celebrar','gift_and_play':'A brincadeira pode continuar fora da caixa',
'holiday_question':'O feriado tem outra origem','holiday_1980':'Lei nº 6.802 • 1980',
'world_dates':'Calendários diferentes','portugal_calendar':'Portugal • 1 de junho','november_calendar':'Dia Mundial da Criança • 20 de novembro',
'international_pair':'Dois marcos em 20 de novembro','worldrights_timeline':'1959 → 1989',
'rights_cards':'Atenção à infância','play_world':'Inventar, brincar, descobrir',
'brazil_rights':'Marcos brasileiros','timeline_1988_1990':'Constituição e Estatuto','rights_book':'Uma comemoração e direitos permanentes',
'listen_scene':'Quem é celebrado também pode participar','different_play':'Brincadeiras e memórias diferentes',
'year_round':'O ano inteiro também importa','care_everyday':'A atenção continua depois da festa','calendar_loop':'Um dia no calendário, infância todos os dias',
'recap_three':'As três pistas se encontram','recap_timeline':'Uma história construída em etapas',
'quiz_dates':'Qual frase reúne as pistas?','quiz_answer':'Diferentes histórias se encontram',
'box_reveal':'A resposta estava dentro da história','childhood_meaning':'Uma sociedade olhando para suas crianças',
'park_end':'Qual brincadeira marcou sua memória?','outro':'Cada pergunta abre outra viagem'}
ARCHIVE={'archive_arrival','year_1924','decree_seal','proposal_path','decree_card','two_dates','october_calendar','date_insight','decree_excerpt','paper_to_people','holiday_question','holiday_1980','brazil_rights','timeline_1988_1990','rights_book','recap_timeline'}
SHOP={'gift_question','gift_not_required','toyshop_arrival','company_timeline','materials_reveal','campaign_board','commercial_flow','gift_chain','box_reveal'}

@lru_cache(None)
def scenery(kind):
 with Image.open(ROOT/'assets'/f'{kind}_Pixel_16x9.png') as im:return im.convert('RGBA').resize((1024,576),Image.Resampling.NEAREST)
def background(kind,t):
 src=scenery(kind);x=round(32+16*math.sin(t*.07));y=round(18+8*math.sin(t*.055));return src.crop((x,y,x+W,y+H))
def circle(d,x,y,r,fill,outline=None,width=2):d.ellipse(tuple(round(q) for q in (x-r,y-r,x+r,y+r)),fill=fill,outline=outline,width=width)
def panel(im,title):
 layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer)
 d.rounded_rectangle((38,77,748,487),radius=11,fill=(5,23,38,237),outline=(109,230,217,160),width=2)
 for x in range(61,733,29):
  for y in range(140,458,27):circle(d,x,y,.6,(140,208,211,29))
 rect(d,(56,91,60,118),GOLD);label(d,(74,105),title,19,GOLD,'lm');im.alpha_composite(layer);return ImageDraw.Draw(im)
def note(d,text='Esquema ilustrado • informações nas fontes'):
 label(d,(70,467),text,10,'#a2c2ca','lm')
def sparkles(d,t,area=(82,140,700,429)):
 for k in range(16):
  x=area[0]+(k*67)%(area[2]-area[0]);y=area[1]+(k*47)%(area[3]-area[1]);r=1+int((math.sin(t+k)+1)*.6)
  circle(d,x,y,r,'#bdac64')
def gift(d,x,y,size=105,t=0):
 y+=math.sin(t*1.3)*3;w=size;h=size*.81
 d.rounded_rectangle((round(x-w/2),round(y-h/2),round(x+w/2),round(y+h/2)),radius=5,fill='#267f7e',outline=TEAL,width=2)
 for xx in range(round(x-w/2+12),round(x+w/2-7),19):
  for yy in range(round(y-h/2+11),round(y+h/2-5),17):circle(d,xx,yy,2,GOLD)
 rect(d,(x-8,y-h/2,x+8,y+h/2),CORAL);rect(d,(x-w/2,y-5,x+w/2,y+5),CORAL)
 d.ellipse((x-37,y-h/2-29,x+3,y-h/2+3),fill=CORAL,outline=GOLD,width=2)
 d.ellipse((x-3,y-h/2-29,x+37,y-h/2+3),fill=CORAL,outline=GOLD,width=2)
 circle(d,x,y-h/2-6,8,GOLD)
def book(d,x,y,w=99,h=119,title=None,color=TEAL):
 d.rounded_rectangle((x-w/2,y-h/2,x+w/2,y+h/2),radius=6,fill='#24485a',outline=color,width=3)
 rect(d,(x-w/2+9,y-h/2+5,x-w/2+16,y+h/2-5),color)
 if title:
  for k,line in enumerate(title.split('\n')):label(d,(x+4,y+(k-(len(title.split('\n'))-1)/2)*25),line,18,color,'mm')
 else:
  for yy in range(round(y-h/2+25),round(y+h/2-15),17):d.line((x-w/2+27,yy,x+w/2-15,yy),fill='#8db8c1',width=2)
def calendar(d,x,y,w,month,day,year=None,color=TEAL):
 h=w*.85;left=x-w/2;top=y-h/2
 d.rounded_rectangle((left,top,left+w,top+h),radius=9,fill=PAPER,outline=color,width=3)
 d.rounded_rectangle((left+3,top+3,left+w-3,top+33),radius=6,fill=color)
 label(d,(x,top+19),month,15,NAVY,'mm')
 label(d,(x,y+5),str(day),round(w*.31),NAVY,'mm')
 if year:label(d,(x,top+h-15),str(year),13,'#345767','mm')
 for xx in [left+w*.27,left+w*.72]:d.line((xx,top-9,xx,top+9),fill=GOLD,width=5)
def child(d,x,y,skin='#bf8057',shirt=TEAL,t=0,size=1):
 # Symbolic character, not the likeness of a photographed child.
 x=round(x);y=round(y+math.sin(t*1.1)*2);r=round(14*size)
 circle(d,x,y,r,skin,NAVY,1);d.arc((x-r,y-r,x+r,y+r),181,359,fill='#3a2b28',width=max(2,round(6*size)))
 circle(d,x-5*size,y,1.3*size,NAVY);circle(d,x+5*size,y,1.3*size,NAVY)
 d.arc((x-6*size,y+1*size,x+6*size,y+9*size),0,180,fill=NAVY,width=1)
 rect(d,(x-13*size,y+15*size,x+13*size,y+47*size),shirt)
 d.line((x-11*size,y+25*size,x-25*size,y+36*size),fill=skin,width=max(3,round(6*size)))
 d.line((x+11*size,y+25*size,x+25*size,y+36*size),fill=skin,width=max(3,round(6*size)))
 d.line((x-7*size,y+47*size,x-10*size,y+70*size),fill='#425e82',width=max(3,round(7*size)))
 d.line((x+7*size,y+47*size,x+10*size,y+70*size),fill='#425e82',width=max(3,round(7*size)))
 rect(d,(x-17*size,y+68*size,x-4*size,y+73*size),NAVY);rect(d,(x+4*size,y+68*size,x+17*size,y+73*size),NAVY)
def ball(d,x,y,r=24,t=0):
 circle(d,x,y,r,GOLD,WHITE,2);d.arc((x-r,y-r,x+r,y+r),int(t*25)%360,int(t*25)%360+160,fill=CORAL,width=5)
 d.line((x-r*.7,y-r*.4,x+r*.7,y+r*.4),fill=NAVY,width=2)
def blocks(d,x,y,t,shape='house'):
 q=(math.sin(t*.5)+1)/2
 for k in range(7):
  if shape=='house':xx=x+(k%3)*33;yy=y-(k//3)*34
  else:xx=x+k*34;yy=y-(30 if k in [0,6] else 64)
  c=[TEAL,CORAL,GOLD,BLUE][k%4];rect(d,(xx,yy,xx+30,yy+30),c)
  d.rectangle((xx+3,yy+3,xx+26,yy+26),outline='#d9efde',width=1)
 if shape=='house':d.polygon([(x-7,y-72),(x+49,y-110),(x+106,y-72)],fill=CORAL,outline=WHITE)
def timeline(d,events,t,y=331,left=114,right=682):
 d.line((left,y,right,y),fill='#558892',width=3)
 for k,(date,text) in enumerate(events):
  x=left+k*(right-left)/max(1,len(events)-1);active=(int(t/1.8)%len(events))==k
  circle(d,x,y,11 if active else 8,GOLD if active else TEAL,NAVY,2)
  label(d,(x,y-44),date,20,GOLD if active else TEAL,'mm')
  for j,line in enumerate(text.split('\n')):label(d,(x,y+34+j*22),line,14,WHITE,'mm')
def card(d,box,head,lines,color=TEAL):
 d.rounded_rectangle(box,radius=10,fill='#1b3c50',outline=color,width=2)
 cx=(box[0]+box[2])/2;label(d,(cx,box[1]+30),head,17,color,'mm')
 for j,line in enumerate(lines):label(d,(cx,box[1]+69+j*30),line,17,WHITE,'mm')
def document(d,t,kind):
 d.rounded_rectangle((166,146,624,436),radius=8,fill=PAPER,outline=GOLD,width=3)
 for xx in range(180,610,35):d.line((xx,160,xx,425),fill='#dfc995',width=1)
 label(d,(395,177),'FICHA DA PESQUISA',12,'#536b69','mm')
 label(d,(395,218),'DECRETO Nº 4.867',25,NAVY,'mm')
 label(d,(395,256),'5 DE NOVEMBRO DE 1924',18,'#425d5f','mm')
 d.line((199,280,591,280),fill='#9d916a',width=2)
 label(d,(395,313),'12 DE OUTUBRO',26,'#245e65','mm')
 label(d,(395,350),'FESTA DA CRIANÇA',21,'#245e65','mm')
 label(d,(395,400),'Fonte: Câmara dos Deputados',13,'#425d5f','mm')
 if kind=='decree_excerpt':
  xx=211+(t*.1%1)*370;d.line((211,371,xx,371),fill=CORAL,width=4)
 note(d,'Síntese visual baseada no documento; não é reprodução do original')
def layers(d,t,kind):
 for k,(x,head,color) in enumerate([(178,'DATA',GOLD),(398,'COSTUMES',CORAL),(612,'DIREITOS',TEAL)]):
  lift=3*math.sin(t*.7+k);box=(x-94,186+lift,x+94,385+lift)
  d.rounded_rectangle(box,radius=12,fill='#19394a',outline=color,width=3)
  label(d,(x,220+lift),head,17,color,'mm')
  if k==0:calendar(d,x,307+lift,112,'OUTUBRO',12,color=color)
  elif k==1:gift(d,x,308+lift,99,t)
  else:book(d,x,304+lift,92,106,'INFÂNCIA',color)
 if kind=='recap_three':label(d,(395,425),'TRÊS PISTAS • UMA INVESTIGAÇÃO',15,GOLD,'mm')
 note(d)
def two_dates(d,t,kind):
 if kind=='october_calendar':
  calendar(d,397,296,230,'OUTUBRO',12,color=TEAL);note(d,'Data anual da comemoração brasileira');return
 calendar(d,233,307,187,'NOVEMBRO',5,1924,GOLD);calendar(d,567,307,187,'OUTUBRO',12,None,TEAL)
 label(d,(233,183),'ASSINATURA',17,GOLD,'mm');label(d,(568,183),'COMEMORAÇÃO',17,TEAL,'mm')
 arrow(d,(353,294),(447,294),WHITE,3)
 label(d,(395,433),'DOIS REGISTROS • DUAS FUNÇÕES',14,WHITE,'mm');note(d)
def gift_question(d,t):
 gift(d,250,327,147,t);calendar(d,539,300,168,'OUTUBRO',12,color=TEAL)
 label(d,(398,170),'QUEM ESCOLHEU ESSA DATA?',20,GOLD,'mm')
 circle(d,423,272,33,'#19394a',GOLD,2);label(d,(423,271),'?',36,GOLD,'mm');note(d)
def proposal(d,t):
 events=[('PROPOSTA','Galdino do\nValle Filho'),('APROVAÇÃO','Congresso\nNacional'),('1924','Artur\nBernardes')];timeline(d,events,t)
 note(d,'Processo resumido conforme registro da Câmara')
def paper_people(d,t,kind):
 book(d,168,291,106,132,'DATA',GOLD)
 for k,(x,head,c) in enumerate([(379,'ESCOLA',TEAL),(614,'FAMÍLIAS',CORAL)]):
  if k==0:book(d,x,284,99,126,None,c)
  else:
   for j in range(3):child(d,x-46+j*43,262,'#bc8b61' if j%2==0 else '#f0c9a3',c,t+j,.8)
  label(d,(x,401),head,16,c,'mm')
 arrow(d,(237,307),(312,307),TEAL,3);arrow(d,(443,307),(501,307),CORAL,3)
 label(d,(397,171),'A DATA CIRCULA EM DIFERENTES ESPAÇOS',16,GOLD,'mm');note(d)
def toy_scene(d,t,kind):
 if kind=='company_timeline':timeline(d,[('1924','Data oficial\nbrasileira'),('1937','Fundação\nda Estrela')],t,left=231,right=565);note(d,'Linha do tempo ilustrada • posições não representam escala temporal');return
 if kind=='materials_reveal':
  for x,word,c in [(200,'PANO',CORAL),(396,'MADEIRA',GOLD),(593,'PLÁSTICO',TEAL)]:
   d.rounded_rectangle((x-77,217,x+77,362),radius=12,fill='#214356',outline=c,width=3)
   if word=='PANO':child(d,x,254,'#d5a77b',CORAL,t,.75)
   elif word=='MADEIRA':blocks(d,x-45,306,t)
   else:ball(d,x,288,38,t)
   label(d,(x,398),word,16,c,'mm')
  note(d,'Objetos genéricos • não são modelos de produtos de uma marca');return
 # An original illustrated storefront, distinct from a real campaign advertisement.
 d.rounded_rectangle((115,190,683,419),radius=8,fill='#183b48',outline=GOLD,width=3)
 for xx in range(135,679,77):d.polygon([(xx,190),(xx+66,190),(xx+64,230),(xx+3,230)],fill=CORAL if ((xx-135)//77)%2 else TEAL)
 label(d,(397,163),'MEADOS DO SÉCULO XX',17,GOLD,'mm')
 if kind=='campaign_board':label(d,(397,253),'CAMPANHAS DE BRINQUEDOS',17,TEAL,'mm')
 gift(d,212,342,90,t);blocks(d,341,386,t);ball(d,600,349,32,t)
 note(d,'Vitrine reconstituída; sem reprodução de anúncio original')
def commercial(d,t,kind):
 if kind=='gift_chain':
  for k,x in enumerate([190,395,600]):gift(d,x,295+5*math.sin(t*.6+k),100,t+k)
  label(d,(395,406),'LEMBRANÇA • PRESENTE • MEMÓRIA',17,GOLD,'mm')
 else:
  for box,head,lines,c in [((80,198,268,365),'ANÚNCIO',['Data aparece'],GOLD),((299,198,488,365),'LEMBRANÇA',['Família recorda'],TEAL),((519,198,708,365),'COSTUME',['Festa e presente'],CORAL)]:card(d,box,head,lines,c)
  arrow(d,(273,281),(291,281),GOLD,2);arrow(d,(493,281),(512,281),TEAL,2)
  label(d,(395,421),'Um processo ilustrado, com experiências diferentes',14,WHITE,'mm')
 note(d)
def play_options(d,t,kind):
 for k,(x,title,c) in enumerate([(190,'JOGOS',TEAL),(397,'HISTÓRIAS',GOLD),(604,'ENCONTROS',CORAL)]):
  d.rounded_rectangle((x-86,203,x+86,368),radius=11,fill='#193d4e',outline=c,width=3)
  if k==0:ball(d,x,279,34,t)
  elif k==1:book(d,x,282,92,108,None,c)
  else:
   child(d,x-28,255,'#bd845e',TEAL,t,.7);child(d,x+33,255,'#edc2a1',CORAL,t+1,.7)
  label(d,(x,405),title,16,c,'mm')
 note(d,'Possibilidades de celebração • nenhuma é uma regra universal')
def gift_custom(d,t):
 book(d,244,282,137,162,'1924',GOLD);gift(d,559,301,139,t)
 label(d,(244,412),'DATA OFICIAL',17,GOLD,'mm');label(d,(560,412),'COSTUME',17,TEAL,'mm');note(d)
def holiday(d,t,kind):
 calendar(d,397,242,131,'OUTUBRO',12,color=TEAL)
 card(d,(79,331,371,432),'DIA DAS CRIANÇAS',['Data brasileira de 1924'],GOLD)
 card(d,(410,331,709,432),'FERIADO NACIONAL',['Nossa Senhora Aparecida'],TEAL)
 if kind=='holiday_1980':label(d,(397,145),'LEI Nº 6.802 • 30/06/1980',20,GOLD,'mm')
 note(d,'Feriado e comemoração: registros com fundamentos diferentes')
def world_dates(d,t,kind):
 if kind=='portugal_calendar':calendar(d,397,289,225,'JUNHO',1,color=GOLD);label(d,(397,425),'PORTUGAL',21,GOLD,'mm');note(d,'Registro da celebração em Portugal');return
 if kind=='november_calendar':calendar(d,397,290,220,'NOVEMBRO',20,color=TEAL);note(d,'Dia Mundial da Criança • ONU/UNICEF');return
 for x,month,day,title,c in [(184,'OUTUBRO',12,'BRASIL',GOLD),(395,'JUNHO',1,'PORTUGAL',CORAL),(606,'NOVEMBRO',20,'ONU / UNICEF',TEAL)]:
  calendar(d,x,290,161,month,day,color=c);label(d,(x,409),title,15,c,'mm')
 note(d,'Diferentes observâncias; datas não são iguais em todos os países')
def international(d,t,kind):
 if kind=='worldrights_timeline':timeline(d,[('1959','Declaração\ndos direitos'),('1989','Convenção\ndos direitos')],t,left=238,right=558);note(d,'Linha do tempo ilustrada • posições não representam escala temporal');return
 for x,year,word,c in [(239,1959,'DECLARAÇÃO',GOLD),(556,1989,'CONVENÇÃO',TEAL)]:
  book(d,x,295,167,178,str(year),c);label(d,(x,415),word,16,c,'mm')
 label(d,(398,159),'20 DE NOVEMBRO',20,WHITE,'mm');note(d,'Adoções pela Assembleia Geral da ONU')
def rights(d,t,kind):
 words=[('EDUCAÇÃO',GOLD),('SAÚDE',CORAL),('PROTEÇÃO',TEAL),('BRINCADEIRA',BLUE)]
 for k,(word,c) in enumerate(words):
  x=224+(k%2)*338;y=224+(k//2)*152
  d.rounded_rectangle((x-137,y-59,x+137,y+59),radius=12,fill='#1b3d4e',outline=c,width=3)
  label(d,(x,y+23),word,18,c,'mm')
  if k==0:book(d,x,y-18,54,49,None,c)
  elif k==1:circle(d,x,y-18,22,c);d.line((x-12,y-18,x+12,y-18),fill=NAVY,width=4);d.line((x,y-30,x,y-6),fill=NAVY,width=4)
  elif k==2:
   d.polygon([(x-25,y-38),(x+25,y-38),(x+20,y-5),(x,y+4),(x-20,y-5)],fill=c,outline=WHITE)
  else:ball(d,x,y-18,22,t)
 note(d,'Ícones ilustrativos • direitos não são presentes ou recompensas')
def playing(d,t,kind):
 child(d,170,298,'#cc956e',TEAL,t,1.13);child(d,620,290,'#f0c7a8',CORAL,t+1,1.1)
 shape='house' if int(t/4)%2==0 else 'bridge';blocks(d,316 if shape=='house' else 274,347,t,shape)
 label(d,(397,176),'MESMOS BLOCOS • NOVAS IDEIAS',17,GOLD,'mm');note(d,'Brincadeira inventada para a cena; personagens simbólicos')
def brazil_rights(d,t,kind):
 if kind=='rights_book':
  book(d,396,292,247,219,'INFÂNCIA\nDIREITOS',TEAL);note(d,'Constituição de 1988 e Estatuto de 1990');return
 timeline(d,[('1988','Constituição\nFederal'),('1990','Estatuto da Criança\ne do Adolescente')],t,left=238,right=563)
 note(d,'Marcos da proteção e do reconhecimento de direitos no Brasil')
def listen(d,t):
 for k,(x,y) in enumerate([(180,251),(390,291),(611,244)]):
  child(d,x,y,['#c18b61','#f2c6a4','#966448'][k],[TEAL,CORAL,GOLD][k],t+k,1.05)
  d.rounded_rectangle((x-55,y-96,x+56,y-45),radius=13,fill='#214655',outline=[TEAL,CORAL,GOLD][k],width=2)
  for j in range(3):circle(d,x-19+j*18,y-70,3,WHITE)
 label(d,(398,429),'ESCUTAR • PARTICIPAR • COMPARTILHAR',15,TEAL,'mm');note(d,'Uma roda de ideias representada por personagens simbólicos')
def variety(d,t):
 for k,x in enumerate([170,396,626]):
  child(d,x,254,['#ae7752','#dfb48d','#f0c9aa'][k],[TEAL,GOLD,CORAL][k],t+k,1.1)
  if k==0:ball(d,x+13,365,22,t)
  elif k==1:book(d,x+1,368,58,58,None,GOLD)
  else:
   d.polygon([(x+10,356),(x+35,332),(x+61,356),(x+35,382)],fill=CORAL,outline=GOLD)
   d.line((x+35,382,x+18,426),fill=WHITE,width=1)
 label(d,(398,177),'BRINCADEIRAS E EXPERIÊNCIAS',18,GOLD,'mm');note(d,'Exemplos ilustrados; nenhuma infância é reduzida a estes exemplos')
def year_round(d,t,kind):
 for k in range(12):
  x=105+(k%4)*163;y=181+(k//4)*85;c=GOLD if k==9 else TEAL
  d.rounded_rectangle((x,y,x+135,y+65),radius=6,fill='#1c3c4d',outline=c,width=2)
  label(d,(x+67,y+20),['JAN','FEV','MAR','ABR','MAI','JUN','JUL','AGO','SET','OUT','NOV','DEZ'][k],14,c,'mm')
  if k==9:label(d,(x+67,y+46),'12',20,GOLD,'mm')
  else:
   for j in range(3):circle(d,x+38+j*28,y+44,2,WHITE)
 active=int(t*1.2)%12;xx=105+(active%4)*163;yy=181+(active//4)*85
 d.rounded_rectangle((xx-4,yy-4,xx+139,yy+69),radius=8,outline=WHITE,width=2)
 note(d,'A data ocupa um dia; a atenção à infância percorre o ano')
def care(d,t):
 for x,word,c in [(181,'ESCUTAR',TEAL),(396,'APRENDER',GOLD),(610,'BRINCAR',CORAL)]:
  card(d,(x-96,217,x+96,361),word,[],c)
  if word=='ESCUTAR':
   for j in range(3):circle(d,x-25+j*25,308,4,WHITE)
  elif word=='APRENDER':book(d,x,310,61,57,None,c)
  else:ball(d,x,307,26,t)
 label(d,(398,165),'DEPOIS DA FESTA, A VIDA CONTINUA',18,GOLD,'mm');note(d)
def recap_timeline(d,t):
 timeline(d,[('1924','Data\nbrasileira'),('SÉCULO XX','Campanhas\ne costumes'),('HOJE','Comemoração\ne seus sentidos')],t,left=148,right=651)
 note(d,'Resumo editorial • a história dos direitos tem trajetória própria')
def quiz(d,t,kind):
 choices=[('A','A fábrica criou a data'),('B','Feriado e festa têm a mesma origem'),('C','Diferentes histórias se encontraram')]
 for k,(letter,line) in enumerate(choices):
  y=190+k*85;c=TEAL if kind=='quiz_answer' and letter=='C' else '#65828f'
  d.rounded_rectangle((78,y,710,y+65),radius=10,fill='#1b3d4e',outline=c,width=3)
  circle(d,112,y+33,20,c);label(d,(112,y+32),letter,18,NAVY,'mm');label(d,(155,y+32),line,17,WHITE,'lm')
 note(d,'A resposta compara as origens; não compara o valor das celebrações')
def reveal(d,t,kind):
 gift(d,399,354,202,t)
 for k,(x,word,c) in enumerate([(197,'HISTÓRIA',GOLD),(399,'MEMÓRIA',CORAL),(603,'INFÂNCIA',TEAL)]):
  yy=219+8*math.sin(t*.65+k);d.rounded_rectangle((x-88,yy-33,x+88,yy+33),radius=9,fill='#1b3d4e',outline=c,width=2)
  label(d,(x,yy),word,17,c,'mm');arrow(d,(399,314),(x,yy+40),c,2)
 note(d,'Imagem simbólica • uma caixa que abre a investigação')

def pixel_scene(kind,t):
 env='Archive' if kind in ARCHIVE else 'Toyshop' if kind in SHOP else 'Park';im=background(env,t)
 if kind in ['park_end','outro']:
  layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer)
  d.rounded_rectangle((56,111,724,315),radius=12,fill=(5,23,37,227),outline=TEAL,width=2)
  label(d,(392,178),'QUASE INFINITO',34,GOLD,'mm');label(d,(392,244),'Cada pergunta abre outra viagem.',19,WHITE,'mm')
  im.alpha_composite(layer);return im.convert('RGB')
 d=panel(im,TITLES[kind])
 if kind=='gift_question':gift_question(d,t)
 elif kind in ['three_layers','calendar_layers','recap_three']:layers(d,t,kind)
 elif kind in ['archive_arrival','year_1924','decree_seal','decree_card','decree_excerpt']:document(d,t,kind)
 elif kind=='proposal_path':proposal(d,t)
 elif kind in ['two_dates','october_calendar','date_insight']:two_dates(d,t,kind)
 elif kind=='gift_not_required':gift_custom(d,t)
 elif kind in ['paper_to_people','tradition_cycle']:paper_people(d,t,kind)
 elif kind in ['toyshop_arrival','company_timeline','materials_reveal','campaign_board']:toy_scene(d,t,kind)
 elif kind in ['commercial_flow','gift_chain']:commercial(d,t,kind)
 elif kind in ['play_options','gift_and_play']:play_options(d,t,kind)
 elif kind in ['holiday_question','holiday_1980']:holiday(d,t,kind)
 elif kind in ['world_dates','portugal_calendar','november_calendar']:world_dates(d,t,kind)
 elif kind in ['international_pair','worldrights_timeline']:international(d,t,kind)
 elif kind=='rights_cards':rights(d,t,kind)
 elif kind=='play_world':playing(d,t,kind)
 elif kind in ['brazil_rights','timeline_1988_1990','rights_book']:brazil_rights(d,t,kind)
 elif kind=='listen_scene':listen(d,t)
 elif kind=='different_play':variety(d,t)
 elif kind in ['year_round','calendar_loop']:year_round(d,t,kind)
 elif kind=='care_everyday':care(d,t)
 elif kind=='recap_timeline':recap_timeline(d,t)
 elif kind in ['quiz_dates','quiz_answer']:quiz(d,t,kind)
 elif kind in ['box_reveal','childhood_meaning']:reveal(d,t,kind)
 else:raise ValueError('Unknown historical scene '+kind)
 return im.convert('RGB')

def overlay(item,scene,local,global_time,source,pixel):
 im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im)
 d.rounded_rectangle((9,9,W-10,H-10),radius=14,outline=TEAL,width=4);d.rounded_rectangle((16,16,W-17,H-17),radius=11,outline=(255,203,114,168),width=1)
 d.rounded_rectangle((26,25,933,64),radius=7,fill=(5,20,33,226));label(d,(43,44),'QUASE INFINITO',13,GOLD,'lm');label(d,(261,44),item['title'],14,WHITE,'lm')
 if pixel:
  source='Reconstituição ilustrada · Quase Infinito' if scene in ARCHIVE or scene in SHOP else 'Pixel art e animação · Quase Infinito'
 else:
  d.rounded_rectangle((746,75,926,101),radius=5,fill=(5,20,33,218))
  label(d,(916,88),'IMAGEM ATUAL ILUSTRATIVA',10,WHITE,'rm')
 rect(d,(27,493,933,521),(5,20,33,223));label(d,(39,507),source[:94],10,'#c0d9dc','lm')
 action=item['action'];height=196 if scene=='outro' else 185;sprite=pico(action,local,height=height)
 if sprite.width>174:height=round(height*174/sprite.width);sprite=pico(action,local,height=height)
 x=min(W-25-sprite.width,759+3*math.sin(local*.43+item['index']*.6));y=281+8*math.sin(local*.7)
 if action=='flying':y-=25*math.sin(local*.44)
 im.alpha_composite(sprite,(round(x),round(y)))
 d=ImageDraw.Draw(im)
 for k in range(5):circle(d,x+52-k*7,y+sprite.height+13+k*.5,1,GOLD)
 d.line((30,529,30+898*max(0,min(1,global_time/498)),529),fill=GOLD,width=2)
 # No narration text, subtitle cues, or automatic caption layer are drawn.
 return im
