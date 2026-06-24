import json, urllib.parse, urllib.request
UA='MyModPack/1.0'
def search(q):
    facets = json.dumps([["project_type:mod"], ["versions:1.20.1"]])
    url='https://api.modrinth.com/v2/search?' + urllib.parse.urlencode({'query': q, 'limit': 5, 'facets': facets})
    r=urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}))
    for hit in json.load(r)['hits']:
        print(f"  {hit['slug']} | {hit['title']} | {hit.get('loaders')}")
queries = ['immersive engineering forge','twilight forest','ae2 things','storage drawers','undergarden','cataclysm forge','alex caves','sol carrot','ftb quests forge','ferritecore forge','repurposed structures datapack','aether forge 1.20.1','inventory sorter forge','openblocks elevator','bad wither no cookie']
for q in queries:
    print('Q:', q)
    search(q)
    print('---')
