# CangJie 重構 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 分三階段重構倉頡輸入法實作，從清理表面問題到架構改善，每階段獨立驗證並 commit。

**Architecture:** 第一階段清理死碼、方向魔術字串、可變旗標；第二階段以純函式 `extract_code` 取代破壞式 helper 類別；第三階段將 `CJLump` 改為 dataclass、移除繼承、把工廠與取碼邏輯移至模組層級函式。

**Tech Stack:** Python 3.13, pytest, uv

## Global Constraints

- 所有 Python 執行用 `uv run`，例如 `uv run pytest`
- 測試指令：`uv run pytest -c tests/pytest-cj.ini --rootdir=. -v`（cj 專用）；`make test`（全套）
- 每個 task 結束前必須全部測試通過
- 不新增任何功能；只重構，不改外部行為
- 主要修改檔案：`codings/CangJie/coding/CangJie/CangJie.py`
- 測試檔案：`tests/cj/testCJLump.py`

---

## Task 1：Phase 1-A — 移除死碼

**Files:**
- Modify: `codings/CangJie/coding/CangJie/CangJie.py:291-293`

**Interfaces:**
- 不新增任何 interface；只刪除一行死碼

- [ ] **Step 1：確認死碼位置**

  ```bash
  grep -n "rtlist = self.cjLumpList" codings/CangJie/coding/CangJie/CangJie.py
  ```

  預期：顯示一行，行號約 292，且下一行為 `rtlist = self.cjLumpListSingleton`。

- [ ] **Step 2：刪除死碼**

  在 `CJCodeInfo.code` property 中，找到：

  ```python
  if self.cjLumpListSingleton:
      rtlist = self.cjLumpList
      rtlist = self.cjLumpListSingleton
      return CJLump.computeTotalCode(rtlist)
  ```

  改為：

  ```python
  if self.cjLumpListSingleton:
      rtlist = self.cjLumpListSingleton
      return CJLump.computeTotalCode(rtlist)
  ```

- [ ] **Step 3：執行測試**

  ```bash
  uv run pytest -c tests/pytest-cj.ini --rootdir=. -v
  ```

  預期：全部通過，無 FAILED。

- [ ] **Step 4：Commit**

  ```bash
  git add codings/CangJie/coding/CangJie/CangJie.py
  git commit -m "refactor(cj): remove dead assignment in CJCodeInfo.code"
  ```

---

## Task 2：Phase 1-B — Direction enum

**Files:**
- Modify: `codings/CangJie/coding/CangJie/CangJie.py`

**Interfaces:**
- 新增 `class Direction(str, Enum)` 供同檔案內部使用
- 不改任何對外 API

- [ ] **Step 1：在檔案頂部加入 import**

  找到現有的 `import re`，在其上方加入：

  ```python
  from enum import Enum
  ```

- [ ] **Step 2：加入 Direction enum**

  在 `import re` 之後、`class CJLump:` 之前，加入：

  ```python
  class Direction(str, Enum):
      LOONG    = "*"
      SPARROW  = "$"
      SILKWORM = "|"
      GOOSE    = "-"
      LOOP     = "@"
      GRID     = "+"
  ```

- [ ] **Step 3：替換 CJCodeInfo 中的方向字串**

  `CJCodeInfo.__init__`：`direction` 參數由呼叫端傳入，不需改。

  `CJCodeInfo.code` property：

  ```python
  # 改前
  if direction == "$":
  # 改後
  if direction == Direction.SPARROW:
  ```

- [ ] **Step 4：替換 CJCodeInfoEncoder 的編碼方法中的方向字串**

  逐一替換下列方法中的 `direction = "..."` 賦值：

  ```python
  def encodeAsLoong(self, codeInfoList):
      direction = Direction.LOONG   # 原為 "*"

  def encodeAsSparrow(self, codeInfoList):
      direction = Direction.SPARROW  # 原為 "$"

  def encodeAsSilkworm(self, codeInfoList):
      direction = Direction.SILKWORM  # 原為 "|"

  def encodeAsGoose(self, codeInfoList):
      direction = Direction.GOOSE  # 原為 "-"

  def encodeAsLoop(self, codeInfoList):
      direction = Direction.LOOP  # 原為 "@"

  def encodeAsMu(self, codeInfoList):
      direction = Direction.SPARROW  # 原為 "$"

  def encodeAsZuo(self, codeInfoList):
      direction = Direction.SPARROW  # 原為 "$"

  def encodeAsJia(self, codeInfoList):
      direction = Direction.SPARROW  # 原為 "$"
  ```

  同時替換 `GridCJCodeInfo.getDirection()` 的回傳值：

  ```python
  def getDirection(self):
      return Direction.GRID  # 原為 "+"
  ```

