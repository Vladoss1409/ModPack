import json, urllib.request
from pathlib import Path
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
MODS=Path(__file__).resolve().parent.parent / 'mods'

def edge_url(fid, name):
    s=str(fid)
    return f'https://edge.forgecdn.net/files/{s[:-3]}/{s[-3:]}/{name}'

def dl_cf(slug, require_1201=True):
    data=json.load(urllib.request.urlopen(urllib.request.Request(f'https://api.cfwidget.com/minecraft/mc-mods/{slug}', headers={'User-Agent':UA})))
    files=data.get('files',[])
    if require_1201:
        files=[f for f in files if any('1.20.1' in v for v in f.get('versions',[]))]
    if not files:
        print('FAIL no files', slug); return
    f=sorted(files, key=lambda x:x['id'], reverse=True)[0]
    name=f['name']
    dest=MODS/name
    if dest.exists():
        print('SKIP', slug, name); return
    url=edge_url(f['id'], name)
    req=urllib.request.Request(url, headers={'User-Agent':UA})
    dest.write_bytes(urllib.request.urlopen(req, timeout=180).read())
    print('OK', slug, name, dest.stat().st_size)

slugs=['the-twilight-forest','ftb-quests','ftb-library','ftb-teams','ftb-xmod-compat','spice-of-life-carrot-edition','ae2-things','aether']
for s in slugs:
    try:
        dl_cf(s)
    except Exception as e:
        print('ERR', s, e)
