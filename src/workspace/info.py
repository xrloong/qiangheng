import abc


class StructureInfo(object, metaclass=abc.ABCMeta):
    def __init__(self):
        self.__codeInfos = None

    def setComputedCodeInfos(self, codeInfos):
        self.__codeInfos = codeInfos

    def getComputedCodeInfos(self):
        return self.__codeInfos

    def isCodeInfoGenerated(self):
        return self.__codeInfos is not None

    def getRadixCodeInfoList(self):
        return filter(lambda x: x.isSupportRadixCode(), self.__codeInfos)

    def getOperator(self):
        return None

    def getOperatorName(self):
        operator = self.getOperator()
        if operator:
            return operator.getName()
        else:
            return ""

    def getExpandedOperator(self):
        return self.getOperator()

    def getExpandedOperatorName(self):
        operator = self.getExpandedOperator()
        if operator:
            return operator.name
        else:
            return ""

    def getExpandedStructureList(self):
        return self.getStructureList()

    @abc.abstractproperty
    def childStructures(self):
        pass

    @property
    def referenceExpression(self):
        return None

    @property
    def referencedNodeStructure(self):
        return None

    @property
    def referencedNodeStructureInfo(self):
        return self.referencedNodeStructure.structureInfo

    def getStructureList(self):
        return []

    @abc.abstractproperty
    def codeInfos(self):
        pass


class UnitStructureInfo(StructureInfo):
    def __init__(self, radixCodeInfo):
        super().__init__()

        self.__radixCodeInfo = radixCodeInfo

        self.__referenceNode = None
        self.__index = 0

    @property
    def childStructures(self):
        return ()

    @property
    def codeInfos(self):
        return ((self.__radixCodeInfo,),)


class WrapperStructureInfo(StructureInfo):
    def __init__(self, nodeStructure, index):
        super().__init__()

        nodeStructureInfo = nodeStructure.structureInfo
        referenceName = nodeStructureInfo.getName()
        if index == 0:
            referenceExpression = "{}".format(referenceName)
        else:
            referenceExpression = "{}.{}".format(referenceName, index)

        self.__nodeStructure = nodeStructure
        self.__index = index
        self.__referenceExpression = referenceExpression

    def getOperatorName(self):
        nodeStructureInfo = self.referencedNodeStructureInfo
        return nodeStructureInfo.getOperatorName()

    def getExpandedOperator(self):
        nodeStructureInfo = self.referencedNodeStructureInfo
        expandedStructure = nodeStructureInfo.mainStructure
        if expandedStructure:
            return expandedStructure.structureInfo.getOperator()
        else:
            return self.getOperator()

    def getExpandedStructureList(self):
        nodeStructureInfo = self.referencedNodeStructureInfo
        expandedStructure = nodeStructureInfo.mainStructure
        if expandedStructure:
            return expandedStructure.getStructureList()
        else:
            return self.getStructureList()

    @property
    def childStructures(self):
        nodeStructure = self.referencedNodeStructure
        return (nodeStructure,)

    @property
    def codeInfos(self):
        nodeStructureInfo = self.__nodeStructure.structureInfo
        index = self.__index

        structureList = nodeStructureInfo.getSubStructureList(index)
        codeInfosList = sum((s.getComputedCodeInfos() for s in structureList), ())
        return tuple((codeInfos,) for codeInfos in codeInfosList)

    @property
    def referenceExpression(self):
        return self.__referenceExpression

    @property
    def referencedNodeStructure(self):
        return self.__nodeStructure


class CompoundStructureInfo(StructureInfo):
    def __init__(self, operator, structureList):
        super().__init__()

        self.__operator = operator
        self.__structureList = structureList

    @property
    def childStructures(self):
        return self.getStructureList()

    @property
    def codeInfos(self):
        codeInfosList = [
            s.structureInfo.getRadixCodeInfoList() for s in self.getStructureList()
        ]
        return CompoundStructureInfo.getAllCodeInfoListFromCodeInfoCollection(
            codeInfosList
        )

    def getOperator(self):
        return self.__operator

    def getStructureList(self):
        return self.__structureList

    @staticmethod
    def getAllCodeInfoListFromCodeInfoCollection(codeInfoListCollection):
        def combineList(infoListList, infoListOfNode):
            prevInfoListList = infoListList if len(infoListList) > 0 else ([],)
            ansListList = [
                infoList + [codeInfo]
                for infoList in prevInfoListList
                for codeInfo in infoListOfNode
            ]
            return ansListList

        combineInfoListList = []
        for codeInfoList in codeInfoListCollection:
            combineInfoListList = combineList(combineInfoListList, codeInfoList)

        return combineInfoListList


class NodeStructureInfo(StructureInfo):
    def __init__(self, name):
        super().__init__()

        self.__name = name

        self.__unitStructureList = []
        self.__mainStructure = None

    def getOperator(self):
        mainStructure = self.mainStructure
        if mainStructure:
            structureInfo = mainStructure.structureInfo
            return structureInfo.getOperator()
        else:
            return None

    @property
    def mainStructure(self):
        return self.__mainStructure

    @property
    def childStructures(self):
        return self.getStructureList(isWithUnit=True)

    @property
    def codeInfos(self):
        return ()

    def getName(self):
        return self.__name

    def addUnitStructure(self, structure):
        self.__unitStructureList.append(structure)

    def setMainStructure(self, structure):
        self.__mainStructure = structure

    def getStructureList(self, isWithUnit=False):
        structureList = []

        if self.__mainStructure:
            structureList = [self.__mainStructure]

        if isWithUnit:
            structureList.extend(self.__unitStructureList)

        return structureList

    def getSubStructure(self, index):
        structure = self.__mainStructure
        if not structure:
            return None

        structureList = structure.getStructureList()
        return structureList[index]

    def getSubStructureList(self, subIndex=0):
        if subIndex > 0:
            structure = self.getSubStructure(subIndex - 1)
            structureList = [structure]
        else:
            structureList = self.getStructureList(isWithUnit=True)
        return structureList
