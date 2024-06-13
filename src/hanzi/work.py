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
			nodeStructure = structure.structureInfo.referencedNodeStructure
			if nodeStructure:
				self.computeCharacterInfo.expandNodeStructure(nodeStructure)

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

	def __constructCharacter(self, character):
		node = self.touchCharacter(character)
		nodeStructure = node.nodeStructure
		assert nodeStructure.isNode()

		self.expandNodeStructure(nodeStructure)
		self.codeInfosComputer.computeForNodeStructure(nodeStructure)

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

		radixManager = structureManager.radixManager

		if radixManager.hasRadix(character) and not nodeStructure.hasUnitStructures():
			radixInfoList = radixManager.getRadixCodeInfoList(character)
			for radixCodeInfo in radixInfoList:
				structure = workspaceManager.getUnitStructure(radixCodeInfo)
				workspaceManager.addStructureIntoNode(structure, nodeStructure)

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

		self.__constructCharacter(name)

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

	def __appendFastCode(self, character: str):
		fastCode = self.structureManager.queryFastCode(character)
		if fastCode:
			node = self.touchCharacter(character)
			characterInfo = node.tag
			characterInfo.setFastCode(fastCode)

	def reset(self):
		self.__workspaceManager.reset()

	def computeCharacter(self, character: str) -> Optional[CharacterInfo]:
		self.__constructCharacter(character)
		self.__appendFastCode(character)
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

