import re, json, sys
GAB = {
 'e1':'7a7c94e6-enam2024r_gabarito_definitivo_-_2024_-_gabarito',
 'e2':'06759caf-enam20242-gabaritos-para-publicacaodpndsa645d1as3_-_2024_segunda_prova_-_gabarito',
 'e3':'d71d3ab1-enam-20251-gabaritos-para-publicacaosssas51c3_-_2025_primeira_prova-_gabarito',
 'e4':'6436c8c3-enam-20252-gabaritos-para-publicacao-v20251028_-_2025_segunda_prova_gabarito',
 'e5':'5bd2cd81-enam-exame-nacional-de-magistratura-2026_primeira_prova_-_gabarito'}
DISC = [(1,16,'Constitucional'),(17,26,'Administrativo'),(27,32,'Humanística'),(33,38,'Direitos Humanos'),(39,50,'Processo Civil'),(51,62,'Civil'),(63,68,'Empresarial'),(69,80,'Penal')]
def disc(n): return next(d for a,b,d in DISC if a<=n<=b)
def gab(k):
    t=open(f'/home/claude/ref/txt/{GAB[k]}.txt').read()
    t=t.split('TIPO 2')[0] if 'TIPO 2' in t else t.split('Tipo 2')[0]
    out={}; lines=[l for l in t.splitlines() if l.strip()]
    i=0
    while i<len(lines)-1:
        nums=re.findall(r'\d+',lines[i]); lets=re.findall(r'(?<![A-Za-z])([A-E*])(?![A-Za-z])',lines[i+1])
        if len(nums)==20 and len(lets)==20:
            for n,l in zip(nums,lets): out[int(n)]=l
            i+=2
        else: i+=1
    return out
res={}
for k in GAB:
    t=open(f'/home/claude/ref/txt/{k}_c.txt').read()
    lines=[l for l in t.splitlines() if not re.search(r'ESCOLA NACIONAL DE FORMA|FGV CONHECIMENTO|PÁGINA \d+|^TIPO|Exame Nacional da Magistratura$|^Realização',l)]; qs={}; cur=None; exp=1
    for l in lines:
        s=l.strip()
        if s==str(exp) :
            cur=exp; qs[cur]=[]; exp+=1; continue
        if cur: qs[cur].append(s)
    g=gab(k)
    res[k]=[{'n':n,'disc':disc(n),'gab':g.get(n),'txt':re.sub(r'\s+',' ',' '.join(v)).strip()} for n,v in qs.items()]
    print(k,len(qs),len(g), sum(1 for q in res[k] if len(q['txt'])<150))
json.dump(res,open('/home/claude/ref/provas.json','w'),ensure_ascii=False)
