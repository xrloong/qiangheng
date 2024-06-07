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
		self.oldStructureInfoList = []

	def getStructureInfo(self):
		return self.structureInfo

	def getComputedCodeInfos(self):
		return self.structureInfo.getComputedCodeInfos()

	def isUnit(self):
		return isinstance(self.structureInfo, UnitStructureInfo)

	def isWrapper(self):
		return isinstance(self.structureInfo, WrapperStructureInfo)

	def isCompound(self):
		return isinstance(self.structureInfo, CompoundStructureInfo)

	def isNode(self):
		return isinstance(self.structureInfo, NodeStructureInfo)

	def isCodeInfoGenerated(self):
		return self.structureInfo.isCodeInfoGenerated()

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

	def getExpandedOperatorName(self):
		return self.structureInfo.getExpandedOperatorName()

	def getExpandedStructureList(self):
		return self.structureInfo.getExpandedStructureList()

	def getChildStructures(self):
		return self.structureInfo.getChildStructures()

	def changeToStructure(self, newTargetStructure):
		self.oldStructureInfoList.append(newTargetStructure.structureInfo)
		self.structureInfo = newTargetStructure.structureInfo


class HanZiWorkspace:
	def __init__(self):
		self.nodeDict = {}

	def addNode(self, node):
		name = node.getName()
		self.nodeDict[name] = node

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

