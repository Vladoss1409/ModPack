import json, urllib.request
UA='MyModPack/1.0'
slugs=['ftb-quests','ftb-library','ftb-teams','ftb-chunks','the-twilight-forest','spice-of-life-carrot-edition','solcarrot','ae2-things','aether']
for slug in slugs:
    data=json.load(urllib.request.urlopen(urllib.request.Request(f'https://api.cfwidget.com/minecraft/mc-mods/{slug}', headers={'User-Agent':UA})))
    print('===', slug, data.get('name'), 'id', data.get('id'))
    for f in sorted(data.get('files',[]), key=lambda x:x.get('id',0), reverse=True)[:3]:
        vers=f.get('versions',[])
        if any('1.20.1' in v for v in vers):
            print(' ', f.get('id'), f.get('filename'), f.get('url')[:80] if f.get('url') else None, vers[:3])
