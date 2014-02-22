#!/usr/bin/env python3

import sys
import copy
import Constant
from gear.CodeVarianceType import CodeVarianceTypeFactory

class StructureDescription:
	"""字符描述"""
	countAnonymousName=0
	def __init__(self, operator, compList):
		self.name=StructureDescription.generateNewAnonymousName()
		self.referenceExpression=None

		self.rootName=None
		self.flagIsRoot=False

		self.operator=operator
		self.compList=compList

		self.codeVariance=CodeVarianceTypeFactory.generate()

	def __str__(self):
		return '<{0}={1}|({2})>'.format(self.getReferenceExpression(), self.getOperator().getName(), ",".join(map(str, self.getCompList())))

	def __repr__(self):
		return str(self)

	def __deepcopy__(self, memo):
		compList=copy.deepcopy(self.getCompList(), memo)
		structureDescription=StructureDescription.generate(self.getOperator(), compList)

		if self.getOperator().getName()=='龜':
			structureDescription.setReferenceExpression(self.getReferenceExpression())
			structureDescription.setCodeVarianceType(self.getCodeVarianceType())

		return structureDescription

	@staticmethod
	def generate(operator, compList):
		targetDescription=StructureDescription(operator, compList)
		return targetDescription

	def clone(self):
		return copy.deepcopy(self)

	def setStructureProperties(self, structProp):
		codeVarianceString=structProp.get(Constant.TAG_CODE_VARIANCE_TYPE, Constant.VALUE_CODE_VARIANCE_TYPE_STANDARD)
		codeVarianceType=CodeVarianceTypeFactory.generateByString(codeVarianceString)
		self.setCodeVarianceType(codeVarianceType)

	def getCodeVarianceType(self):
		return self.target.codeVariance

	def setCodeVarianceType(self, codeVariance):
		self.target.codeVariance=codeVariance

	def getUniqueName(self):
		return self.target.name

	def setReferenceExpression(self, referenceExpression):
		self.target.referenceExpression=referenceExpression

	def getReferenceExpression(self):
		return self.target.referenceExpression

	def getReferenceName(self):
		expression=self.target.referenceExpression
		if expression:
			return expression.split(".")[0]
		else:
			return expression

	def setRootName(self, rootName):
		self.target.rootName=rootName

	def getRootName(self):
		return self.target.rootName

	def isRoot(self):
		return bool(self.target.getRootName())

	def isLeaf(self):
		return bool(self.target.getReferenceName())

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
	def __init__(self, targetDescription):
		self.hangerStructureDescription=targetDescription

	def __deepcopy__(self, memo):
		copy.deepcopy(None, memo)

		newTarget=copy.deepcopy(self.target)
		hangerStructureDescription=HangerStructureDescription(newTarget)
		return hangerStructureDescription

	@staticmethod
	def generate(operator, compList):
		targetDescription=StructureDescription(operator, compList)
		return HangerStructureDescription(targetDescription)

	@property
	def target(self):
		return self.hangerStructureDescription

	def replacedBy(self, newStructureDescription):
		self.hangerStructureDescription=newStructureDescription.target

if __name__=='__main__':
	print(StructureDescription('王', '(龜)', None))

