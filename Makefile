
VERSION	=	0.04
IMLIST	=	cj ar dy bs zm
TEST_IMLIST	=	cj ar dy bs zm
STYLELIST	=	scim gcin ime

all:
	for im in $(IMLIST);\
		do\
		time ./qiangheng.py -i $$im -p puretable -m dynamic > puretable/$$im.puretable.txt;\
		./qiangheng.py -i $$im -p scim -m puretable -t puretable/$$im.puretable.txt > scim/$$im.scim.txt;\
		./qiangheng.py -i $$im -p gcin -m puretable -t puretable/$$im.puretable.txt > gcin/$$im.gcin.txt;\
		./qiangheng.py -i $$im -p msim -m puretable -t puretable/$$im.puretable.txt > msim/$$im.msim.txt;\
	done

testing:
	for im in $(TEST_IMLIST);\
		do ./qiangheng.py --dir-charinfo test/charinfo -i $$im -p puretable -m dynamic > test/puretable/$$im.puretable.txt;\
	done
#	for im in $(IMLIST);\
#		do echo $$im;\
#		./qiangheng.py -i $$im -p puretable -m dynamic | wc -l;\
#		./qiangheng.py -i $$im -p scim -m dynamic | wc -l;\
#		./qiangheng.py -i $$im -p gcin -m dynamic | wc -l;\
#		./qiangheng.py -i $$im -p msim -m dynamic | wc -l;\
#	done

compare: testing
	diff -rN test/puretable_ans test/puretable

tex/principle.pdf: tex/principle.tex
	cd tex; xelatex principle.tex; rm principle.aux  principle.log

tarball: all tex/principle.pdf
	tar cjf ../qiangheng-$(VERSION).tar.bz2 --exclude-vcs -C .. qiangheng

clean:
	rm -f *.pyc im/*.pyc character/*.pyc
	rm -f *~ scim/* gcin/* msim/* puretable/* tex/*.aux tex/*.log
	rm -f charinfo/*/*.bak.txt charinfo/*/*.rst.txt
	rm -f test/puretable/*

