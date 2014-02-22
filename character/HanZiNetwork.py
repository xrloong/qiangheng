
import copy
from .CharDesc import CharDesc

class HanZiStructure:
	def __init__(self, operator, nodeList, codeInfo):
		self.operator=operator
		self.nodeList=nodeList
		self.codeInfo=codeInfo

	def getOperator(self):
		return self.operator

	def getNodeList(self):
		return self.nodeList

	def getCodeInfo(self):
		return self.codeInfo

	def setCodeInfo(self, codeInfo):
		self.codeInfo=codeInfo

	def getCodeInfoList(self):
		return [self.codeInfo]

	def setStructure(self, operator, nodeList):
		self.operator=operator
		self.nodeList=nodeList

	def setByComps(self):
		codeInfo=self.getCodeInfo()
		nodeList=self.nodeList
		if not codeInfo.isToSetTree():
			return

		infoList=[node.getCodeInfoList()[0] for node in nodeList]
		codeInfo.setByComps(self.getOperator(), infoList)

class HanZiNode:
	def __init__(self, charName):
		self.structureList=[]
		self.charName=charName

		self.isToShow=len(charName)==1

	def addStructure(self, structure):
		self.structureList.append(structure)

	def getStructureListWithCondition(self):
#		return self.structureList[:1]
		return self.structureList

	def getCodeInfoList(self):
		structureList=self.getStructureListWithCondition()
		return sum(map(lambda s: s.getCodeInfoList(), structureList), [])

	def getCodeList(self):
		self.setNodeTree()

		codeList=[]
		if self.isToShow:
			structureList=self.getStructureListWithCondition()
			for struct in structureList:
				codeInfo=struct.getCodeInfo()
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
	def __init__(self, codeInfoGenerator):
		self.nodeList=[]

		self.descNetwork={}
		self.srcDescNameToNodeDict={}

		def emptyCodeInfoGenerator():
			return codeInfoGenerator({})

		self.emptyCodeInfoGenerator=emptyCodeInfoGenerator

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

			codeInfo=self.emptyCodeInfoGenerator()
			structure=HanZiStructure(operator, childNodeList, codeInfo)
			dstNode.addStructure(structure)

	def appendNodeInfo(self, charDesc, propDict):
		dstNode=self.findNodeByCharDesc(charDesc)
		codeInfo=self.emptyCodeInfoGenerator()
		codeInfo.setPropDict(propDict)
		structure=HanZiStructure(None, [], codeInfo)
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
