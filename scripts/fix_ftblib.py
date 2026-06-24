import json, urllib.request
from pathlib import Path
UA='Mozilla/5.0'
MODS=Path(__file__).resolve().parent.parent / 'mods'
# remove wrong library
for p in MODS.glob('FTBLib-*.jar'):
    print('REMOVE', p.name); p.unlink()
data=json.load(urllib.request.urlopen(urllib.request.Request('https://api.cfwidget.com/minecraft/mc-mods/ftb-library-forge', headers={'User-Agent':UA})))
files=[f for f in data['files'] if any('1.20.1' in v for v in f.get('versions',[]))]
f=sorted(files,key=lambda x:x['id'], reverse=True)[0]
print('picked', f['id'], f['name'])
fid=f['id']; name=f['name']
url=f'https://edge.forgecdn.net/files/{str(fid)[:-3]}/{str(fid)[-3:]}/{name}'
dest=MODS/name
dest.write_bytes(urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':UA}),timeout=180).read())
print('OK', name, dest.stat().st_size)
print('total mods', len(list(MODS.glob('*.jar'))))
