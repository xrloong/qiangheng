#!/usr/bin/env python3

import sys
from gear import TreeRegExp

class TemplateDescription:
	"""樣本描述"""
	countAnonymousName=0
	def __init__(self, name, matchPattern, replacePattern):
		self.name=name

		self.matchPattern=matchPattern
		self.replacePattern=replacePattern
		self.tre=TreeRegExp.compile(matchPattern)

	def __str__(self):
		return '{0}({1})={2}'.format(self.name, self.matchPattern, self.replacePattern)

	def __repr__(self):
		return str(self)

	def getName(self):
		return self.name

