from .workspace import HanZiStructure, HanZiNode
from .workspace import HanZiWorkspace
from .workspace import UnitStructureInfo, WrapperStructureInfo, CompoundStructureInfo

class HanZiWorkspaceManager:
	def __init__(self):
		self.__workspace = HanZiWorkspace()
		self.__wrapperExpressionDict = {}

	def findNode(self, name):
		return self.__workspace.findNode(name)

	def isWithNode(self, name):
		return self.__workspace.isWithNode(name)

	def isNodeExpanded(self, name):
		return self.__workspace.isNodeExpanded(name)

	def addNode(self, node):
		return self.__workspace.addNode(node)

	def reset(self):
		self.__workspace.reset()

	def touchNode(self, character):
		if not self.isWithNode(character):
			node = self.generateNode(character)
			self.addNode(node)
		return self.findNode(character)

	def generateNode(self, character):
		node = HanZiNode(character)
		return node

	def getUnitStructure(self, radixCodeInfo):
		return self.__generateUnitStructure(radixCodeInfo)

	def getCompoundStructure(self, operator, structureList):
		return self.generateCompoundStructure(operator, structureList)

	def generateCompoundStructure(self, operator, structureList):
		return self.__generateCompoundStructure(operator, structureList)

	def getWrapperStructureByNodeName(self, nodeName, index = 0):
		self.touchNode(nodeName)
		return self.getWrapperStructure(nodeName, index)

	def getWrapperStructure(self, name, index):
		wrapperExpression = (name, index)
		if (name, index) in self.__wrapperExpressionDict:
			return self.__wrapperExpressionDict[wrapperExpression]

		referenceNode = self.findNode(name)
		structure = self.__generateWrapperStructure(referenceNode, index)

		self.__wrapperExpressionDict[wrapperExpression] = structure
		return structure

	def __generateUnitStructure(self, radixCodeInfo):
		structureInfo = UnitStructureInfo(radixCodeInfo)
		return HanZiStructure(structureInfo)

	def __generateWrapperStructure(self, referenceNode, index):
		nodeStrcuture = referenceNode.nodeStructure
		structureInfo = WrapperStructureInfo(nodeStrcuture, index)
		return HanZiStructure(structureInfo)

	def __generateCompoundStructure(self, operator, structureList):
		structureInfo = CompoundStructureInfo(operator, structureList)
		return HanZiStructure(structureInfo)

	def addStructureIntoNode(self, structure, nodeStructure):
		nodeStructure.structureInfo.addStructure(structure)

	def setMainStructureOfNode(self, structure, nodeStructure):
		nodeStructure.structureInfo.setMainStructure(structure)


