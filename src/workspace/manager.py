from .workspace import HanZiStructure, HanZiNode
from .workspace import HanZiWorkspace
from .workspace import UnitStructureInfo, WrapperStructureInfo, CompoundStructureInfo

from coding.Base import CodeInfo
from element.operator import Operator

class HanZiWorkspaceManager:
	def __init__(self):
		self.__workspace = HanZiWorkspace()
		self.__wrapperExpressionDict = {}

	def isNodeExpanded(self, name: str) -> bool:
		return self.__workspace.isNodeExpanded(name)

	def reset(self):
		self.__workspace.reset()

	def touchNode(self, character: str) -> HanZiNode:
		return self.__workspace.touchNode(character)

	def getUnitStructure(self, radixCodeInfo: CodeInfo) -> HanZiStructure:
		return self.__generateUnitStructure(radixCodeInfo)

	def generateCompoundStructure(self, operator: Operator, structureList: list[HanZiStructure]) -> HanZiStructure:
		return self.__generateCompoundStructure(operator, structureList)

	def getWrapperStructure(self, name: str, index: int = 0) -> HanZiStructure:
		wrapperExpression = (name, index)
		if (name, index) in self.__wrapperExpressionDict:
			return self.__wrapperExpressionDict[wrapperExpression]

		referenceNode = self.touchNode(name)
		structure = self.__generateWrapperStructure(referenceNode, index)

		self.__wrapperExpressionDict[wrapperExpression] = structure
		return structure

	def __generateUnitStructure(self, radixCodeInfo: CodeInfo) -> HanZiStructure:
		structureInfo = UnitStructureInfo(radixCodeInfo)
		return HanZiStructure(structureInfo)

	def __generateWrapperStructure(self, referenceNode: HanZiNode, index: int) -> HanZiStructure:
		nodeStrcuture = referenceNode.nodeStructure
		structureInfo = WrapperStructureInfo(nodeStrcuture, index)
		return HanZiStructure(structureInfo)

	def __generateCompoundStructure(self, operator: Operator, structureList: list[HanZiStructure]) -> HanZiStructure:
		structureInfo = CompoundStructureInfo(operator, structureList)
		return HanZiStructure(structureInfo)

	def addStructureIntoNode(self, structure: HanZiStructure, nodeStructure: HanZiStructure):
		assert nodeStructure.isNode()

		nodeStructure.structureInfo.addStructure(structure)

	def setMainStructureOfNode(self, structure: HanZiStructure, nodeStructure: HanZiStructure):
		assert nodeStructure.isNode()

		nodeStructure.structureInfo.setMainStructure(structure)