- [ ] **Step 5：替換 computeLumpListInDirection 中的字串比較**

  完整替換後的方法：

  ```python
  @staticmethod
  def computeLumpListInDirection(direction, codeInfo):
      tmpDirCode = codeInfo.getDirection()

      if direction == Direction.SPARROW:
          lumpList = codeInfo.getLumpList()
      elif tmpDirCode in [Direction.LOOP]:
          tmpRadixList = codeInfo.getLumpList()
          tmpCJLump = CJLump.generateContainer(tmpRadixList)
          lumpList = [tmpCJLump]
      elif tmpDirCode in [Direction.LOONG]:
          tmpRadixList = codeInfo.getLumpList()
          tmpCJLump = CJLump.generateBody(tmpRadixList)
          lumpList = [tmpCJLump]
      elif tmpDirCode in [Direction.GRID] and isinstance(codeInfo, GridCJCodeInfo):
          if direction == Direction.GOOSE:
              newCodeInfo = codeInfo.getCodeInfoH()
              lumpList = newCodeInfo.getLumpList()
          elif direction == Direction.SILKWORM:
              newCodeInfo = codeInfo.getCodeInfoV()
              lumpList = newCodeInfo.getLumpList()
          else:
              ci = codeInfo.getCodeInfoV()
              tmpCJLump = CJLump.generateBody(ci.getLumpList())
              lumpList = [tmpCJLump]
      else:
          if tmpDirCode == direction:
              lumpList = codeInfo.getLumpList()
          else:
              tmpRadixList = codeInfo.getLumpList()
              tmpCJLump = CJLump.generateBody(tmpRadixList)
              lumpList = [tmpCJLump]
      return lumpList
  ```

- [ ] **Step 6：執行測試**

  ```bash
  uv run pytest -c tests/pytest-cj.ini --rootdir=. -v
  ```

  預期：全部通過。

- [ ] **Step 7：Commit**

  ```bash
  git add codings/CangJie/coding/CangJie/CangJie.py
  git commit -m "refactor(cj): introduce Direction enum, replace magic direction strings"
  ```

---

## Task 3：Phase 1-C — 消除 isBodyContainer 可變旗標

**Files:**
- Modify: `codings/CangJie/coding/CangJie/CangJie.py`

**Interfaces:**
- `CJLump.getXCode(as_body_container=False)` — 新增選擇性參數，移除實例欄位 `isBodyContainer`
- `ContainerCJLump.getXCode(as_body_container=False)` — 同上

- [ ] **Step 1：修改 CJLump.__init__ — 移除 isBodyContainer**

  找到：

  ```python
  def __init__(self, frontCode, containerCode, interiorCode):
      self.frontCode = frontCode
      self.containerCode = containerCode
      self.interiorCode = interiorCode

      self.isBodyContainer = False
      self.isDirtySingleton = False
  ```

  改為：

  ```python
  def __init__(self, frontCode, containerCode, interiorCode):
      self.frontCode = frontCode
      self.containerCode = containerCode
      self.interiorCode = interiorCode
  ```

- [ ] **Step 2：修改 CJLump.getXCode — 加入參數（CJLump 本身忽略此參數）**

  找到：

  ```python
  def getXCode(self):
      return [self.frontCode, self.containerCode, self.interiorCode]
  ```

  改為：

  ```python
  def getXCode(self, as_body_container=False):
      return [self.frontCode, self.containerCode, self.interiorCode]
  ```

- [ ] **Step 3：修改 ContainerCJLump.__init__ — 移除 isBodyContainer**

  找到：

  ```python
  def __init__(self, outerLump, innerLump):
      self.outerLump = outerLump
      self.innerLump = innerLump
      self.isBodyContainer = False
  ```

  改為：

  ```python
  def __init__(self, outerLump, innerLump):
      self.outerLump = outerLump
      self.innerLump = innerLump
  ```

- [ ] **Step 4：修改 ContainerCJLump.getXCode — 改用參數取代旗標**

  找到：

  ```python
  def getXCode(self):
      [outerFront, outerContainer, outerInterior] = self.outerLump.getXCode()
      [innerFront, innerContainer, innerInterior] = self.innerLump.getXCode()
      if self.isBodyContainer:
          return [outerFront, outerContainer, self.innerLump.getCodeAsTail()]
      else:
          return [outerFront, outerContainer, self.innerLump.getCodeAsBody()]
  ```

  改為：

  ```python
  def getXCode(self, as_body_container=False):
      [outerFront, outerContainer, outerInterior] = self.outerLump.getXCode()
      if as_body_container:
          return [outerFront, outerContainer, self.innerLump.getCodeAsTail()]
      else:
          return [outerFront, outerContainer, self.innerLump.getCodeAsBody()]
  ```

