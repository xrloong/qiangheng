VERSION	=	0.40
IMLIST	=	ar bs cj dy fc zm
DMLIST	=	dc
CMLIST	=	$(IMLIST) $(DMLIST)

SHELL	=	/bin/bash
PIP	=	pip3
UNAME	:=	$(shell uname)
INSTALL_DIR	:=	$(shell pwd)

define setup_codings
package_ar="coding.Array codings/Array" \
package_bs="coding.Boshiamy codings/Boshiamy" \
package_cj="coding.CangJie codings/CangJie" \
package_dy="coding.DaYi codings/DaYi" \
package_fc="coding.FourCorner codings/FourCorner" \
package_zm="coding.ZhengMa codings/ZhengMa" \
package_dc="coding.DynamicComposition codings/DynamicComposition"
endef

TABLES_PATH	=	tables
PURETABLE_PATH	=	$(TABLES_PATH)/puretable
XML_PATH	=	$(TABLES_PATH)/xml
YAML_PATH	=	$(TABLES_PATH)/yaml
SCIM_PATH	=	$(TABLES_PATH)/scim
IBUS_PATH	=	$(TABLES_PATH)/ibus
GCIN_PATH	=	$(TABLES_PATH)/gcin
OVIM_PATH	=	$(TABLES_PATH)/ovim
MSIM_PATH	=	$(TABLES_PATH)/msim
SVG_PATH	=	font/svg
QHDATA_PATH			=	qhdata
QHDATA_MAIN_PATH		=	$(QHDATA_PATH)/main
QHDATA_MAIN_COMP_PATH		=	$(QHDATA_MAIN_PATH)/component
QHDATA_MAIN_RADIX_PATH		=	$(QHDATA_MAIN_PATH)/radix
QHDATA_STYLE_FILE		=	$(QHDATA_MAIN_PATH)/style.xml
GEN_PATH			=	gen
GEN_QHDATA_PATH			=	$(GEN_PATH)/$(QHDATA_PATH)
GEN_QHDATA_MAIN_PATH		=	$(GEN_QHDATA_PATH)/main
GEN_QHDATA_MAIN_COMP_PATH	=	$(GEN_QHDATA_MAIN_PATH)/component
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

setup-environment: setup-$(UNAME)-environment setup-python-environment

setup-Linux-environment:
	sudo make setup-$(shell lsb_release -si)-environment

setup-Ubuntu-environment:
	apt-get install python3 python3-pip
	apt-get install xsltproc libxml2-utils
	apt-get install fontforge

setup-FreeBSD-environment:
	pkg install python37 py37-pip
	pkg install py37-lxml
	pkg install fontforge

setup-Darwin-environment:
	brew install python3
	brew install fontforge	# To provide python extension of fontforge

setup-python-environment:
	$(PIP) install lxml ruamel.yaml injector ply
	$(PIP) install https://github.com/xrloong/Xie/releases/download/v0.1.5/Xie-0.1.5-py3-none-any.whl

prepare-main:
	mkdir -p $(GEN_QHDATA_MAIN_PATH) $(GEN_QHDATA_MAIN_COMP_PATH)
	xsltproc -o $(GEN_QHDATA_MAIN_PATH)/CJK.yaml xslt/xml2yaml.xslt $(QHDATA_MAIN_PATH)/CJK.xml
	xsltproc -o $(GEN_QHDATA_MAIN_PATH)/CJK-A.yaml xslt/xml2yaml.xslt $(QHDATA_MAIN_PATH)/CJK-A.xml
	xsltproc -o $(GEN_QHDATA_MAIN_COMP_PATH)/CJK.yaml xslt/xml2yaml.xslt $(QHDATA_MAIN_COMP_PATH)/CJK.xml
	xsltproc -o $(GEN_QHDATA_MAIN_COMP_PATH)/CJK-A.yaml xslt/xml2yaml.xslt $(QHDATA_MAIN_COMP_PATH)/CJK-A.xml
	xsltproc -o $(GEN_QHDATA_MAIN_PATH)/style.yaml xslt/xml2yaml.xslt $(QHDATA_STYLE_FILE)
	cp $(QHDATA_MAIN_PATH)/template.yaml $(GEN_QHDATA_MAIN_PATH)/template.yaml
	python3 scripts/split.py $(QHDATA_MAIN_RADIX_PATH)/CJK.xml $(GEN_QHDATA_PATH)/ _CJK.xml
	python3 scripts/split.py $(QHDATA_MAIN_RADIX_PATH)/CJK-A.xml $(GEN_QHDATA_PATH)/ _CJK-A.xml

