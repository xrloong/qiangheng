#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Node:
    pass


class Node:
    def __init__(self, prop: dict = {}, children: tuple[Node] = (), backRefExp: str = None):
        self.__prop = prop
        self.__children = tuple(children)
        self.__backRefExp = backRefExp

    @staticmethod
    def genProp(name: str = None, operator: str = None) -> dict[str: str]:
        prop = {}
        if name: prop["置換"] = name
        if operator: prop["運算"] = operator
        return prop

    def __eq__(self, another):
        return (
            self.prop == another.prop
            and self.children == another.children
            and self.backRefExp == another.backRefExp
        )

    @property
    def prop(self) -> dict:
        return self.__prop

    @property
    def children(self) -> tuple[str]:
        return self.__children

    @property
    def backRefExp(self) -> str:
        return self.__backRefExp

    @property
    def isBackRef(self) -> bool:
        return self.backRefExp is not None

    @property
    def hasBackRef(self) -> bool:
        return self.backRefExp or any([node.hasBackRef for node in self.children])