- [ ] **Step 5：修改 generateBody — 用參數取代旗標設值**

  找到：

  ```python
  @staticmethod
  def generateBody(cjLumpList):
      lastCJLump = cjLumpList[-1]

      lastCJLump.isBodyContainer = True
      [frontCode, containerCode, interiorCode] = lastCJLump.getXCode()
      lastCJLump.isBodyContainer = False

      tmpFrontCode = "".join(x.getCodeAsHead() for x in cjLumpList[:-1])

      tmpCJLump = CJLump.generate(
          tmpFrontCode + frontCode, containerCode, interiorCode
      )
      return tmpCJLump
  ```

  改為：

  ```python
  @staticmethod
  def generateBody(cjLumpList):
      lastCJLump = cjLumpList[-1]
      [frontCode, containerCode, interiorCode] = lastCJLump.getXCode(as_body_container=True)
      tmpFrontCode = "".join(x.getCodeAsHead() for x in cjLumpList[:-1])
      return CJLump.generate(tmpFrontCode + frontCode, containerCode, interiorCode)
  ```

- [ ] **Step 6：修改 generateSingleton — 同上**

  找到：

  ```python
  @staticmethod
  def generateSingleton(cjLumpList):
      lastCJLump = cjLumpList[-1]

      lastCJLump.isBodyContainer = True
      [frontCode, containerCode, interiorCode] = lastCJLump.getXCode()
      lastCJLump.isBodyContainer = False

      tmpFrontCode = "".join(x.getCodeAsBody() for x in cjLumpList[:-1])

      tmpCJLump = CJLump.generate(
          tmpFrontCode + frontCode, containerCode, interiorCode
      )
      return tmpCJLump
  ```

  改為：

  ```python
  @staticmethod
  def generateSingleton(cjLumpList):
      lastCJLump = cjLumpList[-1]
      [frontCode, containerCode, interiorCode] = lastCJLump.getXCode(as_body_container=True)
      tmpFrontCode = "".join(x.getCodeAsBody() for x in cjLumpList[:-1])
      return CJLump.generate(tmpFrontCode + frontCode, containerCode, interiorCode)
  ```

- [ ] **Step 7：確認 isBodyContainer 已完全移除**

  ```bash
  grep -n "isBodyContainer\|isDirtySingleton" codings/CangJie/coding/CangJie/CangJie.py
  ```

  預期：無任何輸出。

- [ ] **Step 8：執行測試**

  ```bash
  uv run pytest -c tests/pytest-cj.ini --rootdir=. -v
  ```

  預期：全部通過。

- [ ] **Step 9：Commit**

  ```bash
  git add codings/CangJie/coding/CangJie/CangJie.py
  git commit -m "refactor(cj): eliminate isBodyContainer mutable flag, use getXCode(as_body_container=)"
  ```

---

## Task 4：Phase 2 — extract_code 純函式，移除 helper 類別

**Files:**
- Modify: `codings/CangJie/coding/CangJie/CangJie.py`
- Create: `tests/cj/testExtractCode.py`

**Interfaces:**
- Produces: `extract_code(segments, head_order, tail_order, head_count, tail_count) -> str`
  - `segments: list[str]` — 碼段列表（不被修改）
  - `head_order: list[int]` — 取頭碼時，依序嘗試的段索引
  - `tail_order: list[int]` — 取尾碼時，依序嘗試的段索引（從段尾取）
  - `head_count: int` — 取幾個頭碼
  - `tail_count: int` — 取幾個尾碼
  - 回傳值：小寫字串

