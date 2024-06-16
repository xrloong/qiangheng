from coding.Input import CodeInfo
from coding.Input import CodeInfoEncoder
from coding.Input import CodingRadixParser


class BSCodeInfo(CodeInfo):
    RADIX_A = "a"
    RADIX_B = "b"
    RADIX_C = "c"
    RADIX_D = "d"
    RADIX_E = "e"
    RADIX_F = "f"
    RADIX_G = "g"
    RADIX_H = "h"
    RADIX_I = "i"
    RADIX_J = "j"
    RADIX_K = "k"
    RADIX_L = "l"
    RADIX_M = "m"
    RADIX_N = "n"
    RADIX_O = "o"
    RADIX_P = "p"
    RADIX_Q = "q"
    RADIX_R = "r"
    RADIX_S = "s"
    RADIX_T = "t"
    RADIX_U = "u"
    RADIX_V = "v"
    RADIX_W = "w"
    RADIX_X = "x"
    RADIX_Y = "y"
    RADIX_Z = "z"

    COMPLEMENTARY_A = "a"
    COMPLEMENTARY_E = "e"
    COMPLEMENTARY_I = "i"
    COMPLEMENTARY_J = "j"
    COMPLEMENTARY_K = "k"
    COMPLEMENTARY_L = "l"
    COMPLEMENTARY_N = "n"
    COMPLEMENTARY_O = "o"
    COMPLEMENTARY_P = "p"
    COMPLEMENTARY_X = "x"
    COMPLEMENTARY_Y = "y"

    radixToCodeDict = {
        RADIX_A: "a",
        RADIX_B: "b",
        RADIX_C: "c",
        RADIX_D: "d",
        RADIX_E: "e",
        RADIX_F: "f",
        RADIX_G: "g",
        RADIX_H: "h",
        RADIX_I: "i",
        RADIX_J: "j",
        RADIX_K: "k",
        RADIX_L: "l",
        RADIX_M: "m",
        RADIX_N: "n",
        RADIX_O: "o",
        RADIX_P: "p",
        RADIX_Q: "q",
        RADIX_R: "r",
        RADIX_S: "s",
        RADIX_T: "t",
        RADIX_U: "u",
        RADIX_V: "v",
        RADIX_W: "w",
        RADIX_X: "x",
        RADIX_Y: "y",
        RADIX_Z: "z",
    }

    def __init__(self, codeSequence, supplementCode, ignoreSupplementCode):
        super().__init__()

        self.__codeSequence = codeSequence
        self.__bs_spcode = supplementCode
        self.__ignore_supplement_code = ignoreSupplementCode

    @staticmethod
    def generateDefaultCodeInfo(codeList, supplementCode):
        codeInfo = BSCodeInfo(codeList, supplementCode, False)
        return codeInfo

    @property
    def code(self):
        codeSequence = self.codeSequence

        if codeSequence is None:
            return None
        else:
            code = "".join(map(lambda x: BSCodeInfo.radixToCodeDict[x], codeSequence))
            if len(code) < 3:
                if self.ignoreSupplement:
                    # 根據嘸蝦米規則，如果是一到十等數目的字，則不用加補碼
                    return code
                else:
                    supplementCode = self.supplementCode
                    if supplementCode is None:
                        return None
                    return code + supplementCode
            elif len(code) > 4:
                return code[:3] + code[-1:]
            else:
                return code

    @property
    def codeSequence(self):
        return self.__codeSequence

    @property
    def supplementCode(self):
        return self.__bs_spcode

    @property
    def ignoreSupplement(self):
        return self.__ignore_supplement_code


class BSCodeInfoEncoder(CodeInfoEncoder):
    RADIX_SEPERATOR = ","

    def generateDefaultCodeInfo(self, codeList, supplementCode):
        return BSCodeInfo.generateDefaultCodeInfo(codeList, supplementCode)

    def isAvailableOperation(self, codeInfoList):
        isAllWithCode = all(map(lambda x: x.codeSequence, codeInfoList))
        return isAllWithCode

    def encodeAsLoong(self, codeInfoList):
        """運算 "龍" """

        bslist = list(map(lambda c: c.codeSequence, codeInfoList))
        bs_code_list = BSCodeInfoEncoder.computeBoshiamyCode(bslist)
        bs_spcode = codeInfoList[-1].supplementCode

        codeInfo = self.generateDefaultCodeInfo(bs_code_list, bs_spcode)
        return codeInfo

    def encodeAsHan(self, codeInfoList):
        """運算 "函" """
        firstCodeInfo = codeInfoList[0]
        secondCodeInfo = codeInfoList[1]

        newCodeInfoList = [secondCodeInfo, firstCodeInfo]
        codeInfo = self.encodeAsLoong(newCodeInfoList)
        return codeInfo

    def encodeAsZhe(self, codeInfoList):
        """運算 "這" """
        firstCodeInfo = codeInfoList[0]
        secondCodeInfo = codeInfoList[1]

        codeInfo = self.encodeAsLoong([secondCodeInfo, firstCodeInfo])
        return codeInfo

    def encodeAsYou(self, codeInfoList):
        """運算 "幽" """

        firstCodeInfo = codeInfoList[0]
        secondCodeInfo = codeInfoList[1]
        thirdCodeInfo = codeInfoList[2]

        newCodeInfoList = [secondCodeInfo, thirdCodeInfo, firstCodeInfo]
        codeInfo = self.encodeAsLoong(newCodeInfoList)
        return codeInfo

    @staticmethod
    def computeBoshiamyCode(bsCodeList):
        bslist = list(sum(bsCodeList, []))
        bs_code_list = (bslist[:3] + bslist[-1:]) if len(bslist) > 4 else bslist
        return bs_code_list


class BSRadixParser(CodingRadixParser):
    RADIX_SEPERATOR = ","

    ATTRIB_CODE_EXPRESSION = "編碼表示式"
    ATTRIB_SUPPLEMENTARY_CODE = "補碼"
    ATTRIB_IGNORE_SUPPLEMENTARY_CODE = "忽略補碼"

    # 多型
    def convertRadixDescToCodeInfo(self, radixDesc):
        codeInfo = self.convertRadixDescToCodeInfoByExpression(radixDesc)
        return codeInfo

    def convertRadixDescToCodeInfoByExpression(self, radixInfo):
        elementCodeInfo = radixInfo.codeElement

        infoDict = elementCodeInfo

        strCodeList = infoDict.get(BSRadixParser.ATTRIB_CODE_EXPRESSION)
        supplementCode = infoDict.get(BSRadixParser.ATTRIB_SUPPLEMENTARY_CODE)
        ignoreSupplementCode = (
            True
            if infoDict.get(BSRadixParser.ATTRIB_IGNORE_SUPPLEMENTARY_CODE) is not None
            else False
        )

        codeList = None
        if strCodeList is not None:
            codeList = strCodeList.split(BSRadixParser.RADIX_SEPERATOR)

        codeInfo = BSCodeInfo(codeList, supplementCode, ignoreSupplementCode)
        return codeInfo
