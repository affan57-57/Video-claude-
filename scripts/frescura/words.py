import json,sys
d=json.load(open(sys.argv[1])); prev=0; line=[]
for s in d:
  for w in s['words']:
    line.append(f"{w['s']:.2f}-{w['e']:.2f}({w['s']-prev:+.2f}){w['w'].strip()}"); prev=w['e']
  print("  ".join(line)); line=[]
