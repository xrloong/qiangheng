#!/usr/bin/env python3

from tree.node import Node as TreeExpression
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

    @property
    def target(self):
        return self

    @property
    def operator(self):
        return self.__operator

    @property
    def compList(self):
        return self.__compList

    @property
    def fontVariance(self):
        return self.__fontVariance

    @property
    def referenceExpression(self):
        return self.__referenceExpression

    @property
    def referenceName(self):
        expression = self.__referenceExpression
        if expression:
            return expression.split(".")[0]
        else:
            return expression

    def updateFontVariance(self, fontVariance: FontVariance):
        self.__fontVariance = fontVariance

    def getUniqueName(self):
        return self.__name

    def setReferenceExpression(self, referenceExpression):
        self.__referenceExpression = referenceExpression

    def isLeaf(self):
        return bool(self.referenceName)

    def isEmpty(self):
        return self.operator.name == "龜" or len(self.__compList) == 0


class DecompositionDescription:
    def __init__(self, model: StructureModel):
        self.__node: TreeExpression = TreeParser.parse(model.expression)
        self.__font = model.font

    @property
    def node(self) -> TreeExpression:
        return self.__node

    @property
    def font(self):
        return self.__font
