import json, math
from collections import Counter, defaultdict
INC=json.load(open('incidencia.json'))
ITENS={ # todos os grupos do edital (inclui os sem incidência)
'Constitucional':['C01 Teoria/poder constituinte/emendas','C03 Eficácia/aplicabilidade/recepção','C06 Direitos fundamentais (teoria, expressão, privacidade)','C07 Garantias processuais/prova/prisão','C08 Direitos sociais','C08t Constitucional do Trabalho','C09 Federação/competências/intervenção','C10 Legislativo/processo legislativo/TCU','C11 Executivo/Adm Pública/servidores','C12 Judiciário/funções essenciais','C13 Defesa do Estado/segurança pública','C14 Tributário/finanças','C15 Controle de constitucionalidade'],
'Administrativo':['A01 Princípios/LINDB','A04 Organização (órgãos, indireta, estatais)','A05 Ato administrativo','A07 Processo administrativo','A08 Licitação','A09 Contratos administrativos','A10-11 Poder de polícia/intervenção na propriedade','A12-13 Serviços públicos/concessões/PPP','A15 Regulação/agências/LGPD/liberdade econômica','A16 Agentes públicos','A17 Bens públicos','A18 Controle/Tribunais de contas','A19 MS/ação popular/ACP/improbidade','A20 Responsabilidade civil do Estado','A21 Prescrição/decadência'],
'Humanística':['H1 Sociologia do direito','H2 Psicologia judiciária/conflitos','H3 Ética/estatuto da magistratura','H4 Filosofia do direito','H5 Teoria geral do direito/gênero','H7 Direito digital/tecnologia','H8 Cognição/decisão/AED','H9 Antidiscriminação'],
'Direitos Humanos':['DH1 Teoria geral/empresas','DH2 Sistema global (ONU)','DH3 Sistema interamericano/Corte IDH','DH4 Controle de convencionalidade','DH5-8 Incorporação/hierarquia/CF','DH7 Jurisprudência STF em DH','DH9 Povos originários'],
'Processo Civil':['P01 Normas fundamentais/NJP','P02 Jurisdição/impedimento/suspeição','P03 Competência/cooperação','P04-05 Ação/partes/terceiros','P06 Atos/prazos/nulidades','P07 Petição inicial/resposta/saneamento','P08 Provas','P09-11 Sentença/coisa julgada','P10 Tutela provisória','P12-15 Precedentes/recursos/IRDR/rescisória','P16-19 Execução/cumprimento','P20-21 Proced. especiais/Fazenda/MS','P22 Juizados','P23 Coletivo/estrutural','P24 Custas/honorários/gratuidade','P25-26 Autocomposição/arbitragem'],
'Civil':['V01 LINDB/constitucionalização/DIP','V02 Pessoas naturais/personalidade/capacidade','V03 Pessoa jurídica/desconsideração','V04 Bens/bem de família','V05 Negócio jurídico/defeitos/prescrição','V06 Obrigações','V07 Teoria geral dos contratos','V08 Contratos em espécie/atos unilaterais','V09 Responsabilidade civil','V10-11 Posse/propriedade/usucapião/registro','V12-14 Condomínio/fiduciária/garantias','V16-17 ECA/idoso/PcD','V18 Marco Civil/LGPD','V19 Família e sucessões','V20 Consumidor'],
'Empresarial':['E02 Empresário/teoria da empresa','E03 Títulos de crédito/protesto','E04 Sociedades (geral/não personificadas/simples)','E05 Limitada e S.A.','E06 Operações societárias/desconsideração','E07 Estabelecimento/trespasse/nome','E08 Contratos empresariais','E09 Bancários/SFN','E10 Recuperação/falência','E11 Propriedade industrial','E12 Consumo/comércio eletrônico'],
'Penal':['D01-03 Princípios/lei penal no tempo e espaço','D04-06 Teoria do crime/tipicidade/dolo/culpa','D07 Iter criminis','D08-10 Ilicitude/culpabilidade/imputabilidade','D11 Concurso de agentes','D12 Penas/concurso de crimes/conflito aparente','D13-16 Efeitos/reabilitação/medida de segurança/ação penal','D17 Extinção da punibilidade/prescrição','D18 Penal econômico/PJ','D19-20 Penal militar/tratados','D21a Crimes contra a pessoa/honra','D21b Crimes contra o patrimônio','D21c Dignidade sexual','D21d Fé pública/Adm Pública/Adm justiça','D21e Leis 7.716/12.288/13.869'],
}
ERROS=Counter({'C15':2,'C07':1,'C14':1,'A15':1,'A04':1,'A19':1,'A08':1,'H1':1,'H5':1,'DH9':1,'DH3':1,'P25-26':1,'P07':1,'P23':1,'V06':2,'V08':2,'E03':1,'E04':1,'D21b':1,'D21e':1,'D12':1,'D07':1,'D01-03':1,'D21d':1})
SERIE={'Penal':8,'Civil':7,'Constitucional':7,'Administrativo':6,'Processo Civil':5,'Humanística':3,'Direitos Humanos':2,'Empresarial':2}
PROVA={'Constitucional':16,'Administrativo':10,'Humanística':6,'Direitos Humanos':6,'Processo Civil':12,'Civil':12,'Empresarial':6,'Penal':12}
NS,NM=21,3
def peso(d,it): return INC.get(d,{}).get(it,0)+1.0+1.5*ERROS[it.split(' ')[0]]
def distribuir(total,d):
    its=ITENS[d]; w={i:peso(d,i) for i in its}; W=sum(w.values())
    q={i:max(2,math.floor(total*w[i]/W)) for i in its}
    while sum(q.values())<total:
        i=max(its,key=lambda i: total*w[i]/W-q[i]); q[i]+=1
    while sum(q.values())>total:
        i=max((i for i in its if q[i]>2),key=lambda i: q[i]-total*w[i]/W); q[i]-=1
    return q
