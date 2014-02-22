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
		self.chInfo=charinfo.CharInfo.NoneChar

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
		self.descDB={}

	def __getitem__(self, key):
		return self.descDB[key]

	def __setitem__(self, key, value):
		self.descDB[key]=value

	def keys(self):
		return self.descDB.keys()

	def get(self, key, value=None):
		return self.descDB.get(key, value)

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

	def getExpandDescriptionByName(self, charName):
		charDesc=copy.copy(self.get(charName, None))
		if not charDesc:
			return None

		self.expandCharDesc(charDesc)
		return charDesc

	def expandCharDesc(self, charDesc):

		if len(charDesc.getCompList())==0:
			chdesc=self.get(charDesc.name, None)
			if len(chdesc.getCompList())==0:
				return chdesc
			else:
				# 現有的資料已見底，但從 DB 中查到者仍可擴展
				return self.expandCharDesc(chdesc)

		l=[]
		for idxChdesc in charDesc.getCompList():
			newDesc=copy.copy(idxChdesc)
			expandDesc=self.expandCharDesc(newDesc)
			l.append(expandDesc)

		self.rearrangeDesc(charDesc)
		return charDesc

	def rearrangeDesc(self, charDesc):
		[newOp, newCompList]=self.getRearrangedOpAndCompList(charDesc)
		direction=CharDescriptionManager.computeDirection(newOp)
		charDesc.setOperatorAndDirection(newOp, direction)

		# deepcopy 可以防止動到 descDB 的內容
		# 但不用 deepcopy 則快很多
#		charDesc.setCompList(copy.deepcopy(newCompList))
		charDesc.setCompList(newCompList)

	def getRearrangedOpAndCompList(self, charDesc):
#		['水', '林', '爻', '卅', '丰', '鑫', '卌', '圭', '燚',]
#		['好', '志',
#		'回', '同', '函', '區', '左',
#		'起', '廖', '載', '聖', '句',
#		'夾', '衍', '衷',]
#		['纂', '膷',]
		ch=charDesc.getChInfo()

		newOperator='龜'
		newCompList=[]

		oldOperator=charDesc.getOperator()
		nameCompList=[x.name for x in charDesc.getCompList()]

		if oldOperator in ['龜']:
			newOperator=oldOperator
			newCompList=[]
		elif oldOperator in ['水']:
			x=self.get(nameCompList[0], None)

			newOperator=oldOperator
			newCompList=[x]
		elif oldOperator in ['好', '志', '回', '同', '函', '區', '載', '廖', '起', '句', '夾']:
			x=self.get(nameCompList[0], None)
			y=self.get(nameCompList[1], None)

			newOperator=oldOperator
			newCompList=[x, y]
		elif oldOperator in ['算', '湘', '霜', '想', '怡', '穎',]:
			x=self.get(nameCompList[0], None)
			y=self.get(nameCompList[1], None)
			z=self.get(nameCompList[2], None)

			newOperator=oldOperator
			newCompList=[x, y, z]
		elif oldOperator in ['纂',]:
			x=self.get(nameCompList[0], None)
			y=self.get(nameCompList[1], None)
			z=self.get(nameCompList[2], None)
			w=self.get(nameCompList[3], None)

			newOperator=oldOperator
			newCompList=[x, y, z, w]
		elif oldOperator in ['林', '爻']:
			x=self.get(nameCompList[0], None)

			if oldOperator=='林':
				newOperator='好'
			elif oldOperator=='爻':
				newOperator='志'
			else:
				newOperator='錯'
			newCompList=[x, x]
		elif oldOperator in ['卅', '鑫']:
			x=self.get(nameCompList[0], None)

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
			x=self.get(nameCompList[0], None)

			newOperator=oldOperator
			newCompList=[x, x, x, x]
		else:
			newOperator='龜'
			newCompList=[]
		return [newOperator, newCompList]

	def setCharTree(self, charDesc):
		"""設定某一個字符所包含的部件的碼"""

		chInfo=charDesc.getChInfo()
		if not chInfo.isToSetTree():
			return

		radixList=charDesc.getCompList()
		for tmpdesc in radixList:
			self.setCharTree(tmpdesc)

		infoList=[x.getChInfo() for x in radixList]
		chInfo.setByComps(infoList, charDesc.getDirection())

if __name__=='__main__':
	print(CharDesc.NoneDesc)
	print(CharDesc('王', '(龜)', None))

