#!/usr/bin/env python3

from tree.parser import TreeParser

import Constant

from parser.enum import FontVariance
from parser.model import StructureModel

class StructureDescription:
	def __init__(self, operator, compList):
		self.fontVariance = FontVariance.All

		self.referenceExpression=None

		self.flagIsRoot=False

		self.operator=operator
		self.compList=compList

	def __str__(self):
		return '<{0}={1}|({2})>'.format(self.getReferenceExpression(), self.getOperator().getName(), ",".join(map(str, self.getCompList())))

	def __repr__(self):
		return str(self)

	def updateFontVariance(self, fontVariance: FontVariance):
		self.fontVariance = fontVariance

	def getFontVariance(self):
		return self.fontVariance

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

	def __convertDescriptionToFontVariance(self, description):
		if not description:
			return FontVariance.All
		elif description in Constant.LIST__FONT_VARIANCE__TRADITIONAL:
			return FontVariance.Traditional
		elif description in Constant.LIST__FONT_VARIANCE__SIMPLIFIED:
			return FontVariance.Simplified
		else:
			return FontVariance.All

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

