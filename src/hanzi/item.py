import abc

from injector import inject

class StructureTag:
	def __init__(self):
		self.codeInfoList=[]

		self.flagIsTemplateApplied = False
		self.flagIsSubstituteApplied = False
		self.flagIsCodeInfoGenerated = False

	def isTemplateApplied(self):
		return self.flagIsTemplateApplied

	def isSubstituteApplied(self):
		return self.flagIsSubstituteApplied

	def isCodeInfoGenerated(self):
		return self.flagIsCodeInfoGenerated

	def setTemplateApplied(self):
		self.flagIsTemplateApplied=True

	def setSubstituteApplied(self):
		self.flagIsSubstituteApplied=True

	def setCodeInfoList(self, codeInfoList):
		self.codeInfoList = codeInfoList
		self.flagIsCodeInfoGenerated = True

	def getCodeInfoList(self):
		return self.codeInfoList

	def getRadixCodeInfoList(self):
		return filter(lambda x: x.isSupportRadixCode(), self.codeInfoList)

class StructureInfo(object, metaclass=abc.ABCMeta):
	def __init__(self):
		pass

	def getOperator(self):
		return None

	def getOperatorName(self):
		operator = self.getOperator()
		if operator:
			return operator.getName()
		else:
			return ""

	def getReferencedNodeStructure(self):
		return None

	def getReferencedNodeStructureInfo(self):
		return None

	def getStructureList(self):
		return []

	def getCodeInfosTuple(self):
		return []

class UnitStructureInfo(StructureInfo):
	def __init__(self, radixCodeInfo):
		self.radixCodeInfo = radixCodeInfo

		self.referenceNode=None
		self.index=0
		self.referenceExpression=""

	def getCodeInfosTuple(self):
		return [[self.radixCodeInfo, ], ]

class WrapperStructureInfo(StructureInfo):
	def __init__(self, nodeStructure, index):
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

	def getCodeInfosTuple(self):
		nodeStructureInfo = self.nodeStructureInfo
		index = self.index

		tagList = nodeStructureInfo.getStructureTagList(index)
		codeInfosList = [childTag.getCodeInfoList() for childTag in tagList]
		codeInfosList = sum(codeInfosList, [])
		return [[codeInfos] for codeInfos in codeInfosList]

	def getReferencedNodeStructure(self):
		return self.nodeStructure

	def getReferencedNodeStructureInfo(self):
		return self.nodeStructureInfo


class CompoundStructureInfo(StructureInfo):
	def __init__(self, operator, structureList):
		self.operator = operator
		self.structureList = structureList

	def getCodeInfosTuple(self):
		tagList = [s.getTag() for s in self.getStructureList()]
		codeInfosList = [tag.getRadixCodeInfoList() for tag in tagList]
		return CompoundStructureInfo.getAllCodeInfoListFromCodeInfoCollection(codeInfosList)

	def changeToStructure(self, operator, structureList):
		self.operator = operator
		self.structureList = structureList

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

	def getCodeInfosTuple(self):
		return []

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


	def getStructureTagList(self, subIndex = 0):
		if(subIndex > 0):
			structure=self.getSubStructure(subIndex - 1)
			structureList=[structure]
		else:
			structureList=self.getStructureList(True)
		return [structure.getTag() for structure in structureList]

