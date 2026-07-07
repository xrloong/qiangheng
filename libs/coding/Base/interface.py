import abc


class IfCodeInfo(object, metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def code(self):
        """回傳此字元的編碼，型別依輸入法而異（字串或圖形物件）。"""


class IfCodeInfoEncoder(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def setByComps(self, operator, codeInfoList):
        """依組字運算子與子部件的 CodeInfo 列表，計算出組合後的 CodeInfo。"""


class IfCodingRadixParser(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def convertRadixDescToCodeInfo(self, radixDesc):
        """將字根描述轉換為對應的 CodeInfo。"""
