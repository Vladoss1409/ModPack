import json, urllib.request
UA='MyModPack/1.0'

def probe(slug):
    q='loaders=%5B%22forge%22%5D&game_versions=%5B%221.20.1%22%5D'
    try:
        vs=json.load(urllib.request.urlopen(urllib.request.Request(f'https://api.modrinth.com/v2/project/{slug}/version?{q}',headers={'User-Agent':UA})))
        print(slug, len(vs), vs[0]['files'][0]['filename'] if vs else 'none')
    except Exception as e:
        print(slug, 'ERR', e)

for s in ['alexs-caves','bosses-of-mass-destruction-forge','bosses-of-mass-destruction','ae2things','repurposed-structures-forge','the-twilight-forest-unofficial']:
    probe(s)

# cfwidget
for slug in ['twilight-forest','ftb-quests-forge','ftb-library-forge','ftb-teams-forge','ftb-chunks-forge','ftb-xmod-compat','spice-of-life-carrot-edition','ae2-things']:
    url=f'https://api.cfwidget.com/minecraft/mc-mods/{slug}'
    try:
        data=json.load(urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':UA})))
        files=[f for f in data.get('files',[]) if '1.20.1' in f.get('versions',[]) and f.get('display')=='release']
        if not files:
            files=[f for f in data.get('files',[]) if '1.20.1' in f.get('versions',[])][:1]
        if files:
            f=sorted(files,key=lambda x:x.get('id',0),reverse=True)[0]
            print('CF', slug, f['filename'], f['url'])
        else:
            print('CF', slug, 'no 1.20.1 file')
    except Exception as e:
        print('CF', slug, 'ERR', e)
