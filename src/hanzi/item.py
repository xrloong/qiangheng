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

	def getReferencedNode(self):
		return None

	def getStructureList(self):
		return []

class UnitStructureInfo(StructureInfo):
	def __init__(self, radixCodeInfo):
		self.radixCodeInfo = radixCodeInfo

		self.referenceNode=None
		self.index=0
		self.referenceExpression=""

		pass

class WrapperStructureInfo(StructureInfo):
	def __init__(self, referenceNode, index):
		nodeStructure = referenceNode.getNodeStructure()
		nodeStructureInfo = nodeStructure.getStructureInfo()
		referenceName = nodeStructureInfo.getName()
		if index==0:
			referenceExpression = "{}".format(referenceName)
		else:
			referenceExpression = "{}.{}".format(referenceName,index)

		self.referenceNode = referenceNode
		self.index = index
		self.referenceExpression = referenceExpression

	def getReferencedNode(self):
		return self.referenceNode


class CompoundStructureInfo(StructureInfo):
	def __init__(self, operator, structureList):
		self.operator = operator
		self.structureList = structureList

	def changeToStructure(self, operator, structureList):
		self.operator = operator
		self.structureList = structureList

	def getOperator(self):
		return self.operator

	def getStructureList(self):
		return self.structureList

class NodeStructureInfo(StructureInfo):
	def __init__(self, name):
		self.name = name

		self.unitStructureList = []
		self.normalStructureList = []
		self.mainStructure = None

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

