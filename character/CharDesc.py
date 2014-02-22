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
		self.propDict=propDict

	def getPropDict(self):
		return self.propDict

	def copyDescription(self):
		copyCharDesc=CharDesc(self.getOperator(), [])
		copyCharDesc.setExpandName(self.getExpandName())
		return copyCharDesc

	def copyDeeply(self, isWithSameExpandName=True):
		ansChildList=[]
		for childDesc in self.getCompList():
			ansChilDesc=childDesc.copyDeeply(False)
			ansChildList.append(ansChilDesc)

		if self.getOperator().getName()=='龜':
			ansDesc=self.copyDescription()
		else:
			ansDesc=CharDesc(self.getOperator(), ansChildList)

		if isWithSameExpandName:
			ansDesc.setExpandName(self.getExpandName())
		return ansDesc

	def getUniqueName(self):
		return self.name

	def getHybridName(self):
		if self.isExpandable():
			return self.getExpandName()
		else:
			return self.getUniqueName()

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

class HangerCharDesc(CharDesc):
	def __init__(self, operator, compList):
		self.hangerCharDesc=CharDesc(operator, compList)

	def setPropDict(self, propDict):
		return self.hangerCharDesc.setPropDict(propDict)

	def getHanger(self):
		return self.hangerCharDesc

	def setHanger(self, hangerCharDesc):
		self.hangerCharDesc=hangerCharDesc

	def getPropDict(self):
		return self.hangerCharDesc.getPropDict()

	def copyDescription(self):
		return HangerCharDesc(self.getOperator(), [])

	def copyDeeply(self, isWithSameExpandName=True):
		hangerCharDesc=HangerCharDesc(self.getOperator(), self.getCompList())
		hangerCharDesc.setHanger(self.getHanger().copyDeeply())
		return hangerCharDesc

	def getUniqueName(self):
		return self.hangerCharDesc.getUniqueName()

	def setExpandName(self, expandName):
		return self.hangerCharDesc.setExpandName(expandName)

	def getExpandName(self):
		return self.hangerCharDesc.getExpandName()

	def isExpandable(self):
		return self.hangerCharDesc.isExpandable()

	def setOperator(self, operator):
		return self.hangerCharDesc.setOperator(operator)

	def getOperator(self):
		return self.hangerCharDesc.getOperator()

	def setCompList(self, compList):
		return self.hangerCharDesc.setCompList(compList)

	def getCompList(self):
		return self.hangerCharDesc.getCompList()

if __name__=='__main__':
	print(CharDesc('王', '(龜)', None))

