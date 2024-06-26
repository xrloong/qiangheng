from coding.Input import CodeInfo
from coding.Input import CodeInfoEncoder
from coding.Input import CodingRadixParser


class ARCodeInfo(CodeInfo):
    RADIX_1_UP = "1^"
    RADIX_2_UP = "2^"
    RADIX_3_UP = "3^"
    RADIX_4_UP = "4^"
    RADIX_5_UP = "5^"
    RADIX_6_UP = "6^"
    RADIX_7_UP = "7^"
    RADIX_8_UP = "8^"
    RADIX_9_UP = "9^"
    RADIX_0_UP = "0^"

    RADIX_1_CENTER = "1-"
    RADIX_2_CENTER = "2-"
    RADIX_3_CENTER = "3-"
    RADIX_4_CENTER = "4-"
    RADIX_5_CENTER = "5-"
    RADIX_6_CENTER = "6-"
    RADIX_7_CENTER = "7-"
    RADIX_8_CENTER = "8-"
    RADIX_9_CENTER = "9-"
    RADIX_0_CENTER = "0-"

    RADIX_1_BOTTOM = "1v"
    RADIX_2_BOTTOM = "2v"
    RADIX_3_BOTTOM = "3v"
    RADIX_4_BOTTOM = "4v"
    RADIX_5_BOTTOM = "5v"
    RADIX_6_BOTTOM = "6v"
    RADIX_7_BOTTOM = "7v"
    RADIX_8_BOTTOM = "8v"
    RADIX_9_BOTTOM = "9v"
    RADIX_0_BOTTOM = "0v"

    radixToCodeDict = {
        RADIX_1_UP: "q",
        RADIX_2_UP: "w",
        RADIX_3_UP: "e",
        RADIX_4_UP: "r",
        RADIX_5_UP: "t",
        RADIX_6_UP: "y",
        RADIX_7_UP: "u",
        RADIX_8_UP: "i",
        RADIX_9_UP: "o",
        RADIX_0_UP: "p",
        RADIX_1_CENTER: "a",
        RADIX_2_CENTER: "s",
        RADIX_3_CENTER: "d",
        RADIX_4_CENTER: "f",
        RADIX_5_CENTER: "g",
        RADIX_6_CENTER: "h",
        RADIX_7_CENTER: "j",
        RADIX_8_CENTER: "k",
        RADIX_9_CENTER: "l",
        RADIX_0_CENTER: ";",
        RADIX_1_BOTTOM: "z",
        RADIX_2_BOTTOM: "x",
        RADIX_3_BOTTOM: "c",
        RADIX_4_BOTTOM: "v",
        RADIX_5_BOTTOM: "b",
        RADIX_6_BOTTOM: "n",
        RADIX_7_BOTTOM: "m",
        RADIX_8_BOTTOM: ",",
        RADIX_9_BOTTOM: ".",
        RADIX_0_BOTTOM: "/",
    }

    def __init__(self, codes=()):
        super().__init__()

        self.codes = codes

    @staticmethod
    def generateDefaultCodeInfo(codeList):
        codeInfo = ARCodeInfo(codeList)
        return codeInfo

    @property
    def code(self):
        mainRadixList = self.getMainCodeList()
        mainCodeList = tuple(
            map(lambda x: ARCodeInfo.radixToCodeDict[x], mainRadixList)
        )
        code = "".join(mainCodeList)
        return code[:3] + code[-1] if len(code) > 4 else code

    def getMainCodeList(self):
        return self.codes


