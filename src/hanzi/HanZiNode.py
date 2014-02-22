from . import HanZiStructure

class HanZiNode:
	def __init__(self, name, characterProperty=None):
		self.name=name
		self.structureList=[]
		self.characterProperty=characterProperty

	def getName(self):
		return self.name

	def getCharacterProperty(self):
		return self.characterProperty

	def addStructure(self, structure):
		self.structureList.append(structure)

	def setStructureList(self, structureList):
		self.structureList=structureList

	def getStructureList(self):
		return self.structureList

	def getStructureListWithCondition(self):
		return self.structureList

	def getSubNodeList(self, index):
		subNodeList=[]
		for structure in self.structureList:
			if isinstance(structure, HanZiStructure.HanZiAssemblageStructure):
				nodeList=structure.getNodeList()
				subNode=nodeList[index]
				subNodeList.append(subNode)
		return subNodeList

	def getSubStructureList(self, index):
		subStructureList=[]
		subNodeList=self.getSubNodeList(index)
		for subNode in subNodeList:
			structureList=subNode.getStructureListWithCondition()
			subStructureList.extend(structureList)
		return subStructureList

	def getCodeInfoList(self):
		structureList=self.getStructureListWithCondition()

		return sum(map(lambda s: s.getCodeInfoList(), structureList), [])

	def getCodePropertiesList(self):
		codeList=[]
		tmpCodeInfoList=self.getCodeInfoList()
		codeInfoList=filter(lambda x: x.isSupportCharacterCode(), tmpCodeInfoList)
		for codeInfo in codeInfoList:
			codeProp=codeInfo.getCodeProperties()
			if codeProp:
				codeList.append(codeProp)

		return codeList

	def setNodeTree(self):
		"""設定某一個字符所包含的部件的碼"""

		structureList=self.getStructureListWithCondition()

		for structure in structureList:
			radixList=structure.getNodeList()
			for childNode in radixList:
				childNode.setNodeTree()

			structure.setCompositions()

	def setCompositions(self):
		self.setNodeTree()

	def printAllCodeInfoInStructure(self):
		structureList=self.getStructureListWithCondition()
		for struct in structureList:
			struct.printAllCodeInfo()

