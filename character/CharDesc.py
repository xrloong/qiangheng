#!/usr/bin/env python3

import copy
from character import Operator

class CharDesc:
	"""字符描述"""
	countAnonymousName=0
	def __init__(self, name, operator, compList, direction, description, chInfo):
		self.name=name

		self.operator=operator
		self.compList=compList

		self.description=description

		# 字符的資訊，如在某種輸入法下如何拆碼
		self.chInfo=chInfo

	def __str__(self):
		return '<{0}={1}|({2})>'.format(self.name, self.operator.getName(), ",".join(map(str, self.compList)))

	def __repr__(self):
		return str(self)

	def copyInfoWithoutCompListFrom(self, srcDesc):
		self.name=srcDesc.name
		srcOperator=srcDesc.getOperator()
#		self.setOperatorAndDirection(srcOperator, srcDesc.getDirection())
		self.setOperator(srcOperator)
		self.description=srcDesc.description
		self.setChInfo(copy.copy(srcDesc.getChInfo()))

	def setName(self, name):
		self.name=name

	def getName(self):
		return self.name

	def setOperatorAndDirection(self, operator, direction):
		self.operator=operator

	def setOperator(self, operator):
		self.operator=operator

	def getOperator(self):
		return self.operator

	def getDirection(self):
		return self.operator.getDirection()

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

	def isTemplate(self):
		return False

	def setCharTree(self):
		"""設定某一個字符所包含的部件的碼"""

		chInfo=self.getChInfo()
		if not chInfo.isToSetTree():
			return

		radixList=self.getCompList()
		for tmpdesc in radixList:
			tmpdesc.setCharTree()

		infoList=[x.getChInfo() for x in radixList]
		chInfo.setByComps(infoList, self.getDirection())

class TemplateCharDesc(CharDesc):
	def __init__(self, name, templateName, argumentNameList):
		self.name=name
		self.templateName=templateName
		self.templateDesc=None
		self.argumentNameList=argumentNameList

	def __str__(self):
		return self.name

	def isTemplate(self):
		return True

	def getTemplateName(self):
		return self.templateName

	def setTemplateDesc(self, templateDesc):
		self.templateDesc=templateDesc

	def setCharDesc(self, charDesc):
		self.charDesc=charDesc

	def getCharDesc(self):
#		return self.charDesc
		return self.templateDesc.getReplacedCharDesc(self.argumentNameList)

if __name__=='__main__':
	print(CharDesc('王', '(龜)', None))

