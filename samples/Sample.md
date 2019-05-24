# 範例

這個以「中國字庋㩪」為例，說明如何增加一個新的輸入法。
1. 在 sample/GuiXie/ 增加相關檔案，包含：
   1. 編碼法資訊：
      * qhdata/info.yaml

        關於編碼法的一些資訊。
   2. 編碼法字根相關編碼：
      * qhdata/radix/CJK.yaml 和 qhdata/radix/CJK-A.yaml

        在 CJK 和 CJK Ext-A 中，一些基本字根編碼。
      * qhdata/radix/adjust.yaml

        對某個編碼法的字根，若有特殊規則不易透過程式來達成，可以在此增加。
      * qhdata/substitute.yaml

        對某個編碼法，若有特殊模式的規則不易透過程式來達成，可以在此增加。

      以上檔案，可以由 samples/qhdata/ 複製出來。

   3. 程式碼：

      增加相關套件：
      * coding/GuiXie/__init__.py

	包含編碼的一些資訊，有以下變數要定義：
        * codingType
        * fontVariance
        * codeMappingInfoInterpreter

        * codingMethodName
        * codingMethodDir
        * CodingSubstituteFileList
        * CodingRadixFileList
      * coding/GuiXie/GuiXie.py

	實作一些基本類別： CodeInfo、CodeInfoEncoder、CodingRadixParser
        * GXCodeInfo 繼承 CodeInfo: 對於一個字符的基本編碼
        * GXCodeInfoEncoder 繼承 CodeInfoEncoder: 對於多個字符的組合的實偏
        * GXRadixParser 繼承 CodingRadixParser: 用於剖析字根的描述的剖析器

   使用以下方式執行：
   ```console
   $ PYTHONPATH="src:samples/GuiXie" time src/qiangheng.py -p coding.GuiXie > qhgx.yaml
   ```

   使用以下方式測試：
   ```console
   $ PYTHONPATH="src:samples/GuiXie" python3 -m unittest discover samples/GuiXie/test/
   ```
