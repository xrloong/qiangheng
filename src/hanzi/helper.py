from injector import inject

from .network import HanZiNetwork
from .network import HanZiStructure, HanZiNode
from model.interpreter import CodeInfoInterpreter
from model.element import CharacterInfo
from model.manager import OperatorManager

class HanZiInterpreter:
	@inject
	def __init__(self, codeInfoInterpreter: CodeInfoInterpreter):
		self.codeInfoInterpreter = codeInfoInterpreter

	def interpretCharacterInfo(self, characterNode):
		return self._getNodeCharacterInfo(characterNode)

	def _getNodeCharacterInfo(self, hanziNode):
		structureList=hanziNode.getStructureList(True)
		tagList=hanziNode.getStructureTagList()
		codeInfoList=sum(map(lambda tag: tag.getCodeInfoList(), tagList), [])
		codeInfoList=filter(lambda x: x.isSupportCharacterCode(), codeInfoList)

		codeList=self.codeInfoInterpreter.interpretCodeInfoList(codeInfoList)

		characterInfo=hanziNode.getTag()
		characterInfo.setCodeList(codeList)

		return characterInfo

class HanZiCodeInfosComputer:
	@inject
	def __init__(self, codeInfoInterpreter: CodeInfoInterpreter):
		self.codeInfoInterpreter = codeInfoInterpreter

	def computeForNode(self, node):
		"""設定某一個字符所包含的部件的碼"""
		self._recursivelyComputeCodeInfosOfNodeTree(node)

	def _recursivelyComputeCodeInfosOfNodeTree(self, node):
		for structure in node.getStructureList(True):
			self._recursivelyComputeCodeInfosOfStructureTree(structure)

	def _recursivelyComputeCodeInfosOfStructureTree(self, structure):
		if not structure:
			return

		if structure.isCodeInfoGenerated():
			return

		if structure.isUnit():
			pass
		elif structure.isWrapper():
			self._recursivelyComputeCodeInfosOfNodeTree(structure.getReferencedNode())
		elif structure.isCompound():
			for cihldStructure in structure.getStructureList():
				self._recursivelyComputeCodeInfosOfStructureTree(cihldStructure)

		self._generateCodeInfosOfStructure(structure)

		structure.setCodeInfoGenerated()

	def _generateCodeInfosOfStructure(self, structure):
		structure.generateCodeInfos(self.codeInfoInterpreter)

class HanZiNetworkManager:
	@inject
	def __init__(self, hanziNetwork: HanZiNetwork):
		self.hanziNetwork = hanziNetwork

	def findNode(self, name):
		return self.hanziNetwork.findNode(name)

	def isWithNode(self, name):
		return self.hanziNetwork.isWithNode(name)

	def isNodeExpanded(self, name):
		return self.hanziNetwork.isNodeExpanded(name)

	def addNode(self, node):
		return self.hanziNetwork.addNode(node)

	def addStructureIntoNode(self, structure, nodeName):
		node = self.findNode(nodeName)
		node.addStructure(structure)
		if not structure.isUnit():
			node.setMainStructure(structure)

class HanZiNetworkItemFactory:
	@inject
	def __init__(self,
		networkManager: HanZiNetworkManager,
		operatorManager: OperatorManager,
		codeInfoInterpreter: CodeInfoInterpreter):
		self.networkManager = networkManager
		self.operatorManager = operatorManager
		self.wrapperExpressionDict = {}

	def touchNode(self, character):
		if not self.networkManager.isWithNode(character):
			node = self.generateNode(character)
			self.networkManager.addNode(node)
		return self.networkManager.findNode(character)

	def generateNode(self, character):
		tag = self._generateNodeTag(character)
		node = HanZiNode(character, tag)
		return node

	def _generateNodeTag(self, character):
		tag = CharacterInfo.CharacterInfo(character)
		return tag

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

	def getWrapperStructureByNodeName(self, nodeName, index=0):
		self.touchNode(nodeName)
		return self.getWrapperStructure(nodeName, index)

	def getWrapperStructure(self, name, index):
		wrapperExpression = (name, index)
		if (name, index) in self.wrapperExpressionDict:
			return self.wrapperExpressionDict[wrapperExpression]

		referenceNode = self.networkManager.findNode(name)
		structure = self.generateWrapperStructure(referenceNode, index)

		self.wrapperExpressionDict[wrapperExpression]=structure
		return structure

	def generateWrapperStructure(self, referenceNode, index):
		return self._generateWrapperStructure(referenceNode, index)

	def _generateUnitStructure(self, radixCodeInfo):
		structure = HanZiStructure()
		structure.setAsUnit(radixCodeInfo)
		return structure

	def _generateWrapperStructure(self, referenceNode, index):
		structure = HanZiStructure()
		structure.setAsWrapper(referenceNode, index)
		return structure

	def _generateCompoundStructure(self, operator, structureList):
		structure = HanZiStructure()
		structure.setAsCompound(operator, structureList)
		return structure

