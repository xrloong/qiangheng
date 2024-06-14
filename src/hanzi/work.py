from typing import Optional
from injector import inject

from element.enum import FontVariance

from workspace import HanZiWorkspaceManager

from .helper import HanZiCodeInfosComputer
from .helper import HanZiInterpreter
from .helper import HanZiTreeRegExpInterpreter
from .manager import StructureManager

from model.element.CharacterInfo import CharacterInfo
from model.manager import SubstituteManager

class CharacterComputingHelper:
	class RearrangeCallback(SubstituteManager.RearrangeCallback):
		def __init__(self, computeCharacterInfo, treInterpreter):
			self.computeCharacterInfo = computeCharacterInfo
			self.treInterpreter = treInterpreter

		def prepare(self, structure):
			if structure.isWrapper():
				character = structure.referencedNodeName
				self.computeCharacterInfo.constructCharacter(character)

		def matchAndReplace(self, tre, structure, result):
			return self.treInterpreter.matchAndReplace(tre, structure, result)

	@inject
	def __init__(self,
			fontVariance: FontVariance,

			structureManager: StructureManager,
			treInterpreter: HanZiTreeRegExpInterpreter,

			workspaceManager: HanZiWorkspaceManager,
			codeInfosComputer: HanZiCodeInfosComputer,

			hanziInterpreter: HanZiInterpreter,
			):
		self.fontVariance = fontVariance

		self.structureManager = structureManager

		self.__workspaceManager = workspaceManager
		self.codeInfosComputer = codeInfosComputer

		self.rearrangeCallback = CharacterComputingHelper.RearrangeCallback(self, treInterpreter)

		self.__hanziInterpreter = hanziInterpreter

	def constructCharacter(self, character):
		node = self.touchCharacter(character)
		nodeStructure = node.nodeStructure
		assert nodeStructure.isNode()

		self.__appendRadicalCodes(nodeStructure)
		self.__appendFastCode(nodeStructure)

		self.expandNodeStructure(nodeStructure)
		self.codeInfosComputer.computeForNode(node)

	def queryDescription(self, characterName):
		return self.structureManager.queryCharacterDescription(characterName)

	def touchCharacter(self, character):
		return self.__workspaceManager.touchNode(character)

	def expandNodeStructure(self, nodeStructure):
		assert nodeStructure.isNode()

		workspaceManager = self.__workspaceManager

		character = nodeStructure.name
		if workspaceManager.isNodeExpanded(character):
			return

		structureManager = self.structureManager

		charDesc = self.queryDescription(character)

		nodeName = character
		structDescList = charDesc.structures
		for structDesc in structDescList:
			if structDesc.isEmpty():
				continue

			structure = self.__convertToStructure(structDesc)

			workspaceManager.addStructureIntoNode(structure, nodeStructure)

			isMainStructure = self.fontVariance.contains(structDesc.fontVariance)
			if isMainStructure:
				workspaceManager.setMainStructureOfNode(structure, nodeStructure)

	def __convertToStructure(self, structDesc):
		structure = self.recursivelyConvertDescriptionToStructure(structDesc)

		structureManager = self.structureManager
		templateManager = structureManager.templateManager
		substituteManager = structureManager.substituteManager

		templateManager.recursivelyRearrangeStructure(structure, self.rearrangeCallback)
		substituteManager.recursivelyRearrangeStructure(structure, self.rearrangeCallback)

		return structure

	def recursivelyConvertDescriptionToStructure(self, structDesc):
		if structDesc.isLeaf():
			structure = self.generateReferenceLink(structDesc)
		else:
			structure = self.generateLink(structDesc)

		return structure

	def generateReferenceLink(self, structDesc):
		name = structDesc.referenceName
		nodeExpression = structDesc.referenceExpression

		self.constructCharacter(name)

		l = nodeExpression.split(".")
		if len(l)>1:
			subIndex = int(l[1])
		else:
			subIndex = 0

		return self.__workspaceManager.getWrapperStructure(name, subIndex)

	def generateLink(self, structDesc):
		childStructureList = []
		childDescList = self.structureManager.queryChildren(structDesc)
		for childSrcDesc in childDescList:
			childStructure = self.recursivelyConvertDescriptionToStructure(childSrcDesc)
			childStructureList.append(childStructure)

		operator = structDesc.operator

		return self.__workspaceManager.generateCompoundStructure(operator, childStructureList)

	def __appendRadicalCodes(self, nodeStructure):
		assert nodeStructure.isNode()

		if not nodeStructure.hasUnitStructures():
			workspaceManager = self.__workspaceManager
			radixManager = self.structureManager.radixManager

			character = nodeStructure.name
			if radixManager.hasRadix(character):
				radixInfoList = radixManager.getRadixCodeInfoList(character)
				for radixCodeInfo in radixInfoList:
					structure = workspaceManager.getUnitStructure(radixCodeInfo)
					workspaceManager.addStructureIntoNode(structure, nodeStructure)


	def __appendFastCode(self, nodeStructure):
		assert nodeStructure.isNode()

		if not nodeStructure.fastCodeInfo:
			character = nodeStructure.name
			fastCodeInfo = self.structureManager.queryFastCodeInfo(character)
			if fastCodeInfo:
				nodeStructure.fastCodeInfo = fastCodeInfo

	def reset(self):
		self.__workspaceManager.reset()

	def computeCharacter(self, character: str) -> Optional[CharacterInfo]:
		self.constructCharacter(character)
		charNode = self.touchCharacter(character)
		return self.__hanziInterpreter.interpretCharacterInfo(charNode) if charNode else None

class CharacterComputingWork:
	@inject
	def __init__(self,
			computingHelper: CharacterComputingHelper,
			):
		self.__computingHelper = computingHelper

	def compute(self, characters, separateComputing) -> list[CharacterInfo]:
		computingHelper = self.__computingHelper

		characterInfos = []
		for character in characters:
			if separateComputing:
				computingHelper.reset()

			characterInfo = computingHelper.computeCharacter(character)
			if characterInfo:
				characterInfos.append(characterInfo)

		return characterInfos

