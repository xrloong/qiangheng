import abc

from injector import inject

class StructureTag:
	def __init__(self):
		self.flagIsTemplateApplied = False
		self.flagIsSubstituteApplied = False

	def isTemplateApplied(self):
		return self.flagIsTemplateApplied

	def isSubstituteApplied(self):
		return self.flagIsSubstituteApplied

	def setTemplateApplied(self):
		self.flagIsTemplateApplied=True

	def setSubstituteApplied(self):
		self.flagIsSubstituteApplied=True

class StructureInfo(object, metaclass=abc.ABCMeta):
	def __init__(self):
		self.codeInfos = None

	def setComputedCodeInfos(self, codeInfos):
		self.codeInfos = codeInfos

	def getComputedCodeInfos(self):
		return self.codeInfos

	def isCodeInfoGenerated(self):
		return self.codeInfos != None

	def getRadixCodeInfoList(self):
		return filter(lambda x: x.isSupportRadixCode(), self.codeInfos)


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
			return operator.getName()
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

	def getCodeInfosTuple(self):
		return ()

class UnitStructureInfo(StructureInfo):
	def __init__(self, radixCodeInfo):
		super().__init__()

		self.radixCodeInfo = radixCodeInfo

		self.referenceNode=None
		self.index=0

	def getChildStructures(self):
		return ()

	def getCodeInfosTuple(self):
		return ((self.radixCodeInfo, ), )

class WrapperStructureInfo(StructureInfo):
	def __init__(self, nodeStructure, index):
		super().__init__()

		nodeStructureInfo = nodeStructure.getStructureInfo()
		referenceName = nodeStructureInfo.getName()
		if index==0:
			referenceExpression = "{}".format(referenceName)
		else:
			referenceExpression = "{}.{}".format(referenceName,index)

		self.nodeStructure = nodeStructure
		self.nodeStructureInfo = nodeStructureInfo
		self.index = index
		self.referenceExpression = referenceExpression

	def getOperatorName(self):
		nodeStructureInfo = self.getReferencedNodeStructureInfo()
		return nodeStructureInfo.getOperatorName()

	def getExpandedOperator(self):
		nodeStructureInfo = self.getReferencedNodeStructureInfo()
		expandedStructure = nodeStructureInfo.getMainStructure()
		if expandedStructure:
			return expandedStructure.getStructureInfo().getOperator()
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

	def getCodeInfosTuple(self):
		nodeStructureInfo = self.nodeStructureInfo
		index = self.index

		structureList = nodeStructureInfo.getSubStructureList(index)
		codeInfosList = sum((s.getComputedCodeInfos() for s in structureList), ())
		return tuple((codeInfos, ) for codeInfos in codeInfosList)

	def getReferenceExpression(self):
		return self.referenceExpression

	def getReferencedNodeStructure(self):
		return self.nodeStructure

	def getReferencedNodeStructureInfo(self):
		return self.nodeStructureInfo


class CompoundStructureInfo(StructureInfo):
	def __init__(self, operator, structureList):
		super().__init__()

		self.operator = operator
		self.structureList = structureList

	def getChildStructures(self):
		return self.getStructureList()

	def getCodeInfosTuple(self):
		codeInfosList = [s.getStructureInfo().getRadixCodeInfoList() for s in self.getStructureList()]
		return CompoundStructureInfo.getAllCodeInfoListFromCodeInfoCollection(codeInfosList)

	def changeToStructure(self, structureInfo):
		self.operator = structureInfo.getOperator()
		self.structureList = structureInfo.getStructureList() 

	def getOperator(self):
		return self.operator

	def getStructureList(self):
		return self.structureList

	@staticmethod
	def getAllCodeInfoListFromCodeInfoCollection(codeInfoListCollection):
		def combineList(infoListList, infoListOfNode):
			prevInfoListList = infoListList if len(infoListList) > 0 else ([], )
			ansListList = [infoList + [codeInfo]
						for infoList in prevInfoListList
						for codeInfo in infoListOfNode]
			return ansListList

		combineInfoListList=[]
		for codeInfoList in codeInfoListCollection:
			combineInfoListList = combineList(combineInfoListList, codeInfoList)

		return combineInfoListList

class NodeStructureInfo(StructureInfo):
	def __init__(self, name):
		super().__init__()

		self.name = name

		self.unitStructureList = []
		self.normalStructureList = []
		self.mainStructure = None

	def getOperator(self):
		mainStructure = self.getMainStructure()
		if mainStructure:
			structureInfo = mainStructure.getStructureInfo()
			return structureInfo.getOperator()
		else:
			return None

	def getChildStructures(self):
		return self.getStructureList(True)

	def getCodeInfosTuple(self):
		return ()

	def __str__(self):
		return self.name

	def getName(self):
		return self.name

	def getMainStructure(self):
		return self.mainStructure

	def setMainStructure(self, structure):
		self.mainStructure=structure

	def addStructure(self, structure):
		if structure.isUnit():
			self.unitStructureList.append(structure)
		else:
			self.normalStructureList.append(structure)

	def getStructureList(self, isWithUnit=False):
		structureList=[]

		if self.mainStructure:
			structureList=[self.mainStructure]

		if isWithUnit:
			structureList.extend(self.unitStructureList)

		return structureList

	def getUnitStructureList(self):
		return self.unitStructureList

	def getNormalStructureList(self):
		return self.normalStructureList

	def getSubStructure(self, index):
		structure = self.mainStructure
		if not structure:
			return None

		structureList=structure.getStructureList()
		return structureList[index]

	def getSubStructureList(self, subIndex = 0):
		if(subIndex > 0):
			structure=self.getSubStructure(subIndex - 1)
			structureList=[structure]
		else:
			structureList=self.getStructureList(True)
		return structureList

