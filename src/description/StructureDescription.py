#!/usr/bin/env python3

import sys
import Constant
from gear.CodeVarianceType import CodeVarianceTypeFactory

class StructureDescription:
	class Generator:
		def __init__(self):
			pass

		def generateLeafNode(self, nodeName):
			structDesc=self.generateNode()
			structDesc.setReferenceExpression(nodeName)
			return structDesc

		def generateNode(self, structInfo=['龜', []]):
			from state import StateManager
			operationManager = StateManager.getOperationManager()

			operatorName, CompList=structInfo
			operator=operationManager.generateOperator(operatorName)
			structDesc=StructureDescription.generate(operator, CompList)
			return structDesc

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

	def clone(self):
		compList=[c.clone() for c in self.getCompList()]
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

