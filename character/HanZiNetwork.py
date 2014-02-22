
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

#		for charName in charNameList:
#			dstDesc=self.get(charName)
#			srcDesc=self.charDescQueryer(charName)
#			dstDesc.setChInfo(copy.copy(srcDesc.getChInfo()))

	def addCharDesc(self, charName):
		dstDesc=self.charDescGenerator(charName)
		srcDesc=self.charDescQueryer(charName)

#		self.rearrangeRecursively(srcDesc)
		self.expandCharDescInNetwork(dstDesc, srcDesc)
#		self.charDescRearranger(charDesc)
		self.rearrangeRecursively(dstDesc)

		self.descNetwork[charName]=dstDesc

	def rearrangeRecursively(self, charDesc):
		self.charDescRearranger(charDesc)
		for childDesc in charDesc.getCompList():
			self.rearrangeRecursively(childDesc)

	def expandCharDescInNetwork(self, dstDesc, srcDesc):
		# 擴展 dstDesc
		# dstDesc 會被改變，而非產生新的 CharDesc

		dstDesc.copyDescriptionFrom(srcDesc)
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
				self.expandCharDescInNetwork(childDstDesc, childSrcDesc)

			else:
				if childSrcDesc.getName() in self.descNetwork:
					childDstDesc=self.descNetwork.get(childSrcDesc.getName())
				else:
					expandChildSrcDesc=self.charDescQueryer(childSrcDesc.getName())

					childDstDesc=self.charDescGenerator(expandChildSrcDesc.getName())

					self.expandCharDescInNetwork(childDstDesc, expandChildSrcDesc)
					self.descNetwork[childDstDesc.getName()]=childDstDesc

			compList.append(childDstDesc)
		dstDesc.setCompList(compList)

#		self.charDescRearranger(dstDesc)

