#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Node: pass

class Node:
    def __init__(self, structure = ('龜', ())):
        operator, nodes = (structure)
        self.__operator = operator
        self.__nodes = tuple(nodes)

    @staticmethod
    def generateLeaf(expression):
        return expression

    @property
    def operator(self) -> str:
        return self.__operator

    @property
    def nodes(self) -> tuple[str]:
        return self.__nodes
