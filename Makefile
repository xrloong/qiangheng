
VERSION	=	0.27
IMLIST	=	ar bs cj dy fc zm
PLATFORM_LIST	=	puretable scim gcin msim
TABLES_PATH	=	tables
PURETABLE_PATH	=	$(TABLES_PATH)/puretable
XML_PATH	=	$(TABLES_PATH)/xml
SCIM_PATH	=	$(TABLES_PATH)/scim
IBUS_PATH	=	$(TABLES_PATH)/ibus
GCIN_PATH	=	$(TABLES_PATH)/gcin
OVIM_PATH	=	$(TABLES_PATH)/ovim
MSIM_PATH	=	$(TABLES_PATH)/msim
QHDATA_PATH			=	qhdata
QHDATA_MAIN_PATH		=	$(QHDATA_PATH)/main
QHDATA_MAIN_COMP_PATH		=	$(QHDATA_MAIN_PATH)/component
QHDATA_TEMPLATE_FILE		=	$(QHDATA_PATH)/template/main.xml
QHDATA_STYLE_PATH		=	$(QHDATA_PATH)/style
QHDATA_COMP_PATH		=	$(QHDATA_PATH)/component
QHDATA_RADIX_PATH		=	$(QHDATA_PATH)/radix
QHDATA_STYLE_FILE		=	standard.xml
QHDATA_STYLE_TRADITIONAL_FILE	=	traditional.xml
QHDATA_STYLE_SIMPLIFIED_FILE	=	simplified.xml
GEN_PATH			=	gen
GEN_QHDATA_PATH			=	$(GEN_PATH)/$(QHDATA_PATH)
GEN_QHDATA_MAIN_PATH		=	$(GEN_QHDATA_PATH)/main
GEN_QHDATA_MAIN_COMP_PATH	=	$(GEN_QHDATA_MAIN_PATH)/component
GEN_QHDATA_TEMPLATE_FILE	=	$(GEN_QHDATA_MAIN_PATH)/template.xml
PROFILE_PATH	=	profiles
TARBALLS_PATH	=	tarballs
XFORM		=	--xform="s:^:qiangheng/:"
ICON_PATH	=	icons/
ICON_ORIGIN_PATH	=	icons/origin/
ICON_PLATFORM_PATH	=	icons/platform/
SCIM_ICON_PATH	=	icons/platform/scim
IBUS_ICON_PATH	=	icons/platform/ibus
GCIN_ICON_PATH	=	icons/platform/gcin
OVIM_ICON_PATH	=	icons/platform/ovim
MSIM_ICON_PATH	=	icons/platform/msim
RELEASE_TYPE_LIST	=	standard all

.PHONY: xml tarballs all-icons

all: xml

prepare-main:
	mkdir -p $(GEN_QHDATA_MAIN_PATH) $(GEN_QHDATA_MAIN_COMP_PATH)
	xalan -xsl xslt/xml2yaml.xslt -in $(QHDATA_MAIN_PATH)/CJK.xml > $(GEN_QHDATA_MAIN_PATH)/CJK.yaml
	xalan -xsl xslt/xml2yaml.xslt -in $(QHDATA_MAIN_PATH)/CJK-A.xml > $(GEN_QHDATA_MAIN_PATH)/CJK-A.yaml
	xalan -xsl xslt/xml2yaml.xslt -in $(QHDATA_MAIN_COMP_PATH)/CJK.xml > $(GEN_QHDATA_MAIN_COMP_PATH)/CJK.yaml
	xalan -xsl xslt/xml2yaml.xslt -in $(QHDATA_MAIN_COMP_PATH)/CJK-A.xml > $(GEN_QHDATA_MAIN_COMP_PATH)/CJK-A.yaml
	xalan -xsl xslt/xml2yaml-template.xslt -in $(QHDATA_TEMPLATE_FILE) > $(GEN_QHDATA_MAIN_PATH)/template.yaml

prepare-tranditional:
	xalan -xsl xslt/xml2yaml.xslt -in $(QHDATA_STYLE_PATH)/$(QHDATA_STYLE_FILE) > $(GEN_QHDATA_MAIN_PATH)/style.yaml
	xalan -xsl xslt/xml2yaml.xslt -in $(QHDATA_STYLE_PATH)/$(QHDATA_STYLE_TRADITIONAL_FILE) > $(GEN_QHDATA_PATH)/$(IM)/style.yaml

