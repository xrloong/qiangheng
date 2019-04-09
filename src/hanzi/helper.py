from injector import inject

from . import HanZiNetwork
from .item import StructureUnitTag, StructureWrapperTag, StructureAssemblageTag
from model.interpreter import CodeInfoInterpreter

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
		structure.generateCodeInfos()

		tag.setCodeInfoGenerated()

	def _computeCodeInfosOfStructure(self, structure):
		tag=structure.getTag()
		if tag.isCodeInfoGenerated():
			return

		structure.generateCodeInfos()

class StructureFactory:
	@inject
	def __init__(self, hanziNetwork: HanZiNetwork,
		codeInfoInterpreter: CodeInfoInterpreter):
		self.hanziNetwork = hanziNetwork
		self.codeInfoInterpreter = codeInfoInterpreter

	def generateUnitStructure(self, radixCodeInfo):
		tag = self._generateUnitTag(radixCodeInfo)
		structure=self.hanziNetwork.generateStructure(tag)
		return structure

	def generateAssemblageStructure(self, operator, structureList):
		tag = self._generateAssemblageTag()
		structure = self.hanziNetwork.generateStructure(tag, compound=[operator, structureList])
		return structure

	def generateWrapperStructure(self, name, index=0):
		tag = self._generateWrapperTag(name, index)
		structure = self.hanziNetwork.generateStructure(tag, reference=[name, index])
		return structure

	def _generateUnitTag(self, radixCodeInfo):
		return StructureUnitTag(radixCodeInfo)

	def _generateWrapperTag(self, name, index):
		return StructureWrapperTag(name, index)

	def _generateAssemblageTag(self):
		return StructureAssemblageTag(self.codeInfoInterpreter)

