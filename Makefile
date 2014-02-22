
VERSION	=	0.04
#IMLIST	=	cj ar dy bs zm
IMLIST	=	zm
STYLELIST	=	scim gcin ime

all:
	for im in $(IMLIST);\
		do ./qiangheng.py -i $$im -p puretable -m dynamic > puretable/$$im.puretable.txt;\
#		./qiangheng.py -i $$im -p scim -m puretable -t puretable/$$im.puretable.txt > scim/$$im.scim.txt;\
#		./qiangheng.py -i $$im -p gcin -m puretable -t puretable/$$im.puretable.txt > gcin/$$im.gcin.txt;\
#		./qiangheng.py -i $$im -p msim -m puretable -t puretable/$$im.puretable.txt > msim/$$im.msim.txt;\
	done

test:
	for im in $(IMLIST);\
		do echo $$im;\
		./qiangheng.py -i $$im -p puretable -m dynamic | wc -l;\
		./qiangheng.py -i $$im -p scim -m dynamic | wc -l;\
		./qiangheng.py -i $$im -p gcin -m dynamic | wc -l;\
		./qiangheng.py -i $$im -p msim -m dynamic | wc -l;\
	done

tex/principle.pdf: tex/principle.tex
	cd tex; xelatex principle.tex; rm principle.aux  principle.log

tarball: all tex/principle.pdf
	tar cjf ../qiangheng-$(VERSION).tar.bz2 --exclude-vcs -C .. qiangheng

clean:
	rm -f *.pyc *~ scim/* gcin/* msim/* puretable/* tex/*.aux tex/*.log
	rm -f charinfo/*/*.bak.txt charinfo/*/*.rst.txt

