import re,sys,subprocess,json
from concurrent.futures import ThreadPoolExecutor
def get(u): return subprocess.run(['curl','-sS','-m','20',u],capture_output=True,text=True).stdout
def chk(s):
    t=get(f'https://mixkit.co/free-stock-video/{s}/')
    lic=re.search(r'"copyrightNotice":"([^"]+)"',t); i=s.rsplit('-',1)[1]
    us=sorted(set(re.findall(rf'https://assets.mixkit.co/videos/{i}/{i}-(\d+)\.mp4',t)),key=int)
    return s,(lic.group(1) if lic else '?'),us
for q in sys.argv[1:]:
    t=get(f'https://mixkit.co/free-stock-video/discover/{q}/')
    slugs=list(dict.fromkeys(m.group(1) for m in re.finditer(r'/free-stock-video/([a-z0-9-]+-\d{2,6})/',t)))[:14]
    with ThreadPoolExecutor(8) as ex: R=list(ex.map(chk,slugs))
    print('==',q)
    for s,l,u in R:
        if l=='Free': print('  ',s,u)
