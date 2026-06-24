import json, urllib.request
UA='Mozilla/5.0'
data=json.load(urllib.request.urlopen(urllib.request.Request('https://api.cfwidget.com/minecraft/mc-mods/ftb-library', headers={'User-Agent':UA})))
for f in sorted(data['files'], key=lambda x:x['id'], reverse=True):
    n=f['name']
    if '2001' in n and 'forge' in n.lower():
        print(f['id'], n, f.get('versions',[])[:3])
        break
