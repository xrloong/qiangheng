import copy
from state import StateManager

class HanZiStructure:
	def __init__(self, operator, nodeList):
		self.operator=operator
		self.nodeList=nodeList

		self.codeInfoList=[]

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

	def setByComps(self):
		if self.flagIsSet:
			return
		self.flagIsSet=True

		nodeList=self.nodeList
		infoListList=self.getAllCodeInfoList(nodeList)

		quantity=StateManager.getQuantity()

		if quantity==StateManager.STATE_QUANTITY_NONE:
			infoListList=[]
		elif quantity==StateManager.STATE_QUANTITY_FIRST:
			infoListList=infoListList[:1]
		elif quantity==StateManager.STATE_QUANTITY_ALL:
			infoListList=infoListList

		for infoList in infoListList:
			codeInfo=StateManager.codeInfoGenerator({})
			codeInfo.setByComps(self.getOperator(), infoList)
			self.appendCodeInfo(codeInfo)

	def getAllCodeInfoList(self, nodeList):
		def combineList(infoListList, infoListOfNode):
			if len(infoListList)==0:
				ansListList=[infoListOfNode]
			else:
				ansListList=[]
				for infoList in infoListList:
					for codeInfo in infoListOfNode:
						ansListList.append(infoList+[codeInfo])

#				ansListList=[infoList+[codeInfo] for infoList in infoListList for codeInfo in infoListOfNode]
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

	def getCodeList(self):
		self.setNodeTree()

		codeList=[]
		if self.isToShow:
			codeInfoList=self.getCodeInfoList()
			for codeInfo in codeInfoList:
				code=codeInfo.getCode()
				if code:
					codeList.append(code)
		return codeList

	def setNodeTree(self):
		"""設定某一個字符所包含的部件的碼"""

		structureList=self.getStructureListWithCondition()
		for structure in structureList:
			radixList=structure.getNodeList()
			for childNode in radixList:
				childNode.setNodeTree()

			structure.setByComps()

class HanZiNetwork:
	def __init__(self):
		self.nodeList=[]

		self.descNetwork={}
		self.srcDescNameToNodeDict={}

	def isInNetwork(self, srcDesc):
		srcName=srcDesc.getHybridName()
		return srcName in self.srcDescNameToNodeDict.keys()

	def addNode(self, charName, charDesc):
		ansNode=HanZiNode(charName)

		self.srcDescNameToNodeDict[charName]=ansNode

		return ansNode

	def addLink(self, charDesc, operator, childDescList):
		if len(childDescList)>0:
			childNodeList=[self.findNodeByCharDesc(childDesc) for childDesc in childDescList]
			dstNode=self.findNodeByCharDesc(charDesc)

			structure=HanZiStructure(operator, childNodeList)
			structure.setToRadix()

			dstNode.addStructure(structure)

	def appendNodeInfo(self, charDesc, propDict):
		dstNode=self.findNodeByCharDesc(charDesc)

		codeInfo=StateManager.codeInfoGenerator(propDict)
		structure=HanZiStructure(None, [])
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
			self.addNode(charName, charDesc)

		ansNode=self.findNodeByCharDesc(charDesc)
		return ansNode

	def getCodeList(self, charDesc):
		charNode=self.findNodeByCharDesc(charDesc)
		return charNode.getCodeList()
