"""Banco ENAM da Karina — monta dist/index.html.
Questões próprias: data/serieNN_*.json e data/simuladoNN_*.json  (campos: disc,item,nivel,tema,enun,alts[[txt,com]x5],c,base,dica,fixa?)
Questões reais: data/reais.json (texto) + data/reais_coment.json (comentários) + matriz.json['reais'] (alocação por caderno)
"""
import json, glob, random, re, os, datetime as dt
ROOT=os.path.dirname(os.path.abspath(__file__)); DATA=os.path.join(ROOT,'data')
ORDEM=["Direito Constitucional","Direito Administrativo","Noções Gerais de Direito e Formação Humanística","Direitos Humanos","Direito Processual Civil","Direito Civil","Direito Empresarial","Direito Penal"]
CURTO={"Constitucional":"Direito Constitucional","Administrativo":"Direito Administrativo","Humanística":"Noções Gerais de Direito e Formação Humanística","Direitos Humanos":"Direitos Humanos","Processo Civil":"Direito Processual Civil","Civil":"Direito Civil","Empresarial":"Direito Empresarial","Penal":"Direito Penal"}
FOCOS={"S01":"Diagnóstico — temas dos erros do simulado + os mais cobrados pela FGV","S02":"Penal e Administrativo em destaque","S03":"Civil e Empresarial em destaque","S04":"Constitucional (trabalho e tributário) e DH","S05":"Processo Civil e Humanística","S06":"Correção ativa do Simulado 1","S07":"Civil (família, sucessões, reais)","S08":"Constitucional (organização do Estado e Judiciário)","S09":"Processo Civil (recursos, execução)","S10":"Penal (parte especial) e criminologia","S11":"Administrativo e DH","S12":"Correção ativa do Simulado 2","S13":"Civil e Processo Civil — teses repetitivas","S14":"Constitucional e Administrativo — STF recente","S15":"Penal e Empresarial","S16":"Humanística e DH","S17":"Mista no formato da prova","S18":"Correção ativa do Simulado 3","S19":"Mista — súmulas e teses mais cobradas","S20":"Mista — lei seca","S21":"Revisão final — caderno de erros"}
def cronograma():
    dias=[]; d=dt.date(2026,11,3); s=m=0; sem=["seg","ter","qua","qui","sex","sáb","dom"]
    while d<=dt.date(2026,11,29):
        wd=d.weekday(); it={"data":d.isoformat(),"dia":f"{d.day:02d}/11","sem":sem[wd]}
        if d==dt.date(2026,11,29): it.update(tipo="prova",id="prova",titulo="6º ENAM",foco="13h às 18h · portões fecham 12h30 · caneta preta transparente + documento")
        elif d==dt.date(2026,11,28): it.update(tipo="descanso",id="d28",titulo="Descanso",foco="Sem questões novas. Confira local de prova, documento e caneta.")
        elif d==dt.date(2026,11,27): it.update(tipo="revisao",id="r27",titulo="Revisão leve",foco="Só as dicas do caderno de erros. Máximo 2 horas.")
        elif wd==6: m+=1; it.update(tipo="simulado",id=f"M{m}",titulo=f"Simulado {m}",foco="80 questões, 13h–18h, modo Prova",n=80)
        else: s+=1; sid=f"S{s:02d}"; it.update(tipo="serie",id=sid,titulo=f"Série {s}",foco=FOCOS.get(sid,"Série mista"),n=40)
        dias.append(it); d+=dt.timedelta(days=1)
    return dias
def norm_item(code,M,disc):
    for d,v in M['disciplinas'].items():
        for it in v['itens']:
            if it['item'].split(' ')[0]==code: return it['item']
    return code
