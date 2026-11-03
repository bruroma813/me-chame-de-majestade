import json,re
from collections import Counter,defaultdict
P=json.load(open('provas.json'))
R={
'Constitucional':{
 'C01 Teoria/poder constituinte/emendas':r'poder constituinte|emenda constitucional|muta[çc][ãa]o|cl[áa]usula p[ée]trea|neoconstitucional|preâmbulo|ADCT',
 'C03 Eficácia/aplicabilidade/recepção':r'recep[çc][ãa]o|efic[áa]cia limitada|efic[áa]cia contida|repristina|desconstitucionaliza',
 'C06 Direitos fundamentais (teoria, expressão, privacidade)':r'liberdade de express|imprensa|intimidade|honra|efic[áa]cia horizontal|rela[çc][õo]es privadas|reuni[ãa]o|religi|transg[êe]nero|nacionalidade|direitos pol[íi]ticos|inelegib',
 'C07 Garantias processuais/prova/prisão':r'presun[çc][ãa]o de inoc|n[ãa]o culpabilidade|pris[ãa]o|prova il[íi]cita|intercepta|algema|flagrante|habeas corpus|tribunal do j[úu]ri',
 'C08 Direitos sociais':r'sa[úu]de|medicamento|educa[çc][ãa]o|moradia|greve|sindica|trabalhador|previd[êe]ncia|mínimo existencial|retrocesso|meio ambiente|ind[íi]gena|defici[êe]ncia|quilombol',
 'C09 Federação/competências/intervenção':r'compet[êe]ncia (legislativa|privativa|concorrente|comum)|interven[çc][ãa]o|munic[íi]pio.*lei|lei estadual|lei municipal|federativ',
 'C10 Legislativo/processo legislativo/TCU':r'processo legislativo|medida provis[óo]ria|iniciativa|(?-i:\bCPI\b)|comiss[ãa]o parlamentar|imunidade parlamentar|Tribunal de Contas|san[çc][ãa]o.*veto|veto',
 'C11 Executivo/Adm Pública/servidores':r'Presidente da Rep[úu]blica.*crime de responsabilidade|servidor|remunera|teto|concurso p[úu]blico|ag[êe]ncia reguladora|recomposi',
 'C12 Judiciário/funções essenciais':r'(?-i:\bCNJ\b)|Conselho Nacional de Justi[çc]a|magistrad|quinto constitucional|Minist[ée]rio P[úu]blico|Defensoria|Justi[çc]a do Trabalho|Justi[çc]a Federal|compet[êe]ncia.*(STF|(?-i:\bSTJ\b)|TST)|precat[óo]rio',
 'C13 Defesa do Estado/segurança pública':r'estado de defesa|estado de s[íi]tio|For[çc]as Armadas|seguran[çc]a p[úu]blica|guarda municipal|pol[íi]cia',
 'C14 Tributário/finanças':r'tribut|imposto|contribui[çc][ãa]o|imunidade|isen[çc][ãa]o|anterioridade|repart|or[çc]ament|(?-i:\bICMS\b)|(?-i:\bIPVA\b)',
 'C15 Controle de constitucionalidade':r'(?-i:\bADI\b)|(?-i:\bADC\b)|(?-i:\bADPF\b)|(?-i:\bADO\b)|controle (concentrado|difuso|de constitucionalidade)|reserva de plen[áa]rio|modula[çc][ãa]o|inconstitucionalidade|mandado de injun|reclama[çc][ãa]o',
},
'Administrativo':{
 'A01 Princípios/LINDB':r'(?-i:\bLINDB\b)|consequ[êe]ncias pr[áa]ticas|princ[íi]pio da (legalidade|moralidade|impessoalidade|efici[êe]ncia|publicidade)|nepotismo|razoabilidade|proporcionalidade',
 'A04 Organização (órgãos, indireta, estatais)':r'[óo]rg[ãa]os? p[úu]blic|autarquia|funda[çc][ãa]o p[úu]blica|empresa p[úu]blica|sociedade de economia mista|cons[óo]rcio p[úu]blico|13\.303|descentraliza|desconcentra|estatal',
 'A05 Ato administrativo':r'ato administrativo|anula[çc][ãa]o|revoga[çc][ãa]o|convalida|motivo|desvio de (poder|finalidade)|vinculad|discricion',
 'A07 Processo administrativo':r'9\.784|processo administrativo|decis[ãa]o coordenada|(?-i:\bPAD\b)|sindic[âa]ncia|disciplinar',
 'A08 Licitação':r'licita|14\.133|preg[ãa]o|di[áa]logo competitivo|concorr[êe]ncia|dispensa|inexigib|contrata[çc][ãa]o direta',
 'A09 Contratos administrativos':r'contrato administrativo|equil[íi]brio econ[ôo]mico|reajuste|repactua|cl[áa]usulas? exorbitant|rescis[ãa]o|extin[çc][ãa]o do contrato|fato do pr[íi]ncipe|matriz de risco',
 'A10-11 Poder de polícia/intervenção na propriedade':r'poder de pol[íi]cia|desapropria|tombamento|servid[ãa]o administrativa|requisi[çc][ãa]o|limita[çc][ãa]o administrativa|ocupa[çc][ãa]o tempor|3\.365|san[çc][ãa]o administrativa',
 'A12-13 Serviços públicos/concessões/PPP':r'servi[çc]o p[úu]blico|concess[ãa]o|permiss[ãa]o|(?-i:\bPPP\b)|parceria p[úu]blico|8\.987|11\.079|usu[áa]rio|13\.460|encampa|caducidade',
 'A15 Regulação/agências/LGPD/liberdade econômica':r'ag[êe]ncia reguladora|13\.848|regula[çc][ãa]o|(?-i:\bLGPD\b)|13\.709|dados pessoais|liberdade econ[ôo]mica|13\.874',
 'A16 Agentes públicos':r'servidor|cargo|concurso|estabilidade|est[áa]gio probat|acumula[çc][ãa]o|agente p[úu]blico|aposentadoria|teto',
 'A17 Bens públicos':r'bens? p[úu]blic|terras devolutas|terreno de marinha|afeta[çc][ãa]o|desafeta',
 'A18 Controle/Tribunais de contas':r'Tribunal de Contas|controle (externo|interno)|(?-i:\bTCU\b)',
 'A19 MS/ação popular/ACP/improbidade':r'improbidade|8\.429|14\.230|a[çc][ãa]o popular|mandado de seguran[çc]a|indisponibilidade',
 'A20 Responsabilidade civil do Estado':r'responsabilidade civil do Estado|37, ?§ ?6|responsabilidade objetiva|indeniza',
 'A21 Prescrição/decadência':r'prescri[çc][ãa]o|decad[êe]ncia|20\.910',
},
'Humanística':{
 'H1 Sociologia do direito':r'sociolog|controle social|Durkheim|Weber|Luhmann|Bourdieu|Marx|fato social|pluralismo jur[íi]dico',
 'H2 Psicologia judiciária/conflitos':r'psicolog|ass[ée]dio|media[çc][ãa]o|negocia[çc][ãa]o|conflito|testemunh|mem[óo]ria|comunica[çc][ãa]o',
 'H3 Ética/estatuto da magistratura':r'[ÉE]tica|(?-i:\bLOMAN\b)|magistrad|Bangalore|Corregedoria|promo[çc][ãa]o|remo[çc][ãa]o|vitalic|Código Ibero',
 'H4 Filosofia do direito':r'justi[çc]a|Arist[óo]teles|Rawls|Kant|equidade|moral|l[óo]gica do razo[áa]vel|Recas[ée]ns|Perelman|Habermas',
 'H5 Teoria geral do direito/gênero':r'fontes do direito|norma jur[íi]dica|Kelsen|Hart|Dworkin|Alexy|Bobbio|precedente|g[êe]nero|patriarcado|perspectiva de g[êe]nero|hermen[êe]utica|interpreta[çc][ãa]o',
 'H7 Direito digital/tecnologia':r'intelig[êe]ncia artificial|tecnolog|digital|algoritm|blockchain|cripto|jurimetria|inova[çc][ãa]o|Resolu[çc][ãa]o (CNJ )?n[º°] ?(332|395|615|345|354)',
 'H8 Cognição/decisão/AED':r'vi[ée]s|heur[íi]stic|an[áa]lise econ[ôo]mica|pragmatismo|consequencialismo|utilitar|economia comportamental|compliance|lavagem|whistleblow',
 'H9 Antidiscriminação':r'discrimina|racismo|a[çc][õo]es afirmativas|LGBT|antidiscrimina|interseccional',
},
'Direitos Humanos':{
 'DH1 Teoria geral/empresas':r'empresa|Ruggie|gera[çc][õo]es|dimens[õo]es|universalismo|relativismo',
 'DH2 Sistema global (ONU)':r'(?-i:\bONU\b)|Na[çc][õo]es Unidas|Comit[êe]|Pacto Internacional|Conselho de Direitos Humanos|Revis[ãa]o Peri[óo]dica',
 'DH3 Sistema interamericano/Corte IDH':r'Corte Interamericana|Comiss[ãa]o Interamericana|Corte IDH|Pacto de S[ãa]o Jos[ée]|caso .* vs\.? Brasil|Conven[çc][ãa]o Americana|opini[ãa]o consultiva',
 'DH4 Controle de convencionalidade':r'convencionalidade',
 'DH5-8 Incorporação/hierarquia/CF':r'incorpora|supralegal|§ ?3[º°]|hierarquia|tratados? internaciona|status',
 'DH7 Jurisprudência STF em DH':r'Supremo Tribunal Federal|(?-i:\bSTF\b)',
 'DH9 Povos originários':r'ind[íi]gena|origin[áa]rio|169|tribais|quilombol',
},
'Processo Civil':{
 'P01 Normas fundamentais/NJP':r'normas fundamentais|neg[óo]cio jur[íi]dico processual|cooperação|boa-f[ée]|contradit[óo]rio|vedação.*surpresa',
 'P02 Jurisdição/impedimento/suspeição':r'impedimento|suspei[çc][ãa]o|jurisdi[çc][ãa]o volunt',
 'P03 Competência/cooperação':r'compet[êe]ncia|conex[ãa]o|contin[êe]ncia|preven[çc][ãa]o|coopera[çc][ãa]o judici|foro',
 'P04-05 Ação/partes/terceiros':r'legitimidade|litiscons[óo]rcio|interven[çc][ãa]o de terceiro|denuncia[çc][ãa]o|chamamento|assist[êe]ncia|amicus|desconsidera[çc][ãa]o|litig[âa]ncia de m[áa]-f[ée]',
 'P06 Atos/prazos/nulidades':r'prazo|intima[çc][ãa]o|cita[çc][ãa]o|nulidade|ato processual|audi[êe]ncia (virtual|remota|h[íi]brida)|ju[íi]zo 100',
 'P07 Petição inicial/resposta/saneamento':r'peti[çc][ãa]o inicial|valor da causa|pedido|contesta[çc][ãa]o|reconven[çc][ãa]o|saneamento|improced[êe]ncia liminar|revelia',
 'P08 Provas':r'prova|per[íi]cia|[ôo]nus da prova|testemunha|ata notarial',
 'P09-11 Sentença/coisa julgada':r'senten[çc]a|coisa julgada|fundamenta[çc][ãa]o|preclus[ãa]o|julgamento antecipado',
 'P10 Tutela provisória':r'tutela (provis[óo]ria|de urg[êe]ncia|de evid[êe]ncia|antecipada|cautelar)|estabiliza[çc][ãa]o',
 'P12-15 Precedentes/recursos/IRDR/rescisória':r'recurso|apela[çc][ãa]o|agravo|embargos de declara|recurso especial|extraordin[áa]rio|(?-i:\bIRDR\b)|repetitiv|rescis[óo]ria|reclama[çc][ãa]o|precedente|julgamento estendido|remessa necess',
 'P16-19 Execução/cumprimento':r'execu[çc][ãa]o|cumprimento (provis[óo]rio )?de senten[çc]a|penhora|fraude [àa] execu|impugna[çc][ãa]o|embargos [àa] execu|t[íi]tulo executivo|alimentos|precat',
 'P20-21 Proced. especiais/Fazenda/MS':r'procedimento especial|possess[óo]ri|monit[óo]ria|invent[áa]rio|mandado de seguran[çc]a|Fazenda P[úu]blica|a[çc][ãa]o popular|habeas data|suspens[ãa]o de seguran',
 'P22 Juizados':r'Juizado',
 'P23 Coletivo/estrutural':r'a[çc][ãa]o civil p[úu]blica|coletiv|difus|individuais homog|estrutura|(?-i:\bTAC\b)|ajustamento de conduta',
 'P24 Custas/honorários/gratuidade':r'honor[áa]rio|custas|gratuidade|despesas',
 'P25-26 Autocomposição/arbitragem':r'arbitra|[áa]rbitro|media[çc][ãa]o|concilia[çc][ãa]o|multiportas|autocomposi',
},
'Civil':{
 'V01 LINDB/constitucionalização/DIP':r'(?-i:\bLINDB\b)|lei estrangeira|domic[íi]lio do de cujus|constitucionaliza|efic[áa]cia da lei',
 'V02 Pessoas naturais/personalidade/capacidade':r'personalidade|capacidade|curatela|tomada de decis[ãa]o apoiada|interdi[çc][ãa]o|aus[êe]ncia|nome|imagem|Estatuto da Pessoa com Defici',
 'V03 Pessoa jurídica/desconsideração':r'pessoa jur[íi]dica|desconsidera|associa[çc][ãa]o|funda[çc][ãa]o',
 'V04 Bens/bem de família':r'bem de fam[íi]lia|bens? (m[óo]veis|im[óo]veis|p[úu]blicos)|pertença|benfeitoria',
 'V05 Negócio jurídico/defeitos/prescrição':r'neg[óo]cio jur[íi]dico|nulidade|anula|simula[çc][ãa]o|les[ãa]o|estado de perigo|coa[çc][ãa]o|dolo|erro|fraude contra credores|convers[ãa]o|prescri[çc][ãa]o|decad[êe]ncia|condi[çc][ãa]o|termo|encargo',
 'V06 Obrigações':r'obriga[çc][ãa]o|solid[áa]ri|divis[íi]vel|cess[ãa]o de cr[ée]dito|assun[çc][ãa]o de d[íi]vida|pagamento|mora|cl[áa]usula penal|arras|juros|perdas e danos|novação|compensa',
 'V07 Teoria geral dos contratos':r'contrato|boa-f[ée]|onerosidade excessiva|revis[ãa]o|resolu[çc][ãa]o|v[íi]cio redibit|evic[çc][ãa]o|exce[çc][ãa]o do contrato',
 'V08 Contratos em espécie/atos unilaterais':r'compra e venda|doa[çc][ãa]o|loca[çc][ãa]o|comodato|m[úu]tuo|empreitada|mandato|seguro|fian[çc]a|transporte|corretagem|pagamento indevido|enriquecimento',
 'V09 Responsabilidade civil':r'responsabilidade civil|dano moral|dano est[ée]tico|indeniza|perda de uma chance|nexo causal|ato il[íi]cito|abuso do direito',
 'V10-11 Posse/propriedade/usucapião/registro':r'posse|possu|usucapi|propriedade|registro de im[óo]veis|vizinhan|laje|reintegra',
 'V12-14 Condomínio/fiduciária/garantias':r'condom[íi]nio|multipropriedade|aliena[çc][ãa]o fiduci|hipoteca|penhor|incorpora[çc][ãa]o imobili|loteamento|14\.711|garantia',
 'V16-17 ECA/idoso/PcD':r'crian[çc]a|adolescente|(?-i:\bECA\b)|idos|Estatuto da Pessoa Idosa',
 'V18 Marco Civil/LGPD':r'Marco Civil|internet|(?-i:\bLGPD\b)|dados pessoais|provedor',
 'V19 Família e sucessões':r'casamento|uni[ãa]o est[áa]vel|div[óo]rcio|regime de bens|alimentos|filia[çc][ãa]o|parentesco|guarda|heran[çc]a|sucess|testamento|herdeiro|invent[áa]rio|leg[íi]tima',
 'V20 Consumidor':r'consumidor|(?-i:\bCDC\b)|8\.078|fornecedor|produto|servi[çc]o defeituoso',
},
'Empresarial':{
 'E02 Empresário/teoria da empresa':r'empres[áa]rio|atividade empresarial|empres[áa]rio rural|capacidade|incapaz|registro p[úu]blico de empresas|Junta Comercial',
 'E03 Títulos de crédito/protesto':r't[íi]tulo de cr[ée]dito|cheque|nota promiss[óo]ria|duplicata|letra de c[âa]mbio|aval|endosso|protesto|aceite|cambi',
 'E04 Sociedades (geral/não personificadas/simples)':r'sociedade em comum|sociedade em conta de participa|sociedade simples|nome coletivo|comandita|cooperativ|s[óo]cio',
 'E05 Limitada e S.A.':r'limitada|(?-i:\bLTDA\b)|an[ôo]nima|6\.404|acionista|assembleia|conselho de administra|deb[êe]nture|unipessoal',
 'E06 Operações societárias/desconsideração':r'incorpora[çc][ãa]o|fus[ãa]o|cis[ãa]o|transforma[çc][ãa]o|desconsidera|dissolu|liquida[çc][ãa]o',
 'E07 Estabelecimento/trespasse/nome':r'estabelecimento|trespasse|ponto comercial|nome empresarial|preposto|escritura[çc][ãa]o|aviamento',
 'E08 Contratos empresariais':r'franquia|representa[çc][ãa]o comercial|distribui[çc][ãa]o|concess[ãa]o comercial|leasing|arrendamento mercantil|factoring|fomento|comiss[ãa]o|cart[ãa]o de cr[ée]dito',
 'E09 Bancários/SFN':r'banc[áa]ri|institui[çc][ãa]o financeira|Banco Central|Sistema Financeiro',
 'E10 Recuperação/falência':r'recupera[çc][ãa]o (judicial|extrajudicial)|fal[êe]ncia|11\.101|administrador judicial|credor|plano de recupera',
 'E11 Propriedade industrial':r'marca|patente|desenho industrial|modelo de utilidade|(?-i:\bINPI\b)|propriedade industrial|direito autoral',
 'E12 Consumo/comércio eletrônico':r'consumidor|comércio eletr[ôo]nico|(?-i:\bCDC\b)|ades[ãa]o',
},
'Penal':{
 'D01-03 Princípios/lei penal no tempo e espaço':r'princ[íi]pio da (insignific|legalidade|lesividade|interven[çc][ãa]o m[íi]nima)|lei penal no tempo|retroativ|extraterritorial|abolitio|tempo do crime|lugar do crime|novatio|ultratividade',
 'D04-06 Teoria do crime/tipicidade/dolo/culpa':r'crime (formal|material|de mera conduta|de perigo|de dano|omissivo|comissivo)|omiss[ãa]o|imputa[çc][ãa]o objetiva|causalidade|dolo eventual|culpa consciente|erro de tipo|preterdolos|teoria geral do crime',
 'D07 Iter criminis':r'tentativa|consuma[çc][ãa]o|desist[êe]ncia|arrependimento|crime imposs[íi]vel',
 'D08-10 Ilicitude/culpabilidade/imputabilidade':r'leg[íi]tima defesa|estado de necessidade|estrito cumprimento|exerc[íi]cio regular|culpabilidade|erro de proibi[çc][ãa]o|putativ|inimput[áa]vel|semi-imput|embriaguez|coa[çc][ãa]o moral|obedi[êe]ncia hier',
 'D11 Concurso de agentes':r'concurso de (agentes|pessoas)|coautor|part[íi]cipe|domínio do fato|autoria mediata',
 'D12 Penas/concurso de crimes/conflito aparente':r'dosimetria|pena-base|regime|substitui[çc][ãa]o|concurso (material|formal)|crime continuado|conflito aparente|especialidade|consun[çc][ãa]o|subsidiariedade|aberratio|erro na execu',
 'D13-16 Efeitos/reabilitação/medida de segurança/ação penal':r'efeitos da condena[çc][ãa]o|confisco|perdimento|reabilita[çc][ãa]o|medida de seguran[çc]a|a[çc][ãa]o penal|representa[çc][ãa]o|queixa',
 'D17 Extinção da punibilidade/prescrição':r'extin[çc][ãa]o da punibilidade|prescri[çc][ãa]o|perd[ãa]o judicial|decad[êe]ncia',
 'D18 Penal econômico/PJ':r'pessoa jur[íi]dica|9\.605|ambiental|econ[ôo]mico|lavagem|tribut[áa]ri',
 'D19-20 Penal militar/tratados':r'militar|Conven[çc][ãa]o das Na[çc][õo]es Unidas contra|Palermo|M[ée]rida|Viena',
 'D21a Crimes contra a pessoa/honra':r'homic[íi]dio|feminic[íi]dio|les[ãa]o corporal|inj[úu]ria|cal[úu]nia|difama|amea[çc]a|sequestro|persegui[çc][ãa]o|stalking',
 'D21b Crimes contra o patrimônio':r'furto|roubo|extors[ãa]o|estelionato|apropria[çc][ãa]o|recepta[çc][ãa]o|dano',
 'D21c Dignidade sexual':r'estupro|dignidade sexual|vulner[áa]vel|importuna[çc][ãa]o|ass[ée]dio sexual',
 'D21d Fé pública/Adm Pública/Adm justiça':r'falsifica|falsidade|uso de documento|peculato|concuss[ãa]o|corrup[çc][ãa]o|prevarica|advocacia administrativa|falso testemunho|denuncia[çc][ãa]o caluniosa|fraude processual|coa[çc][ãa]o no curso',
 'D21e Leis 7.716/12.288/13.869':r'7\.716|racismo|inj[úu]ria racial|12\.288|abuso de autoridade|13\.869',
},
}
out=defaultdict(Counter); lab={}
for k,qs in P.items():
    for q in qs:
        rules=R[q['disc']]; best=None;bs=0
        for item,rx in rules.items():
            s=len(re.findall(rx,q['txt'],re.I))
            if s>bs: best,bs=item,s
        best=best or '?? não classificada'
        out[q['disc']][best]+=1; lab[f"{k}-{q['n']}"]=best
json.dump(lab,open('classif.json','w'),ensure_ascii=False,indent=0)
for d,c in out.items():
    print('\n##',d)
    for it,n in sorted(c.items(),key=lambda x:-x[1]): print(f'  {n:3d}  {it}')
