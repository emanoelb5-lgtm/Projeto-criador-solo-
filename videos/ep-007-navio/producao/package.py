"""Package the complete buoyancy episode and all materials needed for publication."""
import argparse,hashlib,json,re,shutil,subprocess,tempfile,wave,zipfile
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parent;OUT=ROOT/'output';PUB=OUT/'publicacao'
VIDEO=OUT/'Quase_Infinito_Navio_1080p.mp4';ZIP=OUT/'Quase_Infinito_Navio_Publicacao.zip'
REPOSITORY='emanoelb5-lgtm/Projeto-criador-solo-';RELATIVE='videos/ep-007-navio'
TITLE='Por que um navio de aço flutua, mas um prego afunda? | Quase Infinito'
SUMMARY='Um cargueiro feito de aço atravessa a água, enquanto um simples prego afunda. O Pico investiga o que muda quando a mesma quantidade de material ganha outra forma.\n\nA viagem passa pela pressão da água, pelo empuxo, pelo espaço protegido dentro do casco e pela carga de um navio. Depois, compara água doce e salgada e descobre como tanques de lastro ajudam um submarino a mergulhar e voltar à superfície.\n\nAnimações originais, novos cenários de pixel art e filmagens reais conduzem as perguntas e respostas, com a voz Thalita e o Pico v2. Os modelos são ilustrados e o exemplo numérico usa valores inventados para explicar a física. Este episódio não tem legendas na tela.\n\nQue pergunta você quer investigar na próxima viagem?\nCada pergunta abre outra viagem.'
TAGS=['por que navio flutua', 'navio de aço', 'por que prego afunda', 'empuxo', 'princípio de Arquimedes', 'densidade', 'água deslocada', 'calado', 'navio cargueiro', 'submarino', 'tanques de lastro', 'água salgada', 'gelo', 'ciência', 'curiosidades', 'Quase Infinito']
CHAPTERS=[(0, 'Um gigante e um prego'), (2, 'Peso, volume e densidade'), (3, 'Os espaços dentro do casco'), (4, 'A pressão debaixo da água'), (6, 'O princípio de Arquimedes'), (8, 'O equilíbrio do navio'), (9, 'Mesmo material, outra forma'), (11, 'O efeito da carga'), (13, 'Quando a água entra'), (15, 'Água doce e salgada'), (17, 'Como um submarino mergulha'), (19, 'E o gelo?'), (21, 'O desafio dos dois barcos'), (23, 'Cada pergunta abre outra viagem')]
FILES=['base_art.py','pixel_art.py','render.py','prepare_voice.py','prepare_media.py','package.py','episode.json','media_requests.json','media_sources.json','research_sources.json','requirements.txt','art_direction.json','quality_editorial.md','FONTES.md']

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,t):p.write_text(t.strip()+'\n',encoding='utf-8')
def dump(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def stamp(s):return f'{int(s)//60:02d}:{int(s)%60:02d}'

def loudness():
    p=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(VIDEO),'-map','0:a:0','-af','ebur128=peak=true','-f','null','-'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
    text=p.stderr.split('Summary:')[-1];values={}
    for key,pattern in [('integrated_loudness_lufs',r'I:\s+([-+\d.]+)\s+LUFS'),('true_peak_dbtp',r'Peak:\s+([-+\d.]+)\s+dBFS'),('loudness_range_lu',r'LRA:\s+([-+\d.]+)\s+LU')]:
        match=re.search(pattern,text)
        if not match:raise RuntimeError('Missing audio measurement '+key)
        values[key]=float(match[1])
    if values['true_peak_dbtp']>-1 or not -20<values['integrated_loudness_lufs']<-11:raise RuntimeError('Audio outside publication targets')
    return values

def freeze_voice(blocks):
    with tempfile.TemporaryDirectory(prefix='quase-infinito-voice-') as work:
        work=Path(work);output=work/'voice.wav';sr=24000
        with wave.open(str(output),'wb') as master:
            master.setnchannels(1);master.setsampwidth(2);master.setframerate(sr)
            for block in blocks:
                segment=work/f'{block["index"]:02d}.wav'
                filt=f'atempo={block["speed"]:.9f},loudnorm=I=-16:TP=-2:LRA=8,aresample={sr},adelay=350,apad,atrim=duration={block["duration"]:.9f}'
                subprocess.run(['ffmpeg','-y','-v','error','-i',str(ROOT/'audio'/f'{block["index"]:02d}.mp3'),'-af',filt,'-ar',str(sr),'-ac','1',str(segment)],check=True)
                with wave.open(str(segment),'rb') as src:
                    expected=block['frames']*sr//24;master.writeframesraw(src.readframes(expected).ljust(expected*2,b'\x00'))
        mp3=work/'Narracao_Thalita.mp3'
        subprocess.run(['ffmpeg','-y','-v','error','-i',str(output),'-c:a','libmp3lame','-b:a','96k',str(mp3)],check=True)
        (PUB/mp3.name).write_bytes(mp3.read_bytes())

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo-root',type=Path,required=True);ap.add_argument('--visual-reviewed',action='store_true');args=ap.parse_args()
    repository=args.repo_root.resolve();ep=repository/RELATIVE;ep.mkdir(parents=True,exist_ok=True);PUB.mkdir(exist_ok=True)
    limit=json.loads((repository/'config/channel.json').read_text())['delivery']['max_video_file_bytes']
    if VIDEO.stat().st_size>=limit:
        (ep/'video.mp4').write_bytes(VIDEO.read_bytes())
        with tempfile.TemporaryDirectory(prefix='quase-infinito-delivery-') as work:
            subprocess.run(['python3',str(repository/'scripts/prepare_delivery.py'),'--episode',str(ep),'--work-dir',work],check=True)
        VIDEO.write_bytes((ep/'video.mp4').read_bytes())
        import render
        _,shots=render.timeline();render.verify(shots);render.previews(shots)
        raise RuntimeError('MP4 recomprimido; revisar visualmente o novo resultado e executar package.py novamente.')
    timeline=json.loads((OUT/'timeline.json').read_text());blocks=timeline['blocks'];report=json.loads((OUT/'verificacao.json').read_text())
    assert report['full_decode']=='passed' and report['sha256']==sha(VIDEO)
    assert report['subtitle_mode']=='none' and report['embedded_subtitle_streams']==0 and not report['burned_in_captions']
    media=json.loads((ROOT/'media_sources.json').read_text());research=json.loads((ROOT/'research_sources.json').read_text())
    unique={x['source']:x for x in media};media=list(unique.values())
    credits='Filmagens e fotografia: '+', '.join(sorted(set(x['author'] for x in media)))+' — Pexels License.\nRoteiro, edição, trilha e animações dos modelos: Quase Infinito.\nNarração sintetizada: Thalita (pt-BR). Pico, cenários e miniatura: geração de imagem por IA.\nDiagramas e experiências ilustrados, sem escala; não são filmagens de experimentos ou medições. Exemplo de dez toneladas: valores inventados e arredondados.'
    chapters=[{'start_seconds':blocks[index]['start'],'title':title} for index,title in CHAPTERS]
    metadata={'episode':7,'channel':'Quase Infinito','repository':REPOSITORY,'title':TITLE,'alternative_titles':['Como um navio de aço consegue flutuar?', 'Um prego afunda. Por que um navio não afunda?'],'summary':SUMMARY,'language':'pt-BR','category_id':'27','category':'Education','tags':TAGS,'hashtags':['#QuaseInfinito','#Curiosidades','#Ciencia'],'voice':'pt-BR-ThalitaMultilingualNeural','duration_seconds':timeline['duration'],'resolution':[1920,1080],'fps':24,'thumbnail':'miniatura.jpg','subtitle_file':'legendas.srt','subtitle_mode':'none','subtitle_file_role':'optional_transcript','burned_in_captions':False,'embedded_subtitle_streams':0,'video_filename':'video.mp4','video_sha256':sha(VIDEO),'chapters':chapters,'sources':[{'name':s['name'],'url':s['url']} for s in research],'credits':credits,'synthetic_content':{'narration':'síntese de voz Thalita','illustrations':'Pico, cenários e miniatura com IA','graphics':'diagramas e animações originais em código','model':'empuxo, casco e lastro ilustrados; exemplo numérico inventado; sem experimento ou medição anunciados'},'mascot_design_version':2,'mascot_design_reference':'producao/assets/Pico_Design_v2_16x9.png','publication_mode':'manual'}
    narration='\n\n'.join(b['text'] for b in blocks);write(PUB/'Narracao.txt',narration)
    write(PUB/'Roteiro.md','# '+TITLE+'\n\n'+'\n\n'.join(f"## {stamp(b['start'])} — {b['title']}\n\n{b['text']}\n\nPlanos: {', '.join(b['scenes'])}. Pesos: {b['weights']}. Pico: {b['action']}." for b in blocks))
    write(PUB/'Capitulos.txt','\n'.join(stamp(c['start_seconds'])+' '+c['title'] for c in chapters));write(PUB/'Creditos.txt',credits)
    reference='# Fontes e procedência — episódio 007\n\nConsulta: 11/10/2026. Roteiro e analogias redigidos para este episódio.\n\n## Pesquisa científica\n\n'
    for s in research:
        reference+='### '+s['name']+'\n\n'+s['url']+'\n\nUsada para: '+', '.join(s['topics'])+'. Blocos: '+', '.join(str(i+1) for i in s['blocks'])+'.\n\nConferência: '+s['verification']+'\n\n'
    reference+='## Mídias reais\n\n'
    for s in media:
        reference+='- '+s['author']+' — '+s['title']+'\n  Origem: '+s['source']+'\n  Licença/uso: '+s['license']+'\n  SHA-256: '+s['sha256']+'\n  Edição: seleção de trechos, enquadramento, movimento de câmera nas fotografias, moldura, Pico e comentário original.\n\n'
    reference+='## Limites e decisões\n\nO empuxo atua também em objetos que afundam. Para um navio em equilíbrio vertical em água tranquila, seu empuxo equilibra seu peso. O corte do casco mostra espaços protegidos da entrada de água; o ar interno não é apresentado como uma força que levanta o barco. A caixa representa pressões hidrostáticas, sem forças numericamente medidas. Dez toneladas e dez metros cúbicos são um exemplo inventado em água doce com densidade arredondada de 1.000 kg/m³. A massa de modelar é uma simulação ilustrada, não um experimento filmado. Alturas na comparação entre água doce e salgada são exageradas e não representam o calado de um navio real. O modelo de estabilidade apenas ilustra inclinação e deslocamento da carga, sem cálculo naval. Os tanques de lastro são um modelo simplificado: o controle real considera também distribuição de massas, movimento e superfícies de controle. Nenhuma ilustração é apresentada como medição, acidente real ou registro de uma experiência. Os icebergs reais são filmagens; o corte abaixo da água é uma ilustração. Todas as cenas finais são 16:9; a fotografia é enquadrada com movimento, mantendo sua procedência. Os rótulos e créditos não transcrevem a narração. A trilha é uma composição procedural original, com variações de intensidade e redução durante a fala. As políticas do YouTube foram consultadas para orientar a qualidade, fora do roteiro falado.\n'
    write(PUB/'Fontes.md',reference);write(ROOT/'FONTES.md',reference)
    thumb_jpg=ROOT.parent/'Thumb_Navio_Quase_Infinito.jpg';thumb_png=ROOT.parent/'Thumb_Navio_Quase_Infinito.png'
    if not thumb_jpg.exists():thumb_jpg=ROOT.parent/'miniatura.jpg'
    if not thumb_png.exists():thumb_png=ROOT.parent/'miniatura.png'
    for source,target in [(OUT/'Transcricao_Navio_Optional.srt','Transcricao_Optional.srt'),(OUT/'timeline.json','Storyboard.json'),(OUT/'Revisao_16x9.jpg','Revisao_16x9.jpg'),(OUT/'verificacao.json','Verificacao.json'),(ROOT/'quality_editorial.md','Decisoes_Editoriais.md'),(thumb_jpg,'Thumb_Navio_Quase_Infinito.jpg'),(thumb_png,'Thumb_Navio_Quase_Infinito.png')]:shutil.copyfile(source,PUB/target)
    technical={'voice':'pt-BR-ThalitaMultilingualNeural','engine':'edge_tts','edge_tts_version':'7.2.8','text_sha256':hashlib.sha256(narration.strip().encode()).hexdigest(),'segments':[]}
    for b in blocks:
        source=ROOT/'audio'/f'{b["index"]:02d}.mp3';timing=json.loads(source.with_suffix('.json').read_text())
        technical['segments'].append({'index':b['index'],'start_seconds':b['start'],'duration_seconds':b['duration'],'tempo_factor':b['speed'],'source_audio_sha256':sha(source),'tts_rate':timing['rate']})
    dump(PUB/'Narracao_Tecnica.json',technical);freeze_voice(blocks)
    for name in ['Thumb_Navio_Quase_Infinito.jpg','Thumb_Navio_Quase_Infinito.png']:
        with Image.open(PUB/name) as im:assert im.size==(1920,1080)
    assert (PUB/'Thumb_Navio_Quase_Infinito.jpg').stat().st_size<2000000
    for source,target in [(VIDEO,'video.mp4'),(PUB/'Thumb_Navio_Quase_Infinito.jpg','miniatura.jpg'),(PUB/'Thumb_Navio_Quase_Infinito.png','miniatura.png'),(PUB/'Transcricao_Optional.srt','legendas.srt'),(PUB/'Narracao.txt','narracao.txt'),(PUB/'Narracao_Tecnica.json','narracao.json'),(PUB/'Roteiro.md','roteiro.md'),(PUB/'Fontes.md','fontes.md'),(PUB/'Capitulos.txt','capitulos.txt'),(PUB/'Creditos.txt','creditos.txt'),(PUB/'Decisoes_Editoriais.md','decisoes-editoriais.md')]:shutil.copyfile(source,ep/target)
    dump(ep/'metadata.json',metadata)
    subprocess.run(['python3',str(repository/'scripts/package_episode.py'),'--episode',str(ep)],check=True)
    metadata=json.loads((ep/'metadata.json').read_text());qa=json.loads((ep/'qa.json').read_text())
    qa.update({'sha256':sha(VIDEO),'video_frames':report['video_frames'],'shots':len(timeline['shots']),'burned_in_captions':False,'mascot_design_version':2,'visual_review':'final decoded MP4 frames inspected: artwork, original diagrams, real sources, no narration captions and ending' if args.visual_reviewed else 'required before publication','research_review':'primary sources checked; simulations distinguished from records; no claim of measurements'})
    qa['audio'].update(loudness());dump(ep/'qa.json',qa);dump(PUB/'QA_Publicacao.json',qa)
    publication={**metadata,'thumbnail':'Thumb_Navio_Quase_Infinito.jpg','subtitle_file':'Transcricao_Optional.srt','video_filename':VIDEO.name};dump(PUB/'Metadata.json',publication)
    write(PUB/'Descricao_YouTube.txt',metadata['description']);write(PUB/'Titulo_YouTube.txt',TITLE);write(PUB/'Titulos_Alternativos.txt','\n'.join(metadata['alternative_titles']))
    write(OUT/'Titulo_YouTube_Navio.txt',TITLE);write(OUT/'Descricao_YouTube_Navio.txt',metadata['description']);write(ep/'titulo.txt',TITLE)
    readme=f'''# Produção do episódio 007

**{TITLE}**

52 planos com durações variáveis, 8min06s, Full HD 1920 × 1080 e 24 fps. Voz Thalita e Pico v2. Este episódio não tem legendas na tela; o SRT separado é uma transcrição opcional. Moldura, créditos e rótulos científicos permanecem.

Três novos cenários de pixel art — porto, oficina e fundo do mar — acompanham modelos originais de pressão, deslocamento de água, forma do casco, carga, inundação e lastro. Há cinco filmagens reais e uma fotografia com movimento. As experiências e o exemplo numérico são ilustrados. Há movimentos de câmera, reflexos, carga, água nos tanques e do Pico. quality_editorial.md registra as escolhas de qualidade. art_direction.json registra os prompts e o modo da geração de imagem.

## Reproduzir

Requer Python 3.12, FFmpeg com libx264, fontes DejaVu, internet e as dependências de requirements.txt. As miniaturas ficam na pasta do episódio. Mídias brutas e cache ficam fora do histórico Git. Os segmentos de voz congelados e a voz completa sem trilha estão no ZIP.

    python -m pip install -r {RELATIVE}/producao/requirements.txt
    python {RELATIVE}/producao/prepare_media.py
    python {RELATIVE}/producao/prepare_voice.py
    python {RELATIVE}/producao/render.py --workers 4
    python {RELATIVE}/producao/package.py --repo-root . --visual-reviewed

Antes do último comando, inspecione os quadros finais. Os MP4 são fechados e validados em arquivos temporários antes de copiar os bytes completos. O validador geral confere voz, formato, duração, transcrição, miniatura, capítulos e decodificação integral. A opção de revisão visual só deve ser usada depois da inspeção real.

FONTES.md documenta os limites dos modelos e a procedência dos materiais. Regenerar a voz ou baixar mídias alteradas pelo provedor pode mudar o resultado. Emanuel faz a publicação manual no YouTube.

[Publicação](../PUBLICAR.md) · [Fontes](../fontes.md) · [Verificação](../qa.json)
'''
    production=ep/'producao';production.mkdir(exist_ok=True);project=PUB/'Projeto_Producao';project.mkdir(exist_ok=True)
    for destination in [production,project]:
        write(destination/'README.md',readme)
        for name in FILES:
            if (destination/name).resolve()!=(ROOT/name).resolve():shutil.copyfile(ROOT/name,destination/name)
        shutil.copytree(ROOT/'assets',destination/'assets',dirs_exist_ok=True)
    shutil.copytree(ROOT/'audio',project/'audio',dirs_exist_ok=True)
    write(PUB/'Leia_primeiro.txt',f'''QUASE INFINITO — EPISÓDIO 007
{TITLE}

Vídeo final: {VIDEO.name}, entregue separadamente do ZIP.
8min06s · 1920 × 1080 · 16:9 · 24 fps · Thalita · Pico v2.

1. Envie o MP4 final ao YouTube Studio.
2. Copie Titulo_YouTube.txt e Descricao_YouTube.txt.
3. Use Thumb_Navio_Quase_Infinito.jpg como miniatura.
4. Este episódio não usa legendas na tela. O SRT está disponível apenas como transcrição opcional.
5. Metadata.json inclui tags, idioma, categoria sugerida, capítulos, fontes e créditos.
6. Defina público, visibilidade e horário no seu canal.

O pacote inclui título, descrição, alternativas, capítulos, roteiro, texto falado, créditos, fontes, transcrição opcional, miniatura PNG/JPG, narração completa sem trilha, segmentos originais de voz, Pico v2 em seis poses na folha de referência, novos cenários, prompts, código e relatórios de revisão. Os rótulos de diagramas e os créditos não são legendas de narração.

SHA-256 do MP4: {sha(VIDEO)}
Decodificação integral: aprovada. Faixas de legenda embutida: zero.
''')
    files=sorted(p for p in PUB.rglob('*') if p.is_file() and p.name!='Checksums.sha256');write(PUB/'Checksums.sha256',sha(VIDEO)+'  '+VIDEO.name+'\n'+'\n'.join(sha(p)+'  '+p.relative_to(PUB).as_posix() for p in files))
    with tempfile.TemporaryDirectory(prefix='quase-infinito-package-') as work:
        archive=Path(work)/'publicacao.zip'
        with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            for p in sorted(PUB.rglob('*')):
                if p.is_file():z.write(p,'Quase_Infinito_Navio/'+p.relative_to(PUB).as_posix())
        with zipfile.ZipFile(archive) as z:assert z.testzip() is None
        ZIP.write_bytes(archive.read_bytes())
    if ZIP.stat().st_size>=30000000:raise RuntimeError('Package above native API blob limit; review duplicate assets before delivery')
    shutil.copyfile(ZIP,ep/'publicacao.zip')
    write(ep/'PUBLICAR.md',f'''# Pronto para publicar — episódio 007

**{TITLE}**

8min06s · Full HD · 16:9 · 24 fps · voz Thalita · Pico v2 · sem legendas na tela

![Miniatura](miniatura.jpg)

- [Baixar vídeo completo](https://raw.githubusercontent.com/{REPOSITORY}/main/{RELATIVE}/video.mp4)
- [Baixar pacote de publicação](https://raw.githubusercontent.com/{REPOSITORY}/main/{RELATIVE}/publicacao.zip)
- [Miniatura JPG](miniatura.jpg) · [Miniatura PNG](miniatura.png)
- [Título](titulo.txt) · [Descrição com capítulos e créditos](descricao.txt)
- [Transcrição opcional](legendas.srt) · [Metadados](metadata.json)

Envie o MP4 ao YouTube Studio, copie título e descrição e use a miniatura JPG. O vídeo contém somente vídeo e áudio e não usa legendas na tela. O SRT separado é uma transcrição opcional. Defina público, visibilidade e horário no seu canal.

O ZIP reúne os materiais de publicação, a voz sem trilha, os segmentos de narração, os cenários, o Pico v2, os prompts e o projeto de edição. As orientações do YouTube foram usadas nas decisões de qualidade; o episódio responde por que um navio de aço flutua e um prego afunda. Emanuel faz a publicação manual.

[Verificação](qa.json) · [Roteiro](roteiro.md) · [Fontes](fontes.md) · [Decisões editoriais](decisoes-editoriais.md) · [Produção](producao/README.md)

SHA-256 do MP4: {sha(VIDEO)}
''')
    files=sorted(p for p in ep.rglob('*') if p.is_file() and p.name!='checksums.sha256');write(ep/'checksums.sha256','\n'.join(sha(p)+'  '+p.relative_to(ep).as_posix() for p in files))
    result={'video':str(VIDEO),'zip':str(ZIP),'thumbnail':str(PUB/'Thumb_Navio_Quase_Infinito.jpg'),'title':str(OUT/'Titulo_YouTube_Navio.txt'),'description':str(OUT/'Descricao_YouTube_Navio.txt'),'duration_seconds':report['duration_seconds'],'subtitle_mode':'none','description_characters':len(metadata['description']),'video_sha256':sha(VIDEO),'zip_sha256':sha(ZIP),'audio':qa['audio'],'repo_episode':str(ep)}
    dump(OUT/'delivery.json',result);print(json.dumps(result,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
