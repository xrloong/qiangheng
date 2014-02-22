#!/usr/bin/env python3

import shutil, sys

imlist=['ar', 'bs', 'cj', 'dy', 'zm']
arsrc='charinfo/ar/CJK.txt'
fileencoding='utf-8-sig'

removedCharList=sys.argv[1]

for i in imlist:
	fn='charinfo/%s/CJK.txt'%i
	bakfn='charinfo/%s/CJK.bak.txt'%i
	rstfn='charinfo/%s/CJK.rst.txt'%i
	shutil.copy(fn, bakfn)
	rstf=open(rstfn, 'w', encoding=fileencoding)
	for line in open(bakfn, encoding=fileencoding):
		line=line.strip()
		if line=='' or (line and len(line) and line[0]=='#'):
			rstf.write(line+'\n')
		else:
			ll=line.split('\t')
			if ll[1] in removedCharList:
				pass
			else:
				rstf.write(line+'\n')
