import json, urllib.request
UA='Mozilla/5.0'
# ftb-library versions
data=json.load(urllib.request.urlopen(urllib.request.Request('https://api.cfwidget.com/minecraft/mc-mods/ftb-library', headers={'User-Agent':UA})))
vers=set()
for f in data['files'][:30]:
    for v in f.get('versions',[]): vers.add(v)
print('ftb-library sample versions', sorted([v for v in vers if '1.20' in v])[:20])
files=[f for f in data['files'] if any(v.startswith('1.20.1') for v in f.get('versions',[]))]
print('1.20.1 exact count', len(files))
if files:
    f=sorted(files,key=lambda x:x['id'], reverse=True)[0]
    print('latest', f['id'], f['name'])

# ae2 things search cf
for slug in ['ae2-things-forge','ae2-things','ae2-things-forge-1','advanced-ae']:
    try:
        d=json.load(urllib.request.urlopen(urllib.request.Request(f'https://api.cfwidget.com/minecraft/mc-mods/{slug}', headers={'User-Agent':UA})))
        print('found', slug, d.get('id'), len(d.get('files',[])))
    except Exception as e:
        print(slug, e)

# aether cf slug
for slug in ['aether','aether-mod','the-aether','aether-i']:
    try:
        d=json.load(urllib.request.urlopen(urllib.request.Request(f'https://api.cfwidget.com/minecraft/mc-mods/{slug}', headers={'User-Agent':UA})))
        print('aether slug', slug, d.get('id'))
    except Exception as e:
        print('aether slug', slug, e)

# cumulus + aether modrinth redownload
import urllib.parse
from pathlib import Path
MODS=Path(__file__).resolve().parent.parent / 'mods'
for slug in ['aether','cumulus']:
    q=urllib.parse.urlencode([('loaders', json.dumps(['forge'])), ('game_versions', json.dumps(['1.20.1']))])
    vs=json.load(urllib.request.urlopen(urllib.request.Request(f'https://api.modrinth.com/v2/project/{slug}/version?{q}', headers={'User-Agent':'MyModPack/1.0'})))
    if vs:
        f=vs[0]['files'][0]; dest=MODS/f['filename']
        if not dest.exists():
            dest.write_bytes(urllib.request.urlopen(urllib.request.Request(f['url'], headers={'User-Agent':'MyModPack/1.0'})).read())
        print('mr', slug, f['filename'])
