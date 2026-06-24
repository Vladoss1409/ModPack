import json, urllib.request
from pathlib import Path
UA='Mozilla/5.0'
MODS=Path(__file__).resolve().parent.parent / 'mods'

def edge(fid,name):
    s=str(fid); return f'https://edge.forgecdn.net/files/{s[:-3]}/{s[-3:]}/{name}'

def dl_slug(slug):
    data=json.load(urllib.request.urlopen(urllib.request.Request(f'https://api.cfwidget.com/minecraft/mc-mods/{slug}', headers={'User-Agent':UA})))
    files=data['files']
    # ftb-library uses loader version strings
    cand=[f for f in files if '1.20.1' in f.get('name','') or '2001' in f.get('name','')]
    cand=[f for f in cand if 'forge' in f.get('name','').lower()]
    if not cand:
        cand=[f for f in files if any('1.20.1' in v for v in f.get('versions',[]))]
    f=sorted(cand or files, key=lambda x:x['id'], reverse=True)[0]
    name=f['name']; dest=MODS/name
    if dest.exists():
        print('SKIP', name); return
    dest.write_bytes(urllib.request.urlopen(urllib.request.Request(edge(f['id'],name), headers={'User-Agent':UA}), timeout=180).read())
    print('OK', slug, name)

for slug in ['ftb-library','ae2-things-forge','the-aether']:
    try: dl_slug(slug)
    except Exception as e: print('ERR', slug, e)

print('mod count', len(list(MODS.glob('*.jar'))))
