#!/usr/bin/env python3

import charinfo

class CharDesc:
	"""字符描述"""
	def __init__(self, name, description, chInfo):
		self.name=name

		self.op='龜'
		self.compList=[]

		self.description=description

		# 字符的資訊，如在某種輸入法下如何拆碼
		self.chInfo=chInfo

	def setName(self, name):
		self.name=name

	def setOp(self, op):
		self.op=op

	def setCompList(self, compList):
		self.compList=compList

	def getCompList(self):
		return self.compList

	def getDescription(self):
		return self.getDescription

	def setChInfo(self, chInfo):
		self.chInfo=chInfo

	def getChInfo(self):
		return self.chInfo

	def __str__(self):
		return '<{0}={1}|({2})>'.format(self.name, self.op, ",".join(map(str, self.compList)))

	def __repr__(self):
		return str(self)

	def setCharTree(self, descDB):
		"""設定某一個字符所包含的部件的碼"""

		if not self.getChInfo().isToSetTree():
			return

		expand_chdesc=self.expandCharTree(descDB)
		for tmpdesc in expand_chdesc.getSubRootList():
			tmpdesc.setCharTree(descDB)

		expand_chdesc.updateCharInfo()

	def expandCharTree(self, descDB):

		if len(self.getCompList())==0:
			chdesc=descDB.get(self.name, None)
			if len(chdesc.getCompList())==0:
				return chdesc
			else:
				# 現有的資料已見底，但從 DB 中查到者仍可擴展
				return chdesc.expandCharTree(descDB)

		l=[]
		for tc in self.getCompList():
			x=tc.expandCharTree(descDB)
			l.append(x)

		anscomp=self.getRearrangedDesc(descDB)

		return anscomp

	def getSubRootList(self):
		# 計算及更新 self.chInfo
		# normalizationToLinear 會依不同輸人法而多型
		# 倉頡為較大的組件
		# 其它為最小的組件
		return self.chInfo.normalizationToLinear(self)

	def updateCharInfo(self):
		# 計算及更新 self.chInfo
		# updateIMCode 會依不同輸人法而多型
		# 倉頡的演算法與其它不同
		self.chInfo.updateIMCode(self)

	def getRearrangedDesc(self, descDB):
		[newOp, newCompList]=self.getRearrangedOpAndCompList(descDB)
		self.setOp(newOp)
		self.setCompList(newCompList)
		return self

	def getRearrangedOpAndCompList(self, descDB):
#		['水', '林', '爻', '卅', '丰', '鑫', '卌', '圭', '燚',]
#		['好', '志',
#		'回', '同', '函', '區', '左',
#		'起', '廖', '載', '聖', '句',
#		'夾', '衍', '衷',]
#		['纂', '膷',]
#		descDB=self.descDB
		ch=self.getChInfo()

		newOperator='龜'
		newCompList=[]

		oldOperator=ch.operator
		oldCompList=[x for x in map(lambda x: x.name, self.getCompList())]

		if oldOperator in ['龜']:
			newOperator=oldOperator
			newCompList=[]
		elif oldOperator in ['水']:
			x=descDB.get(oldCompList, None)
			x=oldCompList[0]

			newOperator=oldOperator
			newCompList=[x]
		elif oldOperator in ['好', '志', '回', '同', '函', '區', '載', '廖', '起', '句', '夾']:
			x=descDB.get(oldCompList[0], None)
			y=descDB.get(oldCompList[1], None)

			newOperator=oldOperator
			newCompList=[x, y]
		elif oldOperator in ['算', '湘', '霜', '想', '怡', '穎',]:
			x=descDB.get(oldCompList[0], None)
			y=descDB.get(oldCompList[1], None)
			z=descDB.get(oldCompList[2], None)

			newOperator=oldOperator
			newCompList=[x, y, z]
		elif oldOperator in ['纂',]:
			x=descDB.get(oldCompList[0], None)
			y=descDB.get(oldCompList[1], None)
			z=descDB.get(oldCompList[2], None)
			w=descDB.get(oldCompList[3], None)

			newOperator=oldOperator
			newCompList=[x, y, z, w]
		elif oldOperator in ['林', '爻']:
			x=descDB.get(oldCompList[0], None)

			if oldOperator=='林':
				newOperator='好'
			elif oldOperator=='爻':
				newOperator='志'
			else:
				newOperator='錯'
			newCompList=[x, x]
		elif oldOperator in ['卅', '鑫']:
			x=descDB.get(oldCompList[0], None)

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
			x=descDB.get(oldCompList[0], None)

			newOperator=oldOperator
			newCompList=[x, x, x, x]
		else:
			newOperator='龜'
			newCompList=[]
#		chdesc.setOp(newOperator)
#		chdesc.setCompList(newCompList)
		return [newOperator, newCompList]

	def getCJPrePostList(self):
		"""傳回倉頡的字首及字尾的部件串列"""

		oldOperator=self.op
		oldCompList=self.getCompList()

		prelist=[]
		postlist=[]
		if oldOperator in ['龜']:
			prelist=[]
			postlist=[]
		elif oldOperator in ['水']:
			x=oldCompList[0]
			prelist=[x]
			postlist=[]
		elif oldOperator in ['好', '志', '回', '同', '函', '區', '載', '廖', '起', '句', '夾']:
			x=oldCompList[0]
			y=oldCompList[1]
			prelist=[x]
			postlist=[y]
		elif oldOperator in ['算', '湘', '霜', '怡',]:
			x=oldCompList[0]
			y=oldCompList[1]
			z=oldCompList[2]
			prelist=[x]
			postlist=[y, z]
		elif oldOperator in ['想', '穎',]:
			x=oldCompList[0]
			y=oldCompList[1]
			z=oldCompList[2]
			prelist=[x, y]
			postlist=[z]
		elif oldOperator in ['林', '爻']:
			x=oldCompList[0]
			prelist=[x]
			postlist=[x]
		elif oldOperator in ['卅', '鑫']:
			x=oldCompList[0]
			prelist=[x]
			postlist=[x, x]
		elif oldOperator in ['燚',]:
			x=oldCompList[0]
			prelist=[x, x]
			postlist=[x, x]
		elif oldOperator in ['纂',]:
			x=oldCompList[0]
			y=oldCompList[1]
			z=oldCompList[2]
			w=oldCompList[3]
			prelist=[x]
			postlist=[y, z, w]
		else:
			prelist=[]
			postlist=[]
		return [prelist, postlist]

CharDesc.NoneDesc=CharDesc("", '', charinfo.CharInfo.NoneChar)

if __name__=='__main__':
	print(CharDesc.NoneDesc)
	print(CharDesc('王', '(龜)', None))

