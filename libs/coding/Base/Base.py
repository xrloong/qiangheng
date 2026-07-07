import abc

from element.operator import Operator

from element.enum import CodeVariance

from .interface import IfCodeInfo, IfCodeInfoEncoder, IfCodingRadixParser


def truncateCode(seq, max_len=4, head_len=3):
    """Truncate code sequence: keep first head_len and last (max_len - head_len) elements."""
    if len(seq) > max_len:
        tail_len = max_len - head_len
        return seq[:head_len] + seq[-tail_len:]
    return seq


class CodeInfo(IfCodeInfo):
    def __init__(self):
        self.codeVariance = CodeVariance.STANDARD
        self._isSupportRadixCode = True

    @staticmethod
    def generateDefaultCodeInfo():
        codeInfo = CodeInfo()
        return codeInfo

    @property
    def code(self):
        return ""

    def setCodeInfoAttribute(self, codeVariance, isSupportRadixCode):
        self.multiplyCodeVariance(codeVariance)
        self._isSupportRadixCode = isSupportRadixCode

    def __str__(self):
        return "{{{0}}}".format(self.code)

    def __repr__(self):
        return str(self)

    def isSupportRadixCode(self):
        return self._isSupportRadixCode

    def getCodeVariance(self):
        return self.codeVariance

    def multiplyCodeVariance(self, codeVariance):
        self.codeVariance = self.codeVariance * codeVariance

    @property
    def variance(self):
        return self.codeVariance


