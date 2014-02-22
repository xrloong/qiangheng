#!/usr/bin/env python3

import charinfo
import copy

class CharDesc:
	"""字符描述"""
	def __init__(self, name, operator, compList, direction, description):
		self.name=name

		self.op=operator
		self.compList=compList
		self.direction=direction

		self.description=description

		# 字符的資訊，如在某種輸入法下如何拆碼
#		self.chInfo=charinfo.CharInfo.NoneChar
		self.chInfo=copy.copy(charinfo.CharInfo.NoneChar)
		self.chInfo.charname+=" abc "+name+" def"

	def copyInfoFrom(self, srcDesc):
		self.name=srcDesc.name
		self.setOperatorAndDirection(srcDesc.getOperator(), srcDesc.getDirection())
		self.compList=copy.copy(srcDesc.getCompList())
		self.description=srcDesc.description
		self.setChInfo(copy.copy(srcDesc.getChInfo()))

	def copyInfoWithoutCompListFrom(self, srcDesc):
		self.name=srcDesc.name
		self.setOperatorAndDirection(srcDesc.getOperator(), srcDesc.getDirection())
		self.description=srcDesc.description
		self.setChInfo(copy.copy(srcDesc.getChInfo()))

	def setName(self, name):
		self.name=name

	def setOperatorAndDirection(self, op, direction):
		self.direction=direction
		self.op=op

	def getOperator(self):
		return self.op

	def getDirection(self):
		return self.direction

	def setCompList(self, compList):
		self.compList=compList

	def getCompList(self):
		return self.compList

	def setChInfo(self, chInfo):
		self.chInfo=chInfo

	def getChInfo(self):
		return self.chInfo

	def __str__(self):
		return '<{0}={1}|({2})>'.format(self.name, self.op, ",".join(map(str, self.compList)))

	def __repr__(self):
		return str(self)

CharDesc.NoneDesc=CharDesc("", '龜', [], '+', '(龜)')

class CharDescriptionManager:
	def __init__(self):
		# descDB 放最原始、沒有擴展過的 CharDesc ，也就是從檔案讀出來的資料。
		# descNetwork 放擴展過的，且各個 CharDesc 可能會彼此參照。
		# 但 descNetwork 跟 descDB 則是完全獨立。
		# 在使用 descNetwork 前，要先呼叫 ConstructDescriptionNetwork()
		# ConstructDescriptionNetwork() 會從 descDB 建立 descNetwork
		self.descDB={}
		self.descNetwork={}

	def __getitem__(self, key):
		return self.descDB[key]

	def __setitem__(self, key, value):
		self.descDB[key]=value

	def keys(self):
		return self.descDB.keys()

	def ConstructDescriptionNetwork(self):
		for charName, tmpCharDesc in self.descDB.items():
			charDesc=CharDescriptionManager.generateDescription(charName)
			if not charDesc: continue
			self.descNetwork[charName]=charDesc
			charDesc.copyInfoFrom(tmpCharDesc)

		for charName, tmpCharDesc in self.descNetwork.items():
			l=[]
			for idvCharDesc in tmpCharDesc.getCompList():
				c=self.descNetwork.get(idvCharDesc.name)
				l.append(c)
			tmpCharDesc.setCompList(l)
			CharDescriptionManager.rearrangeDesc(tmpCharDesc)

	def ConstructDescriptionNetwork(self):
		for charName in self.descDB.keys():
			if charName not in self.descNetwork:
				charDesc=CharDescriptionManager.generateDescription(charName)
				self.expandCharDescInNetwork(charDesc)
				self.descNetwork[charName]=charDesc

	def expandCharDescInNetwork(self, charDesc):
		# 擴展 charDesc
		# charDesc 會被改變，而非產生新的 CharDesc
		if charDesc.name not in self.descNetwork:
			tmpDesc=self.descDB.get(charDesc.name, None)
			charDesc.copyInfoWithoutCompListFrom(tmpDesc)

			compList=[]
			for idxChdesc in tmpDesc.getCompList():
				subDesc=self.descNetwork.get(idxChdesc.name)
				if subDesc==None:
					subDesc=CharDescriptionManager.generateDescription(idxChdesc.name)
					self.expandCharDescInNetwork(subDesc)
					self.descNetwork[subDesc.name]=subDesc
				compList.append(subDesc)
			charDesc.setCompList(compList)

			CharDescriptionManager.rearrangeDesc(charDesc)

	def getExpandDescriptionByNameInNetwork(self, charName):
		return self.descNetwork.get(charName, None)

	def getExpandDescriptionByName(self, charName):
		charDesc=CharDescriptionManager.generateDescription(charName)
		if not charDesc:
			return None

		self.expandCharDesc(charDesc)
		return charDesc

	def expandCharDesc(self, charDesc):
		# 擴展 charDesc
		# charDesc 會被改變，而非產生新的 CharDesc
		if len(charDesc.getCompList())==0:
			tmpDesc=self.descDB.get(charDesc.name, None)
			if len(tmpDesc.getCompList())==0:
				pass
			else:
				# 現有的資料已見底，但從 DB 中查到者仍可擴展
				self.expandCharDesc(tmpDesc)
			charDesc.copyInfoFrom(tmpDesc)

		else:
			for idxChdesc in charDesc.getCompList():
				self.expandCharDesc(idxChdesc)

		CharDescriptionManager.rearrangeDesc(charDesc)

	@staticmethod
	def generateDescription(charName, structInfo=['龜', [], '(龜)']):
		operator, CompList, expression=structInfo
		direction=CharDescriptionManager.computeDirection(operator)
		charDesc=CharDesc(charName, operator, CompList, direction, expression)
		return charDesc

	@staticmethod
	def getNoneDescription():
		return CharDesc.NoneDesc

	@staticmethod
	def computeDirection(oldOperator):
		"""計算部件的結合方向"""

		ansDir='+'
		if oldOperator in ['龜']:
			ansDir='+'
		elif oldOperator in ['水']:
			# 暫時不會執行這段，且還在重構中
			pass
