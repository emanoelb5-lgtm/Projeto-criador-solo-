"""Download licensed stock clips and public-domain museum/science photos."""
import concurrent.futures, hashlib, html, json, re, requests, subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parent
MEDIA=ROOT/'media';MEDIA.mkdir(exist_ok=True)
CA='/etc/ssl/certs/ca-certificates.crt'

def request(url):
    r=requests.get(url,timeout=45,verify=CA,headers={'User-Agent':'Mozilla/5.0'});r.raise_for_status();return r

def download(url,path):
    if path.exists() and path.stat().st_size>1000:return
    temp=path.with_suffix(path.suffix+'.tmp')
    with requests.get(url,stream=True,timeout=(15,90),verify=CA) as r:
        r.raise_for_status()
        with temp.open('wb') as f:
            for block in r.iter_content(262144):f.write(block)
    temp.replace(path)

def stock(key,identifier):
    cache=MEDIA/f'{key}_page.html'
    slugs={'alarm':'a-close-up-shot-of-an-alarm-clock-4197892','clock_close':'close-up-video-of-a-clock-855782','sunrise':'time-lapse-video-of-sunrise-855646','stars':'stars-at-night-sky-12607634','tower':'clock-tower-in-town-11645112','train':'low-angle-shot-of-train-moving-6616692','phone':'scrolling-through-smartphone-854321','egypt_photo':'pyramids-in-egypt-7532358'}
    if not cache.exists():cache.write_text(request('https://www.pexels.com/video/'+slugs[key]+'/').text)
    text=cache.read_text().replace('\\u002F','/')
    pages=re.findall(r'https://www\.pexels\.com/video/[^"\s<>\\]*'+str(identifier)+r'/',text)
    page=next((p for p in pages if p!=f'https://www.pexels.com/video/{identifier}/'),f'https://www.pexels.com/video/{identifier}/')
    links=list(dict.fromkeys(re.findall(r'https://videos\.pexels\.com/video-files/'+str(identifier)+r'/[^"\s<>\\]+\.mp4',text)))
    options=[]
    for link in links:
        m=re.search(r'(\d+)_(\d+)_(\d+)fps',link)
        if m and int(m[1])>int(m[2]) and int(m[2])>=540:options.append((abs(int(m[2])-720),link))
    if not options:raise RuntimeError(f'No horizontal movie {identifier}')
    url=min(options)[1];path=MEDIA/f'{key}.mp4';download(url,path)
    title=re.search(r'<title>(.*?)</title>',text,re.S)
    author=re.search(r'"(?:creator|author)"\s*:\s*\{[^}]*"name"\s*:\s*"([^"]+)"',text)
    return {'key':key,'path':str(path.relative_to(ROOT)),'source':page,'download':url,'title':html.unescape(title[1]) if title else str(identifier),'author':author[1] if author else 'Pexels (autor na página de origem)','license':'Pexels License: https://www.pexels.com/license/','type':'video','credit':'Filmagem: Pexels • '+(author[1] if author else 'créditos no pacote')}

def museum(key,identifier,caption):
    record=ROOT/f'{key}_record.json'
    if record.exists():d=json.loads(record.read_text())
    else:
        d=request(f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{identifier}').json();record.write_text(json.dumps(d,ensure_ascii=False,indent=2))
    if not d.get('isPublicDomain') or not d.get('primaryImage'):raise RuntimeError('Museum image is not public domain')
    path=MEDIA/f'{key}.jpg';download(d['primaryImage'],path)
    return {'key':key,'path':str(path.relative_to(ROOT)),'source':d['objectURL'],'download':d['primaryImage'],'title':d['title'],'date':d['objectDate'],'author':'The Metropolitan Museum of Art','license':'Public Domain / The Met Open Access (CC0): https://www.metmuseum.org/policies/image-resources','type':'image','credit':'Foto: The Met • domínio público • '+caption,'caption':caption,'object_number':d['accessionNumber']}

def atomic():
    url='https://www.nist.gov/sites/default/files/images/2016/12/27/f2_atomic_clock.jpg';path=MEDIA/'atomic_photo.jpg';download(url,path)
    return {'key':'atomic_photo','path':str(path.relative_to(ROOT)),'source':'https://www.nist.gov/image/f2atomicclockjpg','download':url,'title':'NIST physicists Steve Jefferts and Tom Heavner with the NIST-F2 cesium fountain atomic clock','author':'NIST','date':'2014-04-03','license':'NIST public information; credit requested: https://www.nist.gov/copyrights-disclaimers','type':'image','credit':'Foto: NIST • relógio atômico NIST-F2, 2014'}

def main():
    movies=[('alarm',4197892),('clock_close',855782),('sunrise',855646),('stars',12607634),('tower',11645112),('train',6616692),('phone',854321),('egypt_photo',7532358)]
    jobs=[lambda k=k,i=i:stock(k,i) for k,i in movies]
    jobs.extend([lambda:museum('tablet_photo',321986,'tablete escolar, fim do 1º milênio a.C.'),lambda:museum('sundial_photo',202011,'relógio solar europeu, c. 1860–90'),lambda:museum('waterclock_photo',549190,'modelo de relógio de água, Egito, séc. IV a.C.'),atomic])
    entries=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        for e in pool.map(lambda f:f(),jobs):entries.append(e);print('MEDIA',e['key'],e['author'],flush=True)
    for e in entries:e['sha256']=hashlib.sha256((ROOT/e['path']).read_bytes()).hexdigest()
    (ROOT/'media_sources.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2))
    print('MEDIA_COMPLETE',len(entries),flush=True)
if __name__=='__main__':main()