prepare-simplified:
	xalan -xsl xslt/xml2yaml.xslt -in $(QHDATA_STYLE_PATH)/$(QHDATA_STYLE_FILE) > $(GEN_QHDATA_MAIN_PATH)/style.yaml
	xalan -xsl xslt/xml2yaml.xslt -in $(QHDATA_STYLE_PATH)/$(QHDATA_STYLE_SIMPLIFIED_FILE) > $(GEN_QHDATA_PATH)/$(IM)/style.yaml

prepare-im:
	mkdir -p $(GEN_QHDATA_PATH)/$(IM)/component/ $(GEN_QHDATA_PATH)/$(IM)/radix/
	xalan -xsl xslt/xml2yaml.xslt -in $(QHDATA_COMP_PATH)/CJK/$(IM).xml > $(GEN_QHDATA_PATH)/$(IM)/component/CJK.yaml
	xalan -xsl xslt/xml2yaml.xslt -in $(QHDATA_COMP_PATH)/CJK-A/$(IM).xml > $(GEN_QHDATA_PATH)/$(IM)/component/CJK-A.yaml

prepare-im-general:
	xalan -xsl xslt/xml2yaml-radix.xslt -in $(QHDATA_RADIX_PATH)/CJK/$(IM).xml > $(GEN_QHDATA_PATH)/$(IM)/radix/CJK.yaml
	xalan -xsl xslt/xml2yaml-radix.xslt -in $(QHDATA_RADIX_PATH)/CJK-A/$(IM).xml > $(GEN_QHDATA_PATH)/$(IM)/radix/CJK-A.yaml

prepare-ar:
	mkdir -p $(GEN_QHDATA_PATH)/ar
	make prepare-tranditional IM=ar
	make prepare-im prepare-im-general IM=ar

prepare-bs:
	mkdir -p $(GEN_QHDATA_PATH)/bs
	make prepare-tranditional IM=bs
	make prepare-im prepare-im-general IM=bs

prepare-cj:
	mkdir -p $(GEN_QHDATA_PATH)/cj
	make prepare-tranditional IM=cj
	make prepare-im prepare-im-general IM=cj

prepare-dy:
	mkdir -p $(GEN_QHDATA_PATH)/dy
	make prepare-tranditional IM=dy
	make prepare-im prepare-im-general IM=dy

prepare-fc:
	mkdir -p $(GEN_QHDATA_PATH)/fc
	make prepare-tranditional IM=fc
	make prepare-im prepare-im-general IM=fc

prepare-zm:
	mkdir -p $(GEN_QHDATA_PATH)/zm
	make prepare-simplified IM=zm
	make prepare-im prepare-im-general IM=zm

prepare-dc:
	mkdir -p $(GEN_QHDATA_PATH)/dc
	make prepare-tranditional IM=dc
	make prepare-im IM=dc
	xalan -xsl xslt/xml2yaml-dc.xslt -in $(QHDATA_RADIX_PATH)/CJK/dc.xml > $(GEN_QHDATA_PATH)/dc/radix/CJK.yaml
	xalan -xsl xslt/xml2yaml-dc.xslt -in $(QHDATA_RADIX_PATH)/CJK-A/dc.xml > $(GEN_QHDATA_PATH)/dc/radix/CJK-A.yaml

prepare:
	make prepare-main
	make prepare-ar prepare-bs prepare-cj prepare-dy prepare-fc prepare-zm prepare-dc

$(XML_PATH):
xml:
	mkdir -p $(XML_PATH)
	for im in $(IMLIST);\
	do\
		echo $$im;\
		time src/qiangheng.py -i $$im --format xml |\
			xalan -xsl xslt/formatOutput.xslt -out $(XML_PATH)/qh$$im.xml -indent 4;\
	done
	touch $(XML_PATH)

profile:
	mkdir -p $(PROFILE_PATH)
	for im in $(IMLIST);\
	do\
		echo $$im;\
		src/profiler.py -q -c qhdata/config/$$im.xml > $(PROFILE_PATH)/$$im.txt;\
	done
	touch $(XML_PATH)

