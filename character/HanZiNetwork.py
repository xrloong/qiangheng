
from .CharDesc import CharDesc
class HanZiNetwork:
	def __init__(self, charDescGenerator, charDescRearranger, charDescQueryer):
		self.descNetwork={}
		self.charDescGenerator=charDescGenerator
		self.charDescRearranger=charDescRearranger
		self.charDescQueryer=charDescQueryer

	def get(self, key, defaultValue=None):
		return self.descNetwork.get(key, defaultValue)

	def addCharDesc(self, charName):
		charDesc=self.charDescGenerator(charName)
		srcDesc=self.charDescQueryer(charName)

#		self.operatorMgr.rearrangeDesc(srcDesc)

		self.expandCharDescInNetwork(charDesc, srcDesc)
		self.descNetwork[charName]=charDesc

	def expandCharDescInNetwork(self, dstDesc, srcDesc):
		# 擴展 dstDesc
		# dstDesc 會被改變，而非產生新的 CharDesc

		if not srcDesc.getOperator().isAvailableOperation():
			print("<!-- 錯誤；不合法的運算 %s -->"%operator)
			return None

		dstDesc.copyInfoWithoutCompListFrom(srcDesc)

		compList=[]
		for childSrcDesc in srcDesc.getCompList():
			if childSrcDesc.isAnonymous():
				# 若是為匿名結構，無法用名字查出結構，直接複製
				anonymousName=CharDesc.generateNewAnonymousName()
				childDstDesc=self.charDescGenerator(anonymousName)
				self.expandCharDescInNetwork(childDstDesc, childSrcDesc)

			else:
				if childSrcDesc.name in self.descNetwork:
					childDstDesc=self.descNetwork.get(childSrcDesc.name)
				else:
					expandChildSrcDesc=self.charDescQueryer(childSrcDesc.name)

					childDstDesc=self.charDescGenerator(expandChildSrcDesc.name)

					self.expandCharDescInNetwork(childDstDesc, expandChildSrcDesc)
					self.descNetwork[childDstDesc.name]=childDstDesc

			compList.append(childDstDesc)
		dstDesc.setCompList(compList)

		self.charDescRearranger(dstDesc)

