#!/usr/bin/env python3

from tree.parser import TreeParser

from element.enum import FontVariance
from parser.model import StructureModel

class StructureDescription:
	def __init__(self, operator, compList):
		self.__fontVariance = FontVariance.All

		self.__referenceExpression = None

		self.__flagIsRoot = False

		self.__operator = operator
		self.__compList = compList

	def __str__(self):
		return '<{0} = {1}|({2})>'.format(self.getReferenceExpression(), self.getOperator().getName(), ",".join(map(str, self.getCompList())))

	def __repr__(self):
		return str(self)

	def updateFontVariance(self, fontVariance: FontVariance):
		self.__fontVariance = fontVariance

	def getFontVariance(self):
		return self.__fontVariance

	def getUniqueName(self):
		return self.__name

	def generateName(self):
		if self.isLeaf():
			self.__name = self.getReferenceExpression()
		else:
			strList = [self.getOperator().getName()]
			strList.extend([comp.getUniqueName() for comp in self.__compList])
			self.__name = "({0})".format(" ".join(strList))

	def setReferenceExpression(self, referenceExpression):
		self.__referenceExpression = referenceExpression

	def getReferenceExpression(self):
		return self.__referenceExpression

	def getReferenceName(self):
		expression = self.__referenceExpression
		if expression:
			return expression.split(".")[0]
		else:
			return expression

	def isLeaf(self):
		return bool(self.getReferenceName())

	def isEmpty(self):
		return self.getOperator().getName() == '龜' or len(self.__compList) == 0

	def setOperator(self, operator):
		self.__operator = operator
		self.generateName()

	def getOperator(self):
		return self.__operator

	def setCompList(self, compList):
		self.__compList = compList
		self.generateName()

	def getCompList(self):
		return self.__compList

	@property
	def target(self):
		return self

class DecompositionDescription:
	def __init__(self, model: StructureModel):
		self.__node = TreeParser.parse(model.expression)
		self.__font = model.font

	@property
	def node(self):
		return self.__node

	@property
	def font(self):
		return self.__font