prepare-im:
	mkdir -p $(GEN_QHDATA_PATH)/$(IM)/radix/
	cp -f $(QHDATA_PATH)/$(IM)/info.yaml $(GEN_QHDATA_PATH)/$(IM)/info.yaml
	cp -f $(QHDATA_PATH)/$(IM)/substitute.yaml $(GEN_QHDATA_PATH)/$(IM)/substitute.yaml
	cp -f $(QHDATA_PATH)/$(IM)/adjust.yaml $(GEN_QHDATA_PATH)/$(IM)/adjust.yaml
	cp -f $(QHDATA_PATH)/$(IM)/fast.yaml $(GEN_QHDATA_PATH)/$(IM)/fast.yaml

prepare-im-general:
	XMLLINT_INDENT="    " xmllint --encode UTF-8 --format $(GEN_QHDATA_PATH)/$(IM)/radix/_CJK.xml -o $(GEN_QHDATA_PATH)/$(IM)/radix/CJK.xml
	XMLLINT_INDENT="    " xmllint --encode UTF-8 --format $(GEN_QHDATA_PATH)/$(IM)/radix/_CJK-A.xml -o $(GEN_QHDATA_PATH)/$(IM)/radix/CJK-A.xml
	xsltproc -o $(GEN_QHDATA_PATH)/$(IM)/radix/CJK.yaml xslt/xml2yaml-radix.xslt $(GEN_QHDATA_PATH)/$(IM)/radix/CJK.xml
	xsltproc -o $(GEN_QHDATA_PATH)/$(IM)/radix/CJK-A.yaml xslt/xml2yaml-radix.xslt $(GEN_QHDATA_PATH)/$(IM)/radix/CJK-A.xml

prepare-ar:
	mkdir -p $(GEN_QHDATA_PATH)/ar
	make prepare-im prepare-im-general IM=ar

prepare-bs:
	mkdir -p $(GEN_QHDATA_PATH)/bs
	make prepare-im prepare-im-general IM=bs

prepare-cj:
	mkdir -p $(GEN_QHDATA_PATH)/cj
	make prepare-im prepare-im-general IM=cj

prepare-dy:
	mkdir -p $(GEN_QHDATA_PATH)/dy
	make prepare-im prepare-im-general IM=dy

prepare-fc:
	mkdir -p $(GEN_QHDATA_PATH)/fc
	make prepare-im prepare-im-general IM=fc

prepare-zm:
	mkdir -p $(GEN_QHDATA_PATH)/zm
	make prepare-im prepare-im-general IM=zm

prepare-dc:
	mkdir -p $(GEN_QHDATA_PATH)/dc
	make prepare-im IM=dc
	XMLLINT_INDENT="    " xmllint --encode UTF-8 --format $(GEN_QHDATA_PATH)/dc/radix/_CJK.xml -o $(GEN_QHDATA_PATH)/dc/radix/CJK.xml
	XMLLINT_INDENT="    " xmllint --encode UTF-8 --format $(GEN_QHDATA_PATH)/dc/radix/_CJK-A.xml -o $(GEN_QHDATA_PATH)/dc/radix/CJK-A.xml
	xsltproc -o $(GEN_QHDATA_PATH)/dc/radix/CJK.yaml xslt/xml2yaml-dc.xslt $(GEN_QHDATA_PATH)/dc/radix/CJK.xml
	xsltproc -o $(GEN_QHDATA_PATH)/dc/radix/CJK-A.yaml xslt/xml2yaml-dc.xslt $(GEN_QHDATA_PATH)/dc/radix/CJK-A.xml
	cp $(QHDATA_PATH)/dc/radix/template.yaml $(GEN_QHDATA_PATH)/dc/radix/template.yaml

