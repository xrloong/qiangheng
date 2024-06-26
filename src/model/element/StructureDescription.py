#!/usr/bin/env python3
from typing import Optional

from tree.node import Node as TreeExpression
from tree.parser import TreeParser

from element.enum import FontVariance
from parser.model import StructureModel


class StructureDescription:
    def __init__(self, operator, compList, replacement: Optional[str]):
        self.__fontVariance = FontVariance.All

        if replacement:
            parts = replacement.split(".")
            name = parts[0]
            subIndex = int(parts[1]) if len(parts) > 1 else 0
            self.__reference = (name, subIndex)
        else:
            self.__reference = (None, 0)

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
    def reference(self):
        return self.__reference

    def updateFontVariance(self, fontVariance: FontVariance):
        self.__fontVariance = fontVariance

    def getUniqueName(self):
        return self.__name

    def isLeaf(self):
        return bool(self.reference[0])

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
