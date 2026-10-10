"""Package the verified episode and stage its GitHub publication directory."""
import argparse,hashlib,json,re,shutil,subprocess,zipfile
from pathlib import Path
from PIL import Image
import pixel_art as art

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output'
PUB=OUT/'publicacao'
VIDEO=OUT/'Quase_Infinito_Lua_1080p.mp4'
ZIP=OUT/'Quase_Infinito_Lua_Publicacao.zip'
TITLE='Por que o Lua parece seguir você? | Quase Infinito'
REPOSITORY='emanoelb5-lgtm/Projeto-criador-solo-'
RELATIVE='videos/ep-004-lua'
CHAPTERS=[(0, 'Por que ela parece nos seguir?'), (2, 'A paisagem tem camadas'), (4, 'A distância até a Lua'), (5, 'Um teste com o lápis'), (7, 'A geometria da paralaxe'), (9, 'E se a Lua estivesse perto?'), (12, 'Os movimentos reais do céu'), (14, 'Por que ela parece gigante?'), (15, 'O teste da câmera'), (17, 'Como medir distâncias de estrelas'), (19, 'Observe durante uma viagem'), (22, 'Cada pergunta abre outra viagem')]
TAGS=['por que a Lua parece seguir você', 'Lua', 'paralaxe', 'ilusão da Lua', 'astronomia', 'Lua na estrada', 'distância da Lua', 'Lua no horizonte', 'ciência', 'curiosidades', 'Pico', 'Quase Infinito']
SUMMARY='Você olha pela janela do carro e a Lua parece viajar junto. Como ela consegue acompanhar tanta gente ao mesmo tempo?\n\nNeste episódio do Quase Infinito, o Pico investiga a diferença entre postes, árvores, montanhas e a Lua. Um teste com um lápis revela a paralaxe, e essa descoberta nos leva até a medição das distâncias de estrelas.\n\nTambém vamos separar essa sensação da ilusão de uma Lua gigante no horizonte. Filmagens reais, fotografia com movimento e animações em pixel art acompanham a viagem.\n\nQual foi a sua primeira pergunta olhando para o céu? Conte nos comentários e inscreva-se no Quase Infinito.\nCada pergunta abre outra viagem.'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path,text):path.write_text(text.strip()+'\n',encoding='utf-8')
def dump(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def stamp(seconds):
    q=int(seconds);return f'{q//60:02d}:{q%60:02d}'
def loudness():
    completed=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(VIDEO),'-map','0:a:0','-af','ebur128=peak=true','-f','null','-'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
    text=completed.stderr.split('Summary:')[-1]
    values={}
    for key,pattern in [('integrated_loudness_lufs',r'I:\s+([-+\d.]+)\s+LUFS'),('true_peak_dbtp',r'Peak:\s+([-+\d.]+)\s+dBFS'),('loudness_range_lu',r'LRA:\s+([-+\d.]+)\s+LU')]:
        match=re.search(pattern,text)
        if not match:raise RuntimeError('Missing audio measurement '+key)
        values[key]=float(match[1])
    if values['true_peak_dbtp']>-1:raise RuntimeError('Audio peak exceeds target')
    if not -20<values['integrated_loudness_lufs']<-11:raise RuntimeError('Unexpected narration loudness')
    return values
def thumbnail(name,fallback):
    p=ROOT.parent/name;return p if p.exists() else ROOT.parent/fallback
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--repo-root',type=Path,default=ROOT.parents[2])
    args=parser.parse_args()
    repository=args.repo_root.resolve();ep=repository/RELATIVE
    ep.mkdir(parents=True,exist_ok=True);PUB.mkdir(exist_ok=True)
    timeline=json.loads((OUT/'timeline.json').read_text());blocks=timeline['blocks']
    render_qa=json.loads((OUT/'verificacao.json').read_text())
    assert render_qa['full_decode']=='passed' and render_qa['sha256']==sha(VIDEO)
    assert render_qa['subtitle_mode']=='burned_in' and render_qa['embedded_subtitle_streams']==0
    media=json.loads((ROOT/'media_sources.json').read_text())
    sources=json.loads((ROOT/'research_sources.json').read_text())
    credits='\n'.join(x['author']+' — '+x['source'] for x in media)
    credits+="""\n\nFilmagens e fotografia: Pexels, utilizadas sob a Pexels License.
Roteiro, trilha instrumental, moldura, Pico e animações: produção original do Quase Infinito.
Narração: voz sintetizada Thalita, em português brasileiro.
Miniatura: ilustração criada com geração de imagem por IA.
Diagramas: linhas de visão, órbitas e deslocamentos esquemáticos ampliados, sem escala. A Lua gigante da miniatura é uma ilustração."""
    chapter_data=[{'start_seconds':blocks[index]['start'],'title':text} for index,text in CHAPTERS]
    metadata={'episode':4,'channel':'Quase Infinito','repository':REPOSITORY,'title':TITLE,
        'alternative_titles':['A Lua está seguindo você? O segredo da distância','Por que a Lua acompanha o carro?'],
        'summary':SUMMARY,'language':'pt-BR','category_id':'27','category':'Education','tags':TAGS,
        'hashtags':['#QuaseInfinito','#Curiosidades','#Astronomia'],
        'voice':'pt-BR-ThalitaMultilingualNeural','duration_seconds':timeline['duration'],
        'resolution':[1920,1080],'fps':24,'thumbnail':'miniatura.jpg','subtitle_file':'legendas.srt',
        'subtitle_mode':'burned_in','embedded_subtitle_streams':0,
        'video_filename':'video.mp4','video_sha256':render_qa['sha256'],'chapters':chapter_data,
        'sources':[{'name':x['name'],'url':x['url']} for x in sources],'credits':credits,
        'synthetic_content':{'narration':'síntese de voz Thalita','thumbnail':'ilustração gerada por IA','graphics':'animações e diagramas originais em código'},
        'publication_mode':'manual'}
    narration='\n\n'.join(b['text'] for b in blocks)
    write(PUB/'Narracao.txt',narration)
    write(PUB/'Roteiro.md','# '+TITLE+'\n\n'+'\n\n'.join(f"## {stamp(b['start'])} — {b['title']}\n\n{b['text']}\n\nCenas: {', '.join(b['scenes'])}. Pico: {b['action']}." for b in blocks))
    write(PUB/'Capitulos.txt','\n'.join(stamp(c['start_seconds'])+' '+c['title'] for c in chapter_data))
    write(PUB/'Creditos.txt',credits)
    reference='# Fontes e procedência — episódio 004\n\nConsulta: 10/10/2026.\n\nO roteiro, as analogias e os diagramas foram criados para este episódio. Os desenhos não reproduzem figuras dos livros consultados.\n\n## Pesquisa científica\n\n'
    for source in sources:
        reference+='### '+source['name']+'\n\n'+source['url']+'\n\nUsada para: '+', '.join(source['topics'])+'. Blocos: '+', '.join(str(i+1) for i in source['blocks'])+'.\n\n'
    reference+='## Mídias reais\n\n'
    for source in media:
        reference+='- '+source['key']+' — '+source['author']+'\n  Origem: '+source['source']+'\n  Licença: '+source['license']+'\n  Tratamento: trecho editado ou fotografia com movimento, enquadramento em 16:9, moldura e Pico.\n  SHA-256 da mídia original: '+source['sha256']+'\n\n'
    reference+='## Precisão dos modelos\n\nA distância média usada é de 384.400 km. Linhas de visão, ângulos, órbitas e deslocamentos foram ampliados para explicar a geometria e não mostram escala real. A rotação da Terra, o movimento orbital da Lua e a paralaxe são apresentados como mecanismos distintos. A ilusão da Lua no horizonte não é confundida com a sensação de ser seguido: sua explicação completa ainda é discutida. O teste fotográfico compara largura, com o mesmo equipamento e zoom na mesma noite. A comparação de trinta Terras é aproximada. As estrelas do diagrama e a trajetória dos carros são ilustrativas, sem representar um registro real.\n'
    write(PUB/'Fontes.md',reference);write(ROOT/'FONTES.md',reference)
    for source,target in [(OUT/'Legendas_Lua.srt','Legendas_Lua.srt'),(OUT/'timeline.json','Storyboard.json'),(OUT/'Revisao_16x9.jpg','Revisao_16x9.jpg'),(OUT/'verificacao.json','Verificacao.json'),(ROOT/'media_sources.json','media_sources.json'),(thumbnail('Thumb_Lua_Quase_Infinito.jpg','miniatura.jpg'),'Thumb_Lua_Quase_Infinito.jpg'),(thumbnail('Thumb_Lua_Quase_Infinito.png','miniatura.png'),'Thumb_Lua_Quase_Infinito.png')]:
        shutil.copyfile(source,PUB/target)
    technical={'voice':'pt-BR-ThalitaMultilingualNeural','engine':'edge_tts','edge_tts_version':'7.2.8','text_sha256':hashlib.sha256(narration.strip().encode()).hexdigest(),'segments':[]}
    for b in blocks:
        original=ROOT/'audio'/f"{b['index']:02d}.mp3"
        timing=json.loads(original.with_suffix('.json').read_text())
        technical['segments'].append({'index':b['index'],'start_seconds':b['start'],'duration_seconds':b['duration'],'tempo_factor':b['speed'],'source_audio_sha256':sha(original),'tts_rate':timing['rate']})
    dump(PUB/'Narracao_Tecnica.json',technical)
    shutil.copyfile(ROOT/'thumbnail_prompt.txt',PUB/'Prompt_Miniatura.txt')
    for action in ['wave','question','inspect','point']:
        im=Image.new('RGBA',(1920,1080))
        sprite=art.pico(action,1,'moon').resize((384,480),Image.Resampling.NEAREST)
        im.alpha_composite(sprite,(768,300));im.save(PUB/f'Pico_{action}_16x9.png')
    for name in ['Thumb_Lua_Quase_Infinito.jpg','Thumb_Lua_Quase_Infinito.png']:
        with Image.open(PUB/name) as image:assert image.size==(1920,1080)
    assert (PUB/'Thumb_Lua_Quase_Infinito.jpg').stat().st_size<2000000
    for source,target in [(VIDEO,'video.mp4'),(PUB/'Thumb_Lua_Quase_Infinito.jpg','miniatura.jpg'),(PUB/'Thumb_Lua_Quase_Infinito.png','miniatura.png'),(PUB/'Legendas_Lua.srt','legendas.srt'),(PUB/'Narracao.txt','narracao.txt'),(PUB/'Narracao_Tecnica.json','narracao.json'),(PUB/'Roteiro.md','roteiro.md'),(PUB/'Fontes.md','fontes.md'),(PUB/'Capitulos.txt','capitulos.txt'),(PUB/'Creditos.txt','creditos.txt')]:
        shutil.copyfile(source,ep/target)
    dump(ep/'metadata.json',metadata)
    subprocess.run(['python3',str(repository/'scripts/package_episode.py'),'--episode',str(ep)],check=True)
    metadata=json.loads((ep/'metadata.json').read_text())
    qa=json.loads((ep/'qa.json').read_text())
    qa.update({'sha256':render_qa['sha256'],'video_frames':render_qa['video_frames'],'shots':render_qa['shots'],'visual_review':'reviewed contact sheet and caption layout','research_review':'primary sources and schematic distinctions checked'})
    qa['audio'].update(loudness())
    dump(ep/'qa.json',qa);dump(PUB/'QA_Publicacao.json',qa)
    publication_metadata=dict(metadata);publication_metadata.update({'thumbnail':'Thumb_Lua_Quase_Infinito.jpg','subtitle_file':'Legendas_Lua.srt','video_filename':VIDEO.name})
    dump(PUB/'Metadata.json',publication_metadata)
    write(PUB/'Descricao_YouTube.txt',metadata['description'])
    write(PUB/'Titulo_YouTube.txt',TITLE);write(ep/'titulo.txt',TITLE)
    write(OUT/'Titulo_YouTube_Lua.txt',TITLE)
    write(OUT/'Descricao_YouTube_Lua.txt',metadata['description'])
    write(PUB/'Titulos_Alternativos.txt','\n'.join(metadata['alternative_titles']))
    guide=f"""QUASE INFINITO — EPISÓDIO 004
{TITLE}

Vídeo final: {VIDEO.name} (entregue separadamente deste ZIP).
Duração: 8min24s. Full HD 1920 × 1080, 16:9, 24 fps.
Narração: a mesma voz Thalita aprovada nos episódios anteriores.

PARA PUBLICAR
1. Envie o MP4 final ao YouTube Studio.
2. Copie Titulo_YouTube.txt e Descricao_YouTube.txt.
3. Envie Thumb_Lua_Quase_Infinito.jpg como miniatura.
4. As legendas já estão fixas nas imagens. O MP4 contém somente vídeo e áudio. Guarde Legendas_Lua.srt como transcrição; ativar uma segunda legenda no player pode sobrepor o texto.
5. Metadata.json contém tags, idioma, categoria sugerida e capítulos.
6. Defina público, visibilidade e horário no seu canal.

O pacote contém roteiro, narração, fontes, créditos, storyboard, transcrição, miniatura JPG/PNG, sprites do Pico e verificações. A trilha, a voz e as animações já estão no MP4.

INTEGRIDADE
MP4: {render_qa['bytes']} bytes
SHA-256: {render_qa['sha256']}
Decodificação integral: aprovada.
Faixas de legenda embutida: zero.
"""
    write(PUB/'Leia_primeiro.txt',guide)
    write(PUB/'Checksums.sha256','\n'.join([sha(VIDEO)+'  '+VIDEO.name]+[sha(p)+'  '+p.name for p in sorted(PUB.iterdir()) if p.name!='Checksums.sha256']))
    with zipfile.ZipFile(ZIP,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(PUB.iterdir()):z.write(p,'Quase_Infinito_Lua/'+p.name)
    with zipfile.ZipFile(ZIP) as z:assert z.testzip() is None
    shutil.copyfile(ZIP,ep/'publicacao.zip')
    publish=f"""# Pronto para publicar — episódio 004

**{TITLE}**

8min24s · Full HD 1920 × 1080 · 16:9 · 24 fps · voz Thalita · Pico

- [Baixar vídeo completo](https://raw.githubusercontent.com/{REPOSITORY}/main/{RELATIVE}/video.mp4)
- [Baixar pacote de publicação](https://raw.githubusercontent.com/{REPOSITORY}/main/{RELATIVE}/publicacao.zip)
- [Miniatura JPG](miniatura.jpg) · [Miniatura PNG](miniatura.png)
- [Título](titulo.txt) · [Descrição com capítulos e créditos](descricao.txt)
- [Transcrição SRT](legendas.srt) · [Tags e metadados](metadata.json)

## Publicação

1. Envie o MP4 final ao YouTube Studio.
2. Copie o título e a descrição nos campos correspondentes.
3. Envie a miniatura JPG.
4. As legendas já estão fixas nas imagens. O MP4 contém somente vídeo e áudio. Guarde o SRT como transcrição; ativar uma segunda legenda no player pode sobrepor o texto.
5. Use os metadados para tags e categoria. Defina público, visibilidade e horário no seu canal.

O vídeo é baixado separadamente do ZIP. Os materiais necessários para publicação acompanham o episódio. Emanuel faz a publicação manual no YouTube.

[Verificação técnica](qa.json) · [Roteiro](roteiro.md) · [Fontes](fontes.md) · [Código da produção](producao/README.md)

SHA-256 do MP4: {render_qa['sha256']}
"""
    write(ep/'PUBLICAR.md',publish)
    production=ep/'producao';production.mkdir(exist_ok=True)
    names=['base_art.py','pixel_art.py','render.py','prepare_voice.py','prepare_media.py','package.py','episode.json','media_requests.json','media_sources.json','research_sources.json','requirements.txt','FONTES.md','thumbnail_prompt.txt']
    for name in names:
        destination=production/name
        if destination.resolve()!=(ROOT/name).resolve():shutil.copyfile(ROOT/name,destination)
    readme="""# Produção do episódio 004

**Por que o Lua parece seguir você? | Quase Infinito**

69 cenas, 8min24s, 1920 × 1080, 24 fps. A narração usa a voz aprovada pt-BR-ThalitaMultilingualNeural, com variação pequena de cadência e pausas. Filmagens reais, uma fotografia em movimento, diagramas em pixel art, moldura persistente e o Pico acompanham a história.

## Reproduzir

Requer Python 3.12, FFmpeg com libx264 e fontes DejaVu em /usr/share/fonts/truetype/dejavu/. Os serviços externos de mídia e voz precisam estar disponíveis.

    python -m pip install -r videos/ep-004-lua/producao/requirements.txt
    python videos/ep-004-lua/producao/prepare_media.py
    python videos/ep-004-lua/producao/prepare_voice.py
    python videos/ep-004-lua/producao/render.py --workers 3
    python videos/ep-004-lua/producao/package.py

A miniatura JPG e PNG fica na pasta do episódio. Os resultados aparecem em producao/output; package.py prepara os materiais e valida a entrega com scripts/package_episode.py.

## Arquivos

- episode.json: roteiro original por bloco, cenas e ação do Pico.
- research_sources.json e FONTES.md: referências primárias e afirmações verificadas.
- prepare_voice.py: geração da narração Thalita e tempos das palavras.
- prepare_media.py e media_requests.json: download das mídias licenciadas.
- media_sources.json: autoria, licença, procedência, resolução e hashes.
- base_art.py: desenho estabelecido do Pico, paleta e fontes.
- pixel_art.py: diagramas e animações originais, moldura e legendas fixas.
- render.py: montagem com cache atômico, trilha original, normalização da voz e conferência integral.
- package.py: arquivos de publicação, metadados, relatórios e ZIP.

Os diagramas de paralaxe e órbitas ampliam deslocamentos, sem escala real. A sensação de ser seguido e a ilusão da Lua no horizonte são explicadas separadamente. A montagem inclui somente vídeo e áudio no MP4. As legendas são desenhadas nas imagens, e o verificador rejeita uma segunda faixa embutida. O SRT é uma transcrição separada.

O MP4 entregue é identificado pelo SHA-256 no relatório. Regenerar uma voz ou baixar novamente uma mídia pode mudar os bytes se um serviço externo for atualizado. Os intermediários e as mídias brutas não entram no histórico Git. O fluxo prepara a publicação manual e não envia arquivos ao YouTube.

[Publicar](../PUBLICAR.md) · [Fontes](../fontes.md) · [Verificação](../qa.json)
"""
    write(production/'README.md',readme)
    files=sorted(p for p in ep.rglob('*') if p.is_file() and p.name!='checksums.sha256')
    write(ep/'checksums.sha256','\n'.join(sha(p)+'  '+p.relative_to(ep).as_posix() for p in files))
    result={'video':str(VIDEO),'zip':str(ZIP),'thumbnail':str(PUB/'Thumb_Lua_Quase_Infinito.jpg'),'title':str(OUT/'Titulo_YouTube_Lua.txt'),'description':str(OUT/'Descricao_YouTube_Lua.txt'),'duration_seconds':render_qa['duration_seconds'],'description_characters':len(metadata['description']),'publication_files':len(list(PUB.iterdir())),'video_sha256':sha(VIDEO),'zip_sha256':sha(ZIP),'audio':qa['audio'],'repo_episode':str(ep)}
    dump(OUT/'delivery.json',result)
    print(json.dumps(result,ensure_ascii=False),flush=True)
if __name__=='__main__':main()

