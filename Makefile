
VERSION	=	0.01
IMLIST	=	cj ar dy bs zm
STYLELIST	=	scim gcin ime

all:
	for im in $(IMLIST);\
		do ./qiangheng.py -i $$im -p puretable -m dynamic > puretable/$$im.puretable.txt;\
		./qiangheng.py -i $$im -p scim -m puretable -t puretable/$$im.puretable.txt > scim/$$im.scim.txt;\
		./qiangheng.py -i $$im -p gcin -m puretable -t puretable/$$im.puretable.txt > gcin/$$im.gcin.txt;\
		./qiangheng.py -i $$im -p msim -m puretable -t puretable/$$im.puretable.txt > msim/$$im.msim.txt;\
	done

test:
	for im in $(IMLIST);\
		do echo $$im;\
		./qiangheng.py -i $$im -p puretable -m dynamic | wc -l;\
		./qiangheng.py -i $$im -p scim -m dynamic | wc -l;\
		./qiangheng.py -i $$im -p gcin -m dynamic | wc -l;\
		./qiangheng.py -i $$im -p msim -m dynamic | wc -l;\
	done

tarball: all
	cd ..; tar cjf qiangheng-$(VERSION).tar.bz2 --no-recursion `find qiangheng | egrep -v ".svn"`

clean:
	rm -f *.pyc *~ scim/* gcin/* msim/* puretable/*

