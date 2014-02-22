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

	def setStructureProperties(self, structProp):
		codeVarianceString=structProp.get(Constant.TAG_CODE_VARIANCE_TYPE, Constant.VALUE_CODE_VARIANCE_TYPE_STANDARD)
		codeVarianceType=CodeVarianceTypeFactory.generateByString(codeVarianceString)
		self.setCodeVarianceType(codeVarianceType)

	def getCodeVarianceType(self):
		return self.codeVariance

	def setCodeVarianceType(self, codeVariance):
		self.codeVariance=codeVariance

	def getUniqueName(self):
		return self.name

	def setReferenceExpression(self, referenceExpression):
		self.referenceExpression=referenceExpression

	def getReferenceExpression(self):
		return self.referenceExpression

	def getReferenceName(self):
		expression=self.referenceExpression
		if expression:
			return expression.split(".")[0]
		else:
			return expression

	def setRootName(self, rootName):
		self.rootName=rootName

	def getRootName(self):
		return self.rootName

	def isRoot(self):
		return bool(self.getRootName())

	def isLeaf(self):
		return bool(self.getReferenceName())

	def setOperator(self, operator):
		self.operator=operator

	def getOperator(self):
		return self.operator

	def setCompList(self, compList):
		self.compList=compList

	def getCompList(self):
		return self.compList

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

# 使用代理人模式
class HangerStructureDescription:
	def __init__(self, targetDescription):
		self.targetDescription=targetDescription

	def __deepcopy__(self, memo):
		return HangerStructureDescription(copy.deepcopy(self.target))

	@staticmethod
	def generate(operator, compList):
		targetDescription=StructureDescription(operator, compList)
		return HangerStructureDescription(targetDescription)

	@property
	def target(self):
		return self.targetDescription

	def clone(self):
		return copy.deepcopy(self)

	def replacedBy(self, newStructureDescription):
		self.targetDescription=newStructureDescription.target


	def setStructureProperties(self, structProp):
		self.targetDescription.setStructureProperties(structProp)

	def getCodeVarianceType(self):
		return self.targetDescription.getCodeVarianceType()

	def setCodeVarianceType(self, codeVariance):
		self.targetDescription.setCodeVarianceType(codeVariance)

	def getUniqueName(self):
		return self.targetDescription.getUniqueName()

	def setReferenceExpression(self, referenceExpression):
		self.targetDescription.setReferenceExpression(referenceExpression)

	def getReferenceExpression(self):
		return self.targetDescription.getReferenceExpression()

	def getReferenceName(self):
		return self.targetDescription.getReferenceName()

	def setRootName(self, rootName):
		self.targetDescription.setRootName(rootName)

	def getRootName(self):
		return self.targetDescription.getRootName()

	def isRoot(self):
		return self.targetDescription.isRoot()

	def isLeaf(self):
		return self.targetDescription.isLeaf()

	def setOperator(self, operator):
		self.targetDescription.setOperator(operator)

	def getOperator(self):
		return self.targetDescription.getOperator()

	def setCompList(self, compList):
		self.targetDescription.setCompList(compList)

	def getCompList(self):
		return self.targetDescription.getCompList()

if __name__=='__main__':
	print(StructureDescription('王', '(龜)', None))

