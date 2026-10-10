"""Prepare publication files from the verified final timeline and video."""
import hashlib,json,shutil,subprocess,zipfile
from pathlib import Path
from PIL import Image
import pixel_art as art

ROOT=Path(__file__).resolve().parent;OUT=ROOT/'output';PUB=OUT/'publicacao'
VIDEO=OUT/'Quase_Infinito_24_Horas_1080p.mp4'
TITLE='Quem decidiu que o dia tem 24 horas? | Quase Infinito'
ZIP=OUT/'Quase_Infinito_24_Horas_Publicacao.zip'

def write(name,text):(PUB/name).write_text(text.strip()+'\n',encoding='utf-8')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def mmss(s):
    q=int(s);return f'{q//60:02d}:{q%60:02d}'
def resource(name,repo_name):
    p=ROOT/name;return p if p.exists() else ROOT.parent/repo_name

def main():
    PUB.mkdir(exist_ok=True)
    t=json.loads((OUT/'timeline.json').read_text());blocks=t['blocks'];sources=json.loads((ROOT/'media_sources.json').read_text());qa=json.loads((OUT/'verificacao.json').read_text())
    assert qa['full_decode']=='passed' and qa['sha256']==sha(VIDEO)
    assert qa['subtitle_mode']=='burned_in' and qa['embedded_subtitle_streams']==0
    chapters=[(0,'Quem escolheu 24 horas?'),(3,'O Egito e as doze partes'),(5,'Sombras, estrelas e água'),(8,'Por que sessenta?'),(10,'Engrenagens e pêndulos'),(12,'Trens e horários compartilhados'),(14,'Uma volta não é o mesmo que um dia solar'),(17,'O ritmo do quartzo'),(18,'Relógios atômicos e o segundo'),(20,'O tempo por trás do GPS'),(21,'Quem decidiu, afinal?'),(22,'Cada pergunta abre outra viagem')]
    chaptertext='\n'.join(mmss(blocks[i]['start'])+' '+label for i,label in chapters)
    credittext='\n\n'.join(f"{s['key']} — {s['title']}\nAutor/crédito: {s['author']}\nOrigem: {s['source']}\nLicença: {s['license']}\nTratamento: trecho editado, enquadramento 16:9, moldura e animações; fotos com movimento de aproximação." for s in sources)
    sourceurls=[('Royal Museums Greenwich: divisão do dia','https://www.rmg.co.uk/stories/time/why-12-months-year-seven-days-week-or-60-minutes-hour'),('NIST: primeiros relógios','https://www.nist.gov/pml/time-and-frequency-division/popular-links/walk-through-time/walk-through-time-early-clocks'),('NASA: dia solar e sideral','https://science.nasa.gov/learn/basics-of-space-flight/chapter2-1/'),('NIST: definição do segundo','https://doi.org/10.6028/jres.122.029'),('NASA/JPL: relógios atômicos e GPS','https://www.jpl.nasa.gov/news/five-things-to-know-about-nasas-deep-space-atomic-clock/')]
    description='''Por que o dia tem 24 horas? Essa conta nasceu no céu ou foi uma escolha nossa?

Neste episódio do Quase Infinito, o Pico acompanha uma viagem dos relógios de sombra aos átomos. Descubra as horas do Egito antigo, a herança do número 60, o papel dos trens na coordenação dos horários e por que uma volta da Terra em relação às estrelas leva cerca de 23 horas e 56 minutos.

Uma pergunta simples revela milhares de anos de história escondidos no seu despertador.

Que outro detalhe da sua rotina esconde uma história assim? Conte nos comentários e inscreva-se no Quase Infinito.
Cada pergunta abre outra viagem.

CAPÍTULOS
'''+chaptertext+'\n\nFONTES PRINCIPAIS\n'+'\n'.join(label+'\n'+url for label,url in sourceurls)+'\n\nIMAGENS E FILMAGENS\n'+'\n'.join(s['author']+' — '+s['source'] for s in sources)+'''

Filmagens: Pexels, utilizadas sob a Pexels License.
Fotos de objetos: The Met, Open Access / domínio público.
Foto do relógio NIST-F2: NIST, 2014.
Roteiro, trilha instrumental, moldura e pixel art: produção original do Quase Infinito.
Narração: Thalita, em português brasileiro. Miniatura: ilustração gerada por IA.
Diagramas são esquemáticos; valores de duração são aproximados quando indicados.

#QuaseInfinito #Curiosidades #HistoriaDoTempo
'''
    assert len(description)<=5000,len(description)
    write('Titulo_YouTube.txt',TITLE)
    write('Titulos_Alternativos.txt','1. Por que o dia tem 24 horas? A história escondida no relógio\n2. 24 horas: dos relógios de sombra aos átomos')
    write('Descricao_YouTube.txt',description);write('Capitulos.txt',chaptertext);write('Creditos.txt',credittext)
    write('Narracao.txt','\n\n'.join(b['text'] for b in blocks))
    write('Roteiro.md','# '+TITLE+'\n\n'+'\n\n'.join(f"## {mmss(b['start'])} — {b['title']}\n\n{b['text']}\n\nCenas: {', '.join(b['scenes'])}. Pico: {b['action']}." for b in blocks))
    for src,name in [(OUT/'Legendas_24_Horas.srt','Legendas_24_Horas.srt'),(resource('FONTES.md','fontes.md'),'Fontes.md'),(ROOT/'media_sources.json','media_sources.json'),(OUT/'verificacao.json','Verificacao.json'),(OUT/'timeline.json','Storyboard.json'),(OUT/'Revisao_16x9.jpg','Revisao_16x9.jpg'),(resource('Thumb_24_Horas_Quase_Infinito.jpg','miniatura.jpg'),'Thumb_24_Horas_Quase_Infinito.jpg'),(resource('Thumb_24_Horas_Quase_Infinito.png','miniatura.png'),'Thumb_24_Horas_Quase_Infinito.png')]:shutil.copyfile(src,PUB/name)
    tags=['por que o dia tem 24 horas','24 horas','história do relógio','história do tempo','dia solar','dia sideral','Egito antigo','relógio de água','relógio atômico','quartzo','GPS','ciência','curiosidades','Pico','Quase Infinito']
    metadata={'episode':2,'channel':'Quase Infinito','repository':'emanoelb5-lgtm/Projeto-criador-solo-','title':TITLE,'description':description,'language':'pt-BR','category_id':'27','category':'Education','tags':tags,'hashtags':['QuaseInfinito','Curiosidades','HistoriaDoTempo'],'voice':'pt-BR-ThalitaMultilingualNeural','duration_seconds':qa['duration_seconds'],'resolution':qa['resolution'],'fps':qa['fps'],'thumbnail':'Thumb_24_Horas_Quase_Infinito.jpg','subtitle_file':'Legendas_24_Horas.srt','video_filename':VIDEO.name,'video_sha256':qa['sha256'],'chapters':[{'start_seconds':blocks[i]['start'],'title':label} for i,label in chapters],'synthetic_content':{'narration':'síntese de voz Thalita','thumbnail':'ilustração gerada por IA','graphics':'animações e diagramas originais'},'publishing':'Publicação manual por Emanuel; audiência, visibilidade e agendamento são definidos no envio.'}
    write('Metadata.json',json.dumps(metadata,ensure_ascii=False,indent=2))
    technical={'voice':'pt-BR-ThalitaMultilingualNeural','engine':'edge_tts','text_sha256':sha(PUB/'Narracao.txt'),'segments':[{'index':b['index'],'start_seconds':b['start'],'duration_seconds':b['duration'],'tempo_factor':b['speed'],'source_audio_sha256':sha(ROOT/'audio'/f"{b['index']:02d}.mp3"),'tts_rate':json.loads((ROOT/'audio'/f"{b['index']:02d}.json").read_text())['rate']} for b in blocks]}
    technical['text_sha256']=hashlib.sha256((PUB/'Narracao.txt').read_text().strip().encode()).hexdigest()
    write('Narracao_Tecnica.json',json.dumps(technical,ensure_ascii=False,indent=2))
    for action in ['wave','question','clock','point']:
        im=Image.new('RGBA',(1920,1080));spr=art.pico(action,1,'clock');spr=spr.resize((384,480),Image.Resampling.NEAREST);im.alpha_composite(spr,(768,300));im.save(PUB/f'Pico_{action}_16x9.png')
    write('Leia_primeiro.txt',f'''QUASE INFINITO — EPISÓDIO 002
{TITLE}

Vídeo final: {VIDEO.name} (entregue separadamente deste ZIP).
Duração: 8min24s. Full HD 1920 × 1080, 16:9, 24 fps.
Narração: a mesma voz Thalita aprovada no episódio anterior.

PARA PUBLICAR
1. Envie o MP4 final ao YouTube.
2. Copie Titulo_YouTube.txt e Descricao_YouTube.txt nos campos correspondentes.
3. Envie Thumb_24_Horas_Quase_Infinito.jpg como miniatura.
4. As legendas já estão fixas nas imagens do vídeo. O MP4 não contém uma segunda faixa de legenda. Guarde Legendas_24_Horas.srt como transcrição; ativar uma faixa adicional pode duplicar o texto na tela.
5. Metadata.json reúne tags, idioma, categoria sugerida e capítulos.
6. Defina público, visibilidade e horário na tela de envio do canal.

O pacote inclui roteiro, texto da narração, fontes, créditos, storyboard, miniatura PNG, sprites do Pico e verificação técnica. A trilha, as animações e a narração já estão no MP4. Nenhuma publicação no YouTube é feita por este pacote.

INTEGRIDADE
MP4: {qa['bytes']} bytes
SHA-256: {qa['sha256']}
Verificacao.json registra a decodificação integral aprovada.
''')
    for name in ['Thumb_24_Horas_Quase_Infinito.jpg','Thumb_24_Horas_Quase_Infinito.png']:
        with Image.open(PUB/name) as im:assert im.size==(1920,1080)
    assert (PUB/'Thumb_24_Horas_Quase_Infinito.jpg').stat().st_size<2000000
    sums=[sha(VIDEO)+'  '+VIDEO.name]+[sha(p)+'  '+p.name for p in sorted(PUB.iterdir()) if p.name!='Checksums.sha256']
    write('Checksums.sha256','\n'.join(sums))
    with zipfile.ZipFile(ZIP,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(PUB.iterdir()):z.write(p,'Quase_Infinito_24_Horas/'+p.name)
    with zipfile.ZipFile(ZIP) as z:assert z.testzip() is None
    print(json.dumps({'video':str(VIDEO),'zip':str(ZIP),'zip_bytes':ZIP.stat().st_size,'description_characters':len(description),'publication_files':len(list(PUB.iterdir()))},ensure_ascii=False),flush=True)
if __name__=='__main__':main()

