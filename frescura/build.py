import sys
P,W=sys.argv[1],sys.argv[2]
DUR=31.6; VO=0.5
h=open(P+"/../src/index.template.html").read()
h=h.replace("__WORDS__",open(W+"/words_compact.json").read().strip()).replace("__ENDDUR__",f"{DUR-27.96:.2f}").replace("__DUR__",str(DUR)).replace("__VO__",str(VO))
open(P+"/index.html","w").write(h)