- [ ] **Step 1：撰寫 extract_code 的失敗測試**

  建立 `tests/cj/testExtractCode.py`：

  ```python
  import unittest
  from coding.CangJie.CangJie import extract_code


  class ExtractCodeTestCase(unittest.TestCase):
      # CJLump 使用 head_order=[0,1,2], tail_order=[1,2,0]

      def test_single_segment_head_only(self):
          # CJLump("m","","") getCode(1,0)
          result = extract_code(["m", "", ""], [0,1,2], [1,2,0], 1, 0)
          self.assertEqual(result, "m")

      def test_singleton_short(self):
          # CJLump("mvs","","") getCode(3,1) → "mvs"（共3碼，頭取3、尾無剩）
          result = extract_code(["mvs", "", ""], [0,1,2], [1,2,0], 3, 1)
          self.assertEqual(result, "mvs")

      def test_singleton_long(self):
          # CJLump("mlvs","","") getCode(3,1) → "mlvs"（頭取mlv，尾取s）
          result = extract_code(["mlvs", "", ""], [0,1,2], [1,2,0], 3, 1)
          self.assertEqual(result, "mlvs")

      def test_singleton_very_long(self):
          # CJLump("yukib","","") getCode(3,1) → "yukb"
          result = extract_code(["yukib", "", ""], [0,1,2], [1,2,0], 3, 1)
          self.assertEqual(result, "yukb")

      def test_container_segment_tail_priority(self):
          # CJLump("","WY","i") getCode(0,1) → tail 從 container 取 → "y"
          result = extract_code(["", "WY", "i"], [0,1,2], [1,2,0], 0, 1)
          self.assertEqual(result, "y")

      def test_container_segment_head_and_tail(self):
          # CJLump("","WY","i") getCode(1,1) → head 從 container 取 W，tail 取 Y → "wy"
          result = extract_code(["", "WY", "i"], [0,1,2], [1,2,0], 1, 1)
          self.assertEqual(result, "wy")

      def test_mixed_segments_body(self):
          # CJLump("h","BY","i") getCode(2,1) → head: h, B; tail: Y → "hby"
          result = extract_code(["h", "BY", "i"], [0,1,2], [1,2,0], 2, 1)
          self.assertEqual(result, "hby")

      def test_container_lump_head(self):
          # ContainerCJLump: outerFront="a", outerContainer="B", innerFront="c",
          #                   innerContainer="D", outerInterior="", innerInterior=""
          # head_order=[0,1,2,3,4,5], tail_order=[1,4,3,5,2,0]
          # getCode(1,1) → head: a; tail: B → "ab"
          segs = ["a", "B", "c", "D", "", ""]
          result = extract_code(segs, [0,1,2,3,4,5], [1,4,3,5,2,0], 1, 1)
          self.assertEqual(result, "ab")

      def test_container_lump_singleton(self):
          # getCode(3,1): head: a,B,c; tail from [1,4,3,5,2,0] → B gone → D → "abcd"
          segs = ["a", "B", "c", "D", "", ""]
          result = extract_code(segs, [0,1,2,3,4,5], [1,4,3,5,2,0], 3, 1)
          self.assertEqual(result, "abcd")

      def test_does_not_mutate_input(self):
          segs = ["abc", "DE", "f"]
          extract_code(segs, [0,1,2], [1,2,0], 2, 1)
          self.assertEqual(segs, ["abc", "DE", "f"])


  if __name__ == "__main__":
      unittest.main()
  ```

- [ ] **Step 2：確認測試目前失敗（extract_code 尚不存在）**

  ```bash
  uv run pytest tests/cj/testExtractCode.py -v 2>&1 | head -20
  ```

  預期：`ImportError` 或 `cannot import name 'extract_code'`。

- [ ] **Step 3：實作 extract_code 純函式**

  在 `CangJie.py` 頂部（`import re` 之後、`class Direction` 之前）加入：

  ```python
  def extract_code(
      segments: list,
      head_order: list,
      tail_order: list,
      head_count: int,
      tail_count: int,
  ) -> str:
      segs = list(segments)

      head = []
      for _ in range(head_count):
          for i in head_order:
              if segs[i]:
                  head.append(segs[i][0])
                  segs[i] = segs[i][1:]
                  break

      tail = []
      for _ in range(tail_count):
          for i in tail_order:
              if segs[i]:
                  tail.append(segs[i][-1])
                  segs[i] = segs[i][:-1]
                  break

      return ("".join(head) + "".join(tail)).lower()
  ```

- [ ] **Step 4：執行 extract_code 測試，確認通過**

  ```bash
  uv run pytest tests/cj/testExtractCode.py -v
  ```

  預期：全部 10 個測試通過。

- [ ] **Step 5：用 extract_code 取代 CJLump.getCode()**

  找到：

  ```python
  def getCode(self, headCount, tailCount):
      helper = self.getHelper()
      return helper.getCode(headCount, tailCount).lower()
  ```

  改為：

  ```python
  def getCode(self, headCount, tailCount):
      return extract_code(
          [self.frontCode, self.containerCode, self.interiorCode],
          [0, 1, 2],
          [1, 2, 0],
          headCount, tailCount,
      )
  ```

- [ ] **Step 6：移除 CJLump.getHelper()**

  刪除：

  ```python
  def getHelper(self):
      return CJCodeHelper(self)
  ```

- [ ] **Step 7：為 ContainerCJLump 新增 getCode() override**

  在 `ContainerCJLump` 類別中，在 `getXCode()` 之後加入：

  ```python
  def getCode(self, headCount, tailCount):
      return extract_code(
          [
              self.outerLump.frontCode, self.outerLump.containerCode,
              self.innerLump.frontCode, self.innerLump.containerCode,
              self.outerLump.interiorCode, self.innerLump.interiorCode,
          ],
          [0, 1, 2, 3, 4, 5],
          [1, 4, 3, 5, 2, 0],
          headCount, tailCount,
      )
  ```

  **注意**：`ContainerCJLump.getCodeAsBody()` 保留不動（它有特殊邏輯，不呼叫 `getCode(2,1)`）。

- [ ] **Step 8：移除 ContainerCJLump.getHelper()**

  刪除：

  ```python
  def getHelper(self):
      return ContainerCJCodeHelper(self.outerLump, self.innerLump)
  ```

- [ ] **Step 9：刪除 CJCodeHelper 與 ContainerCJCodeHelper 類別**

  刪除完整的 `class CJCodeHelper:` 定義（約 50 行）與 `class ContainerCJCodeHelper(CJCodeHelper):` 定義（約 65 行）。

