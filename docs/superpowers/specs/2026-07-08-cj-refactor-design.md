# 倉頡（CangJie）重構設計

日期：2026-07-08  
範圍：`codings/CangJie/coding/CangJie/CangJie.py`

## 背景

現有倉頡實作有三層問題，由淺到深：

1. **表面問題**：死碼、方向魔術字串、可變旗標
2. **設計臭味**：`CJCodeHelper` 破壞式讀取（stateful, mutable）、`ContainerCJCodeHelper` 大量重複邏輯
3. **架構問題**：`CJLump` 混合資料與靜態工廠方法；`ContainerCJLump` 透過繼承表達結構差異，但 override 行為過多

重構分三階段逐步進行，每階段獨立驗證（`make test` + `uv run pytest -c tests/pytest-cj.ini --rootdir=.`）並 commit。

---

## 第一階段：清理表面問題

### 1-A 移除死碼

`CJCodeInfo.code`（第 292–293 行）：

```python
# 移除此行（立即被下一行覆蓋，無效）
rtlist = self.cjLumpList
```

### 1-B Direction enum

新增 `Direction(str, Enum)` 取代魔術字串：

```python
class Direction(str, Enum):
    LOONG    = "*"
    SPARROW  = "$"
    SILKWORM = "|"
    GOOSE    = "-"
    LOOP     = "@"
    GRID     = "+"
```

替換範圍：`CJCodeInfo`、`CJCodeInfoEncoder`、`computeLumpListInDirection` 內所有字串比較。

### 1-C 消除 `isBodyContainer` 可變旗標

目前模式（臨時設值再重設）：

```python
lastCJLump.isBodyContainer = True
[f, c, i] = lastCJLump.getXCode()
lastCJLump.isBodyContainer = False
```

改法：`getXCode()` 接受參數，移除實例欄位：

```python
# CJLump
def getXCode(self, as_body_container=False):
    return [self.frontCode, self.containerCode, self.interiorCode]

# ContainerCJLump
def getXCode(self, as_body_container=False):
    if as_body_container:
        return [outerFront, outerContainer, self.innerLump.getCodeAsTail()]
    else:
        return [outerFront, outerContainer, self.innerLump.getCodeAsBody()]
```

呼叫端：

```python
[f, c, i] = lastCJLump.getXCode(as_body_container=True)
```

`isBodyContainer` 實例欄位從 `CJLump` 與 `ContainerCJLump` 全部移除。

---

## 第二階段：純函式取碼

### 核心：`extract_code` 純函式

取碼邏輯本質是「從有序碼段序列，從前取頭、從後取尾」。以純函式實作：

```python
def extract_code(segments: list[str], head_count: int, tail_count: int) -> str:
    """
    從有序碼段序列取碼。
    - 頭碼：從序列前端依序消耗，段用完後往下一段
    - 尾碼：從序列後端反序消耗，段用完後往上一段
    不修改輸入；使用 index 追蹤位置。
    """
```

### 替換 `CJCodeHelper`

`CJLump.getCode()` 直接呼叫 `extract_code`：

```python
def getCode(self, head_count, tail_count):
    segments = [self.frontCode, self.containerCode, self.interiorCode]
    return extract_code(segments, head_count, tail_count).lower()
```

`getHelper()` 方法移除。

### 替換 `ContainerCJCodeHelper`

`ContainerCJLump.getCode()` 以 6 段呼叫 `extract_code`：

```python
def getCode(self, head_count, tail_count):
    outer, inner = self.outerLump, self.innerLump
    segments = [
        outer.frontCode, outer.containerCode,
        inner.frontCode, inner.containerCode,
        outer.interiorCode, inner.interiorCode,
    ]
    return extract_code(segments, head_count, tail_count).lower()
```

**刪除**：`CJCodeHelper`、`ContainerCJCodeHelper`、`CJLump.getHelper()`、`ContainerCJLump.getHelper()`。

---

## 第三階段：重新設計 CJLump 層次

### `CJLump` 改為 dataclass

```python
@dataclass
class CJLump:
    front: str
    container: str
    interior: str
```

原有 `generate(frontCode, containerCode, interiorCode)` 靜態方法刪除，呼叫端改為直接 `CJLump(front, container, interior)`。

測試 `tests/cj/testCJLump.py` 中所有 `CJLump.generate(...)` 呼叫需同步改為 `CJLump(...)`。`computeTotalCode` helper 方法改為呼叫模組層級 `compute_total_code()`。

### `ContainerCJLump` 改為獨立 dataclass

```python
@dataclass
class ContainerCJLump:
    outer: CJLump
    inner: CJLump
```

不再繼承 `CJLump`；取碼函式以 `isinstance` 或 `Union` type 分派。

### 工廠方法移至模組層級函式

原靜態方法移出為模組層級函式：

```python
def make_body_lump(lumps: list) -> CJLump | ContainerCJLump: ...
def make_singleton_lump(lumps: list) -> CJLump | ContainerCJLump: ...
def make_container_lump(lumps: list) -> ContainerCJLump: ...
def compute_total_code(lumps: list) -> str: ...
def compute_body_code(lumps: list) -> str: ...
def compute_singleton_code(lumps: list) -> str: ...
```

### `GridCJCodeInfo` 改為 dataclass 風格

```python
@dataclass
class GridCJCodeInfo(CJCodeInfo):
    code_info_v: CJCodeInfo
    code_info_h: CJCodeInfo
```

移除手動 `__init__`，改用 dataclass 自動產生。

---

## 驗證策略

每階段完成後執行：

```bash
uv run pytest -c tests/pytest-cj.ini --rootdir=.
make test
```

確認全數通過後才 commit。

## 命名風格

- 新模組層級函式：`snake_case`
- 類別方法維持現有 `camelCase`（避免無謂改動）
- `Direction` enum：`UPPER_CASE` 成員名稱
