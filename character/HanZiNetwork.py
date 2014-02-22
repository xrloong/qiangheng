
import copy
from .CharDesc import CharDesc

class HanZiStructure:
	def __init__(self, operator, nodeList, charInfo):
		self.operator=operator
		self.nodeList=nodeList
		self.charInfo=charInfo

	def getOperator(self):
		return self.operator

#	def setOperator(self, operator):
#		self.operator=operator

	def getNodeList(self):
		return self.nodeList

#	def setNodeList(self, nodeList):
#		self.nodeList=nodeList

	def getCharInfo(self):
		return self.charInfo

	def setCharInfo(self, charInfo):
		self.charInfo=charInfo

	def setStructure(self, operator, nodeList):
		self.operator=operator
		self.nodeList=nodeList

class HanZiNode:
	def __init__(self, charDesc, chInfo):
#		self.charDesc=charDesc
		self.flagExpanded=False

		self.structureX=HanZiStructure(charDesc.getOperator(), [], chInfo)
		self.structureList=[self.structureX]

		self.isToShow=charDesc.isToShow()

	def isExpanded(self):
		return self.flagExpanded

	def setExpanded(self, flag):
		self.flagExpanded=flag

	def setChInfo(self, charInfo):
		self.getStructure().setCharInfo(charInfo)

	def getChInfo(self):
		return self.getStructure().getCharInfo()

	def setStructure(self, operator, nodeList):
		self.getStructure().setStructure(operator, nodeList)

	def getStructure(self):
		return self.structureList[0]

	def getNodeList(self):
		return self.getStructure().getNodeList()

	def getOperator(self):
		return self.getStructure().getOperator()

	def getCode(self):
		chinfo=self.getChInfo()
		code=chinfo.getCode()
		if self.isToShow and code:
			return code
		else:
			return None

	def setByComps(self, charDescList):
		chInfo=self.getChInfo()
		if not chInfo.isToSetTree():
			return

		infoList=[x.getChInfo() for x in charDescList]
		chInfo.setByComps(self.getOperator(), infoList)

class HanZiNetwork:
	def __init__(self, emptyCharInfoGenerator, charDescQueryer):
		self.nodeList=[]

		self.descNetwork={}
		self.srcDescNameToNodeDict={}

		self.emptyCharInfoGenerator=emptyCharInfoGenerator
		self.charDescQueryer=charDescQueryer

	def constructHanZiNetwork(self, charNameList):
		sortedNameList=sorted(charNameList)

		for charName in sortedNameList:
			srcDesc=self.charDescQueryer(charName)
			self.recursivelyAddNode(srcDesc)

		for charName in sortedNameList:
			srcDesc=self.charDescQueryer(charName)
			self.recursivelyAddLink(srcDesc)

		for charName in sortedNameList:
			srcDesc=self.charDescQueryer(charName)
			dstNode=self.addOrFindNodeByCharDesc(srcDesc)

			chInfo=srcDesc.getChInfo()
			if chInfo==None:
				chInfo=self.emptyCharInfoGenerator()
			dstNode.setChInfo(chInfo)

	def recursivelyAddNode(self, srcDesc):
		dstNode=self.addOrFindNodeByCharDesc(srcDesc)

		for childSrcDesc in srcDesc.getCompList():
			self.recursivelyAddNode(childSrcDesc)

		dstCharInfo=self.emptyCharInfoGenerator()
		dstNode.setChInfo(dstCharInfo)


	def recursivelyAddLink(self, srcDesc):
		dstNode=self.addOrFindNodeByCharDesc(srcDesc)

		childNodeList=[]
		for childSrcDesc in srcDesc.getCompList():
			childNode=self.addOrFindNodeByCharDesc(childSrcDesc)
			childNodeList.append(childNode)

		if len(childNodeList)>0:
			operator=srcDesc.getOperator()
			dstNode.setStructure(operator, childNodeList)

		for childSrcDesc in srcDesc.getCompList():
			self.recursivelyAddLink(childSrcDesc)

	def isInNetwork(self, srcDesc):
		srcName=srcDesc.getName()
		return srcName in self.srcDescNameToNodeDict.keys()

	def addOrFindNodeByCharDesc(self, charDesc):
		ansNode=None
		charName=charDesc.getName()
		if not self.isInNetwork(charDesc):
			self.addNode(charName, charDesc)

		ansNode=self.findNodeByName(charName)
		return ansNode

	def addNode(self, charName, charDesc):
		dstDesc=charDesc.copyDescription()

		chInfo=charDesc.getChInfo()
		if chInfo==None:
			chInfo=self.emptyCharInfoGenerator()

		ansNode=HanZiNode(dstDesc, chInfo)

		self.srcDescNameToNodeDict[charName]=ansNode

		return ansNode

	def findNodeByName(self, charName):
		return self.srcDescNameToNodeDict.get(charName)

	def findNodeByCharDesc(self, charDesc):
		return self.findNodeByName(charDesc.getName())

	def setNodeTree(self, targetNode):
		"""設定某一個字符所包含的部件的碼"""

		radixList=targetNode.getNodeList()
		for childNode in radixList:
			self.setNodeTree(childNode)

		targetNode.setByComps(radixList)

	def getCode(self, charName):
		charNode=self.findNodeByName(charName)
		self.setNodeTree(charNode)
		return charNode.getCode()

