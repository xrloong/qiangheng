#!/usr/bin/env python3

import copy
from character import Operator

class CharDesc:
	"""字符描述"""
	countAnonymousName=0
	def __init__(self, operator, compList):
		name=CharDesc.generateNewAnonymousName()

		self.name=name
		self.expandName=None

		self.operator=operator
		self.compList=compList

		# 字符的資訊，如在某種輸入法下如何拆碼
		self.propDict=None

	def __str__(self):
		return '<{0}={1}|({2})>'.format(self.getName(), self.operator.getName(), ",".join(map(str, self.compList)))

	def __repr__(self):
		return str(self)

	def setPropDict(self, propDict):
		self.propDict=propDict

	def getPropDict(self):
		return self.propDict

	def copyDescription(self):
		copyCharDesc=CharDesc(self.getOperator(), [])
		copyCharDesc.setName(self.getName())
		copyCharDesc.setExpandName(self.getExpandName())
		return copyCharDesc

	def setName(self, name):
		self.name=name

	def getName(self):
		return self.name

	def getName(self):
		if self.isExpandable():
			return self.getExpandName()
		else:
			return self.name

	def setExpandName(self, expandName):
		self.expandName=expandName

	def getExpandName(self):
		return self.expandName

	def isExpandable(self):
		return bool(self.getExpandName())

	def setOperator(self, operator):
		self.operator=operator

	def getOperator(self):
		return self.operator

	def setCompList(self, compList):
		self.compList=compList

	def getCompList(self):
		return self.compList

	# 匿名結構是指沒有對應到名字的部分。
	# 若定義 夠=(好 (爻 夕)句) ，則 (爻 夕) 的部分為匿名
	# 若定義 夠=(好 多句) ，則沒有匿名結構
	@staticmethod
	def generateNewAnonymousName():
		name="[瑲珩匿名-{0}]".format(CharDesc.countAnonymousName)
		CharDesc.countAnonymousName+=1
		return name

if __name__=='__main__':
	print(CharDesc('王', '(龜)', None))

