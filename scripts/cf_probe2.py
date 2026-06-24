import json, urllib.request
UA='MyModPack/1.0'
for slug in ['the-twilight-forest','ftb-quests','spice-of-life-carrot-edition','ftb-xmod-compat','aether']:
    data=json.load(urllib.request.urlopen(urllib.request.Request(f'https://api.cfwidget.com/minecraft/mc-mods/{slug}', headers={'User-Agent':UA})))
    print(slug, 'files', len(data.get('files',[])), 'categories', data.get('categories'))
    if data.get('files'):
        f=data['files'][0]
        print(' keys', list(f.keys())[:12])
        print(' sample', {k:f.get(k) for k in ['id','fileName','fileDate','releaseType','gameVersions'] if k in f})
