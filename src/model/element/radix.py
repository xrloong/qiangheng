from parser.model import RadixCodeInfoModel
from parser.model import RadicalModel
from parser.model import RadicalSetModel


class RadixCodeInfoDescription:
    def __init__(self, model: RadixCodeInfoModel):
        self.__codeVariance = model.variance
        self.__isSupportRadixCode = model.isSupportRadixCode
        self.__codeElementCodeInfo = model.dict()

    @property
    def codeVariance(self):
        return self.__codeVariance

    @property
    def isSupportRadixCode(self):
        return self.__isSupportRadixCode

    @property
    def codeElement(self):
        return self.__codeElementCodeInfo


class RadixDescription:
    def __init__(self, model: RadicalModel):
        self.radixName = model.name
        self.radixCodeInfoList = tuple(
            RadixCodeInfoDescription(model=modelCoding) for modelCoding in model.codings
        )

    def getRadixName(self):
        return self.radixName

    def getRadixCodeInfoDescriptionList(self):
        return self.radixCodeInfoList

    def getRadixCodeInfoDescription(self, index):
        if index in range(leng(self.radixCodeInfoList)):
            return self.radixCodeInfoList[index]


class RadicalSet:
    def __init__(self, model: RadicalSetModel):
        self.radicals = tuple(
            RadixDescription(model=modelRadical) for modelRadical in model.radicals
        )
