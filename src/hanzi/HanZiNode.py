from state import StateManager

class HanZiCodeInfo:
	def __init__(self, propDict, codeType,):
		codeInfo=StateManager.codeInfoGenerator(propDict)
		self.codeInfo=codeInfo
		self.codeInfo.multiCodeType(codeType)

		hasCharacter=bool("字符碼" in propDict)
		hasRadix=bool("字根碼" in propDict)
		if hasCharacter or hasRadix:
			self._isSupportCharacterCode=False
			self._isSupportRadixCode=False
			if hasCharacter:
				self._isSupportCharacterCode=True
			if hasRadix:
				self._isSupportRadixCode=True
		else:
			self._isSupportCharacterCode=True
			self._isSupportRadixCode=True

	def isSupportCharacterCode(self):
		return self._isSupportCharacterCode

	def isSupportRadixCode(self):
		return self._isSupportRadixCode

	def setRadixCodeProperties(self, propDict):
		self.codeInfo.setRadixCodeProperties(propDict)
		pass

	def setCompositions(self, operator, complist):
		tmpCompList=[comp.codeInfo for comp in complist]
		self.codeInfo.setCompositions(operator, tmpCompList)

	def getCodeType(self):
		return self.codeInfo.getCodeType()

	def getCodeProperties(self):
		return self.codeInfo.getCodeProperties()

class HanZiStructure:
	def __init__(self, codeType, operator, nodeList):
		self.operator=operator
		self.nodeList=nodeList

		self.codeInfoList=[]
		self.codeType=codeType

		self.flagIsSet=False

	def getNodeList(self):
		return self.nodeList

	def getCodeInfoList(self):
		return self.codeInfoList

	def setCompositions(self):
		def getAllCodeInfoList(nodeList):
			def combineList(infoListList, infoListOfNode):
				if len(infoListList)==0:
					ansListList=[]
					for codeInfo in infoListOfNode:
						ansListList.append([codeInfo])
				else:
					ansListList=[]
					for infoList in infoListList:
						for codeInfo in infoListOfNode:
							ansListList.append(infoList+[codeInfo])

				return ansListList

			infoListList=[]

			for node in nodeList:
				tmpCodeInfoList=node.getCodeInfoList()
				codeInfoList=filter(lambda x: x.isSupportRadixCode(), tmpCodeInfoList)
				infoListList=combineList(infoListList, codeInfoList)

			return infoListList


		if self.flagIsSet:
			return

		self.flagIsSet=True

		nodeList=self.nodeList
		infoListList=getAllCodeInfoList(nodeList)

		for infoList in infoListList:
			codeInfo=HanZiCodeInfo({}, self.codeType)
			codeInfo.setCompositions(self.operator, infoList)

			self.codeInfoList.append(codeInfo)

class HanZiTurtleStructure:
	def __init__(self, codeType, codeInfoProperties):
		codeInfo=HanZiCodeInfo(codeInfoProperties, codeType)

		self.codeInfoList=[codeInfo]
		self.codeType=codeType

	def getNodeList(self):
		return []

	def getCodeInfoList(self):
		return self.codeInfoList

	def setCompositions(self):
		pass

class HanZiWrapperStructure:
	def __init__(self, targetNode, expression):
		self.targetNode=targetNode
		self.expression=expression

	def getTargetNode(self):
		tempList=self.expression.split(".")
		if(len(tempList)>1):
			index=int(tempList[1])

			structList=self.targetNode.getStructureListWithCondition()
			struct=structList[0]
			nodeList=struct.getNodeList()

			return nodeList[index]
		else:
			return self.targetNode

	def getCodeInfoList(self):
		return self.getTargetNode().getCodeInfoList()

	def getNodeList(self):
		return [self.targetNode]

	def setCompositions(self):
		structList=self.targetNode.getStructureListWithCondition()
		struct=structList[0]
		struct.setCompositions()

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

	def getStructureListWithCondition(self):
		return self.structureList

	def getCodeInfoList(self):
		structureList=self.getStructureListWithCondition()

		return sum(map(lambda s: s.getCodeInfoList(), structureList), [])

	def getCodePropertiesList(self):
		self.setNodeTree()

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

	def printAllCodeInfoInStructure(self):
		structureList=self.getStructureListWithCondition()
		for struct in structureList:
			struct.printAllCodeInfo()

