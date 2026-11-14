import json
segs=json.load(open('/home/user/work/aud/segs.json')); T=1.22
def m(t):
    acc=0
    for s,e in segs:
        if t<s: return acc/T
        if t<=e: return (acc+t-s)/T
        acc+=e-s
    return acc/T
d=json.load(open('/home/user/work/main_tr2.json')); out=[]
for s in d:
    for w in s['words']:
        if w['s']>=46.08: continue
        out.append(dict(text=w['w'].strip(),start=round(m(w['s']),3),end=round(m(w['e']),3)))
json.dump(out,open('/home/user/work/words_out.json','w'),ensure_ascii=False,indent=0)
print(' '.join(f"{w['text']}@{w['start']:.2f}" for w in out))
