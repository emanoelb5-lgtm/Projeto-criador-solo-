"""Render exactly 69 synchronized documentary shots and a 504 second MP4."""
import argparse, concurrent.futures, hashlib, html, json, math, re, shutil, subprocess, unicodedata, uuid, wave, tempfile
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
import pixel_art as art

ROOT=Path(__file__).resolve().parent;OUT=ROOT/'output';CACHE=OUT/'cache'
FPS=24;SR=48000;DURATION=504;FRAMES=FPS*DURATION
FINAL=OUT/'Quase_Infinito_Lua_1080p.mp4'

def run(args,**kwargs):return subprocess.run(args,check=True,**kwargs)
def probe(path):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(path)]))
def stamp(s):
    v=round(s*1000);q,ms=divmod(v,1000);m,sec=divmod(q,60);h,m=divmod(m,60)
    return f'{h:02d}:{m:02d}:{sec:02d},{ms:03d}'

def norm(text):
    text=unicodedata.normalize('NFD',html.unescape(text)).casefold()
    return re.sub(r'[^a-z0-9]','',text)

def caption_words(words,script):
    # Merge spelled-out CFCs while retaining the true start/end word timing.
    merged=[];i=0
    while i<len(words):
        if i+2<len(words) and [norm(e['text']) for e in words[i:i+3]]==['ce','efe','ces']:
            e=dict(words[i]);last=words[i+2];e['text']='CFCs';e['duration']=last['offset']+last['duration']-e['offset'];merged.append(e);i+=3
        else:merged.append(dict(words[i]));i+=1
    target=script.replace('cé efe cês','CFCs').replace('cê efe cês','CFCs').split();cursor=0
    for e in merged:
        for count in range(1,5):
            if cursor+count<=len(target) and norm(e['text'])==norm(' '.join(target[cursor:cursor+count])):
                e['text']=' '.join(target[cursor:cursor+count]);cursor+=count;break
    return merged

