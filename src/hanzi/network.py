from .item import StructureTag
from .item import UnitStructureInfo, WrapperStructureInfo, CompoundStructureInfo, NodeStructureInfo

class HanZiNode:
	def __init__(self, name, tag):
		self.name = name
		self.tag = tag

		nodeStructureInfo = NodeStructureInfo(name)
		self.nodeStructure = HanZiStructure(nodeStructureInfo)

	def __str__(self):
		return self.name

	def getName(self):
		return self.name

	def getNodeStructure(self):
		return self.nodeStructure

	def getTag(self):
		return self.tag

class HanZiStructure:
	def __init__(self, structureInfo):
		self.structureInfo = structureInfo
		self.tag = StructureTag()


	def getTag(self):
		return self.tag

	def getStructureInfo(self):
		return self.structureInfo


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

	def isMatchStructure(self, operatorName = None, referenceExpression = None):
		isMatch = True
		if referenceExpression:
			isMatch &= referenceExpression == self.structureInfo.getReferenceExpression()

		if operatorName:
			isMatch &= operatorName == self.structureInfo.getExpandedOperatorName()

		return isMatch

	def getStructureList(self):
		return self.structureInfo.getStructureList()

	def getReferencedNodeName(self):
		nodeStructureInfo = self.structureInfo.getReferencedNodeStructureInfo()
		return nodeStructureInfo.getName()

	def getExpandedStructure(self):
		if self.isWrapper():
			nodeStructureInfo = self.structureInfo.getReferencedNodeStructureInfo()
			expandedStructure = nodeStructureInfo.getMainStructure()
			if expandedStructure:
				return expandedStructure
			else:
				return self
		else:
			return self

	def getExpandedStructureList(self):
		expanedStructure = self.getExpandedStructure()
		return expanedStructure.getStructureList()

	def setNewStructure(self, newTargetStructure):
		operator = newTargetStructure.structureInfo.operator
		structureList = newTargetStructure.structureInfo.structureList
		self.structureInfo.changeToStructure(operator, structureList)


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
		nodeStructure = node.getNodeStructure()
		nodeStructureInfo = nodeStructure.getStructureInfo()
		mainStructure = nodeStructureInfo.getMainStructure()
		return bool(mainStructure)

