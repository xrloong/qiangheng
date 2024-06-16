#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Node:
    pass


class Node:
    def __init__(self, prop: dict = {}, children: tuple[Node] = ()):
        self.__prop = prop
        self.__children = tuple(children)

    @staticmethod
    def genProp(operator: str = None) -> dict[str: str]:
        prop = {}
        if operator: prop["運算"] = operator
        return prop

    def __eq__(self, another):
        return self.prop == another.prop and self.children == another.children

    @property
    def prop(self) -> dict:
        return self.__prop

    @property
    def children(self) -> tuple[str]:
        return self.__children
