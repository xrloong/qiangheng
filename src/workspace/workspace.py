from model.element import CharacterInfo

from .info import UnitStructureInfo, WrapperStructureInfo, CompoundStructureInfo, NodeStructureInfo

class HanZiNode:
	def __init__(self, name):
		self.__name = name
		self.__tag = CharacterInfo.CharacterInfo(name)

		nodeStructureInfo = NodeStructureInfo(name)
		self.__nodeStructure = HanZiStructure(nodeStructureInfo)

	def __str__(self):
		return self.name

	@property
	def name(self):
		return self.__name

	@property
	def nodeStructure(self):
		return self.__nodeStructure

	@property
	def tag(self) -> CharacterInfo.CharacterInfo:
		return self.__tag

class HanZiStructure:
	def __init__(self, structureInfo):
		self.__structureInfo = structureInfo

	@property
	def structureInfo(self):
		return self.__structureInfo

	@property
	def name(self) -> str:
		return self.structureInfo.getName()

	@property
	def referencedNodeName(self):
		nodeStructureInfo = self.structureInfo.referencedNodeStructureInfo
		return nodeStructureInfo.getName()

	def hasUnitStructures(self) -> bool:
		return self.structureInfo.hasUnitStructures()

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
			isMatch &= referenceExpression == self.structureInfo.referenceExpression

		if operatorName:
			isMatch &= operatorName == self.structureInfo.getExpandedOperatorName()

		return isMatch

	def getStructureList(self):
		return self.structureInfo.getStructureList()

	def getExpandedOperatorName(self):
		return self.structureInfo.getExpandedOperatorName()

	def getExpandedStructureList(self):
		return self.structureInfo.getExpandedStructureList()

	def getChildStructures(self):
		return self.structureInfo.childStructures

	def changeToStructure(self, newTargetStructure):
		self.__structureInfo = newTargetStructure.structureInfo


class HanZiWorkspace:
	def __init__(self):
		self.__nodeDict = {}

	def reset(self):
		self.__nodeDict = {}

	def __addNode(self, node):
		name = node.name
		self.__nodeDict[name] = node

	def __isWithNode(self, name):
		return name in self.__nodeDict

	def __findNode(self, name):
		return self.__nodeDict.get(name)

	def touchNode(self, character):
		if not self.__isWithNode(character):
			node = HanZiNode(character)
			self.__addNode(node)
		return self.__findNode(character)

	def isNodeExpanded(self, name):
		node = self.__findNode(name)
		nodeStructure = node.nodeStructure
		nodeStructureInfo = nodeStructure.structureInfo
		mainStructure = nodeStructureInfo.getMainStructure()
		return bool(mainStructure)

