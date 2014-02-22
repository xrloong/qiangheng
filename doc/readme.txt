瑲珩（ㄑㄧㄤ　ㄏㄥˊ）以動態生成的方式產生輸入法的表格。
目前專注在於倉頡、行列、大易、嘸蝦米、鄭碼等輸入法。

瑲珩專注在於自動生成輸入法的表格。目前專注在於倉頡、行列、大易、嘸蝦米、鄭碼等輸入法。
亦即建立每個字的結構描述，以一些基礎字根及字的字碼，並透過輸入法的演算法來自動產生所有
字的字碼。

== 安裝 ==
請參考 doc/install.txt

== 原理說明 ==
請參考 tex/principle.pdf

== 釋出歷史 ==
請參考 doc/release.txt

== 授權說明 ==
請參考 doc/license.txt

== 用法說明 ==
Usage: qiangheng.py [options]

Options:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config=CONFIG_FILE
                        輸入法設定檔
  --xml
  --text


== 檔案說明 ==
	doc/
		install.txt		安裝說明
		readme.txt		說明文件
		release.txt		釋出歷史
	icons/				圖檔目錄
	Makefile
	qhdata/				字形結構描述資料目錄
	src/				程式碼
	tex/
		principle.pdf		說明文件
	utils/
	xslt/

== 動態組字說明 ==
	動態組字命令如下：
		make dc
	其所使用的字根之字形描述為 qhdata/radix/CJK/dc.xml 。
	其輸出為 tables/puretable/qhdc-standard.txt 。

== 秀字程式說明 ==
	秀字程式指令如下：
		src/hanzitk.py -s -i tables/puretable/qhdc-standard.txt

== 產生字型說明 ==
	本程式使用 FontForge 來產生字型。目前尚未正式支援 Python3 。
	請使用下列命令：
		make python-fontforge
	其大致會做以下幾件事：
		一、下載 FontForge 源碼（http://sourceforge.net/projects/fontforge/files/fontforge-source/fontforge_full-20110222.tar.bz2/download）
		二、以 fontforge/fontforge-20110222.patch 進行補行。
		三、以 Python3 來組態與編譯，
		四、產生連結檔 src/fontforge.so ，會連結到 fontforge/fontforge-20110222/.libs/libfontforge.so
	此外，在執行前，應確認系統有安裝 Python3 的開發資源，如在 Ubuntu 上應安裝 python3-dev 套件。

	產生字型檔指令如下，預設輸出檔為 font/qhdc.ttf ：
		src/hanzitk.py -g -i tables/puretable/qhdc-standard.txt

== 程式架構說明 ==
請參考 doc/qiangheng.dia （使用 Dia）。

