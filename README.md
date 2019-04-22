# 瑲珩

瑲珩（ㄑㄧㄤ　ㄏㄥˊ）以動態生成的方式產生輸入法的表格。
目前專注在於倉頡、行列、大易、嘸蝦米、鄭碼等輸入法。

瑲珩專注在於自動生成輸入法的表格。目前專注在於倉頡、行列、大易、嘸蝦米、鄭碼等輸入法。
亦即建立每個字的結構描述，以一些基礎字根及字的字碼，並透過輸入法的演算法來自動產生所有
字的字碼。

環境
====
目前專案是以 Python3 寫成，因此需要安裝。
在 Ubutnu 上，
```console
$ apt-get install python3
```
在 Mac 上，
```console
$ brew install python3
```

使用到一些第三方的工具，如 xsltproc、xmllint。
在 Ubutnu 上，
```console
$ apt-get install xsltproc libxml2-utils
```
在 Mac 上，本身就已有這兩個工具，不用特別安裝。

使用到一些第三方的 Python 函式庫，如 lxml、PyYAML、injector、ply。

```console
$ pip3 install lxml PyYAML injector ply
```

如果要使用動態組字，則要另外安裝 Xie （https://github.com/xrloong/Xie）。可下載最新版本，並使用 pip3 來安裝。

計算
====
若之前已經執行計算，且要清除暫存可用：
```console
$ make clean
```

要計算編碼時，要有每個字符的結構資訊，以及字根的編碼資訊，其相關資料放在 qhdata/ 。 
因為歷史因素，原先是使用 XML 格式，而後來改用 YAML 格式。要計算之前，要準備適當的資料
```console
$ make prepare
```
執行過後，會在 gen/ 下產生相關資料。

要計算編碼資訊，可以使用：
```console
$ PYTHONPATH=src:codings/Array time src/qiangheng.py -p coding.Array --format xml
```
其中，PYTHONPATH 用來指定原始碼放置位置，src/ 是主要核心程式碼放置，
而 codings/Array 則是行列輸入法的位置。而 coding.Array 則是行列輸入法的模組名稱。
可以選擇的格式有：xml, yaml, text, quiet 。

目前支援的編碼法（輸入法或描繪法）的相關對照表：

|        |  行列  | 嘸蝦米 |  倉頡  |  大易  |  鄭碼  | 四角號碼 | 動態組字 |
| :----: | :----: | :----: | :----: | :----: | :----: | :------: | :------: |
|     代碼     |   ar   |   bs   |   cj   |   dy   |   zm   |    fc    |    dc    |
|  原始碼位置  |   codings/Array   |   codings/Boshiamy   |   codings/CangJie   |   codings/DaYi   |   codings/ZhengMa   |    codings/FourCorner    |    codings/DynamicComposition    |
|   模組名稱   |   coding.Array   |   coding.Boshiamy   |   coding.CangJie   |   coding.DaYi   |   coding.ZhengMa   |    coding.FourCorner    |    coding.DynamicComposition    |


也可以透過已寫好的 Makefile 來計算。先計算出 xml，再轉成 puretable
```console
$ make xml puretable
```
其結果會放在 tables/ 。

可以用 `CMLIST` 來指定特定編碼法，譬如只想產生「倉頡」的結果，可以使用代碼 cj
```console
$ make xml puretable CMLIST="cj"
```


目前支援的編碼法（輸入法或描繪法）的代碼：

|        |  行列  | 嘸蝦米 |  倉頡  |  大易  |  鄭碼  | 四角號碼 | 動態組字 |
| :----: | :----: | :----: | :----: | :----: | :----: | :------: | :------: |
|  代碼  |   ar   |   bs   |   cj   |   dy   |   zm   |    fc    |    dc    |

```console
$ src/qiangheng.py -p cj --format=xml
```

輸入法
======
安裝
----
* IBus

  輸入法檔案為 tables/ibus/*.db ，圖示檔為 icons/*.svg 。
  選擇所要使用的輸入法，
  將輸入法檔複製到 /usr/share/ibus-table/tables，將圖示檔複製到 /usr/share/ibus-table/icons 。

  重新載入。

* SCIM

  輸入法檔案為 tables/scim/*.bin ，圖示檔為 icons/*.bin 。
  選擇所要使用的輸入法，
  將輸入法檔複製到 /usr/share/scim/tables，將圖示檔複製到 /usr/share/scim/icons 。

  重新登入。

* GCIN

  輸入法檔案為 tables/gcin/*.gtab ，圖示檔為 pixmaps/*.png 。
  選擇所要使用的輸入法，
  將輸入法檔複製到 /usr/share/gcin/table，將圖示檔複製到 /usr/share/pixmaps/gcin 。
  修改 /usr/share/gcin/table/gtab.list

  重新執行。

* OVIM

  香草輸入法(OpenVanilla)。
  輸入法檔案為 tables/ovim/*.cin ，圖示檔為 pixmaps/*.png 。
  未測試過。請依香草輸入法的方式將相關檔案放置至正確位置。

描繪法
======

秀字程式
--------
秀字程式指令如下：
```console
$ src/hanzitk.py -s -i tables/puretable/qhdc-standard.txt
```

產生字型
--------
本程式使用 FontForge 來產生字型。目前有兩種方式：一種是產生 TrueType 字型檔，一種是為每個字符生成 SVG 圖檔。

* 産生 TrueType 字型檔：
  目前因用於 Python3 的 extention 尚未有預先編譯好的版本，所以要自行編譯。
  請使用下列命令：
  ```console
  $ python-fontforge
  ```
  其大致會做以下幾件事：
  1. 下載 FontForge 源碼（https://github.com/fontforge/fontforge.git）
  2. 以 Python3 來組態與編譯
  3. 產生連結檔 src/fontforge.so ，會連結到 fontforge/pyhook/.libs/fontforge.so
  此外，在執行前，應確認系統有安裝 Python3 的開發資源，如在 Ubuntu 上應安裝 python3-dev 套件。

  產生字型檔指令如下，預設輸出檔為 font/qhdc.ttf ：
  ```console
  $ src/hanzitk.py -g ttf -i tables/puretable/qhdc-standard.txt
  ```

* 産生 SVG 圖檔：
  ```console
  $ /hanzitk.py -g svg -i tables/puretable/qhdc-standard.txt
  ```

檔案架構
========
參考 [FILES.md](https://github.com/xrloong/qiangheng/blob/master/FILES.md)


程式架構說明
============
請參考 doc/qiangheng.dia （使用 Dia）。

