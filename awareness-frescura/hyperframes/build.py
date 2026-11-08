import json
src=open("index.src.html.tpl").read()
open("index.html","w").write(src.replace("__CAPTIONS__",json.dumps(json.load(open("captions.json")),ensure_ascii=False)))
