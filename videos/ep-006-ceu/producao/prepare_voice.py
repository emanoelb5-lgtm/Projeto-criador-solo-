"""Freeze the approved Thalita voice and word timing, one narrative block at a time."""
import asyncio, hashlib, importlib, json, ssl, tempfile
from pathlib import Path
import edge_tts

ROOT=Path(__file__).resolve().parent
VOICE='pt-BR-ThalitaMultilingualNeural'
CA=Path('/etc/ssl/certs/ca-certificates.crt')
if CA.exists():
    for name in ('edge_tts.voices','edge_tts.communicate'):
        for value in vars(importlib.import_module(name)).values():
            if isinstance(value,ssl.SSLContext):value.load_verify_locations(str(CA))

async def section(item,sem,total):
    n=item['index'];rate='-2%' if n in (0,8,19,23) else '+1%'
    path=ROOT/'audio'/f'{n:02d}.mp3';timing=path.with_suffix('.json')
    digest=hashlib.sha256((VOICE+rate+item['text']).encode()).hexdigest()
    if path.exists() and timing.exists() and json.loads(timing.read_text()).get('digest')==digest:
        print(f'VOICE {n+1:02d}/{total} cached',flush=True);return
    async with sem:
        for attempt in range(3):
            try:
                words=[]
                with tempfile.TemporaryDirectory(prefix='quase-infinito-tts-') as work:
                    temporary=Path(work)/'voice.mp3'
                    with temporary.open('wb') as out:
                        async for event in edge_tts.Communicate(item['text'],VOICE,rate=rate,boundary='WordBoundary').stream():
                            if event['type']=='audio':out.write(event['data'])
                            elif event['type']=='WordBoundary':words.append(event)
                    if len(words)<len(item['text'].split())*.65 or temporary.stat().st_size<1000:raise RuntimeError('Incomplete voice')
                    path.write_bytes(temporary.read_bytes())
                timing.write_text(json.dumps({'voice':VOICE,'rate':rate,'digest':digest,'words':words},ensure_ascii=False,indent=2)+'\n')
                print(f'VOICE {n+1:02d}/{total} ready {len(words)} words',flush=True);return
            except Exception as exc:
                print(f'VOICE {n+1:02d} retry {attempt+1}: {type(exc).__name__}',flush=True)
                if attempt==2:raise
                await asyncio.sleep(2*(attempt+1))

async def main():
    (ROOT/'audio').mkdir(exist_ok=True)
    items=json.loads((ROOT/'episode.json').read_text());sem=asyncio.Semaphore(3)
    print('SCRIPT_WORDS',sum(len(x['text'].split()) for x in items),flush=True)
    await asyncio.gather(*(section(x,sem,len(items)) for x in items))
if __name__=='__main__':asyncio.run(main())
