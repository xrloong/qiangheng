import copy
from state import StateManager
from description.CodeType import CodeType

class HanZiCodeInfo:
	def __init__(self, propDict, codeType, _isSupportCharacterCode=True, _isSupportRadixCode=True):
		codeInfo=StateManager.codeInfoGenerator(propDict)
		self.codeInfo=codeInfo
		self.codeInfo.multiCodeType(codeType)

		self._isSupportCharacterCode=_isSupportCharacterCode
		self._isSupportRadixCode=_isSupportRadixCode

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

class HanZiNetwork:
	def __init__(self):
		self.nodeList=[]

		self.descNetwork={}
		self.srcDescNameToNodeDict={}

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

		codeInfo=HanZiCodeInfo(codeInfoProperties, codeType, True, False)
		structure.appendCodeInfo(codeInfo)
		codeInfo=HanZiCodeInfo(codeInfoProperties, codeType, False, True)
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

