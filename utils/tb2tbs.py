#!/usr/bin/env python3

fileencoding='utf-8-sig'

tgfilename='CJK.txt'
srcfilename='charinfo/'+tgfilename
mainfilename='charinfo/main/'+tgfilename
cjfilename='charinfo/cj/'+tgfilename
arfilename='charinfo/ar/'+tgfilename
dyfilename='charinfo/dy/'+tgfilename
bsfilename='charinfo/bs/'+tgfilename
zmfilename='charinfo/zm/'+tgfilename

mainfile=open(mainfilename, "w", encoding=fileencoding)
cjfile=open(cjfilename, "w", encoding=fileencoding)
arfile=open(arfilename, "w", encoding=fileencoding)
dyfile=open(dyfilename, "w", encoding=fileencoding)
bsfile=open(bsfilename, "w", encoding=fileencoding)
zmfile=open(zmfilename, "w", encoding=fileencoding)

for line in open(srcfilename, encoding=fileencoding):
	line=line.strip()
	if line and line[0:4]=='# U+':
		continue
	elif line and line=='\n':
		continue
	elif line and line[0]=='#':
		mainfile.write(line+'\n')
		cjfile.write(line+'\n')
		arfile.write(line+'\n')
		dyfile.write(line+'\n')
		bsfile.write(line+'\n')
		zmfile.write(line+'\n')
	else:
		ll=line.split('\t')
		mainfile.write('{0}\t{1}\t{2}\n'.format(*ll))
		if len(ll)>2 and ll[2]=='(龜)':
			cjfile.write('{0}\t{1}\t{2}\t{3}\n'.format(*ll))
			arfile.write('{0}\t{1}\t{2}\t{4}\n'.format(*ll))
			dyfile.write('{0}\t{1}\t{2}\t{5}\n'.format(*ll))
			bsfile.write('{0}\t{1}\t{2}\t{6}\t{7}\n'.format(*ll))
			zmfile.write('{0}\t{1}\t{2}\t{8}\t{9}\n'.format(*ll))

