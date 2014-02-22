瑲珩（ㄑㄧㄤ　ㄏㄥˊ）名字取自於“倉”頡及“行”列的頭一個字再加玉字

瑲珩專注在於自動生成輸入法的表格。目前專注在於倉頡、行列、大易、嘸蝦米、鄭碼等輸入法。
亦即建立每個字的結構描述，以一些基礎字根及字的字碼，並透過輸入法的演算法來自動產生所有
字的字碼。

== 安裝 ==
IBus
	輸入法檔案為 tables/ibus/*.db ，圖示檔為 icons/*.svg 。
	選擇所要使用的輸入法，
	將輸入法檔複製到 /usr/share/ibus-table/tables，將圖示檔複製到 /usr/share/ibus-table/icons 。

	重新載入。

SCIM
	輸入法檔案為 tables/scim/*.bin ，圖示檔為 icons/*.bin 。
	選擇所要使用的輸入法，
	將輸入法檔複製到 /usr/share/scim/tables，將圖示檔複製到 /usr/share/scim/icons 。


	重新登入。

GCIN
	輸入法檔案為 tables/gcin/*.gtab ，圖示檔為 pixmaps/*.png 。
	選擇所要使用的輸入法，
	將輸入法檔複製到 /usr/share/gcin/table，將圖示檔複製到 /usr/share/pixmaps/gcin 。
	修改 /usr/share/gcin/table/gtab.list

	重新執行。

OVIM
	香草輸入法(OpenVanilla)。
	輸入法檔案為 tables/ovim/*.cin ，圖示檔為 pixmaps/*.png 。
	未測試過。請依香草輸入法的方式將相關檔案放置至正確位置。

MSIM
	微軟視窗 IME。
	輸入法檔案為 tables/msim/*.cin 。
	請使用「通用輸入法編輯工具」。請點選「附屬應用程式」中的「通用輸入法編輯工具」。
	依步驟完成安裝。
	未測試過。請依香草輸入法的方式將相關檔案放置至正確位置。

== 原理說明 ==
請參考 tex/principle.pdf

== 用法說明 ==
Usage: qiangheng.py [options]

Options:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config=CONFIG_FILE
                        輸入法設定檔
  --xml
  --text


== 檔案說明 ==
   README.txt		說明文件
   character/		字符類別
   im/			處理輸入法相關的元件
   qiangheng.py		主程式
   qhdata/		字的結構描述所在目錄

