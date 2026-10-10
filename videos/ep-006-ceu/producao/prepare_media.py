"""Download licensed Pexels clips and photograph; keep source and byte hashes."""
import concurrent.futures,hashlib,html,json,re,ssl,subprocess,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parent
MEDIA=ROOT/'media';MEDIA.mkdir(exist_ok=True)
CA=ssl.create_default_context(cafile='/etc/ssl/certs/ca-certificates.crt')
def request(url):
    return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),context=CA,timeout=45)
def download(url,path):
    if path.exists() and path.stat().st_size>1000:return
    temp=path.with_suffix(path.suffix+'.temporary')
    with request(url) as response,temp.open('wb') as stream:
        while block:=response.read(262144):stream.write(block)
    temp.replace(path)
def stock(item):
    key=item['key']
    if item.get('download'):
        path=MEDIA/f'{key}.jpg';download(item['download'],path)
        info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(path)]))
        video=info['streams'][0]
        return {'key':key,'path':str(path.relative_to(ROOT)),'source':item['url'],'download':item['download'],'title':item['title'],'author':item['author'],'license':item['license'],'type':'image','credit':'Registro: Curiosity • NASA/JPL-Caltech/MSSS/TAMU','sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'width':video['width'],'height':video['height']}
    identifier=item['id']
    cache=MEDIA/f'{key}_{identifier}_page.html'
    if not cache.exists():
        with request(item['url']) as response:cache.write_text(response.read().decode())
    text=cache.read_text().replace('\\u002F','/')
    title=re.search(r'<title>(.*?)</title>',text,re.S)
    author=re.search(r'"(?:creator|author)"\s*:\s*\{[^}]*"name"\s*:\s*"([^"]+)"',text)
    if author:item['author']=html.unescape(author[1])
    if item.get('type')=='image':
        links=re.findall(r'https://images\.pexels\.com/photos/'+str(identifier)+r'/[^"\s<>\\?]+\.(?:jpeg|jpg|png)',text)
        if not links:raise RuntimeError('No photograph '+str(identifier))
        url=links[0]+'?auto=compress&cs=tinysrgb&w=1920';path=MEDIA/f'{key}_{identifier}.jpg';kind='image'
    else:
        links=list(dict.fromkeys(re.findall(r'https://videos\.pexels\.com/video-files/'+str(identifier)+r'/[^"\s<>\\]+\.mp4',text)))
        options=[]
        for link in links:
            m=re.search(r'(\d+)_(\d+)_(\d+)fps',link)
            if m and int(m[1])>int(m[2]) and int(m[2])>=540:options.append((abs(int(m[2])-720),link))
        if not options:raise RuntimeError('No horizontal movie '+str(identifier))
        url=min(options)[1];path=MEDIA/f'{key}_{identifier}.mp4';kind='video'
    download(url,path)
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
    video=next(s for s in info['streams'] if s['codec_type']=='video')
    if kind=='video':assert video['width']>video['height']
    out={'key':key,'path':str(path.relative_to(ROOT)),'source':item['url'],'download':url,'title':html.unescape(title[1]) if title else key,'author':item['author'],'license':'Pexels License: https://www.pexels.com/license/','type':kind,'credit':('Foto' if kind=='image' else 'Filmagem')+': '+item['author']+' • Pexels','sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'width':video['width'],'height':video['height']}
    print(json.dumps({'media':key,'author':out['author'],'dimensions':[video['width'],video['height']]},ensure_ascii=False),flush=True)
    return out
def main():
    items=json.loads((ROOT/'media_requests.json').read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:entries=list(pool.map(stock,items))
    if any(x['author']=='verificar na página' for x in entries):raise RuntimeError('Missing author credit')
    detail=dict(next(x for x in entries if x['key']=='mars_photo'));detail['key']='mars_photo_detail';entries.append(detail)
    (ROOT/'media_sources.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n')
    print('MEDIA_READY',len(entries),flush=True)
if __name__=='__main__':main()

