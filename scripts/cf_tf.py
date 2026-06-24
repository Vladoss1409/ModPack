import json, urllib.request
UA='Mozilla/5.0 MyModPack/1.0'
data=json.load(urllib.request.urlopen(urllib.request.Request('https://api.cfwidget.com/minecraft/mc-mods/the-twilight-forest', headers={'User-Agent':UA})))
files=[f for f in data['files'] if any('1.20.1' in v for v in f.get('versions',[]))]
print('count', len(files))
for f in sorted(files,key=lambda x:x['id'], reverse=True)[:5]:
    print(f['id'], f.get('display'), f['name'], f.get('version'))
