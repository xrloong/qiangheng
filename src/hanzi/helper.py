from typing import Optional
from injector import inject

from workspace import HanZiNode, HanZiStructure
from workspace import HanZiWorkspaceManager

from model.element.CharacterInfo import CharacterInfo
from model.interpreter import CodeInfoInterpreter

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
	def __init__(self,
              workspaceManager: HanZiWorkspaceManager,
              codeInfoInterpreter: CodeInfoInterpreter,
              hanziInterpreter: HanZiInterpreter,
              ):
		self.__workspaceManager = workspaceManager
		self.__codeInfoInterpreter = codeInfoInterpreter
		self.__hanziInterpreter = hanziInterpreter

	def __touchCharacter(self, character):
		return self.__workspaceManager.touchNode(character)

	def computeCharacter(self, character: str) -> Optional[CharacterInfo]:
		charNode = self.__touchCharacter(character)
		return self.__computeForNode(charNode)

	def __computeForNode(self, node: HanZiNode) -> Optional[CharacterInfo]:
		"""設定某一個字符所包含的部件的碼"""
		nodeStructure = node.nodeStructure
		assert nodeStructure.isNode()

		self.__recursivelyComputeCodeInfosOfStructureTree(nodeStructure)

		return self.__hanziInterpreter.interpretCharacterInfo(node) if node else None

	def __recursivelyComputeCodeInfosOfStructureTree(self, structure: HanZiStructure):
		if not structure:
			return

		if structure.isCodeInfoGenerated():
			return

		for cihldStructure in structure.getChildStructures():
			self.__recursivelyComputeCodeInfosOfStructureTree(cihldStructure)
		self.__generateCodeInfosOfStructure(structure)

	def __generateCodeInfosOfStructure(self, structure: HanZiStructure):
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

