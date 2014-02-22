import copy
from state import StateManager
from description.CodeType import CodeType

class HanZiStructure:
	def __init__(self, operator, nodeList):
		self.operator=operator
		self.nodeList=nodeList

		self.codeInfoList=[]
		self.codeType=CodeType()

		self.flagIsSet=True

	def setCodeType(self, codeType):
		self.codeType=codeType

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
			codeInfo=StateManager.codeInfoGenerator({})
			codeInfo.setCompositions(self.getOperator(), infoList)
			codeInfo.multiCodeType(self.codeType)

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
			infoListList=combineList(infoListList, node.getCodeInfoList())

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
			codeInfoList=self.getCodeInfoList()
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

			structure=HanZiStructure(operator, childNodeList)
			structure.setCodeType(structDesc.getCodeType())
			structure.setToRadix()

			dstNode.addStructure(structure)

	def appendNodeInfo(self, structDesc, propDict):
		dstNode=self.findNodeByCharDesc(structDesc)

		codeInfo=StateManager.codeInfoGenerator(propDict)
		structure=HanZiStructure(None, [])
		structure.appendCodeInfo(codeInfo)
		structure.setCodeType(structDesc.getCodeType())
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

