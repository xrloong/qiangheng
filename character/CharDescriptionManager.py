#!/usr/bin/env python3

from .CharDesc import CharDesc
from .CharInfo import CharInfo
from .RearrangementManager import RearrangementManager

class CharDescriptionManager:
	NoneInfo=CharInfo('[瑲珩預設]', [])
	NoneDesc=CharDesc("", '龜', [], '+', '(龜)', NoneInfo)

	def __init__(self, CharInfoGenerator):
		# descDB 放最原始、沒有擴展過的 CharDesc ，也就是從檔案讀出來的資料。
		# descNetwork 放擴展過的，且各個 CharDesc 可能會彼此參照。
		# 但 descNetwork 跟 descDB 則是完全獨立。
		# 在使用 descNetwork 前，要先呼叫 ConstructDescriptionNetwork()
		# ConstructDescriptionNetwork() 會從 descDB 建立 descNetwork
		self.descDB={}
		self.descNetwork={}

		def CharDescGenerator(charName, structInfo=['龜', [], '(龜)']):
			operator, CompList, expression=structInfo
			direction=RearrangementManager.computeDirection(operator)
			tmpCharInfo=CharInfoGenerator(charName, [])
			charDesc=CharDesc(charName, operator, CompList, direction, expression, tmpCharInfo)
			return charDesc

		def emptyCharInfoGenerator():
			return CharInfoGenerator("[瑲珩預設]", [])

		def emptyCharDescGenerator():
			anonymousName=CharDesc.generateNewAnonymousName()
			return CharDescGenerator(anonymousName)

		self.rearrangeMgr=RearrangementManager(emptyCharDescGenerator)

		self.charInfoGenerator=CharInfoGenerator
		self.charDescGenerator=CharDescGenerator
		self.emptyCharInfoGenerator=emptyCharInfoGenerator
		self.emptyCharDescGenerator=emptyCharDescGenerator

	def __getitem__(self, key):
		return self.descDB[key]

	def __setitem__(self, key, value):
		self.descDB[key]=value

	def keys(self):
		return self.descDB.keys()

	def getCharInfoGenerator(self):
		return self.charInfoGenerator

	def getCharDescGenerator(self):
		return self.charDescGenerator

	def getEmptyCharInfoGenerator(self):
		return self.emptyCharInfoGenerator

	def getEmptyCharDescGenerator(self):
		return self.emptyCharDescGenerator

	@staticmethod
	def getNoneInfo():
		return CharDescriptionManager.NoneInfo

	@staticmethod
	def getNoneDescription():
		return CharDescriptionManager.NoneDesc

	def ConstructDescriptionNetwork(self):
		for charName in self.descDB.keys():
			if charName not in self.descNetwork:
				charDesc=self.charDescGenerator(charName)
				self.expandCharDescInNetwork(charDesc, self.descDB.get(charName))
				self.descNetwork[charName]=charDesc

	def expandCharDescInNetwork(self, dstDesc, srcDesc):
		# 擴展 dstDesc
		# dstDesc 會被改變，而非產生新的 CharDesc
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
					expandChildSrcDesc=self.descDB.get(childSrcDesc.name)

					childDstDesc=self.charDescGenerator(expandChildSrcDesc.name)

					self.expandCharDescInNetwork(childDstDesc, expandChildSrcDesc)
					self.descNetwork[childDstDesc.name]=childDstDesc

			compList.append(childDstDesc)
		dstDesc.setCompList(compList)

		self.rearrangeMgr.rearrangeDesc(dstDesc)

	def getExpandDescriptionByNameInNetwork(self, charName):
		return self.descNetwork.get(charName, None)

	@staticmethod
	def setCharTree(charDesc):
		"""設定某一個字符所包含的部件的碼"""

		chInfo=charDesc.getChInfo()
		if not chInfo.isToSetTree():
			return

		radixList=charDesc.getCompList()
		for tmpdesc in radixList:
			CharDescriptionManager.setCharTree(tmpdesc)

		infoList=[x.getChInfo() for x in radixList]
		chInfo.setByComps(infoList, charDesc.getDirection())

if __name__=='__main__':
	pass

