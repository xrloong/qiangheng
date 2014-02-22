
import copy
from .CharDesc import CharDesc

class HanZiStructure:
	def __init__(self, operator, nodeList, charInfo):
		self.operator=operator
		self.nodeList=nodeList
		self.charInfo=charInfo

	def getOperator(self):
		return self.operator

	def getNodeList(self):
		return self.nodeList

	def getCharInfo(self):
		return self.charInfo

	def setCharInfo(self, charInfo):
		self.charInfo=charInfo

	def getCharInfoList(self):
		return [self.charInfo]

	def setStructure(self, operator, nodeList):
		self.operator=operator
		self.nodeList=nodeList

	def setByComps(self):
		chInfo=self.getCharInfo()
		nodeList=self.nodeList
		if not chInfo.isToSetTree():
			return

		infoList=[node.getCharInfoList()[0] for node in nodeList]
		chInfo.setByComps(self.getOperator(), infoList)

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

	def getCharInfoList(self):
		structureList=self.getStructureListWithCondition()
		return sum(map(lambda s: s.getCharInfoList(), structureList), [])

	def getCodeList(self):
		self.setNodeTree()

		codeList=[]
		if self.isToShow:
			structureList=self.getStructureListWithCondition()
			for struct in structureList:
				chinfo=struct.getCharInfo()
				code=chinfo.getCode()
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
	def __init__(self, charInfoGenerator):
		self.nodeList=[]

		self.descNetwork={}
		self.srcDescNameToNodeDict={}

		def emptyCharInfoGenerator():
			return charInfoGenerator({})

		self.emptyCharInfoGenerator=emptyCharInfoGenerator

	def isInNetwork(self, srcDesc):
		srcName=srcDesc.getHybridName()
		return srcName in self.srcDescNameToNodeDict.keys()

	def addNode(self, charName, charDesc):
		ansNode=HanZiNode(charName)

		srcPropDict=charDesc.getPropDict()
		if srcPropDict:
			chInfo=self.emptyCharInfoGenerator()
			chInfo.setPropDict(srcPropDict)
			structure=HanZiStructure(None, [], chInfo)
			ansNode.addStructure(structure)

		self.srcDescNameToNodeDict[charName]=ansNode

		return ansNode

	def addLink(self, charDesc, operator, childDescList):
		if len(childDescList)>0:
			childNodeList=[self.findNodeByCharDesc(childDesc) for childDesc in childDescList]
			dstNode=self.findNodeByCharDesc(charDesc)

			chInfo=self.emptyCharInfoGenerator()
			structure=HanZiStructure(operator, childNodeList, chInfo)
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
