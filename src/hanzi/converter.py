from injector import inject

from .helper import HanZiNetworkManager
from .helper import HanZiCodeInfosComputer
from .helper import HanZiNetworkItemFactory
from .helper import HanZiInterpreter
from .network import HanZiNetwork

from model.element.enum import FontVariance

from model.manager import StructureManager
from model.CharacterDescriptionManager import RadixManager
from model.CharacterDescriptionManager import SubstituteManager

from tree.regexp import TreeRegExpInterpreter
from tree.regexp import BasicTreeProxy
from tree.regexp import TreeNodeGenerator

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
	def __init__(self, itemFactory: HanZiNetworkItemFactory):
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


def isBelongToFontVariance(characterFontVariance, targetFontVariance):
	if targetFontVariance ==  FontVariance.All:
		return True
	elif targetFontVariance ==  FontVariance.Traditional:
		return characterFontVariance in [FontVariance.All, FontVariance.Traditional]
	elif targetFontVariance ==  FontVariance.Simplified:
		return characterFontVariance in [FontVariance.All, FontVariance.Simplified]
	else:
		return False

class ConstructCharacter:
	class RearrangeCallback(SubstituteManager.RearrangeCallback):
		def __init__(self, computeCharacterInfo, treInterpreter):
			self.computeCharacterInfo = computeCharacterInfo
			self.treInterpreter = treInterpreter

		def prepare(self, structure):
			nodeStructure = structure.getStructureInfo().getReferencedNodeStructure()
			if nodeStructure:
				self.computeCharacterInfo.expandNodeStructure(nodeStructure)

		def matchAndReplace(self, tre, structure, result):
			return self.treInterpreter.matchAndReplace(tre, structure, result)

	@inject
	def __init__(self,
			fontVariance: FontVariance,

			structureManager: StructureManager,
			treInterpreter: HanZiTreeRegExpInterpreter,

			networkManager: HanZiNetworkManager,
			codeInfosComputer: HanZiCodeInfosComputer,
			itemFactory: HanZiNetworkItemFactory
			):
		self.fontVariance = fontVariance

		self.structureManager = structureManager

		self.networkManager = networkManager
		self.codeInfosComputer = codeInfosComputer
		self.itemFactory = itemFactory

		self.rearrangeCallback = ConstructCharacter.RearrangeCallback(self, treInterpreter)

	def compute(self, characters):
		for character in characters:
			self.constructCharacter(character)

	def constructCharacter(self, character):
		node = self.touchCharacter(character)
		nodeStructure = node.getNodeStructure()
		self.expandNodeStructure(nodeStructure)
		self.computeNode(nodeStructure)

	def appendFastCodes(self):
		fastCharacterDict = self.structureManager.loadFastCodes()
		for (character, fastCodeInfos) in fastCharacterDict.items():
			assert len(fastCodeInfos) ==  1
			fastCodeInfo = fastCodeInfos[0]
			fastCode = fastCodeInfo.code

			node = self.touchCharacter(character)
			characterInfo = node.tag
			characterInfo.setFastCode(fastCode)

	def queryDescription(self, characterName):
		return self.structureManager.queryCharacterDescription(characterName)

	def touchCharacter(self, character):
		return self.itemFactory.touchNode(character)

	def expandNodeStructure(self, nodeStructure):
		networkManager = self.networkManager

		nodeStructureInfo = nodeStructure.getStructureInfo()

		character = nodeStructureInfo.getName()
		if networkManager.isNodeExpanded(character):
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
				networkManager.addStructureIntoNode(structure, nodeStructure)

		charDesc = self.queryDescription(character)

		nodeName = character
		structDescList = charDesc.structures
		for structDesc in structDescList:
			if structDesc.isEmpty():
				continue

			characterFontVariance = structDesc.getFontVariance()
			isMainStructure = isBelongToFontVariance(characterFontVariance, self.fontVariance)

			structure = self.recursivelyConvertDescriptionToStructure(structDesc)

			templateManager.recursivelyRearrangeStructure(structure, self.rearrangeCallback)
			substituteManager.recursivelyRearrangeStructure(structure, self.rearrangeCallback)

			networkManager.addStructureIntoNode(structure, nodeStructure)
			if isMainStructure:
				networkManager.setMainStructureOfNode(structure, nodeStructure)

	def recursivelyConvertDescriptionToStructure(self, structDesc):
		if structDesc.isLeaf():
			structure = self.generateReferenceLink(structDesc)
		else:
			structure = self.generateLink(structDesc)

		return structure

	def generateReferenceLink(self, structDesc):
		name = structDesc.getReferenceName()
		nodeExpression = structDesc.getReferenceExpression()

		self.constructCharacter(name)

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

		operator = structDesc.getOperator()

		return self.itemFactory.getCompoundStructure(operator, childStructureList)

	def computeNode(self, nodeStructure):
		self.codeInfosComputer.computeForNodeStructure(nodeStructure)

class ComputeCharacter:
	@inject
	def __init__(self,
			hanziNetwork: HanZiNetwork,
			hanziInterpreter: HanZiInterpreter,
			):
		self.__hanziNetwork = hanziNetwork
		self.__hanziInterpreter = hanziInterpreter

	def compute(self, characters: list):
		characterInfos = []
		for character in characters:
			characterInfo = self.__computeOne(character)
			if characterInfo:
				characterInfos.append(characterInfo)
		return characterInfos

	def __computeOne(self, character: str):
		charNode = self.__hanziNetwork.findNode(character)
		if charNode:
			characterInfo = self.__hanziInterpreter.interpretCharacterInfo(charNode)
			return characterInfo

