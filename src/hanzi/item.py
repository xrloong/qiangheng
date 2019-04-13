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
		pass
		referenceName = referenceNode.getName()
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