- [ ] **Step 10：確認 helper 類別已完全移除**

  ```bash
  grep -n "CJCodeHelper\|ContainerCJCodeHelper\|getHelper" codings/CangJie/coding/CangJie/CangJie.py
  ```

  預期：無任何輸出。

- [ ] **Step 11：執行全套 cj 測試**

  ```bash
  uv run pytest -c tests/pytest-cj.ini --rootdir=. -v
  ```

  預期：全部通過（含 testCJLump.py 與 testExtractCode.py）。

- [ ] **Step 12：執行 make test**

  ```bash
  make test
  ```

  預期：全部通過。

- [ ] **Step 13：Commit**

  ```bash
  git add codings/CangJie/coding/CangJie/CangJie.py tests/cj/testExtractCode.py
  git commit -m "refactor(cj): replace CJCodeHelper with pure extract_code function"
  ```

---

## Task 5：Phase 3-A — CJLump 欄位改名 + 靜態工廠方法升為模組層級函式

**Files:**
- Modify: `codings/CangJie/coding/CangJie/CangJie.py`

**Interfaces:**
- `CJLump` 欄位：`front: str`, `container: str`, `interior: str`（原 `frontCode`, `containerCode`, `interiorCode`）
- `ContainerCJLump` 欄位：`outer: CJLump`, `inner: CJLump`（原 `outerLump`, `innerLump`）
- 新增模組層級函式（取代 `CJLump` 靜態方法）：
  - `make_body_lump(lumps) -> CJLump`
  - `make_singleton_lump(lumps) -> CJLump`
  - `make_container_lump(lumps) -> ContainerCJLump`
  - `compute_total_code(lumps) -> str`
  - `compute_body_code(lumps) -> str`
  - `compute_singleton_code(lumps) -> str`

- [ ] **Step 1：改名 CJLump 欄位**

  `CJLump.__init__` 改為：

  ```python
  def __init__(self, front, container, interior):
      self.front = front
      self.container = container
      self.interior = interior
  ```

  同時更新同類別內所有參照（`getXCode`, `getCode`, `getFrontCode`, `getContainerCode`, `getInteriorCode`, `__str__`）：

  ```python
  def __str__(self):
      return "%s" % self.getXCode()

  def getFrontCode(self):
      return self.front

  def getContainerCode(self):
      return self.container

  def getInteriorCode(self):
      return self.interior

  def getXCode(self, as_body_container=False):
      return [self.front, self.container, self.interior]

  def getCode(self, headCount, tailCount):
      return extract_code(
          [self.front, self.container, self.interior],
          [0, 1, 2],
          [1, 2, 0],
          headCount, tailCount,
      )
  ```

- [ ] **Step 2：改名 ContainerCJLump 欄位**

  `ContainerCJLump.__init__`：

  ```python
  def __init__(self, outer, inner):
      self.outer = outer
      self.inner = inner
  ```

  更新 `ContainerCJLump` 內所有 `self.outerLump` → `self.outer`，`self.innerLump` → `self.inner`：

  ```python
  def getHelper(self):  # 此方法已在 Task 4 移除，跳過
      pass

  def getCode(self, headCount, tailCount):
      return extract_code(
          [
              self.outer.front, self.outer.container,
              self.inner.front, self.inner.container,
              self.outer.interior, self.inner.interior,
          ],
          [0, 1, 2, 3, 4, 5],
          [1, 4, 3, 5, 2, 0],
          headCount, tailCount,
      )

  def getCodeAsBody(self):
      code = self.outer.getCodeAsHead()
      if len(code) == 1:
          code += self.inner.getCodeAsHead()
      elif len(code) == 2:
          code += self.inner.getCodeAsTail()
      return code

  def getXCode(self, as_body_container=False):
      [outerFront, outerContainer, outerInterior] = self.outer.getXCode()
      if as_body_container:
          return [outerFront, outerContainer, self.inner.getCodeAsTail()]
      else:
          return [outerFront, outerContainer, self.inner.getCodeAsBody()]
  ```

- [ ] **Step 3：確認舊欄位名稱已完全消失**

  ```bash
  grep -n "frontCode\|containerCode\|interiorCode\|outerLump\|innerLump" \
      codings/CangJie/coding/CangJie/CangJie.py
  ```

  預期：無任何輸出。

