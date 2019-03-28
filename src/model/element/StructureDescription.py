#!/usr/bin/env python3

import sys
import Constant
import model

from injector import inject

class StructureDescriptionGenerator:
	@inject
	def __init__(self, operationManager: model.OperatorManager.OperatorManager):
		self.operationManager = operationManager

	def generateLeafNode(self, nodeExpression):
		structDesc=self.generateNode()
		structDesc.setReferenceExpression(nodeExpression)
		structDesc.generateName()
		return structDesc

	def generateNode(self, structInfo=['龜', []]):
		operatorName, compList=structInfo
		operator=self.operationManager.generateOperator(operatorName)
		structDesc=StructureDescription(operator, compList)
		structDesc.generateName()
		return structDesc

class StructureDescription:
	def __init__(self, operator, compList):
		self.referenceExpression=None

		self.flagIsRoot=False

		self.operator=operator
		self.compList=compList

	def __str__(self):
		return '<{0}={1}|({2})>'.format(self.getReferenceExpression(), self.getOperator().getName(), ",".join(map(str, self.getCompList())))

	def __repr__(self):
		return str(self)

	def clone(self):
		compList=[c.clone() for c in self.getCompList()]
		structureDescription=StructureDescription.generate(self.getOperator(), compList)
		structureDescription.setReferenceExpression(self.getReferenceExpression())

		return structureDescription

	def getUniqueName(self):
		return self.name

	def generateName(self):
		if self.isLeaf():
			self.name=self.getReferenceExpression()
		else:
			strList = [self.getOperator().getName()]
			strList.extend([comp.getUniqueName() for comp in self.compList])
			self.name="({0})".format(" ".join(strList))

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

	def isLeaf(self):
		return bool(self.getReferenceName())

	def isEmpty(self):
		return self.getOperator().getName()=='龜' or len(self.compList)==0

	def setOperator(self, operator):
		self.operator=operator
		self.generateName()

	def getOperator(self):
		return self.operator

	def setCompList(self, compList):
		self.compList=compList
		self.generateName()

	def getCompList(self):
		return self.compList

	@property
	def target(self):
		return self

