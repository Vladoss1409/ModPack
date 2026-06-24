import json, urllib.request, urllib.parse
from pathlib import Path
UA='MyModPack/1.0'
ROOT=Path(__file__).resolve().parent.parent
MODS=ROOT/'mods'

MISSING_MR = [
    'immersiveengineering','storagedrawers','the-undergarden','bad-wither-no-cookie',
    'elevatormod','rubidium-extra','bookshelf-lib','inventory-sorter-configurable',
    'l_enders-cataclysm','alexs-caves','bosses-of-mass-destruction-forge','ferrite-core',
    'repurposed-structures-forge',
]

def edge_url(fid, name):
    s = str(fid)
    return f'https://edge.forgecdn.net/files/{s[:-3]}/{s[-3:]}/{name}'

def dl(url, dest, force=False):
    if dest.exists() and not force:
        return False
    req=urllib.request.Request(url, headers={'User-Agent':UA})
    dest.write_bytes(urllib.request.urlopen(req, timeout=180).read())
    return True

def install_mr(slug):
    q=urllib.parse.urlencode([('loaders', json.dumps(['forge'])), ('game_versions', json.dumps(['1.20.1']))])
    vs=json.load(urllib.request.urlopen(urllib.request.Request(f'https://api.modrinth.com/v2/project/{slug}/version?{q}', headers={'User-Agent':UA})))
    if not vs:
        print('FAIL mr', slug); return
    v=next((x for x in vs if x.get('version_type')=='release'), vs[0])
    f=v['files'][0]; dest=MODS/f['filename']
    if dl(f['url'], dest): print('OK mr', slug, f['filename'])
    else: print('SKIP mr', slug)

# fix aether neoforge -> remove and get forge-only
for bad in MODS.glob('*neoforge*.jar'):
    print('REMOVE', bad.name); bad.unlink()
for bad in MODS.glob('cumulus*.jar'):
    print('REMOVE', bad.name); bad.unlink()

# aether forge-only
vs=json.load(urllib.request.urlopen(urllib.request.Request('https://api.modrinth.com/v2/project/aether/version?game_versions=%5B%221.20.1%22%5D', headers={'User-Agent':UA})))
for v in vs:
    loaders=v.get('loaders',[])
    if loaders==['forge'] or ('forge' in loaders and 'neoforge' not in loaders):
        f=v['files'][0]; dest=MODS/f['filename']
        if dl(f['url'], dest): print('OK aether forge', f['filename'])
        break

for slug in MISSING_MR:
    install_mr(slug)

# CurseForge via cfwidget slugs
CF = [
    'the-twilight-forest','ftb-quests-forge','ftb-library-forge','ftb-teams-forge','ftb-chunks',
    'ftb-xmod-compat','spice-of-life-carrot-edition','solcarrot','ae2-things-forge','ae2-things',
]
for slug in CF:
    try:
        data=json.load(urllib.request.urlopen(urllib.request.Request(f'https://api.cfwidget.com/minecraft/mc-mods/{slug}', headers={'User-Agent':UA})))
        cand=[f for f in data.get('files',[]) if any('1.20.1' in v for v in f.get('versions',[]))]
        if not cand:
            print('FAIL cf', slug, 'no file'); continue
        f=sorted(cand, key=lambda x:x.get('id',0), reverse=True)[0]
        fname=f.get('name') or f.get('filename') or f.get('displayName')+'.jar'
        if not fname.endswith('.jar'):
            fname += '.jar'
        url=edge_url(f['id'], fname)
        dest=MODS/fname
        if dl(url, dest): print('OK cf', slug, fname, dest.stat().st_size)
        else: print('SKIP cf', slug)
    except Exception as e:
        print('FAIL cf', slug, e)