- [ ] **Step 4：新增模組層級工廠與計算函式**

  在 `extract_code` 函式之後、`class CJLump:` 之前，加入以下函式（此時先以 forward reference 方式定義，類別在後面）。

  **注意**：這些函式定義在類別之後才能使用，所以實際上要放在所有類別定義結束之後。請在 `class CJRadixParser` 結束後，檔案末尾加入：

  ```python
  # ── 模組層級工廠與計算函式（取代 CJLump 靜態方法）─────────────────────────

  def make_body_lump(lumps):
      last = lumps[-1]
      front, container, interior = last.getXCode(as_body_container=True)
      tmp_front = "".join(x.getCodeAsHead() for x in lumps[:-1])
      return CJLump(tmp_front + front, container, interior)


  def make_singleton_lump(lumps):
      last = lumps[-1]
      front, container, interior = last.getXCode(as_body_container=True)
      tmp_front = "".join(x.getCodeAsBody() for x in lumps[:-1])
      return CJLump(tmp_front + front, container, interior)


  def make_container_lump(lumps):
      first = lumps[0]
      front, container, interior = first.getXCode()
      tmp_lump = make_body_lump(lumps[1:])
      outer = CJLump(front, container, interior)
      return ContainerCJLump(outer, tmp_lump)


  def compute_body_code(lumps):
      if len(lumps) == 1:
          return lumps[0].getCodeAsBody()
      elif len(lumps) > 1:
          head_code = lumps[0].getCodeAsHead()
          if lumps[0].isHeadWithOne():
              tmp = make_body_lump(lumps[1:])
              return head_code + tmp.getCodeAsHead()
          else:
              return head_code + lumps[-1].getCodeAsTail()
      return ""


  def compute_total_code(lumps):
      if len(lumps) == 1:
          return lumps[0].getCodeAsSingleton()
      elif len(lumps) > 1:
          return lumps[0].getCodeAsHead() + compute_body_code(lumps[1:])
      return ""


  def compute_singleton_code(lumps):
      tmp = make_singleton_lump(lumps)
      return tmp.getCodeAsSingleton()
  ```

- [ ] **Step 5：更新 CJLump 靜態方法，改為呼叫新模組層級函式**

  將 `CJLump` 中的靜態方法改為 thin wrapper（之後 Task 6 會移除這些靜態方法；現在保留以確保漸進式改動不破壞測試）：

  ```python
  @staticmethod
  def computeTotalCode(cjLumpList):
      return compute_total_code(cjLumpList)

  @staticmethod
  def computeBodyCode(cjLumpList):
      return compute_body_code(cjLumpList)

  @staticmethod
  def computeSingletonCode(cjLumpList):
      return compute_singleton_code(cjLumpList)

  @staticmethod
  def generateBody(cjLumpList):
      return make_body_lump(cjLumpList)

  @staticmethod
  def generateSingleton(cjLumpList):
      return make_singleton_lump(cjLumpList)

  @staticmethod
  def generateContainer(cjLumpList):
      return make_container_lump(cjLumpList)
  ```

  **注意**：這些靜態方法現在只是 wrapper，方便漸進移除。

- [ ] **Step 6：更新 CJRadixParser.parseCJLumpList — 改用 CJLump 建構子**

  找到：

  ```python
  cjLump = CJLump.generate(frontCode, containerCode, interiorCode)
  ```

  改為：

  ```python
  cjLump = CJLump(frontCode, containerCode, interiorCode)
  ```

  同時刪除 `CJLump.generate` 靜態方法（其他地方不再使用）：

  ```python
  # 刪除以下方法：
  @staticmethod
  def generate(frontCode, containerCode, interiorCode):
      return CJLump(frontCode, containerCode, interiorCode)
  ```

- [ ] **Step 7：更新測試 testCJLump.py — CJLump.generate() → CJLump()**

  在 `tests/cj/testCJLump.py` 的 `setUpLumps` 方法中，將所有 `CJLump.generate(...)` 改為 `CJLump(...)`，例如：

  ```python
  # 改前
  self.lump_一 = CJLump.generate("m", "", "")
  # 改後
  self.lump_一 = CJLump("m", "", "")
  ```

  同時更新 `computeTotalCode` helper：

  ```python
  def computeTotalCode(self, lumpList):
      return compute_total_code(lumpList)
  ```

  並在檔案頂部加入 import：

  ```python
  from coding.CangJie.CangJie import CJLump, compute_total_code
  ```

  （原有 `from coding.CangJie.CangJie import CJLump` 改為上面這行。）

- [ ] **Step 8：執行全套 cj 測試**

  ```bash
  uv run pytest -c tests/pytest-cj.ini --rootdir=. -v
  ```

  預期：全部通過。

- [ ] **Step 9：Commit**

  ```bash
  git add codings/CangJie/coding/CangJie/CangJie.py tests/cj/testCJLump.py
  git commit -m "refactor(cj): rename CJLump fields, extract module-level factory functions"
  ```

---

## Task 6：Phase 3-B — 移除靜態方法殘留、CJLump 改 dataclass、ContainerCJLump 改獨立 dataclass

**Files:**
- Modify: `codings/CangJie/coding/CangJie/CangJie.py`

