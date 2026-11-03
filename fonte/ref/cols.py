import pdfplumber, sys, glob
M={'e1':'438852ce','e2':'bd5ac989','e3':'90364a88','e4':'1620a31e','e5':'4f743d7d'}
for k,p in M.items():
    f=glob.glob(f'/mnt/user-data/uploads/{p}*.pdf')[0]
    out=[]
    with pdfplumber.open(f) as pdf:
        for pg in pdf.pages:
            w,h=pg.width,pg.height
            for box in [(0,40,w/2,h-40),(w/2,40,w,h-40)]:
                t=pg.crop(box).extract_text() or ''
                out.append(t)
    open(f'/home/claude/ref/txt/{k}_c.txt','w').write('\n'.join(out))
    print(k,'ok')
