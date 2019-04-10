from injector import inject

from .network import HanZiNetworkNodeFinder
from .network import HanZiStructure, HanZiNode
from .item import StructureUnitTag, StructureWrapperTag, StructureAssemblageTag
from model.interpreter import CodeInfoInterpreter
from model.element import CharacterInfo

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

		self._computeCodeInfosOfUnitStructuresOfNode(node)

		structure=node.getStructure()
		self._recursivelyComputeCodeInfosOfStructureTree(structure)

	def _computeCodeInfosOfUnitStructuresOfNode(self, node):
		structureList=node.getUnitStructureList()
		for structure in structureList:
			self._computeCodeInfosOfStructure(structure)

	def _recursivelyComputeCodeInfosOfStructureTree(self, structure):
		if not structure:
			return

		tag=structure.getTag()
		if tag.isCodeInfoGenerated():
			return

		for cihldStructure in structure.getStructureList():
			self._recursivelyComputeCodeInfosOfStructureTree(cihldStructure)
		self.generateCodeInfosOfStructure(structure)

		tag.setCodeInfoGenerated()

	def _computeCodeInfosOfStructure(self, structure):
		tag=structure.getTag()
		if tag.isCodeInfoGenerated():
			return

		self.generateCodeInfosOfStructure(structure)

	def generateCodeInfosOfStructure(self, structure):
		structure.generateCodeInfos()

class StructureFactory:
	@inject
	def __init__(self, nodeFinder: HanZiNetworkNodeFinder,
		codeInfoInterpreter: CodeInfoInterpreter):
		self.nodeFinder = nodeFinder
		self.codeInfoInterpreter = codeInfoInterpreter
		self.wrapperExpressionDict = {}

	def generateNode(self, character):
		tag = self._generateNodeTag(character)
		node = HanZiNode(character, tag)
		return node

	def _generateNodeTag(self, character):
		tag = CharacterInfo.CharacterInfo(character)
		return tag

	def generateUnitStructure(self, radixCodeInfo):
		return self._generateUnitStructure(radixCodeInfo)

	def generateAssemblageStructure(self, operator, structureList):
		return self._generateCompoundStructure(operator, structureList)

	def generateWrapperStructure(self, name, index=0):
		if (name, index) in self.wrapperExpressionDict:
			return self.wrapperExpressionDict[(name, index)]

		structure = self._generateWrapperStructure(name, index)

		self.wrapperExpressionDict[(name, index)]=structure
		return structure

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

