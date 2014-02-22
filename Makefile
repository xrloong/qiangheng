
VERSION	=	0.01
IMLIST	=	cj ar dy bs zm
STYLELIST	=	scim gcin ime

all:
	for im in $(IMLIST);\
		do ./qiangheng.py -g $$im -s scim >> scim/$$im.scim.txt;\
		./qiangheng.py -g $$im -s gcin >> gcin/$$im.gcin.txt;\
		./qiangheng.py -g $$im -s msim >> msim/$$im.msim.txt;\
	done

tarball: all
	cd ..; tar cjf qiangheng-$(VERSION).tar.bz2 --no-recursion `find qiangheng | egrep -v ".svn"`

clean:
	rm -f *.pyc *~ scim/* gcin/* msim/*

