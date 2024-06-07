import abc

from injector import inject

class StructureInfo(object, metaclass = abc.ABCMeta):
	def __init__(self):
		self.__codeInfos = None

	def setComputedCodeInfos(self, codeInfos):
		self.__codeInfos = codeInfos

	def getComputedCodeInfos(self):
		return self.__codeInfos

	def isCodeInfoGenerated(self):
		return self.__codeInfos !=  None

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

	def getChildStructures(self):
		return ()

	def getReferenceExpression(self):
		return None

	def getReferencedNodeStructure(self):
		return None

	def getReferencedNodeStructureInfo(self):
		return None

	def getStructureList(self):
		return []

	@abc.abstractproperty
	def codeInfos(self): pass

class UnitStructureInfo(StructureInfo):
	def __init__(self, radixCodeInfo):
		super().__init__()

		self.__radixCodeInfo = radixCodeInfo

		self.__referenceNode = None
		self.__index = 0

	def getChildStructures(self):
		return ()

	@property
	def codeInfos(self):
		return ((self.__radixCodeInfo, ), )

class WrapperStructureInfo(StructureInfo):
	def __init__(self, nodeStructure, index):
		super().__init__()

		nodeStructureInfo = nodeStructure.structureInfo
		referenceName = nodeStructureInfo.getName()
		if index == 0:
			referenceExpression = "{}".format(referenceName)
		else:
			referenceExpression = "{}.{}".format(referenceName,index)

		self.__nodeStructure = nodeStructure
		self.__nodeStructureInfo = nodeStructureInfo
		self.__index = index
		self.__referenceExpression = referenceExpression

	def getOperatorName(self):
		nodeStructureInfo = self.getReferencedNodeStructureInfo()
		return nodeStructureInfo.getOperatorName()

	def getExpandedOperator(self):
		nodeStructureInfo = self.getReferencedNodeStructureInfo()
		expandedStructure = nodeStructureInfo.getMainStructure()
		if expandedStructure:
			return expandedStructure.structureInfo.getOperator()
		else:
			return self.getOperator()

	def getExpandedStructureList(self):
		nodeStructureInfo = self.getReferencedNodeStructureInfo()
		expandedStructure = nodeStructureInfo.getMainStructure()
		if expandedStructure:
			return expandedStructure.getStructureList()
		else:
			return self.getStructureList()

	def getChildStructures(self):
		nodeStructure = self.getReferencedNodeStructure()
		return (nodeStructure, )

	@property
	def codeInfos(self):
		nodeStructureInfo = self.__nodeStructureInfo
		index = self.__index

		structureList = nodeStructureInfo.getSubStructureList(index)
		codeInfosList = sum((s.getComputedCodeInfos() for s in structureList), ())
		return tuple((codeInfos, ) for codeInfos in codeInfosList)

	def getReferenceExpression(self):
		return self.__referenceExpression

	def getReferencedNodeStructure(self):
		return self.__nodeStructure

	def getReferencedNodeStructureInfo(self):
		return self.__nodeStructureInfo


class CompoundStructureInfo(StructureInfo):
	def __init__(self, operator, structureList):
		super().__init__()

		self.__operator = operator
		self.__structureList = structureList

	def getChildStructures(self):
		return self.getStructureList()

	@property
	def codeInfos(self):
		codeInfosList = [s.structureInfo.getRadixCodeInfoList() for s in self.getStructureList()]
		return CompoundStructureInfo.getAllCodeInfoListFromCodeInfoCollection(codeInfosList)

	def getOperator(self):
		return self.__operator

	def getStructureList(self):
		return self.__structureList

	@staticmethod
	def getAllCodeInfoListFromCodeInfoCollection(codeInfoListCollection):
		def combineList(infoListList, infoListOfNode):
			prevInfoListList = infoListList if len(infoListList) > 0 else ([], )
			ansListList = [infoList + [codeInfo]
						for infoList in prevInfoListList
						for codeInfo in infoListOfNode]
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
		self.__normalStructureList = []
		self.__mainStructure = None

	def getOperator(self):
		mainStructure = self.getMainStructure()
		if mainStructure:
			structureInfo = mainStructure.structureInfo
			return structureInfo.getOperator()
		else:
			return None

	def getChildStructures(self):
		return self.getStructureList(True)

	@property
	def codeInfos(self):
		return ()

	def getName(self):
		return self.__name

	def getMainStructure(self):
		return self.__mainStructure

	def setMainStructure(self, structure):
		self.__mainStructure = structure

	def addStructure(self, structure):
		if structure.isUnit():
			self.__unitStructureList.append(structure)
		else:
			self.__normalStructureList.append(structure)

	def getStructureList(self, isWithUnit = False):
		structureList = []

		if self.__mainStructure:
			structureList = [self.__mainStructure]

		if isWithUnit:
			structureList.extend(self.__unitStructureList)

		return structureList

	def getUnitStructureList(self):
		return self.__unitStructureList

	def getNormalStructureList(self):
		return self.__normalStructureList

	def getSubStructure(self, index):
		structure = self.__mainStructure
		if not structure:
			return None

		structureList = structure.getStructureList()
		return structureList[index]

	def getSubStructureList(self, subIndex = 0):
		if(subIndex > 0):
			structure = self.getSubStructure(subIndex - 1)
			structureList = [structure]
		else:
			structureList = self.getStructureList(True)
		return structureList

