import json, urllib.parse, urllib.request
UA='MyModPack/1.0'
MC='1.20.1'

def list_forge(slug, limit=5):
    q=urllib.parse.urlencode([('loaders', json.dumps(['forge'])), ('game_versions', json.dumps([MC]))])
    try:
        vs=json.load(urllib.request.urlopen(urllib.request.Request(f'https://api.modrinth.com/v2/project/{slug}/version?{q}', headers={'User-Agent':UA})))
    except Exception as e:
        print(slug, 'ERR', e); return
    print(slug, 'count', len(vs))
    for v in vs[:limit]:
        print(' ', v['version_number'], v['files'][0]['filename'], v.get('loaders'))

extra = [
    'ae2things','storagedrawers','the-undergarden','bad-wither-no-cookie','elevatormod',
    'rubidium-extra','bookshelf-lib','inventory-sorter-configurable','l_enders-cataclysm',
    'alexscaves-expansion','alex-caves','alexscaves','alex-caves-official','alexscavesofficial',
    'twilight-forest-mod','twilightforest','the-twilight-forest','twilight-forest',
    'spice-of-life-carrot-edition','solcarrot','carrot','bosses-of-mass-destruction',
    'repurposed-structures-fabric','repurposed-structures','immersiveengineering',
    'ferrite-core','ferritecore-mod','ftb-quests-forge','ftb-quests','ftb-library-forge',
    'ftb-library','ftb-teams-forge','ftb-teams','ftb-chunks-forge','ftb-chunks','ftb-xmod-compat'
]
for s in extra:
    list_forge(s, 2)
    print('---')
