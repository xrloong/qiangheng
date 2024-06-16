from injector import inject

from element.operator import Operator

from coding.Base import CodeInfo
from coding.Base import CodeInfoEncoder


class CodeInfoInterpreter:
    @inject
    def __init__(self, codeInfoEncoder: CodeInfoEncoder):
        self.__codeInfoEncoder = codeInfoEncoder

    def computeAllCodeInfos(
        self, operator: Operator, codeInfosCollection: list[list[CodeInfo]]
    ) -> tuple[CodeInfo]:
        computedCodeInfoList = (
            self.__computeCodeInfo(operator, codeInfos)
            for codeInfos in codeInfosCollection
        )
        allCodeInfos = tuple(
            filter(lambda codeInfo: codeInfo != None, computedCodeInfoList)
        )
        return allCodeInfos

    def __computeCodeInfo(
        self, operator: Operator, codeInfos: list[CodeInfo]
    ) -> CodeInfo:
        if operator:
            codeInfo = self.__encodeToCodeInfo(operator, codeInfos)
        else:
            codeInfo = codeInfos[0]
        return codeInfo

    def __encodeToCodeInfo(
        self, operator: Operator, codeInfoList: list[CodeInfo]
    ) -> CodeInfo:
        codeInfo = self.__codeInfoEncoder.setByComps(operator, codeInfoList)
        if codeInfo != None:
            for childCodeInfo in codeInfoList:
                codeVariance = childCodeInfo.getCodeVariance()
                codeInfo.multiplyCodeVariance(codeVariance)
        return codeInfo

    def interpretCodeInfoList(self, codeInfoList: list[CodeInfo]) -> list[(str, str)]:
        codeList = []
        for codeInfo in codeInfoList:
            characterCode = codeInfo.code
            variance = codeInfo.variance
            if characterCode:
                codeList.append([characterCode, str(variance)])

        return codeList
