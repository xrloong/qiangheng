#!/usr/bin/env python3

import copy

class CharDesc:
	"""字符描述"""
	countAnonymousName=0
	def __init__(self, name, operator, compList, direction, description, chInfo):
		self.name=name

		self.op=operator
		self.compList=compList
		self.direction=direction

		self.description=description

		# 字符的資訊，如在某種輸入法下如何拆碼
		self.chInfo=chInfo

	def __str__(self):
		return '<{0}={1}|({2})>'.format(self.name, self.op, ",".join(map(str, self.compList)))

	def __repr__(self):
		return str(self)

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

	# 匿名結構是指沒有對應到名字的部分。
	# 若定義 夠=(好 (爻 夕)句) ，則 (爻 夕) 的部分為匿名
	# 若定義 夠=(好 多句) ，則沒有匿名結構
	@staticmethod
	def generateNewAnonymousName():
		name="[瑲珩匿名-{0}]".format(CharDesc.countAnonymousName)
		CharDesc.countAnonymousName+=1
		return name

	def isAnonymous(self):
		return self.name.count("瑲珩匿名")>0

if __name__=='__main__':
	print(CharDesc('王', '(龜)', None))

