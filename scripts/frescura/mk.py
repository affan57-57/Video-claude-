import re,sys,subprocess
for q in sys.argv[1:]:
    t=subprocess.run(['curl','-sS','-m','20',f'https://mixkit.co/free-stock-video/discover/{q}/'],capture_output=True,text=True).stdout
    slugs=list(dict.fromkeys(re.findall(r'/free-stock-video/([a-z0-9-]+-(\d{3,6}))/',t)))
    print('==',q,len(slugs))
    for s,i in slugs[:16]: print('  ',i,s[:-len(i)-1])
