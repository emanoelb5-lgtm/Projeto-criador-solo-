import asyncio, hashlib, importlib, json, ssl
from pathlib import Path
import edge_tts

ROOT=Path(__file__).resolve().parent
VOICE='pt-BR-ThalitaMultilingualNeural'
SYSTEM_CA=Path('/etc/ssl/certs/ca-certificates.crt')
if SYSTEM_CA.exists():
    for name in ('edge_tts.voices','edge_tts.communicate'):
        for value in vars(importlib.import_module(name)).values():
            if isinstance(value,ssl.SSLContext): value.load_verify_locations(str(SYSTEM_CA))

async def section(item,sem):
    n=item['index']; rate='-3%' if n in (1,12,21,22) else '+0%'
    path=ROOT/'audio'/f'{n:02d}.mp3'; timing=path.with_suffix('.json')
    digest=hashlib.sha256((VOICE+rate+item['text']).encode()).hexdigest()
    if path.exists() and timing.exists() and json.loads(timing.read_text()).get('digest')==digest:
        print(f'VOICE {n+1:02d}/23 cached',flush=True);return
    async with sem:
        for attempt in range(3):
            try:
                words=[];temp=path.with_suffix('.tmp.mp3')
                with temp.open('wb') as out:
                    async for e in edge_tts.Communicate(item['text'],VOICE,rate=rate,boundary='WordBoundary').stream():
                        if e['type']=='audio':out.write(e['data'])
                        elif e['type']=='WordBoundary':words.append(e)
                if len(words)<len(item['text'].split())*.65 or temp.stat().st_size<1000:raise RuntimeError('Incomplete voice')
                temp.replace(path)
                timing.write_text(json.dumps({'voice':VOICE,'rate':rate,'digest':digest,'words':words},ensure_ascii=False,indent=2))
                print(f'VOICE {n+1:02d}/23 ready {len(words)} words',flush=True);return
            except Exception as e:
                print(f'VOICE {n+1:02d} retry {attempt+1}: {type(e).__name__}',flush=True)
                if attempt==2:raise
                await asyncio.sleep(2*(attempt+1))

async def main():
    (ROOT/'audio').mkdir(exist_ok=True)
    items=json.loads((ROOT/'episode.json').read_text());sem=asyncio.Semaphore(3)
    await asyncio.gather(*(section(x,sem) for x in items))
if __name__=='__main__':asyncio.run(main())