prepare:
	make prepare-main
	make prepare-ar prepare-bs prepare-cj prepare-dy prepare-fc prepare-zm prepare-dc

$(XML_PATH):
	mkdir -p $(XML_PATH)

$(YAML_PATH):
	mkdir -p $(YAML_PATH)

$(PURETABLE_PATH):
	mkdir -p $(PURETABLE_PATH)

xml:
	for cm in $(CMLIST);\
	do\
		make $(XML_PATH)/qh$$cm.xml; \
	done

yaml:
	mkdir -p $(YAML_PATH)
	for cm in $(CMLIST);\
	do\
		$(call setup_codings);\
		packageConfig=`eval echo '$$package_'$$cm`; \
		package=`echo $$packageConfig | cut -d" " -f1`;\
		packageDir=`echo $$packageConfig | cut -d" " -f2`;\
		echo $$cm $$package $$packageDir;\
		PYTHONPATH="src:libs:$$packageDir" time src/qiangheng.py -p $$package > $(YAML_PATH)/qh$$cm.yaml; \
	done

puretable:
	for cm in $(CMLIST);\
	do\
		make $(PURETABLE_PATH)/qh$$cm.txt; \
	done

.PRECIOUS: $(YAML_PATH)/qh%.yaml

$(YAML_PATH)/qh%.yaml: $(YAML_PATH)
	mkdir -p $(YAML_PATH)
	filename=$$(basename $@); \
	cm=$${filename:2:2}; \
	$(call setup_codings);\
	packageConfig=`eval echo '$$package_'$$cm`; \
	package=`echo $$packageConfig | cut -d" " -f1`;\
	packageDir=`echo $$packageConfig | cut -d" " -f2`;\
	echo $$cm $$package $$packageDir;\
	PYTHONPATH="src:libs:$$packageDir" time src/qiangheng.py -p $$package > $(YAML_PATH)/qh$$cm.yaml; \

$(XML_PATH)/qh%.xml: $(XML_PATH) $(YAML_PATH)/qh%.yaml
	filename=$$(basename $@); \
	cm=$${filename:2:2}; \
	echo $$cm; \
	python3 scripts/convert_cm_to_xml.py tables/yaml/qh$$cm.yaml gen/qhdata/$$cm/info.yaml |\
		XMLLINT_INDENT="    " xmllint --encode UTF-8 -o $(XML_PATH)/qh$$cm.xml --format -; \

$(PURETABLE_PATH)/qh%.txt: $(PURETABLE_PATH) $(YAML_PATH)/qh%.yaml
	filename=$$(basename $@); \
	cm=$${filename:2:2}; \
	for type in $(RELEASE_TYPE_LIST);\
	do\
		scripts/extract_mapping.py -t $$type $(YAML_PATH)/qh$$cm.yaml > $(PURETABLE_PATH)/qh$$cm-$$type.txt; \
	done

profile:
	mkdir -p $(PROFILE_PATH)
	for cm in $(CMLIST);\
	do\
		$(call setup_codings);\
		packageConfig=`eval echo '$$package_'$$cm`; \
		package=`echo $$packageConfig | cut -d" " -f1`;\
		packageDir=`echo $$packageConfig | cut -d" " -f2`;\
		echo $$cm $$package $$packageDir;\
		PYTHONPATH="src:libs:$$packageDir" src/profiler.py -q -p $$package > $(PROFILE_PATH)/$$cm.txt;\
	done

dc:
	make yaml CMLIST=dc

FORCE:

test: FORCE
	pytest -c tests/pytest-libs.ini --rootdir=.; \
	for cm in $(CMLIST);\
	do\
		pytest -c tests/pytest-$$cm.ini --rootdir=.; \
	done

imtables: scim ibus gcin ovim msim

