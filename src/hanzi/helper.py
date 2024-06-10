from injector import inject

from workspace import HanZiStructure, HanZiNode
from workspace import HanZiWorkspace
from workspace import UnitStructureInfo, WrapperStructureInfo, CompoundStructureInfo

from model.element.CharacterInfo import CharacterInfo
from model.interpreter import CodeInfoInterpreter
from model.helper import OperatorManager

from tree.regexp import TreeRegExpInterpreter
from tree.regexp import BasicTreeProxy
from tree.regexp import TreeNodeGenerator

class HanZiInterpreter:
	@inject
	def __init__(self, codeInfoInterpreter: CodeInfoInterpreter):
		self.codeInfoInterpreter = codeInfoInterpreter

	def interpretCharacterInfo(self, characterNode) -> CharacterInfo:
		return self._getNodeCharacterInfo(characterNode)

	def _getNodeCharacterInfo(self, hanziNode) -> CharacterInfo:
		nodeStructure = hanziNode.nodeStructure
		nodeStructureInfo = nodeStructure.structureInfo

		structureList = nodeStructureInfo.getStructureList(True)
		codeInfoList = sum(map(lambda s: s.getComputedCodeInfos(), structureList), ())

		codeList = self.codeInfoInterpreter.interpretCodeInfoList(codeInfoList)

		characterInfo = hanziNode.tag
		characterInfo.setCodeProps(codeList)

		return characterInfo

class HanZiCodeInfosComputer:
	@inject
	def __init__(self, codeInfoInterpreter: CodeInfoInterpreter):
		self.codeInfoInterpreter = codeInfoInterpreter

	def computeForNodeStructure(self, nodeStructure):
		"""設定某一個字符所包含的部件的碼"""
		self._recursivelyComputeCodeInfosOfStructureTree(nodeStructure)

	def _recursivelyComputeCodeInfosOfStructureTree(self, structure):
		if not structure:
			return

		if structure.isCodeInfoGenerated():
			return

		for cihldStructure in structure.getChildStructures():
			self._recursivelyComputeCodeInfosOfStructureTree(cihldStructure)
		self._generateCodeInfosOfStructure(structure)

	def _generateCodeInfosOfStructure(self, structure):
		structureInfo = structure.structureInfo
		operator = structureInfo.getOperator()

		codeInfosCollection = structureInfo.codeInfos

		allCodeInfos = self._computeAllCodeInfos(operator, codeInfosCollection)
		structureInfo.setComputedCodeInfos(allCodeInfos)

	def _computeAllCodeInfos(self, operator, codeInfosCollection):
		computedCodeInfoList = (self._computeCodeInfo(operator, codeInfos) for codeInfos in codeInfosCollection)
		allCodeInfos = tuple(filter(lambda codeInfo: codeInfo != None, computedCodeInfoList))
		return allCodeInfos

	def _computeCodeInfo(self, operator, codeInfos):
		if operator:
			codeInfo = self.codeInfoInterpreter.encodeToCodeInfo(operator, codeInfos)
		else:
			codeInfo = codeInfos[0]
		return codeInfo


class HanZiWorkspaceManager:
	@inject
	def __init__(self, hanziWorkspace: HanZiWorkspace):
		self.hanziWorkspace = hanziWorkspace

	def findNode(self, name):
		return self.hanziWorkspace.findNode(name)

	def isWithNode(self, name):
		return self.hanziWorkspace.isWithNode(name)

	def isNodeExpanded(self, name):
		return self.hanziWorkspace.isNodeExpanded(name)

	def addNode(self, node):
		return self.hanziWorkspace.addNode(node)

	def addStructureIntoNode(self, structure, nodeStructure):
		nodeStructure.structureInfo.addStructure(structure)

	def setMainStructureOfNode(self, structure, nodeStructure):
		nodeStructure.structureInfo.setMainStructure(structure)

	def reset(self):
		self.hanziWorkspace.reset()

class HanZiWorkspaceItemFactory:
	@inject
	def __init__(self,
		workspaceManager: HanZiWorkspaceManager,
		operatorManager: OperatorManager,
		codeInfoInterpreter: CodeInfoInterpreter):
		self.workspaceManager = workspaceManager
		self.operatorManager = operatorManager
		self.wrapperExpressionDict = {}

	def touchNode(self, character):
		if not self.workspaceManager.isWithNode(character):
			node = self.generateNode(character)
			self.workspaceManager.addNode(node)
		return self.workspaceManager.findNode(character)

	def generateNode(self, character):
		node = HanZiNode(character)
		return node

	def getUnitStructure(self, radixCodeInfo):
		return self.generateUnitStructure(radixCodeInfo)

	def generateUnitStructure(self, radixCodeInfo):
		return self._generateUnitStructure(radixCodeInfo)

	def getCompoundStructure(self, operator, structureList):
		return self.generateCompoundStructure(operator, structureList)

	def getCompoundStructureByOperatorName(self, operatorName, structureList):
		operator = self.operatorManager.generateOperator(operatorName)
		return self.generateCompoundStructure(operator, structureList)

	def generateCompoundStructure(self, operator, structureList):
		return self._generateCompoundStructure(operator, structureList)

	def getWrapperStructureByNodeName(self, nodeName, index = 0):
		self.touchNode(nodeName)
		return self.getWrapperStructure(nodeName, index)

	def getWrapperStructure(self, name, index):
		wrapperExpression = (name, index)
		if (name, index) in self.wrapperExpressionDict:
			return self.wrapperExpressionDict[wrapperExpression]

		referenceNode = self.workspaceManager.findNode(name)
		structure = self.generateWrapperStructure(referenceNode, index)

		self.wrapperExpressionDict[wrapperExpression] = structure
		return structure

	def generateWrapperStructure(self, referenceNode, index):
		return self._generateWrapperStructure(referenceNode, index)

	def _generateUnitStructure(self, radixCodeInfo):
		structureInfo = UnitStructureInfo(radixCodeInfo)
		return HanZiStructure(structureInfo)

	def _generateWrapperStructure(self, referenceNode, index):
		nodeStrcuture = referenceNode.nodeStructure
		structureInfo = WrapperStructureInfo(nodeStrcuture, index)
		return HanZiStructure(structureInfo)

	def _generateCompoundStructure(self, operator, structureList):
		structureInfo = CompoundStructureInfo(operator, structureList)
		return HanZiStructure(structureInfo)


class HanZiTreeProxy(BasicTreeProxy):
	def getChildren(self, currentStructure):
		return currentStructure.getExpandedStructureList()

	def matchSingle(self, tre, currentStructure):
		prop = tre.prop
		opName = prop.get("運算")
		refExp = prop.get("名稱")
		return currentStructure.isMatchStructure(operatorName = opName, referenceExpression = refExp)

class HanZiTreeNodeGenerator(TreeNodeGenerator):
	@inject
	def __init__(self, itemFactory: HanZiWorkspaceItemFactory):
		self.itemFactory = itemFactory

	def generateLeafNode(self, nodeName):
		return self.itemFactory.getWrapperStructureByNodeName(nodeName)

	def generateLeafNodeByReference(self, referencedTreeNode, index):
		structure = referencedTreeNode
		return self.itemFactory.getWrapperStructureByNodeName(structure.getReferencedNodeName(), index)

	def generateNode(self, operatorName, children):
		return self.itemFactory.getCompoundStructureByOperatorName(operatorName, children)

class HanZiTreeRegExpInterpreter(TreeRegExpInterpreter):
	@inject
	def __init__(self, treeNodeGenerator: HanZiTreeNodeGenerator):
		super().__init__(HanZiTreeProxy(), treeNodeGenerator)

