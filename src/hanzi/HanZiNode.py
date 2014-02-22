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

		self.flagIsSet=True

	def setToRadix(self):
		self.flagIsSet=False

	def setToComponent(self):
		pass

	def getOperator(self):
		return self.operator

	def getNodeList(self):
		return self.nodeList

	def appendCodeInfo(self, codeInfo):
		self.codeInfoList.append(codeInfo)

	def getCodeInfoList(self):
		return self.codeInfoList

	def setStructure(self, operator, nodeList):
		self.operator=operator
		self.nodeList=nodeList

	def setCompositions(self):
		if self.flagIsSet:
			return
		self.flagIsSet=True

		nodeList=self.nodeList
		infoListList=self.getAllCodeInfoList(nodeList)

		for infoList in infoListList:
			codeInfo=HanZiCodeInfo({}, self.codeType)
			codeInfo.setCompositions(self.getOperator(), infoList)

			self.appendCodeInfo(codeInfo)

	def getAllCodeInfoList(self, nodeList):
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

class HanZiNode:
	def __init__(self, name):
		self.name=name
		self.structureList=[]

	def getName(self):
		return self.name

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

class HanZiWrapperNode:
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

	def getName(self):
		return self.getTargetNode().getName()

#	def addStructure(self, structure):
#		self.getTargetNode().addStructure(structure)

#	def setStructureList(self, structureList):
#		self.getTargetNode().setStructureList(structureList)

	def getStructureListWithCondition(self):
		return self.getTargetNode().getStructureListWithCondition()

	def getCodeInfoList(self):
		return self.getTargetNode().getCodeInfoList()

	def getCodePropertiesList(self):
		return self.getTargetNode().getCodePropertiesList()

	def setNodeTree(self):
		return self.getTargetNode().setNodeTree()


