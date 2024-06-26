# 瑲珩

瑲珩（ㄑㄧㄤ　ㄏㄥˊ）以動態生成的方式產生輸入法的表格。
目前專注在於倉頡、行列、大易、嘸蝦米、鄭碼等輸入法。

瑲珩專注在於自動生成輸入法的表格。目前專注在於倉頡、行列、大易、嘸蝦米、鄭碼等輸入法。
亦即建立每個字的結構描述，以一些基礎字根及字的字碼，並透過輸入法的演算法來自動產生所有
字的字碼。

環境
====
目前專案是以 Python3 寫成，並且搭配許多套件、工具及函式庫，因此需要安裝。包含：
+ Python 3
+ Python 函式庫
  + lxml
  + ruamel.yaml
  + injector
  + ply
  + Xie
    用於動態組字。
    可到 https://github.com/xrloong/Xie 下載[最新版本](https://github.com/xrloong/Xie/releases/download/v0.1.5/Xie-0.1.5-py3-none-any.whl)
+ 工具
  + xsltproc
  + xmllint

可以透過 make 來安裝（目前支援 Ubuntu、MacOS、FreeBSD）
```console
$ make setup-environment
```

也可手動安裝：
在 Ubutnu 上，
```console
$ apt-get install python3
$ apt-get install xsltproc libxml2-utils
```

在 Mac 上，因本身就已有 xsltproc、xmllint，不用特別安裝。
```console
$ brew install python3
```

在 FreeBSD 上，
```console
$ pkg install python37 py37-pip
$ pkg install py37-lxml
$ pkg install libxml2-utils
```

在各平台共同的部分：
```console
$ pip3 install lxml ruamel.yaml injector ply numpy pydantic
$ pip3 install https://github.com/xrloong/Xie/releases/download/v0.1.5/Xie-0.1.5-py3-none-any.whl
```

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
$ tools/showglyph.py
```

產生字型
--------
本程式使用 FontForge 來產生字型。目前有兩種方式：一種是產生 TrueType 字型檔，一種是為每個字符生成 SVG 圖檔。

* 産生 TrueType 字型檔：
  使用到 FontForge 的 Python3 擴充。

  在 Ubuntu 20.04 上，可以安裝 python3-fontforge：
  ```console
  $ apt-get install python3-fontforge
  ```

  在 MacOS 上，安裝 fontforge 後，會同時安裝其 Python3 擴充：
  ```console
  $ brew insatll fontforge
  ```

  在 FreeBSD 上，安裝 fontforge 後，也會同時安裝其 Python3 擴充：
  ```console
  $ pkg insatll fontforge
  ```

  在其它不支援的環境，可以使用下列命令：
  ```console
  $ make python-fontforge
  ```
  其大致會做以下幾件事：
  1. 下載 [FontForge](https://github.com/fontforge/fontforge.git) 源碼
  2. 以 Python3 來組態與編譯（需要額外安裝 libtool、libglib2.0-dev、libfreetype6-dev、libxml2-dev）
  3. 產生連結檔 src/fontforge.so ，會連結到 fontforge/pyhook/.libs/fontforge.so

  產生字型檔指令如下，預設輸出檔為 font/qhdc.ttf ：
  ```console
  $ tools/genttf.py
  ```

* 産生 SVG 圖檔：
  ```console
  $ tools/gensvg.py
  ```

實作
====

主要流程
--------

對於每個字符，主要經過 3 個階段：
1. 共通轉換：即不論是使用何種輸入法、描繪法都成立的轉換。
2. 共通轉換：針對個別輸入法、描繪法的轉換。尋找特殊結構，進行其方法相應的轉換。
3. 編碼：根據輸入法來為字法編碼，或根據描繪法來描繪結果。

行列、嘸蝦米、大易
------------------

這三個輸入法規則都是很類似的，即根據其各自定義的字根表及規則，將一個字拆成多個字根，並取前三碼及尾碼。

一個字，如果是由多個小字組合而成，那將所有小字的的全字根合起來後，即為原字的全部字根。
將所有小字的前三後一合起來後，再取前三後一，即為原字的前三後一。

所以，這些輸入法的字根，都需要描述其前三後一。

嘸蝦米的規則為「截長取短」。截長，即若超過四個，則取前三碼及尾碼；取短，即如果不足三碼，要再加上一個補碼。
所以嘸蝦米的每個字根，都要再加上一個屬性以記錄補碼。

鄭碼
----

鄭碼的規則，是根據其字根表及規則，將一個拆成多個字根。再根據字根數量，進行編碼。

一個字，如果是由多個小字組合而成，那將所有小字的的全字根合起來後，即為原字的全部字根。

四角號碼
--------

四角號碼的規則，是取四個角的字形。

一個字，如果是由多個小字組合而成，再根據其組合方式，可以取得原字的四角。

所以，這些輸入法的字根，都需要描述其四個角的編碼。

此外，四角號碼還會針對囗、門、门、鬥、行等特殊處理，所以這幾個字根編碼會需要再附額外標記。

倉頡
----

倉頡的規則，會區分獨體字、合體字及其組合方向，而採用相應的編碼方式。

所以倉頡的字根，會包含其組合方向。

說明
====
參考[說明文件](doc/qiangheng.pdf)。

檔案架構
--------
參考[檔案架構說明](README/FILES.md)。


程式架構說明
------------
請參考 doc/qiangheng.dia （使用 Dia）。

範例
----
參考[範例說明](samples/Sample.md)。

