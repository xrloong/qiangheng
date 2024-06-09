from typing import Optional
from injector import inject

from element.enum import FontVariance

from .helper import HanZiWorkspaceManager
from .helper import HanZiCodeInfosComputer
from .helper import HanZiWorkspaceItemFactory
from .helper import HanZiInterpreter
from .helper import HanZiTreeRegExpInterpreter
from .manager import StructureManager

from model.element.CharacterInfo import CharacterInfo
from model.manager import SubstituteManager

class CharacterComputingWork:
	class RearrangeCallback(SubstituteManager.RearrangeCallback):
		def __init__(self, computeCharacterInfo, treInterpreter):
			self.computeCharacterInfo = computeCharacterInfo
			self.treInterpreter = treInterpreter

		def prepare(self, structure):
			nodeStructure = structure.structureInfo.getReferencedNodeStructure()
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
			itemFactory: HanZiWorkspaceItemFactory,

			hanziInterpreter: HanZiInterpreter,
			):
		self.fontVariance = fontVariance

		self.structureManager = structureManager

		self.__workspaceManager = workspaceManager
		self.codeInfosComputer = codeInfosComputer
		self.itemFactory = itemFactory

		self.rearrangeCallback = CharacterComputingWork.RearrangeCallback(self, treInterpreter)

		self.__hanziInterpreter = hanziInterpreter

	def __constructCharacter(self, character):
		node = self.touchCharacter(character)
		nodeStructure = node.nodeStructure
		self.expandNodeStructure(nodeStructure)
		self.codeInfosComputer.computeForNodeStructure(nodeStructure)


	def queryDescription(self, characterName):
		return self.structureManager.queryCharacterDescription(characterName)

	def touchCharacter(self, character):
		return self.itemFactory.touchNode(character)

	def expandNodeStructure(self, nodeStructure):
		workspaceManager = self.__workspaceManager

		nodeStructureInfo = nodeStructure.structureInfo

		character = nodeStructureInfo.getName()
		if workspaceManager.isNodeExpanded(character):
			return

		structureManager = self.structureManager

		radixManager = structureManager.radixManager
		itemFactory = self.itemFactory

		templateManager = structureManager.templateManager
		substituteManager = structureManager.substituteManager

		if radixManager.hasRadix(character) and len(nodeStructureInfo.getUnitStructureList()) == 0:
			radixInfoList = radixManager.getRadixCodeInfoList(character)
			for radixCodeInfo in radixInfoList:
				structure = itemFactory.getUnitStructure(radixCodeInfo)
				workspaceManager.addStructureIntoNode(structure, nodeStructure)

		charDesc = self.queryDescription(character)

		nodeName = character
		structDescList = charDesc.structures
		for structDesc in structDescList:
			if structDesc.isEmpty():
				continue

			characterFontVariance = structDesc.fontVariance
			isMainStructure = characterFontVariance.belongsTo(self.fontVariance)

			structure = self.recursivelyConvertDescriptionToStructure(structDesc)

			templateManager.recursivelyRearrangeStructure(structure, self.rearrangeCallback)
			substituteManager.recursivelyRearrangeStructure(structure, self.rearrangeCallback)

			workspaceManager.addStructureIntoNode(structure, nodeStructure)
			if isMainStructure:
				workspaceManager.setMainStructureOfNode(structure, nodeStructure)

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

		return self.itemFactory.getWrapperStructureByNodeName(name, subIndex)

	def generateLink(self, structDesc):
		childStructureList = []
		childDescList = self.structureManager.queryChildren(structDesc)
		for childSrcDesc in childDescList:
			childStructure = self.recursivelyConvertDescriptionToStructure(childSrcDesc)
			childStructureList.append(childStructure)

		operator = structDesc.operator

		return self.itemFactory.getCompoundStructure(operator, childStructureList)

	def computeCharacter(self, character: str) -> Optional[CharacterInfo]:
		self.__constructCharacter(character)
		fastCode = self.structureManager.queryFastCode(character)
		if fastCode:
			node = self.touchCharacter(character)
			characterInfo = node.tag
			characterInfo.setFastCode(fastCode)

		charNode = self.__workspaceManager.findNode(character)
		return self.__hanziInterpreter.interpretCharacterInfo(charNode) if charNode else None

	def compute(self, characters) -> list[CharacterInfo]:
		characterInfos = []

		for character in characters:
			characterInfo = self.computeCharacter(character)
			if characterInfo:
				characterInfos.append(characterInfo)

		return characterInfos

