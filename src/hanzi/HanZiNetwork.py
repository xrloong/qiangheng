import copy
from state import StateManager
from description.CodeType import CodeType
from description.operator import Operator

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
	def __init__(self, targetNode):
		self.targetNode=targetNode

	def addStructure(self, structure):
		self.targetNode.addStructure(structure)

	def setStructureList(self, structureList):
		self.targetNode.setStructureList(structureList)

	def getStructureListWithCondition(self):
		return self.targetNode.getStructureListWithCondition()

	def getCodeInfoList(self):
		return self.targetNode.getCodeInfoList()

	def getCodePropertiesList(self):
		return self.targetNode.getCodePropertiesList()

	def setNodeTree(self):
		return self.targetNode.setNodeTree()

class DescriptionManagerToHanZiNetworkConverter:
	def __init__(self, descriptionManager):
		self.descriptionManager=descriptionManager
		self.hanziNetwork=HanZiNetwork()

	def constructDescriptionNetwork(self):
		charNameList=self.descriptionManager.getAllCharacters()
		sortedNameList=sorted(charNameList)

		for charName in sortedNameList:
			self.hanziNetwork.addNamedNode(charName)

		for charName in sortedNameList:
			charDesc=self.queryDescription(charName)

			structDescList=charDesc.getStructureList()
			for structDesc in structDescList:
				structDesc.setRootName(charName)
				self.recursivelyAddStructure(structDesc)
		return self.hanziNetwork

	def recursivelyAddStructure(self, structDesc):
		hanziNetwork=self.hanziNetwork

		if structDesc.isLeaf():
			hanziNetwork.addReferenceNode(structDesc)
		elif structDesc.isTurtle():
			hanziNetwork.addTurtleStruct(structDesc)
		else:
			hanziNetwork.addNode(structDesc)
			operator=structDesc.getOperator()
			childDescList=structDesc.getCompList()

			for childSrcDesc in childDescList:
				self.recursivelyAddStructure(childSrcDesc)

			hanziNetwork.addLink(structDesc, operator, childDescList)

	def queryDescription(self, characterName):
		return self.descriptionManager.queryCharacterDescription(characterName)



class HanZiNetwork:
	def __init__(self):
		self.nodeList=[]

		self.structDescUniqueNameToNodeDict={}
		self.structDescExpandNameToNodeDict={}

	@staticmethod
	def construct(descriptionManager):
		toHanZiNetworkConverter=DescriptionManagerToHanZiNetworkConverter(descriptionManager)
		return toHanZiNetworkConverter.constructDescriptionNetwork()

	def addNamedNode(self, name):
		tmpNode=HanZiNode(name)
		self.structDescUniqueNameToNodeDict[name]=tmpNode
		self.structDescExpandNameToNodeDict[name]=tmpNode

	def addNode(self, structDesc):
		anonymousName=structDesc.getUniqueName()
		if anonymousName not in self.structDescUniqueNameToNodeDict:
			tmpNode=HanZiNode(anonymousName)
			self.structDescUniqueNameToNodeDict[anonymousName]=tmpNode

	def addReferenceNode(self, structDesc):
		anonymousName=structDesc.getUniqueName()
		if anonymousName not in self.structDescUniqueNameToNodeDict:
			rootNode=self.structDescExpandNameToNodeDict.get(structDesc.getReferenceName())
			tmpNode=HanZiWrapperNode(rootNode)
			self.structDescUniqueNameToNodeDict[anonymousName]=tmpNode

	def addTurtleStruct(self, structDesc):
		self.addNode(structDesc)

		dstNode=self.findNode(structDesc)

		codeType=structDesc.getCodeType()

		codeInfoProperties=structDesc.getCodeInfoDict()

		codeType=structDesc.getCodeType()
		structure=HanZiStructure(codeType, None, [])

		codeInfo=HanZiCodeInfo(codeInfoProperties, codeType)
		structure.appendCodeInfo(codeInfo)

		structure.setToComponent()

		dstNode.addStructure(structure)

	def addLink(self, structDesc, operator, childDescList):
		if len(childDescList)>0:
			childNodeList=[self.findNode(childDesc) for childDesc in childDescList]
			dstNode=self.findNode(structDesc)

			codeType=structDesc.getCodeType()
			structure=HanZiStructure(codeType, operator, childNodeList)
			structure.setToRadix()

			dstNode.addStructure(structure)

	def findNode(self, structDesc):
		if structDesc.isRoot():
			return self.structDescExpandNameToNodeDict.get(structDesc.getRootName())
		elif structDesc.isLeaf():
			return self.structDescUniqueNameToNodeDict.get(structDesc.getUniqueName())
		else:
			return self.structDescUniqueNameToNodeDict.get(structDesc.getUniqueName())

	def getCodePropertiesList(self, charName):
		charNode=self.structDescExpandNameToNodeDict.get(charName)
		return charNode.getCodePropertiesList()