def timeline():
    items=json.loads((ROOT/'episode.json').read_text());words=[];natural=[]
    for x in items:
        w=json.loads((ROOT/'audio'/f"{x['index']:02d}.json").read_text())['words'];words.append(caption_words(w,x['text']))
        natural.append((w[-1]['offset']+w[-1]['duration'])/1e7)
    speed=sum(natural)/(DURATION-len(items)*1.2)
    if not .9<speed<1.18:raise RuntimeError(f'Unnatural voice tempo {speed}')
    counts=[round((n/speed+1.2)*FPS) for n in natural];counts[-1]+=FRAMES-sum(counts)
    start=0;shots=[];cues=[]
    for x,w,n,count in zip(items,words,natural,counts):
        x.update(start=start/FPS,frames=count,duration=count/FPS,speed=n/(count/FPS-1.2),cues=[])
        local=[];group=[]
        for k,e in enumerate(w):
            token=e['text'];a=.35+e['offset']/1e7/x['speed'];b=.35+(e['offset']+e['duration'])/1e7/x['speed']
            if group and (len(group)>=7 or len(' '.join(v[0] for v in group)+' '+token)>72):local.append(group);group=[]
            group.append((token,a,b))
            if len(group)>=4 and token.endswith(('.',':','?','!',';')):local.append(group);group=[]
        if group:local.append(group)
        for j,g in enumerate(local):
            b=min(x['duration']-.1,g[-1][2]+.17)
            if j+1<len(local):b=min(b,local[j+1][0][1]-.02)
            if b<=g[0][1]:raise RuntimeError('Invalid subtitle interval')
            text=' '.join(e[0] for e in g)
            # Display normal orthography while pronunciation uses letter names.
            text=text.replace('cé efe cês','CFCs').replace('cê efe cês','CFCs')
            c={'start':g[0][1],'end':b,'text':text};x['cues'].append(c)
            cues.append({'start':x['start']+c['start'],'end':x['start']+c['end'],'text':text})
        parts=[count//3,count//3,count-2*(count//3)];pos=0
        for scene,nframes in zip(x['scenes'],parts):
            shots.append({'index':len(shots),'scene':scene,'frames':nframes,'start':(start+pos)/FPS,'local_start':pos/FPS,'item':x});pos+=nframes
        start+=count
    assert len(shots)==69 and start==FRAMES
    OUT.mkdir(exist_ok=True);CACHE.mkdir(exist_ok=True)
    (OUT/'timeline.json').write_text(json.dumps({'duration':DURATION,'fps':FPS,'blocks':items,'shots':[{k:v for k,v in s.items() if k!='item'} for s in shots]},ensure_ascii=False,indent=2))
    (OUT/'Legendas_Lua.srt').write_text('\n'.join(f"{k+1}\n{stamp(c['start'])} --> {stamp(c['end'])}\n"+'\n'.join(art.wrap(c['text']))+'\n' for k,c in enumerate(cues)))
    return items,shots

def score(start,count,index,cuts):
    t=start+np.arange(count,dtype=np.float64)/SR;local=np.arange(count)/SR
    chords=[(146.83,220,293.66),(130.81,196,261.63),(164.81,246.94,329.63),(110,164.81,220)]
    c=chords[int(start//24)%4];pad=np.zeros(count,dtype=np.float32)
    for k,f in enumerate(c):pad+=(np.sin(2*np.pi*f*t)+.24*np.sin(2*np.pi*f*2.003*t))*.0038
    notes=[293.66,440,523.25,587.33,440,329.63,392,293.66]
    beat=1.75;pos=t%beat;n=np.floor(t/beat).astype(int)%len(notes);freq=np.take(notes,n)
    melody=(np.sin(2*np.pi*freq*pos)+.35*np.sin(2*np.pi*freq*2*pos))*np.exp(-pos*5.2)*.011
    track=pad+melody.astype(np.float32)
    for cut in cuts:
        age=local-cut;active=(age>=0)&(age<.22);z=age[active]
        track[active]+=(np.sin(2*np.pi*780*z)*np.exp(-z*35)*.007).astype(np.float32)
    envelope=np.minimum(1,np.minimum(t/.8,(DURATION-t)/1.4))
    track*=np.clip(envelope,0,1)
    return np.column_stack((track,track*(.97+.03*np.sin(t*.2))))

def render_audio(item):
    n=item['index'];path=CACHE/f'audio_{n:02d}.wav';temp=CACHE/f'voice_{n:02d}.wav'
    filt=f"atempo={item['speed']:.9f},loudnorm=I=-16:TP=-2:LRA=8,aresample={SR},adelay=350,apad,atrim=duration={item['duration']:.9f}"
    run(['ffmpeg','-y','-v','error','-i',str(ROOT/'audio'/f'{n:02d}.mp3'),'-af',filt,'-ar',str(SR),'-ac','1',str(temp)])
    with wave.open(str(temp),'rb') as f:voice=np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').astype(np.float32)/32768
    samples=item['frames']*SR//FPS;voice=np.pad(voice,(0,max(0,samples-len(voice))))[:samples]
    music=score(item['start'],samples,n,[i*item['duration']/3 for i in range(3)])
    blocks=np.pad(voice,(0,(-len(voice))%960)).reshape(-1,960);rms=np.sqrt(np.mean(blocks**2,axis=1))
    rms=np.convolve(rms,np.ones(9)/9,mode='same');duck=np.interp(np.arange(samples)/960,np.arange(len(rms)),.40+.60*np.exp(-rms*22))
    music*=duck[:,None];mixed=voice[:,None]*.94+music
    peak=float(np.max(np.abs(mixed)));mixed*=min(1,.94/max(peak,.0001))
    with wave.open(str(path),'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(SR);f.writeframes((mixed*32767).astype('<i2').tobytes())
    temp.unlink()
    return {'index':n,'voice_speed':item['speed'],'peak':peak,'voice_rms':float(np.sqrt(np.mean(voice**2))),'music_rms':float(np.sqrt(np.mean(music**2)))}

def render_shot(shot,sources):
    n=shot['index'];scene=shot['scene'];item=shot['item'];path=CACHE/f'shot_{n:03d}.mp4'
    key=scene;offset=0
    asset=sources.get(key);pixel=asset is None;source='Animação original em pixel art'
    digest=hashlib.sha256((json.dumps(shot,sort_keys=True)+(ROOT/'pixel_art.py').read_text()+'layout-v2-fps24-h1080'+str(asset.get('sha256') if asset else 'original')).encode()).hexdigest()
    marker=path.with_suffix('.digest');temporary=path.with_suffix('.rendering.mp4')
    if path.exists() and marker.exists():
        stored=marker.read_text();adopt=False
        try:
            cache=json.loads(stored)
            if cache.get('recipe')==digest and cache.get('video_sha256')==hashlib.sha256(path.read_bytes()).hexdigest():
                print(f'SHOT {n+1:02d}/69 cached',flush=True);return path
        except (ValueError,AttributeError):
            legacy=ROOT/'cache_legacy_recipes.json'
            if legacy.exists() and json.loads(legacy.read_text()).get(str(n))==stored:
                try:adopt=int(next(s for s in probe(path)['streams'] if s['codec_type']=='video')['nb_frames'])==shot['frames']
                except (subprocess.CalledProcessError,KeyError,StopIteration):adopt=False
        if adopt:
            marker.write_text(json.dumps({'recipe':digest,'video_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}))
            print(f'SHOT {n+1:02d}/69 verified cache',flush=True);return path
    common=['ffmpeg','-y','-v','error','-threads','1','-filter_complex_threads','1']
    if pixel:
        cmd=common+['-f','rawvideo','-pix_fmt','rgb24','-s','960x540','-r',str(FPS),'-i','pipe:0','-vf','scale=1920:1080:flags=neighbor']
    else:
        media=ROOT/asset['path'];info=probe(media);duration=float(info['format'].get('duration',0))
        if asset['type']=='image':
            inputs=['-loop','1','-framerate',str(FPS),'-i',str(media)]
            bg="[0:v]scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,zoompan=z='min(1.045,1+on*0.00025)':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=960x540:fps=24[bg];"
            source=asset['credit']
        else:
            offset=(n*1.7)%max(1,duration-shot['frames']/FPS-.1)
            if offset>=duration:raise RuntimeError(f'Offset outside source: {scene}')
            inputs=['-stream_loop','-1','-ss',str(offset),'-i',str(media)]
            bg='[0:v]fps=24,scale=960:540:force_original_aspect_ratio=increase,crop=960:540,setsar=1[bg];'
            source=asset['credit']
        graph=bg+'[bg][1:v]overlay=shortest=1,scale=1920:1080:flags=lanczos,setsar=1[v]'
        cmd=common+inputs+['-f','rawvideo','-pix_fmt','rgba','-s','960x540','-r',str(FPS),'-i','pipe:0','-filter_complex',graph,'-map','[v]']
    cmd+=['-frames:v',str(shot['frames']),'-an','-c:v','libx264','-preset','veryfast','-crf','24','-maxrate','1400k','-bufsize','2800k','-pix_fmt','yuv420p','-threads','2','-g','48','-video_track_timescale','24000',str(temporary)]
    error=CACHE/f'shot_{n:03d}.log'
    print(f'SHOT {n+1:02d}/69 {scene} {shot["frames"]/FPS:.2f}s',flush=True)
    with error.open('wb') as err:
        proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=err)
        try:
            for k in range(shot['frames']):
                local=shot['local_start']+k/FPS;global_time=shot['start']+k/FPS
                cue=next((c['text'] for c in item['cues'] if c['start']<=local<c['end']),'')
                over=art.overlay(item,scene,local,global_time,cue,source,pixel)
                if pixel:
                    im=art.pixel_scene(scene,k/FPS+item['index']*.4).convert('RGBA');im=Image.alpha_composite(im,over).convert('RGB')
                else:im=over
                proc.stdin.write(im.tobytes())
            proc.stdin.close();code=proc.wait()
            if code:raise RuntimeError(error.read_text())
        except Exception:
            proc.kill();proc.wait();raise
    frames=int(next(s for s in probe(temporary)['streams'] if s['codec_type']=='video')['nb_frames'])
    if frames!=shot['frames']:raise RuntimeError(f'Incomplete shot {n}: {frames}/{shot["frames"]}')
    temporary.replace(path)
    marker.write_text(json.dumps({'recipe':digest,'video_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}))
    print(f'SHOT {n+1:02d}/69 complete',flush=True)
    return path

def assemble(items,shots):
    listing=CACHE/'concat.txt';listing.write_text(''.join(f"file '{CACHE/f'shot_{s["index"]:03d}.mp4'}'\n" for s in shots))
    session=uuid.uuid4().hex
    joined=CACHE/f'joined_{session}.mp4';run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(listing),'-c','copy',str(joined)])
    frames=int(next(s for s in probe(joined)['streams'] if s['codec_type']=='video')['nb_frames'])
    if frames!=FRAMES:raise RuntimeError(f'Incomplete assembled video: {frames}/{FRAMES}')
    mixed=CACHE/f'mix_{session}.wav';count=0
    with wave.open(str(mixed),'wb') as out:
        out.setnchannels(2);out.setsampwidth(2);out.setframerate(SR)
        for item in items:
            with wave.open(str(CACHE/f'audio_{item["index"]:02d}.wav'),'rb') as src:
                out.writeframesraw(src.readframes(src.getnframes()));count+=src.getnframes()
    assert count==SR*DURATION
    temporary=Path(tempfile.mkdtemp(prefix='quase-infinito-assembly-'))/'episode.mp4'
    # pixel_art.overlay already draws the captions into every video frame.
    run(['ffmpeg','-y','-v','error','-i',str(joined),'-i',str(mixed),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','128k','-sn','-metadata','title=Por que o Lua parece seguir você? | Quase Infinito','-t',str(DURATION),'-movflags','+faststart',str(temporary)])
    return temporary

def verify(shots,path=None):
    path=path or FINAL
    data=probe(path);v=next(s for s in data['streams'] if s['codec_type']=='video');a=next(s for s in data['streams'] if s['codec_type']=='audio')
    if any(s['codec_type']=='subtitle' for s in data['streams']):raise RuntimeError('Legendas fixas não devem ter uma segunda faixa embutida no MP4.')
    assert (v['width'],v['height'])==(1920,1080);assert v['r_frame_rate']=='24/1';assert int(v['nb_frames'])==FRAMES
    assert abs(float(data['format']['duration'])-DURATION)<.1;assert abs(float(a['duration'])-DURATION)<.1
    run(['ffmpeg','-xerror','-v','error','-i',str(path),'-map','0:v:0','-map','0:a:0','-f','null','-'],stdout=subprocess.DEVNULL)
    report={'file':FINAL.name,'duration_seconds':float(data['format']['duration']),'resolution':[1920,1080],'fps':24,'shots':len(shots),'video_frames':int(v['nb_frames']),'audio':'AAC stereo 48000 Hz','voice':'pt-BR-ThalitaMultilingualNeural','subtitle_mode':'burned_in','embedded_subtitle_streams':0,'full_decode':'passed','bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    (OUT/'verificacao.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print('VERIFIED',json.dumps(report),flush=True)

def previews(shots):
    sheet=Image.new('RGB',(1920,1080))
    selected=[shots[i] for i in [0,4,13,20,25,42,46,54,68]]
    for i,s in enumerate(selected):
        p=CACHE/f'qa_{i}.jpg';run(['ffmpeg','-y','-v','error','-threads','1','-filter_threads','1','-ss',str(s['start']+1.6),'-i',str(FINAL),'-frames:v','1','-vf','scale=640:360','-threads','1',str(p)])
        with Image.open(p) as im:sheet.paste(im,((i%3)*640,(i//3)*360))
    sheet.save(OUT/'Revisao_16x9.jpg',quality=93)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--workers',type=int,default=3);ap.add_argument('--shot',type=int);ap.add_argument('--verify-only',action='store_true');args=ap.parse_args()
    items,shots=timeline();sources={x['key']:x for x in json.loads((ROOT/'media_sources.json').read_text())}
    for s in shots:
        key=s['scene']
        if key not in sources:art.pixel_scene(key,1)
    if args.verify_only:verify(shots);previews(shots);return
    if args.shot is not None:render_shot(shots[args.shot],sources);return
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        levels=list(pool.map(render_audio,items))
        list(pool.map(lambda s:render_shot(s,sources),shots))
    (OUT/'audio_levels.json').write_text(json.dumps(levels,indent=2))
    temporary=assemble(items,shots)
    # Mux outside the managed output folder, then write the completed bytes.
    # This preserves faststart headers through workspace file synchronization.
    FINAL.write_bytes(temporary.read_bytes())
    verify(shots,FINAL);previews(shots);shutil.rmtree(temporary.parent)
if __name__=='__main__':main()


