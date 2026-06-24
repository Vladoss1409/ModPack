import json, urllib.request
UA='Mozilla/5.0 MyModPack/1.0'
data=json.load(urllib.request.urlopen(urllib.request.Request('https://api.cfwidget.com/minecraft/mc-mods/the-twilight-forest', headers={'User-Agent':UA})))
files=[f for f in data['files'] if any('1.20.1' in v for v in f.get('versions',[])) and f.get('display')=='release']
f=sorted(files,key=lambda x:x['id'], reverse=True)[0]
print('file', f['id'], f['name'], f['url'])
# try edge CDN
fid=f['id']
edge=f"https://edge.forgecdn.net/files/{str(fid)[:-3]}/{str(fid)[-3:]}/{f['name']}"
print('edge', edge)
req=urllib.request.Request(edge, headers={'User-Agent':UA})
try:
    r=urllib.request.urlopen(req, timeout=30)
    print('edge status', r.status, 'len', r.length)
except Exception as e:
    print('edge err', e)
req2=urllib.request.Request(f['url'], headers={'User-Agent':UA})
try:
    r2=urllib.request.urlopen(req2, timeout=30)
    print('url status', r2.status)
except Exception as e:
    print('url err', e)
