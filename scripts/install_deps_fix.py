import json, urllib.request, urllib.parse
from pathlib import Path

UA = 'MyModPack/1.0'
MODS = Path(__file__).resolve().parent.parent / 'mods'


def edge_url(fid, name):
    s = str(fid)
    return f'https://edge.forgecdn.net/files/{s[:-3]}/{s[-3:]}/{name}'


def dl_mr(slug, force=False):
    q = urllib.parse.urlencode([
        ('loaders', json.dumps(['forge'])),
        ('game_versions', json.dumps(['1.20.1'])),
    ])
    vs = json.load(urllib.request.urlopen(
        urllib.request.Request(
            f'https://api.modrinth.com/v2/project/{slug}/version?{q}',
            headers={'User-Agent': UA},
        )
    ))
    if not vs:
        print('FAIL no versions', slug)
        return
    v = next((x for x in vs if x.get('version_type') == 'release'), vs[0])
    f = v['files'][0]
    dest = MODS / f['filename']
    if dest.exists() and force:
        dest.unlink()
    if dest.exists():
        print('SKIP mr', slug, dest.name)
        return
    req = urllib.request.Request(f['url'], headers={'User-Agent': UA})
    dest.write_bytes(urllib.request.urlopen(req, timeout=120).read())
    print('OK mr', slug, f['filename'], dest.stat().st_size)


for slug in ['playeranimator', 'lionfish-api', 'irons-lib']:
    try:
        dl_mr(slug, force=True)
    except Exception as exc:
        print('ERR', slug, exc)

data = json.load(urllib.request.urlopen(
    urllib.request.Request(
        'https://api.cfwidget.com/minecraft/mc-mods/item-filters',
        headers={'User-Agent': UA},
    )
))
files = [
    f for f in data['files']
    if any('1.20.1' in v for v in f.get('versions', []))
    and 'build.5' in f['name']
]
f = sorted(files, key=lambda x: x['id'], reverse=True)[0]
name = f['name']
for old in MODS.glob('item-filters-forge-*.jar'):
    print('REMOVE', old.name)
    old.unlink()
dest = MODS / name
dest.write_bytes(urllib.request.urlopen(
    urllib.request.Request(edge_url(f['id'], name), headers={'User-Agent': UA}),
    timeout=120,
).read())
print('OK cf item-filters', name, dest.stat().st_size)