class ARCodeInfoEncoder(CodeInfoEncoder):
    def generateDefaultCodeInfo(self, codeList):
        return ARCodeInfo.generateDefaultCodeInfo(codeList)

    def isAvailableOperation(self, codeInfoList):
        isAllWithCode = all(map(lambda x: x.getMainCodeList(), codeInfoList))
        return isAllWithCode

    def encodeAsLoong(self, codeInfoList):
        """運算 "龍" """

        arCodeList = list(map(lambda c: c.getMainCodeList(), codeInfoList))
        tmpArCodeList = arCodeList
        arCode = ARCodeInfoEncoder.computeArrayCodeByCodeList(tmpArCodeList)
        codeInfo = self.generateDefaultCodeInfo(arCode)

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

    def encodeAsLuan(self, codeInfoList):
        """運算 "䜌" """
        firstCodeInfo = codeInfoList[0]
        secondCodeInfo = codeInfoList[1]
        codeInfo = self.encodeAsLoong([firstCodeInfo, secondCodeInfo, secondCodeInfo])
        return codeInfo

    def getCodeInfoExceptLast(self, codeInfo):
        mainCodeList = codeInfo.getMainCodeList()

        if len(mainCodeList) > 1:
            tmpCodeInfo = self.generateDefaultCodeInfo([mainCodeList[:-1]])
        else:
            tmpCodeInfo = None

        return tmpCodeInfo

    def getCodeInfoExceptFirst(self, codeInfo):
        mainCodeList = codeInfo.getMainCodeList()

        if len(mainCodeList) > 1:
            tmpCodeInfo = self.generateDefaultCodeInfo([mainCodeList[1:]])
        else:
            tmpCodeInfo = None

        return tmpCodeInfo

    def convertMergedCode(
        self, firstCodeInfo, secondCodeInfo, firstRadix, secondRadix, targetRadix
    ):
        firstMainCodeList = firstCodeInfo.getMainCodeList()
        secondMainCodeList = secondCodeInfo.getMainCodeList()

        if firstMainCodeList[-1] == firstRadix and secondMainCodeList[0] == secondRadix:
            newFirstCodeInfo = self.getCodeInfoExceptLast(firstCodeInfo)
            targetCodeInfo = self.generateDefaultCodeInfo([[targetRadix]])
            newSecondCodeInfo = self.getCodeInfoExceptFirst(secondCodeInfo)
        else:
            newFirstCodeInfo = firstCodeInfo
            targetCodeInfo = None
            newSecondCodeInfo = secondCodeInfo
        return [newFirstCodeInfo, targetCodeInfo, newSecondCodeInfo]

    def getMergedCodeInfoList(self, codeInfoList, mergeCodeInfoList):
        firstCodeInfo = None
        secondCodeInfo = None

        newCodeInfoList = []
        for xCodeInfo in codeInfoList:
            firstCodeInfo = secondCodeInfo
            secondCodeInfo = xCodeInfo

            if firstCodeInfo is None:
                continue

            for [firstRadix, secondRadix, targetRadix] in mergeCodeInfoList:
                [
                    newFirstCodeInfo,
                    targetCodeInfo,
                    newSecondCodeInfo,
                ] = self.convertMergedCode(
                    firstCodeInfo, secondCodeInfo, firstRadix, secondRadix, targetRadix
                )
                if targetCodeInfo:
                    if newFirstCodeInfo:
                        newCodeInfoList.append(newFirstCodeInfo)
                    newCodeInfoList.append(targetCodeInfo)
                    secondCodeInfo = newSecondCodeInfo
                    break
            else:
                newCodeInfoList.append(firstCodeInfo)

        if secondCodeInfo is not None:
            newCodeInfoList.append(secondCodeInfo)

        return newCodeInfoList

    @staticmethod
    def computeArrayCodeByCodeList(arCodeList):
        cat = sum(arCodeList, [])
        arCode = cat[:3] + cat[-1:] if len(cat) > 4 else cat
        return arCode


class ARRadixParser(CodingRadixParser):
    RADIX_SEPERATOR = ","

    ATTRIB_CODE_EXPRESSION = "編碼表示式"

    # 多型
    def convertRadixDescToCodeInfo(self, radixDesc):
        codeInfo = self.convertRadixDescToCodeInfoByExpression(radixDesc)
        return codeInfo

    def convertRadixDescToCodeInfoByExpression(self, radixInfo):
        elementCodeInfo = radixInfo.codeElement

        infoDict = elementCodeInfo

        codeList = None

        str_rtlist = infoDict.get(ARRadixParser.ATTRIB_CODE_EXPRESSION)
        if str_rtlist is not None:
            codeList = str_rtlist.split(ARRadixParser.RADIX_SEPERATOR)

        codeInfo = ARCodeInfo(codeList)
        return codeInfo
