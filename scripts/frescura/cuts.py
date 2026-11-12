import json
gaps=[(2.08,2.42),(4.80,5.34),(10.38,10.88),(14.72,14.86),(14.94,15.20),(18.74,21.44),(22.62,22.90),(24.30,24.52),(25.42,25.70),(26.24,26.46),(27.34,27.84),(28.26,28.38),(29.22,29.44),(30.66,31.06),(31.90,32.26),(33.00,33.14),(34.54,35.18),(40.50,40.62),(42.32,42.62)]
END=44.40; keep=[]; cur=0.0; KEEPGAP=0.10
for a,b in gaps:
    if b-a<=KEEPGAP: continue
    h=KEEPGAP/2; keep.append((cur,a+h)); cur=b-h
keep.append((cur,END))
tot=sum(b-a for a,b in keep); print(len(keep),"segments, total",round(tot,2))
json.dump(keep,open("keep.json","w"))
