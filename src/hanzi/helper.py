from injector import inject

from workspace import HanZiWorkspaceManager

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
		assert nodeStructure.isNode()
		nodeStructureInfo = nodeStructure.structureInfo

		structureList = nodeStructureInfo.childStructures
		codeInfoList = sum(map(lambda s: s.getComputedCodeInfos(), structureList), ())

		fastCodeInfo = nodeStructure.fastCodeInfo
		if fastCodeInfo:
			codeInfoList = codeInfoList + (fastCodeInfo, )

		codeList = self.codeInfoInterpreter.interpretCodeInfoList(codeInfoList)

		characterInfo = hanziNode.tag
		characterInfo.setCodeProps(codeList)

		return characterInfo

class HanZiCodeInfosComputer:
	@inject
	def __init__(self, codeInfoInterpreter: CodeInfoInterpreter):
		self.__codeInfoInterpreter = codeInfoInterpreter

	def computeForNodeStructure(self, nodeStructure):
		"""設定某一個字符所包含的部件的碼"""
		self.__recursivelyComputeCodeInfosOfStructureTree(nodeStructure)

	def __recursivelyComputeCodeInfosOfStructureTree(self, structure):
		if not structure:
			return

		if structure.isCodeInfoGenerated():
			return

		for cihldStructure in structure.getChildStructures():
			self.__recursivelyComputeCodeInfosOfStructureTree(cihldStructure)
		self.__generateCodeInfosOfStructure(structure)

	def __generateCodeInfosOfStructure(self, structure):
		structureInfo = structure.structureInfo
		operator = structureInfo.getOperator()

		codeInfosCollection = structureInfo.codeInfos

		allCodeInfos = self.__computeAllCodeInfos(operator, codeInfosCollection)
		structureInfo.setComputedCodeInfos(allCodeInfos)

	def __computeAllCodeInfos(self, operator, codeInfosCollection):
		computedCodeInfoList = (self.__computeCodeInfo(operator, codeInfos) for codeInfos in codeInfosCollection)
		allCodeInfos = tuple(filter(lambda codeInfo: codeInfo != None, computedCodeInfoList))
		return allCodeInfos

	def __computeCodeInfo(self, operator, codeInfos):
		if operator:
			codeInfo = self.__codeInfoInterpreter.encodeToCodeInfo(operator, codeInfos)
		else:
			codeInfo = codeInfos[0]
		return codeInfo


class HanZiTreeProxy(BasicTreeProxy):
	@inject
	def __init__(self): pass

	def getChildren(self, currentStructure):
		return currentStructure.getExpandedStructureList()

	def matchSingle(self, tre, currentStructure):
		prop = tre.prop
		opName = prop.get("運算")
		refExp = prop.get("名稱")
		return currentStructure.isMatchStructure(operatorName = opName, referenceExpression = refExp)

class HanZiTreeNodeGenerator(TreeNodeGenerator):
	@inject
	def __init__(self,
              workspaceManager: HanZiWorkspaceManager,
              operatorManager: OperatorManager,
              ):
		self.__workspaceManager = workspaceManager
		self.__operatorManager = operatorManager

	def generateLeafNode(self, nodeName):
		return self.__workspaceManager.getWrapperStructure(nodeName)

	def generateLeafNodeByReference(self, referencedTreeNode, index):
		return self.__workspaceManager.getWrapperStructure(referencedTreeNode.referencedNodeName, index)

	def generateNode(self, operatorName, children):
		operator = self.__operatorManager.generateOperator(operatorName)
		return self.__workspaceManager.generateCompoundStructure(operator, children)

class HanZiTreeRegExpInterpreter(TreeRegExpInterpreter):
	@inject
	def __init__(self,
                 treeProxy: HanZiTreeProxy,
                 treeNodeGenerator: HanZiTreeNodeGenerator
              ):
		super().__init__(HanZiTreeProxy(), treeNodeGenerator)

