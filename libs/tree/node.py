#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Node: pass

class Node:
	def __init__(self, prop: dict = {}, children: tuple[Node] = ()):
		self.__prop = prop
		self.__children = tuple(children)

	@property
	def prop(self) -> dict:
		return self.__prop

	@property
	def children(self) -> tuple[str]:
		return self.__children
