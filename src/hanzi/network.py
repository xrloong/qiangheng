from .item import StructureTag
from .item import UnitStructureInfo, WrapperStructureInfo, CompoundStructureInfo

class HanZiNode:
	def __init__(self, name, tag):
		self.name = name

		self.unitStructureList = []
		self.normalStructureList = []
		self.mainStructure = None

		self.tag = tag

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

	def getTag(self):
		return self.tag

	def getStructureTagList(self, subIndex = 0):
		if(subIndex > 0):
			structure=self.getSubStructure(subIndex - 1)
			structureList=[structure]
		else:
			structureList=self.getStructureList(True)
		return [structure.getTag() for structure in structureList]

class HanZiStructure:
	def __init__(self, structureInfo):
		self.structureInfo = structureInfo
		self.tag = StructureTag()

	def __str__(self):
		if self.isCompound():
			structureList=self.getStructureList()
			nameList=[str(structure) for structure in structureList]
			return "(%s %s)"%(self.getOperator(), " ".join(nameList))
		else:
			tag=self.getTag()
			return str(self.tag)

	def isUnit(self):
		return isinstance(self.structureInfo, UnitStructureInfo)

	def isWrapper(self):
		return isinstance(self.structureInfo, WrapperStructureInfo)

	def isCompound(self):
		return isinstance(self.structureInfo, CompoundStructureInfo)

	def isCodeInfoGenerated(self):
		return self.getTag().isCodeInfoGenerated()

	def getReferencedNode(self):
		return self.structureInfo.getReferencedNode()

	def getReferencedNodeName(self):
		return self.getReferencedNode().getName()

	def getOperator(self):
		return self.structureInfo.getOperator()

	def getOperatorName(self):
		if self.isWrapper():
			referenceNode=self.getReferencedNode()
			structure=referenceNode.getMainStructure()
			if structure:
				return structure.getOperator().getName()
			else:
				return ""
		else:
			return self.getOperator().getName()


	def getExpandedStructure(self):
		if self.isWrapper():
			expandedStructure=self.getReferencedNode().getMainStructure()
			if expandedStructure:
				return expandedStructure
			else:
				return self
		else:
			return self

	def getReferenceExpression(self):
		if self.isWrapper():
			return self.structureInfo.referenceExpression
		else:
			return


	def getStructureList(self):
		if self.isCompound():
			return self.structureInfo.getStructureList()
		return []

	def setNewStructure(self, newTargetStructure):
		operator = newTargetStructure.structureInfo.operator
		structureList = newTargetStructure.structureInfo.structureList
		self.structureInfo.changeToStructure(operator, structureList)

	def getTag(self):
		return self.tag

	def getStructureInfo(self):
		return self.structureInfo



class HanZiNetwork:
	def __init__(self):
		self.nodeDict={}

	def addNode(self, node):
		name = node.getName()
		self.nodeDict[name]=node

	def isWithNode(self, name):
		return name in self.nodeDict

	def findNode(self, name):
		return self.nodeDict.get(name)

	def isNodeExpanded(self, name):
		node = self.findNode(name)
		mainStructure = node.getMainStructure()
		return bool(mainStructure)

