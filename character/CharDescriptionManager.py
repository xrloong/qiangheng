#!/usr/bin/env python3

from .CharDesc import CharDesc
from .RearrangementManager import RearrangementManager

class CharDescriptionManager:
	NoneDesc=CharDesc("", '龜', [], '+', '(龜)')

	def __init__(self, CharInfoGenerator):
		# descDB 放最原始、沒有擴展過的 CharDesc ，也就是從檔案讀出來的資料。
		# descNetwork 放擴展過的，且各個 CharDesc 可能會彼此參照。
		# 但 descNetwork 跟 descDB 則是完全獨立。
		# 在使用 descNetwork 前，要先呼叫 ConstructDescriptionNetwork()
		# ConstructDescriptionNetwork() 會從 descDB 建立 descNetwork
		self.descDB={}
		self.descNetwork={}

		def AnonymouseCharInfoGenerator():
			return CharInfoGenerator("XXXX", [])

		def generateAnonymousDescription():
			anonymousName=CharDesc.generateNewAnonymousName()
			return CharDescriptionManager.generateDescription(anonymousName)

		# charInfoGenerator 會產生新的 CharInfo (不同的輸入法有相對應的 CharInfo) 。
		# charDescGenerator 會產生新的 CharDesc ，可自動加上匿名。
		anonymousCharInfoGenerator=AnonymouseCharInfoGenerator
		charInfoGenerator=CharInfoGenerator
		charDescGenerator=generateAnonymousDescription

		self.rearrangeMgr=RearrangementManager(anonymousCharInfoGenerator, charDescGenerator)
		self.anonymousCharInfoGenerator=AnonymouseCharInfoGenerator
		self.charInfoGenerator=charInfoGenerator
		self.charDescGenerator=charDescGenerator

	def __getitem__(self, key):
		return self.descDB[key]

	def __setitem__(self, key, value):
		self.descDB[key]=value

	def keys(self):
		return self.descDB.keys()

	def getCharInfoGenerator(self):
		return self.charInfoGenerator

	def getAnonymousCharInfoGenerator(self):
		return self.anonymousCharInfoGenerator

	def getAnonymousCharDescGenerator(self):
		return self.charDescGenerator

	def ConstructDescriptionNetwork(self):
		for charName in self.descDB.keys():
			if charName not in self.descNetwork:
				charDesc=CharDescriptionManager.generateDescription(charName)
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
				childDstDesc=CharDescriptionManager.generateDescription(anonymousName)
				self.expandCharDescInNetwork(childDstDesc, childSrcDesc)

			else:
				if childSrcDesc.name in self.descNetwork:
					childDstDesc=self.descNetwork.get(childSrcDesc.name)
				else:
					expandChildSrcDesc=self.descDB.get(childSrcDesc.name)

					childDstDesc=CharDescriptionManager.generateDescription(expandChildSrcDesc.name)

					self.expandCharDescInNetwork(childDstDesc, expandChildSrcDesc)
					self.descNetwork[childDstDesc.name]=childDstDesc

			compList.append(childDstDesc)
		dstDesc.setCompList(compList)

		self.rearrangeMgr.rearrangeDesc(dstDesc)

	def getExpandDescriptionByNameInNetwork(self, charName):
		return self.descNetwork.get(charName, None)

	@staticmethod
	def generateDescription(charName, structInfo=['龜', [], '(龜)']):
		operator, CompList, expression=structInfo
		direction=RearrangementManager.computeDirection(operator)
		charDesc=CharDesc(charName, operator, CompList, direction, expression)
		return charDesc

	@staticmethod
	def getNoneDescription():
		return CharDescriptionManager.NoneDesc

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

