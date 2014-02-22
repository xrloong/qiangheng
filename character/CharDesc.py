#!/usr/bin/env python3

import copy
from character import Operator

class CharDesc:
	"""字符描述"""
	countAnonymousName=0
	def __init__(self, operator, compList):
		self.name=CharDesc.generateNewAnonymousName()
		self.expandName=None

		self.operator=operator
		self.compList=compList

		# 字符的資訊，如在某種輸入法下如何拆碼
		self.propDict=None

	def __str__(self):
		return '<{0}={1}|({2})>'.format(self.getHybridName(), self.getOperator().getName(), ",".join(map(str, self.getCompList())))

	def __repr__(self):
		return str(self)

	def setPropDict(self, propDict):
		self.target.propDict=propDict

	def getPropDict(self):
		return self.target.propDict

	def copyDescription(self):
		copyCharDesc=CharDesc(self.getOperator(), [])
		copyCharDesc.setExpandName(self.getExpandName())
		return copyCharDesc

	def copyDeeply(self):
		ansChildList=[]
		for childDesc in self.getCompList():
			ansChilDesc=childDesc.copyDeeply()
			ansChildList.append(ansChilDesc)

		if self.getOperator().getName()=='龜':
			ansDesc=self.copyDescription()
		else:
			ansDesc=CharDesc(self.getOperator(), ansChildList)

#		if isWithSameExpandName:
#			ansDesc.setExpandName(self.getExpandName())
		return ansDesc

	def getUniqueName(self):
		return self.target.name

	def getHybridName(self):
		if self.isExpandable():
			return self.getExpandName()
		else:
			return self.getUniqueName()

	def setExpandName(self, expandName):
		self.target.expandName=expandName

	def getExpandName(self):
		return self.target.expandName

	def isExpandable(self):
		return bool(self.target.getExpandName())

	def setOperator(self, operator):
		self.target.operator=operator

	def getOperator(self):
		return self.target.operator

	def setCompList(self, compList):
		self.target.compList=compList

	def getCompList(self):
		return self.target.compList

	@property
	def target(self):
		return self

	# 匿名結構是指沒有對應到名字的部分。
	# 若定義 夠=(好 (爻 夕)句) ，則 (爻 夕) 的部分為匿名
	# 若定義 夠=(好 多句) ，則沒有匿名結構
	@staticmethod
	def generateNewAnonymousName():
		name="[瑲珩匿名-{0}]".format(CharDesc.countAnonymousName)
		CharDesc.countAnonymousName+=1
		return name

class HangerCharDesc(CharDesc):
	def __init__(self, operator, compList):
		self.hangerCharDesc=CharDesc(operator, compList)

	@property
	def target(self):
		return self.getHanger()

	def getHanger(self):
		return self.hangerCharDesc

	def setHanger(self, hangerCharDesc):
		self.hangerCharDesc=hangerCharDesc

	def copyDescription(self):
		return HangerCharDesc(self.getOperator(), [])

	def copyDeeply(self):
		hangerCharDesc=HangerCharDesc(self.getOperator(), self.getCompList())
		hangerCharDesc.setHanger(self.getHanger().copyDeeply())
		return hangerCharDesc

if __name__=='__main__':
	print(CharDesc('王', '(龜)', None))