**Interfaces:**
- `CJLump` 成為 `@dataclass`，只剩 `front`, `container`, `interior` 三個欄位及取碼實例方法
- `ContainerCJLump` 成為獨立 `@dataclass`（不繼承 `CJLump`），只剩 `outer`, `inner` 兩個欄位及取碼實例方法
- 移除 `CJLump.computeTotalCode`, `computeBodyCode`, `computeSingletonCode`, `generateBody`, `generateSingleton`, `generateContainer`, `generate` 靜態方法

- [ ] **Step 1：加入 dataclass import**

  在 `CangJie.py` 頂部找到 `from enum import Enum`，改為：

  ```python
  from dataclasses import dataclass
  from enum import Enum
  ```

- [ ] **Step 2：將 CJLump 改為 @dataclass**

  替換 `CJLump.__init__`，加上 `@dataclass` decorator，並移除所有靜態方法 wrapper（Task 5 Step 5 新增的那些）。完整的新 `CJLump` 類別：

  ```python
  @dataclass
  class CJLump:
      front: str
      container: str
      interior: str

      def getFrontCode(self):
          return self.front

      def getContainerCode(self):
          return self.container

      def getInteriorCode(self):
          return self.interior

      def getXCode(self, as_body_container=False):
          return [self.front, self.container, self.interior]

      def getCode(self, headCount, tailCount):
          return extract_code(
              [self.front, self.container, self.interior],
              [0, 1, 2],
              [1, 2, 0],
              headCount, tailCount,
          )

      def isHeadWithOne(self):
          return len(self.getCodeAsHead()) == 1

      def getCodeAsSingleton(self):
          return self.getCode(3, 1)

      def getCodeAsHead(self):
          return self.getCode(1, 1)

      def getCodeAsBody(self):
          return self.getCode(2, 1)

      def getCodeAsTail(self):
          return self.getCode(0, 1)
  ```

  **靜態方法全部移除**（`computeTotalCode`, `computeBodyCode`, `computeSingletonCode`, `generate`, `generateBody`, `generateSingleton`, `generateContainer`）。

- [ ] **Step 3：將 ContainerCJLump 改為獨立 @dataclass（不繼承 CJLump）**

  ```python
  @dataclass
  class ContainerCJLump:
      outer: CJLump
      inner: CJLump

      def getCode(self, headCount, tailCount):
          return extract_code(
              [
                  self.outer.front, self.outer.container,
                  self.inner.front, self.inner.container,
                  self.outer.interior, self.inner.interior,
              ],
              [0, 1, 2, 3, 4, 5],
              [1, 4, 3, 5, 2, 0],
              headCount, tailCount,
          )

      def isHeadWithOne(self):
          return len(self.getCodeAsHead()) == 1

      def getCodeAsSingleton(self):
          return self.getCode(3, 1)

      def getCodeAsHead(self):
          return self.getCode(1, 1)

      def getCodeAsBody(self):
          code = self.outer.getCodeAsHead()
          if len(code) == 1:
              code += self.inner.getCodeAsHead()
          elif len(code) == 2:
              code += self.inner.getCodeAsTail()
          return code

      def getCodeAsTail(self):
          return self.getCode(0, 1)

      def getXCode(self, as_body_container=False):
          outer_front, outer_container, _ = self.outer.getXCode()
          if as_body_container:
              return [outer_front, outer_container, self.inner.getCodeAsTail()]
          else:
              return [outer_front, outer_container, self.inner.getCodeAsBody()]
  ```

- [ ] **Step 4：更新 CJCodeInfo.code — 改用模組層級函式**

  找到 `CJCodeInfo.code` property 中對靜態方法的呼叫，替換為：

  ```python
  @property
  def code(self):
      direction = self.getDirection()

      if self.cjLumpListSingleton:
          rtlist = self.cjLumpListSingleton
          return compute_total_code(rtlist)
      else:
          rtlist = self.cjLumpList
          if direction == Direction.SPARROW:
              return compute_singleton_code(rtlist)
          else:
              return compute_total_code(rtlist)
  ```

- [ ] **Step 5：更新 CJCodeInfoEncoder.computeLumpListInDirection — 改用模組層級函式**

  找到方法中對 `CJLump.generateContainer` 和 `CJLump.generateBody` 的呼叫，全部替換：

  ```python
  @staticmethod
  def computeLumpListInDirection(direction, codeInfo):
      tmpDirCode = codeInfo.getDirection()

      if direction == Direction.SPARROW:
          lumpList = codeInfo.getLumpList()
      elif tmpDirCode in [Direction.LOOP]:
          tmpRadixList = codeInfo.getLumpList()
          tmpCJLump = make_container_lump(tmpRadixList)
          lumpList = [tmpCJLump]
      elif tmpDirCode in [Direction.LOONG]:
          tmpRadixList = codeInfo.getLumpList()
          tmpCJLump = make_body_lump(tmpRadixList)
          lumpList = [tmpCJLump]
      elif tmpDirCode in [Direction.GRID] and isinstance(codeInfo, GridCJCodeInfo):
          if direction == Direction.GOOSE:
              newCodeInfo = codeInfo.getCodeInfoH()
              lumpList = newCodeInfo.getLumpList()
          elif direction == Direction.SILKWORM:
              newCodeInfo = codeInfo.getCodeInfoV()
              lumpList = newCodeInfo.getLumpList()
          else:
              ci = codeInfo.getCodeInfoV()
              tmpCJLump = make_body_lump(ci.getLumpList())
              lumpList = [tmpCJLump]
      else:
          if tmpDirCode == direction:
              lumpList = codeInfo.getLumpList()
          else:
              tmpRadixList = codeInfo.getLumpList()
              tmpCJLump = make_body_lump(tmpRadixList)
              lumpList = [tmpCJLump]
      return lumpList
  ```

