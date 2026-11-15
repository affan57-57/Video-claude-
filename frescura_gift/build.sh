cd "$(dirname "$0")/proj" && python3 -c "
import json
w=json.load(open('assets/words.json')); s=open('../index.tpl.html').read()
s=s.replace('__WORDS__',json.dumps(w,separators=(',',':'))).replace('__DUR__','30.8').replace('__S9D__','4.7')
open('index.html','w').write(s)"