dc:
	make xml puretable IMLIST=dc

test:
	PYTHONPATH=src python3 -m unittest discover -s tests/ -p "*.py"

imtables: scim ibus gcin ovim msim puretable

scim: $(SCIM_PATH)
$(SCIM_PATH): $(XML_PATH)
	mkdir -p $(SCIM_PATH)
	for im in $(IMLIST);\
	do\
		xalan -xsl xslt/scim.xslt -in tables/xml/qh$$im.xml -param UUID \"`uuidgen`\" -param SERIAL \"`date +%Y%m%d`\" -param ICON_DIR \"/usr/share/scim/icon/\" -param ICON_FILE \"qh$$im.svg\" -out $(SCIM_PATH)/qh$$im.scim;\
		scim-make-table $(SCIM_PATH)/qh$$im.scim -b -o $(SCIM_PATH)/qh$$im.bin;\
	done
	touch $(SCIM_PATH)

ibus: $(IBUS_PATH)
$(IBUS_PATH): $(XML_PATH)
	mkdir -p $(IBUS_PATH)
	mkdir -p tmp
	for im in $(IMLIST);\
	do\
		xalan -xsl xslt/ibus.xslt -in tables/xml/qh$$im.xml -param UUID \"`uuidgen`\" -param SERIAL \"`date +%Y%m%d`\" -param ICON_FILE \"qh$$im.svg\" -out $(IBUS_PATH)/qh$$im.ibus;\
		bash -c "cd tmp; ibus-table-createdb -s ../$(IBUS_PATH)/qh$$im.ibus";\
	done
	cp tmp/*.db $(IBUS_PATH)
	touch $(IBUS_PATH)

gcin: $(GCIN_PATH)
$(GCIN_PATH): $(XML_PATH)
	mkdir -p $(GCIN_PATH)
	for im in $(IMLIST);\
	do\
		time xalan -xsl xslt/gcin.xslt -in $(XML_PATH)/qh$$im.xml -out $(GCIN_PATH)/qh$$im.cin;\
		gcin2tab $(GCIN_PATH)/qh$$im.cin;\
	done
	touch $(GCIN_PATH)

ovim: $(OVIM_PATH)
$(OVIM_PATH): $(XML_PATH)
	mkdir -p $(OVIM_PATH)
	for im in $(IMLIST);\
	do\
		time xalan -xsl xslt/ovim.xslt -in $(XML_PATH)/qh$$im.xml -out $(OVIM_PATH)/qh$$im.cin;\
	done
	touch $(OVIM_PATH)

msim: $(MSIM_PATH)
$(MSIM_PATH): $(XML_PATH)
	mkdir -p $(MSIM_PATH)
	for im in $(IMLIST);\
	do\
		time xalan -xsl xslt/msim.xslt -in $(XML_PATH)/qh$$im.xml -out $(MSIM_PATH)/qh$$im.msim;\
		sed 's/$$'"/`echo \\\r`/" $(MSIM_PATH)/qh$$im.msim > tmp/qh$$im.msim.dos;\
		iconv -f utf-8 -t utf-16le tmp/qh$$im.msim.dos > $(MSIM_PATH)/qh$$im.msim.txt;\
	done
	touch $(MSIM_PATH)

puretable: $(PURETABLE_PATH)
$(PURETABLE_PATH): $(XML_PATH)
	mkdir -p $(PURETABLE_PATH)
	for type in $(RELEASE_TYPE_LIST);\
	do\
		for im in $(IMLIST);\
		do\
			time xalan -xsl xslt/puretable-$$type.xslt -in $(XML_PATH)/qh$$im.xml -out $(PURETABLE_PATH)/qh$$im-$$type.txt;\
		done;\
	done
	touch $(PURETABLE_PATH)

pdf: tex/qiangheng.pdf

tex/qiangheng.pdf: tex/qiangheng.tex
	cd tex; rm -f qiangheng.aux qiangheng.log
	cd tex; xelatex qiangheng.tex; xelatex qiangheng.tex

all-icons:
	mkdir -p $(SCIM_ICON_PATH) $(GCIN_ICON_PATH) $(OVIM_ICON_PATH) $(MSIM_ICON_PATH) $(IBUS_ICON_PATH)
	for im in $(IMLIST);\
	do\
		inkscape -D -w 48 -h 48 -e $(SCIM_ICON_PATH)/qh$$im.png $(ICON_ORIGIN_PATH)/qh$$im.svg;\
		inkscape -D -w 30 -h 30 -e $(GCIN_ICON_PATH)/qh$$im.png $(ICON_ORIGIN_PATH)/qh$$im.svg;\
		inkscape -D -w 48 -h 48 -e $(OVIM_ICON_PATH)/qh$$im.png $(ICON_ORIGIN_PATH)/qh$$im.svg;\
		cp $(ICON_ORIGIN_PATH)/qh$$im.svg $(IBUS_ICON_PATH)/qh$$im.png;\
	done
	inkscape -D -w 64 -h 64 -e $(ICON_PLATFORM_PATH)/qiangheng.png $(ICON_ORIGIN_PATH)/qiangheng.svg;

tarballs: pre-tarballs pdf tarball-src tarball-all
	make tarball-src VERSION=$(VERSION)
	make xml puretable
	make imtables
	make tarballs-platform VERSION=$(VERSION)
	make tarball-all VERSION=$(VERSION)

pre-tarballs:
	make clean
	mkdir -p $(TARBALLS_PATH)

tarball-src:
	mkdir -p tmp
	git ls-files > tmp/files.list
	echo tex/qiangheng.pdf >> tmp/files.list
	tar cjf $(TARBALLS_PATH)/qiangheng-src-$(VERSION).tar.bz2 --exclude-vcs --no-recursion $(XFORM) -T tmp/files.list

tarballs-platform: all-icons
	tar cjf $(TARBALLS_PATH)/qiangheng-scim-$(VERSION).tar.bz2 --exclude-vcs $(XFORM) $(SCIM_PATH)/*.bin $(ICON_PATH) tex/qiangheng.pdf README.txt
	tar cjf $(TARBALLS_PATH)/qiangheng-ibus-$(VERSION).tar.bz2 --exclude-vcs $(XFORM) $(IBUS_PATH)/*.db $(ICON_PATH) tex/qiangheng.pdf README.txt
	tar cjf $(TARBALLS_PATH)/qiangheng-gcin-$(VERSION).tar.bz2 --exclude-vcs $(XFORM) $(GCIN_PATH)/*.gtab $(ICON_PATH) tex/qiangheng.pdf README.txt
	tar cjf $(TARBALLS_PATH)/qiangheng-ovim-$(VERSION).tar.bz2 --exclude-vcs $(XFORM) $(OVIM_PATH)/*.cin $(ICON_PATH) tex/qiangheng.pdf README.txt
	tar cjf $(TARBALLS_PATH)/qiangheng-msim-$(VERSION).tar.bz2 --exclude-vcs $(XFORM) $(MSIM_PATH)/*.txt $(ICON_PATH) tex/qiangheng.pdf README.txt

tarball-all:
	tar cjf $(TARBALLS_PATH)/qiangheng-$(VERSION).tar.bz2 --exclude-vcs --exclude=tarballs -C .. qiangheng

python-fontforge:
	cd fontforge; wget -O fontforge_full-20110222.tar.bz2 http://sourceforge.net/projects/fontforge/files/fontforge-source/fontforge_full-20110222.tar.bz2/download
	cd fontforge/; tar xjf fontforge_full-20110222.tar.bz2
	cd fontforge/fontforge-20110222; patch -Np1 < ../fontforge-20110222.patch
	cd fontforge/fontforge-20110222; ./configure --enable-pyextension --with-python=python3; make
	cd src/; ln -s ../fontforge/fontforge-20110222/.libs/libfontforge.so fontforge.so

clean:
	rm -rf $(ICON_PLATFORM_PATH)
	rm -rf $(GEN_PATH)
	rm -rf tables/ tmp/ tarballs/ font/qhdc.ttf
	rm -f `find src -name "*.pyc"`
	rm -f *~ scim/* gcin/* msim/* puretable/* tex/*.aux tex/*.log tex/*.pdf

