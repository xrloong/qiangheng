
import copy
from .CharDesc import CharDesc
class HanZiNetwork:
	def __init__(self, emptyCharInfoGenerator, charDescGenerator, charDescRearranger, charDescQueryer):
		self.descNetwork={}
		self.emptyCharInfoGenerator=emptyCharInfoGenerator
		self.charDescGenerator=charDescGenerator
		self.charDescRearranger=charDescRearranger
		self.charDescQueryer=charDescQueryer

	def get(self, key, defaultValue=None):
		return self.descNetwork.get(key, defaultValue)

	def constructHanZiNetwork(self, charNameList):
		for charName in charNameList:
			self.addCharDesc(charName)

	def getAllNode(self):
		# 目前未實作
		return None

	def findNodeByDescription(self, charDesc):
		# 目前即為傳入值
		return charDesc

	def addCharDesc(self, charName):
		srcDesc=self.charDescQueryer(charName)

#		self.rearrangeRecursively(srcDesc)
		dstDesc=self.expandCharDescInNetwork(srcDesc)
		self.rearrangeRecursively(dstDesc)

		self.descNetwork[charName]=dstDesc

	def rearrangeRecursively(self, charDesc):
		self.charDescRearranger(charDesc)
		for childDesc in charDesc.getCompList():
			self.rearrangeRecursively(childDesc)

	def expandCharDescInNetwork(self, srcDesc):
		# 擴展 dstDesc
		# dstDesc 會被改變，而非產生新的 CharDesc

		dstDesc=srcDesc.copyDescription()

		srcCharInfo=srcDesc.getChInfo()
		if srcCharInfo==None:
			dstDesc.setChInfo(self.emptyCharInfoGenerator())
		else:
			dstDesc.setChInfo(srcCharInfo)

		compList=[]
		for childSrcDesc in srcDesc.getCompList():
			if childSrcDesc.isAnonymous():
				# 若是為匿名結構，無法用名字查出結構，直接複製
				anonymousName=CharDesc.generateNewAnonymousName()
				childDstDesc=self.charDescGenerator(anonymousName)
				childDstDesc=self.expandCharDescInNetwork(childSrcDesc)

			else:
				if childSrcDesc.getName() in self.descNetwork:
					childDstDesc=self.descNetwork.get(childSrcDesc.getName())
				else:
					expandChildSrcDesc=self.charDescQueryer(childSrcDesc.getName())

					childDstDesc=self.charDescGenerator(expandChildSrcDesc.getName())

					childDstDesc=self.expandCharDescInNetwork(expandChildSrcDesc)
					self.descNetwork[childDstDesc.getName()]=childDstDesc

			compList.append(childDstDesc)
		dstDesc.setCompList(compList)

		return dstDesc

	def setCharTree(self, targetNode):
		"""設定某一個字符所包含的部件的碼"""

		radixList=targetNode.getCompList()
		for childNode in radixList:
			self.setCharTree(childNode)

		targetNode.setByComps(radixList)

	def getCode(self, charName):
		expandDesc=self.get(charName, None)

		targetNode=self.findNodeByDescription(expandDesc)
		self.setCharTree(targetNode)
		return targetNode.getCode()

