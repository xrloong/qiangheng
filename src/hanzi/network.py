from .item import StructureTag
from .item import UnitStructureInfo, WrapperStructureInfo, CompoundStructureInfo, NodeStructureInfo

class HanZiNode:
	def __init__(self, name, tag):
		self.name = name
		self.tag = tag

		nodeStructureInfo = NodeStructureInfo(name)
		self.nodeStructureInfo = nodeStructureInfo
		self.nodeStructure = HanZiStructure(nodeStructureInfo)

	def __str__(self):
		return self.name

	def getName(self):
		return self.name

	def getNodeStructure(self):
		return self.nodeStructure

	def getMainStructure(self):
		return self.nodeStructureInfo.getMainStructure()

	def setMainStructure(self, structure):
		self.nodeStructureInfo.setMainStructure(structure)

	def addStructure(self, structure):
		self.nodeStructureInfo.addStructure(structure)

	def getStructureList(self, isWithUnit=False):
		return self.nodeStructureInfo.getStructureList(isWithUnit)

	def getUnitStructureList(self):
		return self.nodeStructureInfo.getUnitStructureList()

	def getNormalStructureList(self):
		return self.nodeStructureInfo.getNormalStructureList()

	def getSubStructure(self, index):
		return self.nodeStructureInfo.getSubStructure(index)

	def getTag(self):
		return self.tag

	def getStructureTagList(self, subIndex = 0):
		return self.nodeStructureInfo.getStructureTagList(subIndex)

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

	def isNode(self):
		return isinstance(self.structureInfo, NodeStructureInfo)

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

