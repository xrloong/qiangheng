import copy
from state import StateManager
from description.CodeType import CodeType

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
		return self.codeInfoList.append(codeInfo)

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
	def __init__(self, charName):
		self.structureList=[]
		self.charName=charName

		self.isToShow=len(charName)==1

	def addStructure(self, structure):
		self.structureList.append(structure)

	def getStructureListWithCondition(self):
		return self.structureList

	def getCodeInfoList(self):
		structureList=self.getStructureListWithCondition()
		return sum(map(lambda s: s.getCodeInfoList(), structureList), [])

	def getCodePropertiesList(self):
		self.setNodeTree()

		codeList=[]
		if self.isToShow:
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

class DescriptionManagerToHanZiNetworkConverter:
	def __init__(self, descriptionManager, hanziNetwork, targetCharacterList):
		self.descriptionManager=descriptionManager
		self.hanziNetwork=hanziNetwork
		self.targetCharacterList=targetCharacterList

	def run(self):
		self.constructDescriptionNetwork(self.targetCharacterList)

	def constructDescriptionNetwork(self, targetCharacterList):
		charNameList=targetCharacterList
		hanziNetwork=self.hanziNetwork
		sortedNameList=sorted(charNameList)

		for charName in sortedNameList:
			hanziNetwork.addNode(charName)

		for charName in sortedNameList:
			charDesc=self.queryDescription(charName)
			structDescList=charDesc.getStructureList()
			for structDesc in structDescList:
				self.recursivelyAddNode(structDesc)

		for charName in sortedNameList:
			charDesc=self.queryDescription(charName)
			structDescList=charDesc.getStructureList()
			for structDesc in structDescList:
				if structDesc.isTurtle():
					hanziNetwork.appendTurtleStruct(structDesc)
				else:  
					self.recursivelyAddLink(structDesc)


	def recursivelyAddNode(self, srcDesc):
		self.hanziNetwork.addOrFindNodeByCharDesc(srcDesc)

		for childSrcDesc in srcDesc.getCompList():
			self.recursivelyAddNode(childSrcDesc)

	def recursivelyAddLink(self, structDesc):
		operator=structDesc.getOperator()
		childDescList=structDesc.getCompList()

		self.hanziNetwork.addLink(structDesc, operator, childDescList)

		for childSrcDesc in structDesc.getCompList():
			self.recursivelyAddLink(childSrcDesc)

	def queryDescription(self, characterName):
		return self.descriptionManager.queryCharacterDescription(characterName)



class HanZiNetwork:
	def __init__(self):
		self.nodeList=[]

		self.descNetwork={}
		self.srcDescNameToNodeDict={}

	def construct(self, descriptionManager, targetCharacterList):
		toHanZiNetworkConverter=DescriptionManagerToHanZiNetworkConverter(descriptionManager, self, targetCharacterList)
		toHanZiNetworkConverter.run()

	def isInNetwork(self, srcDesc):
		srcName=srcDesc.getHybridName()
		return srcName in self.srcDescNameToNodeDict.keys()

	def addNode(self, charName):
		ansNode=HanZiNode(charName)

		self.srcDescNameToNodeDict[charName]=ansNode

		return ansNode

	def addLink(self, structDesc, operator, childDescList):
		if len(childDescList)>0:
			childNodeList=[self.findNodeByCharDesc(childDesc) for childDesc in childDescList]
			dstNode=self.findNodeByCharDesc(structDesc)

			codeType=structDesc.getCodeType()
			structure=HanZiStructure(codeType, operator, childNodeList)
			structure.setToRadix()

			dstNode.addStructure(structure)

	def appendTurtleStruct(self, structDesc):
		dstNode=self.findNodeByCharDesc(structDesc)

		codeType=structDesc.getCodeType()

		codeInfoProperties=structDesc.getCodeInfoDict()

		codeType=structDesc.getCodeType()
		structure=HanZiStructure(codeType, None, [])

		codeInfo=HanZiCodeInfo(codeInfoProperties, codeType)
		structure.appendCodeInfo(codeInfo)

		structure.setToComponent()

		dstNode.addStructure(structure)

	def findNodeByCharDesc(self, charDesc):

		hybridName=charDesc.getHybridName()
		return self.srcDescNameToNodeDict.get(hybridName)

	def addOrFindNodeByCharDesc(self, charDesc):
		ansNode=None
		charName=charDesc.getHybridName()
		if not self.isInNetwork(charDesc):
			self.addNode(charName)

		ansNode=self.findNodeByCharDesc(charDesc)
		return ansNode

	def getCodePropertiesList(self, charName):
		charNode=self.srcDescNameToNodeDict.get(charName)
		return charNode.getCodePropertiesList()

