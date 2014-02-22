瑲珩（ㄑㄧㄤ　ㄏㄥˊ）名字取自於“倉”頡及“行”列的頭一個字再加玉字

瑲珩專注在於自動生成輸入法的表格。目前專注在於倉頡、行列、大易、嘸蝦米、鄭碼等輸入法。
亦即建立每個字的結構描述，以一些基礎字根及字的字碼，並透過輸入法的演算法來自動產生所有
字的字碼。

== 安裝 ==
請參考 doc/install.txt

== 原理說明 ==
請參考 tex/principle.pdf

== 釋出歷史 ==
請參考 doc/release.txt

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

== 程式架構說明 ==
請參考 doc/qiangheng.dia （使用 Dia）。