class CodeInfoEncoder(IfCodeInfoEncoder):
    def generateDefaultCodeInfo(self):
        return CodeInfo.generateDefaultCodeInfo()

    def setByComps(self, operator, codeInfoList):
        codeInfo = None

        isAvailable = self.isAvailableOperation(codeInfoList)
        if isAvailable:
            match operator:
                case Operator.Turtle:
                    codeInfo = self.encodeAsTurtle(codeInfoList)
                case Operator.Loong:
                    codeInfo = self.encodeAsLoong(codeInfoList)
                case Operator.Sparrow:
                    codeInfo = self.encodeAsSparrow(codeInfoList)
                case Operator.Equal:
                    codeInfo = self.encodeAsEqual(codeInfoList)

                case Operator.Silkworm:
                    codeInfo = self.encodeAsSilkworm(codeInfoList)
                case Operator.Goose:
                    codeInfo = self.encodeAsGoose(codeInfoList)
                case Operator.Loop:
                    codeInfo = self.encodeAsLoop(codeInfoList)

                case Operator.Qi:
                    codeInfo = self.encodeAsQi(codeInfoList)
                case Operator.Zhe:
                    codeInfo = self.encodeAsZhe(codeInfoList)
                case Operator.Liao:
                    codeInfo = self.encodeAsLiao(codeInfoList)
                case Operator.Zai:
                    codeInfo = self.encodeAsZai(codeInfoList)
                case Operator.Dou:
                    codeInfo = self.encodeAsDou(codeInfoList)

                case Operator.Tong:
                    codeInfo = self.encodeAsTong(codeInfoList)
                case Operator.Qu:
                    codeInfo = self.encodeAsQu(codeInfoList)
                case Operator.Han:
                    codeInfo = self.encodeAsHan(codeInfoList)
                case Operator.Left:
                    codeInfo = self.encodeAsLeft(codeInfoList)

                case Operator.Mu:
                    codeInfo = self.encodeAsMu(codeInfoList)
                case Operator.Zuo:
                    codeInfo = self.encodeAsZuo(codeInfoList)
                case Operator.You:
                    codeInfo = self.encodeAsYou(codeInfoList)
                case Operator.Liang:
                    codeInfo = self.encodeAsLiang(codeInfoList)
                case Operator.Jia:
                    codeInfo = self.encodeAsJia(codeInfoList)

                case Operator.Luan:
                    codeInfo = self.encodeAsLuan(codeInfoList)
                case Operator.Ban:
                    codeInfo = self.encodeAsBan(codeInfoList)
                case Operator.Lin:
                    codeInfo = self.encodeAsLin(codeInfoList)
                case Operator.Li:
                    codeInfo = self.encodeAsLi(codeInfoList)
                case Operator.Yi:
                    codeInfo = self.encodeAsYi(codeInfoList)

                case _:
                    codeInfo = self.encodeAsInvalidate(codeInfoList)
        return codeInfo

    def isAvailableOperation(self, codeInfoList):
        return True

    def encodeAsInvalidate(self, codeInfoList):
        """不合法的運算"""
        raise NotImplementedError(
            f"{type(self).__name__} does not support this encoding operation"
        )

    # ── 第一層：原始空間操作 ────────────────────────────────────────────────
    #
    # 代表字元結構中不同的空間關係。插件應 override 此層的方法。
    #
    # 必須 override：
    #   encodeAsLoong — 所有序列型操作的基礎，幾乎所有輸入法都需要實作。
    #
    # 可選 override（若你的輸入法區分這些空間關係）：
    #   encodeAsSilkworm — 上下排列（蚕），預設 → encodeAsLoong
    #   encodeAsGoose    — 左右排列（鴻），預設 → encodeAsLoong
    #   encodeAsLoop     — 外框包圍（回），預設 → encodeAsLoong
    #   encodeAsQi       — 右上缺角（起），預設 → encodeAsLoong
    #   encodeAsLiao     — 右下缺角（廖），預設 → encodeAsLoong
    #   encodeAsZai      — 左下缺角（載），預設 → encodeAsLoong
    #   encodeAsDou      — 左上缺角（斗），預設 → encodeAsLoong
    #   encodeAsMu       — 田字格（畞），預設 → encodeAsLoong
    #   encodeAsZuo      — 㘴型（參數順序特殊），預設 → encodeAsLoong
    #   encodeAsYou      — 幽型（三部件），預設 → encodeAsLoong
    #   encodeAsLiang    — 㒳型，預設 → encodeAsLoong
    #   encodeAsJia      — 夾型，預設 → encodeAsLoong
    #   encodeAsEqual    — 單部件直接沿用，預設 → encodeAsLoong
    #   encodeAsSparrow  — 獨體字特殊處理（雀），預設 → encodeAsInvalidate
    #   encodeAsTurtle   — 龜型，預設 → encodeAsInvalidate

    def encodeAsLoong(self, codeInfoList):
        """運算 "龍"：一般序列組合，插件必須 override。"""
        return self.encodeAsInvalidate(codeInfoList)

    def encodeAsSilkworm(self, codeInfoList):
        """運算 "蚕"：上下排列。預設同 encodeAsLoong。"""
        return self.encodeAsLoong(codeInfoList)

    def encodeAsGoose(self, codeInfoList):
        """運算 "鴻"：左右排列。預設同 encodeAsLoong。"""
        return self.encodeAsLoong(codeInfoList)

    def encodeAsLoop(self, codeInfoList):
        """運算 "回"：外框包圍。預設同 encodeAsLoong。"""
        return self.encodeAsLoong(codeInfoList)

    def encodeAsQi(self, codeInfoList):
        """運算 "起"：右上缺角。預設同 encodeAsLoong。"""
        return self.encodeAsLoong(codeInfoList)

    def encodeAsLiao(self, codeInfoList):
        """運算 "廖"：右下缺角。預設同 encodeAsLoong。"""
        return self.encodeAsLoong(codeInfoList)

    def encodeAsZai(self, codeInfoList):
        """運算 "載"：左下缺角。預設同 encodeAsLoong。"""
        return self.encodeAsLoong(codeInfoList)

    def encodeAsDou(self, codeInfoList):
        """運算 "斗"：左上缺角。預設同 encodeAsLoong。"""
        return self.encodeAsLoong(codeInfoList)

    def encodeAsMu(self, codeInfoList):
        """運算 "畞"：田字格型。預設同 encodeAsLoong。"""
        return self.encodeAsLoong(codeInfoList)

    def convertCodeInfoListOfZuoOrder(self, codeInfoList):
        # 㘴的參數順序為：土、口、人（大部分到小部件）。
        # 但大部分的輸入法順序為：口、人、土。
        return codeInfoList[1:] + codeInfoList[:1]

    def encodeAsZuo(self, codeInfoList):
        """運算 "㘴"：參數順序為土、口、人，轉換後同 encodeAsLoong。"""
        return self.encodeAsLoong(self.convertCodeInfoListOfZuoOrder(codeInfoList))

    def encodeAsYou(self, codeInfoList):
        """運算 "幽"：三部件型。預設同 encodeAsLoong。"""
        return self.encodeAsLoong(codeInfoList)

    def encodeAsLiang(self, codeInfoList):
        """運算 "㒳"：預設同 encodeAsLoong。"""
        return self.encodeAsLoong(codeInfoList)

    def encodeAsJia(self, codeInfoList):
        """運算 "夾"：預設同 encodeAsLoong。"""
        return self.encodeAsLoong(codeInfoList)

    def encodeAsEqual(self, codeInfoList):
        """運算 "爲"：單部件直接沿用，預設同 encodeAsLoong。"""
        assert len(codeInfoList) == 1
        return self.encodeAsLoong(codeInfoList)

    def encodeAsSparrow(self, codeInfoList):
        """運算 "雀"：獨體字特殊處理。預設不支援。"""
        return self.encodeAsInvalidate(codeInfoList)

    def encodeAsTurtle(self, codeInfoList):
        """運算 "龜"。預設不支援。"""
        return self.encodeAsInvalidate(codeInfoList)

    # ── 第二層：語意別名 ────────────────────────────────────────────────────
    #
    # 這些運算子在語意上與某個第一層操作對應，預設直接委派。
    # 若你的輸入法對這類結構有特殊的參數選取或順序邏輯，可以 override。
    #
    #   encodeAsZhe  → encodeAsQi   （這 ≈ 起，右上缺角變體）
    #   encodeAsHan  → encodeAsLoop （函，部分輸入法對調內外順序）
    #   encodeAsTong → encodeAsLoop （同 ≈ 回）
    #   encodeAsQu   → encodeAsLoop （區 ≈ 回）
    #   encodeAsLeft → encodeAsLoop （左 ≈ 回）

    def encodeAsZhe(self, codeInfoList):
        """運算 "這"：右上缺角變體，預設同 encodeAsQi。"""
        return self.encodeAsQi(codeInfoList)

    def encodeAsHan(self, codeInfoList):
        """運算 "函"：包圍型，預設同 encodeAsLoop。"""
        return self.encodeAsLoop(codeInfoList)

    def encodeAsTong(self, codeInfoList):
        """運算 "同"：包圍型，預設同 encodeAsLoop。"""
        return self.encodeAsLoop(codeInfoList)

    def encodeAsQu(self, codeInfoList):
        """運算 "區"：包圍型，預設同 encodeAsLoop。"""
        return self.encodeAsLoop(codeInfoList)

    def encodeAsLeft(self, codeInfoList):
        """運算 "左"：包圍型，預設同 encodeAsLoop。"""
        return self.encodeAsLoop(codeInfoList)

    # ── 第三層：複合運算子 ──────────────────────────────────────────────────
    #
    # 由第一層原始操作組合而成，插件不需要也不應該 override。
    # 若你 override 了 encodeAsGoose 或 encodeAsSilkworm，
    # 這些複合運算子會自動採用你的實作。

    def encodeAsLuan(self, codeInfoList):
        """運算 "䜌"：encodeAsGoose(B, A, B)"""
        a, b = codeInfoList[0], codeInfoList[1]
        return self.encodeAsGoose([b, a, b])

    def encodeAsBan(self, codeInfoList):
        """運算 "辦"：encodeAsGoose(A, B, A)"""
        a, b = codeInfoList[0], codeInfoList[1]
        return self.encodeAsGoose([a, b, a])

    def encodeAsLin(self, codeInfoList):
        """運算 "粦"：encodeAsSilkworm(A, encodeAsGoose(B, C))"""
        a, b, c = codeInfoList[0], codeInfoList[1], codeInfoList[2]
        return self.encodeAsSilkworm([a, self.encodeAsGoose([b, c])])

    def encodeAsLi(self, codeInfoList):
        """運算 "瓥"：encodeAsSilkworm(encodeAsGoose(A,B), encodeAsGoose(C,D))"""
        a, b = codeInfoList[0], codeInfoList[1]
        c, d = codeInfoList[2], codeInfoList[3]
        return self.encodeAsSilkworm([
            self.encodeAsGoose([a, b]),
            self.encodeAsGoose([c, d]),
        ])

    def encodeAsYi(self, codeInfoList):
        """運算 "燚"：encodeAsLi(A, A, A, A)"""
        a = codeInfoList[0]
        return self.encodeAsLi([a, a, a, a])


class CodingRadixParser(IfCodingRadixParser):
    pass


class CodeMappingInfoInterpreter(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def getCodingTypeName(self):
        pass

    def interpretCodeMappingInfo(self, codeMappingInfo):
        return {
            "字符": codeMappingInfo.getName(),
            "類型": codeMappingInfo.getVariance(),
            "按鍵序列": codeMappingInfo.getCode(),
        }