- [ ] **Step 6：確認靜態方法全部消失**

  ```bash
  grep -n "@staticmethod\|CJLump\.generate\b\|CJLump\.computeTotal\|CJLump\.computeBody\|CJLump\.computeSingleton\|CJLump\.generateBody\|CJLump\.generateSingleton\|CJLump\.generateContainer" \
      codings/CangJie/coding/CangJie/CangJie.py
  ```

  預期：無任何輸出。

- [ ] **Step 7：執行全套 cj 測試**

  ```bash
  uv run pytest -c tests/pytest-cj.ini --rootdir=. -v
  ```

  預期：全部通過。

- [ ] **Step 8：執行 make test**

  ```bash
  make test
  ```

  預期：全部通過。

- [ ] **Step 9：Commit**

  ```bash
  git add codings/CangJie/coding/CangJie/CangJie.py
  git commit -m "refactor(cj): convert CJLump/ContainerCJLump to dataclasses, remove static methods"
  ```

---

## Task 7：Phase 3-C — GridCJCodeInfo 改 dataclass 風格

**Files:**
- Modify: `codings/CangJie/coding/CangJie/CangJie.py`

**Interfaces:**
- `GridCJCodeInfo(CJCodeInfo)` 改用 dataclass 的欄位宣告，移除手動 `__init__`
- 欄位改名：`codeInfoV` → `code_info_v`，`codeInfoH` → `code_info_h`
- 公開方法 `getCodeInfoH()`, `getCodeInfoV()` 保留（向後相容）

- [ ] **Step 1：替換 GridCJCodeInfo 定義**

  找到現有的 `class GridCJCodeInfo(CJCodeInfo):` 完整定義，替換為：

  ```python
  @dataclass
  class GridCJCodeInfo(CJCodeInfo):
      code_info_v: "CJCodeInfo"
      code_info_h: "CJCodeInfo"

      def __post_init__(self):
          CodeInfo.__init__(self)

      @property
      def code(self):
          return self.code_info_v.code

      def getDirection(self):
          return Direction.GRID

      def getLumpList(self):
          return self.code_info_v.getLumpList()

      def getCodeInfoH(self):
          return self.code_info_h

      def getCodeInfoV(self):
          return self.code_info_v
  ```

  **說明**：`GridCJCodeInfo` 繼承 `CJCodeInfo`，但 `CJCodeInfo.__init__` 需要 `direction`, `cjLumpList`, `cjLumpListSingleton`。原有程式碼跳過了 `CJCodeInfo.__init__`（直接呼叫 `CodeInfo.__init__`），所以這裡用 `__post_init__` 維持相同行為。

- [ ] **Step 2：更新 encodeAsYi 呼叫端（GridCJCodeInfo 的建構改變）**

  找到 `encodeAsYi` 中：

  ```python
  codeInfo = GridCJCodeInfo(codeInfoV, codeInfoH)
  ```

  改為（欄位順序依 dataclass 宣告順序）：

  ```python
  codeInfo = GridCJCodeInfo(code_info_v=codeInfoV, code_info_h=codeInfoH)
  ```

- [ ] **Step 3：執行全套 cj 測試**

  ```bash
  uv run pytest -c tests/pytest-cj.ini --rootdir=. -v
  ```

  預期：全部通過。

- [ ] **Step 4：執行 make test**

  ```bash
  make test
  ```

  預期：全部通過。

- [ ] **Step 5：Commit**

  ```bash
  git add codings/CangJie/coding/CangJie/CangJie.py
  git commit -m "refactor(cj): convert GridCJCodeInfo to dataclass"
  ```

---

## 完成核對

全部 7 個 task 完成後：

```bash
# cj 完整測試
uv run pytest -c tests/pytest-cj.ini --rootdir=. -v

# 全套測試
make test

# 確認無殘留舊名稱
grep -n "frontCode\|containerCode\|interiorCode\|outerLump\|innerLump\|isBodyContainer\|isDirtySingleton\|CJCodeHelper\|getHelper" \
    codings/CangJie/coding/CangJie/CangJie.py
```

預期：測試全過，grep 無輸出。
