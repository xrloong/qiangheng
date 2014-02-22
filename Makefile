
VERSION	=	0.04
IMLIST	=	cj ar dy bs zm
TEST_IMLIST	=	cj ar dy bs zm
PLATFORM_LIST	=	puretable scim gcin msim

.PHONY: puretable scim gcin msim

all: puretable

puretable:
	for im in $(IMLIST);\
		do\
		time ./qiangheng.py -i $$im -p puretable -m dynamic > $@/$$im.$@.txt;\
	done

scim gcin msim:
	for im in $(IMLIST);\
		do\
		./qiangheng.py -i $$im -p $@ -m table -t puretable/$$im.puretable.txt > $@/$$im.$@.txt;\
	done

testing:
	for im in $(TEST_IMLIST);\
		do ./qiangheng.py --dir-charinfo test/charinfo -i $$im -p puretable -m dynamic > test/puretable/$$im.puretable.txt;\
	done

compare: testing
	diff -rN test/puretable_ans test/puretable

tex/principle.pdf: tex/principle.tex
	cd tex; xelatex principle.tex; rm principle.aux  principle.log

tarballs: tarball-src tarball-all
	make clean
	make tarball-src VERSION=$(VERSION)
	make puretable
	make scim gcin msim
	make tarball-platform VERSION=$(VERSION)
	make tarball-all VERSION=$(VERSION)

tarball-src:
	tar cjf ../qiangheng-src-$(VERSION).tar.bz2 --exclude-vcs -C .. qiangheng

tarball-platform:
	for p in $(PLATFORM_LIST);\
	do\
		tar cjf ../qiangheng-$$p-$(VERSION).tar.bz2 --exclude-vcs -C .. qiangheng/$$p;\
	done

tarball-all:
	tar cjf ../qiangheng-$(VERSION).tar.bz2 --exclude-vcs -C .. qiangheng

clean:
	rm -f *.pyc im/*.pyc character/*.pyc
	rm -f *~ scim/* gcin/* msim/* puretable/* tex/*.aux tex/*.log
	rm -f charinfo/*/*.bak.txt charinfo/*/*.rst.txt
	rm -f test/puretable/*

