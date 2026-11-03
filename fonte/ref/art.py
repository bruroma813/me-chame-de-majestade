import re,sys
R={'CF':(12,103),'LINDB':(104,107),'CC':(112,217),'CPC':(221,317),'CP':(321,362),'CPP':(374,433),'CTN':(435,451),'CDC':(581,595),'ECA':(750,784),'PCD':(805,818),'IDOSO':(819,829),'14133':(859,899),'8112':(921,942),'LMP':(943,949),'RACIAL':(793,798),'DROGAS':(830,841),'CIDADE':(742,749)}
import os
txt=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'vademecum_2026_colunas.txt'),encoding='utf-8').read()
pags=re.split(r'<<<PAG (\d+)>>>',txt)
pg={int(pags[i]):pags[i+1] for i in range(1,len(pags),2)}
def corpo(lei):
    a,b=R[lei]; t='\n'.join(pg.get(p,'') for p in range(a,b+1))
    return re.sub(r'-\n(?=[a-zà-ú])','',t)
for q in sys.argv[2:]:
    t=corpo(sys.argv[1].upper())
    m=re.search(r'(?:^|\n)Art\. '+re.escape(q)+r'(?:[ºo°])?\.?[ -]',t)
    if not m: print(f'[{q}] não achado'); continue
    rest=t[m.start():]; n=re.search(r'\nArt\. \d',rest[5:])
    print(f'==== {sys.argv[1]} art. {q}\n'+rest[:n.start()+5 if n else 2500][:3000].replace('\n',' '))
