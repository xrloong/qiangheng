from injector import inject

from .network import HanZiNetworkNodeFinder
from .network import HanZiStructure, HanZiNode
from .item import StructureUnitTag, StructureWrapperTag, StructureAssemblageTag
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
		codeInfoList=sum(map(lambda s: s.getTag().getCodeInfoList(), structureList), [])
		codeInfoList=filter(lambda x: x.isSupportCharacterCode(), codeInfoList)

		codeList=self.codeInfoInterpreter.interpretCodeInfoList(codeInfoList)

		characterInfo=hanziNode.getTag()
		characterInfo.setCodeList(codeList)

		return characterInfo

class HanZiProcessor:
	@inject
	def __init__(self):
		pass

	def computeCodeInfosOfNodeTree(self, node):
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
			self._recursivelyComputeCodeInfosOfNodeTree(structure.getReferenceNode())
		elif structure.isCompound():
			for cihldStructure in structure.getStructureList():
				self._recursivelyComputeCodeInfosOfStructureTree(cihldStructure)

		self._generateCodeInfosOfStructure(structure)

		structure.setCodeInfoGenerated()

	def _generateCodeInfosOfStructure(self, structure):
		structure.generateCodeInfos()

class StructureFactory:
	@inject
	def __init__(self, nodeFinder: HanZiNetworkNodeFinder,
		operatorManager: OperatorManager,
		codeInfoInterpreter: CodeInfoInterpreter):
		self.nodeFinder = nodeFinder
		self.operatorManager = operatorManager
		self.codeInfoInterpreter = codeInfoInterpreter
		self.wrapperExpressionDict = {}

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

	def getWrapperStructure(self, name, index=0):
		wrapperExpression = (name, index)
		if (name, index) in self.wrapperExpressionDict:
			return self.wrapperExpressionDict[wrapperExpression]

		structure = self.generateWrapperStructure(name, index)

		self.wrapperExpressionDict[wrapperExpression]=structure
		return structure

	def generateWrapperStructure(self, name, index):
		return self._generateWrapperStructure(name, index)

	def _generateUnitStructure(self, radixCodeInfo):
		tag = StructureUnitTag(radixCodeInfo)
		structure = HanZiStructure(tag)
		return structure

	def _generateWrapperStructure(self, referenceName, index):
		tag = StructureWrapperTag(referenceName, index)

		referenceNode = self.nodeFinder.findNode(referenceName)

		structure = HanZiStructure(tag)
		structure.setAsWrapper(referenceNode, index)
		return structure

	def _generateCompoundStructure(self, operator, structureList):
		tag = StructureAssemblageTag(self.codeInfoInterpreter)

		structure = HanZiStructure(tag)
		structure.setAsCompound(operator, structureList)
		return structure

