import json
T=1.12
segs=json.load(open('segs.json'))
def m(t):
    acc=0
    for a,b in segs:
        if t<a: return acc/T
        if t<=b: return (acc+t-a)/T
        acc+=b-a
    return acc/T
d=json.load(open('main_tx.json'))
ws=[w for s in d for w in s['words'] if w['s']<43.8]
fix={0:'Korang',24:'selesa',57:'menikmati',63:'Frescura',64:None,65:'Body',69:'Buih',71:'garam',72:'laut',80:'Bombshell',82:'Midnight',83:'Fantasy.',85:'rugi',95:'Tekan',96:'beg',99:'check',100:None,101:'out',105:'Frescura',106:None,107:'Body'}
out=[]
for i,w in enumerate(ws):
    txt=w['w'].strip()
    print(i,txt,end=' | ')

print()
P=[(0,3,"Korang tak *takut* ke"),(4,6,"kalau perkara *kecil*"),(7,10,"yang korang selalu *abaikan*"),(11,14,"akhirnya buat *pasangan* korang"),(15,17,"*tak selesa* nak dekat?"),
(18,22,"Antara perkara yang kita kena"),(23,25,"*ambil berat* ialah"),(26,27,"*kebersihan* badan,"),(28,29,"*bau* badan"),(30,31,"dan *pakaian*"),(32,35,"dan jangan pandang *ringan*"),(36,38,"*rutin* penjagaan diri"),(39,42,"walaupun dah lama *berkahwin*"),
(43,47,"Diri sendiri pun *kena jaga*."),(48,51,"Kalau nak sentiasa menjaga"),(52,54,"*kebersihan* dan menikmati"),(55,58,"pengalaman *mandi* yang menyenangkan"),(59,59,"pastinya"),(60,62,"*Frescura Body*"),(63,64,"menjadi *pilihan*"),
(65,66,"*Buih lembut*,"),(67,68,"*garam laut*"),(69,71,"dan wangian *feminine*"),(72,75,"dalam satu botol iaitu"),(76,76,"*Bombshell*"),(77,79,"dan *Midnight Fantasy*"),
(80,82,"So *rugi* tau"),(83,86,"kalau dah tau *kelebihannya*"),(87,91,"tapi masih *tangguh* nak cuba"),(92,94,"*Tekan beg kuning*"),(95,98,"dan *check out* sekarang"),(99,103,"sebab stok *Frescura Body*"),(104,106,"memang *tak banyak*!")]
caps=[]
for i0,i1,txt in P:
    s=m(ws[i0]['s']); e=m(ws[i1]['e'])
    toks=txt.split(' '); 
    # distribute token times across source words proportionally
    n=len(toks); srcw=[(m(ws[k]['s']),m(ws[k]['e'])) for k in range(i0,i1+1)]
    tt=[srcw[min(len(srcw)-1,int(j*len(srcw)/n))][0] for j in range(n)]
    caps.append(dict(s=round(s,3),e=round(e,3),toks=toks,tt=[round(x,3) for x in tt]))
    print(f"{s:6.2f}-{e:6.2f} {txt}")
json.dump(caps,open('caps.json','w'),ensure_ascii=False,indent=0)