scim: $(SCIM_PATH)
$(SCIM_PATH): $(XML_PATH)
	mkdir -p $(SCIM_PATH)
	for im in $(IMLIST);\
	do\
		xsltproc -param UUID \"`uuidgen`\" -param SERIAL \"`date +%Y%m%d`\" -param ICON_DIR \"/usr/share/scim/icon/\" -param ICON_FILE \"qh$$im.svg\" \
			-o $(SCIM_PATH)/qh$$im.scim xslt/scim.xslt tables/xml/qh$$im.xml;\
		scim-make-table $(SCIM_PATH)/qh$$im.scim -b -o $(SCIM_PATH)/qh$$im.bin;\
	done
	touch $(SCIM_PATH)

ibus: $(IBUS_PATH)
$(IBUS_PATH): $(XML_PATH)
	mkdir -p $(IBUS_PATH)
	mkdir -p tmp
	for im in $(IMLIST);\
	do\
		xsltproc -param UUID \"`uuidgen`\" -param SERIAL \"`date +%Y%m%d`\" -param ICON_DIR \"/usr/share/scim/icon/\" -param ICON_FILE \"qh$$im.svg\" \
			-o $(IBUS_PATH)/qh$$im.ibus xslt/ibus.xslt tables/xml/qh$$im.xml;\
		bash -c "cd tmp; ibus-table-createdb -s ../$(IBUS_PATH)/qh$$im.ibus";\
	done
	cp tmp/*.db $(IBUS_PATH)
	touch $(IBUS_PATH)

gcin: $(GCIN_PATH)
$(GCIN_PATH): $(XML_PATH)
	mkdir -p $(GCIN_PATH)
	for im in $(IMLIST);\
	do\
		xsltproc -o $(GCIN_PATH)/qh$$im.cin xslt/gcin.xslt $(XML_PATH)/qh$$im.xml;\
		gcin2tab $(GCIN_PATH)/qh$$im.cin;\
	done
	touch $(GCIN_PATH)

ovim: $(OVIM_PATH)
$(OVIM_PATH): $(XML_PATH)
	mkdir -p $(OVIM_PATH)
	for im in $(IMLIST);\
	do\
		xsltproc -o $(OVIM_PATH)/qh$$im.cin xslt/ovim.xslt $(XML_PATH)/qh$$im.xml;\
	done
	touch $(OVIM_PATH)

msim: $(MSIM_PATH)
$(MSIM_PATH): $(XML_PATH)
	mkdir -p $(MSIM_PATH)
	for im in $(IMLIST);\
	do\
		xsltproc -o $(MSIM_PATH)/qh$$im.msim xslt/msim.xslt $(XML_PATH)/qh$$im.xml;\
		sed 's/$$'"/`echo \\\r`/" $(MSIM_PATH)/qh$$im.msim > tmp/qh$$im.msim.dos;\
		iconv -f utf-8 -t utf-16le tmp/qh$$im.msim.dos > $(MSIM_PATH)/qh$$im.msim.txt;\
	done
	touch $(MSIM_PATH)

svg: $(SVG_PATH)
$(SVG_PATH): $(XML_PATH)
	mkdir -p $(SVG_PATH)
	tools/gensvg.py

pdf: doc/qiangheng.pdf

doc/qiangheng.pdf: doc/lyx/qiangheng.lyx
	lyx -E pdf4 doc/qiangheng.pdf doc/lyx/qiangheng.lyx

all-icons:
	mkdir -p $(SCIM_ICON_PATH) $(GCIN_ICON_PATH) $(OVIM_ICON_PATH) $(MSIM_ICON_PATH) $(IBUS_ICON_PATH)
	for im in $(IMLIST);\
	do\
		convert -resize 48x48 $(ICON_ORIGIN_PATH)/qh$$im.svg $(SCIM_ICON_PATH)/qh$$im.png;\
		convert -resize 48x48 $(ICON_ORIGIN_PATH)/qh$$im.svg $(GCIN_ICON_PATH)/qh$$im.png;\
		convert -resize 48x48 $(ICON_ORIGIN_PATH)/qh$$im.svg $(OVIM_ICON_PATH)/qh$$im.png;\
		cp $(ICON_ORIGIN_PATH)/qh$$im.svg $(IBUS_ICON_PATH)/qh$$im.png;\
	done
	convert -resize 64x64 $(ICON_ORIGIN_PATH)/qiangheng.svg $(ICON_PLATFORM_PATH)/qiangheng.png;

tarballs: pre-tarballs pdf tarball-src
	make tarball-src VERSION=$(VERSION)
	make prepare
	make xml yaml imtables
	make imtables
	make svg
	make tarballs-platform VERSION=$(VERSION)
	make tarball-all VERSION=$(VERSION)

pre-tarballs:
	make clean
	mkdir -p $(TARBALLS_PATH)

tarball-src:
	git archive --format=tar -o $(TARBALLS_PATH)/qiangheng-src-$(VERSION).tar HEAD
	tar -rf $(TARBALLS_PATH)/qiangheng-src-$(VERSION).tar doc/qiangheng.pdf
	bzip2 -c $(TARBALLS_PATH)/qiangheng-src-$(VERSION).tar > $(TARBALLS_PATH)/qiangheng-src-$(VERSION).tar.bz2

tarballs-platform: all-icons
	tar cjf $(TARBALLS_PATH)/qiangheng-scim-$(VERSION).tar.bz2 --exclude-vcs $(XFORM) $(SCIM_PATH)/*.bin $(ICON_PATH) doc/qiangheng.pdf README.md
	tar cjf $(TARBALLS_PATH)/qiangheng-ibus-$(VERSION).tar.bz2 --exclude-vcs $(XFORM) $(IBUS_PATH)/*.db $(ICON_PATH) doc/qiangheng.pdf README.md
	tar cjf $(TARBALLS_PATH)/qiangheng-gcin-$(VERSION).tar.bz2 --exclude-vcs $(XFORM) $(GCIN_PATH)/*.gtab $(ICON_PATH) doc/qiangheng.pdf README.md
	tar cjf $(TARBALLS_PATH)/qiangheng-ovim-$(VERSION).tar.bz2 --exclude-vcs $(XFORM) $(OVIM_PATH)/*.cin $(ICON_PATH) doc/qiangheng.pdf README.md
	tar cjf $(TARBALLS_PATH)/qiangheng-msim-$(VERSION).tar.bz2 --exclude-vcs $(XFORM) $(MSIM_PATH)/*.txt $(ICON_PATH) doc/qiangheng.pdf README.md
	tar cjf $(TARBALLS_PATH)/qiangheng-svg-$(VERSION).tar.bz2 --exclude-vcs $(XFORM) font/svg/* doc/qiangheng.pdf README.md

tarball-all:
	tar cjf $(TARBALLS_PATH)/qiangheng-$(VERSION).tar.bz2 --exclude-vcs --exclude=tarballs -C .. qiangheng

python-fontforge: fontforge/CMakeLists.txt
	rm -rf fontforge/build tools/fontforge.so

	# https://github.com/fontforge/fontforge/issues/5251
	cd fontforge; sed -i.orig 's/\(%[^%[:space:]]*\)hs/\1s/g' fontforgeexe/searchview.c po/de.po po/ca.po po/hr.po po/it.po po/pl.po po/uk.po po/en_GB.po po/fr.po po/vi.po po/ko.po po/ja.po;

	cd fontforge; ( \
		mkdir build; \
		cd build; \
		cmake -GNinja .. -DPython3_EXECUTABLE=`which python3`; \
		ninja; \
		)
	cd tools; ln -s ../fontforge/build/lib/fontforge.so .

fontforge/CMakeLists.txt:
	git clone -b 20230101 https://github.com/fontforge/fontforge.git

clean:
	rm -rf $(ICON_PLATFORM_PATH)
	rm -rf $(GEN_PATH)
	rm -rf tables/ tmp/ tarballs/ font/qhdc.ttf
	rm -f `find src -name "*.pyc"`
	rm -f *~ scim/* gcin/* msim/* tex/*.aux tex/*.log tex/*.pdf