def sequencia(quotas,slots):
    tot=sum(quotas.values()); feito={i:0 for i in quotas}; seq=[]; acum=0
    for nslot in slots:
        acum+=nslot; esc=[]
        for _ in range(nslot):
            cand=[i for i in quotas if feito[i]<quotas[i]]
            def score(i): return (quotas[i]*acum/tot - feito[i]) - (10*esc.count(i))
            i=max(cand,key=score); esc.append(i); feito[i]+=1
        seq.append(esc)
    return seq
mat={'disciplinas':{},'cadernos':{}}
cad=[f'S{i:02d}' for i in range(1,NS+1)]; sims=[f'M{i}' for i in range(1,NM+1)]
for d in ITENS:
    tot=SERIE[d]*NS+PROVA[d]*NM
    q=distribuir(tot,d)
    mat['disciplinas'][d]={'total':tot,'itens':[{'item':i,'incid5provas':INC.get(d,{}).get(i,0),'errosSimulado':ERROS[i.split(' ')[0]],'questoes':q[i]} for i in ITENS[d]]}
    # ordem: simulados e séries intercaladas cronologicamente
    ordem=[]; 
    for w in range(4):
        ordem += cad[w*6:w*6+6] if w<3 else cad[18:]
        if w<3: ordem.append(sims[w])
    seq=sequencia(q,[PROVA[d] if c.startswith('M') else SERIE[d] for c in ordem])
    for c,s in zip(ordem,seq): mat['cadernos'].setdefault(c,{})[d]=s
json.dump(mat,open('/home/claude/app/data/matriz.json','w'),ensure_ascii=False,indent=1)
for d,v in mat['disciplinas'].items():
    print(f"\n## {d} — {v['total']} questões")
    for it in v['itens']: print(f"  {it['questoes']:3d}  (5 provas: {it['incid5provas']:2d}, erros: {it['errosSimulado']})  {it['item']}")
print('\nS01:',json.dumps(mat['cadernos']['S01'],ensure_ascii=False)[:1500])
