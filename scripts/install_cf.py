import json, urllib.request
from pathlib import Path

UA = 'MyModPack/1.0'
MODS = Path(__file__).resolve().parent.parent / 'mods'


def edge_url(fid, name):
    s = str(fid)
    return f'https://edge.forgecdn.net/files/{s[:-3]}/{s[-3:]}/{name}'


def pick_file(data):
    files = [f for f in data.get('files', []) if any('1.20.1' in v for v in f.get('versions', []))]
    files = [f for f in files if f.get('display') == 'release'] or files
    if not files:
        return None
    return sorted(files, key=lambda x: x.get('id', 0), reverse=True)[0]


def dl_cf(slug):
    data = json.load(urllib.request.urlopen(
        urllib.request.Request(
            f'https://api.cfwidget.com/minecraft/mc-mods/{slug}',
            headers={'User-Agent': UA},
        )
    ))
    f = pick_file(data)
    if not f:
        print('FAIL', slug, 'no 1.20.1')
        return
    name = f.get('name')
    if not name.endswith('.jar'):
        name += '.jar'
    dest = MODS / name
    if dest.exists():
        print('SKIP', slug, name)
        return
    url = edge_url(f['id'], name)
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    dest.write_bytes(urllib.request.urlopen(req, timeout=180).read())
    print('OK', slug, name, dest.stat().st_size)


for slug in [
    'the-twilight-forest', 'ftb-quests-forge', 'ftb-library-forge', 'ftb-teams-forge',
    'ftb-chunks', 'ftb-xmod-compat', 'spice-of-life-carrot-edition', 'ae2-things',
]:
    try:
        dl_cf(slug)
    except Exception as e:
        print('ERR', slug, e)

# aether - search modrinth all loaders
vs = json.load(urllib.request.urlopen(
    urllib.request.Request(
        'https://api.modrinth.com/v2/project/aether/version?game_versions=%5B%221.20.1%22%5D',
        headers={'User-Agent': UA},
    )
))
for v in vs:
    if 'forge' in v.get('loaders', []):
        print('aether candidate', v['version_number'], v.get('loaders'), v['files'][0]['filename'])