#			ansDir='+'
#			ansDir=self.getCompList()[0].getDirection()
		elif oldOperator in ['回', '同', '函', '區', '載', '廖', '起', '句', '夾']:
			ansDir='+'
		elif oldOperator in ['纂', '算', '志', '霜', '想', '爻', '卅', ]:
			ansDir='|'
		elif oldOperator in ['湘', '好', '怡', '穎', '林', '鑫', ]:
			ansDir='-'
		elif oldOperator in ['燚',]:
			ansDir='+'
		else:
			ansDir='+'
		return ansDir

	@staticmethod
	def rearrangeDesc(charDesc):
		[newOp, newCompList]=CharDescriptionManager.computeRearrangedOpAndCompList(charDesc)
		direction=CharDescriptionManager.computeDirection(newOp)
		charDesc.setOperatorAndDirection(newOp, direction)
		charDesc.setCompList(newCompList)

	@staticmethod
	def computeRearrangedOpAndCompList(charDesc):
#		['水', '林', '爻', '卅', '丰', '鑫', '卌', '圭', '燚',]
#		['好', '志',
#		'回', '同', '函', '區', '左',
#		'起', '廖', '載', '聖', '句',
#		'夾', '衍', '衷',]
#		['纂', '膷',]
		newOperator='龜'
		newCompList=[]

		oldOperator=charDesc.getOperator()
		oldCompList=charDesc.getCompList()

		if oldOperator in ['龜']:
			newOperator=oldOperator
			newCompList=[]
		elif oldOperator in ['水']:
			x=oldCompList[0]

			newOperator=oldOperator
			newCompList=[x]
		elif oldOperator in ['好', '志', '回', '同', '函', '區', '載', '廖', '起', '句', '夾']:
			x=oldCompList[0]
			y=oldCompList[1]

			newOperator=oldOperator
			newCompList=[x, y]
		elif oldOperator in ['算', '湘', '霜', '想', '怡', '穎',]:
			x=oldCompList[0]
			y=oldCompList[1]
			z=oldCompList[2]

			newOperator=oldOperator
			newCompList=[x, y, z]
		elif oldOperator in ['纂',]:
			x=oldCompList[0]
			y=oldCompList[1]
			z=oldCompList[2]
			w=oldCompList[3]

			newOperator=oldOperator
			newCompList=[x, y, z, w]
		elif oldOperator in ['林', '爻']:
			x=oldCompList[0]

			if oldOperator=='林':
				newOperator='好'
			elif oldOperator=='爻':
				newOperator='志'
			else:
				newOperator='錯'
			newCompList=[x, x]
		elif oldOperator in ['卅', '鑫']:
			x=oldCompList[0]

			if oldOperator=='卅':
				newOperator='湘'
			elif oldOperator=='鑫':
				# 暫不處理
				newOperator='算'
			else:
				newOperator='錯'
			newCompList=[x, x, x]
		elif oldOperator in ['燚',]:
			# 暫不處理
			x=oldCompList[0]

			newOperator=oldOperator
			newCompList=[x, x, x, x]
		else:
			newOperator='龜'
			newCompList=[]
		return [newOperator, newCompList]

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
	print(CharDesc.NoneDesc)
	print(CharDesc('王', '(龜)', None))

