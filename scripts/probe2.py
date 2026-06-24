import json, urllib.request
UA='MyModPack/1.0'
def search(q):
    import urllib.parse
    facets=json.dumps([["project_type:mod"],["versions:1.20.1"]])
    url='https://api.modrinth.com/v2/search?'+urllib.parse.urlencode({'query':q,'limit':8,'facets':facets})
    for h in json.load(urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':UA})))['hits']:
        print(h['slug'], h['title'])
    print('---')

for q in ['Alexs Caves','Twilight Forest','FTB Quests','Bosses of Mass Destruction','AE2 Things','Spice of Life Carrot','Repurposed Structures']:
    print('Q',q); search(q)

# aether forge-only versions
vs=json.load(urllib.request.urlopen(urllib.request.Request('https://api.modrinth.com/v2/project/aether/version?game_versions=%5B%221.20.1%22%5D',headers={'User-Agent':UA})))
for v in vs[:15]:
    if 'forge' in v.get('loaders',[]) and 'neoforge' not in v.get('loaders',[]):
        print('AETHER FORGE', v['version_number'], v['files'][0]['filename'])