def montar(cid,M,rnd):
    proprias=[]
    pref='serie' if cid.startswith('S') else 'simulado'; num=int(cid[1:])
    for f in sorted(glob.glob(os.path.join(DATA,f'{pref}{num:02d}_*.json'))): proprias+=json.load(open(f,encoding='utf-8'))
    if not proprias: return None
    R={r['id']:r for r in json.load(open(os.path.join(DATA,'reais.json'),encoding='utf-8'))}
    C=json.load(open(os.path.join(DATA,'reais_coment.json'),encoding='utf-8'))
    reais=[]
    for d,picks in M['reais'].get(cid,{}).items():
        for p in picks:
            r=R[p['id']]
            if p['id'] not in C: continue
            c=C[p['id']]; gi='ABCDE'.index(r['gab'])
            reais.append({"disc":CURTO[r['disc']],"item":r['item'],"nivel":c['nivel'],"tema":c['tema'],"enun":r['enun'],"alts":[[a,c['coms'][i]] for i,a in enumerate(r['alts'])],"c":gi,"base":c['base'],"dica":c['dica'],"fixa":True,"origem":r['origem']})
    out=[]
    for disc in ORDEM:
        own=[q for q in proprias if q['disc']==disc]; rr=[q for q in reais if q['disc']==disc]
        mix=[]
        while own or rr:
            if own: mix.append(own.pop(0))
            if rr: mix.append(rr.pop(0))
        out+=mix
    # embaralha alternativas das próprias (gabarito equilibrado)
    alvo=[]
    while len(alvo)<len(out): b=list(range(5)); rnd.shuffle(b); alvo+=b
    res=[]
    for i,q in enumerate(out):
        alts,c=q['alts'],q['c']
        if not q.get('fixa'):
            certo=alts[c]; outras=[a for j,a in enumerate(alts) if j!=c]; rnd.shuffle(outras); pos=alvo[i]
            alts=outras[:pos]+[certo]+outras[pos:]; c=pos
        assert len(alts)==5 and alts[c][1].startswith('CORRETA'), (cid,q['tema'])
        item=q.get('item',''); item=item if ' ' in item else norm_item(item,M,q['disc'])
        res.append({"n":i+1,"disc":q['disc'],"tema":q['tema'],"item":item,"nivel":q.get('nivel','médio'),"origem":q.get('origem','Inédita'),
                    "enun":q['enun'],"alts":[a[0] for a in alts],"coms":[a[1] for a in alts],"c":c,"base":q.get('base',''),"dica":q.get('dica','')})
    return res
import hashlib
def qid(q): return q['origem'].split(' – ')[0].replace('ENAM ','F')+'-'+q['origem'].split('Q')[-1] if q['origem']!='Inédita' else 'i-'+hashlib.sha1(q['enun'].encode()).hexdigest()[:8]
def main():
    M=json.load(open(os.path.join(DATA,'matriz.json'),encoding='utf-8'))
    banco={}; sims={}
    nums=sorted({int(re.match(r'serie(\d+)_',os.path.basename(f)).group(1)) for f in glob.glob(os.path.join(DATA,'serie*_*.json'))})
    for cid in [f'S{i:02d}' for i in nums]+['M1','M2','M3']:
        q=montar(cid,M,random.Random(int(hashlib.md5(cid.encode()).hexdigest(),16)%9973))
        if not q: continue
        for x in q: x['id']=qid(x)
        if cid.startswith('M'): sims[cid]=q
        else:
            for x in q: banco[x['id']]=x
    banco=list(banco.values())
    # códigos estáveis e visíveis
    SIG={"Direito Constitucional":"CON","Direito Administrativo":"ADM","Noções Gerais de Direito e Formação Humanística":"HUM","Direitos Humanos":"DHU","Direito Processual Civil":"PCI","Direito Civil":"CIV","Direito Empresarial":"EMP","Direito Penal":"PEN"}
    fc=os.path.join(DATA,'codigos.json'); cods=json.load(open(fc,encoding='utf-8')) if os.path.exists(fc) else {}
    todas=banco+[x for v in sims.values() for x in v]
    for x in todas:
        if x['id'] in cods: continue
        if x['origem']!='Inédita': cods[x['id']]=x['origem'].replace('ENAM ','FGV ').replace(' – ','-')
        else:
            sg=SIG[x['disc']]; n=1+sum(1 for c in cods.values() if c.startswith(sg+'-'))
            cods[x['id']]=f"{sg}-{n:04d}"
    for x in todas: x['cod']=cods[x['id']]
    json.dump(cods,open(fc,'w',encoding='utf-8'),ensure_ascii=False,indent=0)
    cob={d:[{"item":it['item'],"plan":it['questoes'],"inc":it['incid5provas']} for it in v['itens']] for d,v in M['disciplinas'].items()}
    dados={"gerado":dt.datetime.now().strftime("%d/%m/%Y %H:%M"),"banco":banco,"sims":sims,"simsPlan":["M1","M2","M3"],"cobertura":cob,
           "diag":json.load(open(os.path.join(DATA,'diagnostico.json'),encoding='utf-8'))}
    tpl=open(os.path.join(ROOT,'template.html'),encoding='utf-8').read()
    js=json.dumps(dados,ensure_ascii=False).replace('</','<\\/')
    os.makedirs(os.path.join(ROOT,'dist'),exist_ok=True)
    open(os.path.join(ROOT,'dist','index.html'),'w',encoding='utf-8').write(tpl.replace('/*__DADOS__*/null',js))
    from collections import Counter
    print('banco',len(banco),'| gab',dict(Counter('ABCDE'[q['c']] for q in banco)),'| nível',dict(Counter(q['nivel'] for q in banco)),'| reais',sum(q['origem']!='Inédita' for q in banco),'| disc',dict(Counter(q['disc'][:12] for q in banco)))
    print('simulados',{k:len(v) for k,v in sims.items()})
if __name__=='__main__': main()
