#!/usr/bin/env python3

import copy
from character import Operator

class CharDesc:
	"""字符描述"""
	countAnonymousName=0
	def __init__(self, name, operator, compList):
		self.name=name

		self.operator=operator
		self.compList=compList

		# 字符的資訊，如在某種輸入法下如何拆碼
		self.chInfo=None

		self.showFlag=False if len(self.name)>1 else True

	def __str__(self):
#		return '<{0}={1}>'.format(self.name, self.operator.getName())
		chInfo=self.getChInfo()
		if chInfo!=None:
			return '<{0},{3}={1}|({2})>'.format(self.name, self.operator.getName(), ",".join(map(str, self.compList)), chInfo)
		else:
			return '<{0}={1}|({2})>'.format(self.name, self.operator.getName(), ",".join(map(str, self.compList)))

	def __repr__(self):
		return str(self)

	def copyDescription(self):
		return CharDesc(self.getName(), self.getOperator(), [])

	def setName(self, name):
		self.name=name
		self.showFlag=False if len(self.name)>1 else True
#		self.anonymous=self.name.count("瑲珩匿名")>0

	def getName(self):
		return self.name

	def setOperator(self, operator):
		self.operator=operator

	def getOperator(self):
		return self.operator

	def setCompList(self, compList):
		self.compList=compList

	def getCompList(self):
		return self.compList

	def setChInfo(self, chInfo):
		self.chInfo=chInfo

	def getChInfo(self):
		return self.chInfo

	# 匿名結構是指沒有對應到名字的部分。
	# 若定義 夠=(好 (爻 夕)句) ，則 (爻 夕) 的部分為匿名
	# 若定義 夠=(好 多句) ，則沒有匿名結構
	@staticmethod
	def generateNewAnonymousName():
		name="[瑲珩匿名-{0}]".format(CharDesc.countAnonymousName)
		CharDesc.countAnonymousName+=1
		return name

	def isToShow(self):
		return self.showFlag
		return self.chInfo.isToShow()

if __name__=='__main__':
	print(CharDesc('王', '(龜)', None))

