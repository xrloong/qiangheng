#!/usr/bin/env python3

import copy
from character import Operator

class CharDesc:
	"""字符描述"""
	countAnonymousName=0
	def __init__(self, name, operator, compList, expression, chInfo):
		self.name=name

		self.operator=operator
		self.compList=compList

		self.expression=expression

		# 字符的資訊，如在某種輸入法下如何拆碼
		self.chInfo=chInfo

		self.showFlag=False if len(self.name)>1 else True
		self.anonymous=self.name.count("瑲珩匿名")>0

	def __str__(self):
		return '<{0}={1}|({2})>'.format(self.name, self.operator.getName(), ",".join(map(str, self.compList)))

	def __repr__(self):
		return str(self)

	def copyDescriptionFrom(self, srcDesc):
		self.setName(srcDesc.getName())
		self.setOperator(srcDesc.getOperator())
		self.expression=srcDesc.expression

	def setName(self, name):
		self.name=name
		self.showFlag=False if len(self.name)>1 else True
		self.anonymous=self.name.count("瑲珩匿名")>0

	def getName(self):
		return self.name

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
		return self.anonymous

	def setAnonymous(self, anonymous):
		self.anonymous=anonymous

	def isTemplate(self):
		return False

	def isToShow(self):
		return self.showFlag
		return self.chInfo.isToShow()

	def getCode(self):
		chinfo=self.getChInfo()
		code=chinfo.getCode()
		if self.isToShow() and code:
			return code
		else:
			return None

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
	def __init__(self, templateName, argumentNameList):
		self.templateName=templateName
		self.templateDesc=None
		self.argumentNameList=argumentNameList
		self.anonymous=True

	def __str__(self):
		return self.templateName

	def isTemplate(self):
		return True

	def getTemplateName(self):
		return self.templateName

	def setTemplateName(self, templateName):
		self.templateName=templateName

	def setTemplateDesc(self, templateDesc):
		self.templateDesc=templateDesc

	def setCharDesc(self, charDesc):
		self.charDesc=charDesc

	def getCharDesc(self):
#		return self.charDesc
		return self.templateDesc.getReplacedCharDesc(self.argumentNameList)

	def copyDescriptionFrom(self, srcDesc):
		self.setTemplateName(srcDesc.getTemplateName())
		self.setTemplateDesc(self.templateDesc)
		self.setCharDesc(self.getCharDesc())
#		self.setOperator(srcDesc.getOperator())
#		self.expression=srcDesc.expression

if __name__=='__main__':
	print(CharDesc('王', '(龜)', None))

