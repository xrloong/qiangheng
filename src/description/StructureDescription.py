#!/usr/bin/env python3

import copy

class StructureDescription:
	"""字符描述"""
	countAnonymousName=0
	def __init__(self, operator, compList):
		self.name=StructureDescription.generateNewAnonymousName()
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
		copyStructureDescription=StructureDescription(self.getOperator(), [])
		copyStructureDescription.setExpandName(self.getExpandName())
		return copyStructureDescription

	def copyDeeply(self):
		ansChildList=[]
		for childDesc in self.getCompList():
			ansChilDesc=childDesc.copyDeeply()
			ansChildList.append(ansChilDesc)

		if self.getOperator().getName()=='龜':
			ansDesc=self.copyDescription()
		else:
			ansDesc=StructureDescription(self.getOperator(), ansChildList)

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
		name="[瑲珩匿名-{0}]".format(StructureDescription.countAnonymousName)
		StructureDescription.countAnonymousName+=1
		return name

class HangerStructureDescription(StructureDescription):
	def __init__(self, operator, compList):
		self.hangerStructureDescription=StructureDescription(operator, compList)

	@property
	def target(self):
		return self.hangerStructureDescription

	def replacedBy(self, newStructureDescription):
		self.hangerStructureDescription=newStructureDescription.target

	def copyDescription(self):
		return HangerStructureDescription(self.getOperator(), [])

	def copyDeeply(self):
		newTarget=self.target.copyDeeply()
		hangerStructureDescription=HangerStructureDescription(self.getOperator(), self.getCompList())
		hangerStructureDescription.replacedBy(newTarget)
		return hangerStructureDescription

if __name__=='__main__':
	print(StructureDescription('王', '(龜)', None))
