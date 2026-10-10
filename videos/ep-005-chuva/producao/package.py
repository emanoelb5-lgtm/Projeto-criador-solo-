"""Package the verified rain episode, publication materials and improved pixel-art assets."""
import argparse,hashlib,json,re,shutil,subprocess,tempfile,wave,zipfile
from pathlib import Path
from PIL import Image
import pixel_art as art

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output';PUB=OUT/'publicacao'
VIDEO=OUT/'Quase_Infinito_Chuva_1080p.mp4';ZIP=OUT/'Quase_Infinito_Chuva_Publicacao.zip'
TITLE='Por que a chuva tem cheiro? | Quase Infinito'
REPOSITORY='emanoelb5-lgtm/Projeto-criador-solo-';RELATIVE='videos/ep-005-chuva'
CHAPTERS=[(0,'O perfume que aparece do nada'),(2,'A água encontra o ambiente'),(3,'O que é petricor?'),(5,'A fábrica viva da geosmina'),(7,'Como o cheiro chega até nós?'),(9,'Bolhas dentro de uma gota'),(10,'Aerossóis e movimento do ar'),(11,'Mais chuva é mais perfume?'),(13,'Cheiro antes da chuva local'),(15,'Colêmbolos e sinais do solo'),(20,'Observe a próxima chuva'),(22,'Cada pergunta abre outra viagem')]
TAGS=['por que a chuva tem cheiro','cheiro de chuva','terra molhada','petricor','geosmina','aerossóis','gotas de chuva','microrganismos do solo','Streptomyces','colêmbolos','natureza','ciência','curiosidades','Pico','Quase Infinito']
SUMMARY='Caem as primeiras gotas e aparece aquele cheiro de terra molhada. Mas o perfume veio das nuvens ou já estava no chão?\n\nNo Quase Infinito, o Pico segue três pistas: o solo, uma gota e o ar. A viagem passa pelo petricor, pela geosmina, por bolhas minúsculas e pelos sinais químicos que conectam seres vivos no solo.\n\nO episódio traz filmagens reais, fotografias com movimento, cenários de pixel art mais detalhados e o novo design do Pico. A narração mantém a voz Thalita.\n\nQual lugar tem o cheiro de chuva mais marcante para você? Conte nos comentários e acompanhe a próxima pista.\nCada pergunta abre outra viagem.'
PRODUCTION_FILES=['base_art.py','pixel_art.py','render.py','prepare_voice.py','prepare_media.py','package.py','episode.json','media_requests.json','media_sources.json','research_sources.json','requirements.txt','FONTES.md','thumbnail_prompt.txt','art_direction.json','pico_prompt.txt']
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path,text):path.write_text(text.strip()+'\n',encoding='utf-8')
def dump(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def stamp(seconds):
    q=int(seconds);return f'{q//60:02d}:{q%60:02d}'
def loudness():
    p=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(VIDEO),'-map','0:a:0','-af','ebur128=peak=true','-f','null','-'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
    text=p.stderr.split('Summary:')[-1];values={}
    for key,pattern in [('integrated_loudness_lufs',r'I:\s+([-+\d.]+)\s+LUFS'),('true_peak_dbtp',r'Peak:\s+([-+\d.]+)\s+dBFS'),('loudness_range_lu',r'LRA:\s+([-+\d.]+)\s+LU')]:
        m=re.search(pattern,text)
        if not m:raise RuntimeError('Missing audio measurement '+key)
        values[key]=float(m[1])
    if values['true_peak_dbtp']>-1 or not -20<values['integrated_loudness_lufs']<-11:raise RuntimeError('Audio outside publication targets')
    return values
def frozen_voice(blocks):
    """Freeze the complete approved voice with exactly the video timing, without music."""
    with tempfile.TemporaryDirectory(prefix='quase-infinito-voice-') as work:
        work=Path(work);output=work/'Narracao.wav';sr=24000
        with wave.open(str(output),'wb') as master:
            master.setnchannels(1);master.setsampwidth(2);master.setframerate(sr)
            for b in blocks:
                segment=work/f'{b["index"]:02d}.wav'
                filt=f'atempo={b["speed"]:.9f},loudnorm=I=-16:TP=-2:LRA=8,aresample={sr},adelay=350,apad,atrim=duration={b["duration"]:.9f}'
                subprocess.run(['ffmpeg','-y','-v','error','-i',str(ROOT/'audio'/f'{b["index"]:02d}.mp3'),'-af',filt,'-ar',str(sr),'-ac','1',str(segment)],check=True)
                with wave.open(str(segment),'rb') as src:
                    expected=b['frames']*sr//24;data=src.readframes(expected)
                    data=data.ljust(expected*2,b'\x00');master.writeframesraw(data)
        mp3=work/'Narracao_Thalita.mp3'
        subprocess.run(['ffmpeg','-y','-v','error','-i',str(output),'-c:a','libmp3lame','-b:a','96k',str(mp3)],check=True)
        (PUB/mp3.name).write_bytes(mp3.read_bytes())
    return PUB/'Narracao_Thalita.mp3'
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--repo-root',type=Path,default=ROOT.parents[2]);parser.add_argument('--visual-reviewed',action='store_true');args=parser.parse_args()
    repository=args.repo_root.resolve();ep=repository/RELATIVE;ep.mkdir(parents=True,exist_ok=True);PUB.mkdir(exist_ok=True)
    config=json.loads((repository/'config/channel.json').read_text())
    limit=config['delivery']['max_video_file_bytes']
    if VIDEO.stat().st_size>=limit:
        (ep/'video.mp4').write_bytes(VIDEO.read_bytes())
        with tempfile.TemporaryDirectory(prefix='quase-infinito-delivery-') as work:
            subprocess.run(['python3',str(repository/'scripts/prepare_delivery.py'),'--episode',str(ep),'--work-dir',work],check=True)
        VIDEO.write_bytes((ep/'video.mp4').read_bytes())
        import render
        _,shots=render.timeline();render.verify(shots);render.previews(shots)
    timeline=json.loads((OUT/'timeline.json').read_text());blocks=timeline['blocks'];qa_render=json.loads((OUT/'verificacao.json').read_text())
    assert qa_render['full_decode']=='passed' and qa_render['sha256']==sha(VIDEO)
    assert qa_render['subtitle_mode']=='burned_in' and qa_render['embedded_subtitle_streams']==0
    media=json.loads((ROOT/'media_sources.json').read_text());sources=json.loads((ROOT/'research_sources.json').read_text())
    credits='\n'.join(x['author']+' — '+x['source'] for x in media)
    credits+='\n\nFilmagens e fotografias: Pexels License.\nRoteiro, montagem, trilha, ambiente de chuva e diagramas: Quase Infinito.\nNarração sintetizada: Thalita (pt-BR).\nPico v2, cenários e miniatura: ilustrações criadas com geração de imagem por IA. Chuva, câmera, partículas e movimentos foram animados na montagem.\nEsquemas científicos ampliados e desacelerados, sem escala; cenários subterrâneos são ilustrações, não registros microscópicos.'
    chapter_data=[{'start_seconds':blocks[i]['start'],'title':text} for i,text in CHAPTERS]
    metadata={'episode':5,'channel':'Quase Infinito','repository':REPOSITORY,'title':TITLE,
      'alternative_titles':['Por que a terra fica cheirosa quando chove?','O segredo do cheiro de chuva está no chão'],
      'summary':SUMMARY,'language':'pt-BR','category_id':'27','category':'Education','tags':TAGS,
      'hashtags':['#QuaseInfinito','#Curiosidades','#Natureza'],'voice':'pt-BR-ThalitaMultilingualNeural',
      'duration_seconds':timeline['duration'],'resolution':[1920,1080],'fps':24,
      'thumbnail':'miniatura.jpg','subtitle_file':'legendas.srt','subtitle_mode':'burned_in','embedded_subtitle_streams':0,
      'video_filename':'video.mp4','video_sha256':qa_render['sha256'],'chapters':chapter_data,
      'sources':[{'name':s['name'],'url':s['url']} for s in sources],'credits':credits,
      'synthetic_content':{'narration':'síntese de voz Thalita','illustrations':'Pico v2, cenários e miniatura gerados por IA','graphics':'diagramas científicos, chuva, névoa, reflexos e movimentos em código'},
      'mascot_design_version':2,'mascot_design_reference':'producao/assets/Pico_Design_v2_16x9.png',
      'publication_mode':'manual'}
    narration='\n\n'.join(b['text'] for b in blocks);write(PUB/'Narracao.txt',narration)
    write(PUB/'Roteiro.md','# '+TITLE+'\n\n'+'\n\n'.join(f"## {stamp(b['start'])} — {b['title']}\n\n{b['text']}\n\nCenas: {', '.join(b['scenes'])}. Pico: {b['action']}." for b in blocks))
    write(PUB/'Capitulos.txt','\n'.join(stamp(c['start_seconds'])+' '+c['title'] for c in chapter_data));write(PUB/'Creditos.txt',credits)
    reference='# Fontes e procedência — episódio 005\n\nConsulta: 10/10/2026. Roteiro, analogias e diagramas originais.\n\n## Pesquisa científica\n\n'
    for s in sources:
        reference+='### '+s['name']+'\n\n'+s['url']+'\n\nUsada para: '+', '.join(s['topics'])+'. Blocos: '+', '.join(str(i+1) for i in s['blocks'])+'.\n\nConferência: '+s['verification']+'\n\n'
    reference+='## Mídias reais\n\n'
    for s in media:reference+='- '+s['key']+' — '+s['author']+'\n  Origem: '+s['source']+'\n  Licença: '+s['license']+'\n  Tratamento: enquadramento em 16:9, edição, moldura e Pico; fotografias com movimento.\n  SHA-256: '+s['sha256']+'\n\n'
    reference+='## Precisão e ilustrações\n\nPetricor e geosmina não são tratados como sinônimos. Geosmina é uma substância associada ao aroma terroso; há outros ingredientes. A geração de aerossóis em superfícies porosas foi observada; sua contribuição ao cheiro é apresentada como interpretação dos pesquisadores. Chuva leve/moderada não é uma promessa universal de cheiro mais forte: a superfície e as condições de impacto importam. Chão seco e película de água são situações distintas. Colêmbolos são artrópodes; atração por geosmina e 2-MIB e transporte de esporos se apoiam nos experimentos citados. O tubo em Y é um esquema de escolha, não uma reprodução dos dados. Não se identifica qualidade ou segurança do solo pelo cheiro. Uma observação casual não prova a causa.\n\nAs bolhas, bactérias, partículas e colêmbolos são esquemas sem escala; moléculas são símbolos, sem sugerir uma estrutura química. O cenário subterrâneo é uma ilustração artística. O laboratório histórico é uma ilustração esquemática, não uma fotografia de Bear e Thomas. As três cenas ilustradas e o Pico foram gerados com imagegen; os prompts e o modo utilizado constam no projeto de produção.\n'
    write(PUB/'Fontes.md',reference);write(ROOT/'FONTES.md',reference)
    copies=[(OUT/'Legendas_Chuva.srt','Legendas_Chuva.srt'),(OUT/'timeline.json','Storyboard.json'),(OUT/'Revisao_16x9.jpg','Revisao_16x9.jpg'),(OUT/'verificacao.json','Verificacao.json'),(ROOT/'media_sources.json','media_sources.json'),(ROOT/'research_sources.json','research_sources.json'),(ROOT.parent/'Thumb_Chuva_Quase_Infinito.jpg','Thumb_Chuva_Quase_Infinito.jpg'),(ROOT.parent/'Thumb_Chuva_Quase_Infinito.png','Thumb_Chuva_Quase_Infinito.png'),(ROOT/'assets/Pico_Design_v2_16x9.png','Pico_Design_v2_16x9.png'),(ROOT/'art_direction.json','Direcao_de_Arte.json'),(ROOT/'thumbnail_prompt.txt','Prompt_Miniatura.txt'),(ROOT/'pico_prompt.txt','Prompt_Pico.txt')]
    for source,target in copies:shutil.copyfile(source,PUB/target)
    technical={'voice':'pt-BR-ThalitaMultilingualNeural','engine':'edge_tts','edge_tts_version':'7.2.8','text_sha256':hashlib.sha256(narration.strip().encode()).hexdigest(),'segments':[]}
    for b in blocks:
        original=ROOT/'audio'/f"{b['index']:02d}.mp3";timing=json.loads(original.with_suffix('.json').read_text())
        technical['segments'].append({'index':b['index'],'start_seconds':b['start'],'duration_seconds':b['duration'],'tempo_factor':b['speed'],'source_audio_sha256':sha(original),'tts_rate':timing['rate']})
    dump(PUB/'Narracao_Tecnica.json',technical)
    for action in ['wave','question','inspect','point','surprise','flying']:
        canvas=Image.new('RGBA',(1920,1080));sprite=art.pico(action,1,height=720)
        canvas.alpha_composite(sprite,((1920-sprite.width)//2,(1080-sprite.height)//2));canvas.save(PUB/f'Pico_{action}_16x9.png')
    for name in ['Thumb_Chuva_Quase_Infinito.jpg','Thumb_Chuva_Quase_Infinito.png','Pico_Design_v2_16x9.png']:
        with Image.open(PUB/name) as im:assert im.size==(1920,1080)
    assert (PUB/'Thumb_Chuva_Quase_Infinito.jpg').stat().st_size<2000000
    frozen_voice(blocks)
    for source,target in [(VIDEO,'video.mp4'),(PUB/'Thumb_Chuva_Quase_Infinito.jpg','miniatura.jpg'),(PUB/'Thumb_Chuva_Quase_Infinito.png','miniatura.png'),(PUB/'Legendas_Chuva.srt','legendas.srt'),(PUB/'Narracao.txt','narracao.txt'),(PUB/'Narracao_Tecnica.json','narracao.json'),(PUB/'Roteiro.md','roteiro.md'),(PUB/'Fontes.md','fontes.md'),(PUB/'Capitulos.txt','capitulos.txt'),(PUB/'Creditos.txt','creditos.txt')]:shutil.copyfile(source,ep/target)
    dump(ep/'metadata.json',metadata)
    subprocess.run(['python3',str(repository/'scripts/package_episode.py'),'--episode',str(ep)],check=True)
    metadata=json.loads((ep/'metadata.json').read_text());qa=json.loads((ep/'qa.json').read_text())
    qa.update({'sha256':qa_render['sha256'],'video_frames':qa_render['video_frames'],'shots':69,
      'visual_review':'decoded final MP4 frames reviewed: detailed pixel art, Pico v2, subtitles, real footage and ending' if args.visual_reviewed else 'contact sheet created; visual review required before publication',
      'mascot_design_version':2,'research_review':'primary sources checked; aerosol mechanism and interpretation distinguished'})
    qa['audio'].update(loudness());dump(ep/'qa.json',qa);dump(PUB/'QA_Publicacao.json',qa)
    publication=dict(metadata);publication.update({'thumbnail':'Thumb_Chuva_Quase_Infinito.jpg','subtitle_file':'Legendas_Chuva.srt','video_filename':VIDEO.name});dump(PUB/'Metadata.json',publication)
    write(PUB/'Descricao_YouTube.txt',metadata['description']);write(PUB/'Titulo_YouTube.txt',TITLE);write(ep/'titulo.txt',TITLE)
    write(OUT/'Titulo_YouTube_Chuva.txt',TITLE);write(OUT/'Descricao_YouTube_Chuva.txt',metadata['description'])
    write(PUB/'Titulos_Alternativos.txt','\n'.join(metadata['alternative_titles']))
    production=ep/'producao';production.mkdir(exist_ok=True)
    readme="""# Produção do episódio 005

**Por que a chuva tem cheiro? | Quase Infinito**

69 cenas, 8min24s, Full HD 1920 × 1080 e 24 fps. A voz permanece Thalita (pt-BR-ThalitaMultilingualNeural). O episódio combina filmagens reais, duas fotografias em movimento, ilustrações detalhadas em pixel art e esquemas científicos animados.

## Direção de arte

Pico v2 conserva capacete dourado, óculos verde-água, traje turquesa, cachecol coral e asas. O novo desenho traz olhos expressivos, volume, contornos definidos e seis poses coerentes. Há três cenários de pixel art com textura, profundidade e luz. Câmera, chuva, reflexos, folhas e partículas recebem movimento na composição. Moldura persistente e uma única camada de legendas acompanham as cenas.

Os cenários e o Pico são ilustrações geradas com a ferramenta integrada imagegen. art_direction.json, pico_prompt.txt e thumbnail_prompt.txt registram o modo e os prompts. assets contém as referências finais em 16:9.

## Reproduzir no repositório

Requer Python 3.12, FFmpeg com libx264 e fontes DejaVu em /usr/share/fonts/truetype/dejavu/. Voz e mídias usam serviços externos.

    python -m pip install -r videos/ep-005-chuva/producao/requirements.txt
    python videos/ep-005-chuva/producao/prepare_media.py
    python videos/ep-005-chuva/producao/prepare_voice.py
    python videos/ep-005-chuva/producao/render.py --workers 4
    python videos/ep-005-chuva/producao/package.py

As miniaturas JPG e PNG ficam na pasta do episódio. Os resultados vão para producao/output; package.py chama o validador geral scripts/package_episode.py.

## Referências e limites dos esquemas

FONTES.md registra fontes primárias, URL, data, afirmações e procedência das mídias. As gotas, bolhas, bactérias, partículas e colêmbolos são esquemas ampliados, sem escala. O cenário subterrâneo é uma ilustração artística. O papel de aerossóis no cheiro é apresentado como interpretação dos pesquisadores. Petricor e geosmina são distintos.

O MP4 contém apenas vídeo e áudio; as legendas são desenhadas uma vez. O SRT é uma transcrição separada. O verificador rejeita uma segunda faixa embutida e decodifica o vídeo inteiro. MP4s intermediários são fechados antes de copiar os bytes completos, preservando a integridade dos contêineres.

Mídias brutas e cache ficam fora do histórico Git. A voz completa sem trilha e os segmentos originais usados estão no pacote de publicação, para referência e edição. Regenerar a voz ou baixar uma mídia modificada no serviço pode alterar o resultado; hashes identificam os arquivos desta entrega. Emanuel faz a publicação manual.

[Publicação](../PUBLICAR.md) · [Fontes](../fontes.md) · [Verificação](../qa.json)
"""
    write(production/'README.md',readme)
    for name in PRODUCTION_FILES:
        destination=production/name
        if destination.resolve()!=(ROOT/name).resolve():shutil.copyfile(ROOT/name,destination)
    shutil.copytree(ROOT/'assets',production/'assets',dirs_exist_ok=True)
    project=PUB/'Projeto_Producao';project.mkdir(exist_ok=True)
    for name in PRODUCTION_FILES:shutil.copyfile(ROOT/name,project/name)
    write(project/'README.md',readme)
    shutil.copytree(ROOT/'assets',project/'assets',dirs_exist_ok=True)
    shutil.copytree(ROOT/'audio',project/'audio',dirs_exist_ok=True)
    write(PUB/'Leia_primeiro.txt',f"""QUASE INFINITO — EPISÓDIO 005
{TITLE}

Vídeo final: {VIDEO.name}, entregue separadamente deste ZIP.
Duração: 8min24s. Full HD 1920 × 1080, 16:9, 24 fps.
Narração: a voz Thalita aprovada nos episódios anteriores.

PARA PUBLICAR
1. Envie o MP4 final ao YouTube Studio.
2. Copie Titulo_YouTube.txt e Descricao_YouTube.txt.
3. Envie Thumb_Chuva_Quase_Infinito.jpg como miniatura.
4. O vídeo já contém legendas fixas e tem somente vídeo e áudio. Guarde o SRT como transcrição; ativar outra legenda no player pode duplicar o texto.
5. Metadata.json contém tags, idioma, categoria sugerida e capítulos.
6. Defina público, visibilidade e horário no seu canal.

O pacote inclui roteiro, narração, capítulos, descrição, títulos, fontes, créditos, transcrição, miniatura JPG/PNG, a voz completa sem trilha, o novo Pico em seis poses, cenários, prompts, código e relatórios. A pasta Projeto_Producao preserva os segmentos de voz e os assets. A trilha e os efeitos já estão no MP4. O vídeo completo é baixado separadamente.

INTEGRIDADE
MP4: {qa_render['bytes']} bytes
SHA-256: {qa_render['sha256']}
Decodificação integral: aprovada.
Faixas de legenda embutida: zero.
""")
    files=sorted(p for p in PUB.rglob('*') if p.is_file() and p.name!='Checksums.sha256')
    write(PUB/'Checksums.sha256',sha(VIDEO)+'  '+VIDEO.name+'\n'+'\n'.join(sha(p)+'  '+p.relative_to(PUB).as_posix() for p in files))
    with zipfile.ZipFile(ZIP,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(PUB.rglob('*')):
            if p.is_file():z.write(p,'Quase_Infinito_Chuva/'+p.relative_to(PUB).as_posix())
    with zipfile.ZipFile(ZIP) as z:assert z.testzip() is None
    shutil.copyfile(ZIP,ep/'publicacao.zip')
    write(ep/'PUBLICAR.md',f"""# Pronto para publicar — episódio 005

**{TITLE}**

8min24s · Full HD 1920 × 1080 · 16:9 · 24 fps · voz Thalita · Pico v2

![Miniatura](miniatura.jpg)

- [Baixar vídeo completo](https://raw.githubusercontent.com/{REPOSITORY}/main/{RELATIVE}/video.mp4)
- [Baixar pacote de publicação](https://raw.githubusercontent.com/{REPOSITORY}/main/{RELATIVE}/publicacao.zip)
- [Miniatura JPG](miniatura.jpg) · [Miniatura PNG](miniatura.png)
- [Título](titulo.txt) · [Descrição com capítulos e créditos](descricao.txt)
- [Transcrição SRT](legendas.srt) · [Metadados](metadata.json)
- [Novo design do Pico](producao/assets/Pico_Design_v2_16x9.png)

Envie o MP4 ao YouTube Studio, copie título e descrição e use a miniatura JPG. O vídeo já tem legendas fixas e contém somente vídeo e áudio. O SRT é uma transcrição separada; uma segunda legenda no player pode sobrepor o texto. Defina público, visibilidade e horário no seu canal.

O pacote traz todos os materiais para publicação e os assets de edição. A voz completa sem trilha está no ZIP. Emanuel faz a publicação manual no YouTube.

[Verificação](qa.json) · [Roteiro](roteiro.md) · [Fontes](fontes.md) · [Produção](producao/README.md)

SHA-256 do MP4: {qa_render['sha256']}
""")
    files=sorted(p for p in ep.rglob('*') if p.is_file() and p.name!='checksums.sha256')
    write(ep/'checksums.sha256','\n'.join(sha(p)+'  '+p.relative_to(ep).as_posix() for p in files))
    result={'video':str(VIDEO),'zip':str(ZIP),'thumbnail':str(PUB/'Thumb_Chuva_Quase_Infinito.jpg'),'title':str(OUT/'Titulo_YouTube_Chuva.txt'),'description':str(OUT/'Descricao_YouTube_Chuva.txt'),'pico_design':str(PUB/'Pico_Design_v2_16x9.png'),'duration_seconds':qa_render['duration_seconds'],'description_characters':len(metadata['description']),'publication_files':len(list(PUB.rglob('*'))),'video_sha256':sha(VIDEO),'zip_sha256':sha(ZIP),'audio':qa['audio'],'repo_episode':str(ep)}
    dump(OUT/'delivery.json',result);print(json.dumps(result,ensure_ascii=False),flush=True)
if __name__=='__main__':main()

