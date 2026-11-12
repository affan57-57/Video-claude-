import re,sys,subprocess
def get(u): return subprocess.run(['curl','-sS','-m','20',u],capture_output=True,text=True).stdout
kind=sys.argv[1]
for q in sys.argv[2:]:
    t=get(f'https://mixkit.co/free-{kind}/discover/{q}/') or ''
    if len(t)<5000: t=get(f'https://mixkit.co/free-{kind}/{q}/')
    ids=re.findall(r'assets\.mixkit\.co/(?:active_storage/)?(?:sfx|music)/(\d+)/\1-preview\.mp3',t)
    titles=re.findall(r'item-grid-card__title[^>]*>\s*([^<]+?)\s*<',t)
    print('==',q,len(set(ids)))
    seen=[]
    for i in ids:
        if i not in seen: seen.append(i)
    for k,i in enumerate(seen[:12]): print('  ',i, titles[k] if k<len(titles) else '')
