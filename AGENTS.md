# CLAUDE.md

本檔案為 Claude Code（claude.ai/code）在此程式碼庫中工作時的指引。

## 專案概觀

瑲珩（Qiangheng）是一個動態的 CJK 字元輸入法對照表產生器。它透過分析字元結構描述並套用各輸入法專屬的編碼演算法，為多種輸入法（行列、嘸蝦米、倉頡、大易、鄭碼、四角號碼）以及一種繪字方法（動態組字）產生編碼對照表。

## 建置與開發指令

套件管理器：**uv**。所有 Python 執行皆透過 `uv run python3`。

```bash
# 安裝相依套件
make setup-python-environment   # 執行：uv sync --all-extras

# 準備資料（透過 xsltproc 將 XML 轉為 YAML，產生對照表前必須執行）
make prepare

# 產生編碼對照表
make yaml                       # 所有輸入法
make yaml CMLIST="cj"           # 單一輸入法（ar|bs|cj|dy|fc|zm|dc）
make xml                        # XML 輸出格式
make puretable                  # 純文字對應表

# 直接執行單一編碼方法
PYTHONPATH="src:libs:codings/CangJie" uv run python3 src/qiangheng.py -p coding.CangJie

# 執行所有測試
make test

# 執行特定範圍的測試
uv run pytest -c tests/pytest-libs.ini --rootdir=.    # 函式庫測試
uv run pytest -c tests/pytest-cj.ini --rootdir=.      # 倉頡測試
uv run pytest -c tests/pytest-ar.ini --rootdir=.      # 行列測試
# 命名模式：tests/pytest-{ar|bs|cj|dy|fc|zm|dc}.ini

# 執行單一測試檔案
uv run pytest tests/libs/testTreeParser.py

# 效能分析
make profile
```

### Makefile 架構說明

- **`coding_lookup`**（`define` 區塊）— `case` 語句，依輸入法代號（`$cm`）設定 `package` 與 `packageDir` shell 變數，供 `yaml`、`$(YAML_PATH)/qh%.yaml`、`profile` 三個目標使用
- **`prepare-main`** — 將主字元結構 XML 轉為 YAML，並依各輸入法拆分字根檔
- **`prepare-%`**（模式規則）— 處理 `ar/bs/cj/dy/fc/zm`：複製設定檔、格式化 XML、轉為 YAML
- **`prepare-dc`**（具名規則）— 同上但使用 `xslt/xml2yaml-dc.xslt`（dc 專用轉換）
- **平台目標**（`scim`、`ibus`、`gcin`、`ovim`、`msim`）— 將 XML 對照表轉換為各輸入平台格式，需對應平台工具（`scim-make-table`、`ibus-table-createdb`、`gcin2tab` 等）

## 架構

### 三階段處理流程

每個字元經過：**結構解析 → 編碼 → 輸出**

1. **CharacterStructuringWork**（`src/hanzi/work.py`）— 從資料檔解析字元結構，利用模板與代換規則遞迴展開部件樹
2. **CharacterCodeComputingWork**（`src/hanzi/work.py`）— 對結構化後的字元套用輸入法的編碼演算法
3. **Writer**（`src/writer.py`）— 將結果輸出為 YAML（主要格式）、XML、純文字或靜默模式

由 `MainManager`（`src/model/MainManager.py`）統籌，依排序後的順序迭代所有字元。

### 原始碼配置

- **`src/`** — 主應用程式：進入點（`qiangheng.py`）、依賴注入（`injection/`）、流程統籌（`model/`）、字元處理（`hanzi/`）、工作區管理（`workspace/`）
- **`libs/`** — 共用函式庫：編碼基底類別（`coding/Base/`）、元素定義（`element/`）、解析器（`parser/`）、樹狀結構（`tree/`）
- **`codings/`** — 可插拔的輸入法實作（每種輸入法一個目錄）
- **`qhdata/`** — 來源資料：字元結構定義（XML）、各輸入法的字根／代換／調整規則
- **`gen/`** — 產生的中間資料（由 `make prepare` 建立）
- **`xslt/`** — 用於 XML→YAML 轉換與輸入法格式產生的 XSLT 轉換
- **`tables/`** — 產生的輸出對照表（yaml/、xml/、puretable/）

### 插件架構（新增／修改輸入法）

每種輸入法位於 `codings/<Name>/coding/<Name>/`，並且必須提供：

- **`__init__.py`** — 匯出：`CodeInfoEncoder`、`CodingRadixParser`、`fontVariance`、`codeMappingInfoInterpreter`、`codingMethodName`、`codingMethodDir`、`CodingRadixFileList`、`CodingSubstituteFileList`、`CodingAdjustFileList`
- **`<Name>.py`** — 實作三個類別，繼承自 `libs/coding/Base/` 的基底類別：
  - `CodeInfo` — 表示一個字元的編碼（字根碼、位置）
  - `CodeInfoEncoder` — 依組字運算子（龜、龍、雀、蚕、鴻、回等）對字元編碼
  - `CodingRadixParser` — 從 YAML 解析輸入法專屬的字根定義

輸入法代號：`ar`（行列）、`bs`（嘸蝦米）、`cj`（倉頡）、`dy`（大易）、`zm`（鄭碼）、`fc`（四角號碼）、`dc`（動態組字）

### 依賴注入

使用 `injector` 函式庫。模組定義於 `src/injection/module.py`：`PackageModule`、`ManagerModule`、`IOModule`、`CharacterModule`、`ParserModule`。主要繫結位於 `src/injection/key.py`。

### PYTHONPATH 需求

執行應用程式或測試時，PYTHONPATH 必須包含 `src`、`libs` 以及相關的編碼目錄（例如 `codings/CangJie`）。Makefile 與 pytest 的 `.ini` 檔會自動處理這些設定。每個 pytest 設定檔（`tests/pytest-{method}.ini`）的 `pythonpath` 都包含對應的編碼目錄。

### 資料流程

```
qhdata/*.xml  →  xsltproc  →  gen/qhdata/*.yaml  →  Python 處理  →  tables/
```

任何對照表產生前都必須先執行 `make prepare`。它使用 `xsltproc` 與 `xmllint` 將 XML 來源資料轉換為 YAML 中間檔。字元結構資料以中文撰寫（XML 標籤如 `<字符>`、`<字根>`、`<組字/>`）。

### 組字運算子

字元結構以動物／概念命名的運算子描述（定義於 `libs/element/operator.py`）：龜、龍、雀、蚕、鴻、回等。這些運算子表示部件之間的空間關係（上下、左右、包圍等）。`CodeInfoEncoder.setByComps()` 方法透過 match/case 分派至各運算子專屬的編碼邏輯。
